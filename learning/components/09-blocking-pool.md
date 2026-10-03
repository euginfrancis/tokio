# Block 9 — Blocking Pool

> **Role:** a growable pool of plain OS threads for work that **cannot be async**: blocking syscalls (files, DNS, stdin/stdout), CPU-heavy closures (`spawn_blocking`), and — surprisingly — the runtime's own worker threads.
> In the [component diagram](./README.md): the "BLOCKING POOL — up to 512 extra threads" box on the right, fed by the `fs / process` API box ("offloads to").

---

## 1. At a glance

<!-- STATS:blocking_pool -->
| Metric | Value |
|---|---|
| Source files | 7 |
| Code lines | 991 (2.0% of `tokio/src`) |
| Doc + comment lines | 256 (0.26 per code line) |
| Functions | 66 — public API 0, trait impls 10, internal 56, inline tests 0 |
| `async fn` / `unsafe fn` | 0 / 0 |
| `unsafe` occurrences | 2 |
| Integration tests (`tokio/tests`) | none dedicated — exercised through other blocks' tests |
<!-- /STATS -->

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | The blocking task queue, thread creation (up to a cap), idle threads with a keep-alive timeout, "mandatory" tasks that must run even during shutdown, waiting for all threads at runtime drop, the `BlockingTask` future adapter, blocking-pool metrics. |
| **Does not own** | Async scheduling ([Scheduler](./06-scheduler.md)); task memory/state/`JoinHandle` ([Tasks](./01-tasks.md) — a blocking job *is* a normal task, just never stored in `OwnedTasks`); what the closures do (`fs`, `io::stdin`, `lookup_host`, user code). |
| **Input** | Closures: `spawn_blocking(f)`, `spawn_mandatory_blocking(f)`, `Launch::launch` (worker threads), `block_in_place` (replacement worker). |
| **Output** | Runs the closure on a pool thread; the result is stored in the task like any other future output → `JoinHandle` wakes. |
| **Boundary types** | `blocking::Spawner` (in every scheduler `Handle`), `BlockingPool` (owned by `Runtime`), `Task { task: UnownedTask<BlockingSchedule>, mandatory }`. |

---

## 3. Files

<!-- FILES:blocking_pool -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/runtime/blocking/pool.rs`](../../tokio/src/runtime/blocking/pool.rs) | 560 | 108 | 56.5% |
| [`tokio/src/runtime/blocking/sharded.rs`](../../tokio/src/runtime/blocking/sharded.rs) | 208 | 102 | 21.0% |
| [`tokio/src/blocking.rs`](../../tokio/src/blocking.rs) | 75 | 10 | 7.6% |
| [`tokio/src/runtime/blocking/schedule.rs`](../../tokio/src/runtime/blocking/schedule.rs) | 55 | 6 | 5.5% |
| [`tokio/src/runtime/blocking/shutdown.rs`](../../tokio/src/runtime/blocking/shutdown.rs) | 44 | 17 | 4.4% |
| [`tokio/src/runtime/blocking/task.rs`](../../tokio/src/runtime/blocking/task.rs) | 28 | 9 | 2.8% |
| [`tokio/src/runtime/blocking/mod.rs`](../../tokio/src/runtime/blocking/mod.rs) | 21 | 4 | 2.1% |
| **Total (7 files)** | **991** | **256** | 100% |
<!-- /FILES -->

```
runtime/blocking/
├── mod.rs        create_blocking_pool(); re-exports
├── pool.rs       BlockingPool, Spawner, Inner, LockedImpl (default queue), thread loop, shutdown
├── sharded.rs    ShardedImpl — opt-in 16-shard queue (Builder::enable_sharded_blocking_queue / env var)
├── task.rs       BlockingTask<F>: a Future that runs F once (with coop disabled)
├── schedule.rs   BlockingSchedule: no-op Schedule impl (+ test-util auto-advance inhibition)
└── shutdown.rs   one-shot channel: "all blocking threads have exited"
blocking.rs       stubs when the `rt` feature is off (fs/io-std still compile, run inline)
```

---

## 4. Data structures

```rust
pub(crate) struct BlockingPool {          // owned by Runtime; Drop → shutdown(None)
    spawner: Spawner,
    shutdown_rx: shutdown::Receiver,      // resolves when every thread dropped its shutdown_tx
}
pub(crate) struct Spawner { inner: Arc<Inner> }   // cloned into every scheduler Handle
struct Inner {
    inner_impl: InnerImpl,                // enum { Locked(LockedImpl), Sharded(ShardedImpl) }
    thread_name: ThreadNameFn,            // default "tokio-rt-worker"
    stack_size: Option<usize>,
    after_start, before_stop: Option<Callback>,   // on_thread_start / on_thread_stop hooks
    thread_cap: usize,                    // max_blocking_threads (512) + worker_threads
    scheduler_threads: usize,             // how many of the pool's threads are async workers
    keep_alive: Duration,                 // 10 s default (Builder::thread_keep_alive)
    metrics: SpawnerMetrics { num_threads, num_idle_threads, queue_depth },
}
struct LockedImpl { mutex: Mutex<LockedInner>, condvar: Condvar }    // the default queue
struct LockedInner {
    queue: VecDeque<Task>,
    num_notify: u32,                      // pending condvar wake-ups (spurious-wakeup proof)
    thread_mgmt_state: ThreadManagementState,
}
pub(super) struct ThreadManagementState {
    shutdown: bool,
    shutdown_tx: Option<shutdown::Sender>,
    last_exiting_thread: Option<JoinHandle<()>>,   // joined on shutdown
    worker_threads: HashMap<usize, JoinHandle<()>>,
    worker_thread_index: usize,
}
pub(crate) struct Task { task: UnownedTask<BlockingSchedule>, mandatory: Mandatory }
pub(crate) enum Mandatory { Mandatory, NonMandatory }

pub(crate) struct BlockingTask<T> { func: Option<T> }   // Future: take func, coop::stop(), run it, Ready(result)
pub(crate) struct BlockingSchedule { hooks, handle /* test-util */ }  // schedule() is unreachable: never rescheduled
```

---

## 5. How it interacts with the other blocks

```
 [Tasks] spawn_blocking(f) ─▶ Spawner::spawn_blocking ─▶ BlockingTask::new(f) ─▶ task::unowned(..) ─▶ (Task, JoinHandle)
                                    └─▶ spawn_task: lock; push_back; idle thread? notify_one : spawn_thread (if < cap)
 pool thread: run_worker loop ─▶ pop ─▶ task.run() ─▶ [Tasks] Harness::poll ─▶ BlockingTask::poll ─▶ f() ─▶ output → JoinHandle wake
 [fs] / io::stdin / lookup_host ─▶ asyncify / spawn_blocking / spawn_mandatory_blocking (writes)
 [Scheduler] Launch::launch ─▶ spawn_blocking(|| run(worker))          ← worker threads live HERE
 [Scheduler] block_in_place ─▶ spawn_blocking(|| run(worker))          ← replacement worker
 [Timer drv] (test-util) BlockingSchedule::new/release ─▶ clock.inhibit/allow_auto_advance
 Runtime::drop / shutdown_timeout ─▶ BlockingPool::shutdown ─▶ notify_all; wait for threads (bounded or not)
```

| Other block | Direction | Through |
|---|---|---|
| Tasks | ↔ | `UnownedTask`, `JoinHandle`, `BlockingTask` future |
| Scheduler | ← | Holds a `Spawner`; worker threads and `block_in_place` replacements are blocking tasks |
| fs / process / signal, Net (DNS), I/O (stdio) | ← | `spawn_blocking`, `spawn_mandatory_blocking` |
| Timer driver | → | Inhibits paused-clock auto-advance while a blocking task runs (test-util) |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `create_blocking_pool(builder, thread_cap, scheduler_threads)` | `mod.rs` → `pool.rs` | Build the pool from `Builder` settings |
| `spawn_blocking(f)` (crate-level) / `Spawner::spawn_blocking(rt, f)` | `pool.rs` | Wrap in `BlockingTask`, create an unowned task, enqueue |
| `spawn_mandatory_blocking` | `pool.rs` | Same, but the task runs even if shutdown starts before it's picked up (used by `fs::File` writes, stdio) |
| `Spawner::spawn_task` | `pool.rs` | Under the lock: refuse if shut down, push, then wake an idle thread or spawn a new one (≤ cap); tolerate temporary OS thread-spawn failures if some thread exists |
| `Spawner::spawn_thread` | `pool.rs` | `std::thread::Builder` with name/stack size; thread body = `Inner::run` |
| `Inner::run` → `LockedImpl::run_worker(keep_alive)` | `pool.rs` | Thread loop (below) |
| `Task::run / shutdown_or_run_if_mandatory` | `pool.rs` | Normal run / shutdown-time behavior |
| `BlockingPool::shutdown(timeout)` | `pool.rs` | Flag shutdown, `notify_all`, wait for exit (or timeout), join threads |
| `ShardedImpl::spawn_task / run_worker` | `sharded.rs` | Opt-in variant |
| `BlockingTask::poll` | `task.rs` | Run the closure once, coop disabled |

---

## 7. Flows

**Thread loop** (`LockedImpl::run_worker`):
```
lock
loop:
    while let Some(task) = queue.pop_front():  unlock; task.run(); lock     ← run everything queued
    mark idle
    while !shutdown:
        condvar.wait_timeout(keep_alive = 10s)
        if num_notify > 0: num_notify -= 1; break       ← was handed work
        if timed out: exit thread                       ← idle too long
    if shutdown: run mandatory tasks, drop the rest; exit
```

**Spawn decision** (`spawn_task`): push the task; if any thread is idle → `num_notify += 1; condvar.notify_one()`; else if `num_threads < thread_cap` → spawn a new thread; else leave it queued (a busy thread will get to it).

**Shutdown**: `Runtime::drop` → `BlockingPool::drop` → `shutdown(None)` → set `shutdown`, `notify_all` → threads finish their current task, run remaining **mandatory** tasks, exit → `shutdown_rx.wait(timeout)` returns when the last `shutdown_tx` is dropped → join threads. With `None` it waits **forever** — a never-ending blocking task blocks process exit; `shutdown_timeout`/`shutdown_background` bound or skip the wait.

---

## 8. Invariants & gotchas

- **`thread_cap = max_blocking_threads + worker_threads`**: async workers count against the cap, so `max_blocking_threads(512)` means 512 *extra*.
- **Queued, not rejected:** at the cap, new blocking tasks wait in the queue (unbounded) — heavy `spawn_blocking` load shows up as `blocking_queue_depth`, not errors.
- **Blocking tasks can't be aborted once running** — `abort()` only works before a thread picks them up.
- **Coop is disabled** inside blocking tasks (`coop::stop()`), so budgeted Tokio calls made from there never yield.
- **Mandatory vs non-mandatory**: file writes are mandatory so data isn't silently lost at shutdown.
- Threads exit after **10 s idle**; a burst of blocking work creates threads that later disappear.
- In test-util builds, a running blocking task **inhibits auto-advance** of paused time (otherwise timers would race ahead of the blocking work).

---

## 9. Tests & where to start

<!-- TESTS:blocking_pool -->
_No integration test files are dedicated to this block._
<!-- /TESTS -->

Exercised by `tokio/tests/rt_*` (e.g. `spawn_blocking` behavior, shutdown), `fs_*`, `io_std*`, and the loom model `runtime/tests/loom_blocking.rs`.

**Read in this order:** `task.rs` (15 lines) → `pool.rs` (`spawn_blocking_inner`, `spawn_task`, `run_worker`, `shutdown`) → `sharded.rs`.
**Contribution areas seen in history:** shutdown/hang edge cases (e.g. "fix `spawn_blocking` hang when only scheduler workers exist"), idle-thread accounting, the sharded queue.
