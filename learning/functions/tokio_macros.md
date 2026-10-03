# `tokio::macros` — 5 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 5 |

## `tokio/src/macros/join.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 259 | `num_skip`  | `Rotator<COUNT>` | Public API | Accessor / query | Rotates by one each [`Self::num_skip`] call up to COUNT - 1 |
| 276 | `num_skip`  | `BiasedRotator` | Public API | Accessor / query | Always returns 0. |

## `tokio/src/macros/support.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `thread_rng_n`  |  | Public API | Configuration / setter |  |
| 16 | `poll_budget_available`  |  | Public API | Poll function |  |
| 24 | `poll_budget_available`  |  | Public API | Poll function |  |

