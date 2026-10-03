# Block 8 — I/O Driver (reactor) + Signal & Process Drivers

> **Role:** the bridge to the operating system's event notification (epoll on Linux, kqueue on macOS/BSD, IOCP on Windows — via the `mio` crate). It registers sockets/pipes, **blocks the thread** waiting for events when the runtime is idle, and turns "fd 42 is readable" into `waker.wake()`. On Unix, the signal driver and process driver are thin layers on top of it.
> In the [component diagram](./README.md): the "I/O DRIVER (reactor) — epoll/kqueue/IOCP + signals/processes" box at the bottom. It's the **only place a runtime thread actually sleeps in the kernel**.

---

## 1. At a glance

<!-- STATS:io_driver -->
| Metric | Value |
|---|---|
| Source files | 10 |
| Code lines | 1,241 (2.5% of `tokio/src`) |
| Doc + comment lines | 451 (0.36 per code line) |
| Functions | 95 — public API 0, trait impls 14, internal 79, inline tests 2 |
| `async fn` / `unsafe fn` | 4 / 7 |
| `unsafe` occurrences | 40 |
| Integration tests (`tokio/tests`) | none dedicated — exercised through other blocks' tests |
<!-- /STATS -->

Small in code, central in importance: every network operation and every idle runtime thread passes through these ~1,200 lines.

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | The `mio::Poll` instance and its event buffer; the registry of all I/O resources (`RegistrationSet` of `ScheduledIo`); per-resource readiness state + waiting wakers (`ScheduledIo`); the cross-thread wake-up (`mio::Waker`, token 0); dispatching events; safe deregistration; io_uring completion dispatch (unstable). **Signal driver:** draining the self-pipe and broadcasting signals. **Process driver:** reaping orphaned children after each park. |
| **Does not own** | Socket types and read/write logic ([Net & I/O block](./03-net-io.md) — `PollEvented`, `TcpStream`, …); the signal *API* and handler installation, process spawning ([fs/process/signal block](./05-fs-process-signal.md)); timers ([Timer driver](./07-timer-driver.md) wraps this block). |
| **Input** | `add_source(source, interest)` / `deregister_source` from `Registration`; `park` / `park_timeout(d)` from the time driver; `unpark()` from anyone. |
| **Output** | `ScheduledIo::set_readiness` + `wake()` → task wakers; signal broadcast to `watch` channels; orphan reaping. |
| **Boundary types** | `Registration` (held by every I/O resource: `{ handle: scheduler::Handle, shared: Arc<ScheduledIo> }`), `ReadyEvent`, `Interest`/`Ready`, `IoHandle` (enabled/disabled), `IoStack` (driver stack). |

---

## 3. Files

<!-- FILES:io_driver -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/runtime/io/scheduled_io.rs`](../../tokio/src/runtime/io/scheduled_io.rs) | 368 | 159 | 29.7% |
| [`tokio/src/runtime/io/driver.rs`](../../tokio/src/runtime/io/driver.rs) | 274 | 52 | 22.1% |
| [`tokio/src/runtime/io/driver/uring.rs`](../../tokio/src/runtime/io/driver/uring.rs) | 207 | 73 | 16.7% |
| [`tokio/src/runtime/io/registration.rs`](../../tokio/src/runtime/io/registration.rs) | 146 | 89 | 11.8% |
| [`tokio/src/runtime/io/registration_set.rs`](../../tokio/src/runtime/io/registration_set.rs) | 90 | 26 | 7.3% |
| [`tokio/src/runtime/signal/mod.rs`](../../tokio/src/runtime/signal/mod.rs) | 74 | 43 | 6.0% |
| [`tokio/src/runtime/process.rs`](../../tokio/src/runtime/process.rs) | 30 | 4 | 2.4% |
| [`tokio/src/runtime/io/driver/signal.rs`](../../tokio/src/runtime/io/driver/signal.rs) | 19 | 0 | 1.5% |
| [`tokio/src/runtime/io/mod.rs`](../../tokio/src/runtime/io/mod.rs) | 17 | 0 | 1.4% |
| [`tokio/src/runtime/io/metrics.rs`](../../tokio/src/runtime/io/metrics.rs) | 16 | 5 | 1.3% |
| **Total (10 files)** | **1,241** | **451** | 100% |
<!-- /FILES -->

```
runtime/io/
├── driver.rs            Driver { poll, events } — turn(); Handle { registry, registrations, waker, … } — add_source, deregister_source, unpark
├── scheduled_io.rs      ScheduledIo — readiness word + waiters; poll_readiness, set_readiness, wake, Readiness future
├── registration.rs      Registration — what sockets hold; poll_ready, poll_io, try_io, async_io, readiness()
├── registration_set.rs  RegistrationSet — owns Arc<ScheduledIo>s; deferred release
├── driver/signal.rs     consume_signal_ready (TOKEN_SIGNAL)
├── driver/uring.rs      io_uring context (tokio_unstable + io-uring, Linux)
└── metrics.rs           fd count, ready count
runtime/signal/mod.rs    signal::Driver { io, receiver: UnixStream (self-pipe) } — process()
runtime/process.rs       process::Driver { park: signal::Driver } — reap_orphans after every park
```

**Driver stack** (built in `runtime/driver.rs`, parked top-down):
```
time::Driver ─▶ process::Driver ─▶ signal::Driver ─▶ io::Driver ─▶ mio::Poll::poll  (kernel)
```
If I/O is disabled (`enable_io` not called) the bottom is a plain `ParkThread` (mutex + condvar) instead.

---

## 4. Data structures

```rust
pub(crate) struct Driver {                 // io/driver.rs — owned by whichever thread is parked in it
    signal_ready: bool,                    // TOKEN_SIGNAL was seen this turn
    events: mio::Events,                   // reusable event buffer (capacity = Builder::max_io_events_per_tick, default 1024)
    events_busy: Option<mio::Events>,      // smaller batch for zero-timeout polls while busy
    poll: mio::Poll,                       // the epoll/kqueue/IOCP instance
}
pub(crate) struct Handle {                 // shared by all threads (in driver::Handle.io)
    registry: mio::Registry,               // register/deregister fds (thread-safe)
    registrations: RegistrationSet,        // num_pending_release: AtomicUsize
    synced: Mutex<registration_set::Synced>,
    waker: mio::Waker,                     // TOKEN_WAKEUP — unpark() writes to it
    metrics: IoDriverMetrics,
    uring_context, uring_probe,            // tokio_unstable + io-uring
}
pub(super) struct Synced {                 // registration_set.rs
    is_shutdown: bool,
    registrations: LinkedList<Arc<ScheduledIo>>,   // every live registration (keeps them alive)
    pending_release: Vec<Arc<ScheduledIo>>,        // deregistered, freed at the next turn
}

pub(crate) struct ScheduledIo {            // scheduled_io.rs — ONE per socket/fd, 128-byte cache-line aligned
    linked_list_pointers: UnsafeCell<Pointers<Self>>,
    readiness: AtomicUsize,                // READINESS (16 bits) | TICK (15 bits) | SHUTDOWN (1 bit)
    waiters: Mutex<Waiters>,
}
struct Waiters {
    list: LinkedList<Waiter>,              // readable()/writable()/ready() futures (intrusive)
    reader: Option<Waker>,                 // poll_read_ready slot (AsyncRead path)
    writer: Option<Waker>,                 // poll_write_ready slot (AsyncWrite path)
}
pub(crate) struct ReadyEvent { tick: u16, ready: Ready, is_shutdown: bool }   // snapshot handed to callers
pub(super) enum Tick { Set, Clear(u16) }   // ABA guard for clearing readiness

pub(crate) struct Registration {           // registration.rs — embedded in PollEvented (every socket)
    handle: scheduler::Handle,
    shared: Arc<ScheduledIo>,
}

pub(crate) struct signal::Driver { io: io::Driver, receiver: UnixStream, inner: Arc<()> }
pub(crate) struct process::Driver { park: signal::Driver, signal_handle: SignalHandle }
```
**mio tokens:** `0` = wake-up, `1` = signal pipe, anything else = **the address of a `ScheduledIo`** (exposed via `EXPOSE_IO`). Dispatching an event is a pointer cast, no lookup table.

---

## 5. How it interacts with the other blocks

```
 [Net/IO] TcpStream::connect ─▶ PollEvented::new ─▶ Registration::new ─▶ Handle::add_source ─▶ registry.register(fd, token=&ScheduledIo)
 [Net/IO] poll_read ─▶ Registration::poll_read_ready ─▶ ScheduledIo::poll_readiness ─▶ ready? Ready(ReadyEvent) : store waker → Pending
 [Net/IO] read() == WouldBlock ─▶ Registration::clear_readiness(ev) ─▶ set_readiness(Tick::Clear(ev.tick), r - ev.ready)

 [Timer drv] park_timeout(d) ─▶ process::Driver ─▶ signal::Driver ─▶ io::Driver::turn(d)
      turn: release_pending_registrations; poll.poll(events, d)    ← THE THREAD SLEEPS HERE
            for each event:  token 0 → nothing (someone unparked us)
                             token 1 → signal_ready = true
                             else    → io = &*token; io.set_readiness(Tick::Set, |r| r | ready); io.wake(ready)
      signal::Driver::process: drain self-pipe → globals().broadcast() → [Signal API] watch channels
      process::Driver: GlobalOrphanQueue::reap_orphans
 io.wake ─▶ WakeList ─▶ [Tasks] waker.wake ─▶ [Scheduler]

 anyone ─▶ Handle::unpark ─▶ mio::Waker::wake (token 0) ─▶ epoll_wait returns
 [Net/IO] drop(TcpStream) ─▶ deregister_source ─▶ registry.deregister; move Arc<ScheduledIo> to pending_release (unpark after 16)
```

| Other block | Direction | Through |
|---|---|---|
| Net & I/O | ← | `Registration` (`new_with_interest_and_handle`, `poll_ready`, `poll_io`, `try_io`, `async_io`, `readiness`, `clear_readiness`, `deregister`) |
| Timer driver | ← park; ← unpark | `IoStack::park_timeout`; `IoHandle::unpark` when an earlier timer appears |
| Scheduler | ← unpark | `Unparker::unpark` → `driver.unpark()` when waking the worker parked in the driver |
| Tasks | → | `Waker::wake` |
| Signal API / Process API | → | `globals().broadcast()`; orphan reaping; pidfd registrations (Linux) are normal I/O registrations |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `Driver::new(nevents, nevents_busy)` | `driver.rs` | Create `mio::Poll`, `mio::Waker` (token 0), registry clone |
| `Driver::park / park_timeout` | `driver.rs` | `turn(None)` / `turn(Some(d))` |
| **`Driver::turn(handle, max_wait)`** | `driver.rs` | Release deferred registrations, `poll`, dispatch every event |
| `Driver::shutdown` | `driver.rs` | Mark every `ScheduledIo` shut down and wake all waiters |
| `Handle::unpark` | `driver.rs` | `mio::Waker::wake()` |
| `Handle::add_source / deregister_source` | `driver.rs` | Register an fd (token = `ScheduledIo` pointer) / deregister + deferred free |
| `RegistrationSet::allocate / deregister / release / shutdown` | `registration_set.rs` | Own `Arc<ScheduledIo>`s; free only between turns |
| `ScheduledIo::set_readiness(tick_op, f)` | `scheduled_io.rs` | CAS update of readiness; ignores stale clears (tick mismatch) |
| `ScheduledIo::wake(ready)` | `scheduled_io.rs` | Collect matching wakers (≤ 32 at a time) and wake outside the lock |
| `ScheduledIo::poll_readiness(cx, dir)` | `scheduled_io.rs` | Check readiness → or store waker, re-check, `Pending` |
| `ScheduledIo::readiness(interest)` → `Readiness` future | `scheduled_io.rs` | `async` readiness wait (intrusive waiter in `list`) |
| `ScheduledIo::clear_readiness / shutdown / clear_wakers` | `scheduled_io.rs` | Consume readiness, final shutdown, drop on deregister |
| `Registration::poll_read_ready / poll_write_ready / poll_io / try_io / async_io / readiness` | `registration.rs` | The API sockets use |
| `signal::Driver::park → process` | `runtime/signal/mod.rs` | After an I/O turn, drain the self-pipe and `broadcast()` |
| `process::Driver::park` | `runtime/process.rs` | After a turn, `reap_orphans` |

---

## 7. Flows

**Readiness life cycle of one socket** (edge-triggered):
1. Registered with interest READ|WRITE; readiness = 0.
2. Task reads → not ready → waker in `reader` slot → `Pending`.
3. Data arrives → kernel queues an event → `turn` sets READABLE, **tick+1**, wakes the reader.
4. Task polls → `poll_readiness` returns `ReadyEvent{tick, READABLE}` → `read()`:
   - got `n < buf.len()` bytes → socket drained → `clear_readiness(ev)` (epoll/kqueue only optimisation);
   - `WouldBlock` → `clear_readiness(ev)` and loop to wait again.
5. If another event raced in after step 4's snapshot, the tick differs and the clear is **ignored** — no lost wake-up.

**Deregistration safety:** a token is a raw pointer, so a `ScheduledIo` must not be freed while `turn` might still dereference it. `deregister_source` moves the `Arc` into `pending_release`; `turn` frees them at the start of the next poll (and the driver is unparked once 16 are pending so memory doesn't pile up).

**Signals (Unix):** `signal(kind)` installs (once per signal) an OS handler via `signal-hook-registry` → handler sets the event's `pending` flag and writes a byte to a non-blocking `UnixStream` pair → the receiving end is registered with mio under `TOKEN_SIGNAL` → `turn` sets `signal_ready` → `signal::Driver::process` drains the pipe → `globals().broadcast()` sends on each pending signal's `watch` channel → `Signal::recv().await` returns.

**Processes (Unix):** on Linux, `Child` uses a **pidfd** registered with this driver (exit = readable); elsewhere a `SIGCHLD` signal stream triggers `try_wait`. Children dropped without being awaited go to the global orphan queue, reaped by the process driver after each park.

---

## 8. Invariants & gotchas

- **Only one thread at a time runs `turn`** (the worker holding the driver `TryLock`); everyone else interacts via `Handle` (thread-safe).
- **`ScheduledIo` memory outlives its registration until the next turn** (deferred release) — the token-is-a-pointer trick depends on it.
- **Readiness clears are tick-checked**; never clear readiness you didn't observe.
- **Edge-triggered:** a socket only produces a new event after it goes from not-ready to ready; that's why code must read until `WouldBlock` (or a short read) before waiting again.
- **Waking is outside the lock** (`WakeList`, batches of 32).
- After shutdown, every pending and future readiness wait resolves immediately with the shutdown bit → I/O operations return errors.
- The 128-byte alignment of `ScheduledIo` prevents false sharing between sockets used by different threads.

---

## 9. Tests & where to start

<!-- TESTS:io_driver -->
_No integration test files are dedicated to this block._
<!-- /TESTS -->

The driver is exercised by `tokio/tests/io_*`, `tcp_*`, `udp*`, `uds_*`, `signal_*`, `process_*` and `rt_*` (see those blocks), plus inline tests in `driver.rs` and `scheduled_io.rs` (e.g. `stale_event_does_not_clear_readiness_after_u8_wraparound`).

**Read in this order:** `driver.rs` (`turn`, `add_source`) → `scheduled_io.rs` (`set_readiness`, `poll_readiness`, `wake`) → `registration.rs` → `io/poll_evented.rs` (in the Net & I/O block) → `runtime/signal/mod.rs`.
