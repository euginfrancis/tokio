# `tokio-test (crate root)` — 66 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 26 |
| Private helper | 24 |
| Trait impl | 16 |

## `tokio-test/src/io.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 80 | `new`  | `Builder` | Public API | Constructor | Return a new, empty `Builder`. |
| 88 | `read`  | `Builder` | Public API | I/O operation | Sequence a `read` operation. |
| 97 | `read_error`  | `Builder` | Public API | I/O operation | Sequence a `read` operation that produces an error. |
| 107 | `write`  | `Builder` | Public API | I/O operation | Sequence a `write` operation. |
| 116 | `write_error`  | `Builder` | Public API | I/O operation | Sequence a `write` operation that produces an error. |
| 126 | `wait`  | `Builder` | Public API | Runtime/task control | Sequence a wait. |
| 133 | `name`  | `Builder` | Public API | Other / internal logic | Set name of the mock IO object to include in panic messages and debug output |
| 139 | `build`  | `Builder` | Public API | Constructor | Build a `Mock` value according to the defined script. |
| 145 | `build_with_handle`  | `Builder` | Public API | Constructor | Build a `Mock` value paired with a handle |
| 159 | `read`  | `Handle` | Public API | I/O operation | Sequence a `read` operation. |
| 168 | `read_error`  | `Handle` | Public API | I/O operation | Sequence a `read` operation error. |
| 178 | `write`  | `Handle` | Public API | I/O operation | Sequence a `write` operation. |
| 187 | `write_error`  | `Handle` | Public API | I/O operation | Sequence a `write` operation error. |
| 195 | `new`  | `Inner` | Private helper | Constructor |  |
| 214 | `poll_action`  | `Inner` | Private helper | Poll function |  |
| 218 | `read`  | `Inner` | Private helper | I/O operation |  |
| 246 | `write`  | `Inner` | Private helper | I/O operation |  |
| 292 | `remaining_wait`  | `Inner` | Private helper | Other / internal logic |  |
| 299 | `action`  | `Inner` | Private helper | Other / internal logic |  |
| 347 | `maybe_wakeup_reader`  | `Mock` | Private helper | Other / internal logic |  |
| 360 | `poll_read`  | `AsyncRead for Mock` | Trait impl | I/O trait impl |  |
| 408 | `poll_write`  | `AsyncWrite for Mock` | Trait impl | I/O trait impl |  |
| 492 | `poll_flush`  | `AsyncWrite for Mock` | Trait impl | I/O trait impl |  |
| 496 | `poll_shutdown`  | `AsyncWrite for Mock` | Trait impl | I/O trait impl |  |
| 503 | `drop`  | `Drop for Mock` | Trait impl | Drop / cleanup |  |
| 547 | `fmt`  | `fmt::Debug for Inner` | Trait impl | Formatting |  |
| 559 | `fmt`  | `fmt::Display for PanicMsgSnippet<'a>` | Trait impl | Formatting |  |
| 574 | `pmsg`  | `Mock` | Private helper | Other / internal logic |  |

## `tokio-test/src/lib.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `block_on`  |  | Public API | Runtime/task control | Runs the provided future, blocking the current thread until the future completes. |

## `tokio-test/src/stream_mock.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 60 | `new`  | `StreamMockBuilder<T>` | Public API | Constructor | Create a new empty [`StreamMockBuilder`] |
| 65 | `next`  | `StreamMockBuilder<T>` | Public API | Combinator / iteration | Queue an item to be returned by the stream |
| 79 | `wait`  | `StreamMockBuilder<T>` | Public API | Runtime/task control | Queue the stream to wait for a duration |
| 85 | `build`  | `StreamMockBuilder<T>` | Public API | Constructor | Build the [`StreamMock`] |
| 94 | `default`  | `Default for StreamMockBuilder<T>` | Trait impl | Constructor |  |
| 111 | `next_action`  | `StreamMock<T>` | Private helper | Other / internal logic |  |
| 119 | `poll_next`  | `Stream for StreamMock<T>` | Trait impl | Stream impl |  |
| 147 | `drop`  | `Drop for StreamMock<T>` | Trait impl | Drop / cleanup |  |

## `tokio-test/src/task.rs` (29)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 42 | `spawn`  |  | Public API | Runtime/task control | Spawn a future into a [`Spawn`] which wraps the future in a mocked executor. |
| 78 | `into_inner`  | `Spawn<T>` | Public API | Conversion | Consumes `self` returning the inner value |
| 87 | `is_woken`  | `Spawn<T>` | Public API | Accessor / query | Returns `true` if the inner future has received a wake notification since the last call to `enter`. |
| 94 | `waker_ref_count`  | `Spawn<T>` | Public API | Wake / park | Returns the number of references to the task waker The task itself holds a reference. |
| 99 | `enter`  | `Spawn<T>` | Public API | Runtime/task control | Enter the task context |
| 111 | `deref`  | `ops::Deref for Spawn<T>` | Trait impl | Deref |  |
| 117 | `deref_mut`  | `ops::DerefMut for Spawn<T>` | Trait impl | Deref |  |
| 125 | `poll`  | `Spawn<T>` | Public API | Poll function | If `T` is a [`Future`] then poll it. |
| 155 | `poll_until_idle`  | `Spawn<T>` | Public API | Poll function | Polls the future until it is idle. |
| 171 | `poll_next`  | `Spawn<T>` | Public API | Poll function | If `T` is a [`Stream`] then `poll_next` it. |
| 180 | `poll`  | `Future for Spawn<T>` | Trait impl | Future impl (poll) |  |
| 188 | `poll_next`  | `Stream for Spawn<T>` | Trait impl | Stream impl |  |
| 192 | `size_hint`  | `Stream for Spawn<T>` | Trait impl | Stream impl |  |
| 199 | `new`  | `MockTask` | Private helper | Constructor | Creates new mock task |
| 209 | `enter`  | `MockTask` | Private helper | Runtime/task control | Runs a closure from the context of the task. |
| 222 | `is_woken`  | `MockTask` | Private helper | Accessor / query | Returns `true` if the inner future has received a wake notification since the last call to `enter`. |
| 229 | `waker_ref_count`  | `MockTask` | Private helper | Wake / park | Returns the number of references to the task waker The task itself holds a reference. |
| 233 | `waker`  | `MockTask` | Private helper | Wake / park |  |
| 242 | `default`  | `Default for MockTask` | Trait impl | Constructor |  |
| 248 | `new`  | `ThreadWaker` | Private helper | Constructor |  |
| 258 | `clear`  | `ThreadWaker` | Private helper | Configuration / setter | Clears any previously received wakes, avoiding potential spurious wake notifications. |
| 262 | `is_woken`  | `ThreadWaker` | Private helper | Accessor / query |  |
| 270 | `wake`  | `ThreadWaker` | Private helper | Wake / park |  |
| 293 | `to_raw` ⚠ |  | Private helper | Conversion |  |
| 297 | `from_raw` ⚠ |  | Private helper | Conversion |  |
| 301 | `clone` ⚠ |  | Private helper | Other / internal logic |  |
| 310 | `wake` ⚠ |  | Private helper | Wake / park |  |
| 315 | `wake_by_ref` ⚠ |  | Private helper | Wake / park |  |
| 323 | `drop_waker` ⚠ |  | Private helper | Lifecycle / ref-count |  |

