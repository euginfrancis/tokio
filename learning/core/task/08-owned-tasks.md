# Task component 8 — Task Ownership Lists: `OwnedTasks`, `LocalOwnedTasks`, `ShardedList`, intrusive `LinkedList` (`runtime/task/list.rs`, `util/{sharded_list,linked_list}.rs`)

> **One sentence:** every runtime keeps a registry of *all its live tasks* — a **sharded, mutex-per-shard intrusive linked list** whose links live inside each task's `Trailer` — so it can (a) prove which runtime owns a task, (b) cancel everything at shutdown, and (c) refuse new tasks once shutdown has begun.

This is the component that makes **"spawn during shutdown"** and **"cancel every task on drop"** correct.

---

## 1. Where it lives

<!-- FILES:t_owned -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/task/list.rs`](../../../tokio/src/runtime/task/list.rs) | 253 | 70 | 24 |
| [`tokio/src/util/linked_list.rs`](../../../tokio/src/util/linked_list.rs) | 522 | 127 | 36 |
| [`tokio/src/util/sharded_list.rs`](../../../tokio/src/util/sharded_list.rs) | 104 | 38 | 12 |
| **Total (3 files)** | **879** | **235** | **72** |
<!-- /FILES -->

Three layers, from the bottom up:

```
   LinkedList<L: Link>            util/linked_list.rs      intrusive doubly-linked list (unsafe, O(1) everything)
        ▲ one per shard
   ShardedList<L: ShardedListItem> util/sharded_list.rs     Box<[Mutex<LinkedList>]> + shard_mask + counters      (lock striping)
        ▲ + `closed` flag + owner id
   OwnedTasks<S>  /  LocalOwnedTasks<S>   task/list.rs      the task-specific wrappers used by schedulers
```

---

## 2. Data types (DTOs)

### Layer 1 — `LinkedList` and the `Link` trait
```rust
pub(crate) struct LinkedList<L: Link> { head: Option<NonNull<L::Target>>, tail: Option<NonNull<L::Target>> }   // NOT emptied on drop

pub(crate) unsafe trait Link {                   // "how does a type sit inside a list?"
    type Handle;                                  // owning handle, e.g. Task<S>
    type Target;                                  // the node type that contains the pointers, e.g. Header
    fn as_raw(handle: &Self::Handle) -> NonNull<Self::Target>;                  // peek the pointer, don't consume
    unsafe fn from_raw(ptr: NonNull<Self::Target>) -> Self::Handle;             // rebuild the handle on removal
    unsafe fn pointers(target: NonNull<Self::Target>) -> NonNull<Pointers<Self::Target>>;   // where the prev/next live
}
pub(crate) struct Pointers<T> { inner: UnsafeCell<PointersInner<T>> }
struct PointersInner<T> { prev: Option<NonNull<T>>, next: Option<NonNull<T>>, _pin: PhantomPinned }   // 16 bytes
```
`Pointers` is `!Unpin` (`PhantomPinned`) and is only accessed through raw-pointer getters/setters, so the compiler never puts `noalias` on a reference to it (the rust-lang#82834 workaround).

For tasks (`mod.rs`):
```rust
unsafe impl<S> linked_list::Link for Task<S> {
    type Handle = Task<S>;  type Target = Header;
    fn as_raw(h) -> NonNull<Header>                    { h.raw.header_ptr() }
    unsafe fn from_raw(ptr) -> Task<S>                 { Task::from_raw(ptr) }
    unsafe fn pointers(t) -> NonNull<Pointers<Header>> { Trailer::addr_of_owned(Header::get_trailer(t)) }   // &trailer.owned
}
```

### Layer 2 — `ShardedList`
```rust
pub(crate) struct ShardedList<L: ShardedListItem> {
    lists: Box<[Mutex<LinkedList<L>>]>,      // one mutex-protected list per shard (size = power of two)
    added: MetricAtomicU64,                  // total ever pushed (unstable metric)
    count: MetricAtomicUsize,                // live items (len())
    shard_mask: usize,                       // size - 1
}
pub(crate) unsafe trait ShardedListItem: Link { unsafe fn get_shard_id(target: NonNull<Self::Target>) -> usize; }
pub(crate) struct ShardGuard<'a, L: Link> { lock: MutexGuard<'a, LinkedList<L>>, added, count, id }   // a held shard lock
```
For tasks, `get_shard_id` = the task's `Id` (a never-changing integer) ⇒ **a task always maps to the same shard**, so `remove` can lock exactly the right list without searching.

### Layer 3 — `OwnedTasks` / `LocalOwnedTasks`
```rust
pub(crate) struct OwnedTasks<S: 'static> {            // thread-safe; Send tasks only
    list: ShardedList<Task<S>>,
    pub(crate) id: NonZeroU64,                         // unique per OwnedTasks (global counter starting at 1; u32 counter on targets without AtomicU64)
    closed: AtomicBool,
}
pub(crate) struct LocalOwnedTasks<S: 'static> {       // !Send + !Sync; used by LocalSet (and LocalRuntime)
    inner: UnsafeCell<OwnedTasksInner<S>>,             //   { list: LinkedList<Task<S>>, closed: bool }
    pub(crate) id: NonZeroU64,
    _not_send_or_sync: PhantomData<*const ()>,
}
```

**Shard count:** `min(2^16, num_cores.next_power_of_two() * 4)`. Multi-thread passes its worker count; the current-thread scheduler passes `1` ⇒ **4 shards**; e.g. 8 workers ⇒ 32 shards. (The cap exists because more shards worsen memory locality of nodes and slow construction; the multiplier ×4 reduces the chance that two workers hit the same shard.)

---

## 3. Interface (what schedulers call)

| Method | On | Purpose | Notes |
|---|---|---|---|
| `new(num_cores)` / `new()` | both | construct; allocate a fresh owner `id` | |
| `bind(future, scheduler, id, spawned_at) -> (JoinHandle<T::Output>, Option<Notified<S>>)` | both | create the task (`new_task`), stamp `owner_id`, insert; `T: Send` for `OwnedTasks` | `None` ⇒ the list was closed: the task was **shut down immediately** and only the `JoinHandle` is returned |
| `bind_local(...)` | `OwnedTasks` | same for `!Send` futures | `unsafe`: only for `LocalRuntime`, where the task cannot move |
| `assert_owner(Notified<S>) -> LocalNotified<S>` | both | verify the task belongs here and grant poll permission | `OwnedTasks`: `debug_assert_eq!` owner id; `LocalOwnedTasks`: `assert_eq!` (thread safety) |
| `remove(&Task<S>) -> Option<Task<S>>` | both | called from `Schedule::release` on completion | returns the list's `Task` (with its ref-count) or `None` if the task isn't in the list |
| `close_and_shutdown_all(start)` / `close_and_shutdown_all()` | both | set `closed`, pop every task and `Task::shutdown()` it | `start` rotates the first shard per caller to spread contention |
| `get_shard_size() / num_alive_tasks() / is_empty()` | `OwnedTasks` | introspection / metrics (`alive_tasks`, `spawned_tasks_count` unstable) | `len()` = relaxed counter |
| `for_each(f)` | `OwnedTasks` (taskdump) | lock **all** shards, visit every task | used by task dumps |

---

## 4. The algorithms

### `bind_inner` — insertion with a closed-check *under the lock*
```rust
task.header().set_owner_id(self.id);              // exclusive: the task was just created
let shard = self.list.lock_shard(&task);          // lock shard[ id & mask ]
if self.closed.load(Acquire) {                    // checked WHILE HOLDING the shard lock
    drop(shard);
    task.shutdown();                              // never scheduled: cancelled right away
    return None;
}
shard.push(task);                                 // push_front, count += 1, added += 1
Some(notified)
```
`close_and_shutdown_all` does `closed.store(true, Release)` and then, for each shard, locks it and pops. Because the spawner checks `closed` **inside the shard lock** and the closer locks every shard after setting the flag, **every task is either in the list when its shard is drained, or sees `closed` and cancels itself** — no task can slip in after its shard was emptied.

### `close_and_shutdown_all(start)`
```rust
self.closed.store(true, Release);
for i in start..self.get_shard_size() + start {          // each caller starts at a different shard (worker threads pass a random start)
    loop {
        match self.list.pop_back(i) {                    // lock shard i % size, pop one
            Some(task) => task.shutdown(),               // Harness::shutdown → cancel & complete (may call release → remove → None, see below)
            None => break,
        }
    }
}
```
Multiple workers may run this concurrently (each in `Core::pre_shutdown`), each popping from different starting shards, so shutdown is **parallel**. `task.shutdown()` runs *without* holding the shard lock.

### `remove` and the ref-count accounting
`Schedule::release` → `OwnedTasks::remove(&task)`:
```rust
let task_id = task.header().get_owner_id()?;      // None ⇒ never bound ⇒ nothing to remove
assert_eq!(task_id, self.id);                      // "wrong runtime" check
unsafe { self.list.remove(task.header_ptr()) }     // lock the shard, LinkedList::remove(node)
```
`LinkedList::remove` returns `None` if the node isn't linked (it checks `head`/`tail` when `prev`/`next` are null). That happens for tasks already popped by `close_and_shutdown_all` ⇒ `release` returns `None` ⇒ the harness drops 1 ref instead of 2 (the list's ref went away when the popped `Task` handle was consumed by `shutdown`).

### `LinkedList` operations (all O(1))
`push_front`, `pop_front`, `pop_back`, `remove(node)`, `is_empty`, `last`; plus `drain_filter` (used by I/O `ScheduledIo` waiter wake-ups), `for_each`, and a `GuardedLinkedList` variant (used by `Notify::notify_waiters`). Every mutating method is `unsafe` or takes handles because nodes are *intrusive*: removal needs no search, and **a node can sit in at most one list at a time** (it has exactly one `Pointers`).

---

## 5. Communication with other components

| Peer | Direction | What crosses |
|---|---|---|
| Scheduler `Handle::spawn` / `bind_new_task` | scheduler → list | `future`, `Arc<Handle>` (scheduler), `Id`, `SpawnLocation` → `(JoinHandle, Option<Notified>)` |
| Scheduler `Schedule::release` | scheduler → list | `&Task<S>` → `Option<Task<S>>` |
| Scheduler worker `run_task` | worker → list | `Notified<S>` → `LocalNotified<S>` (`assert_owner`) |
| Scheduler `pre_shutdown` | worker → list | `start: usize` (random) → shuts all tasks |
| [Cell](./02-cell-layout.md) | list ↔ cell | `Header.owner_id`; `Trailer.owned` (links) |
| [Handles](./05-handles-and-schedule.md) | list ↔ | `Task<S>` (stored), `Notified`/`LocalNotified` (conversion) |
| [Harness](./04-harness.md) | list → harness | `Task::shutdown` (via vtable) |
| Metrics (`RuntimeMetrics`) | list → | `num_alive_tasks`, `spawned_tasks_count` |
| `LocalSet` | its `LocalState` owns a `LocalOwnedTasks` | binds `!Send` tasks, `assert_owner` on the owner thread |

---

## 6. Invariants & safety arguments

1. **Owner id is write-once**: set while the task is exclusively held (`bind_inner`), never cleared — so it can be read without synchronisation (`assert_owner`, `remove`) even while the task is being removed concurrently. A task that was removed keeps its old id and can never be bound to another list.
2. **Shard id is immutable** (task `Id`), hence "if a node is in some shard of this list, it is in the shard `get_shard_id` names" — the safety argument for `ShardedList::remove`.
3. **Closed-under-lock** protocol (above) gives the dual guarantee: no new task after shutdown, no leaked task.
4. **The list holds a ref-count** for each task (it stores a `Task<S>` handle), so tasks stay alive until `release`/shutdown; a list is **not emptied on drop** — callers must empty it (`close_and_shutdown_all`) first, otherwise tasks leak (documented on `LinkedList`).
5. `LocalOwnedTasks::assert_owner` uses `assert_eq!` on the id in all builds because an erroneous `LocalNotified` would let a `!Send` future be polled on the wrong thread — a soundness hole, not a debug aid.
6. A node must not move while linked (`Link` requires pinned targets) — tasks are heap-allocated and never move.

---

## 7. Performance notes

- Spawn cost = 1 allocation + 1 uncontended mutex lock + O(1) list insertion; completion = 1 mutex + O(1) removal. With `4 × workers` shards, contention is rare.
- `len()` is a relaxed atomic counter, not a sum over shards — cheap enough for metrics.
- Pop order is `pop_back` after `push_front` ⇒ shutdown cancels **oldest tasks first** within a shard.

---

## 8. Tests

<!-- TESTS:t_owned -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/task.rs`](../../../tokio/src/runtime/tests/task.rs) | 13 | 403 |
| [`tokio/src/runtime/tests/loom_local.rs`](../../../tokio/src/runtime/tests/loom_local.rs) | 1 | 30 |
| *inline `#[test]` in the source files above* | 5 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

Inline `test_id_not_broken`; linked-list unit/fuzz-style tests in `util/linked_list.rs` (`fuzz_linked_list` using `Entry` with `Pin<&Entry>` handles); `runtime/tests/task.rs` (`create_shutdown*`, `shutdown*`, `spawn_during_shutdown`); `tokio/tests/rt_shutdown_err.rs`, `rt_threaded.rs` (drop while tasks alive).

**Read next:** [09 — Task ids, hooks & metadata](./09-id-hooks-metadata.md).
