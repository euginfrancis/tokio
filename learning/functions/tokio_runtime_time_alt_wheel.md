# `tokio::runtime::time_alt::wheel` — 45 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 21 |
| Crate-internal | 12 |
| Private helper | 11 |
| Trait impl | 1 |

## `tokio/src/runtime/time_alt/wheel/level.rs` (23)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `new`  | `Level` | Crate-internal | Constructor |  |
| 53 | `next_expiration`  | `Level` | Crate-internal | Time / timers | Finds the slot that needs to be processed next and returns the slot and `Instant` at which this slot must be processed. |
| 110 | `next_occupied_slot`  | `Level` | Private helper | Other / internal logic |  |
| 131 | `add_entry` ⚠ | `Level` | Crate-internal | Other / internal logic |  |
| 141 | `remove_entry` ⚠ | `Level` | Crate-internal | Data movement |  |
| 159 | `take_slot`  | `Level` | Crate-internal | Data movement |  |
| 167 | `fmt`  | `fmt::Debug for Level` | Trait impl | Formatting |  |
| 174 | `occupied_bit`  |  | Private helper | Other / internal logic |  |
| 178 | `slot_range`  |  | Private helper | Other / internal logic |  |
| 182 | `level_range`  |  | Private helper | Other / internal logic |  |
| 187 | `slot_for`  |  | Private helper | Time / timers | Converts a duration (milliseconds) and a level to a slot position. |
| 196 | `test_slot_for`  |  | Test | Other / internal logic |  |
| 209 | `level_with`  |  | Test | Other / internal logic |  |
| 216 | `next_occupied_slot_on_an_empty_level`  |  | Test | Other / internal logic |  |
| 222 | `next_occupied_slot_of_a_single_slot`  |  | Test | Other / internal logic |  |
| 236 | `next_occupied_slot_picks_the_nearest_slot_forward`  |  | Test | Other / internal logic |  |
| 246 | `next_occupied_slot_skips_the_slot_holding_now`  |  | Test | Other / internal logic |  |
| 262 | `next_occupied_slot_of_the_slot_holding_now_when_it_is_the_only_one`  |  | Test | Other / internal logic |  |
| 272 | `next_occupied_slot_of_the_last_slot`  |  | Test | Other / internal logic |  |
| 280 | `next_expiration_reports_the_start_of_the_slot`  |  | Test | Time / timers |  |
| 290 | `next_expiration_below_the_top_level`  |  | Test | Time / timers |  |
| 298 | `next_expiration_at_the_top_level`  |  | Test | Time / timers |  |
| 306 | `next_expiration_wraps_a_slot_at_or_behind_now`  |  | Test | Time / timers |  |

## `tokio/src/runtime/time_alt/wheel/mod.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 45 | `new`  | `Wheel` | Crate-internal | Constructor | Creates a new timing wheel. |
| 55 | `elapsed`  | `Wheel` | Crate-internal | Time / timers | Returns the number of milliseconds that have elapsed since the timing wheel's creation. |
| 70 | `insert` ⚠ | `Wheel` | Crate-internal | Data movement | Inserts an entry into the timing wheel |
| 100 | `remove` ⚠ | `Wheel` | Crate-internal | Data movement | Removes `item` from the timing wheel. |
| 114 | `take_expired`  | `Wheel` | Crate-internal | Data movement | Advances the timer up to the instant represented by `now`. |
| 127 | `next_expiration`  | `Wheel` | Private helper | Time / timers | Returns the instant at which the next timeout expires. |
| 144 | `next_expiration_time`  | `Wheel` | Crate-internal | Time / timers | Returns the tick at which this timer wheel next needs to perform some processing, or None if there are no timers registered. |
| 149 | `no_expirations_before`  | `Wheel` | Private helper | Other / internal logic | Used for debug assertions |
| 160 | `process_expiration`  | `Wheel` | Crate-internal | Time / timers | iteratively find entries that are between the wheel's current time and the expiration time. |
| 197 | `set_elapsed`  | `Wheel` | Private helper | Configuration / setter |  |
| 211 | `take_entries`  | `Wheel` | Private helper | Data movement | Obtains the list of entries that need processing for the given expiration. |
| 215 | `level_for`  | `Wheel` | Private helper | Time / timers |  |
| 220 | `level_for`  |  | Private helper | Time / timers |  |
| 241 | `test_level_for`  |  | Test | Other / internal logic |  |
| 277 | `insert_entry`  |  | Test | Data movement |  |
| 284 | `poll`  |  | Test | Poll function |  |
| 290 | `test_next_expiration_to_level_4`  |  | Test | Other / internal logic |  |
| 315 | `test_next_expiration_to_level_5`  |  | Test | Other / internal logic |  |
| 339 | `test_next_expiration_after_level_5`  |  | Test | Other / internal logic |  |
| 364 | `test_next_expiration_after_level_5_twice`  |  | Test | Other / internal logic |  |
| 395 | `test_next_expiration_to_level_5_and_after_level_5`  |  | Test | Other / internal logic |  |
| 428 | `test_next_expiration_at_slot_5_of_the_top_level`  |  | Test | Other / internal logic |  |

