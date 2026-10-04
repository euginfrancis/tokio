# 12 — Shutdown (ordered teardown of tasks, queues, threads, drivers)

> **Goal:** dropping a `Runtime` must (1) stop accepting work, (2) cancel every task and **drop its future inside the
> runtime context**, (3) leak nothing (no task stuck in a queue holding a ref-count), (4) stop the drivers and
> join the threads — without deadlocks when workers are in the middle of anything.
> **Boundary:** this is a *protocol* spread across `Runtime::drop`, the scheduler (`Handle::close`, `Core::pre_shutdown`,
> `shutdown_core`), `OwnedTasks`, the inject queue, the Parker/driver and the blocking pool.

## 1. Entry points

| API | Path |
|---|---|
| `drop(Runtime)` | `Runtime::drop` (`runtime.rs:506`) → `current_thread.shutdown(&handle)` **or** `multi_thread.shutdown(&handle)`; afterwards the remaining fields drop (`handle`, then `blocking_pool` whose `Drop` calls `shutdown(None)`) |
| `Runtime::shutdown_timeout(d)` | `self.handle.inner.shutdown()` (MT: close + notify), then `blocking_pool.shutdown(Some(d))` — returns after `d` even if blocking threads are still busy |
| `Runtime::shutdown_background()` | `shutdown_timeout(Duration::from_nanos(0))` — allowed from async contexts where blocking in `drop` would panic |

Field order in `struct Runtime { scheduler, handle, blocking_pool }` matters: the scheduler is torn down first, the blocking pool last.

## 2. The two close bits (why *both* are needed)

From the module docs of `multi_thread/worker.rs`:

* **`OwnedTasks.closed`** (`AtomicBool`, checked **under the shard lock** in `bind_inner`): a spawn that observes it closed
  immediately calls `task.shutdown()` itself and returns `None` (no `Notified`, so nothing is scheduled) — the `JoinHandle` completes with `JoinError::Cancelled`.
* **`Inject.synced.is_closed`**: pushes after close drop the `Notified` ([07](./07-inject-queue.md)).

Spawn races during shutdown:

| Spawner sees | What happens |
|---|---|
| `OwnedTasks` **open** (bind happened before/during step 1) | task is in the list ⇒ cleaned up by `close_and_shutdown_all`; its `Notified` can only go to the inject queue/rings, which are either closed or drained later |
| `OwnedTasks` **closed** | task cancelled by the spawner; inject queue never consulted |

Needing both: only an inject bit ⇒ a task could be *bound* long after shutdown; only an `OwnedTasks` bit ⇒ a `Notified` of a still-owned task could be pushed to the inject queue **after** the final drain, leaving it there forever — a ref-count cycle and memory leak.

## 3. Multi-thread protocol (step by step)

```text
 Runtime::drop
   └─ MultiThread::shutdown → Handle::shutdown → Handle::close()
 (1) close():  if shared.inject.close() { notify_all() }          // inject closed; every worker unparked
               (and, with the alternative timer, is_shutdown = true)
     NOTE: OwnedTasks is NOT closed here; it is closed in step 3 by close_and_shutdown_all
           (the module doc at the top of worker.rs says step 1 closes both, but in this snapshot `Handle::close` only closes the inject queue; `OwnedTasks` is closed by `close_and_shutdown_all` in step 3 — the spawn-race table in §2 describes exactly this window)
 (2) each worker, in Core::maintenance (every event_interval ticks / after every park):
          is_shutdown = inject.is_closed()
     -> Context::run loop exits: `while !core.is_shutdown`
 (3) after the loop (in parallel on every worker thread):
          [alt timers] shutdown_local_timers(...)
          core.pre_shutdown(worker):
              start = rand % owned.shard_size
              owned.close_and_shutdown_all(start)   // set closed=true (Release); pop_back every shard from `start`;
                                                    // task.shutdown() on each  (cancel + drop future)
              stats.submit()
          handle.shutdown_core(core)
 (4) Handle::shutdown_core(core):
          cores = shutdown_cores.lock(); cores.push(core)
          if cores.len() != remotes.len() { return }          // not last: just leave
          // LAST worker: single-threaded phase
          debug_assert!(owned.is_empty())
          for core in cores.drain(..) { core.shutdown(handle) }   // see below
          while let Some(t) = next_remote_task() { drop(t) }      // drain inject
```

`Core::shutdown(handle)`:

```rust
let mut park = self.park.take().expect("park missing");
while self.next_local_task().is_some() {}      // drop LIFO slot + all ring entries (their tasks are already shut down)
park.shutdown(&handle.driver);                // first Parker to get the TryLock<Driver> shuts the driver down; all do condvar.notify_all
```

### Why the Cores are collected instead of put back
`shutdown_cores: Mutex<Vec<Box<Core>>>` — doc: the core is **not** placed back in the worker "to avoid it from being stolen by a thread
that was spawned as part of `block_in_place`" (a `Worker.core.take()` in `run` could otherwise resurrect it).

### What `task.shutdown()` does
`Task::shutdown` → `RawTask::shutdown` → `Harness::shutdown` ([task/04](../task/04-harness.md)): `transition_to_shutdown`
sets CANCELLED (and takes RUNNING if idle); then `cancel_task` drops the future (catching panics), stores `Err(JoinError::cancelled)` as the output,
and `complete()`; if the task is *currently running* on another thread, that thread finishes the cancel when its poll returns. User `Drop` code for futures
runs **on worker threads, inside the runtime context** — the reason `MultiThread::shutdown` doesn't need to enter the context itself.

Important: because `close_and_shutdown_all` is run by *all* workers concurrently, each starting at a random shard (`rand.fastrand_n(shard_size)`), they split the work and reduce lock contention on the sharded list ([task/08](../task/08-owned-tasks.md)).

### Parked workers
Step 1's `notify_all` unparks every `Remote.unpark` — including a worker parked on the driver (`driver.unpark()`), or on a condvar — and parked workers re-check `maintenance()` after each park (`Core::park` loop `while !core.is_shutdown && !core.is_traced`).

### Workers inside `block_in_place`
A thread with the Core handed off finishes its blocking closure, then `Reset` attempts to take the Core back; the new thread running the core exits on `is_shutdown`. If the original thread gets no Core it just returns; the pool's `shutdown_rx.wait(timeout)` waits for blocking threads (`BlockingPool::shutdown`) — which is why `shutdown_timeout` exists.

## 4. Current-thread protocol

`CurrentThread::shutdown(handle)` (`current_thread/mod.rs`):

1. `take_core` (the Core must be present — "Oh no! We never placed the Core back, this is a bug!" unless already panicking).
2. If the TLS is alive: `core.enter(|core, _| shutdown2(core, handle))` (so dropping tasks happens inside the runtime context — `Runtime::drop` also sets `context::try_set_current`); else run `shutdown2` without setting the context (spawns would fail anyway).
3. `shutdown2`:
   1. `owned.close_and_shutdown_all(0)` (closes + cancels all) — `LocalOwnedTasks`/`OwnedTasks` per config
   2. drain local queue (`next_local_task` + drop)
   3. `inject.close()`
   4. drain remote queue (pop + drop)
   5. `assert!(owned.is_empty())`
   6. submit metrics
   7. `driver.shutdown(&handle.driver)`

Note the order difference from multi-thread: local queue → inject close → inject drain, in one thread, so no race exists between "close" and "drain".

## 5. The blocking pool's part

`BlockingPool::shutdown(timeout)`: `begin_shutdown` sets `shutdown = true`, drains the pending blocking queue — each queued task gets `shutdown_or_run_if_mandatory()` (non-mandatory ⇒ `task.shutdown()`, mandatory ⇒ run),
notifies idle threads, then `shutdown_rx.wait(timeout)`; if signalled, joins the last-exited thread and all worker thread `JoinHandle`s. Multi-thread *workers are blocking-pool threads* (`Launch::launch` uses `spawn_blocking(run)`), so the pool shutdown is also what waits for the scheduler threads to exit
([components/09](../../components/09-blocking-pool.md)).

## 6. Invariants

| # | Invariant |
|---|---|
| I1 | After `close_and_shutdown_all` returns on all workers, `OwnedTasks` is closed and empty (`debug_assert!(owned.is_empty())`) |
| I2 | A `Notified` is never added to the inject queue after it is closed ⇒ final drain sees every remaining one |
| I3 | Only the **last** worker runs the single-threaded phase (`cores.len() == remotes.len()`) |
| I4 | The driver is shut down exactly once (guarded by `TryLock`) |
| I5 | Task futures are dropped on runtime threads inside the context, never on the dropping thread (MT) |
| I6 | `shutdown` is idempotent for the blocking pool (`begin_shutdown` returns `None` the second time) |

## 7. Tests

`tokio/tests/rt_threaded.rs`: `spawn_shutdown`, `drop_threadpool_drops_futures`, `wake_during_shutdown`, `start_stop_callbacks_called`;
`runtime/tests/loom_multi_thread.rs`: `racy_shutdown`, `pool_shutdown`, `shutdown_with_notification`; `loom_multi_thread/shutdown.rs`; `tokio/tests/rt_common.rs` (`eagerly_drops_futures_on_shutdown`, `shutdown_timeout`, `shutdown_timeout_0`, `shutdown_timeout_max`, `shutdown_wakeup_time`, `shutdown_concurrent_spawn`); `runtime/tests/task_combinations.rs`.

<!-- TESTS:shutdown -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/tests/rt_common.rs`](../../../tokio/tests/rt_common.rs) | 49 | 1,050 |
| [`tokio/src/runtime/tests/loom_multi_thread/shutdown.rs`](../../../tokio/src/runtime/tests/loom_multi_thread/shutdown.rs) | 1 | 21 |
| [`tokio/src/runtime/tests/task_combinations.rs`](../../../tokio/src/runtime/tests/task_combinations.rs) | 1 | 404 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [13 — Driver interface](./13-driver-interface.md)
