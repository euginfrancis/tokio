# Task component 2 — The Task Cell: `Header | Core | Trailer` (`runtime/task/core.rs`)

> **One sentence:** a task is *one heap allocation* — a `#[repr(C)]` `Cell<T, S>` split into **hot** data (`Header`: state, queue link, vtable), the **payload** (`Core`: scheduler handle, id, and the future *or* its output) and **cold** data (`Trailer`: owner-list links, join waker, hooks) — and every other component reaches it through a type-erased `*mut Header`.

---

## 1. Where it lives

<!-- FILES:t_cell -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/core.rs`](../../../tokio/src/runtime/task/core.rs) | 331 | 203 | 29 |
<!-- /FILES -->

---

## 2. The shape of a task in memory

```
 one Box<Cell<T, S>>, #[repr(C)], aligned to 128 bytes on x86_64 / aarch64 / powerpc64
 (64 on most others; 32 on arm/mips/sparc/hexagon; 256 on s390x; 16 on m68k)

 offset 0   ┌──────────────────────────────────────────────┐ ◀── RawTask / Notified / JoinHandle / Waker all point HERE (*mut Header)
            │ Header                              32 bytes │     HOT: touched on every poll, wake, schedule
            │   state        State(AtomicUsize)       8    │
            │   queue_next   UnsafeCell<Option<NonNull<Header>>>  8  │  link used by the inject queue
            │   vtable       &'static Vtable          8    │  type-erased behaviour (see 03-rawtask-vtable)
            │   owner_id     UnsafeCell<Option<NonZeroU64>> 8 │  which OwnedTasks owns me
            │   (tracing_id: Option<tracing::Id> +8, scheduled_at: Option<NonZeroU64> +8 — only with the matching unstable features)
            ├──────────────────────────────────────────────┤
 offset 32  │ Core<T, S>      (24 + stage bytes; 48 for a trivial future)
            │   scheduler    S  = Arc<Handle>         8    │  how the task re-schedules *itself*
            │   task_id      Id(NonZeroU64)           8    │
            │   (spawned_at: &'static Location  +8   — tokio_unstable only)
            │   stage        CoreStage<T> = UnsafeCell<Stage<T>>   │  enum { Running(T) | Finished(Result<T::Output, JoinError>) | Consumed }
            ├──────────────────────────────────────────────┤
 offset …   │ Trailer                             48 bytes │     COLD: used at spawn, completion, join, shutdown
            │   owned   linked_list::Pointers<Header>  16 │  prev/next in OwnedTasks
            │   waker   UnsafeCell<Option<Waker>>       16 │  the JoinHandle's waker
            │   hooks   TaskHarnessScheduleHooks        16 │  Option<Arc<dyn Fn(&TaskMeta)>> (on_task_terminate)
            └──────────────────────────────────────────────┘
 total size = round_up(32 + size_of(Core) + 48, 128)
```

### Measured sizes (64-bit Linux, multi-thread scheduler, this commit)

Measured by temporarily instantiating `Cell<T, Arc<multi_thread::Handle>>` in a unit test (the test was then removed):

| Type | `size_of` |
|---|---:|
| `State` | 8 |
| `Header` | **32** (a test asserts `≤ 8 pointers = 64`, i.e. it must stay within one cache line) |
| `Trailer` | **48** |
| `Vtable` | 80 (one static per `(T, S)` pair, not per task) |
| `RawTask`, `Task`, `Notified`, `JoinHandle`, `Arc<Handle>` | 8 each — a handle is a single pointer |

| Spawned future | `size_of::<T>()` | `Core` | **whole `Cell`** |
|---|---:|---:|---:|
| `async {}` | 1 | 48 | **128 B** |
| `async { yield_now().await }` | 24 | 48 | **128 B** |
| holds a `[u8; 256]` across an `.await` | 280 | 304 | **384 B** |
| holds a `[u8; 1024]` across an `.await` | 1,048 | 1,072 | **1,152 B** |
| holds a `[u8; 16384]` across an `.await` | 16,408 | 16,432 | **16,512 B** |

**What this tells you:** a trivial task costs *exactly one 128-byte block* (32 + 48 + 48 = 128) — the allocation is as small as the alignment allows. Beyond that, a task costs `~48 + 32 + size_of(future)`, rounded up to 128 — the future dominates, so big stack buffers held across `.await` directly become big tasks. (Futures larger than `BOX_FUTURE_THRESHOLD` — **16 KiB in release, 2 KiB in debug builds** — are boxed by `spawn`/`block_on`/`spawn_blocking` via `AutoBox::<F>::SHOULD_BOX`, a *compile-time* constant. The point is to avoid stack overflow when a huge future is moved by value through the call chain; the cell then holds just an 8-byte `Pin<Box<F>>`, at the cost of a second allocation.)

---

## 3. Why this layout — design reasons

| Decision | Reason |
|---|---|
| `#[repr(C)]` with `Header` first | A `*mut Cell<T,S>` and a `*mut Header` are the **same address**; the scheduler only ever stores `*mut Header` and needs no generics |
| Hot / cold split | Wakers and queues touch only `Header` (one cache line); `Trailer` is only read at completion/shutdown, so it stays out of the way of the future |
| 128-byte alignment | Starting with Sandy Bridge the spatial prefetcher loads *pairs* of 64-byte lines; aligning to 128 prevents false sharing between **neighbouring tasks** polled on different threads |
| Scheduler handle *inside* the task (`Core.scheduler: S`) | A waker can be fired from **any** thread (a timer thread, another runtime, a non-Tokio thread). The task itself knows which runtime to go back to — wakers need no extra context |
| Future and output share one slot (`Stage`) | The output reuses the future's memory — no second allocation when the task finishes |
| `Trailer` after the (variable-size) `Core` | Its offset depends on `size_of::<Core<T,S>>()`; therefore the offset must be stored in the vtable (below) |

---

## 4. Data types (DTOs) defined here

```rust
#[repr(C)] pub(super) struct Cell<T: Future, S> { header: Header, core: Core<T, S>, trailer: Trailer }

#[repr(C)] pub(crate) struct Header {            // pub(crate): also used by the inject queue & the blocking pool
    pub(super) state: State,
    pub(super) queue_next: UnsafeCell<Option<NonNull<Header>>>,
    pub(super) vtable: &'static Vtable,
    pub(super) owner_id: UnsafeCell<Option<NonZeroU64>>,
    #[cfg(all(tokio_unstable, feature = "tracing"))] pub(super) tracing_id: Option<tracing::Id>,
    pub(super) scheduled_at: UnsafeCell<ScheduleLatencyInstant>,   // Option<NonZeroU64> ns since runtime start; zero-sized mock when the feature is off
}
unsafe impl Send/Sync for Header {}

#[repr(C)] pub(super) struct Core<T: Future, S> {
    scheduler: S, task_id: Id,
    #[cfg(tokio_unstable)] spawned_at: &'static Location<'static>,
    stage: CoreStage<T>,                          // UnsafeCell<Stage<T>>
}
#[repr(C)] pub(super) enum Stage<T: Future> { Running(T), Finished(super::Result<T::Output>), Consumed }

pub(super) struct Trailer {
    owned: linked_list::Pointers<Header>,         // links for OwnedTasks (intrusive)
    waker: UnsafeCell<Option<Waker>>,             // JoinHandle waker
    hooks: TaskHarnessScheduleHooks,              // { task_terminate_callback: Option<TaskCallback> }
}

pub(crate) struct TaskIdGuard { parent_task_id: Option<Id> }   // RAII: sets CONTEXT.current_task_id while the future runs/drops
```

### The three stages of `Stage<T>`

| Stage | Holds | Entered by | Accessible by |
|---|---|---|---|
| `Running(T)` | the future | `Cell::new` | whoever holds the `RUNNING` bit |
| `Finished(Result<T::Output, JoinError>)` | output, **or** a `JoinError` (panic / cancel) | `store_output` | the `JoinHandle` once `COMPLETE` is set |
| `Consumed` | nothing | `drop_future_or_output`, `take_output` | – |

Note the two-step on success: `Core::poll` sets `Consumed` **as soon as the future returns `Ready`** (dropping the future), then `poll_future` calls `store_output` to place `Finished(Ok(output))`.

---

## 5. Interface (what other components can call)

All of these are `pub(super)` (visible inside `runtime/task/` only), and "should be considered `unsafe`" per the module header — safety comes from the state word.

| Function | Signature | Safety condition | Called by |
|---|---|---|---|
| `Cell::new` | `(future, scheduler, state, task_id, [spawned_at]) -> Box<Cell<T,S>>` | – | `RawTask::new` |
| `Core::poll` | `(&self, Context<'_>) -> Poll<T::Output>` | caller holds `RUNNING`; cell is pinned (heap) | `Harness::poll_future` |
| `Core::store_output` | `(&self, super::Result<T::Output>)` | holds `RUNNING` | `poll_future`, `cancel_task` |
| `Core::take_output` | `(&self) -> super::Result<T::Output>` | `COMPLETE` set & caller is the `JoinHandle` | `Harness::try_read_output` |
| `Core::drop_future_or_output` | `(&self)` | holds `RUNNING` (or is the completing/dropping owner) | harness (`cancel_task`, `complete`, `drop_join_handle_slow`) |
| `Header::get_trailer / get_scheduler::<S> / get_id_ptr / get_id` | `(NonNull<Header>) -> NonNull<…>` | pointer is a valid task header; `S` is the right scheduler type | `RawTask`, handles, `OwnedTasks`, `ShardedListItem::get_shard_id` |
| `Header::set_next / queue_next` | | one queue owns the link, access synchronised | inject queue (via `RawTask::{get,set}_queue_next`) |
| `Header::set_owner_id / get_owner_id` | | `set` only at bind time (exclusive) | `OwnedTasks::bind_inner`; `assert_owner`, `remove` |
| `Header::set_scheduled_at / get_scheduled_at` | | one `Notified` per task ⇒ no concurrent writers | scheduler `schedule_task`, `run_task` |
| `Trailer::set_waker / will_wake / wake_join` | | `JOIN_WAKER` access rules | `can_read_output`, `complete`, `drop_join_handle_slow` |

### How a type-erased `*mut Header` reaches typed fields
`Header::get_trailer(ptr)` = `ptr + vtable.trailer_offset`; `get_scheduler::<S>(ptr)` = `ptr + vtable.scheduler_offset`; `get_id_ptr(ptr)` = `ptr + vtable.id_offset`. The offsets are produced at compile time by `const fn`s in `raw.rs` that *re-implement the `#[repr(C)]` layout algorithm* (see [03-rawtask-vtable](./03-rawtask-vtable.md)). `Cell::new` has a `#[cfg(debug_assertions)]` check that recomputes each field's real address and asserts it equals the vtable-derived pointer — if someone reorders the struct without updating `raw.rs`, every debug build fails immediately.

---

## 6. Communication with other components

| Peer | What it reads/writes in the cell | Through |
|---|---|---|
| [State word](./01-state-word.md) | `Header.state` | `Harness::state()`, `RawTask::state()` |
| [Vtable / RawTask](./03-rawtask-vtable.md) | `Header.vtable`, offsets | `RawTask::*` dispatch |
| [Harness](./04-harness.md) | `Core.stage` (poll, store, take, drop), `Trailer.waker`, `Trailer.hooks`, `Core.scheduler`, `Core.task_id` | typed `Harness<T,S>` over `NonNull<Cell<T,S>>` |
| [OwnedTasks](./08-owned-tasks.md) | `Header.owner_id`; `Trailer.owned` (list links) via `Link::pointers` | `Task<S>: linked_list::Link`, `ShardedListItem::get_shard_id` (= task id) |
| Scheduler inject queue | `Header.queue_next` | `RawTask::{get,set}_queue_next` |
| Scheduler metrics | `Header.scheduled_at` | `Notified::set_scheduled_at`, `LocalNotified::get_scheduled_at` |
| Runtime context | `Core.task_id` ↔ `CONTEXT.current_task_id` | `TaskIdGuard` |

**Who owns each field's access rights** (module header of `task/mod.rs`):

| Field | Exclusive access held by |
|---|---|
| `state` | – (atomic) |
| `Trailer.owned` | the `OwnedTask` reference (the one in `OwnedTasks`) |
| `Header.queue_next` | the `Notified` reference (there is only ever one) |
| `Header.owner_id` | set once at construction; afterwards immutable and readable by anyone |
| `Core.stage` | while `COMPLETE = 0`: the thread that set `RUNNING`; while `COMPLETE = 1`: the `JoinHandle` (or the completing thread if `JOIN_INTEREST = 0`) |
| `Trailer.waker` | by the `JOIN_WAKER` protocol (see [06](./06-waker.md)/[07](./07-join-abort-error.md)) |
| everything else | immutable → any thread |

---

## 7. `TaskIdGuard`: tying the future to its id

`Core::poll`, `set_stage` (store/drop of future or output) all run under `TaskIdGuard::enter(task_id)`, which sets `CONTEXT.current_task_id = Some(id)` and restores the previous value on drop. This is what makes `tokio::task::id()` correct *inside* the future **and inside its destructor and the destructor of its output** (so drop-order logging and `task_local!` teardown see the right id), and nests correctly if a task polls another (e.g. `LocalSet`, `block_on`).

---

## 8. Invariants

1. `Header` is the first field of a `#[repr(C)]` struct → a pointer to the cell is a pointer to the header.
2. The offsets in the vtable equal the true field offsets (debug-asserted at construction).
3. `Cell` memory is only freed by `Harness::dealloc`, called by whoever drops the **last** reference (state word).
4. The future is never moved after `Cell::new` (it lives in a `Box` and is accessed via `Pin::new_unchecked`).
5. Output of a non-`Send` future/`JoinHandle` is never moved across threads by the runtime: the completing thread drops it itself if `JOIN_INTEREST = 0`; otherwise the (equally `!Send`) `JoinHandle` takes/drops it on its own thread.

---

## 9. Tests

<!-- TESTS:t_cell -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

`header_lte_cache_line` (inline) pins `size_of::<Header>() ≤ 8 pointers`. Layout is otherwise protected by the debug assertions in `Cell::new` and exercised by every runtime test.

**Read next:** [03 — RawTask & Vtable](./03-rawtask-vtable.md).
