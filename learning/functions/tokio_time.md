# `tokio::time` — 78 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 39 |
| Crate-internal | 16 |
| Trait impl | 16 |
| Private helper | 7 |

## `tokio/src/time/clock.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `now`  |  | Crate-internal | Time / timers |  |
| 20 | `new`  | `Clock` | Crate-internal | Constructor |  |
| 24 | `now`  | `Clock` | Crate-internal | Time / timers |  |
| 38 | `with_clock`  |  | Private helper | Constructor |  |
| 56 | `with_clock`  |  | Private helper | Constructor |  |
| 161 | `pause`  |  | Public API | Other / internal logic | Pauses time. |
| 180 | `resume`  |  | Public API | Other / internal logic | Resumes time. |
| 270 | `advance` 🅰 |  | Public API | Async operation | Advances time. |
| 284 | `now`  |  | Crate-internal | Time / timers | Returns the current instant, factoring in frozen time. |
| 301 | `new`  | `Clock` | Crate-internal | Constructor | Returns a new `Clock` instance that uses the current execution context's source of time. |
| 322 | `pause`  | `Clock` | Crate-internal | Other / internal logic |  |
| 344 | `inhibit_auto_advance`  | `Clock` | Crate-internal | Other / internal logic | Temporarily stop auto-advancing the clock (see `tokio::time::pause`). |
| 349 | `allow_auto_advance`  | `Clock` | Crate-internal | Other / internal logic |  |
| 354 | `can_auto_advance`  | `Clock` | Crate-internal | Other / internal logic |  |
| 359 | `advance`  | `Clock` | Crate-internal | Other / internal logic |  |
| 370 | `now`  | `Clock` | Crate-internal | Time / timers |  |

## `tokio/src/time/error.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `from`  | `From<Kind> for Error` | Trait impl | Conversion |  |
| 58 | `shutdown`  | `Error` | Public API | Runtime/task control | Creates an error representing a shutdown timer. |
| 63 | `is_shutdown`  | `Error` | Public API | Accessor / query | Returns `true` if the error was caused by the timer being shutdown. |
| 68 | `at_capacity`  | `Error` | Public API | Other / internal logic | Creates an error representing a timer at capacity. |
| 73 | `is_at_capacity`  | `Error` | Public API | Accessor / query | Returns `true` if the error was caused by the timer being at capacity. |
| 78 | `invalid`  | `Error` | Public API | Other / internal logic | Creates an error representing a misconfigured timer. |
| 83 | `is_invalid`  | `Error` | Public API | Accessor / query | Returns `true` if the error was caused by the timer being misconfigured. |
| 91 | `fmt`  | `fmt::Display for Error` | Trait impl | Formatting |  |
| 106 | `new`  | `Elapsed` | Crate-internal | Constructor |  |
| 112 | `fmt`  | `fmt::Display for Elapsed` | Trait impl | Formatting |  |
| 120 | `from`  | `From<Elapsed> for std::io::Error` | Trait impl | Conversion |  |

## `tokio/src/time/instant.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 48 | `now`  | `Instant` | Public API | Time / timers | Returns an instant corresponding to "now". |
| 53 | `from_std`  | `Instant` | Public API | Conversion | Create a `tokio::time::Instant` from a `std::time::Instant`. |
| 58 | `into_std`  | `Instant` | Public API | Conversion | Convert the value into a `std::time::Instant`. |
| 64 | `duration_since`  | `Instant` | Public API | Other / internal logic | Returns the amount of time elapsed from another instant to this one, or zero duration if that instant is later than this one. |
| 85 | `checked_duration_since`  | `Instant` | Public API | Other / internal logic | Returns the amount of time elapsed from another instant to this one, or None if that instant is later than this one. |
| 106 | `saturating_duration_since`  | `Instant` | Public API | Other / internal logic | Returns the amount of time elapsed from another instant to this one, or zero duration if that instant is later than this one. |
| 126 | `elapsed`  | `Instant` | Public API | Time / timers | Returns the amount of time elapsed since this instant was created, or zero duration if this instant is in the future. |
| 133 | `checked_add`  | `Instant` | Public API | Other / internal logic | Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as `Instant` (which means it's inside the bounds of the underlying data structure), `None` otherwise. |
| 140 | `checked_sub`  | `Instant` | Public API | Other / internal logic | Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as `Instant` (which means it's inside the bounds of the underlying data structure), `None` otherwise. |
| 146 | `from`  | `From<std::time::Instant> for Instant` | Trait impl | Conversion |  |
| 152 | `from`  | `From<Instant> for std::time::Instant` | Trait impl | Conversion |  |
| 160 | `add`  | `ops::Add<Duration> for Instant` | Trait impl | Other / internal logic |  |
| 166 | `add_assign`  | `ops::AddAssign<Duration> for Instant` | Trait impl | Other / internal logic |  |
| 174 | `sub`  | `ops::Sub for Instant` | Trait impl | Other / internal logic |  |
| 182 | `sub`  | `ops::Sub<Duration> for Instant` | Trait impl | Other / internal logic |  |
| 188 | `sub_assign`  | `ops::SubAssign<Duration> for Instant` | Trait impl | Other / internal logic |  |
| 194 | `fmt`  | `fmt::Debug for Instant` | Trait impl | Formatting |  |
| 203 | `now`  |  | Crate-internal | Time / timers |  |
| 212 | `now`  |  | Crate-internal | Time / timers |  |

## `tokio/src/time/interval.rs` (14)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 73 | `interval`  |  | Public API | Time / timers | Creates new [`Interval`] that yields with interval of `period`. |
| 108 | `interval_at`  |  | Public API | Time / timers | Creates new [`Interval`] that yields with interval of `period` with the first tick completing at `start`. |
| 114 | `internal_interval_at`  |  | Private helper | Other / internal logic |  |
| 335 | `next_timeout`  | `MissedTickBehavior` | Private helper | Other / internal logic | If a tick is missed, this method is called to determine when the next tick should happen. |
| 370 | `default`  | `Default for MissedTickBehavior` | Trait impl | Constructor | Returns [`MissedTickBehavior::Burst`]. |
| 428 | `tick` 🅰 | `Interval` | Public API | Time / timers | Completes when the next instant in the interval has been reached. |
| 457 | `poll_tick`  | `Interval` | Public API | Poll function | Polls for the next instant in the interval to be reached. |
| 517 | `reset`  | `Interval` | Public API | Configuration / setter | Resets the interval to complete one period after the current time. |
| 549 | `reset_immediately`  | `Interval` | Public API | Other / internal logic | Resets the interval immediately. |
| 582 | `reset_after`  | `Interval` | Public API | Other / internal logic | Resets the interval after the specified [`std::time::Duration`]. |
| 619 | `reset_at`  | `Interval` | Public API | Time / timers | Resets the interval to a [`crate::time::Instant`] deadline. |
| 624 | `missed_tick_behavior`  | `Interval` | Public API | Other / internal logic | Returns the [`MissedTickBehavior`] strategy currently being used. |
| 629 | `set_missed_tick_behavior`  | `Interval` | Public API | Configuration / setter | Sets the [`MissedTickBehavior`] strategy that should be used. |
| 634 | `period`  | `Interval` | Public API | Other / internal logic | Returns the period of the interval. |

## `tokio/src/time/mod.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 87 | `safe_delay`  |  | Private helper | Other / internal logic |  |

## `tokio/src/time/sleep.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 62 | `sleep_until`  |  | Public API | Time / timers |  |
| 123 | `sleep`  |  | Public API | Time / timers |  |
| 230 | `drop`  | `PinnedDrop for Sleep` | Trait impl | Other / internal logic |  |
| 255 | `new_timeout`  | `Sleep` | Crate-internal | Constructor |  |
| 305 | `deadline`  | `Sleep` | Public API | Time / timers | Returns the instant at which the future will complete. |
| 312 | `is_elapsed`  | `Sleep` | Public API | Accessor / query | Returns `true` if `Sleep` has elapsed. |
| 345 | `reset`  | `Sleep` | Public API | Configuration / setter | Resets the `Sleep` instance to a new deadline. |
| 390 | `reset_without_timer` ⚠ | `Sleep` | Crate-internal | Other / internal logic | Resets the `Sleep` instance to a new deadline. |
| 396 | `poll_elapsed`  | `Sleep` | Private helper | Poll function |  |
| 469 | `poll`  | `Future for Sleep` | Trait impl | Future impl (poll) |  |

## `tokio/src/time/timeout.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 86 | `timeout`  |  | Public API | Time / timers | Requires a `Future` to complete before the specified duration has elapsed. |
| 165 | `timeout_at`  |  | Public API | Other / internal logic | Requires a `Future` to complete before the specified instant in time. |
| 189 | `get_ref`  | `Timeout<T>` | Public API | Accessor / query | Gets a reference to the underlying value in this timeout. |
| 194 | `get_mut`  | `Timeout<T>` | Public API | Accessor / query | Gets a mutable reference to the underlying value in this timeout. |
| 199 | `into_inner`  | `Timeout<T>` | Public API | Conversion | Consumes this timeout, returning the underlying value. |
| 210 | `poll`  | `Future for Timeout<T>` | Trait impl | Future impl (poll) |  |
| 229 | `poll_delay`  |  | Private helper | Poll function |  |

