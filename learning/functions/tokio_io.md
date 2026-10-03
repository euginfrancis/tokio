# `tokio::io` — 270 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 111 |
| Public API | 84 |
| Crate-internal | 36 |
| Trait method (declaration/default) | 10 |
| Inside macro_rules! | 10 |
| Private helper | 10 |
| Test | 9 |

## `tokio/src/io/async_buf_read.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 45 | `poll_fill_buf`  | `trait AsyncBufRead` | Trait method (declaration/default) | Poll function | Attempts to return the contents of the internal buffer, filling it with more data from the inner reader if it is empty. |
| 62 | `consume`  | `trait AsyncBufRead` | Trait method (declaration/default) | I/O operation | Tells this buffer that `amt` bytes have been consumed from the buffer, so they should no longer be returned in calls to [`poll_read`]. |
| 67 | `poll_fill_buf`  |  | Inside macro_rules! | Poll function |  |
| 71 | `consume`  |  | Inside macro_rules! | I/O operation |  |
| 90 | `poll_fill_buf`  | `AsyncBufRead for Pin<P>` | Trait impl | I/O trait impl |  |
| 94 | `consume`  | `AsyncBufRead for Pin<P>` | Trait impl | I/O trait impl |  |
| 101 | `poll_fill_buf`  | `AsyncBufRead for &[u8]` | Trait impl | I/O trait impl |  |
| 106 | `consume`  | `AsyncBufRead for &[u8]` | Trait impl | I/O trait impl |  |
| 113 | `poll_fill_buf`  | `AsyncBufRead for io::Cursor<T>` | Trait impl | I/O trait impl |  |
| 118 | `consume`  | `AsyncBufRead for io::Cursor<T>` | Trait impl | I/O trait impl |  |

## `tokio/src/io/async_fd.rs` (51)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 226 | `new`  | `AsyncFd<T>` | Public API | Constructor | Creates an [`AsyncFd`] backed by (and taking ownership of) an object implementing [`AsRawFd`]. |
| 243 | `with_interest`  | `AsyncFd<T>` | Public API | Constructor | Creates an [`AsyncFd`] backed by (and taking ownership of) an object implementing [`AsRawFd`], with a specific [`Interest`]. |
| 251 | `new_with_handle_and_interest`  | `AsyncFd<T>` | Crate-internal | Constructor |  |
| 277 | `try_new`  | `AsyncFd<T>` | Public API | Non-blocking attempt | Creates an [`AsyncFd`] backed by (and taking ownership of) an object implementing [`AsRawFd`]. |
| 297 | `try_with_interest`  | `AsyncFd<T>` | Public API | Non-blocking attempt | Creates an [`AsyncFd`] backed by (and taking ownership of) an object implementing [`AsRawFd`], with a specific [`Interest`]. |
| 305 | `try_new_with_handle_and_interest`  | `AsyncFd<T>` | Crate-internal | Non-blocking attempt |  |
| 323 | `get_ref`  | `AsyncFd<T>` | Public API | Accessor / query | Returns a shared reference to the backing object of this [`AsyncFd`]. |
| 329 | `get_mut`  | `AsyncFd<T>` | Public API | Accessor / query | Returns a mutable reference to the backing object of this [`AsyncFd`]. |
| 333 | `take_inner`  | `AsyncFd<T>` | Private helper | Data movement |  |
| 344 | `into_inner`  | `AsyncFd<T>` | Public API | Conversion | Deregisters this file descriptor and returns ownership of the backing object. |
| 375 | `poll_read_ready`  | `AsyncFd<T>` | Public API | Poll function | Polls for read readiness. |
| 412 | `poll_read_ready_mut`  | `AsyncFd<T>` | Public API | Poll function | Polls for read readiness. |
| 451 | `poll_write_ready`  | `AsyncFd<T>` | Public API | Poll function | Polls for write readiness. |
| 488 | `poll_write_ready_mut`  | `AsyncFd<T>` | Public API | Poll function | Polls for write readiness. |
| 589 | `ready` 🅰 | `AsyncFd<T>` | Public API | I/O operation | Waits for any of the requested ready states, returning a [`AsyncFdReadyGuard`] that must be dropped to resume polling for the requested ready states. |
| 685 | `ready_mut` 🅰 | `AsyncFd<T>` | Public API | I/O operation | Waits for any of the requested ready states, returning a [`AsyncFdReadyMutGuard`] that must be dropped to resume polling for the requested ready states. |
| 713 | `readable` 🅰 | `AsyncFd<T>` | Public API | I/O operation | Waits for the file descriptor to become readable, returning a [`AsyncFdReadyGuard`] that must be dropped to resume read-readiness polling. |
| 731 | `readable_mut` 🅰 | `AsyncFd<T>` | Public API | I/O operation | Waits for the file descriptor to become readable, returning a [`AsyncFdReadyMutGuard`] that must be dropped to resume read-readiness polling. |
| 751 | `writable` 🅰 | `AsyncFd<T>` | Public API | Async operation | Waits for the file descriptor to become writable, returning a [`AsyncFdReadyGuard`] that must be dropped to resume write-readiness polling. |
| 769 | `writable_mut` 🅰 | `AsyncFd<T>` | Public API | Async operation | Waits for the file descriptor to become writable, returning a [`AsyncFdReadyMutGuard`] that must be dropped to resume write-readiness polling. |
| 850 | `async_io` 🅰 | `AsyncFd<T>` | Public API | Async operation | Reads or writes from the file descriptor using a user-provided IO operation. |
| 866 | `async_io_mut` 🅰 | `AsyncFd<T>` | Public API | Async operation | Reads or writes from the file descriptor using a user-provided IO operation. |
| 902 | `try_io`  | `AsyncFd<T>` | Public API | Non-blocking attempt | Tries to read or write from the file descriptor using a user-provided IO operation. |
| 917 | `try_io_mut`  | `AsyncFd<T>` | Public API | Non-blocking attempt | Tries to read or write from the file descriptor using a user-provided IO operation. |
| 928 | `as_raw_fd`  | `AsRawFd for AsyncFd<T>` | Trait impl | OS handle access |  |
| 934 | `as_fd`  | `std::os::unix::io::AsFd for AsyncFd<T>` | Trait impl | OS handle access |  |
| 940 | `fmt`  | `std::fmt::Debug for AsyncFd<T>` | Trait impl | Formatting |  |
| 948 | `drop`  | `Drop for AsyncFd<T>` | Trait impl | Drop / cleanup |  |
| 969 | `clear_ready`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Other / internal logic | Indicates to tokio that the file descriptor is no longer ready. |
| 1058 | `clear_ready_matching`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Other / internal logic | Indicates to tokio that the file descriptor no longer has a specific readiness. |
| 1078 | `retain_ready`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Other / internal logic | This method should be invoked when you intentionally want to keep the ready flag asserted. |
| 1089 | `ready`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | I/O operation | Get the [`Ready`] value associated with this guard. |
| 1151 | `try_io`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Non-blocking attempt |  |
| 1167 | `get_ref`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Accessor / query | Returns a shared reference to the inner [`AsyncFd`]. |
| 1172 | `get_inner`  | `AsyncFdReadyGuard<'a, Inner>` | Public API | Accessor / query | Returns a shared reference to the backing object of the inner [`AsyncFd`]. |
| 1193 | `clear_ready`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Other / internal logic | Indicates to tokio that the file descriptor is no longer ready. |
| 1282 | `clear_ready_matching`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Other / internal logic | Indicates to tokio that the file descriptor no longer has a specific readiness. |
| 1302 | `retain_ready`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Other / internal logic | This method should be invoked when you intentionally want to keep the ready flag asserted. |
| 1313 | `ready`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | I/O operation | Get the [`Ready`] value associated with this guard. |
| 1336 | `try_io`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Non-blocking attempt | Performs the provided IO operation. |
| 1352 | `get_ref`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Accessor / query | Returns a shared reference to the inner [`AsyncFd`]. |
| 1357 | `get_mut`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Accessor / query | Returns a mutable reference to the inner [`AsyncFd`]. |
| 1362 | `get_inner`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Accessor / query | Returns a shared reference to the backing object of the inner [`AsyncFd`]. |
| 1367 | `get_inner_mut`  | `AsyncFdReadyMutGuard<'a, Inner>` | Public API | Accessor / query | Returns a mutable reference to the backing object of the inner [`AsyncFd`]. |
| 1373 | `fmt`  | `std::fmt::Debug for AsyncFdReadyGuard<'a, T>` | Trait impl | Formatting |  |
| 1381 | `fmt`  | `std::fmt::Debug for AsyncFdReadyMutGuard<'a, T>` | Trait impl | Formatting |  |
| 1412 | `into_parts`  | `AsyncFdTryNewError<T>` | Public API | Conversion | Returns the original object passed to [`try_new`] or [`try_with_interest`] alongside the error that caused these functions to fail. |
| 1418 | `fmt`  | `fmt::Display for AsyncFdTryNewError<T>` | Trait impl | Formatting |  |
| 1424 | `fmt`  | `fmt::Debug for AsyncFdTryNewError<T>` | Trait impl | Formatting |  |
| 1430 | `source`  | `Error for AsyncFdTryNewError<T>` | Trait impl | Error type |  |
| 1436 | `from`  | `From<AsyncFdTryNewError<T>> for io::Error` | Trait impl | Conversion |  |

## `tokio/src/io/async_read.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 55 | `poll_read`  | `trait AsyncRead` | Trait method (declaration/default) | Poll function | Attempts to read from the `AsyncRead` into `buf`. |
| 64 | `poll_read`  |  | Inside macro_rules! | Poll function |  |
| 87 | `poll_read`  | `AsyncRead for Pin<P>` | Trait impl | I/O trait impl |  |
| 98 | `poll_read`  | `AsyncRead for &[u8]` | Trait impl | I/O trait impl |  |
| 113 | `poll_read`  | `AsyncRead for io::Cursor<T>` | Trait impl | I/O trait impl |  |

## `tokio/src/io/async_seek.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `start_seek`  | `trait AsyncSeek` | Trait method (declaration/default) | Runtime/task control | Attempts to seek to an offset, in bytes, in a stream. |
| 52 | `poll_complete`  | `trait AsyncSeek` | Trait method (declaration/default) | Poll function | Waits for a seek operation to complete. |
| 57 | `start_seek`  |  | Inside macro_rules! | Runtime/task control |  |
| 61 | `poll_complete`  |  | Inside macro_rules! | Poll function |  |
| 80 | `start_seek`  | `AsyncSeek for Pin<P>` | Trait impl | I/O trait impl |  |
| 84 | `poll_complete`  | `AsyncSeek for Pin<P>` | Trait impl | I/O trait impl |  |
| 91 | `start_seek`  | `AsyncSeek for io::Cursor<T>` | Trait impl | I/O trait impl |  |
| 95 | `poll_complete`  | `AsyncSeek for io::Cursor<T>` | Trait impl | I/O trait impl |  |

## `tokio/src/io/async_write.rs` (40)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 52 | `poll_write`  | `trait AsyncWrite` | Trait method (declaration/default) | Poll function | Attempt to write bytes from `buf` into the object. |
| 67 | `poll_flush`  | `trait AsyncWrite` | Trait method (declaration/default) | Poll function | Attempts to flush the object, ensuring that any buffered data reach their destination. |
| 127 | `poll_shutdown`  | `trait AsyncWrite` | Trait method (declaration/default) | Poll function | Initiates or attempts to shut down this writer, returning success when the I/O connection has completely shut down. |
| 152 | `poll_write_vectored`  | `trait AsyncWrite` | Trait method (declaration/default) | Poll function | Like [`poll_write`], except that it writes from a slice of buffers. |
| 174 | `is_write_vectored`  | `trait AsyncWrite` | Trait method (declaration/default) | Accessor / query | Determines if this writer has an efficient [`poll_write_vectored`] implementation. |
| 181 | `poll_write`  |  | Inside macro_rules! | Poll function |  |
| 189 | `poll_write_vectored`  |  | Inside macro_rules! | Poll function |  |
| 197 | `is_write_vectored`  |  | Inside macro_rules! | Accessor / query |  |
| 201 | `poll_flush`  |  | Inside macro_rules! | Poll function |  |
| 205 | `poll_shutdown`  |  | Inside macro_rules! | Poll function |  |
| 224 | `poll_write`  | `AsyncWrite for Pin<P>` | Trait impl | I/O trait impl |  |
| 232 | `poll_write_vectored`  | `AsyncWrite for Pin<P>` | Trait impl | I/O trait impl |  |
| 240 | `is_write_vectored`  | `AsyncWrite for Pin<P>` | Trait impl | I/O trait impl |  |
| 244 | `poll_flush`  | `AsyncWrite for Pin<P>` | Trait impl | I/O trait impl |  |
| 248 | `poll_shutdown`  | `AsyncWrite for Pin<P>` | Trait impl | I/O trait impl |  |
| 255 | `poll_write`  | `AsyncWrite for Vec<u8>` | Trait impl | I/O trait impl |  |
| 265 | `poll_write_vectored`  | `AsyncWrite for Vec<u8>` | Trait impl | I/O trait impl |  |
| 274 | `is_write_vectored`  | `AsyncWrite for Vec<u8>` | Trait impl | I/O trait impl |  |
| 279 | `poll_flush`  | `AsyncWrite for Vec<u8>` | Trait impl | I/O trait impl |  |
| 284 | `poll_shutdown`  | `AsyncWrite for Vec<u8>` | Trait impl | I/O trait impl |  |
| 291 | `poll_write`  | `AsyncWrite for io::Cursor<&mut [u8]>` | Trait impl | I/O trait impl |  |
| 300 | `poll_write_vectored`  | `AsyncWrite for io::Cursor<&mut [u8]>` | Trait impl | I/O trait impl |  |
| 309 | `is_write_vectored`  | `AsyncWrite for io::Cursor<&mut [u8]>` | Trait impl | I/O trait impl |  |
| 314 | `poll_flush`  | `AsyncWrite for io::Cursor<&mut [u8]>` | Trait impl | I/O trait impl |  |
| 319 | `poll_shutdown`  | `AsyncWrite for io::Cursor<&mut [u8]>` | Trait impl | I/O trait impl |  |
| 326 | `poll_write`  | `AsyncWrite for io::Cursor<&mut Vec<u8>>` | Trait impl | I/O trait impl |  |
| 335 | `poll_write_vectored`  | `AsyncWrite for io::Cursor<&mut Vec<u8>>` | Trait impl | I/O trait impl |  |
| 344 | `is_write_vectored`  | `AsyncWrite for io::Cursor<&mut Vec<u8>>` | Trait impl | I/O trait impl |  |
| 349 | `poll_flush`  | `AsyncWrite for io::Cursor<&mut Vec<u8>>` | Trait impl | I/O trait impl |  |
| 354 | `poll_shutdown`  | `AsyncWrite for io::Cursor<&mut Vec<u8>>` | Trait impl | I/O trait impl |  |
| 361 | `poll_write`  | `AsyncWrite for io::Cursor<Vec<u8>>` | Trait impl | I/O trait impl |  |
| 370 | `poll_write_vectored`  | `AsyncWrite for io::Cursor<Vec<u8>>` | Trait impl | I/O trait impl |  |
| 379 | `is_write_vectored`  | `AsyncWrite for io::Cursor<Vec<u8>>` | Trait impl | I/O trait impl |  |
| 384 | `poll_flush`  | `AsyncWrite for io::Cursor<Vec<u8>>` | Trait impl | I/O trait impl |  |
| 389 | `poll_shutdown`  | `AsyncWrite for io::Cursor<Vec<u8>>` | Trait impl | I/O trait impl |  |
| 396 | `poll_write`  | `AsyncWrite for io::Cursor<Box<[u8]>>` | Trait impl | I/O trait impl |  |
| 405 | `poll_write_vectored`  | `AsyncWrite for io::Cursor<Box<[u8]>>` | Trait impl | I/O trait impl |  |
| 414 | `is_write_vectored`  | `AsyncWrite for io::Cursor<Box<[u8]>>` | Trait impl | I/O trait impl |  |
| 419 | `poll_flush`  | `AsyncWrite for io::Cursor<Box<[u8]>>` | Trait impl | I/O trait impl |  |
| 424 | `poll_shutdown`  | `AsyncWrite for io::Cursor<Box<[u8]>>` | Trait impl | I/O trait impl |  |

## `tokio/src/io/blocking.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 48 | `new` ⚠ | `Blocking<T>` | Crate-internal | Constructor | # Safety The `Read` implementation of `inner` must never read from the buffer it is borrowing and must correctly report the length of the data written into the buffer. |
| 65 | `new_mandatory` ⚠ | `Blocking<T>` | Crate-internal | Constructor | Like `new`, but operations are spawned with `spawn_mandatory_blocking`, so an operation that was started before the runtime began shutting down still runs. |
| 80 | `spawn`  |  | Private helper | Runtime/task control | Runs `f` on the blocking pool. |
| 96 | `poll_read`  | `AsyncRead for Blocking<T>` | Trait impl | I/O trait impl |  |
| 156 | `poll_write`  | `AsyncWrite for Blocking<T>` | Trait impl | I/O trait impl |  |
| 200 | `poll_flush`  | `AsyncWrite for Blocking<T>` | Trait impl | I/O trait impl |  |
| 239 | `poll_shutdown`  | `AsyncWrite for Blocking<T>` | Trait impl | I/O trait impl |  |
| 257 | `with_capacity`  | `Buf` | Crate-internal | Constructor |  |
| 264 | `is_empty`  | `Buf` | Crate-internal | Accessor / query |  |
| 268 | `len`  | `Buf` | Crate-internal | Accessor / query |  |
| 272 | `copy_to`  | `Buf` | Crate-internal | I/O operation |  |
| 285 | `copy_from`  | `Buf` | Crate-internal | I/O operation |  |
| 294 | `bytes`  | `Buf` | Crate-internal | Other / internal logic |  |
| 302 | `read_from` ⚠ | `Buf` | Crate-internal | I/O operation | # Safety `rd` must not read from the buffer `read` is borrowing and must correctly report the length of the data written into the buffer. |
| 331 | `write_to`  | `Buf` | Crate-internal | I/O operation |  |
| 347 | `prepare_uring_read`  | `Buf` | Crate-internal | Other / internal logic | Prepare the internal buffer for an io-uring read operation. |
| 362 | `complete_uring_read` ⚠ | `Buf` | Crate-internal | Runtime/task control | Complete an io-uring read operation. |
| 376 | `discard_read`  | `Buf` | Crate-internal | Other / internal logic |  |
| 383 | `copy_from_bufs`  | `Buf` | Crate-internal | I/O operation |  |
| 402 | `gone`  |  | Private helper | Other / internal logic |  |

## `tokio/src/io/interest.rs` (14)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 86 | `is_readable` 🅲 | `Interest` | Public API | Accessor / query | Returns true if the value includes readable interest. |
| 103 | `is_writable` 🅲 | `Interest` | Public API | Accessor / query | Returns true if the value includes writable interest. |
| 120 | `is_error` 🅲 | `Interest` | Public API | Accessor / query | Returns true if the value includes error interest. |
| 125 | `is_aio` 🅲 | `Interest` | Private helper | Accessor / query |  |
| 130 | `is_lio` 🅲 | `Interest` | Private helper | Accessor / query |  |
| 149 | `is_priority` 🅲 | `Interest` | Public API | Accessor / query | Returns true if the value includes priority interest. |
| 167 | `add` 🅲 | `Interest` | Public API | Other / internal logic | Add together two `Interest` values. |
| 195 | `remove`  | `Interest` | Public API | Data movement | Remove `Interest` from `self`. |
| 206 | `to_mio`  | `Interest` | Crate-internal | Conversion |  |
| 207 | `mio_add`  |  | Private helper | Other / internal logic |  |
| 258 | `mask`  | `Interest` | Crate-internal | Other / internal logic |  |
| 274 | `bitor`  | `ops::BitOr for Interest` | Trait impl | Other / internal logic |  |
| 281 | `bitor_assign`  | `ops::BitOrAssign for Interest` | Trait impl | Other / internal logic |  |
| 287 | `fmt`  | `fmt::Debug for Interest` | Trait impl | Formatting |  |

## `tokio/src/io/join.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `join`  |  | Public API | Other / internal logic | Join two values implementing `AsyncRead` and `AsyncWrite` into a single handle. |
| 38 | `into_inner`  | `Join<R, W>` | Public API | Conversion | Splits this `Join` back into its `AsyncRead` and `AsyncWrite` components. |
| 43 | `reader`  | `Join<R, W>` | Public API | I/O operation | Returns a reference to the inner reader. |
| 48 | `writer`  | `Join<R, W>` | Public API | I/O operation | Returns a reference to the inner writer. |
| 53 | `reader_mut`  | `Join<R, W>` | Public API | I/O operation | Returns a mutable reference to the inner reader. |
| 58 | `writer_mut`  | `Join<R, W>` | Public API | I/O operation | Returns a mutable reference to the inner writer. |
| 63 | `reader_pin_mut`  | `Join<R, W>` | Public API | I/O operation | Returns a pinned mutable reference to the inner reader. |
| 68 | `writer_pin_mut`  | `Join<R, W>` | Public API | I/O operation | Returns a pinned mutable reference to the inner writer. |
| 77 | `poll_read`  | `AsyncRead for Join<R, W>` | Trait impl | I/O trait impl |  |
| 90 | `poll_write`  | `AsyncWrite for Join<R, W>` | Trait impl | I/O trait impl |  |
| 98 | `poll_flush`  | `AsyncWrite for Join<R, W>` | Trait impl | I/O trait impl |  |
| 102 | `poll_shutdown`  | `AsyncWrite for Join<R, W>` | Trait impl | I/O trait impl |  |
| 106 | `poll_write_vectored`  | `AsyncWrite for Join<R, W>` | Trait impl | I/O trait impl |  |
| 114 | `is_write_vectored`  | `AsyncWrite for Join<R, W>` | Trait impl | I/O trait impl |  |
| 123 | `poll_fill_buf`  | `AsyncBufRead for Join<R, W>` | Trait impl | I/O trait impl |  |
| 127 | `consume`  | `AsyncBufRead for Join<R, W>` | Trait impl | I/O trait impl |  |

## `tokio/src/io/poll_evented.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 89 | `new`  | `PollEvented<E>` | Crate-internal | Constructor | Creates a new `PollEvented` associated with the default reactor. |
| 110 | `new_with_interest`  | `PollEvented<E>` | Crate-internal | Constructor | Creates a new `PollEvented` associated with the default reactor, for specific `Interest` state. |
| 115 | `new_with_interest_and_handle`  | `PollEvented<E>` | Crate-internal | Constructor |  |
| 129 | `registration`  | `PollEvented<E>` | Crate-internal | Other / internal logic | Returns a reference to the registration. |
| 135 | `into_inner`  | `PollEvented<E>` | Crate-internal | Conversion | Deregisters the inner io from the registration and returns a Result containing the inner io. |
| 143 | `reregister`  | `PollEvented<E>` | Crate-internal | Other / internal logic | Re-register under new runtime with `interest`. |
| 161 | `poll_read` ⚠ | `PollEvented<E>` | Crate-internal | Poll function |  |
| 229 | `poll_write`  | `PollEvented<E>` | Crate-internal | Poll function |  |
| 280 | `poll_write_vectored`  | `PollEvented<E>` | Crate-internal | Poll function |  |
| 301 | `deref`  | `Deref for PollEvented<E>` | Trait impl | Deref |  |
| 307 | `fmt`  | `fmt::Debug for PollEvented<E>` | Trait impl | Formatting |  |
| 313 | `drop`  | `Drop for PollEvented<E>` | Trait impl | Drop / cleanup |  |

## `tokio/src/io/read_buf.rs` (25)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `new`  | `ReadBuf<'a>` | Public API | Constructor | Creates a new `ReadBuf` from a fully initialized buffer. |
| 48 | `uninit`  | `ReadBuf<'a>` | Public API | Other / internal logic | Creates a new `ReadBuf` from a buffer that may be uninitialized. |
| 58 | `capacity`  | `ReadBuf<'a>` | Public API | Accessor / query | Returns the total capacity of the buffer. |
| 64 | `filled`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a shared reference to the filled portion of the buffer. |
| 73 | `filled_mut`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the filled portion of the buffer. |
| 82 | `take`  | `ReadBuf<'a>` | Public API | Data movement | Returns a new `ReadBuf` comprised of the unfilled section up to `n`. |
| 92 | `initialized`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a shared reference to the initialized portion of the buffer. |
| 103 | `initialized_mut`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the initialized portion of the buffer. |
| 125 | `inner_mut` ⚠ | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the entire buffer, without ensuring that it has been fully initialized. |
| 137 | `unfilled_mut` ⚠ | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the unfilled part of the buffer without ensuring that it has been fully initialized. |
| 146 | `initialize_unfilled`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the unfilled part of the buffer, ensuring it is fully initialized. |
| 158 | `initialize_unfilled_to`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns a mutable reference to the first `n` bytes of the unfilled part of the buffer, ensuring it is fully initialized. |
| 181 | `remaining`  | `ReadBuf<'a>` | Public API | Other / internal logic | Returns the number of bytes at the end of the slice that have not yet been filled. |
| 189 | `clear`  | `ReadBuf<'a>` | Public API | Configuration / setter | Clears the buffer, resetting the filled region to empty. |
| 202 | `advance`  | `ReadBuf<'a>` | Public API | Other / internal logic | Advances the size of the filled region of the buffer. |
| 219 | `set_filled`  | `ReadBuf<'a>` | Public API | Configuration / setter | Sets the size of the filled region of the buffer. |
| 236 | `assume_init` ⚠ | `ReadBuf<'a>` | Public API | Other / internal logic | Asserts that the first `n` unfilled bytes of the buffer are initialized. |
| 250 | `put_slice`  | `ReadBuf<'a>` | Public API | Other / internal logic | Appends data to the buffer, advancing the written position and possibly also the initialized position. |
| 280 | `remaining_mut`  | `bytes::BufMut for ReadBuf<'a>` | Trait impl | Other / internal logic |  |
| 285 | `advance_mut` ⚠ | `bytes::BufMut for ReadBuf<'a>` | Trait impl | Other / internal logic |  |
| 292 | `chunk_mut`  | `bytes::BufMut for ReadBuf<'a>` | Trait impl | Other / internal logic |  |
| 307 | `fmt`  | `fmt::Debug for ReadBuf<'_>` | Trait impl | Formatting |  |
| 320 | `slice_to_uninit_mut` ⚠ |  | Private helper | Other / internal logic | # Safety The caller must ensure that `slice` is fully initialized and never writes uninitialized bytes to the returned slice. |
| 330 | `slice_assume_init` ⚠ |  | Private helper | Other / internal logic |  |
| 340 | `slice_assume_init_mut` ⚠ |  | Private helper | Other / internal logic |  |

## `tokio/src/io/ready.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 57 | `from_mio`  | `Ready` | Crate-internal | Conversion |  |
| 111 | `is_empty`  | `Ready` | Public API | Accessor / query | Returns true if `Ready` is the empty set. |
| 127 | `is_readable`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes `readable`. |
| 143 | `is_writable`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes writable `readiness`. |
| 158 | `is_read_closed`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes read-closed `readiness`. |
| 173 | `is_write_closed`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes write-closed `readiness`. |
| 190 | `is_priority`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes priority `readiness`. |
| 205 | `is_error`  | `Ready` | Public API | Accessor / query | Returns `true` if the value includes error `readiness`. |
| 214 | `contains`  | `Ready` | Crate-internal | Other / internal logic | Returns true if `self` is a superset of `other`. |
| 226 | `from_usize`  | `Ready` | Crate-internal | Conversion | Creates a `Ready` instance using the given `usize` representation. |
| 234 | `as_usize`  | `Ready` | Crate-internal | Conversion | Returns a `usize` representation of the `Ready` value. |
| 238 | `from_interest`  | `Ready` | Crate-internal | Conversion |  |
| 264 | `intersection`  | `Ready` | Crate-internal | Other / internal logic |  |
| 268 | `satisfies`  | `Ready` | Crate-internal | Other / internal logic |  |
| 277 | `bitor`  | `ops::BitOr<Ready> for Ready` | Trait impl | Other / internal logic |  |
| 284 | `bitor_assign`  | `ops::BitOrAssign<Ready> for Ready` | Trait impl | Other / internal logic |  |
| 293 | `bitand`  | `ops::BitAnd<Ready> for Ready` | Trait impl | Other / internal logic |  |
| 302 | `sub`  | `ops::Sub<Ready> for Ready` | Trait impl | Other / internal logic |  |
| 308 | `fmt`  | `fmt::Debug for Ready` | Trait impl | Formatting |  |

## `tokio/src/io/seek.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `seek`  |  | Crate-internal | I/O operation |  |
| 40 | `poll`  | `Future for Seek<'_, S>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/split.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `split`  |  | Public API | Combinator / iteration | Splits a single value implementing `AsyncRead + AsyncWrite` into separate `AsyncRead` and `AsyncWrite` handles. |
| 59 | `with_lock`  | `Inner<T>` | Private helper | Constructor |  |
| 72 | `is_pair_of`  | `ReadHalf<T>` | Public API | Accessor / query | Checks if this `ReadHalf` and some `WriteHalf` were split from the same stream. |
| 84 | `unsplit`  | `ReadHalf<T>` | Public API | Other / internal logic | Reunites with a previously split `WriteHalf`. |
| 105 | `is_pair_of`  | `WriteHalf<T>` | Public API | Accessor / query | Checks if this `WriteHalf` and some `ReadHalf` were split from the same stream. |
| 111 | `poll_read`  | `AsyncRead for ReadHalf<T>` | Trait impl | I/O trait impl |  |
| 121 | `poll_write`  | `AsyncWrite for WriteHalf<T>` | Trait impl | I/O trait impl |  |
| 129 | `poll_flush`  | `AsyncWrite for WriteHalf<T>` | Trait impl | I/O trait impl |  |
| 133 | `poll_shutdown`  | `AsyncWrite for WriteHalf<T>` | Trait impl | I/O trait impl |  |
| 137 | `poll_write_vectored`  | `AsyncWrite for WriteHalf<T>` | Trait impl | I/O trait impl |  |
| 146 | `is_write_vectored`  | `AsyncWrite for WriteHalf<T>` | Trait impl | I/O trait impl |  |
| 157 | `fmt`  | `fmt::Debug for ReadHalf<T>` | Trait impl | Formatting |  |
| 163 | `fmt`  | `fmt::Debug for WriteHalf<T>` | Trait impl | Formatting |  |

## `tokio/src/io/stderr.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 82 | `stderr`  |  | Public API | Other / internal logic | Constructs a new handle to the standard error of the current process. |
| 101 | `as_raw_fd`  | `AsRawFd for Stderr` | Trait impl | OS handle access |  |
| 107 | `as_fd`  | `AsFd for Stderr` | Trait impl | OS handle access |  |
| 117 | `as_raw_handle`  | `AsRawHandle for Stderr` | Trait impl | OS handle access |  |
| 123 | `as_handle`  | `AsHandle for Stderr` | Trait impl | OS handle access |  |
| 130 | `poll_write`  | `AsyncWrite for Stderr` | Trait impl | I/O trait impl |  |
| 138 | `poll_flush`  | `AsyncWrite for Stderr` | Trait impl | I/O trait impl |  |
| 142 | `poll_shutdown`  | `AsyncWrite for Stderr` | Trait impl | I/O trait impl |  |

## `tokio/src/io/stdin.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `stdin`  |  | Public API | Other / internal logic | Constructs a new handle to the standard input of the current process. |
| 62 | `as_raw_fd`  | `AsRawFd for Stdin` | Trait impl | OS handle access |  |
| 68 | `as_fd`  | `AsFd for Stdin` | Trait impl | OS handle access |  |
| 78 | `as_raw_handle`  | `AsRawHandle for Stdin` | Trait impl | OS handle access |  |
| 84 | `as_handle`  | `AsHandle for Stdin` | Trait impl | OS handle access |  |
| 91 | `poll_read`  | `AsyncRead for Stdin` | Trait impl | I/O trait impl |  |

## `tokio/src/io/stdio_common.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `new`  | `SplitByUtf8BoundaryIfWindows<W>` | Crate-internal | Constructor |  |
| 32 | `poll_write`  | `crate::io::AsyncWrite for SplitByUtf8BoundaryIfWindows<W>` | Trait impl | I/O trait impl |  |
| 94 | `poll_flush`  | `crate::io::AsyncWrite for SplitByUtf8BoundaryIfWindows<W>` | Trait impl | I/O trait impl |  |
| 101 | `poll_shutdown`  | `crate::io::AsyncWrite for SplitByUtf8BoundaryIfWindows<W>` | Trait impl | I/O trait impl |  |
| 123 | `poll_write`  | `crate::io::AsyncWrite for TextMockWriter` | Test | I/O trait impl |  |
| 133 | `poll_flush`  | `crate::io::AsyncWrite for TextMockWriter` | Test | I/O trait impl |  |
| 137 | `poll_shutdown`  | `crate::io::AsyncWrite for TextMockWriter` | Test | I/O trait impl |  |
| 150 | `new`  | `LoggingMockWriter` | Test | Constructor |  |
| 158 | `poll_write`  | `crate::io::AsyncWrite for LoggingMockWriter` | Test | I/O trait impl |  |
| 168 | `poll_flush`  | `crate::io::AsyncWrite for LoggingMockWriter` | Test | I/O trait impl |  |
| 172 | `poll_shutdown`  | `crate::io::AsyncWrite for LoggingMockWriter` | Test | I/O trait impl |  |
| 182 | `test_splitter`  |  | Test | Other / internal logic |  |
| 196 | `test_pseudo_text`  |  | Test | Other / internal logic |  |

## `tokio/src/io/stdout.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 170 | `stdout`  |  | Public API | Other / internal logic | Constructs a new handle to the standard output of the current process. |
| 189 | `as_raw_fd`  | `AsRawFd for Stdout` | Trait impl | OS handle access |  |
| 195 | `as_fd`  | `AsFd for Stdout` | Trait impl | OS handle access |  |
| 205 | `as_raw_handle`  | `AsRawHandle for Stdout` | Trait impl | OS handle access |  |
| 211 | `as_handle`  | `AsHandle for Stdout` | Trait impl | OS handle access |  |
| 218 | `poll_write`  | `AsyncWrite for Stdout` | Trait impl | I/O trait impl |  |
| 226 | `poll_flush`  | `AsyncWrite for Stdout` | Trait impl | I/O trait impl |  |
| 230 | `poll_shutdown`  | `AsyncWrite for Stdout` | Trait impl | I/O trait impl |  |

