# `tokio (crate root)` — 10 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 6 |
| Trait impl | 2 |
| Private helper | 1 |
| Test | 1 |

## `tokio/src/blocking.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `spawn_blocking`  |  | Crate-internal | Runtime/task control |  |
| 39 | `spawn_mandatory_blocking`  |  | Crate-internal | Runtime/task control |  |
| 54 | `spawn_blocking`  |  | Crate-internal | Runtime/task control |  |
| 64 | `spawn_mandatory_blocking`  |  | Crate-internal | Runtime/task control |  |
| 83 | `poll`  | `Future for JoinHandle<R>` | Trait impl | Future impl (poll) |  |
| 92 | `fmt`  | `fmt::Debug for JoinHandle<T>` | Trait impl | Formatting |  |
| 97 | `assert_send_sync`  |  | Private helper | Debugging / tracing |  |

## `tokio/src/lib.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 636 | `trace_leaf`  |  | Crate-internal | Debugging / tracing |  |
| 642 | `async_trace_leaf` 🅰 |  | Crate-internal | Async operation |  |
| 749 | `is_unpin`  |  | Test | Accessor / query |  |

