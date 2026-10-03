# `tokio::runtime::tests::loom_multi_thread` — 9 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 9 |

## `tokio/src/runtime/tests/loom_multi_thread/queue.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `new_stats`  |  | Test | Constructor |  |
| 12 | `basic`  |  | Test | Other / internal logic |  |
| 66 | `steal_overflow`  |  | Test | Data movement |  |
| 116 | `multi_stealer`  |  | Test | Other / internal logic |  |
| 119 | `steal_tasks`  |  | Test | Data movement |  |
| 170 | `chained_steal`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/tests/loom_multi_thread/shutdown.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `join_handle_cancel_on_shutdown`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/tests/loom_multi_thread/yield_now.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 6 | `yield_calls_park_before_scheduling_again`  |  | Test | Other / internal logic |  |
| 32 | `mk_runtime`  |  | Test | Other / internal logic |  |

