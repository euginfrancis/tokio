# `tokio::runtime` — 227 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 88 |
| Crate-internal | 76 |
| Private helper | 50 |
| Trait impl | 12 |
| Test | 1 |

## `tokio/src/runtime/builder.rs` (53)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 253 | `sharded_blocking_queue_default`  |  | Private helper | Other / internal logic | The default for the `sharded_blocking_queue` option: enabled iff the `TOKIO_UNSTABLE_SHARDED_BLOCKING_QUEUE` environment variable is set to a value other than `0`. |
| 278 | `new_current_thread`  | `Builder` | Public API | Constructor | Returns a new builder with the current thread scheduler selected. |
| 293 | `new_multi_thread`  | `Builder` | Public API | Constructor | Returns a new builder with the multi thread scheduler selected. |
| 302 | `new`  | `Builder` | Crate-internal | Constructor | Returns a new runtime builder initialized with default configuration values. |
| 398 | `enable_all`  | `Builder` | Public API | Configuration / setter | Enables both I/O and time drivers. |
| 450 | `enable_alt_timer`  | `Builder` | Public API | Configuration / setter |  |
| 485 | `enable_eager_driver_handoff`  | `Builder` | Public API | Configuration / setter | Enable eager hand-off of the I/O and time drivers for multi-threaded runtimes, which is disabled by default. |
| 526 | `enable_sharded_blocking_queue`  | `Builder` | Public API | Configuration / setter | Enables the sharded `spawn_blocking` queue, which is disabled by default. |
| 582 | `worker_threads`  | `Builder` | Public API | Metrics / counters | Sets the number of worker threads the `Runtime` will use. |
| 633 | `max_blocking_threads`  | `Builder` | Public API | Configuration / setter | Specifies the limit for additional threads spawned by the Runtime. |
| 657 | `thread_name`  | `Builder` | Public API | Configuration / setter | Sets name of threads spawned by the `Runtime`'s thread pool. |
| 684 | `name`  | `Builder` | Public API | Other / internal logic | Sets the name of the runtime. |
| 713 | `thread_name_fn`  | `Builder` | Public API | Configuration / setter | Sets a function used to generate the name of threads spawned by the `Runtime`'s thread pool. |
| 743 | `thread_stack_size`  | `Builder` | Public API | Configuration / setter | Sets the stack size (in bytes) for worker threads. |
| 769 | `on_thread_start`  | `Builder` | Public API | Configuration / setter | Executes function `f` after each thread is started but before it starts doing work. |
| 797 | `on_thread_stop`  | `Builder` | Public API | Configuration / setter | Executes function `f` before each thread stops. |
| 878 | `on_thread_park`  | `Builder` | Public API | Configuration / setter | Executes function `f` just before a thread is parked (goes idle). |
| 916 | `on_thread_unpark`  | `Builder` | Public API | Configuration / setter | Executes function `f` just after a thread unparks (starts executing tasks). |
| 966 | `on_task_spawn`  | `Builder` | Public API | Configuration / setter | Executes function `f` just before a task is spawned. |
| 1016 | `on_before_task_poll`  | `Builder` | Public API | Other / internal logic | Executes function `f` just before a task is polled `f` is called within the Tokio context, so functions like [`tokio::spawn`](crate::spawn) can be called, and may result in this callback being invoked |
| 1066 | `on_after_task_poll`  | `Builder` | Public API | Other / internal logic | Executes function `f` just after a task is polled `f` is called within the Tokio context, so functions like [`tokio::spawn`](crate::spawn) can be called, and may result in this callback being invoked  |
| 1115 | `on_task_terminate`  | `Builder` | Public API | Configuration / setter | Executes function `f` just after a task is terminated. |
| 1146 | `build`  | `Builder` | Public API | Constructor | Creates the configured `Runtime`. |
| 1182 | `build_local`  | `Builder` | Public API | Constructor | Creates the configured [`LocalRuntime`]. |
| 1190 | `get_cfg`  | `Builder` | Private helper | Accessor / query |  |
| 1225 | `thread_keep_alive`  | `Builder` | Public API | Configuration / setter | Sets a custom timeout for a thread in the blocking pool. |
| 1267 | `global_queue_interval`  | `Builder` | Public API | Configuration / setter | Sets the number of scheduler ticks after which the scheduler will poll the global task queue. |
| 1308 | `event_interval`  | `Builder` | Public API | Configuration / setter | Sets the number of scheduler ticks after which the scheduler will poll for external events (timers, I/O, and so on). |
| 1374 | `unhandled_panic`  | `Builder` | Public API | Other / internal logic | Configure how the runtime responds to an unhandled panic on a spawned task. |
| 1425 | `disable_lifo_slot`  | `Builder` | Public API | Configuration / setter | Disables the LIFO task scheduler heuristic. |
| 1458 | `rng_seed`  | `Builder` | Public API | Other / internal logic | Specifies the random number generation seed to use within all threads associated with the runtime being built. |
| 1506 | `enable_metrics_poll_time_histogram`  | `Builder` | Public API | Configuration / setter | Enables tracking the distribution of task poll times. |
| 1516 | `enable_metrics_poll_count_histogram`  | `Builder` | Public API | Configuration / setter | Deprecated. |
| 1547 | `metrics_poll_count_histogram_scale`  | `Builder` | Public API | Metrics / counters | Sets the histogram scale for tracking the distribution of task poll times. |
| 1646 | `metrics_poll_time_histogram_configuration`  | `Builder` | Public API | Metrics / counters | Configure the histogram for tracking poll times By default, a linear histogram with 10 buckets each 100 microseconds wide will be used. |
| 1682 | `metrics_poll_count_histogram_resolution`  | `Builder` | Public API | Metrics / counters | Sets the histogram resolution for tracking the distribution of task poll times. |
| 1719 | `metrics_poll_count_histogram_buckets`  | `Builder` | Public API | Metrics / counters | Sets the number of buckets for the histogram tracking the distribution of task poll times. |
| 1725 | `build_current_thread_runtime`  | `Builder` | Private helper | Constructor |  |
| 1738 | `build_current_thread_local_runtime`  | `Builder` | Private helper | Constructor |  |
| 1753 | `build_current_thread_runtime_components`  | `Builder` | Private helper | Constructor |  |
| 1816 | `metrics_poll_count_histogram_builder`  | `Builder` | Private helper | Metrics / counters |  |
| 1824 | `metrics_schedule_latency_histogram_builder`  | `Builder` | Private helper | Metrics / counters |  |
| 1847 | `enable_io`  | `Builder` | Public API | Configuration / setter | Enables the I/O driver. |
| 1875 | `max_io_events_per_tick`  | `Builder` | Public API | Configuration / setter | Sets the max number of I/O events processed per tick. |
| 1921 | `max_io_events_per_busy_tick`  | `Builder` | Public API | Configuration / setter | Sets the max number of I/O events a worker processes when it polls the driver while it still has tasks to run. |
| 1947 | `enable_time`  | `Builder` | Public API | Configuration / setter | Enables the time driver. |
| 1971 | `enable_io_uring`  | `Builder` | Public API | Configuration / setter | Enables the tokio's io_uring driver. |
| 1997 | `start_paused`  | `Builder` | Public API | Runtime/task control | Controls if the runtime's clock starts paused or advancing. |
| 2041 | `track_task_schedule_latency`  | `Builder` | Public API | Other / internal logic | Enables tracking task schedule latency. |
| 2090 | `enable_metrics_schedule_latency_histogram`  | `Builder` | Public API | Configuration / setter | Enables tracking the distribution of task schedule latencies. |
| 2171 | `metrics_schedule_latency_histogram_configuration`  | `Builder` | Public API | Metrics / counters | Configure the histogram for tracking task schedule latencies. |
| 2180 | `build_threaded_runtime`  | `Builder` | Private helper | Constructor |  |
| 2240 | `fmt`  | `fmt::Debug for Builder` | Trait impl | Formatting |  |

## `tokio/src/runtime/context.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 131 | `thread_rng_n`  |  | Crate-internal | Configuration / setter |  |
| 140 | `budget`  |  | Crate-internal | Other / internal logic |  |
| 147 | `thread_id`  |  | Crate-internal | Configuration / setter |  |
| 160 | `set_current_task_id`  |  | Crate-internal | Configuration / setter |  |
| 164 | `current_task_id`  |  | Crate-internal | Other / internal logic |  |
| 168 | `worker_index`  |  | Crate-internal | Metrics / counters |  |
| 173 | `defer`  |  | Crate-internal | Runtime/task control |  |
| 185 | `set_scheduler`  |  | Crate-internal | Configuration / setter |  |
| 194 | `drop`  | `Drop for ClearSchedulerGuard` | Trait impl | Drop / cleanup |  |
| 201 | `clear_scheduler`  |  | Crate-internal | Other / internal logic | Unsets the scheduler context until the guard drops, on unwind too. |
| 206 | `with_scheduler`  |  | Crate-internal | Constructor |  |
| 222 | `with_trace` ⚠ |  | Crate-internal | Constructor | SAFETY: Callers of this function must ensure that trace frames always form a valid linked list. |

## `tokio/src/runtime/driver.rs` (33)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 48 | `new`  | `Driver` | Crate-internal | Constructor |  |
| 68 | `park`  | `Driver` | Crate-internal | Wake / park |  |
| 72 | `park_timeout`  | `Driver` | Crate-internal | Wake / park |  |
| 76 | `shutdown`  | `Driver` | Crate-internal | Runtime/task control |  |
| 82 | `unpark`  | `Handle` | Crate-internal | Wake / park |  |
| 93 | `io`  | `Handle` | Crate-internal | Other / internal logic |  |
| 102 | `signal`  | `Handle` | Crate-internal | Other / internal logic |  |
| 114 | `time`  | `Handle` | Crate-internal | Other / internal logic | Returns a reference to the time driver handle. |
| 121 | `with_time`  | `Handle` | Crate-internal | Constructor |  |
| 128 | `clock`  | `Handle` | Crate-internal | Other / internal logic |  |
| 133 | `now`  | `Handle` | Test | Time / timers |  |
| 156 | `create_io_stack`  |  | Private helper | Constructor |  |
| 177 | `park`  | `IoStack` | Crate-internal | Wake / park |  |
| 184 | `park_timeout`  | `IoStack` | Crate-internal | Wake / park |  |
| 191 | `shutdown`  | `IoStack` | Crate-internal | Runtime/task control |  |
| 200 | `unpark`  | `IoHandle` | Crate-internal | Wake / park |  |
| 207 | `as_ref`  | `IoHandle` | Crate-internal | Conversion |  |
| 222 | `create_io_stack`  |  | Private helper | Constructor |  |
| 229 | `park`  | `IoStack` | Crate-internal | Wake / park |  |
| 233 | `park_timeout`  | `IoStack` | Crate-internal | Wake / park |  |
| 237 | `shutdown`  | `IoStack` | Crate-internal | Runtime/task control |  |
| 242 | `is_enabled`  | `IoStack` | Crate-internal | Accessor / query | This is not a "real" driver, so it is not considered enabled. |
| 254 | `create_signal_driver`  |  | Private helper | Constructor |  |
| 267 | `create_signal_driver`  |  | Private helper | Constructor |  |
| 278 | `create_process_driver`  |  | Private helper | Constructor |  |
| 287 | `create_process_driver`  |  | Private helper | Constructor |  |
| 308 | `create_clock`  |  | Private helper | Constructor |  |
| 312 | `create_time_driver`  |  | Private helper | Constructor |  |
| 335 | `park`  | `TimeDriver` | Crate-internal | Wake / park |  |
| 343 | `park_timeout`  | `TimeDriver` | Crate-internal | Wake / park |  |
| 351 | `shutdown`  | `TimeDriver` | Crate-internal | Runtime/task control |  |
| 367 | `create_clock`  |  | Private helper | Constructor |  |
| 371 | `create_time_driver`  |  | Private helper | Constructor |  |

## `tokio/src/runtime/dump.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 60 | `from_backtrace_symbol`  | `BacktraceSymbol` | Crate-internal | Conversion |  |
| 73 | `name_raw`  | `BacktraceSymbol` | Public API | Other / internal logic | Return the raw name of the symbol. |
| 78 | `name_demangled`  | `BacktraceSymbol` | Public API | Other / internal logic | Return the demangled name of the symbol. |
| 83 | `addr`  | `BacktraceSymbol` | Public API | Networking | Returns the starting address of this symbol. |
| 89 | `filename`  | `BacktraceSymbol` | Public API | Other / internal logic | Returns the file name where this function was defined. |
| 96 | `lineno`  | `BacktraceSymbol` | Public API | Other / internal logic | Returns the line number for where this symbol is currently executing. |
| 103 | `colno`  | `BacktraceSymbol` | Public API | Other / internal logic | Returns the column number for where this symbol is currently executing. |
| 119 | `from_resolved_backtrace_frame`  | `BacktraceFrame` | Crate-internal | Conversion |  |
| 134 | `ip`  | `BacktraceFrame` | Public API | Other / internal logic | Return the instruction pointer of this frame. |
| 139 | `symbol_address`  | `BacktraceFrame` | Public API | Other / internal logic | Returns the starting symbol address of the frame of this function. |
| 148 | `symbols`  | `BacktraceFrame` | Public API | Other / internal logic | Return an iterator over the symbols of this backtrace frame. |
| 164 | `frames`  | `Backtrace` | Public API | Other / internal logic | Return the frames in this backtrace, innermost (in a task dump, likely to be a leaf future's poll function) first. |
| 202 | `resolve_backtraces`  | `Trace` | Public API | Other / internal logic | Resolve and return a list of backtraces that are involved in polls in this trace. |
| 267 | `capture`  | `Trace` | Public API | Other / internal logic | Runs the function `f` in tracing mode, and returns its result along with the resulting [`Trace`]. |
| 280 | `root`  | `Trace` | Public API | Other / internal logic | Create a root for stack traces captured using [`Trace::capture`]. |
| 289 | `new`  | `Dump` | Crate-internal | Constructor |  |
| 296 | `tasks`  | `Dump` | Public API | Other / internal logic | Tasks in this snapshot. |
| 303 | `iter`  | `Tasks` | Public API | Combinator / iteration | Iterate over tasks. |
| 309 | `new`  | `Task` | Crate-internal | Constructor |  |
| 327 | `id`  | `Task` | Public API | Accessor / query | Returns a [task ID] that uniquely identifies this task relative to other tasks spawned at the time of the dump. |
| 332 | `trace`  | `Task` | Public API | Debugging / tracing | A trace of this task's state. |
| 338 | `fmt`  | `fmt::Display for Trace` | Trait impl | Formatting |  |

## `tokio/src/runtime/handle.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 86 | `enter`  | `Handle` | Public API | Runtime/task control | Enters the runtime context. |
| 144 | `current`  | `Handle` | Public API | Handle / reference plumbing | Returns a `Handle` view over the currently running `Runtime`. |
| 155 | `try_current`  | `Handle` | Public API | Non-blocking attempt | Returns a Handle view over the currently running Runtime Returns an error if no Runtime has been started Contrary to `current`, this never panics |
| 197 | `spawn`  | `Handle` | Public API | Runtime/task control | Spawns a future onto the Tokio runtime. |
| 234 | `spawn_blocking`  | `Handle` | Public API | Runtime/task control | Runs the provided function on an executor dedicated to blocking operations. |
| 342 | `block_on`  | `Handle` | Public API | Runtime/task control | Runs a future to completion on this `Handle`'s associated `Runtime`. |
| 352 | `block_on_inner`  | `Handle` | Private helper | Runtime/task control |  |
| 379 | `spawn_named`  | `Handle` | Crate-internal | Runtime/task control |  |
| 409 | `spawn_local_named` ⚠ | `Handle` | Crate-internal | Runtime/task control | # Safety This must only be called in `LocalRuntime` if the runtime has been verified to be owned by the current thread. |
| 461 | `runtime_flavor`  | `Handle` | Public API | Other / internal logic | Returns the flavor of the current `Runtime`. |
| 483 | `id`  | `Handle` | Public API | Accessor / query | Returns the [`Id`] of the current `Runtime`. |
| 505 | `name`  | `Handle` | Public API | Other / internal logic | Returns the name of the current `Runtime`. |
| 515 | `metrics`  | `Handle` | Public API | Accessor / query | Returns a view that lets you get information about how the runtime is performing. |
| 646 | `dump` 🅰 | `Handle` | Public API | Debugging / tracing | Captures a snapshot of the runtime's state. |
| 666 | `is_tracing`  | `Handle` | Public API | Accessor / query | Produces `true` if the current task is being traced for a dump; otherwise false. |
| 673 | `spawn_thread` 🅰 |  | Private helper | Runtime/task control | Spawn a new thread and asynchronously await on its result. |
| 697 | `new_no_context`  | `TryCurrentError` | Crate-internal | Constructor |  |
| 703 | `new_thread_local_destroyed`  | `TryCurrentError` | Crate-internal | Constructor |  |
| 711 | `is_missing_context`  | `TryCurrentError` | Public API | Accessor / query | Returns true if the call failed because there is currently no runtime in the Tokio context. |
| 718 | `is_thread_local_destroyed`  | `TryCurrentError` | Public API | Accessor / query | Returns true if the call failed because the Tokio context thread-local had been destroyed. |
| 729 | `fmt`  | `fmt::Debug for TryCurrentErrorKind` | Trait impl | Formatting |  |
| 738 | `fmt`  | `fmt::Display for TryCurrentError` | Trait impl | Formatting |  |

## `tokio/src/runtime/id.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `new`  | `Id` | Crate-internal | Constructor |  |
| 39 | `fmt`  | `fmt::Display for Id` | Trait impl | Formatting |  |

## `tokio/src/runtime/jspi.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `emscripten_has_asyncify`  |  | Private helper | Other / internal logic | Reports the `ASYNCIFY` build mode: 0 = none, 1 = legacy `Asyncify`, 2 = JSPI. |
| 28 | `emscripten_promise_create`  |  | Private helper | Other / internal logic |  |
| 29 | `emscripten_promise_destroy`  |  | Private helper | Other / internal logic |  |
| 30 | `emscripten_promise_resolve`  |  | Private helper | Other / internal logic |  |
| 32 | `emscripten_set_timeout`  |  | Private helper | Other / internal logic |  |
| 37 | `emscripten_clear_timeout`  |  | Private helper | Other / internal logic |  |
| 38 | `emscripten_set_immediate`  |  | Private helper | Other / internal logic |  |
| 39 | `emscripten_clear_immediate`  |  | Private helper | Other / internal logic |  |
| 53 | `emscripten_promise_await_unchecked`  |  | Private helper | Other / internal logic |  |
| 57 | `jspi_enabled`  |  | Crate-internal | Other / internal logic | Whether JSPI suspension is available: linked with `-sJSPI`. |
| 72 | `new` 🅲 | `Slot` | Crate-internal | Constructor |  |
| 92 | `set`  | `Timer` | Private helper | Configuration / setter |  |
| 107 | `drop`  | `Drop for Timer` | Trait impl | Drop / cleanup |  |
| 119 | `resolve`  |  | Private helper | Other / internal logic |  |
| 132 | `drop`  | `Drop for Park<'_>` | Trait impl | Drop / cleanup |  |
| 143 | `park`  |  | Crate-internal | Wake / park | Suspend the owning activation until [`unpark`] is called on `slot`, or `dur` elapses on a host timer if given. |
| 168 | `unpark`  |  | Crate-internal | Wake / park | Resume the activation parked on `slot`, if any. |

## `tokio/src/runtime/mod.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 464 | `new`  | `Timer` | Crate-internal | Constructor |  |
| 476 | `init`  | `Timer` | Crate-internal | Other / internal logic |  |
| 489 | `is_elapsed`  | `Timer` | Crate-internal | Accessor / query |  |
| 497 | `cancel`  | `Timer` | Crate-internal | Lifecycle / ref-count |  |
| 513 | `reset`  | `Timer` | Crate-internal | Configuration / setter |  |
| 531 | `poll_elapsed`  | `Timer` | Crate-internal | Poll function |  |
| 619 | `worker_index`  |  | Public API | Metrics / counters | Returns the index of the current worker thread, if called from a runtime worker thread. |

## `tokio/src/runtime/park.rs` (31)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 47 | `new`  | `ParkThread` | Crate-internal | Constructor |  |
| 59 | `unpark`  | `ParkThread` | Crate-internal | Wake / park |  |
| 64 | `park`  | `ParkThread` | Crate-internal | Wake / park |  |
| 70 | `park_timeout`  | `ParkThread` | Crate-internal | Wake / park |  |
| 76 | `shutdown`  | `ParkThread` | Crate-internal | Runtime/task control |  |
| 85 | `park`  | `Inner` | Private helper | Wake / park |  |
| 133 | `park`  | `Inner` | Private helper | Wake / park |  |
| 139 | `park_jspi`  | `Inner` | Private helper | Wake / park | Parks the activation until unparked or `dur` elapses, if given. |
| 178 | `drop`  | `Drop for Unpark<'_>` | Trait impl | Drop / cleanup |  |
| 193 | `park_timeout`  | `Inner` | Private helper | Wake / park | Parks the current thread for at most `dur`. |
| 244 | `park_timeout`  | `Inner` | Private helper | Wake / park |  |
| 248 | `unpark`  | `Inner` | Private helper | Wake / park |  |
| 281 | `shutdown`  | `Inner` | Private helper | Runtime/task control |  |
| 287 | `default`  | `Default for ParkThread` | Trait impl | Constructor |  |
| 295 | `unpark`  | `UnparkThread` | Crate-internal | Wake / park |  |
| 323 | `new`  | `CachedParkThread` | Crate-internal | Constructor | Creates a new `ParkThread` handle for the current thread. |
| 331 | `waker`  | `CachedParkThread` | Crate-internal | Wake / park |  |
| 335 | `unpark`  | `CachedParkThread` | Private helper | Wake / park |  |
| 339 | `park`  | `CachedParkThread` | Crate-internal | Wake / park |  |
| 344 | `park_timeout`  | `CachedParkThread` | Crate-internal | Wake / park |  |
| 350 | `with_current`  | `CachedParkThread` | Private helper | Constructor | Gets a reference to the `ParkThread` handle for this thread. |
| 362 | `block_on`  | `CachedParkThread` | Crate-internal | Runtime/task control |  |
| 382 | `into_waker`  | `UnparkThread` | Crate-internal | Conversion |  |
| 392 | `into_raw`  | `Inner` | Private helper | Conversion |  |
| 399 | `from_raw` ⚠ | `Inner` | Private helper | Conversion | # Safety The pointer must have been created by [`Self::into_raw`]. |
| 405 | `unparker_to_raw_waker` ⚠ |  | Private helper | Wake / park |  |
| 415 | `clone` ⚠ |  | Private helper | Other / internal logic | # Safety The pointer must have been created by [`Inner::into_raw`]. |
| 425 | `drop_waker` ⚠ |  | Private helper | Lifecycle / ref-count | # Safety The pointer must have been created by [`Inner::into_raw`]. |
| 432 | `wake` ⚠ |  | Private helper | Wake / park | # Safety The pointer must have been created by [`Inner::into_raw`]. |
| 440 | `wake_by_ref` ⚠ |  | Private helper | Wake / park | # Safety The pointer must have been created by [`Inner::into_raw`]. |
| 448 | `current_thread_park_count`  |  | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/process.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `new`  | `Driver` | Crate-internal | Constructor | Creates a new signal `Driver` instance that delegates wakeups to `park`. |
| 31 | `park`  | `Driver` | Crate-internal | Wake / park |  |
| 36 | `park_timeout`  | `Driver` | Crate-internal | Wake / park |  |
| 41 | `shutdown`  | `Driver` | Crate-internal | Runtime/task control |  |

## `tokio/src/runtime/runtime.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 132 | `from_parts`  | `Runtime` | Crate-internal | Conversion |  |
| 179 | `new`  | `Runtime` | Public API | Constructor | Creates a new runtime instance with default configuration values. |
| 206 | `handle`  | `Runtime` | Public API | Handle / reference plumbing | Returns a handle to the runtime's spawner. |
| 244 | `spawn`  | `Runtime` | Public API | Runtime/task control | Spawns a future onto the Tokio runtime. |
| 280 | `spawn_blocking`  | `Runtime` | Public API | Runtime/task control | Runs the provided function on an executor dedicated to blocking operations. |
| 343 | `block_on`  | `Runtime` | Public API | Runtime/task control | Runs a future to completion on the Tokio runtime. |
| 353 | `block_on_inner`  | `Runtime` | Private helper | Runtime/task control |  |
| 424 | `enter`  | `Runtime` | Public API | Runtime/task control | Enters the runtime context. |
| 457 | `shutdown_timeout`  | `Runtime` | Public API | Runtime/task control | Shuts down the runtime, waiting for at most `duration` for all spawned work to stop. |
| 494 | `shutdown_background`  | `Runtime` | Public API | Runtime/task control | Shuts down the runtime, without waiting for any spawned work to stop. |
| 500 | `metrics`  | `Runtime` | Public API | Accessor / query | Returns a view that lets you get information about how the runtime is performing. |
| 506 | `drop`  | `Drop for Runtime` | Trait impl | Drop / cleanup |  |
| 528 | `display_eq`  |  | Private helper | Other / internal logic |  |
| 537 | `write_str`  | `Write for FormatEq<'r>` | Trait impl | I/O operation |  |
| 585 | `is_rt_shutdown_err`  |  | Public API | Accessor / query | Checks whether the given error was emitted by Tokio when shutting down its runtime. |

## `tokio/src/runtime/task_hooks.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `spawn`  | `TaskHooks` | Crate-internal | Runtime/task control |  |
| 14 | `from_config`  | `TaskHooks` | Crate-internal | Conversion |  |
| 27 | `poll_start_callback`  | `TaskHooks` | Crate-internal | Poll function |  |
| 35 | `poll_stop_callback`  | `TaskHooks` | Crate-internal | Poll function |  |
| 76 | `id`  | `TaskMeta<'a>` | Public API | Accessor / query | Return the opaque ID of the task. |
| 82 | `spawned_at`  | `TaskMeta<'a>` | Public API | Runtime/task control | Return the source code location where the task was spawned. |
| 108 | `schedule_latency`  | `TaskMeta<'a>` | Public API | Runtime/task control | Returns the latency between scheduling the task and starting its current poll. |

## `tokio/src/runtime/thread_id.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `next`  | `ThreadId` | Crate-internal | Combinator / iteration |  |
| 35 | `exhausted`  |  | Private helper | Other / internal logic |  |

