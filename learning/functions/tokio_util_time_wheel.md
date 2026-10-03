# `tokio-util::time::wheel` — 36 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 14 |
| Private helper | 12 |
| Trait method (declaration/default) | 7 |
| Test | 2 |
| Trait impl | 1 |

## `tokio-util/src/time/wheel/level.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `Level<T>` | Crate-internal | Constructor |  |
| 51 | `next_expiration`  | `Level<T>` | Crate-internal | Time / timers | Finds the slot that needs to be processed next and returns the slot and `Instant` at which this slot must be processed. |
| 103 | `next_occupied_slot`  | `Level<T>` | Private helper | Other / internal logic |  |
| 117 | `add_entry`  | `Level<T>` | Crate-internal | Other / internal logic |  |
| 124 | `remove_entry`  | `Level<T>` | Crate-internal | Data movement |  |
| 138 | `pop_entry_slot`  | `Level<T>` | Crate-internal | Data movement |  |
| 151 | `peek_entry_slot`  | `Level<T>` | Crate-internal | Combinator / iteration |  |
| 157 | `fmt`  | `fmt::Debug for Level<T>` | Trait impl | Formatting |  |
| 164 | `occupied_bit`  |  | Private helper | Other / internal logic |  |
| 168 | `slot_range`  |  | Private helper | Other / internal logic |  |
| 172 | `level_range`  |  | Private helper | Other / internal logic |  |
| 177 | `slot_for`  |  | Private helper | Time / timers | Convert a duration (milliseconds) and a level to a slot position |
| 186 | `test_slot_for`  |  | Test | Other / internal logic |  |

## `tokio-util/src/time/wheel/mod.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 61 | `new`  | `Wheel<T>` | Crate-internal | Constructor | Create a new timing wheel |
| 69 | `elapsed`  | `Wheel<T>` | Crate-internal | Time / timers | Return the number of milliseconds that have elapsed since the timing wheel's creation. |
| 94 | `insert`  | `Wheel<T>` | Crate-internal | Data movement | Insert an entry into the timing wheel. |
| 122 | `remove`  | `Wheel<T>` | Crate-internal | Data movement | Remove `item` from the timing wheel. |
| 138 | `poll_at`  | `Wheel<T>` | Crate-internal | Poll function | Instant at which to poll |
| 143 | `peek`  | `Wheel<T>` | Crate-internal | Combinator / iteration | Next key that will expire |
| 149 | `poll`  | `Wheel<T>` | Crate-internal | Poll function | Advances the timer up to the instant represented by `now`. |
| 172 | `next_expiration`  | `Wheel<T>` | Private helper | Time / timers | Returns the instant at which the next timeout expires. |
| 188 | `no_expirations_before`  | `Wheel<T>` | Private helper | Other / internal logic | Used for debug assertions |
| 206 | `poll_expiration`  | `Wheel<T>` | Crate-internal | Poll function | iteratively find entries that are between the wheel's current time and the expiration time. |
| 228 | `set_elapsed`  | `Wheel<T>` | Private helper | Configuration / setter |  |
| 241 | `pop_entry`  | `Wheel<T>` | Private helper | Data movement |  |
| 245 | `peek_entry`  | `Wheel<T>` | Private helper | Combinator / iteration |  |
| 249 | `level_for`  | `Wheel<T>` | Private helper | Time / timers |  |
| 254 | `level_for`  |  | Private helper | Time / timers |  |
| 274 | `test_level_for`  |  | Test | Other / internal logic |  |

## `tokio-util/src/time/wheel/stack.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `is_empty`  | `trait Stack` | Trait method (declaration/default) | Accessor / query | Returns `true` if the stack is empty |
| 20 | `push`  | `trait Stack` | Trait method (declaration/default) | Data movement | Push an item onto the stack |
| 23 | `pop`  | `trait Stack` | Trait method (declaration/default) | Data movement | Pop an item from the stack |
| 26 | `peek`  | `trait Stack` | Trait method (declaration/default) | Combinator / iteration | Peek into the stack. |
| 33 | `peek_earliest`  | `trait Stack` | Trait method (declaration/default) | Combinator / iteration | Peek at the item in the stack with the earliest deadline. |
| 35 | `remove`  | `trait Stack` | Trait method (declaration/default) | Data movement |  |
| 37 | `when`  | `trait Stack` | Trait method (declaration/default) | Other / internal logic |  |

