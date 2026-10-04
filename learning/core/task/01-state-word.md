# Task component 1 — The State Word (`runtime/task/state.rs`)

> **One sentence:** every task has a single `AtomicUsize` that packs *six flags and a reference count*; every lifecycle change is a compare-and-swap on that word that returns an enum telling the caller exactly what to do next.
> It is the **synchronisation backbone** of the task system: it is the lock around the future, the lifecycle state machine, the cancellation flag, the join-handle protocol, and the memory-management reference count — all in one machine word.

---

## 1. Where it lives

<!-- FILES:t_state -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/state.rs`](../../../tokio/src/runtime/task/state.rs) | 399 | 157 | 41 |
<!-- /FILES -->

Only **six other files** touch it — `harness.rs`, `waker.rs`, `join.rs`, `abort.rs`, `raw.rs` and `mod.rs` (handle drops + the task-dump hook) — and `core.rs` merely contains it in `Header`. Nothing outside `runtime/task/` can see `State` (`pub(super)`), which is what makes its invariants enforceable.

---

## 2. Bit layout

```
 bit:  63 ……………………………………………… 6 | 5         4           3             2         1         0
       ┌──────────────────────────┐ ┌─────────┬───────────┬─────────────┬─────────┬─────────┬─────────┐
       │   REFERENCE COUNT        │ │CANCELLED│ JOIN_WAKER│JOIN_INTEREST│ NOTIFIED│ COMPLETE│ RUNNING │
       │  (REF_ONE = 1 << 6)      │ │  0b100000│ 0b10000  │  0b1000     │  0b100  │  0b10   │  0b1    │
       └──────────────────────────┘ └─────────┴───────────┴─────────────┴─────────┴─────────┴─────────┘
                                                                            └── LIFECYCLE_MASK = 0b11 ─┘
 STATE_MASK     = 0b111111      (the six low bits)
 REF_COUNT_MASK = !STATE_MASK   REF_COUNT_SHIFT = 6   REF_ONE = 64
 INITIAL_STATE  = 3·REF_ONE | JOIN_INTEREST | NOTIFIED      (= 0b11_001100 = 204)
```

| Bit | Meaning | Set by | Cleared by | Used for |
|---|---|---|---|---|
| `RUNNING` | A thread is polling (or cancelling) the future right now | `transition_to_running`, `transition_to_shutdown` | `transition_to_idle`, `transition_to_complete` (XOR) | **Lock** around the future/output (`Stage`) |
| `COMPLETE` | The future finished (or was cancelled) and its output is stored | `transition_to_complete` | never | Terminal marker; hands `Stage` over to the `JoinHandle` |
| `NOTIFIED` | A `Notified` handle for this task exists (it is in a queue, or is about to be) | spawn (initial), any wake that submits | `transition_to_running` | Prevents *double scheduling*; detects "woken while running" |
| `JOIN_INTEREST` | A `JoinHandle` still exists | spawn (initial) | `JoinHandle` drop | Decides who drops the output |
| `JOIN_WAKER` | The `JoinHandle` stored a waker in `Trailer.waker` | `JoinHandle` (`set_join_waker`) | `JoinHandle` (`unset_waker`) or runtime after completion | **Access-control** for the waker field (see [06-waker](./06-waker.md) / [07-join](./07-join-abort-error.md)) |
| `CANCELLED` | The task must be cancelled at the next opportunity | `abort`, shutdown | never | Cancellation request |
| ref-count | Number of live handles to the allocation | see §5 | see §5 | Memory management |

**Derived lifecycle** (only two bits): `idle` = neither `RUNNING` nor `COMPLETE`; `running` = `RUNNING`; `complete` = `COMPLETE`. `RUNNING` and `COMPLETE` are **never both set** (`transition_to_complete` asserts it).

---

## 3. Data types (DTOs) in this component

```rust
pub(super) struct State { val: AtomicUsize }          // the shared word — lives in Header.state
#[derive(Copy, Clone)] pub(super) struct Snapshot(usize);   // a *value* copy of the word; all `is_*` queries are on this
type UpdateResult = Result<Snapshot, Snapshot>;       // Ok(new) | Err(current, unchanged)
```

Every transition returns a small `#[must_use]` enum — these are the **return DTOs** that carry the decision from the state machine to the harness:

| Enum | Variants | Meaning of each |
|---|---|---|
| `TransitionToRunning` | `Success` | Locked `RUNNING`; poll the future |
| | `Cancelled` | Locked `RUNNING` but `CANCELLED` was set → drop the future, store `JoinError::Cancelled`, complete |
| | `Failed` | Task is already running/complete elsewhere; **this `Notified`'s ref-count was consumed**; do nothing |
| | `Dealloc` | Same as `Failed`, and that was the last ref → free memory |
| `TransitionToIdle` | `Ok` | Back to idle, nobody woke it; the poll's ref-count was consumed |
| | `OkNotified` | Woken *during* the poll → a **new** ref-count for a fresh `Notified` was created; caller must reschedule |
| | `OkDealloc` | Idle and that was the last ref → free |
| | `Cancelled` | `CANCELLED` seen → state **unchanged**, caller cancels (it still holds `RUNNING`) |
| `TransitionToNotifiedByVal` | `DoNothing` / `Submit` / `Dealloc` | wake that *consumes* the caller's ref: submit a `Notified`, drop silently, or free |
| `TransitionToNotifiedByRef` | `DoNothing` / `Submit` | wake that *borrows* the caller's ref |
| `TransitionToJoinHandleDrop` | `{ drop_waker: bool, drop_output: bool }` | what the dropping `JoinHandle` must clean up |

---

## 4. The transition table (every state-changing function)

Notation: `R`=RUNNING `C`=COMPLETE `N`=NOTIFIED `JI`=JOIN_INTEREST `JW`=JOIN_WAKER `X`=CANCELLED. All are CAS loops via `fetch_update_action`/`fetch_update` (`AcqRel` on success, `Acquire` on failure) unless noted.

| Function | Precondition | Effect on bits | Ref-count effect | Returns | Called by |
|---|---|---|---|---|---|
| `new()` | – | `INITIAL_STATE` | 3 | – | `RawTask::new` |
| `transition_to_running` | `N` set (asserted) | idle: `+R −N` | none | `Success` / `Cancelled` (if `X`) | `Harness::poll_inner` |
| | | not idle (`R` or `C`): – | **−1** (the Notified's) | `Failed` / `Dealloc` (if 0) | |
| `transition_to_idle` | `R` set (asserted) | `X` set: *no change* | none | `Cancelled` | `Harness::poll_inner` |
| | | else `−R` and `N` clear | **−1** (poll's ref) | `Ok` / `OkDealloc` | |
| | | else `−R` and `N` set | **+1** (new Notified; caller keeps its own, drops it after rescheduling) | `OkNotified` | |
| `transition_to_complete` | `R`, `!C` (asserted) | `fetch_xor(R\|C)` — atomic flip | none | `Snapshot` after flip | `Harness::complete` |
| `transition_to_terminal(n)` | – | – | **−n** | `true` if now 0 | `Harness::complete` |
| `transition_to_notified_by_val` | caller owns a ref | `R`: set `N` | −1 | `DoNothing` | `RawTask::wake_by_val` (a `Waker::wake`) |
| | | `C` or `N` already: – | −1 | `DoNothing` / `Dealloc` | |
| | | idle & `!N`: set `N` | **+1** (net 0: ref moves to the new `Notified`) | `Submit` | |
| `transition_to_notified_by_ref` | caller holds a ref | `C`: no write | – | `DoNothing` | `RawTask::wake_by_ref` |
| | | `N`: **writes the same value** (Release store, pairs with Acquire in `transition_to_running`) | – | `DoNothing` | |
| | | `R`: set `N` | – | `DoNothing` | |
| | | idle & `!N`: set `N` | +1 | `Submit` | |
| `transition_to_notified_and_cancel` | – | `X` or `C`: nothing | – | `false` | `RawTask::remote_abort` (`JoinHandle::abort`, `AbortHandle::abort`) |
| | | `R`: set `N\|X` | – | `false` (the polling thread will notice `X`) | |
| | | idle: set `X`; if `!N` set `N` | +1 if `N` was newly set | `true` iff newly notified | |
| `transition_to_shutdown` | – | always set `X`; if idle also set `R` | – | `true` iff it was idle (caller now holds the lock and must drop the future) | `Harness::shutdown` |
| `drop_join_handle_fast` | state `== INITIAL_STATE` exactly | CAS → `(INITIAL − REF_ONE) & !JI` | −1 | `Ok`/`Err` | `JoinHandle::drop` |
| `transition_to_join_handle_dropped` | `JI` set | clear `JI`; if `!C` also clear `JW` | – | `{drop_waker, drop_output}` | `Harness::drop_join_handle_slow` |
| `set_join_waker` | `JI`, `!JW` (asserted) | set `JW` unless `C` | – | `Ok(new)` / `Err(current)` | `can_read_output` |
| `unset_waker` | `JI`, `JW` (asserted) | clear `JW` unless `C` | – | `Ok`/`Err` | `can_read_output` |
| `unset_waker_after_complete` | `C`, `JW` (asserted) | `fetch_and(!JW)` | – | `Snapshot` | `Harness::complete` |
| `ref_inc` | – | – | `fetch_add(REF_ONE, Relaxed)`; **abort the process** if it had exceeded `isize::MAX` | – | `clone_waker`, `AbortHandle::clone`, `JoinHandle::abort_handle`, `UnownedTask::into_task` |
| `ref_dec` | count ≥ 1 | – | `fetch_sub(REF_ONE, AcqRel)` | `true` if it was 1 | `Task::drop`, `drop_reference`, waker drop |
| `ref_dec_twice` | count ≥ 2 | – | `fetch_sub(2·REF_ONE)` | `true` if it was 2 | `UnownedTask::drop` |

### The lifecycle state machine

```
                        spawn: refs=3, N, JI
                               │
                               ▼
        ┌──────────────── IDLE+N  (a Notified is queued) ◀─────────────────────────────┐
        │                      │ transition_to_running  (clears N, sets R)             │
        │                      ▼                                                       │
        │                  RUNNING ──poll Ready──▶ transition_to_complete ──▶ COMPLETE (terminal)
        │                      │                                                       ▲
        │       poll Pending   │ woken during poll → N set by wake                     │
        │            ┌─────────┴───────────┐                                           │
        │            ▼                     ▼                                           │
        │   transition_to_idle        transition_to_idle                               │
        │    N clear: refs−1           N set: refs+1                                   │
        │        IDLE (waiting)         OkNotified ──▶ yield_now(Notified) ───────────┘ (back to a queue)
        │            │ wake (by val/ref): idle & !N → set N, refs+1, Submit ──▶ schedule(Notified)
        │            └──────────────────────────────────────────────────────────▶ IDLE+N
        │
        └── abort / shutdown at any point: CANCELLED is set; the next time the lock is taken
            (transition_to_running → Cancelled, transition_to_idle → Cancelled, or transition_to_shutdown)
            the future is dropped, JoinError::Cancelled is stored and the task goes to COMPLETE.
```

---

## 5. Reference-count ownership ledger

Every `+1` in the table corresponds to creating a *new typed handle*; every `−1` to dropping one. Which handle holds which reference:

| Holder | Count | Created by | Dropped by |
|---|---:|---|---|
| `Task` stored in `OwnedTasks`/`LocalOwnedTasks` | 1 | `new_task` | `Scheduler::release` during `complete` (returned task is `forget`-ed and counted as 1 of the `transition_to_terminal(n)`) |
| `Notified` (in a queue, or being polled) | 1 | `new_task`; every `Submit` | consumed by `transition_to_running` (`Failed`/`Dealloc`) **or** carried through the poll and consumed by `transition_to_idle` / `complete` |
| `JoinHandle` | 1 | `new_task` | `JoinHandle::drop` |
| each `Waker` clone | 1 each | `clone_waker` | `drop_waker` / `wake_by_val` |
| each `AbortHandle` | 1 each | `JoinHandle::abort_handle`, `AbortHandle::clone` | `AbortHandle::drop` |
| `UnownedTask` (blocking pool) | 2 | `unowned()` | `UnownedTask::drop` (`ref_dec_twice`) |

### Worked example: a task that sleeps once and finishes

| Step | Event | Flags after | Refs | Who holds them |
|---|---|---|---:|---|
| 1 | `spawn` → `new_task` | `N JI` | **3** | list, Notified, JoinHandle |
| 2 | worker `transition_to_running` | `R JI` | 3 | list, *poll* (ex-Notified), JoinHandle |
| 3 | future calls `sleep`, timer clones the waker | `R JI` | 4 | + timer's waker |
| 4 | poll → `Pending`; `transition_to_idle` (no `N`) | `JI` | 3 | list, JoinHandle, timer waker |
| 5 | timer fires `wake_by_val` → `Submit` (`+1`, then caller drops its waker `−1`) | `N JI` | 3 | list, JoinHandle, **new Notified** |
| 6 | worker `transition_to_running` | `R JI` | 3 | list, poll, JoinHandle |
| 7 | poll → `Ready`; output stored; `transition_to_complete` (XOR) | `C JI` | 3 | |
| 8 | `JoinHandle` had registered a waker (`JW`) → woken; `unset_waker_after_complete` | `C JI` | 3 | |
| 9 | `release()` removes from `OwnedTasks` → `transition_to_terminal(2)` | `C JI` | **1** | JoinHandle |
| 10 | `JoinHandle` awaited: `take_output`; handle dropped → `drop_join_handle_slow` → `ref_dec` → **0 → dealloc** | – | 0 | – |

---

## 6. Memory ordering

| Operation | Ordering | Why |
|---|---|---|
| `load` | `Acquire` | See everything the last RMW published |
| all `fetch_update*` (CAS) | `AcqRel` / `Acquire` on failure | Each transition is both a *release* of this thread's work (e.g. finished polling) and an *acquire* of the previous owner's work |
| `transition_to_complete` | `fetch_xor` `AcqRel` | Publishes the stored output to the `JoinHandle` |
| `ref_inc` | **`Relaxed`** | New refs can only be made from an existing ref, which already provides the needed synchronisation (same argument as `Arc::clone`) |
| `ref_dec` | `AcqRel` | The thread dropping the last ref must observe all writes by earlier droppers before freeing |
| `drop_join_handle_fast` | `Release` / `Relaxed` | If it succeeds nothing else ever touched the task through the join handle |
| `wake_by_ref` on already-`NOTIFIED` | writes the same value back (CAS) | A *Release* so that the wake "synchronises-with" the later `Acquire` in `transition_to_running` — otherwise data written before `wake()` could be invisible to the poll |

---

## 7. Communication: who uses the state word and with what

| Caller (component) | Calls | Data crossing the boundary | Direction |
|---|---|---|---|
| [Harness](./04-harness.md) | `transition_to_running/idle/complete/terminal/shutdown`, `transition_to_notified_by_val/ref/and_cancel`, `transition_to_join_handle_dropped`, `set_join_waker`, `unset_waker*`, `ref_dec` | returns the `Transition*` enums and `Snapshot` | harness → state (request) / state → harness (decision) |
| [Waker](./06-waker.md) | `ref_inc` (clone), via `RawTask::wake_*`/`drop_reference` | – | waker → state |
| [JoinHandle / AbortHandle](./07-join-abort-error.md) | `drop_join_handle_fast`, `load().is_complete()`, `ref_inc` | `bool`s | handle → state |
| [Handles](./05-handles-and-schedule.md) | `ref_dec` on `Task::drop`, `ref_dec_twice` on `UnownedTask::drop`, `ref_inc` on `into_task` | – | handle → state |
| `Header` ([cell layout](./02-cell-layout.md)) | owns the `State` as its first field | – | containment |

**Boundary rule:** the state word never calls out. It does not know about schedulers, futures or wakers; it only answers "given the current word, what is the next word and what must the caller do?".

---

## 8. Invariants

1. `RUNNING` ⇒ exactly one thread may access `Stage` (the future/output). `COMPLETE` ⇒ the `JoinHandle` (or, if `JI` is clear, the completing thread) owns the output.
2. `RUNNING` and `COMPLETE` are never both set. `COMPLETE` is never cleared.
3. `NOTIFIED` set ⇔ exactly one `Notified` ref exists (queued, or held by the thread about to poll / reschedule). A second one is never created while it is set → a task is **never in two queues**.
4. Ref-count ≥ 1 until the single `dealloc`; `REF_COUNT` never underflows (asserted); overflow aborts the process.
5. `JOIN_WAKER` may only be changed by the `JoinHandle` while `COMPLETE` is clear, and only by the runtime once `COMPLETE` is set.
6. `CANCELLED` is monotone (never cleared) and `abort()` of a `COMPLETE` task is a no-op.

---

## 9. Edge cases worth knowing

- **Wake after complete:** `transition_to_notified_by_val` on a complete task just drops the ref (maybe freeing the task). Stale wakers are harmless.
- **Wake while running:** only `NOTIFIED` is set; the *running thread* reschedules it when it hits `transition_to_idle` (`OkNotified`). This is why a self-waking future (`cx.waker().wake_by_ref(); Pending`) is requeued rather than spun.
- **`Notified` for a task that has already completed** (e.g. shutdown completed it while a `Notified` sat in a queue): `transition_to_running` sees "not idle", drops that ref, returns `Failed` — a benign no-op.
- **`abort()` during poll:** `CANCELLED|NOTIFIED` set; the poll finishes normally, `transition_to_idle` returns `Cancelled`, the harness then drops the future and completes with `JoinError::Cancelled` (the poll's *output is discarded*).

---

## 10. Tests

<!-- TESTS:t_state -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| [`tokio/src/runtime/tests/task_combinations.rs`](../../../tokio/src/runtime/tests/task_combinations.rs) | 1 | 404 |
| [`tokio/tests/task_abort.rs`](../../../tokio/tests/task_abort.rs) | 8 | 226 |
| [`tokio/tests/task_join_set.rs`](../../../tokio/tests/task_join_set.rs) | 24 | 519 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

State-word logic is exercised through `runtime/tests/task.rs` (spawn/abort/shutdown/drop combinations), `task_combinations.rs` (all interleavings of join-handle drop, abort, completion), the loom models (`loom_join_set.rs`, `loom_local.rs`, `loom_multi_thread/*`), and `tokio/tests/task_abort.rs`, `task_join_set.rs`.

**Read next:** [Harness](./04-harness.md), which is the only large consumer of these transitions.
