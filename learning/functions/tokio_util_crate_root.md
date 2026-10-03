# `tokio-util (crate root)` — 53 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 35 |
| Trait method (declaration/default) | 9 |
| Public API | 6 |
| Test | 2 |
| Private helper | 1 |

## `tokio-util/src/compat.rs` (25)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 135 | `compat`  | `trait FuturesAsyncReadCompatExt` | Trait method (declaration/default) | Other / internal logic | Wraps `self` with a compatibility layer that implements `tokio_io::AsyncRead`. |
| 150 | `compat_write`  | `trait FuturesAsyncWriteCompatExt` | Trait method (declaration/default) | Other / internal logic | Wraps `self` with a compatibility layer that implements `tokio::io::AsyncWrite`. |
| 165 | `compat`  | `trait TokioAsyncReadCompatExt` | Trait method (declaration/default) | Other / internal logic | Wraps `self` with a compatibility layer that implements `futures_io::AsyncRead`. |
| 180 | `compat_write`  | `trait TokioAsyncWriteCompatExt` | Trait method (declaration/default) | Other / internal logic | Wraps `self` with a compatibility layer that implements `futures_io::AsyncWrite`. |
| 193 | `new`  | `Compat<T>` | Private helper | Constructor |  |
| 202 | `get_ref`  | `Compat<T>` | Public API | Accessor / query | Get a reference to the `Future`, `Stream`, `AsyncRead`, or `AsyncWrite` object contained within. |
| 208 | `get_mut`  | `Compat<T>` | Public API | Accessor / query | Get a mutable reference to the `Future`, `Stream`, `AsyncRead`, or `AsyncWrite` object contained within. |
| 213 | `into_inner`  | `Compat<T>` | Public API | Conversion | Returns the wrapped item. |
| 222 | `poll_read`  | `tokio::io::AsyncRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 244 | `poll_read`  | `futures_io::AsyncRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 263 | `poll_fill_buf`  | `tokio::io::AsyncBufRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 270 | `consume`  | `tokio::io::AsyncBufRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 279 | `poll_fill_buf`  | `futures_io::AsyncBufRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 286 | `consume`  | `futures_io::AsyncBufRead for Compat<T>` | Trait impl | I/O trait impl |  |
| 295 | `poll_write`  | `tokio::io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 303 | `poll_flush`  | `tokio::io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 307 | `poll_shutdown`  | `tokio::io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 316 | `poll_write`  | `futures_io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 324 | `poll_flush`  | `futures_io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 328 | `poll_close`  | `futures_io::AsyncWrite for Compat<T>` | Trait impl | I/O trait impl |  |
| 334 | `poll_seek`  | `futures_io::AsyncSeek for Compat<T>` | Trait impl | I/O trait impl |  |
| 352 | `start_seek`  | `tokio::io::AsyncSeek for Compat<T>` | Trait impl | I/O trait impl |  |
| 357 | `poll_complete`  | `tokio::io::AsyncSeek for Compat<T>` | Trait impl | I/O trait impl |  |
| 376 | `as_raw_fd`  | `std::os::unix::io::AsRawFd for Compat<T>` | Trait impl | OS handle access |  |
| 383 | `as_raw_handle`  | `std::os::windows::io::AsRawHandle for Compat<T>` | Trait impl | OS handle access |  |

## `tokio-util/src/context.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 119 | `new`  | `TokioContext<F>` | Public API | Constructor | Associate the provided future with the context of the runtime behind the provided `Handle`. |
| 127 | `handle`  | `TokioContext<F>` | Public API | Handle / reference plumbing | Obtain a reference to the handle inside this `TokioContext`. |
| 132 | `into_inner`  | `TokioContext<F>` | Public API | Conversion | Remove the association between the Tokio runtime and the wrapped future. |
| 140 | `poll`  | `Future for TokioContext<F>` | Trait impl | Future impl (poll) |  |
| 189 | `wrap`  | `trait RuntimeExt` | Trait method (declaration/default) | Other / internal logic | Create a [`TokioContext`] that wraps the provided future and runs it in this runtime's context. |
| 193 | `wrap`  | `RuntimeExt for Runtime` | Trait impl | Other / internal logic |  |

## `tokio-util/src/either.rs` (18)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 90 | `poll`  | `Future for Either<L, R>` | Trait impl | Future impl (poll) |  |
| 100 | `poll_read`  | `AsyncRead for Either<L, R>` | Trait impl | I/O trait impl |  |
| 114 | `poll_fill_buf`  | `AsyncBufRead for Either<L, R>` | Trait impl | I/O trait impl |  |
| 118 | `consume`  | `AsyncBufRead for Either<L, R>` | Trait impl | I/O trait impl |  |
| 128 | `start_seek`  | `AsyncSeek for Either<L, R>` | Trait impl | I/O trait impl |  |
| 132 | `poll_complete`  | `AsyncSeek for Either<L, R>` | Trait impl | I/O trait impl |  |
| 142 | `poll_write`  | `AsyncWrite for Either<L, R>` | Trait impl | I/O trait impl |  |
| 146 | `poll_flush`  | `AsyncWrite for Either<L, R>` | Trait impl | I/O trait impl |  |
| 150 | `poll_shutdown`  | `AsyncWrite for Either<L, R>` | Trait impl | I/O trait impl |  |
| 154 | `poll_write_vectored`  | `AsyncWrite for Either<L, R>` | Trait impl | I/O trait impl |  |
| 162 | `is_write_vectored`  | `AsyncWrite for Either<L, R>` | Trait impl | I/O trait impl |  |
| 177 | `poll_next`  | `futures_core::stream::Stream for Either<L, R>` | Trait impl | Stream impl |  |
| 189 | `poll_ready`  | `futures_sink::Sink<Item> for Either<L, R>` | Trait impl | Sink impl |  |
| 196 | `start_send`  | `futures_sink::Sink<Item> for Either<L, R>` | Trait impl | Sink impl |  |
| 200 | `poll_flush`  | `futures_sink::Sink<Item> for Either<L, R>` | Trait impl | Sink impl |  |
| 207 | `poll_close`  | `futures_sink::Sink<Item> for Either<L, R>` | Trait impl | Sink impl |  |
| 222 | `either_is_stream` 🅰 |  | Test | Async operation |  |
| 229 | `either_is_async_read` 🅰 |  | Test | Async operation |  |

## `tokio-util/src/future.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `timeout`  | `trait FutureExt` | Trait method (declaration/default) | Time / timers | A wrapper around [`tokio::time::timeout`], with the advantage that it is easier to write fluent call chains. |
| 54 | `timeout_at`  | `trait FutureExt` | Trait method (declaration/default) | Other / internal logic | A wrapper around [`tokio::time::timeout_at`], with the advantage that it is easier to write fluent call chains. |
| 89 | `with_cancellation_token`  | `trait FutureExt` | Trait method (declaration/default) | Constructor | Similar to [`CancellationToken::run_until_cancelled`], but with the advantage that it is easier to write fluent call chains. |
| 126 | `with_cancellation_token_owned`  | `trait FutureExt` | Trait method (declaration/default) | Constructor | Similar to [`CancellationToken::run_until_cancelled_owned`], but with the advantage that it is easier to write fluent call chains. |

