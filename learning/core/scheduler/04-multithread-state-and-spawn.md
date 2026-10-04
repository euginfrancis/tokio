# Scheduler component 4 — Multi-Thread Scheduler: Shared State, Construction & the Spawn Path (`scheduler/multi_thread/{mod,handle,worker}.rs`)

> **One sentence:** the work-stealing scheduler is *N workers sharing one `Arc<Handle>`*: each worker owns a movable `Core` (run queue, LIFO slot, RNG, stats), all workers expose a small `Remote` (steal handle + unparker) to each other, and everything cross-thread — inject queue, idle tracking, `OwnedTasks`, shutdown collection — lives in a single `Shared` struct.

This document is the **map** of the multi-thread scheduler's data; [05 — worker loop](./05-worker-loop.md) is the behaviour that runs over it.

---

## 1. Where it lives

<!-- FILES:s_mt_state -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/scheduler/multi_thread/mod.rs`](../../../tokio/src/runtime/scheduler/multi_thread/mod.rs) | 79 | 7 | 4 |
| [`tokio/src/runtime/scheduler/multi_thread/handle.rs`](../../../tokio/src/runtime/scheduler/multi_thread/handle.rs) | 105 | 10 | 11 |
| [`tokio/src/runtime/scheduler/mod.rs`](../../../tokio/src/runtime/scheduler/mod.rs) | 252 | 14 | 30 |
| **Total (3 files)** | **436** | **31** | **45** |
<!-- /FILES -->

(`worker.rs` is shared with docs 05, 11 and 12 — it holds the data (this doc), the loop (05), `block_in_place` (11) and shutdown (12).)

---

## 2. The data model

```
                                   Arc<Handle>   (multi_thread/handle.rs)
        ┌───────────────────────────────────────────────────────────────────────────────────────────┐
        │ name, shared: Shared, driver: driver::Handle, blocking_spawner, seed_generator, task_hooks,│
        │ timer_flavor, [is_shutdown: AtomicBool]                                                      │
        └──────────────┬────────────────────────────────────────────────────────────────────────────┘
                       ▼
        Shared  (worker.rs)                                      — touched by ALL threads
        ├─ remotes: Box<[Remote]>   ───────────────┐   one per worker:
        ├─ inject:  InjectQueue<Arc<Handle>>        │     Remote { steal: queue::Steal<Arc<Handle>>,   // others steal from this worker's local queue
        ├─ idle:    Idle  { state: AtomicUsize }    │                unpark: Unparker }                // others wake this worker
        ├─ owned:   OwnedTasks<Arc<Handle>>         │
        ├─ synced:  Mutex<Synced { idle: idle::Synced{ sleepers: Vec<usize> }, [inject_timers] }>
        ├─ shutdown_cores: Mutex<Vec<Box<Core>>>    │
        ├─ trace_status, config: Config, scheduler_metrics, worker_metrics: Box<[WorkerMetrics]>,
        ├─ schedule_latency_start: Option<Instant>, _counters
        ▼
   Workers (one per thread) —— each:  Arc<Worker { handle: Arc<Handle>, index: usize, core: AtomicCell<Core> }>
        ▼
   Core (Box, MOVABLE, touched only by the thread currently holding it)
        ├─ tick: u32, lifo_slot: Option<Notified>, lifo_enabled: bool
        ├─ run_queue: queue::Local<Arc<Handle>>        // the producer end of this worker's 256-slot ring
        ├─ park: Option<Parker>                         // taken out during park
        ├─ is_searching, is_shutdown, is_traced, had_driver: HadDriver, enable_eager_driver_handoff
        ├─ stats: Stats                                 // metrics batch + EWMA of poll time
        ├─ global_queue_interval: u32, rand: FastRand
        ▼
   Context (on the worker thread's stack; reachable via the thread-local Scoped pointer)
        ├─ worker: Arc<Worker>
        ├─ core: RefCell<Option<Box<Core>>>             // the core is "in" the context only while a task is being polled / parking
        └─ defer: Defer                                 // wakers to fire after the next driver poll (yield_now, coop exhaustion)
```

### Field-by-field access rules (who may touch what)

| Field | Touched by | Synchronisation |
|---|---|---|
| `Core.*` | the one thread holding the `Box<Core>` | none needed (exclusive); moves between threads via `AtomicCell` (`block_in_place`) or `shutdown_cores` |
| `Core.run_queue` (`Local`) | holder only (push/pop) | the ring's own atomics let **others** steal concurrently (see [06](./06-local-queue.md)) |
| `Remote.steal` | **any** worker | lock-free (`steal_into`) |
| `Remote.unpark` | any thread | atomic state + condvar/driver wake ([09](./09-parker.md)) |
| `Shared.inject` | any thread | mutex + atomic `len` ([07](./07-inject-queue.md)) |
| `Shared.idle.state` | any thread | `SeqCst` atomics; sleeper *list* under `synced` mutex ([08](./08-idle-coordination.md)) |
| `Shared.owned` | any thread | sharded mutexes ([task 08](../task/08-owned-tasks.md)) |
| `Shared.shutdown_cores` | workers at shutdown | mutex ([12](./12-shutdown.md)) |
| `Worker.core: AtomicCell<Core>` | the worker thread at startup; `block_in_place` hand-off | atomic pointer swap |
| `Context.core: RefCell<Option<Box<Core>>>` | the holding thread | single-threaded; `None` ⇔ the core was handed away (block_in_place) or is parked with the parker taken |
| `Context.defer` | the holding thread | `RefCell` |

`Core` is **boxed and moved** rather than borrowed so it can be (a) stolen by a replacement worker thread during `block_in_place`, and (b) collected at shutdown into `Shared.shutdown_cores`, *without* being returned to its `Worker` (to prevent a block_in_place thread from re-acquiring it).

---

## 3. Construction: `MultiThread::new` → `worker::create`

```rust
MultiThread::new(size, driver, driver_handle, blocking_spawner, seed_generator, config, timer_flavor, name)
    -> (MultiThread /* unit struct */, Arc<Handle>, Launch)
{
    let parker = Parker::new(driver);                                  // the ONE driver, behind Arc<Shared{ driver: TryLock<Driver> }>
    let (handle, launch) = worker::create(size, parker, driver_handle, blocking_spawner, seed_generator, config, timer_flavor, name);
    (MultiThread, handle, launch)
}
```
`worker::create` (annotated):
```rust
for _ in 0..size {
    let (steal, run_queue) = queue::local();                  // Arc<Inner{head,tail,buffer[256]}> split into the two handle types
    let park   = park.clone();                                // NEW Inner(state,mutex,condvar) per worker, SHARED driver Arc
    let unpark = park.unpark();
    let metrics = WorkerMetrics::from_config(&config);
    let stats   = Stats::new(&metrics);
    cores.push(Box::new(Core { tick: 0, lifo_slot: None, lifo_enabled: !config.disable_lifo_slot, run_queue,
        is_searching: false, is_shutdown: false, is_traced: false, had_driver: HadDriver::No,
        enable_eager_driver_handoff: config.enable_eager_driver_handoff, park: Some(park), 
        global_queue_interval: stats.tuned_global_queue_interval(&config),      // initial value from the seeded EWMA (≈61)
        stats, rand: FastRand::from_seed(config.seed_generator.next_seed()) }));   // per-worker deterministic RNG stream
    remotes.push(Remote { steal, unpark });  worker_metrics.push(metrics);
}
let (idle, idle_synced) = Idle::new(size);                    // all `size` workers start counted as "unparked"
let handle = Arc::new(Handle { …, shared: Shared { remotes, inject: InjectQueue::new(), idle, owned: OwnedTasks::new(size),
                               synced: Mutex::new(Synced{ idle: idle_synced, … }), shutdown_cores: Mutex::new(vec![]), … } });
let launch = Launch(cores.into_iter().enumerate().map(|(index, core)| Arc::new(Worker{ handle: handle.clone(), index, core: AtomicCell::new(Some(core)) })).collect());
```
Starting the threads (`Builder::build_threaded_runtime`, inside `handle.enter()`):
```rust
impl Launch { pub(crate) fn launch(mut self) { for worker in self.0.drain(..) { runtime::spawn_blocking(move || run(worker)); } } }
```
Each worker thread is therefore a **blocking-pool task** (`thread_cap = max_blocking_threads + workers`), named with the builder's `thread_name`.

---

## 4. The spawn path through this component

```
Handle::spawn(me, future, id, spawned_at) → bind_new_task(me, future, id, spawned_at)
    let (handle, notified) = me.shared.owned.bind(future, me.clone(), id, spawned_at);     // task core: allocate, register, maybe closed⇒None
    me.task_hooks.spawn(&TaskMeta { id, spawned_at, … });                                   // on_task_spawn (unstable)
    me.schedule_option_task_without_yield(notified);                                        // if Some → schedule_task(task, is_yield = false)
    handle                                                                                   // JoinHandle to the user

Handle::schedule_task(&self, task: Notified, is_yield: bool):
    (stamp scheduled_at if latency tracking)
    with_current(|maybe_cx| {                                    // thread-local scheduler Context, MultiThread variant only
        if let Some(cx) = maybe_cx {
            if self.ptr_eq(&cx.worker.handle) {                  // a worker of THIS runtime…
                if let Some(core) = cx.core.borrow_mut().as_mut() {          // …currently holding its core
                    self.schedule_local(core, task, is_yield);   // fast path, no locks
                    return;
                }
            }
        }
        self.push_remote_task(task);                             // inject queue (+ remote_schedule_count metric)
        self.notify_parked_remote();                             // wake ONE sleeper, only if nobody is searching
    })
```

### `schedule_local(core, task, is_yield)` — where a task goes on a worker
```rust
core.stats.inc_local_schedule_count();
let should_notify = if is_yield || !core.lifo_enabled {
    core.run_queue.push_back_or_overflow(task, self /* as Overflow */, &mut core.stats);   // back of the ring; may overflow half to inject
    true
} else {
    let prev = core.lifo_slot.take();                            // LIFO: newest task runs next
    let ret  = prev.is_some();
    if let Some(prev) = prev { core.run_queue.push_back_or_overflow(prev, self, &mut core.stats); }   // displaced task goes to the ring
    core.lifo_slot = Some(task);
    ret                                                          // only notify if something became stealable
};
if should_notify && core.park.is_some() { self.notify_parked_local(); }   // `park == None` ⇒ we're inside the driver park: notification delayed until it ends
```
| Situation | Destination | Why |
|---|---|---|
| woken/spawned by a task on a worker (non-yield, LIFO enabled) | `lifo_slot` | cache locality, request/response latency; stealers can't see the slot, so *no wake-up needed* unless it displaced another task |
| `yield_now`, budget-exhausted wake, `lifo` disabled | back of `run_queue` | fairness; stealable |
| spawned/woken from a non-worker thread, a worker of another runtime, or a worker whose core was handed away | `inject` | any worker may take it |
| local ring full | **half the ring + this task → inject** (`push_overflow`) | bounded local memory, load balancing |

### Waking workers
```rust
fn notify_parked_local(&self) -> bool {
    if let Some(index) = self.shared.idle.worker_to_notify(&self.shared) {      // None if someone is already searching / all awake
        self.shared.remotes[index].unpark.unpark(&self.driver);  true
    } else { false }
}
fn notify_parked_remote(&self) { same, no return value }
fn notify_all(&self)           { for remote in remotes { remote.unpark.unpark(&self.driver) } }          // shutdown
fn notify_if_work_pending(&self) {                                                                       // after the last searcher parks
    for remote in remotes { if !remote.steal.is_empty() { self.notify_parked_local(); return } }
    if !self.shared.inject.is_empty() { self.notify_parked_local(); }
}
```

### `Overflow` (the queue → scheduler callback)
```rust
impl Overflow<Arc<Handle>> for Handle {
    fn push(&self, task)              { self.push_remote_task(task) }                 // single task to inject
    fn push_batch<I>(&self, iter: I)  { self.shared.inject.push_batch(iter) }         // 129 tasks linked then inserted with ONE lock acquisition
}
```
This trait is why `queue.rs` doesn't depend on `Handle`: the ring only needs *"somewhere to dump tasks"* (it is unit-tested against a `RefCell<Vec<_>>`).

---

## 5. Other `Handle` members

| Member | Meaning |
|---|---|
| `shutdown()` | `close()` (close inject; `notify_all` if it was open) — [12](./12-shutdown.md) |
| `owned_id()`, `name()` | `OwnedTasks.id` (= `runtime::Id`), runtime name |
| `num_workers()`, `num_alive_tasks()`, `injection_queue_depth()`, `worker_metrics(i)`, `worker_local_queue_depth(i)`, unstable `spawned_tasks_count`, `num_blocking_threads`, `blocking_queue_depth` | `RuntimeMetrics` sources ([10](./10-stats-and-metrics.md)) |
| `trace_core`, `dump()` (taskdump, unstable) | async backtraces: workers pause, trace their tasks, resume (`multi_thread/{trace,worker/taskdump,handle/taskdump}.rs`; a no-op mock when the feature is off) |
| `push_remote_timer`, `take_remote_timers` (unstable alt-timer) | timers registered from non-worker threads |
| `impl Schedule for Arc<Handle>` | `release` = `owned.remove`; `schedule` = `schedule_task(.., false)`; `yield_now` = `schedule_task(.., true)`; `hooks` |

---

## 6. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| [Builder](./01-runtime-handle-builder.md) | → | `Config`, `Driver`, `driver::Handle`, `Spawner`, seeds → `(Arc<Handle>, Launch)` |
| [Task core](../task/05-handles-and-schedule.md) | ↔ | `owned.bind`, `Notified`, `Schedule` impl, `assert_owner`, `release`, `close_and_shutdown_all` |
| [Worker loop](./05-worker-loop.md) | data → behaviour | the `Core`/`Context`/`Shared` described here |
| [Local queue](./06-local-queue.md) | `Core.run_queue` / `Remote.steal` | `Local`, `Steal`, `Overflow` |
| [Inject queue](./07-inject-queue.md) | `Shared.inject` | `Notified` pushes/pops, batches |
| [Idle](./08-idle-coordination.md) / [Parker](./09-parker.md) | `Shared.idle`, `Remote.unpark`, `Core.park` | worker indices, wake-ups |
| [Blocking pool](../../components/09-blocking-pool.md) | `Launch::launch`, `block_in_place` | `spawn_blocking(move || run(worker))` |
| [Context](./02-context-thread-local.md) | `with_current` | `&multi_thread::Context` |

---

## 7. Invariants

1. `remotes.len() == worker_metrics.len() == number of Workers == Idle.num_workers == OwnedTasks shard basis`.
2. Every `Core` is in exactly one place: inside a `Worker.core` cell (not started / being handed over), inside a thread's `Context.core`, or in `Shared.shutdown_cores`.
3. A `Notified` is in exactly one of: a `lifo_slot`, a `run_queue` ring, the inject list, or being polled — never two (state bit `NOTIFIED`).
4. All workers start "unparked"; `idle.state.num_unparked == size` initially.
5. `schedule_local` is only used when the *thread-local* context proves the caller is a worker of this very `Handle` holding its core.

---

## 8. Tests

<!-- TESTS:s_mt_state -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/rt_threaded.rs`, `time_alt.rs` (alternative timer), `rt_unstable_eager_driver_handoff.rs`, `rt_common.rs`, `rt_metrics.rs`/`rt_unstable_metrics.rs`, and the loom suite `runtime/tests/loom_multi_thread/{queue,shutdown,yield_now}.rs` + `loom_multi_thread.rs`.

**Read next:** [05 — The worker loop](./05-worker-loop.md).
