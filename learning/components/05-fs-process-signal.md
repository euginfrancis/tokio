# Block 5 — fs / process / signal (OS services)

> **Role:** async access to operating-system services that aren't sockets: the **filesystem**, **child processes**, and **OS signals** (Ctrl-C, SIGTERM, …).
> In the [component diagram](./README.md): the "fs / process — fs::read, Command, signal::ctrl_c" API box, with the arrow "offloads to" the [Blocking pool](./09-blocking-pool.md). Files go to the blocking pool; processes and signals are driven by the [I/O driver](./08-io-driver.md)'s signal and process layers.

---

## 1. At a glance

<!-- STATS:fs_process_signal -->
| Metric | Value |
|---|---|
| Source files | 45 |
| Code lines | 5,408 (10.7% of `tokio/src`) |
| Doc + comment lines | 4,010 (0.74 per code line) |
| Functions | 492 — public API 153, trait impls 128, internal 110, inline tests 85 |
| `async fn` / `unsafe fn` | 66 / 9 |
| `unsafe` occurrences | 54 |
| Integration tests (`tokio/tests`) | 47 files, 136 test fns, 2,959 code lines |
<!-- /STATS -->

Three sub-modules with three different strategies:

| Sub-module | Strategy | Why |
|---|---|---|
| `fs` | Run `std::fs` on the **blocking pool** (optional io_uring on Linux, unstable) | Most OSes have no readiness-based async file I/O |
| `process` | Spawn with `std::process`, then wait for exit via **pidfd** (Linux) / **SIGCHLD** (other Unix) / **wait handle** (Windows); stdio pipes are normal async I/O | Exit isn't an fd event on most systems |
| `signal` | OS handler writes to a **self-pipe**; the I/O driver wakes on it; delivered via `watch` channels | Signal handlers may do almost nothing safely |

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | `fs::*` functions, `File` (+ its buffer/state machine), `OpenOptions`, `ReadDir`/`DirEntry`, `DirBuilder`; `Command`, `Child`, `ChildStdin/Stdout/Stderr`, orphan reaping queue, pidfd/signal reapers, `kill_on_drop`; `ctrl_c`, Unix `signal(SignalKind)`, Windows `ctrl_*`, the global signal registry. |
| **Does not own** | Running blocking calls ([Blocking pool](./09-blocking-pool.md)); polling the self-pipe/pidfds and reaping after each park ([I/O driver](./08-io-driver.md) — signal & process drivers); generic I/O traits ([Net & I/O](./03-net-io.md)); `watch` channels ([Sync](./04-sync.md)). |
| **Input** | User calls; OS events (signal delivery, child exit). |
| **Output** | Blocking closures; I/O registrations (pipes, pidfds, self-pipe); `watch` sends. |

---

## 3. Files

<!-- FILES:fs_process_signal -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/fs/file/tests.rs`](../../tokio/src/fs/file/tests.rs) | 765 | 5 | 14.1% |
| [`tokio/src/fs/file.rs`](../../tokio/src/fs/file.rs) | 634 | 437 | 11.7% |
| [`tokio/src/process/mod.rs`](../../tokio/src/process/mod.rs) | 627 | 1,091 | 11.6% |
| [`tokio/src/process/unix/mod.rs`](../../tokio/src/process/unix/mod.rs) | 283 | 30 | 5.2% |
| [`tokio/src/fs/open_options.rs`](../../tokio/src/fs/open_options.rs) | 279 | 550 | 5.2% |
| [`tokio/src/process/unix/orphan.rs`](../../tokio/src/process/unix/orphan.rs) | 258 | 22 | 4.8% |
| [`tokio/src/process/unix/pidfd_reaper.rs`](../../tokio/src/process/unix/pidfd_reaper.rs) | 258 | 4 | 4.8% |
| [`tokio/src/signal/unix.rs`](../../tokio/src/signal/unix.rs) | 235 | 256 | 4.3% |
| [`tokio/src/process/unix/reap.rs`](../../tokio/src/process/unix/reap.rs) | 228 | 28 | 4.2% |
| [`tokio/src/process/windows.rs`](../../tokio/src/process/windows.rs) | 225 | 21 | 4.2% |
| [`tokio/src/signal/registry.rs`](../../tokio/src/signal/registry.rs) | 185 | 29 | 3.4% |
| [`tokio/src/signal/windows/sys.rs`](../../tokio/src/signal/windows/sys.rs) | 169 | 42 | 3.1% |
| [`tokio/src/signal/reusable_box.rs`](../../tokio/src/signal/reusable_box.rs) | 149 | 42 | 2.8% |
| [`tokio/src/fs/mocks.rs`](../../tokio/src/fs/mocks.rs) | 146 | 18 | 2.7% |
| [`tokio/src/fs/read_dir.rs`](../../tokio/src/fs/read_dir.rs) | 146 | 184 | 2.7% |
| [`tokio/src/fs/open_options/uring_open_options.rs`](../../tokio/src/fs/open_options/uring_open_options.rs) | 108 | 2 | 2.0% |
| [`tokio/src/signal/windows.rs`](../../tokio/src/signal/windows.rs) | 106 | 408 | 2.0% |
| [`tokio/src/fs/read_uring.rs`](../../tokio/src/fs/read_uring.rs) | 91 | 31 | 1.7% |
| [`tokio/src/fs/mod.rs`](../../tokio/src/fs/mod.rs) | 76 | 221 | 1.4% |
| [`tokio/src/fs/write.rs`](../../tokio/src/fs/write.rs) | 68 | 21 | 1.3% |
| [`tokio/src/fs/try_exists.rs`](../../tokio/src/fs/try_exists.rs) | 44 | 40 | 0.8% |
| [`tokio/src/fs/dir_builder.rs`](../../tokio/src/fs/dir_builder.rs) | 39 | 80 | 0.7% |
| [`tokio/src/fs/open_options/mock_open_options.rs`](../../tokio/src/fs/open_options/mock_open_options.rs) | 36 | 1 | 0.7% |
| [`tokio/src/signal/mod.rs`](../../tokio/src/signal/mod.rs) | 36 | 44 | 0.7% |
| [`tokio/src/fs/rename.rs`](../../tokio/src/fs/rename.rs) | 34 | 6 | 0.6% |
| [`tokio/src/fs/read.rs`](../../tokio/src/fs/read.rs) | 30 | 60 | 0.6% |
| [`tokio/src/signal/windows/stub.rs`](../../tokio/src/signal/windows/stub.rs) | 17 | 2 | 0.3% |
| [`tokio/src/process/kill.rs`](../../tokio/src/process/kill.rs) | 9 | 2 | 0.2% |
| [`tokio/src/signal/ctrl_c.rs`](../../tokio/src/signal/ctrl_c.rs) | 9 | 51 | 0.2% |
| [`tokio/src/fs/hard_link.rs`](../../tokio/src/fs/hard_link.rs) | 8 | 33 | 0.1% |
| *…15 smaller files* | 110 | 249 | 2.0% |
| **Total (45 files)** | **5,408** | **4,010** | 100% |
<!-- /FILES -->

```
fs/
├── mod.rs (asyncify)       every one-shot fn = asyncify(move || std::fs::xxx(path))
├── read.rs, write.rs, copy.rs, rename.rs, remove_*.rs, create_dir*.rs, metadata.rs, … (≈1 file per fn)
├── file.rs                 File: Idle/Busy state machine over a blocking task (largest fs file)
├── open_options.rs (+ uring_open_options.rs), read_dir.rs, dir_builder.rs
└── mocks.rs                test doubles for spawn_blocking
process/
├── mod.rs                  Command, Child, ChildStd*, kill_on_drop, FusedChild
├── unix/mod.rs             spawn_child: try pidfd, else SIGCHLD reaper; Pipe/ChildStdio (PollEvented)
├── unix/pidfd_reaper.rs    Linux: exit = pidfd becomes readable
├── unix/reap.rs            other Unix: re-check try_wait on every SIGCHLD
├── unix/orphan.rs          global queue of dropped-but-running children
├── windows.rs              RegisterWaitForSingleObject → oneshot
└── kill.rs
signal/
├── ctrl_c.rs, unix.rs (signal(), SignalKind, handler `action`), windows.rs + windows/
├── registry.rs             Globals { registry: per-signal EventInfo { pending, watch::Sender<()> } }
└── reusable_box.rs         ReusableBoxFuture used by RxFuture
```

---

## 4. Data structures

### fs
```rust
pub struct File {                          // fs/file.rs
    std: Arc<StdFile>,                     // shared with the blocking task
    inner: Mutex<Inner>,                   // tokio::sync::Mutex
    max_buf_size: usize,                   // default 2 MiB per blocking op
}
struct Inner { state: State, last_write_err: Option<io::ErrorKind>, pos: u64 }
enum State {
    Idle(Option<Buf>),                     // buffer available (may hold read-ahead data)
    Busy(JoinHandle<(Operation, Buf)>),    // a blocking read/write/seek is running
}
enum Operation { Read(io::Result<usize>), Write(io::Result<()>), Seek(io::Result<u64>) }
pub(crate) struct Buf { buf: Vec<u8>, pos: usize }   // io/blocking.rs (shared with stdio)
```

### process
```rust
pub struct Command { std: std::process::Command, kill_on_drop: bool }
pub struct Child { child: FusedChild, stdin, stdout, stderr: Option<ChildStd*> }
enum FusedChild { Child(ChildDropGuard<imp::Child>), Done(ExitStatus) }
pub(crate) enum imp::Child {                         // process/unix/mod.rs
    SignalReaper(Reaper<StdChild, GlobalOrphanQueue, Signal>),   // SIGCHLD-driven
    PidfdReaper(PidfdReaper<StdChild, GlobalOrphanQueue>),       // Linux pidfd (PollEvented<Pidfd>)
}
pub struct ChildStdout { inner: ChildStdio }        // ChildStdio = PollEvented<Pipe> on Unix
pub(crate) struct OrphanQueueImpl<T> { sigchild: Mutex<Option<watch::Receiver<()>>>, queue: Mutex<Vec<T>> }
```

### signal
```rust
pub struct Signal { inner: RxFuture }                    // signal/unix.rs
struct RxFuture { inner: ReusableBoxFuture<watch::Receiver<()>> }
pub(crate) struct Globals { extra: OsExtraData { sender: UnixStream, receiver: UnixStream }, registry: Registry<OsStorage> }
pub(crate) struct EventInfo { pending: AtomicBool, tx: watch::Sender<()> }   // one per signal number
```

---

## 5. How it interacts with the other blocks

```
 fs::read(p) ─▶ asyncify ─▶ [Blocking pool] std::fs::read(p) ─▶ JoinHandle ─▶ result
 file.read(&mut buf) ─▶ Idle(buf): copy cached bytes, or start Busy(spawn_blocking(read into buf)) ─▶ Pending
                      ─▶ Busy finished ─▶ copy out ─▶ Idle(buf)
 file.write(data)    ─▶ copy into buf ─▶ Busy(spawn_mandatory_blocking(write)) ─▶ returns Ready(len) immediately
 file.flush()/drop   ─▶ waits for / lets the in-flight write finish (mandatory: runs even during shutdown)

 Command::spawn ─▶ std spawn ─▶ Linux: pidfd_open ─▶ PollEvented ─▶ [I/O driver]   |  else: signal(SIGCHLD) stream
 child.wait()   ─▶ pidfd readable / SIGCHLD seen ─▶ try_wait() ─▶ ExitStatus
 drop(child) running ─▶ kill if kill_on_drop ─▶ push to GlobalOrphanQueue ─▶ [I/O driver] process::Driver reaps after each park
 child stdout   ─▶ PollEvented<Pipe> ─▶ normal AsyncRead ([Net & I/O] + [I/O driver])

 signal(SIGTERM) ─▶ first time: install handler (signal-hook-registry) ─▶ watch::Receiver for that signal
 OS delivers SIGTERM ─▶ handler `action`: pending = true; write 1 byte to self-pipe
 [I/O driver] TOKEN_SIGNAL ─▶ signal::Driver::process: drain pipe ─▶ globals().broadcast() ─▶ watch send ─▶ Signal::recv wakes
```

| Other block | Direction | Through |
|---|---|---|
| Blocking pool | → | `asyncify` / `spawn_blocking` / `spawn_mandatory_blocking` |
| I/O driver | → | `PollEvented` for pipes and pidfds; self-pipe under `TOKEN_SIGNAL`; orphan reaping in `process::Driver::park` |
| Sync | → | `watch` channels (signals), `tokio::sync::Mutex` (`File`) |
| Net & I/O | ↔ | `File` and `ChildStd*` implement `AsyncRead/AsyncWrite/AsyncSeek`; share `io::blocking::Buf` |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `asyncify(f)` | `fs/mod.rs` | `spawn_blocking(f).await`, map a `JoinError` to `io::Error` |
| `fs::read / read_to_string / write / copy / rename / remove_file / create_dir_all / metadata / canonicalize / try_exists / …` | `fs/*.rs` | One-shot ops (≈ 25 functions, ≈ 1 file each) |
| `File::open / create / options / read / write / seek / sync_all / sync_data / set_len / metadata / try_clone / into_std / set_max_buf_size` | `fs/file.rs` | Async file handle |
| `File::poll_read / poll_write / poll_flush / start_seek / poll_complete` | `fs/file.rs` | The Idle/Busy state machine |
| `read_dir → ReadDir::next_entry`, `DirEntry::path / metadata / file_type` | `fs/read_dir.rs` | Directory listing (batches of entries per blocking call) |
| `Command::new / arg(s) / env / current_dir / stdin / stdout / stderr / kill_on_drop / spawn / output / status` | `process/mod.rs` | Build and run |
| `Child::wait / try_wait / kill / start_kill / wait_with_output / id` | `process/mod.rs` | Manage a child |
| `spawn_child` (Unix) | `process/unix/mod.rs` | Choose pidfd reaper or SIGCHLD reaper |
| `GlobalOrphanQueue::reap_orphans` | `process/unix/mod.rs`, `orphan.rs` | Reap dropped children |
| `signal::ctrl_c()` | `signal/ctrl_c.rs` | `os_impl::ctrl_c()?.recv().await` |
| `unix::signal(kind) → Signal::recv / poll_recv` | `signal/unix.rs` | Signal stream |
| `signal_enable`, `action` | `signal/unix.rs` | Install handler once / handler body |
| `Globals::record_event / broadcast`, `Registry::register_listener` | `signal/registry.rs` | Pending flags → `watch` sends |
| `windows::ctrl_break / ctrl_close / ctrl_logoff / ctrl_shutdown` | `signal/windows.rs` | Console events |

---

## 7. Flows

**`File` read:** if the internal `Buf` still holds bytes (e.g. after a partial copy), they're copied out first; otherwise a blocking read of `min(your buffer size, max_buf_size = 2 MiB)` bytes is started into the internal `Buf` (`State::Busy`) and the call returns `Pending`; when it finishes, the bytes are copied into your `ReadBuf` and the state returns to `Idle`. There is no read-ahead — use `BufReader` for small reads. A `seek` or `set_len` first discards unread buffered bytes (seeking back by that amount).

**`File` write is asynchronous after return:** `write` copies your bytes into the internal buffer, starts a **mandatory** blocking write and returns `Ready(n)` immediately. Errors surface on the **next** operation (`last_write_err`) or on `flush()`. Call `flush()`/`sync_all()` before relying on the data being on disk.

**Child exit on Linux:** `pidfd_open(pid)` → register the pidfd with the I/O driver (readable = exited) → `wait()` awaits readability → `try_wait()`. If pidfds are unavailable (old kernel), fall back to the SIGCHLD reaper, which re-runs `try_wait` whenever any SIGCHLD arrives (signals coalesce, so each child checks on every SIGCHLD).

**Signal delivery is coalescing:** many identical signals between two polls arrive as **one** `recv()`. Once a handler is installed for a signal, it stays installed for the life of the process (the OS default action, e.g. terminate on SIGINT, no longer happens).

---

## 8. Invariants & gotchas

- **`fs` is not "truly" async:** each call costs a blocking-pool handoff. For many small ops, do them all inside one `spawn_blocking`.
- **`File` needs `flush()`** before drop if you care about write errors; drop doesn't report them.
- **Only one in-flight operation per `File`** (`Busy` state); concurrent use from two tasks serialises through the `Mutex`.
- **Processes:** without `kill_on_drop(true)`, dropping a `Child` leaves the process running (it's reaped later as an orphan). `Command::output()` reads stdout/stderr concurrently to avoid pipe deadlocks.
- **Signals:** creating a listener permanently replaces the default action for that signal; some signals are forbidden (`SIGKILL`, `SIGSTOP`, `SIGILL`, `SIGFPE`, `SIGSEGV`).
- On Unix, signals and process reaping **require the I/O driver** (`enable_io`); `fs` requires only the blocking pool.

---

## 9. Tests & where to start

<!-- TESTS:fs_process_signal -->
**47 integration test files · 136 test functions · 2,959 code lines**

[`fs.rs`](../../tokio/tests/fs.rs), [`fs_canonicalize_dir.rs`](../../tokio/tests/fs_canonicalize_dir.rs), [`fs_copy.rs`](../../tokio/tests/fs_copy.rs), [`fs_dir.rs`](../../tokio/tests/fs_dir.rs), [`fs_file.rs`](../../tokio/tests/fs_file.rs), [`fs_file_join_error.rs`](../../tokio/tests/fs_file_join_error.rs), [`fs_link.rs`](../../tokio/tests/fs_link.rs), [`fs_open_options.rs`](../../tokio/tests/fs_open_options.rs), [`fs_open_options_windows.rs`](../../tokio/tests/fs_open_options_windows.rs), [`fs_remove_dir_all.rs`](../../tokio/tests/fs_remove_dir_all.rs), [`fs_remove_file.rs`](../../tokio/tests/fs_remove_file.rs), [`fs_rename.rs`](../../tokio/tests/fs_rename.rs), [`fs_symlink_dir_windows.rs`](../../tokio/tests/fs_symlink_dir_windows.rs), [`fs_symlink_file_windows.rs`](../../tokio/tests/fs_symlink_file_windows.rs), [`fs_try_exists.rs`](../../tokio/tests/fs_try_exists.rs), [`fs_uring.rs`](../../tokio/tests/fs_uring.rs), [`fs_uring_cancel_open.rs`](../../tokio/tests/fs_uring_cancel_open.rs), [`fs_uring_completed_then_dropped_before_repoll.rs`](../../tokio/tests/fs_uring_completed_then_dropped_before_repoll.rs), [`fs_uring_file_read.rs`](../../tokio/tests/fs_uring_file_read.rs), [`fs_uring_no_io.rs`](../../tokio/tests/fs_uring_no_io.rs), … (+27 more)
<!-- /TESTS -->

**Read in this order:** `fs/mod.rs` (`asyncify`) → `fs/read.rs` → `fs/file.rs` (`poll_read`, `poll_write`) → `signal/unix.rs` (`action`, `signal_enable`) + `registry.rs` → `process/unix/mod.rs` header comment → `pidfd_reaper.rs`.
**Contribution areas seen in history:** missing `fs` functions/options, io_uring-backed ops (`open`, `read`, `write`, `statx`, `rename`), platform specifics (FreeBSD, Windows signals), process edge cases.
