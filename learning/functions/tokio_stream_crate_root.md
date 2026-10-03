# `tokio-stream (crate root)` — 71 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait method (declaration/default) | 23 |
| Public API | 22 |
| Trait impl | 18 |
| Crate-internal | 5 |
| Private helper | 3 |

## `tokio-stream/src/empty.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `empty` 🅲 |  | Public API | Other / internal logic | Creates a stream that yields nothing. |
| 44 | `poll_next`  | `Stream for Empty<T>` | Trait impl | Stream impl |  |
| 56 | `size_hint`  | `Stream for Empty<T>` | Trait impl | Stream impl |  |
| 62 | `is_terminated`  | `FusedStream for Empty<T>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/iter.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `iter`  |  | Public API | Combinator / iteration | Converts an `Iterator` into a `Stream`. |
| 51 | `poll_next`  | `Stream for Iter<I>` | Trait impl | Stream impl |  |
| 82 | `size_hint`  | `Stream for Iter<I>` | Trait impl | Stream impl |  |

## `tokio-stream/src/once.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `once`  |  | Public API | Other / internal logic | Creates a stream that emits an element exactly once. |
| 44 | `poll_next`  | `Stream for Once<T>` | Trait impl | Stream impl |  |
| 57 | `size_hint`  | `Stream for Once<T>` | Trait impl | Stream impl |  |
| 67 | `is_terminated`  | `FusedStream for Once<T>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/pending.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 40 | `pending` 🅲 |  | Public API | Other / internal logic | Creates a stream that is never ready The returned stream is never ready. |
| 47 | `poll_next`  | `Stream for Pending<T>` | Trait impl | Stream impl |  |
| 51 | `size_hint`  | `Stream for Pending<T>` | Trait impl | Stream impl |  |

## `tokio-stream/src/stream_close.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 45 | `new`  | `StreamNotifyClose<S>` | Public API | Constructor | Create a new `StreamNotifyClose`. |
| 54 | `into_inner`  | `StreamNotifyClose<S>` | Public API | Conversion | Get back the inner `Stream`. |
| 65 | `poll_next`  | `Stream for StreamNotifyClose<S>` | Trait impl | Stream impl |  |
| 85 | `size_hint`  | `Stream for StreamNotifyClose<S>` | Trait impl | Stream impl |  |
| 100 | `is_terminated`  | `FusedStream for StreamNotifyClose<S>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext.rs` (24)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 144 | `next`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Consumes and returns the next value in the stream or `None` if the stream is finished. |
| 186 | `try_next`  | `trait StreamExt` | Trait method (declaration/default) | Non-blocking attempt | Consumes and returns the next item in the stream. |
| 219 | `map`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Maps this stream's items to a different type, returning a new stream of the resulting type. |
| 261 | `map_while`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Map this stream's items to a different type for as long as determined by the provided closure. |
| 305 | `then`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Maps this stream's items asynchronously to a different type, returning a new stream of the resulting type. |
| 398 | `merge`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Combine two streams into one by interleaving the output of both as it is produced. |
| 436 | `filter`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Filters the values produced by this stream according to the provided predicate. |
| 474 | `filter_map`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Filters the values produced by this stream while simultaneously mapping them to a different type according to the provided closure. |
| 543 | `fuse`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Creates a stream which ends after the first `None`. |
| 570 | `take`  | `trait StreamExt` | Trait method (declaration/default) | Data movement | Creates a new stream of at most `n` items of the underlying stream. |
| 599 | `take_while`  | `trait StreamExt` | Trait method (declaration/default) | Data movement | Take elements from this stream while the provided predicate resolves to `true`. |
| 625 | `skip`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Creates a new stream that will skip the `n` first items of the underlying stream. |
| 655 | `skip_while`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Skip elements from the underlying stream while the provided predicate resolves to `true`. |
| 716 | `all`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Tests if every element of the stream matches a predicate. |
| 775 | `any`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Tests if any element of the stream matches a predicate. |
| 810 | `chain`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Combine two streams into one by first returning all values from the first stream then all values from the second stream. |
| 840 | `fold`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | A combinator that applies a function to every element in a stream producing a single, final value. |
| 919 | `collect`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Drain stream pushing all emitted values into a collection. |
| 1005 | `timeout`  | `trait StreamExt` | Trait method (declaration/default) | Time / timers | Applies a per-item timeout to the passed stream. |
| 1093 | `timeout_repeating`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Applies a per-item timeout to the passed stream. |
| 1123 | `throttle`  | `trait StreamExt` | Trait method (declaration/default) | Other / internal logic | Slows down a stream by enforcing a delay between items. |
| 1179 | `chunks_timeout`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Batches the items in the given stream using a maximum duration and size for each batch. |
| 1205 | `peekable`  | `trait StreamExt` | Trait method (declaration/default) | Combinator / iteration | Turns the stream into a peekable stream, whose next element can be peeked at without being consumed. |
| 1216 | `merge_size_hints`  |  | Private helper | Other / internal logic | Merge the size hints from two streams. |

## `tokio-stream/src/stream_map.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 230 | `iter`  | `StreamMap<K, V>` | Public API | Combinator / iteration | An iterator visiting all key-value pairs in arbitrary order. |
| 253 | `iter_mut`  | `StreamMap<K, V>` | Public API | Combinator / iteration | An iterator visiting all key-value pairs mutably in arbitrary order. |
| 269 | `new`  | `StreamMap<K, V>` | Public API | Constructor | Creates an empty `StreamMap`. |
| 285 | `with_capacity`  | `StreamMap<K, V>` | Public API | Constructor | Creates an empty `StreamMap` with the specified capacity. |
| 310 | `keys`  | `StreamMap<K, V>` | Public API | Other / internal logic | Returns an iterator visiting all keys in arbitrary order. |
| 333 | `values`  | `StreamMap<K, V>` | Public API | Other / internal logic | An iterator visiting all values in arbitrary order. |
| 356 | `values_mut`  | `StreamMap<K, V>` | Public API | Other / internal logic | An iterator visiting all values mutably in arbitrary order. |
| 373 | `capacity`  | `StreamMap<K, V>` | Public API | Accessor / query | Returns the number of streams the map can hold without reallocating. |
| 389 | `len`  | `StreamMap<K, V>` | Public API | Accessor / query | Returns the number of streams in the map. |
| 405 | `is_empty`  | `StreamMap<K, V>` | Public API | Accessor / query | Returns `true` if the map contains no elements. |
| 422 | `clear`  | `StreamMap<K, V>` | Public API | Configuration / setter | Clears the map, removing all key-stream pairs. |
| 446 | `insert`  | `StreamMap<K, V>` | Public API | Data movement | Insert a key-stream pair into the map. |
| 471 | `remove`  | `StreamMap<K, V>` | Public API | Data movement | Removes a key from the map, returning the stream at the key if the key was previously in the map. |
| 500 | `contains_key`  | `StreamMap<K, V>` | Public API | Other / internal logic | Returns `true` if the map contains a stream for the specified key. |
| 515 | `poll_next_entry`  | `StreamMap<K, V>` | Private helper | Poll function | Polls the next value, includes the vec entry index |
| 554 | `default`  | `Default for StreamMap<K, V>` | Trait impl | Constructor |  |
| 581 | `next_many` 🅰 | `StreamMap<K, V>` | Public API | Async operation | Receives multiple items on this [`StreamMap`], extending the provided `buffer`. |
| 597 | `poll_next_many`  | `StreamMap<K, V>` | Public API | Poll function | Polls to receive multiple items on this `StreamMap`, extending the provided `buffer`. |
| 676 | `poll_next`  | `Stream for StreamMap<K, V>` | Trait impl | Stream impl |  |
| 685 | `size_hint`  | `Stream for StreamMap<K, V>` | Trait impl | Stream impl |  |
| 708 | `from_iter`  | `FromIterator<(K, V)> for StreamMap<K, V>` | Trait impl | Conversion |  |
| 722 | `extend`  | `Extend<(K, V)> for StreamMap<K, V>` | Trait impl | Combinator / iteration |  |
| 743 | `seed`  |  | Crate-internal | Configuration / setter |  |
| 751 | `seed`  |  | Crate-internal | Configuration / setter |  |
| 772 | `new`  | `FastRand` | Crate-internal | Constructor | Initialize a new, thread-local, fast random number generator. |
| 787 | `fastrand_n`  | `FastRand` | Crate-internal | Other / internal logic |  |
| 794 | `fastrand`  | `FastRand` | Private helper | Other / internal logic |  |
| 809 | `thread_rng_n`  |  | Crate-internal | Configuration / setter |  |

