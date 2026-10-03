# `tokio::task::coop` — 30 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Private helper | 11 |
| Public API | 6 |
| Crate-internal | 6 |
| Trait impl | 5 |
| Test | 2 |

## `tokio/src/task/coop/consume_budget.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `consume_budget` 🅰 |  | Public API | I/O operation | Consumes a unit of budget and returns the execution back to the Tokio runtime *if* the task's coop budget was exhausted. |

## `tokio/src/task/coop/mod.rs` (26)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 115 | `initial` 🅲 | `Budget` | Private helper | Other / internal logic | Budget assigned to a task on each poll. |
| 120 | `unconstrained` 🅲 | `Budget` | Crate-internal | Other / internal logic | Returns an unconstrained budget. |
| 124 | `has_remaining`  | `Budget` | Private helper | Accessor / query |  |
| 132 | `budget`  |  | Crate-internal | Other / internal logic | Runs the given closure with a cooperative task budget. |
| 139 | `with_unconstrained`  |  | Crate-internal | Constructor | Runs the given closure with an unconstrained task budget. |
| 144 | `with_budget`  |  | Private helper | Constructor |  |
| 150 | `drop`  | `Drop for ResetGuard` | Trait impl | Drop / cleanup |  |
| 223 | `has_budget_remaining`  |  | Public API | Accessor / query | Returns `true` if there is still budget left on the task. |
| 231 | `set`  |  | Crate-internal | Configuration / setter | Sets the current task's budget. |
| 240 | `stop`  |  | Crate-internal | Other / internal logic | Forcibly removes the budgeting constraints early. |
| 263 | `new`  | `RestoreOnPending` | Private helper | Constructor |  |
| 273 | `made_progress`  | `RestoreOnPending` | Public API | Other / internal logic | Signals that the task that obtained this `RestoreOnPending` was able to make progress. |
| 279 | `drop`  | `Drop for RestoreOnPending` | Trait impl | Drop / cleanup |  |
| 343 | `poll_proceed`  |  | Public API | Poll function | Decrements the task budget and returns [`Poll::Pending`] if the budget is depleted. |
| 371 | `poll_budget_available`  |  | Crate-internal | Poll function | Returns `Poll::Ready` if the current task has budget to consume, and `Poll::Pending` otherwise. |
| 384 | `inc_budget_forced_yield_count`  |  | Private helper | Metrics / counters |  |
| 393 | `inc_budget_forced_yield_count`  |  | Private helper | Metrics / counters |  |
| 396 | `register_waker`  |  | Private helper | I/O registration |  |
| 403 | `inc_budget_forced_yield_count`  |  | Private helper | Metrics / counters |  |
| 405 | `register_waker`  |  | Private helper | I/O registration |  |
| 413 | `decrement`  | `Budget` | Private helper | Other / internal logic | Decrements the budget. |
| 429 | `is_unconstrained`  | `Budget` | Private helper | Accessor / query |  |
| 447 | `poll`  | `Future for Coop<F>` | Trait impl | Future impl (poll) |  |
| 491 | `cooperative`  |  | Public API | Other / internal logic | Creates a wrapper future that makes the inner future cooperate with the Tokio scheduler. |
| 503 | `get`  |  | Test | Accessor / query |  |
| 508 | `budgeting`  |  | Test | Other / internal logic |  |

## `tokio/src/task/coop/unconstrained.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `poll`  | `Future for Unconstrained<F>` | Trait impl | Future impl (poll) |  |
| 30 | `poll`  | `Future for Unconstrained<F>` | Trait impl | Future impl (poll) |  |
| 43 | `unconstrained`  |  | Public API | Other / internal logic | Turn off cooperative scheduling for a future. |

