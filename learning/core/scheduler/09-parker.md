# 09 — Parker (blocking a worker thread, with or without the driver)

> **Role:** put a worker thread to sleep until (a) a notifier calls `unpark`, (b) the
> timeout expires, or (c) — if this worker holds the **resource driver** — an I/O /
> timer / signal event arrives. It is the bridge between the scheduler and the
> [driver stack](./13-driver-interface.md).
> **Boundary:** it knows nothing about tasks or queues; it only has a 4-state
> atomic, a mutex+condvar, and a shared `TryLock<Driver>`.

**File:** `tokio/src/runtime/scheduler/multi_thread/park.rs` (316 lines).
The *current-thread* scheduler has its own, simpler `runtime/park.rs`
(`Parker`/`Unparker`/`CachedParkThread` – see [03](./03-current-thread.md) and
[13](./13-driver-interface.md)).

## 1. Data structures

```rust
pub(crate) struct Parker   { inner: Arc<Inner> }       // owned by the worker's Core (Option<Parker>)
pub(crate) struct Unparker { inner: Arc<Inner> }       // stored in Remote.unpark; shareable

struct Inner {
    state:   AtomicUsize,          // EMPTY | PARKED_CONDVAR | PARKED_DRIVER | NOTIFIED
    mutex:   Mutex<()>,            // guards the condvar hand-shake
    condvar: Condvar,              // used when this worker is NOT the driver owner
    shared:  Arc<Shared>,          // shared by ALL workers' parkers
}
struct Shared { driver: TryLock<Driver> }               // exactly one thread may own the driver at a time

pub(crate) enum HadDriver { Yes, No }                   // returned by park*: did this thread drive the driver?
```

* **One `Inner` per worker, one `Shared` per runtime.** `Parker::clone()` creates a *new*
  `Inner` (fresh state/mutex/condvar) but `Arc`-shares the `Shared` — that is how
  `worker::create` builds N parkers from one (`let park = park.clone()` per worker).
* `TryLock<T>` (`util/try_lock.rs`): an `AtomicBool` + `UnsafeCell<T>` whose
  `try_lock` is one `compare_exchange(false, true, SeqCst, SeqCst)`; the guard
  is `!Send` (a `PhantomData<Rc<()>>`) and releases on drop. Never blocks.

### State machine of `Inner.state`

```text
              park (driver free)                      unpark
   EMPTY ------------------------> PARKED_DRIVER  ------------------> (driver.unpark(); state = NOTIFIED)
     |  \                                |
     |   \ park (driver busy)            | driver returns -> swap(EMPTY)
     |    +--------------> PARKED_CONDVAR ---- unpark: swap(NOTIFIED) then lock/notify_one
     |                         |
     |  unpark when nobody parked: swap(NOTIFIED)        (a "token" is stored)
     v
  NOTIFIED  --- next park(): CAS(NOTIFIED -> EMPTY), return immediately (consume token)
```

Values: `EMPTY=0, PARKED_CONDVAR=1, PARKED_DRIVER=2, NOTIFIED=3`.

## 2. Operations

### `Parker::park(&mut self, handle) -> HadDriver`  (indefinite)

1. **Consume a pending token:** `CAS(NOTIFIED→EMPTY)`; success ⇒ return `HadDriver::No` without sleeping.
2. `shared.driver.try_lock()`:
   * `Some(driver)` → `park_driver(driver, handle, None)`: CAS `EMPTY→PARKED_DRIVER`
     (if it finds `NOTIFIED`, `swap(EMPTY)` and return `No`), then `driver.park(handle)` —
     blocks in the OS poller (epoll/kqueue/IOCP wait) with the **timer wheel's next
     deadline as timeout**. On return `swap(EMPTY)` must be `NOTIFIED` or `PARKED_DRIVER`; returns `Yes`.
   * `None` → `park_condvar(None)` and return `No`.

### `Parker::park_timeout(handle, duration)` — used for *yield*

Used by `Context::park_yield` with `Duration::ZERO` (see
[05](./05-worker-loop.md) `maintenance` every `event_interval` ticks, and when `defer` is non-empty):

* driver free → `park_driver(.., Some(duration))`. **Zero duration special case:** doesn't
  touch `state`; just `driver.park_timeout(handle, ZERO)` (poll events + fire timers, no sleep) and returns `Yes`.
* driver busy and `duration.is_zero()` → return `No` immediately (no condvar sleep with zero);
  with non-zero → condvar with timeout.

### `park_condvar(duration)`

```text
m = mutex.lock()
CAS(EMPTY -> PARKED_CONDVAR)
    Err(NOTIFIED) -> swap(EMPTY) (an acquire read that pairs with the unparker's write); return
    Err(other)    -> panic (inconsistent state)
loop:
    wait on condvar (with deadline recomputed manually – loom has no wait_timeout_until)
    timed out? -> swap(EMPTY): PARKED_CONDVAR or NOTIFIED are both fine; others panic
    else if CAS(NOTIFIED->EMPTY) ok -> return       // real notification
    else spurious wakeup -> loop
```

Overflowing deadline: `Instant::now().checked_add(d)` falls back to `now + 1s`
("best effort to avoid overflow").

### `Unparker::unpark(&self, driver)`

```rust
match self.state.swap(NOTIFIED, SeqCst) {
    EMPTY | NOTIFIED => {}                 // nobody sleeping: leave a token / already unparked
    PARKED_CONDVAR   => self.unpark_condvar(),
    PARKED_DRIVER    => driver.unpark(),   // wake the poller (mio Waker / eventfd etc.)
    actual           => panic!(..),
}
```

* It is a **swap, not a CAS**, on purpose (comment): the release store must happen even if
  already `NOTIFIED`, so the parked thread's later acquire sees all writes
  preceding *this* unpark call.
* `unpark_condvar`: `drop(self.mutex.lock()); condvar.notify_one();`. Taking and
  releasing the mutex first closes the window between the sleeper setting `PARKED_CONDVAR` and actually
  waiting on the condvar (lost-wake-up prevention); notifying *after* releasing avoids waking a
  thread that would immediately block on the mutex.

### `Parker::shutdown(handle)`

If the driver is free (`try_lock`): `driver.shutdown(handle)` (closes the I/O registrations, time wheel, signal driver). Always `condvar.notify_all()`.
The [shutdown protocol](./12-shutdown.md) calls it per core from `Core::shutdown`; only one succeeds in grabbing the driver.

## 3. Who owns the driver?

There is no designated "I/O thread". **Whichever idle worker wins `try_lock` first
becomes the driver thread for that park**, all others sleep on their own condvar.
Consequences:

| Fact | Where it shows up |
|---|---|
| A worker that parked on the driver may be woken by I/O events directly, with the events already dispatched to wakers → tasks scheduled via `schedule_task` while its `Core.park` is `None` | `schedule_local`: `should_notify && core.park.is_some()` – notification is *deferred* ("scheduling is from a resource driver. As notifications often come in batches, the notification is delayed until the park is complete") and performed at the end of `park_internal` (`should_notify_others`) |
| After waking from the driver, worker has `had_driver = Yes` | optional *eager driver handoff* (`tokio_unstable`, `enable_eager_driver_handoff`): in `run_task`, if the worker held the driver and hasn't notified anyone, wake another parked worker so the driver is released quickly |
| A wake directed at the driver-holder must interrupt the poller | `PARKED_DRIVER ⇒ driver.unpark()` |
| Worker not holding the driver must be woken via condvar | `PARKED_CONDVAR ⇒ unpark_condvar()` |

```text
  Worker A (driver owner)               Worker B                Worker C
  try_lock ok -> epoll_wait(timeout)    try_lock fails          try_lock fails
       ^                                condvar.wait()          condvar.wait()
       |  I/O event -> wakers -> schedule_task ... notify B (Idle.worker_to_notify -> sleepers.pop)
       +--- unpark(A) uses driver.unpark() ; unpark(B/C) use condvar.notify_one()
```

## 4. Invariants & subtle points

| # | Point |
|---|---|
| I1 | `state` is only ever written with `SeqCst`; the total order is what makes park/unpark race-free |
| I2 | A `NOTIFIED` token is never lost: set by `unpark` when no one sleeps, consumed by the next `park` |
| I3 | At most one thread is inside `Driver::park*` at a time (`TryLock`) |
| I4 | `park_condvar` is never entered with a zero timeout (its doc comment says it panics; callers branch on `is_zero` first) |
| I5 | Spurious condvar wake-ups are handled by the loop; spurious *returns* from `park` are handled one level up by `Core::park`'s `while` loop + `transition_from_parked` returning `false` while still in `sleepers` |
| I6 | `HadDriver::Yes` is returned even if the OS wait ended by timeout — it records "I used the driver", not "I got events" |

## 5. Interactions

* **Idle** ([08](./08-idle-coordination.md)): `Idle` picks *whom* to wake, `Parker` performs *how*.
  `Remote.unpark: Unparker` is what `notify_parked_{local,remote}` call: `self.shared.remotes[index].unpark.unpark(&self.driver)`.
* **Driver** ([13](./13-driver-interface.md)): `Driver::park/park_timeout/shutdown` and `driver::Handle::unpark`.
* **Worker** ([05](./05-worker-loop.md)): `Context::park_internal` takes `Parker` **out of `Core`** before sleeping
  (`core.park.take()`), stores the `Core` in the thread-local context so a driver-triggered wake can schedule locally, then puts the parker back.
  This is why `Core.park: Option<Parker>`.
* **block_in_place** ([11](./11-block-in-place-and-defer.md)): moves the `Core` (and its parker) to a fresh worker thread.

## 6. Tests

Loom models in `runtime/tests/loom_multi_thread.rs` (the whole pool relies on parking), and `tokio/tests/rt_threaded.rs`
(`many_oneshot_futures`, `wake_during_shutdown`, `start_stop_callbacks_called`, …).

<!-- TESTS:park -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [10 — Stats & metrics](./10-stats-and-metrics.md)
