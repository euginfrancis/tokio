# `tokio-util::net` — 8 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait method (declaration/default) | 3 |
| Trait impl | 3 |
| Public API | 2 |

## `tokio-util/src/net/mod.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `poll_accept`  | `trait Listener` | Trait method (declaration/default) | Poll function | Polls to accept a new incoming connection to this listener. |
| 25 | `accept`  | `trait Listener` | Trait method (declaration/default) | Networking | Accepts a new incoming connection from this listener. |
| 33 | `local_addr`  | `trait Listener` | Trait method (declaration/default) | Networking | Returns the local address that this listener is bound to. |
| 40 | `poll_accept`  | `Listener for tokio::net::TcpListener` | Trait impl | Poll function |  |
| 44 | `local_addr`  | `Listener for tokio::net::TcpListener` | Trait impl | Networking |  |
| 62 | `poll`  | `Future for ListenerAcceptFut<'a, L>` | Trait impl | Future impl (poll) |  |
| 73 | `accept` 🅰 | `Either<L, R>` | Public API | Networking | Accepts a new incoming connection from this listener. |
| 87 | `local_addr`  | `Either<L, R>` | Public API | Networking | Returns the local address that this listener is bound to. |

