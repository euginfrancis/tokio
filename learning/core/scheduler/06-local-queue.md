# Scheduler component 6 — The Local Run Queue: a bounded lock-free SPMC ring (`multi_thread/queue.rs`, `multi_thread/overflow.rs`)

> **One sentence:** each worker owns a **256-slot ring buffer** that only *it* pushes into, but that *other workers can steal half of* — coordinated with just two atomics (`tail`, and a `head` that packs *two* indices), so the common path (push/pop by the owner) takes no lock and the rare path (steal, overflow) takes no lock either.

---

## 1. Where it lives

<!-- FILES:s_queue -->
| File | Code | Docs+comments | Functions |
|---|---:|---:|---:|
| [`tokio/src/runtime/scheduler/multi_thread/queue.rs`](../../../tokio/src/runtime/scheduler/multi_thread/queue.rs) | 327 | 176 | 22 |
| [`tokio/src/runtime/scheduler/multi_thread/overflow.rs`](../../../tokio/src/runtime/scheduler/multi_thread/overflow.rs) | 21 | 0 | 4 |
| **Total (2 files)** | **348** | **176** | **26** |
<!-- /FILES -->

---

## 2. Data

```rust
pub(crate) struct Local<T: 'static> { inner: Arc<Inner<T>> }     // PRODUCER handle  — !Clone, used by exactly one thread (the core holder)
pub(crate) struct Steal<T: 'static>(Arc<Inner<T>>);              // CONSUMER handle  — Clone, used by any worker
pub(crate) struct Inner<T: 'static> {
    head:   AtomicUnsignedLong,    // u64: two u32 indices packed — (steal << 32) | real
    tail:   AtomicUnsignedShort,   // u32: written only by the owner, read by everyone
    buffer: Box<[UnsafeCell<MaybeUninit<task::Notified<T>>>; LOCAL_QUEUE_CAPACITY]>,    // 256 slots (loom: 4)
}
pub(crate) fn local<T>() -> (Steal<T>, Local<T>)                  // constructor: one Arc<Inner>, two handle types
pub(crate) trait Overflow<T> { fn push(&self, task); fn push_batch<I: Iterator<Item = Notified<T>>>(&self, iter: I); }   // "where do I dump tasks?"
```
| Constant / type | Value | Why |
|---|---|---|
| `LOCAL_QUEUE_CAPACITY` | **256** (`4` under loom so the model checker can explore more interleavings) | power of two ⇒ `index & MASK` instead of `%`; must be ≤ `u8::MAX+1` (asserted by a test) |
| `UnsignedShort` / `UnsignedLong` | `u32` / `u64` (targets with 64-bit atomics) — else `u16` / `u32` | **wider than the index range on purpose**: ABA resistance (issue #5041) and to distinguish *full* (`tail − head = 256`) from *empty* (`= 0`) |
| `MASK` | `255` | slot = `index & MASK` |
| `Local` is `!Sync`-by-contract | – | "may only be used from a single thread" |

### The packed `head`
```
 head (u64):  63 ………………… 32 | 31 ………………… 0
              ┌─────────────────┬─────────────────┐
              │  steal (u32)    │   real (u32)    │
              └─────────────────┴─────────────────┘
 pack(steal, real) = real | (steal << 32)        unpack(n) = (steal, real)

 real  = the true head: next element to be popped / next to be claimed by a stealer
 steal = the first index of a steal currently in progress   (steal == real  ⇔  no steal in progress)
```
`tail` is a plain `u32` that only grows (wrapping). Indices are *free-running*; the slot is `idx & 255`.

| Quantity | Formula |
|---|---|
| number of queued tasks (owner's view) | `tail − real` (`wrapping_sub`) |
| free capacity | `256 − (tail − steal)` ← **measured from `steal`, not `real`** |
| queue empty | `real == tail` |
| steal in progress | `steal != real` |

**Why capacity is measured from `steal`:** slots between `steal` and `real` have been *claimed* by a stealer but may not have been *copied out* yet. If the owner counted them as free it could overwrite a task the stealer is still reading. Measuring from `steal` keeps them reserved until the stealer finishes (`steal := real`).

---

## 3. The operations

### 3.1 `Local::push_back_or_overflow(task, overflow, stats)` — owner pushes one task
```rust
let tail = loop {
    let head = self.inner.head.load(Acquire);
    let (steal, real) = unpack(head);
    let tail = self.inner.tail.unsync_load();                       // only the owner writes tail → non-atomic read is fine
    if tail.wrapping_sub(steal) < 256 { break tail; }               // ① room → fast path
    else if steal != real {                                         // ② full, but a steal is in progress (it will free room)
        overflow.push(task);  return;                               //    don't fight it: single task to the inject queue
    } else {                                                        // ③ really full, nobody stealing
        match self.push_overflow(task, real, tail, overflow, stats) { Ok(_) => return, Err(v) => task = v /* lost a race: retry */ }
    }
};
self.push_back_finish(task, tail);                                  // write slot[tail & MASK]; tail.store(tail+1, Release)
```
`push_back_finish` writes the slot **first**, then publishes it with `tail.store(.., Release)` — pairing with the `Acquire` load of `tail` in `steal_into2`.

### 3.2 `push_overflow` — moving half the ring to the inject queue *without moving data*
Precondition: `tail − head == 256` (asserted). Let `h = head = real = steal`, `tail = h + 256`.
```
1. CAS head: (h,h) ──────────────▶ (tail,tail)         // ONE CAS claims ALL 256 tasks: the queue now looks EMPTY to everyone
      lost the race? → return Err(task); caller retries the whole push

   positions:   h ………… h+127 │ h+128 ………… h+255 │
   contents:    [ first half ]  [ second half    ]      (old tail = h+256)

2. tail.store(tail + 128, Release)                     // new tail = h+384, real = h+256  ⇒ length 128
      The live range is now positions h+256 … h+383, which map (mod 256) to slots h … h+127  — the FIRST half, untouched!
3. BatchTaskIter reads the SECOND half out of slots (h+128 … h+255) and chains the new task:
      overflow.push_batch(second_half.chain(once(task)))       // 128 + 1 = 129 tasks, linked and inserted under ONE inject lock
4. stats.incr_overflow_count()
```
Design notes from the source comments:
- It keeps the **older** half local and sends the **newer** half to inject. Tasks that were just taken *from* the inject queue are always placed in the *first* half of the ring (via `push_back` in `next_task`), so a task fetched from inject can't be bounced straight back to inject before being polled once.
- A concurrent stealer that observes the "empty" window and goes to sleep isn't a problem: the batch push to inject wakes someone (`schedule_local` notifies after overflow).

### 3.3 `Local::pop()` — owner takes the oldest
```rust
let mut head = self.inner.head.load(Acquire);
let idx = loop {
    let (steal, real) = unpack(head);
    let tail = self.inner.tail.unsync_load();
    if real == tail { return None; }
    let next_real = real.wrapping_add(1);
    let next = if steal == real { pack(next_real, next_real) }              // no stealer: advance both
               else             { assert_ne!(steal, next_real); pack(steal, next_real) };   // stealer active: only advance real
    match self.inner.head.compare_exchange_weak(head, next, AcqRel, Acquire) { Ok(_) => break real as usize & MASK, Err(a) => head = a }
};
Some(slot[idx].read())                                                       // we won the CAS ⇒ exclusive ownership of that slot
```
The owner pops from the **front** (oldest first = FIFO). The CAS is contended only when a stealer is simultaneously claiming.

### 3.4 `Steal::steal_into(dst, dst_stats)` and `steal_into2` — taking ⌈n/2⌉ from a victim
```rust
// Guard: does dst have room? dst may LOOK empty but still have slots reserved by a stealer of dst
let dst_tail = dst.inner.tail.unsync_load();
let (steal, _) = unpack(dst.inner.head.load(Acquire));
if dst_tail.wrapping_sub(steal) > 256 / 2 { return None; }                   // abort rather than steal a smaller amount (simplicity)

let mut n = self.steal_into2(dst, dst_tail);                                 // copies tasks into dst's buffer (NOT yet visible)
if n == 0 { return None; }
dst_stats.incr_steal_count(n);  dst_stats.incr_steal_operations();
n -= 1;                                                                      // one task is returned to the caller to run right now
let ret = dst.buffer[(dst_tail + n) & MASK].read();
if n > 0 { dst.inner.tail.store(dst_tail + n, Release); }                    // publish the remaining n tasks to dst's own stealers
Some(ret)
```
```rust
fn steal_into2(&self, dst: &mut Local<T>, dst_tail: UnsignedShort) -> UnsignedShort {
    let mut prev_packed = self.0.head.load(Acquire);
    let n = loop {
        let (src_head_steal, src_head_real) = unpack(prev_packed);
        let src_tail = self.0.tail.load(Acquire);
        if src_head_steal != src_head_real { return 0; }                     // another thief is already stealing from this victim → give up
        let n = src_tail.wrapping_sub(src_head_real);   let n = n - n / 2;   // ⌈available/2⌉
        if n == 0 { return 0; }
        let steal_to = src_head_real.wrapping_add(n);
        let next_packed = pack(src_head_steal, steal_to);                    // steal stays at the OLD real; real jumps forward by n  ⇒ "steal in progress"
        match self.0.head.compare_exchange_weak(prev_packed, next_packed, AcqRel, Acquire) { Ok(_) => break n, Err(a) => prev_packed = a }
    };
    // copy src[first .. first+n] → dst[dst_tail .. dst_tail+n]   (first = old real)
    // finish: CAS head (steal, real) → (real, real)                          // clear "in progress": the victim may now reuse those slots
    n
}
```
Worked example — victim has 8 tasks at positions 100..107 (`head = (100,100)`, `tail = 108`):
```
 n = 8 − 8/2 = 4        CAS head → (steal=100, real=104)       ← tasks 100..103 are claimed; owner can still pop 104.. and push (capacity counted from 100)
 copy slots 100..103 into thief's buffer
 CAS head → (104, 104)                                           ← slots 100..103 are free again
 thief runs the last stolen task, publishes the other 3 in its own ring
```
Properties: thieves take the **oldest** tasks (front); a victim can be stolen from by **one thief at a time**; the owner is never blocked (its CAS in `pop` just retries if it loses to a thief's CAS).

### 3.5 Other API
| Method | Purpose |
|---|---|
| `Local::len / remaining_slots / max_capacity / has_tasks` | owner-side introspection; `remaining_slots` counts from `steal` |
| `Local::push_back(iter)` | batch push (used by `next_task` for the inject share); `assert`s `len ≤ 256` and that it **fits** (panics otherwise: the caller pre-limits to `min(remaining_slots, 128)`) |
| `Steal::len / is_empty` | used by `notify_if_work_pending` and metrics |
| `Drop for Local` | `assert!(self.pop().is_none(), "queue not empty")` unless panicking — a worker must drain its ring before dropping it |

---

## 4. Memory-ordering summary

| Access | Ordering | Pairs with |
|---|---|---|
| owner `tail.store(t+1)` after writing the slot | `Release` | thieves' `tail.load(Acquire)` in `steal_into2` |
| owner `tail.unsync_load()` | non-atomic | owner is the only writer |
| `head` CAS in `pop`, `steal_into2` | `AcqRel`/`Acquire` | each other (slot ownership hand-off) |
| `push_overflow` claim CAS | `Release`/`Relaxed` | (only the owner pushes; a failed CAS means a stealer changed `head`) |
| thief's final `(steal,real)→(real,real)` CAS | `AcqRel` | owner's `head.load(Acquire)` before reusing slots |

---

## 5. Communication with other components

| Peer | Direction | Data |
|---|---|---|
| [Worker loop](./05-worker-loop.md) | → queue | `pop`, `push_back`, `push_back_or_overflow(task, &*handle /*Overflow*/, &mut stats)`, `steal_into(&mut my_ring, &mut stats)`, `remaining_slots`, `has_tasks` |
| [Handle](./04-multithread-state-and-spawn.md) | queue → | implements `Overflow`: `push` → `push_remote_task`; `push_batch` → `inject.push_batch` |
| [Inject queue](./07-inject-queue.md) | queue → | the overflow batch (129 `Notified`) |
| [Stats](./10-stats-and-metrics.md) | queue → | `incr_overflow_count`, `incr_steal_count(n)`, `incr_steal_operations` |
| Other workers | `Remote.steal` | `Steal::{steal_into, len, is_empty}` |
| [Task core](../task/05-handles-and-schedule.md) | stores `Notified<Arc<Handle>>` by value | ownership of one ref-count per slot |

---

## 6. Invariants

1. **Single producer:** only the thread holding the `Core` calls `Local::*` (enforced by `&mut self` and the core's exclusivity).
2. Each `Notified` is owned by exactly one place: a slot in `[real, tail)`, a stealer's destination, the inject list, or a polling thread.
3. A slot in `[steal, real)` is *reserved* (being copied) and must not be overwritten.
4. `tail − steal ≤ 256` always.
5. `steal == real` whenever no steal is in progress; at most one steal per victim at a time.
6. The LIFO slot is **not** part of this queue and cannot be stolen (documented limitation: "Eventually, the LIFO slot will become stealable").

---

## 7. Tests

<!-- TESTS:s_queue -->
| Test file | Test fns | Code lines |
|---|---:|---:|
| [`tokio/src/runtime/tests/queue.rs`](../../../tokio/src/runtime/tests/queue.rs) | 7 | 208 |
| [`tokio/src/runtime/tests/loom_multi_thread/queue.rs`](../../../tokio/src/runtime/tests/loom_multi_thread/queue.rs) | 4 | 147 |
| *inline `#[test]` in the source files above* | 1 | – |

_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._
<!-- /TESTS -->

Unit tests (`runtime/tests/queue.rs`): `fits_256_one_at_a_time`, `fits_256_all_at_once`, `fits_256_all_in_chunks`, `overflow`, `steal_batch`, `stress1`, `stress2` (multi-thread stress with a thread pool of thieves). **Loom** (`runtime/tests/loom_multi_thread/queue.rs`): `basic`, `steal_overflow`, `multi_stealer`, `chained_steal` — exhaustive interleavings with capacity 4.

**Read next:** [07 — Inject queue](./07-inject-queue.md).
