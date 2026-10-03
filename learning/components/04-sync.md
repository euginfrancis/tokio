# Block 4 — Sync (synchronization primitives)

> **Role:** let tasks **share state** and **pass messages** without ever blocking a thread: async locks, semaphores, notifications, channels and one-time cells.
> In the [component diagram](./README.md): the "sync" API box, with the arrow "wakes tasks directly". This is the only block that needs **no driver at all** — tasks wake each other through `Waker`s, so `tokio::sync` works under any executor.

---

## 1. At a glance

<!-- STATS:sync -->
| Metric | Value |
|---|---|
| Source files | 41 |
| Code lines | 9,135 (18.1% of `tokio/src`) |
| Doc + comment lines | 10,488 (1.15 per code line) |
| Functions | 755 — public API 249, trait impls 182, internal 210, inline tests 107 |
| `async fn` / `unsafe fn` | 39 / 34 |
| `unsafe` occurrences | 230 |
| Integration tests (`tokio/tests`) | 19 files, 361 test fns, 5,413 code lines |
<!-- /STATS -->

Second-largest public block, and the most heavily tested per line of code (several loom models per primitive).

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | `Mutex`, `RwLock`, `Semaphore` (+ owned/mapped guards), `Notify`, `Barrier`, `OnceCell`, `SetOnce`; channels `mpsc` (bounded + unbounded), `oneshot`, `broadcast`, `watch`; the internal **batch semaphore** and **`AtomicWaker`** that other blocks reuse. |
| **Does not own** | Scheduling or waking mechanics beyond calling `Waker::wake` ([Tasks](./01-tasks.md) / [Scheduler](./06-scheduler.md)); coop budget values (it *calls* `poll_proceed`). |
| **Input** | Task calls (`lock`, `send`, `recv`, `notified`, …) and `Waker`s from the polling task. |
| **Output** | `Waker::wake()` of other tasks; values handed between tasks. |
| **Reused by other blocks** | `batch_semaphore` (mpsc capacity, RwLock, OnceCell), `Notify` (watch, CurrentThread, many internals), `AtomicWaker` (mpsc receiver, timer `StateCell`, LocalSet), `watch` (signal delivery, Barrier). |

---

## 3. Files

<!-- FILES:sync -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/sync/mutex.rs`](../../tokio/src/sync/mutex.rs) | 634 | 667 | 6.9% |
| [`tokio/src/sync/broadcast.rs`](../../tokio/src/sync/broadcast.rs) | 619 | 1,000 | 6.8% |
| [`tokio/src/sync/notify.rs`](../../tokio/src/sync/notify.rs) | 594 | 672 | 6.5% |
| [`tokio/src/sync/oneshot.rs`](../../tokio/src/sync/oneshot.rs) | 552 | 934 | 6.0% |
| [`tokio/src/sync/batch_semaphore.rs`](../../tokio/src/sync/batch_semaphore.rs) | 543 | 143 | 5.9% |
| [`tokio/src/sync/rwlock.rs`](../../tokio/src/sync/rwlock.rs) | 505 | 538 | 5.5% |
| [`tokio/src/sync/watch.rs`](../../tokio/src/sync/watch.rs) | 469 | 968 | 5.1% |
| [`tokio/src/sync/mpsc/chan.rs`](../../tokio/src/sync/mpsc/chan.rs) | 431 | 83 | 4.7% |
| [`tokio/src/sync/mpsc/bounded.rs`](../../tokio/src/sync/mpsc/bounded.rs) | 413 | 1,451 | 4.5% |
| [`tokio/src/sync/semaphore.rs`](../../tokio/src/sync/semaphore.rs) | 313 | 1,046 | 3.4% |
| [`tokio/src/sync/mpsc/list.rs`](../../tokio/src/sync/mpsc/list.rs) | 238 | 143 | 2.6% |
| [`tokio/src/sync/mpsc/block.rs`](../../tokio/src/sync/mpsc/block.rs) | 229 | 173 | 2.5% |
| [`tokio/src/sync/once_cell.rs`](../../tokio/src/sync/once_cell.rs) | 229 | 239 | 2.5% |
| [`tokio/src/sync/rwlock/owned_write_guard.rs`](../../tokio/src/sync/rwlock/owned_write_guard.rs) | 225 | 204 | 2.5% |
| [`tokio/src/sync/tests/loom_notify.rs`](../../tokio/src/sync/tests/loom_notify.rs) | 224 | 41 | 2.5% |
| [`tokio/src/sync/tests/loom_mpsc.rs`](../../tokio/src/sync/tests/loom_mpsc.rs) | 221 | 0 | 2.4% |
| [`tokio/src/sync/tests/semaphore_batch.rs`](../../tokio/src/sync/tests/semaphore_batch.rs) | 218 | 12 | 2.4% |
| [`tokio/src/sync/rwlock/write_guard.rs`](../../tokio/src/sync/rwlock/write_guard.rs) | 217 | 210 | 2.4% |
| [`tokio/src/sync/tests/loom_semaphore_batch.rs`](../../tokio/src/sync/tests/loom_semaphore_batch.rs) | 196 | 3 | 2.1% |
| [`tokio/src/sync/mpsc/unbounded.rs`](../../tokio/src/sync/mpsc/unbounded.rs) | 186 | 493 | 2.0% |
| [`tokio/src/sync/tests/loom_broadcast.rs`](../../tokio/src/sync/tests/loom_broadcast.rs) | 168 | 2 | 1.8% |
| [`tokio/src/sync/tests/loom_oneshot.rs`](../../tokio/src/sync/tests/loom_oneshot.rs) | 155 | 18 | 1.7% |
| [`tokio/src/sync/set_once.rs`](../../tokio/src/sync/set_once.rs) | 151 | 201 | 1.7% |
| [`tokio/src/sync/task/atomic_waker.rs`](../../tokio/src/sync/task/atomic_waker.rs) | 146 | 202 | 1.6% |
| [`tokio/src/sync/barrier.rs`](../../tokio/src/sync/barrier.rs) | 124 | 71 | 1.4% |
| [`tokio/src/sync/mpsc/error.rs`](../../tokio/src/sync/mpsc/error.rs) | 116 | 24 | 1.3% |
| [`tokio/src/sync/rwlock/owned_write_guard_mapped.rs`](../../tokio/src/sync/rwlock/owned_write_guard_mapped.rs) | 116 | 99 | 1.3% |
| [`tokio/src/sync/rwlock/write_guard_mapped.rs`](../../tokio/src/sync/rwlock/write_guard_mapped.rs) | 110 | 88 | 1.2% |
| [`tokio/src/sync/rwlock/owned_read_guard.rs`](../../tokio/src/sync/rwlock/owned_read_guard.rs) | 103 | 91 | 1.1% |
| [`tokio/src/sync/rwlock/read_guard.rs`](../../tokio/src/sync/rwlock/read_guard.rs) | 98 | 80 | 1.1% |
| *…11 smaller files* | 592 | 592 | 6.5% |
| **Total (41 files)** | **9,135** | **10,488** | 100% |
<!-- /FILES -->

```
sync/
├── batch_semaphore.rs   ★ FIFO-fair semaphore with partial assignment — foundation of Mutex/RwLock/Semaphore/mpsc/OnceCell
├── mutex.rs, rwlock.rs + rwlock/ (6 guard types), semaphore.rs (public wrapper)
├── notify.rs            ★ Notify — the other foundation
├── task/atomic_waker.rs ★ AtomicWaker — lock-free single waker slot
├── mpsc/  bounded.rs, unbounded.rs (public); chan.rs (shared core); list.rs + block.rs (lock-free block list)
├── oneshot.rs, broadcast.rs, watch.rs
├── once_cell.rs, set_once.rs, barrier.rs
└── tests/               loom models: loom_mpsc, loom_notify, loom_semaphore_batch, loom_rwlock, loom_watch, …
```

---

## 4. Data structures

### Foundations
```rust
pub(crate) struct Semaphore {              // batch_semaphore.rs
    waiters: Mutex<Waitlist>,              // Waitlist { queue: LinkedList<Waiter>, closed: bool }
    permits: AtomicUsize,                  // available << 1 | CLOSED
}
struct Waiter {                            // lives INSIDE the Acquire future (intrusive, pinned)
    state: AtomicUsize,                    // permits still needed
    waker: UnsafeCell<Option<Waker>>,
    pointers: linked_list::Pointers<Waiter>,
}
pub struct Notify {                        // notify.rs
    state: AtomicUsize,                    // EMPTY | WAITING | NOTIFIED  + notify_waiters call counter
    waiters: Mutex<LinkedList<Waiter>>,    // Waiter { waker, notification: AtomicNotification, pointers }
}
pub(crate) struct AtomicWaker { state: AtomicUsize /* WAITING|REGISTERING|WAKING */, waker: UnsafeCell<Option<Waker>> }
```

### Locks (thin wrappers)
```rust
pub struct Mutex<T>  { s: batch_semaphore::Semaphore /* 1 permit */, c: UnsafeCell<T> }
pub struct RwLock<T> { mr: u32 /* max readers */, s: Semaphore /* mr permits */, c: UnsafeCell<T> }
pub struct Semaphore { ll_sem: batch_semaphore::Semaphore }
pub struct OnceCell<T> { value_set: AtomicBool, value: UnsafeCell<MaybeUninit<T>>, semaphore: Semaphore /* 1 permit, closed when set */ }
pub struct Barrier { state: Mutex<BarrierState { waker: watch::Sender<usize>, arrived, generation }>, wait: watch::Receiver<usize>, n }
```

### Channels
```rust
// mpsc — one shared Chan per channel
pub(super) struct Chan<T, S> {
    tx: CachePadded<list::Tx<T>>,          // tail_position: AtomicUsize + block_tail: AtomicPtr<Block<T>>
    rx_waker: CachePadded<AtomicWaker>,    // the single receiver's waker
    notify_rx_closed: Notify,              // Sender::closed().await
    semaphore: S,                          // bounded: (batch Semaphore, bound) | unbounded: AtomicUsize
    tx_count: AtomicUsize, tx_weak_count: AtomicUsize,
    rx_fields: UnsafeCell<RxFields<T>>,    // { list: list::Rx<T> (head block, index), rx_closed }
}
pub(crate) struct Block<T> {               // mpsc/block.rs — 32 slots (64-bit)
    header: BlockHeader { start_index, next: AtomicPtr<Block<T>>, ready_slots: AtomicUsize /* bitmap + RELEASED + TX_CLOSED */, observed_tail_position },
    values: [UnsafeCell<MaybeUninit<T>>; 32],
}

// oneshot
struct Inner<T> { state: AtomicUsize /* RX_TASK_SET|VALUE_SENT|CLOSED|TX_TASK_SET */, value: UnsafeCell<Option<T>>, tx_task: Task, rx_task: Task }

// broadcast — ring buffer
struct Shared<T> {
    buffer: Box<[Mutex<Slot<T>>]>,         // Slot { rem: usize /* receivers left */, pos: u64, val: Option<T> }
    mask: usize,                           // capacity - 1 (power of two)
    tail: Mutex<Tail>,                     // Tail { pos: u64, rx_cnt, closed, waiters: LinkedList<Waiter> }
    num_tx, num_weak_tx: AtomicUsize, notify_last_rx_drop: Notify,
}
pub struct Receiver<T> { shared: Arc<Shared<T>>, next: u64 }   // each receiver's own cursor

// watch — one value + version
struct Shared<T> {
    value: RwLock<T>,                      // std-style lock: readers borrow() briefly
    state: AtomicState,                    // version (step 2) | CLOSED bit
    ref_count_rx, ref_count_tx: AtomicUsize,
    notify_rx: BigNotify,                  // 8 Notify instances, receivers spread across them (less contention)
    notify_tx: Notify,                     // Sender::closed()
}
pub struct Receiver<T> { shared: Arc<Shared<T>>, version: Version }   // last version seen
```

---

## 5. How it interacts with the other blocks

```
 Task A: mutex.lock().await ─▶ Acquire { Waiter } ─▶ poll_acquire: CAS permits ── none ──▶ push Waiter, store waker, Pending
 Task B: drop(guard) ─▶ release(1) ─▶ add_permits_locked: assign to oldest waiter ─▶ WakeList ─▶ waker.wake() ─▶ [Tasks]/[Scheduler]
 Task A re-polled ─▶ Waiter satisfied ─▶ Ready(guard)

 tx.send(v).await ─▶ semaphore.acquire(1) ─▶ list.push (fetch_add slot, write, set ready bit) ─▶ rx_waker.wake()
 rx.recv().await  ─▶ coop::poll_proceed ─▶ list.pop ─▶ none? register rx_waker, pop again ─▶ Pending
                       value ─▶ semaphore.add_permit() ─▶ may wake a blocked sender
```

| Other block | Direction | Through |
|---|---|---|
| Tasks / Scheduler | → | `Waker::wake` only; `coop::poll_proceed` in every receive/acquire |
| Signal (fs/process/signal block) | ← | Each signal kind is a `watch` channel |
| Scheduler internals | ← | `Notify` (current-thread core hand-off), `AtomicWaker` |
| Timer driver | ← | `AtomicWaker` in each timer's `StateCell` |
| `tokio-util` | ← | `PollSemaphore`, `PollSender`, `CancellationToken` (builds its own tree) |
| `tokio-stream` | ← | `ReceiverStream`, `BroadcastStream`, `WatchStream` |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `Semaphore::acquire / acquire_many / try_acquire / add_permits / close / forget_permits / acquire_owned` | `semaphore.rs` → `batch_semaphore.rs` | Permits |
| `batch_semaphore::poll_acquire`, `add_permits_locked`, `Waiter::assign_permits`, `Drop for Acquire` | `batch_semaphore.rs` | Core algorithm (fast CAS path, FIFO queue, partial fills, cancel-safe give-back) |
| `Mutex::lock / try_lock / lock_owned / blocking_lock / get_mut / into_inner`, `MutexGuard::map` | `mutex.rs` | Async mutex |
| `RwLock::read / write / try_read / try_write / *_owned`, guard `map`/`downgrade` | `rwlock.rs` | Readers = 1 permit, writer = all |
| `Notify::notified / notify_one / notify_last / notify_waiters`, `Notified::enable` | `notify.rs` | Permit-or-wake notifications |
| `mpsc::channel(n) / unbounded_channel()` | `mpsc/bounded.rs`, `unbounded.rs` | Create |
| `Sender::send / try_send / reserve / reserve_many / send_timeout / blocking_send / closed / downgrade` | `mpsc/bounded.rs` | Send side |
| `Receiver::recv / recv_many / try_recv / blocking_recv / close / poll_recv` | `mpsc/bounded.rs` | Receive side |
| `chan::Tx::send`, `chan::Rx::recv`, `list::Tx::push / find_block`, `list::Rx::pop / reclaim_blocks` | `mpsc/chan.rs`, `list.rs` | Shared core + lock-free list |
| `oneshot::channel`, `Sender::send / closed / is_closed`, `Receiver::await / try_recv / close / blocking_recv` | `oneshot.rs` | One value |
| `broadcast::channel(n)`, `Sender::send / subscribe / receiver_count`, `Receiver::recv / try_recv / resubscribe` | `broadcast.rs` | Fan-out; `RecvError::Lagged(n)` |
| `watch::channel(v)`, `Sender::send / send_modify / send_if_modified / subscribe / closed`, `Receiver::borrow / borrow_and_update / changed / wait_for` | `watch.rs` | Latest value |
| `OnceCell::get_or_init / get_or_try_init / set / get`, `SetOnce::set / wait` | `once_cell.rs`, `set_once.rs` | One-time init |
| `Barrier::new(n) / wait` | `barrier.rs` | Rendezvous; one waiter is the "leader" |

---

## 7. Flows

**Fairness without starvation (semaphore):** while any waiter is queued, released permits go to the waiter queue first, so `permits` stays at 0 and a newcomer's CAS fast path fails → it queues behind. A writer needing all `MAX_READS` permits collects them gradually (partial assignment) and blocks later readers.

**Lost-wake-up prevention ("check, register, re-check"):** `mpsc::Rx::recv`, `oneshot` receive, `Notify`, `ScheduledIo` all try the operation, then register the waker, then try again before returning `Pending`.

**`Notify` permit semantics:** `notify_one()` with nobody waiting stores **one** permit (state `NOTIFIED`); the next `notified().await` completes immediately. `notify_waiters()` stores nothing and wakes only current waiters (it bumps a counter so already-created-but-not-yet-polled `Notified`s also see it).

**`broadcast` send:** lock tail → write value into `buffer[pos & mask]` (overwriting the oldest), set `rem = rx_cnt`, `pos += 1` → wake all waiting receivers. A receiver whose `next` is older than the oldest kept value gets `Lagged(n)` and jumps forward.

**`watch` send:** write-lock the value, replace, `state += 2` (version bump), `notify_rx.notify_waiters()` → each `changed()` compares its stored version with the shared one.

---

## 8. Invariants & gotchas

- **Never hold a `std::sync::Mutex` guard across `.await`**; `tokio::sync::Mutex` is designed for that but is slower — prefer std's if you don't await while locked.
- **Waiters are intrusive** (inside your future): dropping the future (cancellation) unlinks it under the lock and returns partially assigned permits.
- **Cancel safety:** `mpsc::Receiver::recv`, `broadcast::recv`, `watch::changed`, `Notified`, `Semaphore::acquire` are cancel-safe; `mpsc::Sender::send` is *not* (the value is lost if dropped mid-send — use `reserve()` first).
- **Bounded mpsc capacity is a semaphore**: `send` waits for a permit; the receiver returns one per received message.
- **Channel closure**: mpsc/broadcast close when all senders drop (`recv` → `None`/`Closed`); senders observe receiver drop through `closed()`/send errors.
- `blocking_*` variants panic if called from inside an async context.
- `RwLock` is **write-preferring** (fair FIFO), unlike `std`'s platform-dependent policy.

---

## 9. Tests & where to start

<!-- TESTS:sync -->
**19 integration test files · 361 test functions · 5,413 code lines**

[`sync_barrier.rs`](../../tokio/tests/sync_barrier.rs), [`sync_broadcast.rs`](../../tokio/tests/sync_broadcast.rs), [`sync_broadcast_weak.rs`](../../tokio/tests/sync_broadcast_weak.rs), [`sync_emscripten_blocking.rs`](../../tokio/tests/sync_emscripten_blocking.rs), [`sync_errors.rs`](../../tokio/tests/sync_errors.rs), [`sync_mpsc.rs`](../../tokio/tests/sync_mpsc.rs), [`sync_mpsc_weak.rs`](../../tokio/tests/sync_mpsc_weak.rs), [`sync_mutex.rs`](../../tokio/tests/sync_mutex.rs), [`sync_mutex_owned.rs`](../../tokio/tests/sync_mutex_owned.rs), [`sync_notify.rs`](../../tokio/tests/sync_notify.rs), [`sync_notify_owned.rs`](../../tokio/tests/sync_notify_owned.rs), [`sync_once_cell.rs`](../../tokio/tests/sync_once_cell.rs), [`sync_oneshot.rs`](../../tokio/tests/sync_oneshot.rs), [`sync_panic.rs`](../../tokio/tests/sync_panic.rs), [`sync_rwlock.rs`](../../tokio/tests/sync_rwlock.rs), [`sync_semaphore.rs`](../../tokio/tests/sync_semaphore.rs), [`sync_semaphore_owned.rs`](../../tokio/tests/sync_semaphore_owned.rs), [`sync_set_once.rs`](../../tokio/tests/sync_set_once.rs), [`sync_watch.rs`](../../tokio/tests/sync_watch.rs)
<!-- /TESTS -->

**Read in this order:** `oneshot.rs` (smallest complete channel) → `notify.rs` → `batch_semaphore.rs` (module doc) → `mutex.rs` (see how little it adds) → `mpsc/chan.rs` → `mpsc/list.rs` + `block.rs` → `broadcast.rs` → `watch.rs`.
**Contribution areas seen in history:** doc clarifications (lagging, cancel safety, drop behavior), small API additions (`downgrade`, `reserve_many`, getters), semaphore edge-case fixes, new loom tests.
