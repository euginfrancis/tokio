# Block 7 — Timer Driver

> **Role:** stores every pending timer of the runtime, tells the scheduler how long it may sleep, and fires (wakes) timers when their deadline passes.
> In the [component diagram](./README.md): the "TIMER DRIVER — wheel" box. It sits **between the scheduler and the I/O driver**: the scheduler parks in the timer driver, which parks in the I/O driver with a timeout equal to the next deadline.

---

## 1. At a glance

<!-- STATS:timer_driver -->
| Metric | Value |
|---|---|
| Source files | 20 |
| Code lines | 2,601 (5.1% of `tokio/src`) |
| Doc + comment lines | 883 (0.34 per code line) |
| Functions | 239 — public API 0, trait impls 28, internal 135, inline tests 76 |
| `async fn` / `unsafe fn` | 0 / 36 |
| `unsafe` occurrences | 124 |
| Integration tests (`tokio/tests`) | none dedicated — exercised through other blocks' tests |
<!-- /STATS -->

The highest `unsafe` density of any block: timers are **intrusive list nodes living inside user futures**, linked into the wheel by raw pointer.

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | The hierarchical timing wheel (6 levels × 64 slots, 1 ms ticks), each timer's shared state (`TimerShared`: deadline + fire state + waker), `Instant` ↔ tick conversion (`TimeSource`), the driver's park logic, firing, shutdown of timers, and the experimental per-worker **alternative timer** (`time_alt/`). |
| **Does not own** | The user API (`Sleep`, `Timeout`, `Interval` — [Time block](./02-time.md)); actually blocking the thread (it delegates to the [I/O driver](./08-io-driver.md) / `ParkThread`); scheduling the woken tasks ([Scheduler](./06-scheduler.md)). |
| **Input** | `reregister(tick, entry)`, `clear_entry(entry)` from `TimerEntry`; `park(handle)` / `park_timeout(handle, d)` from the scheduler. |
| **Output** | `Waker::wake()` for fired timers; `park_timeout(min(next_deadline - now, limit))` into the I/O stack; `unpark()` of the I/O driver when a new timer is earlier than the current sleep. |
| **Boundary types** | `TimerEntry` (owned by `Sleep`), `TimerHandle` (raw pointer used by the wheel), `time::Handle` (in `driver::Handle.time`), `time::Driver` (wraps `IoStack`). |

---

## 3. Files

<!-- FILES:timer_driver -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/runtime/time/entry.rs`](../../tokio/src/runtime/time/entry.rs) | 287 | 246 | 11.0% |
| [`tokio/src/runtime/time/wheel/mod.rs`](../../tokio/src/runtime/time/wheel/mod.rs) | 287 | 111 | 11.0% |
| [`tokio/src/runtime/time/mod.rs`](../../tokio/src/runtime/time/mod.rs) | 276 | 139 | 10.6% |
| [`tokio/src/runtime/time_alt/wheel/mod.rs`](../../tokio/src/runtime/time_alt/wheel/mod.rs) | 260 | 95 | 10.0% |
| [`tokio/src/runtime/time/tests/mod.rs`](../../tokio/src/runtime/time/tests/mod.rs) | 215 | 4 | 8.3% |
| [`tokio/src/runtime/time_alt/wheel/level.rs`](../../tokio/src/runtime/time_alt/wheel/level.rs) | 194 | 65 | 7.5% |
| [`tokio/src/runtime/time/wheel/level.rs`](../../tokio/src/runtime/time/wheel/level.rs) | 192 | 64 | 7.4% |
| [`tokio/src/runtime/time_alt/tests.rs`](../../tokio/src/runtime/time_alt/tests.rs) | 192 | 33 | 7.4% |
| [`tokio/src/runtime/time_alt/entry.rs`](../../tokio/src/runtime/time_alt/entry.rs) | 183 | 57 | 7.0% |
| [`tokio/src/runtime/time_alt/timer.rs`](../../tokio/src/runtime/time_alt/timer.rs) | 90 | 12 | 3.5% |
| [`tokio/src/runtime/time_alt/cancellation_queue/tests.rs`](../../tokio/src/runtime/time_alt/cancellation_queue/tests.rs) | 77 | 0 | 3.0% |
| [`tokio/src/runtime/time_alt/cancellation_queue.rs`](../../tokio/src/runtime/time_alt/cancellation_queue.rs) | 65 | 11 | 2.5% |
| [`tokio/src/runtime/time_alt/wake_queue/tests.rs`](../../tokio/src/runtime/time_alt/wake_queue/tests.rs) | 55 | 1 | 2.1% |
| [`tokio/src/runtime/time_alt/registration_queue/tests.rs`](../../tokio/src/runtime/time_alt/registration_queue/tests.rs) | 41 | 0 | 1.6% |
| [`tokio/src/runtime/time/handle.rs`](../../tokio/src/runtime/time/handle.rs) | 39 | 23 | 1.5% |
| [`tokio/src/runtime/time_alt/context.rs`](../../tokio/src/runtime/time_alt/context.rs) | 36 | 4 | 1.4% |
| [`tokio/src/runtime/time/source.rs`](../../tokio/src/runtime/time/source.rs) | 35 | 3 | 1.3% |
| [`tokio/src/runtime/time_alt/wake_queue.rs`](../../tokio/src/runtime/time_alt/wake_queue.rs) | 33 | 8 | 1.3% |
| [`tokio/src/runtime/time_alt/registration_queue.rs`](../../tokio/src/runtime/time_alt/registration_queue.rs) | 28 | 7 | 1.1% |
| [`tokio/src/runtime/time_alt/mod.rs`](../../tokio/src/runtime/time_alt/mod.rs) | 16 | 0 | 0.6% |
| **Total (20 files)** | **2,601** | **883** | 100% |
<!-- /FILES -->

```
runtime/time/                 TRADITIONAL timer (default)
├── mod.rs                    Driver (park), Handle internals (process, reregister, clear_entry), Inner
├── handle.rs                 time::Handle { time_source, inner }
├── entry.rs                  TimerEntry, TimerShared, StateCell, TimerHandle  (≈ the trickiest file)
├── source.rs                 TimeSource: Instant ↔ u64 ms ticks
└── wheel/{mod,level}.rs      Wheel { elapsed, levels[6], pending }, Level { occupied bitmap, slot[64] }
runtime/time_alt/             ALTERNATIVE timer (tokio_unstable + rt-multi-thread, Builder::enable_alt_timer)
├── context.rs                per-worker LocalContext { wheel, registration_queue, cancellation channel }
├── wheel/, entry.rs, timer.rs, registration_queue.rs, cancellation_queue.rs, wake_queue.rs
```

---

## 4. Data structures

```rust
pub(crate) struct Driver { park: IoStack }                // time/mod.rs — wraps the I/O stack it parks in

pub(crate) struct Handle {                                // time/handle.rs — shared by all threads
    time_source: TimeSource,                              // { start_time: Instant }
    inner: Inner,
}
enum Inner {
    Traditional { state: Mutex<InnerState>, is_shutdown: AtomicBool, did_wake: AtomicBool },
    Alternative { is_shutdown: AtomicBool, did_wake: AtomicBool },   // wheels live in worker Cores instead
}
struct InnerState {
    next_wake: Option<NonZeroU64>,                        // tick the parked thread will wake at
    wheel: wheel::Wheel,
}

pub(crate) struct Wheel {                                 // wheel/mod.rs
    elapsed: u64,                                         // ticks processed so far ("now" of the wheel)
    levels: Box<[Level; 6]>,
    pending: LinkedList<TimerShared>,                     // expired, waiting to be returned by poll()
}
pub(crate) struct Level {                                 // wheel/level.rs
    level: usize,
    occupied: u64,                                        // bit i = slot i non-empty
    slot: [LinkedList<TimerShared>; 64],                  // intrusive lists
}

pub(crate) struct TimerEntry { inner: TimerShared, … }   // entry.rs — embedded (pinned) in Sleep
pub(crate) struct TimerShared {                           // the node that's linked into the wheel
    pointers: linked_list::Pointers<TimerShared>,
    registered_when: AtomicU64,                           // deadline the wheel slot was chosen for
    state: StateCell,
    _p: PhantomPinned,
}
pub(super) struct StateCell {
    state: AtomicU64,          // true deadline tick, or STATE_PENDING_FIRE (u64::MAX-1), or STATE_DEREGISTERED (u64::MAX)
    result: UnsafeCell<TimerResult>,                      // Ok(()) or Err(shutdown)
    waker: AtomicWaker,                                   // the waiting task
}
pub(crate) struct TimerHandle { inner: NonNull<TimerShared> }   // what the wheel stores/returns
```

**Two deadlines per timer:** `registered_when` (which slot it's in) and `state` (the *true* deadline). A later deadline can be written to `state` lock-free; the wheel discovers it when the old slot expires and re-inserts the timer. That's the **lazy reset** that makes resetting idle timeouts nearly free.

---

## 5. How it interacts with the other blocks

```
 [Time API] Sleep first poll ──▶ TimerEntry::init ──▶ Handle::reregister ──lock──▶ wheel.insert
                                                              │ earlier than next_wake? ──▶ [I/O drv] unpark()
 [Time API] Sleep::reset (later) ──▶ extend_expiration (atomic store, no lock)
 [Time API] drop(Sleep) ──▶ TimerEntry::cancel ──▶ clear_entry ──lock──▶ wheel.remove (O(1))

 [Scheduler] idle ──▶ time::Driver::park(_timeout)
        ├─ lock; next = wheel.next_expiration_time(); store next_wake; unlock
        ├─ [I/O drv] park_timeout(min(next - now, limit))        ← thread sleeps in epoll_wait here
        └─ Handle::process(now) ──lock──▶ wheel.poll(now) ─▶ entry.fire(Ok) ─▶ WakeList (32 at a time, wake outside lock)
                                                                                   └─▶ [Tasks] wake ─▶ [Scheduler]
```

| Other block | Direction | Through |
|---|---|---|
| Time API | ← | `TimerEntry::{init, reset, cancel, poll_elapsed}`; `TimeSource::deadline_to_tick` |
| Scheduler | ← park / → none | `driver::Driver::park/park_timeout/shutdown` (the scheduler only ever talks to the top of the stack) |
| I/O driver | → | `IoStack::park_timeout`; `IoHandle::unpark` when an earlier timer appears |
| Tasks | → | `Waker::wake` of fired timers |
| Blocking pool | ← | blocking tasks *inhibit auto-advance* of a paused clock while running |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `Driver::new(park, clock)` | `time/mod.rs` | Wrap the I/O stack; create `Handle` with an empty wheel |
| `Driver::park / park_timeout / park_internal` | `time/mod.rs` | Compute sleep time from the next deadline, park the I/O stack, then `process` |
| `park_thread_timeout` | `time/mod.rs` | With a paused clock: park for 0, and if nothing woke, `clock.advance(duration)` (auto-advance) |
| `Handle::process / process_at_time(now)` | `time/mod.rs` | Fire every due timer; wake in batches of 32 outside the lock |
| `Handle::reregister(unpark, tick, entry)` | `time/mod.rs` | Move/insert a timer; unpark if it's now the earliest; fire immediately if already elapsed |
| `Handle::clear_entry(entry)` | `time/mod.rs` | Remove a timer (on drop); also a happens-before fence with the driver |
| `Driver::shutdown` | `time/mod.rs` | Set `is_shutdown`, `process_at_time(u64::MAX)` (fire everything), shut down the I/O stack |
| `Wheel::insert / remove / poll / next_expiration / next_expiration_time / poll_at` | `wheel/mod.rs` | Wheel operations |
| `Wheel::process_expiration`, `level_for` | `wheel/mod.rs` | Cascade a slot's timers to finer levels or into `pending` |
| `Level::add_entry / remove_entry / next_expiration / next_occupied_slot / take_slot` | `wheel/level.rs` | Bitmap + slot lists |
| `TimerEntry::init / reset / cancel / poll_elapsed / is_elapsed` | `entry.rs` | Owner-side API |
| `TimerShared::extend_expiration / set_expiration / mark_pending / fire` | `entry.rs` | Lock-free extend; driver-side state changes |
| `StateCell::poll / fire / mark_pending` | `entry.rs` | The atomic deadline/fired state + waker |
| `TimeSource::deadline_to_tick / instant_to_tick / tick_to_duration / now` | `source.rs` | ms tick math (round **up**) |

---

## 7. Flows

**Insert** (`Wheel::insert`): `level = level_for(elapsed, when)` (highest differing 6-bit group of `elapsed XOR when`), `slot = (when >> 6·level) % 64`, push into `slot` list, set `occupied` bit. If `when <= elapsed` → `Err(Elapsed)` and the caller fires it at once.

**Park** (`park_internal`): lock → `next_expiration_time()` (scan 6 levels with `rotate_right` + `trailing_zeros` on each `occupied` bitmap) → record `next_wake` → unlock → park I/O for the remaining time (or 0 if overdue; forever if no timers) → `process(now)`.

**Process** (`Wheel::poll(now)`): loop { return anything in `pending`; find the earliest expiring slot; if its deadline ≤ now → `process_expiration`: take the whole slot; for each timer `mark_pending(deadline)` — if its *true* deadline has arrived it moves to `pending`, otherwise (higher level, or lazily extended) it's re-inserted at a finer level } → `fire(Ok)` each pending timer → collect wakers.

**Alternative timer** (`time_alt`, unstable): each worker `Core` owns a `LocalContext { wheel, registration_queue, canc_tx, canc_rx }`; timers register into the local wheel of the worker that polls them; registrations from non-worker threads go through `Shared.synced.inject_timers`; cancellations go through a channel. This avoids the global `Mutex<InnerState>` under heavy timer load.

---

## 8. Invariants & gotchas

- **Rule from `entry.rs`:** `TimerShared` may be touched only via `&mut TimerEntry` **or** while holding the driver lock — that's what makes the many relaxed/non-atomic writes sound.
- A timer is in **at most one list** (a slot, or `pending`) — `Pointers` are reused.
- Dropping a `Sleep` must unlink it *before* its memory is freed → `PinnedDrop` → `cancel` → `clear_entry` under the lock.
- Wakers are always called **after** releasing the lock (`WakeList`), never inside it.
- `next_wake` lets `reregister` decide cheaply whether the sleeping thread must be woken to shorten its sleep.
- After shutdown, polling a `Sleep` panics (`RUNTIME_SHUTTING_DOWN_ERROR`); `reregister` fires new entries with `Err(shutdown)`.
- Paused clock: auto-advance happens **only** when the runtime is fully idle and no blocking task inhibits it.

---

## 9. Tests & where to start

<!-- TESTS:timer_driver -->
_No integration test files are dedicated to this block._
<!-- /TESTS -->

The driver is tested through `tokio/tests/time_*.rs` and `rt_*.rs` (see [Time block](./02-time.md)), plus inline unit tests in `wheel/mod.rs` (`test_level_for`), `runtime/time/tests/` and loom models.

**Read in this order:** the module doc at the top of `entry.rs` → `wheel/mod.rs` (`level_for`, `insert`, `poll`) → `wheel/level.rs` → `time/mod.rs` (`park_internal`, `process_at_time`, `reregister`).
**Hands-on:** [`dsa-exercises/src/wheel.rs`](../dsa-exercises/src/wheel.rs) is a safe-Rust version of this wheel with tests.
