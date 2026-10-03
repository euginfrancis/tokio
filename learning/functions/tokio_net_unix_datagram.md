# `tokio::net::unix::datagram` — 39 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 33 |
| Trait impl | 4 |
| Crate-internal | 1 |
| Private helper | 1 |

## `tokio/src/net/unix/datagram/socket.rs` (39)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 102 | `from_mio`  | `UnixDatagram` | Crate-internal | Conversion |  |
| 182 | `ready` 🅰 | `UnixDatagram` | Public API | I/O operation | Waits for any of the requested ready states. |
| 239 | `writable` 🅰 | `UnixDatagram` | Public API | Async operation | Waits for the socket to become writable. |
| 273 | `poll_send_ready`  | `UnixDatagram` | Public API | Poll function | Polls for write/send readiness. |
| 335 | `readable` 🅰 | `UnixDatagram` | Public API | I/O operation | Waits for the socket to become readable. |
| 369 | `poll_recv_ready`  | `UnixDatagram` | Public API | Poll function | Polls for read/receive readiness. |
| 395 | `bind`  | `UnixDatagram` | Public API | Networking | Creates a new `UnixDatagram` bound to the specified path. |
| 433 | `pair`  | `UnixDatagram` | Public API | Constructor | Creates an unnamed pair of connected sockets. |
| 495 | `from_std`  | `UnixDatagram` | Public API | Conversion | Creates new [`UnixDatagram`] from a [`std::os::unix::net::UnixDatagram`]. |
| 524 | `into_std`  | `UnixDatagram` | Public API | Conversion | Turns a [`tokio::net::UnixDatagram`] into a [`std::os::unix::net::UnixDatagram`]. |
| 531 | `new`  | `UnixDatagram` | Private helper | Constructor |  |
| 568 | `unbound`  | `UnixDatagram` | Public API | Other / internal logic | Creates a new `UnixDatagram` which is not bound to any address. |
| 611 | `connect`  | `UnixDatagram` | Public API | Networking | Connects the socket to the specified address. |
| 648 | `send` 🅰 | `UnixDatagram` | Public API | Data movement | Sends data on the socket to the socket's peer. |
| 693 | `try_send`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to send a datagram to the peer without waiting. |
| 736 | `try_send_to`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to send a datagram to the peer without waiting. |
| 779 | `recv` 🅰 | `UnixDatagram` | Public API | Data movement | Receives data from the socket. |
| 830 | `try_recv`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to receive a datagram from the peer without waiting. |
| 880 | `try_recv_buf_from`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to receive data from the socket without waiting. |
| 937 | `recv_buf_from` 🅰 | `UnixDatagram` | Public API | Data movement | Receives from the socket, advances the buffer's internal cursor and returns how many bytes were read and the origin. |
| 999 | `try_recv_buf`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 1047 | `recv_buf` 🅰 | `UnixDatagram` | Public API | Data movement | Receives data from the socket from the address to which it is connected, advancing the buffer's internal cursor, returning how many bytes were read. |
| 1105 | `send_to` 🅰 | `UnixDatagram` | Public API | Data movement | Sends data on the socket to the specified address. |
| 1156 | `recv_from` 🅰 | `UnixDatagram` | Public API | Data movement | Receives data from the socket. |
| 1183 | `poll_recv_from`  | `UnixDatagram` | Public API | Poll function | Attempts to receive a single datagram on the specified address. |
| 1223 | `poll_send_to`  | `UnixDatagram` | Public API | Poll function | Attempts to send data to the specified address. |
| 1260 | `poll_send`  | `UnixDatagram` | Public API | Poll function | Attempts to send data on the socket to the remote address to which it was previously `connect`ed. |
| 1289 | `poll_recv`  | `UnixDatagram` | Public API | Poll function | Attempts to receive a single datagram message on the socket from the remote address to which it is `connect`ed. |
| 1351 | `try_recv_from`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to receive data from the socket without waiting. |
| 1392 | `try_io`  | `UnixDatagram` | Public API | Non-blocking attempt | Tries to read or write from the socket using a user-provided IO operation. |
| 1427 | `async_io` 🅰 | `UnixDatagram` | Public API | Async operation | Reads or writes from the socket using a user-provided IO operation. |
| 1480 | `local_addr`  | `UnixDatagram` | Public API | Networking | Returns the local address that this socket is bound to. |
| 1531 | `peer_addr`  | `UnixDatagram` | Public API | Networking | Returns the address of this socket's peer. |
| 1555 | `take_error`  | `UnixDatagram` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 1592 | `shutdown`  | `UnixDatagram` | Public API | Runtime/task control | Shuts down the read, write, or both halves of this connection. |
| 1604 | `try_from`  | `TryFrom<std::os::unix::net::UnixDatagram> for UnixDatagram` | Trait impl | Conversion | Consumes stream, returning the Tokio I/O object. |
| 1610 | `fmt`  | `fmt::Debug for UnixDatagram` | Trait impl | Formatting |  |
| 1616 | `as_raw_fd`  | `AsRawFd for UnixDatagram` | Trait impl | OS handle access |  |
| 1622 | `as_fd`  | `AsFd for UnixDatagram` | Trait impl | OS handle access |  |

