# `tokio::signal::windows` — 21 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 10 |
| Test | 7 |
| Private helper | 3 |
| Trait impl | 1 |

## `tokio/src/signal/windows/stub.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `ctrl_break`  |  | Crate-internal | Other / internal logic |  |
| 11 | `ctrl_close`  |  | Crate-internal | Other / internal logic |  |
| 15 | `ctrl_c`  |  | Crate-internal | Other / internal logic |  |
| 19 | `ctrl_logoff`  |  | Crate-internal | Other / internal logic |  |
| 23 | `ctrl_shutdown`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/signal/windows/sys.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `terminates` 🅲 | `SignalKind` | Private helper | Other / internal logic |  |
| 39 | `ctrl_break`  |  | Crate-internal | Other / internal logic |  |
| 43 | `ctrl_close`  |  | Crate-internal | Other / internal logic |  |
| 47 | `ctrl_c`  |  | Crate-internal | Other / internal logic |  |
| 51 | `ctrl_logoff`  |  | Crate-internal | Other / internal logic |  |
| 55 | `ctrl_shutdown`  |  | Crate-internal | Other / internal logic |  |
| 59 | `new`  |  | Private helper | Constructor |  |
| 91 | `index`  | `Index<SignalKind> for Registry` | Trait impl | Other / internal logic |  |
| 108 | `handler` ⚠ |  | Private helper | Other / internal logic |  |
| 151 | `raise_event` ⚠ |  | Test | Other / internal logic |  |
| 162 | `ctrl_c`  |  | Test | Other / internal logic |  |
| 181 | `ctrl_break`  |  | Test | Other / internal logic |  |
| 199 | `ctrl_close`  |  | Test | Other / internal logic |  |
| 217 | `ctrl_shutdown`  |  | Test | Other / internal logic |  |
| 235 | `ctrl_logoff`  |  | Test | Other / internal logic |  |
| 252 | `rt`  |  | Test | Other / internal logic |  |

