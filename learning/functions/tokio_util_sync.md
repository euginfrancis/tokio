# `tokio-util::sync` — 70 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 31 |
| Trait impl | 25 |
| Private helper | 12 |
| Crate-internal | 2 |

## `tokio-util/src/sync/cancellation_token.rs` (26)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 107 | `fmt`  | `core::fmt::Debug for CancellationToken` | Trait impl | Formatting |  |
| 117 | `clone`  | `Clone for CancellationToken` | Trait impl | Clone | Creates a clone of the [`CancellationToken`] which will get cancelled whenever the current token gets cancelled, and vice versa. |
| 131 | `eq`  | `PartialEq for CancellationToken` | Trait impl | Comparison | Checks if two tokens are equal in terms of their cancellation operation. |
| 140 | `hash`  | `core::hash::Hash for CancellationToken` | Trait impl | Comparison |  |
| 146 | `drop`  | `Drop for CancellationToken` | Trait impl | Drop / cleanup |  |
| 152 | `default`  | `Default for CancellationToken` | Trait impl | Constructor |  |
| 159 | `new`  | `CancellationToken` | Public API | Constructor | Creates a new [`CancellationToken`] in the non-cancelled state. |
| 204 | `child_token`  | `CancellationToken` | Public API | Other / internal logic | Creates a [`CancellationToken`] which will get cancelled whenever the current token gets cancelled. |
| 220 | `cancel`  | `CancellationToken` | Public API | Lifecycle / ref-count | Cancel the [`CancellationToken`] and all child tokens which had been derived from it. |
| 225 | `is_cancelled`  | `CancellationToken` | Public API | Accessor / query | Returns `true` if the `CancellationToken` is cancelled. |
| 243 | `cancelled`  | `CancellationToken` | Public API | Lifecycle / ref-count | Returns a [`Future`] that gets fulfilled when cancellation is requested. |
| 267 | `cancelled_owned`  | `CancellationToken` | Public API | Lifecycle / ref-count | Returns a [`Future`] that gets fulfilled when cancellation is requested. |
| 275 | `drop_guard`  | `CancellationToken` | Public API | Lifecycle / ref-count | Creates a [`DropGuard`] for this token. |
| 283 | `drop_guard_ref`  | `CancellationToken` | Public API | Lifecycle / ref-count | Creates a [`DropGuardRef`] for this token. |
| 300 | `run_until_cancelled` 🅰 | `CancellationToken` | Public API | Runtime/task control | Runs a future to completion and returns its result wrapped inside of an `Option` unless the [`CancellationToken`] is cancelled. |
| 330 | `run_until_cancelled_owned` 🅰 | `CancellationToken` | Public API | Runtime/task control | Runs a future to completion and returns its result wrapped inside of an `Option` unless the [`CancellationToken`] is cancelled. |
| 341 | `fmt`  | `core::fmt::Debug for WaitForCancellationFuture<'a>` | Trait impl | Formatting |  |
| 349 | `poll`  | `Future for WaitForCancellationFuture<'a>` | Trait impl | Future impl (poll) |  |
| 372 | `fmt`  | `core::fmt::Debug for WaitForCancellationFutureOwned` | Trait impl | Formatting |  |
| 378 | `new`  | `WaitForCancellationFutureOwned` | Private helper | Constructor |  |
| 395 | `new_future` ⚠ | `WaitForCancellationFutureOwned` | Private helper | Constructor | # Safety The returned future must be destroyed before the cancellation token is destroyed. |
| 409 | `poll`  | `Future for WaitForCancellationFutureOwned` | Trait impl | Future impl (poll) |  |
| 449 | `new`  | `RunUntilCancelledFuture<'a, F>` | Crate-internal | Constructor |  |
| 460 | `poll`  | `Future for RunUntilCancelledFuture<'a, F>` | Trait impl | Future impl (poll) |  |
| 488 | `poll`  | `Future for RunUntilCancelledFutureOwned<F>` | Trait impl | Future impl (poll) |  |
| 501 | `new`  | `RunUntilCancelledFutureOwned<F>` | Crate-internal | Constructor |  |

## `tokio-util/src/sync/mpsc.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `into_inner`  | `PollSendError<T>` | Public API | Conversion | Consumes the stored value, if any. |
| 25 | `fmt`  | `fmt::Display for PollSendError<T>` | Trait impl | Formatting |  |
| 55 | `make_acquire_future` 🅰 |  | Private helper | Async operation |  |
| 75 | `empty`  | `PollSenderFuture<T>` | Private helper | Other / internal logic | Create with an empty inner future with no `Send` bound. |
| 84 | `new`  | `PollSenderFuture<T>` | Private helper | Constructor | Create with an empty inner future. |
| 91 | `poll`  | `PollSenderFuture<T>` | Private helper | Poll function | Poll the inner future. |
| 96 | `set`  | `PollSenderFuture<T>` | Private helper | Configuration / setter | Replace the inner future. |
| 112 | `new`  | `PollSender<T>` | Public API | Constructor | Creates a new `PollSender`. |
| 120 | `take_state`  | `PollSender<T>` | Private helper | Data movement |  |
| 137 | `poll_reserve`  | `PollSender<T>` | Public API | Poll function | Attempts to prepare the sender to receive a value. |
| 183 | `send_item`  | `PollSender<T>` | Public API | Data movement | Sends an item to the channel. |
| 206 | `is_closed`  | `PollSender<T>` | Public API | Accessor / query | Checks whether this sender is closed. |
| 214 | `get_ref`  | `PollSender<T>` | Public API | Accessor / query | Gets a reference to the `Sender` of the underlying channel. |
| 230 | `close`  | `PollSender<T>` | Public API | Data movement | Closes this sender. |
| 252 | `abort_send`  | `PollSender<T>` | Public API | Lifecycle / ref-count | Aborts the current in-progress send, if any. |
| 292 | `clone`  | `Clone for PollSender<T>` | Trait impl | Clone | Clones this `PollSender`. |
| 309 | `poll_ready`  | `Sink<T> for PollSender<T>` | Trait impl | Sink impl |  |
| 313 | `poll_flush`  | `Sink<T> for PollSender<T>` | Trait impl | Sink impl |  |
| 317 | `start_send`  | `Sink<T> for PollSender<T>` | Trait impl | Sink impl |  |
| 321 | `poll_close`  | `Sink<T> for PollSender<T>` | Trait impl | Sink impl |  |

## `tokio-util/src/sync/poll_semaphore.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `new`  | `PollSemaphore` | Public API | Constructor | Create a new `PollSemaphore`. |
| 31 | `close`  | `PollSemaphore` | Public API | Data movement | Closes the semaphore. |
| 36 | `clone_inner`  | `PollSemaphore` | Public API | Handle / reference plumbing | Obtain a clone of the inner semaphore. |
| 41 | `into_inner`  | `PollSemaphore` | Public API | Conversion | Get back the inner semaphore. |
| 58 | `poll_acquire`  | `PollSemaphore` | Public API | Poll function | Poll to acquire a permit from the semaphore. |
| 75 | `poll_acquire_many`  | `PollSemaphore` | Public API | Poll function | Poll to acquire many permits from the semaphore. |
| 127 | `available_permits`  | `PollSemaphore` | Public API | Other / internal logic | Returns the current number of available permits. |
| 140 | `add_permits`  | `PollSemaphore` | Public API | Locking / permits | Adds `n` new permits to the semaphore. |
| 148 | `poll_next`  | `Stream for PollSemaphore` | Trait impl | Stream impl |  |
| 154 | `clone`  | `Clone for PollSemaphore` | Trait impl | Clone |  |
| 160 | `fmt`  | `fmt::Debug for PollSemaphore` | Trait impl | Formatting |  |
| 168 | `as_ref`  | `AsRef<Semaphore> for PollSemaphore` | Trait impl | Conversion |  |

## `tokio-util/src/sync/reusable_box.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `new`  | `ReusableBoxFuture<'a, T>` | Public API | Constructor | Create a new `ReusableBoxFuture<T>` containing the provided future. |
| 32 | `set`  | `ReusableBoxFuture<'a, T>` | Public API | Configuration / setter | Replace the future currently stored in this box. |
| 46 | `try_set`  | `ReusableBoxFuture<'a, T>` | Public API | Non-blocking attempt | Replace the future currently stored in this box. |
| 55 | `real_try_set`  |  | Private helper | Other / internal logic |  |
| 71 | `get_pin`  | `ReusableBoxFuture<'a, T>` | Public API | Accessor / query | Get a pinned reference to the underlying future. |
| 76 | `poll`  | `ReusableBoxFuture<'a, T>` | Public API | Poll function | Poll the future stored inside this box. |
| 85 | `poll`  | `Future for ReusableBoxFuture<'_, T>` | Trait impl | Future impl (poll) | Poll the future stored inside this box. |
| 96 | `fmt`  | `fmt::Debug for ReusableBoxFuture<'_, T>` | Trait impl | Formatting |  |
| 101 | `reuse_pin_box`  |  | Private helper | Other / internal logic |  |
| 141 | `new`  | `O> CallOnDrop<O, F>` | Private helper | Constructor |  |
| 145 | `call`  | `O> CallOnDrop<O, F>` | Private helper | Other / internal logic |  |
| 153 | `drop`  | `O> Drop for CallOnDrop<O, F>` | Trait impl | Other / internal logic |  |

