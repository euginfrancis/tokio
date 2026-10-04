# Task component 3 — `RawTask` and the `Vtable` (`runtime/task/raw.rs`)

> **One sentence:** `RawTask` is an 8-byte, `Copy`, *untyped* pointer to a task header, and the `Vtable` it points to is a hand-written table of function pointers (plus three field offsets) that lets the scheduler, wakers and join handles operate on a task **without knowing the future's type `T` or the scheduler type `S`**.

---

## 1. Where it lives

<!-- FILES:t_raw -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/raw.rs`](../../../tokio/src/runtime/task/raw.rs) | 252 | 72 | 30 |
<!-- /FILES -->

---

## 2. Why a hand-rolled vtable (and not `dyn Trait`)?

The scheduler's queues hold *only* `Notified` handles — a single pointer each. They have to be small, `Copy`-like to move and **homogeneous**, yet every task has a different `T: Future`. Options:

| Option | Problem |
|---|---|
| `Box<dyn Future>` per task + wrapper | 16-byte fat pointers in every queue slot; no place to put the atomic state, queue link, join waker; extra allocation |
| Generic scheduler `Scheduler<T>` | Impossible: one queue, many `T`s |
| `Arc<dyn Task>` | 16-byte pointer, and a second vtable pointer chase; no control over where fields sit |
| **Own vtable stored in the header** (chosen) | 8-byte pointers; the vtable pointer sits *in the header* (one cache line with the state), generated once per `(T, S)` as a `static`; offsets of fields that depend on `T` are stored alongside |

The cost is `unsafe` code, paid back as one allocation per task, 8-byte handles and a single indirect call per operation.

---

## 3. Data types (DTOs)

```rust
#[derive(Clone)] pub(crate) struct RawTask { ptr: NonNull<Header> }     // + `impl Copy`

pub(super) struct Vtable {
    pub(super) poll:                  unsafe fn(NonNull<Header>),
    pub(super) schedule:              unsafe fn(NonNull<Header>),
    pub(super) dealloc:               unsafe fn(NonNull<Header>),
    pub(super) try_read_output:       unsafe fn(NonNull<Header>, *mut (), &Waker),
    pub(super) drop_join_handle_slow: unsafe fn(NonNull<Header>),
    pub(super) drop_abort_handle:     unsafe fn(NonNull<Header>),
    pub(super) shutdown:              unsafe fn(NonNull<Header>),
    pub(super) trailer_offset:        usize,    // bytes from Header to Trailer
    pub(super) scheduler_offset:      usize,    // bytes from Header to Core.scheduler (== start of Core)
    pub(super) id_offset:             usize,    // bytes from Header to Core.task_id
    #[cfg(tokio_unstable)] pub(super) spawn_location_offset: usize,
}                                                // size_of::<Vtable>() = 80 bytes (measured)
```

### The seven operations and what they do

| Vtable slot | Instantiated function | Delegates to | Purpose | Called through |
|---|---|---|---|---|
| `poll` | `poll::<T,S>(ptr)` | `Harness::poll` | run the future once; **consumes one ref-count** | `RawTask::poll` ← `LocalNotified::run`, `UnownedTask::run` |
| `schedule` | `schedule::<S>(ptr)` | `scheduler.schedule(Notified(…))` | hand the task back to *its* scheduler (note: only `S` is needed, not `T`) | `RawTask::schedule` ← `wake_by_val/ref`, `remote_abort` |
| `dealloc` | `dealloc::<T,S>(ptr)` | `Harness::dealloc` | `drop(Box::from_raw(cell))` — drops `Stage`, waker, scheduler `Arc` | `RawTask::dealloc` ← `drop_reference`, `Task::drop`, harness |
| `try_read_output` | `try_read_output::<T,S>(ptr, dst, waker)` | `Harness::try_read_output` | move the output into `*dst` (a `*mut Poll<Result<T::Output,JoinError>>` passed as `*mut ()`) or store the join waker | `JoinHandle::poll` |
| `drop_join_handle_slow` | `…::<T,S>` | `Harness::drop_join_handle_slow` | `JoinHandle` dropped on a non-initial state: drop output/waker as needed | `JoinHandle::drop` |
| `drop_abort_handle` | `…::<T,S>` | `Harness::drop_reference` | `AbortHandle` dropped → `ref_dec`, maybe dealloc | `AbortHandle::drop` |
| `shutdown` | `…::<T,S>` | `Harness::shutdown` | forcibly cancel at runtime shutdown | `Task::shutdown` ← `OwnedTasks::close_and_shutdown_all` |

Why `try_read_output` takes `*mut ()`: the generic type of the output cannot appear in a non-generic function pointer, so the caller passes a pointer to its own typed `Poll<Result<O, JoinError>>` slot and the instantiated function casts it back (`JoinHandle<O>` and the task were created with the same `T::Output = O`, which is the unsafe contract).

---

## 4. How the vtable is built (the clever part)

```rust
pub(super) fn vtable<T: Future, S: Schedule>() -> &'static Vtable {
    &Vtable {                         // promoted to a `static` because every field is a constant expression
        poll: poll::<T, S>,  schedule: schedule::<S>,  dealloc: dealloc::<T, S>, …,
        trailer_offset:   OffsetHelper::<T, S>::TRAILER_OFFSET,
        scheduler_offset: OffsetHelper::<T, S>::SCHEDULER_OFFSET,
        id_offset:        OffsetHelper::<T, S>::ID_OFFSET,
    }
}
struct OffsetHelper<T, S>(T, S);      // an associated *const*, not a const fn call, so rvalue-static-promotion still works
impl<T: Future, S: Schedule> OffsetHelper<T, S> {
    const TRAILER_OFFSET:   usize = get_trailer_offset(size_of::<Header>(), size_of::<Core<T,S>>(), align_of::<Core<T,S>>(), align_of::<Trailer>());
    const SCHEDULER_OFFSET: usize = get_core_offset(size_of::<Header>(), align_of::<Core<T,S>>());
    const ID_OFFSET:        usize = get_id_offset(size_of::<Header>(), align_of::<Core<T,S>>(), size_of::<S>(), align_of::<Id>());
}
```

The three `const fn`s re-derive the **`#[repr(C)]` layout algorithm** (align the offset up to the next field's alignment, then add the field's size):

```
core_offset    = align_up(size_of(Header), align_of(Core<T,S>))
trailer_offset = align_up(core_offset + size_of(Core<T,S>), align_of(Trailer))
id_offset      = align_up(core_offset + size_of(S), align_of(Id))        // `scheduler` is Core's first field, `task_id` its second
```
(With `tokio_unstable`, a fourth offset locates `spawned_at` the same way.)

Two non-obvious constraints, both documented in the code:
1. The vtable must be a *promotable constant*; calling a `const fn` directly inside the struct literal would block promotion to `&'static` ⇒ the offsets are computed through `OffsetHelper` associated consts (rust-lang forum thread cited in the source).
2. `size_of`/`align_of` are passed *as arguments* because trait bounds on generic params of `const fn` were unstable on the MSRV.

**One static vtable per `(T, S)`**: with `N` distinct future types spawned on one runtime flavor you get `N` vtables (80 B each, in `.rodata`), not one per task.

---

## 5. `RawTask` API

| Function | Visibility | What it does |
|---|---|---|
| `RawTask::new::<T,S>(task, scheduler, id, spawned_at)` | `pub(super)` | `Box::into_raw(Cell::new(…, State::new(), …))` → `RawTask` (**refs = 3**) |
| `from_raw(NonNull<Header>)` | `pub(super)`, `unsafe` | wrap a raw pointer (used by every vtable fn and by `Link::from_raw`) |
| `header_ptr() / header() / trailer_ptr() / trailer() / state()` | `pub(super)` | typed-free accessors; `trailer_ptr` uses `Header::get_trailer` (the vtable offset) |
| `poll(self)` | `pub(crate)` | `(vtable.poll)(ptr)` — "mutual exclusion is required to call this" (guaranteed by the state word) |
| `schedule(self)`, `dealloc(self)`, `shutdown(self)` | `pub(super)` | vtable dispatch |
| `try_read_output(self, dst, &Waker)` | `pub(super)`, `unsafe` | see above |
| `drop_join_handle_slow(self)`, `drop_abort_handle(self)` | `pub(super)` | vtable dispatch |
| `ref_inc(self)` | `pub(super)` | `state.ref_inc()`; used only when creating or cloning an `AbortHandle` (wakers call `State::ref_inc` directly) |
| `get_queue_next(self) / set_queue_next(self, Option<RawTask>)` | `pub(crate)`, `unsafe` | read/write `Header.queue_next` — **only for the inject queue**, which must synchronise access |
| Non-generic helpers in `harness.rs`: `drop_reference`, `wake_by_val`, `wake_by_ref`, `remote_abort`, `try_set_join_waker` | `pub(super)` | implemented on `RawTask` itself (not `Harness<T,S>`) so **only one copy is compiled** — they don't need `T` or `S` |

That last point is a deliberate **code-size optimisation**: operations that need neither the future type nor the scheduler type (ref counting, waking via the state word, abort) live on `RawTask`; everything that touches `Stage<T>` lives on the generic `Harness<T,S>` and is reached through the vtable.

---

## 6. Communication with other components

```
 scheduler / queues ─────────────┐
 wakers (waker.rs) ──────────────┤                    ┌─▶ Harness<T,S>::poll / dealloc / try_read_output /
 JoinHandle / AbortHandle ───────┼─▶ RawTask ──vtable─┤    drop_join_handle_slow / shutdown        (typed)
 OwnedTasks (Task handles) ──────┤   (8 bytes)        └─▶ S::schedule(Notified)                    (needs S only)
 inject queue ─▶ get/set_queue_next ─▶ Header.queue_next
```

| Caller | Calls | Data in | Data out |
|---|---|---|---|
| Scheduler worker (`LocalNotified::run`) | `poll` | – (ptr) | – (result is side effects) |
| Waker | `wake_by_val/ref` → `schedule` | – | `Notified` given to `S::schedule` |
| `JoinHandle::poll` | `try_read_output` | `&mut Poll<Result<T,JoinError>>` (as `*mut ()`), `&Waker` | writes `Ready(output)` into the slot |
| `JoinHandle::drop` | `drop_join_handle_slow` | – | – |
| Inject queue | `get_queue_next/set_queue_next` | `Option<RawTask>` | – |

---

## 7. Safety contract (what callers must guarantee)

| Slot | Caller must guarantee |
|---|---|
| `poll` | the caller owns a ref-count that poll will consume; the `Notified` was bound to a list on this runtime (`assert_owner` — see [08](./08-owned-tasks.md)) so polling on this thread is allowed |
| `try_read_output` | `dst` really is `*mut Poll<Result<T::Output, JoinError>>` for *this* task's `T` |
| `get/set_queue_next` | exactly one queue owns the link at a time, and access is synchronised (inject mutex) |
| any vtable fn | `ptr` points at a live header (ref-count ≥ 1 held by the caller) |

---

## 8. Invariants

1. Every `Header.vtable` is the vtable for exactly the `(T, S)` of the surrounding `Cell`.
2. Offsets in the vtable = real offsets (debug-asserted in `Cell::new`).
3. `RawTask` is `Copy` and has **no `Drop`** — ref-counting is entirely explicit through the state word; typed wrappers (`Task`, `Notified`, `JoinHandle`, …) add the RAII.

---

## 9. Tests

<!-- TESTS:t_raw -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| *inline `#[test]` in the source files above* | 0 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

Covered by every runtime test (all dispatch through it); the debug layout assertions guard the offsets; `runtime/tests/task.rs` instantiates tasks with a test `Schedule` implementation to exercise all seven slots.

**Read next:** [04 — Harness](./04-harness.md), the typed code those slots call.
