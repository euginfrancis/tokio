# Scheduler component 5 — The Worker Loop (`multi_thread/worker.rs`: `run`, `Context::run`, `run_task`, `Core::next_task`, `steal_work`, `park`)

> **One sentence:** each worker thread runs one loop — *tick → maybe service the drivers → take a task (LIFO slot, local ring, inject batch, or steal) → poll it (plus the LIFO chain, under one budget) → if there is nothing, search, then park inside the shared driver or on a condvar* — and every other component exists to make this loop fast, fair and lock-free on the hot path.

---

## 1. Where it lives

<!-- FILES:s_worker -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/scheduler/multi_thread/worker.rs`](../../../tokio/src/runtime/scheduler/multi_thread/worker.rs) | 939 | 387 | 54 |
<!-- /FILES -->

All of this is in `worker.rs` (~940 code lines; the biggest source file in the runtime). Sections of the file: data (doc 04) · `block_in_place` (doc 11) · **loop, task selection, parking, transitions (this doc)** · shutdown (doc 12) · scheduling & notification (doc 04).

---

## 2. A worker's life — state machine

```
                           launch: spawn_blocking(|| run(worker))
                                         │  worker.core.take() → Some(core)  (else: another thread already runs this worker ⇒ return)
                                         ▼
   ┌──────────────────────────────  RUNNING  ◀─────────────────────────────────────────────────────┐
   │ tick += 1; every 61 ticks: maintenance()                                                         │
   │ next_task(): LIFO slot → local ring → (inject batch)           ── Some(task) ──▶ run_task() ───┘
   │        │ None                                                  (then loop)
   │        ▼
   │  SEARCHING   (allowed only while 2·num_searching < num_workers)
   │   steal_work(): random victim → steal ⌈n/2⌉ ; finally inject.pop()   ── Some(task) ──▶ run_task()
   │        │ nothing
   │        ▼
   │  PARKING      transition_to_parked(): sleepers.push(me); unparked−1 (searching−1); last searcher ⇒ notify_if_work_pending()
   │        │
   │        ├─ driver.try_lock() ok ──▶ PARKED_DRIVER : sleeps in epoll_wait/kqueue, timeout = next timer deadline
   │        └─ else ──────────────────▶ PARKED_CONDVAR: sleeps on its own condvar
   │        │  wake: Unparker::unpark / I/O or timer event / timeout
   │        ▼
   └── transition_from_parked()  ─ has tasks (driver woke a task into my core)  ──▶ RUNNING
                                  ─ removed from sleepers by a notifier (counted as searching) ──▶ SEARCHING
                                  ─ still in sleepers (spurious) ──▶ park again
   core.is_shutdown (inject closed) ⇒ leave loop ⇒ pre_shutdown ⇒ shutdown_core   (doc 12)
```

---

## 3. Thread entry — `run(worker)`

```rust
fn run(worker: Arc<Worker>) {
    #[cfg(debug_assertions)] let _abort_on_panic = AbortOnPanic;      // debug builds abort the process if a worker thread panics (loom/test sanity)
    let core = match worker.core.take() { Some(c) => c, None => return };      // AtomicCell swap: whoever gets it IS this worker
    worker.handle.shared.worker_metrics[worker.index].set_thread_id(thread::current().id());
    let handle = scheduler::Handle::MultiThread(worker.handle.clone());
    context::enter_runtime(&handle, true /*allow_block_in_place*/, |_| {
        let cx = scheduler::Context::MultiThread(Context { worker, core: RefCell::new(None), defer: Defer::new() });
        context::set_scheduler(&cx, || {                 // thread-local Scoped pointer: schedule_task/defer can now find `cx`
            let cx = cx.expect_multi_thread();
            cx.run(core);                                // ← the loop
            cx.defer.wake();                             // after core loss (block_in_place) wake any still-deferred wakers
        });
    });
}
```
The `Option` return of `core.take()` matters for `block_in_place`: a *replacement* thread also executes `run(worker)`; the original, if it later returns from its blocking call and finds the core gone, simply returns and stops being a worker.

---

## 4. `Context::run(core)` — the loop, annotated

```rust
fn run(&self, mut core: Box<Core>) {
    self.reset_lifo_enabled(&mut core);                       // lifo_enabled = !config.disable_lifo_slot   (the core may come from a stolen thread with it disabled)
    core.stats.start_processing_scheduled_tasks();
    while !core.is_shutdown {
        self.assert_lifo_enabled_is_correct(&core);           // debug invariant
        if core.is_traced { core = self.worker.handle.trace_core(core); }     // task-dump support: pause here while others trace
        core.tick();                                          // tick = tick.wrapping_add(1)
        core = self.maintenance(core);                        // every `event_interval` (61) ticks: poll drivers, check shutdown/trace
        if let Some(task) = core.next_task(&self.worker) {                        // ① local work
            core = match self.run_task(task, core) { Continue(c) => c, Break(()) => return };
            continue;
        }
        core.stats.end_processing_scheduled_tasks();          // EWMA sample point (see 10)
        if let Some(task) = core.steal_work(&self.worker) {                       // ② steal / inject
            core.stats.start_processing_scheduled_tasks();
            core = match self.run_task(task, core) { Continue(c) => c, Break(()) => return };
        } else {
            core = if !self.defer.is_empty() { self.park_yield(core) }            // ③ yielded tasks pending → poll drivers w/o sleeping
                   else                       { self.park(core) };                // ④ truly idle → sleep
            core.stats.start_processing_scheduled_tasks();
        }
    }
    (alt timer: shutdown_local_timers …)
    core.pre_shutdown(&self.worker);                          // cancel all tasks (doc 12)
    self.worker.handle.shutdown_core(core);                   // hand the core to the shutdown collector
}
```
`ControlFlow::Break(())` from `run_task` means *the core was taken away while polling the task* (`block_in_place`): this thread is no longer a worker and returns immediately.

---

## 5. Choosing the next task — `Core::next_task`

```rust
fn next_task(&mut self, worker: &Worker) -> Option<Notified> {
    if self.tick % self.global_queue_interval == 0 {                // fairness tick: remote work gets priority
        self.tune_global_queue_interval(worker);                    // re-read the EWMA; only change if |new − old| > 2 (anti-jitter)
        worker.handle.next_remote_task().or_else(|| self.next_local_task())
    } else {
        let maybe_task = self.next_local_task();                    // LIFO slot first, then ring.pop()
        if maybe_task.is_some() { return maybe_task; }
        if worker.inject().is_empty() { return None; }             // lock-free check of the atomic len
        // local work exhausted: take a FAIR SHARE of the inject queue
        let cap = min(self.run_queue.remaining_slots(), self.run_queue.max_capacity() / 2);      // never more than half the ring (so overflow can't ping-pong them back)
        let n   = min(worker.inject().len() / worker.handle.shared.remotes.len() + 1, cap);      // len/#workers + 1
        let n   = max(1, n);
        worker.inject().pop_n(n, |mut tasks| { let ret = tasks.next(); self.run_queue.push_back(tasks); ret })   // first task returned, rest go to the ring
    }
}
fn next_local_task(&mut self) -> Option<Notified> { self.lifo_slot.take().or_else(|| self.run_queue.pop()) }
```
| Rule | Reason |
|---|---|
| LIFO slot **before** the ring | the task just woken by the previous one is cache-hot (message-passing latency) |
| Check inject every `global_queue_interval` ticks (self-tuned 2..127, default start ≈61) | tasks spawned from *outside* must not starve behind a busy local ring |
| Pull `len/N + 1` tasks, ≤ ½ ring | spreads a burst of injected tasks across all workers instead of one grabbing everything |
| Ring `pop` is a CAS, `pop_n` takes the inject **mutex once** for the whole batch | amortised lock cost |

---

## 6. Stealing — `Core::steal_work`

```rust
fn steal_work(&mut self, worker: &Worker) -> Option<Notified> {
    if !self.transition_to_searching(worker) { return None; }       // Idle::transition_worker_to_searching: refuse if 2·num_searching ≥ num_workers
    let num = worker.handle.shared.remotes.len();
    let start = self.rand.fastrand_n(num as u32) as usize;           // random starting victim (xorshift, Lemire reduction)
    for i in 0..num {
        let i = (start + i) % num;
        if i == worker.index { continue; }
        if let Some(task) = worker.handle.shared.remotes[i].steal.steal_into(&mut self.run_queue, &mut self.stats) { return Some(task); }   // ⌈n/2⌉ tasks, one returned, rest queued locally
    }
    worker.handle.next_remote_task()                                 // last resort: ONE task from the inject queue
}
```
`is_searching` stays `true` until the worker actually polls a task (`transition_from_searching` in `run_task`) or parks. A searching worker that finds work and was the **last** searcher must wake another sleeper (`Idle::transition_worker_from_searching` returns `true` ⇒ `notify_parked_local`), so that work found later still gets a searcher — the "chain reaction" that avoids both a thundering herd and lost work.

---

## 7. Running a task — `Context::run_task` (+ the LIFO chain)

```rust
fn run_task(&self, task: Notified, mut core: Box<Core>) -> ControlFlow<(), Box<Core>> {
    let task = self.worker.handle.shared.owned.assert_owner(task);           // Notified → LocalNotified   (task core)
    let notified_parked_worker = core.transition_from_searching(&self.worker);   // leave SEARCHING; maybe wake a sleeper
    if cfg!(tokio_unstable) && core.enable_eager_driver_handoff && core.had_driver == HadDriver::Yes && !notified_parked_worker {
        core.had_driver = HadDriver::No;  self.worker.handle.notify_parked_local();    // I just came out of the driver: let another worker take the driver over while I poll
    }
    (schedule-latency accounting: task.get_scheduled_at().prepare(..) → core.stats.start_poll(ctx))
    *self.core.borrow_mut() = Some(core);                                     // put the core into the CONTEXT so wakes during the poll can use schedule_local()
    coop::budget(|| {                                                         // ONE 128-unit budget for the task AND its LIFO chain
        [hooks: poll_start]  task.run();  [hooks: poll_stop]                  // → RawTask::poll → Harness::poll → Future::poll
        let mut lifo_polls = 0;
        loop {
            let mut core = match self.core.borrow_mut().take() { Some(c) => c, None => return ControlFlow::Break(()) };   // core stolen by block_in_place
            let task = match core.lifo_slot.take() {
                Some(t) => t,
                None => { self.reset_lifo_enabled(&mut core); core.stats.end_poll(); return Continue(core); }
            };
            if !coop::has_budget_remaining() {                                // budget used up by the previous polls
                core.stats.end_poll();
                core.run_queue.push_back_or_overflow(task, &*self.worker.handle, &mut core.stats);   // demote to the ring (stealable, FIFO)
                return Continue(core);
            }
            lifo_polls += 1;  inc_lifo_schedules();
            if lifo_polls >= MAX_LIFO_POLLS_PER_TICK /* 3 */ { core.lifo_enabled = false; inc_lifo_capped(); }   // stop prioritising the slot: later schedule_local → ring
            let task = self.worker.handle.shared.owned.assert_owner(task);
            (record schedule latency for this LIFO task)
            *self.core.borrow_mut() = Some(core);
            [hooks]  task.run();  [hooks]
        }
    })
}
```
**Why the core is moved into the context during a poll:** `Waker::wake` called from *inside* the task (or from anything running on this thread, such as the task's own destructor) reaches `schedule_task` → `with_current` → `cx.core.borrow_mut()` → `schedule_local`. Without the core there, every in-task wake would go through the inject queue's mutex.

**Why the LIFO cap (3):** two tasks that wake each other (ping-pong) would otherwise monopolise the worker; once a chain has made 3 LIFO polls `lifo_enabled = false`, so tasks scheduled *after that* go to the *back of the ring* (visible to stealers); it is re-armed by `reset_lifo_enabled` when the chain ends (the LIFO slot is found empty) and at the start of `Context::run`.

---

## 8. Periodic maintenance — `Context::maintenance`

```rust
fn maintenance(&self, mut core: Box<Core>) -> Box<Core> {
    if core.tick % config.event_interval == 0 {                // 61
        inc_num_maintenance();
        core.stats.end_processing_scheduled_tasks();
        core = self.park_yield(core);                          // poll I/O + timers WITHOUT sleeping (so a saturated worker still delivers events)
        core.maintenance(&self.worker);                        // Core::maintenance: stats.submit(); is_shutdown = inject.is_closed(); is_traced = trace_requested()
        core.stats.start_processing_scheduled_tasks();
    }
    core
}
```

---

## 9. Parking — `park`, `park_yield`, `park_internal`

```rust
fn park(&self, mut core: Box<Core>) -> Box<Core> {
    if let Some(f) = &config.before_park { f(); }
    if core.transition_to_parked(&self.worker) {                       // false if the core still has tasks (LIFO/ring) or is traced
        while !core.is_shutdown && !core.is_traced {
            core.stats.about_to_park();  core.stats.submit(&worker_metrics[idx]);
            core = self.park_internal(core, None);                     // blocks
            core.stats.unparked();
            core.maintenance(&self.worker);
            if core.transition_from_parked(&self.worker) { break; }    // real wake-up → leave; spurious → loop
        }
    }
    if let Some(f) = &config.after_unpark { f(); }
    core
}
fn park_yield(&self, core: Box<Core>) -> Box<Core> { self.park_internal(core, Some(Duration::from_millis(0))) }

fn park_internal(&self, mut core: Box<Core>, duration: Option<Duration>) -> Box<Core> {
    let mut park = core.park.take().expect("park missing");            // take the Parker OUT of the core
    *self.core.borrow_mut() = Some(core);                              // …and put the core INTO the context: the drivers will wake tasks
    (alt timer: maintain_local_timers_before_parking)                  //   from inside park(); those wakes call schedule_local on THIS core
    let had_driver = match duration { Some(t) => park.park_timeout(&driver_handle, t), None => park.park(&driver_handle) };
    self.defer.wake();                                                 // fire yield_now / budget-exhausted wakers (they land in this core's ring)
    core = self.core.borrow_mut().take().expect("core missing");
    core.park = Some(park);  core.had_driver = had_driver;
    if core.should_notify_others() { self.worker.handle.notify_parked_local(); }     // !is_searching && (lifo + ring) > 1 ⇒ there is work others could steal
    core
}
```
- `Parker::park` decides *where* the thread sleeps (driver vs condvar) — see [09](./09-parker.md).
- `transition_to_parked` → `Idle::transition_worker_to_parked`; if it returns "last searcher" ⇒ `notify_if_work_pending()` (a final re-check so work submitted while the last searcher was going to sleep isn't stranded).
- `transition_from_parked` (above in §2) resolves *who woke me*: `unpark_worker_by_id` if I still appear in `sleepers` (woken by an event, not by a notifier).
- `Context::defer(&Waker)` (used by coop/yield): if `core` is `None` (we are inside `block_in_place`) → `wake_by_ref()` immediately; else queue in `self.defer`.

---

## 10. The transitions in one table

| Core method | Calls | Meaning |
|---|---|---|
| `transition_to_searching` | `Idle::transition_worker_to_searching` | become a searcher if < ½ of workers are searching (`SeqCst`) |
| `transition_from_searching` | `Idle::transition_worker_from_searching` → maybe `notify_parked_local` | leave search; wake another if I was the last searcher |
| `has_tasks` | – | `lifo_slot.is_some() || run_queue.has_tasks()` |
| `should_notify_others` | – | `!is_searching && lifo + ring.len() > 1` |
| `transition_to_parked` | `Idle::transition_worker_to_parked` (+ `notify_if_work_pending`) | register as sleeper |
| `transition_from_parked` | `Idle::{unpark_worker_by_id, is_parked}` | decide RUNNING / SEARCHING / stay parked |

---

## 11. Communication — who calls whom, with what data

| From → To | Call | Data (DTO) | Ownership |
|---|---|---|---|
| loop → [task core](../task/05-handles-and-schedule.md) | `assert_owner(Notified)`; `LocalNotified::run()` | `Notified`→`LocalNotified` | moved; ref consumed by `poll` |
| loop → [coop](../task/10-coop-budget.md) | `coop::budget`, `has_budget_remaining`, `Defer::wake` | `Budget` (TLS), `Waker`s | – |
| loop → [local queue](./06-local-queue.md) | `pop`, `push_back`, `push_back_or_overflow`, `steal_into`, `remaining_slots` | `Notified` | moved into/out of ring slots |
| loop → [inject queue](./07-inject-queue.md) | `is_empty`, `pop`, `pop_n(n, f)`, `is_closed` | `Pop` iterator of `Notified` | batch moved to ring |
| loop → [idle](./08-idle-coordination.md) | `transition_worker_{to,from}_searching`, `…_to_parked`, `unpark_worker_by_id`, `is_parked`, `worker_to_notify` | worker index (`usize`), `bool` | – |
| loop → [parker](./09-parker.md) | `park`, `park_timeout`, `shutdown`; `Unparker::unpark` | `Duration`; `HadDriver` | `Parker` moved out of/into `Core` |
| loop → [stats](./10-stats-and-metrics.md) | `start/end_processing_scheduled_tasks`, `start_poll`, `end_poll`, `about_to_park`, `unparked`, `submit`, `incr_*` | counters (batched in `Core`) | `Core`-local |
| loop ↔ [context](./02-context-thread-local.md) | `set_scheduler`; `Context.core` RefCell | `&Context` pointer | scoped |
| loop → drivers (via parker) | `driver.park[_timeout]` | `Duration` | – |
| loop → user hooks | `before_park`, `after_unpark`, `poll_start/stop` | `&TaskMeta` | – |
| loop → [shutdown](./12-shutdown.md) | `pre_shutdown`, `shutdown_core(core)` | `Box<Core>` | moved |

---

## 12. Worked trace (illustrative): a task spawned from `main` on a 3-worker runtime

```
t0  main thread: tokio::spawn(fut)           → bind (shard lock) → schedule_task: not a worker → inject.push(task); idle.worker_to_notify() = Some(2) → W2.unpark()
t1  W2 (PARKED_DRIVER in epoll_wait): unpark ⇒ driver.unpark() writes the mio Waker ⇒ epoll_wait returns ⇒ park_driver returns
t2  W2: transition_from_parked: still in sleepers? no (worker_to_notify popped it and counted it "searching") ⇒ is_searching = true ⇒ RUNNING
t3  W2: next_task: LIFO empty, ring empty, inject.len()=1 ⇒ n = 1/3+1 = 1 ⇒ pop_n(1) ⇒ task
t4  W2: run_task: transition_from_searching (last searcher ⇒ notify_parked_local ⇒ wakes W1 as a new searcher, finds nothing, re-parks);
        assert_owner; coop::budget { Harness::poll → future runs until its first .await (say a socket read) → registers waker, Pending }
t5  W2: lifo_slot empty ⇒ Continue ⇒ next_task: none ⇒ steal_work: others empty ⇒ park (driver now free: W2 or W1 takes the try_lock)
t6  data arrives: the worker holding the driver gets epoll event ⇒ ScheduledIo::wake ⇒ Waker::wake ⇒ schedule_task: we ARE on a worker (inside park_internal, core is in context) ⇒ schedule_local ⇒ LIFO slot
t7  that worker returns from park_internal ⇒ transition_from_parked: has_tasks ⇒ RUNNING ⇒ polls the task from its LIFO slot
```

---

## 13. Invariants

1. A task is polled only via `run_task`, after `assert_owner`, under one `coop::budget`.
2. The `Core` is in `Context.core` **exactly when** a task (or the driver) is running on the thread; between those it is owned by the loop's local variable.
3. `is_searching` ⇒ counted in `Idle.num_searching`; the counts are only changed through the `transition_*` methods.
4. At most one thread sleeps in the driver (`TryLock`); all others are on condvars.
5. The loop exits only on `is_shutdown` or `Break` (core lost). It never returns while tasks remain in its queues unless shutting down.
6. `lifo_enabled` is reset (`reset_lifo_enabled`) whenever a LIFO chain ends, so the cap affects one burst, not forever.

---

## 14. Tests

<!-- TESTS:s_worker -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| [`tokio/tests/rt_busy_tick.rs`](../../../tokio/tests/rt_busy_tick.rs) | 4 | 77 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

Behaviour: `tokio/tests/rt_threaded.rs` (stealing, parking, block_in_place, shutdown), `rt_common.rs`; loom models `runtime/tests/loom_multi_thread.rs` + `loom_multi_thread/{queue,shutdown,yield_now}.rs` and `queue.rs`/`inject.rs` unit tests.

**Read next:** [06 — Local run queue](./06-local-queue.md).
