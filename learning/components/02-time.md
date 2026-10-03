# Block 2 — Time (public API)

> **Role:** the user-facing time primitives: wait (`sleep`), give up (`timeout`), repeat (`interval`), read the clock (`Instant`), and control the clock in tests (`pause`/`advance`).
> In the [component diagram](./README.md): the "time" API box. It **registers timers** with the [Timer driver](./07-timer-driver.md), which does the actual bookkeeping and firing.

---

## 1. At a glance

<!-- STATS:time -->
| Metric | Value |
|---|---|
| Source files | 7 |
| Code lines | 769 (1.5% of `tokio/src`) |
| Doc + comment lines | 1,249 (1.62 per code line) |
| Functions | 78 — public API 39, trait impls 16, internal 23, inline tests 0 |
| `async fn` / `unsafe fn` | 2 / 1 |
| `unsafe` occurrences | 2 |
| Integration tests (`tokio/tests`) | 8 files, 76 test fns, 1,409 code lines |
<!-- /STATS -->

The smallest API block: **7 files, more docs than code** (1.6 doc lines per code line). The heavy lifting lives in the timer driver.

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | `Sleep`, `Timeout<F>`, `Interval` + `MissedTickBehavior`, `Instant`, `Elapsed`/`Error`, the `Clock` (real or paused/auto-advancing in tests). |
| **Does not own** | Storing timers, deciding when they fire, waking tasks ([Timer driver](./07-timer-driver.md)); the 1 ms tick conversion (`TimeSource` lives in the driver). |
| **Input** | Durations / deadlines from the user; the current runtime handle from the thread-local context. |
| **Output** | `TimerEntry` registrations (`init`, `reset`, `cancel`) and `poll_elapsed` calls into the timer driver. |
| **Boundary** | `Sleep` holds `driver: scheduler::Handle` + `timer: Option<Timer>` (enum: traditional `TimerEntry` or alternative timer). Everything else (`Timeout`, `Interval`) is built **on top of `Sleep`**. |

---

## 3. Files

<!-- FILES:time -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/time/sleep.rs`](../../tokio/src/time/sleep.rs) | 198 | 242 | 25.7% |
| [`tokio/src/time/clock.rs`](../../tokio/src/time/clock.rs) | 167 | 169 | 21.7% |
| [`tokio/src/time/interval.rs`](../../tokio/src/time/interval.rs) | 132 | 475 | 17.2% |
| [`tokio/src/time/instant.rs`](../../tokio/src/time/instant.rs) | 94 | 95 | 12.2% |
| [`tokio/src/time/timeout.rs`](../../tokio/src/time/timeout.rs) | 87 | 148 | 11.3% |
| [`tokio/src/time/error.rs`](../../tokio/src/time/error.rs) | 71 | 32 | 9.2% |
| [`tokio/src/time/mod.rs`](../../tokio/src/time/mod.rs) | 20 | 88 | 2.6% |
| **Total (7 files)** | **769** | **1,249** | 100% |
<!-- /FILES -->

```
time/
├── sleep.rs      Sleep, sleep(), sleep_until()               ← the only type that talks to the driver
├── timeout.rs    Timeout<F>, timeout(), timeout_at()         = future + Option<Sleep>
├── interval.rs   Interval, interval(), interval_at(), MissedTickBehavior   = Pin<Box<Sleep>> + period
├── instant.rs    Instant (wraps std::time::Instant)
├── clock.rs      Clock: now(), pause(), resume(), advance()  (test-util)
├── error.rs      Error (shutdown / at capacity / invalid), Elapsed
└── mod.rs        re-exports, docs
```

---

## 4. Data structures

```rust
pub struct Sleep {                       // time/sleep.rs (pin_project)
    deadline: Instant,
    driver: scheduler::Handle,           // the runtime it was created in
    inner: Inner,                        // tracing spans (unstable)
    #[pin] timer: Option<Timer>,         // None until first poll → lazy registration
}
// PinnedDrop: if registered, timer.cancel(driver) → unlink from the wheel

pub struct Timeout<T> {                  // time/timeout.rs
    #[pin] value: T,                     // the wrapped future
    #[pin] delay: Option<Sleep>,         // None when now + duration overflows Instant (never times out)
}

pub struct Interval {                    // time/interval.rs
    delay: Pin<Box<Sleep>>,              // reused for every tick (reset, never re-allocated)
    period: Duration,
    missed_tick_behavior: MissedTickBehavior,
}
pub enum MissedTickBehavior { Burst /* default */, Delay, Skip }

pub struct Instant { std: std::time::Instant }   // + offset when the clock is paused
pub(crate) struct Clock { inner: Mutex<Inner> }  // test-util: base instant, paused flag, auto-advance inhibit count
```

---

## 5. How it interacts with the other blocks

```
 user: sleep(d)            ──▶ Sleep { deadline = now + d, timer: None }     (no driver work yet)
 first poll                ──▶ coop::poll_proceed ─▶ deadline_to_tick ─▶ TimerEntry::init ─▶ [Timer drv] reregister
 later polls               ──▶ TimerEntry::poll_elapsed ─▶ StateCell: fired? Ready : store waker, Pending
 sleep.reset(new)          ──▶ TimerEntry::reset ─▶ later deadline? lock-free extend : reregister
 drop(sleep)               ──▶ TimerEntry::cancel ─▶ [Timer drv] clear_entry (unlink, O(1))
 timeout(d, fut).poll      ──▶ poll fut first; if Pending → poll the Sleep
 interval.tick().poll      ──▶ poll Sleep; on fire compute next deadline (MissedTickBehavior) and reset
 [Timer drv] fires         ──▶ wake() ─▶ [Tasks] ─▶ [Scheduler]
 Instant::now()            ──▶ Clock (real or paused)
```

| Other block | Direction | Through |
|---|---|---|
| Timer driver | → | `TimerEntry::{init, reset, cancel, poll_elapsed}`, `TimeSource::deadline_to_tick` |
| Scheduler | → | `scheduler::Handle::current()` captured at creation; panics *"A Tokio 1.x context was found, but timers are disabled"* if `enable_time` wasn't called |
| Tasks | → | `coop::poll_proceed` before checking the timer |
| `tokio-util` | ← | `DelayQueue` and `FutureExt::timeout` build on this block |
| `tokio-stream` | ← | `IntervalStream`, `StreamExt::timeout/throttle` |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `sleep(d)`, `sleep_until(t)` | `sleep.rs` | Create a `Sleep` (deadline = now + d) |
| `Sleep::poll` → `poll_elapsed` | `sleep.rs` | Lazy-register on first poll, then ask the entry if it fired |
| `Sleep::reset(t)`, `deadline()`, `is_elapsed()` | `sleep.rs` | Move the deadline without re-allocating |
| `timeout(d, fut)`, `timeout_at(t, fut)` | `timeout.rs` | Wrap a future with a `Sleep` |
| `Timeout::poll` | `timeout.rs` | Poll the inner future first; then the delay (even if the inner future used up the budget) |
| `Timeout::get_ref / get_mut / into_inner` | `timeout.rs` | Access the wrapped future |
| `interval(p)`, `interval_at(start, p)` | `interval.rs` | First tick is immediate (`interval`) or at `start` |
| `Interval::tick / poll_tick / reset / reset_immediately / reset_after / set_missed_tick_behavior` | `interval.rs` | Periodic ticking |
| `MissedTickBehavior::next_timeout` | `interval.rs` | `Burst`: `deadline + period`; `Delay`: `now + period`; `Skip`: next multiple of `period` after now |
| `Instant::now / elapsed / duration_since / checked_add / into_std` | `instant.rs` | Clock reads |
| `pause() / resume() / advance(d)` | `clock.rs` | Freeze / step virtual time (feature `test-util`) |

---

## 7. Flows

**`timeout(d, fut).await`**
1. `Timeout::poll` notes whether the task still has coop budget.
2. Polls `fut`. `Ready(v)` → `Ok(v)`.
3. Otherwise polls the `Sleep`. If polling `fut` used up the budget, the `Sleep` is polled **unconstrained** — so a busy future can't prevent its own timeout from being noticed.
4. `Sleep` ready → `Err(Elapsed)`; the caller drops `Timeout`, which drops `fut` (cancellation) and the `Sleep` (unlinks the timer).

**`interval.tick().await`** (`poll_tick`)
1. Wait for the inner `Sleep`.
2. If we are more than 5 ms late, compute the next deadline with `MissedTickBehavior`; otherwise `deadline + period`.
3. `reset_without_timer(next)` — cheap; the driver re-arms lazily.
4. Return the instant the tick was *scheduled* for.

**Paused time (tests):** with `start_paused = true` or `pause()`, `Instant::now()` stops. When every task is idle, the time driver's `park_thread_timeout` sees the clock can auto-advance and **jumps to the next timer** instead of sleeping. Blocking-pool work inhibits auto-advance while it runs.

---

## 8. Invariants & gotchas

- **Resolution is 1 ms; deadlines are rounded up** (`deadline_to_tick` adds 999 999 ns). `sleep(Duration::ZERO)` still yields once.
- **Lazy registration:** creating a `Sleep` costs nothing in the driver; it registers on first poll. A `Sleep` that's never polled never touches the wheel.
- **`Sleep` is `!Unpin`** (holds an intrusive list node) — to poll it by `&mut` in a loop, `tokio::pin!` it or `Box::pin` it.
- **Must be created inside a runtime with time enabled**; otherwise it panics.
- `Interval`'s default `Burst` fires missed ticks back-to-back; use `Delay` or `Skip` for "at most one tick per period" semantics.
- `timeout` does **not** stop CPU work inside the future — it only stops *polling* it.
- The wheel covers ≈ 2.2 years; later deadlines sit in its top level and are re-inserted as time passes (ticks are only capped near `u64::MAX` ms).

---

## 9. Tests & where to start

<!-- TESTS:time -->
**8 integration test files · 76 test functions · 1,409 code lines**

[`time_alt.rs`](../../tokio/tests/time_alt.rs), [`time_interval.rs`](../../tokio/tests/time_interval.rs), [`time_panic.rs`](../../tokio/tests/time_panic.rs), [`time_pause.rs`](../../tokio/tests/time_pause.rs), [`time_rt.rs`](../../tokio/tests/time_rt.rs), [`time_sleep.rs`](../../tokio/tests/time_sleep.rs), [`time_timeout.rs`](../../tokio/tests/time_timeout.rs), [`time_wasm.rs`](../../tokio/tests/time_wasm.rs)
<!-- /TESTS -->

**Read in this order:** `sleep.rs` (`poll_elapsed`) → `timeout.rs` → `interval.rs` → then the [Timer driver](./07-timer-driver.md).
**Contribution areas seen in history:** `Interval` API additions, docs on cancel safety and missed ticks, test-util time behavior.
