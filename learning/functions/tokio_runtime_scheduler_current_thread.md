# `tokio::runtime::scheduler::current_thread` — 46 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 19 |
| Private helper | 18 |
| Trait impl | 9 |

## `tokio/src/runtime/scheduler/current_thread/mod.rs` (46)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 138 | `new`  | `CurrentThread` | Crate-internal | Constructor |  |
| 200 | `block_on`  | `CurrentThread` | Crate-internal | Runtime/task control |  |
| 241 | `take_core`  | `CurrentThread` | Private helper | Data movement |  |
| 254 | `shutdown`  | `CurrentThread` | Crate-internal | Runtime/task control |  |
| 287 | `shutdown2`  |  | Private helper | Runtime/task control |  |
| 321 | `fmt`  | `fmt::Debug for CurrentThread` | Trait impl | Formatting |  |
| 330 | `tick`  | `Core` | Private helper | Time / timers | Get and increment the current tick |
| 334 | `next_task`  | `Core` | Private helper | Other / internal logic |  |
| 345 | `next_local_task`  | `Core` | Private helper | Other / internal logic |  |
| 354 | `push_task`  | `Core` | Private helper | Data movement |  |
| 363 | `submit_metrics`  | `Core` | Private helper | Metrics / counters |  |
| 369 | `wake_deferred_tasks_and_free`  |  | Private helper | Wake / park |  |
| 381 | `run_task`  | `Context` | Private helper | Runtime/task control | Execute the closure with the given scheduler core stored in the thread-local context. |
| 407 | `park`  | `Context` | Private helper | Wake / park | Blocks the current thread until an event is received by the driver, including I/O events, timer events, ... |
| 445 | `park_yield`  | `Context` | Private helper | Wake / park | Checks the driver for new events without blocking the thread. |
| 456 | `has_pending_work`  | `Context` | Private helper | Accessor / query |  |
| 460 | `park_internal`  | `Context` | Private helper | Wake / park |  |
| 478 | `enter`  | `Context` | Private helper | Runtime/task control |  |
| 492 | `defer`  | `Context` | Crate-internal | Runtime/task control |  |
| 502 | `spawn`  | `Handle` | Crate-internal | Runtime/task control | Spawns a future onto the `CurrentThread` scheduler |
| 537 | `spawn_local` ⚠ | `Handle` | Crate-internal | Runtime/task control | Spawn a task which isn't safe to send across thread boundaries onto the runtime. |
| 581 | `dump`  | `Handle` | Crate-internal | Debugging / tracing |  |
| 624 | `next_remote_task`  | `Handle` | Private helper | Other / internal logic |  |
| 628 | `waker_ref`  | `Handle` | Private helper | Wake / park |  |
| 636 | `reset_woken`  | `Handle` | Crate-internal | Other / internal logic |  |
| 640 | `num_alive_tasks`  | `Handle` | Crate-internal | Accessor / query |  |
| 644 | `injection_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 648 | `worker_metrics`  | `Handle` | Crate-internal | Metrics / counters |  |
| 656 | `scheduler_metrics`  | `Handle` | Crate-internal | Other / internal logic |  |
| 660 | `worker_local_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 664 | `num_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 668 | `num_idle_blocking_threads`  | `Handle` | Crate-internal | Accessor / query |  |
| 672 | `blocking_queue_depth`  | `Handle` | Crate-internal | Metrics / counters |  |
| 677 | `spawned_tasks_count`  | `Handle` | Crate-internal | Runtime/task control |  |
| 688 | `owned_id`  | `Handle` | Crate-internal | Other / internal logic |  |
| 692 | `name`  | `Handle` | Crate-internal | Other / internal logic |  |
| 698 | `fmt`  | `fmt::Debug for Handle` | Trait impl | Formatting |  |
| 706 | `release`  | `Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 710 | `schedule`  | `Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 740 | `hooks`  | `Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 747 | `unhandled_panic`  | `Schedule for Arc<Handle>` | Trait impl | Scheduler hook |  |
| 780 | `wake`  | `Wake for Handle` | Trait impl | Waker |  |
| 785 | `wake_by_ref`  | `Wake for Handle` | Trait impl | Waker | Wake by reference |
| 814 | `block_on`  | `CoreGuard<'_>` | Private helper | Runtime/task control |  |
| 894 | `enter`  | `CoreGuard<'_>` | Private helper | Runtime/task control | Enters the scheduler context. |
| 913 | `drop`  | `Drop for CoreGuard<'_>` | Trait impl | Drop / cleanup |  |

