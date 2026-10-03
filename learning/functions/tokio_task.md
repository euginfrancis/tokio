# `tokio::task` — 108 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 54 |
| Trait impl | 28 |
| Private helper | 21 |
| Crate-internal | 3 |
| Test | 2 |

## `tokio/src/task/blocking.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 74 | `block_in_place`  |  | Public API | Other / internal logic | Runs the provided blocking function on the current thread without blocking the executor. |
| 220 | `spawn_blocking`  |  | Public API | Runtime/task control | Runs the provided closure on a thread where blocking is acceptable. |

## `tokio/src/task/builder.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 69 | `new`  | `Builder<'a>` | Public API | Constructor | Creates a new task builder. |
| 74 | `name`  | `Builder<'a>` | Public API | Other / internal logic | Assigns a name to the task which will be spawned. |
| 87 | `spawn`  | `Builder<'a>` | Public API | Runtime/task control | Spawns a task with this builder's settings on the current runtime. |
| 108 | `spawn_on`  | `Builder<'a>` | Public API | Runtime/task control | Spawn a task with this builder's settings on the provided [runtime handle]. |
| 139 | `spawn_local`  | `Builder<'a>` | Public API | Runtime/task control | Spawns a `!Send` task on the current [`LocalSet`] or [`LocalRuntime`] with this builder's settings. |
| 160 | `spawn_local_on`  | `Builder<'a>` | Public API | Runtime/task control | Spawns `!Send` a task on the provided [`LocalSet`] with this builder's settings. |
| 186 | `spawn_blocking`  | `Builder<'a>` | Public API | Runtime/task control | Spawns blocking code on the blocking threadpool. |
| 205 | `spawn_blocking_on`  | `Builder<'a>` | Public API | Runtime/task control | Spawns blocking code on the provided [runtime handle]'s blocking threadpool. |

## `tokio/src/task/join_set.rs` (34)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 82 | `new`  | `JoinSet<T>` | Public API | Constructor | Create a new `JoinSet`. |
| 89 | `len`  | `JoinSet<T>` | Public API | Accessor / query | Returns the number of tasks currently in the `JoinSet`. |
| 94 | `is_empty`  | `JoinSet<T>` | Public API | Accessor / query | Returns whether the `JoinSet` is empty. |
| 122 | `build_task`  | `JoinSet<T>` | Public API | Constructor | Returns a [`Builder`] that can be used to configure a task prior to spawning it on this `JoinSet`. |
| 142 | `spawn`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the provided task on the `JoinSet`, returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 161 | `spawn_on`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the provided task on the provided runtime and store it in this `JoinSet` returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 186 | `spawn_local`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the provided task on the current [`LocalSet`] or [`LocalRuntime`] and store it in this `JoinSet`, returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 206 | `spawn_local_on`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the provided task on the provided [`LocalSet`] and store it in this `JoinSet`, returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 254 | `spawn_blocking`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool and store it in this `JoinSet`, returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 269 | `spawn_blocking_on`  | `JoinSet<T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool of the provided runtime and store it in this `JoinSet`, returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 278 | `insert`  | `JoinSet<T>` | Private helper | Data movement |  |
| 296 | `join_next` 🅰 | `JoinSet<T>` | Public API | Async operation | Waits until one of the tasks in the set completes and returns its output. |
| 316 | `join_next_with_id` 🅰 | `JoinSet<T>` | Public API | Async operation | Waits until one of the tasks in the set completes and returns its output, along with the [task ID] of the completed task. |
| 323 | `try_join_next`  | `JoinSet<T>` | Public API | Non-blocking attempt | Tries to join one of the tasks in the set that has completed and return its output. |
| 352 | `try_join_next_with_id`  | `JoinSet<T>` | Public API | Non-blocking attempt | Tries to join one of the tasks in the set that has completed and return its output, along with the [task ID] of the completed task. |
| 381 | `shutdown` 🅰 | `JoinSet<T>` | Public API | Runtime/task control | Aborts all tasks and waits for them to finish shutting down. |
| 446 | `join_all` 🅰 | `JoinSet<T>` | Public API | Async operation | Awaits the completion of all tasks in this `JoinSet`, returning a vector of their results. |
| 463 | `abort_all`  | `JoinSet<T>` | Public API | Lifecycle / ref-count | Aborts all tasks on this `JoinSet`. |
| 471 | `detach_all`  | `JoinSet<T>` | Public API | Other / internal logic | Removes all tasks from this `JoinSet` without aborting them. |
| 500 | `poll_join_next`  | `JoinSet<T>` | Public API | Poll function | Polls for one of the tasks in the set to complete. |
| 556 | `poll_join_next_with_id`  | `JoinSet<T>` | Public API | Poll function | Polls for one of the tasks in the set to complete. |
| 592 | `drop`  | `Drop for JoinSet<T>` | Trait impl | Drop / cleanup |  |
| 598 | `fmt`  | `fmt::Debug for JoinSet<T>` | Trait impl | Formatting |  |
| 604 | `default`  | `Default for JoinSet<T>` | Trait impl | Constructor |  |
| 643 | `from_iter`  | `std::iter::FromIterator<F> for JoinSet<T>` | Trait impl | Conversion |  |
| 687 | `extend`  | `std::iter::Extend<F> for JoinSet<T>` | Trait impl | Combinator / iteration |  |
| 703 | `name`  | `Builder<'a, T>` | Public API | Other / internal logic | Assigns a name to the task which will be spawned. |
| 722 | `spawn`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the provided task with this builder's settings and store it in the [`JoinSet`], returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 742 | `spawn_on`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the provided task on the provided [runtime handle] with this builder's settings, and store it in the [`JoinSet`]. |
| 765 | `spawn_blocking`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool with this builder's settings, and store it in the [`JoinSet`]. |
| 785 | `spawn_blocking_on`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool of the provided runtime handle with this builder's settings, and store it in the [`JoinSet`]. |
| 811 | `spawn_local`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the provided task on the current [`LocalSet`] or [`LocalRuntime`] with this builder's settings, and store it in the [`JoinSet`]. |
| 829 | `spawn_local_on`  | `Builder<'a, T>` | Public API | Runtime/task control | Spawn the provided task on the provided [`LocalSet`] with this builder's settings, and store it in the [`JoinSet`]. |
| 845 | `fmt`  | `fmt::Debug for Builder<'a, T>` | Trait impl | Formatting |  |

## `tokio/src/task/local.rs` (42)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 301 | `enter`  | `LocalData` | Private helper | Runtime/task control | Should be called except when we call `LocalSet::enter`. |
| 320 | `drop`  | `Drop for LocalDataEnterGuard<'a>` | Trait impl | Drop / cleanup |  |
| 394 | `spawn_local`  |  | Public API | Runtime/task control | Spawns a `!Send` future on the current [`LocalSet`] or [`LocalRuntime`]. |
| 409 | `spawn_local_inner`  |  | Crate-internal | Runtime/task control |  |
| 482 | `drop`  | `Drop for LocalEnterGuard` | Trait impl | Drop / cleanup |  |
| 496 | `fmt`  | `fmt::Debug for LocalEnterGuard` | Trait impl | Formatting |  |
| 503 | `new`  | `LocalSet` | Public API | Constructor | Returns a new local task set. |
| 532 | `enter`  | `LocalSet` | Public API | Runtime/task control | Enters the context of this `LocalSet`. |
| 591 | `spawn_local`  | `LocalSet` | Public API | Runtime/task control | Spawns a `!Send` task onto the local task set. |
| 672 | `block_on`  | `LocalSet` | Public API | Runtime/task control | Runs a future to completion on the provided runtime, driving any local futures spawned on this task set on the current thread. |
| 711 | `run_until` 🅰 | `LocalSet` | Public API | Runtime/task control | Runs a future to completion on the local set, returning its output. |
| 723 | `spawn_named`  | `LocalSet` | Crate-internal | Runtime/task control |  |
| 736 | `spawn_named_inner`  | `LocalSet` | Private helper | Runtime/task control |  |
| 755 | `tick`  | `LocalSet` | Private helper | Time / timers | Ticks the scheduler, returning whether the local future needs to be notified again. |
| 780 | `next_task`  | `LocalSet` | Private helper | Other / internal logic |  |
| 811 | `pop_local`  | `LocalSet` | Private helper | Data movement |  |
| 820 | `with`  | `LocalSet` | Private helper | Combinator / iteration |  |
| 829 | `with_if_possible`  | `LocalSet` | Private helper | Constructor | This method is like `with`, but it just calls `f` without setting the thread-local if that fails. |
| 858 | `id`  | `LocalSet` | Public API | Accessor / query | Returns the [`Id`] of the current [`LocalSet`] runtime. |
| 923 | `unhandled_panic`  | `LocalSet` | Public API | Other / internal logic | Configure how the `LocalSet` responds to an unhandled panic on a spawned task. |
| 935 | `fmt`  | `fmt::Debug for LocalSet` | Trait impl | Formatting |  |
| 943 | `poll`  | `Future for LocalSet` | Trait impl | Future impl (poll) |  |
| 970 | `default`  | `Default for LocalSet` | Trait impl | Constructor |  |
| 976 | `drop`  | `Drop for LocalSet` | Trait impl | Drop / cleanup |  |
| 1027 | `spawn`  | `Context` | Private helper | Runtime/task control |  |
| 1059 | `poll`  | `Future for RunUntil<'_, T>` | Trait impl | Future impl (poll) |  |
| 1089 | `schedule`  | `Shared` | Private helper | Runtime/task control | Schedule the provided task on the scheduler. |
| 1132 | `ptr_eq`  | `Shared` | Private helper | Handle / reference plumbing |  |
| 1142 | `release`  | `task::Schedule for Arc<Shared>` | Trait impl | Scheduler hook |  |
| 1147 | `schedule`  | `task::Schedule for Arc<Shared>` | Trait impl | Scheduler hook |  |
| 1152 | `hooks`  | `task::Schedule for Arc<Shared>` | Trait impl | Scheduler hook |  |
| 1159 | `unhandled_panic`  | `task::Schedule for Arc<Shared>` | Trait impl | Scheduler hook |  |
| 1189 | `task_pop_front` ⚠ | `LocalState` | Private helper | Other / internal logic | # Safety This method must only be called from the thread who has the same [`ThreadId`] as [`Self::owner`]. |
| 1202 | `task_push_back` ⚠ | `LocalState` | Private helper | Other / internal logic | # Safety This method must only be called from the thread who has the same [`ThreadId`] as [`Self::owner`]. |
| 1215 | `take_local_queue` ⚠ | `LocalState` | Private helper | Data movement | # Safety This method must only be called from the thread who has the same [`ThreadId`] as [`Self::owner`]. |
| 1224 | `task_remove` ⚠ | `LocalState` | Private helper | Other / internal logic |  |
| 1233 | `owned_is_empty` ⚠ | `LocalState` | Private helper | Other / internal logic | Returns true if the `LocalSet` does not have any spawned tasks |
| 1241 | `assert_owner` ⚠ | `LocalState` | Private helper | Debugging / tracing |  |
| 1252 | `close_and_shutdown_all` ⚠ | `LocalState` | Private helper | Data movement |  |
| 1261 | `assert_called_from_owner_thread`  | `LocalState` | Private helper | Debugging / tracing |  |
| 1289 | `local_current_thread_scheduler`  |  | Test | Other / internal logic |  |
| 1311 | `wakes_to_local_queue`  |  | Test | Wake / park |  |

## `tokio/src/task/spawn.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 174 | `spawn`  |  | Public API | Runtime/task control | Spawns a new asynchronous task, returning a [`JoinHandle`] for it. |
| 188 | `spawn_inner`  |  | Crate-internal | Runtime/task control |  |

## `tokio/src/task/task_local.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 130 | `scope`  | `LocalKey<T>` | Public API | Other / internal logic | Sets a value `T` as the task-local value for the future `F`. |
| 168 | `sync_scope`  | `LocalKey<T>` | Public API | Other / internal logic | Sets a value `T` as the task-local value for the closure `F`. |
| 179 | `scope_inner`  | `LocalKey<T>` | Private helper | Other / internal logic |  |
| 189 | `drop`  | `Drop for Guard<'a, T>` | Trait impl | Drop / cleanup |  |
| 230 | `with`  | `LocalKey<T>` | Public API | Combinator / iteration | Accesses the current task-local and runs the provided closure. |
| 245 | `try_with`  | `LocalKey<T>` | Public API | Non-blocking attempt | Accesses the current task-local and runs the provided closure. |
| 275 | `get`  | `LocalKey<T>` | Public API | Accessor / query | Returns a copy of the task-local value if the task-local value implements `Clone`. |
| 285 | `try_get`  | `LocalKey<T>` | Public API | Non-blocking attempt | Returns a copy of the task-local value if the task-local value implements `Clone`. |
| 291 | `fmt`  | `fmt::Debug for LocalKey<T>` | Trait impl | Formatting |  |
| 331 | `drop`  | `PinnedDrop for TaskLocalFuture<T, F>` | Trait impl | Other / internal logic |  |
| 383 | `take_value`  | `TaskLocalFuture<T, F>` | Public API | Data movement | Returns the value stored in the task local by this `TaskLocalFuture`. |
| 393 | `poll`  | `Future for TaskLocalFuture<T, F>` | Trait impl | Future impl (poll) |  |
| 422 | `fmt`  | `fmt::Debug for TaskLocalFuture<T, F>` | Trait impl | Formatting |  |
| 428 | `fmt`  | `fmt::Debug for TransparentOption<'a, T>` | Trait impl | Formatting |  |
| 450 | `fmt`  | `fmt::Debug for AccessError` | Trait impl | Formatting |  |
| 456 | `fmt`  | `fmt::Display for AccessError` | Trait impl | Formatting |  |
| 470 | `panic`  | `ScopeInnerErr` | Private helper | Other / internal logic |  |
| 479 | `from`  | `From<std::cell::BorrowMutError> for ScopeInnerErr` | Trait impl | Conversion |  |
| 485 | `from`  | `From<std::thread::AccessError> for ScopeInnerErr` | Trait impl | Conversion |  |

## `tokio/src/task/yield_now.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `yield_now` 🅰 |  | Public API | Async operation | Yields execution back to the Tokio runtime. |

