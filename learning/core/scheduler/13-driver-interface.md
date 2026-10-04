# 13 — The Driver interface (how the scheduler talks to I/O, signals, processes and timers)

> **Role:** give the scheduler **one** object with three verbs — `park`, `park_timeout`, `shutdown` — and **one** shared
> handle with `unpark`, behind which a *stack* of event sources hides. The scheduler never knows whether epoll, a timer wheel,
> a signal self-pipe or a plain thread-park is underneath.
> **Boundary:** the driver *produces wake-ups* (`Waker::wake`) — it never touches the run queues. All scheduling decisions stay in the scheduler.

**Files:** `runtime/driver.rs` (383 lines; composition), `runtime/park.rs` (simple thread parker, `ParkThread`/`UnparkThread`/`CachedParkThread`),
`runtime/io/driver.rs` (mio reactor), `runtime/signal/mod.rs`, `runtime/process.rs`, `runtime/time/mod.rs`; consumers: `multi_thread/park.rs` ([09](./09-parker.md)), `current_thread/mod.rs` ([03](./03-current-thread.md)).

## 1. The two public types

```rust
pub(crate) struct Driver { inner: TimeDriver }       // owned by ONE thread at a time (&mut self methods)
pub(crate) struct Handle {                           // cloneable/shared inside scheduler::Handle
    pub(crate) io:     IoHandle,       // Enabled(io::Handle) | Disabled(UnparkThread)
    pub(crate) signal: SignalHandle,   // Option<signal::Handle> on unix+signal, else ()
    pub(crate) time:   TimeHandle,     // Option<time::Handle> (None if time disabled)
    pub(crate) clock:  Clock,          // source of Instant::now(); pausable with test-util
}
pub(crate) struct Cfg { enable_io, enable_time, enable_pause_time, start_paused, nevents, nevents_busy, timer_flavor }
```

| Method | Meaning |
|---|---|
| `Driver::new(cfg) -> io::Result<(Driver, Handle)>` | build the stack bottom-up (below) |
| `Driver::park(&mut self, &Handle)` | block until an event, a timer, or `Handle::unpark` |
| `Driver::park_timeout(&mut self, &Handle, Duration)` | same with an upper bound; `Duration::ZERO` ⇒ poll without blocking |
| `Driver::shutdown(&mut self, &Handle)` | tear the sources down (wake pending futures with errors) |
| `Handle::unpark(&self)` | interrupt a blocked `park` from **any** thread (`time.unpark()` if time enabled, then `io.unpark()`) |
| `Handle::io()/signal()/time()/clock()` | typed accessors; panic with the "…IO is disabled. Call `enable_io`…" / "timers are disabled…" messages |

`&mut self` is the point: only one thread may be inside `Driver::park` — enforced by `TryLock<Driver>` in the multi-thread Parker, and by owning the driver in `Core` for current-thread.
`&Handle` is `Sync`: resources (sockets, timers) register through it from anywhere.

## 2. The layered stack (decorator chain)

Built in `Driver::new`:

```text
                      TimeDriver                       (adds timer wheel; computes park timeout from next deadline)
                          |  wraps
                      IoStack = ProcessDriver          (reaps orphaned child processes after each park)
                          |  wraps
                      SignalDriver                     (self-pipe read after each park -> broadcast signals)
                          |  wraps
                      IoDriver (mio::Poll + Waker)     (epoll/kqueue/IOCP; dispatches readiness -> ScheduledIo.wake)
```

| Layer | Type (cfg) | `park` does | `shutdown` does |
|---|---|---|---|
| IO | `runtime::io::Driver` (`rt` + io) | `turn(handle, max_wait)`: `release_pending_registrations`, `poll.poll(events, max_wait)`, then for each event: `TOKEN_WAKEUP` ⇒ nothing (just unblocks), `TOKEN_SIGNAL` ⇒ `signal_ready = true`, else `ScheduledIo::set_readiness(Tick::Set, curr|ready)` + **`io.wake(ready)`**; io_uring completion dispatch (unstable, Linux); `metrics.incr_ready_count_by` | `registrations.shutdown(..)` then `io.shutdown()` for each *outside the lock* |
| Signal | `runtime::signal::Driver` (unix + `signal` feature, else the IO driver itself) | `io.park(..)` then `process()`: if `consume_signal_ready()`, drain the self-pipe and `broadcast` | delegates to IO |
| Process | `runtime::process::Driver` (`process` feature, else = signal driver) | `signal.park(..)` then `GlobalOrphanQueue::reap_orphans` | delegates |
| Time | `runtime::time::Driver` → `TimeDriver::{Enabled{driver}, EnabledAlt(IoStack), Disabled(IoStack)}` | `park_internal` (§3), then `handle.process(clock)` | mark `is_shutdown`, `process_at_time(u64::MAX)` (fire **everything**, "advance time to the end of time"), then `park.shutdown` |
| Fallback | `ParkThread` (when io disabled / not built) | condvar park | notify all |

`IoStack`/`IoHandle` are enums so the *same* driver code works when I/O is disabled: `IoStack::Disabled(ParkThread)` / `IoHandle::Disabled(UnparkThread)` (a thread parker, no OS poller).
Feature gating is done with `cfg_io_driver!`, `cfg_time!`, `cfg_signal_internal_and_unix!`, `cfg_process_driver!` macros that swap type aliases (e.g. `type TimeHandle = ()` when time is off), so no runtime cost for unused layers.

## 3. Time driver park algorithm (`time/mod.rs::park_internal`)

```text
lock = handle.inner.lock()
next_wake = lock.wheel.next_expiration_time()            // earliest pending deadline (tick)
lock.next_wake = next_wake (clamped to ≥ 1)               // so Sleep::reset can tell if it must unpark the driver
unlock
match next_wake:
  Some(when):
      duration = tick_to_duration(when - now)             // "effectively round up to 1ms" (ticks are ms)
      if duration > 0:  park_thread_timeout(min(limit, duration))   // test-util: may auto-advance paused clock
      else:             park.park_timeout(ZERO)                     // already due: poll only
  None:
      limit ⇒ park_thread_timeout(limit)  else park.park()
handle.process(clock)                                      // fire everything due: wheel.poll(now) loop, batch of wakers (WakeList), lock dropped while waking
```

Timer firing wakes `Waker`s ⇒ tasks are scheduled; with `start_paused`/`test-util`, `park_thread_timeout` polls the lower layers with zero timeout and **advances the clock by `duration`** unless the driver "did_wake" (so `tokio::time::pause()` tests run instantly).
`process_at_time` also protects against a non-monotonic clock ("Time went backwards" – VM on Windows host, issue #3619) by clamping `now` to `wheel.elapsed()`.

With the `Alternative` timer flavor (unstable, multi-thread), timers live in each worker's local wheel (`time_alt`, `LocalContext`) and the `TimeDriver::EnabledAlt(IoStack)` is *only* the I/O stack; `park_internal` in the worker computes the timeout from the local wheel (`maintain_local_timers_before_parking`). See [05](./05-worker-loop.md).

## 4. How events become task executions (the whole path)

```text
 OS event ──> mio::Poll::poll (inside Driver::park on some worker thread)
          ──> io::Driver::turn: ScheduledIo::set_readiness + wake(ready)
          ──> stored Waker::wake()                      [task/06-waker.md]
          ──> RawTask::wake_by_val -> Harness::wake_by_val -> state.transition_to_notified_by_val
          ──> <Arc<Handle> as Schedule>::schedule(task)  [task/05]
          ──> Handle::schedule_task -> schedule_local (core.park is None while in driver => delayed notify) | inject.push
          ──> (end of park_internal) should_notify_others -> notify_parked_local -> Idle::worker_to_notify -> Unparker::unpark
          ──> worker polls the task
```

The key subtlety: during `park_internal` the worker's `Core.park` is `None` and the Core is stored in the thread-local context, so `schedule_local` can push into **this worker's own LIFO slot / ring** with no cross-thread traffic; waking *other* workers is postponed to the end of park ("notifications often come in batches").

For the opposite direction — someone needs the driver thread to wake **now** (a timer was inserted earlier than the current deadline, or a remote spawn) — `driver::Handle::unpark()` writes the mio `Waker` (an eventfd/self-pipe) ⇒ `TOKEN_WAKEUP` event ⇒ `turn` returns.

## 5. Who calls what

| Caller | Method |
|---|---|
| `multi_thread::park::Inner::park_driver` | `driver.park(handle)` / `driver.park_timeout(handle, d)` with `TryLock<Driver>` held; `Unparker::unpark` → `driver.unpark()` when state `PARKED_DRIVER` |
| `multi_thread::park::Parker::shutdown` | `driver.shutdown(handle)` (if lock obtained) |
| `current_thread::Context::park_internal` | `driver.park_timeout(&handle.driver, dur)` or `driver.park(..)`, then `defer.wake()`; `Driver` lives in `Core.driver: Option<Driver>` (taken during park) |
| `current_thread::shutdown2` | `driver.shutdown(&handle.driver)` |
| `Handle::unpark` | current-thread `Handle::waker_ref` → `driver.unpark()` when a remote thread wakes the `block_on` future; MT `notify_*` goes through `Unparker` |
| resources: `TcpStream`, `Sleep`, `Signal` … | `driver::Handle::io()` / `time()` → register / insert timer entries |
| `Builder::build_*` | `driver::Cfg{…}` → `Driver::new(cfg)`; result split: `Driver` → Parker/Core, `Handle` → `scheduler::Handle.driver` |

## 6. Invariants

| # | Invariant |
|---|---|
| I1 | At most one thread executes `Driver::park*` at a time (`&mut self` + `TryLock`/ownership) |
| I2 | `Handle::unpark` is safe from any thread and **never lost**: the mio waker makes the *next* poll return immediately if not currently blocked (doc on `io::Handle::unpark`) |
| I3 | `Driver::shutdown` is called once, after tasks were shut down (so wakers fired by shutdown find closed queues) |
| I4 | A `Driver` made with `enable_io = false` still blocks correctly (ParkThread) — `enable_time` without `enable_io` works, I/O APIs panic with the explicit message |
| I5 | Timer processing happens **after** the poll returns (events first, then timers); wakers are batched and invoked with the timer lock dropped |

## 7. Tests

Driver code is exercised through integration suites: `tokio/tests/rt_common.rs` (park/unpark, time), `tokio/tests/io_*.rs`, `time_*.rs`, `signal_*.rs`, `process_*.rs`;
unit tests in `runtime/time/tests/` and `runtime/io/` ; loom: `runtime/tests/loom_current_thread.rs`.

<!-- TESTS:driver -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_common.rs`](../../../tokio/tests/rt_common.rs) | 49 | 1,050 |
| [`tokio/src/runtime/tests/loom_current_thread.rs`](../../../tokio/src/runtime/tests/loom_current_thread.rs) | 3 | 140 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Index:** [← core/README](../README.md)
