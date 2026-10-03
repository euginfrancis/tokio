# Tokio function index

Every function defined under `*/src` of the Tokio crates, categorized automatically by [`fn_index.py`](../fn_index.py). For hand-written explanations of the important ones, read [`../HOW_TOKIO_WORKS.md`](../HOW_TOKIO_WORKS.md).

**Total functions: 5,480** (async: 240, unsafe: 205, const: 68)

## By crate

| Crate | Functions | % |
|---|---:|---:|
| `tokio` | 4,397 | 80.2% |
| `tokio-util` | 648 | 11.8% |
| `tokio-stream` | 330 | 6.0% |
| `tokio-test` | 66 | 1.2% |
| `tokio-macros` | 39 | 0.7% |

## By kind

| Kind | Functions | % | Meaning |
|---|---:|---:|---|
| Public API | 1,548 | 28.2% | `pub fn` — callable by users of the crate (if its module is public) |
| Trait impl | 1,344 | 24.5% | Implements a trait for a type (`Future::poll`, `Drop::drop`, `Debug::fmt`, …) |
| Crate-internal | 1,199 | 21.9% | `pub(crate)` / `pub(super)` / `pub(in path)`: shared between Tokio's own modules, invisible to users |
| Private helper | 722 | 13.2% | No `pub`: used only inside its own module |
| Test | 467 | 8.5% | Inside `#[cfg(test)]` modules or test-only files |
| Trait method (declaration/default) | 173 | 3.2% | Declared inside a `trait { … }` block |
| Inside macro_rules! | 27 | 0.5% | Function written inside a macro body (generated per use) |

## By role (non-test)

Role is guessed from the trait being implemented or the function name.

| Role | Functions | % |
|---|---:|---:|
| Other / internal logic | 760 | 15.2% |
| Constructor | 483 | 9.6% |
| Accessor / query | 417 | 8.3% |
| Conversion | 309 | 6.2% |
| Runtime/task control | 300 | 6.0% |
| I/O trait impl | 267 | 5.3% |
| Data movement | 239 | 4.8% |
| I/O operation | 225 | 4.5% |
| Formatting | 202 | 4.0% |
| Configuration / setter | 173 | 3.5% |
| Non-blocking attempt | 166 | 3.3% |
| Poll function | 158 | 3.2% |
| Combinator / iteration | 125 | 2.5% |
| Metrics / counters | 124 | 2.5% |
| Wake / park | 109 | 2.2% |
| Drop / cleanup | 108 | 2.2% |
| Networking | 79 | 1.6% |
| Stream impl | 78 | 1.6% |
| Future impl (poll) | 75 | 1.5% |
| OS handle access | 71 | 1.4% |
| Async operation | 69 | 1.4% |
| Handle / reference plumbing | 61 | 1.2% |
| Lifecycle / ref-count | 58 | 1.2% |
| Time / timers | 51 | 1.0% |
| Deref | 42 | 0.8% |
| Intrusive-list link | 39 | 0.8% |
| Sink impl | 36 | 0.7% |
| Locking / permits | 32 | 0.6% |
| I/O registration | 28 | 0.6% |
| Debugging / tracing | 22 | 0.4% |
| Clone | 20 | 0.4% |
| State transition | 20 | 0.4% |
| Blocking (sync) variant | 18 | 0.4% |
| Scheduler hook | 15 | 0.3% |
| Codec impl | 12 | 0.2% |
| Iterator | 11 | 0.2% |
| Comparison | 6 | 0.1% |
| Waker | 4 | 0.1% |
| Error type | 1 | 0.0% |

## By component

| Component | Functions | Public API | Trait impls | Internal | Unsafe | Async | Page |
|---|---:|---:|---:|---:|---:|---:|---|
| `tokio (crate root)` | 10 | 0 | 2 | 7 | 0 | 1 | [tokio_crate_root.md](./tokio_crate_root.md) |
| `tokio-macros (crate root)` | 39 | 8 | 2 | 29 | 0 | 0 | [tokio_macros_crate_root.md](./tokio_macros_crate_root.md) |
| `tokio-stream (crate root)` | 71 | 22 | 18 | 8 | 0 | 1 | [tokio_stream_crate_root.md](./tokio_stream_crate_root.md) |
| `tokio-stream::stream_ext` | 173 | 43 | 100 | 27 | 0 | 2 | [tokio_stream_stream_ext.md](./tokio_stream_stream_ext.md) |
| `tokio-stream::wrappers` | 86 | 31 | 53 | 2 | 0 | 2 | [tokio_stream_wrappers.md](./tokio_stream_wrappers.md) |
| `tokio-test (crate root)` | 66 | 26 | 16 | 24 | 6 | 0 | [tokio_test_crate_root.md](./tokio_test_crate_root.md) |
| `tokio-util (crate root)` | 53 | 6 | 35 | 1 | 0 | 2 | [tokio_util_crate_root.md](./tokio_util_crate_root.md) |
| `tokio-util::codec` | 138 | 72 | 53 | 9 | 0 | 0 | [tokio_util_codec.md](./tokio_util_codec.md) |
| `tokio-util::future` | 4 | 0 | 2 | 2 | 0 | 0 | [tokio_util_future.md](./tokio_util_future.md) |
| `tokio-util::io` | 100 | 35 | 54 | 11 | 0 | 2 | [tokio_util_io.md](./tokio_util_io.md) |
| `tokio-util::net` | 8 | 2 | 3 | 0 | 0 | 1 | [tokio_util_net.md](./tokio_util_net.md) |
| `tokio-util::net::unix` | 2 | 0 | 2 | 0 | 0 | 0 | [tokio_util_net_unix.md](./tokio_util_net_unix.md) |
| `tokio-util::sync` | 70 | 31 | 25 | 14 | 1 | 3 | [tokio_util_sync.md](./tokio_util_sync.md) |
| `tokio-util::sync::cancellation_token` | 17 | 4 | 2 | 11 | 0 | 0 | [tokio_util_sync_cancellation_token.md](./tokio_util_sync_cancellation_token.md) |
| `tokio-util::sync::tests` | 7 | 0 | 0 | 0 | 0 | 0 | [tokio_util_sync_tests.md](./tokio_util_sync_tests.md) |
| `tokio-util::task` | 126 | 76 | 28 | 18 | 0 | 6 | [tokio_util_task.md](./tokio_util_task.md) |
| `tokio-util::time` | 59 | 23 | 15 | 21 | 0 | 0 | [tokio_util_time.md](./tokio_util_time.md) |
| `tokio-util::time::wheel` | 36 | 0 | 1 | 26 | 0 | 0 | [tokio_util_time_wheel.md](./tokio_util_time_wheel.md) |
| `tokio-util::udp` | 13 | 8 | 5 | 0 | 0 | 0 | [tokio_util_udp.md](./tokio_util_udp.md) |
| `tokio-util::util` | 15 | 2 | 3 | 7 | 0 | 0 | [tokio_util_util.md](./tokio_util_util.md) |
| `tokio::doc` | 11 | 0 | 3 | 0 | 2 | 0 | [tokio_doc.md](./tokio_doc.md) |
| `tokio::fs` | 135 | 75 | 33 | 27 | 4 | 52 | [tokio_fs.md](./tokio_fs.md) |
| `tokio::fs::file` | 28 | 0 | 0 | 0 | 0 | 0 | [tokio_fs_file.md](./tokio_fs_file.md) |
| `tokio::fs::open_options` | 27 | 7 | 9 | 11 | 0 | 0 | [tokio_fs_open_options.md](./tokio_fs_open_options.md) |
| `tokio::future` | 13 | 3 | 3 | 3 | 0 | 0 | [tokio_future.md](./tokio_future.md) |
| `tokio::io` | 270 | 84 | 111 | 46 | 12 | 8 | [tokio_io.md](./tokio_io.md) |
| `tokio::io::bsd` | 15 | 5 | 6 | 1 | 0 | 0 | [tokio_io_bsd.md](./tokio_io_bsd.md) |
| `tokio::io::uring` | 38 | 0 | 24 | 11 | 3 | 1 | [tokio_io_uring.md](./tokio_io_uring.md) |
| `tokio::io::util` | 273 | 47 | 90 | 50 | 0 | 7 | [tokio_io_util.md](./tokio_io_util.md) |
| `tokio::loom` | 10 | 0 | 0 | 10 | 0 | 0 | [tokio_loom.md](./tokio_loom.md) |
| `tokio::loom::std` | 74 | 0 | 18 | 56 | 3 | 0 | [tokio_loom_std.md](./tokio_loom_std.md) |
| `tokio::macros` | 5 | 5 | 0 | 0 | 0 | 0 | [tokio_macros.md](./tokio_macros.md) |
| `tokio::net` | 91 | 62 | 21 | 7 | 0 | 17 | [tokio_net.md](./tokio_net.md) |
| `tokio::net::tcp` | 168 | 103 | 50 | 15 | 2 | 21 | [tokio_net_tcp.md](./tokio_net_tcp.md) |
| `tokio::net::unix` | 185 | 103 | 51 | 31 | 1 | 21 | [tokio_net_unix.md](./tokio_net_unix.md) |
| `tokio::net::unix::datagram` | 39 | 33 | 4 | 2 | 0 | 10 | [tokio_net_unix_datagram.md](./tokio_net_unix_datagram.md) |
| `tokio::net::windows` | 70 | 51 | 16 | 3 | 5 | 9 | [tokio_net_windows.md](./tokio_net_windows.md) |
| `tokio::process` | 94 | 37 | 28 | 11 | 2 | 4 | [tokio_process.md](./tokio_process.md) |
| `tokio::process::unix` | 97 | 0 | 43 | 23 | 0 | 0 | [tokio_process_unix.md](./tokio_process_unix.md) |
| `tokio::runtime` | 227 | 88 | 12 | 126 | 8 | 2 | [tokio_runtime.md](./tokio_runtime.md) |
| `tokio::runtime::blocking` | 59 | 0 | 8 | 51 | 0 | 0 | [tokio_runtime_blocking.md](./tokio_runtime_blocking.md) |
| `tokio::runtime::context` | 22 | 0 | 6 | 16 | 0 | 0 | [tokio_runtime_context.md](./tokio_runtime_context.md) |
| `tokio::runtime::driver` | 8 | 0 | 3 | 2 | 1 | 0 | [tokio_runtime_driver.md](./tokio_runtime_driver.md) |
| `tokio::runtime::io` | 66 | 0 | 13 | 51 | 6 | 3 | [tokio_runtime_io.md](./tokio_runtime_io.md) |
| `tokio::runtime::io::driver` | 18 | 0 | 1 | 17 | 1 | 1 | [tokio_runtime_io_driver.md](./tokio_runtime_io_driver.md) |
| `tokio::runtime::local_runtime` | 12 | 9 | 1 | 2 | 0 | 0 | [tokio_runtime_local_runtime.md](./tokio_runtime_local_runtime.md) |
| `tokio::runtime::metrics` | 112 | 40 | 2 | 63 | 0 | 0 | [tokio_runtime_metrics.md](./tokio_runtime_metrics.md) |
| `tokio::runtime::metrics::histogram` | 26 | 8 | 3 | 5 | 0 | 0 | [tokio_runtime_metrics_histogram.md](./tokio_runtime_metrics_histogram.md) |
| `tokio::runtime::scheduler` | 41 | 0 | 0 | 41 | 1 | 0 | [tokio_runtime_scheduler.md](./tokio_runtime_scheduler.md) |
| `tokio::runtime::scheduler::current_thread` | 46 | 0 | 9 | 37 | 1 | 0 | [tokio_runtime_scheduler_current_thread.md](./tokio_runtime_scheduler_current_thread.md) |
| `tokio::runtime::scheduler::inject` | 30 | 0 | 4 | 26 | 4 | 0 | [tokio_runtime_scheduler_inject.md](./tokio_runtime_scheduler_inject.md) |
| `tokio::runtime::scheduler::multi_thread` | 177 | 0 | 20 | 155 | 0 | 3 | [tokio_runtime_scheduler_multi_thread.md](./tokio_runtime_scheduler_multi_thread.md) |
| `tokio::runtime::scheduler::util` | 11 | 0 | 0 | 11 | 0 | 0 | [tokio_runtime_scheduler_util.md](./tokio_runtime_scheduler_util.md) |
| `tokio::runtime::signal` | 7 | 0 | 0 | 7 | 0 | 0 | [tokio_runtime_signal.md](./tokio_runtime_signal.md) |
| `tokio::runtime::task` | 234 | 14 | 25 | 187 | 39 | 0 | [tokio_runtime_task.md](./tokio_runtime_task.md) |
| `tokio::runtime::task::trace` | 29 | 1 | 7 | 21 | 2 | 0 | [tokio_runtime_task_trace.md](./tokio_runtime_task_trace.md) |
| `tokio::runtime::tests` | 113 | 0 | 0 | 0 | 3 | 3 | [tokio_runtime_tests.md](./tokio_runtime_tests.md) |
| `tokio::runtime::tests::loom_current_thread` | 2 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_tests_loom_current_thread.md](./tokio_runtime_tests_loom_current_thread.md) |
| `tokio::runtime::tests::loom_multi_thread` | 9 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_tests_loom_multi_thread.md](./tokio_runtime_tests_loom_multi_thread.md) |
| `tokio::runtime::time` | 67 | 0 | 8 | 58 | 16 | 0 | [tokio_runtime_time.md](./tokio_runtime_time.md) |
| `tokio::runtime::time::tests` | 11 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_time_tests.md](./tokio_runtime_time_tests.md) |
| `tokio::runtime::time::wheel` | 45 | 0 | 1 | 24 | 4 | 0 | [tokio_runtime_time_wheel.md](./tokio_runtime_time_wheel.md) |
| `tokio::runtime::time_alt` | 58 | 0 | 18 | 30 | 12 | 0 | [tokio_runtime_time_alt.md](./tokio_runtime_time_alt.md) |
| `tokio::runtime::time_alt::cancellation_queue` | 5 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_time_alt_cancellation_queue.md](./tokio_runtime_time_alt_cancellation_queue.md) |
| `tokio::runtime::time_alt::registration_queue` | 4 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_time_alt_registration_queue.md](./tokio_runtime_time_alt_registration_queue.md) |
| `tokio::runtime::time_alt::wake_queue` | 4 | 0 | 0 | 0 | 0 | 0 | [tokio_runtime_time_alt_wake_queue.md](./tokio_runtime_time_alt_wake_queue.md) |
| `tokio::runtime::time_alt::wheel` | 45 | 0 | 1 | 23 | 4 | 0 | [tokio_runtime_time_alt_wheel.md](./tokio_runtime_time_alt_wheel.md) |
| `tokio::signal` | 90 | 34 | 14 | 25 | 1 | 10 | [tokio_signal.md](./tokio_signal.md) |
| `tokio::signal::windows` | 21 | 0 | 1 | 13 | 2 | 0 | [tokio_signal_windows.md](./tokio_signal_windows.md) |
| `tokio::sync` | 386 | 158 | 96 | 128 | 19 | 24 | [tokio_sync.md](./tokio_sync.md) |
| `tokio::sync::mpsc` | 196 | 68 | 52 | 70 | 11 | 13 | [tokio_sync_mpsc.md](./tokio_sync_mpsc.md) |
| `tokio::sync::rwlock` | 57 | 23 | 28 | 6 | 0 | 0 | [tokio_sync_rwlock.md](./tokio_sync_rwlock.md) |
| `tokio::sync::task` | 14 | 0 | 6 | 6 | 0 | 0 | [tokio_sync_task.md](./tokio_sync_task.md) |
| `tokio::sync::tests` | 102 | 0 | 0 | 0 | 4 | 2 | [tokio_sync_tests.md](./tokio_sync_tests.md) |
| `tokio::task` | 108 | 54 | 28 | 24 | 7 | 6 | [tokio_task.md](./tokio_task.md) |
| `tokio::task::coop` | 30 | 6 | 5 | 17 | 0 | 1 | [tokio_task_coop.md](./tokio_task_coop.md) |
| `tokio::time` | 78 | 39 | 16 | 23 | 1 | 2 | [tokio_time.md](./tokio_time.md) |
| `tokio::util` | 169 | 1 | 27 | 128 | 17 | 0 | [tokio_util.md](./tokio_util.md) |
| `tokio::util::rand` | 5 | 1 | 0 | 4 | 0 | 0 | [tokio_util_rand.md](./tokio_util_rand.md) |
