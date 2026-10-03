# `tokio::runtime::time` — 67 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 44 |
| Private helper | 14 |
| Trait impl | 8 |
| Test | 1 |

## `tokio/src/runtime/time/entry.rs` (38)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 104 | `default`  | `Default for StateCell` | Trait impl | Constructor |  |
| 110 | `fmt`  | `std::fmt::Debug for StateCell` | Trait impl | Formatting |  |
| 116 | `new`  | `StateCell` | Private helper | Constructor |  |
| 124 | `is_pending`  | `StateCell` | Private helper | Accessor / query |  |
| 129 | `when`  | `StateCell` | Private helper | Other / internal logic | Returns the current expiration time, or None if not currently scheduled. |
| 141 | `poll`  | `StateCell` | Private helper | Poll function | If the timer is completed, returns the result of the timer. |
| 150 | `read_state`  | `StateCell` | Private helper | I/O operation |  |
| 170 | `mark_pending` ⚠ | `StateCell` | Private helper | Other / internal logic | Marks this timer as being moved to the pending list, if its scheduled time is not after `not_after`. |
| 210 | `fire` ⚠ | `StateCell` | Private helper | Other / internal logic | Fires the timer, setting the result to the provided result. |
| 237 | `set_expiration`  | `StateCell` | Private helper | Configuration / setter | Marks the timer as registered (poll will return None) and sets the expiration time. |
| 251 | `extend_expiration`  | `StateCell` | Private helper | Other / internal logic | Attempts to adjust the timer to a new timestamp. |
| 274 | `might_be_registered`  | `StateCell` | Crate-internal | Other / internal logic | Returns true if the state of this timer indicates that the timer might be registered with the driver. |
| 349 | `fmt`  | `std::fmt::Debug for TimerShared` | Trait impl | Formatting |  |
| 362 | `addr_of_pointers` ⚠ | `TimerShared` | Private helper | Handle / reference plumbing |  |
| 369 | `new`  | `TimerShared` | Crate-internal | Constructor |  |
| 379 | `registered_when`  | `TimerShared` | Crate-internal | I/O registration | Gets the cached time-of-expiration value. |
| 389 | `sync_when` ⚠ | `TimerShared` | Crate-internal | Other / internal logic | Gets the true time-of-expiration value, and copies it into the cached time-of-expiration value. |
| 401 | `set_registered_when` ⚠ | `TimerShared` | Private helper | Configuration / setter | Sets the cached time-of-expiration value. |
| 406 | `true_when`  | `TimerShared` | Crate-internal | Other / internal logic | Returns the true time-of-expiration value, with relaxed memory ordering. |
| 415 | `set_expiration` ⚠ | `TimerShared` | Crate-internal | Configuration / setter | Sets the true time-of-expiration value, even if it is less than the current expiration or the timer is deregistered. |
| 421 | `extend_expiration`  | `TimerShared` | Crate-internal | Other / internal logic | Sets the true time-of-expiration only if it is after the current. |
| 426 | `handle`  | `TimerShared` | Crate-internal | Handle / reference plumbing | Returns a `TimerHandle` for this timer. |
| 436 | `might_be_registered`  | `TimerShared` | Crate-internal | Other / internal logic | Returns true if the state of this timer indicates that the timer might be registered with the driver. |
| 446 | `as_raw`  | `linked_list::Link for TimerShared` | Trait impl | Intrusive-list link |  |
| 450 | `from_raw` ⚠ | `linked_list::Link for TimerShared` | Trait impl | Intrusive-list link |  |
| 454 | `pointers` ⚠ | `linked_list::Link for TimerShared` | Trait impl | Intrusive-list link |  |
| 464 | `new`  | `TimerEntry` | Crate-internal | Constructor |  |
| 470 | `init`  | `TimerEntry` | Crate-internal | Other / internal logic |  |
| 479 | `is_elapsed`  | `TimerEntry` | Crate-internal | Accessor / query |  |
| 485 | `cancel`  | `TimerEntry` | Crate-internal | Lifecycle / ref-count | Cancels and deregisters the timer. |
| 511 | `reset`  | `TimerEntry` | Crate-internal | Configuration / setter |  |
| 524 | `poll_elapsed`  | `TimerEntry` | Crate-internal | Poll function |  |
| 540 | `registered_when` ⚠ | `TimerHandle` | Crate-internal | I/O registration |  |
| 544 | `sync_when` ⚠ | `TimerHandle` | Crate-internal | Other / internal logic |  |
| 548 | `is_pending` ⚠ | `TimerHandle` | Crate-internal | Accessor / query |  |
| 556 | `set_expiration` ⚠ | `TimerHandle` | Crate-internal | Configuration / setter | Forcibly sets the true and cached expiration times to the given tick. |
| 571 | `mark_pending` ⚠ | `TimerHandle` | Crate-internal | Other / internal logic | Attempts to mark this entry as pending. |
| 600 | `fire` ⚠ | `TimerHandle` | Crate-internal | Other / internal logic | Attempts to transition to a terminal state. |

## `tokio/src/runtime/time/handle.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `time_source`  | `Handle` | Crate-internal | Other / internal logic | Returns the time source associated with this handle. |
| 17 | `is_shutdown`  | `Handle` | Crate-internal | Accessor / query | Checks whether the driver has been shutdown. |
| 22 | `unpark`  | `Handle` | Crate-internal | Wake / park | Track that the driver is being unparked |
| 58 | `current`  | `Handle` | Crate-internal | Handle / reference plumbing | Tries to get a handle to the current timer. |
| 65 | `fmt`  | `fmt::Debug for Handle` | Trait impl | Formatting |  |

## `tokio/src/runtime/time/mod.rs` (18)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 145 | `new`  | `Driver` | Crate-internal | Constructor | Creates a new `Driver` instance that uses `park` to block the current thread and `time_source` to get the current time and convert to ticks. |
| 168 | `new_alt`  | `Driver` | Crate-internal | Constructor |  |
| 181 | `park`  | `Driver` | Crate-internal | Wake / park |  |
| 185 | `park_timeout`  | `Driver` | Crate-internal | Wake / park |  |
| 189 | `shutdown`  | `Driver` | Crate-internal | Runtime/task control |  |
| 213 | `park_internal`  | `Driver` | Private helper | Wake / park |  |
| 259 | `park_thread_timeout`  | `Driver` | Private helper | Wake / park |  |
| 283 | `park_thread_timeout`  | `Driver` | Private helper | Wake / park |  |
| 290 | `process`  | `Handle` | Crate-internal | Other / internal logic |  |
| 296 | `process_at_time`  | `Handle` | Crate-internal | Runtime/task control |  |
| 340 | `process_at_time_alt`  | `Handle` | Crate-internal | Runtime/task control |  |
| 360 | `shutdown_alt`  | `Handle` | Crate-internal | Runtime/task control |  |
| 380 | `clear_entry` ⚠ | `Handle` | Crate-internal | Other / internal logic | Removes a registered timer from the driver. |
| 398 | `reregister` ⚠ | `Handle` | Crate-internal | Other / internal logic | Removes and re-adds an entry to the driver. |
| 453 | `did_wake`  | `Handle` | Crate-internal | Other / internal logic |  |
| 467 | `lock`  | `Inner` | Crate-internal | Locking / permits | Locks the driver's inner structure |
| 476 | `is_shutdown`  | `Inner` | Crate-internal | Accessor / query |  |
| 486 | `fmt`  | `fmt::Debug for Inner` | Trait impl | Formatting |  |

## `tokio/src/runtime/time/source.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `new`  | `TimeSource` | Crate-internal | Constructor |  |
| 17 | `deadline_to_tick`  | `TimeSource` | Crate-internal | Other / internal logic |  |
| 22 | `instant_to_tick`  | `TimeSource` | Crate-internal | Other / internal logic |  |
| 32 | `tick_to_duration`  | `TimeSource` | Crate-internal | Time / timers |  |
| 36 | `now`  | `TimeSource` | Crate-internal | Time / timers |  |
| 42 | `start_time`  | `TimeSource` | Test | Runtime/task control |  |

