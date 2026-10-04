# Task component 4 — The Harness (`runtime/task/harness.rs`)

> **One sentence:** the `Harness<T, S>` is the *typed* engine of a task — it turns state-word decisions into actions: it polls the future under the `RUNNING` lock with panics caught, completes or cancels the task, runs the wake/abort/join-handle protocols, and decides when the memory is freed.

If the [state word](./01-state-word.md) answers *"what may I do?"*, the harness is the code that *does it*; the [vtable](./03-rawtask-vtable.md) is how the rest of the runtime reaches it.

---

## 1. Where it lives

<!-- FILES:t_harness -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/harness.rs`](../../../tokio/src/runtime/task/harness.rs) | 318 | 186 | 29 |
<!-- /FILES -->

Two `impl` blocks matter:

| Block | Methods | Generic over | Why |
|---|---|---|---|
| `impl RawTask` (non-generic) | `drop_reference`, `wake_by_val`, `wake_by_ref`, `remote_abort`, `try_set_join_waker` | nothing | Only the state word + one vtable call are needed → **one copy in the binary** |
| `impl<T: Future, S: Schedule> Harness<T, S>` | `poll`, `poll_inner`, `shutdown`, `dealloc`, `try_read_output`, `drop_join_handle_slow`, `complete`, `release`, `get_new_task`, `drop_reference` | `T`, `S` | Touch `Stage<T>`, call `S::release/yield_now/unhandled_panic` |

Free functions: `poll_future`, `cancel_task`, `can_read_output`, `set_join_waker`, `panic_to_error`, `panic_result_to_join_error`.

---

## 2. Data types (DTOs)

```rust
pub(super) struct Harness<T: Future, S: 'static> { cell: NonNull<Cell<T, S>> }   // a typed view; Copy-like, no ownership

enum PollFuture { Complete, Notified, Done, Dealloc }     // result of poll_inner (private)
```

| `PollFuture` | Produced when | What `Harness::poll` then does | Ref-counts the caller owns |
|---|---|---|---|
| `Done` | idle again, or the lock was not obtained (`Failed`) | nothing | 0 (consumed) |
| `Notified` | woken during the poll (`OkNotified`) | `scheduler.yield_now(Notified(get_new_task()))`, then `drop_reference()` | 2 |
| `Complete` | future returned `Ready`, or was cancelled | `complete()` | 1 |
| `Dealloc` | that was the last ref-count | `dealloc()` | 0 (freed) |

Inputs from the other components: `Core<T,S>` (stage, scheduler, id), `Trailer` (join waker, hooks), `State` transitions + `Snapshot`s, `&Waker` (from the `JoinHandle`).
Outputs: side effects only — future dropped/polled, output stored, wakers woken, scheduler asked to `schedule`/`yield_now`/`release`, memory freed.

---

## 3. The interfaces it *requires* from the scheduler (`Schedule`)

```rust
pub(crate) trait Schedule: Sync + Sized + 'static {
    fn release(&self, task: &Task<Self>) -> Option<Task<Self>>;     // called by complete()
    fn schedule(&self, task: Notified<Self>);                       // called via the vtable on wake
    fn hooks(&self) -> TaskHarnessScheduleHooks;                    // called once, by Cell::new
    fn yield_now(&self, task: Notified<Self>) { self.schedule(task) }   // called by poll() for OkNotified
    fn unhandled_panic(&self) {}                                    // called when a poll/drop panics
}
```
Full contract in [05 — Handles & Schedule](./05-handles-and-schedule.md).

---

## 4. `Harness::poll` — the heart (annotated)

```rust
pub(super) fn poll(self) {                     // consumes one ref-count (the Notified's)
    match self.poll_inner() {
        PollFuture::Notified => {              // woken during poll: we were given TWO refs back
            self.core().scheduler.yield_now(Notified(self.get_new_task()));   // one goes to the new Notified
            self.drop_reference();             // the other is dropped only AFTER yield_now returns, so the
        }                                      // task can't be freed if yield_now drops the Notified
        PollFuture::Complete => self.complete(),
        PollFuture::Dealloc  => self.dealloc(),
        PollFuture::Done     => (),
    }
}

fn poll_inner(&self) -> PollFuture {
    match self.state().transition_to_running() {                  // CAS: take the lock
        Success => {
            let waker_ref = waker_ref::<S>(&self.header_ptr());   // a Waker borrowed from the header — NO ref_inc
            let res = poll_future(self.core(), Context::from_waker(&waker_ref));
            if res == Poll::Ready(()) { return PollFuture::Complete; }     // output already stored by poll_future
            match self.state().transition_to_idle() {             // give the lock back
                Ok          => Done,
                OkNotified  => Notified,
                OkDealloc   => Dealloc,
                Cancelled   => { cancel_task(self.core()); Complete }      // abort() raced with this poll
            }
        }
        Cancelled => { cancel_task(self.core()); Complete }       // abort/shutdown before we even started
        Failed    => Done,
        Dealloc   => Dealloc,
    }
}
```

### `poll_future` — panic isolation
```rust
let output = catch_unwind(|| {
    let guard = Guard { core };            // Drop = core.drop_future_or_output()
    let res = guard.core.poll(cx);         // Core::poll → future.poll(&mut cx) under TaskIdGuard
    mem::forget(guard);                    // no panic → disarm
    res
});
match output {
    Ok(Pending)   => return Pending,
    Ok(Ready(v))  => store Ok(v),
    Err(panic)    => store Err(panic_to_error(..))     // scheduler.unhandled_panic() + JoinError::panic(id, payload)
}
catch_unwind(|| core.store_output(output))              // storing/dropping the old stage may itself panic (a Drop impl)
if that panicked { core.scheduler.unhandled_panic() }
Ready(())
```
If the future panics, the **guard drops the future inside the `catch_unwind`** so its destructors run with the panic contained; the payload is wrapped in a `JoinError` and returned through the `JoinHandle`. The worker thread never unwinds.

---

## 5. `complete()` — finishing a task

```
complete(self):                       // precondition: RUNNING is held; output (or error) is in Stage::Finished
  snapshot = transition_to_complete()                // RUNNING→COMPLETE via XOR
  catch_unwind {
     if !snapshot.is_join_interested():  core.drop_future_or_output()     // nobody wants the output → drop it HERE (maybe !Send)
     else if snapshot.is_join_waker_set():
          trailer.wake_join()                                              // read-only access: JOIN_WAKER && COMPLETE (rule 4)
          if !state.unset_waker_after_complete().is_join_interested():     // hand the waker field back to the JoinHandle…
               trailer.set_waker(None)                                     // …unless it was dropped meanwhile: then we drop the waker
  }
  [tokio_unstable] task_terminate_callback(&TaskMeta{id, spawned_at, …}) inside catch_unwind
  num_release = self.release()                       // scheduler.release(task): 2 if it removed the task from its list, else 1
  if state.transition_to_terminal(num_release) { self.dealloc() }
```
Order matters: the join waker is woken **after** `COMPLETE` is published and **before** the scheduler's reference is dropped, and the `task_terminate` hook runs when the task *appears* complete but before it may be freed.

### `release()`
```rust
let me = ManuallyDrop::new(self.get_new_task());        // a Task handle WITHOUT a ref-count bump
if let Some(task) = self.core().scheduler.release(&me) { mem::forget(task); 2 } else { 1 }
```
`Schedule::release` returns the `Task` that was stored in the owner list (its removal frees the list's reference). The harness `forget`s it and accounts for it as the extra `2nd` decrement in `transition_to_terminal`.

---

## 6. The other operations

| Operation | Called when | Algorithm |
|---|---|---|
| `wake_by_val` | `Waker::wake(self)` | `transition_to_notified_by_val` → `Submit`: `schedule()`, **then** `drop_reference()` (keep the ref alive across `schedule` in case it drops the `Notified`); `Dealloc`: free; `DoNothing` |
| `wake_by_ref` | `Waker::wake_by_ref` | `transition_to_notified_by_ref` → `Submit`: `schedule()` (the caller's ref keeps the task alive) |
| `remote_abort` | `JoinHandle::abort`, `AbortHandle::abort` | `transition_to_notified_and_cancel` → `true`: `schedule()` so **the runtime** (right thread) cancels it |
| `shutdown` | `Task::shutdown` (runtime teardown) | `transition_to_shutdown`: if it was **not** idle → the polling thread will see `CANCELLED`; `drop_reference` and return. If idle → we now hold `RUNNING`: `cancel_task` then `complete` |
| `try_read_output` | `JoinHandle::poll` | `can_read_output(...)` → if complete: `*dst = Poll::Ready(core.take_output())` |
| `drop_join_handle_slow` | `JoinHandle::drop` (non-trivial state) | `transition_to_join_handle_dropped` → maybe `drop_future_or_output` (in `catch_unwind`: panics are swallowed because the user dropped interest), maybe `set_waker(None)`, then `drop_reference` |
| `dealloc` | last ref-count | touch `waker`/`stage` with `with_mut` (so loom sees exclusive access), then `drop(Box::from_raw(cell))` |
| `cancel_task` | any cancel path | `catch_unwind(drop_future_or_output)`, then `store_output(Err(JoinError::cancelled(id) or ::panic(id, payload_from_drop)))` |

### `can_read_output` — the `JOIN_WAKER` protocol (task/mod.rs rules 1–7)
```
snapshot = state.load()
if COMPLETE:                    return true                         // caller may take_output
if JOIN_WAKER is set:           // a waker is stored, JoinHandle has shared (read) access
     if trailer.will_wake(new): return false                        // same task → leave it
     unset_waker() ──▶ set_join_waker(clone)                        // rule 5: clear JW, write, set JW
else:                           // JW clear → JoinHandle has exclusive access
     set_join_waker(clone)
on Err(snapshot) → snapshot is COMPLETE (a race) → return true
```
`set_join_waker()` writes the waker into `Trailer.waker` **first**, then sets `JOIN_WAKER`; if the CAS fails because `COMPLETE` appeared, it clears the waker again.

---

## 7. Communication with other components

| Peer | Direction | What crosses | Mechanism |
|---|---|---|---|
| [State word](./01-state-word.md) | harness → state | transition requests; ← `Transition*`, `Snapshot` | direct calls |
| [Cell](./02-cell-layout.md) | harness ↔ cell | `Stage<T>`, `Trailer.waker`, scheduler, id | `NonNull<Cell<T,S>>` |
| [Vtable](./03-rawtask-vtable.md) | vtable → harness | `NonNull<Header>` → `Harness::from_raw` | fn pointers |
| Scheduler | harness → scheduler | `Notified<S>` (`schedule`, `yield_now`), `&Task<S>` (`release`), `()` (`unhandled_panic`) | the `Schedule` trait on `Core.scheduler` |
| [Waker](./06-waker.md) | waker → harness | `RawTask::wake_by_val/by_ref`, `drop_reference` | direct |
| [JoinHandle](./07-join-abort-error.md) | handle → harness | `try_read_output(dst, &Waker)`, `drop_join_handle_slow`, `remote_abort` | vtable |
| User code (the future) | harness → future | `Context<'_>` containing the task's `Waker` | `Future::poll` |
| Runtime context | harness → context | `CONTEXT.current_task_id` | `TaskIdGuard` |
| Hooks | harness → user | `&TaskMeta` | `Trailer.hooks.task_terminate_callback` (unstable) |

---

## 8. Panic and unwind policy

| Where a panic can happen | Handling | Result |
|---|---|---|
| `Future::poll` | caught in `poll_future`; future dropped by the guard; `scheduler.unhandled_panic()` | `JoinError::Panic(payload)` stored as the output |
| Drop of the *future* when cancelling | caught in `cancel_task` | `JoinError::panic(payload)` instead of `cancelled` |
| Drop of the *output* (`store_output` replacing the old stage) | caught | `scheduler.unhandled_panic()` |
| Drop of the output in `drop_join_handle_slow` | caught & **swallowed** | (user dropped interest) |
| Waking the join waker / dropping the output in `complete` | caught in one `catch_unwind` | ignored — completion proceeds |
| `task_terminate` hook | caught | ignored |

`Schedule::unhandled_panic` is how the *runtime-level* policy (`Builder::unhandled_panic(UnhandledPanic::ShutdownRuntime)`, `tokio_unstable`) is implemented. The trait default is a no-op ("maintains the 1.0 behavior"); **only the current-thread scheduler and `LocalSet` override it** (`scheduler/current_thread/mod.rs`, `task/local.rs`): with `ShutdownRuntime` they set an `unhandled_panic` flag and call `close_and_shutdown_all`, and the current-thread `block_on` loop then exits and panics. The multi-thread scheduler and the blocking pool keep the no-op default.

---

## 9. Invariants & subtle points

1. **Ref-count ownership is explicit in comments and return values**: `poll` consumes one; `PollFuture::Notified` hands back two; `Complete` hands back one for `complete` to feed into `transition_to_terminal`.
2. `schedule()` is always called *while the caller still holds a reference*, because `schedule` may drop the `Notified` it is given (e.g. runtime shut down).
3. `complete()` assumes `RUNNING` is held and `Stage` holds the output/error.
4. The harness never frees memory except through `ref_dec`/`transition_to_terminal` returning `true`.
5. `yield_now` (not `schedule`) is used for a task woken *while polling*, so schedulers can put it at the **back** of the queue (and not in the LIFO slot) — see [scheduler worker loop](../scheduler/05-worker-loop.md).
6. A `Notified` for an already-finished task is harmless (`Failed`/`Dealloc`).

---

## 10. Tests

<!-- TESTS:t_harness -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| [`tokio/src/runtime/tests/task_combinations.rs`](../../../tokio/src/runtime/tests/task_combinations.rs) | 1 | 404 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`runtime/tests/task.rs` (create/drop/abort-handle/shutdown permutations with a minimal scheduler), `task_combinations.rs` (a matrix over runtime flavor {current-thread, 2 multi-thread configs} × `LocalSet` {yes, no} × task behavior {panic on run / on drop / both / none} × output {panic on drop / none} × join interest {polled / not} × join-handle fate × abort timing × abort source {`JoinHandle` / `AbortHandle`}), loom models, and `tokio/tests/task_abort.rs`, `rt_*`, `task_join_set.rs`.

**Read next:** [05 — Handles & the `Schedule` trait](./05-handles-and-schedule.md).
