# Task component 5 — Typed Handles and the `Schedule` Trait (`runtime/task/mod.rs`)

> **One sentence:** the same 8-byte pointer wears four different *types* — `Task`, `Notified`, `LocalNotified`, `UnownedTask` — and each type encodes **a permission and a ref-count** (who may do what with the task); the `Schedule` trait is the *only* contract between the task system and any scheduler.

This file is the **public face of the task module to the rest of the runtime**: schedulers and the blocking pool import from here.

---

## 1. Where it lives

<!-- FILES:t_handles -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/mod.rs`](../../../tokio/src/runtime/task/mod.rs) | 348 | 259 | 42 |
<!-- /FILES -->

---

## 2. The four handle types (type-state pattern)

```rust
#[repr(transparent)] pub(crate) struct Task<S: 'static> { raw: RawTask, _p: PhantomData<S> }
#[repr(transparent)] pub(crate) struct Notified<S: 'static>(Task<S>);
pub(crate) struct LocalNotified<S: 'static> { task: Task<S>, _not_send: PhantomData<*const ()> }
pub(crate) struct UnownedTask<S: 'static> { raw: RawTask, _p: PhantomData<S> }
```
All are one pointer wide. They differ in **what the type system lets you do**:

| Type | Meaning | Ref-counts held | `Send`? | Created by | Consumed by |
|---|---|---:|---|---|---|
| `Task<S>` | "This runtime *owns* this task" — stored in an `OwnedTasks`/`LocalOwnedTasks` list (and used for shutdown) | 1 | yes (`unsafe impl Send + Sync`) | `new_task` | `Task::shutdown`; `Drop` (`ref_dec`) |
| `Notified<S>` | "This task is **scheduled**" — what lives in run queues. Cannot be polled by itself | 1 | yes, *conditionally* (`S: Schedule`) — "cannot touch the task without first verifying the thread is allowed to poll it" | `new_task`; every `Submit` (wake/abort) | `OwnedTasks::assert_owner` → `LocalNotified`; `Drop` |
| `LocalNotified<S>` | "This **thread** is allowed to poll this task" | 1 | **no** (`PhantomData<*const ()>`) | `OwnedTasks::assert_owner`, `LocalOwnedTasks::assert_owner` | `LocalNotified::run` (polls it) |
| `UnownedTask<S>` | A task **not in any list** — blocking tasks. Directly runnable. | **2** | yes | `unowned()` | `UnownedTask::run` / `shutdown`; `Drop` (`ref_dec_twice`) |

Why `LocalNotified` is `!Send`: it is the *proof* required to call `run()`. A `Notified` can travel between threads (stealing); but to poll it you must first call `assert_owner`, which for `LocalOwnedTasks` checks (by owner id, in all builds) that you are on the right thread. The `!Send` marker keeps the proof from escaping that thread.

### Constructors and conversions

```
new_task(future, scheduler, id, spawned_at) -> (Task<S>, Notified<S>, JoinHandle<T::Output>)
        RawTask::new  ──▶ refs=3 ──▶ three handles to the SAME pointer

unowned(future, scheduler, id, spawned_at) -> (UnownedTask<S>, JoinHandle<T::Output>)      // T: Send, Output: Send
        new_task(..) then  UnownedTask{raw}; mem::forget(task); mem::forget(notified)       // 2 refs transferred, JoinHandle keeps 1

 Notified ──OwnedTasks::assert_owner──▶ LocalNotified ──.run()──▶ RawTask::poll   (consumes the ref, mem::forget(self))
 UnownedTask ──.run()──▶ { raw.poll(); drop(Task from the 2nd ref) }
 UnownedTask ──.shutdown()──▶ into_task() (ref_dec) ──▶ Task::shutdown ──▶ raw.shutdown
 Task ──.shutdown()──▶ RawTask::shutdown (mem::forget(self): the ref is consumed by the vtable fn)
 Notified ──into_raw()/from_raw()──▶ RawTask      // used by the inject queue to store tasks as raw pointers without ref-count traffic
```

### Drop behaviour (the RAII half of the state word)
```rust
impl Drop for Task<S>        { fn drop(&mut self) { if self.header().state.ref_dec()       { self.raw.dealloc(); } } }
impl Drop for UnownedTask<S> { fn drop(&mut self) { if self.raw.header().state.ref_dec_twice() { self.raw.dealloc(); } } }
```
`Notified` and `LocalNotified` drop through their inner `Task`. A `Notified` being dropped (e.g. runtime shut down while it sat in a queue) just releases a ref — it does **not** cancel the task; cancellation is the job of `Task::shutdown` via `OwnedTasks` (see the comment in the unit test "A Notified does not shut down on drop").

---

## 3. The `Schedule` trait — the task ↔ scheduler contract

```rust
pub(crate) trait Schedule: Sync + Sized + 'static {
    fn release(&self, task: &Task<Self>) -> Option<Task<Self>>;   // task finished: remove it from your list, give the list's Task back
    fn schedule(&self, task: Notified<Self>);                     // a woken/spawned/aborted task is ready: queue it
    fn hooks(&self) -> TaskHarnessScheduleHooks;                  // snapshot of hooks to store in the task's Trailer
    fn yield_now(&self, task: Notified<Self>) { self.schedule(task) }   // woken *while running*: queue it fairly (default = schedule)
    fn unhandled_panic(&self) {}                                  // poll panicked: should the runtime shut down?
}
pub(crate) struct TaskHarnessScheduleHooks { pub(crate) task_terminate_callback: Option<TaskCallback> }
```

`S` is stored **inside every task** (`Core.scheduler`), so *any* thread that fires a waker can call `S::schedule` and the task goes home. In practice `S = Arc<Handle>` (a cheap clone per task).

### Who implements it and how

| Implementor | `release` | `schedule` | `yield_now` | `unhandled_panic` | `hooks` |
|---|---|---|---|---|---|
| `Arc<multi_thread::Handle>` | `shared.owned.remove(task)` | `schedule_task(task, is_yield = false)` → local LIFO/queue **or** inject queue | `schedule_task(task, true)` → **back of the local queue** | default (no-op) | clones `task_hooks.task_terminate_callback` |
| `Arc<current_thread::Handle>` | `shared.owned.remove(task)` | on-thread: `core.push_task` (VecDeque); otherwise `inject.push` + `driver.unpark()` | default (= `schedule`) | unstable: shutdown on panic | same |
| `Arc<local::Shared>` (`LocalSet`) | `local_state.task_remove(task)` | same-thread: local queue; other thread: `queue` mutex + `waker.wake()` | default | unstable: shutdown on panic | `None` (hooks unsupported) |
| `BlockingSchedule` | returns `None` (test-util: re-enable clock auto-advance) | `unreachable!()` — blocking tasks are never rescheduled | – | default | clones callback |
| test `Runtime` (`runtime/tests/task.rs`) | `owned.remove(task)` | `queue.push_back` (VecDeque) | default | default | `None` |
| `NoopSchedule` (tests) | `None` | `unreachable!()` | – | – | `None` |

### What `release` must do (and why it returns an `Option<Task>`)
`complete()` calls `release(&task)` once. The scheduler should remove the task from its `OwnedTasks`; `OwnedTasks::remove` returns the stored `Task` handle (carrying the list's ref-count). The harness `forget`s it and decrements **two** refs instead of one in `transition_to_terminal`. If the scheduler already removed it (e.g. during `close_and_shutdown_all`, which *pops* tasks before calling `shutdown`) it returns `None` and only one ref is dropped.

---

## 4. The smallest possible scheduler (this is the entire contract in code)

The unit-test runtime in `runtime/tests/task.rs` (≈70 lines) is a complete scheduler built only on this interface:

```rust
struct Runtime(Arc<Inner>);
struct Inner { core: Mutex<Core>, owned: OwnedTasks<Runtime> }
struct Core { queue: VecDeque<task::Notified<Runtime>> }

impl Runtime {
    fn spawn<T>(&self, future: T) -> JoinHandle<T::Output> {
        let (handle, notified) = self.0.owned.bind(future, self.clone(), Id::next(), SpawnLocation::capture());
        if let Some(notified) = notified { self.schedule(notified); }      // None ⇒ OwnedTasks was closed
        handle
    }
    fn tick_max(&self, max: usize) -> usize {
        while !self.is_empty() && n < max {
            let task = self.next_task();                    // pop_front
            let task = self.0.owned.assert_owner(task);     // Notified → LocalNotified
            task.run();                                     // → RawTask::poll → vtable → Harness::poll
        }
    }
    fn shutdown(&self) {
        self.0.owned.close_and_shutdown_all(0);             // cancel everything, refuse new binds
        while let Some(task) = core.queue.pop_back() { drop(task); }   // drop leftover Notifieds
    }
}
impl Schedule for Runtime {
    fn release(&self, task: &Task<Self>) -> Option<Task<Self>> { self.0.owned.remove(task) }
    fn schedule(&self, task: Notified<Self>)                    { self.0.core.lock().queue.push_back(task) }
    fn hooks(&self) -> TaskHarnessScheduleHooks                 { TaskHarnessScheduleHooks { task_terminate_callback: None } }
}
```
Everything Tokio's real schedulers add — work stealing, LIFO slot, parking, drivers — sits *around* exactly these five calls: **`bind`**, **`schedule`**, **`assert_owner` + `run`**, **`release`**, **`close_and_shutdown_all`**.

---

## 5. Other items defined in this file

| Item | Role |
|---|---|
| `pub(crate) type Result<T> = std::result::Result<T, JoinError>` | The type stored in `Stage::Finished` and returned by `JoinHandle` |
| `pub(crate) use SpawnLocation` | `#[derive(Copy)] struct SpawnLocation(&'static Location)` with `tokio_unstable`; a **zero-sized** `SpawnLocation()` otherwise (asserted by the test `spawn_location_is_zero_sized`) so spawn-site capture costs nothing in stable builds |
| `impl linked_list::Link for Task<S>` | `Handle = Task<S>`, `Target = Header`, `pointers = Trailer::addr_of_owned` — how tasks are threaded into `OwnedTasks` (see [08](./08-owned-tasks.md)) |
| `impl sharded_list::ShardedListItem for Task<S>` | `get_shard_id` = the task's `Id` (immutable ⇒ a task never changes shard) |
| `Task::{header, header_ptr, id, spawned_at, task_meta}` | field access; `task_meta` builds the `TaskMeta` passed to hooks |
| `Notified::set_scheduled_at / LocalNotified::get_scheduled_at` | schedule-latency metric stamps (single `Notified` per task ⇒ no data race) |
| `Task::notify_for_tracing` (task dump) | `transition_to_notified_for_tracing` → a `Notified` used to poll a task for its async backtrace |

---

## 6. Data flow between this component and its neighbours

```
          spawn(fut)                                                           wake / abort
              │                                                                      │
              ▼                                                                      ▼
   OwnedTasks::bind ── new_task ──▶ (Task, Notified, JoinHandle)        RawTask::wake_by_val/ref, remote_abort
        │ Task → list (ref 1)            │ Notified (ref 2)                          │ Submit ⇒ S::schedule(Notified)  [vtable.schedule]
        │ JoinHandle → user (ref 3)      ▼                                           ▼
        │                         S::schedule(Notified) ──▶ scheduler queues (Notified lives here)
        │                                                          │ worker pops
        │                                                          ▼
        │                                  OwnedTasks::assert_owner(Notified) ──▶ LocalNotified
        │                                                          │ .run()
        ▼                                                          ▼
   (list keeps Task)                                       RawTask::poll → Harness::poll → …
        ▲                                                          │ finished
        └────────────── S::release(&Task) ◀── Harness::complete ───┘
```

| Interface | Type that crosses | Ownership |
|---|---|---|
| spawn → scheduler | `Notified<S>` | moved (scheduler now owns that ref) |
| scheduler → task | `LocalNotified<S>` | moved into `run()` (ref consumed by `poll`) |
| task → scheduler (wake) | `Notified<S>` | newly created ref, moved into `schedule` |
| task → scheduler (finish) | `&Task<S>` | borrowed; returned `Option<Task<S>>` is moved back to the harness |
| runtime → task (shutdown) | `Task<S>` | moved into `Task::shutdown` |
| blocking pool → task | `UnownedTask<S>` | moved into `run()`/`shutdown()` |

---

## 7. Invariants

1. At most one `Notified` exists per task at any time (state bit `NOTIFIED`).
2. A `Notified` becomes a `LocalNotified` only through `assert_owner` of **the list that owns the task** (the owner id is checked: `debug_assert` for `OwnedTasks`, `assert` for `LocalOwnedTasks`).
3. `Send` is claimed for the handles only because the *constructors* require `Send` futures (`OwnedTasks::bind`, `unowned`) — or, for `!Send` futures, the only way to create them is `LocalOwnedTasks`/`bind_local`, whose `assert_owner` pins them to a thread.
4. `UnownedTask` always holds exactly two refs (it is built by forgetting the `Task` and `Notified`).

---

## 8. Tests

<!-- TESTS:t_handles -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| [`tokio/src/runtime/tests/task_combinations.rs`](../../../tokio/src/runtime/tests/task_combinations.rs) | 1 | 404 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`runtime/tests/task.rs` is the unit-test suite for exactly this layer (`create_drop*`, `drop_abort_handle*`, `create_shutdown*`, `unowned_poll`, `schedule`, `shutdown*`, `spawn_during_shutdown`).

**Read next:** [06 — Waker](./06-waker.md).
