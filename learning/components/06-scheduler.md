# Block 6 — Scheduler

> **Role:** decides *which* task runs *where* and *when*. Owns the worker threads, the run queues, work stealing, idle/park coordination, the runtime object and its configuration.
> In the [component diagram](./README.md) it's the box on the left that every API block feeds tasks into, and that parks inside the drivers when idle.

---

## 1. At a glance

<!-- STATS:scheduler -->
| Metric | Value |
|---|---|
| Source files | 76 |
| Code lines | 10,301 (20.4% of `tokio/src`) |
| Doc + comment lines | 5,979 (0.58 per code line) |
| Functions | 832 — public API 145, trait impls 60, internal 480, inline tests 142 |
| `async fn` / `unsafe fn` | 8 / 18 |
| `unsafe` occurrences | 104 |
| Integration tests (`tokio/tests`) | 21 files, 230 test fns, 4,852 code lines |
<!-- /STATS -->

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | `Runtime`/`Handle`/`Builder`; the two scheduler flavors (`current_thread`, `multi_thread`); per-worker `Core` (local run queue, LIFO slot, tick, RNG, stats); the global inject queue; work stealing; idle-worker tracking; parking threads; the thread-local runtime `CONTEXT`; runtime metrics and hooks; driver *wiring* (`runtime/driver.rs` builds the driver stack). |
| **Does not own** | What a task *is* (memory layout, state word, `JoinHandle`: [Tasks block](./01-tasks.md)); how I/O readiness and timers work ([I/O driver](./08-io-driver.md), [Timer driver](./07-timer-driver.md)); running blocking closures ([Blocking pool](./09-blocking-pool.md)). |
| **Input** | `Notified` task handles: from `spawn` (new tasks), from wakers (woken tasks), from `yield_now`. |
| **Output** | Calls `task.run()` (→ the task harness polls the future); calls `driver.park(timeout)` when idle. |
| **Boundary types** | `task::Schedule` trait (implemented by `Arc<multi_thread::Handle>`, `Arc<current_thread::Handle>`); `Notified<S>` / `LocalNotified<S>` / `OwnedTasks<S>`; `driver::Driver` / `driver::Handle`. |

---

## 3. Files

<!-- FILES:scheduler -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/runtime/scheduler/multi_thread/worker.rs`](../../tokio/src/runtime/scheduler/multi_thread/worker.rs) | 939 | 387 | 9.1% |
| [`tokio/src/runtime/scheduler/current_thread/mod.rs`](../../tokio/src/runtime/scheduler/current_thread/mod.rs) | 623 | 131 | 6.0% |
| [`tokio/src/runtime/builder.rs`](../../tokio/src/runtime/builder.rs) | 586 | 1,540 | 5.7% |
| [`tokio/src/runtime/metrics/histogram.rs`](../../tokio/src/runtime/metrics/histogram.rs) | 494 | 21 | 4.8% |
| [`tokio/src/runtime/tests/task_combinations.rs`](../../tokio/src/runtime/tests/task_combinations.rs) | 404 | 42 | 3.9% |
| [`tokio/src/runtime/tests/task.rs`](../../tokio/src/runtime/tests/task.rs) | 403 | 4 | 3.9% |
| [`tokio/src/runtime/metrics/histogram/h2_histogram.rs`](../../tokio/src/runtime/metrics/histogram/h2_histogram.rs) | 361 | 117 | 3.5% |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../tokio/src/runtime/tests/loom_multi_thread.rs) | 355 | 24 | 3.4% |
| [`tokio/src/runtime/scheduler/multi_thread/queue.rs`](../../tokio/src/runtime/scheduler/multi_thread/queue.rs) | 327 | 176 | 3.2% |
| [`tokio/src/runtime/metrics/batch.rs`](../../tokio/src/runtime/metrics/batch.rs) | 323 | 36 | 3.1% |
| [`tokio/src/runtime/driver.rs`](../../tokio/src/runtime/driver.rs) | 299 | 15 | 2.9% |
| [`tokio/src/runtime/park.rs`](../../tokio/src/runtime/park.rs) | 298 | 84 | 2.9% |
| [`tokio/src/runtime/metrics/runtime.rs`](../../tokio/src/runtime/metrics/runtime.rs) | 285 | 974 | 2.8% |
| [`tokio/src/runtime/handle.rs`](../../tokio/src/runtime/handle.rs) | 254 | 460 | 2.5% |
| [`tokio/src/runtime/scheduler/mod.rs`](../../tokio/src/runtime/scheduler/mod.rs) | 252 | 14 | 2.4% |
| [`tokio/src/runtime/scheduler/multi_thread/park.rs`](../../tokio/src/runtime/scheduler/multi_thread/park.rs) | 212 | 65 | 2.1% |
| [`tokio/src/runtime/tests/queue.rs`](../../tokio/src/runtime/tests/queue.rs) | 208 | 2 | 2.0% |
| [`tokio/src/runtime/runtime.rs`](../../tokio/src/runtime/runtime.rs) | 178 | 385 | 1.7% |
| [`tokio/src/runtime/mod.rs`](../../tokio/src/runtime/mod.rs) | 177 | 472 | 1.7% |
| [`tokio/src/runtime/dump.rs`](../../tokio/src/runtime/dump.rs) | 169 | 139 | 1.6% |
| [`tokio/src/runtime/context.rs`](../../tokio/src/runtime/context.rs) | 163 | 23 | 1.6% |
| [`tokio/src/runtime/driver/op.rs`](../../tokio/src/runtime/driver/op.rs) | 158 | 48 | 1.5% |
| [`tokio/src/runtime/tests/loom_blocking.rs`](../../tokio/src/runtime/tests/loom_blocking.rs) | 157 | 36 | 1.5% |
| [`tokio/src/runtime/scheduler/multi_thread/idle.rs`](../../tokio/src/runtime/scheduler/multi_thread/idle.rs) | 147 | 54 | 1.4% |
| [`tokio/src/runtime/scheduler/util/time_alt.rs`](../../tokio/src/runtime/scheduler/util/time_alt.rs) | 147 | 10 | 1.4% |
| [`tokio/src/runtime/tests/loom_multi_thread/queue.rs`](../../tokio/src/runtime/tests/loom_multi_thread/queue.rs) | 147 | 6 | 1.4% |
| [`tokio/src/runtime/tests/loom_current_thread.rs`](../../tokio/src/runtime/tests/loom_current_thread.rs) | 140 | 30 | 1.4% |
| [`tokio/src/runtime/local_runtime/runtime.rs`](../../tokio/src/runtime/local_runtime/runtime.rs) | 131 | 249 | 1.3% |
| [`tokio/src/runtime/scheduler/inject/rt_multi_thread.rs`](../../tokio/src/runtime/scheduler/inject/rt_multi_thread.rs) | 124 | 56 | 1.2% |
| [`tokio/src/runtime/scheduler/multi_thread/handle.rs`](../../tokio/src/runtime/scheduler/multi_thread/handle.rs) | 105 | 10 | 1.0% |
| *…46 smaller files* | 1,735 | 369 | 16.8% |
| **Total (76 files)** | **10,301** | **5,979** | 100% |
<!-- /FILES -->

**Directory map**

```
runtime/
├── builder.rs, config.rs          configuration → Config
├── runtime.rs, handle.rs          public Runtime / Handle
├── local_runtime/                 LocalRuntime (!Send tasks on one thread)
├── context.rs, context/           thread-local CONTEXT (current handle, scheduler, budget, rng, task id)
├── driver.rs, driver/             builds and parks the driver stack (time → process → signal → io)
├── park.rs                        ParkThread / CachedParkThread (block_on for non-worker threads)
├── scheduler/
│   ├── mod.rs                     enum Handle { CurrentThread, MultiThread }, enum Context
│   ├── current_thread/mod.rs      single-thread scheduler (~620 code lines)
│   ├── multi_thread/              work-stealing scheduler
│   │   ├── worker.rs              the worker loop (~940 code lines — the heart)
│   │   ├── queue.rs               lock-free local run queue (256 slots)
│   │   ├── idle.rs                who is sleeping / searching
│   │   ├── park.rs                Parker/Unparker (driver vs condvar)
│   │   ├── stats.rs               EWMA poll time → global queue interval
│   │   └── handle.rs, overflow.rs, counters.rs, trace.rs
│   ├── inject/                    global FIFO queue (mutex + atomic len)
│   ├── block_in_place.rs, defer.rs
├── metrics/                       RuntimeMetrics, histograms, per-worker stats
├── task_hooks.rs, dump.rs, id.rs, thread_id.rs
└── tests/                         loom models of queue, scheduler, shutdown
```

---

## 4. Data structures

### `Runtime` and the handle enum
```rust
pub struct Runtime {                       // runtime/runtime.rs
    scheduler: Scheduler,                  // enum { CurrentThread(CurrentThread), MultiThread(MultiThread) }
    handle: Handle,                        // public, cloneable
    blocking_pool: BlockingPool,           // owned here so Drop waits for blocking threads
}
pub(crate) enum Handle {                   // runtime/scheduler/mod.rs — what `Handle::current()` wraps
    CurrentThread(Arc<current_thread::Handle>),
    MultiThread(Arc<multi_thread::Handle>),
}
```

### Multi-thread: `Handle` → `Shared` → `Remote[]`, plus one `Worker` + `Core` per thread
```rust
pub(crate) struct Handle {                 // multi_thread/handle.rs — shared by all workers + all spawners
    shared: worker::Shared,
    driver: driver::Handle,                // to unpark the I/O driver, register timers
    blocking_spawner: blocking::Spawner,
    seed_generator, task_hooks, timer_flavor, name, …
}
pub(crate) struct Shared {                 // multi_thread/worker.rs
    remotes: Box<[Remote]>,                // one per worker: what OTHER threads may touch
    inject: InjectQueue<Arc<Handle>>,      // global FIFO for tasks from outside / overflow
    idle: Idle,                            // packed counters: #searching, #unparked + sleepers list
    owned: OwnedTasks<Arc<Handle>>,        // every live task (sharded list) — for shutdown
    synced: Mutex<Synced>,                 // idle sleepers list (+ timers queued for the alt timer)
    shutdown_cores: Mutex<Vec<Box<Core>>>, // cores collected during shutdown
    config: Config, scheduler_metrics, worker_metrics: Box<[WorkerMetrics]>, trace_status, …
}
struct Remote {
    steal: queue::Steal<Arc<Handle>>,      // other workers steal through this
    unpark: Unparker,                      // others wake this worker through this
}
pub(super) struct Worker {
    handle: Arc<Handle>,
    index: usize,
    core: AtomicCell<Core>,                // the Core can be handed to another thread (block_in_place)
}
struct Core {                              // only ever touched by the thread that holds it
    tick: u32,
    lifo_slot: Option<Notified>,           // "run this next" fast path
    lifo_enabled: bool,
    run_queue: queue::Local<Arc<Handle>>,  // owner end of the 256-slot ring buffer
    is_searching: bool, is_shutdown: bool, is_traced: bool,
    park: Option<Parker>,                  // taken out while parking
    stats: Stats,                          // EWMA of poll time, metrics batch
    global_queue_interval: u32,
    rand: FastRand,                        // victim selection when stealing
    …
}
pub(crate) struct Context {                // stored in the thread-local CONTEXT while a worker runs
    worker: Arc<Worker>,
    core: RefCell<Option<Box<Core>>>,      // Core lives here while a task is being polled
    defer: Defer,                          // wakers from yield_now, woken after the next park
}
```
**Key design point:** the `Core` is a `Box` that *moves*. A worker thread "is" a worker only while it holds the core. `block_in_place` hands the core to a new thread; shutdown collects all cores into `shutdown_cores`.

### Local run queue (`multi_thread/queue.rs`)
```rust
pub(crate) struct Local<T>(Arc<Inner<T>>);   // owner: push_back / pop
pub(crate) struct Steal<T>(Arc<Inner<T>>);   // others: steal_into (takes half)
pub(crate) struct Inner<T> {
    head: AtomicU64,                         // packs (steal_head: u32, real_head: u32)
    tail: AtomicU32,                         // written only by the owner
    buffer: Box<[UnsafeCell<MaybeUninit<Notified<T>>>; 256]>,
}
```
Lock-free single-producer / multi-consumer ring; see [DSA D4](../DSA_IN_TOKIO.md).

### Inject queue (`scheduler/inject/`)
```rust
pub(crate) enum InjectQueue<T> { Locked(Inject<T>) }               // multi-thread wrapper (one variant today)
pub(crate) struct Inject<T> { shared: Shared<T>, synced: Mutex<Synced> }
pub(crate) struct Shared<T> { len: AtomicUsize }                  // check "empty?" without locking
pub(crate) struct Synced { is_closed: bool, head: Option<RawTask>, tail: Option<RawTask> }  // behind Inject.synced
```
An intrusive singly linked list: the `next` pointer lives in each task's `Header.queue_next`.

### Idle tracking (`multi_thread/idle.rs`)
```rust
pub(super) struct Idle { state: AtomicUsize /* num_searching | num_unparked << 16 */, num_workers: usize }
pub(super) struct Synced { sleepers: Vec<usize> }                  // indices of parked workers
```

### Parker (`multi_thread/park.rs`)
```rust
pub(crate) struct Parker { inner: Arc<Inner> }
struct Inner { state: AtomicUsize /* EMPTY | PARKED_CONDVAR | PARKED_DRIVER | NOTIFIED */,
               mutex: Mutex<()>, condvar: Condvar, shared: Arc<Shared> }
struct Shared { driver: TryLock<Driver> }                           // ONE driver shared by all workers
```

### Current-thread
```rust
pub(crate) struct CurrentThread { core: AtomicCell<Core>, notify: Notify }   // whoever takes `core` drives the runtime
struct Core { tasks: VecDeque<Notified>, tick: u32, driver: Option<Driver>, metrics, global_queue_interval, unhandled_panic }
struct Shared { inject: Inject<Arc<Handle>>, owned: OwnedTasks<…>, woken: AtomicBool /* block_on future woken */, config, … }
```

### `Config` (from `Builder`)
`global_queue_interval`, `event_interval` (61), `before_park`/`after_unpark`/`before_spawn`/`after_termination`/`before_poll`/`after_poll` hooks, `disable_lifo_slot`, `seed_generator`, histogram settings, `unhandled_panic`, `enable_eager_driver_handoff`.

### Thread-local `CONTEXT` (`runtime/context.rs`)
`thread_id`, `current: HandleCell` (the runtime this thread is in), `scheduler: Scoped<scheduler::Context>` (set only on worker threads), `current_task_id`, `runtime: EnterRuntime` (nested-runtime guard), `rng`, `budget` (coop).

---

## 5. How it interacts with the other blocks

```
            spawn(fut) / wake()                     Notified handles
 [Tasks] ─────────────────────────▶ schedule_task ─────────────▶ LIFO slot / local queue / inject queue
 [Sync]  ── waker.wake() ─┐                                       │
 [I/O drv] ─ wake() ──────┼──▶ Harness::schedule ─▶ Handle::schedule_task
 [Timer drv] ─ wake() ────┘                                       ▼
                                                    Context::run → run_task → task.run()  ──▶ [Tasks] Harness::poll
                                                          │ no work
                                                          ▼
                                     Parker::park ── try_lock(driver) ─┬─▶ [Timer drv] park(timeout) ─▶ [I/O drv] epoll_wait
                                                                       └─▶ condvar wait
 [Blocking pool] ◀── Launch::launch / block_in_place: worker threads are spawned as blocking tasks
```

| Other block | Direction | Through |
|---|---|---|
| Tasks | ↔ | `Schedule` trait (`schedule`, `release`, `yield_now`, `hooks`); `OwnedTasks::bind/assert_owner/close_and_shutdown_all`; `Notified::run` |
| Timer & I/O drivers | → park; ← unpark | `driver::Driver::park/park_timeout/shutdown`; `driver::Handle::unpark` |
| Blocking pool | → | `blocking::Spawner` (worker threads and `block_in_place` replacements are spawned there) |
| Sync | ← | Indirect only — sync primitives call `Waker::wake`, which lands in `schedule_task` |
| Every API block | ← | `context::with_current` to find the runtime (`spawn`, `sleep`, `TcpStream::connect`, …) |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `Builder::new_multi_thread / new_current_thread / build` | `builder.rs` | Configure and construct a runtime |
| `build_threaded_runtime` | `builder.rs` | Driver stack + blocking pool + `MultiThread::new` + `launch` |
| `Runtime::block_on` | `runtime.rs` | Run a future to completion on the calling thread |
| `Runtime::spawn / spawn_blocking / enter / shutdown_timeout / shutdown_background` | `runtime.rs` | Public runtime control |
| `Handle::current / try_current / spawn / block_on / metrics` | `handle.rs` | Cloneable runtime reference |
| `enter_runtime` | `context/runtime.rs` | Mark thread as inside a runtime; panic if nested |
| `with_current`, `with_scheduler`, `budget`, `defer`, `thread_rng_n` | `context.rs` | Access the thread-local context |
| `Launch::launch`, `run(worker)` | `multi_thread/worker.rs` | Start each worker thread |
| `Context::run` | `worker.rs` | **The worker main loop** |
| `Context::run_task` | `worker.rs` | Poll a task, then drain the LIFO slot within one coop budget |
| `Core::next_task / next_local_task / steal_work` | `worker.rs` | Choose the next task |
| `Context::park / park_internal / park_yield / maintenance` | `worker.rs` | Sleep in the driver; periodic driver polls |
| `Handle::schedule_task / schedule_local / push_remote_task` | `worker.rs` | Where a woken/spawned task goes |
| `notify_parked_local / notify_parked_remote / notify_all` | `worker.rs` | Wake sleeping workers |
| `Idle::worker_to_notify / transition_worker_to_searching / transition_worker_to_parked` | `idle.rs` | Throttle searchers, pick who to wake |
| `Local::push_back_or_overflow / pop`, `Steal::steal_into` | `queue.rs` | Local queue ops; overflow half to inject; steal half |
| `Inject::push / pop / pop_n / close` | `inject/*.rs` | Global queue |
| `Parker::park / park_timeout`, `Unparker::unpark` | `multi_thread/park.rs` | Driver-or-condvar sleeping |
| `Stats::tuned_global_queue_interval` | `stats.rs` | EWMA → how often to check the inject queue |
| `block_in_place`, `maybe_move_runtime` | `worker.rs` | Hand the core to a new thread |
| `Handle::shutdown`, `Core::pre_shutdown`, `Handle::shutdown_core` | `handle.rs`, `worker.rs` | Ordered shutdown |
| `CurrentThread::block_on`, `CoreGuard::block_on`, `current_thread::Handle::schedule` | `current_thread/mod.rs` | Single-thread variant |
| `RuntimeMetrics::*` | `metrics/runtime.rs` | ~40 read-only metric accessors |

---

## 7. Flows

**Worker loop** (`Context::run`), every iteration:
1. `tick += 1`; every **61** ticks `maintenance()` → poll drivers with zero timeout, check shutdown flag, publish metrics.
2. `next_task()`: every `global_queue_interval` ticks check the inject queue first; otherwise LIFO slot → local queue → a fair batch (`inject.len / workers + 1`) from the inject queue.
3. `run_task()`: poll it; keep running LIFO-slot tasks (max 3 in a row) while the 128-unit budget lasts.
4. Nothing local → `steal_work()` (if fewer than half the workers are already searching): random victim, steal ⌈n/2⌉.
5. Still nothing → `park()`: register as sleeper → `Parker::park` → whoever gets the driver lock sleeps in `epoll_wait` (timeout = next timer), others on a condvar.

**Where a scheduled task goes** (`schedule_task`):
- On a worker of this runtime holding a core → LIFO slot (displaced task → local queue) or local queue if it's a yield; overflow → half to inject.
- Anywhere else → inject queue + wake one sleeping worker — only if no worker is searching and not all workers are already awake (`Idle::notify_should_wakeup`).

**Shutdown:** `close()` the inject queue → `notify_all` → each worker sees `is_shutdown` in `maintenance` → `pre_shutdown` cancels all owned tasks → `shutdown_core`; the last one drains every queue and shuts down the drivers.

---

## 8. Invariants & gotchas

- **Only the thread holding a `Core` may touch it.** Everything other threads need (stealing, unparking) is in `Remote`/`Shared`.
- **Exactly one parked worker owns the driver** (`TryLock<Driver>`). Waking that worker = writing to mio's waker (`driver.unpark()`); waking the others = condvar.
- **At most ~half the workers search at once**; a searcher that finds work wakes another to keep searching (avoid thundering herd *and* lost work).
- **LIFO slot is capped** (3 polls/tick) to prevent ping-pong starvation; LIFO tasks are not stealable.
- **Both** the inject queue and `OwnedTasks` have a closed bit; the proof is in the `worker.rs` header comment.
- The `block_on` future of a multi-thread runtime is **not** on a worker — it runs on the caller's thread with `CachedParkThread`.
- Calling `block_on` inside a runtime panics (`enter_runtime`).

---

## 9. Tests & where to start

<!-- TESTS:scheduler -->
**21 integration test files · 230 test functions · 4,852 code lines**

[`rt_basic.rs`](../../tokio/tests/rt_basic.rs), [`rt_blocking_thread_exhaust.rs`](../../tokio/tests/rt_blocking_thread_exhaust.rs), [`rt_busy_tick.rs`](../../tokio/tests/rt_busy_tick.rs), [`rt_common.rs`](../../tokio/tests/rt_common.rs), [`rt_common_before_park.rs`](../../tokio/tests/rt_common_before_park.rs), [`rt_emscripten_block_on.rs`](../../tokio/tests/rt_emscripten_block_on.rs), [`rt_emscripten_jspi.rs`](../../tokio/tests/rt_emscripten_jspi.rs), [`rt_handle.rs`](../../tokio/tests/rt_handle.rs), [`rt_handle_block_on.rs`](../../tokio/tests/rt_handle_block_on.rs), [`rt_local.rs`](../../tokio/tests/rt_local.rs), [`rt_metrics.rs`](../../tokio/tests/rt_metrics.rs), [`rt_multi_thread_emscripten.rs`](../../tokio/tests/rt_multi_thread_emscripten.rs), [`rt_panic.rs`](../../tokio/tests/rt_panic.rs), [`rt_poll_callbacks.rs`](../../tokio/tests/rt_poll_callbacks.rs), [`rt_shutdown_err.rs`](../../tokio/tests/rt_shutdown_err.rs), [`rt_spawn_blocking.rs`](../../tokio/tests/rt_spawn_blocking.rs), [`rt_threaded.rs`](../../tokio/tests/rt_threaded.rs), [`rt_time_start_paused.rs`](../../tokio/tests/rt_time_start_paused.rs), [`rt_unstable_eager_driver_handoff.rs`](../../tokio/tests/rt_unstable_eager_driver_handoff.rs), [`rt_unstable_metrics.rs`](../../tokio/tests/rt_unstable_metrics.rs), … (+1 more)
<!-- /TESTS -->

**Read in this order:** `current_thread/mod.rs` (whole scheduler in one file) → `multi_thread/worker.rs` header comment → `Context::run` → `queue.rs` → `idle.rs` → `park.rs`.
**Contribution areas seen in history:** builder options and their docs, metrics, `LocalRuntime`, `spawn_blocking`/shutdown edge cases, loom tests.
