# `tokio::runtime::task` — 234 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 125 |
| Private helper | 62 |
| Trait impl | 25 |
| Public API | 14 |
| Trait method (declaration/default) | 5 |
| Test | 3 |

## `tokio/src/runtime/task/abort.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 28 | `new`  | `AbortHandle` | Crate-internal | Constructor |  |
| 53 | `abort`  | `AbortHandle` | Public API | Lifecycle / ref-count | Abort the task associated with the handle. |
| 63 | `is_finished`  | `AbortHandle` | Public API | Accessor / query | Checks if the task associated with this `AbortHandle` has finished. |
| 72 | `id`  | `AbortHandle` | Public API | Accessor / query | Returns a [task ID] that uniquely identifies this task relative to other currently spawned tasks. |
| 85 | `fmt`  | `fmt::Debug for AbortHandle` | Trait impl | Formatting |  |
| 94 | `drop`  | `Drop for AbortHandle` | Trait impl | Drop / cleanup |  |
| 101 | `clone`  | `Clone for AbortHandle` | Trait impl | Clone | Returns a cloned `AbortHandle` that can be used to remotely abort this task. |

## `tokio/src/runtime/task/core.rs` (29)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 217 | `addr_of_owned` ⚠ | `Trailer` | Crate-internal | Handle / reference plumbing |  |
| 234 | `new`  | `Cell<T, S>` | Crate-internal | Constructor | Allocates a new task cell, containing the header, trailer, and core structures. |
| 242 | `new_header`  |  | Private helper | Constructor |  |
| 283 | `check` ⚠ |  | Private helper | Other / internal logic |  |
| 328 | `with_mut`  | `CoreStage<T>` | Crate-internal | Constructor |  |
| 340 | `enter`  | `TaskIdGuard` | Private helper | Runtime/task control |  |
| 348 | `drop`  | `Drop for TaskIdGuard` | Trait impl | Drop / cleanup |  |
| 367 | `poll`  | `Core<T, S>` | Crate-internal | Poll function | Polls the future. |
| 396 | `drop_future_or_output`  | `Core<T, S>` | Crate-internal | Lifecycle / ref-count | Drops the future. |
| 408 | `store_output`  | `Core<T, S>` | Crate-internal | Other / internal logic | Stores the task output. |
| 420 | `take_output`  | `Core<T, S>` | Crate-internal | Data movement | Takes the task output. |
| 432 | `set_stage` ⚠ | `Core<T, S>` | Private helper | Configuration / setter |  |
| 439 | `set_next` ⚠ | `Header` | Crate-internal | Configuration / setter |  |
| 446 | `set_owner_id` ⚠ | `Header` | Crate-internal | Configuration / setter |  |
| 450 | `get_owner_id`  | `Header` | Crate-internal | Accessor / query |  |
| 461 | `get_trailer` ⚠ | `Header` | Crate-internal | Accessor / query | Gets a pointer to the `Trailer` of the task containing this `Header`. |
| 475 | `get_scheduler` ⚠ | `Header` | Crate-internal | Accessor / query | Gets a pointer to the scheduler of the task containing this `Header`. |
| 486 | `get_id_ptr` ⚠ | `Header` | Crate-internal | Accessor / query | Gets a pointer to the id of the task containing this `Header`. |
| 497 | `get_id` ⚠ | `Header` | Crate-internal | Accessor / query | Gets the id of the task containing this `Header`. |
| 509 | `get_spawn_location_ptr` ⚠ | `Header` | Crate-internal | Accessor / query | Gets a pointer to the source code location where the task containing this `Header` was spawned. |
| 528 | `get_spawn_location` ⚠ | `Header` | Crate-internal | Accessor / query | Gets the source code location where the task containing this `Header` was spawned |
| 539 | `get_tracing_id` ⚠ | `Header` | Crate-internal | Accessor / query | Gets the tracing id of the task containing this `Header`. |
| 549 | `set_scheduled_at` ⚠ | `Header` | Crate-internal | Configuration / setter | Updates the last time this task was scheduled. |
| 554 | `get_scheduled_at`  | `Header` | Crate-internal | Accessor / query | Gets the last time this task was scheduled. |
| 562 | `new`  | `Trailer` | Private helper | Constructor |  |
| 570 | `set_waker` ⚠ | `Trailer` | Crate-internal | Configuration / setter |  |
| 576 | `will_wake` ⚠ | `Trailer` | Crate-internal | Other / internal logic |  |
| 581 | `wake_join`  | `Trailer` | Crate-internal | Wake / park |  |
| 591 | `header_lte_cache_line`  |  | Private helper | Handle / reference plumbing |  |

## `tokio/src/runtime/task/error.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `cancelled`  | `JoinError` | Crate-internal | Lifecycle / ref-count |  |
| 28 | `panic`  | `JoinError` | Crate-internal | Other / internal logic |  |
| 40 | `is_cancelled`  | `JoinError` | Public API | Accessor / query | Returns true if the error was caused by the task being cancelled. |
| 63 | `is_panic`  | `JoinError` | Public API | Accessor / query | Returns true if the error was caused by the task panicking. |
| 93 | `into_panic`  | `JoinError` | Public API | Conversion | Consumes the join error, returning the object with which the task panicked. |
| 119 | `try_into_panic`  | `JoinError` | Public API | Non-blocking attempt | Consumes the join error, returning the object with which the task panicked if the task terminated due to a panic. |
| 130 | `id`  | `JoinError` | Public API | Accessor / query | Returns a [task ID] that identifies the task which errored relative to other currently spawned tasks. |
| 136 | `fmt`  | `fmt::Display for JoinError` | Trait impl | Formatting |  |
| 156 | `fmt`  | `fmt::Debug for JoinError` | Trait impl | Formatting |  |
| 172 | `from`  | `From<JoinError> for io::Error` | Trait impl | Conversion |  |
| 180 | `panic_payload_as_str`  |  | Private helper | Other / internal logic |  |

## `tokio/src/runtime/task/harness.rs` (29)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `from_raw` ⚠ | `Harness<T, S>` | Crate-internal | Conversion |  |
| 32 | `header_ptr`  | `Harness<T, S>` | Private helper | Handle / reference plumbing |  |
| 36 | `header`  | `Harness<T, S>` | Private helper | Handle / reference plumbing |  |
| 40 | `state`  | `Harness<T, S>` | Private helper | Other / internal logic |  |
| 44 | `trailer`  | `Harness<T, S>` | Private helper | Other / internal logic |  |
| 48 | `core`  | `Harness<T, S>` | Private helper | Other / internal logic |  |
| 57 | `drop_reference`  | `RawTask` | Crate-internal | Lifecycle / ref-count |  |
| 68 | `wake_by_val`  | `RawTask` | Crate-internal | Wake / park | This call consumes a ref-count and notifies the task. |
| 96 | `wake_by_ref`  | `RawTask` | Crate-internal | Wake / park | This call notifies the task. |
| 118 | `remote_abort`  | `RawTask` | Crate-internal | Other / internal logic | Remotely aborts the task. |
| 133 | `try_set_join_waker`  | `RawTask` | Crate-internal | Non-blocking attempt | Try to set the waker notified when the task is complete. |
| 143 | `drop_reference`  | `Harness<T, S>` | Crate-internal | Lifecycle / ref-count |  |
| 153 | `poll`  | `Harness<T, S>` | Crate-internal | Poll function | Polls the inner future. |
| 193 | `poll_inner`  | `Harness<T, S>` | Private helper | Poll function | Polls the task and cancel it if necessary. |
| 199 | `transition_result_to_poll_future`  |  | Private helper | State transition |  |
| 240 | `shutdown`  | `Harness<T, S>` | Crate-internal | Runtime/task control | Forcibly shuts down the task. |
| 253 | `dealloc`  | `Harness<T, S>` | Crate-internal | Lifecycle / ref-count |  |
| 281 | `try_read_output`  | `Harness<T, S>` | Crate-internal | Non-blocking attempt | Read the task output into `dst`. |
| 287 | `drop_join_handle_slow`  | `Harness<T, S>` | Crate-internal | Lifecycle / ref-count |  |
| 331 | `complete`  | `Harness<T, S>` | Private helper | Runtime/task control | Completes the task. |
| 394 | `release`  | `Harness<T, S>` | Private helper | Locking / permits | Releases the task from the scheduler. |
| 415 | `get_new_task`  | `Harness<T, S>` | Private helper | Accessor / query | Creates a new task that holds its own ref-count. |
| 422 | `can_read_output`  |  | Private helper | Other / internal logic |  |
| 466 | `set_join_waker`  |  | Private helper | Configuration / setter |  |
| 502 | `cancel_task`  |  | Private helper | Lifecycle / ref-count | Cancels the task and store the appropriate error in the stage field. |
| 511 | `panic_result_to_join_error`  |  | Private helper | Other / internal logic |  |
| 523 | `poll_future`  |  | Private helper | Poll function | Polls the future. |
| 530 | `drop`  | `Drop for Guard<'a, T, S>` | Trait impl | Drop / cleanup |  |
| 562 | `panic_to_error`  |  | Private helper | Other / internal logic |  |

## `tokio/src/runtime/task/id.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 45 | `id`  |  | Public API | Accessor / query | Returns the [`Id`] of the currently running task. |
| 58 | `try_id`  |  | Public API | Non-blocking attempt | Returns the [`Id`] of the currently running task, or `None` if called outside of a task. |
| 63 | `fmt`  | `fmt::Display for Id` | Trait impl | Formatting |  |
| 69 | `next`  | `Id` | Crate-internal | Combinator / iteration |  |
| 88 | `as_u64`  | `Id` | Crate-internal | Conversion |  |

## `tokio/src/runtime/task/join.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 176 | `new`  | `JoinHandle<T>` | Crate-internal | Constructor |  |
| 227 | `abort`  | `JoinHandle<T>` | Public API | Lifecycle / ref-count | Abort the task associated with the handle. |
| 258 | `is_finished`  | `JoinHandle<T>` | Public API | Accessor / query | Checks if the task associated with this `JoinHandle` has finished. |
| 264 | `set_join_waker`  | `JoinHandle<T>` | Crate-internal | Configuration / setter | Set the waker that is notified when the task completes. |
| 307 | `abort_handle`  | `JoinHandle<T>` | Public API | Lifecycle / ref-count | Returns a new `AbortHandle` that can be used to remotely abort this task. |
| 316 | `id`  | `JoinHandle<T>` | Public API | Accessor / query | Returns a [task ID] that uniquely identifies this task relative to other currently spawned tasks. |
| 327 | `poll`  | `Future for JoinHandle<T>` | Trait impl | Future impl (poll) |  |
| 358 | `drop`  | `Drop for JoinHandle<T>` | Trait impl | Drop / cleanup |  |
| 371 | `fmt`  | `fmt::Debug for JoinHandle<T>` | Trait impl | Formatting |  |

## `tokio/src/runtime/task/list.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `get_next_id`  |  | Private helper | Accessor / query |  |
| 48 | `get_next_id`  |  | Private helper | Accessor / query |  |
| 76 | `new`  | `OwnedTasks<S>` | Crate-internal | Constructor |  |
| 87 | `bind`  | `OwnedTasks<S>` | Crate-internal | Networking | Binds the provided task to this `OwnedTasks` instance. |
| 109 | `bind_local` ⚠ | `OwnedTasks<S>` | Crate-internal | Networking | Bind a task that isn't safe to transfer across thread boundaries. |
| 127 | `bind_inner` ⚠ | `OwnedTasks<S>` | Private helper | Networking | The part of `bind` that's the same for every type of future. |
| 152 | `assert_owner`  | `OwnedTasks<S>` | Crate-internal | Debugging / tracing | Asserts that the given task is owned by this `OwnedTasks` and convert it to a `LocalNotified`, giving the thread permission to poll this task. |
| 167 | `close_and_shutdown_all`  | `OwnedTasks<S>` | Crate-internal | Data movement | Shuts down all tasks in the collection. |
| 186 | `get_shard_size`  | `OwnedTasks<S>` | Crate-internal | Accessor / query |  |
| 190 | `num_alive_tasks`  | `OwnedTasks<S>` | Crate-internal | Accessor / query |  |
| 196 | `spawned_tasks_count`  | `OwnedTasks<S>` | Crate-internal | Runtime/task control |  |
| 202 | `remove`  | `OwnedTasks<S>` | Crate-internal | Data movement |  |
| 214 | `is_empty`  | `OwnedTasks<S>` | Crate-internal | Accessor / query |  |
| 229 | `gen_sharded_list_size`  | `OwnedTasks<S>` | Private helper | Other / internal logic | Generates the size of the sharded list based on the number of worker threads. |
| 238 | `for_each`  | `OwnedTasks<S>` | Crate-internal | Combinator / iteration | Locks the tasks, and calls `f` on an iterator over them. |
| 248 | `new`  | `LocalOwnedTasks<S>` | Crate-internal | Constructor |  |
| 259 | `bind`  | `LocalOwnedTasks<S>` | Crate-internal | Networking |  |
| 293 | `close_and_shutdown_all`  | `LocalOwnedTasks<S>` | Crate-internal | Data movement | Shuts down all tasks in the collection. |
| 304 | `remove`  | `LocalOwnedTasks<S>` | Crate-internal | Data movement |  |
| 320 | `assert_owner`  | `LocalOwnedTasks<S>` | Crate-internal | Debugging / tracing | Asserts that the given task is owned by this `LocalOwnedTasks` and convert it to a `LocalNotified`, giving the thread permission to poll this task. |
| 333 | `with_inner`  | `LocalOwnedTasks<S>` | Private helper | Constructor |  |
| 343 | `is_closed`  | `LocalOwnedTasks<S>` | Crate-internal | Accessor / query |  |
| 347 | `is_empty`  | `LocalOwnedTasks<S>` | Crate-internal | Accessor / query |  |
| 359 | `test_id_not_broken`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/task/mod.rs` (42)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 248 | `set_scheduled_at`  | `Notified<S>` | Crate-internal | Configuration / setter |  |
| 274 | `task_meta`  | `LocalNotified<S>` | Crate-internal | Other / internal logic |  |
| 281 | `get_scheduled_at`  | `LocalNotified<S>` | Crate-internal | Accessor / query |  |
| 312 | `release`  | `trait Schedule` | Trait method (declaration/default) | Locking / permits | The task has completed work and is ready to be released. |
| 315 | `schedule`  | `trait Schedule` | Trait method (declaration/default) | Runtime/task control | Schedule the task |
| 317 | `hooks`  | `trait Schedule` | Trait method (declaration/default) | Other / internal logic |  |
| 321 | `yield_now`  | `trait Schedule` | Trait method (declaration/default) | Other / internal logic | Schedule the task to run in the near future, yielding the thread to other tasks. |
| 326 | `unhandled_panic`  | `trait Schedule` | Trait method (declaration/default) | Other / internal logic | Polling the task resulted in a panic. |
| 336 | `new_task`  |  | Private helper | Constructor | This is the constructor for a new task. |
| 370 | `unowned`  |  | Crate-internal | Other / internal logic | Creates a new task with an associated join handle. |
| 402 | `new` ⚠ | `Task<S>` | Private helper | Constructor |  |
| 412 | `from_raw` ⚠ | `Task<S>` | Private helper | Conversion | # Safety `ptr` must be a valid pointer to a [`Header`]. |
| 417 | `as_raw`  | `Task<S>` | Crate-internal | Conversion |  |
| 422 | `header`  | `Task<S>` | Private helper | Handle / reference plumbing |  |
| 426 | `header_ptr`  | `Task<S>` | Private helper | Handle / reference plumbing |  |
| 435 | `id`  | `Task<S>` | Crate-internal | Accessor / query | Returns a [task ID] that uniquely identifies this task relative to other currently spawned tasks. |
| 441 | `spawned_at`  | `Task<S>` | Crate-internal | Runtime/task control |  |
| 450 | `task_meta`  | `Task<S>` | Crate-internal | Other / internal logic |  |
| 467 | `notify_for_tracing`  | `Task<S>` | Crate-internal | Wake / park | Notify the task for task dumping. |
| 481 | `header`  | `Notified<S>` | Private helper | Handle / reference plumbing |  |
| 487 | `task_id`  | `Notified<S>` | Crate-internal | Other / internal logic |  |
| 496 | `from_raw` ⚠ | `Notified<S>` | Crate-internal | Conversion | # Safety [`RawTask::ptr`] must be a valid pointer to a [`Header`]. |
| 502 | `into_raw`  | `Notified<S>` | Crate-internal | Conversion |  |
| 511 | `shutdown`  | `Task<S>` | Crate-internal | Runtime/task control | Preemptively cancels the task as part of the shutdown process. |
| 520 | `run`  | `LocalNotified<S>` | Crate-internal | Runtime/task control | Runs the task. |
| 530 | `waker_ref`  | `LocalNotified<S>` | Crate-internal | Wake / park | Returns a `WakerRef` borrowing from this task. |
| 540 | `into_notified`  | `UnownedTask<S>` | Test | Conversion |  |
| 544 | `into_task`  | `UnownedTask<S>` | Private helper | Conversion |  |
| 558 | `run`  | `UnownedTask<S>` | Crate-internal | Runtime/task control |  |
| 574 | `shutdown`  | `UnownedTask<S>` | Crate-internal | Runtime/task control |  |
| 580 | `drop`  | `Drop for Task<S>` | Trait impl | Drop / cleanup |  |
| 590 | `drop`  | `Drop for UnownedTask<S>` | Trait impl | Drop / cleanup |  |
| 600 | `fmt`  | `fmt::Debug for Task<S>` | Trait impl | Formatting |  |
| 606 | `fmt`  | `fmt::Debug for Notified<S>` | Trait impl | Formatting |  |
| 618 | `as_raw`  | `linked_list::Link for Task<S>` | Trait impl | Intrusive-list link |  |
| 622 | `from_raw` ⚠ | `linked_list::Link for Task<S>` | Trait impl | Intrusive-list link |  |
| 626 | `pointers` ⚠ | `linked_list::Link for Task<S>` | Trait impl | Intrusive-list link |  |
| 637 | `get_shard_id` ⚠ | `sharded_list::ShardedListItem for Task<S>` | Trait impl | Accessor / query |  |
| 655 | `from`  | `From<&'static Location<'static>> for SpawnLocation` | Trait impl | Conversion |  |
| 669 | `from`  | `From<&'static Location<'static>> for SpawnLocation` | Trait impl | Conversion |  |
| 676 | `spawn_location_is_zero_sized`  |  | Test | Runtime/task control |  |
| 684 | `capture`  | `SpawnLocation` | Crate-internal | Other / internal logic |  |

## `tokio/src/runtime/task/raw.rs` (30)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 61 | `vtable`  |  | Crate-internal | Other / internal logic | Get the vtable for the requested `T` and `S` generics. |
| 125 | `get_trailer_offset` 🅲 |  | Private helper | Accessor / query | Compute the offset of the `Trailer` field in `Cell<T, S>` using the `#[repr(C)]` algorithm. |
| 152 | `get_core_offset` 🅲 |  | Private helper | Accessor / query | Compute the offset of the `Core<T, S>` field in `Cell<T, S>` using the `#[repr(C)]` algorithm. |
| 168 | `get_id_offset` 🅲 |  | Private helper | Accessor / query | Compute the offset of the `Id` field in `Cell<T, S>` using the `#[repr(C)]` algorithm. |
| 191 | `get_spawn_location_offset` 🅲 |  | Private helper | Accessor / query | Compute the offset of the `&'static Location<'static>` field in `Cell<T, S>` using the `#[repr(C)]` algorithm. |
| 211 | `new`  | `RawTask` | Crate-internal | Constructor |  |
| 237 | `from_raw` ⚠ | `RawTask` | Crate-internal | Conversion | # Safety `ptr` must be a valid pointer to a [`Header`]. |
| 241 | `header_ptr`  | `RawTask` | Crate-internal | Handle / reference plumbing |  |
| 246 | `header_ptr_ref`  | `RawTask` | Crate-internal | Handle / reference plumbing |  |
| 251 | `trailer_ptr`  | `RawTask` | Crate-internal | Other / internal logic |  |
| 256 | `header`  | `RawTask` | Crate-internal | Handle / reference plumbing | Returns a reference to the task's header. |
| 261 | `trailer`  | `RawTask` | Crate-internal | Other / internal logic | Returns a reference to the task's trailer. |
| 266 | `state`  | `RawTask` | Crate-internal | Other / internal logic | Returns a reference to the task's state. |
| 271 | `poll`  | `RawTask` | Crate-internal | Poll function | Safety: mutual exclusion is required to call this function. |
| 276 | `schedule`  | `RawTask` | Crate-internal | Runtime/task control |  |
| 281 | `dealloc`  | `RawTask` | Crate-internal | Lifecycle / ref-count |  |
| 290 | `try_read_output` ⚠ | `RawTask` | Crate-internal | Non-blocking attempt | Safety: `dst` must be a `*mut Poll<super::Result<T::Output>>` where `T` is the future stored by the task. |
| 295 | `drop_join_handle_slow`  | `RawTask` | Crate-internal | Lifecycle / ref-count |  |
| 300 | `drop_abort_handle`  | `RawTask` | Crate-internal | Lifecycle / ref-count |  |
| 305 | `shutdown`  | `RawTask` | Crate-internal | Runtime/task control |  |
| 313 | `ref_inc`  | `RawTask` | Crate-internal | Lifecycle / ref-count | Increment the task's reference count. |
| 322 | `get_queue_next` ⚠ | `RawTask` | Crate-internal | Accessor / query | Get the queue-next pointer This is for usage by the injection queue Safety: make sure only one queue uses this and access is synchronized. |
| 334 | `set_queue_next` ⚠ | `RawTask` | Crate-internal | Configuration / setter | Sets the queue-next pointer This is for usage by the injection queue Safety: make sure only one queue uses this and access is synchronized. |
| 341 | `poll` ⚠ |  | Private helper | Poll function |  |
| 346 | `schedule` ⚠ |  | Private helper | Runtime/task control |  |
| 355 | `dealloc` ⚠ |  | Private helper | Lifecycle / ref-count |  |
| 360 | `try_read_output` ⚠ |  | Private helper | Non-blocking attempt |  |
| 371 | `drop_join_handle_slow` ⚠ |  | Private helper | Lifecycle / ref-count |  |
| 376 | `drop_abort_handle` ⚠ |  | Private helper | Lifecycle / ref-count |  |
| 381 | `shutdown` ⚠ |  | Private helper | Runtime/task control |  |

## `tokio/src/runtime/task/state.rs` (41)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 102 | `new`  | `State` | Crate-internal | Constructor | Returns a task's initial state. |
| 111 | `load`  | `State` | Crate-internal | Other / internal logic | Loads the current state, establishes `Acquire` ordering. |
| 117 | `transition_to_running`  | `State` | Crate-internal | State transition | Attempts to transition the lifecycle to `Running`. |
| 151 | `transition_to_idle`  | `State` | Crate-internal | State transition | Transitions the task from `Running` -> `Idle`. |
| 184 | `transition_to_complete`  | `State` | Crate-internal | State transition | Transitions the task from `Running` -> `Complete`. |
| 198 | `transition_to_terminal`  | `State` | Crate-internal | State transition | Transitions from `Complete` -> `Terminal`, decrementing the reference count the specified number of times. |
| 215 | `transition_to_notified_by_val`  | `State` | Crate-internal | State transition | Transitions the state to `NOTIFIED`. |
| 253 | `transition_to_notified_by_ref`  | `State` | Crate-internal | State transition | Transitions the state to `NOTIFIED`. |
| 286 | `transition_to_notified_for_tracing`  | `State` | Crate-internal | State transition | Transitions the state to `NOTIFIED` if idle and not already notified, increasing the ref count. |
| 303 | `transition_to_notified_and_cancel`  | `State` | Crate-internal | State transition | Sets the cancelled bit and transitions the state to `NOTIFIED` if idle. |
| 338 | `transition_to_shutdown`  | `State` | Crate-internal | State transition | Sets the `CANCELLED` bit and attempts to transition to `Running`. |
| 360 | `drop_join_handle_fast`  | `State` | Crate-internal | Lifecycle / ref-count | Optimistically tries to swap the state assuming the join handle is __immediately__ dropped on spawn. |
| 385 | `transition_to_join_handle_dropped`  | `State` | Crate-internal | State transition | Unsets the `JOIN_INTEREST` flag. |
| 427 | `set_join_waker`  | `State` | Crate-internal | Configuration / setter | Sets the `JOIN_WAKER` bit. |
| 447 | `unset_waker`  | `State` | Crate-internal | Configuration / setter | Unsets the `JOIN_WAKER` bit. |
| 469 | `unset_waker_after_complete`  | `State` | Crate-internal | Configuration / setter | Unsets the `JOIN_WAKER` bit unconditionally after task completion. |
| 476 | `ref_inc`  | `State` | Crate-internal | Lifecycle / ref-count |  |
| 500 | `ref_dec`  | `State` | Crate-internal | Lifecycle / ref-count | Returns `true` if the task should be released. |
| 507 | `ref_dec_twice`  | `State` | Crate-internal | Lifecycle / ref-count | Returns `true` if the task should be released. |
| 513 | `fetch_update_action`  | `State` | Private helper | Other / internal logic |  |
| 535 | `fetch_update`  | `State` | Private helper | Other / internal logic |  |
| 561 | `is_idle`  | `Snapshot` | Crate-internal | Accessor / query | Returns `true` if the task is in an idle state. |
| 566 | `is_notified`  | `Snapshot` | Crate-internal | Accessor / query | Returns `true` if the task has been flagged as notified. |
| 570 | `unset_notified`  | `Snapshot` | Private helper | Configuration / setter |  |
| 574 | `set_notified`  | `Snapshot` | Private helper | Configuration / setter |  |
| 578 | `is_running`  | `Snapshot` | Crate-internal | Accessor / query |  |
| 582 | `set_running`  | `Snapshot` | Private helper | Configuration / setter |  |
| 586 | `unset_running`  | `Snapshot` | Private helper | Configuration / setter |  |
| 590 | `is_cancelled`  | `Snapshot` | Crate-internal | Accessor / query |  |
| 594 | `set_cancelled`  | `Snapshot` | Private helper | Configuration / setter |  |
| 599 | `is_complete`  | `Snapshot` | Crate-internal | Accessor / query | Returns `true` if the task's future has completed execution. |
| 603 | `is_join_interested`  | `Snapshot` | Crate-internal | Accessor / query |  |
| 607 | `unset_join_interested`  | `Snapshot` | Private helper | Configuration / setter |  |
| 611 | `is_join_waker_set`  | `Snapshot` | Crate-internal | Accessor / query |  |
| 615 | `set_join_waker`  | `Snapshot` | Private helper | Configuration / setter |  |
| 619 | `unset_join_waker`  | `Snapshot` | Private helper | Configuration / setter |  |
| 623 | `ref_count`  | `Snapshot` | Crate-internal | Lifecycle / ref-count |  |
| 627 | `ref_inc`  | `Snapshot` | Private helper | Lifecycle / ref-count |  |
| 632 | `ref_dec`  | `Snapshot` | Crate-internal | Lifecycle / ref-count |  |
| 639 | `fmt`  | `fmt::Debug for State` | Trait impl | Formatting |  |
| 646 | `fmt`  | `fmt::Debug for Snapshot` | Trait impl | Formatting |  |

## `tokio/src/runtime/task/waker.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `waker_ref`  |  | Crate-internal | Wake / park | Returns a `WakerRef` which avoids having to preemptively increase the refcount if there is no need to do so. |
| 39 | `deref`  | `ops::Deref for WakerRef<'_, S>` | Trait impl | Deref |  |
| 70 | `clone_waker` ⚠ |  | Private helper | Other / internal logic |  |
| 81 | `drop_waker` ⚠ |  | Private helper | Lifecycle / ref-count |  |
| 93 | `wake_by_val` ⚠ |  | Private helper | Wake / park |  |
| 106 | `wake_by_ref` ⚠ |  | Private helper | Wake / park |  |
| 121 | `raw_waker`  |  | Private helper | Other / internal logic |  |

