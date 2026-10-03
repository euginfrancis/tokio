# `tokio::runtime::task::trace` — 29 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 11 |
| Private helper | 10 |
| Trait impl | 7 |
| Public API | 1 |

## `tokio/src/runtime/task/trace/mod.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 79 | `new` 🅲 | `Context` | Crate-internal | Constructor |  |
| 88 | `try_with_current` ⚠ | `Context` | Private helper | Non-blocking attempt | SAFETY: Callers of this function must ensure that trace frames always form a valid linked list. |
| 97 | `with_current_frame` ⚠ | `Context` | Private helper | Constructor | SAFETY: Callers of this function must ensure that trace frames always form a valid linked list. |
| 106 | `current_frame_addr`  | `Context` | Private helper | Other / internal logic |  |
| 119 | `try_with_current_trace_leaf_fn`  | `Context` | Private helper | Non-blocking attempt | Calls the provided closure if we are being traced. |
| 147 | `is_tracing`  | `Context` | Crate-internal | Accessor / query | Produces `true` if the current task is being traced; otherwise false. |
| 209 | `trace_with`  |  | Public API | Debugging / tracing | Runs `f`. |
| 258 | `capture`  | `Trace` | Crate-internal | Other / internal logic | Invokes `f`, returning both its result and the collection of backtraces captured at each sub-invocation of [`trace_leaf`]. |
| 267 | `empty`  | `Trace` | Crate-internal | Other / internal logic |  |
| 271 | `push_backtrace`  | `Trace` | Private helper | Data movement |  |
| 277 | `root`  | `Trace` | Crate-internal | Other / internal logic | The root of a trace. |
| 281 | `backtraces`  | `Trace` | Crate-internal | Other / internal logic |  |
| 296 | `trace_leaf`  |  | Crate-internal | Debugging / tracing |  |
| 314 | `fmt`  | `fmt::Display for Trace` | Trait impl | Formatting |  |
| 319 | `defer`  |  | Private helper | Runtime/task control |  |
| 326 | `drop`  | `R, R> Drop for Defer<F, R>` | Trait impl | Other / internal logic |  |
| 340 | `poll`  | `Future for Root<T>` | Trait impl | Future impl (poll) |  |
| 367 | `trace_current_thread`  |  | Crate-internal | Debugging / tracing | Trace and poll all tasks of the `current_thread` runtime. |
| 393 | `trace_multi_thread`  |  | Crate-internal | Debugging / tracing | Trace and poll all tasks of the `multi_thread` runtime. |
| 420 | `trace_owned`  |  | Private helper | Debugging / tracing | Trace the `OwnedTasks`. |

## `tokio/src/runtime/task/trace/symbol.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `hash`  | `Hash for Symbol` | Trait impl | Comparison |  |
| 45 | `eq`  | `PartialEq for Symbol` | Trait impl | Comparison |  |
| 66 | `fmt`  | `fmt::Display for Symbol` | Trait impl | Formatting |  |

## `tokio/src/runtime/task/trace/trace_impl.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `trace_leaf`  |  | Crate-internal | Debugging / tracing | Capture a backtrace via `backtrace::trace` and collect it into `trace`. |

## `tokio/src/runtime/task/trace/tree.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `from_trace`  | `Tree` | Crate-internal | Conversion | Constructs a [`Tree`] from [`Trace`] |
| 47 | `consequences`  | `Tree` | Private helper | Other / internal logic | Produces the sub-symbols of a given symbol. |
| 52 | `display`  | `Tree` | Private helper | Other / internal logic | Format this [`Tree`] as a textual tree. |
| 93 | `fmt`  | `fmt::Display for Tree` | Trait impl | Formatting |  |
| 103 | `to_symboltrace`  |  | Private helper | Conversion | Resolve a sequence of [`backtrace::BacktraceFrame`]s into a sequence of [`Symbol`]s. |

