# `tokio::runtime::scheduler::multi_thread` — 177 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 93 |
| Private helper | 62 |
| Trait impl | 20 |
| Trait method (declaration/default) | 2 |

## `tokio/src/runtime/scheduler/multi_thread/counters.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `drop`  | `Drop for super::Counters` | Trait impl | Drop / cleanup |  |
| 29 | `inc_num_inc_notify_local`  |  | Crate-internal | Metrics / counters |  |
| 33 | `inc_num_unparks_local`  |  | Crate-internal | Metrics / counters |  |
| 37 | `inc_num_maintenance`  |  | Crate-internal | Metrics / counters |  |
| 41 | `inc_lifo_schedules`  |  | Crate-internal | Metrics / counters |  |
| 45 | `inc_lifo_capped`  |  | Crate-internal | Metrics / counters |  |
| 52 | `inc_num_inc_notify_local`  |  | Crate-internal | Metrics / counters |  |
| 53 | `inc_num_unparks_local`  |  | Crate-internal | Metrics / counters |  |
| 54 | `inc_num_maintenance`  |  | Crate-internal | Metrics / counters |  |
| 55 | `inc_lifo_schedules`  |  | Crate-internal | Metrics / counters |  |
| 56 | `inc_lifo_capped`  |  | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/scheduler/multi_thread/handle.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 55 | `spawn`  | `Handle` | Crate-internal | Runtime/task control | Spawns a future onto the thread pool |
| 69 | `is_shutdown`  | `Handle` | Crate-internal | Accessor / query |  |
| 74 | `shutdown`  | `Handle` | Crate-internal | Runtime/task control |  |
| 81 | `bind_new_task`  | `Handle` | Crate-internal | Networking |  |
| 108 | `release`  | `task::Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 112 | `schedule`  | `task::Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 116 | `hooks`  | `task::Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 122 | `yield_now`  | `task::Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 128 | `owned_id`  | `Handle` | Crate-internal | Other / internal logic |  |
| 132 | `name`  | `Handle` | Crate-internal | Other / internal logic |  |
| 138 | `fmt`  | `fmt::Debug for Handle` | Trait impl | Formatting |  |

## `tokio/src/runtime/scheduler/multi_thread/handle/metrics.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `num_workers`  | `Handle` | Crate-internal | Accessor / query |  |
| 13 | `num_alive_tasks`  | `Handle` | Crate-internal | Accessor / query |  |
| 17 | `injection_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 21 | `worker_metrics`  | `Handle` | Crate-internal | Metrics / counters |  |
| 27 | `spawned_tasks_count`  | `Handle` | Crate-internal | Runtime/task control |  |
| 32 | `num_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 36 | `num_idle_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 40 | `scheduler_metrics`  | `Handle` | Crate-internal | Other / internal logic |  |
| 44 | `worker_local_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 48 | `blocking_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/scheduler/multi_thread/handle/taskdump.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 6 | `dump` 🅰 | `Handle` | Crate-internal | Debugging / tracing |  |

## `tokio/src/runtime/scheduler/multi_thread/idle.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `new`  | `Idle` | Crate-internal | Constructor |  |
| 51 | `worker_to_notify`  | `Idle` | Crate-internal | Metrics / counters | If there are no workers actively searching, returns the index of a worker currently sleeping. |
| 86 | `transition_worker_to_parked`  | `Idle` | Crate-internal | State transition | Returns `true` if the worker needs to do a final check for submitted work. |
| 108 | `transition_worker_to_searching`  | `Idle` | Crate-internal | State transition |  |
| 125 | `transition_worker_from_searching`  | `Idle` | Crate-internal | State transition | A lightweight transition from searching -> running. |
| 133 | `unpark_worker_by_id`  | `Idle` | Crate-internal | Wake / park | Unpark a specific worker. |
| 152 | `is_parked`  | `Idle` | Crate-internal | Accessor / query | Returns `true` if `worker_id` is contained in the sleep set. |
| 157 | `notify_should_wakeup`  | `Idle` | Private helper | Wake / park |  |
| 167 | `new`  | `State` | Private helper | Constructor |  |
| 175 | `load`  | `State` | Private helper | Other / internal logic |  |
| 179 | `unpark_one`  | `State` | Private helper | Wake / park |  |
| 183 | `inc_num_searching`  | `State` | Private helper | Metrics / counters |  |
| 188 | `dec_num_searching`  | `State` | Private helper | Metrics / counters | Returns `true` if this is the final searching worker |
| 196 | `dec_num_unparked`  | `State` | Private helper | Metrics / counters | Track a sleeping worker Returns `true` if this is the final searching worker. |
| 209 | `num_searching`  | `State` | Private helper | Accessor / query | Number of workers currently searching |
| 214 | `num_unparked`  | `State` | Private helper | Accessor / query | Number of workers currently unparked |
| 220 | `from`  | `From<usize> for State` | Trait impl | Conversion |  |
| 226 | `from`  | `From<State> for usize` | Trait impl | Conversion |  |
| 232 | `fmt`  | `fmt::Debug for State` | Trait impl | Formatting |  |
| 241 | `test_state`  |  | Private helper | Other / internal logic |  |

## `tokio/src/runtime/scheduler/multi_thread/mod.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 56 | `new`  | `MultiThread` | Crate-internal | Constructor |  |
| 85 | `block_on`  | `MultiThread` | Crate-internal | Runtime/task control | Blocks the current thread waiting for the future to complete. |
| 94 | `shutdown`  | `MultiThread` | Crate-internal | Runtime/task control |  |
| 103 | `fmt`  | `fmt::Debug for MultiThread` | Trait impl | Formatting |  |

## `tokio/src/runtime/scheduler/multi_thread/overflow.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `push`  | `trait Overflow` | Trait method (declaration/default) | Data movement |  |
| 9 | `push_batch`  | `trait Overflow` | Trait method (declaration/default) | Data movement |  |
| 16 | `push`  | `Overflow<T> for RefCell<Vec<task::Notified<T>>>` | Trait impl | Data movement |  |
| 20 | `push_batch`  | `Overflow<T> for RefCell<Vec<task::Notified<T>>>` | Trait impl | Data movement |  |

## `tokio/src/runtime/scheduler/multi_thread/park.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 57 | `new`  | `Parker` | Crate-internal | Constructor |  |
| 70 | `unpark`  | `Parker` | Crate-internal | Wake / park |  |
| 76 | `park`  | `Parker` | Crate-internal | Wake / park |  |
| 85 | `park_timeout`  | `Parker` | Crate-internal | Wake / park | Parks the current thread for up to `duration`. |
| 106 | `shutdown`  | `Parker` | Crate-internal | Runtime/task control |  |
| 112 | `clone`  | `Clone for Parker` | Trait impl | Clone |  |
| 125 | `unpark`  | `Unparker` | Crate-internal | Wake / park |  |
| 132 | `park`  | `Inner` | Private helper | Wake / park | Parks the current thread for at most `dur`. |
| 158 | `park_condvar`  | `Inner` | Private helper | Wake / park | Parks the current thread using a condvar for up to `duration`. |
| 228 | `park_driver`  | `Inner` | Private helper | Wake / park |  |
| 277 | `unpark`  | `Inner` | Private helper | Wake / park |  |
| 292 | `unpark_condvar`  | `Inner` | Private helper | Wake / park |  |
| 309 | `shutdown`  | `Inner` | Private helper | Runtime/task control |  |

## `tokio/src/runtime/scheduler/multi_thread/queue.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 77 | `make_fixed_size`  |  | Private helper | Other / internal logic |  |
| 85 | `local`  |  | Crate-internal | Other / internal logic | Create a new local run-queue |
| 105 | `len`  | `Local<T>` | Crate-internal | Accessor / query | Returns the number of entries in the queue |
| 113 | `remaining_slots`  | `Local<T>` | Crate-internal | Other / internal logic | How many tasks can be pushed into the queue |
| 121 | `max_capacity`  | `Local<T>` | Crate-internal | Configuration / setter |  |
| 129 | `has_tasks`  | `Local<T>` | Crate-internal | Accessor / query | Returns false if there are any entries in the queue Separate to `is_stealable` so that refactors of `is_stealable` to "protect" some tasks from stealing won't affect this |
| 139 | `push_back`  | `Local<T>` | Crate-internal | Data movement | Pushes a batch of tasks to the back of the queue. |
| 188 | `push_back_or_overflow`  | `Local<T>` | Crate-internal | Data movement | Pushes a task to the back of the local queue, if there is not enough capacity in the queue, this triggers the overflow operation. |
| 226 | `push_back_finish`  | `Local<T>` | Private helper | Data movement |  |
| 253 | `push_overflow`  | `Local<T>` | Private helper | Data movement | Moves a batch of tasks into the inject queue. |
| 328 | `next`  | `Iterator for BatchTaskIter<'a, T>` | Trait impl | Iterator |  |
| 361 | `pop`  | `Local<T>` | Crate-internal | Data movement | Pops a task from the local queue. |
| 404 | `len`  | `Steal<T>` | Crate-internal | Accessor / query | Returns the number of entries in the queue |
| 412 | `is_empty`  | `Steal<T>` | Crate-internal | Accessor / query | Return true if the queue is empty, false if there are any entries in the queue |
| 417 | `steal_into`  | `Steal<T>` | Crate-internal | Data movement | Steals half the tasks from self and place them into `dst`. |
| 472 | `steal_into2`  | `Steal<T>` | Private helper | Data movement |  |
| 566 | `clone`  | `Clone for Steal<T>` | Trait impl | Clone |  |
| 572 | `drop`  | `Drop for Local<T>` | Trait impl | Drop / cleanup |  |
| 581 | `len`  |  | Private helper | Accessor / query | Calculate the length of the queue using the head and tail. |
| 587 | `unpack`  |  | Private helper | Other / internal logic | Split the head value into the real head and the index a stealer is working on. |
| 595 | `pack`  |  | Private helper | Other / internal logic | Join the two head values |
| 600 | `test_local_queue_capacity`  |  | Private helper | Other / internal logic |  |

## `tokio/src/runtime/scheduler/multi_thread/stats.rs` (14)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `new`  | `Stats` | Crate-internal | Constructor |  |
| 56 | `tuned_global_queue_interval`  | `Stats` | Crate-internal | Other / internal logic |  |
| 70 | `submit`  | `Stats` | Crate-internal | Metrics / counters |  |
| 74 | `about_to_park`  | `Stats` | Crate-internal | Other / internal logic |  |
| 78 | `unparked`  | `Stats` | Crate-internal | Wake / park |  |
| 82 | `inc_local_schedule_count`  | `Stats` | Crate-internal | Metrics / counters |  |
| 86 | `start_processing_scheduled_tasks`  | `Stats` | Crate-internal | Runtime/task control |  |
| 93 | `end_processing_scheduled_tasks`  | `Stats` | Crate-internal | Other / internal logic |  |
| 117 | `start_poll`  | `Stats` | Crate-internal | Runtime/task control |  |
| 127 | `record_schedule_latency`  | `Stats` | Crate-internal | Other / internal logic |  |
| 134 | `end_poll`  | `Stats` | Crate-internal | Other / internal logic |  |
| 138 | `incr_steal_count`  | `Stats` | Crate-internal | Metrics / counters |  |
| 142 | `incr_steal_operations`  | `Stats` | Crate-internal | Metrics / counters |  |
| 146 | `incr_overflow_count`  | `Stats` | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/scheduler/multi_thread/trace.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `new`  | `TraceStatus` | Crate-internal | Constructor |  |
| 27 | `trace_requested`  | `TraceStatus` | Crate-internal | Debugging / tracing |  |
| 31 | `start_trace_request` 🅰 | `TraceStatus` | Crate-internal | Runtime/task control |  |
| 42 | `stash_result`  | `TraceStatus` | Crate-internal | Other / internal logic |  |
| 47 | `take_result`  | `TraceStatus` | Crate-internal | Data movement |  |
| 51 | `end_trace_request` 🅰 | `TraceStatus` | Crate-internal | Async operation |  |

## `tokio/src/runtime/scheduler/multi_thread/trace_mock.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `new`  | `TraceStatus` | Crate-internal | Constructor |  |
| 8 | `trace_requested`  | `TraceStatus` | Crate-internal | Debugging / tracing |  |

## `tokio/src/runtime/scheduler/multi_thread/worker.rs` (54)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 272 | `create`  |  | Crate-internal | Constructor |  |
| 364 | `block_in_place`  |  | Crate-internal | Other / internal logic |  |
| 375 | `drop`  | `Drop for Reset` | Trait impl | Drop / cleanup |  |
| 420 | `maybe_move_runtime`  |  | Private helper | Other / internal logic |  |
| 512 | `launch`  | `Launch` | Crate-internal | Other / internal logic |  |
| 519 | `run`  |  | Private helper | Runtime/task control |  |
| 524 | `drop`  | `Drop for AbortOnPanic` | Trait impl | Drop / cleanup |  |
| 570 | `run`  | `Context` | Private helper | Runtime/task control |  |
| 647 | `run_task`  | `Context` | Private helper | Runtime/task control | Running a task may consume the core. |
| 798 | `reset_lifo_enabled`  | `Context` | Private helper | Other / internal logic |  |
| 802 | `assert_lifo_enabled_is_correct`  | `Context` | Private helper | Debugging / tracing |  |
| 809 | `maintenance`  | `Context` | Private helper | Other / internal logic |  |
| 839 | `park`  | `Context` | Private helper | Wake / park | Parks the worker thread while waiting for tasks to execute. |
| 869 | `park_yield`  | `Context` | Private helper | Wake / park |  |
| 873 | `park_internal`  | `Context` | Private helper | Wake / park |  |
| 936 | `defer`  | `Context` | Crate-internal | Runtime/task control |  |
| 958 | `maintain_local_timers_before_parking`  | `Context` | Private helper | Other / internal logic | Maintain local timers before parking the resource driver. |
| 1026 | `maintain_local_timers_after_parking`  | `Context` | Private helper | Other / internal logic | Maintain local timers after unparking the resource driver. |
| 1054 | `with_core`  | `Context` | Private helper | Constructor |  |
| 1065 | `with_time_temp_local_context`  | `Context` | Crate-internal | Constructor |  |
| 1078 | `worker_index`  | `Context` | Crate-internal | Metrics / counters |  |
| 1085 | `tick`  | `Core` | Private helper | Time / timers | Increment the tick |
| 1090 | `next_task`  | `Core` | Private helper | Other / internal logic | Return the next notified task available to this worker. |
| 1158 | `next_local_task`  | `Core` | Private helper | Other / internal logic |  |
| 1167 | `steal_work`  | `Core` | Private helper | Data movement | Function responsible for stealing tasks from another worker Note: Only if less than half the workers are searching for tasks to steal a new worker will actually try to steal. |
| 1197 | `transition_to_searching`  | `Core` | Private helper | State transition |  |
| 1205 | `transition_from_searching`  | `Core` | Private helper | State transition |  |
| 1214 | `has_tasks`  | `Core` | Private helper | Accessor / query |  |
| 1218 | `should_notify_others`  | `Core` | Private helper | Other / internal logic |  |
| 1230 | `transition_to_parked`  | `Core` | Private helper | State transition | Prepares the worker state for parking. |
| 1257 | `transition_from_parked`  | `Core` | Private helper | State transition | Returns `true` if the transition happened. |
| 1289 | `maintenance`  | `Core` | Private helper | Other / internal logic | Runs maintenance work such as checking the pool's state. |
| 1306 | `pre_shutdown`  | `Core` | Private helper | Other / internal logic | Signals all tasks to shut down, and waits for them to complete. |
| 1323 | `shutdown`  | `Core` | Private helper | Runtime/task control | Shuts down the core. |
| 1333 | `tune_global_queue_interval`  | `Core` | Private helper | Other / internal logic |  |
| 1347 | `inject`  | `Worker` | Private helper | Other / internal logic | Returns a reference to the scheduler's injection queue. |
| 1353 | `schedule_task`  | `Handle` | Crate-internal | Runtime/task control |  |
| 1379 | `schedule_option_task_without_yield`  | `Handle` | Crate-internal | Runtime/task control |  |
| 1385 | `schedule_local`  | `Handle` | Private helper | Runtime/task control |  |
| 1419 | `next_remote_task`  | `Handle` | Private helper | Other / internal logic |  |
| 1423 | `push_remote_task`  | `Handle` | Private helper | Data movement |  |
| 1430 | `push_remote_timer`  | `Handle` | Crate-internal | Data movement |  |
| 1440 | `take_remote_timers`  | `Handle` | Crate-internal | Data movement |  |
| 1450 | `close`  | `Handle` | Crate-internal | Data movement |  |
| 1459 | `notify_parked_local`  | `Handle` | Private helper | Wake / park | Notify a parked worker. |
| 1471 | `notify_parked_remote`  | `Handle` | Private helper | Wake / park |  |
| 1477 | `notify_all`  | `Handle` | Crate-internal | Wake / park |  |
| 1483 | `notify_if_work_pending`  | `Handle` | Private helper | Wake / park |  |
| 1497 | `transition_worker_from_searching`  | `Handle` | Private helper | State transition | Returns `true` if another parked worker was notified, `false` otherwise. |
| 1511 | `shutdown_core`  | `Handle` | Private helper | Runtime/task control | Signals that a worker has observed the shutdown signal and has replaced its core back into its handle. |
| 1533 | `ptr_eq`  | `Handle` | Private helper | Handle / reference plumbing |  |
| 1539 | `push`  | `Overflow<Arc<Handle>> for Handle` | Trait impl | Data movement |  |
| 1543 | `push_batch`  | `Overflow<Arc<Handle>> for Handle` | Trait impl | Data movement |  |
| 1559 | `with_current`  |  | Private helper | Constructor |  |

## `tokio/src/runtime/scheduler/multi_thread/worker/metrics.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `injection_queue_depth`  | `Shared` | Crate-internal | Metrics / counters |  |
| 11 | `worker_local_queue_depth`  | `Shared` | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/scheduler/multi_thread/worker/taskdump.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `trace_core`  | `Handle` | Crate-internal | Debugging / tracing |  |
| 59 | `steal_all`  | `Shared` | Crate-internal | Data movement | Steal all tasks from remotes into a single local queue. |

## `tokio/src/runtime/scheduler/multi_thread/worker/taskdump_mock.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `trace_core`  | `Handle` | Crate-internal | Debugging / tracing |  |

