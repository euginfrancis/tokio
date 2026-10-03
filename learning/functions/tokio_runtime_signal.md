# `tokio::runtime::signal` — 7 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 6 |
| Private helper | 1 |

## `tokio/src/runtime/signal/mod.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `new`  | `Driver` | Crate-internal | Constructor | Creates a new signal `Driver` instance that delegates wakeups to `park`. |
| 85 | `handle`  | `Driver` | Crate-internal | Handle / reference plumbing | Returns a handle to this event loop which can be sent across threads and can be used as a proxy to the event loop itself. |
| 91 | `park`  | `Driver` | Crate-internal | Wake / park |  |
| 96 | `park_timeout`  | `Driver` | Crate-internal | Wake / park |  |
| 101 | `shutdown`  | `Driver` | Crate-internal | Runtime/task control |  |
| 105 | `process`  | `Driver` | Private helper | Other / internal logic |  |
| 133 | `check_inner`  | `Handle` | Crate-internal | Runtime/task control |  |

