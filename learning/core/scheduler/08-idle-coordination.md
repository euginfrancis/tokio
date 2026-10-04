# 08 — Idle coordination (who sleeps, who searches, who gets woken)

> **Role:** decide, with as little locking as possible, *which* sleeping worker to
> wake when work appears, and avoid the two classic failure modes of a
> work-stealing pool: **lost wake-ups** (work sits in a queue while every worker
> sleeps) and **thundering herds** (every worker spins stealing at once).
> **Boundary:** `Idle` only does accounting (counts + a sleeper list). The actual
> blocking is in the [Parker](./09-parker.md); the actual stealing is in
> [06 – local queue](./06-local-queue.md) / [05 – worker loop](./05-worker-loop.md).

**File:** `tokio/src/runtime/scheduler/multi_thread/idle.rs` (222 lines incl. a
unit test). Call sites live in `worker.rs` (`Core::transition_*`, `Handle::notify_*`).

## 1. Data structures

```rust
pub(super) struct Idle {
    state: AtomicUsize,     // packed: [ num_unparked : high bits | num_searching : low 16 bits ]
    num_workers: usize,
}

pub(super) struct Synced {          // lives inside worker::Synced, i.e. under Shared.synced: Mutex
    sleepers: Vec<usize>,           // indexes of parked workers (a stack: pop() = most recently parked)
}

const UNPARK_SHIFT: usize = 16;
const SEARCH_MASK: usize = (1 << UNPARK_SHIFT) - 1;   // low 16 bits
const UNPARK_MASK: usize = !SEARCH_MASK;
```

Packed word, 2 counters in one atomic so they can be changed **together** with
one `fetch_add`/`fetch_sub`:

```text
 63                     16 15                0
 +-------------------------+-----------------+
 |     num_unparked        |  num_searching  |
 +-------------------------+-----------------+
 initial: num_unparked = num_workers, num_searching = 0
```

Definitions:

* **unparked** – a worker that is either running tasks or searching. Everyone
  starts unparked.
* **searching** – an unparked worker with an empty local queue that is
  currently trying to find work (inject queue, stealing). Always ⊆ unparked.
* **sleeper** – a worker parked in `Parker::park`; identified by index in
  `sleepers`.

The `Synced` half is a field of `worker::Synced` (the single scheduler mutex
`Shared.synced`), which also holds `inject_timers` when the alternative timer
is enabled; the comment in the code explains that the two *must* share the lock
so a timer push cannot be stranded while every worker sleeps.

## 2. The state machine of one worker

```text
            transition_worker_to_searching          (fails if 2*searching >= num_workers)
  running ------------------------------------> searching
     ^                                              |  \
     |  transition_worker_from_searching            |   \  found work: leave searching
     |  (if I was the LAST searcher -> must         |    \ (run_task calls transition_from_searching;
     |   notify another worker)                     |     \ if it returns true => notify_parked_local)
     +----------------------------------------------+      \
                                                            \ nothing found
                      transition_worker_to_parked            v
  running/searching ---------------------------------->  parked (in sleepers)
                          (decrement unparked,
                           and searching if it was searching)
                                  ^                      |
                                  |  woken by            |  worker_to_notify()   (unpark_one(1): unparked+1, searching+1)
                                  |  worker_to_notify    |  unpark_worker_by_id  (unpark_one(0): unparked+1 only)
                                  +----------------------+
```

### Functions

| Function | Lock? | Effect on `state` | Returns |
|---|---|---|---|
| `worker_to_notify(shared)` | fast-path check **without** lock; recheck **with** lock | `unpark_one(1)`: `num_unparked += 1`, `num_searching += 1` (single `fetch_add(1 \| 1<<16)`) | `Some(index)` popped from `sleepers` |
| `transition_worker_to_parked(shared, worker, is_searching)` | lock | `fetch_sub((1<<16) + is_searching)` | `true` iff this was the **last searcher** (⇒ caller must do a final check of all queues) |
| `transition_worker_to_searching()` | none | `fetch_add(1)` if `2 * num_searching < num_workers` | `bool` (permission granted) |
| `transition_worker_from_searching()` | none | `fetch_sub(1)` | `true` iff the previous `num_searching == 1` ⇒ caller **must** wake another worker |
| `unpark_worker_by_id(shared, id)` | lock | removes `id` from `sleepers` (`swap_remove`), `unpark_one(0)` (unparked+1, searching unchanged) | `true` if it *was* parked |
| `is_parked(shared, id)` | lock | none | `sleepers.contains(&id)` |
| `notify_should_wakeup()` | none | **`fetch_add(0, SeqCst)`** – an RMW used as a full-fence read | `num_searching == 0 && num_unparked < num_workers` |

## 3. The three rules that make it correct

### Rule 1 — "One searcher is enough" (anti-thundering-herd)

`worker_to_notify` returns `None` if *any* worker is searching. Reasoning (from the code comment): a searching
worker will eventually find **some** work and, when it leaves the searching
state as the last searcher, `transition_worker_from_searching` returns `true`
and it wakes the *next* sleeper. So wake-ups chain: each newly woken worker
becomes a searcher; when it finds work it wakes another. The chain stops
when nothing is left.

Conversely, `transition_worker_to_searching` allows at most **half** the workers
to search (`2 * num_searching >= num_workers ⇒ false`), a deliberate soft limit
("It is possible for this routine to allow more than 50% … That is OK … an
optimization to prevent too much contention").

### Rule 2 — Double-checked locking for notification

```rust
if !self.notify_should_wakeup() { return None; }   // cheap, no lock; hot path
let mut lock = shared.synced.lock();
if !self.notify_should_wakeup() { return None; }   // authoritative, under lock
State::unpark_one(&self.state, 1);                 // count the woken worker as unparked AND searching
let ret = lock.idle.sleepers.pop();                // guaranteed Some by the check
```

The count is bumped by the *waker* (not by the woken thread) while holding the
lock. That prevents two concurrent notifiers from waking the same sleeper or from
both deciding "nobody is searching" and over-waking: the second one will see
`num_searching == 1` already.

Why `SeqCst` / `fetch_add(0)`? Comment in `notify_should_wakeup`: "it is what
makes the caller's preceding inject-queue push visible to a parking worker's
subsequent unlocked queue-emptiness check." Acquire/Release alone doesn't give the
needed store→load ordering (a classic *Dekker*-style handshake: producer
`push; read state` vs. consumer `write state; read queue`). Both sides need
a total order to guarantee at least one sees the other.

### Rule 3 — The last searcher must double-check before sleeping

```rust
// Core::transition_to_parked
if self.has_tasks() || self.is_traced { return false; }       // never park with local work
let is_last_searcher = idle.transition_worker_to_parked(shared, index, self.is_searching);
self.is_searching = false;
if is_last_searcher { worker.handle.notify_if_work_pending(); }
```

Scenario that this prevents: worker A is the sole searcher, scans all queues
(empty), then B pushes work and calls `worker_to_notify` — it sees
`num_searching == 1` and *doesn't wake anyone* (Rule 1). If A now parks without
re-checking, the work is stranded. Therefore: a searcher that parks and was the
last one re-checks `remotes[*].steal.is_empty()` and `inject.is_empty()`
(`notify_if_work_pending`) and wakes a worker if anything is present.

The mirror case for leaving searching: `transition_from_searching` returning
`true` means "I was the last searcher and I found work → there may be more
work than I can do alone, wake one more" (done in `run_task` via
`notified_parked_worker`).

## 4. Who triggers it

| Event | Path | Notifies? |
|---|---|---|
| Remote schedule (`inject.push`) | `schedule_task` → `push_remote_task` + `notify_parked_remote` | `worker_to_notify` → `unpark` that worker's `Parker` |
| Local schedule to ring / LIFO displace | `schedule_local` → `notify_parked_local` iff `core.park.is_some()` | same; if `park` is `None` (resource-driver wake inside `park`) notification is *delayed* until park finishes (see `park_internal` end: `should_notify_others`) |
| Spawn of a task inside the runtime | `bind_new_task` → `schedule_option_task_without_yield` | as above |
| After polling while having more than one runnable item | `Core::should_notify_others` (`lifo_slot as usize + run_queue.len() > 1`, and not searching) | `notify_parked_local()` in `park_internal` |
| Leaving searching as last searcher | `run_task` | `notify_parked_local()` inside `transition_worker_from_searching` |
| Shutdown | `Handle::close` → `notify_all` | unparks *every* remote directly (no `Idle` bookkeeping) |
| Task dump | trace requested | `notify_all`; workers fix up state in `transition_from_parked` (`is_traced`) |

`notify_parked_local` vs `notify_parked_remote`: identical except the former
increments `counters::inc_num_inc_notify_local` / `inc_num_unparks_local`
(only relevant when `tokio_internal_mt_counters` is on) and returns a `bool`.

## 5. Waking up: `transition_from_parked`

When `Parker::park` returns, the worker must reconcile with `Idle`:

```text
has_tasks() or is_traced?
  yes -> is_searching = !unpark_worker_by_id(...)      // if we were still in sleepers (woken by I/O / local push),
                                                       // remove ourselves and DON'T claim "searching";
                                                       // if somebody already removed us (worker_to_notify) we are already counted searching
        return true
  no  -> if is_parked(...) { return false }             // spurious wake: still in sleepers -> go back to sleep (outer `while` in `park`)
         is_searching = true; return true               // someone popped us from sleepers -> they already counted us as searching
```

Important subtlety (comment in the code): "We do *not* want the worker to
transition to 'searching' when it wakes when the I/O driver receives new events."
A worker that was woken by the driver itself (it holds the driver and found
events) takes the `unpark_worker_by_id` path where `unpark_one(0)` only adds to
`num_unparked`.

## 6. Invariants

| # | Invariant |
|---|---|
| I1 | `num_searching ≤ num_unparked ≤ num_workers` (the `debug_assert!(prev.num_unparked() > 0)` and the packed layout) |
| I2 | A worker index is in `sleepers` iff it is parked and not yet claimed by a notifier (`debug_assert!(!sleepers.contains(&worker))` on park) |
| I3 | Every `unpark_one` is paired with exactly one `sleepers` removal under the same lock hold |
| I4 | A worker never parks while it has local tasks (`has_tasks()`), and the last searcher re-scans before sleeping |
| I5 | `num_searching` (16 bits) can't overflow because of the half-of-workers soft cap (<65 536 workers) |

## 7. Tests

`idle.rs::test_state` (mask sanity). Behaviour is exercised end-to-end by
`tokio/tests/rt_threaded.rs` and the loom models in
`runtime/tests/loom_multi_thread.rs` (`racy_shutdown`, `pool_multi_spawn`,
`pool_shutdown`, `pool_multi_notify`, `shutdown_with_notification`,
`complete_block_on_under_load`) and `loom_multi_thread/{queue,shutdown,yield_now}.rs`.

<!-- TESTS:idle -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/rt_threaded.rs`](../../../tokio/tests/rt_threaded.rs) | 31 | 700 |
| [`tokio/src/runtime/tests/loom_multi_thread.rs`](../../../tokio/src/runtime/tests/loom_multi_thread.rs) | 12 | 355 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

**Read next:** [09 — Parker](./09-parker.md)
