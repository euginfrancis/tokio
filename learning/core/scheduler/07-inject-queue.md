# 07 — Inject queue (the global, locked, intrusive FIFO)

> **Role:** the *one* place where work can be handed to the scheduler from
> "outside" (a non-worker thread, a driver thread without a core, a task woken
> by a foreign thread) **and** the overflow sink when a worker's 256-slot
> [local queue](./06-local-queue.md) is full.
> **Boundary:** it stores `task::Notified<T>` handles only. It never polls, never
> wakes workers (the caller does that), and never decides *who* takes a task.

**Files** (`tokio/src/runtime/scheduler/`):

| File | Lines | Content |
|---|---|---|
| `inject.rs` | 71 | `Inject<T>` = `Shared<T>` + `Mutex<Synced>`; lock-taking wrappers (`push`, `pop`, `close`, `is_closed`) |
| `inject/shared.rs` | 121 | `Shared<T>` – the lock-free-readable half (`len`) + the algorithms that need `&mut Synced` |
| `inject/synced.rs` | 37 | `Synced` – the mutex-protected half (`is_closed`, `head`, `tail`) + `Synced::pop` |
| `inject/pop.rs` | 55 | `Pop<'a, T>` – the iterator returned by `pop_n` (borrowed `&mut Synced`) |
| `inject/rt_multi_thread.rs` | 212 | `InjectQueue<T>` enum (multi-thread only) + `push_batch`, `pop_n(n, f)`, `drain_into` |
| `inject/metrics.rs` | 7 | `Inject::len()` for metrics |

## 1. Data structures

```rust
pub(crate) struct Inject<T: 'static> {
    shared: Shared<T>,          // len: AtomicUsize
    synced: Mutex<Synced>,      // is_closed, head, tail
}

pub(crate) struct Shared<T: 'static> {
    pub(super) len: AtomicUsize,   // "helps prevent unnecessary locking in the hot path"
    _p: PhantomData<T>,
}

pub(crate) struct Synced {
    pub(super) is_closed: bool,
    pub(super) head: Option<task::RawTask>,
    pub(super) tail: Option<task::RawTask>,
}
```

Why the split? The `Shared`/`Synced` division lets the algorithms in
`shared.rs` take `&mut Synced` as a *proof of lock ownership* (all are
`unsafe fn(&self, synced: &mut Synced, …)` with the contract "must be called
with the same `Synced` returned by `Shared::new`"), while `len` stays readable
**without** the lock so idle workers can answer "is there anything?" with one
atomic load.

`InjectQueue<T>` (multi-thread only) is a single-variant enum
`Locked(Inject<T>)`; "each variant owns its queue and lock topology" – it is the
seam where an alternative topology (e.g. sharded) could be added without
touching callers. Today every method is `match self { Locked(q) => q.… }`.
The current-thread scheduler uses `Inject<T>` directly (see
[03](./03-current-thread.md)).

### The list is *intrusive*

There is no node allocation. The queue links tasks through the
`Header.queue_next: UnsafeCell<Option<NonNull<Header>>>` field that every task
already carries ([task/02 – cell layout](../task/02-cell-layout.md)). Access goes
through `RawTask::{get_queue_next,set_queue_next}` (see
[task/03](../task/03-rawtask-vtable.md)).

> **Why that is safe:** a `Notified` is a *unique* right to schedule the task.
> While you hold one, nobody else is in a queue with that task, so you have
> exclusive access to `queue_next`. The `Notified` is **consumed** by
> `into_raw()` on push and **re-created** with `Notified::from_raw()` on pop;
> the ref-count the `Notified` carried travels with the pointer.

Consequences:

* Push never allocates and therefore never fails (it is the *unbounded*
  fallback for the bounded ring).
* A task is in at most one of {local ring, LIFO slot, inject queue, being
  polled} at a time (the NOTIFIED bit in the [state word](../task/01-state-word.md)
  guarantees one `Notified` exists).

## 2. Invariants

| # | Invariant | Maintained by |
|---|---|---|
| I1 | `len` equals the number of tasks reachable from `head` | every mutation updates it *while holding the mutex* |
| I2 | `head.is_none() == tail.is_none()` | `push`/`push_batch_inner`/`Synced::pop` |
| I3 | the last task's `queue_next` is `None`; popped tasks have `queue_next` reset to `None` | `Synced::pop` calls `set_queue_next(None)`; `debug_assert!`s in `push` |
| I4 | once `is_closed`, nothing is ever added | `push` returns early (drops task: see below), `push_batch_inner` drops the batch |
| I5 | `len` may be read without the lock, but written only under it | `unsync_load()` + `store(Release)` pattern |

### The `unsync_load` + `store(Release)` pattern

```rust
// safety: only mutated with the lock held
let len = unsafe { self.len.unsync_load() };   // plain, non-atomic read
...
self.len.store(len + 1, Release);              // publish
```

Because every writer holds the mutex, no read-modify-write race exists; an
atomic `fetch_add` (a locked bus cycle) is unnecessary. Readers use
`load(Acquire)` (`Shared::len`). A reader can see a slightly stale value – that
is fine, `len` is only a hint to skip the lock (`pop` returns `None` early
when `is_empty()`), never a correctness condition. `unsync_load` is a
loom-aware shim (`loom/std/atomic_usize.rs`).

## 3. Operations

### `push(task)`  — `Inject::push` → `Shared::push`

```text
lock
  if synced.is_closed          -> return      (task dropped when the param goes out of scope)
  len  = len.unsync_load()
  raw  = task.into_raw()
  tail.set_queue_next(raw)  or  head = raw
  tail = raw
  len.store(len+1, Release)
unlock
```

On a closed queue, `push` simply returns and the `Notified` parameter is
dropped; dropping a `Notified` decrements the ref-count and, if last, runs
`dealloc`. (Shutdown correctness depends on `OwnedTasks` also having a closed
bit – see [12 – shutdown](./12-shutdown.md).)

### `pop()` — `Inject::pop`

```rust
if self.shared.is_empty() { return None; }    // lock-free fast path
let mut synced = self.synced.lock();
unsafe { self.shared.pop(&mut synced) }       // == pop_n(1).next()
```

### `pop_n(n, f)` — the batch grab used by idle workers

```rust
pub(crate) fn pop_n<R>(&self, n: usize, f: impl FnOnce(Pop<'_, T>) -> R) -> R {
    let mut synced = self.synced.lock();
    f(unsafe { self.shared.pop_n(&mut synced, n) })
}
```

`Shared::pop_n` clamps `n = min(n, len)`, **decrements `len` up-front**, then
returns a `Pop` that lazily unlinks `n` items. Properties worth noting:

* The callback form means the **lock is held while `f` runs** (`f` pushes the
  items into the local ring via `run_queue.push_back(tasks)`). Rationale in
  the doc comment: leftover items "are removed from the queue and dropped before
  the lock is released".
* `Pop` implements `Iterator + ExactSizeIterator`, and its `Drop` drains the
  remaining items (`for _ in self.by_ref() {}`) so `len` (already reduced) and
  the list stay consistent even if the consumer stops early. The test
  `pop_n_drains_on_drop` pins this.

### `push_batch(iter)` — used by overflow

```text
first = iter.next()?  (None -> return, no lock)
link first -> next -> ... (set_queue_next) WITHOUT the lock   // O(n) outside critical section
lock
  if closed:
      unlock first          // "Drop the lock before dropping the tasks:
      walk list, from_raw().drop()   // user Drop code may re-enter schedule()"
      return
  splice [batch_head..batch_tail] after tail (or become head)
  len.store(len + n, Release)
unlock
```

Two design points: (1) all the linking happens before the lock so the critical
section is O(1); (2) on a closed queue the tasks are dropped **after releasing
the lock**, because dropping a task may run arbitrary user `Drop` code that
could call `schedule()` → `push` → `lock()` again (deadlock).

### `close()` / `is_closed()`

`close` takes the lock, sets `is_closed`, and returns `true` only on the
open→closed transition (the caller `Handle::close` uses that to `notify_all()` exactly once).

### `drain_into(&mut Vec)` (cfg `tokio_unstable` + `taskdump`)

Holds the lock for the whole drain so a task dump sees a consistent set.

## 4. Who calls it (interactions)

| Caller | Call | When |
|---|---|---|
| `multi_thread::Handle::push_remote_task` | `inject.push` | `schedule_task` from a non-worker thread, a worker of another runtime, or a thread that currently holds no core (followed by `notify_parked_remote`) |
| `impl Overflow for Handle` | `push` / `push_batch` | local ring full → [push_overflow](./06-local-queue.md) sends half of the ring + the new task |
| `Core::next_task` → `Core::next_remote_task` | `inject.pop` | every `global_queue_interval` ticks, and as a fallback when nothing local |
| `Core::run_queue_pop / pop_n` path in `next_task` (line ~1106–1155) | `inject().is_empty/len/pop_n` | idle worker refills local ring: `n = max(1, min(len/num_workers + 1, cap))`, `cap = min(remaining_slots, max_capacity/2)` |
| `Handle::close` | `inject.close()` | first step of shutdown |
| `Core::maintenance` | `inject().is_closed()` | workers detect shutdown |
| `Handle::notify_if_work_pending` | `inject.is_empty()` | before parking: "did anyone leave work for me?" |
| `Handle::shutdown_core` | `next_remote_task()` loop | last worker out drops everything still queued |
| `current_thread::Handle::schedule` | `inject.push` (non-owner thread) | cross-thread wakeups for the current-thread runtime |
| `current_thread::shutdown2` | `inject.close()` then pop-and-drop loop | runtime drop |
| metrics | `injection_queue_depth()` → `len` | `RuntimeMetrics` |

### Why *`len/num_workers + 1`* ?

The first task is returned directly to the caller, the rest are copied into
the local ring. Taking `len/workers + 1` shares work fairly: if 10 tasks are
queued and 4 workers exist a worker takes 3, leaving 7 for the others, and
ensuring a single idle worker never starves the rest. The cap at half the ring
keeps the batch in the *first half* of the ring so a later `push_overflow` (which only moves
the older half) never bounces the same tasks straight back to inject.

## 5. Costs & trade-offs

* **One mutex for all producers and consumers.** Simple and correct; the
  hot path (local ring + LIFO slot) avoids it entirely, and workers consult it
  rarely (every `global_queue_interval` ticks – self-tuned from the poll-time EWMA, targeting ~61 polls per 200µs unless fixed by the builder – or when idle). The single-variant `InjectQueue` enum leaves room for other
  lock topologies without touching callers.
* **Unbounded.** There is no back-pressure: a flood of remote wakeups simply grows the list
  (memory is the tasks themselves, no extra allocation).
* **FIFO** – fairness for remote tasks versus the LIFO optimisation locally.

## 6. Tests

| Where | What |
|---|---|
| `runtime/tests/inject.rs` | `push_and_pop`, `push_batch_and_pop`, `pop_n_drains_on_drop` |
| `runtime/tests/loom_multi_thread.rs` & friends | exercise inject indirectly through spawn-from-outside / shutdown models |
| `tokio/tests/rt_threaded.rs` | cross-thread spawn, shutdown with queued tasks |

<!-- TESTS:inject -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/inject.rs`](../../../tokio/src/runtime/tests/inject.rs) | 3 | 32 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [08 — Idle coordination](./08-idle-coordination.md)
