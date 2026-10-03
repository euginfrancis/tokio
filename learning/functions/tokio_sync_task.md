# `tokio::sync::task` — 14 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 6 |
| Crate-internal | 4 |
| Private helper | 2 |
| Trait method (declaration/default) | 2 |

## `tokio/src/sync/task/atomic_waker.rs` (14)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 142 | `new`  | `AtomicWaker` | Crate-internal | Constructor | Create an `AtomicWaker` |
| 171 | `register_by_ref`  | `AtomicWaker` | Crate-internal | I/O registration | Registers the provided waker to be notified on calls to `wake`. |
| 175 | `do_register`  | `AtomicWaker` | Private helper | Other / internal logic |  |
| 179 | `catch_unwind`  |  | Private helper | Other / internal logic |  |
| 303 | `wake`  | `AtomicWaker` | Crate-internal | Wake / park | Wakes the task that last called `register`. |
| 313 | `take_waker`  | `AtomicWaker` | Crate-internal | Data movement | Attempts to take the `Waker` value out of the `AtomicWaker` with the intention that the caller will wake the task later. |
| 346 | `default`  | `Default for AtomicWaker` | Trait impl | Constructor |  |
| 352 | `fmt`  | `fmt::Debug for AtomicWaker` | Trait impl | Formatting |  |
| 361 | `wake`  | `trait WakerRef` | Trait method (declaration/default) | Wake / park |  |
| 362 | `into_waker`  | `trait WakerRef` | Trait method (declaration/default) | Conversion |  |
| 366 | `wake`  | `WakerRef for Waker` | Trait impl | Wake / park |  |
| 370 | `into_waker`  | `WakerRef for Waker` | Trait impl | Conversion |  |
| 376 | `wake`  | `WakerRef for &Waker` | Trait impl | Wake / park |  |
| 380 | `into_waker`  | `WakerRef for &Waker` | Trait impl | Conversion |  |

