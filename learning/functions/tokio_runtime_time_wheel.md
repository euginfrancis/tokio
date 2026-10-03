# `tokio::runtime::time::wheel` — 45 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 20 |
| Crate-internal | 13 |
| Private helper | 11 |
| Trait impl | 1 |

## `tokio/src/runtime/time/wheel/level.rs` (23)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 42 | `new`  | `Level` | Crate-internal | Constructor |  |
| 52 | `next_expiration`  | `Level` | Crate-internal | Time / timers | Finds the slot that needs to be processed next and returns the slot and `Instant` at which this slot must be processed. |
| 109 | `next_occupied_slot`  | `Level` | Private helper | Other / internal logic |  |
| 130 | `add_entry` ⚠ | `Level` | Crate-internal | Other / internal logic |  |
| 138 | `remove_entry` ⚠ | `Level` | Crate-internal | Data movement |  |
| 156 | `take_slot`  | `Level` | Crate-internal | Data movement |  |
| 164 | `fmt`  | `fmt::Debug for Level` | Trait impl | Formatting |  |
| 171 | `occupied_bit`  |  | Private helper | Other / internal logic |  |
| 175 | `slot_range`  |  | Private helper | Other / internal logic |  |
| 179 | `level_range`  |  | Private helper | Other / internal logic |  |
| 184 | `slot_for`  |  | Private helper | Time / timers | Converts a duration (milliseconds) and a level to a slot position. |
| 193 | `test_slot_for`  |  | Test | Other / internal logic |  |
| 206 | `level_with`  |  | Test | Other / internal logic |  |
| 213 | `next_occupied_slot_on_an_empty_level`  |  | Test | Other / internal logic |  |
| 219 | `next_occupied_slot_of_a_single_slot`  |  | Test | Other / internal logic |  |
| 233 | `next_occupied_slot_picks_the_nearest_slot_forward`  |  | Test | Other / internal logic |  |
| 243 | `next_occupied_slot_skips_the_slot_holding_now`  |  | Test | Other / internal logic |  |
| 259 | `next_occupied_slot_of_the_slot_holding_now_when_it_is_the_only_one`  |  | Test | Other / internal logic |  |
| 269 | `next_occupied_slot_of_the_last_slot`  |  | Test | Other / internal logic |  |
| 277 | `next_expiration_reports_the_start_of_the_slot`  |  | Test | Time / timers |  |
| 287 | `next_expiration_below_the_top_level`  |  | Test | Time / timers |  |
| 295 | `next_expiration_at_the_top_level`  |  | Test | Time / timers |  |
| 303 | `next_expiration_wraps_a_slot_at_or_behind_now`  |  | Test | Time / timers |  |

## `tokio/src/runtime/time/wheel/mod.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 54 | `new`  | `Wheel` | Crate-internal | Constructor | Creates a new timing wheel. |
| 65 | `elapsed`  | `Wheel` | Crate-internal | Time / timers | Returns the number of milliseconds that have elapsed since the timing wheel's creation. |
| 90 | `insert` ⚠ | `Wheel` | Crate-internal | Data movement | Inserts an entry into the timing wheel. |
| 117 | `remove` ⚠ | `Wheel` | Crate-internal | Data movement | Removes `item` from the timing wheel. |
| 137 | `poll_at`  | `Wheel` | Crate-internal | Poll function | Instant at which to poll. |
| 142 | `poll`  | `Wheel` | Crate-internal | Poll function | Advances the timer up to the instant represented by `now`. |
| 169 | `next_expiration`  | `Wheel` | Private helper | Time / timers | Returns the instant at which the next timeout expires. |
| 195 | `next_expiration_time`  | `Wheel` | Crate-internal | Time / timers | Returns the tick at which this timer wheel next needs to perform some processing, or None if there are no timers registered. |
| 200 | `no_expirations_before`  | `Wheel` | Private helper | Other / internal logic | Used for debug assertions |
| 218 | `process_expiration`  | `Wheel` | Crate-internal | Time / timers | iteratively find entries that are between the wheel's current time and the expiration time. |
| 253 | `set_elapsed`  | `Wheel` | Private helper | Configuration / setter |  |
| 267 | `take_entries`  | `Wheel` | Private helper | Data movement | Obtains the list of entries that need processing for the given expiration. |
| 271 | `level_for`  | `Wheel` | Private helper | Time / timers |  |
| 276 | `level_for`  |  | Private helper | Time / timers |  |
| 298 | `test_level_for`  |  | Test | Other / internal logic |  |
| 334 | `insert_entry`  |  | Test | Data movement |  |
| 345 | `test_next_expiration_to_level_4`  |  | Test | Other / internal logic |  |
| 370 | `test_next_expiration_to_level_5`  |  | Test | Other / internal logic |  |
| 394 | `test_next_expiration_after_level_5`  |  | Test | Other / internal logic |  |
| 419 | `test_next_expiration_after_level_5_twice`  |  | Test | Other / internal logic |  |
| 450 | `test_next_expiration_to_level_5_and_after_level_5`  |  | Test | Other / internal logic |  |
| 483 | `test_next_expiration_at_slot_5_of_the_top_level`  |  | Test | Other / internal logic |  |

