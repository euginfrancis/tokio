# `tokio::fs::open_options` — 27 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 11 |
| Trait impl | 9 |
| Public API | 7 |

## `tokio/src/fs/open_options/mock_open_options.rs` (15)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `append`  |  | Public API | Other / internal logic |  |
| 16 | `create`  |  | Public API | Constructor |  |
| 17 | `create_new`  |  | Public API | Constructor |  |
| 18 | `open`  |  | Public API | Constructor |  |
| 19 | `read`  |  | Public API | I/O operation |  |
| 20 | `truncate`  |  | Public API | Other / internal logic |  |
| 21 | `write`  |  | Public API | I/O operation |  |
| 24 | `clone`  | `Clone for OpenOptions` | Trait impl | Clone |  |
| 28 | `custom_flags`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 29 | `mode`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 33 | `access_mode`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 34 | `share_mode`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 35 | `custom_flags`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 36 | `attributes`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |
| 37 | `security_qos_flags`  | `OpenOptionsExt for OpenOptions` | Trait impl | Other / internal logic |  |

## `tokio/src/fs/open_options/uring_open_options.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `new`  | `UringOpenOptions` | Crate-internal | Constructor |  |
| 34 | `append`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 39 | `create`  | `UringOpenOptions` | Crate-internal | Constructor |  |
| 44 | `create_new`  | `UringOpenOptions` | Crate-internal | Constructor |  |
| 49 | `read`  | `UringOpenOptions` | Crate-internal | I/O operation |  |
| 54 | `write`  | `UringOpenOptions` | Crate-internal | I/O operation |  |
| 59 | `truncate`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 64 | `mode`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 69 | `custom_flags`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 75 | `access_mode`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 87 | `creation_mode`  | `UringOpenOptions` | Crate-internal | Other / internal logic |  |
| 113 | `from`  | `From<UringOpenOptions> for StdOpenOptions` | Trait impl | Conversion |  |

