# `tokio::io::bsd` — 15 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 6 |
| Public API | 5 |
| Trait method (declaration/default) | 3 |
| Private helper | 1 |

## `tokio/src/io/bsd/poll_aio.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 29 | `register`  | `trait AioSource` | Trait method (declaration/default) | I/O registration | Registers this AIO event source with Tokio's reactor. |
| 36 | `register_borrowed`  | `trait AioSource` | Trait method (declaration/default) | I/O registration | Registers this AIO event source with Tokio's reactor. |
| 44 | `deregister`  | `trait AioSource` | Trait method (declaration/default) | I/O registration | Deregisters this AIO event source with Tokio's reactor. |
| 52 | `register`  | `Source for MioSource<T>` | Trait impl | I/O registration |  |
| 64 | `deregister`  | `Source for MioSource<T>` | Trait impl | I/O registration |  |
| 69 | `reregister`  | `Source for MioSource<T>` | Trait impl | Other / internal logic |  |
| 125 | `new_for_aio`  | `Aio<E>` | Public API | Constructor | Creates a new `Aio` suitable for use with POSIX AIO functions. |
| 137 | `new_for_lio`  | `Aio<E>` | Public API | Constructor | Creates a new `Aio` suitable for use with [`lio_listio`]. |
| 141 | `new_with_interest`  | `Aio<E>` | Private helper | Constructor |  |
| 165 | `clear_ready`  | `Aio<E>` | Public API | Other / internal logic | Indicates to Tokio that the source is no longer ready. |
| 170 | `into_inner`  | `Aio<E>` | Public API | Conversion | Destroy the [`Aio`] and return its inner source. |
| 188 | `poll_ready`  | `Aio<E>` | Public API | Poll function | Polls for readiness. |
| 197 | `deref`  | `Deref for Aio<E>` | Trait impl | Deref |  |
| 203 | `deref_mut`  | `DerefMut for Aio<E>` | Trait impl | Deref |  |
| 209 | `fmt`  | `fmt::Debug for Aio<E>` | Trait impl | Formatting |  |

