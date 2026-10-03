# `tokio::fs::file` — 28 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 28 |

## `tokio/src/fs/file/tests.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `open_read`  |  | Test | Constructor |  |
| 39 | `read_twice_before_dispatch`  |  | Test | I/O operation |  |
| 63 | `read_with_smaller_buf`  |  | Test | I/O operation |  |
| 99 | `read_with_bigger_buf`  |  | Test | I/O operation |  |
| 154 | `read_err_then_read_success`  |  | Test | I/O operation |  |
| 196 | `open_write`  |  | Test | Constructor |  |
| 221 | `flush_while_idle`  |  | Test | I/O operation |  |
| 232 | `read_with_buffer_larger_than_max`  |  | Test | I/O operation |  |
| 304 | `write_with_buffer_larger_than_max`  |  | Test | I/O operation |  |
| 372 | `write_twice_before_dispatch`  |  | Test | I/O operation |  |
| 412 | `incomplete_read_followed_by_write`  |  | Test | Other / internal logic |  |
| 452 | `incomplete_partial_read_followed_by_write`  |  | Test | Other / internal logic |  |
| 496 | `incomplete_read_followed_by_flush`  |  | Test | Other / internal logic |  |
| 536 | `incomplete_flush_followed_by_write`  |  | Test | Other / internal logic |  |
| 572 | `read_err`  |  | Test | I/O operation |  |
| 592 | `write_write_err`  |  | Test | I/O operation |  |
| 610 | `write_read_write_err`  |  | Test | I/O operation |  |
| 644 | `write_read_flush_err`  |  | Test | I/O operation |  |
| 678 | `write_seek_write_err`  |  | Test | I/O operation |  |
| 710 | `write_seek_flush_err`  |  | Test | I/O operation |  |
| 742 | `sync_all_ordered_after_write`  |  | Test | Other / internal logic |  |
| 773 | `sync_all_err_ordered_after_write`  |  | Test | Other / internal logic |  |
| 806 | `sync_data_ordered_after_write`  |  | Test | Other / internal logic |  |
| 837 | `sync_data_err_ordered_after_write`  |  | Test | Other / internal logic |  |
| 870 | `open_set_len_ok`  |  | Test | Constructor |  |
| 886 | `open_set_len_err`  |  | Test | Constructor |  |
| 904 | `partial_read_set_len_ok`  |  | Test | Other / internal logic |  |
| 960 | `busy_file_seek_error`  |  | Test | Other / internal logic |  |

