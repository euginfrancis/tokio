# `tokio::runtime::scheduler` — 41 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 41 |

## `tokio/src/runtime/scheduler/block_in_place.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 4 | `block_in_place`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/runtime/scheduler/defer.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 9 | `new`  | `Defer` | Crate-internal | Constructor |  |
| 15 | `defer`  | `Defer` | Crate-internal | Runtime/task control |  |
| 28 | `is_empty`  | `Defer` | Crate-internal | Accessor / query |  |
| 32 | `wake`  | `Defer` | Crate-internal | Wake / park |  |
| 39 | `take_deferred`  | `Defer` | Crate-internal | Data movement |  |

## `tokio/src/runtime/scheduler/inject.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 30 | `new`  | `Inject<T>` | Crate-internal | Constructor |  |
| 41 | `is_closed`  | `Inject<T>` | Crate-internal | Accessor / query |  |
| 48 | `close`  | `Inject<T>` | Crate-internal | Data movement | Closes the injection queue, returns `true` if the queue is open when the transition is made. |
| 56 | `push`  | `Inject<T>` | Crate-internal | Data movement | Pushes a value into the queue. |
| 62 | `pop`  | `Inject<T>` | Crate-internal | Data movement |  |

## `tokio/src/runtime/scheduler/mod.rs` (30)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 53 | `driver`  | `Handle` | Crate-internal | Other / internal logic |  |
| 89 | `current`  | `Handle` | Crate-internal | Handle / reference plumbing |  |
| 96 | `blocking_spawner`  | `Handle` | Crate-internal | Blocking (sync) variant |  |
| 100 | `is_local`  | `Handle` | Crate-internal | Accessor / query |  |
| 110 | `timer_flavor`  | `Handle` | Crate-internal | Other / internal logic |  |
| 121 | `is_shutdown`  | `Handle` | Crate-internal | Accessor / query | Returns true if the runtime is shutting down. |
| 132 | `push_remote_timer`  | `Handle` | Crate-internal | Data movement | Push a timer entry that was created outside of this runtime into the runtime-global queue. |
| 140 | `can_spawn_local_on_local_runtime`  | `Handle` | Crate-internal | Other / internal logic | Returns true if this is a local runtime and the runtime is owned by the current thread. |
| 149 | `spawn`  | `Handle` | Crate-internal | Runtime/task control |  |
| 170 | `spawn_local` ⚠ | `Handle` | Crate-internal | Runtime/task control | Spawn a local task |
| 183 | `shutdown`  | `Handle` | Crate-internal | Runtime/task control |  |
| 192 | `seed_generator`  | `Handle` | Crate-internal | Other / internal logic |  |
| 196 | `as_current_thread`  | `Handle` | Crate-internal | Conversion |  |
| 204 | `hooks`  | `Handle` | Crate-internal | Other / internal logic |  |
| 214 | `num_workers`  | `Handle` | Crate-internal | Accessor / query |  |
| 222 | `num_alive_tasks`  | `Handle` | Crate-internal | Accessor / query |  |
| 226 | `injection_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 230 | `worker_metrics`  | `Handle` | Crate-internal | Metrics / counters |  |
| 240 | `spawned_tasks_count`  | `Handle` | Crate-internal | Runtime/task control |  |
| 245 | `num_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 249 | `num_idle_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 253 | `scheduler_metrics`  | `Handle` | Crate-internal | Other / internal logic |  |
| 257 | `worker_local_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 261 | `blocking_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 269 | `expect_current_thread`  | `Context` | Crate-internal | Other / internal logic |  |
| 277 | `defer`  | `Context` | Crate-internal | Runtime/task control |  |
| 281 | `worker_index`  | `Context` | Crate-internal | Metrics / counters |  |
| 291 | `expect_multi_thread`  | `Context` | Crate-internal | Other / internal logic |  |
| 310 | `current`  | `Handle` | Crate-internal | Handle / reference plumbing |  |
| 316 | `timer_flavor`  | `Handle` | Crate-internal | Other / internal logic |  |

