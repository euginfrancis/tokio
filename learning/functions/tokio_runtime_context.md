# `tokio::runtime::context` — 22 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 16 |
| Trait impl | 6 |

## `tokio/src/runtime/context/blocking.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `try_enter_blocking_region`  |  | Crate-internal | Non-blocking attempt |  |
| 34 | `disallow_block_in_place`  |  | Crate-internal | Other / internal logic | Disallows blocking in the current runtime context until the guard is dropped. |
| 53 | `new`  | `BlockingRegionGuard` | Crate-internal | Constructor |  |
| 59 | `block_on`  | `BlockingRegionGuard` | Crate-internal | Runtime/task control | Blocks the thread on the specified future, returning the value with which that future completes. |
| 73 | `block_on_timeout`  | `BlockingRegionGuard` | Crate-internal | Runtime/task control | Blocks the thread on the specified future for **at most** `timeout` If the future completes before `timeout`, the result is returned. |
| 110 | `drop`  | `Drop for DisallowBlockInPlaceGuard` | Trait impl | Drop / cleanup |  |

## `tokio/src/runtime/context/current.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `try_set_current`  |  | Crate-internal | Non-blocking attempt | Sets this [`Handle`] as the current active [`Handle`]. |
| 37 | `with_current`  |  | Crate-internal | Constructor |  |
| 49 | `set_current`  | `Context` | Crate-internal | Configuration / setter |  |
| 67 | `new` 🅲 | `HandleCell` | Crate-internal | Constructor |  |
| 76 | `drop`  | `Drop for SetCurrentGuard` | Trait impl | Drop / cleanup |  |

## `tokio/src/runtime/context/runtime.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 35 | `enter_runtime`  |  | Crate-internal | Runtime/task control | Marks the current thread as being within the dynamic extent of an executor. |
| 78 | `fmt`  | `fmt::Debug for EnterRuntimeGuard` | Trait impl | Formatting |  |
| 84 | `drop`  | `Drop for EnterRuntimeGuard` | Trait impl | Drop / cleanup |  |
| 97 | `is_entered`  | `EnterRuntime` | Crate-internal | Accessor / query |  |

## `tokio/src/runtime/context/runtime_mt.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `current_enter_context`  |  | Crate-internal | Other / internal logic | Returns true if in a runtime context. |
| 10 | `exit_runtime`  |  | Crate-internal | Other / internal logic | Forces the current "entered" state to be cleared while the closure is executed. |
| 15 | `drop`  | `Drop for Reset` | Trait impl | Drop / cleanup |  |

## `tokio/src/runtime/context/scoped.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `new` 🅲 | `Scoped<T>` | Crate-internal | Constructor |  |
| 17 | `set`  | `Scoped<T>` | Crate-internal | Configuration / setter | Inserts a value into the scoped cell for the duration of the closure |
| 27 | `drop`  | `Drop for Reset<'_, T>` | Trait impl | Drop / cleanup |  |
| 44 | `with`  | `Scoped<T>` | Crate-internal | Combinator / iteration | Gets the value out of the scoped cell; |

