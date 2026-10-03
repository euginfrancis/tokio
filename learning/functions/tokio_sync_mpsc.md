# `tokio::sync::mpsc` — 196 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 68 |
| Crate-internal | 54 |
| Trait impl | 52 |
| Private helper | 16 |
| Trait method (declaration/default) | 5 |
| Test | 1 |

## `tokio/src/sync/mpsc/block.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 72 | `start_index`  |  | Crate-internal | Runtime/task control | Returns the index of the first slot in the block referenced by `slot_index`. |
| 78 | `offset`  |  | Crate-internal | Other / internal logic | Returns the offset into the block referenced by `slot_index`. |
| 84 | `addr_of_header` ⚠ | `Block<T>` | Private helper | Handle / reference plumbing |  |
| 88 | `addr_of_values` ⚠ | `Block<T>` | Private helper | Handle / reference plumbing |  |
| 95 | `new`  | `Block<T>` | Crate-internal | Constructor |  |
| 129 | `is_at_index`  | `Block<T>` | Crate-internal | Accessor / query | Returns `true` if the block matches the given index. |
| 138 | `distance`  | `Block<T>` | Crate-internal | Other / internal logic | Returns the number of blocks between `self` and the block at the specified index. |
| 152 | `read` ⚠ | `Block<T>` | Crate-internal | I/O operation | Reads the value at the given offset. |
| 180 | `has_value`  | `Block<T>` | Crate-internal | Accessor / query | Returns true if *this* block has a value in the given slot. |
| 201 | `write` ⚠ | `Block<T>` | Crate-internal | I/O operation | Writes a value to the block at the given offset. |
| 219 | `tx_close` ⚠ | `Block<T>` | Crate-internal | Other / internal logic | Signal to the receiver that the sender half of the list is closed. |
| 232 | `reclaim` ⚠ | `Block<T>` | Crate-internal | Other / internal logic | Resets the block to a blank state. |
| 248 | `tx_release` ⚠ | `Block<T>` | Crate-internal | Other / internal logic | Releases the block to the rx half for freeing. |
| 266 | `set_ready`  | `Block<T>` | Private helper | Configuration / setter | Mark a slot as ready |
| 275 | `is_final`  | `Block<T>` | Crate-internal | Accessor / query | Returns `true` when all slots have their `ready` bits set. |
| 280 | `observed_tail_position`  | `Block<T>` | Crate-internal | Other / internal logic | Returns the `observed_tail_position` value, if set |
| 293 | `load_next`  | `Block<T>` | Crate-internal | Other / internal logic | Loads the next block |
| 321 | `try_push` ⚠ | `Block<T>` | Crate-internal | Non-blocking attempt | Pushes `block` as the next block in the link. |
| 357 | `grow`  | `Block<T>` | Crate-internal | Other / internal logic | Grows the `Block` linked list by allocating and appending a new block. |
| 420 | `is_ready`  |  | Private helper | Accessor / query | Returns `true` if the specified slot has a value ready to be consumed. |
| 426 | `is_tx_closed`  |  | Private helper | Accessor / query | Returns `true` if the closed flag has been set. |
| 436 | `initialize` ⚠ | `Values<T>` | Private helper | Runtime/task control | Initialize a `Values` struct from a pointer. |
| 452 | `index`  | `ops::Index<usize> for Values<T>` | Trait impl | Other / internal logic |  |
| 459 | `assert_no_stack_overflow`  |  | Test | Debugging / tracing |  |

## `tokio/src/sync/mpsc/bounded.rs` (60)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 159 | `channel`  |  | Public API | Constructor | Creates a bounded mpsc channel for communicating between asynchronous tasks with backpressure. |
| 182 | `new`  | `Receiver<T>` | Crate-internal | Constructor |  |
| 243 | `recv` 🅰 | `Receiver<T>` | Public API | Data movement | Receives the next value for this receiver. |
| 319 | `recv_many` 🅰 | `Receiver<T>` | Public API | Data movement | Receives the next values for this receiver and extends `buffer`. |
| 364 | `try_recv`  | `Receiver<T>` | Public API | Non-blocking attempt | Tries to receive the next value for this receiver. |
| 424 | `blocking_recv`  | `Receiver<T>` | Public API | Blocking (sync) variant | Blocking receive to call outside of asynchronous contexts. |
| 434 | `blocking_recv_many`  | `Receiver<T>` | Public API | Blocking (sync) variant | Variant of [`Self::recv_many`] for blocking contexts. |
| 478 | `close`  | `Receiver<T>` | Public API | Data movement | Closes the receiving half of a channel without dropping it. |
| 504 | `is_closed`  | `Receiver<T>` | Public API | Accessor / query | Checks if a channel is closed. |
| 526 | `is_empty`  | `Receiver<T>` | Public API | Accessor / query | Checks if a channel is empty. |
| 545 | `len`  | `Receiver<T>` | Public API | Accessor / query | Returns the number of messages in the channel. |
| 591 | `capacity`  | `Receiver<T>` | Public API | Accessor / query | Returns the current capacity of the channel. |
| 625 | `max_capacity`  | `Receiver<T>` | Public API | Configuration / setter | Returns the maximum buffer capacity of the channel. |
| 650 | `poll_recv`  | `Receiver<T>` | Public API | Poll function | Polls to receive the next message on this channel. |
| 722 | `poll_recv_many`  | `Receiver<T>` | Public API | Poll function | Polls to receive multiple messages on this channel, extending the provided buffer. |
| 732 | `sender_strong_count`  | `Receiver<T>` | Public API | Data movement | Returns the number of [`Sender`] handles. |
| 737 | `sender_weak_count`  | `Receiver<T>` | Public API | Data movement | Returns the number of [`WeakSender`] handles. |
| 743 | `fmt`  | `fmt::Debug for Receiver<T>` | Trait impl | Formatting |  |
| 753 | `new`  | `Sender<T>` | Crate-internal | Constructor |  |
| 816 | `send` 🅰 | `Sender<T>` | Public API | Data movement | Sends a value, waiting until there is capacity. |
| 862 | `closed` 🅰 | `Sender<T>` | Public API | Data movement | Completes when the receiver has dropped. |
| 924 | `try_send`  | `Sender<T>` | Public API | Non-blocking attempt | Attempts to immediately send a message on this `Sender`. |
| 988 | `send_timeout` 🅰 | `Sender<T>` | Public API | Data movement | Sends a value, waiting until there is capacity, but only for a limited time. |
| 1046 | `blocking_send`  | `Sender<T>` | Public API | Blocking (sync) variant | Blocking send to call outside of asynchronous contexts. |
| 1068 | `is_closed`  | `Sender<T>` | Public API | Accessor / query | Checks if the channel has been closed. |
| 1116 | `reserve` 🅰 | `Sender<T>` | Public API | Async operation | Waits for channel capacity. |
| 1177 | `reserve_many` 🅰 | `Sender<T>` | Public API | Async operation | Waits for channel capacity. |
| 1265 | `reserve_owned` 🅰 | `Sender<T>` | Public API | Async operation | Waits for channel capacity, moving the `Sender` and returning an owned permit. |
| 1272 | `reserve_inner` 🅰 | `Sender<T>` | Private helper | Async operation |  |
| 1291 | `drop`  | `Drop for WakeReceiverOnDrop<'_, T>` | Trait impl | Drop / cleanup |  |
| 1356 | `try_reserve`  | `Sender<T>` | Public API | Non-blocking attempt | Tries to acquire a slot in the channel without waiting for the slot to become available. |
| 1434 | `try_reserve_many`  | `Sender<T>` | Public API | Non-blocking attempt | Tries to acquire `n` slots in the channel without waiting for the slot to become available. |
| 1506 | `try_reserve_owned`  | `Sender<T>` | Public API | Non-blocking attempt | Tries to acquire a slot in the channel without waiting for the slot to become available, returning an owned permit. |
| 1530 | `same_channel`  | `Sender<T>` | Public API | Handle / reference plumbing | Returns `true` if senders belong to the same channel. |
| 1567 | `capacity`  | `Sender<T>` | Public API | Accessor / query | Returns the current capacity of the channel. |
| 1576 | `downgrade`  | `Sender<T>` | Public API | Handle / reference plumbing | Converts the `Sender` to a [`WeakSender`] that does not count towards RAII semantics, i.e. |
| 1614 | `max_capacity`  | `Sender<T>` | Public API | Configuration / setter | Returns the maximum buffer capacity of the channel. |
| 1619 | `strong_count`  | `Sender<T>` | Public API | Metrics / counters | Returns the number of [`Sender`] handles. |
| 1624 | `weak_count`  | `Sender<T>` | Public API | Metrics / counters | Returns the number of [`WeakSender`] handles. |
| 1630 | `clone`  | `Clone for Sender<T>` | Trait impl | Clone |  |
| 1638 | `fmt`  | `fmt::Debug for Sender<T>` | Trait impl | Formatting |  |
| 1646 | `clone`  | `Clone for WeakSender<T>` | Trait impl | Clone |  |
| 1656 | `drop`  | `Drop for WeakSender<T>` | Trait impl | Drop / cleanup |  |
| 1665 | `upgrade`  | `WeakSender<T>` | Public API | Handle / reference plumbing | Tries to convert a `WeakSender` into a [`Sender`]. |
| 1670 | `strong_count`  | `WeakSender<T>` | Public API | Metrics / counters | Returns the number of [`Sender`] handles. |
| 1675 | `weak_count`  | `WeakSender<T>` | Public API | Metrics / counters | Returns the number of [`WeakSender`] handles. |
| 1681 | `fmt`  | `fmt::Debug for WeakSender<T>` | Trait impl | Formatting |  |
| 1721 | `send`  | `Permit<'_, T>` | Public API | Data movement | Sends a value using the reserved capacity. |
| 1732 | `drop`  | `Drop for Permit<'_, T>` | Trait impl | Drop / cleanup |  |
| 1749 | `fmt`  | `fmt::Debug for Permit<'_, T>` | Trait impl | Formatting |  |
| 1761 | `next`  | `Iterator for PermitIterator<'a, T>` | Trait impl | Iterator |  |
| 1770 | `size_hint`  | `Iterator for PermitIterator<'a, T>` | Trait impl | Iterator |  |
| 1779 | `drop`  | `Drop for PermitIterator<'_, T>` | Trait impl | Drop / cleanup |  |
| 1800 | `fmt`  | `fmt::Debug for PermitIterator<'_, T>` | Trait impl | Formatting |  |
| 1845 | `send`  | `OwnedPermit<T>` | Public API | Data movement | Sends a value using the reserved capacity. |
| 1884 | `release`  | `OwnedPermit<T>` | Public API | Locking / permits | Releases the reserved capacity *without* sending a message, returning the [`Sender`]. |
| 1915 | `same_channel`  | `OwnedPermit<T>` | Public API | Handle / reference plumbing | Returns `true` if permits belong to the same channel. |
| 1940 | `same_channel_as_sender`  | `OwnedPermit<T>` | Public API | Other / internal logic | Returns `true` if this permit belongs to the same channel as the given [`Sender`]. |
| 1948 | `drop`  | `Drop for OwnedPermit<T>` | Trait impl | Drop / cleanup |  |
| 1960 | `fmt`  | `fmt::Debug for OwnedPermit<T>` | Trait impl | Formatting |  |

## `tokio/src/sync/mpsc/chan.rs` (53)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `fmt`  | `fmt::Debug for Tx<T, S>` | Trait impl | Formatting |  |
| 35 | `fmt`  | `fmt::Debug for Rx<T, S>` | Trait impl | Formatting |  |
| 41 | `is_idle`  | `trait Semaphore` | Trait method (declaration/default) | Accessor / query |  |
| 43 | `add_permit`  | `trait Semaphore` | Trait method (declaration/default) | Other / internal logic |  |
| 45 | `add_permits`  | `trait Semaphore` | Trait method (declaration/default) | Locking / permits |  |
| 47 | `close`  | `trait Semaphore` | Trait method (declaration/default) | Data movement |  |
| 49 | `is_closed`  | `trait Semaphore` | Trait method (declaration/default) | Accessor / query |  |
| 81 | `fmt`  | `fmt::Debug for Chan<T, S>` | Trait impl | Formatting |  |
| 102 | `fmt`  | `fmt::Debug for RxFields<T>` | Trait impl | Formatting |  |
| 115 | `channel`  |  | Crate-internal | Constructor |  |
| 137 | `new`  | `Tx<T, S>` | Private helper | Constructor |  |
| 141 | `strong_count`  | `Tx<T, S>` | Crate-internal | Metrics / counters |  |
| 145 | `weak_count`  | `Tx<T, S>` | Crate-internal | Metrics / counters |  |
| 149 | `downgrade`  | `Tx<T, S>` | Crate-internal | Handle / reference plumbing |  |
| 156 | `upgrade`  | `Tx<T, S>` | Crate-internal | Handle / reference plumbing |  |
| 175 | `semaphore`  | `Tx<T, S>` | Crate-internal | Handle / reference plumbing |  |
| 180 | `send`  | `Tx<T, S>` | Crate-internal | Data movement | Send a message and notify the receiver. |
| 185 | `wake_rx`  | `Tx<T, S>` | Crate-internal | Wake / park | Wake the receive half |
| 190 | `same_channel`  | `Tx<T, S>` | Crate-internal | Handle / reference plumbing | Returns `true` if senders belong to the same channel. |
| 196 | `is_closed`  | `Tx<T, S>` | Crate-internal | Accessor / query |  |
| 200 | `closed` 🅰 | `Tx<T, S>` | Crate-internal | Data movement |  |
| 214 | `clone`  | `Clone for Tx<T, S>` | Trait impl | Clone |  |
| 226 | `drop`  | `Drop for Tx<T, S>` | Trait impl | Drop / cleanup |  |
| 242 | `new`  | `Rx<T, S>` | Private helper | Constructor |  |
| 246 | `close`  | `Rx<T, S>` | Crate-internal | Data movement |  |
| 261 | `is_closed`  | `Rx<T, S>` | Crate-internal | Accessor / query |  |
| 274 | `is_empty`  | `Rx<T, S>` | Crate-internal | Accessor / query |  |
| 281 | `len`  | `Rx<T, S>` | Crate-internal | Accessor / query |  |
| 289 | `recv`  | `Rx<T, S>` | Crate-internal | Data movement | Receive the next value |
| 344 | `recv_many`  | `Rx<T, S>` | Crate-internal | Data movement | Receives up to `limit` values into `buffer` For `limit > 0`, receives up to limit values into `buffer`. |
| 424 | `try_recv`  | `Rx<T, S>` | Crate-internal | Non-blocking attempt | Try to receive the next value. |
| 474 | `semaphore`  | `Rx<T, S>` | Crate-internal | Handle / reference plumbing |  |
| 478 | `sender_strong_count`  | `Rx<T, S>` | Crate-internal | Data movement |  |
| 482 | `sender_weak_count`  | `Rx<T, S>` | Crate-internal | Data movement |  |
| 488 | `drop`  | `Drop for Rx<T, S>` | Trait impl | Drop / cleanup |  |
| 502 | `drain`  | `Guard<'a, T, S>` | Private helper | Combinator / iteration |  |
| 511 | `drop`  | `Drop for Guard<'a, T, S>` | Trait impl | Drop / cleanup |  |
| 535 | `send`  | `Chan<T, S>` | Private helper | Data movement |  |
| 543 | `decrement_weak_count`  | `Chan<T, S>` | Crate-internal | Metrics / counters |  |
| 547 | `increment_weak_count`  | `Chan<T, S>` | Crate-internal | Metrics / counters |  |
| 551 | `strong_count`  | `Chan<T, S>` | Crate-internal | Metrics / counters |  |
| 555 | `weak_count`  | `Chan<T, S>` | Crate-internal | Metrics / counters |  |
| 561 | `drop`  | `Drop for Chan<T, S>` | Trait impl | Drop / cleanup |  |
| 578 | `add_permit`  | `Semaphore for bounded::Semaphore` | Trait impl | Other / internal logic |  |
| 582 | `add_permits`  | `Semaphore for bounded::Semaphore` | Trait impl | Locking / permits |  |
| 586 | `is_idle`  | `Semaphore for bounded::Semaphore` | Trait impl | Accessor / query |  |
| 590 | `close`  | `Semaphore for bounded::Semaphore` | Trait impl | Data movement |  |
| 594 | `is_closed`  | `Semaphore for bounded::Semaphore` | Trait impl | Accessor / query |  |
| 602 | `add_permit`  | `Semaphore for unbounded::Semaphore` | Trait impl | Other / internal logic |  |
| 611 | `add_permits`  | `Semaphore for unbounded::Semaphore` | Trait impl | Locking / permits |  |
| 620 | `is_idle`  | `Semaphore for unbounded::Semaphore` | Trait impl | Accessor / query |  |
| 624 | `close`  | `Semaphore for unbounded::Semaphore` | Trait impl | Data movement |  |
| 628 | `is_closed`  | `Semaphore for unbounded::Semaphore` | Trait impl | Accessor / query |  |

## `tokio/src/sync/mpsc/error.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `fmt`  | `fmt::Debug for SendError<T>` | Trait impl | Formatting |  |
| 17 | `fmt`  | `fmt::Display for SendError<T>` | Trait impl | Formatting |  |
| 40 | `into_inner`  | `TrySendError<T>` | Public API | Conversion | Consume the `TrySendError`, returning the unsent value. |
| 49 | `fmt`  | `fmt::Debug for TrySendError<T>` | Trait impl | Formatting |  |
| 58 | `fmt`  | `fmt::Display for TrySendError<T>` | Trait impl | Formatting |  |
| 73 | `from`  | `From<SendError<T>> for TrySendError<T>` | Trait impl | Conversion |  |
| 92 | `fmt`  | `fmt::Display for TryRecvError` | Trait impl | Formatting |  |
| 112 | `fmt`  | `fmt::Display for RecvError` | Trait impl | Formatting |  |
| 137 | `into_inner`  | `SendTimeoutError<T>` | Public API | Conversion | Consume the `SendTimeoutError`, returning the unsent value. |
| 146 | `fmt`  | `fmt::Debug for SendTimeoutError<T>` | Trait impl | Formatting |  |
| 155 | `fmt`  | `fmt::Display for SendTimeoutError<T>` | Trait impl | Formatting |  |

## `tokio/src/sync/mpsc/list.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 51 | `channel`  |  | Crate-internal | Constructor |  |
| 74 | `push`  | `Tx<T>` | Crate-internal | Data movement | Pushes a value into the list. |
| 92 | `close`  | `Tx<T>` | Crate-internal | Data movement | Closes the send half of the list. |
| 102 | `find_block`  | `Tx<T>` | Private helper | Other / internal logic |  |
| 194 | `reclaim_block` ⚠ | `Tx<T>` | Crate-internal | Other / internal logic | # Safety Behavior is undefined if any of the following conditions are violated: - The `block` was created by [`Box::into_raw`]. |
| 245 | `fmt`  | `fmt::Debug for Tx<T>` | Trait impl | Formatting |  |
| 254 | `is_empty`  | `Rx<T>` | Crate-internal | Accessor / query |  |
| 269 | `is_maybe_closed`  | `Rx<T>` | Private helper | Accessor / query |  |
| 298 | `len`  | `Rx<T>` | Crate-internal | Accessor / query |  |
| 320 | `pop`  | `Rx<T>` | Crate-internal | Data movement | Pops the next value off the queue. |
| 349 | `try_pop`  | `Rx<T>` | Crate-internal | Non-blocking attempt | Pops the next value off the queue, detecting whether the block is busy or empty on failure. |
| 364 | `try_advancing_head`  | `Rx<T>` | Private helper | Non-blocking attempt | Tries advancing the block pointer to the block referenced by `self.index`. |
| 391 | `reclaim_blocks`  | `Rx<T>` | Private helper | Other / internal logic |  |
| 429 | `free_blocks` ⚠ | `Rx<T>` | Crate-internal | Other / internal logic | Effectively `Drop` all the blocks. |
| 450 | `fmt`  | `fmt::Debug for Rx<T>` | Trait impl | Formatting |  |

## `tokio/src/sync/mpsc/unbounded.rs` (33)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 50 | `clone`  | `Clone for UnboundedSender<T>` | Trait impl | Clone |  |
| 58 | `fmt`  | `fmt::Debug for UnboundedSender<T>` | Trait impl | Formatting |  |
| 78 | `fmt`  | `fmt::Debug for UnboundedReceiver<T>` | Trait impl | Formatting |  |
| 95 | `unbounded_channel`  |  | Public API | Constructor | Creates an unbounded mpsc channel for communicating between asynchronous tasks without backpressure. |
| 109 | `new`  | `UnboundedReceiver<T>` | Crate-internal | Constructor |  |
| 167 | `recv` 🅰 | `UnboundedReceiver<T>` | Public API | Data movement | Receives the next value for this receiver. |
| 241 | `recv_many` 🅰 | `UnboundedReceiver<T>` | Public API | Data movement | Receives the next values for this receiver and extends `buffer`. |
| 286 | `try_recv`  | `UnboundedReceiver<T>` | Public API | Non-blocking attempt | Tries to receive the next value for this receiver. |
| 321 | `blocking_recv`  | `UnboundedReceiver<T>` | Public API | Blocking (sync) variant | Blocking receive to call outside of asynchronous contexts. |
| 331 | `blocking_recv_many`  | `UnboundedReceiver<T>` | Public API | Blocking (sync) variant | Variant of [`Self::recv_many`] for blocking contexts. |
| 342 | `close`  | `UnboundedReceiver<T>` | Public API | Data movement | Closes the receiving half of a channel, without dropping it. |
| 368 | `is_closed`  | `UnboundedReceiver<T>` | Public API | Accessor / query | Checks if a channel is closed. |
| 390 | `is_empty`  | `UnboundedReceiver<T>` | Public API | Accessor / query | Checks if a channel is empty. |
| 409 | `len`  | `UnboundedReceiver<T>` | Public API | Accessor / query | Returns the number of messages in the channel. |
| 434 | `poll_recv`  | `UnboundedReceiver<T>` | Public API | Poll function | Polls to receive the next message on this channel. |
| 509 | `poll_recv_many`  | `UnboundedReceiver<T>` | Public API | Poll function | Polls to receive multiple messages on this channel, extending the provided buffer. |
| 519 | `sender_strong_count`  | `UnboundedReceiver<T>` | Public API | Data movement | Returns the number of [`UnboundedSender`] handles. |
| 524 | `sender_weak_count`  | `UnboundedReceiver<T>` | Public API | Data movement | Returns the number of [`WeakUnboundedSender`] handles. |
| 530 | `new`  | `UnboundedSender<T>` | Crate-internal | Constructor |  |
| 547 | `send`  | `UnboundedSender<T>` | Public API | Data movement | Attempts to send a message on this `UnboundedSender` without blocking. |
| 556 | `inc_num_messages`  | `UnboundedSender<T>` | Private helper | Metrics / counters |  |
| 623 | `closed` 🅰 | `UnboundedSender<T>` | Public API | Data movement | Completes when the receiver has dropped. |
| 645 | `is_closed`  | `UnboundedSender<T>` | Public API | Accessor / query | Checks if the channel has been closed. |
| 661 | `same_channel`  | `UnboundedSender<T>` | Public API | Handle / reference plumbing | Returns `true` if senders belong to the same channel. |
| 670 | `downgrade`  | `UnboundedSender<T>` | Public API | Handle / reference plumbing | Converts the `UnboundedSender` to a [`WeakUnboundedSender`] that does not count towards RAII semantics, i.e. |
| 677 | `strong_count`  | `UnboundedSender<T>` | Public API | Metrics / counters | Returns the number of [`UnboundedSender`] handles. |
| 682 | `weak_count`  | `UnboundedSender<T>` | Public API | Metrics / counters | Returns the number of [`WeakUnboundedSender`] handles. |
| 688 | `clone`  | `Clone for WeakUnboundedSender<T>` | Trait impl | Clone |  |
| 698 | `drop`  | `Drop for WeakUnboundedSender<T>` | Trait impl | Drop / cleanup |  |
| 707 | `upgrade`  | `WeakUnboundedSender<T>` | Public API | Handle / reference plumbing | Tries to convert a `WeakUnboundedSender` into an [`UnboundedSender`]. |
| 712 | `strong_count`  | `WeakUnboundedSender<T>` | Public API | Metrics / counters | Returns the number of [`UnboundedSender`] handles. |
| 717 | `weak_count`  | `WeakUnboundedSender<T>` | Public API | Metrics / counters | Returns the number of [`WeakUnboundedSender`] handles. |
| 723 | `fmt`  | `fmt::Debug for WeakUnboundedSender<T>` | Trait impl | Formatting |  |

