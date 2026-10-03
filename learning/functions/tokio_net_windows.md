# `tokio::net::windows` — 70 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 51 |
| Trait impl | 16 |
| Private helper | 3 |

## `tokio/src/net/windows/named_pipe.rs` (70)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 132 | `from_raw_handle` ⚠ | `NamedPipeServer` | Public API | Conversion | Constructs a new named pipe server from the specified raw handle. |
| 161 | `info`  | `NamedPipeServer` | Public API | Other / internal logic | Retrieves information about the named pipe the server is associated with. |
| 196 | `connect` 🅰 | `NamedPipeServer` | Public API | Networking | Enables a named pipe server process to wait for a client process to connect to an instance of a named pipe. |
| 237 | `disconnect`  | `NamedPipeServer` | Public API | Other / internal logic | Disconnects the server end of a named pipe instance from a client process. |
| 309 | `ready` 🅰 | `NamedPipeServer` | Public API | I/O operation | Waits for any of the requested ready states. |
| 359 | `readable` 🅰 | `NamedPipeServer` | Public API | I/O operation | Waits for the pipe to become readable. |
| 392 | `poll_read_ready`  | `NamedPipeServer` | Public API | Poll function | Polls for read readiness. |
| 461 | `try_read`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffer, returning how many bytes were read. |
| 539 | `try_read_vectored`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffers, returning how many bytes were read. |
| 604 | `try_read_buf`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 666 | `writable` 🅰 | `NamedPipeServer` | Public API | Async operation | Waits for the pipe to become writable. |
| 699 | `poll_write_ready`  | `NamedPipeServer` | Public API | Poll function | Polls for write readiness. |
| 753 | `try_write`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to write a buffer to the pipe, returning how many bytes were written. |
| 815 | `try_write_vectored`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to write several buffers to the pipe, returning how many bytes were written. |
| 853 | `try_io`  | `NamedPipeServer` | Public API | Non-blocking attempt | Tries to read or write from the pipe using a user-provided IO operation. |
| 886 | `async_io` 🅰 | `NamedPipeServer` | Public API | Async operation | Reads or writes from the pipe using a user-provided IO operation. |
| 896 | `poll_read`  | `AsyncRead for NamedPipeServer` | Trait impl | I/O trait impl |  |
| 906 | `poll_write`  | `AsyncWrite for NamedPipeServer` | Trait impl | I/O trait impl |  |
| 914 | `poll_write_vectored`  | `AsyncWrite for NamedPipeServer` | Trait impl | I/O trait impl |  |
| 922 | `poll_flush`  | `AsyncWrite for NamedPipeServer` | Trait impl | I/O trait impl |  |
| 926 | `poll_shutdown`  | `AsyncWrite for NamedPipeServer` | Trait impl | I/O trait impl |  |
| 932 | `as_raw_handle`  | `AsRawHandle for NamedPipeServer` | Trait impl | OS handle access |  |
| 938 | `as_handle`  | `AsHandle for NamedPipeServer` | Trait impl | OS handle access |  |
| 1007 | `from_raw_handle` ⚠ | `NamedPipeClient` | Public API | Conversion | Constructs a new named pipe client from the specified raw handle. |
| 1034 | `info`  | `NamedPipeClient` | Public API | Other / internal logic | Retrieves information about the named pipe the client is associated with. |
| 1106 | `ready` 🅰 | `NamedPipeClient` | Public API | I/O operation | Waits for any of the requested ready states. |
| 1155 | `readable` 🅰 | `NamedPipeClient` | Public API | I/O operation | Waits for the pipe to become readable. |
| 1188 | `poll_read_ready`  | `NamedPipeClient` | Public API | Poll function | Polls for read readiness. |
| 1256 | `try_read`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffer, returning how many bytes were read. |
| 1333 | `try_read_vectored`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to read data from the pipe into the provided buffers, returning how many bytes were read. |
| 1398 | `try_read_buf`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to read data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 1459 | `writable` 🅰 | `NamedPipeClient` | Public API | Async operation | Waits for the pipe to become writable. |
| 1492 | `poll_write_ready`  | `NamedPipeClient` | Public API | Poll function | Polls for write readiness. |
| 1545 | `try_write`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to write a buffer to the pipe, returning how many bytes were written. |
| 1606 | `try_write_vectored`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to write several buffers to the pipe, returning how many bytes were written. |
| 1644 | `try_io`  | `NamedPipeClient` | Public API | Non-blocking attempt | Tries to read or write from the pipe using a user-provided IO operation. |
| 1677 | `async_io` 🅰 | `NamedPipeClient` | Public API | Async operation | Reads or writes from the pipe using a user-provided IO operation. |
| 1687 | `poll_read`  | `AsyncRead for NamedPipeClient` | Trait impl | I/O trait impl |  |
| 1697 | `poll_write`  | `AsyncWrite for NamedPipeClient` | Trait impl | I/O trait impl |  |
| 1705 | `poll_write_vectored`  | `AsyncWrite for NamedPipeClient` | Trait impl | I/O trait impl |  |
| 1713 | `poll_flush`  | `AsyncWrite for NamedPipeClient` | Trait impl | I/O trait impl |  |
| 1717 | `poll_shutdown`  | `AsyncWrite for NamedPipeClient` | Trait impl | I/O trait impl |  |
| 1723 | `as_raw_handle`  | `AsRawHandle for NamedPipeClient` | Trait impl | OS handle access |  |
| 1729 | `as_handle`  | `AsHandle for NamedPipeClient` | Trait impl | OS handle access |  |
| 1770 | `new`  | `ServerOptions` | Public API | Constructor | Creates a new named pipe builder with the default settings. |
| 1795 | `pipe_mode`  | `ServerOptions` | Public API | Other / internal logic | The pipe mode. |
| 1891 | `access_inbound`  | `ServerOptions` | Public API | Other / internal logic | The flow of data in the pipe goes from client to server only. |
| 1989 | `access_outbound`  | `ServerOptions` | Public API | Other / internal logic | The flow of data in the pipe goes from server to client only. |
| 2057 | `first_pipe_instance`  | `ServerOptions` | Public API | Other / internal logic | If you attempt to create multiple instances of a pipe with this flag set, creation of the first server instance succeeds, but creation of any subsequent instances will fail with [`std::io::ErrorKind:: |
| 2139 | `write_dac`  | `ServerOptions` | Public API | I/O operation | Requests permission to modify the pipe's discretionary access control list. |
| 2149 | `write_owner`  | `ServerOptions` | Public API | I/O operation | Requests permission to modify the pipe's owner. |
| 2159 | `access_system_security`  | `ServerOptions` | Public API | Other / internal logic | Requests permission to modify the pipe's system access control list. |
| 2170 | `reject_remote_clients`  | `ServerOptions` | Public API | Other / internal logic | Indicates whether this server can accept remote clients or not. |
| 2230 | `max_instances`  | `ServerOptions` | Public API | Configuration / setter | The maximum number of instances that can be created for this pipe. |
| 2241 | `out_buffer_size`  | `ServerOptions` | Public API | Other / internal logic | The number of bytes to reserve for the output buffer. |
| 2251 | `in_buffer_size`  | `ServerOptions` | Public API | Other / internal logic | The number of bytes to reserve for the input buffer. |
| 2281 | `create`  | `ServerOptions` | Public API | Constructor | Creates the named pipe identified by `addr` for use as a server. |
| 2310 | `create_with_security_attributes_raw` ⚠ | `ServerOptions` | Public API | Constructor | Creates the named pipe identified by `addr` for use as a server. |
| 2376 | `default`  | `Default for ServerOptions` | Trait impl | Constructor |  |
| 2407 | `new`  | `ClientOptions` | Public API | Constructor | Creates a new named pipe builder with the default settings. |
| 2423 | `read`  | `ClientOptions` | Public API | I/O operation | If the client supports reading data. |
| 2434 | `write`  | `ClientOptions` | Public API | I/O operation | If the created pipe supports writing data. |
| 2460 | `security_qos_flags`  | `ClientOptions` | Public API | Other / internal logic | Sets qos flags which are combined with other flags and attributes in the call to [`CreateFile`]. |
| 2470 | `pipe_mode`  | `ClientOptions` | Public API | Other / internal logic | The pipe mode. |
| 2525 | `open`  | `ClientOptions` | Public API | Constructor | Opens the named pipe identified by `addr`. |
| 2546 | `open_with_security_attributes_raw` ⚠ | `ClientOptions` | Public API | Constructor | Opens the named pipe identified by `addr`. |
| 2614 | `get_flags`  | `ClientOptions` | Private helper | Accessor / query |  |
| 2621 | `default`  | `Default for ClientOptions` | Trait impl | Constructor |  |
| 2688 | `encode_addr`  |  | Private helper | Other / internal logic | Encodes an address so that it is a null-terminated wide string. |
| 2697 | `named_pipe_info` ⚠ |  | Private helper | Other / internal logic | Internal function to get the info out of a raw named pipe. |

