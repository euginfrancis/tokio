# Task component 10 — Cooperative Budgeting (`task/coop/`, `scheduler/defer.rs`, `context::{budget, defer}`)

> **One sentence:** Tokio cannot preempt a task, so it gives every poll a budget of **128 units**; budget-aware resources (sockets, channels, timers, join handles…) spend one unit per successful operation, and when the budget hits zero they return `Pending` **and ask the scheduler to wake the task later** — forcing a yield so one busy task can't starve the others.

It sits exactly on the **Task ↔ Scheduler boundary**: the *scheduler* installs the budget around each poll; the *resources* spend it; the *deferred-wake list* in the scheduler turns "out of budget" into "run me again after the others".

---

## 1. Where it lives

<!-- FILES:t_coop -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/task/coop/mod.rs`](../../../tokio/src/task/coop/mod.rs) | 258 | 252 | 26 |
| [`tokio/src/task/coop/consume_budget.rs`](../../../tokio/src/task/coop/consume_budget.rs) | 15 | 23 | 1 |
| [`tokio/src/task/coop/unconstrained.rs`](../../../tokio/src/task/coop/unconstrained.rs) | 34 | 6 | 3 |
| **Total (3 files)** | **307** | **281** | **30** |
<!-- /FILES -->

Plus `runtime/scheduler/defer.rs` (43 lines, the deferred-waker list) and `runtime/context.rs` (`budget()`, `defer()` accessors on the thread-local).

---

## 2. Data types (DTOs)

```rust
#[derive(Copy, Clone)] pub(crate) struct Budget(Option<u8>);       // Some(n) = n units left; None = unconstrained
impl Budget { const fn initial() -> Budget { Budget(Some(128)) }  pub(crate) const fn unconstrained() -> Budget { Budget(None) } }
pub(crate) struct BudgetDecrement { success: bool, hit_zero: bool }

#[must_use] pub struct RestoreOnPending(Cell<Budget>, PhantomData<*mut ()>);   // guard returned by poll_proceed (!Send)
//   made_progress(): keep the spent unit.   Drop without it: put the budget back (the op returned Pending → no charge)

pin_project! { pub struct Coop<F: Future> { #[pin] fut: F } }       // wrapper future: polls `fut` only after spending a unit
pub struct Unconstrained<F> { #[pin] inner: F }                      // wrapper future: polls `inner` with Budget::unconstrained()

// storage: thread-local CONTEXT.budget: Cell<Budget>
// deferred wakers: scheduler::Defer { deferred: RefCell<Vec<Waker>> }   (one per worker `Context` / current-thread `Context`)
```
One byte of state per thread (`Option<u8>`), no atomics, no allocation on the hot path.

---

## 3. Interface

| Function | Visibility | Role |
|---|---|---|
| `budget(f)` | `pub(crate)` | **Scheduler → budget**: set `Budget::initial()` (128), run `f`, restore the previous value via a `ResetGuard` (Drop) |
| `with_unconstrained(f)` | `pub(crate)` | run `f` with `Budget::unconstrained()` |
| `stop() -> Budget` | `pub(crate)` | set unconstrained and return the previous (used by `block_in_place` and blocking tasks) |
| `set(Budget)` | `pub(crate)` (multi-thread) | restore a previously saved budget (`block_in_place`'s `Reset` guard) |
| `has_budget_remaining() -> bool` | `pub` | `true` if `None` or `> 0`; `true` outside a runtime |
| **`poll_proceed(cx) -> Poll<RestoreOnPending>`** | `pub` — part of the public `tokio::task::coop` module, so third-party resources can be budget-aware too | **Resource → budget**: try to spend one unit |
| `poll_budget_available(cx) -> Poll<()>` | `pub(crate)` | check without spending (used by `select!`, `join!` loops) |
| `cooperative(fut) -> Coop<F>` | `pub` | wrap a future so that it spends a unit per poll |
| `consume_budget().await` | **public** `tokio::task::consume_budget` | user-callable: spend a unit; may yield; for long CPU loops that don't touch Tokio resources |
| `unconstrained(fut) -> Unconstrained<F>` | **public** `tokio::task::unconstrained` | opt a future out of budgeting (e.g. a latency-critical inner loop) |
| `Defer::{defer, wake, is_empty, take_deferred}` | `pub(crate)` | the deferred-waker list |
| `context::defer(waker)` | `pub(crate)` | route a waker to the current scheduler's `Defer`, or **wake immediately** if called outside a runtime |

---

## 4. The algorithm

### Spending: `poll_proceed`
```rust
pub fn poll_proceed(cx: &mut Context<'_>) -> Poll<RestoreOnPending> {
    context::budget(|cell| {
        let mut budget = cell.get();
        let decrement = budget.decrement();           // None → success; Some(0) → fail; Some(n>0) → n-1 (hit_zero if now 0)
        if decrement.success {
            let restore = RestoreOnPending::new(cell.get());    // remembers the budget BEFORE the decrement
            cell.set(budget);
            if decrement.hit_zero { inc_budget_forced_yield_count(); }   // unstable metric: budget_forced_yield_count
            Poll::Ready(restore)
        } else {
            register_waker(cx);                       // = context::defer(cx.waker())
            Poll::Pending
        }
    }).unwrap_or(Poll::Ready(RestoreOnPending::new(Budget::unconstrained())))   // TLS gone (thread teardown) → don't constrain
}
```

### The refund rule (`RestoreOnPending`)
A resource looks like:
```rust
let coop = ready!(coop::poll_proceed(cx));      // 1 unit spent (or return Pending: out of budget)
match try_operation() {
    Ready(v)  => { coop.made_progress(); Ready(v) }        // keep the charge
    Pending   => Pending                                   // `coop` dropped → the unit is RESTORED (no progress ⇒ no charge)
}
```
Only *successful* operations consume budget, so a task polling many idle resources isn't penalised.

### Installing: where the scheduler calls `coop::budget`
| Caller | Scope of one budget |
|---|---|
| multi-thread `Context::run_task` | **one** budget (128) for the polled task **and the whole LIFO-slot chain** that follows it; `has_budget_remaining()` is checked before each LIFO task |
| `current_thread` `Context::run_task` | one budget **per task** poll |
| `current_thread` `CoreGuard::block_on` | one budget per poll of the `block_on` future |
| `CachedParkThread::block_on` (multi-thread `Runtime::block_on`), `context/blocking.rs` | one per poll of the `block_on` future |
| `LocalSet` (`task/local.rs` `next_task` loop) | one per local task poll (`budget(|| task.run())`) |
| blocking tasks | `coop::stop()` — **no budget** (a blocking closure can't yield) |
| `timeout()` | polls its inner `Sleep` *unconstrained* if the wrapped future just exhausted the budget, so a busy future can't mask its own deadline (`timeout.rs`) |

### Exhaustion: forcing a yield
```
 budget == 0  →  poll_proceed: register_waker(cx) → context::defer(cx.waker()) → Context::defer (per-worker `Defer`)
                              → returns Pending      (the task returns Pending to the scheduler)
 scheduler:  task returns → run_task finishes → …
             worker loop:  `if !self.defer.is_empty() { park_yield } else { park }`
             park_internal: …driver polled with zero timeout… then `self.defer.wake()`  → each deferred waker.wake() → task re-queued
```
- The task is **not** woken immediately: that would just put it back on the queue it is about to leave, possibly in the LIFO slot. Deferring the wake until *after* the scheduler has looked at its queues and driven the I/O/timer drivers makes the yield real: other ready tasks and fresh I/O events run first.
- `Defer::defer` skips a waker identical to the **last** one queued (`will_wake`), so a task exhausting its budget on many resources in one poll is queued once.
- Outside a scheduler context (e.g. a future polled by a foreign executor), `context::defer` falls back to `wake_by_ref()` immediately.
- `current_thread`'s `has_pending_work` also counts `!defer.is_empty()` so the thread won't sleep in the driver while yielded tasks exist.

### What `yield_now()` does with the same machinery
`yield_now` is the explicit version: first poll calls `context::defer(cx.waker())` and returns `Pending`; the next poll returns `Ready`.

---

## 5. Which resources spend budget (verified by search)

| Spend via `poll_proceed` directly | Spend via `cooperative(...)` wrapper |
|---|---|
| `JoinHandle::poll`; I/O `Registration::{poll_ready, poll_io, async_io}` (all socket reads/writes/accept/connect); `mpsc::chan::Rx::recv`/`recv_many`; `oneshot::Receiver` poll; `batch_semaphore::Acquire` (⇒ `Mutex`, `RwLock`, `Semaphore`, mpsc **send**); `time::Sleep` (⇒ `timeout`, `interval`); `io::copy`, `copy_buf`, `empty`, `repeat`, `sink`, `duplex`; `process::Child` waits | `broadcast::Receiver::recv`; `watch::Receiver::{changed, wait_for}` and related; `spawn_blocking`'s stub when the runtime is disabled; `consume_budget` |

**Not budgeted** (verified: no `poll_proceed`/`cooperative` call in the file): `Notify::notified`, plain `std` futures, user `async` code that never awaits a Tokio resource. A loop around those can monopolise a worker; use `task::yield_now()` or `task::consume_budget()` inside it.

(The test `coop_budget.rs` checks that each public async API consumes/restores budget as documented.)

---

## 6. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| [Scheduler](../scheduler/05-worker-loop.md) `run_task` / `park_internal` | scheduler → coop | `budget(|| task.run())`; `Defer::wake()` after parking; `has_budget_remaining()` for the LIFO loop |
| Resources (I/O, sync, time, join) | resource → coop | `poll_proceed(cx)` → `RestoreOnPending`; `register_waker(cx)` on exhaustion |
| Runtime context | coop ↔ TLS | `CONTEXT.budget: Cell<Budget>`, `scheduler.defer(&Waker)` |
| [Waker](./06-waker.md) | coop → | `cx.waker().clone()` stored in `Defer` (one ref-count) |
| `block_in_place` | scheduler ↔ coop | `coop::stop()` before running the blocking closure; `coop::set(saved)` after |
| Metrics | coop → | `budget_forced_yield_count` (unstable) |
| User code | user → coop | `consume_budget`, `unconstrained`, `has_budget_remaining` |

---

## 7. Invariants & gotchas

1. The budget is **per thread, per poll**: `budget()` saves/restores, so nested polls (e.g. `block_on` inside `LocalSet`) get their own 128.
2. Resources must call `made_progress()` **iff** they made progress; forgetting leads to *refunds that never happen* (lost budget) and calling it too eagerly lets a task spin without yielding.
3. `RestoreOnPending` is `!Send` (raw-pointer `PhantomData`): it must be held across no `.await`.
4. After exhaustion, *every* budgeted resource in that poll returns `Pending` until the scheduler re-polls the task with a fresh budget.
5. Budget exhaustion changes **fairness, not correctness**: results are the same, only the interleaving differs.
6. `budget_forced_yield_count` (unstable metric) counts how often a task hit zero — a handy signal for "this task is hogging".

---

## 8. Tests

<!-- TESTS:t_coop -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/coop_budget.rs`](../../../tokio/tests/coop_budget.rs) | 2 | 54 |
| [`tokio/tests/task_yield_now.rs`](../../../tokio/tests/task_yield_now.rs) | 2 | 27 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/coop_budget.rs` (exhaustion/refund for each resource), `task_yield_now.rs`, `rt_*` (LIFO + budget interaction), the inline `budgeting` test in `task/coop/mod.rs`.

**Next:** the Task side is complete. The **Scheduler** components start at [../scheduler/01-runtime-handle-builder.md](../scheduler/01-runtime-handle-builder.md).
