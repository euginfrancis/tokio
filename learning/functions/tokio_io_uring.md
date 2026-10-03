# `tokio::io::uring` — 38 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 24 |
| Crate-internal | 10 |
| Trait method (declaration/default) | 3 |
| Private helper | 1 |

## `tokio/src/io/uring/open.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 31 | `complete`  | `Completable for Open` | Trait impl | Runtime/task control |  |
| 37 | `complete_with_error`  | `Completable for Open` | Trait impl | Runtime/task control |  |
| 43 | `cancel`  | `Cancellable for Open` | Trait impl | Lifecycle / ref-count |  |
| 50 | `open`  | `Op<Open>` | Crate-internal | Constructor | Submit a request to open a file. |
| 71 | `open` 🅰 |  | Crate-internal | Constructor |  |

## `tokio/src/io/uring/read.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `uring_read_prepare`  | `trait ReadBuffer` | Trait method (declaration/default) | Other / internal logic | Prepare the buffer for a read operation. |
| 22 | `uring_read_complete` ⚠ | `trait ReadBuffer` | Trait method (declaration/default) | Other / internal logic | Complete a read of `n` bytes. |
| 26 | `uring_read_prepare`  | `ReadBuffer for Vec<u8>` | Trait impl | Other / internal logic |  |
| 32 | `uring_read_complete` ⚠ | `ReadBuffer for Vec<u8>` | Trait impl | Other / internal logic |  |
| 40 | `uring_read_prepare`  | `ReadBuffer for Buf` | Trait impl | Other / internal logic |  |
| 44 | `uring_read_complete` ⚠ | `ReadBuffer for Buf` | Trait impl | Other / internal logic |  |
| 56 | `fmt`  | `fmt::Debug for Read<B, F>` | Trait impl | Formatting |  |
| 66 | `complete`  | `Completable for Read<B, F>` | Trait impl | Runtime/task control |  |
| 75 | `complete_with_error`  | `Completable for Read<B, F>` | Trait impl | Runtime/task control |  |
| 81 | `cancel`  | `Cancellable for Read<Vec<u8>, OwnedFd>` | Trait impl | Lifecycle / ref-count |  |
| 87 | `cancel`  | `Cancellable for Read<Buf, ArcFd>` | Trait impl | Lifecycle / ref-count |  |
| 102 | `read_at`  | `Op<Read<B, F>>` | Crate-internal | I/O operation | Submit a read operation via io-uring. |

## `tokio/src/io/uring/rename.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `complete`  | `Completable for Rename` | Trait impl | Runtime/task control |  |
| 25 | `complete_with_error`  | `Completable for Rename` | Trait impl | Runtime/task control |  |
| 31 | `cancel`  | `Cancellable for Rename` | Trait impl | Lifecycle / ref-count |  |
| 37 | `rename`  | `Op<Rename>` | Crate-internal | Other / internal logic |  |

## `tokio/src/io/uring/statx.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `len`  | `Metadata` | Crate-internal | Accessor / query | Returns the size of the file, in bytes, this metadata is for. |
| 40 | `fmt`  | `Debug for Metadata` | Trait impl | Formatting |  |
| 58 | `complete`  | `Completable for Statx` | Trait impl | Runtime/task control |  |
| 68 | `complete_with_error`  | `Completable for Statx` | Trait impl | Runtime/task control |  |
| 74 | `cancel`  | `Cancellable for Statx` | Trait impl | Lifecycle / ref-count |  |
| 82 | `statx`  | `Op<Statx>` | Private helper | Other / internal logic | Submit a request to retrieve a file's status. |
| 110 | `metadata`  | `Op<Statx>` | Crate-internal | Other / internal logic | Retrieves the metadata information of the given path, following symlinks if the path provided points to a symlink location. |
| 115 | `file_metadata`  | `Op<Statx>` | Crate-internal | Other / internal logic | Retrieves the metadata information of the given file |
| 155 | `symlink_metadata`  | `Op<Statx>` | Crate-internal | Other / internal logic | Retrieves the metadata information of the given path without following symlinks. |

## `tokio/src/io/uring/utils.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `as_raw_fd`  | `trait UringFd` | Trait method (declaration/default) | Conversion |  |
| 18 | `as_raw_fd`  | `UringFd for OwnedFd` | Trait impl | Conversion |  |
| 24 | `as_raw_fd`  | `UringFd for ArcFd` | Trait impl | Conversion |  |
| 29 | `cstr`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/io/uring/write.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `complete`  | `Completable for Write` | Trait impl | Runtime/task control |  |
| 20 | `complete_with_error`  | `Completable for Write` | Trait impl | Runtime/task control |  |
| 26 | `cancel`  | `Cancellable for Write` | Trait impl | Lifecycle / ref-count |  |
| 34 | `write_at`  | `Op<Write>` | Crate-internal | I/O operation | Issue a write that starts at `buf_offset` within `buf` and writes some bytes into `file` at `file_offset`. |

