# `tokio::util` — 169 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 97 |
| Private helper | 31 |
| Trait impl | 27 |
| Trait method (declaration/default) | 7 |
| Test | 6 |
| Public API | 1 |

## `tokio/src/util/as_ref.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `as_ref`  | `AsRef<[u8]> for OwnedBuf` | Trait impl | Conversion |  |
| 20 | `upgrade`  |  | Crate-internal | Handle / reference plumbing |  |

## `tokio/src/util/atomic_cell.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `new`  | `AtomicCell<T>` | Crate-internal | Constructor |  |
| 20 | `swap`  | `AtomicCell<T>` | Crate-internal | Other / internal logic |  |
| 25 | `set`  | `AtomicCell<T>` | Crate-internal | Configuration / setter |  |
| 29 | `take`  | `AtomicCell<T>` | Crate-internal | Data movement |  |
| 34 | `to_raw`  |  | Private helper | Conversion |  |
| 38 | `from_raw`  |  | Private helper | Conversion |  |
| 47 | `drop`  | `Drop for AtomicCell<T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/util/bit.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `least_significant` 🅲 | `Pack` | Crate-internal | Other / internal logic | Value is packed in the `width` least-significant bits. |
| 18 | `then` 🅲 | `Pack` | Crate-internal | Other / internal logic | Value is packed in the `width` more-significant bits. |
| 26 | `width` 🅲 | `Pack` | Crate-internal | Other / internal logic | Width, in bits, dedicated to storing the value. |
| 31 | `max_value` 🅲 | `Pack` | Crate-internal | Configuration / setter | Max representable value. |
| 35 | `pack`  | `Pack` | Crate-internal | Other / internal logic |  |
| 40 | `unpack`  | `Pack` | Crate-internal | Other / internal logic |  |
| 46 | `fmt`  | `fmt::Debug for Pack` | Trait impl | Formatting |  |
| 56 | `mask_for` 🅲 |  | Crate-internal | Other / internal logic | Returns a `usize` with the right-most `n` bits set. |
| 62 | `unpack` 🅲 |  | Crate-internal | Other / internal logic | Unpacks a value using a mask & shift. |

## `tokio/src/util/blocking_check.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `check_socket_for_blocking`  |  | Crate-internal | Runtime/task control |  |
| 25 | `check_socket_for_blocking`  |  | Crate-internal | Runtime/task control |  |

## `tokio/src/util/cacheline.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 72 | `new`  | `CachePadded<T>` | Crate-internal | Constructor | Pads and aligns a value to the length of a cache line. |
| 80 | `deref`  | `Deref for CachePadded<T>` | Trait impl | Deref |  |
| 86 | `deref_mut`  | `DerefMut for CachePadded<T>` | Trait impl | Deref |  |

## `tokio/src/util/idle_notified_set.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 103 | `addr_of_pointers` ⚠ | `ListEntry<T>` | Private helper | Handle / reference plumbing |  |
| 125 | `new`  | `IdleNotifiedSet<T>` | Crate-internal | Constructor | Create a new `IdleNotifiedSet`. |
| 138 | `len`  | `IdleNotifiedSet<T>` | Crate-internal | Accessor / query |  |
| 142 | `is_empty`  | `IdleNotifiedSet<T>` | Crate-internal | Accessor / query |  |
| 147 | `insert_idle`  | `IdleNotifiedSet<T>` | Crate-internal | Data movement | Insert the given value into the `idle` list. |
| 169 | `pop_notified`  | `IdleNotifiedSet<T>` | Crate-internal | Data movement | Pop an entry from the notified list to poll it. |
| 205 | `try_pop_notified`  | `IdleNotifiedSet<T>` | Crate-internal | Non-blocking attempt | Tries to pop an entry from the notified list to poll it. |
| 232 | `for_each`  | `IdleNotifiedSet<T>` | Crate-internal | Combinator / iteration | Call a function on every element in this list. |
| 233 | `get_ptrs`  |  | Private helper | Accessor / query |  |
| 278 | `drain`  | `IdleNotifiedSet<T>` | Crate-internal | Combinator / iteration | Remove all entries in both lists, applying some function to each element. |
| 296 | `pop_next`  | `AllEntries<T, F>` | Private helper | Data movement |  |
| 311 | `drop`  | `Drop for AllEntries<T, F>` | Trait impl | Drop / cleanup |  |
| 346 | `move_to_new_list` ⚠ |  | Private helper | Other / internal logic | # Safety The mutex for the entries must be held, and the target list must be such that setting `my_list` to `Neither` is ok. |
| 367 | `remove`  | `EntryInOneOfTheLists<'a, T>` | Crate-internal | Data movement | Remove this entry from the list it is in, returning the value associated with the entry. |
| 406 | `with_value_and_context`  | `EntryInOneOfTheLists<'a, T>` | Crate-internal | Constructor | Access the value in this entry together with a context for its waker. |
| 424 | `drop`  | `Drop for IdleNotifiedSet<T>` | Trait impl | Drop / cleanup |  |
| 438 | `wake_by_ref`  | `Wake for ListEntry<T>` | Trait impl | Waker |  |
| 466 | `wake`  | `Wake for ListEntry<T>` | Trait impl | Waker |  |
| 478 | `as_raw`  | `linked_list::Link for ListEntry<T>` | Trait impl | Intrusive-list link |  |
| 484 | `from_raw` ⚠ | `linked_list::Link for ListEntry<T>` | Trait impl | Intrusive-list link |  |
| 488 | `pointers` ⚠ | `linked_list::Link for ListEntry<T>` | Trait impl | Intrusive-list link |  |
| 504 | `join_set_test`  |  | Test | Other / internal logic |  |

## `tokio/src/util/linked_list.rs` (36)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 57 | `as_raw`  | `trait Link` | Trait method (declaration/default) | Conversion | Convert the handle to a raw pointer without consuming the handle. |
| 60 | `from_raw` ⚠ | `trait Link` | Trait method (declaration/default) | Conversion | Convert the raw pointer to a handle |
| 72 | `pointers` ⚠ | `trait Link` | Trait method (declaration/default) | Other / internal logic | Return the pointers for a node |
| 113 | `new` 🅲 | `LinkedList<L>` | Crate-internal | Constructor | Creates an empty linked list. |
| 121 | `push_front`  | `LinkedList<L>` | Crate-internal | Data movement | Adds an element first in the list. |
| 144 | `pop_front`  | `LinkedList<L>` | Crate-internal | Data movement | Removes the first element from a list and returns it, or None if it is empty. |
| 164 | `pop_back`  | `LinkedList<L>` | Crate-internal | Data movement | Removes the last element from a list and returns it, or None if it is empty. |
| 183 | `is_empty`  | `LinkedList<L>` | Crate-internal | Accessor / query | Returns whether the linked list does not contain any node |
| 202 | `remove` ⚠ | `LinkedList<L>` | Crate-internal | Data movement | Removes the specified node from the list |
| 238 | `fmt`  | `fmt::Debug for LinkedList<L>` | Trait impl | Formatting |  |
| 254 | `last`  | `LinkedList<L>` | Crate-internal | Other / internal logic |  |
| 261 | `default`  | `Default for LinkedList<L>` | Trait impl | Constructor |  |
| 276 | `drain_filter`  | `LinkedList<L>` | Crate-internal | Combinator / iteration |  |
| 295 | `next`  | `Iterator for DrainFilter<'a, L, F>` | Trait impl | Iterator |  |
| 313 | `for_each`  | `LinkedList<L>` | Crate-internal | Combinator / iteration |  |
| 356 | `into_guarded`  | `LinkedList<L>` | Crate-internal | Conversion | Turns a linked list into the guarded version by linking the guard node with the head and tail nodes. |
| 383 | `tail`  | `GuardedLinkedList<L>` | Private helper | Other / internal logic |  |
| 400 | `pop_back`  | `GuardedLinkedList<L>` | Crate-internal | Data movement | Removes the last element from a list and returns it, or None if it is empty. |
| 421 | `new`  | `Pointers<T>` | Crate-internal | Constructor | Create a new set of empty pointers |
| 431 | `get_prev`  | `Pointers<T>` | Crate-internal | Accessor / query |  |
| 435 | `get_next`  | `Pointers<T>` | Crate-internal | Accessor / query |  |
| 440 | `set_prev`  | `Pointers<T>` | Private helper | Configuration / setter |  |
| 446 | `set_next`  | `Pointers<T>` | Private helper | Configuration / setter |  |
| 455 | `fmt`  | `fmt::Debug for Pointers<T>` | Trait impl | Formatting |  |
| 483 | `as_raw`  | `Link for &'a Entry` | Trait impl | Intrusive-list link |  |
| 487 | `from_raw` ⚠ | `Link for &'a Entry` | Trait impl | Intrusive-list link |  |
| 491 | `pointers` ⚠ | `Link for &'a Entry` | Trait impl | Intrusive-list link |  |
| 496 | `entry`  |  | Private helper | Other / internal logic |  |
| 503 | `ptr`  |  | Private helper | Other / internal logic |  |
| 507 | `collect_list`  |  | Private helper | Other / internal logic |  |
| 517 | `push_all`  |  | Private helper | Data movement |  |
| 540 | `const_new`  |  | Private helper | Constructor |  |
| 545 | `push_and_drain`  |  | Private helper | Data movement |  |
| 565 | `push_pop_push_pop`  |  | Private helper | Data movement |  |
| 587 | `remove_by_address`  |  | Private helper | Data movement |  |
| 737 | `fuzz_linked_list`  |  | Public API | Other / internal logic | This is a fuzz test. |

## `tokio/src/util/memchr.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `memchr_inner`  |  | Private helper | Other / internal logic |  |
| 12 | `memchr_inner`  |  | Private helper | Other / internal logic |  |
| 36 | `memchr`  |  | Crate-internal | Other / internal logic |  |
| 58 | `memchr_test`  |  | Test | Other / internal logic |  |
| 82 | `memchr_all`  |  | Test | Other / internal logic |  |
| 97 | `memchr_empty`  |  | Test | Other / internal logic |  |

## `tokio/src/util/metric_atomics.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `load`  | `MetricAtomicU64` | Crate-internal | Other / internal logic |  |
| 28 | `store`  | `MetricAtomicU64` | Crate-internal | Configuration / setter |  |
| 32 | `new`  | `MetricAtomicU64` | Crate-internal | Constructor |  |
| 36 | `add`  | `MetricAtomicU64` | Crate-internal | Other / internal logic |  |
| 42 | `store`  | `MetricAtomicU64` | Crate-internal | Configuration / setter |  |
| 44 | `add`  | `MetricAtomicU64` | Crate-internal | Other / internal logic |  |
| 45 | `new`  | `MetricAtomicU64` | Crate-internal | Constructor |  |
| 60 | `new`  | `MetricAtomicUsize` | Crate-internal | Constructor |  |
| 66 | `load`  | `MetricAtomicUsize` | Crate-internal | Other / internal logic |  |
| 70 | `store`  | `MetricAtomicUsize` | Crate-internal | Configuration / setter |  |
| 74 | `increment`  | `MetricAtomicUsize` | Crate-internal | Other / internal logic |  |
| 78 | `decrement`  | `MetricAtomicUsize` | Crate-internal | Other / internal logic |  |

## `tokio/src/util/mod.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 108 | `pin_as_deref_mut`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/util/ptr_expose.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `new` 🅲 | `PtrExposeDomain<T>` | Crate-internal | Constructor |  |
| 30 | `expose_provenance`  | `PtrExposeDomain<T>` | Crate-internal | Other / internal logic |  |
| 46 | `from_exposed_addr`  | `PtrExposeDomain<T>` | Crate-internal | Conversion |  |
| 63 | `unexpose_provenance`  | `PtrExposeDomain<T>` | Crate-internal | Other / internal logic |  |

## `tokio/src/util/rand.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 36 | `new`  | `RngSeed` | Crate-internal | Constructor | Creates a random seed using loom internally. |
| 40 | `from_u64`  | `RngSeed` | Private helper | Conversion |  |
| 47 | `from_pair`  | `RngSeed` | Private helper | Conversion |  |
| 58 | `new`  | `FastRand` | Crate-internal | Constructor | Initialize a new fast random number generator using the default source of entropy. |
| 63 | `from_seed`  | `FastRand` | Crate-internal | Conversion | Initializes a new, thread-local, fast random number generator. |
| 71 | `fastrand_n`  | `FastRand` | Crate-internal | Other / internal logic |  |
| 78 | `fastrand`  | `FastRand` | Private helper | Other / internal logic |  |
| 97 | `non_zero_seed_from_u64`  |  | Test | Other / internal logic |  |
| 104 | `non_zero_seed_from_pair`  |  | Test | Other / internal logic |  |

## `tokio/src/util/rc_cell.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `new` 🅲 | `RcCell<T>` | Crate-internal | Constructor |  |
| 21 | `new`  | `RcCell<T>` | Crate-internal | Constructor |  |
| 29 | `with_inner` ⚠ | `RcCell<T>` | Private helper | Constructor | Safety: This method may not be called recursively. |
| 41 | `get`  | `RcCell<T>` | Crate-internal | Accessor / query |  |
| 47 | `replace`  | `RcCell<T>` | Crate-internal | Other / internal logic |  |
| 53 | `set`  | `RcCell<T>` | Crate-internal | Configuration / setter |  |

## `tokio/src/util/sharded_list.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `get_shard_id` ⚠ | `trait ShardedListItem` | Trait method (declaration/default) | Accessor / query | # Safety The provided pointer must point at a valid list item. |
| 45 | `new`  | `ShardedList<L>` | Crate-internal | Constructor | Creates a new and empty sharded linked list with the specified size. |
| 60 | `pop_back`  | `ShardedList<L>` | Crate-internal | Data movement | Removes the last element from a list specified by `shard_id` and returns it, or None if it is empty. |
| 77 | `remove` ⚠ | `ShardedList<L>` | Crate-internal | Data movement | Removes the specified node from the list. |
| 90 | `lock_shard`  | `ShardedList<L>` | Crate-internal | Locking / permits | Gets the lock of `ShardedList`, makes us have the write permission. |
| 101 | `len`  | `ShardedList<L>` | Crate-internal | Accessor / query | Gets the count of elements in this list. |
| 108 | `added`  | `ShardedList<L>` | Crate-internal | Other / internal logic | Gets the total number of elements added to this list. |
| 115 | `is_empty`  | `ShardedList<L>` | Crate-internal | Accessor / query | Returns whether the linked list does not contain any node. |
| 122 | `shard_size`  | `ShardedList<L>` | Crate-internal | Other / internal logic | Gets the shard size of this `ShardedList`. |
| 127 | `shard_inner`  | `ShardedList<L>` | Private helper | Other / internal logic |  |
| 135 | `push`  | `ShardGuard<'a, L>` | Crate-internal | Data movement | Push a value to this shard. |
| 146 | `for_each`  | `ShardedList<L>` | Crate-internal | Combinator / iteration |  |

## `tokio/src/util/sync_wrapper.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `new`  | `SyncWrapper<T>` | Crate-internal | Constructor |  |
| 25 | `into_inner`  | `SyncWrapper<T>` | Crate-internal | Conversion |  |
| 32 | `downcast_ref_sync`  | `SyncWrapper<Box<dyn Any + Send>>` | Crate-internal | Other / internal logic | Attempt to downcast using `Any::downcast_ref()` to a type that is known to be `Sync`. |

## `tokio/src/util/trace.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `new`  | `SpawnMeta<'a>` | Crate-internal | Constructor | Create new spawn meta with a name and original size (before possible auto-boxing) |
| 35 | `new_unnamed`  | `SpawnMeta<'a>` | Crate-internal | Constructor | Create a new unnamed spawn meta with the original size (before possible auto-boxing) |
| 62 | `task`  |  | Crate-internal | Other / internal logic |  |
| 63 | `get_span`  |  | Private helper | Accessor / query |  |
| 89 | `blocking_task`  |  | Crate-internal | Blocking (sync) variant |  |
| 114 | `async_op`  |  | Crate-internal | Other / internal logic |  |
| 156 | `poll`  | `Future for InstrumentedAsyncOp<F>` | Trait impl | Future impl (poll) |  |
| 169 | `task`  |  | Crate-internal | Other / internal logic |  |
| 175 | `blocking_task`  |  | Crate-internal | Blocking (sync) variant |  |
| 185 | `caller_location`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/util/try_lock.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 35 | `new` 🅲 | `TryLock<T>` | Crate-internal | Constructor | Create a new `TryLock` |
| 41 | `new`  | `TryLock<T>` | Crate-internal | Constructor | Create a new `TryLock` |
| 46 | `try_lock`  | `TryLock<T>` | Crate-internal | Non-blocking attempt | Attempt to acquire lock |
| 65 | `deref`  | `Deref for LockGuard<'_, T>` | Trait impl | Deref |  |
| 71 | `deref_mut`  | `DerefMut for LockGuard<'_, T>` | Trait impl | Deref |  |
| 77 | `drop`  | `Drop for LockGuard<'_, T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/util/typeid.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `try_transmute` ⚠ |  | Crate-internal | Non-blocking attempt |  |
| 21 | `nonstatic_typeid`  |  | Private helper | Other / internal logic |  |
| 26 | `get_type_id`  | `trait NonStaticAny` | Trait method (declaration/default) | Accessor / query |  |
| 33 | `get_type_id`  | `NonStaticAny for PhantomData<T>` | Trait impl | Accessor / query |  |

## `tokio/src/util/wake.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `wake`  | `trait Wake` | Trait method (declaration/default) | Wake / park | Wake by value. |
| 14 | `wake_by_ref`  | `trait Wake` | Trait method (declaration/default) | Wake / park | Wake by reference. |
| 27 | `deref`  | `Deref for WakerRef<'_>` | Trait impl | Deref |  |
| 33 | `waker_ref`  |  | Crate-internal | Wake / park | Creates a reference to a `Waker` from a reference to `Arc<impl Wake>`. |
| 44 | `waker_vtable`  |  | Private helper | Wake / park |  |
| 53 | `clone_arc_raw` ⚠ |  | Private helper | Other / internal logic |  |
| 61 | `wake_arc_raw` ⚠ |  | Private helper | Wake / park |  |
| 68 | `wake_by_ref_arc_raw` ⚠ |  | Private helper | Wake / park |  |
| 75 | `drop_arc_raw` ⚠ |  | Private helper | Lifecycle / ref-count |  |

## `tokio/src/util/wake_list.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 18 | `new`  | `WakeList` | Crate-internal | Constructor |  |
| 28 | `can_push`  | `WakeList` | Crate-internal | Other / internal logic |  |
| 32 | `push`  | `WakeList` | Crate-internal | Data movement |  |
| 39 | `wake_all`  | `WakeList` | Crate-internal | Wake / park |  |
| 46 | `drop`  | `Drop for DropGuard` | Trait impl | Drop / cleanup |  |
| 77 | `drop`  | `Drop for WakeList` | Trait impl | Drop / cleanup |  |

