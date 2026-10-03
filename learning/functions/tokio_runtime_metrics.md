# `tokio::runtime::metrics` — 112 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 53 |
| Public API | 40 |
| Private helper | 10 |
| Test | 7 |
| Trait impl | 2 |

## `tokio/src/runtime/metrics/batch.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 73 | `new`  | `MetricsBatch` | Crate-internal | Constructor |  |
| 81 | `new_unstable`  | `MetricsBatch` | Private helper | Constructor |  |
| 92 | `new_unstable`  | `MetricsBatch` | Private helper | Constructor |  |
| 130 | `submit`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 141 | `submit_unstable`  | `MetricsBatch` | Private helper | Metrics / counters |  |
| 150 | `submit_unstable`  | `MetricsBatch` | Private helper | Metrics / counters |  |
| 185 | `about_to_park`  | `MetricsBatch` | Crate-internal | Other / internal logic | The worker is about to park. |
| 192 | `about_to_park`  | `MetricsBatch` | Crate-internal | Other / internal logic | The worker is about to park. |
| 207 | `unparked`  | `MetricsBatch` | Crate-internal | Wake / park | The worker was unparked. |
| 212 | `start_processing_scheduled_tasks`  | `MetricsBatch` | Crate-internal | Runtime/task control | Start processing a batch of tasks |
| 217 | `end_processing_scheduled_tasks`  | `MetricsBatch` | Crate-internal | Other / internal logic | Stop processing a batch of tasks |
| 229 | `start_poll`  | `MetricsBatch` | Crate-internal | Runtime/task control | Start polling an individual task |
| 242 | `start_poll`  | `MetricsBatch` | Crate-internal | Runtime/task control | Start polling an individual task |
| 272 | `record_schedule_latency`  | `MetricsBatch` | Crate-internal | Other / internal logic | Record the schedule latency of an additional task polled as part of the current poll operation. |
| 283 | `record_schedule_latency`  | `MetricsBatch` | Crate-internal | Other / internal logic | Record the schedule latency of an additional task polled as part of the current poll operation. |
| 302 | `record_schedule_latency_at`  | `MetricsBatch` | Private helper | Other / internal logic |  |
| 323 | `end_poll`  | `MetricsBatch` | Crate-internal | Other / internal logic | Stop polling an individual task |
| 327 | `end_poll`  | `MetricsBatch` | Crate-internal | Other / internal logic | Stop polling an individual task |
| 338 | `inc_local_schedule_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 341 | `inc_local_schedule_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 352 | `incr_steal_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 355 | `incr_steal_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 363 | `incr_steal_operations`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 366 | `incr_steal_operations`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 374 | `incr_overflow_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 377 | `incr_overflow_count`  | `MetricsBatch` | Crate-internal | Metrics / counters |  |
| 385 | `duration_as_u64`  |  | Crate-internal | Other / internal logic |  |
| 391 | `now`  |  | Private helper | Time / timers | Gate unsupported time metrics for `wasm32-unknown-unknown` <https://github.com/tokio-rs/tokio/issues/7319> |

## `tokio/src/runtime/metrics/histogram.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `default`  | `Default for LegacyBuilder` | Trait impl | Constructor |  |
| 79 | `linear`  | `HistogramConfiguration` | Public API | Other / internal logic | Create a linear bucketed histogram |
| 91 | `log`  | `HistogramConfiguration` | Public API | Other / internal logic | Creates a log-scaled bucketed histogram See [`LogHistogramBuilder`] for information about configuration & defaults |
| 112 | `num_buckets`  | `HistogramType` | Crate-internal | Accessor / query |  |
| 119 | `value_to_bucket`  | `HistogramType` | Private helper | Other / internal logic |  |
| 145 | `bucket_range`  | `HistogramType` | Private helper | Other / internal logic |  |
| 191 | `num_buckets`  | `Histogram` | Crate-internal | Accessor / query |  |
| 196 | `get`  | `Histogram` | Crate-internal | Accessor / query |  |
| 201 | `bucket_range`  | `Histogram` | Crate-internal | Other / internal logic |  |
| 207 | `from_histogram`  | `HistogramBatch` | Crate-internal | Conversion |  |
| 216 | `measure`  | `HistogramBatch` | Crate-internal | Other / internal logic |  |
| 220 | `submit`  | `HistogramBatch` | Crate-internal | Metrics / counters |  |
| 229 | `value_to_bucket`  | `HistogramBatch` | Private helper | Other / internal logic |  |
| 235 | `new`  | `HistogramBuilder` | Crate-internal | Constructor |  |
| 245 | `legacy_mut`  | `HistogramBuilder` | Crate-internal | Other / internal logic |  |
| 250 | `build`  | `HistogramBuilder` | Crate-internal | Constructor |  |
| 280 | `default`  | `Default for HistogramBuilder` | Trait impl | Constructor |  |
| 295 | `linear`  |  | Test | Other / internal logic |  |
| 307 | `test_legacy_builder`  |  | Test | Other / internal logic |  |
| 314 | `log_scale_resolution_1`  |  | Test | Other / internal logic |  |
| 371 | `log_scale_resolution_2`  |  | Test | Other / internal logic |  |
| 460 | `linear_scale_resolution_1`  |  | Test | Other / internal logic |  |
| 516 | `linear_scale_resolution_100`  |  | Test | Other / internal logic |  |
| 590 | `inc_by_more_than_one`  |  | Test | Metrics / counters |  |

## `tokio/src/runtime/metrics/io.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `incr_fd_count`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |
| 18 | `dec_fd_count`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |
| 22 | `incr_ready_count_by`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/metrics/mock.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `new`  | `SchedulerMetrics` | Crate-internal | Constructor |  |
| 14 | `inc_remote_schedule_count`  | `SchedulerMetrics` | Crate-internal | Metrics / counters | Increment the number of tasks scheduled externally |

## `tokio/src/runtime/metrics/runtime.rs` (40)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `new`  | `RuntimeMetrics` | Crate-internal | Constructor |  |
| 48 | `num_workers`  | `RuntimeMetrics` | Public API | Accessor / query | Returns the number of worker threads used by the runtime. |
| 74 | `num_alive_tasks`  | `RuntimeMetrics` | Public API | Accessor / query | Returns the current number of alive tasks in the runtime. |
| 100 | `global_queue_depth`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks currently scheduled in the runtime's global queue. |
| 141 | `worker_total_busy_duration`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the amount of time the given worker thread has been busy. |
| 186 | `worker_park_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the total number of times the given worker thread has parked. |
| 240 | `worker_park_unpark_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the total number of times the given worker thread has parked and unparked. |
| 276 | `num_blocking_threads`  | `RuntimeMetrics` | Public API | Accessor / query | Returns the number of additional threads spawned by the runtime. |
| 282 | `active_tasks_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Renamed to [`RuntimeMetrics::num_alive_tasks`] |
| 309 | `num_idle_blocking_threads`  | `RuntimeMetrics` | Public API | Accessor / query | Returns the number of idle threads, which have spawned by the runtime for `spawn_blocking` calls. |
| 349 | `worker_thread_id`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the thread id of the given worker thread. |
| 359 | `injection_queue_depth`  | `RuntimeMetrics` | Public API | Metrics / counters | Renamed to [`RuntimeMetrics::global_queue_depth`] |
| 397 | `worker_local_queue_depth`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks currently scheduled in the given worker's local queue. |
| 430 | `poll_time_histogram_enabled`  | `RuntimeMetrics` | Public API | Poll function | Returns `true` if the runtime is tracking the distribution of task poll times. |
| 440 | `poll_count_histogram_enabled`  | `RuntimeMetrics` | Public API | Poll function |  |
| 471 | `poll_time_histogram_num_buckets`  | `RuntimeMetrics` | Public API | Poll function | Returns the number of histogram buckets tracking the distribution of task poll times. |
| 485 | `poll_count_histogram_num_buckets`  | `RuntimeMetrics` | Public API | Poll function | Deprecated. |
| 524 | `poll_time_histogram_bucket_range`  | `RuntimeMetrics` | Public API | Poll function | Returns the range of task poll times tracked by the given bucket. |
| 545 | `poll_count_histogram_bucket_range`  | `RuntimeMetrics` | Public API | Poll function | Deprecated. |
| 569 | `blocking_queue_depth`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks currently scheduled in the blocking thread pool, spawned using `spawn_blocking`. |
| 599 | `spawned_tasks_count`  | `RuntimeMetrics` | Public API | Runtime/task control | Returns the number of tasks spawned in this runtime since it was created. |
| 627 | `remote_schedule_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks scheduled from **outside** of the runtime. |
| 642 | `budget_forced_yield_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of times that tasks have been forced to yield back to the scheduler after exhausting their task budgets. |
| 685 | `worker_noop_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of times the given worker thread unparked but performed no work before parking again. |
| 731 | `worker_steal_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks the given worker thread stole from another worker thread. |
| 777 | `worker_steal_operations`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of times the given worker thread stole tasks from another worker thread. |
| 818 | `worker_poll_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks the given worker thread has polled. |
| 863 | `worker_local_schedule_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of tasks scheduled from **within** the runtime on the given worker's local queue. |
| 909 | `worker_overflow_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of times the given worker thread saturated its local queue. |
| 972 | `poll_time_histogram_bucket_count`  | `RuntimeMetrics` | Public API | Poll function | Returns the number of times the given worker polled tasks with a poll duration within the given bucket's range. |
| 983 | `poll_count_histogram_bucket_count`  | `RuntimeMetrics` | Public API | Poll function |  |
| 1018 | `worker_mean_poll_time`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the mean duration of task polls, in nanoseconds. |
| 1060 | `schedule_latency_histogram_enabled`  | `RuntimeMetrics` | Public API | Runtime/task control | Returns `true` if the runtime is tracking the distribution of task schedule latencies. |
| 1090 | `schedule_latency_histogram_num_buckets`  | `RuntimeMetrics` | Public API | Runtime/task control | Returns the number of histogram buckets tracking the distribution of task schedule latencies. |
| 1133 | `schedule_latency_histogram_bucket_range`  | `RuntimeMetrics` | Public API | Runtime/task control | Returns the range of task schedule latencies tracked by the given bucket. |
| 1204 | `schedule_latency_histogram_bucket_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of times the given worker polled tasks with a schedule latency within the given bucket's range. |
| 1241 | `io_driver_fd_registered_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of file descriptors that have been registered with the runtime's I/O driver. |
| 1263 | `io_driver_fd_deregistered_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of file descriptors that have been deregistered by the runtime's I/O driver. |
| 1285 | `io_driver_ready_count`  | `RuntimeMetrics` | Public API | Metrics / counters | Returns the number of ready events processed by the runtime's I/O driver. |
| 1289 | `with_io_driver_metrics`  | `RuntimeMetrics` | Private helper | Constructor |  |

## `tokio/src/runtime/metrics/schedule_latency.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `new`  | `ScheduleLatencyInstant` | Crate-internal | Constructor | Create a new `ScheduleLatencyInstant` using the provided scheduler startup Instant. |
| 27 | `prepare`  | `ScheduleLatencyInstant` | Crate-internal | Other / internal logic | Prepare a context that can calculate the number of nanoseconds elapsed since this task was scheduled. |
| 55 | `elapsed_nanos`  | `ScheduleLatencyContext` | Crate-internal | Other / internal logic | Calculate how many nanoseconds have elapsed between `now` and when this task was last scheduled. |

## `tokio/src/runtime/metrics/schedule_latency_mock.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `new`  | `ScheduleLatencyInstant` | Crate-internal | Constructor |  |
| 15 | `prepare`  | `ScheduleLatencyInstant` | Crate-internal | Other / internal logic |  |

## `tokio/src/runtime/metrics/scheduler.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `new`  | `SchedulerMetrics` | Crate-internal | Constructor |  |
| 27 | `inc_remote_schedule_count`  | `SchedulerMetrics` | Crate-internal | Metrics / counters | Increment the number of tasks scheduled externally |
| 32 | `inc_budget_forced_yield_count`  | `SchedulerMetrics` | Crate-internal | Metrics / counters | Increment the number of tasks forced to yield due to budget exhaustion |

## `tokio/src/runtime/metrics/worker.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 75 | `new`  | `WorkerMetrics` | Crate-internal | Constructor |  |
| 79 | `set_queue_depth`  | `WorkerMetrics` | Crate-internal | Configuration / setter |  |
| 83 | `set_thread_id`  | `WorkerMetrics` | Crate-internal | Configuration / setter |  |
| 89 | `from_config`  | `WorkerMetrics` | Crate-internal | Conversion |  |
| 94 | `from_config`  | `WorkerMetrics` | Crate-internal | Conversion |  |
| 114 | `queue_depth`  | `WorkerMetrics` | Crate-internal | Metrics / counters |  |
| 118 | `thread_id`  | `WorkerMetrics` | Crate-internal | Configuration / setter |  |

