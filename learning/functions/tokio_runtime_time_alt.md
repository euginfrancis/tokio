# `tokio::runtime::time_alt` — 58 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 25 |
| Trait impl | 18 |
| Test | 10 |
| Private helper | 5 |

## `tokio/src/runtime/time_alt/cancellation_queue.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `drop`  | `Drop for Inner` | Trait impl | Drop / cleanup |  |
| 20 | `new`  | `Inner` | Private helper | Constructor |  |
| 31 | `push_front` ⚠ | `Inner` | Private helper | Data movement | # Safety Behavior is undefined if any of the following conditions are violated: - `hdl` must not in any [`super::cancellation_queue`], and also mus not in any [`super::WakeQueue`]. |
| 35 | `into_iter`  | `Inner` | Private helper | Conversion |  |
| 41 | `next`  | `Iterator for Iter` | Trait impl | Iterator |  |
| 61 | `send` ⚠ | `Sender` | Crate-internal | Data movement | # Safety Behavior is undefined if any of the following conditions are violated: - `hdl` must not in any cancellation queue. |
| 74 | `recv_all`  | `Receiver` | Crate-internal | Data movement |  |
| 79 | `new`  |  | Crate-internal | Constructor |  |

## `tokio/src/runtime/time_alt/context.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `new`  | `LocalContext` | Crate-internal | Constructor |  |
| 35 | `new_running`  | `TempLocalContext<'a>` | Crate-internal | Constructor |  |
| 42 | `new_shutdown`  | `TempLocalContext<'a>` | Crate-internal | Constructor |  |

## `tokio/src/runtime/time_alt/entry.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 62 | `as_raw`  | `linked_list::Link for Entry` | Trait impl | Intrusive-list link |  |
| 66 | `from_raw` ⚠ | `linked_list::Link for Entry` | Trait impl | Intrusive-list link |  |
| 72 | `pointers` ⚠ | `linked_list::Link for Entry` | Trait impl | Intrusive-list link |  |
| 93 | `as_raw`  | `linked_list::Link for RegistrationQueueEntry` | Trait impl | Intrusive-list link |  |
| 97 | `from_raw` ⚠ | `linked_list::Link for RegistrationQueueEntry` | Trait impl | Intrusive-list link |  |
| 103 | `pointers` ⚠ | `linked_list::Link for RegistrationQueueEntry` | Trait impl | Intrusive-list link |  |
| 124 | `as_raw`  | `linked_list::Link for CancellationQueueEntry` | Trait impl | Intrusive-list link |  |
| 128 | `from_raw` ⚠ | `linked_list::Link for CancellationQueueEntry` | Trait impl | Intrusive-list link |  |
| 134 | `pointers` ⚠ | `linked_list::Link for CancellationQueueEntry` | Trait impl | Intrusive-list link |  |
| 155 | `as_raw`  | `linked_list::Link for WakeQueueEntry` | Trait impl | Intrusive-list link |  |
| 159 | `from_raw` ⚠ | `linked_list::Link for WakeQueueEntry` | Trait impl | Intrusive-list link |  |
| 165 | `pointers` ⚠ | `linked_list::Link for WakeQueueEntry` | Trait impl | Intrusive-list link |  |
| 180 | `from`  | `From<&Handle> for NonNull<Entry>` | Trait impl | Conversion |  |
| 187 | `new`  | `Handle` | Crate-internal | Constructor |  |
| 200 | `wake`  | `Handle` | Crate-internal | Wake / park | Wake the entry if it is already in the pending queue of the timer wheel. |
| 214 | `register_cancel_tx`  | `Handle` | Crate-internal | I/O registration | Returns `false` if the `self` has already been cancelled or woken up. |
| 226 | `poll`  | `Handle` | Crate-internal | Poll function |  |
| 246 | `cancel`  | `Handle` | Crate-internal | Lifecycle / ref-count |  |
| 262 | `deadline`  | `Handle` | Crate-internal | Time / timers |  |
| 266 | `is_woken_up`  | `Handle` | Crate-internal | Accessor / query |  |
| 271 | `is_cancelled`  | `Handle` | Crate-internal | Accessor / query |  |
| 278 | `inner_strong_count`  | `Handle` | Test | Metrics / counters | Only used for unit tests. |

## `tokio/src/runtime/time_alt/registration_queue.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `drop`  | `Drop for RegistrationQueue` | Trait impl | Drop / cleanup |  |
| 20 | `new`  | `RegistrationQueue` | Crate-internal | Constructor |  |
| 31 | `push_front` ⚠ | `RegistrationQueue` | Crate-internal | Data movement | # Safety Behavior is undefined if any of the following conditions are violated: - `Entry::extra_pointers` of `hdl` must not being used. |
| 35 | `pop_front`  | `RegistrationQueue` | Crate-internal | Data movement |  |

## `tokio/src/runtime/time_alt/tests.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `new_handle`  |  | Test | Constructor |  |
| 18 | `new_handle_with_deadline`  |  | Test | Constructor |  |
| 25 | `model`  |  | Test | Other / internal logic |  |
| 34 | `wake_up_in_the_same_thread`  |  | Test | Wake / park |  |
| 64 | `cancel_in_the_same_thread`  |  | Test | Lifecycle / ref-count |  |
| 99 | `insert_of_already_cancelled_entry_does_not_enter_wheel`  |  | Test | Data movement |  |
| 138 | `cancel_races_with_insert`  |  | Test | Lifecycle / ref-count |  |
| 192 | `wake_up_in_the_different_thread`  |  | Test | Wake / park |  |
| 228 | `cancel_in_the_different_thread`  |  | Test | Lifecycle / ref-count |  |

## `tokio/src/runtime/time_alt/timer.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `fmt`  | `std::fmt::Debug for Timer` | Trait impl | Formatting |  |
| 23 | `new`  | `Timer` | Crate-internal | Constructor |  |
| 43 | `cancel`  | `Timer` | Crate-internal | Lifecycle / ref-count |  |
| 47 | `is_elapsed`  | `Timer` | Crate-internal | Accessor / query |  |
| 51 | `poll_elapsed`  | `Timer` | Crate-internal | Poll function |  |
| 56 | `with_current_temp_local_context`  |  | Private helper | Constructor |  |
| 108 | `push_from_remote`  |  | Private helper | Data movement |  |

## `tokio/src/runtime/time_alt/wake_queue.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `drop`  | `Drop for WakeQueue` | Trait impl | Drop / cleanup |  |
| 20 | `new`  | `WakeQueue` | Crate-internal | Constructor |  |
| 26 | `is_empty`  | `WakeQueue` | Crate-internal | Accessor / query |  |
| 35 | `push_front` ⚠ | `WakeQueue` | Crate-internal | Data movement | # Safety Behavior is undefined if any of the following conditions are violated: - `Entry::extra_pointers` of `hdl` must not being used. |
| 40 | `wake_all`  | `WakeQueue` | Crate-internal | Wake / park | Wakes all entries in the wake queue. |

