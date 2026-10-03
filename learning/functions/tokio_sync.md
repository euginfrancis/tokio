# `tokio::sync` — 386 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 158 |
| Private helper | 99 |
| Trait impl | 96 |
| Crate-internal | 29 |
| Test | 4 |

## `tokio/src/sync/barrier.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 63 | `new`  | `Barrier` | Public API | Constructor | Creates a new barrier that can block a given number of tasks. |
| 125 | `wait` 🅰 | `Barrier` | Public API | Runtime/task control | Does not resolve until all tasks have rendezvoused here. |
| 139 | `wait_internal` 🅰 | `Barrier` | Private helper | Runtime/task control |  |
| 210 | `is_leader`  | `BarrierWaitResult` | Public API | Accessor / query | Returns `true` if this task from wait is the "leader task". |

## `tokio/src/sync/batch_semaphore.rs` (30)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 116 | `addr_of_pointers` ⚠ | `Waiter` | Private helper | Handle / reference plumbing |  |
| 140 | `new`  | `Semaphore` | Crate-internal | Constructor | Creates a new semaphore with the initial number of permits Maximum number of permits on 32-bit platforms is `1<<29`. |
| 182 | `const_new` 🅲 | `Semaphore` | Crate-internal | Constructor | Creates a new semaphore with the initial number of permits. |
| 197 | `new_closed`  | `Semaphore` | Crate-internal | Constructor | Creates a new closed semaphore with 0 permits. |
| 211 | `const_new_closed` 🅲 | `Semaphore` | Crate-internal | Constructor | Creates a new closed semaphore with 0 permits. |
| 224 | `available_permits`  | `Semaphore` | Crate-internal | Other / internal logic | Returns the current number of available permits. |
| 231 | `release`  | `Semaphore` | Crate-internal | Locking / permits | Adds `added` new permits to the semaphore. |
| 242 | `close`  | `Semaphore` | Crate-internal | Data movement | Closes the semaphore. |
| 262 | `is_closed`  | `Semaphore` | Crate-internal | Accessor / query | Returns true if the semaphore is closed. |
| 266 | `try_acquire`  | `Semaphore` | Crate-internal | Non-blocking attempt |  |
| 297 | `acquire`  | `Semaphore` | Crate-internal | Locking / permits |  |
| 306 | `add_permits_locked`  | `Semaphore` | Private helper | Locking / permits | Release `rem` permits to the semaphore's wait list, starting from the end of the queue. |
| 376 | `forget_permits`  | `Semaphore` | Crate-internal | Locking / permits | Decrease a semaphore's permits by a maximum of `n`. |
| 397 | `poll_acquire`  | `Semaphore` | Private helper | Poll function |  |
| 526 | `fmt`  | `fmt::Debug for Semaphore` | Trait impl | Formatting |  |
| 534 | `new`  | `Waiter` | Private helper | Constructor |  |
| 551 | `assign_permits`  | `Waiter` | Private helper | Other / internal logic | Assign permits to the waiter. |
| 578 | `poll`  | `Future for Acquire<'_>` | Trait impl | Future impl (poll) |  |
| 622 | `new`  | `Acquire<'a>` | Private helper | Constructor |  |
| 666 | `project`  | `Acquire<'a>` | Private helper | Combinator / iteration |  |
| 667 | `is_unpin`  |  | Private helper | Accessor / query |  |
| 687 | `drop`  | `Drop for Acquire<'_>` | Trait impl | Drop / cleanup |  |
| 721 | `closed`  | `AcquireError` | Private helper | Data movement |  |
| 727 | `fmt`  | `fmt::Display for AcquireError` | Trait impl | Formatting |  |
| 739 | `is_closed`  | `TryAcquireError` | Crate-internal | Accessor / query | Returns `true` if the error was caused by a closed semaphore. |
| 746 | `is_no_permits`  | `TryAcquireError` | Crate-internal | Accessor / query | Returns `true` if the error was caused by calling `try_acquire` on a semaphore with no available permits. |
| 752 | `fmt`  | `fmt::Display for TryAcquireError` | Trait impl | Formatting |  |
| 769 | `as_raw`  | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 773 | `from_raw` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 777 | `pointers` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |

## `tokio/src/sync/broadcast.rs` (58)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 278 | `fmt`  | `fmt::Display for SendError<T>` | Trait impl | Formatting |  |
| 311 | `fmt`  | `fmt::Display for RecvError` | Trait impl | Formatting |  |
| 353 | `fmt`  | `fmt::Display for TryRecvError` | Trait impl | Formatting |  |
| 440 | `new`  | `Waiter` | Private helper | Constructor |  |
| 452 | `addr_of_pointers` ⚠ | `Waiter` | Private helper | Handle / reference plumbing |  |
| 539 | `channel`  |  | Public API | Constructor | Create a bounded, multi-producer, multi-consumer channel where each sent value is broadcasted to all active receivers. |
| 557 | `new`  | `Sender<T>` | Public API | Constructor | Creates the sending-half of the [`broadcast`] channel. |
| 574 | `new_with_receiver_count` ⚠ | `Sender<T>` | Private helper | Constructor | Creates the sending-half of the [`broadcast`](self) channel, and provide the receiver count. |
| 660 | `send`  | `Sender<T>` | Public API | Data movement | Attempts to send a value to all active [`Receiver`] handles, returning it back if it could not be sent. |
| 721 | `subscribe`  | `Sender<T>` | Public API | Data movement | Creates a new [`Receiver`] handle that will receive values sent **after** this call to `subscribe`. |
| 731 | `downgrade`  | `Sender<T>` | Public API | Handle / reference plumbing | Converts the `Sender` to a [`WeakSender`] that does not count towards RAII semantics, i.e. |
| 775 | `len`  | `Sender<T>` | Public API | Accessor / query | Returns the number of queued values. |
| 822 | `is_empty`  | `Sender<T>` | Public API | Accessor / query | Returns true if there are no queued values. |
| 865 | `receiver_count`  | `Sender<T>` | Public API | Data movement | Returns the number of active receivers. |
| 889 | `same_channel`  | `Sender<T>` | Public API | Handle / reference plumbing | Returns `true` if senders belong to the same channel. |
| 918 | `closed` 🅰 | `Sender<T>` | Public API | Data movement | A future which completes when the number of [Receiver]s subscribed to this `Sender` reaches zero. |
| 934 | `close_channel`  | `Sender<T>` | Private helper | Data movement |  |
| 942 | `strong_count`  | `Sender<T>` | Public API | Metrics / counters | Returns the number of [`Sender`] handles. |
| 947 | `weak_count`  | `Sender<T>` | Public API | Metrics / counters | Returns the number of [`WeakSender`] handles. |
| 953 | `new_receiver`  |  | Private helper | Constructor | Create a new `Receiver` which reads starting from the tail. |
| 983 | `drop`  | `Drop for WaitersList<'a, T>` | Trait impl | Drop / cleanup |  |
| 994 | `new`  | `WaitersList<'a, T>` | Private helper | Constructor |  |
| 1010 | `pop_back_locked`  | `WaitersList<'a, T>` | Private helper | Data movement | Removes the last element from the guarded list. |
| 1022 | `notify_rx`  | `Shared<T>` | Private helper | Wake / park |  |
| 1088 | `clone`  | `Clone for Sender<T>` | Trait impl | Clone |  |
| 1097 | `drop`  | `Drop for Sender<T>` | Trait impl | Drop / cleanup |  |
| 1110 | `upgrade`  | `WeakSender<T>` | Public API | Handle / reference plumbing | Tries to convert a `WeakSender` into a [`Sender`]. |
| 1135 | `strong_count`  | `WeakSender<T>` | Public API | Metrics / counters | Returns the number of [`Sender`] handles. |
| 1140 | `weak_count`  | `WeakSender<T>` | Public API | Metrics / counters | Returns the number of [`WeakSender`] handles. |
| 1146 | `clone`  | `Clone for WeakSender<T>` | Trait impl | Clone |  |
| 1155 | `drop`  | `Drop for WeakSender<T>` | Trait impl | Drop / cleanup |  |
| 1198 | `len`  | `Receiver<T>` | Public API | Accessor / query | Returns the number of messages that were sent into the channel and that this [`Receiver`] has yet to receive. |
| 1228 | `is_empty`  | `Receiver<T>` | Public API | Accessor / query | Returns true if there aren't any messages in the channel that the [`Receiver`] has yet to receive. |
| 1251 | `same_channel`  | `Receiver<T>` | Public API | Handle / reference plumbing | Returns `true` if receivers belong to the same channel. |
| 1256 | `recv_ref`  | `Receiver<T>` | Private helper | Data movement | Locks the next value if there is one. |
| 1364 | `sender_strong_count`  | `Receiver<T>` | Public API | Data movement | Returns the number of [`Sender`] handles. |
| 1369 | `sender_weak_count`  | `Receiver<T>` | Public API | Data movement | Returns the number of [`WeakSender`] handles. |
| 1394 | `is_closed`  | `Receiver<T>` | Public API | Accessor / query | Checks if a channel is closed. |
| 1424 | `resubscribe`  | `Receiver<T>` | Public API | Other / internal logic | Re-subscribes to the channel starting from the current tail element. |
| 1502 | `recv` 🅰 | `Receiver<T>` | Public API | Data movement | Receives the next value for this receiver. |
| 1548 | `try_recv`  | `Receiver<T>` | Public API | Non-blocking attempt | Attempts to return a pending value on this receiver without awaiting. |
| 1580 | `blocking_recv`  | `Receiver<T>` | Public API | Blocking (sync) variant | Blocking receive to call outside of asynchronous contexts. |
| 1586 | `drop`  | `Drop for Receiver<T>` | Trait impl | Drop / cleanup |  |
| 1615 | `new`  | `Recv<'a, T>` | Private helper | Constructor |  |
| 1629 | `project`  | `Recv<'a, T>` | Private helper | Combinator / iteration | A custom `project` implementation is used in place of `pin-project-lite` as a custom drop implementation is needed. |
| 1646 | `poll`  | `Future for Recv<'a, T>` | Trait impl | Future impl (poll) |  |
| 1663 | `drop`  | `Drop for Recv<'a, T>` | Trait impl | Drop / cleanup |  |
| 1709 | `as_raw`  | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1713 | `from_raw` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1717 | `pointers` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1723 | `fmt`  | `fmt::Debug for Sender<T>` | Trait impl | Formatting |  |
| 1729 | `fmt`  | `fmt::Debug for WeakSender<T>` | Trait impl | Formatting |  |
| 1735 | `fmt`  | `fmt::Debug for Receiver<T>` | Trait impl | Formatting |  |
| 1741 | `clone_value`  | `RecvGuard<'a, T>` | Private helper | Other / internal logic |  |
| 1750 | `drop`  | `Drop for RecvGuard<'a, T>` | Trait impl | Drop / cleanup |  |
| 1759 | `is_unpin`  |  | Private helper | Accessor / query |  |
| 1767 | `receiver_count_on_sender_constructor`  |  | Test | Data movement |  |
| 1790 | `receiver_count_on_channel_constructor`  |  | Test | Data movement |  |

## `tokio/src/sync/mutex.rs` (56)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 296 | `fmt`  | `fmt::Display for TryLockError` | Trait impl | Formatting |  |
| 305 | `bounds`  |  | Private helper | Other / internal logic |  |
| 306 | `check_send`  |  | Private helper | Runtime/task control |  |
| 307 | `check_unpin`  |  | Private helper | Runtime/task control |  |
| 309 | `check_send_sync_val`  |  | Private helper | Runtime/task control |  |
| 310 | `check_send_sync`  |  | Private helper | Runtime/task control |  |
| 311 | `check_static`  |  | Private helper | Runtime/task control |  |
| 312 | `check_static_val`  |  | Private helper | Runtime/task control |  |
| 338 | `new`  | `Mutex<T>` | Public API | Constructor | Creates a new lock in an unlocked state ready for use. |
| 395 | `const_new` 🅲 | `Mutex<T>` | Public API | Constructor | Creates a new lock in an unlocked state ready for use. |
| 434 | `lock` 🅰 | `Mutex<T>` | Public API | Locking / permits | Locks this mutex, causing the current task to yield until the lock has been acquired. |
| 520 | `blocking_lock`  | `Mutex<T>` | Public API | Blocking (sync) variant | Blockingly locks this `Mutex`. |
| 578 | `blocking_lock_owned`  | `Mutex<T>` | Public API | Blocking (sync) variant | Blockingly locks this `Mutex`. |
| 618 | `lock_owned` 🅰 | `Mutex<T>` | Public API | Locking / permits | Locks this mutex, causing the current task to yield until the lock has been acquired. |
| 655 | `acquire` 🅰 | `Mutex<T>` | Private helper | Locking / permits |  |
| 682 | `try_lock`  | `Mutex<T>` | Public API | Non-blocking attempt | Attempts to acquire the lock, and returns [`TryLockError`] if the lock is currently held somewhere else. |
| 722 | `get_mut`  | `Mutex<T>` | Public API | Accessor / query | Returns a mutable reference to the underlying data. |
| 750 | `try_lock_owned`  | `Mutex<T>` | Public API | Non-blocking attempt | Attempts to acquire the lock, and returns [`TryLockError`] if the lock is currently held somewhere else. |
| 787 | `into_inner`  | `Mutex<T>` | Public API | Conversion | Consumes the mutex, returning the underlying data. |
| 796 | `from`  | `From<T> for Mutex<T>` | Trait impl | Conversion |  |
| 805 | `default`  | `Default for Mutex<T>` | Trait impl | Constructor |  |
| 814 | `fmt`  | `std::fmt::Debug for Mutex<T>` | Trait impl | Formatting |  |
| 827 | `skip_drop`  | `MutexGuard<'a, T>` | Private helper | Combinator / iteration |  |
| 869 | `map`  | `MutexGuard<'a, T>` | Public API | Combinator / iteration | Makes a new [`MappedMutexGuard`] for a component of the locked data. |
| 918 | `try_map`  | `MutexGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`MappedMutexGuard`] for a component of the locked data. |
| 959 | `mutex`  | `MutexGuard<'a, T>` | Public API | Other / internal logic | Returns a reference to the original `Mutex`. |
| 965 | `drop`  | `Drop for MutexGuard<'_, T>` | Trait impl | Drop / cleanup |  |
| 980 | `deref`  | `Deref for MutexGuard<'_, T>` | Trait impl | Deref |  |
| 986 | `deref_mut`  | `DerefMut for MutexGuard<'_, T>` | Trait impl | Deref |  |
| 992 | `fmt`  | `fmt::Debug for MutexGuard<'_, T>` | Trait impl | Formatting |  |
| 998 | `fmt`  | `fmt::Display for MutexGuard<'_, T>` | Trait impl | Formatting |  |
| 1006 | `skip_drop`  | `OwnedMutexGuard<T>` | Private helper | Combinator / iteration |  |
| 1051 | `map`  | `OwnedMutexGuard<T>` | Public API | Combinator / iteration | Makes a new [`OwnedMappedMutexGuard`] for a component of the locked data. |
| 1100 | `try_map`  | `OwnedMutexGuard<T>` | Public API | Non-blocking attempt | Attempts to make a new [`OwnedMappedMutexGuard`] for a component of the locked data. |
| 1141 | `mutex`  | `OwnedMutexGuard<T>` | Public API | Other / internal logic | Returns a reference to the original `Arc<Mutex>`. |
| 1147 | `drop`  | `Drop for OwnedMutexGuard<T>` | Trait impl | Drop / cleanup |  |
| 1162 | `deref`  | `Deref for OwnedMutexGuard<T>` | Trait impl | Deref |  |
| 1168 | `deref_mut`  | `DerefMut for OwnedMutexGuard<T>` | Trait impl | Deref |  |
| 1174 | `fmt`  | `fmt::Debug for OwnedMutexGuard<T>` | Trait impl | Formatting |  |
| 1180 | `fmt`  | `fmt::Display for OwnedMutexGuard<T>` | Trait impl | Formatting |  |
| 1188 | `skip_drop`  | `MappedMutexGuard<'a, T>` | Private helper | Combinator / iteration |  |
| 1207 | `map`  | `MappedMutexGuard<'a, T>` | Public API | Combinator / iteration | Makes a new [`MappedMutexGuard`] for a component of the locked data. |
| 1232 | `try_map`  | `MappedMutexGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`MappedMutexGuard`] for a component of the locked data. |
| 1252 | `drop`  | `Drop for MappedMutexGuard<'a, T>` | Trait impl | Drop / cleanup |  |
| 1267 | `deref`  | `Deref for MappedMutexGuard<'a, T>` | Trait impl | Deref |  |
| 1273 | `deref_mut`  | `DerefMut for MappedMutexGuard<'a, T>` | Trait impl | Deref |  |
| 1279 | `fmt`  | `fmt::Debug for MappedMutexGuard<'a, T>` | Trait impl | Formatting |  |
| 1285 | `fmt`  | `fmt::Display for MappedMutexGuard<'a, T>` | Trait impl | Formatting |  |
| 1293 | `skip_drop`  | `OwnedMappedMutexGuard<T, U>` | Private helper | Combinator / iteration |  |
| 1316 | `map`  | `OwnedMappedMutexGuard<T, U>` | Public API | Combinator / iteration | Makes a new [`OwnedMappedMutexGuard`] for a component of the locked data. |
| 1341 | `try_map`  | `OwnedMappedMutexGuard<T, U>` | Public API | Non-blocking attempt | Attempts to make a new [`OwnedMappedMutexGuard`] for a component of the locked data. |
| 1360 | `drop`  | `Drop for OwnedMappedMutexGuard<T, U>` | Trait impl | Drop / cleanup |  |
| 1375 | `deref`  | `Deref for OwnedMappedMutexGuard<T, U>` | Trait impl | Deref |  |
| 1381 | `deref_mut`  | `DerefMut for OwnedMappedMutexGuard<T, U>` | Trait impl | Deref |  |
| 1387 | `fmt`  | `fmt::Debug for OwnedMappedMutexGuard<T, U>` | Trait impl | Formatting |  |
| 1393 | `fmt`  | `fmt::Display for OwnedMappedMutexGuard<T, U>` | Trait impl | Formatting |  |

## `tokio/src/sync/notify.rs` (43)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 237 | `new`  | `Waiter` | Private helper | Constructor |  |
| 249 | `addr_of_pointers` ⚠ | `Waiter` | Private helper | Handle / reference plumbing |  |
| 274 | `none`  | `AtomicNotification` | Private helper | Other / internal logic |  |
| 280 | `store_release`  | `AtomicNotification` | Private helper | Other / internal logic | Store-release a notification. |
| 289 | `load`  | `AtomicNotification` | Private helper | Other / internal logic |  |
| 304 | `clear`  | `AtomicNotification` | Private helper | Configuration / setter | Clears the notification. |
| 333 | `new`  | `NotifyWaitersList<'a>` | Private helper | Constructor |  |
| 349 | `pop_back_locked`  | `NotifyWaitersList<'a>` | Private helper | Data movement | Removes the last element from the guarded list. |
| 361 | `drop`  | `Drop for NotifyWaitersList<'_>` | Trait impl | Drop / cleanup |  |
| 450 | `set_state`  |  | Private helper | State transition |  |
| 454 | `get_state`  |  | Private helper | Accessor / query |  |
| 458 | `get_num_notify_waiters_calls`  |  | Private helper | Accessor / query |  |
| 462 | `inc_num_notify_waiters_calls`  |  | Private helper | Metrics / counters |  |
| 466 | `atomic_inc_num_notify_waiters_calls`  |  | Private helper | Other / internal logic |  |
| 480 | `new`  | `Notify` | Public API | Constructor | Create a new `Notify`, initialized without a permit. |
| 505 | `const_new` 🅲 | `Notify` | Public API | Constructor | Create a new `Notify`, initialized without a permit. |
| 562 | `notified`  | `Notify` | Public API | Other / internal logic | Wait for a notification. |
| 610 | `notified_owned`  | `Notify` | Public API | Other / internal logic | Wait for a notification with an owned `Future`. |
| 657 | `notify_one`  | `Notify` | Public API | Wake / park |  |
| 670 | `notify_last`  | `Notify` | Public API | Wake / park | Notifies the last waiting task. |
| 674 | `notify_with_strategy`  | `Notify` | Private helper | Wake / park |  |
| 740 | `notify_waiters`  | `Notify` | Public API | Wake / park | Notifies all waiting tasks. |
| 744 | `inner_notify_waiters`  | `Notify` | Private helper | Other / internal logic |  |
| 817 | `lock_waiter_list`  | `Notify` | Crate-internal | Locking / permits |  |
| 833 | `default`  | `Default for Notify` | Trait impl | Constructor |  |
| 841 | `notify_locked`  |  | Private helper | Wake / park |  |
| 1003 | `enable`  | `Notified<'_>` | Public API | Configuration / setter | Adds this future to the list of futures that are ready to receive wakeups from calls to [`notify_one`]. |
| 1007 | `project`  | `Notified<'_>` | Private helper | Combinator / iteration |  |
| 1025 | `poll_notified`  | `Notified<'_>` | Private helper | Poll function |  |
| 1033 | `poll`  | `Future for Notified<'_>` | Trait impl | Future impl (poll) |  |
| 1039 | `drop`  | `Drop for Notified<'_>` | Trait impl | Drop / cleanup |  |
| 1056 | `enable`  | `OwnedNotified` | Public API | Configuration / setter | Adds this future to the list of futures that are ready to receive wakeups from calls to [`notify_one`]. |
| 1062 | `project`  | `OwnedNotified` | Private helper | Combinator / iteration | A custom `project` implementation is used in place of `pin-project-lite` as a custom drop implementation is needed. |
| 1080 | `poll_notified`  | `OwnedNotified` | Private helper | Poll function |  |
| 1088 | `poll`  | `Future for OwnedNotified` | Trait impl | Future impl (poll) |  |
| 1094 | `drop`  | `Drop for OwnedNotified` | Trait impl | Drop / cleanup |  |
| 1105 | `poll_notified`  | `NotifiedProject<'_>` | Private helper | Poll function |  |
| 1329 | `drop_notified`  | `NotifiedProject<'_>` | Private helper | Lifecycle / ref-count |  |
| 1382 | `as_raw`  | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1386 | `from_raw` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1390 | `pointers` ⚠ | `linked_list::Link for Waiter` | Trait impl | Intrusive-list link |  |
| 1395 | `is_unpin`  |  | Private helper | Accessor / query |  |
| 1408 | `notify_waiters`  | `NotifyGuard<'_>` | Crate-internal | Wake / park |  |

## `tokio/src/sync/once_cell.rs` (25)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 77 | `default`  | `Default for OnceCell<T>` | Trait impl | Constructor |  |
| 83 | `fmt`  | `fmt::Debug for OnceCell<T>` | Trait impl | Formatting |  |
| 91 | `clone`  | `Clone for OnceCell<T>` | Trait impl | Clone |  |
| 97 | `eq`  | `PartialEq for OnceCell<T>` | Trait impl | Comparison |  |
| 105 | `drop`  | `Drop for OnceCell<T>` | Trait impl | Drop / cleanup |  |
| 116 | `from`  | `From<T> for OnceCell<T>` | Trait impl | Conversion |  |
| 127 | `new`  | `OnceCell<T>` | Public API | Constructor | Creates a new empty `OnceCell` instance. |
| 168 | `const_new` 🅲 | `OnceCell<T>` | Public API | Constructor | Creates a new empty `OnceCell` instance. |
| 185 | `new_with`  | `OnceCell<T>` | Public API | Constructor |  |
| 223 | `const_new_with` 🅲 | `OnceCell<T>` | Public API | Constructor | Creates a new `OnceCell` that contains the provided value. |
| 233 | `initialized`  | `OnceCell<T>` | Public API | Other / internal logic | Returns `true` if the `OnceCell` currently contains a value, and `false` otherwise. |
| 241 | `initialized_mut`  | `OnceCell<T>` | Private helper | Other / internal logic | Returns `true` if the `OnceCell` currently contains a value, and `false` otherwise. |
| 246 | `get_unchecked` ⚠ | `OnceCell<T>` | Private helper | Accessor / query |  |
| 251 | `get_unchecked_mut` ⚠ | `OnceCell<T>` | Private helper | Accessor / query |  |
| 259 | `set_value`  | `OnceCell<T>` | Private helper | Configuration / setter |  |
| 277 | `get`  | `OnceCell<T>` | Public API | Accessor / query | Returns a reference to the value currently stored in the `OnceCell`, or `None` if the `OnceCell` is empty. |
| 291 | `get_mut`  | `OnceCell<T>` | Public API | Accessor / query | Returns a mutable reference to the value currently stored in the `OnceCell`, or `None` if the `OnceCell` is empty. |
| 310 | `set`  | `OnceCell<T>` | Public API | Configuration / setter | Sets the value of the `OnceCell` to the given value if the `OnceCell` is empty. |
| 350 | `get_or_init` 🅰 | `OnceCell<T>` | Public API | Accessor / query | Gets the value currently in the `OnceCell`, or initialize it with the given asynchronous operation. |
| 400 | `get_or_try_init` 🅰 | `OnceCell<T>` | Public API | Accessor / query | Gets the value currently in the `OnceCell`, or initialize it with the given asynchronous operation. |
| 442 | `into_inner`  | `OnceCell<T>` | Public API | Conversion | Takes the value from the cell, destroying the cell in the process. |
| 454 | `take`  | `OnceCell<T>` | Public API | Data movement | Takes ownership of the current value, leaving the cell empty. |
| 486 | `fmt`  | `fmt::Display for SetError<T>` | Trait impl | Formatting |  |
| 498 | `is_already_init_err`  | `SetError<T>` | Public API | Accessor / query | Whether `SetError` is `SetError::AlreadyInitializedError`. |
| 506 | `is_initializing_err`  | `SetError<T>` | Public API | Accessor / query | Whether `SetError` is `SetError::InitializingError` |

## `tokio/src/sync/oneshot.rs` (41)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 363 | `fmt`  | `fmt::Display for RecvError` | Trait impl | Formatting |  |
| 373 | `fmt`  | `fmt::Display for TryRecvError` | Trait impl | Formatting |  |
| 418 | `will_wake` ⚠ | `Task` | Private helper | Other / internal logic | # Safety The caller must do the necessary synchronization to ensure that the [`Self::0`] contains the valid [`Waker`] during the call. |
| 426 | `with_task` ⚠ | `Task` | Private helper | Constructor | # Safety The caller must do the necessary synchronization to ensure that the [`Self::0`] contains the valid [`Waker`] during the call. |
| 440 | `drop_task` ⚠ | `Task` | Private helper | Lifecycle / ref-count | # Safety The caller must do the necessary synchronization to ensure that the [`Self::0`] contains the valid [`Waker`] during the call. |
| 453 | `set_task` ⚠ | `Task` | Private helper | Configuration / setter | # Safety The caller must do the necessary synchronization to ensure that the [`Self::0`] contains the valid [`Waker`] during the call. |
| 497 | `channel`  |  | Public API | Constructor | Creates a new one-shot channel for sending single values across asynchronous tasks. |
| 622 | `send`  | `Sender<T>` | Public API | Data movement | Attempts to send a value on this channel, returning it back if it could not be sent. |
| 727 | `closed` 🅰 | `Sender<T>` | Public API | Data movement | Waits for the associated [`Receiver`] handle to close. |
| 773 | `is_closed`  | `Sender<T>` | Public API | Accessor / query | Returns `true` if the associated [`Receiver`] handle has been dropped. |
| 820 | `poll_closed`  | `Sender<T>` | Public API | Poll function | Checks whether the `oneshot` channel has been closed, and if not, schedules the `Waker` in the provided `Context` to receive a notification when the channel is closed. |
| 872 | `drop`  | `Drop for Sender<T>` | Trait impl | Drop / cleanup |  |
| 947 | `close`  | `Receiver<T>` | Public API | Data movement | Prevents the associated [`Sender`] handle from sending a value. |
| 1015 | `is_terminated`  | `Receiver<T>` | Public API | Accessor / query | Checks if this receiver is terminated. |
| 1082 | `is_empty`  | `Receiver<T>` | Public API | Accessor / query | Checks if a channel is empty. |
| 1171 | `try_recv`  | `Receiver<T>` | Public API | Non-blocking attempt | Attempts to receive a value. |
| 1240 | `blocking_recv`  | `Receiver<T>` | Public API | Blocking (sync) variant | Blocking receive to call outside of asynchronous contexts. |
| 1246 | `drop`  | `Drop for Receiver<T>` | Trait impl | Drop / cleanup |  |
| 1271 | `poll`  | `Future for Receiver<T>` | Trait impl | Future impl (poll) |  |
| 1300 | `complete`  | `Inner<T>` | Private helper | Runtime/task control |  |
| 1317 | `poll_recv`  | `Inner<T>` | Private helper | Poll function |  |
| 1387 | `close`  | `Inner<T>` | Private helper | Data movement | Called by `Receiver` to indicate that the value will never be received. |
| 1421 | `consume_value` ⚠ | `Inner<T>` | Private helper | I/O operation | Consumes the value. |
| 1434 | `has_value` ⚠ | `Inner<T>` | Private helper | Accessor / query | Returns true if there is a value. |
| 1442 | `mut_load`  |  | Private helper | Other / internal logic |  |
| 1447 | `drop`  | `Drop for Inner<T>` | Trait impl | Drop / cleanup |  |
| 1474 | `fmt`  | `fmt::Debug for Inner<T>` | Trait impl | Formatting |  |
| 1508 | `new`  | `State` | Private helper | Constructor |  |
| 1512 | `is_complete`  | `State` | Private helper | Accessor / query |  |
| 1516 | `set_complete`  | `State` | Private helper | Configuration / setter |  |
| 1551 | `is_rx_task_set`  | `State` | Private helper | Accessor / query |  |
| 1555 | `set_rx_task`  | `State` | Private helper | Configuration / setter |  |
| 1560 | `unset_rx_task`  | `State` | Private helper | Configuration / setter |  |
| 1565 | `is_closed`  | `State` | Private helper | Accessor / query |  |
| 1569 | `set_closed`  | `State` | Private helper | Configuration / setter |  |
| 1576 | `set_tx_task`  | `State` | Private helper | Configuration / setter |  |
| 1581 | `unset_tx_task`  | `State` | Private helper | Configuration / setter |  |
| 1586 | `is_tx_task_set`  | `State` | Private helper | Accessor / query |  |
| 1590 | `as_usize`  | `State` | Private helper | Conversion |  |
| 1594 | `load`  | `State` | Private helper | Other / internal logic |  |
| 1601 | `fmt`  | `fmt::Debug for State` | Trait impl | Formatting |  |

## `tokio/src/sync/rwlock.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 103 | `bounds`  |  | Private helper | Other / internal logic |  |
| 104 | `check_send`  |  | Private helper | Runtime/task control |  |
| 105 | `check_sync`  |  | Private helper | Runtime/task control |  |
| 106 | `check_unpin`  |  | Private helper | Runtime/task control |  |
| 108 | `check_send_sync_val`  |  | Private helper | Runtime/task control |  |
| 203 | `new`  | `RwLock<T>` | Public API | Constructor | Creates a new instance of an `RwLock<T>` which is unlocked. |
| 270 | `with_max_readers`  | `RwLock<T>` | Public API | Constructor | Creates a new instance of an `RwLock<T>` which is unlocked and allows a maximum of `max_reads` concurrent readers. |
| 347 | `const_new` 🅲 | `RwLock<T>` | Public API | Constructor | Creates a new instance of an `RwLock<T>` which is unlocked. |
| 375 | `const_with_max_readers` 🅲 | `RwLock<T>` | Public API | Other / internal logic | Creates a new instance of an `RwLock<T>` which is unlocked and allows a maximum of `max_reads` concurrent readers. |
| 436 | `read` 🅰 | `RwLock<T>` | Public API | I/O operation | Locks this `RwLock` with shared read access, causing the current task to yield until the lock has been acquired. |
| 529 | `blocking_read`  | `RwLock<T>` | Public API | Blocking (sync) variant | Blockingly locks this `RwLock` with shared read access. |
| 584 | `read_owned` 🅰 | `RwLock<T>` | Public API | I/O operation | Locks this `RwLock` with shared read access, causing the current task to yield until the lock has been acquired. |
| 660 | `try_read`  | `RwLock<T>` | Public API | Non-blocking attempt | Attempts to acquire this `RwLock` with shared read access. |
| 725 | `try_read_owned`  | `RwLock<T>` | Public API | Non-blocking attempt | Attempts to acquire this `RwLock` with shared read access. |
| 780 | `write` 🅰 | `RwLock<T>` | Public API | I/O operation | Locks this `RwLock` with exclusive write access, causing the current task to yield until the lock has been acquired. |
| 877 | `blocking_write`  | `RwLock<T>` | Public API | Blocking (sync) variant | Blockingly locks this `RwLock` with exclusive write access. |
| 916 | `write_owned` 🅰 | `RwLock<T>` | Public API | I/O operation | Locks this `RwLock` with exclusive write access, causing the current task to yield until the lock has been acquired. |
| 985 | `try_write`  | `RwLock<T>` | Public API | Non-blocking attempt | Attempts to acquire this `RwLock` with exclusive write access. |
| 1044 | `try_write_owned`  | `RwLock<T>` | Public API | Non-blocking attempt | Attempts to acquire this `RwLock` with exclusive write access. |
| 1090 | `get_mut`  | `RwLock<T>` | Public API | Accessor / query | Returns a mutable reference to the underlying data. |
| 1095 | `into_inner`  | `RwLock<T>` | Public API | Conversion | Consumes the lock, returning the underlying data. |
| 1104 | `from`  | `From<T> for RwLock<T>` | Trait impl | Conversion |  |
| 1113 | `default`  | `Default for RwLock<T>` | Trait impl | Constructor |  |
| 1122 | `fmt`  | `std::fmt::Debug for RwLock<T>` | Trait impl | Formatting |  |

## `tokio/src/sync/semaphore.rs` (37)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 462 | `bounds`  |  | Private helper | Other / internal logic |  |
| 463 | `check_unpin`  |  | Private helper | Runtime/task control |  |
| 465 | `check_send_sync_val`  |  | Private helper | Runtime/task control |  |
| 466 | `check_send_sync`  |  | Private helper | Runtime/task control |  |
| 485 | `new`  | `Semaphore` | Public API | Constructor | Creates a new semaphore with the initial number of permits. |
| 533 | `const_new` 🅲 | `Semaphore` | Public API | Constructor | Creates a new semaphore with the initial number of permits. |
| 542 | `new_closed`  | `Semaphore` | Crate-internal | Constructor | Creates a new closed semaphore with 0 permits. |
| 552 | `const_new_closed` 🅲 | `Semaphore` | Crate-internal | Constructor | Creates a new closed semaphore with 0 permits. |
| 561 | `available_permits`  | `Semaphore` | Public API | Other / internal logic | Returns the current number of available permits. |
| 568 | `add_permits`  | `Semaphore` | Public API | Locking / permits | Adds `n` new permits to the semaphore. |
| 576 | `forget_permits`  | `Semaphore` | Public API | Locking / permits | Decrease a semaphore's permits by a maximum of `n`. |
| 614 | `acquire` 🅰 | `Semaphore` | Public API | Locking / permits | Acquires a permit from the semaphore. |
| 661 | `acquire_many` 🅰 | `Semaphore` | Public API | Locking / permits | Acquires `n` permits from the semaphore. |
| 709 | `try_acquire`  | `Semaphore` | Public API | Non-blocking attempt | Tries to acquire a permit from the semaphore. |
| 744 | `try_acquire_many`  | `Semaphore` | Public API | Non-blocking attempt | Tries to acquire `n` permits from the semaphore. |
| 802 | `blocking_acquire`  | `Semaphore` | Public API | Blocking (sync) variant | Acquires a permit from the semaphore, blocking the current thread until one is available. |
| 838 | `blocking_acquire_many`  | `Semaphore` | Public API | Blocking (sync) variant | Acquires `n` permits from the semaphore, blocking the current thread until they are available. |
| 884 | `acquire_owned` 🅰 | `Semaphore` | Public API | Locking / permits | Acquires a permit from the semaphore. |
| 945 | `acquire_many_owned` 🅰 | `Semaphore` | Public API | Locking / permits | Acquires `n` permits from the semaphore. |
| 999 | `try_acquire_owned`  | `Semaphore` | Public API | Non-blocking attempt | Tries to acquire a permit from the semaphore. |
| 1038 | `try_acquire_many_owned`  | `Semaphore` | Public API | Non-blocking attempt | Tries to acquire `n` permits from the semaphore. |
| 1086 | `blocking_acquire_owned`  | `Semaphore` | Public API | Blocking (sync) variant | Acquires a permit from the semaphore, blocking the current thread until one is available. |
| 1125 | `blocking_acquire_many_owned`  | `Semaphore` | Public API | Blocking (sync) variant | Acquires `n` permits from the semaphore, blocking the current thread until they are available. |
| 1161 | `close`  | `Semaphore` | Public API | Data movement | Closes the semaphore. |
| 1166 | `is_closed`  | `Semaphore` | Public API | Accessor / query | Returns true if the semaphore is closed |
| 1193 | `forget`  | `SemaphorePermit<'a>` | Public API | Locking / permits | Forgets the permit **without** releasing it back to the semaphore. |
| 1230 | `merge`  | `SemaphorePermit<'a>` | Public API | Combinator / iteration | Merge two [`SemaphorePermit`] instances together, consuming `other` without releasing the permits it holds. |
| 1260 | `split`  | `SemaphorePermit<'a>` | Public API | Combinator / iteration | Splits `n` permits from `self` and returns a new [`SemaphorePermit`] instance that holds `n` permits. |
| 1274 | `semaphore`  | `SemaphorePermit<'a>` | Public API | Handle / reference plumbing | Returns the [`Semaphore`] from which this permit was acquired. |
| 1279 | `num_permits`  | `SemaphorePermit<'a>` | Public API | Accessor / query | Returns the number of permits held by `self`. |
| 1306 | `forget`  | `OwnedSemaphorePermit` | Public API | Locking / permits | Forgets the permit **without** releasing it back to the semaphore. |
| 1343 | `merge`  | `OwnedSemaphorePermit` | Public API | Combinator / iteration | Merge two [`OwnedSemaphorePermit`] instances together, consuming `other` without releasing the permits it holds. |
| 1377 | `split`  | `OwnedSemaphorePermit` | Public API | Combinator / iteration | Splits `n` permits from `self` and returns a new [`OwnedSemaphorePermit`] instance that holds `n` permits. |
| 1391 | `semaphore`  | `OwnedSemaphorePermit` | Public API | Handle / reference plumbing | Returns the [`Semaphore`] from which this permit was acquired. |
| 1396 | `num_permits`  | `OwnedSemaphorePermit` | Public API | Accessor / query | Returns the number of permits held by `self`. |
| 1402 | `drop`  | `Drop for SemaphorePermit<'_>` | Trait impl | Drop / cleanup |  |
| 1408 | `drop`  | `Drop for OwnedSemaphorePermit` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/set_once.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 98 | `default`  | `Default for SetOnce<T>` | Trait impl | Constructor |  |
| 104 | `fmt`  | `fmt::Debug for SetOnce<T>` | Trait impl | Formatting |  |
| 112 | `clone`  | `Clone for SetOnce<T>` | Trait impl | Clone |  |
| 118 | `eq`  | `PartialEq for SetOnce<T>` | Trait impl | Comparison |  |
| 126 | `drop`  | `Drop for SetOnce<T>` | Trait impl | Drop / cleanup |  |
| 137 | `from`  | `From<T> for SetOnce<T>` | Trait impl | Conversion |  |
| 148 | `new`  | `SetOnce<T>` | Public API | Constructor | Creates a new empty `SetOnce` instance. |
| 190 | `const_new` 🅲 | `SetOnce<T>` | Public API | Constructor | Creates a new empty `SetOnce` instance. |
| 203 | `new_with`  | `SetOnce<T>` | Public API | Constructor | Creates a new `SetOnce` that contains the provided value, if any. |
| 240 | `const_new_with` 🅲 | `SetOnce<T>` | Public API | Constructor | Creates a new `SetOnce` that contains the provided value. |
| 250 | `initialized`  | `SetOnce<T>` | Public API | Other / internal logic | Returns `true` if the `SetOnce` currently contains a value, and `false` otherwise. |
| 257 | `get_unchecked` ⚠ | `SetOnce<T>` | Private helper | Accessor / query |  |
| 263 | `get`  | `SetOnce<T>` | Public API | Accessor / query | Returns a reference to the value currently stored in the `SetOnce`, or `None` if the `SetOnce` is empty. |
| 280 | `set`  | `SetOnce<T>` | Public API | Configuration / setter | Sets the value of the `SetOnce` to the given value if the `SetOnce` is empty. |
| 311 | `into_inner`  | `SetOnce<T>` | Public API | Conversion | Takes the value from the cell, destroying the cell in the process. |
| 339 | `wait` 🅰 | `SetOnce<T>` | Public API | Runtime/task control | Waits until the value is set. |
| 383 | `fmt`  | `fmt::Display for SetOnceError<T>` | Trait impl | Formatting |  |

## `tokio/src/sync/watch.rs` (51)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 202 | `clone`  | `Clone for Sender<T>` | Trait impl | Clone |  |
| 212 | `default`  | `Default for Sender<T>` | Trait impl | Constructor |  |
| 291 | `has_changed`  | `Ref<'a, T>` | Public API | Accessor / query | Indicates if the borrowed value is considered as _changed_ since the last time it has been marked as seen. |
| 320 | `fmt`  | `fmt::Debug for Shared<T>` | Trait impl | Formatting |  |
| 344 | `fmt`  | `fmt::Debug for SendError<T>` | Trait impl | Formatting |  |
| 350 | `fmt`  | `fmt::Display for SendError<T>` | Trait impl | Formatting |  |
| 364 | `fmt`  | `fmt::Display for RecvError` | Trait impl | Formatting |  |
| 394 | `new`  | `BigNotify` | Crate-internal | Constructor |  |
| 406 | `notify_waiters`  | `BigNotify` | Crate-internal | Wake / park |  |
| 414 | `notified`  | `BigNotify` | Crate-internal | Other / internal logic | This function implements the case where randomness is not available. |
| 421 | `notified`  | `BigNotify` | Crate-internal | Other / internal logic | This function implements the case where randomness is available. |
| 461 | `decrement`  | `Version` | Crate-internal | Other / internal logic | Decrements the version. |
| 473 | `version`  | `StateSnapshot` | Crate-internal | Other / internal logic | Extract the version from the state. |
| 478 | `is_closed`  | `StateSnapshot` | Crate-internal | Accessor / query | Is the closed bit set? |
| 486 | `new`  | `AtomicState` | Crate-internal | Constructor | Create a new `AtomicState` that is not closed and which has the version set to `Version::INITIAL`. |
| 498 | `load`  | `AtomicState` | Crate-internal | Other / internal logic | Load the current value of the state. |
| 503 | `increment_version_while_locked`  | `AtomicState` | Crate-internal | Other / internal logic | Increment the version counter. |
| 512 | `set_closed`  | `AtomicState` | Crate-internal | Configuration / setter | Set the closed bit in the state. |
| 554 | `channel`  |  | Public API | Constructor | Creates a new watch channel, returning the "send" and "receive" handles. |
| 577 | `from_shared`  | `Receiver<T>` | Private helper | Conversion |  |
| 629 | `borrow`  | `Receiver<T>` | Public API | Combinator / iteration | Returns a reference to the most recently sent value. |
| 676 | `borrow_and_update`  | `Receiver<T>` | Public API | Combinator / iteration | Returns a reference to the most recently sent value and marks that value as seen. |
| 738 | `has_changed`  | `Receiver<T>` | Public API | Accessor / query | Checks if this channel contains a message that this receiver has not yet seen. |
| 764 | `is_closed`  | `Receiver<T>` | Public API | Accessor / query | Checks if the channel has been closed. |
| 776 | `mark_changed`  | `Receiver<T>` | Public API | Other / internal logic | Marks the state as changed. |
| 786 | `mark_unchanged`  | `Receiver<T>` | Public API | Other / internal logic | Marks the state as unchanged. |
| 836 | `changed` 🅰 | `Receiver<T>` | Public API | Async operation | Waits for a change notification, then marks the current value as seen. |
| 907 | `wait_for` 🅰 | `Receiver<T>` | Public API | Runtime/task control | Waits for a value that satisfies the provided condition. |
| 914 | `wait_for_inner` 🅰 | `Receiver<T>` | Private helper | Runtime/task control |  |
| 968 | `same_channel`  | `Receiver<T>` | Public API | Handle / reference plumbing | Returns `true` if receivers belong to the same channel. |
| 973 | `try_has_changed`  | `Receiver<T>` | Crate-internal | Non-blocking attempt |  |
| 979 | `maybe_changed`  |  | Private helper | Other / internal logic |  |
| 1001 | `changed_impl` 🅰 |  | Private helper | Async operation |  |
| 1023 | `clone`  | `Clone for Receiver<T>` | Trait impl | Clone |  |
| 1032 | `drop`  | `Drop for Receiver<T>` | Trait impl | Drop / cleanup |  |
| 1059 | `new`  | `Sender<T>` | Public API | Constructor | Creates the sending-half of the [`watch`] channel. |
| 1082 | `send`  | `Sender<T>` | Public API | Data movement | Sends a new value via the channel, notifying all receivers. |
| 1122 | `send_modify`  | `Sender<T>` | Public API | Data movement | Modifies the watched value **unconditionally** in-place, notifying all receivers. |
| 1189 | `send_if_modified`  | `Sender<T>` | Public API | Data movement | Modifies the watched value **conditionally** in-place, notifying all receivers only if modified. |
| 1247 | `send_replace`  | `Sender<T>` | Public API | Data movement | Sends a new value via the channel, notifying all receivers and returning the previous value in the channel. |
| 1271 | `borrow`  | `Sender<T>` | Public API | Combinator / iteration | Returns a reference to the most recently sent value Outstanding borrows hold a read lock on the inner value. |
| 1292 | `is_closed`  | `Sender<T>` | Public API | Accessor / query | Checks if the channel has been closed. |
| 1331 | `closed` 🅰 | `Sender<T>` | Public API | Data movement | Completes when all receivers have dropped. |
| 1405 | `subscribe`  | `Sender<T>` | Public API | Data movement | Creates a new [`Receiver`] connected to this `Sender`. |
| 1432 | `receiver_count`  | `Sender<T>` | Public API | Data movement | Returns the number of receivers that currently exist. |
| 1455 | `sender_count`  | `Sender<T>` | Public API | Data movement | Returns the number of senders that currently exist. |
| 1471 | `same_channel`  | `Sender<T>` | Public API | Handle / reference plumbing | Returns `true` if senders belong to the same channel. |
| 1477 | `drop`  | `Drop for Sender<T>` | Trait impl | Drop / cleanup |  |
| 1490 | `deref`  | `ops::Deref for Ref<'_, T>` | Trait impl | Deref |  |
| 1502 | `watch_spurious_wakeup`  |  | Test | Other / internal logic |  |
| 1536 | `watch_borrow`  |  | Test | Other / internal logic |  |

