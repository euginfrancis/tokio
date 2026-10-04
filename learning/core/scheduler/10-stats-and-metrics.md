# 10 — Stats & metrics (worker self-tuning + observable counters)

> **Role:** two jobs that share one data path.
> 1. **Tuning:** each worker keeps an exponentially-weighted moving average (EWMA) of how long one task poll takes
>    and uses it to pick `global_queue_interval` (how often to look at the inject queue).
> 2. **Reporting:** cheap per-worker counters/histograms that are *batched* thread-locally and *published* with
>    `Relaxed` stores so `RuntimeMetrics` can read them from any thread.
> **Boundary:** counters never affect scheduling correctness. Only the EWMA affects behaviour (and only the interval).

**Files**

| File | Lines | Content |
|---|---|---|
| `scheduler/multi_thread/stats.rs` | 149 | `Stats` – per-worker (owned by `Core`), EWMA + wraps a `MetricsBatch` |
| `metrics/batch.rs` | 401 | `MetricsBatch` – plain `u64` counters mutated without atomics; `submit()` publishes |
| `metrics/worker.rs` | 122 | `WorkerMetrics` – shared atomics, `#[repr(align(128))]` per worker |
| `metrics/scheduler.rs` | 35 | `SchedulerMetrics` – runtime-wide atomics (`remote_schedule_count`, `budget_forced_yield_count`) |
| `metrics/runtime.rs` | 1303 | public `RuntimeMetrics` accessor API (mostly docs) |
| `metrics/histogram.rs` | 629 | `Histogram`, `HistogramBatch`, `HistogramBuilder`, linear/log scales (unstable) |
| `metrics/schedule_latency*.rs` | 61+22 | `ScheduleLatencyInstant/Context` or a mock (cfg `schedule-latency`) |
| `util/metric_atomics.rs` | – | `MetricAtomicU64/Usize` (a no-op U64 where the target lacks 64-bit atomics) |

## 1. Data structures

```rust
// scheduler/multi_thread/stats.rs  — owned by Core, single-threaded
pub(crate) struct Stats {
    batch: MetricsBatch,
    processing_scheduled_tasks_started_at: Instant,
    tasks_polled_in_batch: usize,
    task_poll_time_ewma: f64,          // nanoseconds
}

// metrics/batch.rs — plain integers, unsynchronised
pub(crate) struct MetricsBatch {
    busy_duration_total: u64,
    processing_scheduled_tasks_started_at: Option<Instant>,
    park_count: u64,
    park_unpark_count: u64,
    // cfg(tokio_unstable):
    noop_count, steal_count, steal_operations, poll_count, poll_count_on_last_park,
    local_schedule_count, overflow_count: u64,
    poll_timer: Option<PollTimer>,                // histogram of poll durations
    schedule_latencies: Option<HistogramBatch>,   // + feature "schedule-latency"
}

// metrics/worker.rs — shared, read by other threads
#[repr(align(128))]
pub(crate) struct WorkerMetrics {
    busy_duration_total, park_count, park_unpark_count: MetricAtomicU64,
    queue_depth: MetricAtomicUsize,               // current-thread scheduler only
    thread_id: Mutex<Option<ThreadId>>,
    // unstable: noop_count, steal_count, steal_operations, poll_count, mean_poll_time,
    //           local_schedule_count, overflow_count, poll_count_histogram, schedule_latency_histogram
}
```

Why three layers (`Stats` → `MetricsBatch` → `WorkerMetrics`)?

* The worker hot loop increments counters **many times per task**. Doing that on shared atomics
  would put cache-line ping-pong into the hottest path. So the worker mutates *local* `u64`s in
  `MetricsBatch` and only copies them to the atomics in `submit()`.
* `#[repr(align(128))]` on `WorkerMetrics` avoids **false sharing** between the metrics of different workers (128 B covers
  adjacent-line prefetching on x86 and 128-byte lines on some ARM parts).
* `Stats` = tuning state + batch; the code comment says they'll be unified "when we stabilize metrics".
* The runtime-wide `SchedulerMetrics` counters *are* shared atomics (`add(1, Relaxed)`), because the events
  (`remote_schedule_count`, `budget_forced_yield_count`) can happen on any thread, and are rare compared with polls.

### "stable" vs "unstable" builds

`cfg_metrics_variant! { stable: {…}, unstable: {…} }` compiles each batch method twice: in stable builds most
of them are empty or return `None`, so the hot path pays *nothing*. Only `busy_duration_total`, `park_count` and
`park_unpark_count` exist in stable builds. Everything else needs `--cfg tokio_unstable`. Without 64-bit atomics (`cfg_64bit_metrics!`) the
`u64` accessors are removed.

## 2. The EWMA tuner

Constants (`stats.rs`):

| Const | Value | Meaning |
|---|---|---|
| `TASK_POLL_TIME_EWMA_ALPHA` | `0.1` | per-poll weight ("plucked from thin air") |
| `TARGET_GLOBAL_QUEUE_INTERVAL` | `200 µs` (as ns `f64`) | desired wall time between inject checks |
| `TARGET_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL` | `61` | the *previous* fixed default; used to seed the EWMA |
| `MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL` | `127` | cap = 2× the old default |

**Seed:** `ewma = 200_000 ns / 61 ≈ 3 278 ns` so that the first computed interval is ≈ 61 (`200 µs / seed`).

**Update (once per processing batch, in `end_processing_scheduled_tasks`)**, only if `tasks_polled_in_batch > 0`:

```rust
let elapsed   = (now - processing_scheduled_tasks_started_at).as_nanos() as f64;
let num_polls = tasks_polled_in_batch as f64;
let mean      = elapsed / num_polls;
let weighted_alpha = 1.0 - (1.0 - ALPHA).powf(num_polls);        // = weight of n sequential updates
ewma = weighted_alpha * mean + (1.0 - weighted_alpha) * ewma;
```

This is the closed form of applying the ordinary update `ewma ← α·x + (1−α)·ewma` **n times with the same sample `x`**:
the old value's weight decays by `(1−α)^n`. It lets the worker take *one* timestamp pair per batch instead of
two clock reads per poll.

**Use:** `tuned_global_queue_interval(config)`:

```rust
if let Some(c) = config.global_queue_interval { return c; }        // user-fixed → no tuning
let n = (TARGET_GLOBAL_QUEUE_INTERVAL / ewma) as u32;              // polls that fit in 200 µs (saturating cast)
n.clamp(2, 127)                                                    // never < 2 (else inject is checked every tick)
```

| mean poll time | interval |
|---|---|
| ≈ 3.3 µs (seed) | 61 |
| 1 µs | 127 (cap; 200 would clamp) |
| 10 µs | 20 |
| 100 µs | 2 |
| ≥ 100 µs | 2 (floor) |

`Core::tune_global_queue_interval` (called from `next_task` right after the tick check) applies **hysteresis**: only
replaces the stored interval if it differs by more than 2 (`abs_diff > 2`) "to smooth out jitter".
`Core::new` seeds it with `stats.tuned_global_queue_interval(&config)`.

Rationale: slow polls ⇒ fewer polls between checks, so remote work sees bounded latency (~200 µs);
fast polls ⇒ check less often, since each inject check costs a lock.

## 3. Where each counter is touched (multi-thread)

| Hook | Called from | Effect |
|---|---|---|
| `start_processing_scheduled_tasks` | `Context::run` (before loop, after park, after maintenance) | resets the batch timer and `tasks_polled_in_batch = 0`; `batch` records `processing_scheduled_tasks_started_at` |
| `end_processing_scheduled_tasks` | before `steal_work`/park, and in `maintenance` | adds *busy time* to `busy_duration_total`; updates the EWMA |
| `start_poll(ctx)` | `run_task` | `tasks_polled_in_batch += 1`; (unstable) `poll_count += 1`, stamps `poll_started_at` if a poll-count histogram exists; returns schedule latency |
| `record_schedule_latency(ctx)` | each LIFO-slot task polled in the chain | per-task latency sample *without* a second poll count |
| `end_poll()` | `run_task` when the LIFO chain ends | records elapsed into the poll-time histogram |
| `about_to_park()` | `Context::park` loop | `park_count++`, `park_unpark_count++`, and `noop_count++` if no task was polled since the last park |
| `unparked()` | after `park_internal` | `park_unpark_count++` |
| `inc_local_schedule_count()` | `Handle::schedule_local` | local schedule count |
| `incr_steal_count(n)`, `incr_steal_operations()` | `queue::Steal::steal_into` | after a successful steal of `n` |
| `incr_overflow_count()` | `queue::Local::push_overflow` | one per overflow event |
| `submit(&WorkerMetrics)` | `Core::maintenance` (every `event_interval` ticks), before parking, `pre_shutdown` | publishes everything with `Relaxed` stores; also `mean_poll_time = ewma as u64` |
| `SchedulerMetrics::inc_remote_schedule_count` | `Handle::push_remote_task` | atomic add |
| `SchedulerMetrics::inc_budget_forced_yield_count` | coop budget exhaustion | atomic add (see [task/10](../task/10-coop-budget.md)) |

Because publishing happens only at `submit`, **reads from `RuntimeMetrics` are slightly stale by design** (bounded by `event_interval` ticks or the next park).

### Worker thread id

`WorkerMetrics.thread_id: Mutex<Option<ThreadId>>` is written once per worker (`set_thread_id` at `Launch`/worker start) — the only mutex in the metrics path, off the hot path.

## 4. Reading it: `RuntimeMetrics`

`Runtime::metrics()` / `Handle::metrics()` returns `RuntimeMetrics { handle: Handle }`; each accessor goes
`handle.inner.worker_metrics(i).<field>.load(Relaxed)`. Examples and stability:

| Accessor | Stable? | Source |
|---|---|---|
| `num_workers`, `num_alive_tasks`, `global_queue_depth` | stable | `worker_metrics.len()`, `OwnedTasks::num_alive_tasks`, `Inject::len` |
| `worker_total_busy_duration`, `worker_park_count`, `worker_park_unpark_count` | stable (64-bit atomics) | `WorkerMetrics` |
| `worker_noop_count`, `worker_steal_count`, `worker_steal_operations`, `worker_poll_count`, `worker_local_schedule_count`, `worker_overflow_count`, `worker_mean_poll_time` | `tokio_unstable` | `MetricsBatch`/EWMA |
| `remote_schedule_count`, `budget_forced_yield_count`, `spawned_tasks_count`, `num_blocking_threads`, `num_idle_blocking_threads`, `blocking_queue_depth`, `worker_thread_id`, `worker_local_queue_depth` | `tokio_unstable` | scheduler/blocking pool |
| `poll_time_histogram_*`, `poll_count_histogram_*`, `schedule_latency_histogram_*` | `tokio_unstable` (latency also needs `schedule-latency`) | `Histogram` |
| `io_driver_fd_registered_count`, `io_driver_fd_deregistered_count`, `io_driver_ready_count` | `tokio_unstable` + `net` | `IoDriverMetrics` |

Histograms: `HistogramBuilder` (linear or log scale; `HistogramConfiguration`, `LogHistogramBuilder`) →
`Histogram` (`Vec<MetricAtomicU64>` buckets shared) and `HistogramBatch` (plain `Vec<u64>` per worker, merged
on `submit`).

## 5. Interactions

* **Worker loop** ([05](./05-worker-loop.md)): the only writer of `Stats`; `Core.stats` is *moved with the Core* (including through `block_in_place` hand-off).
* **Local queue** ([06](./06-local-queue.md)): takes `&mut Stats` in `push_back_or_overflow` and `steal_into` so it can count without locking.
* **Task** (`task_meta` / schedule latency): `Notified::get_scheduled_at()` → `ScheduleLatencyInstant` → `prepare(start)` → context; see [task/09](../task/09-id-hooks-metadata.md).
* **Current-thread scheduler**: no EWMA; uses `WorkerMetrics.queue_depth` and a `MetricsBatch` of its own (single worker, index 0).

## 6. Invariants

| # | Invariant |
|---|---|
| I1 | `Stats`/`MetricsBatch` are only touched by the thread that owns the `Core` (no atomics needed) |
| I2 | Published values are monotone counters (except `queue_depth`, `mean_poll_time`) |
| I3 | `tuned_global_queue_interval` ∈ [2, 127] when auto-tuned; user value ≥ 1 (builder asserts `> 0`) |
| I4 | Stable builds with default features add no work to the poll path beyond the EWMA's two `Instant` reads per batch |

## 7. Tests

* `tokio/tests/rt_threaded.rs::test_tuning` (EWMA/interval behaviour) and `global_queue_interval_set_to_one`.
* `tokio/tests/rt_metrics.rs` and `rt_unstable_metrics.rs` (metrics API) – counters for park, steal, poll, overflow, histograms.
* `runtime/metrics/histogram.rs` unit tests (bucket math).

<!-- TESTS:stats -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_metrics.rs`](../../../tokio/tests/rt_metrics.rs) | 7 | 178 |
| [`tokio/tests/rt_unstable_metrics.rs`](../../../tokio/tests/rt_unstable_metrics.rs) | 28 | 742 |
| *inline `#[test]` in the source files above* | 6 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [11 — block_in_place & defer](./11-block-in-place-and-defer.md)
