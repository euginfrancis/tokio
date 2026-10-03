# `tokio::runtime::driver` — 8 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 3 |
| Trait method (declaration/default) | 3 |
| Crate-internal | 2 |

## `tokio/src/runtime/driver/op.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 97 | `new` ⚠ | `Op<T>` | Crate-internal | Constructor | # Safety Callers must ensure that parameters of the entry (such as buffer) are valid and will be valid for the entire duration of the operation, otherwise it may cause memory problems. |
| 105 | `take_data`  | `Op<T>` | Crate-internal | Data movement |  |
| 111 | `drop`  | `Drop for Op<T>` | Trait impl | Drop / cleanup |  |
| 134 | `from`  | `From<cqueue::Entry> for CqeResult` | Trait impl | Conversion |  |
| 148 | `complete`  | `trait Completable` | Trait method (declaration/default) | Runtime/task control |  |
| 154 | `complete_with_error`  | `trait Completable` | Trait method (declaration/default) | Runtime/task control |  |
| 159 | `cancel`  | `trait Cancellable` | Trait method (declaration/default) | Lifecycle / ref-count |  |
| 167 | `poll`  | `Future for Op<T>` | Trait impl | Future impl (poll) |  |

