# `tokio-util::time` — 59 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 23 |
| Trait impl | 15 |
| Crate-internal | 13 |
| Private helper | 8 |

## `tokio-util/src/time/delay_queue.rs` (58)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 181 | `with_capacity`  | `SlabStorage<T>` | Crate-internal | Constructor |  |
| 191 | `insert`  | `SlabStorage<T>` | Crate-internal | Data movement |  |
| 231 | `remove`  | `SlabStorage<T>` | Crate-internal | Data movement |  |
| 244 | `shrink_to_fit`  | `SlabStorage<T>` | Crate-internal | Other / internal logic |  |
| 249 | `compact`  | `SlabStorage<T>` | Crate-internal | Other / internal logic |  |
| 278 | `remap_key`  | `SlabStorage<T>` | Private helper | Other / internal logic |  |
| 287 | `create_new_key`  | `SlabStorage<T>` | Private helper | Constructor |  |
| 295 | `len`  | `SlabStorage<T>` | Crate-internal | Accessor / query |  |
| 299 | `capacity`  | `SlabStorage<T>` | Crate-internal | Accessor / query |  |
| 303 | `clear`  | `SlabStorage<T>` | Crate-internal | Configuration / setter |  |
| 309 | `reserve`  | `SlabStorage<T>` | Crate-internal | Other / internal logic |  |
| 317 | `is_empty`  | `SlabStorage<T>` | Crate-internal | Accessor / query |  |
| 321 | `contains`  | `SlabStorage<T>` | Crate-internal | Other / internal logic |  |
| 335 | `fmt`  | `fmt::Debug for SlabStorage<T>` | Trait impl | Formatting |  |
| 350 | `index`  | `Index<Key> for SlabStorage<T>` | Trait impl | Other / internal logic |  |
| 361 | `index_mut`  | `IndexMut<Key> for SlabStorage<T>` | Trait impl | Other / internal logic |  |
| 448 | `new`  | `DelayQueue<T>` | Public API | Constructor | Creates a new, empty, `DelayQueue`. |
| 477 | `with_capacity`  | `DelayQueue<T>` | Public API | Constructor | Creates a new, empty, `DelayQueue` with the specified capacity. |
| 538 | `insert_at`  | `DelayQueue<T>` | Public API | Data movement | Inserts `value` into the queue set to expire at a specific instant in time. |
| 582 | `poll_expired`  | `DelayQueue<T>` | Public API | Poll function | Attempts to pull out the next value of the delay queue, registering the current task for wakeup if the value is not yet available, and returning `None` if the queue is exhausted. |
| 652 | `insert`  | `DelayQueue<T>` | Public API | Data movement | Inserts `value` into the queue set to expire after the requested duration elapses. |
| 657 | `insert_idx`  | `DelayQueue<T>` | Private helper | Data movement |  |
| 701 | `deadline`  | `DelayQueue<T>` | Public API | Time / timers | Returns the deadline of the item associated with `key`. |
| 712 | `remove_key`  | `DelayQueue<T>` | Private helper | Data movement | Removes the key from the expired queue or the timer wheel depending on its expiration status. |
| 752 | `remove`  | `DelayQueue<T>` | Public API | Data movement | Removes the item associated with `key` from the queue. |
| 809 | `try_remove`  | `DelayQueue<T>` | Public API | Non-blocking attempt | Attempts to remove the item associated with `key` from the queue. |
| 852 | `reset_at`  | `DelayQueue<T>` | Public API | Time / timers | Sets the delay of the item associated with `key` to expire at `when`. |
| 887 | `shrink_to_fit`  | `DelayQueue<T>` | Public API | Other / internal logic | Shrink the capacity of the slab, which `DelayQueue` uses internally for storage allocation. |
| 918 | `compact`  | `DelayQueue<T>` | Public API | Other / internal logic | Shrink the capacity of the slab, which `DelayQueue` uses internally for storage allocation, to the number of elements that are contained in it. |
| 951 | `peek`  | `DelayQueue<T>` | Public API | Combinator / iteration | Gets the [`Key`] that [`poll_expired`] will pull out of the queue next, without pulling it out or waiting for the deadline to expire. |
| 960 | `next_deadline`  | `DelayQueue<T>` | Private helper | Other / internal logic | Returns the next time to poll as determined by the wheel. |
| 1002 | `reset`  | `DelayQueue<T>` | Public API | Configuration / setter | Sets the delay of the item associated with `key` to expire after `timeout`. |
| 1033 | `clear`  | `DelayQueue<T>` | Public API | Configuration / setter | Clears the queue, removing all items. |
| 1058 | `capacity`  | `DelayQueue<T>` | Public API | Accessor / query | Returns the number of elements the queue can hold without reallocating. |
| 1078 | `len`  | `DelayQueue<T>` | Public API | Accessor / query | Returns the number of elements currently in the queue. |
| 1116 | `reserve`  | `DelayQueue<T>` | Public API | Other / internal logic | Reserves capacity for at least `additional` more items to be queued without allocating. |
| 1144 | `is_empty`  | `DelayQueue<T>` | Public API | Accessor / query | Returns `true` if there are no items in the queue. |
| 1152 | `poll_idx`  | `DelayQueue<T>` | Private helper | Poll function | Polls the queue, returning the index of the next slot in the slab that should be returned. |
| 1187 | `normalize_deadline`  | `DelayQueue<T>` | Private helper | Other / internal logic |  |
| 1202 | `default`  | `Default for DelayQueue<T>` | Trait impl | Constructor |  |
| 1212 | `poll_next`  | `futures_core::Stream for DelayQueue<T>` | Trait impl | Stream impl |  |
| 1222 | `is_empty`  | `wheel::Stack for Stack<T>` | Trait impl | Accessor / query |  |
| 1226 | `push`  | `wheel::Stack for Stack<T>` | Trait impl | Data movement |  |
| 1242 | `pop`  | `wheel::Stack for Stack<T>` | Trait impl | Data movement |  |
| 1259 | `peek`  | `wheel::Stack for Stack<T>` | Trait impl | Combinator / iteration |  |
| 1263 | `peek_earliest`  | `wheel::Stack for Stack<T>` | Trait impl | Combinator / iteration |  |
| 1285 | `remove`  | `wheel::Stack for Stack<T>` | Trait impl | Data movement |  |
| 1323 | `when`  | `wheel::Stack for Stack<T>` | Trait impl | Other / internal logic |  |
| 1329 | `default`  | `Default for Stack<T>` | Trait impl | Constructor |  |
| 1338 | `new`  | `Key` | Crate-internal | Constructor |  |
| 1344 | `new`  | `KeyInternal` | Crate-internal | Constructor |  |
| 1350 | `from`  | `From<Key> for KeyInternal` | Trait impl | Conversion |  |
| 1356 | `from`  | `From<KeyInternal> for Key` | Trait impl | Conversion |  |
| 1363 | `get_ref`  | `Expired<T>` | Public API | Accessor / query | Returns a reference to the inner value. |
| 1368 | `get_mut`  | `Expired<T>` | Public API | Accessor / query | Returns a mutable reference to the inner value. |
| 1373 | `into_inner`  | `Expired<T>` | Public API | Conversion | Consumes `self` and returns the inner value. |
| 1378 | `deadline`  | `Expired<T>` | Public API | Time / timers | Returns the deadline that the expiration was set to. |
| 1383 | `key`  | `Expired<T>` | Public API | Other / internal logic | Returns the key that the expiration is indexed by. |

## `tokio-util/src/time/mod.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `ms`  |  | Private helper | Other / internal logic | Convert a `Duration` to milliseconds, rounding up and saturating at `u64::MAX`. |

