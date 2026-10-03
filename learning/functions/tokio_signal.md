# `tokio::signal` — 90 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 34 |
| Trait impl | 14 |
| Test | 14 |
| Private helper | 13 |
| Crate-internal | 12 |
| Trait method (declaration/default) | 3 |

## `tokio/src/signal/ctrl_c.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 59 | `ctrl_c` 🅰 |  | Public API | Async operation | Completes when a "ctrl-c" notification is sent to the process. |

## `tokio/src/signal/mod.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 67 | `make_future` 🅰 |  | Private helper | Async operation |  |
| 73 | `new`  | `RxFuture` | Private helper | Constructor |  |
| 79 | `recv` 🅰 | `RxFuture` | Private helper | Data movement |  |
| 84 | `poll_recv`  | `RxFuture` | Private helper | Poll function |  |

## `tokio/src/signal/registry.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `default`  | `Default for EventInfo` | Trait impl | Constructor |  |
| 32 | `event_info`  | `trait Storage` | Trait method (declaration/default) | Other / internal logic | Gets the `EventInfo` for `id` if it exists. |
| 35 | `iter`  | `trait Storage` | Trait method (declaration/default) | Combinator / iteration | Returns an iterator over the storage. |
| 39 | `event_info`  | `Storage for Vec<EventInfo>` | Trait impl | Other / internal logic |  |
| 43 | `iter`  | `Storage for Vec<EventInfo>` | Trait impl | Combinator / iteration |  |
| 58 | `new`  | `Registry<S>` | Private helper | Constructor |  |
| 65 | `register_listener`  | `Registry<S>` | Private helper | I/O registration | Registers a new listener for `event_id`. |
| 75 | `record_event`  | `Registry<S>` | Private helper | Other / internal logic | Marks `event_id` as having been delivered, without broadcasting it to any listeners. |
| 84 | `broadcast`  | `Registry<S>` | Private helper | Data movement | Broadcasts all previously recorded events to their respective listeners. |
| 103 | `deref`  | `ops::Deref for Globals` | Trait impl | Deref |  |
| 110 | `register_listener`  | `Globals` | Crate-internal | I/O registration | Registers a new listener for `event_id`. |
| 116 | `record_event`  | `Globals` | Crate-internal | Other / internal logic | Marks `event_id` as having been delivered, without broadcasting it to any listeners. |
| 123 | `broadcast`  | `Globals` | Crate-internal | Data movement | Broadcasts all previously recorded events to their respective listeners. |
| 128 | `storage`  | `Globals` | Crate-internal | Other / internal logic |  |
| 133 | `globals_init`  |  | Private helper | Other / internal logic |  |
| 144 | `globals`  |  | Crate-internal | Other / internal logic |  |
| 163 | `smoke`  |  | Test | Other / internal logic |  |
| 215 | `register_panics_on_invalid_input`  |  | Test | I/O registration |  |
| 222 | `record_invalid_event_does_nothing`  |  | Test | Other / internal logic |  |
| 228 | `broadcast_returns_if_at_least_one_event_fired`  |  | Test | Data movement |  |
| 247 | `rt`  |  | Test | Other / internal logic |  |
| 254 | `collect` 🅰 |  | Test | Async operation |  |

## `tokio/src/signal/reusable_box.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `new`  | `ReusableBoxFuture<T>` | Crate-internal | Constructor | Create a new `ReusableBoxFuture<T>` containing the provided future. |
| 37 | `set`  | `ReusableBoxFuture<T>` | Crate-internal | Configuration / setter | Replaces the future currently stored in this box. |
| 51 | `try_set`  | `ReusableBoxFuture<T>` | Crate-internal | Non-blocking attempt | Replaces the future currently stored in this box. |
| 79 | `set_same_layout` ⚠ | `ReusableBoxFuture<T>` | Private helper | Configuration / setter | Sets the current future. |
| 110 | `get_pin`  | `ReusableBoxFuture<T>` | Crate-internal | Accessor / query | Gets a pinned reference to the underlying future. |
| 117 | `poll`  | `ReusableBoxFuture<T>` | Crate-internal | Poll function | Polls the future stored inside this box. |
| 126 | `poll`  | `Future for ReusableBoxFuture<T>` | Trait impl | Future impl (poll) | Polls the future stored inside this box. |
| 143 | `drop`  | `Drop for ReusableBoxFuture<T>` | Trait impl | Drop / cleanup |  |
| 151 | `fmt`  | `fmt::Debug for ReusableBoxFuture<T>` | Trait impl | Formatting |  |
| 166 | `test_different_futures`  |  | Test | Other / internal logic |  |
| 187 | `test_different_sizes`  |  | Test | Other / internal logic |  |
| 208 | `poll`  | `Future for ZeroSizedFuture` | Test | Future impl (poll) |  |
| 214 | `test_zero_sized`  |  | Test | Other / internal logic |  |

## `tokio/src/signal/unix.rs` (35)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `get`  | `OsStorage` | Private helper | Accessor / query |  |
| 33 | `default`  | `Default for OsStorage` | Trait impl | Constructor |  |
| 51 | `event_info`  | `Storage for OsStorage` | Trait impl | Other / internal logic |  |
| 55 | `iter`  | `Storage for OsStorage` | Trait impl | Combinator / iteration |  |
| 67 | `default`  | `Default for OsExtraData` | Trait impl | Constructor |  |
| 95 | `from_raw` 🅲 | `SignalKind` | Public API | Conversion |  |
| 106 | `as_raw_value` 🅲 | `SignalKind` | Public API | Conversion | Get the signal's numeric value. |
| 114 | `alarm` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGALRM` signal. |
| 122 | `child` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGCHLD` signal. |
| 130 | `hangup` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGHUP` signal. |
| 146 | `info` 🅲 | `SignalKind` | Public API | Other / internal logic |  |
| 154 | `interrupt` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGINT` signal. |
| 163 | `io` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGPOLL` signal. |
| 171 | `io` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGIO` signal. |
| 180 | `pipe` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGPIPE` signal. |
| 189 | `quit` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGQUIT` signal. |
| 197 | `terminate` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGTERM` signal. |
| 205 | `user_defined1` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGUSR1` signal. |
| 213 | `user_defined2` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGUSR2` signal. |
| 221 | `window_change` 🅲 | `SignalKind` | Public API | Other / internal logic | Represents the `SIGWINCH` signal. |
| 227 | `from`  | `From<std::os::raw::c_int> for SignalKind` | Trait impl | Conversion |  |
| 233 | `from`  | `From<SignalKind> for std::os::raw::c_int` | Trait impl | Conversion |  |
| 252 | `action`  |  | Private helper | Other / internal logic | Our global signal handler for all signals registered by this module. |
| 266 | `signal_enable`  |  | Private helper | Other / internal logic | Enables this module to receive signal notifications for the `signal` provided. |
| 398 | `signal`  |  | Public API | Other / internal logic | Creates a new listener which will receive notifications when the current process receives the specified signal `kind`. |
| 407 | `signal_with_handle`  |  | Crate-internal | Other / internal logic |  |
| 448 | `recv` 🅰 | `Signal` | Public API | Data movement | Receives the next signal notification event. |
| 482 | `poll_recv`  | `Signal` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |
| 490 | `poll_recv`  | `trait InternalStream` | Trait method (declaration/default) | Poll function |  |
| 495 | `poll_recv`  | `InternalStream for Signal` | Trait impl | Poll function |  |
| 500 | `ctrl_c`  |  | Crate-internal | Other / internal logic |  |
| 509 | `signal_enable_error_on_invalid_input`  |  | Test | Other / internal logic |  |
| 523 | `signal_enable_error_on_forbidden_input`  |  | Test | Other / internal logic |  |
| 537 | `from_c_int`  |  | Test | Conversion |  |
| 542 | `into_c_int`  |  | Test | Conversion |  |

## `tokio/src/signal/windows.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 46 | `ctrl_c`  |  | Public API | Other / internal logic | Creates a new listener which receives "ctrl-c" notifications sent to the process. |
| 93 | `recv` 🅰 | `CtrlC` | Public API | Data movement | Receives the next signal notification event. |
| 127 | `poll_recv`  | `CtrlC` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |
| 172 | `recv` 🅰 | `CtrlBreak` | Public API | Data movement | Receives the next signal notification event. |
| 206 | `poll_recv`  | `CtrlBreak` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |
| 231 | `ctrl_break`  |  | Public API | Other / internal logic | Creates a new listener which receives "ctrl-break" notifications sent to the process. |
| 259 | `ctrl_close`  |  | Public API | Other / internal logic | Creates a new listener which receives "ctrl-close" notifications sent to the process. |
| 301 | `recv` 🅰 | `CtrlClose` | Public API | Data movement | Receives the next signal notification event. |
| 335 | `poll_recv`  | `CtrlClose` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |
| 359 | `ctrl_shutdown`  |  | Public API | Other / internal logic | Creates a new listener which receives "ctrl-shutdown" notifications sent to the process. |
| 401 | `recv` 🅰 | `CtrlShutdown` | Public API | Data movement | Receives the next signal notification event. |
| 435 | `poll_recv`  | `CtrlShutdown` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |
| 459 | `ctrl_logoff`  |  | Public API | Other / internal logic | Creates a new listener which receives "ctrl-logoff" notifications sent to the process. |
| 501 | `recv` 🅰 | `CtrlLogoff` | Public API | Data movement | Receives the next signal notification event. |
| 535 | `poll_recv`  | `CtrlLogoff` | Public API | Poll function | Polls to receive the next signal notification event, outside of an `async` context. |

