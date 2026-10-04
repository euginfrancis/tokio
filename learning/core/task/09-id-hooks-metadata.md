# Task component 9 — Task Identity, Hooks & Metadata (`runtime/task/id.rs`, `runtime/task_hooks.rs`, parts of `core.rs`/`runtime/metrics`)

> **One sentence:** small, cross-cutting pieces that let the runtime and users *observe* tasks — a unique `Id` per task (readable from inside the task), a `TaskMeta` snapshot (id, spawn location, schedule latency) and four optional lifecycle **hooks** (`spawn`, `before_poll`, `after_poll`, `terminate`).

---

## 1. Where it lives

<!-- FILES:t_idhooks -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/id.rs`](../../../tokio/src/runtime/task/id.rs) | 38 | 43 | 5 |
| [`tokio/src/runtime/task_hooks.rs`](../../../tokio/src/runtime/task_hooks.rs) | 71 | 33 | 7 |
| **Total (2 files)** | **109** | **76** | **12** |
<!-- /FILES -->

---

## 2. Task identity

```rust
pub struct Id(pub(crate) NonZeroU64);          // Clone, Copy, Debug, Hash, Eq, Ord, Display
pub fn id() -> Id            { context::current_task_id().expect("Can't get a task id when not inside a task") }   // #[track_caller]
pub fn try_id() -> Option<Id> { context::current_task_id() }
impl Id { pub(crate) fn next() -> Self;  pub(crate) fn as_u64(&self) -> u64 }
```

| Aspect | Detail |
|---|---|
| Generation | process-wide `static NEXT_ID: AtomicU64 = AtomicU64::new(1)`; `fetch_add(1, Relaxed)` in a loop that skips `0` (so the `NonZeroU64` invariant holds even after a 2⁶⁴ wrap) |
| Uniqueness | unique across **all runtimes in the process** for the lifetime of the process (practically; documented as "unique relative to other currently spawned tasks") |
| Where it is stored | `Core.task_id` inside the task cell; reachable from a bare `*mut Header` via `vtable.id_offset` (so `JoinHandle::id()`, `AbortHandle::id()` need no state access) |
| Where it is used | `JoinError` (which task failed), `ShardedListItem::get_shard_id` (**shard = id & mask**), `TaskMeta`, tracing spans, `LocalSet`, `task::id()` |
| Reading it inside a task | `CONTEXT.current_task_id: Cell<Option<Id>>`, set by `TaskIdGuard` for exactly the duration of `Future::poll` **and** of dropping the future/output (see [02-cell-layout](./02-cell-layout.md) §7); nested polls restore the previous id |

⚠ Not to be confused with `runtime::Id` (`runtime/id.rs`, from `Handle::id()`). That one identifies a *runtime* — and it is **the same number as that runtime's `OwnedTasks.id`** (`Handle::id()` returns `runtime::Id::new(handle.owned_id())`), which is what gets stamped into each task's `Header.owner_id` and checked by `assert_owner`. So a task's `owner_id` equals its runtime's id; a task's own `Id` is a different counter.

---

## 3. `TaskMeta` — the snapshot given to hooks

```rust
pub struct TaskMeta<'a> {                       // `pub` only with tokio_unstable; fields are pub(crate)
    pub(crate) id: Id,
    pub(crate) spawned_at: SpawnLocation,       // &'static Location with tokio_unstable; ZST otherwise
    #[cfg(all(tokio_unstable, feature = "schedule-latency"))] pub(crate) schedule_latency: Option<Duration>,
    pub(crate) _phantom: PhantomData<&'a ()>,
}
impl TaskMeta<'_> { pub fn id(&self) -> Id;  /* unstable: */ pub fn spawned_at(&self) -> &'static Location<'static>;  pub fn schedule_latency(&self) -> Option<Duration>; }
pub(crate) type TaskCallback = Arc<dyn Fn(&TaskMeta<'_>) + Send + Sync>;
```
Built by `Task::task_meta(schedule_latency)` (from the header: id + spawn location) or by hand at spawn/terminate time.

`spawned_at` comes from `SpawnLocation::capture()` = `Location::caller()` through the `#[track_caller]` chain `spawn → spawn_inner → Handle::spawn → bind_new_task` — the *user's* call site.

---

## 4. Hooks

### Configuration path
```
Builder::on_task_spawn / on_task_terminate / on_before_task_poll / on_after_task_poll   (unstable)
    → builder fields before_spawn, after_termination, before_poll, after_poll
    → runtime::Config { before_spawn, after_termination, before_poll, after_poll, … }
    → TaskHooks::from_config(&config)             // stored in every scheduler Handle
```
```rust
#[derive(Clone)] pub(crate) struct TaskHooks {
    task_spawn_callback: Option<TaskCallback>,
    task_terminate_callback: Option<TaskCallback>,
    #[cfg(tokio_unstable)] before_poll_callback: Option<TaskCallback>,
    #[cfg(tokio_unstable)] after_poll_callback: Option<TaskCallback>,
}
pub(crate) struct TaskHarnessScheduleHooks { pub(crate) task_terminate_callback: Option<TaskCallback> }   // the subset the *task* needs, cloned into Trailer at spawn
```
The terminate callback is **copied into each task's `Trailer`** at creation (`Cell::new` calls `scheduler.hooks()`), because the harness — which has no access to the scheduler's `Handle` fields beyond the `Schedule` trait — must invoke it from `complete()`.

### Where each hook fires (verified call sites)

| Hook | Called from | When |
|---|---|---|
| `on_task_spawn` | `multi_thread::Handle::bind_new_task`; `current_thread::Handle::spawn` / `spawn_local` (`task_hooks.spawn(&TaskMeta)`) | right after the task is bound, **before** it is scheduled |
| `on_before_task_poll` / `on_after_task_poll` | `multi_thread` `Context::run_task` (around the first `task.run()` **and** around each LIFO-slot `task.run()`); `current_thread` `Context::run_task` | immediately around `LocalNotified::run` |
| `on_task_terminate` | `Harness::complete` (via `Trailer.hooks`), inside `catch_unwind` | after the task is `COMPLETE` and wakers were notified, before the scheduler's reference is released |
| *(none)* | `LocalSet` | `hooks()` returns `task_terminate_callback: None`; the code comment says *"localset does not currently support task hooks"* |
| terminate only | blocking pool (`BlockingSchedule`) | blocking tasks fire `on_task_terminate`, but never the poll hooks |

Hooks run **on the thread that polled the task**, must be `Send + Sync`, and **panics inside the terminate hook are caught and ignored** (`catch_unwind` in `complete`); the other hooks are called inline with no `catch_unwind` at their call sites, so keep them panic-free.

---

## 5. Schedule-latency stamping (metadata carried in the header)

```rust
Header.scheduled_at: UnsafeCell<ScheduleLatencyInstant>     // ScheduleLatencyInstant(Option<NonZeroU64>): nanoseconds since scheduler start
```
Enabled only with `tokio_unstable` + feature `schedule-latency` **and** `Builder::track_task_schedule_latency()` (or `enable_metrics_schedule_latency_histogram()`, which implies it); **64-bit targets only**. Otherwise it is a zero-sized mock.

| Step | Code |
|---|---|
| stamp on enqueue | `schedule_task`: `if shared.schedule_latency_start.is_some() { task.set_scheduled_at(ScheduleLatencyInstant::new(start)) }` (the `Notified` is the sole reference ⇒ no race) |
| read on dequeue | `run_task`: `task.get_scheduled_at().prepare(start)` → latency context → `stats.start_poll(ctx)` (first task) or `stats.record_schedule_latency(ctx)` (LIFO tasks) |
| result | per-worker poll-latency histogram; `TaskMeta.schedule_latency` for hooks |

---

## 6. Communication with other components

| Peer | Direction | What |
|---|---|---|
| Runtime context (`context.rs`) | `TaskIdGuard` ↔ `CONTEXT.current_task_id` | `Option<Id>` |
| [Cell](./02-cell-layout.md) | stores `task_id`, `spawned_at`, `scheduled_at`, hooks | fields |
| [Harness](./04-harness.md) | `complete()` → terminate hook | `&TaskMeta` |
| Scheduler | spawn/poll hooks; `TaskHooks` in `Handle`; stamps `scheduled_at` | `&TaskMeta`, `ScheduleLatencyInstant` |
| `Builder`/`Config` | supplies callbacks | `Arc<dyn Fn>` |
| tracing / task dump / tokio-console | read ids & spawn locations | `tracing_id`, `Id` |

---

## 7. Tests

<!-- TESTS:t_idhooks -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/task_id.rs`](../../../tokio/tests/task_id.rs) | 19 | 265 |
| [`tokio/tests/task_hooks.rs`](../../../tokio/tests/task_hooks.rs) | 10 | 325 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/task_id.rs` (ids inside tasks, `JoinHandle::id`, nesting, `LocalSet`), `task_hooks.rs` (every hook, ordering, `TaskMeta` contents; requires `--cfg tokio_unstable`), `rt_unstable_metrics.rs` (schedule latency).

**Read next:** [10 — Cooperative budget](./10-coop-budget.md).
