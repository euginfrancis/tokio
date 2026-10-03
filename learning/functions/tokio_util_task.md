# `tokio-util::task` — 126 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 76 |
| Trait impl | 28 |
| Private helper | 18 |
| Test | 4 |

## `tokio-util/src/task/abort_on_drop.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `drop`  | `Drop for AbortOnDropHandle<T>` | Trait impl | Drop / cleanup |  |
| 31 | `new`  | `AbortOnDropHandle<T>` | Public API | Constructor | Create an [`AbortOnDropHandle`] from a [`JoinHandle`]. |
| 38 | `abort`  | `AbortOnDropHandle<T>` | Public API | Lifecycle / ref-count | Abort the task associated with this handle, equivalent to [`JoinHandle::abort`]. |
| 45 | `is_finished`  | `AbortOnDropHandle<T>` | Public API | Accessor / query | Checks if the task associated with this handle is finished, equivalent to [`JoinHandle::is_finished`]. |
| 51 | `abort_handle`  | `AbortOnDropHandle<T>` | Public API | Lifecycle / ref-count | Returns a new [`AbortHandle`] that can be used to remotely abort this task, equivalent to [`JoinHandle::abort_handle`]. |
| 56 | `detach`  | `AbortOnDropHandle<T>` | Public API | Other / internal logic | Cancels aborting on drop and returns the original [`JoinHandle`]. |
| 66 | `fmt`  | `std::fmt::Debug for AbortOnDropHandle<T>` | Trait impl | Formatting |  |
| 76 | `poll`  | `Future for AbortOnDropHandle<T>` | Trait impl | Future impl (poll) |  |
| 82 | `as_ref`  | `AsRef<JoinHandle<T>> for AbortOnDropHandle<T>` | Trait impl | Conversion |  |
| 100 | `drop`  | `Drop for AbortOnDrop` | Trait impl | Drop / cleanup |  |
| 107 | `new`  | `AbortOnDrop` | Public API | Constructor | Create an [`AbortOnDrop`] from a [`AbortHandle`]. |
| 114 | `abort`  | `AbortOnDrop` | Public API | Lifecycle / ref-count | Abort the task associated with this handle, equivalent to [`AbortHandle::abort`]. |
| 121 | `is_finished`  | `AbortOnDrop` | Public API | Accessor / query | Checks if the task associated with this handle is finished, equivalent to [`AbortHandle::is_finished`]. |
| 126 | `detach`  | `AbortOnDrop` | Public API | Other / internal logic | Cancels aborting on drop and returns the original [`AbortHandle`]. |
| 136 | `fmt`  | `std::fmt::Debug for AbortOnDrop` | Trait impl | Formatting |  |
| 150 | `is_debug`  |  | Test | Accessor / query |  |
| 153 | `assert_debug`  |  | Test | Debugging / tracing |  |

## `tokio-util/src/task/join_map.rs` (35)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 131 | `new`  | `JoinMap<K, V>` | Public API | Constructor | Creates a new empty `JoinMap`. |
| 148 | `with_capacity`  | `JoinMap<K, V>` | Public API | Constructor | Creates an empty `JoinMap` with the specified capacity. |
| 168 | `with_hasher`  | `JoinMap<K, V, S>` | Public API | Constructor | Creates an empty `JoinMap` which will use the given hash builder to hash keys. |
| 201 | `with_capacity_and_hasher`  | `JoinMap<K, V, S>` | Public API | Constructor | Creates an empty `JoinMap` with the specified capacity, using `hash_builder` to hash the keys. |
| 210 | `len`  | `JoinMap<K, V, S>` | Public API | Accessor / query | Returns the number of tasks currently in the `JoinMap`. |
| 217 | `is_empty`  | `JoinMap<K, V, S>` | Public API | Accessor / query | Returns whether the `JoinMap` is empty. |
| 237 | `capacity`  | `JoinMap<K, V, S>` | Public API | Accessor / query | Returns the number of tasks the map can hold without reallocating. |
| 264 | `spawn`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the provided task and store it in this `JoinMap` with the provided key. |
| 284 | `spawn_on`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the provided task on the provided runtime and store it in this `JoinMap` with the provided key. |
| 313 | `spawn_blocking`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool and store it in this `JoinMap` with the provided key. |
| 338 | `spawn_blocking_on`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool of the provided runtime and store it in this `JoinMap` with the provided key. |
| 364 | `spawn_local`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the provided task on the current [`LocalSet`] or [`LocalRuntime`] and store it in this `JoinMap` with the provided key. |
| 384 | `spawn_local_on`  | `JoinMap<K, V, S>` | Public API | Runtime/task control | Spawn the provided task on the provided [`LocalSet`] and store it in this `JoinMap` with the provided key. |
| 393 | `insert`  | `JoinMap<K, V, S>` | Private helper | Data movement |  |
| 455 | `join_next` 🅰 | `JoinMap<K, V, S>` | Public API | Async operation | Waits until one of the tasks in the map completes and returns its output, along with the key corresponding to that task. |
| 510 | `try_join_next`  | `JoinMap<K, V, S>` | Public API | Non-blocking attempt | Tries to join one of the tasks in the map that has completed and returns its output, along with the key corresponding to that task. |
| 535 | `shutdown` 🅰 | `JoinMap<K, V, S>` | Public API | Runtime/task control | Aborts all tasks and waits for them to finish shutting down. |
| 593 | `abort`  | `JoinMap<K, V, S>` | Public API | Lifecycle / ref-count | Abort the task corresponding to the provided `key`. |
| 660 | `abort_matching`  | `JoinMap<K, V, S>` | Public API | Lifecycle / ref-count | Aborts all tasks with keys matching `predicate`. |
| 677 | `keys`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Returns an iterator visiting all keys in this `JoinMap` in arbitrary order. |
| 690 | `contains_key`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Returns `true` if this `JoinMap` contains a task for the provided key. |
| 706 | `contains_task`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Returns `true` if this `JoinMap` contains a task with the provided [task ID]. |
| 730 | `reserve`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Reserves capacity for at least `additional` more tasks to be spawned on this `JoinMap` without reallocating for the map of task keys. |
| 757 | `shrink_to_fit`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Shrinks the capacity of the `JoinMap` as much as possible. |
| 787 | `shrink_to`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Shrinks the capacity of the map with a lower limit. |
| 795 | `get_by_key`  | `JoinMap<K, V, S>` | Private helper | Accessor / query | Look up a task in the map by its key, returning the key and abort handle. |
| 805 | `remove_by_id`  | `JoinMap<K, V, S>` | Private helper | Data movement | Remove a task from the map by ID, returning the key for that task. |
| 829 | `abort_all`  | `JoinMap<K, V, S>` | Public API | Lifecycle / ref-count | Aborts all tasks on this `JoinMap`. |
| 837 | `detach_all`  | `JoinMap<K, V, S>` | Public API | Other / internal logic | Removes all tasks from this `JoinMap` without aborting them. |
| 847 | `fmt`  | `fmt::Debug for JoinMap<K, V, S>` | Trait impl | Formatting |  |
| 854 | `fmt`  | `fmt::Debug for KeySet<'_, K>` | Trait impl | Formatting |  |
| 872 | `default`  | `Default for JoinMap<K, V>` | Trait impl | Constructor |  |
| 889 | `next`  | `Iterator for JoinMapKeys<'a, K, V>` | Trait impl | Iterator |  |
| 893 | `size_hint`  | `Iterator for JoinMapKeys<'a, K, V>` | Trait impl | Iterator |  |
| 899 | `len`  | `ExactSizeIterator for JoinMapKeys<'a, K, V>` | Trait impl | Accessor / query |  |

## `tokio-util/src/task/join_queue.rs` (26)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 28 | `new` 🅲 | `JoinQueue<T>` | Public API | Constructor | Create a new empty [`JoinQueue`]. |
| 33 | `with_capacity`  | `JoinQueue<T>` | Public API | Constructor | Creates an empty [`JoinQueue`] with space for at least `capacity` tasks. |
| 42 | `len`  | `JoinQueue<T>` | Public API | Accessor / query | Returns the number of tasks currently in the [`JoinQueue`]. |
| 47 | `is_empty`  | `JoinQueue<T>` | Public API | Accessor / query | Returns whether the [`JoinQueue`] is empty. |
| 64 | `spawn`  | `JoinQueue<T>` | Public API | Runtime/task control | Spawn the provided task on the [`JoinQueue`], returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 82 | `spawn_on`  | `JoinQueue<T>` | Public API | Runtime/task control | Spawn the provided task on the provided runtime and store it in this [`JoinQueue`] returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 106 | `spawn_local`  | `JoinQueue<T>` | Public API | Runtime/task control | Spawn the provided task on the current [`LocalSet`] or [`LocalRuntime`] and store it in this [`JoinQueue`], returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 124 | `spawn_blocking`  | `JoinQueue<T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool and store it in this [`JoinQueue`], returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 138 | `spawn_blocking_on`  | `JoinQueue<T>` | Public API | Runtime/task control | Spawn the blocking code on the blocking threadpool of the provided runtime and store it in this [`JoinQueue`], returning an [`AbortHandle`] that can be used to remotely cancel the task. |
| 146 | `push_back`  | `JoinQueue<T>` | Private helper | Data movement |  |
| 162 | `join_next` 🅰 | `JoinQueue<T>` | Public API | Async operation | Waits until the next task in FIFO order completes and returns its output. |
| 182 | `join_next_with_id` 🅰 | `JoinQueue<T>` | Public API | Async operation | Waits until the next task in FIFO order completes and returns its output, along with the [task ID] of the completed task. |
| 190 | `try_poll_handle`  | `JoinQueue<T>` | Private helper | Non-blocking attempt | Tries to poll an `AbortOnDropHandle` without blocking or yielding. |
| 211 | `try_join_next`  | `JoinQueue<T>` | Public API | Non-blocking attempt | Tries to join the next task in FIFO order if it has completed. |
| 231 | `try_join_next_with_id`  | `JoinQueue<T>` | Public API | Non-blocking attempt | Tries to join the next task in FIFO order if it has completed and return its output, along with its [task ID]. |
| 253 | `shutdown` 🅰 | `JoinQueue<T>` | Public API | Runtime/task control | Aborts all tasks and waits for them to finish shutting down. |
| 274 | `join_all` 🅰 | `JoinQueue<T>` | Public API | Async operation | Awaits the completion of all tasks in this [`JoinQueue`], returning a vector of their results. |
| 291 | `abort_all`  | `JoinQueue<T>` | Public API | Lifecycle / ref-count | Aborts all tasks on this [`JoinQueue`]. |
| 299 | `detach_all`  | `JoinQueue<T>` | Public API | Other / internal logic | Removes all tasks from this [`JoinQueue`] without aborting them. |
| 323 | `poll_join_next`  | `JoinQueue<T>` | Public API | Poll function | Polls for the next task in [`JoinQueue`] to complete. |
| 361 | `poll_join_next_with_id`  | `JoinQueue<T>` | Public API | Poll function | Polls for the next task in [`JoinQueue`] to complete. |
| 386 | `fmt`  | `std::fmt::Debug for JoinQueue<T>` | Trait impl | Formatting |  |
| 394 | `default`  | `Default for JoinQueue<T>` | Trait impl | Constructor |  |
| 407 | `from_iter`  | `std::iter::FromIterator<F> for JoinQueue<T>` | Trait impl | Conversion |  |
| 423 | `is_debug`  |  | Test | Accessor / query |  |
| 426 | `assert_debug`  |  | Test | Debugging / tracing |  |

## `tokio-util/src/task/spawn_pinned.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 65 | `new`  | `LocalPoolHandle` | Public API | Constructor | Create a new pool of threads to handle `!Send` tasks. |
| 79 | `num_threads`  | `LocalPoolHandle` | Public API | Accessor / query | Returns the number of threads of the Pool. |
| 85 | `get_task_loads_for_each_worker`  | `LocalPoolHandle` | Public API | Accessor / query | Returns the number of tasks scheduled on each worker. |
| 125 | `spawn_pinned`  | `LocalPoolHandle` | Public API | Runtime/task control | Spawn a task onto a worker thread and pin it there so it can't be moved off of the thread. |
| 181 | `spawn_pinned_by_idx`  | `LocalPoolHandle` | Public API | Runtime/task control | Differs from `spawn_pinned` only in that you can choose a specific worker thread of the pool, whereas `spawn_pinned` chooses the worker with the smallest number of tasks scheduled. |
| 194 | `fmt`  | `Debug for LocalPoolHandle` | Trait impl | Formatting |  |
| 211 | `spawn_pinned`  | `LocalPool` | Private helper | Runtime/task control | Spawn a `?Send` future onto a worker |
| 313 | `find_and_incr_least_burdened_worker`  | `LocalPool` | Private helper | Other / internal logic | Find the worker with the least number of tasks, increment its task count, and return its handle. |
| 340 | `find_worker_by_idx`  | `LocalPool` | Private helper | Other / internal logic |  |
| 353 | `drop`  | `Drop for JobCountGuard` | Trait impl | Drop / cleanup |  |
| 364 | `drop`  | `Drop for AbortGuard` | Trait impl | Drop / cleanup |  |
| 379 | `new_worker`  | `LocalWorkerHandle` | Private helper | Constructor | Create a new worker for executing pinned tasks |
| 400 | `run`  | `LocalWorkerHandle` | Private helper | Runtime/task control |  |

## `tokio-util/src/task/task_tracker.rs` (35)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 208 | `new`  | `TaskTrackerInner` | Private helper | Constructor |  |
| 216 | `is_closed_and_empty`  | `TaskTrackerInner` | Private helper | Accessor / query |  |
| 225 | `set_closed`  | `TaskTrackerInner` | Private helper | Configuration / setter |  |
| 252 | `set_open`  | `TaskTrackerInner` | Private helper | Configuration / setter |  |
| 259 | `add_task`  | `TaskTrackerInner` | Private helper | Other / internal logic |  |
| 264 | `drop_task`  | `TaskTrackerInner` | Private helper | Lifecycle / ref-count |  |
| 274 | `notify_now`  | `TaskTrackerInner` | Private helper | Wake / park |  |
| 293 | `new`  | `TaskTracker` | Public API | Constructor | Creates a new `TaskTracker`. |
| 318 | `wait`  | `TaskTracker` | Public API | Runtime/task control | Waits until this `TaskTracker` is both closed and empty. |
| 337 | `close`  | `TaskTracker` | Public API | Data movement | Close this `TaskTracker`. |
| 349 | `reopen`  | `TaskTracker` | Public API | Other / internal logic | Reopen this `TaskTracker`. |
| 356 | `is_closed`  | `TaskTracker` | Public API | Accessor / query | Returns `true` if this `TaskTracker` is [closed](Self::close). |
| 363 | `len`  | `TaskTracker` | Public API | Accessor / query | Returns the number of tasks tracked by this `TaskTracker`. |
| 370 | `is_empty`  | `TaskTracker` | Public API | Accessor / query | Returns `true` if there are no tasks in this `TaskTracker`. |
| 381 | `spawn`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided future on the current Tokio runtime, and track it in this `TaskTracker`. |
| 396 | `spawn_on`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided future on the provided Tokio runtime, and track it in this `TaskTracker`. |
| 419 | `spawn_local`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided future on the current [`LocalSet`] or [`LocalRuntime`] and track it in this `TaskTracker`. |
| 436 | `spawn_local_on`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided future on the provided [`LocalSet`], and track it in this `TaskTracker`. |
| 452 | `spawn_blocking`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided blocking task on the current Tokio runtime, and track it in this `TaskTracker`. |
| 474 | `spawn_blocking_on`  | `TaskTracker` | Public API | Runtime/task control | Spawn the provided blocking task on the provided Tokio runtime, and track it in this `TaskTracker`. |
| 532 | `track_future`  | `TaskTracker` | Public API | Other / internal logic | Track the provided future. |
| 549 | `token`  | `TaskTracker` | Public API | Handle / reference plumbing | Creates a [`TaskTrackerToken`] representing a task tracked by this `TaskTracker`. |
| 572 | `ptr_eq`  | `TaskTracker` | Public API | Handle / reference plumbing | Returns `true` if both task trackers correspond to the same set of tasks. |
| 582 | `default`  | `Default for TaskTracker` | Trait impl | Constructor | Creates a new `TaskTracker`. |
| 623 | `clone`  | `Clone for TaskTracker` | Trait impl | Clone | Returns a new `TaskTracker` that tracks the same set of tasks. |
| 630 | `debug_inner`  |  | Private helper | Debugging / tracing |  |
| 643 | `fmt`  | `fmt::Debug for TaskTracker` | Trait impl | Formatting |  |
| 652 | `task_tracker`  | `TaskTrackerToken` | Public API | Other / internal logic | Returns the [`TaskTracker`] that this token is associated with. |
| 662 | `clone`  | `Clone for TaskTrackerToken` | Trait impl | Clone | Returns a new `TaskTrackerToken` associated with the same [`TaskTracker`]. |
| 670 | `drop`  | `Drop for TaskTrackerToken` | Trait impl | Drop / cleanup | Dropping the token indicates to the [`TaskTracker`] that the task has exited. |
| 679 | `poll`  | `Future for TrackedFuture<F>` | Trait impl | Future impl (poll) |  |
| 685 | `fmt`  | `fmt::Debug for TrackedFuture<F>` | Trait impl | Formatting |  |
| 697 | `poll`  | `Future for TaskTrackerWaitFuture<'a>` | Trait impl | Future impl (poll) |  |
| 716 | `fmt`  | `fmt::Debug for TaskTrackerWaitFuture<'a>` | Trait impl | Formatting |  |
| 720 | `fmt`  | `fmt::Debug for Helper<'_>` | Trait impl | Formatting |  |

