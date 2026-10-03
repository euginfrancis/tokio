# `tokio-util::codec` — 138 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 72 |
| Trait impl | 53 |
| Private helper | 9 |
| Trait method (declaration/default) | 4 |

## `tokio-util/src/codec/any_delimiter_codec.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 75 | `new`  | `AnyDelimiterCodec` | Public API | Constructor | Returns a `AnyDelimiterCodec` for splitting up data into chunks. |
| 103 | `new_with_max_length`  | `AnyDelimiterCodec` | Public API | Constructor | Returns a `AnyDelimiterCodec` with a maximum chunk length limit. |
| 128 | `max_length`  | `AnyDelimiterCodec` | Public API | Configuration / setter | Returns the maximum chunk length when decoding. |
| 137 | `decode`  | `Decoder for AnyDelimiterCodec` | Trait impl | Codec impl |  |
| 192 | `decode_eof`  | `Decoder for AnyDelimiterCodec` | Trait impl | Codec impl |  |
| 215 | `encode`  | `Encoder<T> for AnyDelimiterCodec` | Trait impl | Codec impl |  |
| 226 | `default`  | `Default for AnyDelimiterCodec` | Trait impl | Constructor |  |
| 244 | `fmt`  | `fmt::Display for AnyDelimiterCodecError` | Trait impl | Formatting |  |
| 255 | `from`  | `From<io::Error> for AnyDelimiterCodecError` | Trait impl | Conversion |  |

## `tokio-util/src/codec/bytes_codec.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 49 | `new`  | `BytesCodec` | Public API | Constructor | Creates a new `BytesCodec` for shipping around raw bytes. |
| 58 | `decode`  | `Decoder for BytesCodec` | Trait impl | Codec impl |  |
| 71 | `encode`  | `Encoder<Bytes> for BytesCodec` | Trait impl | Codec impl |  |
| 81 | `encode`  | `Encoder<BytesMut> for BytesCodec` | Trait impl | Codec impl |  |

## `tokio-util/src/codec/decoder.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 124 | `decode`  | `trait Decoder` | Trait method (declaration/default) | Other / internal logic | Attempts to decode a frame from the provided buffer of bytes. |
| 144 | `decode_eof`  | `trait Decoder` | Trait method (declaration/default) | Other / internal logic | A default method available to be called when there are no more bytes available to be read from the underlying I/O. |
| 178 | `framed`  | `trait Decoder` | Trait method (declaration/default) | Other / internal logic | Provides a [`Stream`] and [`Sink`] interface for reading and writing to this `Io` object, using `Decode` and `Encode` to read and write the raw data. |

## `tokio-util/src/codec/encoder.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `encode`  | `trait Encoder` | Trait method (declaration/default) | Other / internal logic | Encodes a frame into the buffer provided. |

## `tokio-util/src/codec/framed.rs` (25)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 73 | `new`  | `Framed<T, U>` | Public API | Constructor | Provides a [`Stream`] and [`Sink`] interface for reading and writing to this I/O object, using [`Decoder`] and [`Encoder`] to read and write the raw data. |
| 107 | `with_capacity`  | `Framed<T, U>` | Public API | Constructor | Provides a [`Stream`] and [`Sink`] interface for reading and writing to this I/O object, using [`Decoder`] and [`Encoder`] to read and write the raw data, with a specific read buffer initial capacity. |
| 155 | `from_parts`  | `Framed<T, U>` | Public API | Conversion | Provides a [`Stream`] and [`Sink`] interface for reading and writing to this I/O object, using [`Decoder`] and [`Encoder`] to read and write the raw data. |
| 174 | `get_ref`  | `Framed<T, U>` | Public API | Accessor / query | Returns a reference to the underlying I/O stream wrapped by `Framed`. |
| 184 | `get_mut`  | `Framed<T, U>` | Public API | Accessor / query | Returns a mutable reference to the underlying I/O stream wrapped by `Framed`. |
| 194 | `get_pin_mut`  | `Framed<T, U>` | Public API | Accessor / query | Returns a pinned mutable reference to the underlying I/O stream wrapped by `Framed`. |
| 203 | `codec`  | `Framed<T, U>` | Public API | Other / internal logic | Returns a reference to the underlying codec wrapped by `Framed`. |
| 212 | `codec_mut`  | `Framed<T, U>` | Public API | Other / internal logic | Returns a mutable reference to the underlying codec wrapped by `Framed`. |
| 221 | `map_codec`  | `Framed<T, U>` | Public API | Combinator / iteration | Maps the codec `U` to `C`, preserving the read and write buffers wrapped by `Framed`. |
| 241 | `codec_pin_mut`  | `Framed<T, U>` | Public API | Other / internal logic | Returns a mutable reference to the underlying codec wrapped by `Framed`. |
| 246 | `read_buffer`  | `Framed<T, U>` | Public API | I/O operation | Returns a reference to the read buffer. |
| 251 | `read_buffer_mut`  | `Framed<T, U>` | Public API | I/O operation | Returns a mutable reference to the read buffer. |
| 256 | `write_buffer`  | `Framed<T, U>` | Public API | I/O operation | Returns a reference to the write buffer. |
| 261 | `write_buffer_mut`  | `Framed<T, U>` | Public API | I/O operation | Returns a mutable reference to the write buffer. |
| 266 | `backpressure_boundary`  | `Framed<T, U>` | Public API | Other / internal logic | Returns backpressure boundary |
| 271 | `set_backpressure_boundary`  | `Framed<T, U>` | Public API | Configuration / setter | Updates backpressure boundary |
| 280 | `into_inner`  | `Framed<T, U>` | Public API | Conversion | Consumes the `Framed`, returning its underlying I/O stream. |
| 290 | `into_parts`  | `Framed<T, U>` | Public API | Conversion | Consumes the `Framed`, returning its underlying I/O stream, the buffer with unprocessed data, and the codec. |
| 309 | `poll_next`  | `Stream for Framed<T, U>` | Trait impl | Stream impl |  |
| 323 | `poll_ready`  | `Sink<I> for Framed<T, U>` | Trait impl | Sink impl |  |
| 327 | `start_send`  | `Sink<I> for Framed<T, U>` | Trait impl | Sink impl |  |
| 331 | `poll_flush`  | `Sink<I> for Framed<T, U>` | Trait impl | Sink impl |  |
| 335 | `poll_close`  | `Sink<I> for Framed<T, U>` | Trait impl | Sink impl |  |
| 345 | `fmt`  | `fmt::Debug for Framed<T, U>` | Trait impl | Formatting |  |
| 380 | `new`  | `FramedParts<T, U>` | Public API | Constructor | Create a new, default, `FramedParts` |

## `tokio-util/src/codec/framed_impl.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 47 | `default`  | `Default for ReadFrame` | Trait impl | Constructor |  |
| 58 | `default`  | `Default for WriteFrame` | Trait impl | Constructor |  |
| 67 | `from`  | `From<BytesMut> for ReadFrame` | Trait impl | Conversion |  |
| 84 | `from`  | `From<BytesMut> for WriteFrame` | Trait impl | Conversion |  |
| 98 | `borrow`  | `Borrow<ReadFrame> for RWFrames` | Trait impl | Combinator / iteration |  |
| 103 | `borrow_mut`  | `BorrowMut<ReadFrame> for RWFrames` | Trait impl | Combinator / iteration |  |
| 108 | `borrow`  | `Borrow<WriteFrame> for RWFrames` | Trait impl | Combinator / iteration |  |
| 113 | `borrow_mut`  | `BorrowMut<WriteFrame> for RWFrames` | Trait impl | Combinator / iteration |  |
| 125 | `poll_next`  | `Stream for FramedImpl<T, U, R>` | Trait impl | Stream impl |  |
| 263 | `poll_ready`  | `Sink<I> for FramedImpl<T, U, W>` | Trait impl | Sink impl |  |
| 271 | `start_send`  | `Sink<I> for FramedImpl<T, U, W>` | Trait impl | Sink impl |  |
| 279 | `poll_flush`  | `Sink<I> for FramedImpl<T, U, W>` | Trait impl | Sink impl |  |
| 307 | `poll_close`  | `Sink<I> for FramedImpl<T, U, W>` | Trait impl | Sink impl |  |

## `tokio-util/src/codec/framed_read.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `FramedRead<T, D>` | Public API | Constructor | Creates a new `FramedRead` with the given `decoder`. |
| 53 | `with_capacity`  | `FramedRead<T, D>` | Public API | Constructor | Creates a new `FramedRead` with the given `decoder` and a buffer of `capacity` initial size. |
| 74 | `get_ref`  | `FramedRead<T, D>` | Public API | Accessor / query | Returns a reference to the underlying I/O stream wrapped by `FramedRead`. |
| 84 | `get_mut`  | `FramedRead<T, D>` | Public API | Accessor / query | Returns a mutable reference to the underlying I/O stream wrapped by `FramedRead`. |
| 94 | `get_pin_mut`  | `FramedRead<T, D>` | Public API | Accessor / query | Returns a pinned mutable reference to the underlying I/O stream wrapped by `FramedRead`. |
| 103 | `into_inner`  | `FramedRead<T, D>` | Public API | Conversion | Consumes the `FramedRead`, returning its underlying I/O stream. |
| 108 | `decoder`  | `FramedRead<T, D>` | Public API | Other / internal logic | Returns a reference to the underlying decoder. |
| 113 | `decoder_mut`  | `FramedRead<T, D>` | Public API | Other / internal logic | Returns a mutable reference to the underlying decoder. |
| 119 | `map_decoder`  | `FramedRead<T, D>` | Public API | Combinator / iteration | Maps the decoder `D` to `C`, preserving the read buffer wrapped by `Framed`. |
| 139 | `decoder_pin_mut`  | `FramedRead<T, D>` | Public API | Other / internal logic | Returns a mutable reference to the underlying decoder. |
| 144 | `read_buffer`  | `FramedRead<T, D>` | Public API | I/O operation | Returns a reference to the read buffer. |
| 149 | `read_buffer_mut`  | `FramedRead<T, D>` | Public API | I/O operation | Returns a mutable reference to the read buffer. |
| 155 | `into_parts`  | `FramedRead<T, D>` | Public API | Conversion | Consumes the `FramedRead`, returning its underlying I/O stream, the buffer with unprocessed data, and the codec. |
| 174 | `poll_next`  | `Stream for FramedRead<T, D>` | Trait impl | Stream impl |  |
| 186 | `poll_ready`  | `Sink<I> for FramedRead<T, D>` | Trait impl | Sink impl |  |
| 190 | `start_send`  | `Sink<I> for FramedRead<T, D>` | Trait impl | Sink impl |  |
| 194 | `poll_flush`  | `Sink<I> for FramedRead<T, D>` | Trait impl | Sink impl |  |
| 198 | `poll_close`  | `Sink<I> for FramedRead<T, D>` | Trait impl | Sink impl |  |
| 208 | `fmt`  | `fmt::Debug for FramedRead<T, D>` | Trait impl | Formatting |  |

## `tokio-util/src/codec/framed_write.rs` (21)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 40 | `new`  | `FramedWrite<T, E>` | Public API | Constructor | Creates a new `FramedWrite` with the given `encoder`. |
| 52 | `with_capacity`  | `FramedWrite<T, E>` | Public API | Constructor | Creates a new `FramedWrite` with the given `encoder` and a buffer of `capacity` initial size. |
| 71 | `get_ref`  | `FramedWrite<T, E>` | Public API | Accessor / query | Returns a reference to the underlying I/O stream wrapped by `FramedWrite`. |
| 81 | `get_mut`  | `FramedWrite<T, E>` | Public API | Accessor / query | Returns a mutable reference to the underlying I/O stream wrapped by `FramedWrite`. |
| 91 | `get_pin_mut`  | `FramedWrite<T, E>` | Public API | Accessor / query | Returns a pinned mutable reference to the underlying I/O stream wrapped by `FramedWrite`. |
| 100 | `into_inner`  | `FramedWrite<T, E>` | Public API | Conversion | Consumes the `FramedWrite`, returning its underlying I/O stream. |
| 105 | `encoder`  | `FramedWrite<T, E>` | Public API | Other / internal logic | Returns a reference to the underlying encoder. |
| 110 | `encoder_mut`  | `FramedWrite<T, E>` | Public API | Other / internal logic | Returns a mutable reference to the underlying encoder. |
| 116 | `map_encoder`  | `FramedWrite<T, E>` | Public API | Combinator / iteration | Maps the encoder `E` to `C`, preserving the write buffer wrapped by `Framed`. |
| 136 | `encoder_pin_mut`  | `FramedWrite<T, E>` | Public API | Other / internal logic | Returns a mutable reference to the underlying encoder. |
| 141 | `write_buffer`  | `FramedWrite<T, E>` | Public API | I/O operation | Returns a reference to the write buffer. |
| 146 | `write_buffer_mut`  | `FramedWrite<T, E>` | Public API | I/O operation | Returns a mutable reference to the write buffer. |
| 151 | `backpressure_boundary`  | `FramedWrite<T, E>` | Public API | Other / internal logic | Returns backpressure boundary |
| 156 | `set_backpressure_boundary`  | `FramedWrite<T, E>` | Public API | Configuration / setter | Updates backpressure boundary |
| 162 | `into_parts`  | `FramedWrite<T, E>` | Public API | Conversion | Consumes the `FramedWrite`, returning its underlying I/O stream, the buffer with unprocessed data, and the codec. |
| 182 | `poll_ready`  | `Sink<I> for FramedWrite<T, E>` | Trait impl | Sink impl |  |
| 186 | `start_send`  | `Sink<I> for FramedWrite<T, E>` | Trait impl | Sink impl |  |
| 190 | `poll_flush`  | `Sink<I> for FramedWrite<T, E>` | Trait impl | Sink impl |  |
| 194 | `poll_close`  | `Sink<I> for FramedWrite<T, E>` | Trait impl | Sink impl |  |
| 206 | `poll_next`  | `Stream for FramedWrite<T, D>` | Trait impl | Stream impl |  |
| 216 | `fmt`  | `fmt::Debug for FramedWrite<T, U>` | Trait impl | Formatting |  |

## `tokio-util/src/codec/length_delimited.rs` (32)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 469 | `new`  | `LengthDelimitedCodec` | Public API | Constructor | Creates a new `LengthDelimitedCodec` with the default configuration values. |
| 478 | `builder`  | `LengthDelimitedCodec` | Public API | Constructor | Creates a new length delimited codec builder with default configuration values. |
| 486 | `max_frame_length`  | `LengthDelimitedCodec` | Public API | Configuration / setter | Returns the current max frame setting This is the largest size this codec will accept from the wire. |
| 499 | `set_max_frame_length`  | `LengthDelimitedCodec` | Public API | Configuration / setter | Updates the max frame setting. |
| 504 | `decode_head`  | `LengthDelimitedCodec` | Private helper | Other / internal logic |  |
| 564 | `decode_data`  | `LengthDelimitedCodec` | Private helper | Other / internal logic |  |
| 579 | `decode`  | `Decoder for LengthDelimitedCodec` | Trait impl | Codec impl |  |
| 609 | `encode`  | `Encoder<&[u8]> for LengthDelimitedCodec` | Trait impl | Codec impl |  |
| 653 | `encode`  | `Encoder<Bytes> for LengthDelimitedCodec` | Trait impl | Codec impl |  |
| 659 | `default`  | `Default for LengthDelimitedCodec` | Trait impl | Constructor |  |
| 706 | `new`  | `Builder` | Public API | Constructor | Creates a new length delimited codec builder with default configuration values. |
| 747 | `big_endian`  | `Builder` | Public API | Other / internal logic | Read the length field as a big endian integer This is the default setting. |
| 771 | `little_endian`  | `Builder` | Public API | Other / internal logic | Read the length field as a little endian integer The default setting is big endian. |
| 795 | `native_endian`  | `Builder` | Public API | Other / internal logic | Read the length field as a native endian integer The default setting is big endian. |
| 829 | `max_frame_length`  | `Builder` | Public API | Configuration / setter | Sets the max frame length in bytes This configuration option applies to both encoding and decoding. |
| 866 | `length_field_type`  | `Builder` | Public API | Accessor / query | Sets the unsigned integer type used to represent the length field. |
| 889 | `length_field_length`  | `Builder` | Public API | Accessor / query | Sets the number of bytes used to represent the length field The default value is `4`. |
| 912 | `length_field_offset`  | `Builder` | Public API | Accessor / query | Sets the number of bytes in the header before the length field This configuration option only applies to decoding. |
| 933 | `length_adjustment`  | `Builder` | Public API | Accessor / query | Delta between the payload length specified in the header and the real payload length |
| 957 | `num_skip`  | `Builder` | Public API | Accessor / query | Sets the number of bytes to skip before reading the payload Default value is `length_field_len + length_field_offset` This configuration option only applies to decoding |
| 983 | `new_codec`  | `Builder` | Public API | Constructor | Create a configured length delimited `LengthDelimitedCodec` |
| 1015 | `new_read`  | `Builder` | Public API | Constructor | Create a configured length delimited `FramedRead` |
| 1036 | `new_write`  | `Builder` | Public API | Constructor | Create a configured length delimited `FramedWrite` |
| 1058 | `new_framed`  | `Builder` | Public API | Constructor | Create a configured length delimited `Framed` |
| 1065 | `num_head_bytes`  | `Builder` | Private helper | Accessor / query |  |
| 1070 | `get_num_skip`  | `Builder` | Private helper | Accessor / query |  |
| 1075 | `adjust_max_frame_len`  | `Builder` | Private helper | Other / internal logic |  |
| 1083 | `max_allowed_frame_len`  | `Builder` | Private helper | Configuration / setter |  |
| 1091 | `max_length_field_value`  | `Builder` | Private helper | Configuration / setter |  |
| 1100 | `default`  | `Default for Builder` | Trait impl | Constructor |  |
| 1108 | `fmt`  | `fmt::Debug for LengthDelimitedCodecError` | Trait impl | Formatting |  |
| 1114 | `fmt`  | `fmt::Display for LengthDelimitedCodecError` | Trait impl | Formatting |  |

## `tokio-util/src/codec/lines_codec.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 42 | `new`  | `LinesCodec` | Public API | Constructor | Returns a `LinesCodec` for splitting up data into lines. |
| 68 | `new_with_max_length`  | `LinesCodec` | Public API | Constructor | Returns a `LinesCodec` with a maximum line length limit. |
| 89 | `max_length`  | `LinesCodec` | Public API | Configuration / setter | Returns the maximum line length when decoding. |
| 94 | `utf8`  |  | Private helper | Other / internal logic |  |
| 99 | `without_carriage_return`  |  | Private helper | Other / internal logic |  |
| 111 | `decode`  | `Decoder for LinesCodec` | Trait impl | Codec impl |  |
| 165 | `decode_eof`  | `Decoder for LinesCodec` | Trait impl | Codec impl |  |
| 190 | `encode`  | `Encoder<T> for LinesCodec` | Trait impl | Codec impl |  |
| 200 | `default`  | `Default for LinesCodec` | Trait impl | Constructor |  |
| 215 | `fmt`  | `fmt::Display for LinesCodecError` | Trait impl | Formatting |  |
| 224 | `from`  | `From<io::Error> for LinesCodecError` | Trait impl | Conversion |  |

