# `tokio-util::util` — 15 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 4 |
| Trait impl | 3 |
| Private helper | 3 |
| Test | 3 |
| Public API | 2 |

## `tokio-util/src/util/maybe_dangling.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 31 | `drop`  | `Drop for MaybeDangling<T>` | Trait impl | Drop / cleanup |  |
| 38 | `new`  | `MaybeDangling<T>` | Crate-internal | Constructor |  |
| 46 | `poll`  | `Future for MaybeDangling<F>` | Trait impl | Future impl (poll) |  |
| 54 | `maybedangling_runs_drop`  |  | Private helper | Other / internal logic |  |
| 58 | `drop`  | `Drop for SetOnDrop<'_>` | Trait impl | Drop / cleanup |  |

## `tokio-util/src/util/memchr.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `memchr_inner`  |  | Private helper | Other / internal logic |  |
| 12 | `memchr_inner`  |  | Private helper | Other / internal logic |  |
| 36 | `memchr`  |  | Crate-internal | Other / internal logic |  |
| 58 | `memchr_test`  |  | Test | Other / internal logic |  |
| 82 | `memchr_all`  |  | Test | Other / internal logic |  |
| 97 | `memchr_empty`  |  | Test | Other / internal logic |  |

## `tokio-util/src/util/mod.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `made_progress`  | `RestoreOnPending` | Crate-internal | Other / internal logic |  |
| 30 | `poll_proceed`  |  | Crate-internal | Poll function |  |

## `tokio-util/src/util/poll_buf.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 47 | `poll_read_buf`  |  | Public API | Poll function | Try to read data from an `AsyncRead` into an implementer of the [`BufMut`] trait. |
| 121 | `poll_write_buf`  |  | Public API | Poll function | Try to write data from an implementer of the [`Buf`] trait to an [`AsyncWrite`], advancing the buffer's internal cursor. |

