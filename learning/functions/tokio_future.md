# `tokio::future` — 13 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 3 |
| Public API | 3 |
| Trait impl | 3 |
| Test | 3 |
| Trait method (declaration/default) | 1 |

## `tokio/src/future/block_on.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 5 | `block_on`  |  | Crate-internal | Runtime/task control |  |
| 18 | `block_on`  |  | Crate-internal | Runtime/task control |  |

## `tokio/src/future/maybe_done.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `maybe_done`  |  | Public API | Other / internal logic | Wraps a future into a `MaybeDone`. |
| 37 | `output_mut`  | `MaybeDone<Fut>` | Public API | Other / internal logic | Returns an [`Option`] containing a mutable reference to the output of the future. |
| 47 | `take_output`  | `MaybeDone<Fut>` | Public API | Data movement | Attempts to take the output of a `MaybeDone` without driving it towards completion. |
| 63 | `poll`  | `Future for MaybeDone<Fut>` | Trait impl | Future impl (poll) |  |
| 93 | `poll`  | `Future for ThingAdder<'_>` | Test | Future impl (poll) |  |
| 102 | `maybe_done_miri`  |  | Test | Other / internal logic |  |
| 121 | `wake`  | `Wake for DummyWaker` | Test | Waker |  |

## `tokio/src/future/trace.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `id`  | `trait InstrumentedFuture` | Trait method (declaration/default) | Accessor / query |  |
| 8 | `id`  | `InstrumentedFuture for tracing::instrument::Instrumented<F>` | Trait impl | Accessor / query |  |

## `tokio/src/future/try_join.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 8 | `try_join3`  |  | Crate-internal | Non-blocking attempt |  |
| 49 | `poll`  | `Future for TryJoin3<F1, F2, F3>` | Trait impl | Future impl (poll) |  |

