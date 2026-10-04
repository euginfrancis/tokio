# The core of Tokio: **Task** and **Scheduler** — component-by-component deep dive

One Markdown file per component. Each page follows the same outline as [`../components/`](../components/README.md):
**responsibility & boundary → files & LOC → data structures (real code) → interactions → functions → flows → invariants → tests**,
and every claim was checked against the source snapshot (`8667843`).

## Map

```text
                       user code:  tokio::spawn · JoinHandle · Runtime::block_on · block_in_place · yield_now
                                   │
 ┌─────────────────────────────────▼────────────────────────────────────────────────────────────────────┐
 │ RUNTIME FACADE        Runtime · Handle · Builder · Config                          sched/01          │
 │ THREAD-LOCAL CONTEXT  CONTEXT { current handle, scheduler ctx, budget, rng }       sched/02          │
 ├──────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │ SCHEDULERS                                                                                           │
 │   current-thread  (AtomicCell core "baton" + Notify)                               sched/03          │
 │   multi-thread    Handle/Shared/Remote/Core        sched/04 · worker loop          sched/05          │
 │      ├ local ring (256, SPMC, steal)               sched/06                                          │
 │      ├ inject queue (Mutex, intrusive FIFO)        sched/07                                          │
 │      ├ Idle (searching/unparked/sleepers)          sched/08                                          │
 │      ├ Parker (condvar | driver TryLock)           sched/09                                          │
 │      ├ Stats (EWMA) & metrics                      sched/10                                          │
 │      ├ block_in_place + Defer                      sched/11                                          │
 │      └ ordered shutdown                            sched/12                                          │
 │   Driver interface (time→process→signal→io)       sched/13                                          │
 ├───────────────────────────  trait Schedule  ·  Notified / Waker  ───────────────────────────────────┤
 │ TASK                                                                                                 │
 │   State word 01 · Cell layout 02 · RawTask+Vtable 03 · Harness 04 · Handles+Schedule 05              │
 │   Waker 06 · JoinHandle/Abort/JoinError 07 · OwnedTasks (+linked/sharded list) 08 · Id/hooks 09      │
 │   Cooperative budget 10                                                                              │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Cross-cutting pages (read these to see *how the pieces connect*)

| Page | What it answers |
|---|---|
| [`INTERFACES_AND_DTOS.md`](./INTERFACES_AND_DTOS.md) | Which traits/vtables are the contracts (`Schedule`, `Vtable`, `Overflow`, `Link`, driver, hooks) and which values cross boundaries (`Task`/`Notified`/`LocalNotified`, state-transition enums, `Config`, `Core`, `Pop`, …) |
| [`COMMUNICATION.md`](./COMMUNICATION.md) | Who calls whom (matrix), 8 sequence diagrams (spawn inside/outside, I/O wake-up, poll+completion, stealing, overflow, `block_in_place`, shutdown) and the synchronisation primitive used at each boundary |

## Task (`tokio/src/runtime/task/` + helpers) — [`task/`](./task)

| # | Page | One-line summary |
|---|---|---|
| 01 | [State word](./task/01-state-word.md) | One `AtomicUsize` = 6 flag bits + ref-count; transition table, orderings, ref-count ledger |
| 02 | [Cell layout](./task/02-cell-layout.md) | `Cell = Header \| Core \| Trailer`, `repr(C)`, measured sizes, const offsets |
| 03 | [RawTask & Vtable](./task/03-rawtask-vtable.md) | Type erasure by hand: `NonNull<Header>` + function-pointer table |
| 04 | [Harness](./task/04-harness.md) | poll / complete / shutdown / join-read algorithms over the state machine |
| 05 | [Handles & `Schedule`](./task/05-handles-and-schedule.md) | `Task`, `Notified`, `LocalNotified`, `UnownedTask`; the scheduler contract |
| 06 | [Waker](./task/06-waker.md) | `RawWakerVTable` built on the header; wake-by-ref/by-val; `will_wake` |
| 07 | [JoinHandle / AbortHandle / JoinError](./task/07-join-abort-error.md) | Output retrieval, abort, drop protocol, `JoinError` |
| 08 | [OwnedTasks & lists](./task/08-owned-tasks.md) | Sharded intrusive lists, `closed` flag, id→shard |
| 09 | [Ids, hooks, metadata](./task/09-id-hooks-metadata.md) | `task::Id`, `TaskMeta`, spawn/terminate/poll hooks, schedule latency |
| 10 | [Cooperative budget](./task/10-coop-budget.md) | 128-poll budget, `poll_proceed`, `RestoreOnPending`, `unconstrained` |

## Scheduler (`tokio/src/runtime/scheduler/` + facade/driver glue) — [`scheduler/`](./scheduler)

| # | Page | One-line summary |
|---|---|---|
| 01 | [Runtime, Handle, Builder](./scheduler/01-runtime-handle-builder.md) | Public facade, config assembly, flavors |
| 02 | [Thread-local context](./scheduler/02-context-thread-local.md) | `CONTEXT`, `Scoped`, enter/exit guards, budget & rng cells |
| 03 | [Current-thread scheduler](./scheduler/03-current-thread.md) | One thread, core "baton", `block_on` loop, `Notify` |
| 04 | [Multi-thread: state & spawn](./scheduler/04-multithread-state-and-spawn.md) | `Handle`, `Shared`, `Remote`, `Core`, `Worker`; spawn paths |
| 05 | [Worker loop](./scheduler/05-worker-loop.md) | tick/maintenance, `next_task`, LIFO chain, stealing, park |
| 06 | [Local queue](./scheduler/06-local-queue.md) | 256-slot SPMC ring, packed head, overflow, steal |
| 07 | [Inject queue](./scheduler/07-inject-queue.md) | Global intrusive FIFO behind one mutex, `len` fast path |
| 08 | [Idle coordination](./scheduler/08-idle-coordination.md) | Searching/unparked counters, sleepers, anti-lost-wakeup rules |
| 09 | [Parker](./scheduler/09-parker.md) | 4-state park/unpark; who gets the driver |
| 10 | [Stats & metrics](./scheduler/10-stats-and-metrics.md) | EWMA tuning of `global_queue_interval`, batched counters, histograms |
| 11 | [`block_in_place` & Defer](./scheduler/11-block-in-place-and-defer.md) | Core hand-off to another thread; "wake after the driver" queue |
| 12 | [Shutdown](./scheduler/12-shutdown.md) | Two close bits, per-worker cancel, last-worker cleanup |
| 13 | [Driver interface](./scheduler/13-driver-interface.md) | The decorator stack behind `park`/`unpark`; event → wake → task path |

## Size of the core (snapshot `8667843`; generated by [`core_stats.py`](./core_stats.py))

| Scope | Source files | Code lines | Docs + comments | Share of `tokio/src` code (50,599) |
|---|---:|---:|---:|---:|
| Task docs (`runtime/task`, `task::coop`, `task_hooks`, `linked_list`, `sharded_list`) | 17 | 3,253 | 1,900 | 6.4% |
| Scheduler docs (scheduler, facade, context, metrics, driver glue + I/O/time/signal/process entry files, blocking pool) | 47 | 7,875 | 5,235 | 15.6% |
| **Both (unique files)** | **64** | **11,128** | **7,135** | **22.0%** |

Per-component line counts, function counts and test counts are in each page's "files" and "tests" tables and in [`core_stats.json`](./core_stats.json).
Regenerate: `python3 learning/core/core_stats.py` (run from the repo root; needs `learning/functions/functions.csv`).

## Suggested reading order

1. Task **01 → 05** (state word, layout, vtable, harness, handles) – the "what is a task" half.
2. Scheduler **03** (simplest scheduler) then **04 → 06** (multi-thread data + worker loop + ring).
3. [`COMMUNICATION.md`](./COMMUNICATION.md) sequences S1, S4, S5 to tie both halves together.
4. Scheduler **07 → 09** (inject, idle, parker) – the sleep/wake protocol.
5. Task **06–10**, scheduler **10–13** – the edges (waker, join, coop, metrics, block-in-place, shutdown, drivers).
6. Try the exercises in [`../dsa-exercises`](../dsa-exercises) (`work-stealing queue`, `task state`, `EWMA`) to see these algorithms in safe Rust.
