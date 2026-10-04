# Task component 6 — The Task Waker (`runtime/task/waker.rs`)

> **One sentence:** a task's `std::task::Waker` is a `RawWaker` whose data pointer *is* the task's `Header` pointer and whose vtable is one shared static of four tiny functions — so waking a task from any thread is "flip the `NOTIFIED` bit, and if it was idle, push a `Notified` to the scheduler stored inside the task".

It is the **entry point of every wake-up in Tokio**: sockets, timers, channels, locks, `JoinHandle`s — everything that says "poll me again" ends in this 124-line file.

---

## 1. Where it lives

<!-- FILES:t_waker -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/waker.rs`](../../../tokio/src/runtime/task/waker.rs) | 88 | 22 | 7 |
<!-- /FILES -->

---

## 2. Data types (DTOs)

```rust
pub(crate) struct WakerRef<'a, S: 'static> {          // a *borrowed* Waker
    waker: ManuallyDrop<Waker>,                        // never dropped ⇒ no ref-count decrement
    _p: PhantomData<(&'a Header, S)>,
}
static WAKER_VTABLE: RawWakerVTable = RawWakerVTable::new(clone_waker, wake_by_val, wake_by_ref, drop_waker);
fn raw_waker(header: NonNull<Header>) -> RawWaker { RawWaker::new(header.as_ptr() as *const (), &WAKER_VTABLE) }
```

| Piece | Value |
|---|---|
| `RawWaker.data` | the task's `*const Header` (the same address as the cell) |
| `RawWaker.vtable` | **one** process-wide `static WAKER_VTABLE` — *not* per `(T, S)` |
| Size of a `Waker` | 16 bytes (data + vtable pointers) — the std type; cloning it costs one `Relaxed` `fetch_add` |

### The four functions (all `unsafe fn(*const ())`)

| Function | Action | Ref-count | State-word transition | Then |
|---|---|---|---|---|
| `clone_waker(ptr)` | `header.state.ref_inc()`, return a new `RawWaker` with the same pointer | **+1** | – | – |
| `drop_waker(ptr)` | `RawTask::drop_reference` | **−1** (dealloc if last) | – | – |
| `wake_by_val(ptr)` (`Waker::wake(self)`) | `RawTask::wake_by_val` | consumes the waker's ref | `transition_to_notified_by_val` | `Submit` ⇒ `schedule()` through the vtable, then drop the ref |
| `wake_by_ref(ptr)` (`Waker::wake_by_ref`) | `RawTask::wake_by_ref` | none | `transition_to_notified_by_ref` | `Submit` ⇒ `schedule()` |

(With `tokio_unstable` + `tracing`, each function also emits a `tokio::task::waker` trace event carrying the task's tracing id: ops `waker.clone`, `waker.drop`, `waker.wake`, `waker.wake_by_ref`.)

---

## 3. `waker_ref`: the "free" waker handed to `Future::poll`

```rust
pub(super) fn waker_ref<S: Schedule>(header: &NonNull<Header>) -> WakerRef<'_, S> {
    let waker = unsafe { ManuallyDrop::new(Waker::from_raw(raw_waker(*header))) };
    WakerRef { waker, _p: PhantomData }
}
impl Deref for WakerRef<'_, S> { type Target = Waker; … }
```
`Harness::poll_inner` builds one of these for every poll and passes `&*waker_ref` to `Context::from_waker`. Because it is wrapped in `ManuallyDrop` and **never dropped**, polling a task does **not** touch the ref-count at all. The ref-count only moves when the future *clones* the waker to store it somewhere (a socket's `ScheduledIo`, a timer entry, a channel's waiter list, a `JoinHandle`...).

### Why a single static vtable matters
`Waker::will_wake(&other)` compares **both** the data pointer *and the vtable pointer*. If the vtable were generic (one per `(T, S)`), the compiler could emit different copies and `will_wake` would return `false` even for wakers of the same task (rust-lang/rust#66281). Using one `static` makes `will_wake` reliable, which Tokio relies on to *skip re-registering* wakers:

| Where `will_wake` / `clone_from` is used | Effect |
|---|---|
| `JoinHandle::poll` → `can_read_output` → `trailer.will_wake` (`harness.rs`) | polling the same `JoinHandle` repeatedly from the same task doesn't rewrite the join waker |
| `Defer::defer` (`scheduler/defer.rs`) | the **deferred-wake list** (used by `yield_now` and coop budget exhaustion) skips a waker equal to the last one queued |
| `ScheduledIo::poll_readiness` / `Readiness::poll` (`clone_from`) | re-polling a socket from the same task keeps the stored reader/writer waker |
| `batch_semaphore::poll_acquire`, `Notify`, `broadcast::Recv`, `oneshot` (both halves), `IdleNotifiedSet` | skip the clone + drop of the previous waker when the same task re-polls |

---

## 4. Control flow of a wake-up

```
 resource fires (epoll event / timer expiry / channel send / semaphore release / task finishing)
        │  Waker::wake() or wake_by_ref()         (any thread, any runtime, or no runtime at all)
        ▼
   waker.rs:  wake_by_val / wake_by_ref(ptr)
        ▼
   RawTask::wake_by_val / wake_by_ref   (harness.rs; NON-generic)
        ▼
   State::transition_to_notified_by_val / _by_ref          ← atomic CAS on the state word
        │
        ├── task RUNNING      → set NOTIFIED only. The thread polling it will reschedule it itself (OkNotified → yield_now)
        ├── task COMPLETE     → nothing (just drop the ref for by_val)
        ├── already NOTIFIED  → nothing   (a Notified is already queued → no duplicate)
        └── idle & !NOTIFIED  → set NOTIFIED, ref+1, return Submit
                │
                ▼
        RawTask::schedule()  →  vtable.schedule::<S>(ptr)
                ▼
        S::schedule(Notified(Task::from_raw(ptr)))         ← S read from the task via vtable.scheduler_offset
                ▼
        multi_thread: Handle::schedule_task(task, false)  → local LIFO / local queue, or inject queue + unpark
        current_thread: push_task, or inject + driver.unpark()
```

Note that the wake path **never takes a lock** in the task layer: one CAS, then the scheduler's own enqueue.

### `by_val` vs `by_ref` — why both exist
`Waker::wake(self)` consumes the waker; with `by_val` the harness can *reuse the waker's own reference* as the new `Notified`'s reference (`Submit` creates `+1` for the Notified, then the caller's `−1` is applied after `schedule`) — net zero traffic when the task was idle. `wake_by_ref` has to **add** a reference for the new `Notified` and keep the caller's. Hot paths (channel sends, I/O readiness) prefer `wake()` for this reason, and `ScheduledIo::wake`/`WakeList::wake_all` use it.

### The "Release store on already-notified" subtlety
`transition_to_notified_by_ref` on an already-`NOTIFIED` task writes the *same value back* (a CAS with an unchanged value). Without it a `wake_by_ref` that merely observes `NOTIFIED` would not *release* the data the waker's caller wrote (e.g. "I set the shared flag, then woke you"), and the later `Acquire` in `transition_to_running` would have nothing to synchronise with. That tiny no-op write is the memory-ordering fix.

---

## 5. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| [Harness](./04-harness.md) (`RawTask` impl) | waker → harness | `NonNull<Header>` → `wake_by_val/by_ref`, `drop_reference` |
| [State word](./01-state-word.md) | via harness; `clone_waker` calls `ref_inc` directly | `Transition*` enums |
| [Vtable](./03-rawtask-vtable.md) | harness → vtable.schedule | `NonNull<Header>` |
| Scheduler | → | `Notified<S>` through `Schedule::schedule` |
| Resource drivers (I/O, timer, sync) | → waker (they store clones and call `wake`) | `Waker` values (16 B), `WakeList` (32-slot stack array) |
| User futures | ← | `cx.waker()` returns `&Waker` (the `WakerRef`'s) |

---

## 6. Invariants & edge cases

1. A `Waker` is a *counted* reference: it keeps the task allocation alive even after the task finished and was removed from `OwnedTasks`. A stale waker is safe to wake (it will just decrement and maybe free).
2. A task's wakers are `Send + Sync` (the std `Waker` contract); correctness across threads comes entirely from the state word.
3. The waker handed to `poll` must **not** be dropped (it is `ManuallyDrop` for that reason); anything that needs to keep a waker must `clone()` it.
4. `wake()` after the runtime has shut down is safe: `schedule_task` finds no usable core/inject queue and the `Notified` is dropped (shutdown paths handle it, see [scheduler shutdown](../scheduler/12-shutdown.md)).
5. Waking from **inside** the task's own poll just sets `NOTIFIED`; the task is re-queued at the **back** (via `yield_now`) after the poll returns.

---

## 7. Tests

<!-- TESTS:t_waker -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

Exercised indirectly everywhere; directly by `task_combinations.rs`, loom models (`loom_oneshot`, `loom_multi_thread`), and `tokio/tests/task_*`/`sync_*`.

**Read next:** [07 — JoinHandle, AbortHandle & JoinError](./07-join-abort-error.md).
