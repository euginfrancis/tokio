# Interfaces and data-transfer objects of the Task + Scheduler core

This is the **contract catalogue**: every trait/vtable that lets the layers talk to each other, and every value that is *passed between* them (the DTOs).
Nothing here owns long-lived state — those are the structures documented in the per-component pages; this page is about **what crosses a boundary**.

Legend: 🔒 = `pub(crate)`/private, 🌐 = public API of the `tokio` crate (possibly `tokio_unstable`).

---

## 1. Interfaces (traits and vtables)

### 1.1 `task::Schedule` — the **task → scheduler** contract  🔒
`runtime/task/mod.rs:306`

```rust
pub(crate) trait Schedule: Sync + Sized + 'static {
    fn release(&self, task: &Task<Self>) -> Option<Task<Self>>;   // task finished: give back the OwnedTasks ref (or None if already removed)
    fn schedule(&self, task: Notified<Self>);                      // "this task is runnable" — the ONE way work enters a scheduler
    fn hooks(&self) -> TaskHarnessScheduleHooks;                   // { task_terminate_callback: Option<TaskCallback> }
    fn yield_now(&self, task: Notified<Self>) { self.schedule(task) }   // default: same as schedule; overridden by the MT scheduler to push to the back
    fn unhandled_panic(&self) {}                                   // default: nothing (1.0 behaviour); overridden by current-thread / LocalSet
}
```

Direction: **called by the task module** (Harness/Waker/spawn), **implemented by schedulers**. It is the only compile-time coupling from `task` to schedulers (generic parameter `S`), and it is why a task never needs to know what a "worker" is.

| Implementor | Where | `schedule` does |
|---|---|---|
| `Arc<multi_thread::Handle>` | `multi_thread/worker.rs` | `Handle::schedule_task(task, false)`: local LIFO/ring or inject queue (see [sched/05](./scheduler/05-worker-loop.md)) |
| `Arc<current_thread::Handle>` | `current_thread/mod.rs` | local queue if on the owning thread else `inject.push` + wake driver ([sched/03](./scheduler/03-current-thread.md)) |
| `Arc<local::Shared>` (LocalSet) | `task/local.rs` | local queue / remote queue of the `LocalSet` |
| `BlockingSchedule` | `blocking/schedule.rs` | does nothing — blocking "tasks" are never rescheduled |
| noop test scheduler | `runtime/tests/mod.rs` | – |

### 1.2 `task::Vtable` (`RawTask`) — the **type-erasure** contract  🔒
`runtime/task/raw.rs`. A hand-written per-`(Future, Schedule)` table of `unsafe fn(NonNull<Header>)` pointers:
`poll`, `schedule`, `dealloc`, `try_read_output`, `drop_join_handle_slow`, `drop_abort_handle`, `shutdown`, plus three (four with `tokio_unstable`) const-computed byte offsets: `trailer_offset`, `scheduler_offset`, `id_offset`, `spawn_location_offset`.
Direction: **everything that holds only a `NonNull<Header>`** (queues, `OwnedTasks`, `JoinHandle`, `Waker`) calls into the concrete `Harness<T,S>` through it. Details: [task/03](./task/03-rawtask-vtable.md).

### 1.3 `Waker` vtable (std `RawWakerVTable`)  🌐
`runtime/task/waker.rs` builds `RawWakerVTable{clone, wake, wake_by_ref, drop}` whose data pointer is the task `Header`. This is the **future → task** contract (std's `Context::waker()`), and the entry into `Schedule::schedule`.
Details: [task/06](./task/06-waker.md).

### 1.4 `multi_thread::Overflow<T>` — **local queue → inject queue**  🔒
`multi_thread/overflow.rs`

```rust
pub(crate) trait Overflow<T: 'static> {
    fn push(&self, task: task::Notified<T>);
    fn push_batch<I: Iterator<Item = task::Notified<T>>>(&self, iter: I);
}
```
Implemented by `Handle` (→ `push_remote_task`/`inject.push_batch`) and, for the queue unit tests, by `RefCell<Vec<Notified<T>>>`. It lets `queue::Local` (a leaf data structure) spill without depending on `Handle`. Details: [sched/06](./scheduler/06-local-queue.md).

### 1.5 `linked_list::Link` — **intrusive list ↔ element**  🔒
`util/linked_list.rs`: `unsafe trait Link { type Handle; type Target; as_raw, from_raw, pointers }`. Implemented by `task::Task<S>` (the `Pointers<Header>` live in the task's **`Trailer.owned`** field) for `OwnedTasks`; `ShardedListItem` picks the shard from the task id. The inject queue does **not** use it; it uses `Header.queue_next` directly through `RawTask::{get,set}_queue_next`.

### 1.4b Driver contract  🔒
`driver::Driver { park, park_timeout, shutdown }` + `driver::Handle { unpark, io(), time(), clock() }` — **scheduler/parker → event sources** ([sched/13](./scheduler/13-driver-interface.md)).

### 1.6 `scheduler::Handle` / `scheduler::Context` enums — **runtime → scheduler dispatch**  🔒
`runtime/scheduler/mod.rs`:

```rust
pub(crate) enum Handle  { CurrentThread(Arc<current_thread::Handle>), MultiThread(Arc<multi_thread::Handle>), Disabled }
pub(crate) enum Context { CurrentThread(current_thread::Context),    MultiThread(multi_thread::Context) }
```
`match_flavor!` macro forwards methods (`spawn`, `driver()`, `blocking_spawner()`, `hooks()`, `defer()`, `worker_index()`, metrics accessors…). This enum dispatch (instead of `dyn Trait`) gives monomorphic, inlinable calls.

### 1.7 Public hooks 🌐
`Builder::on_thread_start/stop/park/unpark`, `on_task_spawn/terminate` (`TaskCallback`), unstable `on_before_task_poll/on_after_task_poll`. Stored in `Config`, forwarded to workers/tasks via `TaskHarnessScheduleHooks` and `task_hooks::TaskHooks`. See [task/09](./task/09-id-hooks-metadata.md).

---

## 2. Data-transfer objects (values that cross boundaries)

### 2.1 The task handles — *ownership tokens* (all are 1 pointer wide, `NonNull<Header>` inside)

| Type | Meaning | Ref-count it owns | Crosses |
|---|---|---|---|
| `Task<S>` | "the right to the OwnedTasks list slot / to release the task" | 1 | `spawn` → `OwnedTasks`; `Schedule::release` |
| `Notified<S>` | "the right to **schedule** this task once" (the NOTIFIED bit ↔ exactly one `Notified` exists) | 1 | Waker/spawn → `Schedule::schedule` → queues → worker |
| `LocalNotified<S>` | `Notified` proven to belong to *this* `OwnedTasks`/thread; allowed to `run()` | 1 (it *is* the `Notified`, re-typed) | `assert_owner` → `run_task` |
| `UnownedTask<S>` | task that is not in an `OwnedTasks` (blocking pool, `spawn_local` w/o owner) | 2 | blocking pool |
| `JoinHandle<T>` 🌐 | read the output / `abort` | 1 | user ← `spawn` |
| `AbortHandle` 🌐 | abort only | 1 | user |
| `RawTask` | untyped pointer + vtable access | 0 (borrowed view) | inside queues & lists |
| `Waker` 🌐 | "make this task runnable" | 1 | future ← poll `Context` |

The rule "**one handle = one ref-count unit, moved not copied**" is the ledger in [task/01](./task/01-state-word.md) §ref-count. `Notified` carrying its ref through `into_raw()`/`from_raw()` is what allows queues to be intrusive and allocation-free.

### 2.2 Per-task data in the heap cell (`Cell<T,S>`: `Header | Core | Trailer`)

| Part | DTO fields | Read by |
|---|---|---|
| `Header` | `state: State(AtomicUsize)`, `queue_next`, `vtable`, `owner_id`, (`tracing_id`), `scheduled_at` | everything via `RawTask` |
| `Core<T,S>` | `scheduler: S`, `task_id`, `spawned_at` (unstable), `stage: CoreStage<T>` wrapping `Stage` = `Running(Future)` \| `Finished(Result<Output, JoinError>)` \| `Consumed` | Harness (poll / output) |
| `Trailer` | `owned: Pointers<Header>` (OwnedTasks links), `waker: UnsafeCell<Option<Waker>>` (the JoinHandle's waker), `hooks: TaskHarnessScheduleHooks` | join / complete / owned list |

### 2.3 Poll/transition results (small enums returned by the state machine)

| Enum | Variants | Producer → Consumer |
|---|---|---|
| `TransitionToRunning` | `Success`, `Cancelled`, `Failed`, `Dealloc` | `State` → `Harness::poll` |
| `TransitionToIdle` | `Ok`, `OkNotified`, `OkDealloc`, `Cancelled` | `State` → `Harness::poll` |
| `TransitionToNotifiedByVal` / `ByRef` | `DoNothing`, `Submit`, (`Dealloc` – by-val only) | `State` → `Waker` wake paths |
| `TransitionToJoinHandleDrop` | `{ drop_waker, drop_output }` | `State` → `Harness::drop_join_handle_slow` |
| `PollFuture` | `Complete`, `Notified`, `Done`, `Dealloc` | `Harness::poll_future` → `poll` |
| `Snapshot` (usize newtype) | bit-field view of the state word | `State` internals |
| `Result<T, JoinError>` (`JoinError` = cancelled / panic with `Id`) | stored in `Stage::Finished` | Harness → `JoinHandle` |

### 2.4 Scheduler-side DTOs

| DTO | Fields | Flow |
|---|---|---|
| `Config` (`runtime/config.rs`) | `global_queue_interval`, `event_interval`, `before_park`, `after_unpark`, `before_spawn`, `after_termination`, (`before_poll`,`after_poll`), `disable_lifo_slot`, `seed_generator`, `metrics_*_histogram`, `track_task_schedule_latency`, `unhandled_panic`, `enable_eager_driver_handoff` | `Builder` → scheduler constructors (copied into `Shared.config`) |
| `driver::Cfg` | `enable_io/time/pause_time`, `start_paused`, `nevents`, `nevents_busy`, `timer_flavor` | `Builder` → `Driver::new` |
| `driver::Handle` | io/signal/time handles + `Clock` | `Builder` → `scheduler::Handle.driver` → resources |
| `blocking::Spawner` | `Arc<Inner>` | `Builder` → `Handle.blocking_spawner`; used for `spawn_blocking` & MT worker launch |
| `Launch(Vec<Arc<Worker>>)` | all workers | `create` → `Runtime` → `launch()` spawns them |
| `Box<Core>` (MT) | LIFO slot, ring, parker, stats, flags | moves **by pointer** between `Worker.core` ⇄ `Context.core` ⇄ `shutdown_cores` ([sched/11](./scheduler/11-block-in-place-and-defer.md)) |
| `Pop<'a,T>` | iterator holding `&mut Synced` + count | inject → worker ring ([sched/07](./scheduler/07-inject-queue.md)) |
| `Steal<T>` / `Local<T>` | two handles on one `Arc<Inner>` ring | `queue::local()` → `Remote.steal` (shared) & `Core.run_queue` (owner) |
| `Remote { steal, unpark }` | steal handle + `Unparker` | all workers read each other's `Remote` |
| `HadDriver::{Yes,No}` | whether the park used the driver | `Parker::park` → `Core.had_driver` |
| `MetricsBatch → WorkerMetrics` | counters | `Stats::submit` → readers ([sched/10](./scheduler/10-stats-and-metrics.md)) |
| `TaskMeta<'a>` 🌐 | `id`, `spawned_at`, `schedule_latency` | worker → user callbacks |
| `ScheduleLatencyInstant/Context` | timestamp stamped when scheduled | `schedule_*` → `run_task` |
| `EnterRuntime::{Entered{allow_block_in_place}, NotEntered}` | thread-local state | context ⇄ `block_in_place` |
| `SetCurrentGuard` / `EnterRuntimeGuard` | RAII guards restoring TLS | `Handle::enter`, `block_on` |
| `Budget(Option<u8>)` | 128 per poll | `coop::budget` ⇄ `poll_proceed` |

### 2.5 Public-facing DTOs 🌐
`JoinHandle<T>`, `AbortHandle`, `JoinError`, `task::Id`, `runtime::Id`, `Handle`, `EnterGuard`, `Runtime`, `RuntimeFlavor`, `RuntimeMetrics`, `TaskMeta`, `UnhandledPanic`, `LocalRuntime`/`LocalSet`.

---

## 3. Who implements / who calls — summary matrix

| Interface | Declared in | Implemented by | Called by |
|---|---|---|---|
| `Schedule` | task | MT/CT handles, LocalSet shared, BlockingSchedule | Harness, Waker, spawn |
| `Vtable` | task::raw | generated per `Harness<T,S>` | JoinHandle, queues, OwnedTasks, Waker |
| `Overflow` | multi_thread | `Handle` | `queue::Local` |
| `Link` | util | `Task` | `LinkedList`/`ShardedList` (OwnedTasks) |
| `driver::{Driver,Handle}` | runtime::driver | I/O + signal + process + time layers | `Parker`, current-thread `Context`, resources |
| `Future::poll` + `Waker` | std | user futures | Harness (`poll_future`) |

---

## 4. Why these particular interfaces?

1. **`Schedule` is generic, `Vtable` is dynamic.** Generics keep the hot path monomorphised *inside* a task; the vtable erases `(T, S)` so queues hold a uniform pointer.
2. **Ownership as types** (`Task`/`Notified`/`LocalNotified`): Rust's move semantics make "exactly one scheduler owns the right to run this" a compile-time property; only the *transition* is `unsafe`.
3. **Narrow surfaces.** Tasks know 5 methods of the scheduler; the scheduler knows `Notified` + `RawTask`; queues know `Notified` and `queue_next`; drivers know `Waker`. No cycle of knowledge.
4. **Enums over `dyn`** at the runtime layer, because flavors are closed (two) and cfg-gated.
