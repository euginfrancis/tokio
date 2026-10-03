# `tokio::process::unix` — 97 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 43 |
| Test | 28 |
| Crate-internal | 15 |
| Private helper | 8 |
| Trait method (declaration/default) | 3 |

## `tokio/src/process/unix/mod.rs` (39)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 52 | `id`  | `Wait for StdChild` | Trait impl | Accessor / query |  |
| 56 | `try_wait`  | `Wait for StdChild` | Trait impl | Non-blocking attempt |  |
| 62 | `kill`  | `Kill for StdChild` | Trait impl | Runtime/task control |  |
| 68 | `get_orphan_queue`  |  | Private helper | Accessor / query |  |
| 78 | `get_orphan_queue`  |  | Private helper | Accessor / query |  |
| 88 | `fmt`  | `fmt::Debug for GlobalOrphanQueue` | Trait impl | Formatting |  |
| 94 | `reap_orphans`  | `GlobalOrphanQueue` | Crate-internal | Other / internal logic |  |
| 100 | `push_orphan`  | `OrphanQueue<StdChild> for GlobalOrphanQueue` | Trait impl | Data movement |  |
| 113 | `fmt`  | `fmt::Debug for Child` | Trait impl | Formatting |  |
| 118 | `build_child`  |  | Crate-internal | Constructor |  |
| 148 | `id`  | `Child` | Crate-internal | Accessor / query |  |
| 156 | `std_child`  | `Child` | Private helper | Other / internal logic |  |
| 164 | `try_wait`  | `Child` | Crate-internal | Non-blocking attempt |  |
| 170 | `kill`  | `Kill for Child` | Trait impl | Runtime/task control |  |
| 178 | `poll`  | `Future for Child` | Trait impl | Future impl (poll) |  |
| 195 | `from`  | `From<T> for Pipe` | Trait impl | Conversion |  |
| 202 | `read`  | `io::Read for &Pipe` | Trait impl | I/O operation |  |
| 208 | `write`  | `io::Write for &Pipe` | Trait impl | I/O operation |  |
| 212 | `flush`  | `io::Write for &Pipe` | Trait impl | I/O operation |  |
| 216 | `write_vectored`  | `io::Write for &Pipe` | Trait impl | I/O operation |  |
| 222 | `as_raw_fd`  | `AsRawFd for Pipe` | Trait impl | OS handle access |  |
| 228 | `as_fd`  | `AsFd for Pipe` | Trait impl | OS handle access |  |
| 233 | `convert_to_blocking_file`  |  | Private helper | Other / internal logic |  |
| 245 | `convert_to_stdio`  |  | Crate-internal | Other / internal logic |  |
| 250 | `register`  | `Source for Pipe` | Trait impl | I/O registration |  |
| 259 | `reregister`  | `Source for Pipe` | Trait impl | Other / internal logic |  |
| 268 | `deregister`  | `Source for Pipe` | Trait impl | I/O registration |  |
| 278 | `into_owned_fd`  | `ChildStdio` | Crate-internal | Conversion |  |
| 284 | `fmt`  | `fmt::Debug for ChildStdio` | Trait impl | Formatting |  |
| 290 | `as_raw_fd`  | `AsRawFd for ChildStdio` | Trait impl | OS handle access |  |
| 296 | `as_fd`  | `AsFd for ChildStdio` | Trait impl | OS handle access |  |
| 302 | `poll_write`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 310 | `poll_flush`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 314 | `poll_shutdown`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 318 | `poll_write_vectored`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 326 | `is_write_vectored`  | `AsyncWrite for ChildStdio` | Trait impl | I/O trait impl |  |
| 332 | `poll_read`  | `AsyncRead for ChildStdio` | Trait impl | I/O trait impl |  |
| 342 | `set_nonblocking`  |  | Private helper | Configuration / setter |  |
| 365 | `stdio`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/process/unix/orphan.rs` (23)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `id`  | `trait Wait` | Trait method (declaration/default) | Accessor / query | Get the identifier for this process or diagnostics. |
| 14 | `try_wait`  | `trait Wait` | Trait method (declaration/default) | Non-blocking attempt | Try waiting for a process to exit in a non-blocking manner. |
| 18 | `id`  | `Wait for &mut T` | Trait impl | Accessor / query |  |
| 22 | `try_wait`  | `Wait for &mut T` | Trait impl | Non-blocking attempt |  |
| 30 | `push_orphan`  | `trait OrphanQueue` | Trait method (declaration/default) | Data movement | Adds an orphan to the queue. |
| 34 | `push_orphan`  | `OrphanQueue<T> for &O` | Trait impl | Data movement |  |
| 48 | `new`  | `OrphanQueueImpl<T>` | Crate-internal | Constructor |  |
| 57 | `new` 🅲 | `OrphanQueueImpl<T>` | Crate-internal | Constructor |  |
| 66 | `len`  | `OrphanQueueImpl<T>` | Test | Accessor / query |  |
| 70 | `push_orphan`  | `OrphanQueueImpl<T>` | Crate-internal | Data movement |  |
| 79 | `reap_orphans`  | `OrphanQueueImpl<T>` | Crate-internal | Other / internal logic | Attempts to reap every process in the queue, ignoring any errors and enqueueing any orphans which have not yet exited. |
| 113 | `drain_orphan_queue`  |  | Private helper | Combinator / iteration |  |
| 149 | `new`  | `MockQueue<W>` | Test | Constructor |  |
| 157 | `push_orphan`  | `OrphanQueue<W> for MockQueue<W>` | Test | Data movement |  |
| 169 | `new`  | `MockWait` | Test | Constructor |  |
| 177 | `with_err`  | `MockWait` | Test | Constructor |  |
| 187 | `id`  | `Wait for MockWait` | Test | Accessor / query |  |
| 191 | `try_wait`  | `Wait for MockWait` | Test | Non-blocking attempt |  |
| 210 | `drain_attempts_a_single_reap_of_all_queued_orphans`  |  | Test | Combinator / iteration |  |
| 255 | `no_reap_if_no_signal_received`  |  | Test | Other / internal logic |  |
| 279 | `no_reap_if_signal_lock_held`  |  | Test | Other / internal logic |  |
| 297 | `does_not_register_signal_if_queue_empty`  |  | Test | Other / internal logic |  |
| 319 | `does_nothing_if_signal_could_not_be_registered`  |  | Test | Other / internal logic |  |

## `tokio/src/process/unix/pidfd_reaper.rs` (18)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `open`  | `Pidfd` | Private helper | Constructor |  |
| 59 | `as_raw_fd`  | `AsRawFd for Pidfd` | Trait impl | OS handle access |  |
| 65 | `register`  | `Source for Pidfd` | Trait impl | I/O registration |  |
| 74 | `reregister`  | `Source for Pidfd` | Trait impl | Other / internal logic |  |
| 83 | `deregister`  | `Source for Pidfd` | Trait impl | I/O registration |  |
| 103 | `poll`  | `Future for PidfdReaperInner<W>` | Trait impl | Future impl (poll) |  |
| 141 | `deref`  | `Deref for PidfdReaper<W, Q>` | Trait impl | Deref |  |
| 151 | `new`  | `PidfdReaper<W, Q>` | Crate-internal | Constructor |  |
| 165 | `inner_mut`  | `PidfdReaper<W, Q>` | Crate-internal | Other / internal logic |  |
| 177 | `poll`  | `Future for PidfdReaper<W, Q>` | Trait impl | Future impl (poll) |  |
| 193 | `kill`  | `Kill for PidfdReaper<W, Q>` | Trait impl | Runtime/task control |  |
| 203 | `drop`  | `Drop for PidfdReaper<W, Q>` | Trait impl | Drop / cleanup |  |
| 222 | `create_runtime`  |  | Test | Constructor |  |
| 229 | `run_test`  |  | Test | Runtime/task control |  |
| 233 | `is_pidfd_available`  |  | Test | Accessor / query |  |
| 251 | `test_pidfd_reaper_poll`  |  | Test | Other / internal logic |  |
| 271 | `test_pidfd_reaper_kill`  |  | Test | Other / internal logic |  |
| 293 | `test_pidfd_reaper_drop`  |  | Test | Other / internal logic |  |

## `tokio/src/process/unix/reap.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 33 | `deref`  | `Deref for Reaper<W, Q, S>` | Trait impl | Deref |  |
| 43 | `new`  | `Reaper<W, Q, S>` | Crate-internal | Constructor |  |
| 51 | `inner`  | `Reaper<W, Q, S>` | Private helper | Handle / reference plumbing |  |
| 55 | `inner_mut`  | `Reaper<W, Q, S>` | Crate-internal | Other / internal logic |  |
| 68 | `poll`  | `Future for Reaper<W, Q, S>` | Trait impl | Future impl (poll) |  |
| 112 | `kill`  | `Kill for Reaper<W, Q, S>` | Trait impl | Runtime/task control |  |
| 122 | `drop`  | `Drop for Reaper<W, Q, S>` | Trait impl | Drop / cleanup |  |
| 152 | `new`  | `MockWait` | Test | Constructor |  |
| 163 | `id`  | `Wait for MockWait` | Test | Accessor / query |  |
| 167 | `try_wait`  | `Wait for MockWait` | Test | Non-blocking attempt |  |
| 180 | `kill`  | `Kill for MockWait` | Test | Runtime/task control |  |
| 192 | `new`  | `MockStream` | Test | Constructor |  |
| 201 | `poll_recv`  | `InternalStream for MockStream` | Test | Poll function |  |
| 211 | `reaper`  |  | Test | Other / internal logic |  |
| 250 | `kill`  |  | Test | Runtime/task control |  |
| 264 | `drop_reaps_if_possible`  |  | Test | Lifecycle / ref-count |  |
| 283 | `drop_enqueues_orphan_if_wait_fails`  |  | Test | Lifecycle / ref-count |  |

