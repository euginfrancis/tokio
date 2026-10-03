# `tokio-util::future` — 4 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 2 |
| Trait impl | 2 |

## `tokio-util/src/future/with_cancellation_token.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `new`  | `WithCancellationTokenFuture<'a, F>` | Crate-internal | Constructor |  |
| 37 | `poll`  | `Future for WithCancellationTokenFuture<'a, F>` | Trait impl | Future impl (poll) |  |
| 61 | `new`  | `WithCancellationTokenFutureOwned<F>` | Crate-internal | Constructor |  |
| 72 | `poll`  | `Future for WithCancellationTokenFutureOwned<F>` | Trait impl | Future impl (poll) |  |

