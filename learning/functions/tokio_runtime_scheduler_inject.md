# `tokio::runtime::scheduler::inject` — 30 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 25 |
| Trait impl | 4 |
| Private helper | 1 |

## `tokio/src/runtime/scheduler/inject/metrics.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `len`  | `Inject<T>` | Crate-internal | Accessor / query |  |

## `tokio/src/runtime/scheduler/inject/pop.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `new`  | `Pop<'a, T>` | Crate-internal | Constructor |  |
| 26 | `next`  | `Iterator for Pop<'a, T>` | Trait impl | Iterator |  |
| 40 | `size_hint`  | `Iterator for Pop<'a, T>` | Trait impl | Iterator |  |
| 46 | `len`  | `ExactSizeIterator for Pop<'a, T>` | Trait impl | Accessor / query |  |
| 52 | `drop`  | `Drop for Pop<'a, T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/runtime/scheduler/inject/rt_multi_thread.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `new`  | `InjectQueue<T>` | Crate-internal | Constructor |  |
| 19 | `is_empty`  | `InjectQueue<T>` | Crate-internal | Accessor / query |  |
| 25 | `len`  | `InjectQueue<T>` | Crate-internal | Accessor / query |  |
| 31 | `is_closed`  | `InjectQueue<T>` | Crate-internal | Accessor / query |  |
| 39 | `close`  | `InjectQueue<T>` | Crate-internal | Data movement | Closes the queue, returns `true` if the queue was open when the transition was made. |
| 48 | `push`  | `InjectQueue<T>` | Crate-internal | Data movement | Pushes a value into the queue. |
| 54 | `pop`  | `InjectQueue<T>` | Crate-internal | Data movement |  |
| 63 | `push_batch`  | `InjectQueue<T>` | Crate-internal | Data movement | Pushes several values into the queue. |
| 75 | `pop_n`  | `InjectQueue<T>` | Crate-internal | Data movement | Pops up to `n` values from the queue, passing an iterator over them to `f`. |
| 84 | `drain_into`  | `InjectQueue<T>` | Crate-internal | Combinator / iteration | Pops every task from the queue into `dst`, atomically with respect to concurrent pushes. |
| 92 | `is_empty`  | `Inject<T>` | Crate-internal | Accessor / query |  |
| 98 | `push_batch`  | `Inject<T>` | Crate-internal | Data movement | Pushes several values into the queue. |
| 143 | `push_batch_inner` ⚠ | `Inject<T>` | Private helper | Data movement | Inserts several tasks that have been linked together into the queue. |
| 196 | `pop_n`  | `Inject<T>` | Crate-internal | Data movement | Pops up to `n` values from the queue, passing an iterator over them to `f`. |
| 205 | `drain_into`  | `Inject<T>` | Crate-internal | Combinator / iteration | Pops every task from the queue into `dst`, holding the queue lock for the entire drain so it is atomic with respect to concurrent pushes. |

## `tokio/src/runtime/scheduler/inject/shared.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `new`  | `Shared<T>` | Crate-internal | Constructor |  |
| 36 | `is_empty`  | `Shared<T>` | Crate-internal | Accessor / query |  |
| 42 | `is_closed`  | `Shared<T>` | Crate-internal | Accessor / query |  |
| 48 | `close`  | `Shared<T>` | Crate-internal | Data movement | Closes the injection queue, returns `true` if the queue is open when the transition is made. |
| 57 | `len`  | `Shared<T>` | Crate-internal | Accessor / query |  |
| 68 | `push` ⚠ | `Shared<T>` | Crate-internal | Data movement | Pushes a value into the queue. |
| 97 | `pop` ⚠ | `Shared<T>` | Crate-internal | Data movement | Pop a value from the queue. |
| 106 | `pop_n` ⚠ | `Shared<T>` | Crate-internal | Data movement | Pop `n` values from the queue |

## `tokio/src/runtime/scheduler/inject/synced.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `pop`  | `Synced` | Crate-internal | Data movement |  |

