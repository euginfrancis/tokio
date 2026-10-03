# `tokio::net::tcp` — 168 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 103 |
| Trait impl | 50 |
| Crate-internal | 11 |
| Private helper | 4 |

## `tokio/src/net/tcp/listener.rs` (18)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 102 | `bind` 🅰 | `TcpListener` | Public API | Networking | Creates a new `TcpListener`, which will be bound to the specified address. |
| 122 | `bind_addr`  | `TcpListener` | Private helper | Networking |  |
| 162 | `accept` 🅰 | `TcpListener` | Public API | Networking | Accepts a new incoming connection from this listener. |
| 179 | `poll_accept`  | `TcpListener` | Public API | Poll function | Polls to accept a new incoming connection to this listener. |
| 243 | `from_std`  | `TcpListener` | Public API | Conversion | Creates new `TcpListener` from a `std::net::TcpListener`. |
| 273 | `into_std`  | `TcpListener` | Public API | Conversion | Turns a [`tokio::net::TcpListener`] into a [`std::net::TcpListener`]. |
| 303 | `new`  | `TcpListener` | Crate-internal | Constructor |  |
| 332 | `local_addr`  | `TcpListener` | Public API | Networking | Returns the local address that this listener is bound to. |
| 359 | `ttl`  | `TcpListener` | Public API | Networking | Gets the value of the `IP_TTL` option for this socket. |
| 384 | `set_ttl`  | `TcpListener` | Public API | Configuration / setter | Sets the value for the `IP_TTL` option on this socket. |
| 396 | `try_from`  | `TryFrom<net::TcpListener> for TcpListener` | Trait impl | Conversion | Consumes stream, returning the tokio I/O object. |
| 402 | `fmt`  | `fmt::Debug for TcpListener` | Trait impl | Formatting |  |
| 413 | `as_raw_fd`  | `AsRawFd for TcpListener` | Trait impl | OS handle access |  |
| 419 | `as_fd`  | `AsFd for TcpListener` | Trait impl | OS handle access |  |
| 432 | `as_raw_fd`  | `AsRawFd for TcpListener` | Trait impl | OS handle access |  |
| 438 | `as_fd`  | `AsFd for TcpListener` | Trait impl | OS handle access |  |
| 449 | `as_raw_socket`  | `AsRawSocket for TcpListener` | Trait impl | OS handle access |  |
| 455 | `as_socket`  | `AsSocket for TcpListener` | Trait impl | OS handle access |  |

## `tokio/src/net/tcp/socket.rs` (42)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 126 | `new_v4`  | `TcpSocket` | Public API | Constructor | Creates a new socket configured for IPv4. |
| 159 | `new_v6`  | `TcpSocket` | Public API | Constructor | Creates a new socket configured for IPv6. |
| 163 | `new`  | `TcpSocket` | Private helper | Constructor |  |
| 194 | `set_keepalive`  | `TcpSocket` | Public API | Configuration / setter | Sets value for the `SO_KEEPALIVE` option on this socket. |
| 199 | `keepalive`  | `TcpSocket` | Public API | Other / internal logic | Gets the value of the `SO_KEEPALIVE` option on this socket. |
| 229 | `set_reuseaddr`  | `TcpSocket` | Public API | Configuration / setter | Allows the socket to bind to an in-use address. |
| 255 | `reuseaddr`  | `TcpSocket` | Public API | Other / internal logic | Retrieves the value set for `SO_REUSEADDR` on this socket. |
| 301 | `set_reuseport`  | `TcpSocket` | Public API | Configuration / setter |  |
| 348 | `reuseport`  | `TcpSocket` | Public API | Other / internal logic |  |
| 355 | `set_send_buffer_size`  | `TcpSocket` | Public API | Configuration / setter | Sets the size of the TCP send buffer on this socket. |
| 382 | `send_buffer_size`  | `TcpSocket` | Public API | Data movement | Returns the size of the TCP send buffer for this socket. |
| 389 | `set_recv_buffer_size`  | `TcpSocket` | Public API | Configuration / setter | Sets the size of the TCP receive buffer on this socket. |
| 416 | `recv_buffer_size`  | `TcpSocket` | Public API | Data movement | Returns the size of the TCP receive buffer for this socket. |
| 444 | `set_linger`  | `TcpSocket` | Public API | Configuration / setter | Sets the linger duration of this socket by setting the `SO_LINGER` option. |
| 462 | `set_zero_linger`  | `TcpSocket` | Public API | Configuration / setter | Sets a linger duration of zero on this socket by setting the `SO_LINGER` option. |
| 473 | `linger`  | `TcpSocket` | Public API | Networking | Reads the linger duration for this socket by getting the `SO_LINGER` option. |
| 496 | `set_nodelay`  | `TcpSocket` | Public API | Configuration / setter | Sets the value of the `TCP_NODELAY` option on this socket. |
| 518 | `nodelay`  | `TcpSocket` | Public API | Networking | Gets the value of the `TCP_NODELAY` option on this socket. |
| 553 | `tclass_v6`  | `TcpSocket` | Public API | Other / internal logic |  |
| 591 | `set_tclass_v6`  | `TcpSocket` | Public API | Configuration / setter |  |
| 620 | `tos_v4`  | `TcpSocket` | Public API | Other / internal logic |  |
| 650 | `tos`  | `TcpSocket` | Public API | Other / internal logic |  |
| 684 | `set_tos_v4`  | `TcpSocket` | Public API | Configuration / setter |  |
| 714 | `set_tos`  | `TcpSocket` | Public API | Configuration / setter |  |
| 726 | `device`  | `TcpSocket` | Public API | Other / internal logic |  |
| 742 | `bind_device`  | `TcpSocket` | Public API | Networking |  |
| 768 | `local_addr`  | `TcpSocket` | Public API | Networking | Gets the local address of this socket. |
| 773 | `take_error`  | `TcpSocket` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 805 | `bind`  | `TcpSocket` | Public API | Networking | Binds the socket to the given address. |
| 841 | `connect` 🅰 | `TcpSocket` | Public API | Networking | Establishes a TCP connection with a peer at the specified socket address. |
| 906 | `listen`  | `TcpSocket` | Public API | Networking | Converts the socket into a `TcpListener`. |
| 960 | `from_std_stream`  | `TcpSocket` | Public API | Conversion | Converts a [`std::net::TcpStream`] into a `TcpSocket`. |
| 979 | `convert_address`  |  | Private helper | Other / internal logic |  |
| 990 | `fmt`  | `fmt::Debug for TcpSocket` | Trait impl | Formatting |  |
| 1000 | `as_raw_fd`  | `AsRawFd for TcpSocket` | Trait impl | OS handle access |  |
| 1006 | `as_fd`  | `AsFd for TcpSocket` | Trait impl | OS handle access |  |
| 1018 | `from_raw_fd` ⚠ | `FromRawFd for TcpSocket` | Trait impl | Conversion | Converts a `RawFd` to a `TcpSocket`. |
| 1027 | `into_raw_fd`  | `IntoRawFd for TcpSocket` | Trait impl | Conversion |  |
| 1035 | `into_raw_socket`  | `IntoRawSocket for TcpSocket` | Trait impl | Conversion |  |
| 1041 | `as_raw_socket`  | `AsRawSocket for TcpSocket` | Trait impl | OS handle access |  |
| 1047 | `as_socket`  | `AsSocket for TcpSocket` | Trait impl | OS handle access |  |
| 1059 | `from_raw_socket` ⚠ | `FromRawSocket for TcpSocket` | Trait impl | Conversion | Converts a `RawSocket` to a `TcpStream`. |

## `tokio/src/net/tcp/split.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 51 | `split`  |  | Crate-internal | Combinator / iteration |  |
| 90 | `poll_peek`  | `ReadHalf<'_>` | Public API | Poll function | Attempts to receive data on the socket, without removing that data from the queue, registering the current task for wakeup if data is not yet available. |
| 137 | `peek` 🅰 | `ReadHalf<'_>` | Public API | Combinator / iteration | Receives data on the socket from the remote address to which it is connected, without removing that data from the queue. |
| 165 | `ready` 🅰 | `ReadHalf<'_>` | Public API | I/O operation | Waits for any of the requested ready states. |
| 182 | `readable` 🅰 | `ReadHalf<'_>` | Public API | I/O operation | Waits for the socket to become readable. |
| 209 | `try_read`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, returning how many bytes were read. |
| 238 | `try_read_vectored`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 262 | `try_read_buf`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 268 | `peer_addr`  | `ReadHalf<'_>` | Public API | Networking | Returns the remote address that this stream is connected to. |
| 273 | `local_addr`  | `ReadHalf<'_>` | Public API | Networking | Returns the local address that this stream is bound to. |
| 302 | `ready` 🅰 | `WriteHalf<'_>` | Public API | I/O operation | Waits for any of the requested ready states. |
| 317 | `writable` 🅰 | `WriteHalf<'_>` | Public API | Async operation | Waits for the socket to become writable. |
| 334 | `try_write`  | `WriteHalf<'_>` | Public API | Non-blocking attempt | Tries to write a buffer to the stream, returning how many bytes were written. |
| 355 | `try_write_vectored`  | `WriteHalf<'_>` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 360 | `peer_addr`  | `WriteHalf<'_>` | Public API | Networking | Returns the remote address that this stream is connected to. |
| 365 | `local_addr`  | `WriteHalf<'_>` | Public API | Networking | Returns the local address that this stream is bound to. |
| 371 | `poll_read`  | `AsyncRead for ReadHalf<'_>` | Trait impl | I/O trait impl |  |
| 381 | `poll_write`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 389 | `poll_write_vectored`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 397 | `is_write_vectored`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 402 | `poll_flush`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 408 | `poll_shutdown`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 414 | `as_ref`  | `AsRef<TcpStream> for ReadHalf<'_>` | Trait impl | Conversion |  |
| 420 | `as_ref`  | `AsRef<TcpStream> for WriteHalf<'_>` | Trait impl | Conversion |  |

## `tokio/src/net/tcp/split_owned.rs` (30)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 59 | `split_owned`  |  | Crate-internal | Combinator / iteration |  |
| 71 | `reunite`  |  | Crate-internal | Combinator / iteration |  |
| 91 | `fmt`  | `fmt::Display for ReuniteError` | Trait impl | Formatting |  |
| 107 | `reunite`  | `OwnedReadHalf` | Public API | Combinator / iteration | Attempts to put the two halves of a `TcpStream` back together and recover the original socket. |
| 145 | `poll_peek`  | `OwnedReadHalf` | Public API | Poll function | Attempt to receive data on the socket, without removing that data from the queue, registering the current task for wakeup if data is not yet available. |
| 192 | `peek` 🅰 | `OwnedReadHalf` | Public API | Combinator / iteration | Receives data on the socket from the remote address to which it is connected, without removing that data from the queue. |
| 220 | `ready` 🅰 | `OwnedReadHalf` | Public API | I/O operation | Waits for any of the requested ready states. |
| 237 | `readable` 🅰 | `OwnedReadHalf` | Public API | I/O operation | Waits for the socket to become readable. |
| 264 | `try_read`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, returning how many bytes were read. |
| 293 | `try_read_vectored`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 317 | `try_read_buf`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 323 | `peer_addr`  | `OwnedReadHalf` | Public API | Networking | Returns the remote address that this stream is connected to. |
| 328 | `local_addr`  | `OwnedReadHalf` | Public API | Networking | Returns the local address that this stream is bound to. |
| 334 | `poll_read`  | `AsyncRead for OwnedReadHalf` | Trait impl | I/O trait impl |  |
| 349 | `reunite`  | `OwnedWriteHalf` | Public API | Combinator / iteration | Attempts to put the two halves of a `TcpStream` back together and recover the original socket. |
| 356 | `forget`  | `OwnedWriteHalf` | Public API | Locking / permits | Destroys the write half, but don't close the write half of the stream until the read half is dropped. |
| 384 | `ready` 🅰 | `OwnedWriteHalf` | Public API | I/O operation | Waits for any of the requested ready states. |
| 399 | `writable` 🅰 | `OwnedWriteHalf` | Public API | Async operation | Waits for the socket to become writable. |
| 416 | `try_write`  | `OwnedWriteHalf` | Public API | Non-blocking attempt | Tries to write a buffer to the stream, returning how many bytes were written. |
| 437 | `try_write_vectored`  | `OwnedWriteHalf` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 442 | `peer_addr`  | `OwnedWriteHalf` | Public API | Networking | Returns the remote address that this stream is connected to. |
| 447 | `local_addr`  | `OwnedWriteHalf` | Public API | Networking | Returns the local address that this stream is bound to. |
| 453 | `drop`  | `Drop for OwnedWriteHalf` | Trait impl | Drop / cleanup |  |
| 461 | `poll_write`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 469 | `poll_write_vectored`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 477 | `is_write_vectored`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 482 | `poll_flush`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 488 | `poll_shutdown`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 498 | `as_ref`  | `AsRef<TcpStream> for OwnedReadHalf` | Trait impl | Conversion |  |
| 504 | `as_ref`  | `AsRef<TcpStream> for OwnedWriteHalf` | Trait impl | Conversion |  |

## `tokio/src/net/tcp/stream.rs` (54)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 121 | `connect` 🅰 | `TcpStream` | Public API | Networking | Opens a TCP connection to a remote host. |
| 142 | `connect_addr` 🅰 | `TcpStream` | Private helper | Networking | Establishes a connection to the specified `addr`. |
| 147 | `connect_mio` 🅰 | `TcpStream` | Crate-internal | Networking |  |
| 166 | `new`  | `TcpStream` | Crate-internal | Constructor |  |
| 174 | `new_accepted`  | `TcpStream` | Crate-internal | Constructor | A stream returned by `accept`: assumed readable and writable, so that its first read and write try the socket instead of waiting for the driver's first event (see `Registration::assume_ready`). |
| 225 | `from_std`  | `TcpStream` | Public API | Conversion | Creates new `TcpStream` from a `std::net::TcpStream`. |
| 271 | `into_std`  | `TcpStream` | Public API | Conversion | Turns a [`tokio::net::TcpStream`] into a [`std::net::TcpStream`]. |
| 314 | `local_addr`  | `TcpStream` | Public API | Networking | Returns the local address that this stream is bound to. |
| 319 | `take_error`  | `TcpStream` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 337 | `peer_addr`  | `TcpStream` | Public API | Networking | Returns the remote address that this stream is connected to. |
| 383 | `poll_peek`  | `TcpStream` | Public API | Poll function | Attempts to receive data on the socket, without removing that data from the queue, registering the current task for wakeup if data is not yet available. |
| 482 | `ready` 🅰 | `TcpStream` | Public API | I/O operation | Waits for any of the requested ready states. |
| 537 | `readable` 🅰 | `TcpStream` | Public API | I/O operation | Waits for the socket to become readable. |
| 571 | `poll_read_ready`  | `TcpStream` | Public API | Poll function | Polls for read readiness. |
| 638 | `try_read`  | `TcpStream` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, returning how many bytes were read. |
| 716 | `try_read_vectored`  | `TcpStream` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 782 | `try_read_buf`  | `TcpStream` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 849 | `writable` 🅰 | `TcpStream` | Public API | Async operation | Waits for the socket to become writable. |
| 883 | `poll_write_ready`  | `TcpStream` | Public API | Poll function | Polls for write readiness. |
| 935 | `try_write`  | `TcpStream` | Public API | Non-blocking attempt | Try to write a buffer to the stream, returning how many bytes were written. |
| 997 | `try_write_vectored`  | `TcpStream` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 1037 | `try_io`  | `TcpStream` | Public API | Non-blocking attempt | Tries to read or write from the socket using a user-provided IO operation. |
| 1072 | `async_io` 🅰 | `TcpStream` | Public API | Async operation | Reads or writes from the socket using a user-provided IO operation. |
| 1127 | `peek` 🅰 | `TcpStream` | Public API | Combinator / iteration | Receives data on the socket from the remote address to which it is connected, without removing that data from the queue. |
| 1144 | `shutdown_std`  | `TcpStream` | Crate-internal | Runtime/task control | Shuts down the read, write, or both halves of this connection. |
| 1169 | `nodelay`  | `TcpStream` | Public API | Networking | Gets the value of the `TCP_NODELAY` option on this socket. |
| 1193 | `set_nodelay`  | `TcpStream` | Public API | Configuration / setter | Sets the value of the `TCP_NODELAY` option on this socket. |
| 1228 | `quickack`  | `TcpStream` | Public API | Other / internal logic |  |
| 1268 | `set_quickack`  | `TcpStream` | Public API | Configuration / setter |  |
| 1293 | `linger`  | `TcpStream` | Public API | Networking | Reads the linger duration for this socket by getting the `SO_LINGER` option. |
| 1335 | `set_linger`  | `TcpStream` | Public API | Configuration / setter | Sets the linger duration of this socket by setting the `SO_LINGER` option. |
| 1368 | `set_zero_linger`  | `TcpStream` | Public API | Configuration / setter | Sets a linger duration of zero on this socket by setting the `SO_LINGER` option. |
| 1391 | `ttl`  | `TcpStream` | Public API | Networking | Gets the value of the `IP_TTL` option for this socket. |
| 1412 | `set_ttl`  | `TcpStream` | Public API | Configuration / setter | Sets the value for the `IP_TTL` option on this socket. |
| 1426 | `split`  | `TcpStream` | Public API | Combinator / iteration | Splits a `TcpStream` into a read half and a write half, which can be used to read and write the stream concurrently. |
| 1441 | `into_split`  | `TcpStream` | Public API | Conversion | Splits a `TcpStream` into a read half and a write half, which can be used to read and write the stream concurrently. |
| 1451 | `poll_read_priv`  | `TcpStream` | Crate-internal | Poll function |  |
| 1460 | `poll_write_priv`  | `TcpStream` | Crate-internal | Poll function |  |
| 1468 | `poll_write_vectored_priv`  | `TcpStream` | Crate-internal | Poll function |  |
| 1484 | `try_from`  | `TryFrom<std::net::TcpStream> for TcpStream` | Trait impl | Conversion | Consumes stream, returning the tokio I/O object. |
| 1492 | `poll_read`  | `AsyncRead for TcpStream` | Trait impl | I/O trait impl |  |
| 1502 | `poll_write`  | `AsyncWrite for TcpStream` | Trait impl | I/O trait impl |  |
| 1510 | `poll_write_vectored`  | `AsyncWrite for TcpStream` | Trait impl | I/O trait impl |  |
| 1518 | `is_write_vectored`  | `AsyncWrite for TcpStream` | Trait impl | I/O trait impl |  |
| 1523 | `poll_flush`  | `AsyncWrite for TcpStream` | Trait impl | I/O trait impl |  |
| 1528 | `poll_shutdown`  | `AsyncWrite for TcpStream` | Trait impl | I/O trait impl |  |
| 1535 | `fmt`  | `fmt::Debug for TcpStream` | Trait impl | Formatting |  |
| 1542 | `as_ref`  | `AsRef<Self> for TcpStream` | Trait impl | Conversion |  |
| 1553 | `as_raw_fd`  | `AsRawFd for TcpStream` | Trait impl | OS handle access |  |
| 1559 | `as_fd`  | `AsFd for TcpStream` | Trait impl | OS handle access |  |
| 1569 | `as_raw_socket`  | `AsRawSocket for TcpStream` | Trait impl | OS handle access |  |
| 1575 | `as_socket`  | `AsSocket for TcpStream` | Trait impl | OS handle access |  |
| 1587 | `as_raw_fd`  | `AsRawFd for TcpStream` | Trait impl | OS handle access |  |
| 1593 | `as_fd`  | `AsFd for TcpStream` | Trait impl | OS handle access |  |

