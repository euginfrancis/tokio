# `tokio::net::unix` — 185 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 103 |
| Trait impl | 51 |
| Crate-internal | 20 |
| Private helper | 11 |

## `tokio/src/net/unix/listener.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 60 | `new`  | `UnixListener` | Crate-internal | Constructor |  |
| 76 | `bind`  | `UnixListener` | Public API | Networking | Creates a new `UnixListener` bound to the specified path. |
| 108 | `bind_addr`  | `UnixListener` | Public API | Networking | Creates a new `UnixListener` bound to the specified address. |
| 156 | `from_std`  | `UnixListener` | Public API | Conversion | Creates new [`UnixListener`] from a [`std::os::unix::net::UnixListener`]. |
| 184 | `into_std`  | `UnixListener` | Public API | Conversion | Turns a [`tokio::net::UnixListener`] into a [`std::os::unix::net::UnixListener`]. |
| 192 | `local_addr`  | `UnixListener` | Public API | Networking | Returns the local socket address of this listener. |
| 197 | `take_error`  | `UnixListener` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 209 | `accept` 🅰 | `UnixListener` | Public API | Networking | Accepts a new incoming connection to this listener. |
| 227 | `poll_accept`  | `UnixListener` | Public API | Poll function | Polls to accept a new incoming connection to this listener. |
| 242 | `try_from`  | `TryFrom<std::os::unix::net::UnixListener> for UnixListener` | Trait impl | Conversion | Consumes stream, returning the tokio I/O object. |
| 248 | `fmt`  | `fmt::Debug for UnixListener` | Trait impl | Formatting |  |
| 254 | `as_raw_fd`  | `AsRawFd for UnixListener` | Trait impl | OS handle access |  |
| 260 | `as_fd`  | `AsFd for UnixListener` | Trait impl | OS handle access |  |

## `tokio/src/net/unix/pipe.rs` (51)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 67 | `pipe`  |  | Public API | Other / internal logic | Creates a new anonymous Unix pipe. |
| 132 | `new`  | `OpenOptions` | Public API | Constructor | Creates a blank new set of options ready for configuration. |
| 173 | `read_write`  | `OpenOptions` | Public API | I/O operation | Sets the option for read-write access. |
| 205 | `unchecked`  | `OpenOptions` | Public API | Other / internal logic | Sets the option to skip the check for FIFO file type. |
| 229 | `open_receiver`  | `OpenOptions` | Public API | Constructor | Creates a [`Receiver`] from a FIFO file with the options specified by `self`. |
| 255 | `open_sender`  | `OpenOptions` | Public API | Constructor | Creates a [`Sender`] from a FIFO file with the options specified by `self`. |
| 260 | `open`  | `OpenOptions` | Private helper | Constructor |  |
| 283 | `default`  | `Default for OpenOptions` | Trait impl | Constructor |  |
| 370 | `from_mio`  | `Sender` | Private helper | Conversion |  |
| 394 | `from_file`  | `Sender` | Public API | Conversion | Creates a new `Sender` from a [`File`]. |
| 419 | `from_owned_fd`  | `Sender` | Public API | Conversion | Creates a new `Sender` from an [`OwnedFd`]. |
| 474 | `from_file_unchecked`  | `Sender` | Public API | Conversion | Creates a new `Sender` from a [`File`] without checking pipe properties. |
| 494 | `from_owned_fd_unchecked`  | `Sender` | Public API | Conversion | Creates a new `Sender` from an [`OwnedFd`] without checking pipe properties. |
| 519 | `ready` 🅰 | `Sender` | Public API | I/O operation | Waits for any of the requested ready states. |
| 564 | `writable` 🅰 | `Sender` | Public API | Async operation | Waits for the pipe to become writable. |
| 596 | `poll_write_ready`  | `Sender` | Public API | Poll function | Polls for write readiness. |
| 663 | `try_write`  | `Sender` | Public API | Non-blocking attempt | Tries to write a buffer to the pipe, returning how many bytes were written. |
| 739 | `try_write_vectored`  | `Sender` | Public API | Non-blocking attempt | Tries to write several buffers to the pipe, returning how many bytes were written. |
| 771 | `try_io`  | `Sender` | Public API | Non-blocking attempt | Tries to write from the socket using a user-provided IO operation. |
| 781 | `into_blocking_fd`  | `Sender` | Public API | Conversion | Converts the pipe into an [`OwnedFd`] in blocking mode. |
| 792 | `into_nonblocking_fd`  | `Sender` | Public API | Conversion | Converts the pipe into an [`OwnedFd`] in nonblocking mode. |
| 804 | `poll_write`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 812 | `poll_write_vectored`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 820 | `is_write_vectored`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 824 | `poll_flush`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 828 | `poll_shutdown`  | `AsyncWrite for Sender` | Trait impl | I/O trait impl |  |
| 834 | `as_raw_fd`  | `AsRawFd for Sender` | Trait impl | OS handle access |  |
| 840 | `as_fd`  | `AsFd for Sender` | Trait impl | OS handle access |  |
| 918 | `from_mio`  | `Receiver` | Private helper | Conversion |  |
| 942 | `from_file`  | `Receiver` | Public API | Conversion | Creates a new `Receiver` from a [`File`]. |
| 967 | `from_owned_fd`  | `Receiver` | Public API | Conversion | Creates a new `Receiver` from an [`OwnedFd`]. |
| 1022 | `from_file_unchecked`  | `Receiver` | Public API | Conversion | Creates a new `Receiver` from a [`File`] without checking pipe properties. |
| 1042 | `from_owned_fd_unchecked`  | `Receiver` | Public API | Conversion | Creates a new `Receiver` from an [`OwnedFd`] without checking pipe properties. |
| 1067 | `ready` 🅰 | `Receiver` | Public API | I/O operation | Waits for any of the requested ready states. |
| 1116 | `readable` 🅰 | `Receiver` | Public API | I/O operation | Waits for the pipe to become readable. |
| 1148 | `poll_read_ready`  | `Receiver` | Public API | Poll function | Polls for read readiness. |
| 1222 | `try_read`  | `Receiver` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffer, returning how many bytes were read. |
| 1306 | `try_read_vectored`  | `Receiver` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffers, returning how many bytes were read. |
| 1338 | `try_io`  | `Receiver` | Public API | Non-blocking attempt | Tries to read to the socket using a user-provided IO operation. |
| 1411 | `try_read_buf`  | `Receiver` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 1436 | `into_blocking_fd`  | `Receiver` | Public API | Conversion | Converts the pipe into an [`OwnedFd`] in blocking mode. |
| 1447 | `into_nonblocking_fd`  | `Receiver` | Public API | Conversion | Converts the pipe into an [`OwnedFd`] in nonblocking mode. |
| 1459 | `poll_read`  | `AsyncRead for Receiver` | Trait impl | I/O trait impl |  |
| 1471 | `as_raw_fd`  | `AsRawFd for Receiver` | Trait impl | OS handle access |  |
| 1477 | `as_fd`  | `AsFd for Receiver` | Trait impl | OS handle access |  |
| 1483 | `is_pipe`  |  | Private helper | Accessor / query | Checks if the file descriptor is a pipe or a FIFO. |
| 1500 | `get_file_flags`  |  | Private helper | Accessor / query | Gets file descriptor's flags by fcntl. |
| 1511 | `has_read_access`  |  | Private helper | Accessor / query | Checks for `O_RDONLY` or `O_RDWR` access mode. |
| 1517 | `has_write_access`  |  | Private helper | Accessor / query | Checks for `O_WRONLY` or `O_RDWR` access mode. |
| 1523 | `set_nonblocking`  |  | Private helper | Configuration / setter | Sets file descriptor's flags with `O_NONBLOCK` by fcntl. |
| 1539 | `set_blocking`  |  | Private helper | Configuration / setter | Removes `O_NONBLOCK` from fd's flags. |

## `tokio/src/net/unix/socket.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 95 | `ty`  | `UnixSocket` | Private helper | Other / internal logic |  |
| 107 | `new_datagram`  | `UnixSocket` | Public API | Constructor | Creates a new Unix datagram socket. |
| 119 | `new_stream`  | `UnixSocket` | Public API | Constructor | Creates a new Unix stream socket. |
| 123 | `new`  | `UnixSocket` | Private helper | Constructor |  |
| 153 | `bind`  | `UnixSocket` | Public API | Networking | Binds the socket to the given address. |
| 171 | `listen`  | `UnixSocket` | Public API | Networking | Converts the socket into a `UnixListener`. |
| 200 | `connect` 🅰 | `UnixSocket` | Public API | Networking | Establishes a Unix connection with a peer at the specified socket address. |
| 228 | `datagram`  | `UnixSocket` | Public API | Other / internal logic | Converts the socket into a [`UnixDatagram`]. |
| 246 | `as_raw_fd`  | `AsRawFd for UnixSocket` | Trait impl | OS handle access |  |
| 252 | `as_fd`  | `AsFd for UnixSocket` | Trait impl | OS handle access |  |
| 258 | `from_raw_fd` ⚠ | `FromRawFd for UnixSocket` | Trait impl | Conversion |  |
| 267 | `into_raw_fd`  | `IntoRawFd for UnixSocket` | Trait impl | Conversion |  |

## `tokio/src/net/unix/socketaddr.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 18 | `is_unnamed`  | `SocketAddr` | Public API | Accessor / query | Returns `true` if the address is unnamed. |
| 27 | `as_pathname`  | `SocketAddr` | Public API | Conversion | Returns the contents of this address if it is a `pathname` address. |
| 40 | `as_abstract_name`  | `SocketAddr` | Public API | Conversion | Returns the contents of this address if it is in the abstract namespace. |
| 51 | `fmt`  | `fmt::Debug for SocketAddr` | Trait impl | Formatting |  |
| 57 | `from`  | `From<std::os::unix::net::SocketAddr> for SocketAddr` | Trait impl | Conversion |  |
| 63 | `from`  | `From<SocketAddr> for std::os::unix::net::SocketAddr` | Trait impl | Conversion |  |

## `tokio/src/net/unix/split.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 51 | `split`  |  | Crate-internal | Combinator / iteration |  |
| 79 | `ready` 🅰 | `ReadHalf<'_>` | Public API | I/O operation | Wait for any of the requested ready states. |
| 94 | `readable` 🅰 | `ReadHalf<'_>` | Public API | I/O operation | Waits for the socket to become readable. |
| 121 | `try_read`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, returning how many bytes were read. |
| 144 | `try_read_buf`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 174 | `try_read_vectored`  | `ReadHalf<'_>` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 179 | `peer_addr`  | `ReadHalf<'_>` | Public API | Networking | Returns the socket address of the remote half of this connection. |
| 184 | `local_addr`  | `ReadHalf<'_>` | Public API | Networking | Returns the socket address of the local half of this connection. |
| 213 | `ready` 🅰 | `WriteHalf<'_>` | Public API | I/O operation | Waits for any of the requested ready states. |
| 228 | `writable` 🅰 | `WriteHalf<'_>` | Public API | Async operation | Waits for the socket to become writable. |
| 245 | `try_write`  | `WriteHalf<'_>` | Public API | Non-blocking attempt | Tries to write a buffer to the stream, returning how many bytes were written. |
| 266 | `try_write_vectored`  | `WriteHalf<'_>` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 271 | `peer_addr`  | `WriteHalf<'_>` | Public API | Networking | Returns the socket address of the remote half of this connection. |
| 276 | `local_addr`  | `WriteHalf<'_>` | Public API | Networking | Returns the socket address of the local half of this connection. |
| 282 | `poll_read`  | `AsyncRead for ReadHalf<'_>` | Trait impl | I/O trait impl |  |
| 292 | `poll_write`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 300 | `poll_write_vectored`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 308 | `is_write_vectored`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 312 | `poll_flush`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 316 | `poll_shutdown`  | `AsyncWrite for WriteHalf<'_>` | Trait impl | I/O trait impl |  |
| 322 | `as_ref`  | `AsRef<UnixStream> for ReadHalf<'_>` | Trait impl | Conversion |  |
| 328 | `as_ref`  | `AsRef<UnixStream> for WriteHalf<'_>` | Trait impl | Conversion |  |

## `tokio/src/net/unix/split_owned.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 59 | `split_owned`  |  | Crate-internal | Combinator / iteration |  |
| 71 | `reunite`  |  | Crate-internal | Combinator / iteration |  |
| 91 | `fmt`  | `fmt::Display for ReuniteError` | Trait impl | Formatting |  |
| 107 | `reunite`  | `OwnedReadHalf` | Public API | Combinator / iteration | Attempts to put the two halves of a `UnixStream` back together and recover the original socket. |
| 134 | `ready` 🅰 | `OwnedReadHalf` | Public API | I/O operation | Waits for any of the requested ready states. |
| 149 | `readable` 🅰 | `OwnedReadHalf` | Public API | I/O operation | Waits for the socket to become readable. |
| 176 | `try_read`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, returning how many bytes were read. |
| 200 | `try_read_buf`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 230 | `try_read_vectored`  | `OwnedReadHalf` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 235 | `peer_addr`  | `OwnedReadHalf` | Public API | Networking | Returns the socket address of the remote half of this connection. |
| 240 | `local_addr`  | `OwnedReadHalf` | Public API | Networking | Returns the socket address of the local half of this connection. |
| 246 | `poll_read`  | `AsyncRead for OwnedReadHalf` | Trait impl | I/O trait impl |  |
| 261 | `reunite`  | `OwnedWriteHalf` | Public API | Combinator / iteration | Attempts to put the two halves of a `UnixStream` back together and recover the original socket. |
| 268 | `forget`  | `OwnedWriteHalf` | Public API | Locking / permits | Destroys the write half, but don't close the write half of the stream until the read half is dropped. |
| 296 | `ready` 🅰 | `OwnedWriteHalf` | Public API | I/O operation | Waits for any of the requested ready states. |
| 311 | `writable` 🅰 | `OwnedWriteHalf` | Public API | Async operation | Waits for the socket to become writable. |
| 328 | `try_write`  | `OwnedWriteHalf` | Public API | Non-blocking attempt | Tries to write a buffer to the stream, returning how many bytes were written. |
| 349 | `try_write_vectored`  | `OwnedWriteHalf` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 354 | `peer_addr`  | `OwnedWriteHalf` | Public API | Networking | Returns the socket address of the remote half of this connection. |
| 359 | `local_addr`  | `OwnedWriteHalf` | Public API | Networking | Returns the socket address of the local half of this connection. |
| 365 | `drop`  | `Drop for OwnedWriteHalf` | Trait impl | Drop / cleanup |  |
| 373 | `poll_write`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 381 | `poll_write_vectored`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 389 | `is_write_vectored`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 394 | `poll_flush`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 400 | `poll_shutdown`  | `AsyncWrite for OwnedWriteHalf` | Trait impl | I/O trait impl |  |
| 410 | `as_ref`  | `AsRef<UnixStream> for OwnedReadHalf` | Trait impl | Conversion |  |
| 416 | `as_ref`  | `AsRef<UnixStream> for OwnedWriteHalf` | Trait impl | Conversion |  |

## `tokio/src/net/unix/stream.rs` (41)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 49 | `connect_mio` 🅰 | `UnixStream` | Crate-internal | Networking |  |
| 81 | `connect` 🅰 | `UnixStream` | Public API | Networking | Connects to the socket named by `path`. |
| 116 | `connect_addr` 🅰 | `UnixStream` | Public API | Networking | Connects to the socket named by `socket_addr`. |
| 204 | `ready` 🅰 | `UnixStream` | Public API | I/O operation | Waits for any of the requested ready states. |
| 261 | `readable` 🅰 | `UnixStream` | Public API | I/O operation | Waits for the socket to become readable. |
| 295 | `poll_read_ready`  | `UnixStream` | Public API | Poll function | Polls for read readiness. |
| 364 | `try_read`  | `UnixStream` | Public API | Non-blocking attempt | Try to read data from the stream into the provided buffer, returning how many bytes were read. |
| 442 | `try_read_vectored`  | `UnixStream` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffers, returning how many bytes were read. |
| 508 | `try_read_buf`  | `UnixStream` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 577 | `writable` 🅰 | `UnixStream` | Public API | Async operation | Waits for the socket to become writable. |
| 611 | `poll_write_ready`  | `UnixStream` | Public API | Poll function | Polls for write readiness. |
| 665 | `try_write`  | `UnixStream` | Public API | Non-blocking attempt | Tries to write a buffer to the stream, returning how many bytes were written. |
| 727 | `try_write_vectored`  | `UnixStream` | Public API | Non-blocking attempt | Tries to write several buffers to the stream, returning how many bytes were written. |
| 765 | `try_io`  | `UnixStream` | Public API | Non-blocking attempt | Tries to read or write from the socket using a user-provided IO operation. |
| 800 | `async_io` 🅰 | `UnixStream` | Public API | Async operation | Reads or writes from the socket using a user-provided IO operation. |
| 853 | `from_std`  | `UnixStream` | Public API | Conversion | Creates new [`UnixStream`] from a [`std::os::unix::net::UnixStream`]. |
| 901 | `into_std`  | `UnixStream` | Public API | Conversion | Turns a [`tokio::net::UnixStream`] into a [`std::os::unix::net::UnixStream`]. |
| 913 | `pair`  | `UnixStream` | Public API | Constructor | Creates an unnamed pair of connected sockets. |
| 926 | `new_accepted`  | `UnixStream` | Crate-internal | Constructor | See `TcpStream::new_accepted`. |
| 935 | `new`  | `UnixStream` | Crate-internal | Constructor |  |
| 956 | `local_addr`  | `UnixStream` | Public API | Networking | Returns the socket address of the local half of this connection. |
| 976 | `peer_addr`  | `UnixStream` | Public API | Networking | Returns the socket address of the remote half of this connection. |
| 981 | `peer_cred`  | `UnixStream` | Public API | Other / internal logic | Returns effective credentials of the process which called `connect` or `pair`. |
| 986 | `take_error`  | `UnixStream` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 1000 | `shutdown_std`  | `UnixStream` | Crate-internal | Runtime/task control | Shuts down the read, write, or both halves of this connection. |
| 1017 | `split`  | `UnixStream` | Public API | Combinator / iteration | Splits a `UnixStream` into a read half and a write half, which can be used to read and write the stream concurrently. |
| 1032 | `into_split`  | `UnixStream` | Public API | Conversion | Splits a `UnixStream` into a read half and a write half, which can be used to read and write the stream concurrently. |
| 1044 | `try_from`  | `TryFrom<net::UnixStream> for UnixStream` | Trait impl | Conversion | Consumes stream, returning the tokio I/O object. |
| 1050 | `poll_read`  | `AsyncRead for UnixStream` | Trait impl | I/O trait impl |  |
| 1060 | `poll_write`  | `AsyncWrite for UnixStream` | Trait impl | I/O trait impl |  |
| 1068 | `poll_write_vectored`  | `AsyncWrite for UnixStream` | Trait impl | I/O trait impl |  |
| 1076 | `is_write_vectored`  | `AsyncWrite for UnixStream` | Trait impl | I/O trait impl |  |
| 1080 | `poll_flush`  | `AsyncWrite for UnixStream` | Trait impl | I/O trait impl |  |
| 1084 | `poll_shutdown`  | `AsyncWrite for UnixStream` | Trait impl | I/O trait impl |  |
| 1097 | `poll_read_priv`  | `UnixStream` | Crate-internal | Poll function |  |
| 1106 | `poll_write_priv`  | `UnixStream` | Crate-internal | Poll function |  |
| 1114 | `poll_write_vectored_priv`  | `UnixStream` | Crate-internal | Poll function |  |
| 1124 | `fmt`  | `fmt::Debug for UnixStream` | Trait impl | Formatting |  |
| 1130 | `as_ref`  | `AsRef<Self> for UnixStream` | Trait impl | Conversion |  |
| 1136 | `as_raw_fd`  | `AsRawFd for UnixStream` | Trait impl | OS handle access |  |
| 1142 | `as_fd`  | `AsFd for UnixStream` | Trait impl | OS handle access |  |

## `tokio/src/net/unix/ucred.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `uid`  | `UCred` | Public API | Other / internal logic | Gets UID (user ID) of the process. |
| 21 | `gid`  | `UCred` | Public API | Other / internal logic | Gets GID (group ID) of the process. |
| 31 | `pid`  | `UCred` | Public API | Other / internal logic | Gets PID (process ID) of the process. |
| 107 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 156 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 198 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 229 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 304 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 348 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 380 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 413 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |
| 431 | `get_peer_cred`  |  | Crate-internal | Accessor / query |  |

