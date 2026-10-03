# `tokio::runtime::blocking` — 59 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 33 |
| Private helper | 18 |
| Trait impl | 8 |

## `tokio/src/runtime/blocking/mod.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 26 | `create_blocking_pool`  |  | Crate-internal | Constructor |  |

## `tokio/src/runtime/blocking/pool.rs` (41)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `num_threads`  | `SpawnerMetrics` | Crate-internal | Accessor / query |  |
| 42 | `num_idle_threads`  | `SpawnerMetrics` | Crate-internal | Accessor / query |  |
| 47 | `queue_depth`  | `SpawnerMetrics` | Private helper | Metrics / counters |  |
| 52 | `inc_num_threads`  | `SpawnerMetrics` | Private helper | Metrics / counters |  |
| 56 | `dec_num_threads`  | `SpawnerMetrics` | Crate-internal | Metrics / counters |  |
| 60 | `inc_num_idle_threads`  | `SpawnerMetrics` | Crate-internal | Metrics / counters |  |
| 64 | `dec_num_idle_threads`  | `SpawnerMetrics` | Crate-internal | Metrics / counters |  |
| 68 | `inc_queue_depth`  | `SpawnerMetrics` | Crate-internal | Metrics / counters |  |
| 72 | `dec_queue_depth`  | `SpawnerMetrics` | Crate-internal | Metrics / counters |  |
| 156 | `begin_shutdown`  | `ThreadManagementState` | Crate-internal | Runtime/task control | Flag the pool as shutting down and hand back the worker `JoinHandle`s to join. |
| 172 | `worker_timed_out`  | `ThreadManagementState` | Crate-internal | Metrics / counters | Bookkeeping for a worker exiting on its keep-alive timeout: leaves its own handle for the next timed-out worker (or shutdown) to join, and returns the previous timed-out thread's handle, which the cal |
| 202 | `from`  | `From<SpawnError> for io::Error` | Trait impl | Conversion |  |
| 211 | `new`  | `Task` | Crate-internal | Constructor |  |
| 215 | `shutdown`  | `Task` | Crate-internal | Runtime/task control |  |
| 219 | `run`  | `Task` | Crate-internal | Runtime/task control |  |
| 223 | `shutdown_or_run_if_mandatory`  | `Task` | Crate-internal | Runtime/task control |  |
| 238 | `spawn_blocking`  |  | Crate-internal | Runtime/task control | Runs the provided function on an executor dedicated to blocking operations. |
| 257 | `spawn_mandatory_blocking`  |  | Crate-internal | Runtime/task control | Runs the provided function on an executor dedicated to blocking operations. |
| 270 | `new`  | `BlockingPool` | Crate-internal | Constructor |  |
| 310 | `spawner`  | `BlockingPool` | Crate-internal | Runtime/task control |  |
| 314 | `shutdown`  | `BlockingPool` | Crate-internal | Runtime/task control |  |
| 344 | `drop`  | `Drop for BlockingPool` | Trait impl | Drop / cleanup |  |
| 350 | `fmt`  | `fmt::Debug for BlockingPool` | Trait impl | Formatting |  |
| 359 | `spawn_blocking`  | `Spawner` | Crate-internal | Runtime/task control |  |
| 398 | `spawn_mandatory_blocking`  | `Spawner` | Crate-internal | Runtime/task control |  |
| 429 | `spawn_blocking_inner`  | `Spawner` | Crate-internal | Runtime/task control |  |
| 455 | `num_blocking_threads`  | `Spawner` | Crate-internal | Accessor / query |  |
| 462 | `spawn_task`  | `Spawner` | Private helper | Runtime/task control |  |
| 508 | `spawn_thread`  | `Spawner` | Private helper | Runtime/task control |  |
| 533 | `num_idle_threads`  | `Spawner` | Crate-internal | Accessor / query |  |
| 537 | `queue_depth`  | `Spawner` | Crate-internal | Metrics / counters |  |
| 549 | `spawn_task`  | `InnerImpl` | Private helper | Runtime/task control |  |
| 564 | `run_worker`  | `InnerImpl` | Private helper | Runtime/task control |  |
| 576 | `begin_shutdown`  | `InnerImpl` | Private helper | Runtime/task control |  |
| 589 | `new`  | `LockedImpl` | Private helper | Constructor |  |
| 603 | `spawn_task`  | `LockedImpl` | Private helper | Runtime/task control | Push a task and either notify an idle worker or invoke `on_no_idle` (which is responsible for spawning a new worker if possible). |
| 642 | `run_worker`  | `LockedImpl` | Private helper | Runtime/task control | Run a worker thread's main loop. |
| 740 | `begin_shutdown`  | `LockedImpl` | Private helper | Runtime/task control | Begin pool shutdown: set the shutdown flag, drop the shutdown sender, wake all waiting workers, and hand back the worker `JoinHandle`s for the caller to join. |
| 750 | `is_temporary_os_thread_error`  |  | Private helper | Accessor / query |  |
| 755 | `run`  | `Inner` | Private helper | Runtime/task control |  |
| 775 | `fmt`  | `fmt::Debug for Spawner` | Trait impl | Formatting |  |

## `tokio/src/runtime/blocking/schedule.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 20 | `new`  | `BlockingSchedule` | Crate-internal | Constructor |  |
| 42 | `release`  | `task::Schedule for BlockingSchedule` | Trait impl | Scheduler hook |  |
| 57 | `schedule`  | `task::Schedule for BlockingSchedule` | Trait impl | Scheduler hook |  |
| 61 | `hooks`  | `task::Schedule for BlockingSchedule` | Trait impl | Scheduler hook |  |

## `tokio/src/runtime/blocking/sharded.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 73 | `new`  | `ShardedImpl` | Crate-internal | Constructor |  |
| 96 | `push_shard_index`  | `ShardedImpl` | Private helper | Data movement | Pick a shard to push to. |
| 104 | `push_shard_index`  | `ShardedImpl` | Private helper | Data movement | Under loom the RNG would make each execution take a different path, breaking loom's requirement that executions be deterministic, so use round-robin selection instead. |
| 114 | `push`  | `ShardedImpl` | Private helper | Data movement | Push a task onto one of the shards, or hand it back if the chosen shard has been sealed for shutdown. |
| 129 | `pop`  | `ShardedImpl` | Private helper | Data movement | Pop a task, checking the worker's preferred shard first. |
| 165 | `drain_and_seal`  | `ShardedImpl` | Private helper | Combinator / iteration | Drain every shard, sealing each so that later pushes are rejected, and run-or-cancel the collected tasks. |
| 186 | `spawn_task`  | `ShardedImpl` | Crate-internal | Runtime/task control | Push a task and either notify an idle worker or invoke `on_no_idle` (which is responsible for spawning a new worker if possible). |
| 238 | `run_worker`  | `ShardedImpl` | Crate-internal | Runtime/task control | Run a worker thread's main loop. |
| 336 | `begin_shutdown`  | `ShardedImpl` | Crate-internal | Runtime/task control | Begin pool shutdown: set the shutdown flag, drop the shutdown sender, wake all waiting workers, and hand back the worker `JoinHandle`s for the caller to join. |

## `tokio/src/runtime/blocking/shutdown.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 21 | `channel`  |  | Crate-internal | Constructor |  |
| 37 | `wait`  | `Receiver` | Crate-internal | Runtime/task control | Blocks the current thread until all `Sender` handles drop. |

## `tokio/src/runtime/blocking/task.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 12 | `new`  | `BlockingTask<T>` | Crate-internal | Constructor | Initializes a new blocking task from the given function. |
| 27 | `poll`  | `Future for BlockingTask<T>` | Trait impl | Future impl (poll) |  |

