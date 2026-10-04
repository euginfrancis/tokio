# Scheduler component 3 — The Current-Thread Scheduler (`runtime/scheduler/current_thread/mod.rs`)

> **One sentence:** a complete Tokio scheduler in ~900 lines — one `VecDeque` run queue, one inject queue, one `Core` that is *passed around like a baton*: whichever thread calls `block_on` takes the core, **becomes** the scheduler for the duration, and gives it back (waking another waiter) when done.

It is the best place to learn the scheduler contract before reading the work-stealing one, because every concept is present in minimal form: `OwnedTasks`, `schedule`, `tick`, `event_interval`, `global_queue_interval`, park/yield, defer, shutdown.

---

## 1. Where it lives

<!-- FILES:s_current -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/scheduler/current_thread/mod.rs`](../../../tokio/src/runtime/scheduler/current_thread/mod.rs) | 623 | 131 | 46 |
<!-- /FILES -->

---

## 2. Objects

```rust
pub(crate) struct CurrentThread { core: AtomicCell<Core>, notify: Notify }        // the "seat" held by Runtime::scheduler

pub(crate) struct Handle {                          // shared (Arc): spawn, schedule, wake, shutdown reach it from any thread
    name: Option<String>,
    shared: Shared,
    pub(crate) driver: driver::Handle,              // I/O + timer + signal handles
    pub(crate) blocking_spawner: blocking::Spawner,
    pub(crate) seed_generator: RngSeedGenerator,
    pub(crate) task_hooks: TaskHooks,
    pub(crate) local_tid: Option<ThreadId>,         // Some(thread) for a LocalRuntime: pins the runtime to its creating thread
}
struct Shared {
    inject: Inject<Arc<Handle>>,                    // MPSC list + mutex + atomic len (see 07-inject-queue)
    owned: OwnedTasks<Arc<Handle>>,                 // all live tasks; new(1) ⇒ 4 shards
    woken: AtomicBool,                              // "the block_on future was woken"
    config: Config, scheduler_metrics, worker_metrics: WorkerMetrics, schedule_latency_start: Option<Instant>,
}
struct Core {                                       // the baton — only the holder may touch it
    tasks: VecDeque<Notified>,                      // local run queue (initial capacity 64), FIFO
    tick: u32,
    driver: Option<Driver>,                         // taken out while parked, so no one else touches it
    metrics: MetricsBatch,
    global_queue_interval: u32,                     // default 31 (Config.global_queue_interval overrides)
    unhandled_panic: bool,                          // set by Schedule::unhandled_panic under ShutdownRuntime
}
pub(crate) struct Context { handle: Arc<Handle>, core: RefCell<Option<Box<Core>>>, pub(crate) defer: Defer }   // lives on the driving thread's stack
struct CoreGuard<'a> { context: scheduler::Context, scheduler: &'a CurrentThread }                          // RAII: returns the core on drop
```

**Where each piece lives:** `Handle` — heap, shared by all; `Core` — inside the `AtomicCell` when idle, inside `Context.core` while a thread drives; `Context` — on the stack of `CoreGuard::block_on`, exposed to the rest of the runtime through the thread-local `Scoped` pointer ([02](./02-context-thread-local.md)).

---

## 3. The baton protocol (multi-thread `block_on` on a current-thread runtime)

```
CurrentThread::block_on(handle, future):
    pin!(future)
    enter_runtime(handle, allow_block_in_place = false, |blocking| {
        loop {
            if let Some(core) = self.take_core(handle) {                 // AtomicCell::take (swap with null)
                return core.block_on(future)                             //   ← THIS thread is now the scheduler
            } else {
                // someone else is driving: wait until either (a) the core is returned (notify) or (b) our own future finishes
                let notified = self.notify.notified();  pin!(notified);
                if let Some(out) = blocking.block_on(poll_fn(|cx| {
                        if notified.poll(cx).is_ready() { return Ready(None) }      // go and try take_core again
                        if let Ready(out) = future.poll(cx) { return Ready(Some(out)) }
                        Pending
                    })) { return out }
            }
        }
    })

CoreGuard::drop:   self.scheduler.core.set(core);  self.scheduler.notify.notify_one();   // pass the baton on
```
So several threads may call `rt.block_on(..)` on the same current-thread runtime: **one drives, the others park on their own future and take over (driver "theft") when the driver's future finishes**. Their futures are polled by the *driving* thread only if they are spawned tasks; a `block_on` future of a non-driving thread is polled by that thread's `blocking.block_on` loop.

---

## 4. `CoreGuard::block_on` — the entire scheduler loop

```rust
self.enter(|mut core, context| {                 // context::set_scheduler(&context, …) around the closure
    let waker = Handle::waker_ref(&context.handle);       // sets `woken = true` initially (poll the future once); Waker = Wake for Handle
    let mut cx = Context::from_waker(&waker);
    pin!(future);
    core.metrics.start_processing_scheduled_tasks();
    'outer: loop {
        if handle.reset_woken() {                                           // swap(woken, false)
            let (c, res) = context.enter(core, || coop::budget(|| future.as_mut().poll(&mut cx)));
            core = c;  if let Ready(v) = res { return (core, Some(v)) }     // the main future finished
        }
        for _ in 0..handle.shared.config.event_interval {                   // 61 ticks, then service the drivers
            if core.unhandled_panic { return (core, None) }                 // → panics "a spawned task panicked and the runtime is configured to shut down…"
            core.tick();
            let task = match core.next_task(handle) {
                Some(t) => t,
                None => {                                                   // nothing runnable
                    core.metrics.end_processing_scheduled_tasks();
                    core = if context.has_pending_work(&core) { context.park_yield(core, handle) }   // tasks/defer/woken pending → poll drivers, don't sleep
                           else                               { context.park(core, handle) };        // sleep in the driver until an event/unpark
                    core.metrics.start_processing_scheduled_tasks();
                    continue 'outer;                                        // re-check the block_on future
                }
            };
            core = context.run_task(handle.shared.owned.assert_owner(task), core);
        }
        core.metrics.end_processing_scheduled_tasks();
        core = context.park_yield(core, handle);                            // event_interval exhausted: poll I/O + timers without blocking
        core.metrics.start_processing_scheduled_tasks();
    }
})
```

### What each piece does
| Piece | Behaviour |
|---|---|
| `woken` flag + `Wake for Handle` | The `block_on` future is **not** a task; its waker sets `woken` (swap `true`); if it wasn't already set and the caller is **not** on this runtime's thread, `driver.unpark()`. The loop polls the future only when `reset_woken()` returns `true` |
| `next_task` | `tick % global_queue_interval == 0` → inject queue **first**, then local; else local first, then inject (fairness for remote spawns) |
| `run_task(task, core)` | stamps schedule latency, `enter(core, || coop::budget(|| { poll_start hook; task.run(); poll_stop hook }))` — **one 128-unit budget per task** |
| `park(core, handle)` | take the driver out of the core; `before_park` hook (runs *inside* `enter`); if no pending work: submit metrics → `park_internal(None)` (block); else `park_internal(Some(0))` (don't block; but still poll the driver once — see issue #8212 in the source); `after_unpark` hook; put the driver back |
| `park_yield` | `park_internal(Some(0ms))` — poll I/O/timers without sleeping |
| `park_internal` | `enter(core, || driver.park[_timeout](&handle.driver)); self.defer.wake();` ← **wakes all deferred wakers (yield_now / budget-exhausted tasks) after the drivers were polled** |
| `has_pending_work` | `!core.tasks.is_empty() || !defer.is_empty() || shared.woken.load(Acquire)` |

---

## 5. Scheduling a task (`impl Schedule for Arc<Handle>`)

```rust
fn schedule(&self, task: Notified) {
    (stamp scheduled_at if latency tracking is on)
    context::with_scheduler(|maybe_cx| match maybe_cx {
        Some(CurrentThread(cx)) if Arc::ptr_eq(self, &cx.handle) => {         // we are on the thread that drives THIS runtime
            if let Some(core) = cx.core.borrow_mut().as_mut() { core.push_task(self, task); }   // VecDeque::push_back; (core absent ⇒ shutting down ⇒ drop)
        }
        _ => {                                                                  // any other thread, or a different runtime
            self.shared.scheduler_metrics.inc_remote_schedule_count();
            self.shared.inject.push(task);
            self.driver.unpark();                                               // wake the driving thread out of epoll_wait
        }
    })
}
fn release(&self, task) -> Option<Task> { self.shared.owned.remove(task) }
fn hooks(&self) { clone of task_terminate_callback }
fn yield_now(&self, task)   -> default: = schedule()     // current-thread has no LIFO slot, so FIFO already puts it at the back
fn unhandled_panic(&self)   -> unstable: ShutdownRuntime ⇒ core.unhandled_panic = true; owned.close_and_shutdown_all(0)
```
Spawn: `Handle::spawn` → `owned.bind(future, handle.clone(), id, spawned_at)` → `task_hooks.spawn(&TaskMeta{…})` → `schedule(notified)` (if `bind` returned `Some`). `spawn_local` (unsafe; `LocalRuntime` only) uses `bind_local`, which allows `!Send` futures.

---

## 6. Shutdown (`CurrentThread::shutdown` → `shutdown2`)

Triggered by `Drop for Runtime` (after setting the context current):
```
take_core(handle)  → panics "Oh no! We never placed the Core back" if a thread is still driving (unless panicking)
if the thread-local is still alive:  core.enter(|core, _| shutdown2(core, handle))
else:                                 shutdown2 directly without setting the context (spawns would fail anyway)

shutdown2(core, handle):
    1. handle.shared.owned.close_and_shutdown_all(0)       // close list, cancel every task (their wakers/destructors may call schedule → pushes to core.tasks)
    2. while let Some(task) = core.next_local_task(handle) { drop(task) }     // drop queued Notifieds (tasks already cancelled)
    3. handle.shared.inject.close();                        // refuse further remote pushes
    4. while let Some(task) = handle.shared.inject.pop() { drop(task) }       // drop remote Notifieds
    5. assert!(handle.shared.owned.is_empty());
    6. core.submit_metrics(handle);
    7. driver.shutdown(&handle.driver);                     // time: fire all timers with Err; I/O: shut down all ScheduledIo; signal/process
```
Order matters: tasks are cancelled **while the context is still current** so that destructors that call `tokio::spawn`-like APIs or wake other tasks behave sanely, and the inject queue is closed only after the local queue is drained (a cancelled task's drop may still try to schedule).

---

## 7. Differences from the multi-thread scheduler

| | current-thread | multi-thread |
|---|---|---|
| Run queues | one `VecDeque` + inject | per-worker 256-slot ring + LIFO slot + global inject |
| Threads | the `block_on` caller(s); core handed over via `AtomicCell`+`Notify` | N worker threads, each owns a `Core` permanently |
| `block_on` future | polled **by the scheduler loop** (`woken` flag) | polled on the caller's own thread (`CachedParkThread`) |
| Cross-thread wake | `inject.push` + `driver.unpark()` | `inject.push` + `Idle`-controlled `unpark` of one worker |
| Default `global_queue_interval` | 31 | self-tuned 2..127 (EWMA) |
| `event_interval` | 61 | 61 |
| Coop budget scope | per task | one budget for a task + its LIFO chain |
| Test-clock pausing (`start_paused`, `pause()`) | supported (`enable_pause_time = true`) | not supported |
| `block_in_place` | **not allowed** (panics) | allowed |
| Work stealing / idle tracking | none | yes |
| `!Send` tasks | via `LocalRuntime` (`spawn_local`) or `LocalSet` | `LocalSet` only |

---

## 8. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| [Task core](../task/05-handles-and-schedule.md) | scheduler ↔ task | `OwnedTasks::{bind, assert_owner, remove, close_and_shutdown_all}`; `Notified`/`LocalNotified`; `Schedule` impl |
| [Context](./02-context-thread-local.md) | scheduler → | `set_scheduler(&cx)`; `with_scheduler` in `schedule` |
| Drivers | scheduler → | `Driver::{park, park_timeout, shutdown}`; `driver::Handle::unpark` |
| [Coop](../task/10-coop-budget.md) | scheduler → | `coop::budget` around each poll; `Defer::wake` after parking |
| [Inject queue](./07-inject-queue.md) | ↔ | `push`, `pop`, `close` |
| [Metrics](./10-stats-and-metrics.md) | → | `MetricsBatch` (poll counts, park counts, busy time), `WorkerMetrics::set_queue_depth` |
| User hooks | → | `before_park`, `after_unpark` (run inside `enter` so they see the runtime context), task hooks |

---

## 9. Invariants

1. At most one thread holds the `Core` (`AtomicCell::take` is the lock). `Drop for CoreGuard` always returns it and notifies.
2. A `Notified` is only polled by the thread holding the core (`assert_owner` → `LocalNotified`).
3. The driver is *removed from the core while parked* so reentrancy (hooks, wakers) can't reach it.
4. `woken` is the only coordination for the `block_on` future: lost wake-ups are impossible because `waker_ref` pre-sets it and every wake sets it before unparking.
5. `shutdown2` asserts `owned.is_empty()` — a leaked task would be a bug.

---

## 10. Tests

<!-- TESTS:s_current -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/loom_current_thread.rs`](../../../tokio/src/runtime/tests/loom_current_thread.rs) | 3 | 140 |
| [`tokio/tests/rt_basic.rs`](../../../tokio/tests/rt_basic.rs) | 16 | 416 |
| [`tokio/tests/rt_common.rs`](../../../tokio/tests/rt_common.rs) | 49 | 1,050 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/rt_basic.rs` (the current-thread suite), `rt_common.rs` (same tests run on all flavors), `rt_local.rs` (LocalRuntime), `time_pause.rs` (auto-advance only here), loom: `runtime/tests/loom_current_thread*.rs`.

**Read next:** [04 — Multi-thread shared state & spawn path](./04-multithread-state-and-spawn.md).
