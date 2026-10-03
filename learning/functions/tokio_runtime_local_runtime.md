# `tokio::runtime::local_runtime` — 12 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 9 |
| Crate-internal | 1 |
| Private helper | 1 |
| Trait impl | 1 |

## `tokio/src/runtime/local_runtime/runtime.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 54 | `from_parts`  | `LocalRuntime` | Crate-internal | Conversion |  |
| 96 | `new`  | `LocalRuntime` | Public API | Constructor | Creates a new local runtime instance with default configuration values. |
| 124 | `handle`  | `LocalRuntime` | Public API | Handle / reference plumbing | Returns a handle to the runtime's spawner. |
| 151 | `spawn_local`  | `LocalRuntime` | Public API | Runtime/task control | Spawns a task on the runtime. |
| 194 | `spawn_blocking`  | `LocalRuntime` | Public API | Runtime/task control | Runs the provided function on a thread from a dedicated blocking thread pool. |
| 224 | `block_on`  | `LocalRuntime` | Public API | Runtime/task control | Runs a future to completion on the Tokio runtime. |
| 236 | `block_on_inner`  | `LocalRuntime` | Private helper | Runtime/task control |  |
| 310 | `enter`  | `LocalRuntime` | Public API | Runtime/task control | Enters the runtime context. |
| 346 | `shutdown_timeout`  | `LocalRuntime` | Public API | Runtime/task control | Shuts down the runtime, waiting for at most `duration` for all spawned work to stop. |
| 380 | `shutdown_background`  | `LocalRuntime` | Public API | Runtime/task control | Shuts down the runtime, without waiting for any spawned work to stop. |
| 386 | `metrics`  | `LocalRuntime` | Public API | Accessor / query | Returns a view that lets you get information about how the runtime is performing. |
| 392 | `drop`  | `Drop for LocalRuntime` | Trait impl | Drop / cleanup |  |

