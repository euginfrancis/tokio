# Scheduler component 1 — `Runtime`, `Handle`, `Builder`, `Config` and the flavor dispatch (`runtime/{runtime,handle,builder,config}.rs`, `scheduler/mod.rs`)

> **One sentence:** this is the *composition root* of Tokio — `Builder` turns user options into an immutable `Config`, builds the driver stack, blocking pool and one of two schedulers, and returns a `Runtime` (owner) plus cheap `Handle`s (shared references); an `enum` (not a trait object) dispatches every call to the right flavor.

---

## 1. Where it lives

<!-- FILES:s_runtime -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/runtime.rs`](../../../tokio/src/runtime/runtime.rs) | 178 | 385 | 15 |
| [`tokio/src/runtime/handle.rs`](../../../tokio/src/runtime/handle.rs) | 254 | 460 | 22 |
| [`tokio/src/runtime/builder.rs`](../../../tokio/src/runtime/builder.rs) | 586 | 1,540 | 53 |
| [`tokio/src/runtime/config.rs`](../../../tokio/src/runtime/config.rs) | 30 | 24 | 0 |
| **Total (4 files)** | **1,048** | **2,409** | **90** |
<!-- /FILES -->

---

## 2. Objects and ownership

```
Runtime  (pub; owner — dropping it shuts everything down)
 ├── scheduler: Scheduler            enum { CurrentThread(CurrentThread), MultiThread(MultiThread) }   ← the "driver seat" (block_on)
 ├── handle:    Handle { inner: scheduler::Handle }                                                     ← what everyone else clones
 └── blocking_pool: BlockingPool                                                                        ← owned here so Drop waits for its threads

scheduler::Handle  (pub(crate) enum, Clone = Arc clone)
 ├── CurrentThread(Arc<current_thread::Handle>)
 └── MultiThread(Arc<multi_thread::Handle>)
        each Handle holds: shared scheduler state (queues, OwnedTasks, config, metrics)
                           driver::Handle (I/O + timer + signal handles)    blocking::Spawner
                           seed_generator, task_hooks, name, …
```

| Type | Role | Cloneable? | Lives |
|---|---|---|---|
| `Runtime` | owns the scheduler "seat" and the blocking pool; `block_on`, `shutdown_*`, `Drop` | no | the whole runtime lifetime |
| `Runtime::scheduler: Scheduler` | `CurrentThread{ core: AtomicCell<Core>, notify: Notify }` or `MultiThread` (a unit struct — all state is in the `Handle`) | no | |
| `runtime::Handle { inner }` | public handle: `spawn`, `spawn_blocking`, `block_on`, `enter`, `current`, `metrics`, `id`, `runtime_flavor` | **yes** (`Arc`) | held by `Runtime`, by the thread-local context, by every task (`Core.scheduler`) and by sockets/timers |
| `scheduler::Handle` | the dispatch enum | yes | |
| `EnterGuard<'a>` | RAII from `Handle::enter()`: sets the thread's "current runtime" | no (`!Send`) | |
| `TryCurrentError` | `NoContext` / `ThreadLocalDestroyed` | – | |

**Why an enum, not `dyn Scheduler`:** both flavors are known at compile time; matching on a 2-variant enum is a predictable branch, lets the compiler inline `spawn`, keeps `Handle` thin, and avoids a vtable for the hottest call in a server. `match_flavor!` (a macro in `scheduler/mod.rs`) generates the repetitive dispatch for ~20 methods (`blocking_spawner`, `seed_generator`, `num_alive_tasks`, `injection_queue_depth`, `worker_metrics`, …).

---

## 3. `Builder` → `Config` → schedulers (data flow)

```
 Builder::new_multi_thread() / new_current_thread()        (event_interval = 61; loom: 4)
        │  fluent setters (≈ 60): worker_threads, max_blocking_threads, thread_name, thread_stack_size, thread_keep_alive,
        │      enable_io / enable_time / enable_all, start_paused, event_interval, global_queue_interval, disable_lifo_slot,
        │      on_thread_start/stop/park/unpark, on_task_spawn/terminate/before_poll/after_poll, rng_seed, metrics_*, unhandled_panic …
        ▼
 Builder::build()  →  match kind { CurrentThread => build_current_thread_runtime(), MultiThread => build_threaded_runtime() }
        │
        ├─ 1. driver::Driver::new(self.get_cfg())                    // Cfg { enable_pause_time, enable_io, enable_time, start_paused, nevents, nevents_busy, timer_flavor }
        │       enable_pause_time = true ONLY for CurrentThread       // paused-clock tests need a single driver thread
        ├─ 2. blocking::create_blocking_pool(self, thread_cap, scheduler_threads)
        │       multi-thread: thread_cap = max_blocking_threads + worker_threads, scheduler_threads = worker_threads
        │       current-thread: max_blocking_threads, 0
        ├─ 3. seed_generator_1/2 = self.seed_generator.next_generator()           // deterministic RNG streams (rng_seed)
        ├─ 4. Config { …all the knobs… }                                          // immutable snapshot, moved into the scheduler
        ├─ 5. MultiThread::new(workers, driver, driver_handle, blocking_spawner, seed, config, timer_flavor, name)
        │      or CurrentThread::new(driver, driver_handle, blocking_spawner, seed, config, local_tid, name)
        ├─ 6. multi-thread only: `let _enter = handle.enter(); launch.launch();`      // start N worker threads (as blocking tasks)
        └─ 7. Runtime::from_parts(Scheduler, Handle, BlockingPool)
```

### Defaults worth knowing (from `Builder::new`)
| Setting | Default |
|---|---|
| `enable_io`, `enable_time`, `start_paused` | `false` (`#[tokio::main]`/`Runtime::new` call `enable_all`) |
| `nevents` (I/O events per `epoll_wait`) | `1024` |
| `worker_threads` | `num_cpus` (`std::thread::available_parallelism`, or `TOKIO_WORKER_THREADS` env) |
| `max_blocking_threads` | `512` (extra, beyond workers) |
| thread name | `"tokio-rt-worker"` |
| `keep_alive` for idle blocking threads | `None` → 10 s |
| `event_interval` | **61** ticks |
| `global_queue_interval` | `None` → self-tuned (multi-thread, 2..127) / **31** (current-thread) |
| `disable_lifo_slot` | `false` |
| `unhandled_panic` | `Ignore` |
| timer flavor | `Traditional` |

### `Config` — the immutable DTO handed to a scheduler
`global_queue_interval: Option<u32>`, `event_interval: u32`, hooks `before_park/after_unpark: Option<Callback>`, `before_spawn/after_termination/before_poll/after_poll: Option<TaskCallback>`, `disable_lifo_slot`, `seed_generator`, `metrics_poll_count_histogram`, `track_task_schedule_latency`, `metrics_schedule_latency_histogram`, `unhandled_panic`, `enable_eager_driver_handoff`. The current-thread builder forces `enable_eager_driver_handoff: false` ("only configures how the I/O driver is stolen across workers").

---

## 4. `Runtime` and `Handle` — interface

| Method | On | What it does |
|---|---|---|
| `Runtime::new()` | `Runtime` | `Builder::new_multi_thread().enable_all().build()` |
| `block_on(fut)` | `Runtime`, `Handle` | box if `size_of::<F>() > BOX_FUTURE_THRESHOLD` → `enter()` → **`Scheduler::block_on`** (Runtime) or `context::enter_runtime(handle, true, |b| b.block_on(fut))` (**Handle** — runs on `CachedParkThread`, *never* drives the scheduler) |
| `spawn(fut)` | both | box if large → `spawn_named` → `Id::next()` → `scheduler::Handle::spawn` → flavor `Handle::spawn` → `OwnedTasks::bind` + `schedule` |
| `spawn_blocking(f)` | both | `blocking_spawner().spawn_blocking(handle, f)` |
| `enter()` | both | `EnterGuard` that makes this runtime "current" on this thread |
| `Handle::current() / try_current()` | `Handle` | clone of the thread-local current handle, or panic / `Err(TryCurrentError)` |
| `metrics()` | both | `RuntimeMetrics::new(handle.clone())` |
| `id()` | `Handle` | `runtime::Id::new(owned_tasks.id)` — the same id stamped into every task's `Header.owner_id` |
| `runtime_flavor()`, `name()` | `Handle` | |
| `shutdown_timeout(d)` / `shutdown_background()` | `Runtime` | `handle.inner.shutdown()` then `blocking_pool.shutdown(Some(d))` (`0 ns` for background) |
| `Drop for Runtime` | `Runtime` | current-thread: set current, `CurrentThread::shutdown`; multi-thread: `Handle::shutdown`; then fields drop — **`BlockingPool::drop` joins all threads (incl. workers)** |
| `dump()` | `Handle` (`taskdump`, unstable) | async backtraces of every task |

**`Runtime::block_on` vs `Handle::block_on`:** with a *current-thread* runtime, `Runtime::block_on` makes the calling thread **become the scheduler** (it takes the `Core` out of the `AtomicCell`). `Handle::block_on` never does — it only polls your future on a parker, so on a current-thread runtime other tasks only advance if some other thread is driving the runtime. This is documented behaviour and a classic source of "my spawned task never runs" reports.

### Dispatch enum internals (`scheduler/mod.rs`)
```rust
pub(crate) enum Handle { CurrentThread(Arc<current_thread::Handle>), MultiThread(Arc<multi_thread::Handle>), /* Disabled when `rt` is off */ }
pub(super) enum Context { CurrentThread(current_thread::Context), MultiThread(multi_thread::Context) }   // thread-local scheduler context
```
Notable methods: `Handle::{current, spawn, spawn_local (unsafe, LocalRuntime), shutdown, blocking_spawner, seed_generator, hooks, driver, num_workers (1 or N), num_alive_tasks, injection_queue_depth, worker_metrics, timer_flavor, is_local, can_spawn_local_on_local_runtime, as_current_thread}`; `Context::{defer(&Waker), worker_index, expect_current_thread, expect_multi_thread}`.

---

## 5. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| User / `#[tokio::main]` | user → Builder/Runtime | options; futures; `JoinHandle`s back |
| Drivers ([I/O](../../components/08-io-driver.md), [timer](../../components/07-timer-driver.md)) | Builder → | `driver::Cfg`; gets back `Driver` (owned by the scheduler `Core`/`Parker`) + `driver::Handle` (shared) |
| [Blocking pool](../../components/09-blocking-pool.md) | Builder → | `create_blocking_pool(builder, cap, scheduler_threads)`; `Spawner` stored in every `Handle` |
| [Task core](../task/05-handles-and-schedule.md) | `Handle::spawn` → `OwnedTasks::bind` | `future`, `Arc<Handle>` as `Schedule`, `Id`, `SpawnLocation` |
| [Thread-local context](./02-context-thread-local.md) | `Handle::enter`, `enter_runtime` | `scheduler::Handle` clones |
| Schedulers ([current-thread](./03-current-thread.md), [multi-thread](./04-multithread-state-and-spawn.md)) | Builder → `new(...)` | `Config`, `Driver`, `driver::Handle`, `Spawner`, seed generators |
| Sockets / timers / blocking tasks | ← `Handle::current()` | a `scheduler::Handle` clone stored in `Registration`/`Sleep` |

---

## 6. Invariants

1. A `Runtime` has exactly one scheduler flavor for its lifetime; `Handle` clones keep the shared state alive after the `Runtime` is dropped, but they refuse new work (`OwnedTasks` closed ⇒ `spawn` returns an immediately-cancelled `JoinHandle`).
2. `Builder::build` never panics on config errors that are checkable: e.g. `worker_threads(0)` panics at the setter (`assert!`), `thread_keep_alive` etc. are plain values.
3. Worker threads are started **inside** `handle.enter()` so the runtime context is already current when they begin.
4. `Config` is cloned/copied into the scheduler once; later `Builder` mutations don't affect a built runtime.

---

## 7. Tests

<!-- TESTS:s_runtime -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_basic.rs`](../../../tokio/tests/rt_basic.rs) | 16 | 416 |
| [`tokio/tests/rt_common.rs`](../../../tokio/tests/rt_common.rs) | 49 | 1,050 |
| [`tokio/tests/rt_handle.rs`](../../../tokio/tests/rt_handle.rs) | 7 | 93 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [02 — Thread-local context](./02-context-thread-local.md).
