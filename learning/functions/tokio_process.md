# `tokio::process` — 94 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 37 |
| Trait impl | 28 |
| Inside macro_rules! | 9 |
| Test | 8 |
| Crate-internal | 6 |
| Private helper | 5 |
| Trait method (declaration/default) | 1 |

## `tokio/src/process/kill.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 6 | `kill`  | `trait Kill` | Trait method (declaration/default) | Runtime/task control | Forcefully kills the process. |
| 10 | `kill`  | `Kill for &mut T` | Trait impl | Runtime/task control |  |

## `tokio/src/process/mod.rs` (70)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 317 | `new`  | `Command` | Public API | Constructor | Constructs a new `Command` for launching the program at path `program`, with the following default configuration: * No arguments to the program * Inherit the current process's environment * Inherit th |
| 323 | `as_std`  | `Command` | Public API | Conversion | Cheaply convert to a `&std::process::Command` for places where the type from the standard library is expected. |
| 329 | `as_std_mut`  | `Command` | Public API | Conversion | Cheaply convert to a `&mut std::process::Command` for places where the type from the standard library is expected. |
| 338 | `into_std`  | `Command` | Public API | Conversion | Cheaply convert into a `std::process::Command`. |
| 382 | `arg`  | `Command` | Public API | Other / internal logic | Adds an argument to pass to the program. |
| 406 | `args`  | `Command` | Public API | Other / internal logic | Adds multiple arguments to pass to the program. |
| 420 | `raw_arg`  | `Command` | Public API | Other / internal logic | Append literal text to the command line without any quoting or escaping. |
| 444 | `env`  | `Command` | Public API | Other / internal logic | Inserts or updates an environment variable mapping. |
| 479 | `envs`  | `Command` | Public API | Other / internal logic | Adds or updates multiple environment variable mappings. |
| 504 | `env_remove`  | `Command` | Public API | Other / internal logic | Removes an environment variable mapping. |
| 524 | `env_clear`  | `Command` | Public API | Other / internal logic | Clears the entire environment map for the child process. |
| 554 | `current_dir`  | `Command` | Public API | Other / internal logic | Sets the working directory for the child process. |
| 579 | `stdin`  | `Command` | Public API | Other / internal logic | Sets configuration for the child process's standard input (stdin) handle. |
| 606 | `stdout`  | `Command` | Public API | Other / internal logic | Sets configuration for the child process's standard output (stdout) handle. |
| 633 | `stderr`  | `Command` | Public API | Other / internal logic | Sets configuration for the child process's standard error (stderr) handle. |
| 664 | `kill_on_drop`  | `Command` | Public API | Other / internal logic | Controls whether a `kill` operation should be invoked on a spawned child process when its corresponding `Child` handle is dropped. |
| 675 | `creation_flags`  | `Command` | Public API | Other / internal logic | Sets the [process creation flags][1] to be passed to `CreateProcess`. |
| 686 | `uid`  | `Command` | Public API | Other / internal logic | Sets the child process's user ID. |
| 697 | `gid`  | `Command` | Public API | Other / internal logic | Similar to `uid` but sets the group ID of the child process. |
| 710 | `arg0`  | `Command` | Public API | Other / internal logic | Sets executable argument. |
| 749 | `pre_exec` ⚠ | `Command` | Public API | Other / internal logic | Schedules a closure to be run just before the `exec` function is invoked. |
| 790 | `process_group`  | `Command` | Public API | Runtime/task control | Sets the process group ID (PGID) of the child process. |
| 863 | `spawn`  | `Command` | Public API | Runtime/task control | Executes the command as a child process, returning a handle to it. |
| 934 | `spawn_with`  | `Command` | Public API | Runtime/task control | Executes the command as a child process with a custom spawning function, returning a handle to it. |
| 950 | `build_child`  | `Command` | Private helper | Constructor | Small indirection for the spawn implementations. |
| 1002 | `status`  | `Command` | Public API | Other / internal logic | Executes the command as a child process, waiting for it to finish and collecting its exit status. |
| 1065 | `output`  | `Command` | Public API | Other / internal logic | Executes the command as a child process, waiting for it to finish and collecting all of its output. |
| 1090 | `get_kill_on_drop`  | `Command` | Public API | Accessor / query | Returns the boolean value that was previously set by [`Command::kill_on_drop`]. |
| 1096 | `from`  | `From<StdCommand> for Command` | Trait impl | Conversion |  |
| 1112 | `kill`  | `Kill for ChildDropGuard<T>` | Trait impl | Runtime/task control |  |
| 1124 | `drop`  | `Drop for ChildDropGuard<T>` | Trait impl | Drop / cleanup |  |
| 1137 | `poll`  | `Future for ChildDropGuard<F>` | Trait impl | Future impl (poll) |  |
| 1222 | `id`  | `Child` | Public API | Accessor / query | Returns the OS-assigned process identifier associated with this child while it is still running. |
| 1232 | `raw_handle`  | `Child` | Public API | Other / internal logic | Extracts the raw handle of the process associated with this child while it is still running. |
| 1247 | `start_kill`  | `Child` | Public API | Runtime/task control | Attempts to force the child to exit, but does not wait for the request to take effect. |
| 1326 | `kill` 🅰 | `Child` | Public API | Runtime/task control | Forces the child to exit. |
| 1379 | `wait` 🅰 | `Child` | Public API | Runtime/task control | Waits for the child to exit completely, returning the status that it exited with. |
| 1413 | `try_wait`  | `Child` | Public API | Non-blocking attempt | Attempts to collect the exit status of the child if it has already exited. |
| 1446 | `wait_with_output` 🅰 | `Child` | Public API | Runtime/task control | Returns a future that will resolve to an `Output`, containing the exit status, stdout, and stderr of the child process. |
| 1449 | `read_to_end` 🅰 |  | Private helper | I/O operation |  |
| 1512 | `from_std`  | `ChildStdin` | Public API | Conversion | Creates an asynchronous `ChildStdin` from a synchronous one. |
| 1527 | `from_std`  | `ChildStdout` | Public API | Conversion | Creates an asynchronous `ChildStdout` from a synchronous one. |
| 1542 | `from_std`  | `ChildStderr` | Public API | Conversion | Creates an asynchronous `ChildStderr` from a synchronous one. |
| 1550 | `poll_write`  | `AsyncWrite for ChildStdin` | Trait impl | I/O trait impl |  |
| 1558 | `poll_flush`  | `AsyncWrite for ChildStdin` | Trait impl | I/O trait impl |  |
| 1562 | `poll_shutdown`  | `AsyncWrite for ChildStdin` | Trait impl | I/O trait impl |  |
| 1566 | `poll_write_vectored`  | `AsyncWrite for ChildStdin` | Trait impl | I/O trait impl |  |
| 1574 | `is_write_vectored`  | `AsyncWrite for ChildStdin` | Trait impl | I/O trait impl |  |
| 1580 | `poll_read`  | `AsyncRead for ChildStdout` | Trait impl | I/O trait impl |  |
| 1590 | `poll_read`  | `AsyncRead for ChildStderr` | Trait impl | I/O trait impl |  |
| 1602 | `try_into`  | `TryInto<Stdio> for ChildStdin` | Trait impl | Non-blocking attempt |  |
| 1610 | `try_into`  | `TryInto<Stdio> for ChildStdout` | Trait impl | Non-blocking attempt |  |
| 1618 | `try_into`  | `TryInto<Stdio> for ChildStderr` | Trait impl | Non-blocking attempt |  |
| 1637 | `into_owned_fd`  | `$type` | Inside macro_rules! | Conversion | Convert into [`OwnedFd`]. |
| 1643 | `as_raw_fd`  | `AsRawFd for $type` | Inside macro_rules! | OS handle access |  |
| 1649 | `as_fd`  | `AsFd for $type` | Inside macro_rules! | OS handle access |  |
| 1672 | `into_owned_handle`  | `$type` | Inside macro_rules! | Conversion | Convert into [`OwnedHandle`]. |
| 1678 | `as_raw_handle`  | `AsRawHandle for $type` | Inside macro_rules! | OS handle access |  |
| 1684 | `as_handle`  | `AsHandle for $type` | Inside macro_rules! | OS handle access |  |
| 1696 | `into_owned_handle`  | `$type` | Inside macro_rules! | Conversion | Convert into [`OwnedHandle`]. |
| 1702 | `as_raw_handle`  | `AsRawHandle for $type` | Inside macro_rules! | OS handle access |  |
| 1708 | `as_handle`  | `AsHandle for $type` | Inside macro_rules! | OS handle access |  |
| 1738 | `new`  | `Mock` | Test | Constructor |  |
| 1742 | `with_result`  | `Mock` | Test | Constructor |  |
| 1752 | `kill`  | `Kill for Mock` | Test | Runtime/task control |  |
| 1761 | `poll`  | `Future for Mock` | Test | Future impl (poll) |  |
| 1769 | `kills_on_drop_if_specified`  |  | Test | Other / internal logic |  |
| 1785 | `no_kill_on_drop_by_default`  |  | Test | Other / internal logic |  |
| 1801 | `no_kill_if_already_killed`  |  | Test | Other / internal logic |  |
| 1818 | `no_kill_if_reaped`  |  | Test | Other / internal logic |  |

## `tokio/src/process/windows.rs` (22)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 50 | `fmt`  | `fmt::Debug for Child` | Trait impl | Formatting |  |
| 68 | `build_child`  |  | Crate-internal | Constructor |  |
| 85 | `id`  | `Child` | Crate-internal | Accessor / query |  |
| 89 | `try_wait`  | `Child` | Crate-internal | Non-blocking attempt |  |
| 95 | `kill`  | `Kill for Child` | Trait impl | Runtime/task control |  |
| 103 | `poll`  | `Future for Child` | Trait impl | Future impl (poll) |  |
| 147 | `as_raw_handle`  | `AsRawHandle for Child` | Trait impl | OS handle access |  |
| 153 | `drop`  | `Drop for Waiting` | Trait impl | Drop / cleanup |  |
| 164 | `callback` ⚠ |  | Private helper | Other / internal logic |  |
| 173 | `read`  | `io::Read for ArcFile` | Trait impl | I/O operation |  |
| 179 | `write`  | `io::Write for ArcFile` | Trait impl | I/O operation |  |
| 183 | `flush`  | `io::Write for ArcFile` | Trait impl | I/O operation |  |
| 197 | `into_owned_handle`  | `ChildStdio` | Crate-internal | Conversion |  |
| 203 | `as_raw_handle`  | `AsRawHandle for ChildStdio` | Trait impl | OS handle access |  |
| 209 | `poll_read`  | `AsyncRead for ChildStdio` | Trait impl | I/O trait impl |  |
| 219 | `poll_write`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 227 | `poll_flush`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 231 | `poll_shutdown`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 236 | `stdio`  |  | Crate-internal | Other / internal logic |  |
| 251 | `convert_to_file`  |  | Private helper | Other / internal logic |  |
| 258 | `convert_to_stdio`  |  | Crate-internal | Other / internal logic |  |
| 262 | `duplicate_handle`  |  | Private helper | Other / internal logic |  |

