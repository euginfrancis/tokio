# Block 1 — Tasks

> **Role:** turns a `Future` into an independently scheduled **task**, and gives you handles to wait for it, cancel it, group it and give it local state.
> In the [component diagram](./README.md): the "tasks" API box (`spawn`, `JoinHandle`, `JoinSet`, `spawn_blocking`) — plus the **task core** (`runtime/task/`) that every scheduler uses to store and poll tasks.

---

## 1. At a glance

<!-- STATS:tasks -->
| Metric | Value |
|---|---|
| Source files | 26 |
| Code lines | 4,386 (8.7% of `tokio/src`) |
| Doc + comment lines | 4,009 (0.91 per code line) |
| Functions | 401 — public API 75, trait impls 65, internal 249, inline tests 7 |
| `async fn` / `unsafe fn` | 7 / 48 |
| `unsafe` occurrences | 170 |
| Integration tests (`tokio/tests`) | 14 files, 130 test fns, 3,604 code lines |
<!-- /STATS -->

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | Task memory (one allocation per task), the task **state machine** (running/notified/complete/cancelled + ref-count in one atomic word), polling a task safely (panic catching), wakers that point at tasks, `JoinHandle`/`AbortHandle`/`JoinError`, the list of all tasks per runtime (`OwnedTasks`), `JoinSet`, `LocalSet`/`spawn_local`, `task_local!`, `yield_now`, coop budgeting, task ids. |
| **Does not own** | Choosing which task to run next or on which thread ([Scheduler](./06-scheduler.md)); running blocking closures ([Blocking pool](./09-blocking-pool.md)) — `spawn_blocking` is only a front door here. |
| **Input** | A future (`spawn`, `JoinSet::spawn`, `spawn_local`), or a closure (`spawn_blocking`). |
| **Output** | A `Notified` handle given to the scheduler via the `Schedule` trait; a `JoinHandle<T>` given to the user. |
| **Boundary types** | `trait Schedule { release, schedule, hooks, yield_now, unhandled_panic }` — the *only* thing the task core knows about schedulers. `RawTask` (type-erased pointer) — the only thing schedulers know about tasks. |

---

## 3. Files

<!-- FILES:tasks -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/task/local.rs`](../../tokio/src/task/local.rs) | 580 | 651 | 13.2% |
| [`tokio/src/runtime/task/state.rs`](../../tokio/src/runtime/task/state.rs) | 399 | 157 | 9.1% |
| [`tokio/src/runtime/task/mod.rs`](../../tokio/src/runtime/task/mod.rs) | 348 | 259 | 7.9% |
| [`tokio/src/runtime/task/core.rs`](../../tokio/src/runtime/task/core.rs) | 331 | 203 | 7.5% |
| [`tokio/src/runtime/task/harness.rs`](../../tokio/src/runtime/task/harness.rs) | 318 | 186 | 7.3% |
| [`tokio/src/task/join_set.rs`](../../tokio/src/task/join_set.rs) | 312 | 489 | 7.1% |
| [`tokio/src/runtime/task/trace/mod.rs`](../../tokio/src/runtime/task/trace/mod.rs) | 270 | 135 | 6.2% |
| [`tokio/src/task/coop/mod.rs`](../../tokio/src/task/coop/mod.rs) | 258 | 252 | 5.9% |
| [`tokio/src/runtime/task/list.rs`](../../tokio/src/runtime/task/list.rs) | 253 | 70 | 5.8% |
| [`tokio/src/runtime/task/raw.rs`](../../tokio/src/runtime/task/raw.rs) | 252 | 72 | 5.7% |
| [`tokio/src/task/task_local.rs`](../../tokio/src/task/task_local.rs) | 241 | 209 | 5.5% |
| [`tokio/src/task/builder.rs`](../../tokio/src/task/builder.rs) | 118 | 107 | 2.7% |
| [`tokio/src/runtime/task/error.rs`](../../tokio/src/runtime/task/error.rs) | 99 | 80 | 2.3% |
| [`tokio/src/runtime/task/trace/tree.rs`](../../tokio/src/runtime/task/trace/tree.rs) | 92 | 15 | 2.1% |
| [`tokio/src/runtime/task/waker.rs`](../../tokio/src/runtime/task/waker.rs) | 88 | 22 | 2.0% |
| [`tokio/src/runtime/task/join.rs`](../../tokio/src/runtime/task/join.rs) | 79 | 278 | 1.8% |
| [`tokio/src/runtime/task/trace/symbol.rs`](../../tokio/src/runtime/task/trace/symbol.rs) | 71 | 13 | 1.6% |
| [`tokio/src/task/spawn.rs`](../../tokio/src/task/spawn.rs) | 46 | 165 | 1.0% |
| [`tokio/src/runtime/task/abort.rs`](../../tokio/src/runtime/task/abort.rs) | 44 | 51 | 1.0% |
| [`tokio/src/task/mod.rs`](../../tokio/src/task/mod.rs) | 44 | 277 | 1.0% |
| [`tokio/src/runtime/task/id.rs`](../../tokio/src/runtime/task/id.rs) | 38 | 43 | 0.9% |
| [`tokio/src/task/coop/unconstrained.rs`](../../tokio/src/task/coop/unconstrained.rs) | 34 | 6 | 0.8% |
| [`tokio/src/task/blocking.rs`](../../tokio/src/task/blocking.rs) | 20 | 205 | 0.5% |
| [`tokio/src/runtime/task/trace/trace_impl.rs`](../../tokio/src/runtime/task/trace/trace_impl.rs) | 19 | 4 | 0.4% |
| [`tokio/src/task/yield_now.rs`](../../tokio/src/task/yield_now.rs) | 17 | 37 | 0.4% |
| [`tokio/src/task/coop/consume_budget.rs`](../../tokio/src/task/coop/consume_budget.rs) | 15 | 23 | 0.3% |
| **Total (26 files)** | **4,386** | **4,009** | 100% |
<!-- /FILES -->

```
task/                       PUBLIC API
├── spawn.rs                tokio::spawn
├── blocking.rs             spawn_blocking, block_in_place (front doors)
├── join_set.rs             JoinSet
├── local.rs                LocalSet, spawn_local (≈ its own mini scheduler)
├── task_local.rs           task_local! / LocalKey
├── yield_now.rs, builder.rs
└── coop/                   cooperative budget (128 units per poll)
runtime/task/               TASK CORE (used by every scheduler)
├── mod.rs                  Task / Notified / LocalNotified / UnownedTask, Schedule trait, new_task
├── core.rs                 Cell { Header | Core | Trailer } memory layout
├── state.rs                the atomic state word and all transitions
├── raw.rs                  RawTask + Vtable (type erasure)
├── harness.rs              poll / complete / cancel / wake / dealloc
├── waker.rs                RawWakerVTable for task wakers
├── join.rs, abort.rs, error.rs   JoinHandle, AbortHandle, JoinError
├── list.rs                 OwnedTasks (sharded) / LocalOwnedTasks
├── id.rs                   task::Id
└── trace/                  task dumps (unstable)
```

---

## 4. Data structures

### The task allocation (`runtime/task/core.rs`)
```rust
#[repr(C)]
pub(super) struct Cell<T: Future, S> {   // ONE heap allocation per task
    header: Header,                      // hot, type-independent: read by schedulers and wakers
    core: Core<T, S>,                    // the future / its output
    trailer: Trailer,                    // cold: list links, JoinHandle waker
}
pub(crate) struct Header {
    state: State,                                    // AtomicUsize: flags + ref-count
    queue_next: UnsafeCell<Option<NonNull<Header>>>, // intrusive link for the inject queue
    vtable: &'static Vtable,                         // poll / schedule / dealloc / … for this T,S
    owner_id: UnsafeCell<Option<NonZeroU64>>,        // which OwnedTasks list it belongs to
    tracing_id, scheduled_at, …
}
pub(super) struct Core<T: Future, S> {
    scheduler: S,                        // Arc<Handle> of the runtime — how the task reschedules itself
    task_id: Id,
    spawned_at: &'static Location<'static>,
    stage: CoreStage<T>,                 // UnsafeCell<Stage<T>>
}
pub(super) enum Stage<T: Future> { Running(T), Finished(Result<T::Output, JoinError>), Consumed }
pub(super) struct Trailer {
    owned: linked_list::Pointers<Header>,   // links in OwnedTasks
    waker: UnsafeCell<Option<Waker>>,       // JoinHandle's waker
    hooks: TaskHarnessScheduleHooks,        // on_task_terminate
}
```

### The state word (`runtime/task/state.rs`)
```
bit 0 RUNNING   bit 1 COMPLETE   bit 2 NOTIFIED   bit 3 JOIN_INTEREST   bit 4 JOIN_WAKER   bit 5 CANCELLED   bits 6.. REF_COUNT
INITIAL_STATE = 3 refs | JOIN_INTEREST | NOTIFIED      // refs: OwnedTasks, Notified, JoinHandle
```

### Handles — all just a pointer to the same allocation
| Type | Who holds it | Meaning |
|---|---|---|
| `RawTask` (`NonNull<Header>`) | everything | Untyped pointer; calls go through the vtable |
| `Task<S>` | `OwnedTasks` list | "This runtime owns the task" (1 ref) |
| `Notified<S>` | run queues | "This task is scheduled; whoever pops it may poll it" (1 ref) |
| `LocalNotified<S>` | worker while polling | `!Send` proof that the current thread may poll |
| `UnownedTask<S>` | blocking pool | Task not in any `OwnedTasks` (2 refs) |
| `JoinHandle<T>` | user | Read output / abort (1 ref while held) |
| `AbortHandle` | user | Abort only |
| `Waker` | resources (sockets, timers, channels) | Any number; each clone = 1 ref |

### `Vtable` (`raw.rs`)
`poll, schedule, dealloc, try_read_output, drop_join_handle_slow, drop_abort_handle, shutdown` + `trailer_offset, scheduler_offset, id_offset` — one static vtable per `(T, S)` pair, generated by `RawTask::new::<T, S>`.

### Collections
```rust
pub(crate) struct OwnedTasks<S> {        // list.rs — every live task of a runtime
    list: ShardedList<Task<S>>,          // N mutex-protected intrusive lists, shard = hash(id)
    id: NonZeroU64,                      // checked by assert_owner()
    closed: AtomicBool,                  // set at shutdown: bind() then refuses new tasks
}
pub struct JoinSet<T> { inner: IdleNotifiedSet<JoinHandle<T>> }   // two intrusive lists: idle / notified
pub struct LocalSet { tick: Cell<u8>, context: Rc<Context>, _not_send }
struct Shared {                          // LocalSet internals
    local_state: LocalState { owner: ThreadId, local_queue: VecDeque<Notified>, owned: LocalOwnedTasks },
    queue: Mutex<Option<VecDeque<Notified>>>,   // tasks woken from OTHER threads
    waker: AtomicWaker,                          // wakes the task that drives the LocalSet
}
```

### Errors, ids, locals, budget
```rust
pub struct JoinError { repr: Repr, id: Id }   enum Repr { Cancelled, Panic(Box<dyn Any + Send>) }
pub struct Id(NonZeroU64);                     // from a global AtomicU64 counter
pub struct LocalKey<T> { inner: thread::LocalKey<RefCell<Option<T>>> }   // swapped in/out around each poll
pub(crate) struct Budget(Option<u8>);          // Some(128) per poll; None = unconstrained
```

---

## 5. How it interacts with the other blocks

```
 user ──spawn(fut)──▶ spawn_inner ──▶ [Scheduler] Handle::spawn ──▶ OwnedTasks::bind ──▶ new_task (allocate Cell)
                                                        │                                   │
                                                        ▼                                   ▼
                                          schedule(Notified) ◀──────────────── returns (Task, Notified, JoinHandle)
 [Scheduler] pops Notified ──▶ task.run() ──▶ vtable.poll ──▶ Harness::poll ──▶ future.poll(cx with task Waker)
                                                                                     │ Pending: waker stored in
                                                                                     ▼ [I/O drv] / [Timer drv] / [Sync]
 resource fires ──▶ Waker::wake ──▶ Harness::wake_by_val ──▶ state NOTIFIED ──▶ vtable.schedule ──▶ [Scheduler]
 future Ready ──▶ Harness::complete ──▶ store output, wake JoinHandle ──▶ Schedule::release (remove from OwnedTasks)
 user ──JoinHandle.await──▶ try_read_output (or store waker)          user ──abort()──▶ remote_abort ──▶ schedule
 spawn_blocking(f) ──▶ [Blocking pool] (wraps f in a BlockingTask future + UnownedTask)
```

| Other block | Direction | Through |
|---|---|---|
| Scheduler | ↔ | `Schedule` trait (task → scheduler), `RawTask`/`Notified::run` (scheduler → task), `OwnedTasks` |
| Blocking pool | → | `spawn_blocking`, `block_in_place` |
| I/O & timer drivers, Sync | ← | They hold task `Waker`s and call `wake()` |
| All resources | ← | `coop::poll_proceed` reads the budget this block sets per poll |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `spawn`, `spawn_inner` | `task/spawn.rs` | Assign an `Id`, find the current runtime, hand the future to it |
| `JoinSet::spawn / join_next / abort_all / shutdown / try_join_next` | `task/join_set.rs` | Manage a group; results in completion order |
| `LocalSet::new / spawn_local / run_until / block_on`, `spawn_local` | `task/local.rs` | Run `!Send` futures on one thread |
| `yield_now` | `task/yield_now.rs` | Defer own waker, return `Pending` once |
| `coop::budget / poll_proceed / consume_budget / unconstrained` | `task/coop/mod.rs` | Cooperative scheduling budget |
| `task_local! / LocalKey::scope / with / get` | `task/task_local.rs` | Task-local values |
| `id() / try_id()` | `runtime/task/id.rs` | Current task id |
| `new_task`, `RawTask::new` | `runtime/task/mod.rs`, `raw.rs` | Allocate the `Cell` and its vtable |
| `OwnedTasks::bind / remove / assert_owner / close_and_shutdown_all` | `runtime/task/list.rs` | Track all tasks, refuse after close |
| `Harness::poll / poll_inner / complete / shutdown / dealloc / wake_by_val / wake_by_ref / remote_abort` | `runtime/task/harness.rs` | Task lifecycle |
| `poll_future`, `cancel_task` | `harness.rs` | `catch_unwind` around `poll`; drop future on cancel |
| `State::transition_to_running / _idle / _complete / _notified_by_val / _notified_and_cancel / ref_inc / ref_dec` | `runtime/task/state.rs` | CAS state transitions |
| `clone_waker / wake_by_val / wake_by_ref / drop_waker` | `runtime/task/waker.rs` | Task wakers |
| `JoinHandle::poll / abort / is_finished / abort_handle`, `JoinError::is_panic / into_panic` | `join.rs`, `error.rs` | User-facing handles |

---

## 7. Flows

**Life of a task:** `spawn` → `Cell` allocated with refs = 3 and `NOTIFIED` → bound to `OwnedTasks` (shard lock; rejected if closed) → `Notified` scheduled → worker polls: `NOTIFIED→RUNNING` → `poll_future` (catch panics) → `Pending`: `RUNNING→idle` (if woken meanwhile → `yield_now` reschedule) / `Ready`: store output, `COMPLETE`, wake `JoinHandle` → `release` from `OwnedTasks` → last ref → `dealloc`.

**Cancellation:** `abort()` sets `CANCELLED|NOTIFIED` and schedules the task → next `transition_to_running` sees `CANCELLED` → `cancel_task` drops the future, stores `JoinError::Cancelled` → complete. Runtime shutdown does the same via `shutdown()` on every owned task.

**`JoinSet::join_next`:** each spawned task's `JoinHandle` is an entry; the entry's waker moves it from the *idle* list to the *notified* list; `join_next` polls only notified entries — O(1) to find a finished task among thousands.

**`LocalSet`:** a future that, when polled, runs its own queue of `!Send` tasks (local queue for same-thread wakes, mutex queue for cross-thread wakes), up to a budget per poll, then yields back to the outer runtime.

---

## 8. Invariants & gotchas

- `spawn` requires `Send + 'static` because the task may migrate between workers between polls and outlive the caller.
- The `RUNNING` bit is a **lock** on the `Stage`: only the thread that set it may touch the future.
- Every handle type owns exactly one ref-count (`Unowned` owns two); the last `ref_dec` deallocates.
- Dropping a `JoinHandle` **detaches**; dropping a `JoinSet` **aborts** all its tasks.
- A panic inside a task becomes `JoinError::Panic` — unless the runtime's `unhandled_panic = ShutdownRuntime` (unstable).
- Non-`Send` tasks are aborted *by scheduling* (`remote_abort`) so the future is dropped on its own thread.
- `task_local!` values are only visible inside `LocalKey::scope` — not inherited by `spawn`ed children.

---

## 9. Tests & where to start

<!-- TESTS:tasks -->
**14 integration test files · 130 test functions · 3,604 code lines**

[`async_send_sync.rs`](../../tokio/tests/async_send_sync.rs), [`coop_budget.rs`](../../tokio/tests/coop_budget.rs), [`task_abort.rs`](../../tokio/tests/task_abort.rs), [`task_blocking.rs`](../../tokio/tests/task_blocking.rs), [`task_builder.rs`](../../tokio/tests/task_builder.rs), [`task_emscripten.rs`](../../tokio/tests/task_emscripten.rs), [`task_hooks.rs`](../../tokio/tests/task_hooks.rs), [`task_id.rs`](../../tokio/tests/task_id.rs), [`task_join_set.rs`](../../tokio/tests/task_join_set.rs), [`task_local.rs`](../../tokio/tests/task_local.rs), [`task_local_set.rs`](../../tokio/tests/task_local_set.rs), [`task_panic.rs`](../../tokio/tests/task_panic.rs), [`task_trace_self.rs`](../../tokio/tests/task_trace_self.rs), [`task_yield_now.rs`](../../tokio/tests/task_yield_now.rs)
<!-- /TESTS -->

**Read in this order:** `runtime/task/mod.rs` (module docs explain every handle and field) → `state.rs` → `harness.rs` → `task/spawn.rs` → `join_set.rs` → `local.rs`.
**Contribution areas seen in history:** `JoinSet`/`LocalSet` API additions and docs, `spawn_local` behavior, coop budgeting in more places, task hooks and ids.
