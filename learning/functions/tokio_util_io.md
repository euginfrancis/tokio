# `tokio-util::io` — 100 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 54 |
| Public API | 35 |
| Private helper | 11 |

## `tokio-util/src/io/copy_to_bytes.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `new`  | `CopyToBytes<S>` | Public API | Constructor | Creates a new [`CopyToBytes`]. |
| 31 | `get_ref`  | `CopyToBytes<S>` | Public API | Accessor / query | Gets a reference to the underlying sink. |
| 36 | `get_mut`  | `CopyToBytes<S>` | Public API | Accessor / query | Gets a mutable reference to the underlying sink. |
| 41 | `into_inner`  | `CopyToBytes<S>` | Public API | Conversion | Consumes this [`CopyToBytes`], returning the underlying sink. |
| 52 | `poll_ready`  | `Sink<&'a [u8]> for CopyToBytes<S>` | Trait impl | Sink impl |  |
| 56 | `start_send`  | `Sink<&'a [u8]> for CopyToBytes<S>` | Trait impl | Sink impl |  |
| 62 | `poll_flush`  | `Sink<&'a [u8]> for CopyToBytes<S>` | Trait impl | Sink impl |  |
| 66 | `poll_close`  | `Sink<&'a [u8]> for CopyToBytes<S>` | Trait impl | Sink impl |  |
| 73 | `poll_next`  | `Stream for CopyToBytes<S>` | Trait impl | Stream impl |  |

## `tokio-util/src/io/inspect.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `new`  | `InspectReader<R, F>` | Public API | Constructor | Create a new `InspectReader`, wrapping `reader` and calling `f` for the new data supplied by each read call. |
| 35 | `get_ref`  | `InspectReader<R, F>` | Public API | Accessor / query | Acquires a reference to the underlying reader. |
| 42 | `get_mut`  | `InspectReader<R, F>` | Public API | Accessor / query | Acquires a mutable reference to the underlying reader. |
| 49 | `get_pin_mut`  | `InspectReader<R, F>` | Public API | Accessor / query | Acquires a pinned mutable reference to the underlying reader. |
| 54 | `into_inner`  | `InspectReader<R, F>` | Public API | Conversion | Consumes the `InspectReader`, returning the wrapped reader |
| 60 | `poll_read`  | `AsyncRead for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 74 | `poll_write`  | `AsyncWrite for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 82 | `poll_flush`  | `AsyncWrite for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 89 | `poll_shutdown`  | `AsyncWrite for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 96 | `poll_write_vectored`  | `AsyncWrite for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 104 | `is_write_vectored`  | `AsyncWrite for InspectReader<R, F>` | Trait impl | I/O trait impl |  |
| 127 | `new`  | `InspectWriter<W, F>` | Public API | Constructor | Create a new `InspectWriter`, wrapping `write` and calling `f` for the data successfully written by each write call. |
| 136 | `get_ref`  | `InspectWriter<W, F>` | Public API | Accessor / query | Acquires a reference to the underlying writer. |
| 143 | `get_mut`  | `InspectWriter<W, F>` | Public API | Accessor / query | Acquires a mutable reference to the underlying writer. |
| 150 | `get_pin_mut`  | `InspectWriter<W, F>` | Public API | Accessor / query | Acquires a pinned mutable reference to the underlying writer. |
| 155 | `into_inner`  | `InspectWriter<W, F>` | Public API | Conversion | Consumes the `InspectWriter`, returning the wrapped writer |
| 161 | `poll_write`  | `AsyncWrite for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |
| 172 | `poll_flush`  | `AsyncWrite for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |
| 177 | `poll_shutdown`  | `AsyncWrite for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |
| 182 | `poll_write_vectored`  | `AsyncWrite for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |
| 204 | `is_write_vectored`  | `AsyncWrite for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |
| 210 | `poll_read`  | `AsyncRead for InspectWriter<W, F>` | Trait impl | I/O trait impl |  |

## `tokio-util/src/io/read_arc.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `read_exact_arc` 🅰 |  | Public API | I/O operation | Read data from an `AsyncRead` into an `Arc`. |

## `tokio-util/src/io/read_buf.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `read_buf` 🅰 |  | Public API | I/O operation | Read data from an `AsyncRead` into an implementer of the [`BufMut`] trait. |

## `tokio-util/src/io/reader_stream.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 68 | `new`  | `ReaderStream<R>` | Public API | Constructor | Convert an [`AsyncRead`] into a [`Stream`] with item type `Result<Bytes, std::io::Error>`. |
| 82 | `with_capacity`  | `ReaderStream<R>` | Public API | Constructor | Convert an [`AsyncRead`] into a [`Stream`] with item type `Result<Bytes, std::io::Error>`, with a specific read buffer initial capacity. |
| 93 | `poll_next`  | `Stream for ReaderStream<R>` | Trait impl | Stream impl |  |

## `tokio-util/src/io/simplex.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 39 | `with_capacity`  | `Inner` | Private helper | Constructor |  |
| 49 | `register_receiver_waker`  | `Inner` | Private helper | I/O registration |  |
| 56 | `register_sender_waker`  | `Inner` | Private helper | I/O registration |  |
| 63 | `take_receiver_waker`  | `Inner` | Private helper | Data movement |  |
| 67 | `take_sender_waker`  | `Inner` | Private helper | Data movement |  |
| 71 | `is_closed`  | `Inner` | Private helper | Accessor / query |  |
| 75 | `close_receiver`  | `Inner` | Private helper | Data movement |  |
| 80 | `close_sender`  | `Inner` | Private helper | Data movement |  |
| 107 | `drop`  | `Drop for Receiver` | Trait impl | Drop / cleanup | This also wakes up the [`Sender`]. |
| 120 | `poll_read`  | `AsyncRead for Receiver` | Trait impl | I/O trait impl |  |
| 183 | `drop`  | `Drop for Sender` | Trait impl | Drop / cleanup | This also wakes up the [`Receiver`]. |
| 200 | `poll_write`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl | # Errors This method will return [`IoErrorKind::BrokenPipe`] if the channel has been closed. |
| 250 | `poll_flush`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl | # Errors This method will return [`IoErrorKind::BrokenPipe`] if the channel has been closed. |
| 265 | `poll_shutdown`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl | After returns [`Poll::Ready`], all the following call to [`Sender::poll_write`] and [`Sender::poll_flush`] will return error. |
| 278 | `is_write_vectored`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 282 | `poll_write_vectored`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 355 | `new`  |  | Public API | Constructor | Create a simplex channel. |

## `tokio-util/src/io/sink_writer.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 72 | `new`  | `SinkWriter<S>` | Public API | Constructor | Creates a new [`SinkWriter`]. |
| 77 | `get_ref`  | `SinkWriter<S>` | Public API | Accessor / query | Gets a reference to the underlying sink. |
| 82 | `get_mut`  | `SinkWriter<S>` | Public API | Accessor / query | Gets a mutable reference to the underlying sink. |
| 87 | `into_inner`  | `SinkWriter<S>` | Public API | Conversion | Consumes this [`SinkWriter`], returning the underlying sink. |
| 96 | `poll_write`  | `AsyncWrite for SinkWriter<S>` | Trait impl | I/O trait impl |  |
| 110 | `poll_flush`  | `AsyncWrite for SinkWriter<S>` | Trait impl | I/O trait impl |  |
| 114 | `poll_shutdown`  | `AsyncWrite for SinkWriter<S>` | Trait impl | I/O trait impl |  |
| 121 | `poll_next`  | `Stream for SinkWriter<S>` | Trait impl | Stream impl |  |
| 127 | `poll_read`  | `AsyncRead for SinkWriter<S>` | Trait impl | I/O trait impl |  |

## `tokio-util/src/io/stream_reader.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 179 | `new`  | `StreamReader<S, B>` | Public API | Constructor | Convert a stream of byte chunks into an [`AsyncRead`]. |
| 188 | `has_chunk`  | `StreamReader<S, B>` | Private helper | Accessor / query | Do we have a chunk and is it non-empty? |
| 199 | `into_inner_with_chunk`  | `StreamReader<S, B>` | Public API | Conversion | Consumes this `StreamReader`, returning a Tuple consisting of the underlying stream and an Option of the internal buffer, which is Some in case the buffer contains elements. |
| 212 | `get_ref`  | `StreamReader<S, B>` | Public API | Accessor / query | Gets a reference to the underlying stream. |
| 219 | `get_mut`  | `StreamReader<S, B>` | Public API | Accessor / query | Gets a mutable reference to the underlying stream. |
| 226 | `get_pin_mut`  | `StreamReader<S, B>` | Public API | Accessor / query | Gets a pinned mutable reference to the underlying stream. |
| 237 | `into_inner`  | `StreamReader<S, B>` | Public API | Conversion | Consumes this `BufWriter`, returning the underlying stream. |
| 248 | `poll_read`  | `AsyncRead for StreamReader<S, B>` | Trait impl | I/O trait impl |  |
| 276 | `poll_fill_buf`  | `AsyncBufRead for StreamReader<S, B>` | Trait impl | I/O trait impl |  |
| 300 | `consume`  | `AsyncBufRead for StreamReader<S, B>` | Trait impl | I/O trait impl |  |
| 326 | `project`  | `StreamReader<S, B>` | Private helper | Combinator / iteration |  |
| 340 | `poll_ready`  | `Sink<T> for StreamReader<S, B>` | Trait impl | Sink impl |  |
| 344 | `start_send`  | `Sink<T> for StreamReader<S, B>` | Trait impl | Sink impl |  |
| 348 | `poll_flush`  | `Sink<T> for StreamReader<S, B>` | Trait impl | Sink impl |  |
| 352 | `poll_close`  | `Sink<T> for StreamReader<S, B>` | Trait impl | Sink impl |  |

## `tokio-util/src/io/sync_bridge.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 270 | `fill_buf`  | `BufRead for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 275 | `consume`  | `BufRead for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 280 | `read_until`  | `BufRead for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 285 | `read_line`  | `BufRead for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 292 | `read`  | `Read for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 297 | `read_to_end`  | `Read for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 302 | `read_to_string`  | `Read for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 307 | `read_exact`  | `Read for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 316 | `write`  | `Write for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 321 | `flush`  | `Write for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 326 | `write_all`  | `Write for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 331 | `write_vectored`  | `Write for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 338 | `seek`  | `Seek for SyncIoBridge<T>` | Trait impl | I/O operation |  |
| 350 | `is_write_vectored`  | `SyncIoBridge<T>` | Public API | Accessor / query | Determines if the underlying [`tokio::io::AsyncWrite`] target supports efficient vectored writes. |
| 364 | `shutdown`  | `SyncIoBridge<T>` | Public API | Runtime/task control | Shutdown this writer. |
| 393 | `new`  | `SyncIoBridge<T>` | Public API | Constructor | Use a [`tokio::io::AsyncRead`] synchronously as a [`std::io::Read`] or a [`tokio::io::AsyncWrite`] as a [`std::io::Write`]. |
| 402 | `new_with_handle`  | `SyncIoBridge<T>` | Public API | Constructor | Use a [`tokio::io::AsyncRead`] synchronously as a [`std::io::Read`] or a [`tokio::io::AsyncWrite`] as a [`std::io::Write`]. |
| 407 | `into_inner`  | `SyncIoBridge<T>` | Public API | Conversion | Consume this bridge, returning the underlying stream. |
| 413 | `as_mut`  | `AsMut<T> for SyncIoBridge<T>` | Trait impl | Conversion |  |
| 419 | `as_ref`  | `AsRef<T> for SyncIoBridge<T>` | Trait impl | Conversion |  |

## `tokio-util/src/io/write_all_vectored.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 92 | `write_all_vectored`  |  | Public API | I/O operation | Like [`write_all`] but writes all data from multiple buffers into this writer. |
| 112 | `poll`  | `Future for WriteAllVectored<'_, '_, W>` | Trait impl | Future impl (poll) |  |
| 140 | `advance_slices`  |  | Private helper | Other / internal logic |  |

