# `tokio::runtime::io` — 66 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 41 |
| Trait impl | 13 |
| Private helper | 10 |
| Test | 2 |

## `tokio/src/runtime/io/driver.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 86 | `with_ready`  | `ReadyEvent` | Crate-internal | Constructor |  |
| 110 | `_assert_kinds`  |  | Private helper | Other / internal logic |  |
| 111 | `_assert`  |  | Private helper | Other / internal logic |  |
| 121 | `new`  | `Driver` | Crate-internal | Constructor | Creates a new event loop, returning any error that happened during the creation. |
| 164 | `park`  | `Driver` | Crate-internal | Wake / park |  |
| 169 | `park_timeout`  | `Driver` | Crate-internal | Wake / park |  |
| 174 | `shutdown`  | `Driver` | Crate-internal | Runtime/task control |  |
| 184 | `turn`  | `Driver` | Private helper | Other / internal logic |  |
| 265 | `fmt`  | `fmt::Debug for Driver` | Trait impl | Formatting |  |
| 280 | `unpark`  | `Handle` | Crate-internal | Wake / park | Forces a reactor blocked in a call to `turn` to wakeup, or otherwise makes the next call to `turn` return immediately. |
| 288 | `add_source`  | `Handle` | Crate-internal | Other / internal logic | Registers an I/O resource with the reactor for a given `mio::Ready` state. |
| 315 | `deregister_source`  | `Handle` | Crate-internal | I/O registration | Deregisters an I/O resource from the reactor. |
| 336 | `release_pending_registrations`  | `Handle` | Private helper | Locking / permits |  |
| 344 | `fmt`  | `fmt::Debug for Handle` | Trait impl | Formatting |  |
| 350 | `mask`  | `Direction` | Crate-internal | Other / internal logic |  |
| 364 | `busy_turn_takes_busy_batch`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/io/metrics.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `incr_fd_count`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |
| 13 | `dec_fd_count`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |
| 14 | `incr_ready_count_by`  | `IoDriverMetrics` | Crate-internal | Metrics / counters |  |

## `tokio/src/runtime/io/registration.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 73 | `new_with_interest_and_handle`  | `Registration` | Crate-internal | Constructor | Registers the I/O resource with the reactor for the provided handle, for a specific `Interest`. |
| 99 | `deregister`  | `Registration` | Crate-internal | I/O registration | Deregisters the I/O resource from the reactor it is associated with. |
| 103 | `clear_readiness`  | `Registration` | Crate-internal | I/O registration |  |
| 114 | `assume_ready`  | `Registration` | Crate-internal | Other / internal logic | Marks the resource ready without waiting for the driver's first event. |
| 120 | `poll_read_ready`  | `Registration` | Crate-internal | Poll function |  |
| 126 | `poll_write_ready`  | `Registration` | Crate-internal | Poll function |  |
| 133 | `poll_read_io`  | `Registration` | Crate-internal | Poll function |  |
| 143 | `poll_write_io`  | `Registration` | Crate-internal | Poll function |  |
| 155 | `poll_ready`  | `Registration` | Private helper | Poll function | Polls for events on the I/O resource's `direction` readiness stream. |
| 173 | `poll_io`  | `Registration` | Private helper | Poll function |  |
| 194 | `try_io`  | `Registration` | Crate-internal | Non-blocking attempt |  |
| 215 | `readiness` 🅰 | `Registration` | Crate-internal | I/O operation |  |
| 225 | `async_io` 🅰 | `Registration` | Crate-internal | Async operation |  |
| 247 | `handle`  | `Registration` | Private helper | Handle / reference plumbing |  |
| 253 | `drop`  | `Drop for Registration` | Trait impl | Drop / cleanup |  |
| 265 | `gone`  |  | Private helper | Other / internal logic |  |

## `tokio/src/runtime/io/registration_set.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `new`  | `RegistrationSet` | Crate-internal | Constructor |  |
| 47 | `is_shutdown`  | `RegistrationSet` | Crate-internal | Accessor / query |  |
| 52 | `needs_release`  | `RegistrationSet` | Crate-internal | Other / internal logic | Returns `true` if there are registrations that need to be released |
| 56 | `allocate`  | `RegistrationSet` | Crate-internal | Other / internal logic |  |
| 73 | `deregister`  | `RegistrationSet` | Crate-internal | I/O registration |  |
| 82 | `shutdown`  | `RegistrationSet` | Crate-internal | Runtime/task control |  |
| 103 | `release`  | `RegistrationSet` | Crate-internal | Locking / permits |  |
| 116 | `remove` ⚠ | `RegistrationSet` | Crate-internal | Data movement |  |
| 131 | `as_raw`  | `linked_list::Link for Arc<ScheduledIo>` | Trait impl | Intrusive-list link |  |
| 136 | `from_raw` ⚠ | `linked_list::Link for Arc<ScheduledIo>` | Trait impl | Intrusive-list link |  |
| 141 | `pointers` ⚠ | `linked_list::Link for Arc<ScheduledIo>` | Trait impl | Intrusive-list link |  |

## `tokio/src/runtime/io/scheduled_io.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 140 | `addr_of_pointers` ⚠ | `Waiter` | Private helper | Handle / reference plumbing |  |
| 177 | `default`  | `Default for ScheduledIo` | Trait impl | Constructor |  |
| 191 | `assume_ready`  | `ScheduledIo` | Crate-internal | Other / internal logic | Marks the resource ready in the given directions without an event from the driver. |
| 198 | `token`  | `ScheduledIo` | Crate-internal | Handle / reference plumbing |  |
| 204 | `shutdown`  | `ScheduledIo` | Crate-internal | Runtime/task control | Invoked when the IO driver is shut down; forces this `ScheduledIo` into a permanently shutdown state. |
| 218 | `set_readiness`  | `ScheduledIo` | Crate-internal | Configuration / setter | Sets the readiness on this `ScheduledIo` by invoking the given closure on the current value, returning the previous readiness value. |
| 251 | `wake`  | `ScheduledIo` | Crate-internal | Wake / park | Notifies all pending waiters that have registered interest in `ready`. |
| 303 | `ready_event`  | `ScheduledIo` | Crate-internal | I/O operation |  |
| 318 | `poll_readiness`  | `ScheduledIo` | Crate-internal | Poll function | Polls for readiness events in a given direction. |
| 372 | `clear_readiness`  | `ScheduledIo` | Crate-internal | I/O registration |  |
| 379 | `clear_wakers`  | `ScheduledIo` | Crate-internal | Other / internal logic |  |
| 387 | `drop`  | `Drop for ScheduledIo` | Trait impl | Drop / cleanup |  |
| 397 | `readiness` 🅰 | `ScheduledIo` | Crate-internal | I/O operation | An async version of `poll_readiness` which uses a linked list of wakers. |
| 405 | `readiness_fut`  | `ScheduledIo` | Private helper | I/O operation |  |
| 424 | `as_raw`  | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 428 | `from_raw` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 432 | `pointers` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 442 | `poll`  | `Future for Readiness<'_>` | Trait impl | Future impl (poll) |  |
| 582 | `drop`  | `Drop for Readiness<'_>` | Trait impl | Drop / cleanup |  |
| 602 | `stale_event_does_not_clear_readiness_after_u8_wraparound`  |  | Test | Other / internal logic |  |

