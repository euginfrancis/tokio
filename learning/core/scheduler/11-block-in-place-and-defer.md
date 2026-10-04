# 11 — `block_in_place` (core hand-off) and the `Defer` queue

Two small mechanisms, both about **not letting a worker thread's blocking or
yielding behaviour stall the pool**.

---

## Part A — `block_in_place`: moving the *Core* to another thread

> **Problem:** a task on a worker thread must run a long synchronous operation (blocking I/O, a mutex, CPU work).
> While it blocks, that worker's `Core` — its LIFO slot, 256-slot local run queue, parker (maybe the I/O driver!) —
> is frozen; the tasks in its queue would starve.
> **Solution:** the *thread* keeps blocking, but the *Core* (the "worker" in the logical sense) is handed to
> **another thread from the blocking pool**, which keeps running the scheduler loop. When the closure returns,
> the original thread tries to take a Core back.

**Files:** `multi_thread/worker.rs` (`block_in_place`, `maybe_move_runtime`, `run`),
`runtime/context/runtime_mt.rs` (`exit_runtime`, `current_enter_context`), public wrapper
`tokio/src/task/blocking.rs::block_in_place`, `runtime/scheduler/mod.rs` (dispatcher),
`runtime/blocking` (thread source; see [../../components/09-blocking-pool.md](../../components/09-blocking-pool.md)).

### A.1 The two structures that make it possible

```rust
pub(super) struct Worker {                 // shared by Arc, one per worker index
    handle: Arc<Handle>,
    index: usize,
    core: AtomicCell<Core>,                // the "parking spot" for the Core when no thread is running it
}

pub(super) struct Context {                // thread-local (via scheduler::Context), one per OS thread running the loop
    worker: Arc<Worker>,
    core: RefCell<Option<Box<Core>>>,      // the Core while THIS thread runs it
    pub(crate) defer: Defer,
}
```

`AtomicCell<T>` (`util/atomic_cell.rs`) is an `AtomicPtr<T>` holding `Option<Box<T>>`: `set` = swap-in, `take` = swap-out (null).
So exactly one of {`Worker.core`, some `Context.core`, a `shutdown_cores` Vec} owns a given `Box<Core>` at any time — *ownership transfer by pointer swap*, no lock.

### A.2 Algorithm

```text
block_in_place(f):
  (had_entered, take_core) = maybe_move_runtime()
  if had_entered:
      _reset = Reset{ take_core, budget: coop::stop() }     // blocking is not budget-limited
      exit_runtime(f)                                        // mark thread NotEntered while f runs
  else:
      f()

maybe_move_runtime():            // non-generic to limit monomorphisation
  match (current_enter_context(), worker context present?):
    (Entered, yes)  -> had_entered = true; continue to hand-off below
    (Entered, no)   -> if allow_block_in_place { had_entered = true; return }     // block_on of a MT runtime
                       else Err("can call blocking only when running on the multi-threaded runtime")  // current_thread / LocalSet
    (NotEntered, yes) -> return                 // nested call; already handed off
    (NotEntered, no)  -> return                 // outside tokio; plain call
  cx.defer.wake()                               // deferred tasks don't stay on core -> wake them now
  core = cx.core.take() else return             // no core => nothing to hand off
  if let Some(t) = core.lifo_slot.take() { core.run_queue.push_back_or_overflow(t, ..) }   // LIFO slot tasks can't be stolen
  take_core = true
  assert!(core.park.is_some())
  cx.worker.core.set(core)                      // publish Core in the shared slot
  spawn_blocking(move || run(worker.clone()))   // another thread picks it up (or any worker thread steals the slot)
```

Then in the new thread, `run(worker)` does `worker.core.take()`: **if `None`, someone else already runs this worker → return immediately**
(the `Some(core) => core, None => return` early-out, which also explains why launching extra "worker runners" is harmless).

When `f` finishes (or panics), `Reset::drop` runs:

```rust
if self.take_core {
    let core = cx.worker.core.take();          // try to steal the Core back (may be None: another thread is running it)
    if core.is_some() { worker_metrics[idx].set_thread_id(current) }
    *cx.core.borrow_mut() = core;              // assert it was None before
}
coop::set(self.budget);                        // restore the task's budget
```

If it got the Core back, this thread continues the scheduler loop where the task resumes; if not (`None`), the
original thread simply has **no core**: later `schedule_task` calls on it fall through to the inject queue
(`cx.core.borrow_mut().as_mut()` is `None`), `Context::defer` wakes immediately (see Part B), and after the task polls
returns `run_task` sees `self.core.borrow_mut().take()` is `None` → `ControlFlow::Break(())`: this thread's `run` exits and the thread returns to the blocking pool.

### A.3 Sequence

```text
Task T on Thread 1 (core C)        Blocking pool         Thread 2
-----------------------------      -------------         ---------
block_in_place(f):
  move C -> Worker.core
  spawn_blocking(run(W)) ----------> picks job ---------> run(W): core = W.core.take()  (gets C)
  exit_runtime(f)  (blocks)                               loop { next_task ... run tasks ... }
  ...f done...
  Reset: W.core.take()
     case 1: Some(C)  -> nobody took the Core (e.g. no free blocking thread yet, or Thread 2
                         already parked it back); Thread 1 resumes as the worker.
     case 2: None     -> Thread 2 owns C. T finishes its poll without a core; run_task returns
                         Break and Thread 1 returns to the blocking pool.
```

`AtomicCell` guarantees only one thread can win the `take()`; the loser simply sees `None`.

### A.4 Consequences / constraints

| Constraint | Reason |
|---|---|
| Only on the **multi-thread** runtime; panics on current-thread/LocalSet | blocking the only thread would deadlock the scheduler (the `Err(...)` message) |
| Allowed inside `Runtime::block_on` of a MT runtime (`allow_block_in_place` flag set by `enter_runtime(&handle, true, …)`) | that thread is not a worker but isn't the only one |
| Code in `f` **cannot be cancelled** | the thread is blocked; runtime shutdown waits for the blocking pool |
| The task's `coop` budget is suspended and restored | blocking sections aren't budgeted; `coop::stop()` returns the old budget |
| A `Core` stolen by another thread is recorded in metrics (`set_thread_id`) | metrics follow the Core |
| `shutdown_cores` doc: Cores are **not** put back in the worker at shutdown "to avoid it from being stolen by a thread spawned as part of `block_in_place`" | see [12](./12-shutdown.md) |
| Heavy use needs blocking-pool threads (`max_blocking_threads`) | if none available the job queues; the code moves the LIFO-slot task to the ring first so the stuck Core's other tasks can be stolen by others |

### A.5 Tests

`tokio/tests/rt_threaded.rs`: `blocking`, `coop_and_block_in_place`, `yield_after_block_in_place`,
`test_nested_block_in_place_with_block_on_between`, `yield_now_in_block_in_place`, `mutex_in_block_in_place`,
`wake_deferred_tasks_before_block_in_place`, `max_blocking_threads(_set_to_zero)`; loom `blocking_and_regular*`, `only_blocking*`
in `runtime/tests/loom_multi_thread.rs`.

<!-- TESTS:block_in_place -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/tests/task_blocking.rs`](../../../tokio/tests/task_blocking.rs) | 16 | 257 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

---

## Part B — `Defer`: "wake me after you've run everything else"

> **Problem:** `yield_now()` and coop-budget exhaustion must give *other* work a chance (including the I/O and timer
> drivers). A plain `wake_by_ref()` would put the task straight back in the queue (LIFO slot!) and it could run again before anyone else.
> **Solution:** park the *waker* in a per-thread list; the scheduler wakes the list only **after** it has run out of ready tasks and polled the driver.

**File:** `runtime/scheduler/defer.rs` (49 lines)

```rust
pub(crate) struct Defer { deferred: RefCell<Vec<Waker>> }      // !Sync on purpose: only the owning thread touches it

defer(&self, waker)   // skip if the LAST entry will_wake(waker) (same task deferring repeatedly), else push(waker.clone())
is_empty()
wake()                // while let Some(w) = deferred.borrow_mut().pop() { w.wake() }   (LIFO order; borrow released before wake)
take_deferred()       // taskdump only: std::mem::take
```

`wake()` pops one at a time and releases the `RefCell` borrow before calling `waker.wake()` — waking may schedule
(re-enter `defer`/`schedule_local`), and holding the borrow would panic.

### Callers

| Caller | Effect |
|---|---|
| `task::yield_now()` → `context::defer(cx.waker())` | "Don't wake the task immediately … hand the waker to the scheduler, which wakes deferred tasks only after it has run out of ready tasks and polled the driver" |
| `coop` `register_waker` (budget exhausted → `Pending`) → `context::defer` | same; also increments `budget_forced_yield_count` |
| `task/trace` (taskdump) | re-enqueues a task being traced |
| `context::defer(waker)` | `with_scheduler(|s| s.defer(waker))`; **no scheduler ⇒ `waker.wake_by_ref()` immediately** |
| `multi_thread::Context::defer` | if `self.core` is `None` (this thread is in `block_in_place`, has no Core) → `waker.wake_by_ref()` immediately, else `self.defer.defer(waker)` |

### Who drains it

| Drain point | Code |
|---|---|
| Worker out of work and `!defer.is_empty()` | `Context::run`: `park_yield(core)` instead of `park(core)` — a zero-timeout driver poll — which ends with `self.defer.wake()` inside `park_internal` |
| After any real park | `park_internal`: `self.defer.wake()` right after `park.park(...)` returns |
| Before `block_in_place` hand-off | `maybe_move_runtime`: `cx.defer.wake()` (the Core—and with it the chance to drain—moves away) |
| End of `run(worker)` | `cx.defer.wake()` after `cx.run(core)` returns (core lost due to `block_in_place` within a task) |
| Current-thread: `park_internal` (used by both `park` and `park_yield`) | `driver.park*()` then `self.defer.wake()` (see [03](./03-current-thread.md)); `has_pending_work` also counts a non-empty defer queue so `park` doesn't block; `wake_deferred_tasks_and_free` for taskdump |

So the guaranteed order is: *run ready tasks → poll driver (events, timers) → wake deferred → they become ready for the **next** round.*
This is what makes `yield_now()` a real yield and what makes a budget-exhausted task not starve I/O.

### Invariants

* A deferred waker is woken **at most once** per `defer` call (the vec entry is popped).
* Consecutive duplicates collapse (`will_wake` on the last element only — cheap, not a set).
* Nothing is lost on thread loss: if the Core is gone, wake immediately (A) or drain at thread exit.

**Tests:** `tokio/tests/task_yield_now.rs`, `rt_threaded.rs::wake_deferred_tasks_before_block_in_place`, `runtime/tests/loom_multi_thread/yield_now.rs`, coop tests (`tokio/tests/coop_budget.rs`).

<!-- TESTS:defer -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/task_yield_now.rs`](../../../tokio/tests/task_yield_now.rs) | 2 | 27 |
| [`tokio/tests/coop_budget.rs`](../../../tokio/tests/coop_budget.rs) | 2 | 54 |
| [`tokio/src/runtime/tests/loom_multi_thread/yield_now.rs`](../../../tokio/src/runtime/tests/loom_multi_thread/yield_now.rs) | 1 | 29 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [12 — Shutdown](./12-shutdown.md)
