# Task component 7 — `JoinHandle`, `AbortHandle`, `JoinError` (`runtime/task/{join,abort,error}.rs`)

> **One sentence:** these are the **user's remote controls** for a spawned task — await its result (`JoinHandle`), cancel it (`JoinHandle`/`AbortHandle`), and learn how it ended (`JoinError`: cancelled or panicked) — all implemented as thin typed wrappers around the same `RawTask` plus a small lock-free handshake over the `Trailer.waker` field.

---

## 1. Where it lives

<!-- FILES:t_join -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/join.rs`](../../../tokio/src/runtime/task/join.rs) | 79 | 278 | 9 |
| [`tokio/src/runtime/task/abort.rs`](../../../tokio/src/runtime/task/abort.rs) | 44 | 51 | 7 |
| [`tokio/src/runtime/task/error.rs`](../../../tokio/src/runtime/task/error.rs) | 99 | 80 | 11 |
| **Total (3 files)** | **222** | **409** | **27** |
<!-- /FILES -->

---

## 2. Data types (DTOs)

```rust
pub struct JoinHandle<T> { raw: RawTask, _p: PhantomData<T> }      // 8 bytes; owns 1 ref-count; the ONLY handle that can read the output
unsafe impl<T: Send> Send for JoinHandle<T> {}   unsafe impl<T: Send> Sync for JoinHandle<T> {}
impl<T> Unpin for JoinHandle<T> {}                                   // it is just a pointer: can be polled by `&mut` without pinning
impl<T> UnwindSafe / RefUnwindSafe for JoinHandle<T> {}

pub struct AbortHandle { raw: RawTask }                              // owns 1 ref-count; can only abort / inspect; Clone
unsafe impl Send + Sync for AbortHandle {}

pub struct JoinError { repr: Repr, id: Id }
enum Repr { Cancelled, Panic(SyncWrapper<Box<dyn Any + Send + 'static>>) }

pub(crate) struct SyncWrapper<T> { value: T }     // util/sync_wrapper.rs: `Send` if T: Send; **always `Sync`** because it exposes no `&T` access
```

### Why `SyncWrapper` around the panic payload
A panic payload is `Box<dyn Any + Send>` — `Send` but **not** `Sync`. `JoinError` is returned from `JoinHandle::poll` inside `Result<T, JoinError>` and users expect `JoinError: Send + Sync` (it implements `std::error::Error`, is stored in `Arc`s, `anyhow`, etc.). `SyncWrapper<T>` makes that sound: it is `Sync` unconditionally and exposes **no general `&T`**. The only ways in are `into_inner(self)` (ownership) and `downcast_ref_sync::<U: Any + Sync>(&self)` — a shared reference is handed out *only* if the payload is downcast to a type that is itself `Sync` (`String`, `&'static str` — exactly what `Display`/`Debug` need). If the downcast fails the payload is never touched.

### Types that cross these APIs
| Type | Direction | Meaning |
|---|---|---|
| `Poll<Result<T, JoinError>>` | `JoinHandle::poll` → user | the join result |
| `&Waker` | user → `try_read_output` | the awaiting task's waker (cloned into `Trailer.waker`) |
| `Id` | `JoinHandle::id`, `AbortHandle::id`, `JoinError::id` | the task's identity, read straight from the header via the vtable's `id_offset` (no state access) |
| `AbortHandle` | `JoinHandle::abort_handle()` | a second counted reference: `raw.ref_inc()` |

---

## 3. Interface (public + internal)

### `JoinHandle<T>`
| Method | Visibility | Implementation | State-word effect |
|---|---|---|---|
| `abort(&self)` | pub | `raw.remote_abort()` | `transition_to_notified_and_cancel` → maybe `schedule` |
| `is_finished(&self) -> bool` | pub | `state.load().is_complete()` | read-only |
| `abort_handle(&self) -> AbortHandle` | pub | `raw.ref_inc(); AbortHandle::new(raw)` | `ref_inc` |
| `id(&self) -> Id` | pub | `Header::get_id(raw.header_ptr())` | none |
| `impl Future::poll` | – | see §4 | `JOIN_WAKER` handshake |
| `set_join_waker(&mut self, &Waker)` | `pub(crate)` | `if raw.try_set_join_waker(waker) { waker.wake_by_ref() }` | handshake; **used only by `JoinSet`** (`join_set.rs:283`) so an `IdleNotifiedSet` entry can be woken without polling the handle |
| `impl Drop` | – | `drop_join_handle_fast()` else `drop_join_handle_slow()` | see §5 |

### `AbortHandle`
`abort()` (`remote_abort`), `is_finished()`, `id()`, `Clone` (`ref_inc`), `Drop` (→ `raw.drop_abort_handle()` → vtable → `Harness::drop_reference`). It **cannot** read the output and does not touch `JOIN_INTEREST`/`JOIN_WAKER`, so any number may exist next to one `JoinHandle`.

### `JoinError`
| Method | Meaning |
|---|---|
| `is_cancelled() / is_panic()` | which `Repr` |
| `into_panic() -> Box<dyn Any + Send>` (`#[track_caller]`, panics if cancelled) / `try_into_panic() -> Result<_, JoinError>` | recover the payload (e.g. to `resume_unwind`) |
| `id() -> Id` | the failed task |
| `Display` | `task {id} was cancelled` / `task {id} panicked with message "…"` (message only if the payload is a `String` or `&'static str`) |
| `Debug` | `JoinError::Cancelled(Id(n))` / `JoinError::Panic(Id(n), "msg", ...)` |
| `impl Error`, `From<JoinError> for io::Error` | → `io::Error::other("task was cancelled" / "task panicked")` — used by `fs::asyncify` |
| crate-internal `cancelled(id)`, `panic(id, payload)` | constructors used by the harness (`cancel_task`, `panic_to_error`) |

---

## 4. `JoinHandle::poll` — reading the result

```rust
fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
    ready!(crate::trace::trace_leaf());                       // task-dump instrumentation point
    let mut ret = Poll::Pending;
    let coop = ready!(crate::task::coop::poll_proceed(cx));   // awaiting a JoinHandle consumes 1 budget unit
    unsafe { self.raw.try_read_output(&mut ret, cx.waker()); }    // vtable → Harness::try_read_output
    if ret.is_ready() { coop.made_progress(); }               // keep the budget unit only if it succeeded
    ret
}
```
`try_read_output` → `can_read_output(header, trailer, waker)` ([04-harness](./04-harness.md) §6):
- **COMPLETE** → `*dst = Poll::Ready(core.take_output())` — the output is **moved out** of `Stage::Finished` (leaving `Consumed`). Polling again panics: *"JoinHandle polled after completion"*.
- else → store/refresh the join waker, `Pending`.

### The JOIN_WAKER handshake (task/mod.rs rules 1–7) as a protocol

Two parties share one field (`Trailer.waker`): the **JoinHandle** (writer, while the task runs) and the **runtime** (reader, when the task completes). The `JOIN_WAKER` bit says who may touch it:

| `JOIN_WAKER` | `COMPLETE` | `JOIN_INTEREST` | Who may access `waker` |
|---|---|---|---|
| 0 | 0 | 1 | **JoinHandle**, exclusive (write) |
| 1 | 0 | 1 | **JoinHandle**, shared (read only, e.g. `will_wake`) |
| 1 | 1 | 1 | **Runtime**, shared (read: wake it); JoinHandle must not change the bit any more |
| 0 | 1 | 1 | JoinHandle exclusive again (runtime finished waking and cleared the bit) |
| 0 | 1 | 0 | **Runtime**, exclusive — the handle is gone, so the runtime drops the waker |

Writer sequence for the JoinHandle (rule 5): `unset_waker` (if set) → write new waker → `set_join_waker`. If `COMPLETE` appears at any CAS, the step fails: the handle then clears its just-written waker and *returns Ready* (a race with completion is resolved in favour of reading the output).

```
 JoinHandle (poll)                                    Runtime (complete)
 ─────────────────                                    ──────────────────
 load: !COMPLETE, JW=0
 write waker into Trailer.waker
 CAS: set JW (fails if COMPLETE) ──────────────┐
                                               │          transition_to_complete  (sets COMPLETE)
  ok → Pending                                 │          snapshot: JI=1, JW=1 → read & wake the waker (rule 4)
                                               │          unset_waker_after_complete  (clears JW)
                                               └─ fail ─▶ if the handle was dropped meanwhile (JI=0): drop the waker ourselves
 next poll: COMPLETE → take_output
```

---

## 5. Dropping a `JoinHandle`

```rust
fn drop(&mut self) {
    if self.raw.state().drop_join_handle_fast().is_ok() { return; }   // 1 CAS: state was EXACTLY the initial state
    self.raw.drop_join_handle_slow();                                  // general case
}
```
- **Fast path**: the very common `tokio::spawn(fut);` (handle dropped immediately, never polled, task not yet run): state == `INITIAL_STATE` → CAS to `(INITIAL − REF_ONE) & !JOIN_INTEREST`. No vtable call, no waker, `Release` ordering only.
- **Slow path** (`Harness::drop_join_handle_slow`): `transition_to_join_handle_dropped` → `{drop_output, drop_waker}`:
  - task already complete → the handle must drop the stored output (it may be `!Send` ⇒ must happen on the handle's thread, not whichever thread frees the last ref) — panics from that drop are swallowed;
  - task not complete → clear `JOIN_WAKER` to regain exclusive access, then drop the waker;
  - finally `drop_reference()` (maybe dealloc).
- **Dropping detaches**: the task keeps running; its output will be dropped by the runtime at completion (`!snapshot.is_join_interested()` in `complete`).

---

## 6. Abort semantics

```
 handle.abort()  ──▶ raw.remote_abort() ──▶ transition_to_notified_and_cancel()
        ├ complete or already cancelled : no-op
        ├ running   : CANCELLED|NOTIFIED set; the polling thread sees CANCELLED at transition_to_idle → cancel_task → JoinError::Cancelled
        └ idle      : CANCELLED set, NOTIFIED set (+ref) → schedule(Notified)  → next poll attempt: transition_to_running = Cancelled
```
- **Cancellation is cooperative-at-poll-boundaries**: a future is never interrupted mid-poll; it is *dropped* at the next opportunity, and `await`ing the `JoinHandle` yields `Err(JoinError::Cancelled)` (or the panic payload if its destructor panicked).
- Aborting goes **through the scheduler** (not by dropping the future on the caller's thread) so a `!Send` future is dropped on its own thread.
- `is_finished()` becomes `true` once `COMPLETE` is set — i.e. after the future (or cancellation) finished — **not** when the output has been read.
- Blocking tasks (`spawn_blocking`) can only be aborted **before they start**; once the closure runs there's no poll boundary.

---

## 7. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| [Vtable/RawTask](./03-rawtask-vtable.md) | handle → | `try_read_output`, `drop_join_handle_slow`, `drop_abort_handle`, `remote_abort`, `ref_inc` |
| [State word](./01-state-word.md) | handle → | `drop_join_handle_fast`, `load().is_complete()` |
| [Harness](./04-harness.md) | via vtable | `can_read_output`, `take_output`, `complete` waking the join waker |
| Coop budget ([10](./10-coop-budget.md)) | handle → | `poll_proceed` in `poll` |
| `JoinSet` / `IdleNotifiedSet` (`task/join_set.rs`) | JoinSet → handle | owns many `JoinHandle<T>`; uses `Pin<&mut JoinHandle>.poll` and `set_join_waker` |
| `fs::asyncify`, `spawn_blocking` | → | `JoinError` → `io::Error` |
| Task dump (`trace`) | – | `trace_leaf()` marks the await point |

---

## 8. Invariants

1. Exactly **one** `JoinHandle` per task, holding exactly one ref-count and `JOIN_INTEREST`; `AbortHandle`s are additional refs without interest.
2. Only the `JoinHandle` may call `take_output`, and only after observing `COMPLETE`.
3. `JoinHandle<T>: Send` iff `T: Send` — so a `!Send` output can never be moved across threads by the handle.
4. A `JoinHandle` can be polled after `abort()`; it resolves to `Err(Cancelled)`.
5. Panics never cross the poll: `JoinError::Panic` is the only way a task's panic reaches user code (and `resume_unwind(err.into_panic())` re-throws it).

---

## 9. Tests

<!-- TESTS:t_join -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/tests/task_abort.rs`](../../../tokio/tests/task_abort.rs) | 8 | 226 |
| [`tokio/tests/task_join_set.rs`](../../../tokio/tests/task_join_set.rs) | 24 | 519 |
| [`tokio/tests/task_panic.rs`](../../../tokio/tests/task_panic.rs) | 7 | 94 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`tokio/tests/task_abort.rs` (abort semantics, panic payloads), `task_join_set.rs`, `rt_*` (JoinHandle across flavors), `runtime/tests/task.rs` (`drop_abort_handle*`, `create_drop*`), and the `task_combinations.rs` matrix.

**Read next:** [08 — OwnedTasks, ShardedList & the intrusive list](./08-owned-tasks.md).
