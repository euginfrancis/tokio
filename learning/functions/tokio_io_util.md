# `tokio::io::util` — 273 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 90 |
| Trait method (declaration/default) | 67 |
| Public API | 47 |
| Crate-internal | 32 |
| Private helper | 18 |
| Test | 11 |
| Inside macro_rules! | 8 |

## `tokio/src/io/util/async_buf_read_ext.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 96 | `read_until`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | I/O operation | Reads all bytes into `buf` until the delimiter `byte` or EOF is reached. |
| 199 | `read_line`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | I/O operation | Reads all bytes until a newline (the 0xA byte) is reached, and append them to the provided buffer. |
| 240 | `split`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | Combinator / iteration | Returns a stream of the contents of this reader split on the byte `byte`. |
| 277 | `fill_buf`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | I/O operation | Returns the contents of the internal buffer, filling it with more data from the inner reader if it is empty. |
| 299 | `consume`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | I/O operation | Tells this buffer that `amt` bytes have been consumed from the buffer, so they should no longer be returned in calls to [`read`]. |
| 348 | `lines`  | `trait AsyncBufReadExt` | Trait method (declaration/default) | Other / internal logic | Returns a stream over the lines of this reader. |

## `tokio/src/io/util/async_read_ext.rs` (29)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 98 | `chain`  | `trait AsyncReadExt` | Trait method (declaration/default) | Combinator / iteration | Creates a new `AsyncRead` instance that chains this stream with `next`. |
| 177 | `read`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Pulls some bytes from this source into the specified buffer, returning how many bytes were read. |
| 258 | `read_buf`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Pulls some bytes from this source into the specified buffer, advancing the buffer's internal cursor. |
| 324 | `read_exact`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads the exact number of bytes required to fill `buf`. |
| 374 | `read_u8`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 8 bit integer from the underlying reader. |
| 418 | `read_i8`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads a signed 8 bit integer from the underlying reader. |
| 462 | `read_u16`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 16-bit integer in big-endian order from the underlying reader. |
| 506 | `read_i16`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads a signed 16-bit integer in big-endian order from the underlying reader. |
| 549 | `read_u32`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 32-bit integer in big-endian order from the underlying reader. |
| 593 | `read_i32`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads a signed 32-bit integer in big-endian order from the underlying reader. |
| 638 | `read_u64`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 64-bit integer in big-endian order from the underlying reader. |
| 681 | `read_i64`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an signed 64-bit integer in big-endian order from the underlying reader. |
| 727 | `read_u128`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 128-bit integer in big-endian order from the underlying reader. |
| 773 | `read_i128`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an signed 128-bit integer in big-endian order from the underlying reader. |
| 816 | `read_f32`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an 32-bit floating point type in big-endian order from the underlying reader. |
| 861 | `read_f64`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an 64-bit floating point type in big-endian order from the underlying reader. |
| 905 | `read_u16_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 16-bit integer in little-endian order from the underlying reader. |
| 949 | `read_i16_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads a signed 16-bit integer in little-endian order from the underlying reader. |
| 992 | `read_u32_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 32-bit integer in little-endian order from the underlying reader. |
| 1036 | `read_i32_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads a signed 32-bit integer in little-endian order from the underlying reader. |
| 1081 | `read_u64_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 64-bit integer in little-endian order from the underlying reader. |
| 1124 | `read_i64_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an signed 64-bit integer in little-endian order from the underlying reader. |
| 1170 | `read_u128_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an unsigned 128-bit integer in little-endian order from the underlying reader. |
| 1216 | `read_i128_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an signed 128-bit integer in little-endian order from the underlying reader. |
| 1259 | `read_f32_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an 32-bit floating point type in little-endian order from the underlying reader. |
| 1304 | `read_f64_le`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads an 64-bit floating point type in little-endian order from the underlying reader. |
| 1356 | `read_to_end`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads all bytes until EOF in this source, placing them into `buf`. |
| 1406 | `read_to_string`  | `trait AsyncReadExt` | Trait method (declaration/default) | I/O operation | Reads all bytes until EOF in this source, appending them to `buf`. |
| 1447 | `take`  | `trait AsyncReadExt` | Trait method (declaration/default) | Data movement | Creates an adaptor which reads at most `limit` bytes from it. |

## `tokio/src/io/util/async_seek_ext.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 66 | `seek`  | `trait AsyncSeekExt` | Trait method (declaration/default) | I/O operation | Creates a future which will seek an IO object, and then yield the new position in the object and the object itself. |
| 76 | `rewind`  | `trait AsyncSeekExt` | Trait method (declaration/default) | Other / internal logic | Creates a future which will rewind to the beginning of the stream. |
| 87 | `stream_position`  | `trait AsyncSeekExt` | Trait method (declaration/default) | Other / internal logic | Creates a future which will return the current seek position from the start of the stream. |

## `tokio/src/io/util/async_write_ext.rs` (29)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 130 | `write`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a buffer into this writer, returning how many bytes were written. |
| 182 | `write_vectored`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Like [`write`], except that it writes from a slice of buffers. |
| 266 | `write_buf`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a buffer into this writer, advancing the buffer's internal cursor. |
| 336 | `write_all_buf`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Attempts to write an entire buffer into this writer. |
| 392 | `write_all`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Attempts to write an entire buffer into this writer. |
| 435 | `write_u8`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 8-bit integer to the underlying writer. |
| 472 | `write_i8`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a signed 8-bit integer to the underlying writer. |
| 510 | `write_u16`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 16-bit integer in big-endian order to the underlying writer. |
| 548 | `write_i16`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a signed 16-bit integer in big-endian order to the underlying writer. |
| 586 | `write_u32`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 32-bit integer in big-endian order to the underlying writer. |
| 624 | `write_i32`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a signed 32-bit integer in big-endian order to the underlying writer. |
| 662 | `write_u64`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 64-bit integer in big-endian order to the underlying writer. |
| 700 | `write_i64`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an signed 64-bit integer in big-endian order to the underlying writer. |
| 740 | `write_u128`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 128-bit integer in big-endian order to the underlying writer. |
| 780 | `write_i128`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an signed 128-bit integer in big-endian order to the underlying writer. |
| 817 | `write_f32`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an 32-bit floating point type in big-endian order to the underlying writer. |
| 856 | `write_f64`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an 64-bit floating point type in big-endian order to the underlying writer. |
| 894 | `write_u16_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 16-bit integer in little-endian order to the underlying writer. |
| 932 | `write_i16_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a signed 16-bit integer in little-endian order to the underlying writer. |
| 970 | `write_u32_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 32-bit integer in little-endian order to the underlying writer. |
| 1008 | `write_i32_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes a signed 32-bit integer in little-endian order to the underlying writer. |
| 1046 | `write_u64_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 64-bit integer in little-endian order to the underlying writer. |
| 1084 | `write_i64_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an signed 64-bit integer in little-endian order to the underlying writer. |
| 1124 | `write_u128_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an unsigned 128-bit integer in little-endian order to the underlying writer. |
| 1164 | `write_i128_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an signed 128-bit integer in little-endian order to the underlying writer. |
| 1201 | `write_f32_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an 32-bit floating point type in little-endian order to the underlying writer. |
| 1240 | `write_f64_le`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Writes an 64-bit floating point type in little-endian order to the underlying writer. |
| 1286 | `flush`  | `trait AsyncWriteExt` | Trait method (declaration/default) | I/O operation | Flushes this output stream, ensuring that all intermediately buffered contents reach their destination. |
| 1328 | `shutdown`  | `trait AsyncWriteExt` | Trait method (declaration/default) | Runtime/task control | Shuts down the output stream, ensuring that the value can be dropped cleanly. |

## `tokio/src/io/util/buf_reader.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 40 | `new`  | `BufReader<R>` | Public API | Constructor | Creates a new `BufReader` with a default buffer capacity. |
| 50 | `with_capacity`  | `BufReader<R>` | Public API | Constructor | Creates a new `BufReader` with the specified buffer capacity. |
| 65 | `get_ref`  | `BufReader<R>` | Public API | Accessor / query | Gets a reference to the underlying reader. |
| 72 | `get_mut`  | `BufReader<R>` | Public API | Accessor / query | Gets a mutable reference to the underlying reader. |
| 79 | `get_pin_mut`  | `BufReader<R>` | Public API | Accessor / query | Gets a pinned mutable reference to the underlying reader. |
| 86 | `into_inner`  | `BufReader<R>` | Public API | Conversion | Consumes this `BufReader`, returning the underlying reader. |
| 93 | `buffer`  | `BufReader<R>` | Public API | Other / internal logic | Returns a reference to the internally buffered data. |
| 99 | `discard_buffer`  | `BufReader<R>` | Private helper | Other / internal logic | Invalidates all data in the internal buffer. |
| 107 | `poll_read`  | `AsyncRead for BufReader<R>` | Trait impl | I/O trait impl |  |
| 129 | `poll_fill_buf`  | `AsyncBufRead for BufReader<R>` | Trait impl | I/O trait impl |  |
| 146 | `consume`  | `AsyncBufRead for BufReader<R>` | Trait impl | I/O trait impl |  |
| 183 | `start_seek`  | `AsyncSeek for BufReader<R>` | Trait impl | I/O trait impl |  |
| 193 | `poll_complete`  | `AsyncSeek for BufReader<R>` | Trait impl | I/O trait impl |  |
| 268 | `poll_write`  | `AsyncWrite for BufReader<R>` | Trait impl | I/O trait impl |  |
| 276 | `poll_write_vectored`  | `AsyncWrite for BufReader<R>` | Trait impl | I/O trait impl |  |
| 284 | `is_write_vectored`  | `AsyncWrite for BufReader<R>` | Trait impl | I/O trait impl |  |
| 288 | `poll_flush`  | `AsyncWrite for BufReader<R>` | Trait impl | I/O trait impl |  |
| 292 | `poll_shutdown`  | `AsyncWrite for BufReader<R>` | Trait impl | I/O trait impl |  |
| 298 | `fmt`  | `fmt::Debug for BufReader<R>` | Trait impl | Formatting |  |
| 314 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/buf_stream.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 29 | `new`  | `BufStream<RW>` | Public API | Constructor | Wraps a type in both [`BufWriter`] and [`BufReader`]. |
| 44 | `with_capacity`  | `BufStream<RW>` | Public API | Constructor | Creates a `BufStream` with the specified [`BufReader`] capacity and [`BufWriter`] capacity. |
| 60 | `get_ref`  | `BufStream<RW>` | Public API | Accessor / query | Gets a reference to the underlying I/O object. |
| 67 | `get_mut`  | `BufStream<RW>` | Public API | Accessor / query | Gets a mutable reference to the underlying I/O object. |
| 74 | `get_pin_mut`  | `BufStream<RW>` | Public API | Accessor / query | Gets a pinned mutable reference to the underlying I/O object. |
| 81 | `into_inner`  | `BufStream<RW>` | Public API | Conversion | Consumes this `BufStream`, returning the underlying I/O object. |
| 87 | `from`  | `From<BufReader<BufWriter<RW>>> for BufStream<RW>` | Trait impl | Conversion |  |
| 93 | `from`  | `From<BufWriter<BufReader<RW>>> for BufStream<RW>` | Trait impl | Conversion |  |
| 127 | `poll_write`  | `AsyncWrite for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 135 | `poll_write_vectored`  | `AsyncWrite for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 143 | `is_write_vectored`  | `AsyncWrite for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 147 | `poll_flush`  | `AsyncWrite for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 151 | `poll_shutdown`  | `AsyncWrite for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 157 | `poll_read`  | `AsyncRead for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 185 | `start_seek`  | `AsyncSeek for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 189 | `poll_complete`  | `AsyncSeek for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 195 | `poll_fill_buf`  | `AsyncBufRead for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 199 | `consume`  | `AsyncBufRead for BufStream<RW>` | Trait impl | I/O trait impl |  |
| 209 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/buf_writer.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 44 | `new`  | `BufWriter<W>` | Public API | Constructor | Creates a new `BufWriter` with a default buffer capacity. |
| 49 | `with_capacity`  | `BufWriter<W>` | Public API | Constructor | Creates a new `BufWriter` with the specified buffer capacity. |
| 58 | `flush_buf`  | `BufWriter<W>` | Private helper | I/O operation |  |
| 88 | `get_ref`  | `BufWriter<W>` | Public API | Accessor / query | Gets a reference to the underlying writer. |
| 95 | `get_mut`  | `BufWriter<W>` | Public API | Accessor / query | Gets a mutable reference to the underlying writer. |
| 102 | `get_pin_mut`  | `BufWriter<W>` | Public API | Accessor / query | Gets a pinned mutable reference to the underlying writer. |
| 109 | `into_inner`  | `BufWriter<W>` | Public API | Conversion | Consumes this `BufWriter`, returning the underlying writer. |
| 114 | `buffer`  | `BufWriter<W>` | Public API | Other / internal logic | Returns a reference to the internally buffered data. |
| 120 | `poll_write`  | `AsyncWrite for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 137 | `poll_write_vectored`  | `AsyncWrite for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 199 | `is_write_vectored`  | `AsyncWrite for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 203 | `poll_flush`  | `AsyncWrite for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 208 | `poll_shutdown`  | `AsyncWrite for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 228 | `start_seek`  | `AsyncSeek for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 236 | `poll_complete`  | `AsyncSeek for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 271 | `poll_read`  | `AsyncRead for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 281 | `poll_fill_buf`  | `AsyncBufRead for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 285 | `consume`  | `AsyncBufRead for BufWriter<W>` | Trait impl | I/O trait impl |  |
| 291 | `fmt`  | `fmt::Debug for BufWriter<W>` | Trait impl | Formatting |  |
| 308 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/chain.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `chain`  |  | Crate-internal | Combinator / iteration |  |
| 40 | `get_ref`  | `Chain<T, U>` | Public API | Accessor / query | Gets references to the underlying readers in this `Chain`. |
| 49 | `get_mut`  | `Chain<T, U>` | Public API | Accessor / query | Gets mutable references to the underlying readers in this `Chain`. |
| 58 | `get_pin_mut`  | `Chain<T, U>` | Public API | Accessor / query | Gets pinned mutable references to the underlying readers in this `Chain`. |
| 64 | `into_inner`  | `Chain<T, U>` | Public API | Conversion | Consumes the `Chain`, returning the wrapped readers. |
| 74 | `fmt`  | `fmt::Debug for Chain<T, U>` | Trait impl | Formatting |  |
| 87 | `poll_read`  | `AsyncRead for Chain<T, U>` | Trait impl | I/O trait impl |  |
| 114 | `poll_fill_buf`  | `AsyncBufRead for Chain<T, U>` | Trait impl | I/O trait impl |  |
| 128 | `consume`  | `AsyncBufRead for Chain<T, U>` | Trait impl | I/O trait impl |  |
| 143 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/copy.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `new`  | `CopyBuffer` | Crate-internal | Constructor |  |
| 30 | `poll_fill_buf`  | `CopyBuffer` | Private helper | Poll function |  |
| 56 | `poll_write_buf`  | `CopyBuffer` | Private helper | Poll function |  |
| 83 | `poll_copy`  | `CopyBuffer` | Crate-internal | Poll function |  |
| 287 | `copy` 🅰 |  | Public API | I/O operation | Asynchronously copies the entire contents of a reader into a writer. |
| 307 | `poll`  | `Future for Copy<'_, R, W>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/copy_bidirectional.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `transfer_one_direction`  |  | Private helper | Other / internal logic |  |
| 76 | `copy_bidirectional` 🅰 |  | Public API | I/O operation | Copies data in both directions between `a` and `b`. |
| 99 | `copy_bidirectional_with_sizes` 🅰 |  | Public API | I/O operation | Copies data in both directions between `a` and `b` using buffers of the specified size. |
| 127 | `copy_bidirectional_impl` 🅰 |  | Private helper | I/O operation |  |

## `tokio/src/io/util/copy_buf.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 70 | `copy_buf` 🅰 |  | Public API | I/O operation | Asynchronously copies the entire contents of a reader into a writer. |
| 91 | `poll`  | `Future for CopyBuf<'_, R, W>` | Trait impl | Future impl (poll) |  |
| 172 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/empty.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 62 | `empty`  |  | Public API | Other / internal logic | Creates a value that is always at EOF for reads, and ignores all data written. |
| 69 | `poll_read`  | `AsyncRead for Empty` | Trait impl | I/O trait impl |  |
| 82 | `poll_fill_buf`  | `AsyncBufRead for Empty` | Trait impl | I/O trait impl |  |
| 89 | `consume`  | `AsyncBufRead for Empty` | Trait impl | I/O trait impl |  |
| 94 | `poll_write`  | `AsyncWrite for Empty` | Trait impl | I/O trait impl |  |
| 105 | `poll_flush`  | `AsyncWrite for Empty` | Trait impl | I/O trait impl |  |
| 112 | `poll_shutdown`  | `AsyncWrite for Empty` | Trait impl | I/O trait impl |  |
| 119 | `is_write_vectored`  | `AsyncWrite for Empty` | Trait impl | I/O trait impl |  |
| 124 | `poll_write_vectored`  | `AsyncWrite for Empty` | Trait impl | I/O trait impl |  |
| 138 | `start_seek`  | `AsyncSeek for Empty` | Trait impl | I/O trait impl |  |
| 143 | `poll_complete`  | `AsyncSeek for Empty` | Trait impl | I/O trait impl |  |
| 151 | `fmt`  | `fmt::Debug for Empty` | Trait impl | Formatting |  |
| 161 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/fill_buf.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `fill_buf`  |  | Crate-internal | I/O operation |  |
| 34 | `poll`  | `Future for FillBuf<'a, R>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/flush.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `flush`  |  | Crate-internal | I/O operation | Creates a future which will entirely flush an I/O object. |
| 43 | `poll`  | `Future for Flush<'_, A>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/lines.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `lines`  |  | Crate-internal | Other / internal logic |  |
| 65 | `next_line` 🅰 | `Lines<R>` | Public API | Async operation | Returns the next line in the stream. |
| 72 | `get_mut`  | `Lines<R>` | Public API | Accessor / query | Obtains a mutable reference to the underlying reader. |
| 77 | `get_ref`  | `Lines<R>` | Public API | Accessor / query | Obtains a reference to the underlying reader. |
| 85 | `into_inner`  | `Lines<R>` | Public API | Conversion | Unwraps this `Lines<R>`, returning the underlying reader. |
| 114 | `poll_next_line`  | `Lines<R>` | Public API | Poll function | Polls for the next line in the stream. |
| 149 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/mem.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 109 | `duplex`  |  | Public API | Other / internal logic | Create a new pair of `DuplexStream`s that act like a pair of connected sockets. |
| 132 | `poll_read`  | `AsyncRead for DuplexStream` | Trait impl | I/O trait impl |  |
| 143 | `poll_write`  | `AsyncWrite for DuplexStream` | Trait impl | I/O trait impl |  |
| 151 | `poll_write_vectored`  | `AsyncWrite for DuplexStream` | Trait impl | I/O trait impl |  |
| 159 | `is_write_vectored`  | `AsyncWrite for DuplexStream` | Trait impl | I/O trait impl |  |
| 164 | `poll_flush`  | `AsyncWrite for DuplexStream` | Trait impl | I/O trait impl |  |
| 172 | `poll_shutdown`  | `AsyncWrite for DuplexStream` | Trait impl | I/O trait impl |  |
| 181 | `drop`  | `Drop for DuplexStream` | Trait impl | Drop / cleanup |  |
| 221 | `simplex`  |  | Public API | Other / internal logic | Creates unidirectional buffer that acts like in memory pipe. |
| 237 | `new_unsplit`  | `SimplexStream` | Public API | Constructor | Creates unidirectional buffer that acts like in memory pipe. |
| 248 | `close_write`  | `SimplexStream` | Private helper | Data movement |  |
| 256 | `close_read`  | `SimplexStream` | Private helper | Data movement |  |
| 264 | `poll_read_internal`  | `SimplexStream` | Private helper | Poll function |  |
| 293 | `poll_write_internal`  | `SimplexStream` | Private helper | Poll function |  |
| 319 | `poll_write_vectored_internal`  | `SimplexStream` | Private helper | Poll function |  |
| 357 | `poll_read`  | `AsyncRead for SimplexStream` | Trait impl | I/O trait impl |  |
| 374 | `poll_read`  | `AsyncRead for SimplexStream` | Trait impl | I/O trait impl |  |
| 387 | `poll_write`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 404 | `poll_write`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 415 | `poll_write_vectored`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 432 | `poll_write_vectored`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 442 | `is_write_vectored`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 446 | `poll_flush`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |
| 450 | `poll_shutdown`  | `AsyncWrite for SimplexStream` | Trait impl | I/O trait impl |  |

## `tokio/src/io/util/mod.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 91 | `poll_proceed_and_make_progress`  |  | Private helper | Poll function |  |
| 99 | `poll_proceed_and_make_progress`  |  | Private helper | Poll function |  |

## `tokio/src/io/util/read.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `read`  |  | Crate-internal | I/O operation | Tries to read some bytes directly into the given `buf` in asynchronous manner, returning a future type. |
| 49 | `poll`  | `Future for Read<'_, R>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_buf.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `read_buf`  |  | Crate-internal | I/O operation |  |
| 42 | `poll`  | `Future for ReadBuf<'_, R, B>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_exact.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `read_exact`  |  | Crate-internal | I/O operation | A future which can be used to easily read exactly enough bytes to fill a buffer. |
| 43 | `eof`  |  | Private helper | Other / internal logic |  |
| 53 | `poll`  | `Future for ReadExact<'_, A>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_int.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `new`  | `$name<R>` | Inside macro_rules! | Constructor |  |
| 48 | `poll`  | `Future for $name<R>` | Inside macro_rules! | Future impl (poll) |  |
| 97 | `new`  | `$name<R>` | Inside macro_rules! | Constructor |  |
| 111 | `poll`  | `Future for $name<R>` | Inside macro_rules! | Future impl (poll) |  |

## `tokio/src/io/util/read_line.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `read_line`  |  | Crate-internal | I/O operation |  |
| 46 | `put_back_original_data`  |  | Private helper | Other / internal logic |  |
| 56 | `finish_string_read`  |  | Crate-internal | Other / internal logic | This handles the various failure cases and puts the string back into `output`. |
| 92 | `read_line_internal`  |  | Private helper | I/O operation |  |
| 112 | `poll`  | `Future for ReadLine<'_, R>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_to_end.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `read_to_end`  |  | Crate-internal | I/O operation |  |
| 39 | `read_to_end_internal`  |  | Crate-internal | I/O operation |  |
| 61 | `poll_read_to_end`  |  | Private helper | Poll function | Tries to read from the provided [`AsyncRead`]. |
| 139 | `poll`  | `Future for ReadToEnd<'_, A>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_to_string.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `read_to_string`  |  | Crate-internal | I/O operation |  |
| 50 | `read_to_string_internal`  |  | Private helper | I/O operation |  |
| 73 | `poll`  | `Future for ReadToString<'_, A>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/read_until.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `read_until`  |  | Crate-internal | I/O operation |  |
| 47 | `read_until_internal`  |  | Crate-internal | I/O operation |  |
| 80 | `poll`  | `Future for ReadUntil<'_, R>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/repeat.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 47 | `repeat`  |  | Public API | Other / internal logic | Creates an instance of an async reader that infinitely repeats one byte. |
| 54 | `poll_read`  | `AsyncRead for Repeat` | Trait impl | I/O trait impl |  |
| 71 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/shutdown.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `shutdown`  |  | Crate-internal | Runtime/task control | Creates a future which will shutdown an I/O object. |
| 42 | `poll`  | `Future for Shutdown<'_, A>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/sink.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 48 | `sink`  |  | Public API | Other / internal logic | Creates an instance of an async writer which will successfully consume all data. |
| 55 | `poll_write`  | `AsyncWrite for Sink` | Trait impl | I/O trait impl |  |
| 66 | `poll_flush`  | `AsyncWrite for Sink` | Trait impl | I/O trait impl |  |
| 73 | `poll_shutdown`  | `AsyncWrite for Sink` | Trait impl | I/O trait impl |  |
| 81 | `fmt`  | `fmt::Debug for Sink` | Trait impl | Formatting |  |
| 91 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/split.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 28 | `split`  |  | Crate-internal | Combinator / iteration |  |
| 61 | `next_segment` 🅰 | `Split<R>` | Public API | Async operation | Returns the next segment in the stream. |
| 89 | `poll_next_segment`  | `Split<R>` | Public API | Poll function | Polls for the next segment in the stream. |
| 118 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/take.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `take`  |  | Crate-internal | Data movement |  |
| 37 | `limit`  | `Take<R>` | Public API | Other / internal logic | Returns the remaining number of bytes that can be read before this instance will return EOF. |
| 45 | `set_limit`  | `Take<R>` | Public API | Configuration / setter | Sets the number of bytes that can be read before this instance will return EOF. |
| 50 | `get_ref`  | `Take<R>` | Public API | Accessor / query | Gets a reference to the underlying reader. |
| 59 | `get_mut`  | `Take<R>` | Public API | Accessor / query | Gets a mutable reference to the underlying reader. |
| 68 | `get_pin_mut`  | `Take<R>` | Public API | Accessor / query | Gets a pinned mutable reference to the underlying reader. |
| 73 | `into_inner`  | `Take<R>` | Public API | Conversion | Consumes the `Take`, returning the wrapped reader. |
| 79 | `poll_read`  | `AsyncRead for Take<R>` | Trait impl | I/O trait impl |  |
| 108 | `poll_fill_buf`  | `AsyncBufRead for Take<R>` | Trait impl | I/O trait impl |  |
| 121 | `consume`  | `AsyncBufRead for Take<R>` | Trait impl | I/O trait impl |  |
| 135 | `assert_unpin`  |  | Test | Debugging / tracing |  |

## `tokio/src/io/util/vec_with_initialized.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 36 | `take`  | `VecWithInitialized<Vec<u8>>` | Crate-internal | Data movement |  |
| 46 | `new`  | `VecWithInitialized<V>` | Crate-internal | Constructor |  |
| 56 | `reserve`  | `VecWithInitialized<V>` | Crate-internal | Other / internal logic |  |
| 68 | `is_empty`  | `VecWithInitialized<V>` | Crate-internal | Accessor / query |  |
| 72 | `get_read_buf`  | `VecWithInitialized<V>` | Crate-internal | Accessor / query |  |
| 96 | `apply_read_buf`  | `VecWithInitialized<V>` | Crate-internal | Other / internal logic |  |
| 119 | `try_small_read_first`  | `VecWithInitialized<V>` | Crate-internal | Non-blocking attempt |  |
| 136 | `into_read_buf_parts`  |  | Crate-internal | Conversion |  |

## `tokio/src/io/util/write.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `write`  |  | Crate-internal | I/O operation | Tries to write some bytes from the given `buf` to the writer in an asynchronous manner, returning a future. |
| 42 | `poll`  | `Future for Write<'_, W>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/write_all.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `write_all`  |  | Crate-internal | I/O operation |  |
| 40 | `poll`  | `Future for WriteAll<'_, W>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/write_all_buf.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `write_all_buf`  |  | Crate-internal | I/O operation | Tries to write some bytes from the given `buf` to the writer in an asynchronous manner, returning a future. |
| 44 | `poll`  | `Future for WriteAllBuf<'_, W, B>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/write_buf.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `write_buf`  |  | Crate-internal | I/O operation | Tries to write some bytes from the given `buf` to the writer in an asynchronous manner, returning a future. |
| 44 | `poll`  | `Future for WriteBuf<'_, W, B>` | Trait impl | Future impl (poll) |  |

## `tokio/src/io/util/write_int.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 31 | `new`  | `$name<W>` | Inside macro_rules! | Constructor |  |
| 49 | `poll`  | `Future for $name<W>` | Inside macro_rules! | Future impl (poll) |  |
| 93 | `new`  | `$name<W>` | Inside macro_rules! | Constructor |  |
| 108 | `poll`  | `Future for $name<W>` | Inside macro_rules! | Future impl (poll) |  |

## `tokio/src/io/util/write_vectored.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `write_vectored`  |  | Crate-internal | I/O operation |  |
| 43 | `poll`  | `Future for WriteVectored<'_, '_, W>` | Trait impl | Future impl (poll) |  |

