# `tokio::runtime::tests` — 113 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 113 |

## `tokio/src/runtime/tests/inject.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `push_and_pop`  |  | Test | Data movement |  |
| 26 | `push_batch_and_pop`  |  | Test | Data movement |  |
| 37 | `pop_n_drains_on_drop`  |  | Test | Data movement |  |

## `tokio/src/runtime/tests/loom_blocking.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `blocking_shutdown`  |  | Test | Blocking (sync) variant |  |
| 28 | `spawn_mandatory_blocking_should_always_run`  |  | Test | Runtime/task control |  |
| 49 | `spawn_mandatory_blocking_should_run_even_when_shutting_down_from_other_thread`  |  | Test | Runtime/task control |  |
| 78 | `mandatory_blocking_io_write_should_always_run`  |  | Test | Other / internal logic |  |
| 87 | `write`  | `io::Write for Writer` | Test | I/O operation |  |
| 94 | `flush`  | `io::Write for Writer` | Test | I/O operation |  |
| 118 | `spawn_blocking_when_paused`  |  | Test | Runtime/task control |  |
| 139 | `spawn_blocking_then_shutdown`  |  | Test | Runtime/task control | See <https://github.com/tokio-rs/tokio/pull/7922> |
| 180 | `spawn_blocking_at_thread_cap_runs`  |  | Test | Runtime/task control | Regression-style test for the class of bug behind <https://github.com/tokio-rs/tokio/issues/8056>: a `spawn_blocking` while the pool is at its thread cap must not be stranded when it races with the on |
| 208 | `spawn_blocking_racing_shutdown_resolves`  |  | Test | Runtime/task control | A `spawn_blocking` racing runtime shutdown must never strand the task: its `JoinHandle` must resolve (the task ran or was cancelled) no matter how the spawn interleaves with shutdown's drain. |
| 225 | `mk_runtime`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/tests/loom_current_thread.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `assert_at_most_num_polls`  |  | Test | Debugging / tracing |  |
| 37 | `block_on_num_polls`  |  | Test | Runtime/task control |  |
| 71 | `assert_no_unnecessary_polls`  |  | Test | Debugging / tracing |  |
| 110 | `drop_jh_during_schedule`  |  | Test | Lifecycle / ref-count |  |
| 111 | `waker_clone` ⚠ |  | Test | Wake / park |  |
| 116 | `waker_drop` ⚠ |  | Test | Wake / park |  |
| 120 | `waker_nop` ⚠ |  | Test | Wake / park |  |
| 171 | `poll`  | `Future for BlockedFuture` | Test | Future impl (poll) |  |
| 189 | `poll`  | `Future for ResetFuture` | Test | Future impl (poll) |  |

## `tokio/src/runtime/tests/loom_join_set.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 5 | `test_join_set`  |  | Test | Other / internal logic |  |
| 37 | `abort_all_during_completion`  |  | Test | Lifecycle / ref-count |  |

## `tokio/src/runtime/tests/loom_local.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 16 | `wake_during_shutdown`  |  | Test | Wake / park | Waking a runtime will attempt to push a task into a queue of notifications in the runtime, however the tasks in such a queue usually have a reference to the runtime itself. |

## `tokio/src/runtime/tests/loom_multi_thread.rs` (25)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 36 | `new`  | `AtomicTake<T>` | Test | Constructor |  |
| 43 | `take`  | `AtomicTake<T>` | Test | Data movement |  |
| 54 | `drop`  | `Drop for AtomicTake<T>` | Test | Drop / cleanup |  |
| 65 | `new`  | `AtomicOneshot<T>` | Test | Constructor |  |
| 71 | `assert_send`  | `AtomicOneshot<T>` | Test | Debugging / tracing |  |
| 81 | `racy_shutdown`  |  | Test | Other / internal logic |  |
| 103 | `pool_multi_spawn`  |  | Test | Other / internal logic |  |
| 135 | `only_blocking_inner`  |  | Test | Other / internal logic |  |
| 155 | `only_blocking_without_pending`  |  | Test | Other / internal logic |  |
| 160 | `only_blocking_with_pending`  |  | Test | Other / internal logic |  |
| 168 | `blocking_and_regular_inner`  |  | Test | Blocking (sync) variant |  |
| 206 | `blocking_and_regular`  |  | Test | Blocking (sync) variant |  |
| 211 | `blocking_and_regular_with_pending`  |  | Test | Blocking (sync) variant |  |
| 216 | `join_output`  |  | Test | Other / internal logic |  |
| 230 | `poll_drop_handle_then_drop`  |  | Test | Poll function |  |
| 247 | `complete_block_on_under_load`  |  | Test | Runtime/task control |  |
| 265 | `shutdown_with_notification`  |  | Test | Runtime/task control |  |
| 295 | `pool_shutdown`  |  | Test | Other / internal logic |  |
| 316 | `pool_multi_notify`  |  | Test | Other / internal logic |  |
| 350 | `mk_pool`  |  | Test | Other / internal logic |  |
| 359 | `gated2`  |  | Test | Other / internal logic |  |
| 396 | `multi_gated` 🅰 |  | Test | Async operation |  |
| 428 | `track`  |  | Test | Other / internal logic |  |
| 445 | `into_inner`  | `Track<T>` | Test | Conversion |  |
| 453 | `poll`  | `Future for Track<T>` | Test | Future impl (poll) |  |

## `tokio/src/runtime/tests/loom_oneshot.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `channel`  |  | Test | Constructor |  |
| 32 | `send`  | `Sender<T>` | Test | Data movement |  |
| 39 | `recv`  | `Receiver<T>` | Test | Data movement |  |

## `tokio/src/runtime/tests/mod.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `release`  | `task::Schedule for NoopSchedule` | Test | Scheduler hook |  |
| 19 | `schedule`  | `task::Schedule for NoopSchedule` | Test | Scheduler hook |  |
| 23 | `hooks`  | `task::Schedule for NoopSchedule` | Test | Scheduler hook |  |
| 37 | `unowned`  |  | Test | Other / internal logic |  |
| 52 | `unowned`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/tests/queue.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `new_stats`  |  | Test | Constructor |  |
| 32 | `fits_256_one_at_a_time`  |  | Test | Other / internal logic |  |
| 52 | `fits_256_all_at_once`  |  | Test | Other / internal logic |  |
| 69 | `fits_256_all_in_chunks`  |  | Test | Other / internal logic |  |
| 90 | `overflow`  |  | Test | Other / internal logic |  |
| 116 | `steal_batch`  |  | Test | Data movement |  |
| 147 | `normal_or_miri` 🅲 |  | Test | Other / internal logic |  |
| 156 | `stress1`  |  | Test | Other / internal logic |  |
| 225 | `stress2`  |  | Test | Other / internal logic |  |

## `tokio/src/runtime/tests/task.rs` (34)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 19 | `assert_dropped`  | `AssertDropHandle` | Test | Debugging / tracing |  |
| 24 | `assert_not_dropped`  | `AssertDropHandle` | Test | Debugging / tracing |  |
| 33 | `new`  | `AssertDrop` | Test | Constructor |  |
| 46 | `drop`  | `Drop for AssertDrop` | Test | Drop / cleanup |  |
| 54 | `create_drop1`  |  | Test | Constructor |  |
| 72 | `create_drop2`  |  | Test | Constructor |  |
| 90 | `drop_abort_handle1`  |  | Test | Lifecycle / ref-count |  |
| 111 | `drop_abort_handle2`  |  | Test | Lifecycle / ref-count |  |
| 132 | `drop_abort_handle_clone`  |  | Test | Lifecycle / ref-count |  |
| 157 | `create_shutdown1`  |  | Test | Constructor |  |
| 175 | `create_shutdown2`  |  | Test | Constructor |  |
| 193 | `unowned_poll`  |  | Test | Other / internal logic |  |
| 199 | `schedule`  |  | Test | Runtime/task control |  |
| 211 | `shutdown`  |  | Test | Runtime/task control |  |
| 226 | `shutdown_immediately`  |  | Test | Runtime/task control |  |
| 240 | `spawn_niche_in_task`  |  | Test | Runtime/task control |  |
| 270 | `new`  | `Subscriber` | Test | Constructor |  |
| 278 | `wait` 🅰 | `Subscriber` | Test | Runtime/task control |  |
| 296 | `new`  | `State` | Test | Constructor |  |
| 303 | `poll_update`  | `State` | Test | Poll function |  |
| 323 | `set_version`  | `State` | Test | Configuration / setter |  |
| 333 | `spawn_during_shutdown`  |  | Test | Runtime/task control |  |
| 338 | `drop`  | `Drop for SpawnOnDrop` | Test | Drop / cleanup |  |
| 361 | `with`  |  | Test | Combinator / iteration |  |
| 365 | `drop`  | `Drop for Reset` | Test | Drop / cleanup |  |
| 399 | `spawn`  | `Runtime` | Test | Runtime/task control |  |
| 416 | `tick`  | `Runtime` | Test | Time / timers |  |
| 420 | `tick_max`  | `Runtime` | Test | Time / timers |  |
| 433 | `is_empty`  | `Runtime` | Test | Accessor / query |  |
| 437 | `next_task`  | `Runtime` | Test | Other / internal logic |  |
| 441 | `shutdown`  | `Runtime` | Test | Runtime/task control |  |
| 456 | `release`  | `Schedule for Runtime` | Test | Scheduler hook |  |
| 460 | `schedule`  | `Schedule for Runtime` | Test | Scheduler hook |  |
| 464 | `hooks`  | `Schedule for Runtime` | Test | Scheduler hook |  |

## `tokio/src/runtime/tests/task_combinations.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 69 | `test_combinations`  |  | Test | Other / internal logic |  |
| 154 | `is_debug`  |  | Test | Accessor / query |  |
| 157 | `test_combination`  |  | Test | Other / internal logic |  |
| 207 | `new`  | `Rt` | Test | Constructor |  |
| 227 | `block_on`  | `Rt` | Test | Runtime/task control |  |
| 236 | `spawn`  | `Rt` | Test | Runtime/task control |  |
| 254 | `disarm`  | `Output` | Test | Other / internal logic |  |
| 259 | `drop`  | `Drop for Output` | Test | Drop / cleanup |  |
| 275 | `poll`  | `Future for FutWrapper<F>` | Test | Future impl (poll) |  |
| 284 | `drop`  | `Drop for FutWrapper<F>` | Test | Drop / cleanup |  |
| 300 | `my_task` 🅰 |  | Test | Async operation |  |

