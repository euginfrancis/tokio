# `tokio::loom` — 10 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 10 |

## `tokio/src/loom/mocked.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `new`  | `Mutex<T>` | Crate-internal | Constructor |  |
| 19 | `lock`  | `Mutex<T>` | Crate-internal | Locking / permits |  |
| 24 | `try_lock`  | `Mutex<T>` | Crate-internal | Non-blocking attempt |  |
| 35 | `new`  | `RwLock<T>` | Crate-internal | Constructor |  |
| 40 | `read`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 45 | `try_read`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |
| 50 | `write`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 55 | `try_write`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |
| 64 | `seed`  |  | Crate-internal | Configuration / setter |  |
| 70 | `num_cpus`  |  | Crate-internal | Accessor / query |  |

