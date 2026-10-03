# `tokio::fs` — 135 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 75 |
| Trait impl | 33 |
| Private helper | 19 |
| Crate-internal | 8 |

## `tokio/src/fs/canonicalize.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 46 | `canonicalize` 🅰 |  | Public API | Async operation | Returns the canonical, absolute form of a path with all intermediate components normalized and symbolic links resolved. |

## `tokio/src/fs/copy.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 20 | `copy` 🅰 |  | Public API | I/O operation | Copies the contents of one file to another. |

## `tokio/src/fs/create_dir.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 47 | `create_dir` 🅰 |  | Public API | Constructor | Creates a new, empty directory at the provided path. |

## `tokio/src/fs/create_dir_all.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 51 | `create_dir_all` 🅰 |  | Public API | Constructor | Recursively creates a directory and all of its parent components if they are missing. |

## `tokio/src/fs/dir_builder.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `new`  | `DirBuilder` | Public API | Constructor | Creates a new set of options with default mode/security settings for all platforms and also non-recursive. |
| 52 | `recursive`  | `DirBuilder` | Public API | Other / internal logic | Indicates whether to create directories recursively (including all parent directories). |
| 91 | `create` 🅰 | `DirBuilder` | Public API | Constructor | Creates the specified directory with the configured options. |
| 124 | `mode`  | `DirBuilder` | Public API | Other / internal logic | Sets the mode to create new directories with. |

## `tokio/src/fs/file.rs` (40)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 157 | `open` 🅰 | `File` | Public API | Constructor | Attempts to open a file in read-only mode. |
| 192 | `create` 🅰 | `File` | Public API | Constructor | Opens a file in write-only mode. |
| 232 | `create_new` 🅰 | `File` | Public API | Constructor | Opens a file in read-write mode. |
| 268 | `options`  | `File` | Public API | Other / internal logic | Returns a new [`OpenOptions`] object. |
| 282 | `from_std`  | `File` | Public API | Conversion | Converts a [`std::fs::File`] to a [`tokio::fs::File`](File). |
| 317 | `sync_all` 🅰 | `File` | Public API | Async operation | Attempts to sync all OS-internal metadata to disk. |
| 352 | `sync_data` 🅰 | `File` | Public API | Async operation | This function is similar to `sync_all`, except that it may not synchronize file metadata to the filesystem. |
| 390 | `set_len` 🅰 | `File` | Public API | Configuration / setter | Truncates or extends the underlying file, updating the size of this file to become size. |
| 456 | `metadata` 🅰 | `File` | Public API | Async operation | Queries metadata about the underlying file. |
| 476 | `try_clone` 🅰 | `File` | Public API | Non-blocking attempt | Creates a new `File` instance that shares the same underlying file handle as the existing `File` instance. |
| 501 | `into_std` 🅰 | `File` | Public API | Conversion | Destructures `File` into a [`std::fs::File`]. |
| 525 | `try_into_std`  | `File` | Public API | Non-blocking attempt | Tries to immediately destructure `File` into a [`std::fs::File`]. |
| 564 | `set_permissions` 🅰 | `File` | Public API | Configuration / setter | Changes the permissions on the underlying file. |
| 598 | `set_max_buf_size`  | `File` | Public API | Configuration / setter | Set the maximum buffer size for the underlying [`AsyncRead`] / [`AsyncWrite`] operation. |
| 604 | `max_buf_size`  | `File` | Public API | Configuration / setter | Get the maximum buffer size for the underlying [`AsyncRead`] / [`AsyncWrite`] operation. |
| 610 | `poll_read`  | `AsyncRead for File` | Trait impl | I/O trait impl |  |
| 682 | `start_seek`  | `AsyncSeek for File` | Trait impl | I/O trait impl |  |
| 713 | `poll_complete`  | `AsyncSeek for File` | Trait impl | I/O trait impl |  |
| 750 | `poll_write`  | `AsyncWrite for File` | Trait impl | I/O trait impl |  |
| 830 | `poll_write_vectored`  | `AsyncWrite for File` | Trait impl | I/O trait impl |  |
| 910 | `is_write_vectored`  | `AsyncWrite for File` | Trait impl | I/O trait impl |  |
| 914 | `poll_flush`  | `AsyncWrite for File` | Trait impl | I/O trait impl |  |
| 920 | `poll_shutdown`  | `AsyncWrite for File` | Trait impl | I/O trait impl |  |
| 927 | `from`  | `From<StdFile> for File` | Trait impl | Conversion |  |
| 933 | `fmt`  | `fmt::Debug for File` | Trait impl | Formatting |  |
| 942 | `from`  | `From<std::os::fd::OwnedFd> for File` | Trait impl | Conversion |  |
| 949 | `as_raw_fd`  | `std::os::unix::io::AsRawFd for File` | Trait impl | OS handle access |  |
| 956 | `as_fd`  | `std::os::unix::io::AsFd for File` | Trait impl | OS handle access |  |
| 965 | `from_raw_fd` ⚠ | `std::os::unix::io::FromRawFd for File` | Trait impl | Conversion |  |
| 976 | `from`  | `From<OwnedHandle> for File` | Trait impl | Conversion |  |
| 982 | `as_raw_handle`  | `AsRawHandle for File` | Trait impl | OS handle access |  |
| 988 | `as_handle`  | `AsHandle for File` | Trait impl | OS handle access |  |
| 998 | `from_raw_handle` ⚠ | `FromRawHandle for File` | Trait impl | Conversion |  |
| 1007 | `poll_read_inner`  | `Inner` | Private helper | Poll function |  |
| 1056 | `uring_read` 🅰 | `Inner` | Private helper | Async operation |  |
| 1090 | `lazy_init_read` 🅰 | `Inner` | Private helper | Async operation |  |
| 1113 | `spawn_blocking_read`  | `Inner` | Private helper | Runtime/task control |  |
| 1128 | `complete_inflight` 🅰 | `Inner` | Private helper | Runtime/task control |  |
| 1134 | `poll_complete_inflight`  | `Inner` | Private helper | Poll function |  |
| 1146 | `poll_flush`  | `Inner` | Private helper | Poll function |  |

## `tokio/src/fs/hard_link.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 39 | `hard_link` 🅰 |  | Public API | Async operation | Creates a new hard link on the filesystem. |

## `tokio/src/fs/metadata.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 43 | `metadata` 🅰 |  | Public API | Async operation | Given a path, queries the file system to get information about a file, directory, etc. |

## `tokio/src/fs/mocks.rs` (30)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `create`  |  | Public API | Constructor |  |
| 27 | `inner_flush`  |  | Public API | Other / internal logic |  |
| 28 | `inner_read`  |  | Public API | Other / internal logic |  |
| 29 | `inner_seek`  |  | Public API | Other / internal logic |  |
| 30 | `inner_write`  |  | Public API | Other / internal logic |  |
| 31 | `metadata`  |  | Public API | Other / internal logic |  |
| 32 | `open`  |  | Public API | Constructor |  |
| 33 | `set_len`  |  | Public API | Configuration / setter |  |
| 34 | `set_permissions`  |  | Public API | Configuration / setter |  |
| 35 | `set_max_buf_size`  |  | Public API | Configuration / setter |  |
| 36 | `sync_all`  |  | Public API | Other / internal logic |  |
| 37 | `sync_data`  |  | Public API | Other / internal logic |  |
| 38 | `try_clone`  |  | Public API | Non-blocking attempt |  |
| 42 | `from`  | `From<std::os::windows::io::OwnedHandle> for File` | Trait impl | Conversion |  |
| 46 | `as_raw_handle`  | `std::os::windows::io::AsRawHandle for File` | Trait impl | OS handle access |  |
| 50 | `from_raw_handle` ⚠ | `std::os::windows::io::FromRawHandle for File` | Trait impl | Conversion |  |
| 54 | `as_raw_fd`  | `std::os::unix::io::AsRawFd for File` | Trait impl | OS handle access |  |
| 59 | `from_raw_fd` ⚠ | `std::os::unix::io::FromRawFd for File` | Trait impl | Conversion |  |
| 64 | `read`  | `Read for MockFile` | Trait impl | I/O operation |  |
| 77 | `read`  | `Read for &'_ MockFile` | Trait impl | I/O operation |  |
| 90 | `seek`  | `Seek for &'_ MockFile` | Trait impl | I/O operation |  |
| 96 | `write`  | `Write for &'_ MockFile` | Trait impl | I/O operation |  |
| 100 | `flush`  | `Write for &'_ MockFile` | Trait impl | I/O operation |  |
| 108 | `from`  | `From<MockFile> for OwnedFd` | Trait impl | Conversion |  |
| 116 | `from`  | `From<OwnedFd> for MockFile` | Trait impl | Conversion |  |
| 131 | `spawn_blocking`  |  | Crate-internal | Runtime/task control |  |
| 146 | `spawn_mandatory_blocking`  |  | Crate-internal | Runtime/task control |  |
| 164 | `poll`  | `Future for JoinHandle<T>` | Trait impl | Future impl (poll) |  |
| 178 | `len`  |  | Crate-internal | Accessor / query |  |
| 182 | `run_one`  |  | Crate-internal | Runtime/task control |  |

## `tokio/src/fs/mod.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 320 | `asyncify` 🅰 |  | Crate-internal | Async operation |  |

## `tokio/src/fs/open_options.rs` (20)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 122 | `new`  | `OpenOptions` | Public API | Constructor | Creates a blank new set of options ready for configuration. |
| 168 | `read`  | `OpenOptions` | Public API | I/O operation | Sets the option for read access. |
| 212 | `write`  | `OpenOptions` | Public API | I/O operation | Sets the option for write access. |
| 285 | `append`  | `OpenOptions` | Public API | Other / internal logic | Sets the option for the append mode. |
| 332 | `truncate`  | `OpenOptions` | Public API | Other / internal logic | Sets the option for truncating a previous file. |
| 382 | `create`  | `OpenOptions` | Public API | Constructor | Sets the option for creating a new file. |
| 439 | `create_new`  | `OpenOptions` | Public API | Constructor | Sets the option to always create a new file. |
| 520 | `open` 🅰 | `OpenOptions` | Public API | Constructor | Opens a file at `path` with the options specified by `self`. |
| 524 | `open_inner` 🅰 | `OpenOptions` | Private helper | Constructor |  |
| 552 | `std_open` 🅰 | `OpenOptions` | Private helper | Async operation |  |
| 560 | `as_inner_mut`  | `OpenOptions` | Crate-internal | Conversion |  |
| 594 | `mode`  | `OpenOptions` | Public API | Other / internal logic | Sets the mode bits that a new file will be created with. |
| 639 | `custom_flags`  | `OpenOptions` | Public API | Other / internal logic | Passes custom flags to the `flags` argument of `open`. |
| 685 | `access_mode`  | `OpenOptions` | Public API | Other / internal logic | Overrides the `dwDesiredAccess` argument to the call to [`CreateFile`] with the specified value. |
| 718 | `share_mode`  | `OpenOptions` | Public API | Other / internal logic | Overrides the `dwShareMode` argument to the call to [`CreateFile`] with the specified value. |
| 750 | `custom_flags`  | `OpenOptions` | Public API | Other / internal logic | Sets extra flags for the `dwFileFlags` argument to the call to [`CreateFile2`] to the specified value (or combines it with `attributes` and `security_qos_flags` to set the `dwFlagsAndAttributes` for [ |
| 789 | `attributes`  | `OpenOptions` | Public API | Other / internal logic | Sets the `dwFileAttributes` argument to the call to [`CreateFile2`] to the specified value (or combines it with `custom_flags` and `security_qos_flags` to set the `dwFlagsAndAttributes` for [`CreateFi |
| 837 | `security_qos_flags`  | `OpenOptions` | Public API | Other / internal logic | Sets the `dwSecurityQosFlags` argument to the call to [`CreateFile2`] to the specified value (or combines it with `custom_flags` and `attributes` to set the `dwFlagsAndAttributes` for [`CreateFile`]). |
| 845 | `from`  | `From<StdOpenOptions> for OpenOptions` | Trait impl | Conversion |  |
| 857 | `default`  | `Default for OpenOptions` | Trait impl | Constructor |  |

## `tokio/src/fs/read.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 56 | `read` 🅰 |  | Public API | I/O operation | Reads the entire contents of a file into a bytes vector. |
| 93 | `read_spawn_blocking` 🅰 |  | Private helper | I/O operation |  |

## `tokio/src/fs/read_dir.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `read_dir` 🅰 |  | Public API | I/O operation | Returns a stream over the entries within a directory. |
| 78 | `next_entry` 🅰 | `ReadDir` | Public API | Async operation | Returns the next entry in the directory stream. |
| 101 | `poll_next_entry`  | `ReadDir` | Public API | Poll function | Polls for the next directory entry in the stream. |
| 127 | `next_chunk`  | `ReadDir` | Private helper | Other / internal logic |  |
| 183 | `ino`  | `DirEntry` | Public API | Other / internal logic | Returns the underlying `d_ino` field in the contained `dirent` structure. |
| 244 | `path`  | `DirEntry` | Public API | Other / internal logic | Returns the full path to the file that this entry represents. |
| 265 | `file_name`  | `DirEntry` | Public API | Other / internal logic | Returns the bare file name of this directory entry without any other leading path component. |
| 299 | `metadata` 🅰 | `DirEntry` | Public API | Async operation | Returns the metadata for the file that this entry points at. |
| 334 | `file_type` 🅰 | `DirEntry` | Public API | Async operation | Returns the file type for the file that this entry points at. |
| 354 | `as_inner`  | `DirEntry` | Crate-internal | Conversion | Returns a reference to the underlying `std::fs::DirEntry`. |

## `tokio/src/fs/read_link.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `read_link` 🅰 |  | Public API | I/O operation | Reads a symbolic link, returning the file that the link points to. |

## `tokio/src/fs/read_to_string.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 27 | `read_to_string` 🅰 |  | Public API | I/O operation | Creates a future which will open a file for reading and read the entire contents into a string and return said string. |

## `tokio/src/fs/read_uring.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `read_uring` 🅰 |  | Crate-internal | I/O operation |  |
| 56 | `read_to_end_uring` 🅰 |  | Private helper | I/O operation |  |
| 100 | `small_probe_read` 🅰 |  | Private helper | Async operation |  |
| 129 | `op_read` 🅰 |  | Private helper | Async operation |  |

## `tokio/src/fs/remove_dir.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `remove_dir` 🅰 |  | Public API | Data movement | Removes an existing, empty directory. |

## `tokio/src/fs/remove_dir_all.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `remove_dir_all` 🅰 |  | Public API | Data movement | Removes a directory at this path, after removing all its contents. |

## `tokio/src/fs/remove_file.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `remove_file` 🅰 |  | Public API | Data movement | Removes a file from the filesystem. |

## `tokio/src/fs/rename.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `rename` 🅰 |  | Public API | Async operation | Renames a file or directory to a new name, replacing the original file if `to` already exists. |
| 44 | `rename_blocking` 🅰 |  | Private helper | Async operation |  |

## `tokio/src/fs/set_permissions.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `set_permissions` 🅰 |  | Public API | Configuration / setter | Changes the permissions found on a file or a directory. |

## `tokio/src/fs/symlink.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `symlink` 🅰 |  | Public API | Async operation | Creates a new symbolic link on the filesystem. |

## `tokio/src/fs/symlink_dir.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `symlink_dir` 🅰 |  | Public API | Async operation | Creates a new directory symlink on the filesystem. |

## `tokio/src/fs/symlink_file.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `symlink_file` 🅰 |  | Public API | Async operation | Creates a new file symbolic link on the filesystem. |

## `tokio/src/fs/symlink_metadata.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `symlink_metadata` 🅰 |  | Public API | Async operation | Queries the file system metadata for a path. |

## `tokio/src/fs/try_exists.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 25 | `try_exists` 🅰 |  | Public API | Non-blocking attempt | Returns `Ok(true)` if the path points at an existing entity. |
| 74 | `try_exists_uring` 🅰 |  | Private helper | Non-blocking attempt |  |
| 85 | `try_exists_spawn_blocking` 🅰 |  | Private helper | Non-blocking attempt |  |

## `tokio/src/fs/write.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `write` 🅰 |  | Public API | I/O operation | Creates a future that will open a file for writing and write the entire contents of `contents` to it. |
| 60 | `write_uring` 🅰 |  | Private helper | I/O operation |  |
| 98 | `write_spawn_blocking` 🅰 |  | Private helper | I/O operation |  |

