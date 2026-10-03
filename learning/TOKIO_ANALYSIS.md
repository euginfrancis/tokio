# Tokio — Codebase Analysis & Learning Guide

> Snapshot: `tokio-rs/tokio` @ `8667843` (2026-10-03, "rt: skip non-idle tasks during taskdumps (#8568)")
> Local clone: `/home/user/tokio`, branch `learn/explore-tokio`
> Measured with [`loc.py`](./loc.py) (counts code / `//` comments / `///`+`//!` doc comments / blank lines per file)

---

## 1. At a glance

| Metric | Value |
|---|---|
| Total files (excl. `.git`) | **883** |
| Rust source files (`.rs`) | **808** (91.5% of files) |
| Total Rust lines | **185,227** |
| Rust **code** lines | **103,257** |
| Doc-comment lines (`///`, `//!`) | **51,075** |
| Regular comment lines (`//`, `/* */`) | **7,955** |
| Blank lines | **22,940** |
| Crate versions | `tokio 1.53.1`, `tokio-util 0.7.19`, `tokio-stream 0.1.19`, `tokio-macros 2.7.2`, `tokio-test 0.4.6` |
| MSRV (min. Rust version) | **1.85** |
| Commits / contributors | **4,725** commits by **1,082** people (first commit 2016-07-30) |
| Test functions in `tokio/tests/` | **~1,313** (`#[test]` + `#[tokio::test]`) across 192 files |
| Files in `tokio/src` using `unsafe` | **141** (~1,076 occurrences) |

### What a Rust line in Tokio is made of

```
Code      ██████████████████████████░░░░░░░░░░░░░░░░░░░░░░  55.7%  103,257
Docs      █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  27.6%   51,075
Blank     ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12.4%   22,940
Comments  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4.3%    7,955
```

**Takeaway:** almost 1 in 3 lines is documentation. Tokio's docs *are* its tutorial — and the doc examples are compiled and run as tests (doctests). Writing/fixing docs is a very real way to contribute.

### File types

| Extension | Files | Lines |
|---|---:|---:|
| `.rs` | 808 | 185,227 |
| `.md` | 29 | 7,641 |
| `.yml` (CI) | 11 | 1,926 |
| `.toml` | 18 | 911 |
| `.stderr` (compile-fail test expectations) | 6 | 441 |
| other | 11 | 523 |

---

## 2. The workspace: crates and their share

Tokio is a **Cargo workspace** — several crates in one repo.

| Crate / dir | Files | Code LOC | % of code | Purpose |
|---|---:|---:|---:|---|
| `tokio/` | 571 | 79,352 | **76.8%** | The runtime + all async primitives. *This is Tokio.* |
| `tokio-util/` | 90 | 12,586 | 12.2% | Extras: codecs/framing, `CancellationToken`, `DelayQueue`, compat layers |
| `tokio-stream/` | 72 | 5,353 | 5.2% | `Stream` trait adapters/wrappers (`StreamExt`, `wrappers::*`) |
| `benches/` | 18 | 2,082 | 2.0% | Criterion benchmarks |
| `examples/` | 20 | 1,306 | 1.3% | Runnable examples (echo server, chat, etc.) — **start here** |
| `tokio-test/` | 10 | 1,185 | 1.1% | Testing helpers (`io::Builder` mocks, `task::spawn`, `assert_ready!`) |
| `tokio-macros/` | 3 | 801 | 0.8% | Proc macros: `#[tokio::main]`, `#[tokio::test]` |
| `tests-integration/` | 9 | 315 | 0.3% | Cross-crate / process integration tests |
| `tests-build/` | 14 | 232 | 0.2% | Compile-fail tests (`trybuild`) for the macros |
| `stress-test/` | 1 | 45 | <0.1% | Long-running stress test |

```
tokio          ██████████████████████████████████████░░░░░░░░░░░░  76.8%
tokio-util     ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12.2%
tokio-stream   ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   5.2%
benches        █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2.0%
examples       █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   1.3%
everything else ▏                                                    2.5%
```

### Source vs. tests (code lines)

| Crate | `src/` | `tests/` | Test share |
|---|---:|---:|---:|
| `tokio` | 50,599 (378 files) | 28,748 (192 files) | 36% |
| `tokio-util` | 6,437 | 6,149 | 49% |
| `tokio-stream` | 3,203 | 2,094 | 40% |
| `tokio-test` | 811 | 374 | 32% |

Plus: many `tokio/src` modules have inline `#[cfg(test)]` modules and **loom** model tests (e.g. `runtime/tests/`, `sync/tests/`) that are counted under `src`.

---

## 3. Inside the `tokio` crate — module breakdown

`tokio/src` = **50,599 code lines**. Each top-level module maps to a Cargo feature (`rt`, `sync`, `net`, `fs`, …; `full` enables all). Nothing is on by default.

| Module | Files | Code | % of src | Doc+comment lines | Doc/code ratio | What it is |
|---|---:|---:|---:|---:|---:|---|
| `runtime/` | 127 | 17,760 | **35.1%** | 9,147 | 0.52 | The engine: schedulers, task system, I/O & time drivers, blocking pool, metrics |
| `sync/` | 41 | 9,135 | **18.1%** | 10,488 | 1.15 | `Mutex`, `RwLock`, `Semaphore`, `Notify`, channels (`mpsc`, `oneshot`, `broadcast`, `watch`), `OnceCell`, `Barrier` |
| `io/` | 63 | 6,315 | 12.5% | 6,320 | 1.00 | `AsyncRead`/`AsyncWrite` traits, `AsyncReadExt`/`WriteExt`, `BufReader`, `split`, `copy`, `AsyncFd`, stdio, io_uring |
| `net/` | 23 | 4,589 | 9.1% | 10,228 | **2.23** | `TcpListener`/`TcpStream`, `UdpSocket`, Unix sockets, Windows named pipes, DNS lookup |
| `fs/` | 30 | 2,614 | 5.2% | 1,938 | 0.74 | Async filesystem (wraps std via the blocking pool, or io_uring on Linux w/ unstable) |
| `util/` | 24 | 1,927 | 3.8% | 521 | 0.27 | Internal: intrusive linked list, slabs, `AtomicCell`, RNG, `WakeList`, … |
| `process/` | 7 | 1,888 | 3.7% | 1,198 | 0.63 | `Command`, `Child` — async child processes |
| `macros/` | 11 | 1,742 | 3.4% | 1,124 | 0.65 | `select!`, `join!`, `try_join!`, `pin!`, and the `cfg_*!` feature-gating macros |
| `task/` | 11 | 1,685 | 3.3% | 2,421 | 1.44 | Public task API: `spawn`, `spawn_blocking`, `JoinSet`, `LocalSet`, `task_local!`, `yield_now`, coop budgeting |
| `signal/` | 8 | 906 | 1.8% | 874 | 0.96 | Unix signals / Windows ctrl-c |
| `time/` | 7 | 769 | 1.5% | 1,249 | 1.62 | Public time API: `sleep`, `timeout`, `interval`, `Instant` (the timer *engine* is in `runtime/time`) |
| `loom/` | 16 | 736 | 1.5% | 182 | 0.25 | Shim that swaps std atomics/threads for `loom` versions under `--cfg loom` |
| `future/` | 5 | 212 | 0.4% | 16 | — | Small future helpers |
| root (`lib.rs`, `blocking.rs`) | 3 | 262 | 0.5% | 538 | — | Crate root, re-exports, top-level docs |
| `doc/` | 2 | 59 | 0.1% | 46 | — | Doc-only stubs |

```
runtime   █████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  35.1%
sync      █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  18.1%
io        ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12.5%
net       ████▌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9.1%
fs        ██▌░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   5.2%
util      █▉░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.8%
process   █▉░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.7%
macros    █▋░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.4%
task      █▋░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.3%
others    ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   5.8%
```

**Observations**
- **`runtime` + `sync` = 53%** of the crate. That's the hard, concurrency-heavy core.
- **`net` has 2.2× more docs than code** — the public networking API is thin wrappers over `mio` plus heavy documentation.
- `runtime` has the *lowest* doc ratio among big modules (0.52): it is internal (`pub(crate)`), documented with design comments for maintainers rather than users.

### 3a. `runtime/` drill-down (17,760 code lines)

| Submodule | Files | Code | % of runtime | Role |
|---|---:|---:|---:|---|
| `scheduler/` | 28 | 3,535 | 19.9% | `current_thread` and `multi_thread` (work-stealing) schedulers, inject queue |
| `task/` | 15 | 2,701 | 15.2% | Task memory layout, atomic state machine, ref-counting, `JoinHandle`, wakers, task dumps |
| `tests/` | 15 | 2,123 | 12.0% | Loom model tests for the runtime internals |
| `metrics/` | 11 | 1,671 | 9.4% | `RuntimeMetrics` (worker counts, poll counts, histograms) |
| `time/` | 7 | 1,331 | 7.5% | Hierarchical timer wheel driver |
| `time_alt/` | 13 | 1,270 | 7.2% | Alternative timer implementation (only with `tokio_unstable` + `rt-multi-thread`) |
| `io/` | 8 | 1,137 | 6.4% | I/O driver (the "reactor"): `mio::Poll`, `ScheduledIo`, readiness registration, io_uring driver |
| `blocking/` | 6 | 916 | 5.2% | Thread pool for `spawn_blocking` (also backs `fs`) |
| `builder.rs` | 1 | 586 | 3.3% | `runtime::Builder` — all the knobs |
| other files | — | 2,490 | 14.0% | `driver.rs`, `park.rs`, `handle.rs`, `context/`, `local_runtime/`, `dump.rs`, … |

### 3b. `tokio-util` drill-down (6,437 src code lines)

| Module | Code | % | Highlights |
|---|---:|---:|---|
| `codec/` | 1,336 | 20.8% | `Framed`, `Decoder`/`Encoder`, `LengthDelimitedCodec`, `LinesCodec` |
| `task/` | 1,158 | 18.0% | `JoinMap`, `TaskTracker`, `LocalPoolHandle` |
| `sync/` | 1,024 | 15.9% | `CancellationToken`, `PollSemaphore`, `PollSender` |
| `io/` | 961 | 14.9% | `ReaderStream`, `StreamReader`, `SyncIoBridge`, `InspectReader` |
| `time/` | 895 | 13.9% | `DelayQueue` (+ its own wheel) |
| other | 1,063 | 16.5% | `compat` (futures-io bridge), `either`, `udp::UdpFramed`, `net`, … |

### 3c. Largest files (by code lines)

| Code | Docs | File | Note |
|---:|---:|---|---|
| 1,283 | 3 | `tokio/tests/sync_mpsc.rs` | test |
| 1,050 | 14 | `tokio/tests/rt_common.rs` | test — same suite run against every runtime flavor |
| **939** | 189 | `tokio/src/runtime/scheduler/multi_thread/worker.rs` | **the heart of the multi-threaded scheduler** |
| 742 | 549 | `tokio/src/macros/select.rs` | `select!` macro |
| 683 | 34 | `tokio/src/macros/cfg.rs` | feature-gating macros (`cfg_rt!`, `cfg_net!`, …) |
| 650 | 5 | `tokio-macros/src/entry.rs` | `#[tokio::main]` / `#[tokio::test]` |
| 634 | 642 | `tokio/src/sync/mutex.rs` | async `Mutex` |
| 634 | 398 | `tokio/src/fs/file.rs` | async `File` |
| 627 | 1,080 | `tokio/src/process/mod.rs` | `Command` / `Child` |
| 623 | 64 | `tokio/src/runtime/scheduler/current_thread/mod.rs` | single-threaded scheduler |
| 623 | 1,607 | `tokio/src/net/udp.rs` | `UdpSocket` |
| 619 | 898 | `tokio/src/sync/broadcast.rs` | broadcast channel |
| 594 | 528 | `tokio/src/sync/notify.rs` | `Notify` — a building block for many other primitives |
| 592 | 2,004 | `tokio/src/net/windows/named_pipe.rs` | most-documented file in the repo |

---

## 4. How Tokio works — high-level, then in depth

### 4.1 The one-paragraph version

Rust `async fn`s compile into **state machines that implement `Future`**. A future does nothing on its own; something must repeatedly call `poll()` on it. Tokio is that "something": an **executor** (schedulers that poll tasks) glued to **drivers** (an OS event loop for I/O and a timer wheel) that know *when* a task is worth polling again. A future that can't make progress returns `Poll::Pending` after registering its **`Waker`** with a driver; when the OS reports readiness or a timer fires, the driver calls `wake()`, which puts the task back on a run queue.

### 4.2 The big picture

```
 your code                       tokio::spawn(fut)
    │                                   │
    ▼                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ RUNTIME  (runtime::Builder → Runtime / Handle)                         │
│                                                                       │
│  ┌──────────── task/ ─────────────┐     ┌──────── scheduler/ ───────┐ │
│  │ Task = Header | Core | Trailer │     │ current_thread  OR        │ │
│  │  state: AtomicUsize bitfield   │───▶ │ multi_thread (work-steal) │ │
│  │  RUNNING|COMPLETE|NOTIFIED|... │     │  per-worker local queue   │ │
│  │  + ref-count in upper bits     │     │  + LIFO slot + global     │ │
│  │ JoinHandle / Waker / Notified  │     │    inject queue           │ │
│  └────────────────────────────────┘     └────────────┬──────────────┘ │
│              ▲  wake() → schedule()                   │ poll()         │
│              │                                        ▼                │
│  ┌───────────┴──────── driver (park/unpark) ─────────────────────────┐ │
│  │  io/   : mio::Poll (epoll / kqueue / IOCP) → ScheduledIo readiness │ │
│  │          (+ io_uring driver on Linux, tokio_unstable)              │ │
│  │  time/ : hierarchical timing wheel (6 levels × 64 slots)           │ │
│  │  signal: self-pipe into the I/O driver                             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│  ┌──────── blocking/ ────────┐                                         │
│  │ thread pool for            │◀── spawn_blocking, fs::*, stdio        │
│  │ spawn_blocking (fs, stdio) │                                         │
│  └────────────────────────────┘                                         │
└───────────────────────────────────────────────────────────────────────┘
        ▲ used by the public APIs: net/, io/, fs/, time/, sync/, process/, signal/
```

### 4.3 Life of a task (follow this in the code)

1. **`#[tokio::main]`** (`tokio-macros/src/entry.rs`) rewrites `async fn main` into: build a `Runtime`, then `block_on(your_body)`.
2. **`tokio::spawn(fut)`** (`tokio/src/task/spawn.rs`) → `Handle::spawn` → the scheduler allocates a task (`runtime/task/core.rs`: a single heap allocation holding `Header` (state + vtable), `Core` (the future or its output), `Trailer` (join waker)).
3. The task is **bound** to the runtime's `OwnedTasks` list (so shutdown can find and cancel it) and a `Notified` handle is pushed onto a run queue.
4. A **worker** (`runtime/scheduler/multi_thread/worker.rs`) pops it and calls `poll` through `runtime/task/harness.rs`, which flips the `RUNNING` bit (acting as a lock), polls the future, and handles completion/cancellation/panics.
5. If the future returns **`Pending`**, it has already stored the task's `Waker` somewhere — e.g. in a `ScheduledIo` slot for a socket, a timer entry in the wheel, or a waiter list of a `Mutex`/`Notify`.
6. When the worker has nothing to do it **parks** on the driver (`runtime/driver.rs`, `park.rs`): it blocks in `epoll_wait` (via mio) with a timeout equal to the next timer deadline.
7. The OS says "socket readable" → the I/O driver sets readiness bits and **wakes** the waker → `schedule()` pushes the task back onto a queue → goto 4.
8. When the future returns **`Ready(output)`**, the output is stored in `Core`, `COMPLETE` is set, and the `JoinHandle`'s waker (if any) is notified.

### 4.4 The multi-threaded scheduler, in depth

From `runtime/scheduler/multi_thread/{worker,queue,stats}.rs`:

- **N workers**, one OS thread each (default = number of CPU cores). Each worker owns a **`Core`** with its run queue.
- **Local queue**: fixed-size ring buffer of **256** tasks (`LOCAL_QUEUE_CAPACITY`), lock-free, single-producer / multi-consumer. When it overflows, **half** of it is moved to the global queue in one batch.
- **LIFO slot**: a newly woken task that was spawned/woken *by the currently running task* goes into a one-element "LIFO slot" and runs next — great for request/response ping-pong (cache-hot). It can be disabled with `Builder::disable_lifo_slot` (unstable API).
- **Global inject queue**: a mutex-protected queue used for tasks spawned from outside a worker. Workers check it periodically; the interval is **self-tuning** (targets ~200µs between checks, `stats.rs`) unless you set `Builder::global_queue_interval`.
- **Work stealing**: an idle worker picks a random sibling and **steals half** its local queue before going to sleep.
- **Event interval = 61** ticks: how often a worker polls the I/O/timer drivers even while busy, so I/O events aren't starved.
- **`block_in_place`**: hands the worker's `Core` to a *new* thread so the scheduler keeps going while the current thread blocks.
- **Shutdown** is a carefully ordered protocol (close inject queue + `OwnedTasks`, drain, last worker finishes) — the doc comment at the top of `worker.rs` explains why both queues need a "closed" bit to avoid leaks. Worth reading in full.

`current_thread` (`scheduler/current_thread/mod.rs`) is the same idea with one queue and one thread — **read it first**, it's much easier.

### 4.5 Cooperative scheduling (task budget)

Futures are not preempted. A task that keeps getting `Ready` (e.g. reading from a fast channel in a loop) could hog a worker forever. Tokio gives each task a **budget of 128** operations per poll (`task/coop/mod.rs`). Tokio resources call `coop::poll_proceed`; once the budget is exhausted they return `Pending` and immediately wake the task, forcing a yield back to the scheduler.

### 4.6 The I/O driver ("reactor")

- `runtime/io/driver.rs` wraps a `mio::Poll`. Each registered socket gets a **`ScheduledIo`** (`scheduled_io.rs`) with an atomic readiness word + reader/writer waker lists.
- Public types like `TcpStream` hold a `PollEvented<mio::net::TcpStream>` (`io/poll_evented.rs`). On `poll_read`: try the syscall; on `WouldBlock`, clear the readiness bit and register the waker; return `Pending`.
- `AsyncFd` (`io/async_fd.rs`) exposes the same mechanism for any raw file descriptor you own.
- **io_uring** (`io/uring/`, `runtime/io/driver/uring.rs`) is an experimental Linux backend for some `fs` ops (open/read/write/statx/rename) behind `--cfg tokio_unstable`.

### 4.7 The time driver

- `runtime/time/wheel/`: a **hierarchical timing wheel** with **6 levels × 64 slots** (`NUM_LEVELS = 6`, `BITS_PER_LEVEL = 6`), 1 ms resolution → covers ~2 years. Inserting / cancelling a timer is O(1).
- `sleep()` creates a `TimerEntry` intrusively linked into the wheel. The driver computes the next deadline and uses it as the park timeout.
- `time/` (top level) is only the user-facing API: `sleep`, `timeout`, `interval`, `Instant`, and `pause()`/`advance()` for **deterministic tests** (`test-util` feature).
- `runtime/time_alt/` is a newer alternative implementation, gated behind `tokio_unstable` — an active area of development.

### 4.8 `sync/` — async primitives

The core building block is **`batch_semaphore.rs`**: an async semaphore with an intrusive waiter list. `Mutex`, `RwLock`, `Semaphore` and the bounded `mpsc` channel are all built on it. `Notify` is the other building block (used by `watch`, `Barrier`, and many internals). Channels:

| Channel | Shape | Typical use |
|---|---|---|
| `mpsc` | many → one, bounded/unbounded | work queues, actor mailboxes |
| `oneshot` | one → one, single value | request/response replies |
| `broadcast` | many → many, every receiver sees every value | pub/sub, shutdown fan-out |
| `watch` | one → many, only the latest value | config / state updates |

### 4.9 Cross-cutting engineering patterns you'll see everywhere

| Pattern | Where | Why it matters to you |
|---|---|---|
| **Feature-gating macros** `cfg_rt! { … }`, `cfg_net! { … }` | `macros/cfg.rs` (683 lines!) | Almost every file is wrapped in these; read `cfg.rs` once so the rest becomes readable |
| **`tokio_unstable`** `--cfg` | metrics, task dumps, io_uring, `time_alt`, `LocalRuntime` | Unstable APIs are opt-in via `RUSTFLAGS="--cfg tokio_unstable"` |
| **Loom** (`--cfg loom`) | `src/loom/`, `runtime/tests/`, `sync/tests/` | Exhaustively explores thread interleavings to prove lock-free code correct |
| **Intrusive linked lists** | `util/linked_list.rs` | Waiters/timers live *inside* the futures (no extra allocation) — the main reason for `unsafe` + `Pin` |
| **Manual vtables** | `runtime/task/raw.rs` | Type-erased tasks without `Box<dyn Future>` overhead |
| **Atomic bitfield state machines** | `runtime/task/state.rs`, `scheduled_io.rs` | Lock-free coordination between wakers and pollers |

---

## 5. A Rust learning path through this repo

Ordered so each step uses only concepts from the previous ones.

| Step | Read / do | Rust concepts you'll learn |
|---|---|---|
| 1 | The official [Tokio tutorial](https://tokio.rs/tokio/tutorial) + run `examples/` (`cargo run --example echo-tcp`, `chat`) | `async`/`.await`, `spawn`, `Arc<Mutex<_>>`, `Result`/`?` |
| 2 | `tokio/src/sync/oneshot.rs`, then `sync/watch.rs` | Ownership across tasks, `Arc`, atomics, `Drop` |
| 3 | `tokio-stream/src/` (small, self-contained adapters) | `Stream`, `Pin<&mut Self>`, `poll_next`, `pin-project-lite` |
| 4 | `tokio/src/io/util/` (e.g. `read_to_end.rs`, `copy.rs`) | Writing a `Future` by hand, `Poll`, `Context`, `ready!` |
| 5 | `tokio/src/time/sleep.rs` → `runtime/time/entry.rs` → `wheel/` | `Pin` + intrusive structures, `unsafe` with safety comments |
| 6 | `runtime/scheduler/current_thread/mod.rs` | Executors, `Waker`, `RawWakerVTable`, thread-locals |
| 7 | `runtime/task/` (`mod.rs` docs → `state.rs` → `harness.rs` → `raw.rs`) | Atomics & memory ordering, manual memory layout, vtables |
| 8 | `runtime/scheduler/multi_thread/` (`queue.rs` → `worker.rs`) | Lock-free ring buffers, work stealing |
| 9 | `src/loom/` + a loom test in `sync/tests/` | Model-checking concurrent code |

Tip: open every file with `cargo doc --open --features full` side by side — the public docs and the source are the same text.

---

## 6. Contributing workflow (from `docs/contributing/`)

```bash
cd /home/user/tokio            # local clone, branch: learn/explore-tokio

# build & test (verified: `cargo build --features full` compiles cleanly here)
cargo build --all-features
cargo test  --all-features
cargo test  -p tokio --features full --test sync_mpsc      # one test file

# lint — CI pins a specific toolchain for clippy
cargo +1.88 clippy --all --tests --all-features

# format — NOTE: `cargo fmt` does NOT work on this repo (cfg macros hide files)
rustfmt --check --edition 2021 $(git ls-files '*.rs')

# docs as docs.rs builds them
RUSTDOCFLAGS="--cfg docsrs --cfg tokio_unstable" RUSTFLAGS="--cfg docsrs --cfg tokio_unstable" \
  cargo +nightly doc --all-features --open

# loom (concurrency model checking)
LOOM_MAX_PREEMPTIONS=1 LOOM_MAX_BRANCHES=10000 RUSTFLAGS="--cfg loom -C debug_assertions" \
  cargo test --lib --release --features full -- --test-threads=1 --nocapture
```

Conventions:
- **Commit / PR titles are prefixed by area**, e.g. `sync: …`, `rt: …`, `io: …`, `net: …`. In 2026 so far, the busiest prefixes were `runtime`/`rt` (60), `io` (34), `ci` (34), `chore` (33), `sync` (29), `net` (28), `time` (22), `stream` (19).
- **MSRV is 1.85** — don't use newer std APIs in library code.
- CI (`.github/workflows/`): `ci.yml` (main matrix), `loom.yml`, `stress-test.yml`, `audit.yml`, `uring-kernel-version-test.yml`.
- Fork `tokio-rs/tokio` on GitHub, push your branch to your fork, open the PR against `master`.

### Where a newcomer can realistically start

1. **Docs** — 27.6% of the repo is doc comments; doctest examples, typos, missing "# Cancel safety" / "# Panics" sections are welcome and teach you the API.
2. **Issues labeled `E-easy` / `E-help-wanted`** on the issue tracker.
3. **`tokio-stream` and `tokio-util`** — smaller, mostly safe Rust, self-contained adapters and utilities.
4. **Tests** — add missing test cases in `tokio/tests/` for edge cases you find while reading.
5. Leave `runtime/scheduler` and `runtime/task` for later: they are `unsafe`-heavy and loom-verified.

---

## 7. Reproducing these numbers

```bash
python3 learning/loc.py . rows.json   # one JSON row per file
```
Counting rules: lines starting with `///` or `//!` = docs; `//` or `/* … */` = comments; empty = blank; everything else (including trailing comments) = code. Non-Rust files are counted as raw line totals.
