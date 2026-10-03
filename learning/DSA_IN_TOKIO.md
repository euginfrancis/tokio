# Data Structures & Algorithms in Tokio

> A field guide to every notable data structure and algorithm in the Tokio codebase (`tokio-rs/tokio` @ `8667843`).
> Each entry says **what** it is, **where** it lives, **how** it works, its **complexity**, and **why** Tokio needs it.
> Runnable mini-versions you can play with are in [`dsa-exercises/`](./dsa-exercises) (`cd learning/dsa-exercises && cargo test`).

Paths are relative to the repo root. Difficulty: 🟢 easy to read · 🟡 moderate · 🔴 hard (`unsafe`, atomics, loom-tested).

---

## Index

| # | Name | Category | Where | Difficulty |
|---|---|---|---|---|
| **Data structures** |||||
| D1 | Intrusive doubly linked list | List | `tokio/src/util/linked_list.rs` | 🔴 |
| D2 | Sharded linked list | List + hashing | `tokio/src/util/sharded_list.rs` | 🟡 |
| D3 | Idle/notified set (two lists) | List | `tokio/src/util/idle_notified_set.rs` | 🔴 |
| D4 | Work-stealing ring buffer (SPMC) | Queue / ring buffer | `tokio/src/runtime/scheduler/multi_thread/queue.rs` | 🔴 |
| D5 | Inject queue (intrusive FIFO) | Queue | `tokio/src/runtime/scheduler/inject/` | 🟡 |
| D6 | LIFO slot | Single-element cache | `tokio/src/runtime/scheduler/multi_thread/worker.rs` | 🟢 |
| D7 | Hierarchical timing wheel | Wheel + bitmap | `tokio/src/runtime/time/wheel/` | 🟡 |
| D8 | Block-linked list (mpsc) | Unrolled linked list | `tokio/src/sync/mpsc/{block,list}.rs` | 🔴 |
| D9 | Broadcast ring buffer | Ring buffer | `tokio/src/sync/broadcast.rs` | 🟡 |
| D10 | Watch version counter | Versioned cell | `tokio/src/sync/watch.rs` | 🟢 |
| D11 | Task cell (Header/Core/Trailer) + vtable | Struct layout / type erasure | `tokio/src/runtime/task/{core,raw}.rs` | 🔴 |
| D12 | Atomic bitfield state words | Bit-packed state | `runtime/task/state.rs`, `sync/notify.rs`, … | 🟡 |
| D13 | `WakeList` (fixed array batch) | Array / stack | `tokio/src/util/wake_list.rs` | 🟢 |
| D14 | Sharded blocking-pool queue + occupancy mask | Sharded queues + bitmap | `tokio/src/runtime/blocking/sharded.rs` | 🟡 |
| D15 | H2 log-linear histogram | Histogram | `tokio/src/runtime/metrics/histogram/h2_histogram.rs` | 🟡 |
| D16 | Cancellation tree | Tree | `tokio-util/src/sync/cancellation_token/tree_node.rs` | 🟡 |
| D17 | `DelayQueue`: slab + wheel + intrusive stack | Slab / wheel | `tokio-util/src/time/delay_queue.rs`, `tokio-util/src/time/wheel/` | 🟡 |
| D18 | `JoinMap`: two hash tables | Hash map | `tokio-util/src/task/join_map.rs` | 🟡 |
| D19 | `StreamMap`: vec + swap_remove | Array | `tokio-stream/src/stream_map.rs` | 🟢 |
| **Algorithms** |||||
| A1 | Work-stealing scheduling (steal half) | Scheduling | `multi_thread/{worker,queue}.rs` | 🔴 |
| A2 | Overflow: move half to global queue | Load balancing | `multi_thread/queue.rs` | 🟡 |
| A3 | Self-tuning global-queue interval (EWMA) | Statistics / control | `multi_thread/stats.rs` | 🟢 |
| A4 | Cooperative budgeting | Fairness | `tokio/src/task/coop/mod.rs` | 🟢 |
| A5 | Timer level selection via `ilog2(elapsed ^ when)` | Bit math | `runtime/time/wheel/mod.rs` | 🟡 |
| A6 | Next timer via `rotate_right` + `trailing_zeros` | Bit scan | `runtime/time/wheel/level.rs` | 🟡 |
| A7 | Cascading timers down levels | Wheel | `runtime/time/wheel/mod.rs` | 🟡 |
| A8 | xorshift64+ PRNG | Randomness | `tokio/src/util/rand.rs` | 🟢 |
| A9 | Lemire's fast range reduction | Randomness | `tokio/src/util/rand.rs` | 🟢 |
| A10 | Randomized fair polling (`select!`, `StreamMap`, stealing) | Fairness | `macros/select.rs`, `stream_map.rs` | 🟢 |
| A11 | FIFO-fair batch semaphore | Synchronization | `tokio/src/sync/batch_semaphore.rs` | 🔴 |
| A12 | RwLock on top of a semaphore | Synchronization | `tokio/src/sync/rwlock.rs` | 🟡 |
| A13 | `AtomicWaker` register/wake protocol | Lock-free | `tokio/src/sync/task/atomic_waker.rs` | 🔴 |
| A14 | Park/unpark 3-state protocol | Lock-free + condvar | `tokio/src/runtime/park.rs` | 🟡 |
| A15 | Atomic reference counting in a bitfield | Memory management | `runtime/task/state.rs` | 🔴 |
| A16 | Ordered shutdown protocol | Distributed-ish protocol | `multi_thread/worker.rs` | 🔴 |
| A17 | Idle-worker coordination (packed counters) | Synchronization | `multi_thread/idle.rs` | 🟡 |
| A18 | Deadlock-free tree locking (lock ordering) | Concurrency | `cancellation_token/tree_node.rs` | 🟡 |
| A19 | Byte search (`memchr`) & line framing | String search / parsing | `util/memchr.rs`, `tokio-util/src/codec/lines_codec.rs` | 🟢 |
| A20 | Length-delimited framing state machine | Parsing / FSM | `tokio-util/src/codec/length_delimited.rs` | 🟢 |
| A21 | Buffered copy & bidirectional copy | Streaming | `tokio/src/io/util/copy*.rs` | 🟢 |
| A22 | Model checking (loom) | Verification | `tokio/src/loom/`, `*/tests/loom_*.rs` | 🟡 |

---

## Part 1 — Data structures

### D1. Intrusive doubly linked list 🔴
**Where:** `tokio/src/util/linked_list.rs`
**What:** A doubly linked list where the `prev`/`next` pointers live **inside the element itself** (a `Pointers<T>` field), not in a separate heap node. The list only stores `head`/`tail` raw pointers.
**Why Tokio needs it:** A future waiting on a `Mutex`, `Notify`, `Semaphore` or timer must be put on a wait queue **without allocating**. The future already lives somewhere stable (it's pinned), so the node can be embedded in the future. Removing a node is O(1) when the future is dropped (cancellation).
**Complexity:** push_front / pop_back / remove(node) = **O(1)**, no allocation.
**Used by:** `Notify` waiters, batch-semaphore waiters, timer wheel slots, `OwnedTasks`, broadcast receivers, I/O `ScheduledIo` waiters, `IdleNotifiedSet`.
**Rust concepts:** `NonNull<T>`, `Pin` (an element must not move while linked), `PhantomPinned`, a `Link` trait with `unsafe fn pointers()`.
**DSA lesson:** This is the classic "intrusive list" from the Linux kernel (`list_head`), done in Rust.

### D2. Sharded linked list 🟡
**Where:** `tokio/src/util/sharded_list.rs`, used by `OwnedTasks` in `runtime/task/list.rs`
**What:** An array of `Mutex<LinkedList>` shards. An item's shard = `hash(task id) & shard_mask`. Shard count = `min(2^16, next_power_of_two(cores) * 4)` (`list.rs: gen_sharded_list_size`).
**Why:** Every spawn and every task completion touches the "all tasks" list. One mutex would be a global contention point; N shards cut contention ~N×.
**Complexity:** O(1) insert/remove; iteration is O(n) across shards. Order is not preserved.
**DSA lesson:** *lock striping* — the same idea as Java's old `ConcurrentHashMap` segments. Power-of-two size makes `& mask` replace `%`.

### D3. Idle/notified set 🔴
**Where:** `tokio/src/util/idle_notified_set.rs` (backs `JoinSet`)
**What:** Every entry is in exactly one of two intrusive lists: **idle** or **notified**. When an entry's waker fires, the entry moves from idle → notified (O(1)). `JoinSet::join_next` only pops from the notified list.
**Why:** With 10,000 tasks in a `JoinSet`, polling all of them on each wake-up would be O(n). This makes "find a task that is ready" **O(1)**.
**DSA lesson:** Partitioning items into lists by state — like a "ready list" in an OS scheduler.

### D4. Work-stealing ring buffer (bounded SPMC queue) 🔴
**Where:** `tokio/src/runtime/scheduler/multi_thread/queue.rs`
**What:** Each worker owns a fixed array of **256** slots (`LOCAL_QUEUE_CAPACITY`, power of two, `MASK = 255`). One producer (the owning worker) pushes at `tail`; consumers (owner + thieves) take from `head`.
- `tail: AtomicU32` — written only by the owner.
- `head: AtomicU64` — **packs two u32 indices**: the *real head* and the *steal head*. A thief first advances the real head (claiming a batch), copies the tasks, then moves the steal head forward. While they differ, another thief can't start stealing.
- Indices are wider than needed (u32 for 256 slots) and wrap freely; `index & MASK` gives the slot. The extra bits **mitigate ABA** and distinguish full vs empty.
**Complexity:** push/pop O(1) amortized, lock-free; steal moves ⌈n/2⌉ items in one batch.
**Why:** The hot path (worker pushing/popping its own tasks) has no locks at all.
**DSA lesson:** Ring buffer + Chase-Lev-style work stealing (Tokio's variant is SPMC with batched steals). See also Go's runtime `runq`.

### D5. Inject queue 🟡
**Where:** `tokio/src/runtime/scheduler/inject/` (`synced.rs`, `shared.rs`, `pop.rs`)
**What:** A singly linked FIFO of tasks with `head`/`tail` pointers behind a mutex, plus an `AtomicUsize len` so workers can check "is it empty?" **without taking the lock**. The "next" pointer is stored inside the task header (intrusive again).
**Why:** Tasks spawned from outside a worker thread (e.g. from `block_on` or another thread) need a shared entry point.
**Complexity:** push/pop O(1); push_batch links a whole chain in O(1) after building it.

### D6. LIFO slot 🟢
**Where:** `lifo_slot: Option<Notified>` in `multi_thread/worker.rs`
**What:** A one-element cache in front of the run queue. A task woken by the currently running task is put here and runs next.
**Why:** Message-passing patterns (task A sends to B, B replies) get cache locality and low latency. To prevent two tasks ping-ponging forever and starving others, at most `MAX_LIFO_POLLS_PER_TICK = 3` LIFO polls happen in a row.
**DSA lesson:** A tiny "most recently used" fast path in front of a FIFO — the same idea as CPU write buffers.

### D7. Hierarchical timing wheel 🟡
**Where:** `tokio/src/runtime/time/wheel/{mod,level}.rs`
**What:** **6 levels × 64 slots** (`NUM_LEVELS = 6`, `LEVEL_MULT = 64`). Level 0 slots are 1 ms wide, level 1 slots 64 ms, level 2 slots ~4 s, … level 5 slots ~12.4 days. Total range `2^36 ms` ≈ 2.2 years. Each slot is an intrusive list of timers. Each level has an `occupied: u64` **bitmap** — bit *i* set ⇔ slot *i* is non-empty.
**Complexity:** insert **O(1)**, cancel **O(1)**, find next expiration **O(levels) = O(1)** via bit scans (see A5, A6). Compare: a binary heap is O(log n) per insert/cancel.
**Why:** Servers create and cancel huge numbers of timeouts (most never fire). O(1) cancel is the key.
**DSA lesson:** Varghese & Lauck's *"Hashed and Hierarchical Timing Wheels"* (1987) — the same design as the Linux kernel timer wheel and Kafka's purgatory.

### D8. Block-linked list for `mpsc` 🔴
**Where:** `tokio/src/sync/mpsc/block.rs`, `list.rs`, `chan.rs`
**What:** An *unrolled* linked list: each node is a **block of `BLOCK_CAP = 32` slots** (16 on 32-bit). Each block has a `ready_slots: AtomicUsize` bitmap (one bit per slot + `RELEASED` and `TX_CLOSED` flag bits). Senders claim a slot index with `fetch_add` on a shared tail, write the value, then set its ready bit. The receiver walks blocks, reading slots whose bit is set.
**Recycling:** when the receiver finishes a block, it tries to append it back to the tail (a few attempts) instead of freeing it — fewer allocations.
**Complexity:** send/recv O(1) amortized; one allocation per 32 messages (less with reuse).
**DSA lesson:** Unrolled linked list + per-slot readiness bitmap; similar to crossbeam's `SegQueue` and Vyukov's MPSC designs.

### D9. Broadcast ring buffer 🟡
**Where:** `tokio/src/sync/broadcast.rs`
**What:** `buffer: Box<[Mutex<Slot<T>>]>` with power-of-two capacity and `mask`. Every slot stores its absolute `pos: u64` and a remaining-receivers count `rem`. Each receiver keeps its own `next: u64` cursor. A slot is at index `pos & mask`.
**Lagging:** if the sender laps a slow receiver, the receiver detects `slot.pos != expected` and gets `RecvError::Lagged(n)` — it is **not** allowed to block the sender.
**DSA lesson:** Ring buffer with *absolute sequence numbers* to detect overwrite (like the LMAX Disruptor).

### D10. Watch version counter 🟢
**Where:** `tokio/src/sync/watch.rs` (`Version`, `AtomicState`)
**What:** One value behind an `RwLock` and an atomic version counter. The version is incremented by `STEP_SIZE = 2` so that **bit 0 is free for a `CLOSED` flag**. Receivers remember the last version they saw; `changed()` returns when the shared version differs.
**DSA lesson:** Sequence numbers + flag-in-low-bit packing.

### D11. Task cell + manual vtable 🔴
**Where:** `tokio/src/runtime/task/core.rs`, `raw.rs`, `harness.rs`
**What:** A task is **one heap allocation** laid out as `Cell<T, S> { header: Header, core: Core<T, S>, trailer: Trailer }`, `#[repr(C)]`. `Header` holds the state word, a queue-next pointer, and a pointer to a static **vtable** (`poll`, `schedule`, `dealloc`, `try_read_output`, …). `RawTask` is just a `NonNull<Header>`, so the scheduler can handle tasks of any future type without generics or `Box<dyn Future>`.
**Why:** Fewer allocations, smaller pointers in queues, hot fields (header) together in cache.
**DSA lesson:** Type erasure by hand — this is how C++ `std::function` or Rust `dyn Trait` work internally.

### D12. Atomic bitfield state words 🟡
**Where:** `runtime/task/state.rs`, `sync/notify.rs`, `sync/watch.rs`, `sync/batch_semaphore.rs`, `runtime/io/scheduled_io.rs`, `util/bit.rs` (`Pack` helper)
**What:** A single `AtomicUsize` encodes several flags *and* a counter. Example — task state:
```
bit 0 RUNNING | bit 1 COMPLETE | bit 2 NOTIFIED | bit 3 JOIN_INTEREST | bit 4 JOIN_WAKER | bit 5 CANCELLED | bits 6.. ref-count
```
`REF_ONE = 1 << 6`, new tasks start at `3 * REF_ONE | JOIN_INTEREST | NOTIFIED`. Transitions are compare-and-swap loops (`fetch_update`).
**Why:** Updating several fields **atomically together** without a lock.
**DSA lesson:** Bit packing, masks, shifts; CAS loops.

### D13. `WakeList` 🟢
**Where:** `tokio/src/util/wake_list.rs`
**What:** A fixed array of **32** `MaybeUninit<Waker>` + a length. Code collects wakers while holding a lock, **releases the lock**, then calls `wake_all()`.
**Why:** Calling `wake()` while holding a mutex can deadlock or create contention. Batching in a fixed array avoids heap allocation.
**DSA lesson:** Bounded stack; "collect under lock, act outside lock" pattern.

### D14. Sharded blocking-pool queue 🟡
**Where:** `tokio/src/runtime/blocking/sharded.rs`
**What:** An **opt-in** alternative to the default queue (`Builder::enable_sharded_blocking_queue()` or env `TOKIO_UNSTABLE_SHARDED_BLOCKING_QUEUE=1`): `NUM_SHARDS = 16` queues each with its own mutex. Spawners pick a shard with the thread-local RNG; workers scan starting from a shard derived from their id. An **occupancy mask** records which shards have tasks so empty shards are skipped without locking. The **default** pool (`pool.rs`) is a single mutex-protected `VecDeque` + `Condvar`, with idle threads exiting after a **10 s keep-alive**.
**DSA lesson:** Lock striping again + bitmap index.

### D15. H2 log-linear histogram 🟡
**Where:** `tokio/src/runtime/metrics/histogram/h2_histogram.rs`, `histogram.rs`
**What:** Poll-time metrics can use linear buckets or an **H2 histogram** (HdrHistogram-like): buckets grow exponentially, each power-of-two range split into `2^p` linear sub-buckets, giving a guaranteed relative error of `2^-p` (default p = 2 → 25%). Bucket index is computed with bit operations (leading zeros), not a search.
**DSA lesson:** Logarithmic bucketing; O(1) bucket lookup via bit math.

### D16. Cancellation tree 🟡
**Where:** `tokio-util/src/sync/cancellation_token/tree_node.rs`
**What:** Each `CancellationToken` points to a `TreeNode { parent, children: Vec<Arc<TreeNode>>, parent_idx, … }` under a mutex. `child_token()` adds a child. Cancelling a node cancels its whole subtree (DFS). Removing a child is O(1) by `swap_remove` using the stored `parent_idx` (and fixing the moved sibling's index). When a node dies, its children are re-parented to its parent.
**DSA lesson:** N-ary tree with index back-pointers; see A18 for its locking rule.

### D17. `DelayQueue` 🟡
**Where:** `tokio-util/src/time/delay_queue.rs`, `tokio-util/src/time/wheel/{mod,level,stack}.rs`
**What:** A user-facing "queue of items that pop out when their deadline passes". Items live in a **`Slab`** (vector with a free list → stable integer keys); the wheel slots hold an **intrusive stack** of slab keys (`Stack` trait). Same 6×64 wheel idea as D7.
**DSA lesson:** Slab allocator (index-based arena) + timing wheel; arena indices instead of pointers is the "safe Rust" way to do linked structures.

### D18. `JoinMap` 🟡
**Where:** `tokio-util/src/task/join_map.rs`
**What:** Two hash tables: `tasks_by_key: HashTable<(K, AbortHandle)>` and `hashes_by_task: HashMap<task::Id, u64>`. When a task finishes, its `Id` → stored hash → find & remove the key entry, without needing to re-hash or clone `K`.
**DSA lesson:** Bidirectional mapping; using `hashbrown`'s raw `HashTable` to store precomputed hashes.

### D19. `StreamMap` 🟢
**Where:** `tokio-stream/src/stream_map.rs`
**What:** A `Vec<(K, V)>` of streams. `remove` uses `swap_remove` (O(1), order not kept). `poll_next` starts at a **random index** (A10) and loops around so no stream starves.

---

## Part 2 — Algorithms

### A1. Work stealing 🔴
**Where:** `multi_thread/worker.rs` (`steal_work`), `queue.rs` (`steal_into`, `steal_into2`)
**How:**
1. Worker looks for work in order: LIFO slot → local queue → (every N ticks) global inject queue.
2. If empty, it becomes a *searcher* (A17 limits searchers to fewer than half the workers) and picks a **random start** worker: `start = rand.fastrand_n(num)`; then tries `(start + i) % num`.
3. From the victim it steals `n - n/2` (= ⌈n/2⌉) tasks in one batch into its own queue.
4. Then checks the inject queue; if still nothing → park.
**Why half?** Taking one task causes repeated steals; taking all leaves the victim idle. Half balances load in O(log n) rounds.
**DSA lesson:** Randomized load balancing (Blumofe & Leiserson, Cilk).

### A2. Overflow to global queue 🟡
**Where:** `queue.rs` (`push_back_or_overflow`, `push_overflow`)
**How:** When the 256-slot local queue is full, the worker claims **half (128) of its tasks plus the new one** with a single CAS and moves them in one linked batch to the inject queue.
**DSA lesson:** Amortization — one expensive operation per 128 pushes.

### A3. Self-tuning global queue interval (EWMA) 🟢
**Where:** `multi_thread/stats.rs`
**How:** Keeps an **exponentially weighted moving average** of task poll time (`alpha = 0.1`). Interval = `200 µs / avg_poll_time`, clamped to `[2, 127]` tasks. Fast tasks → check the global queue less often; slow tasks → more often.
`ewma = alpha * sample + (1 - alpha) * ewma`
**DSA lesson:** EWMA (used in TCP RTT estimation, load averages); feedback control.

### A4. Cooperative budgeting 🟢
**Where:** `tokio/src/task/coop/mod.rs`
**How:** Each task poll gets a budget of **128**. Every Tokio resource operation calls `poll_proceed`, which decrements. At 0 → resource returns `Pending` and wakes the task immediately, forcing a yield.
**DSA lesson:** Token-bucket-like fairness; prevents starvation in a non-preemptive scheduler.

### A5. Timer level selection 🟡
**Where:** `runtime/time/wheel/mod.rs`, `fn level_for`
```rust
let masked = elapsed ^ when | SLOT_MASK;   // SLOT_MASK = 63
if masked >= MAX_DURATION { return NUM_LEVELS - 1; }
masked.ilog2() as usize / BITS_PER_LEVEL   // BITS_PER_LEVEL = 6
```
**How:** XOR finds the **highest bit where "now" and "deadline" differ**. If they differ only in the low 6 bits → level 0; in bits 6–11 → level 1; etc. `ilog2` = position of the highest set bit (one CPU instruction). OR-ing `63` ensures a minimum of level 0.
**Complexity:** O(1), no loops.
**DSA lesson:** Using XOR + highest-set-bit to compare numbers by "prefix". Same trick as a radix tree / trie on bits.

### A6. Find next occupied slot 🟡
**Where:** `runtime/time/wheel/level.rs`, `fn next_occupied_slot`
```rust
let now_slot = ((now / slot_range(level)) % 64) as usize + 1;
let occupied = self.occupied.rotate_right(now_slot as u32);
let zeros = occupied.trailing_zeros() as usize;
let slot = (zeros + now_slot) % 64;
```
**How:** Rotate the 64-bit occupancy bitmap so that "the slot after now" becomes bit 0, then `trailing_zeros` finds the nearest non-empty slot going forward — **circularly**, in one instruction.
**DSA lesson:** Bitmap + bit-scan = O(1) "find next set bit in a circular buffer".

### A7. Cascading timers 🟡
**Where:** `runtime/time/wheel/mod.rs` (`poll`, `process_expiration`)
**How:** When a slot on level *k > 0* expires, its timers aren't fired yet — they are **re-inserted** and fall to a finer level (now closer to their deadline). Only level-0 expirations fire. Each timer cascades at most 5 times.
**DSA lesson:** Hierarchical bucketing, like radix sort by digits from most to least significant.

### A8. xorshift64+ PRNG 🟢
**Where:** `tokio/src/util/rand.rs` (`FastRand::fastrand`)
```rust
s1 ^= s1 << 17;
s1 = s1 ^ s0 ^ s1 >> 7 ^ s0 >> 16;
self.one = s0; self.two = s1;
s0.wrapping_add(s1)
```
**How:** Two 32-bit xorshift states with Marsaglia shift triplet `[17, 7, 16]`. Not cryptographic; very fast, passes SmallCrush. Seedable via `RngSeed` for deterministic tests.

### A9. Lemire's fast range reduction 🟢
**Where:** `util/rand.rs` (`fastrand_n`)
```rust
((rand as u64 * n as u64) >> 32) as u32   // ≈ rand % n, without division
```
**How:** Maps a 32-bit random number to `[0, n)` with one multiply and shift — avoids a slow division.

### A10. Randomized fair polling 🟢
**Where:** `macros/select.rs` (start index from `thread_rng_n(BRANCHES)`), `tokio-stream/src/stream_map.rs`, work-stealing victim selection
**How:** Instead of always checking branch 0 first (which would starve the others when it's always ready), start at a random index and wrap around. `select! { biased; … }` disables this.

### A11. FIFO-fair batch semaphore 🔴
**Where:** `tokio/src/sync/batch_semaphore.rs`
**How:**
- `permits: AtomicUsize` stores `available << 1 | CLOSED`.
- Fast path: CAS to subtract permits.
- Slow path: lock the waiter list, enqueue the waiter at the **back** (intrusive list, D1).
- On release: permits are handed to waiters from the **front**; a waiter can be *partially* filled (it needs 5, gets 3 now, 2 later). Only when fully satisfied is it woken — via a `WakeList` after unlocking.
**Why it matters:** Strict FIFO means a writer needing many permits is never starved by a stream of readers needing one.
**Builds:** `Mutex` (1 permit), `RwLock` (A12), `Semaphore`, bounded `mpsc` capacity, `OnceCell` init.

### A12. RwLock as a semaphore 🟡
**Where:** `tokio/src/sync/rwlock.rs`
**How:** Semaphore with `MAX_READS` permits (`u32::MAX >> 3`). A reader acquires **1** permit; a writer acquires **all** `MAX_READS`. Because the semaphore is FIFO (A11), a waiting writer blocks later readers → no writer starvation. Elegant reduction of one problem to another.

### A13. `AtomicWaker` 🔴
**Where:** `tokio/src/sync/task/atomic_waker.rs`
**How:** A single slot holding a `Waker`, guarded by a state word with `WAITING = 0`, `REGISTERING = 0b01`, `WAKING = 0b10`. `register()` CASes WAITING→REGISTERING, stores the waker, then CASes back; if a `wake()` happened concurrently (state now REGISTERING|WAKING) the registrant wakes the new waker itself. Guarantees **no lost wake-ups** without a mutex.
**DSA lesson:** Classic lock-free handshake (same design as `futures::task::AtomicWaker`).

### A14. Park / unpark protocol 🟡
**Where:** `tokio/src/runtime/park.rs`
**How:** State `EMPTY | PARKED | NOTIFIED` plus a `Mutex` + `Condvar`. `unpark` sets NOTIFIED; `park` consumes NOTIFIED if present (no sleep), otherwise CASes to PARKED and waits on the condvar. Avoids the lost-wakeup race between "check" and "sleep".
**DSA lesson:** The standard "binary semaphore with a fast path" (same as `std::thread::park`).

### A15. Reference counting inside the state word 🔴
**Where:** `runtime/task/state.rs`, `harness.rs`
**How:** The ref-count lives in the high bits (D12). `ref_inc` = `fetch_add(REF_ONE)`; `ref_dec` = `fetch_sub(REF_ONE)`, and whoever brings it to zero deallocates via the vtable. Combining the count with the flags lets one CAS do "set COMPLETE **and** drop my reference".
**DSA lesson:** Manual `Arc`; memory reclamation without GC.

### A16. Ordered shutdown 🔴
**Where:** top-of-file comment and `Core::pre_shutdown`, `Shared::shutdown` in `multi_thread/worker.rs`
**How:** (1) close inject queue + `OwnedTasks` (both have a closed bit), (2) each worker drains & cancels its owned tasks, (3) workers hand their cores to `shutdown_cores`; the **last** one empties all local queues and the inject queue. The comment proves why both closed bits are needed to avoid a ref-count cycle leak.
**DSA lesson:** Reasoning about linearization points and invariants — a great example of a correctness argument in comments.

### A17. Idle-worker coordination 🟡
**Where:** `multi_thread/idle.rs`
**How:** One `AtomicUsize` packs `num_searching` (low 16 bits) and `num_unparked` (high bits, `UNPARK_SHIFT = 16`). Rules: a worker may start searching (stealing) only if `2 * num_searching < num_workers` — at most half the workers search at once; and a sleeping worker is woken only if **no** worker is already searching. Prevents a *thundering herd* of workers all trying to steal the same task.
**DSA lesson:** Packed counters; throttling contention.

### A18. Deadlock-free tree locking 🟡
**Where:** `tokio-util/src/sync/cancellation_token/tree_node.rs` (`with_locked_node_and_parent`)
**How:** Invariant: **always lock parent before child**. But you only learn a node's parent after locking the node. So: lock node, read parent, `try_lock` the parent (fast path, can't deadlock). If that fails: unlock node, lock parent, re-lock node, and re-check the parent didn't change in between (loop and retry if it did).
**DSA lesson:** Lock ordering — the textbook cure for deadlock (break the "circular wait" condition).

### A19. Byte search & line framing 🟢
**Where:** `tokio/src/util/memchr.rs` (calls `libc::memchr`, which uses SIMD; falls back to `iter().position`), `tokio-util/src/codec/lines_codec.rs`, `tokio/src/io/util/read_until.rs`
**How:** `LinesCodec` remembers `next_index` — how far it already scanned — so a partially received line isn't re-scanned from the beginning each time more bytes arrive (avoids O(n²)).

### A20. Length-delimited framing FSM 🟢
**Where:** `tokio-util/src/codec/length_delimited.rs`
**How:** Two-state machine `DecodeState::{Head, Data(len)}`: read the N-byte length header (configurable offset, size, endianness, adjustment) → wait until `len` bytes are buffered → emit a frame → back to `Head`. Rejects frames over `max_frame_length`.
**DSA lesson:** Finite-state machine parsing of a byte stream.

### A21. Buffered copy 🟢
**Where:** `tokio/src/io/util/copy.rs`, `copy_bidirectional.rs`, `copy_buf.rs`
**How:** A `CopyBuffer` with `pos`/`cap` indices: read into the buffer when empty, write out what's buffered, flush at the end. `copy_bidirectional` runs two of these in one future and polls both directions.

### A22. Model checking with loom 🟡
**Where:** `tokio/src/loom/` (shim), `runtime/tests/loom_*.rs`, `sync/tests/loom_*.rs`
**How:** Under `--cfg loom`, `std::sync::atomic`/`thread` are replaced by loom's versions, and loom **exhaustively enumerates thread interleavings** (bounded by `LOOM_MAX_PREEMPTIONS`) using dynamic partial-order reduction. That's how D4, D8, A11, A13, A15 are verified.

---

## Part 3 — Cross-reference by classic DSA topic

| Classic topic | Where to see it in Tokio |
|---|---|
| Linked lists (singly/doubly, intrusive) | D1, D2, D3, D5, D8 |
| Queues / deques / ring buffers | D4, D5, D9, `VecDeque` in blocking pool (D14) |
| Stacks | D13, `tokio-util` wheel `Stack` (D17) |
| Hash tables / hashing | D2 (shard by id hash), D18 |
| Trees | D16 |
| Arrays / slabs / arenas | D17 (Slab), D19 |
| Bit manipulation | D7, D12, A5, A6, A9, A17, D15 |
| Randomized algorithms | A1, A8, A9, A10 |
| Amortized analysis | A2, D8 block reuse, A19 |
| Scheduling / fairness | A1, A3, A4, A10, A11 |
| State machines | D12, A13, A14, A20, every hand-written `Future` |
| Concurrency: CAS, lock-free | D4, D8, A13, A15 |
| Concurrency: locks, deadlock avoidance | D2, A11, A12, A18 |
| Statistics | A3 (EWMA), D15 (histogram) |
| Verification | A22 |

---

## Part 4 — Suggested study order

1. 🟢 A8 + A9 (`util/rand.rs`, ~90 lines) — warm up with bit operations.
2. 🟢 D13 `wake_list.rs` — `MaybeUninit`, fixed arrays.
3. 🟢 D10 `watch.rs` `Version`/`AtomicState` — version counters.
4. 🟡 D7 + A5 + A6 + A7 timing wheel — read `wheel/mod.rs` with its unit tests.
5. 🟡 A11 + A12 semaphore → RwLock.
6. 🔴 D1 linked list → D3 idle-notified set.
7. 🔴 D12 + A15 task state.
8. 🔴 D4 + A1 + A2 work-stealing queue.
9. 🔴 D8 mpsc blocks, A13 `AtomicWaker`.
10. Run the loom test for one of them (A22) and break something on purpose to watch loom catch it.

For each, do the matching exercise in `dsa-exercises/` first, then read the real code.
