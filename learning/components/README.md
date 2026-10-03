# Tokio Components — one document per block

Each block of the component diagram (from the [functional guide](../TOKIO_FUNCTIONAL_GUIDE.md#3-the-big-picture-components-and-how-they-connect)) has its own document covering:
**responsibility & boundary · files & LOC · data structures (real code) · how it interacts with the other blocks · basic functions · flows · invariants & gotchas · tests**.

```
                         YOUR APPLICATION (async fn main, handlers, …)
     ┌───────────────┬──────────────┬──────────────┬───────────────┬───────────────┐
     │ ① tasks       │ ② time       │ ③ net / io   │ ④ sync        │ ⑤ fs/process/ │  PUBLIC
     │ spawn         │ sleep        │ TcpStream    │ Mutex         │   signal      │  APIs
     │ JoinHandle    │ timeout      │ UdpSocket    │ mpsc/oneshot  │ fs::read      │
     │ JoinSet       │ interval     │ AsyncRead/   │ broadcast     │ Command       │
     │ spawn_blocking│              │ AsyncWrite   │ watch, Notify │ ctrl_c        │
     └──────┬────────┴──────┬───────┴──────┬───────┴───────┬───────┴───────┬───────┘
            │ creates tasks │ registers    │ registers     │ wakes tasks   │ offloads to
            ▼               │ timers       │ sockets       │ directly      ▼
   ┌─────────────────┐      │              │               │      ┌──────────────────┐
   │ ⑥ SCHEDULER     │◀─────┼──────────────┼───────────────┘      │ ⑨ BLOCKING POOL  │
   │ run queues,     │      ▼              ▼                      │ up to 512 extra  │
   │ workers, steal  │  ┌──────────┐  ┌──────────────┐  wake()    │ threads          │
   │ idle? → park ───┼─▶│ ⑦ TIMER  │─▶│ ⑧ I/O DRIVER │──────────▶ └──────────────────┘
   │                 │◀─│  DRIVER  │  │ epoll/kqueue │◀── OS events
   └─────────────────┘  └──────────┘  │ /IOCP+signals│
                                      └──────────────┘
```

## The blocks at a glance

| Block | Layer | Files | Code LOC | % of `tokio/src` | Doc lines | Functions | Integration test fns | `unsafe` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ① [Tasks](./01-tasks.md) | API + task core | 26 | 4,386 | 8.7% | 4,009 | 401 | 130 | 170 |
| ② [Time](./02-time.md) | API | 7 | 769 | 1.5% | 1,249 | 78 | 76 | 2 |
| ③ [Net & I/O](./03-net-io.md) | API | 86 | 10,904 | 21.5% | 16,548 | 1,149 | 315 | 203 |
| ④ [Sync](./04-sync.md) | API | 41 | 9,135 | 18.1% | 10,488 | 755 | 361 | 230 |
| ⑤ [fs / process / signal](./05-fs-process-signal.md) | API | 45 | 5,408 | 10.7% | 4,010 | 492 | 136 | 54 |
| ⑥ [Scheduler](./06-scheduler.md) | engine | 76 | 10,301 | 20.4% | 5,979 | 832 | 230 | 104 |
| ⑦ [Timer driver](./07-timer-driver.md) | engine | 20 | 2,601 | 5.1% | 883 | 239 | — | 124 |
| ⑧ [I/O driver (+ signal/process drivers)](./08-io-driver.md) | engine | 10 | 1,241 | 2.5% | 451 | 95 | — | 40 |
| ⑨ [Blocking pool](./09-blocking-pool.md) | engine | 7 | 991 | 2.0% | 256 | 66 | — | 2 |
| *Not in the diagram:* `macros/` 1,742 · `util/` 1,927 · `loom/` 736 · `future/` 212 · `lib.rs`/`doc/` 246 | shared | | 4,863 | 9.6% | | | | |
| **`tokio/src` total** | | | **50,599** | 100% | | | | |

The API blocks are **60.5%** of the code, the engine blocks **30.0%**, shared helpers **9.6%**. The engine blocks have no dedicated integration tests: they are exercised through the API blocks' tests, inline unit tests and loom models.

## Who talks to whom

| From ↓ / To → | Tasks | Time | Net&IO | Sync | fs/proc/sig | Scheduler | Timer drv | I/O drv | Blocking |
|---|---|---|---|---|---|---|---|---|---|
| **Tasks** | | | | | | `Schedule` trait, `OwnedTasks` | | | `spawn_blocking` |
| **Time** | coop budget | | | | | find runtime | `TimerEntry` init/reset/cancel | | |
| **Net & I/O** | coop budget | | | | | find runtime | | `Registration` | stdio, DNS |
| **Sync** | `Waker::wake`, coop | | | | | | | | |
| **fs/proc/sig** | | | `AsyncRead/Write` | `watch`, `Mutex` | | | | pidfd, self-pipe, pipes | `asyncify` |
| **Scheduler** | `task.run()` | | | `Notify` | | | park | park / unpark | worker threads |
| **Timer drv** | `Waker::wake` | | | `AtomicWaker` | | | | `park_timeout`, unpark | |
| **I/O drv** | `Waker::wake` | | | `watch` (signals) | orphan reaping | | | | |
| **Blocking** | runs `UnownedTask` | | | | | | inhibit auto-advance | | |

## Reading order

1. **⑥ Scheduler** and **① Tasks**: the engine and what it runs.
2. **⑧ I/O driver** and **⑦ Timer driver**: where idle threads sleep and what wakes them.
3. **③ Net & I/O** and **② Time**: the APIs built on those drivers.
4. **④ Sync**: needs no driver; tasks wake each other directly.
5. **⑨ Blocking pool** and **⑤ fs/process/signal**: everything that can't be async.

## Regenerating the numbers

The *At a glance*, *Files* and *Tests* sections of each document are generated from the source:

```bash
python3 learning/fn_index.py . learning/functions      # function index (feeds the function counts)
python3 learning/components/block_stats.py              # recompute stats + refill the docs
```
Which source files belong to which block is defined in `BLOCKS` at the top of [`block_stats.py`](./block_stats.py).
