# `tokio::runtime::io::driver` — 18 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 15 |
| Private helper | 2 |
| Trait impl | 1 |

## `tokio/src/runtime/io/driver/signal.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 6 | `register_signal_receiver`  | `Handle` | Crate-internal | I/O registration |  |
| 17 | `consume_signal_ready`  | `Driver` | Crate-internal | I/O operation |  |

## `tokio/src/runtime/io/driver/uring.rs` (16)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 23 | `new`  | `UringContext` | Crate-internal | Constructor |  |
| 30 | `ring`  | `UringContext` | Crate-internal | Other / internal logic |  |
| 34 | `ring_mut`  | `UringContext` | Crate-internal | Other / internal logic |  |
| 43 | `try_init`  | `UringContext` | Crate-internal | Non-blocking attempt | Perform `io_uring_setup` system call, and Returns true if this actually initialized the io_uring. |
| 65 | `dispatch_completions`  | `UringContext` | Crate-internal | Other / internal logic |  |
| 108 | `submit`  | `UringContext` | Crate-internal | Metrics / counters |  |
| 128 | `remove_op`  | `UringContext` | Crate-internal | Data movement |  |
| 135 | `drop`  | `Drop for UringContext` | Trait impl | Drop / cleanup |  |
| 176 | `add_uring_source`  | `Handle` | Private helper | Other / internal logic |  |
| 182 | `get_uring`  | `Handle` | Crate-internal | Accessor / query |  |
| 191 | `is_uring_ready`  | `Handle` | Crate-internal | Accessor / query | Returns `true` if io_uring has already been initialized and the given opcode is supported. |
| 202 | `is_uring_probed`  | `Handle` | Crate-internal | Accessor / query | Returns `true` if the io_uring probe has already been attempted (regardless of whether io_uring is supported). |
| 218 | `check_and_init` 🅰 | `Handle` | Crate-internal | Runtime/task control | Check if the io_uring context is initialized. |
| 243 | `try_init`  | `Handle` | Private helper | Non-blocking attempt | Initialize the io_uring context if it hasn't been initialized yet. |
| 262 | `register_op` ⚠ | `Handle` | Crate-internal | I/O registration | Register an operation with the io_uring. |
| 298 | `cancel_op`  | `Handle` | Crate-internal | Lifecycle / ref-count |  |

