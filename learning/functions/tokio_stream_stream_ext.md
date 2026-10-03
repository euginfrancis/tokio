# `tokio-stream::stream_ext` — 173 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 100 |
| Public API | 43 |
| Crate-internal | 24 |
| Trait method (declaration/default) | 3 |
| Private helper | 3 |

## `tokio-stream/src/stream_ext/all.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `new`  | `AllFuture<'a, St, F>` | Crate-internal | Constructor |  |
| 39 | `poll`  | `Future for AllFuture<'_, St, F>` | Trait impl | Future impl (poll) |  |

## `tokio-stream/src/stream_ext/any.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `new`  | `AnyFuture<'a, St, F>` | Crate-internal | Constructor |  |
| 39 | `poll`  | `Future for AnyFuture<'_, St, F>` | Trait impl | Future impl (poll) |  |

## `tokio-stream/src/stream_ext/chain.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 20 | `new`  | `Chain<T, U>` | Crate-internal | Constructor |  |
| 36 | `poll_next`  | `Stream for Chain<T, U>` | Trait impl | Stream impl |  |
| 48 | `size_hint`  | `Stream for Chain<T, U>` | Trait impl | Stream impl |  |
| 58 | `is_terminated`  | `FusedStream for Chain<T, U>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/chunks_timeout.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `new`  | `ChunksTimeout<S>` | Crate-internal | Constructor |  |
| 38 | `into_remainder`  | `ChunksTimeout<S>` | Public API | Conversion | Consumes the [`ChunksTimeout`] and then returns all buffered items. |
| 47 | `poll_next`  | `Stream for ChunksTimeout<S>` | Trait impl | Stream impl |  |
| 85 | `size_hint`  | `Stream for ChunksTimeout<S>` | Trait impl | Stream impl |  |

## `tokio-stream/src/stream_ext/collect.rs` (41)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 46 | `new`  | `Collect<T, U, U::InternalCollection>` | Crate-internal | Constructor |  |
| 66 | `poll`  | `Future for Collect<T, U, U::InternalCollection>` | Trait impl | Future impl (poll) |  |
| 93 | `initialize`  | `sealed::FromStreamPriv<()> for ()` | Trait impl | Runtime/task control |  |
| 95 | `extend`  | `sealed::FromStreamPriv<()> for ()` | Trait impl | Combinator / iteration |  |
| 99 | `finalize`  | `sealed::FromStreamPriv<()> for ()` | Trait impl | Runtime/task control |  |
| 107 | `initialize`  | `sealed::FromStreamPriv<T> for String` | Trait impl | Runtime/task control |  |
| 111 | `extend`  | `sealed::FromStreamPriv<T> for String` | Trait impl | Combinator / iteration |  |
| 116 | `finalize`  | `sealed::FromStreamPriv<T> for String` | Trait impl | Runtime/task control |  |
| 126 | `initialize`  | `sealed::FromStreamPriv<T> for Vec<T>` | Trait impl | Runtime/task control |  |
| 130 | `extend`  | `sealed::FromStreamPriv<T> for Vec<T>` | Trait impl | Combinator / iteration |  |
| 135 | `finalize`  | `sealed::FromStreamPriv<T> for Vec<T>` | Trait impl | Runtime/task control |  |
| 145 | `initialize`  | `sealed::FromStreamPriv<T> for VecDeque<T>` | Trait impl | Runtime/task control |  |
| 149 | `extend`  | `sealed::FromStreamPriv<T> for VecDeque<T>` | Trait impl | Combinator / iteration |  |
| 154 | `finalize`  | `sealed::FromStreamPriv<T> for VecDeque<T>` | Trait impl | Runtime/task control |  |
| 164 | `initialize`  | `sealed::FromStreamPriv<T> for LinkedList<T>` | Trait impl | Runtime/task control |  |
| 168 | `extend`  | `sealed::FromStreamPriv<T> for LinkedList<T>` | Trait impl | Combinator / iteration |  |
| 173 | `finalize`  | `sealed::FromStreamPriv<T> for LinkedList<T>` | Trait impl | Runtime/task control |  |
| 183 | `initialize`  | `sealed::FromStreamPriv<T> for BTreeSet<T>` | Trait impl | Runtime/task control |  |
| 187 | `extend`  | `sealed::FromStreamPriv<T> for BTreeSet<T>` | Trait impl | Combinator / iteration |  |
| 192 | `finalize`  | `sealed::FromStreamPriv<T> for BTreeSet<T>` | Trait impl | Runtime/task control |  |
| 202 | `initialize`  | `sealed::FromStreamPriv<(K, V)> for BTreeMap<K, V>` | Trait impl | Runtime/task control |  |
| 206 | `extend`  | `sealed::FromStreamPriv<(K, V)> for BTreeMap<K, V>` | Trait impl | Combinator / iteration |  |
| 211 | `finalize`  | `sealed::FromStreamPriv<(K, V)> for BTreeMap<K, V>` | Trait impl | Runtime/task control |  |
| 221 | `initialize`  | `sealed::FromStreamPriv<T> for HashSet<T>` | Trait impl | Runtime/task control |  |
| 225 | `extend`  | `sealed::FromStreamPriv<T> for HashSet<T>` | Trait impl | Combinator / iteration |  |
| 230 | `finalize`  | `sealed::FromStreamPriv<T> for HashSet<T>` | Trait impl | Runtime/task control |  |
| 240 | `initialize`  | `sealed::FromStreamPriv<(K, V)> for HashMap<K, V>` | Trait impl | Runtime/task control |  |
| 244 | `extend`  | `sealed::FromStreamPriv<(K, V)> for HashMap<K, V>` | Trait impl | Combinator / iteration |  |
| 249 | `finalize`  | `sealed::FromStreamPriv<(K, V)> for HashMap<K, V>` | Trait impl | Runtime/task control |  |
| 259 | `initialize`  | `sealed::FromStreamPriv<T> for BinaryHeap<T>` | Trait impl | Runtime/task control |  |
| 263 | `extend`  | `sealed::FromStreamPriv<T> for BinaryHeap<T>` | Trait impl | Combinator / iteration |  |
| 268 | `finalize`  | `sealed::FromStreamPriv<T> for BinaryHeap<T>` | Trait impl | Runtime/task control |  |
| 278 | `initialize`  | `sealed::FromStreamPriv<T> for Box<[T]>` | Trait impl | Runtime/task control |  |
| 282 | `extend`  | `sealed::FromStreamPriv<T> for Box<[T]>` | Trait impl | Combinator / iteration |  |
| 286 | `finalize`  | `sealed::FromStreamPriv<T> for Box<[T]>` | Trait impl | Runtime/task control |  |
| 300 | `initialize`  | `sealed::FromStreamPriv<Result<T, E>> for Result<U, E>` | Trait impl | Runtime/task control |  |
| 308 | `extend`  | `sealed::FromStreamPriv<Result<T, E>> for Result<U, E>` | Trait impl | Combinator / iteration |  |
| 326 | `finalize`  | `sealed::FromStreamPriv<Result<T, E>> for Result<U, E>` | Trait impl | Runtime/task control |  |
| 346 | `initialize`  | `trait FromStreamPriv` | Trait method (declaration/default) | Runtime/task control | Initialize the collection |
| 355 | `extend`  | `trait FromStreamPriv` | Trait method (declaration/default) | Combinator / iteration | Extend the collection with the received item Return `true` to continue streaming, `false` complete collection. |
| 358 | `finalize`  | `trait FromStreamPriv` | Trait method (declaration/default) | Runtime/task control | Finalize collection into target type. |

## `tokio-stream/src/stream_ext/filter.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `fmt`  | `fmt::Debug for Filter<St, F>` | Trait impl | Formatting |  |
| 31 | `new`  | `Filter<St, F>` | Crate-internal | Constructor |  |
| 36 | `get_ref`  | `Filter<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 43 | `get_mut`  | `Filter<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 50 | `get_pin_mut`  | `Filter<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 57 | `into_inner`  | `Filter<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 69 | `poll_next`  | `Stream for Filter<St, F>` | Trait impl | Stream impl |  |
| 82 | `size_hint`  | `Stream for Filter<St, F>` | Trait impl | Stream impl |  |
| 92 | `is_terminated`  | `FusedStream for Filter<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/filter_map.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `fmt`  | `fmt::Debug for FilterMap<St, F>` | Trait impl | Formatting |  |
| 31 | `new`  | `FilterMap<St, F>` | Crate-internal | Constructor |  |
| 36 | `get_ref`  | `FilterMap<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 43 | `get_mut`  | `FilterMap<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 50 | `get_pin_mut`  | `FilterMap<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 57 | `into_inner`  | `FilterMap<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 69 | `poll_next`  | `Stream for FilterMap<St, F>` | Trait impl | Stream impl |  |
| 82 | `size_hint`  | `Stream for FilterMap<St, F>` | Trait impl | Stream impl |  |
| 92 | `is_terminated`  | `FusedStream for FilterMap<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/fold.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `new`  | `FoldFuture<St, B, F>` | Crate-internal | Constructor |  |
| 42 | `poll`  | `Future for FoldFuture<St, B, F>` | Trait impl | Future impl (poll) |  |

## `tokio-stream/src/stream_ext/fuse.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `new`  | `Fuse<T>` | Crate-internal | Constructor |  |
| 34 | `poll_next`  | `Stream for Fuse<T>` | Trait impl | Stream impl |  |
| 48 | `size_hint`  | `Stream for Fuse<T>` | Trait impl | Stream impl |  |
| 60 | `is_terminated`  | `FusedStream for Fuse<T>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/map.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `fmt`  | `fmt::Debug for Map<St, F>` | Trait impl | Formatting |  |
| 29 | `new`  | `Map<St, F>` | Crate-internal | Constructor |  |
| 34 | `get_ref`  | `Map<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 41 | `get_mut`  | `Map<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 48 | `get_pin_mut`  | `Map<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 55 | `into_inner`  | `Map<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 67 | `poll_next`  | `Stream for Map<St, F>` | Trait impl | Stream impl |  |
| 75 | `size_hint`  | `Stream for Map<St, F>` | Trait impl | Stream impl |  |
| 85 | `is_terminated`  | `FusedStream for Map<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/map_while.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `fmt`  | `fmt::Debug for MapWhile<St, F>` | Trait impl | Formatting |  |
| 33 | `new`  | `MapWhile<St, F>` | Crate-internal | Constructor |  |
| 42 | `get_ref`  | `MapWhile<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 49 | `get_mut`  | `MapWhile<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 56 | `get_pin_mut`  | `MapWhile<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 63 | `into_inner`  | `MapWhile<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 75 | `poll_next`  | `Stream for MapWhile<St, F>` | Trait impl | Stream impl |  |
| 92 | `size_hint`  | `Stream for MapWhile<St, F>` | Trait impl | Stream impl |  |
| 106 | `is_terminated`  | `FusedStream for MapWhile<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/merge.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `new`  | `Merge<T, U>` | Crate-internal | Constructor |  |
| 42 | `poll_next`  | `Stream for Merge<T, U>` | Trait impl | Stream impl |  |
| 56 | `size_hint`  | `Stream for Merge<T, U>` | Trait impl | Stream impl |  |
| 66 | `is_terminated`  | `FusedStream for Merge<T, U>` | Trait impl | Accessor / query |  |
| 71 | `poll_next`  |  | Private helper | Poll function |  |

## `tokio-stream/src/stream_ext/next.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 29 | `new`  | `Next<'a, St>` | Crate-internal | Constructor |  |
| 40 | `poll`  | `Future for Next<'_, St>` | Trait impl | Future impl (poll) |  |

## `tokio-stream/src/stream_ext/peekable.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 20 | `new`  | `Peekable<T>` | Crate-internal | Constructor |  |
| 26 | `peek` 🅰 | `Peekable<T>` | Public API | Combinator / iteration | Peek at the next item in the stream. |
| 39 | `peek_mut` 🅰 | `Peekable<T>` | Public API | Combinator / iteration | Peek at the next item in the stream as a mutable reference. |
| 52 | `poll_peek`  | `Peekable<T>` | Public API | Poll function | Poll to peek at the next item in the stream as a mutable reference. |
| 69 | `poll_next`  | `Stream for Peekable<T>` | Trait impl | Stream impl |  |
| 78 | `size_hint`  | `Stream for Peekable<T>` | Trait impl | Stream impl |  |

## `tokio-stream/src/stream_ext/skip.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `fmt`  | `fmt::Debug for Skip<St>` | Trait impl | Formatting |  |
| 31 | `new`  | `Skip<St>` | Crate-internal | Constructor |  |
| 36 | `get_ref`  | `Skip<St>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 43 | `get_mut`  | `Skip<St>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 50 | `get_pin_mut`  | `Skip<St>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 57 | `into_inner`  | `Skip<St>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 68 | `poll_next`  | `Stream for Skip<St>` | Trait impl | Stream impl |  |
| 82 | `size_hint`  | `Stream for Skip<St>` | Trait impl | Stream impl |  |
| 96 | `is_terminated`  | `FusedStream for Skip<St>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/skip_while.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `fmt`  | `fmt::Debug for SkipWhile<St, F>` | Trait impl | Formatting |  |
| 31 | `new`  | `SkipWhile<St, F>` | Crate-internal | Constructor |  |
| 39 | `get_ref`  | `SkipWhile<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 46 | `get_mut`  | `SkipWhile<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 53 | `get_pin_mut`  | `SkipWhile<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 60 | `into_inner`  | `SkipWhile<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 72 | `poll_next`  | `Stream for SkipWhile<St, F>` | Trait impl | Stream impl |  |
| 91 | `size_hint`  | `Stream for SkipWhile<St, F>` | Trait impl | Stream impl |  |
| 107 | `is_terminated`  | `FusedStream for SkipWhile<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/take.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `fmt`  | `fmt::Debug for Take<St>` | Trait impl | Formatting |  |
| 32 | `new`  | `Take<St>` | Crate-internal | Constructor |  |
| 37 | `get_ref`  | `Take<St>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 44 | `get_mut`  | `Take<St>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 51 | `get_pin_mut`  | `Take<St>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 58 | `into_inner`  | `Take<St>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 69 | `poll_next`  | `Stream for Take<St>` | Trait impl | Stream impl |  |
| 87 | `size_hint`  | `Stream for Take<St>` | Trait impl | Stream impl |  |
| 109 | `is_terminated`  | `FusedStream for Take<St>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/take_while.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `fmt`  | `fmt::Debug for TakeWhile<St, F>` | Trait impl | Formatting |  |
| 33 | `new`  | `TakeWhile<St, F>` | Crate-internal | Constructor |  |
| 42 | `get_ref`  | `TakeWhile<St, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 49 | `get_mut`  | `TakeWhile<St, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 56 | `get_pin_mut`  | `TakeWhile<St, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 63 | `into_inner`  | `TakeWhile<St, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 75 | `poll_next`  | `Stream for TakeWhile<St, F>` | Trait impl | Stream impl |  |
| 91 | `size_hint`  | `Stream for TakeWhile<St, F>` | Trait impl | Stream impl |  |
| 107 | `is_terminated`  | `FusedStream for TakeWhile<St, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/then.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `fmt`  | `fmt::Debug for Then<St, Fut, F>` | Trait impl | Formatting |  |
| 34 | `new`  | `Then<St, Fut, F>` | Crate-internal | Constructor |  |
| 43 | `get_ref`  | `Then<St, Fut, F>` | Public API | Accessor / query | Returns a reference to the inner stream. |
| 50 | `get_mut`  | `Then<St, Fut, F>` | Public API | Accessor / query | Returns a mutable reference to the inner stream. |
| 57 | `get_pin_mut`  | `Then<St, Fut, F>` | Public API | Accessor / query | Returns a pinned mutable reference to the inner stream. |
| 64 | `into_inner`  | `Then<St, Fut, F>` | Public API | Conversion | Consumes this combinator and returns the inner stream. |
| 77 | `poll_next`  | `Stream for Then<St, Fut, F>` | Trait impl | Stream impl |  |
| 101 | `size_hint`  | `Stream for Then<St, Fut, F>` | Trait impl | Stream impl |  |
| 118 | `is_terminated`  | `FusedStream for Then<St, Fut, F>` | Trait impl | Accessor / query |  |

## `tokio-stream/src/stream_ext/throttle.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `throttle`  |  | Crate-internal | Other / internal logic |  |
| 47 | `get_ref`  | `Throttle<T>` | Public API | Accessor / query | Acquires a reference to the underlying stream that this combinator is pulling from. |
| 56 | `get_mut`  | `Throttle<T>` | Public API | Accessor / query | Acquires a mutable reference to the underlying stream that this combinator is pulling from. |
| 64 | `into_inner`  | `Throttle<T>` | Public API | Conversion | Consumes this combinator, returning the underlying stream. |
| 72 | `poll_next`  | `Stream for Throttle<T>` | Trait impl | Stream impl |  |
| 96 | `size_hint`  | `Stream for Throttle<T>` | Trait impl | Stream impl |  |
| 102 | `is_terminated`  | `FusedStream for Throttle<T>` | Trait impl | Accessor / query |  |
| 107 | `is_zero`  |  | Private helper | Accessor / query |  |

## `tokio-stream/src/stream_ext/timeout.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 31 | `new`  | `Timeout<S>` | Crate-internal | Constructor |  |
| 46 | `poll_next`  | `Stream for Timeout<S>` | Trait impl | Stream impl |  |
| 69 | `size_hint`  | `Stream for Timeout<S>` | Trait impl | Stream impl |  |
| 77 | `twice_plus_one`  |  | Private helper | Other / internal logic |  |
| 88 | `new`  | `Elapsed` | Crate-internal | Constructor |  |
| 94 | `fmt`  | `fmt::Display for Elapsed` | Trait impl | Formatting |  |
| 102 | `from`  | `From<Elapsed> for std::io::Error` | Trait impl | Conversion |  |

## `tokio-stream/src/stream_ext/timeout_repeating.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `new`  | `TimeoutRepeating<S>` | Crate-internal | Constructor |  |
| 33 | `poll_next`  | `Stream for TimeoutRepeating<S>` | Trait impl | Stream impl |  |
| 50 | `size_hint`  | `Stream for TimeoutRepeating<S>` | Trait impl | Stream impl |  |

## `tokio-stream/src/stream_ext/try_next.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `new`  | `TryNext<'a, St>` | Crate-internal | Constructor |  |
| 41 | `poll`  | `Future for TryNext<'_, St>` | Trait impl | Future impl (poll) |  |

