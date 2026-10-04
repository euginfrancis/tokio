# Scheduler component 2 — The Thread-Local Runtime Context (`runtime/context.rs`, `runtime/context/*.rs`)

> **One sentence:** a single `thread_local!` struct (`CONTEXT`) is how *code that has no handle* — `tokio::spawn`, `sleep`, `TcpStream::connect`, `Waker`s, `poll_proceed` — finds out **which runtime it is in, whether this thread is a scheduler thread, which task it is polling, how much budget is left and which RNG to use**.

It is the implicit "ambient state" of Tokio. Understanding it explains *"there is no reactor running"*, *"cannot start a runtime from within a runtime"*, *"can call blocking only when running on the multi-threaded runtime"* and why `Handle::enter()` guards must nest.

---

## 1. Where it lives

<!-- FILES:s_context -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/context.rs`](../../../tokio/src/runtime/context.rs) | 163 | 23 | 12 |
| [`tokio/src/runtime/context/blocking.rs`](../../../tokio/src/runtime/context/blocking.rs) | 94 | 13 | 6 |
| [`tokio/src/runtime/context/current.rs`](../../../tokio/src/runtime/context/current.rs) | 71 | 9 | 5 |
| [`tokio/src/runtime/context/runtime.rs`](../../../tokio/src/runtime/context/runtime.rs) | 73 | 11 | 4 |
| [`tokio/src/runtime/context/runtime_mt.rs`](../../../tokio/src/runtime/context/runtime_mt.rs) | 26 | 5 | 3 |
| [`tokio/src/runtime/context/scoped.rs`](../../../tokio/src/runtime/context/scoped.rs) | 44 | 3 | 4 |
| **Total (6 files)** | **471** | **64** | **34** |
<!-- /FILES -->

```
runtime/context.rs            the CONTEXT struct + small accessors (thread_rng_n, budget, thread_id, current_task_id, defer, with_scheduler …)
runtime/context/current.rs    "which runtime is current": HandleCell, SetCurrentGuard, with_current, try_set_current
runtime/context/scoped.rs     Scoped<T>: a scoped raw-pointer cell (used for the scheduler Context)
runtime/context/runtime.rs    EnterRuntime state, enter_runtime(), EnterRuntimeGuard
runtime/context/runtime_mt.rs current_enter_context(), exit_runtime()           (multi-thread only; used by block_in_place)
runtime/context/blocking.rs   BlockingRegionGuard (block_on parking), disallow_block_in_place
```

---

## 2. Data: the `CONTEXT`

```rust
struct Context {                                     // one per thread, const-initialised
    thread_id:       Cell<Option<ThreadId>>,         // lazily assigned process-unique id (runtime::ThreadId::next())
    current:         current::HandleCell,            // { handle: RefCell<Option<scheduler::Handle>>, depth: Cell<usize> }
    scheduler:       Scoped<scheduler::Context>,     // Cell<*const Context> — set ONLY while a scheduler runs on this thread
    current_task_id: Cell<Option<task::Id>>,
    runtime:         Cell<EnterRuntime>,             // NotEntered | Entered { allow_block_in_place: bool }
    rng:             Cell<Option<FastRand>>,         // thread-local xorshift for select!/steal/shard picking
    budget:          Cell<coop::Budget>,             // Option<u8>, starts Unconstrained (None)
    trace:           trace::Context,                 // task dumps (unstable, Linux)
}
```

| Field | Written by | Read by | Purpose |
|---|---|---|---|
| `current` | `Handle::enter`, `enter_runtime`, `try_set_current` (RAII `SetCurrentGuard`) | `with_current` ← `spawn`, `Sleep::new`, `Registration::new`, `TcpStream::connect`, `Handle::current` … | "ambient runtime". `depth` is a nesting counter so out-of-order guard drops are detected |
| `runtime` | `enter_runtime`, `exit_runtime`, `disallow_block_in_place` | `with_scheduler`, `block_in_place`, `block_on` | "is this thread inside a runtime?" — nested `block_on` is forbidden |
| `scheduler` | `context::set_scheduler(&cx, f)` in the worker `run()` and `CoreGuard::enter` | `with_scheduler` ← `schedule_task`, `defer`, `worker_index`, `block_in_place` | the **scheduler `Context`** (worker + core + defer list) — present only on scheduler threads |
| `current_task_id` | `TaskIdGuard` (task core) | `task::id()` | id of the task being polled |
| `rng` | `enter_runtime` (reseeds from the runtime's seed generator), `thread_rng_n` | `select!`, `shuffle` in blocking pool sharding | per-thread xorshift state; `enter_runtime` swaps in a *seeded* generator so `rng_seed` makes the runtime deterministic, and restores the old one on exit |
| `budget` | `coop::{budget, stop, set}`, `poll_proceed` | resources | cooperative-scheduling budget |
| `thread_id` | `thread_id()` (lazy) | `LocalSet` (owner-thread checks in `schedule`, `assert_called_from_owner_thread`) | process-unique `runtime::ThreadId`, assigned on first use |

All accessors use `CONTEXT.try_with(..)` (not `with`) wherever they can run during thread teardown; failure maps to `AccessError` → `TryCurrentError::ThreadLocalDestroyed`, "unconstrained budget", `None`, … — so dropping a `JoinHandle` or waking a task from a thread-local *destructor* never panics.

---

## 3. `Scoped<T>` — a scope-limited thread-local pointer

```rust
pub(super) struct Scoped<T> { inner: Cell<*const T> }
fn set<F,R>(&self, t: &T, f: F) -> R   // saves prev, stores &t, runs f, restores prev on drop (Reset guard — also on unwind)
fn with<F,R>(&self, f: F) -> R where F: FnOnce(Option<&T>) -> R    // f(Some(&*ptr)) if non-null else f(None)
```
This is what lets the *scheduler context live on the worker's stack* (no allocation, no `'static`) yet be reachable from deep inside user code: `Context::run` is invoked inside `context::set_scheduler(&cx, || cx.run(core))`; any `Waker::wake` on that thread can then call `with_scheduler` and obtain `&Context` to push into the local queue. After `f` returns, the pointer is restored (to null or to an outer scheduler) — the borrow checker can't see the dynamic extent, so the safety argument is "pointer is valid exactly while `set` is on the stack".

`with_scheduler` adds a second gate:
```rust
CONTEXT.try_with(|c| if matches!(c.runtime.get(), EnterRuntime::Entered { .. }) { c.scheduler.with(f) } else { f(None) })
```
A thread that is *not* inside `enter_runtime` never sees a scheduler context, even if a stale pointer existed.

---

## 4. `EnterRuntime` and the kinds of threads

```rust
pub(crate) enum EnterRuntime { Entered { allow_block_in_place: bool }, NotEntered }
```

| Thread kind | How it got there | `runtime` | `current` | `scheduler` (Scoped) | `block_in_place` |
|---|---|---|---|---|---|
| **Multi-thread worker** | worker `run()`: `enter_runtime(&handle, true, …)` then `set_scheduler(&cx, …)` | `Entered{true}` | handle | **MultiThread ctx** | allowed — hands the core to a new thread |
| **`Runtime::block_on` caller (multi-thread)** | `enter_runtime(handle, true, |b| b.block_on(f))` | `Entered{true}` | handle | `None` | allowed (`(Entered{allow}, no scheduler)` branch of `maybe_move_runtime`) |
| **`Runtime::block_on` caller (current-thread)** | `enter_runtime(handle, false, …)`; then `CoreGuard::enter` sets the scheduler | `Entered{false}` | handle | **CurrentThread ctx** | **panics** "can call blocking only when running on the multi-threaded runtime" |
| **Blocking-pool thread** | `spawn_thread`: `let _enter = rt.enter();` | `NotEntered` | handle | `None` | n/a (already a blocking thread) |
| **Any thread after `handle.enter()`** | `EnterGuard` | `NotEntered` | handle | `None` | n/a |
| **Plain thread** | – | `NotEntered` | `None` | `None` | – |

### `enter_runtime(handle, allow_block_in_place, f)`
```rust
let maybe_guard = CONTEXT.with(|c| {
    if c.runtime.get().is_entered() { None }                         // already inside a runtime ⇒ forbidden
    else {
        c.runtime.set(Entered { allow_block_in_place });
        let seed = handle.seed_generator().next_seed();              // deterministic if Builder::rng_seed was set
        let mut rng = c.rng.get().unwrap_or_else(FastRand::new);
        let old_seed = rng.replace_seed(seed);  c.rng.set(Some(rng));
        Some(EnterRuntimeGuard { blocking: BlockingRegionGuard::new(), handle: c.set_current(handle), old_seed })
    }
});
if let Some(mut guard) = maybe_guard { return f(&mut guard.blocking); }
panic!("Cannot start a runtime from within a runtime. … use `.await` on the future instead of blocking on it.");
```
`EnterRuntimeGuard::drop` asserts the state is still `Entered`, resets to `NotEntered` and restores the saved RNG seed. `BlockingRegionGuard` (`!Send`/`!Sync`) is the capability to park the thread: `block_on` (builds a `CachedParkThread` and polls the future in a loop under `coop::budget`) and `block_on_timeout`.

### `SetCurrentGuard` and nesting
`set_current(handle)` **replaces** the current handle (remembering the old one), increments `depth`, returns a guard recording its depth. On drop: if `depth` doesn't match (guards dropped out of order) it panics ("`EnterGuard` values dropped out of order … must be dropped in the reverse order as they were acquired") unless already panicking; otherwise restores the previous handle and decrements `depth`. This is why `Handle::enter()` guards are `!Send` (`PhantomData<SyncNotSend>`).

### `exit_runtime(f)` (multi-thread only)
Temporarily sets `runtime = NotEntered` around `f` (so `f` may call `block_on`/`Handle::block_on` again) and restores the previous state afterwards via a `Reset` guard (asserting `f` didn't "claim a permanent executor"). Used by `block_in_place`.

### `disallow_block_in_place()`
Flips `allow_block_in_place` to `false` and returns a guard that flips it back — held by `LocalSet` while it drives local tasks (`run_until`, `block_on`, the `LocalSet` future's poll), because `block_in_place` would hand the core to another thread and strand `!Send` tasks.

---

## 4b. Interface summary (all `pub(crate)`)

| Function | Returns | Used by |
|---|---|---|
| `with_current(f)` | `Result<R, TryCurrentError>` | `Handle::current`, `Handle::spawn` paths (`task::spawn`), `Sleep`, `Registration` |
| `try_set_current(&handle)` | `Option<SetCurrentGuard>` | `Handle::enter`, `Runtime::drop` (current-thread), `blocking pool threads` |
| `enter_runtime(handle, allow, f)` | `R` | `Runtime::block_on`, `Handle::block_on`, worker `run()` |
| `exit_runtime(f)`, `current_enter_context()` | `R` / `EnterRuntime` | `block_in_place` |
| `set_scheduler(&cx, f)` (private to `runtime`) | `R` | worker `run()`, `CoreGuard::enter` |
| `with_scheduler(f)` | `R` | `schedule_task`, `Handle::schedule` (current-thread), `defer`, `worker_index`, `unhandled_panic`, `Wake for Handle` |
| `defer(&Waker)` | – | `coop::register_waker`, `yield_now` |
| `budget(f)` | `Result<R, AccessError>` | `coop::*` |
| `thread_rng_n(n)` | `u32` | `select!`, blocking-pool sharding, work stealing (workers use their own `Core.rand` instead) |
| `thread_id()` | `Result<ThreadId, AccessError>` | `LocalSet`, metrics |
| `set_current_task_id(id)` / `current_task_id()` | `Option<Id>` | `TaskIdGuard`, `task::id()` |
| `disallow_block_in_place()` | guard | `LocalSet` (3 sites in `task/local.rs`) |
| `try_enter_blocking_region()` | `Option<BlockingRegionGuard>` | `future::block_on` (the `futures`-free `block_on` helper), `blocking::shutdown::Receiver::wait` (pool shutdown waits) |

---

## 5. Communication with other components

| Peer | Direction | What crosses the thread-local |
|---|---|---|
| [Runtime/Handle](./01-runtime-handle-builder.md) | Handle ↔ context | `scheduler::Handle` clone (current), via `enter`/`enter_runtime` |
| [Worker loop](./05-worker-loop.md) / [current-thread](./03-current-thread.md) | scheduler → context | `&scheduler::Context` via `set_scheduler`; reads it back in `schedule_task` |
| [Task core](../task/09-id-hooks-metadata.md), [harness](../task/04-harness.md) | `TaskIdGuard` ↔ context | `Option<Id>` |
| [Coop budget](../task/10-coop-budget.md) | coop ↔ context | `Cell<Budget>`, `defer(&Waker)` |
| [block_in_place](./11-block-in-place-and-defer.md) | scheduler ↔ context | `current_enter_context()`, `exit_runtime`, the worker `Context.core` |
| Resources (I/O, timers, sync) | resources → context | `with_current(|h| …)` to find the driver |

---

## 6. Invariants & gotchas

1. **A thread is in at most one runtime** (`runtime` is a flag, not a stack). `Handle::enter()` can nest *current-handle* scopes (stack with `depth`) without being "inside" the runtime.
2. **The scheduler pointer is only valid inside `set_scheduler`** — never stored beyond; `with_scheduler` is the only reader.
3. `schedule_task` distinguishes "a worker of **this** runtime holding a core" from everything else with `ptr_eq` on the handle: a task of runtime A woken on a worker of runtime B goes through A's *inject queue*.
4. `Handle::current()` outside any runtime panics with `"there is no reactor running, must be called from the context of a Tokio 1.x runtime"` (`CONTEXT_MISSING_ERROR`); inside a destroyed TLS: `THREAD_LOCAL_DESTROYED_ERROR`.
5. Context is **per OS thread, not per task** — across an `.await` the task may resume on another thread, whose context is that thread's own (the *runtime* is the same, the *budget* is fresh).
6. The `rng` swap in `enter_runtime` is what makes `Builder::rng_seed` produce reproducible `select!` branch orders in tests.

---

## 7. Tests

<!-- TESTS:s_context -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_common.rs`](../../../tokio/tests/rt_common.rs) | 49 | 1,050 |
| [`tokio/tests/rt_worker_index.rs`](../../../tokio/tests/rt_worker_index.rs) | 10 | 119 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/rt_handle.rs`, `rt_handle_block_on.rs` (enter/current/nesting), `rt_basic.rs`/`rt_threaded.rs` (nested `block_on` panics), `rt_common.rs`, `task_local*.rs`, `macros_select.rs` (rng seed determinism).

**Read next:** [03 — Current-thread scheduler](./03-current-thread.md).
