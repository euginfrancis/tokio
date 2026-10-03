# `tokio-util::udp` — 13 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 8 |
| Trait impl | 5 |

## `tokio-util/src/udp/frame.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 67 | `poll_next`  | `Stream for UdpFramed<C, T>` | Trait impl | Stream impl |  |
| 121 | `poll_ready`  | `Sink<(I, SocketAddr)> for UdpFramed<C, T>` | Trait impl | Sink impl |  |
| 132 | `start_send`  | `Sink<(I, SocketAddr)> for UdpFramed<C, T>` | Trait impl | Sink impl |  |
| 144 | `poll_flush`  | `Sink<(I, SocketAddr)> for UdpFramed<C, T>` | Trait impl | Sink impl |  |
| 171 | `poll_close`  | `Sink<(I, SocketAddr)> for UdpFramed<C, T>` | Trait impl | Sink impl |  |
| 184 | `new`  | `UdpFramed<C, T>` | Public API | Constructor | Create a new `UdpFramed` backed by the given socket and codec. |
| 204 | `get_ref`  | `UdpFramed<C, T>` | Public API | Accessor / query | Returns a reference to the underlying I/O stream wrapped by `Framed`. |
| 215 | `get_mut`  | `UdpFramed<C, T>` | Public API | Accessor / query | Returns a mutable reference to the underlying I/O stream wrapped by `Framed`. |
| 224 | `codec`  | `UdpFramed<C, T>` | Public API | Other / internal logic | Returns a reference to the underlying codec wrapped by `Framed`. |
| 233 | `codec_mut`  | `UdpFramed<C, T>` | Public API | Other / internal logic | Returns a mutable reference to the underlying codec wrapped by `UdpFramed`. |
| 238 | `read_buffer`  | `UdpFramed<C, T>` | Public API | I/O operation | Returns a reference to the read buffer. |
| 243 | `read_buffer_mut`  | `UdpFramed<C, T>` | Public API | I/O operation | Returns a mutable reference to the read buffer. |
| 248 | `into_inner`  | `UdpFramed<C, T>` | Public API | Conversion | Consumes the `Framed`, returning its underlying I/O stream. |

