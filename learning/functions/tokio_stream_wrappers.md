# `tokio-stream::wrappers` — 86 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 53 |
| Public API | 31 |
| Private helper | 2 |

## `tokio-stream/src/wrappers/broadcast.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 54 | `fmt`  | `fmt::Display for BroadcastStreamRecvError` | Trait impl | Formatting |  |
| 63 | `make_future` 🅰 |  | Private helper | Async operation |  |
| 70 | `new`  | `BroadcastStream<T>` | Public API | Constructor | Create a new `BroadcastStream`. |
| 79 | `poll_next`  | `Stream for BroadcastStream<T>` | Trait impl | Stream impl |  |
| 93 | `fmt`  | `fmt::Debug for BroadcastStream<T>` | Trait impl | Formatting |  |
| 99 | `from`  | `From<Receiver<T>> for BroadcastStream<T>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/interval.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 39 | `new`  | `IntervalStream` | Public API | Constructor | Create a new `IntervalStream`. |
| 44 | `into_inner`  | `IntervalStream` | Public API | Conversion | Get back the inner `Interval`. |
| 52 | `poll_next`  | `Stream for IntervalStream` | Trait impl | Stream impl |  |
| 56 | `size_hint`  | `Stream for IntervalStream` | Trait impl | Stream impl |  |
| 62 | `is_terminated`  | `FusedStream for IntervalStream` | Trait impl | Accessor / query |  |
| 68 | `as_ref`  | `AsRef<Interval> for IntervalStream` | Trait impl | Conversion |  |
| 74 | `as_mut`  | `AsMut<Interval> for IntervalStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/lines.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `LinesStream<R>` | Public API | Constructor | Create a new `LinesStream`. |
| 46 | `into_inner`  | `LinesStream<R>` | Public API | Conversion | Get back the inner `Lines`. |
| 51 | `as_pin_mut`  | `LinesStream<R>` | Public API | Conversion | Obtain a pinned reference to the inner `Lines<R>`. |
| 59 | `poll_next`  | `Stream for LinesStream<R>` | Trait impl | Stream impl |  |
| 68 | `as_ref`  | `AsRef<Lines<R>> for LinesStream<R>` | Trait impl | Conversion |  |
| 74 | `as_mut`  | `AsMut<Lines<R>> for LinesStream<R>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/mpsc_bounded.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `ReceiverStream<T>` | Public API | Constructor | Create a new `ReceiverStream`. |
| 46 | `into_inner`  | `ReceiverStream<T>` | Public API | Conversion | Get back the inner `Receiver`. |
| 60 | `close`  | `ReceiverStream<T>` | Public API | Data movement | Closes the receiving half of a channel without dropping it. |
| 68 | `poll_next`  | `Stream for ReceiverStream<T>` | Trait impl | Stream impl |  |
| 82 | `size_hint`  | `Stream for ReceiverStream<T>` | Trait impl | Stream impl | Returns the bounds of the stream based on the underlying receiver. |
| 93 | `is_terminated`  | `FusedStream for ReceiverStream<T>` | Trait impl | Accessor / query |  |
| 99 | `as_ref`  | `AsRef<Receiver<T>> for ReceiverStream<T>` | Trait impl | Conversion |  |
| 105 | `as_mut`  | `AsMut<Receiver<T>> for ReceiverStream<T>` | Trait impl | Conversion |  |
| 111 | `from`  | `From<Receiver<T>> for ReceiverStream<T>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/mpsc_unbounded.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `UnboundedReceiverStream<T>` | Public API | Constructor | Create a new `UnboundedReceiverStream`. |
| 46 | `into_inner`  | `UnboundedReceiverStream<T>` | Public API | Conversion | Get back the inner `UnboundedReceiver`. |
| 54 | `close`  | `UnboundedReceiverStream<T>` | Public API | Data movement | Closes the receiving half of a channel without dropping it. |
| 62 | `poll_next`  | `Stream for UnboundedReceiverStream<T>` | Trait impl | Stream impl |  |
| 71 | `size_hint`  | `Stream for UnboundedReceiverStream<T>` | Trait impl | Stream impl | Returns the bounds of the stream based on the underlying receiver. |
| 82 | `is_terminated`  | `FusedStream for UnboundedReceiverStream<T>` | Trait impl | Accessor / query |  |
| 88 | `as_ref`  | `AsRef<UnboundedReceiver<T>> for UnboundedReceiverStream<T>` | Trait impl | Conversion |  |
| 94 | `as_mut`  | `AsMut<UnboundedReceiver<T>> for UnboundedReceiverStream<T>` | Trait impl | Conversion |  |
| 100 | `from`  | `From<UnboundedReceiver<T>> for UnboundedReceiverStream<T>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/read_dir.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `new`  | `ReadDirStream` | Public API | Constructor | Create a new `ReadDirStream`. |
| 42 | `into_inner`  | `ReadDirStream` | Public API | Conversion | Get back the inner `ReadDir`. |
| 50 | `poll_next`  | `Stream for ReadDirStream` | Trait impl | Stream impl |  |
| 56 | `as_ref`  | `AsRef<ReadDir> for ReadDirStream` | Trait impl | Conversion |  |
| 62 | `as_mut`  | `AsMut<ReadDir> for ReadDirStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/signal_unix.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `new`  | `SignalStream` | Public API | Constructor | Create a new `SignalStream`. |
| 39 | `into_inner`  | `SignalStream` | Public API | Conversion | Get back the inner `Signal`. |
| 47 | `poll_next`  | `Stream for SignalStream` | Trait impl | Stream impl |  |
| 53 | `as_ref`  | `AsRef<Signal> for SignalStream` | Trait impl | Conversion |  |
| 59 | `as_mut`  | `AsMut<Signal> for SignalStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/signal_windows.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 35 | `new`  | `CtrlCStream` | Public API | Constructor | Create a new `CtrlCStream`. |
| 40 | `into_inner`  | `CtrlCStream` | Public API | Conversion | Get back the inner `CtrlC`. |
| 48 | `poll_next`  | `Stream for CtrlCStream` | Trait impl | Stream impl |  |
| 54 | `as_ref`  | `AsRef<CtrlC> for CtrlCStream` | Trait impl | Conversion |  |
| 60 | `as_mut`  | `AsMut<CtrlC> for CtrlCStream` | Trait impl | Conversion |  |
| 94 | `new`  | `CtrlBreakStream` | Public API | Constructor | Create a new `CtrlBreakStream`. |
| 99 | `into_inner`  | `CtrlBreakStream` | Public API | Conversion | Get back the inner `CtrlBreak`. |
| 107 | `poll_next`  | `Stream for CtrlBreakStream` | Trait impl | Stream impl |  |
| 113 | `as_ref`  | `AsRef<CtrlBreak> for CtrlBreakStream` | Trait impl | Conversion |  |
| 119 | `as_mut`  | `AsMut<CtrlBreak> for CtrlBreakStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/split.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `new`  | `SplitStream<R>` | Public API | Constructor | Create a new `SplitStream`. |
| 46 | `into_inner`  | `SplitStream<R>` | Public API | Conversion | Get back the inner `Split`. |
| 51 | `as_pin_mut`  | `SplitStream<R>` | Public API | Conversion | Obtain a pinned reference to the inner `Split<R>`. |
| 59 | `poll_next`  | `Stream for SplitStream<R>` | Trait impl | Stream impl |  |
| 68 | `as_ref`  | `AsRef<Split<R>> for SplitStream<R>` | Trait impl | Conversion |  |
| 74 | `as_mut`  | `AsMut<Split<R>> for SplitStream<R>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/task.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 36 | `new`  | `JoinSetStream<T>` | Public API | Constructor | Create a new `JoinSetStream`. |
| 41 | `into_inner`  | `JoinSetStream<T>` | Public API | Conversion | Get back the inner `JoinSet`. |
| 49 | `poll_next`  | `Stream for JoinSetStream<T>` | Trait impl | Stream impl |  |
| 56 | `size_hint`  | `Stream for JoinSetStream<T>` | Trait impl | Stream impl | Returns the bounds of the stream based on the underlying `JoinSet`. |
| 63 | `as_ref`  | `AsRef<JoinSet<T>> for JoinSetStream<T>` | Trait impl | Conversion |  |
| 69 | `as_mut`  | `AsMut<JoinSet<T>> for JoinSetStream<T>` | Trait impl | Conversion |  |
| 75 | `from`  | `From<JoinSet<T>> for JoinSetStream<T>` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/tcp_listener.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 49 | `new`  | `TcpListenerStream` | Public API | Constructor | Create a new `TcpListenerStream`. |
| 54 | `into_inner`  | `TcpListenerStream` | Public API | Conversion | Get back the inner `TcpListener`. |
| 62 | `poll_next`  | `Stream for TcpListenerStream` | Trait impl | Stream impl |  |
| 75 | `as_ref`  | `AsRef<TcpListener> for TcpListenerStream` | Trait impl | Conversion |  |
| 81 | `as_mut`  | `AsMut<TcpListener> for TcpListenerStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/unix_listener.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `new`  | `UnixListenerStream` | Public API | Constructor | Create a new `UnixListenerStream`. |
| 43 | `into_inner`  | `UnixListenerStream` | Public API | Conversion | Get back the inner `UnixListener`. |
| 51 | `poll_next`  | `Stream for UnixListenerStream` | Trait impl | Stream impl |  |
| 64 | `as_ref`  | `AsRef<UnixListener> for UnixListenerStream` | Trait impl | Conversion |  |
| 70 | `as_mut`  | `AsMut<UnixListener> for UnixListenerStream` | Trait impl | Conversion |  |

## `tokio-stream/src/wrappers/watch.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 78 | `make_future` 🅰 |  | Private helper | Async operation |  |
| 87 | `new`  | `WatchStream<T>` | Public API | Constructor | Create a new `WatchStream`. |
| 94 | `from_changes`  | `WatchStream<T>` | Public API | Conversion | Create a new `WatchStream` that waits for the value to be changed. |
| 104 | `poll_next`  | `Stream for WatchStream<T>` | Trait impl | Stream impl |  |
| 123 | `fmt`  | `fmt::Debug for WatchStream<T>` | Trait impl | Formatting |  |
| 129 | `from`  | `From<Receiver<T>> for WatchStream<T>` | Trait impl | Conversion |  |

