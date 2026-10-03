# Tokio — What It Does and How It Flows

> A **functional** guide: what problems Tokio solves, what features it gives you, how the pieces work together, and how data and control flow through a program.
> No function-level detail here. For that, see [`HOW_TOKIO_WORKS.md`](./HOW_TOKIO_WORKS.md) (internals) and [`functions/`](./functions/README.md) (every function).
> Snapshot: `tokio-rs/tokio` @ `8667843` (tokio 1.53).

---

## Contents

1. [What problem Tokio solves](#1-what-problem-tokio-solves)
2. [The five core ideas](#2-the-five-core-ideas)
3. [The big picture: components and how they connect](#3-the-big-picture-components-and-how-they-connect)
4. [The main flows](#4-the-main-flows)
5. [Functionality catalog — everything Tokio offers](#5-functionality-catalog--everything-tokio-offers)
   - 5.1 [Runtime](#51-runtime) · 5.2 [Tasks](#52-tasks) · 5.3 [Time](#53-time) · 5.4 [I/O](#54-io) · 5.5 [Networking](#55-networking) · 5.6 [Filesystem](#56-filesystem) · 5.7 [Processes](#57-processes) · 5.8 [Signals](#58-signals) · 5.9 [Synchronization](#59-synchronization) · 5.10 [Macros](#510-macros) · 5.11 [Observability](#511-observability--debugging) · 5.12 [Testing](#512-testing)
6. [The companion crates](#6-the-companion-crates)
7. [Feature flags: what you switch on](#7-feature-flags-what-you-switch-on)
8. [Guarantees and rules you must know](#8-guarantees-and-rules-you-must-know)
9. [Common pitfalls](#9-common-pitfalls)
10. [Choosing the right tool — cheat sheet](#10-choosing-the-right-tool--cheat-sheet)

---

## 1. What problem Tokio solves

A server handling 10,000 connections has two classic options:

| Approach | How | Problem |
|---|---|---|
| **One OS thread per connection** | Each thread blocks on `read()` | Threads are expensive (memory for stacks, context switches). 10k threads is slow; 1M is impossible. |
| **Event loop (callbacks)** | One thread asks the OS "which sockets are ready?" (epoll/kqueue/IOCP) and reacts | Very efficient, but code becomes a tangle of callbacks and manual state machines. |

**Rust's `async/await` + Tokio give you the efficiency of the event loop with code that reads like the thread-per-connection version.**

- Rust's compiler turns each `async fn` into a **state machine** (a `Future`) that can pause at every `.await` and resume later.
- But Rust ships **no engine to run them**. A `Future` does nothing until someone calls `poll()` on it.
- **Tokio is that engine** — the *runtime*. It runs millions of futures on a handful of threads, talks to the OS to find out which I/O is ready, keeps track of timers, and wakes the right future at the right time.

Plus, Tokio supplies the **async versions of everything a program needs**: sockets, files, timers, processes, signals, channels, locks.

```
Without Tokio:   async fn → Future → … nothing runs
With Tokio:      async fn → Future → Tokio runtime polls it → OS events wake it → it completes
```

---

## 2. The five core ideas

### ① Future — "a computation that may not be finished yet"
A value representing work in progress. Polling it either gives `Ready(result)` or `Pending` ("not yet, I'll tell you when to try again"). Futures are **lazy**: nothing happens until they're polled, and **dropping** a future cancels it.

### ② Waker — "call me when I can make progress"
When a future returns `Pending`, it first hands its `Waker` to whoever will cause progress (the network driver, a timer, a channel). When the event happens, that party calls `wake()`, and the runtime polls the future again. **No busy-looping; no polling things that can't make progress.**

### ③ Task — "a future the runtime owns and runs independently"
`tokio::spawn(future)` turns a future into a **task**: the runtime's unit of scheduling, like a very lightweight thread (a few hundred bytes, no stack of its own). You get back a `JoinHandle` to await its result or cancel it. Tasks run concurrently, and with the multi-thread runtime, in parallel.

### ④ Runtime — "the engine"
The runtime = **scheduler** (decides which task to poll next, on which thread) + **drivers** (the I/O event loop and the timer system) + a **blocking thread pool** (for work that can't be async). You usually create it with `#[tokio::main]`.

### ⑤ Cooperative scheduling — "tasks must yield"
Tokio cannot interrupt a task. A task only gives the thread back when it hits an `.await` that returns `Pending`. **If you run a long CPU loop or a blocking call without `.await`, you freeze that worker thread** and every task waiting on it. (Tokio helps with a per-task *budget* that forces Tokio operations to yield occasionally, but it can't fix code that never awaits.)

---

## 3. The big picture: components and how they connect

```
                         YOUR APPLICATION (async fn main, handlers, …)
     ┌───────────────┬──────────────┬──────────────┬───────────────┬───────────────┐
     │   tasks       │   time       │   net / io   │   sync        │ fs / process  │  PUBLIC
     │ spawn         │ sleep        │ TcpStream    │ Mutex         │ fs::read      │  APIs
     │ JoinHandle    │ timeout      │ UdpSocket    │ mpsc/oneshot  │ Command       │
     │ JoinSet       │ interval     │ AsyncRead/   │ broadcast     │ signal::      │
     │ spawn_blocking│              │ AsyncWrite   │ watch, Notify │ ctrl_c        │
     └──────┬────────┴──────┬───────┴──────┬───────┴───────┬───────┴───────┬───────┘
            │ creates tasks │ registers    │ registers     │ wakes tasks   │ offloads to
            ▼               │ timers       │ sockets       │ directly      ▼
   ┌─────────────────┐      │              │               │      ┌──────────────────┐
   │   SCHEDULER     │◀─────┼──────────────┼───────────────┘      │  BLOCKING POOL   │
   │ run queues,     │      │              │   wake()             │ up to 512 extra  │
   │ worker threads, │      ▼              ▼                      │ threads for      │
   │ work stealing   │  ┌──────────┐  ┌──────────────┐  wake()    │ blocking calls   │
   │                 │◀─│  TIMER   │  │  I/O DRIVER  │──────────▶ └──────────────────┘
   │ idle? → park in │  │  DRIVER  │  │  (reactor)   │
   │ the drivers ────┼─▶│  wheel   │─▶│ epoll/kqueue │◀── OS: "socket 42 is readable"
   └─────────────────┘  └──────────┘  │ /IOCP + signals/processes │
                                      └──────────────┘
```

**How the components cooperate**

| Component | Responsibility | Talks to |
|---|---|---|
| **Scheduler** | Keeps queues of ready tasks; polls them on worker threads; balances load | Tasks (polls them), drivers (sleeps inside them when idle) |
| **I/O driver ("reactor")** | Registers sockets/pipes with the OS; when the OS reports readiness, wakes the waiting tasks | OS (epoll, kqueue, IOCP via the `mio` crate), tasks (wakes) |
| **Time driver** | Holds all timers in a timing wheel; tells the scheduler how long it may sleep; fires due timers | Scheduler, I/O driver (sleeps with a timeout) |
| **Signal / process drivers** | Turn OS signals and child-process exits into wake-ups | I/O driver (Unix: signals arrive through a pipe) |
| **Blocking pool** | Separate threads for blocking work (`spawn_blocking`, `fs`, stdin/stdout) so async workers never block | Scheduler (its threads also host the workers) |
| **Sync primitives** | Coordinate tasks (locks, channels, notifications) without blocking threads | Tasks only — they wake each other directly; no driver involved |

---

## 4. The main flows

### Flow A — Program lifecycle

```
#[tokio::main] async fn main()
        │  macro expands to:
        ▼
1. BUILD    Builder::new_multi_thread().enable_all().build()
            → create I/O driver (epoll fd), time driver, blocking pool,
              N worker threads (N = CPU cores)
        ▼
2. RUN      runtime.block_on(main_body)
            → the main future runs on the main thread;
              everything it spawns runs on the workers
        ▼
3. WORK     main spawns tasks, awaits sockets/timers/channels…
            workers poll tasks; idle workers sleep in the drivers
        ▼
4. RETURN   main_body completes → block_on returns
        ▼
5. SHUTDOWN runtime is dropped:
            → stop accepting tasks, cancel (drop) all remaining tasks,
              fire remaining timers, close the I/O driver,
              wait for blocking-pool threads to finish
            → program exits
```
**Consequence:** when `main` returns, **all spawned tasks are cancelled** even if not finished. Await their `JoinHandle`s (or use `JoinSet`/`TaskTracker`) if they must complete.

### Flow B — Life of a task

```
 spawn(fut) ──▶ [SCHEDULED] ──▶ [RUNNING: poll()] ──┬─▶ Ready ──▶ [COMPLETE] ──▶ output → JoinHandle
                    ▲                               │
                    │                               └─▶ Pending ──▶ [IDLE: waiting]
                    │                                                 │
                    └──────────── wake() (I/O ready, timer fired, ────┘
                                  channel message, lock released…)

 abort() / runtime shutdown ──▶ [CANCELLED]: future dropped at its next poll point
 panic inside the task ──────▶ caught; JoinHandle returns Err(JoinError::Panic)
```
- A task is polled **only** when it's been woken — never speculatively.
- A task can move between worker threads between polls (multi-thread runtime) — hence the `Send` requirement.
- Dropping the `JoinHandle` **detaches** the task; it keeps running.

### Flow C — Scheduling (how a worker decides what to run)

```
Each worker thread loops:
  1. Run the task in my "LIFO slot" (the task just woken by the one I ran — great for request/response)
  2. Else pop from my local queue (up to 256 tasks)
  3. Every so often, check the shared global queue first (fairness for tasks spawned from outside)
  4. Else take a fair share from the global queue
  5. Else STEAL half the tasks of a random busy worker
  6. Else PARK: one idle worker sleeps inside epoll (waiting for I/O/timers), the others on a condvar
  Every 61 iterations: check I/O and timers even while busy, so events aren't starved
```

### Flow D — Network I/O (e.g. `socket.read(&mut buf).await`)

```
 task: socket.read()                               OS kernel
   │ 1. is the socket marked "readable"? ── no ──┐
   │                                             │ 2. store task's Waker in the socket's slot
   │◀──────── Pending (task goes idle) ──────────┘
   ·
   ·   (worker runs other tasks / sleeps in epoll_wait)
   ·                                                 3. data arrives → epoll reports socket ready
   │                                 I/O driver ◀───┘
   │                                 4. mark socket readable, wake() the stored Waker
   │◀─── task re-scheduled & polled ─┘
   │ 5. try the real non-blocking read() → got bytes → Ready(n)
   │    (if the OS says "would block" after all: clear readiness, wait again)
```
**Key point:** sockets are always in non-blocking mode; Tokio only tries the syscall when the OS said it's likely to succeed.

### Flow E — Timers (e.g. `sleep(5s).await`, `timeout(...)`)

```
 sleep(5s) ──first poll──▶ register in timer wheel (deadline rounded to 1 ms) ──▶ Pending
 idle worker: "next timer is due in 4.98s" → epoll_wait(timeout = 4.98s)
 time passes → epoll_wait returns → time driver fires all due timers → wake() each task
 task polled → sleep is Ready
 Dropping the Sleep before it fires → removed from the wheel (cheap, O(1))
```

### Flow F — Task-to-task communication (e.g. an mpsc channel)

```
 producer task                         consumer task
 tx.send(msg).await                    rx.recv().await
   │ 1. reserve capacity (wait if full)   │ nothing yet → store Waker → Pending
   │ 2. push msg into channel buffer       │
   │ 3. wake() consumer ─────────────────▶│ re-scheduled → recv() returns Some(msg)
   │                                       │ frees one slot → wakes a waiting producer
```
No driver, no OS involvement — tasks wake each other directly. Same for `Mutex`, `Notify`, `oneshot`, etc.

### Flow G — Blocking work (e.g. `fs::read`, `spawn_blocking`)

```
 task: fs::read("big.json").await
   │ 1. hand the closure `std::fs::read(path)` to the BLOCKING POOL
   │◀── Pending
   ·                     blocking thread: runs std::fs::read (blocks this thread only)
   ·                     done → stores result → wake() task
   │ 2. task polled → gets the bytes
```
**Why:** most operating systems don't offer truly async regular-file I/O, so Tokio uses threads. (On Linux, an experimental io_uring backend exists behind `tokio_unstable`.)

### Flow H — Cancellation

```
 Cancellation in Tokio = DROPPING a future.
   • select! picks one branch → the other branches' futures are dropped
   • timeout(d, fut) expires → fut is dropped
   • handle.abort() → the task's future is dropped at the runtime's next opportunity
   • runtime shutdown → all tasks' futures are dropped
 Dropping a future runs its destructors: waiters unregister, locks release, sockets close.
 Work done before the last .await stays done — "cancel safety" is about whether
 dropping mid-operation can lose data (each Tokio method documents this).
```

### Flow I — Graceful shutdown of an application (the usual pattern)

```
 signal::ctrl_c().await  (or a CancellationToken / watch channel)
        │ broadcast "shutting down" to all tasks
        ▼
 tasks finish their current work, stop accepting new work
        │ wait for them (JoinSet / TaskTracker::wait)
        ▼
 main returns → runtime shutdown (Flow A step 5)
```

---

## 5. Functionality catalog — everything Tokio offers

### 5.1 Runtime
*Module `tokio::runtime` · feature `rt` (+ `rt-multi-thread`)*

| Functionality | What it gives you |
|---|---|
| **Multi-thread runtime** | A pool of worker threads (default = CPU cores) with work stealing. Default for `#[tokio::main]`. Best for servers. |
| **Current-thread runtime** | Everything runs on the thread that calls `block_on`. Lower overhead, deterministic; default for `#[tokio::test]`. Good for CLIs, tests, embedding. |
| **`LocalRuntime`** | A current-thread runtime that can `spawn_local` non-`Send` futures directly. |
| **`Builder`** | Configure: worker thread count, thread names and stack size, max blocking threads, keep-alive, which drivers to enable (`enable_io`, `enable_time`, `enable_all`), start paused (tests), event/global-queue intervals, RNG seed (deterministic `select!`), lifecycle hooks. |
| **Lifecycle hooks** | `on_thread_start/stop`, `on_thread_park/unpark`; with `tokio_unstable`: `on_task_spawn`, `on_task_terminate`, `on_before/after_task_poll`. |
| **`Runtime`** | `block_on(fut)` (run a future to completion from sync code), `spawn`, `spawn_blocking`, `enter`, `shutdown_timeout`, `shutdown_background`, `metrics`. |
| **`Handle`** | A cheap, cloneable reference to a runtime. Spawn onto it from anywhere (even non-Tokio threads); `Handle::current()` inside a runtime; `try_current()`. |
| **Unhandled panic policy** *(unstable)* | Choose whether a panicking task shuts down the runtime instead of being reported through its `JoinHandle`. |
| **Task dumps** *(unstable, Linux)* | Snapshot every task's current `.await` backtrace — "where is everything stuck?". |

### 5.2 Tasks
*Module `tokio::task` · feature `rt`*

| Functionality | What it gives you |
|---|---|
| **`spawn(fut)`** | Run a `Send + 'static` future concurrently. Returns `JoinHandle<T>`. |
| **`JoinHandle`** | Await the task's result (`Result<T, JoinError>`), `abort()` it, check `is_finished()`, get an `AbortHandle`. Dropping it detaches the task. |
| **`JoinError`** | Tells you whether the task panicked (with payload) or was cancelled. |
| **`JoinSet`** | A collection of tasks: spawn many, await them **in completion order** (`join_next`), abort all, and all are aborted when the set is dropped. The standard way to manage a dynamic group. |
| **`spawn_blocking(f)`** | Run blocking/CPU-heavy synchronous code on the blocking pool; await its result. |
| **`block_in_place(f)`** | Run blocking code on the *current* worker thread, after handing its job to a new thread (multi-thread runtime only). |
| **`LocalSet` / `spawn_local`** | Run **non-`Send`** futures (e.g. using `Rc`) on one thread. |
| **`task_local!`** | Per-task variables (like thread-locals, but follow the task). |
| **`yield_now()`** | Voluntarily give other tasks a turn. |
| **Coop budgeting** | `consume_budget()`, `unconstrained(fut)` (opt out of the budget). |
| **Task identity** | `task::id()`, `try_id()`, `Id` — unique per task. |
| **`task::Builder`** *(unstable)* | Spawn with a name (shows up in tracing/console). |

### 5.3 Time
*Module `tokio::time` · feature `time`*

| Functionality | What it gives you |
|---|---|
| **`sleep(d)` / `sleep_until(t)`** | Wait for a duration/instant without blocking a thread. `Sleep` can be `reset()` cheaply. |
| **`timeout(d, fut)` / `timeout_at`** | Run a future with a deadline; returns `Err(Elapsed)` and drops the future if it's too slow. |
| **`interval(period)` / `interval_at`** | Periodic ticks. `MissedTickBehavior` decides what happens if you fall behind: `Burst` (default, catch up quickly), `Delay`, or `Skip`. |
| **`Instant`** | Tokio's clock (respects pausing in tests). |
| **`pause()` / `advance(d)` / `resume()`** | Freeze and manually move time in tests (feature `test-util`). With time paused, an idle runtime auto-jumps to the next timer, so a 1-hour timeout test finishes instantly. |
| Resolution | 1 millisecond; timers are rounded **up**. |

### 5.4 I/O
*Module `tokio::io` · features `io-util`, `io-std`*

| Functionality | What it gives you |
|---|---|
| **Core traits** | `AsyncRead`, `AsyncWrite`, `AsyncBufRead`, `AsyncSeek` — the async equivalents of `std::io::{Read, Write, BufRead, Seek}`. Implemented by sockets, files, pipes, stdio, in-memory streams. |
| **Extension traits** | `AsyncReadExt` (`read`, `read_exact`, `read_to_end`, `read_to_string`, `read_u32`…), `AsyncWriteExt` (`write_all`, `flush`, `shutdown`, `write_u32`…), `AsyncBufReadExt` (`read_line`, `lines`, `read_until`), `AsyncSeekExt`. |
| **Buffering** | `BufReader`, `BufWriter`, `BufStream`. |
| **Copying** | `copy`, `copy_buf`, `copy_bidirectional` (proxy two streams both ways). |
| **Splitting** | `split()` (generic read/write halves); `TcpStream::split`/`into_split` (zero-cost). |
| **In-memory pipes** | `duplex(size)` (bidirectional, great for tests), `simplex` (one-way). |
| **Adapters** | `empty`, `repeat`, `sink`, `chain`, `take`, `join(reader, writer)`. |
| **Stdio** | `stdin()`, `stdout()`, `stderr()` (via the blocking pool). |
| **`AsyncFd`** *(Unix)* | Make **any** file descriptor async (e.g. a device or a library's socket) by registering it with Tokio's reactor. |
| **`Interest` / `Ready`** | Ask for / inspect readiness (readable, writable, error, priority). `ready()`, `readable()`, `writable()`, `try_read`/`try_write` APIs on sockets. |

### 5.5 Networking
*Module `tokio::net` · feature `net`*

| Functionality | What it gives you |
|---|---|
| **TCP** | `TcpListener` (`bind`, `accept`), `TcpStream` (`connect`, read/write, `split`, `peek`, `set_nodelay`, `try_read`, `readable`…), `TcpSocket` (configure before connect/listen: reuse address, buffer sizes, keepalive, bind device). |
| **UDP** | `UdpSocket`: `send_to`/`recv_from`, `connect` + `send`/`recv`, multicast, broadcast, `peek`. |
| **Unix domain sockets** | `UnixListener`, `UnixStream`, `UnixDatagram`, `UnixSocket`, peer credentials. |
| **Windows named pipes** | `NamedPipeServer`, `NamedPipeClient` (`net::windows::named_pipe`). |
| **DNS** | `lookup_host("example.com:80")` (std resolver on the blocking pool). |
| **Conversions** | `from_std` / `into_std` to move sockets between Tokio and the standard library. |

Not included: TLS (use `tokio-rustls`/`tokio-native-tls`), HTTP (use `hyper`, `axum`, `reqwest`), WebSockets (`tokio-tungstenite`).

### 5.6 Filesystem
*Module `tokio::fs` · feature `fs`*

| Functionality | What it gives you |
|---|---|
| **One-shot helpers** | `read`, `read_to_string`, `write`, `copy`, `rename`, `remove_file`, `create_dir(_all)`, `remove_dir(_all)`, `metadata`, `symlink_metadata`, `canonicalize`, `hard_link`, `symlink`, `read_link`, `set_permissions`, `try_exists`. |
| **`File`** | Async file handle implementing `AsyncRead/Write/Seek`; `OpenOptions`; `sync_all`, `set_len`, `metadata`. |
| **Directories** | `read_dir` → `ReadDir` stream of `DirEntry`; `DirBuilder`. |
| **How it works** | Each call runs the std blocking operation on the blocking pool (Flow G). Batch work in one `spawn_blocking` if you do many small ops. Optional io_uring backend (Linux, unstable). |

### 5.7 Processes
*Module `tokio::process` · feature `process`*

| Functionality | What it gives you |
|---|---|
| **`Command`** | Same builder as `std::process::Command` (args, env, cwd, stdio, uid/gid, process group) plus `kill_on_drop`. `spawn`, `output().await`, `status().await`. |
| **`Child`** | `wait().await`, `try_wait`, `kill().await`, `start_kill`, `wait_with_output`, `id`. |
| **Async pipes** | `ChildStdin`/`ChildStdout`/`ChildStderr` implement `AsyncWrite`/`AsyncRead` — stream a child's output line by line. |
| **How exits are detected** | Unix: `SIGCHLD` via the signal driver (or pidfd on Linux); Windows: wait handles. |

### 5.8 Signals
*Module `tokio::signal` · feature `signal`*

| Functionality | What it gives you |
|---|---|
| **`ctrl_c()`** | Cross-platform future that completes on Ctrl-C. |
| **Unix** | `signal(SignalKind::terminate())` etc. → a stream of signal arrivals (SIGTERM, SIGHUP, SIGUSR1, …). |
| **Windows** | `ctrl_break`, `ctrl_close`, `ctrl_logoff`, `ctrl_shutdown`. |

### 5.9 Synchronization
*Module `tokio::sync` · feature `sync` (works with any executor, not just Tokio's)*

**Channels — passing data between tasks**

| Type | Shape | Behaviour | Typical use |
|---|---|---|---|
| **`mpsc`** | many senders → one receiver | Bounded (backpressure: `send` waits when full) or unbounded | Work queues, actor mailboxes |
| **`oneshot`** | one value, once | Sender sends, receiver awaits | Replies ("respond to this request") |
| **`broadcast`** | many → many | Every receiver gets every message; slow receivers get `Lagged` instead of blocking senders | Pub/sub, event fan-out |
| **`watch`** | one → many | Only the **latest** value is kept; receivers see changes | Config reloads, state, shutdown flags |

All channels: `try_send`/`try_recv` (non-async), `blocking_send`/`blocking_recv` (from sync threads), detect closure when all senders/receivers are dropped.

**Locks and coordination — sharing state between tasks**

| Type | What it does | Note |
|---|---|---|
| **`Mutex<T>`** | Async mutual exclusion; the guard can be held across `.await` | FIFO-fair. Prefer `std::sync::Mutex` if you never hold it across `.await` (it's faster). |
| **`RwLock<T>`** | Many readers or one writer | Fair: a waiting writer blocks new readers |
| **`Semaphore`** | Limit concurrency to N permits | e.g. at most 100 concurrent DB queries; `acquire_many` |
| **`Notify`** | Wake one or all waiting tasks, no data | Building block for custom primitives |
| **`Barrier`** | Wait until N tasks arrive | Phased work |
| **`OnceCell<T>`** | Async lazy initialization, exactly once | Global clients, config |
| **`SetOnce<T>`** | A value set once, awaitable by others | One-time results |
| Owned variants | `lock_owned`, `acquire_owned`, … return `'static` guards (hold an `Arc`) | Move a guard into a spawned task |
| Mapped guards | `MutexGuard::map` | Lock a whole struct, expose one field |

### 5.10 Macros
*Feature `macros`*

| Macro | What it does |
|---|---|
| **`#[tokio::main]`** | Turns `async fn main` into a sync `main` that builds a runtime and `block_on`s your body. Options: `flavor = "current_thread"`, `worker_threads = N`, `start_paused`. |
| **`#[tokio::test]`** | Same for tests (default current-thread). |
| **`select!`** | Wait on several futures; run the branch of the **first** to complete, **drop the rest**. Random branch order for fairness (`biased;` for fixed order), pattern guards, `else` branch. |
| **`join!` / `try_join!`** | Run several futures **concurrently on the same task** and wait for all (or the first error). |
| **`pin!`** | Pin a future on the stack (needed to poll it by reference, e.g. in a `select!` loop). |
| **`task_local!`** | Declare task-local variables. |

`join!` vs `spawn`: `join!` gives **concurrency** within one task (one thread at a time); `spawn` gives **parallelism** (tasks may run simultaneously on different workers).

### 5.11 Observability & debugging

| Functionality | What it gives you |
|---|---|
| **`RuntimeMetrics`** | Worker count, alive tasks, global queue depth; with `tokio_unstable`: per-worker poll counts, steal counts, park counts, busy time, local queue depth, poll-time histograms, I/O driver stats, blocking pool stats. |
| **`tracing` integration** *(unstable + `tracing` feature)* | Emits spans/events for tasks and resources — powers **tokio-console** (a `top`-like live view of tasks). |
| **Task dumps** *(unstable)* | Async backtraces of all tasks. |
| **Hooks** | Thread start/stop/park/unpark; task spawn/terminate/poll (unstable). |

### 5.12 Testing

| Functionality | Where |
|---|---|
| `#[tokio::test]`, `start_paused = true` | `tokio-macros` |
| `time::pause/advance` — deterministic time | `tokio::time` (feature `test-util`) |
| `io::duplex` — in-memory socket pair | `tokio::io` |
| `tokio_test::io::Builder` — scripted mock reader/writer ("expect read X, then write Y") | `tokio-test` |
| `tokio_test::task::spawn` + `assert_pending!`/`assert_ready!` — poll a future manually, step by step | `tokio-test` |
| Seeded RNG (`Builder::rng_seed`) — deterministic `select!` order | `tokio::runtime` |

---

## 6. The companion crates

### `tokio-util` — higher-level building blocks
| Area | Functionality |
|---|---|
| **Codecs (`codec`)** | Turn a byte stream into a stream of **frames/messages**: `Framed`, `FramedRead`, `FramedWrite` + `Decoder`/`Encoder` traits. Built-ins: `LinesCodec`, `LengthDelimitedCodec`, `BytesCodec`, `AnyDelimiterCodec`. This is how protocols are usually implemented. |
| **Cancellation (`sync`)** | `CancellationToken` — a tree of tokens; cancelling a parent cancels all children. `DropGuard` cancels on drop. The standard graceful-shutdown tool. Also `PollSemaphore`, `PollSender`, `ReusableBoxFuture`. |
| **Task management (`task`)** | `TaskTracker` (wait until all tracked tasks finish — graceful shutdown), `JoinMap` (JoinSet keyed by your own key), `AbortOnDropHandle`, `JoinQueue`, `LocalPoolHandle` (pool of `LocalSet`s for `!Send` work). |
| **Time (`time`)** | `DelayQueue` — a queue whose items pop out when their deadlines expire (caches with TTL, retries). |
| **I/O (`io`)** | `ReaderStream` / `StreamReader` (bytes ↔ `Stream`), `SyncIoBridge` (use async I/O from sync code), `InspectReader`/`InspectWriter`, `SinkWriter`, `CopyToBytes`. |
| **Compat (`compat`)** | Adapt between Tokio's I/O traits and the `futures` crate's I/O traits. |
| **UDP (`udp`)** | `UdpFramed` — codecs over UDP. |
| **Misc** | `Either` (two future/IO types as one), `FutureExt::timeout`. |

### `tokio-stream` — async iterators
- `Stream` = async `Iterator` (`next().await`). `StreamExt` gives `map`, `filter`, `take`, `chain`, `merge`, `timeout`, `throttle`, `chunks_timeout`, `fold`, `collect`, …
- `StreamMap` — poll many keyed streams fairly, as one stream.
- **Wrappers** turning Tokio types into streams: `ReceiverStream` (mpsc), `UnboundedReceiverStream`, `BroadcastStream`, `WatchStream`, `IntervalStream`, `TcpListenerStream`, `UnixListenerStream`, `LinesStream`, `SplitStream`, `ReadDirStream`, `SignalStream`, `JoinSetStream`.
- Constructors: `iter`, `once`, `empty`, `pending`.

### `tokio-macros`
The procedural macros behind `#[tokio::main]` and `#[tokio::test]` (re-exported by `tokio`).

### `tokio-test`
Testing helpers listed in §5.12.

---

## 7. Feature flags: what you switch on

Tokio compiles **nothing** by default — you opt into what you need (keeps builds small and fast).

| Feature | Enables |
|---|---|
| `rt` | Current-thread runtime, `spawn`, `JoinHandle`, `JoinSet`, `LocalSet`, blocking pool |
| `rt-multi-thread` | The multi-thread, work-stealing runtime |
| `macros` | `#[tokio::main]`, `#[tokio::test]`, `select!`, `join!` |
| `net` | TCP/UDP/Unix sockets, named pipes, `AsyncFd`, I/O driver |
| `io-util` | `AsyncReadExt`/`AsyncWriteExt`, buffers, `copy`, `duplex` |
| `io-std` | `stdin`/`stdout`/`stderr` |
| `time` | `sleep`, `timeout`, `interval`, time driver |
| `fs` | `tokio::fs` |
| `process` | `tokio::process` |
| `signal` | `tokio::signal` |
| `sync` | Channels, `Mutex`, `RwLock`, `Semaphore`, `Notify`, `OnceCell`, … |
| `parking_lot` | Use `parking_lot` locks internally |
| `test-util` | `time::pause/advance`, test helpers |
| `tracing` | Instrumentation (with `tokio_unstable`) |
| `full` | All of the above except `test-util` and `tracing` |

**Unstable features** require `RUSTFLAGS="--cfg tokio_unstable"`: extra metrics, task hooks, task dumps (`taskdump`), io_uring (`io-uring`), unhandled-panic policy, named task builder, alternative timer.

**Platform support:** Linux, macOS, Windows, FreeBSD and other BSDs, Android, iOS, illumos; partial WASM/WASI. MSRV: Rust 1.85. LTS releases receive fixes for a long period (see `README.md`).

---

## 8. Guarantees and rules you must know

| Topic | The rule |
|---|---|
| **`Send + 'static` for `spawn`** | Spawned tasks may move between threads and outlive the caller. Use `Arc` to share data, move ownership in, or use `LocalSet`/`spawn_local` for `!Send` data. |
| **Never block a worker** | No `std::thread::sleep`, no blocking I/O, no long CPU loops without `.await`. Use `tokio::time::sleep`, async I/O, `spawn_blocking`, or `block_in_place`. |
| **Cancellation = drop** | Any `.await` point can be the last one if the future is dropped (`select!`, `timeout`, `abort`). Write code so that's safe; check "Cancel safety" in each method's docs. |
| **Panics are isolated** | A panic in a task is caught; the `JoinHandle` gets `Err(JoinError::Panic)`. The runtime keeps going (unless configured otherwise). |
| **Fairness** | FIFO-fair locks and semaphores; random branch order in `select!`; coop budget stops a busy task from monopolizing a thread; global queue is checked regularly. |
| **Runtime shutdown** | When the runtime is dropped, remaining tasks are cancelled; dropping the runtime waits for blocking-pool threads (use `shutdown_timeout`/`shutdown_background` to bound that). |
| **One runtime per thread** | Calling `block_on` inside a runtime panics ("Cannot start a runtime from within a runtime"). Use `.await`, `Handle::spawn`, or `block_in_place`. |
| **Runtime-bound resources** | Sockets and timers belong to the runtime that created them; using them after that runtime shuts down returns errors or panics. |
| **Executor-agnostic parts** | `tokio::sync` works with any executor; `net`/`time`/`fs`/`process`/`signal` need a Tokio runtime. |

---

## 9. Common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything freezes / latency spikes | Blocking call inside async code | `spawn_blocking`, async equivalents |
| Panic: *"there is no reactor running"* | Using Tokio I/O/time outside a runtime (or a different async runtime) | Run inside `#[tokio::main]` / `Runtime::block_on` / `Handle::enter` |
| Panic: *"Cannot start a runtime from within a runtime"* | `block_on` inside async code | `.await` the future instead |
| Spawned work silently never finishes | `main` returned and the runtime shut down | Await handles; `JoinSet`, `TaskTracker` |
| Deadlock with `std::sync::Mutex` | Guard held across `.await` | `tokio::sync::Mutex`, or drop the guard before awaiting |
| Data lost in a `select!` loop | Branch future isn't cancel-safe | Use cancel-safe methods, or keep the future alive outside the loop (`pin!` + `&mut fut`) |
| Unbounded memory growth | `unbounded_channel` with a slow consumer | Bounded `mpsc` (backpressure) |
| `broadcast` receiver gets `Lagged(n)` | Consumer slower than producer | Bigger capacity, or `watch` if only the latest value matters |
| Program won't exit on drop | A `spawn_blocking` task (or stdin read) never returns | `shutdown_timeout` / `shutdown_background` |
| Single-threaded performance only | Using the current-thread runtime, or all work in one task with `join!` | Multi-thread runtime + `spawn` |

---

## 10. Choosing the right tool — cheat sheet

| I want to… | Use |
|---|---|
| Run async code from `main` | `#[tokio::main]` |
| Do things concurrently and wait for all | `join!` (few, fixed) / `JoinSet` (many, dynamic) |
| Run something in the background | `tokio::spawn` |
| Take whichever finishes first | `select!` |
| Give up after a deadline | `time::timeout` |
| Do something every N seconds | `time::interval` |
| Run blocking or CPU-heavy code | `task::spawn_blocking` (or `rayon` for parallel CPU work) |
| Send work to a worker task | `mpsc` (bounded) |
| Get a single reply | `oneshot` |
| Notify all subscribers of every event | `broadcast` |
| Share "current state" with many readers | `watch` |
| Share mutable state across `.await` | `Arc<tokio::sync::Mutex<T>>` (or an actor with `mpsc` + `oneshot`) |
| Limit concurrency | `Semaphore` |
| Lazily initialize a shared value | `OnceCell` |
| Implement a line/length-framed protocol | `tokio_util::codec::Framed` + `LinesCodec`/`LengthDelimitedCodec` |
| Shut down gracefully | `signal::ctrl_c` + `CancellationToken` + `TaskTracker` |
| Treat a channel/listener as a stream | `tokio_stream::wrappers::*` + `StreamExt` |
| Test with timers without waiting | `#[tokio::test(start_paused = true)]` |
| See what tasks are doing in production | `tokio-console` (needs `tokio_unstable` + `tracing`), `RuntimeMetrics` |

---

### Where to go next
- Hands-on: the official tutorial at <https://tokio.rs/tokio/tutorial> (builds a mini-Redis), and `examples/` in this repo (`cargo run --example echo-tcp`, `chat`, `tinyhttp`).
- Internals: [`HOW_TOKIO_WORKS.md`](./HOW_TOKIO_WORKS.md) → [`DSA_IN_TOKIO.md`](./DSA_IN_TOKIO.md) → source.
