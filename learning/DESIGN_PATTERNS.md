# Design patterns in Tokio — with real examples

Every example points to a real place in the snapshot (`8667843`; paths relative to `tokio/src/`). Snippets are trimmed, not invented.
Patterns are grouped as **creational → structural → behavioural → concurrency/systems → Rust-specific idioms**.
Where Tokio's version differs from the textbook one, that is called out — usually because Rust's ownership rules make the pattern cheaper or stricter.

## Index

| # | Pattern | Where (one line) |
|---|---|---|
| 1 | Builder | `runtime::Builder`, `task::Builder` |
| 2 | Facade | `Runtime`, `Handle` |
| 3 | Strategy | `Schedule`, `Overflow` traits |
| 4 | Decorator / Chain of responsibility | driver stack (time → process → signal → io) |
| 5 | Adapter | `PollEvented`, `ReadHalf/WriteHalf`, `AsyncRead`↔`Stream` |
| 6 | Extension trait (blanket impl) | `AsyncReadExt` |
| 7 | Null object | `IoStack::Disabled`, metrics mocks |
| 8 | Bridge by `cfg` | `cfg_*!` macros, stable/unstable metrics |
| 9 | Type erasure / Command via vtable | `RawTask` + `Vtable`, `RawWaker` |
| 10 | State machine | task `State` word, `oneshot`, `Registration` readiness |
| 11 | Typestate / capability types | `Task` → `Notified` → `LocalNotified` |
| 12 | RAII guard / Scope guard | `EnterGuard`, `Reset`, `Scoped`, `MutexGuard`, `Permit` |
| 13 | Observer / Pub-Sub | `broadcast`, `watch`, `Notify` |
| 14 | Mediator / Context object | thread-local `CONTEXT`, `Handle` |
| 15 | Iterator with cleanup | inject `Pop` |
| 16 | Template method | `Schedule` default methods |
| 17 | Reactor | I/O driver (`mio`) + `ScheduledIo` |
| 18 | Work-stealing thread pool | multi-thread scheduler |
| 19 | Object pool | blocking pool threads |
| 20 | Baton / token passing | current-thread `AtomicCell<Core>` |
| 21 | Producer–consumer / Channel | `mpsc`, `oneshot` |
| 22 | Semaphore-as-universal-primitive | `batch_semaphore` under `Mutex`, `RwLock`, `mpsc` bounds |
| 23 | Intrusive collections | `LinkedList`, `OwnedTasks`, waiter lists |
| 24 | Sharding / lock striping | `ShardedList`, `OwnedTasks` |
| 25 | Batching / amortisation | `WakeList`, `MetricsBatch`, inject `push_batch` |
| 26 | Double-checked locking / Dekker handshake | `Idle::worker_to_notify`, `Parker` |
| 27 | Self-tuning feedback control | EWMA `global_queue_interval` |
| 28 | Cooperative scheduling (budget) | `coop::poll_proceed` |
| 29 | Deferred execution | `Defer`, `yield_now` |
| 30 | Hierarchical timing wheel | `runtime/time` |
| 31 | Reference-counting ownership ledger | task ref-count units |
| 32 | Cancellation by drop / token | futures drop, `JoinHandle::abort`, `CancellationToken` |
| 33 | Combinator / wrapper future | `Timeout`, `Instrumented`, `select!` |

---

## Creational

### 1. Builder
`runtime/builder.rs:55` — `pub struct Builder`; chained `&mut self -> &mut Self` setters, terminal `build()`.

```rust
let rt = tokio::runtime::Builder::new_multi_thread()
    .worker_threads(4)
    .enable_all()
    .global_queue_interval(31)
    .build()?;
```
Same style: `task::Builder` (`task/builder.rs:63`, `.name("x").spawn(..)`), `LogHistogramBuilder`, `HistogramBuilder`. Why: dozens of optional knobs (`event_interval`, hooks, stack size, thread name fn …), validated at `build()`; `Config` is the immutable result handed to the scheduler.

---

## Structural

### 2. Facade
`Runtime` (`runtime/runtime.rs`) hides *scheduler flavor + driver stack + blocking pool*: `spawn`, `block_on`, `handle()`, `shutdown_*`. `Handle` (`runtime/handle.rs:13`) is a clonable facade over `scheduler::Handle` (an enum of the two flavors).

### 3. Strategy
Two traits let leaf code stay ignorant of the policy:
```rust
// runtime/task/mod.rs
pub(crate) trait Schedule: Sync + Sized + 'static {
    fn release(&self, task: &Task<Self>) -> Option<Task<Self>>;
    fn schedule(&self, task: Notified<Self>);
    ...
}
// runtime/scheduler/multi_thread/overflow.rs
pub(crate) trait Overflow<T: 'static> { fn push(&self, task: Notified<T>); fn push_batch<I>(&self, iter: I) ... }
```
Concrete strategies for `Schedule`: multi-thread `Handle`, current-thread `Handle`, `LocalSet` shared, `BlockingSchedule` (does nothing). `queue::Local` is tested against a trivial `RefCell<Vec<_>>` overflow instead of the real inject queue.

### 4. Decorator / Chain of responsibility
`runtime/driver.rs` builds layers, each wrapping the previous and delegating `park/park_timeout/shutdown`:
```text
TimeDriver ─wraps→ ProcessDriver ─wraps→ SignalDriver ─wraps→ IoDriver (mio)
```
Each layer does its own post-park work (`signal::Driver::park`: `self.park.park(h); self.process();`, process driver reaps orphans, time driver fires timers). Each of those wrappers exists also as a type alias to the inner one when the feature is off (`type ProcessDriver = SignalDriver`), i.e. a decorator that compiles away.

### 5. Adapter
- `io/poll_evented.rs:66` `PollEvented<E: Source>` adapts a raw `mio` source to `AsyncRead/AsyncWrite` via `Registration` + readiness polling. `TcpStream` is a thin wrapper over it.
- `io/split.rs` `ReadHalf<T>`/`WriteHalf<T>` adapt one `AsyncRead+AsyncWrite` into two halves (shared through a lock); `TcpStream::split` (`net/tcp/stream.rs:1426`, borrowed) vs `into_split` (`:1441`, owned halves via `Arc`).
- `tokio-stream` adapts `AsyncRead`/channels/intervals into `Stream`.

### 6. Extension trait with blanket impl
`io/util/async_read_ext.rs:1456`:
```rust
impl<R: AsyncRead + ?Sized> AsyncReadExt for R {}
```
The core trait (`AsyncRead::poll_read`, `io/async_read.rs:44`) is minimal; ergonomics (`read_u32`, `read_exact`, `take`, `chain`, `lines`…) live in the extension trait, each returning a small future struct. Same for `AsyncWriteExt`, `AsyncBufReadExt`, `StreamExt`.

### 7. Null Object
- `runtime/driver.rs:147`: `IoStack::Disabled(ParkThread)` / `IoHandle::Disabled(UnparkThread)` — with I/O off the runtime still has a "driver", it just parks the thread.
- `runtime/metrics/mock.rs`: empty `SchedulerMetrics`, `HistogramBuilder` with the same method names doing nothing, so call sites need no `if`.
- `ScheduleLatencyInstant/Context` mock when the feature is off.

### 8. Bridge by conditional compilation
Instead of `dyn` indirection, **feature flags select the implementation at compile time**: `macros/cfg.rs` defines `cfg_rt!`, `cfg_io_driver!`, `cfg_time!`, `cfg_unix!`… and `cfg_metrics_variant! { stable: {…}, unstable: {…} }` compiles the same method as an empty body in stable builds. Hot paths pay nothing for disabled features.

### 9. Type erasure / Command object (hand-rolled vtable)
`runtime/task/raw.rs:24` `Vtable { poll, schedule, dealloc, try_read_output, drop_join_handle_slow, drop_abort_handle, shutdown, trailer_offset, … }` — a `&'static` table per `(Future, Schedule)` pair; queues, `JoinHandle`, `Waker` hold only `NonNull<Header>` and call `(header.vtable.poll)(ptr)`. The same trick is used for `RawWakerVTable` in `task/waker.rs`. Why not `dyn`? One thin pointer, const-computed field offsets, control over drop/dealloc order.

---

## Behavioural

### 10. State machine
`runtime/task/state.rs`: the whole task lifecycle is **one `AtomicUsize`** (`RUNNING, COMPLETE, NOTIFIED, JOIN_INTEREST, JOIN_WAKER, CANCELLED | ref-count`). Every transition is a CAS loop that returns an enum telling the caller what to do next:
```rust
enum TransitionToRunning { Success, Cancelled, Failed, Dealloc }
enum TransitionToIdle    { Ok, OkNotified, OkDealloc, Cancelled }
```
Other state machines: `oneshot` (`Inner` + state bits), `ScheduledIo` readiness, `Parker` (`EMPTY/PARKED_CONDVAR/PARKED_DRIVER/NOTIFIED`), `Idle` counters, semaphore permits.

### 11. Typestate / capability types
`Task<S>`, `Notified<S>` (`runtime/task/mod.rs:245`), `LocalNotified<S>`, `UnownedTask<S>` are all `NonNull<Header>` wrappers whose **type says what you may do**: only a `Notified` can be scheduled, only a `LocalNotified` (checked by `OwnedTasks::assert_owner`) can be `run()`. Moving the value is the transition; you cannot schedule the same task twice. (`mpsc::Permit` — "reserve a slot, then send" — is the same idea.)

### 12. RAII guard / scope guard
- `runtime/context/current.rs:11` `SetCurrentGuard` and `runtime/handle.rs:34` `EnterGuard` restore the previous runtime handle on drop.
- `runtime/context/scoped.rs:5` `Scoped<T>` sets a thread-local pointer for the duration of a closure; an inner `Reset` restores it, panic-safe.
- `block_in_place` (`multi_thread/worker.rs:369`) defines a local `struct Reset { take_core, budget }` whose `Drop` steals the Core back and restores the coop budget — even if the closure panics.
- `sync::MutexGuard`, `RwLock*Guard`, `Permit`, `SemaphorePermit`.

### 13. Observer / Publish–Subscribe
- `sync::broadcast` (`:179` `Sender`): one producer, many receivers each with a cursor into a ring of slots — every receiver sees every message.
- `sync::watch` (`:197`): "latest value" observers with change notification (`changed().await`).
- `sync::Notify` (`:199`): wake-up signal without data. Waiters live in an intrusive list inside their own pinned futures.

### 14. Mediator / Context object
Thread-local `CONTEXT` (`runtime/context.rs:82`) holds the current runtime handle, scheduler context, coop budget, RNG, current task id. Resources (sleep, spawn, sockets) never get passed a runtime; they ask the mediator (`Handle::current()`, `context::defer(waker)`, `with_scheduler`). Trade-off: implicit dependency, but avoids threading a handle through every API.

### 15. Iterator with cleanup-on-drop
`runtime/scheduler/inject/pop.rs`: `Pop<'a,T>` borrows `&mut Synced` (so the lock is held), implements `Iterator + ExactSizeIterator`, and its `Drop` drains whatever the consumer did not take, keeping the queue's `len` consistent.

### 16. Template method
`Schedule` has default bodies: `yield_now` → `self.schedule(task)`, `unhandled_panic` → no-op. Implementations override only the hooks they need (multi-thread overrides `yield_now` to push to the back; current-thread/`LocalSet` override `unhandled_panic`).

---

## Concurrency / systems patterns

### 17. Reactor
`runtime/io/driver.rs`: one `mio::Poll` loop (`turn`) dispatches readiness events to `ScheduledIo` objects, which hold the wakers of tasks waiting on that fd. Resources register interest (`Registration`), poll readiness, and re-register on `WouldBlock` (clearing readiness). Tasks are the "handlers" invoked through `Waker::wake`.

### 18. Work-stealing thread pool
`scheduler/multi_thread/`: per-worker 256-slot SPMC ring + LIFO slot, global inject queue, idle workers *search* and steal half of a victim's ring (`queue.rs`), `Idle` bounds searchers to half the workers. Details: [`core/scheduler/05–08`](./core/README.md).

### 19. Object pool
`runtime/blocking/pool.rs` (`BlockingPool`): worker threads are spawned on demand up to `max_blocking_threads`, idle ones wait with a keep-alive (`KEEP_ALIVE = 10s`) and are reused. The multi-thread scheduler's own workers are launched on this pool.

### 20. Baton passing
Current-thread scheduler: `AtomicCell<Core>`; whichever thread holds the `Core` drives the runtime; `block_on` callers on other threads wait on a `Notify` for the baton. Multi-thread `block_in_place` hands a `Box<Core>` through `AtomicCell` the same way.

### 21. Producer–consumer / channels
`sync::mpsc` (`Chan<T, S>` in `mpsc/chan.rs:52`, block-linked list, bounded via semaphore, unbounded via counter), `oneshot` (single value, `Inner<T>`), `broadcast`, `watch`. Back-pressure comes from permits (`reserve()` → `Permit`).

### 22. One primitive, many uses
`sync/batch_semaphore.rs` is a fair (FIFO) async semaphore with an intrusive waiter list (`Waiter`, `:79`). `Mutex` is a semaphore with 1 permit; `RwLock` uses `MAX_READS` permits; bounded `mpsc` capacity is a semaphore; `Semaphore` is the public wrapper.

### 23. Intrusive collections
Nodes live *inside* the objects they link, so no allocation per insertion: `util/linked_list.rs` (`unsafe trait Link`), task `Trailer.owned` pointers for `OwnedTasks`, `Header.queue_next` for the inject queue, waiter nodes inside pinned futures for `Notify`/semaphore. Removal on drop gives cancellation safety.

### 24. Lock striping
`util/sharded_list.rs` (`ShardedList`, `ShardGuard` at `:36`, `lock_shard` at `:90`): N mutex-protected lists chosen by task id; shutdown workers start at random shards to spread contention.

### 25. Batching / amortisation
`util/wake_list.rs` (`WakeList`: collect wakers under a lock, wake after unlocking), `MetricsBatch` (plain counters flushed with `Relaxed` stores), inject `push_batch` (link outside the lock, one lock acquisition), steal-half, `global_queue_interval`.

### 26. Double-checked locking & Dekker-style handshake
`Idle::worker_to_notify`: cheap `SeqCst` check without lock → lock → check again → mutate. `Parker::unpark` uses `swap(NOTIFIED)` (not CAS) so the release store always happens. Pattern in the comments: "this load must happen before the thread transitioning `num_searching` to zero".

### 27. Feedback control (self-tuning)
`multi_thread/stats.rs`: EWMA of poll time → `global_queue_interval = clamp(200µs / ewma, 2, 127)` with hysteresis (`abs_diff > 2`). Runnable analogue: `learning/dsa-exercises/src/ewma.rs`.

### 28. Cooperative scheduling
`task/coop/mod.rs`: each poll gets `Budget(128)`; resources call `poll_proceed(cx)`; at zero they return `Pending` after deferring their waker. A `RestoreOnPending` guard refunds the unit if the operation made no progress.

### 29. Deferred execution
`runtime/scheduler/defer.rs`: `yield_now()` and budget exhaustion park the *waker* in a per-thread list that the scheduler drains only after running ready tasks and polling the driver. Guarantees a real yield.

### 30. Hierarchical timing wheel
`runtime/time/wheel/`: 6 levels × 64 slots, O(1) insert/cancel, cascading on level rollover; entries are intrusive nodes. See `learning/dsa-exercises` timer-wheel exercise.

### 31. Reference-count ownership ledger
A task starts with 3 ref units (OwnedTasks `Task`, scheduler `Notified`, `JoinHandle`); every handle type *is* one unit and is moved, never cloned silently; dealloc happens when the count reaches 0 inside a state transition. Documented as a table in [`core/task/01`](./core/task/01-state-word.md).

---

## Rust-specific idioms

### 32. Cancellation by drop
Dropping a future cancels it; intrusive waiters unlink in `Drop`; `JoinHandle::abort()` sets `CANCELLED` and the harness drops the future on the next poll/shutdown. `tokio-util::CancellationToken` (`:57`) adds hierarchical, explicit cancellation.

### 33. Combinator / wrapper futures
`time::Timeout<T>` (`time/timeout.rs:179`, polls inner, then the `Sleep`), `Instrumented`/trace wrappers, `JoinSet`, `select!` (`macros/select.rs`: random start branch for fairness, polls all branches in one `poll_fn`), `poll_fn`. Pattern: a pinned struct with `pin_project`-style projection and a `poll` that delegates and decorates.

---

## How to spot more
- Search for `impl Drop for` → RAII guards / unlink-on-drop.
- `grep -n "unsafe trait\|Vtable"` → type-erasure and intrusive structures.
- `cfg_*!` macro usage → compile-time bridge.
- Enums returned from `State::transition_*` → command/result style state machines.
