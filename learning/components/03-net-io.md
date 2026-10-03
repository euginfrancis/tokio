# Block 3 — Net & I/O (public API)

> **Role:** everything that reads and writes bytes asynchronously: the I/O traits (`AsyncRead`, `AsyncWrite`, …), their ~40 helper futures (`read_exact`, `write_all`, `copy`, `lines`, …), buffering, in-memory pipes, stdio, and every socket type (TCP, UDP, Unix, Windows named pipes) plus DNS lookup.
> In the [component diagram](./README.md): the "net / io" API box. Sockets **register** with the [I/O driver](./08-io-driver.md); the generic I/O utilities work on *any* `AsyncRead`/`AsyncWrite` and need no driver at all.

---

## 1. At a glance

<!-- STATS:net_io -->
| Metric | Value |
|---|---|
| Source files | 86 |
| Code lines | 10,904 (21.5% of `tokio/src`) |
| Doc + comment lines | 16,548 (1.52 per code line) |
| Functions | 1,149 — public API 488, trait impls 373, internal 166, inline tests 20 |
| `async fn` / `unsafe fn` | 94 / 23 |
| `unsafe` occurrences | 203 |
| Integration tests (`tokio/tests`) | 62 files, 315 test fns, 8,314 code lines |
<!-- /STATS -->

The **largest block by files and doc lines**: `net` alone has more than 2 lines of docs per line of code, because each socket type exposes many small methods that are thin wrappers over `mio` + the driver.

---

## 2. Responsibility & boundary

| | |
|---|---|
| **Owns** | The four async I/O traits and `ReadBuf`; extension traits and all their futures; `BufReader/BufWriter/BufStream`; `copy*`; `split`/`join`; `duplex`/`simplex`; `empty`/`repeat`/`sink`; stdin/stdout/stderr; `AsyncFd`; `Interest`/`Ready`; `PollEvented` (the glue between a `mio` source and the driver); all socket types and their split halves; `ToSocketAddrs` + `lookup_host`. |
| **Does not own** | Waiting for the OS and dispatching events ([I/O driver](./08-io-driver.md)); running blocking stdio / DNS calls ([Blocking pool](./09-blocking-pool.md)); files ([fs block](./05-fs-process-signal.md)); framing/codecs (`tokio-util`). |
| **Input** | User calls (`read`, `write_all`, `accept`, `connect`, `send_to`, …). |
| **Output** | Non-blocking syscalls on `mio` sockets; readiness waits on `Registration`. |
| **Boundary types** | `AsyncRead`/`AsyncWrite` (the contract with the whole ecosystem: hyper, tonic, tokio-util…); `PollEvented<E>` → `Registration` (the contract with the driver). |

---

## 3. Files

<!-- FILES:net_io -->
| File | Code | Docs+comments | % of block |
|---|---:|---:|---:|
| [`tokio/src/net/udp.rs`](../../tokio/src/net/udp.rs) | 623 | 1,630 | 5.7% |
| [`tokio/src/net/windows/named_pipe.rs`](../../tokio/src/net/windows/named_pipe.rs) | 592 | 2,033 | 5.4% |
| [`tokio/src/net/tcp/socket.rs`](../../tokio/src/net/tcp/socket.rs) | 426 | 581 | 3.9% |
| [`tokio/src/net/tcp/stream.rs`](../../tokio/src/net/tcp/stream.rs) | 404 | 1,109 | 3.7% |
| [`tokio/src/io/async_fd.rs`](../../tokio/src/io/async_fd.rs) | 368 | 999 | 3.4% |
| [`tokio/src/net/unix/ucred.rs`](../../tokio/src/net/unix/ucred.rs) | 356 | 22 | 3.3% |
| [`tokio/src/net/unix/pipe.rs`](../../tokio/src/net/unix/pipe.rs) | 335 | 1,143 | 3.1% |
| [`tokio/src/io/blocking.rs`](../../tokio/src/io/blocking.rs) | 295 | 54 | 2.7% |
| [`tokio/src/net/unix/datagram/socket.rs`](../../tokio/src/net/unix/datagram/socket.rs) | 292 | 1,269 | 2.7% |
| [`tokio/src/io/util/mem.rs`](../../tokio/src/io/util/mem.rs) | 290 | 126 | 2.7% |
| [`tokio/src/net/unix/stream.rs`](../../tokio/src/net/unix/stream.rs) | 281 | 804 | 2.6% |
| [`tokio/src/io/async_write.rs`](../../tokio/src/io/async_write.rs) | 240 | 145 | 2.2% |
| [`tokio/src/io/util/buf_writer.rs`](../../tokio/src/io/util/buf_writer.rs) | 229 | 54 | 2.1% |
| [`tokio/src/io/util/copy.rs`](../../tokio/src/io/util/copy.rs) | 227 | 69 | 2.1% |
| [`tokio/src/net/addr.rs`](../../tokio/src/net/addr.rs) | 212 | 42 | 1.9% |
| [`tokio/src/io/util/buf_reader.rs`](../../tokio/src/io/util/buf_reader.rs) | 202 | 85 | 1.9% |
| [`tokio/src/io/poll_evented.rs`](../../tokio/src/io/poll_evented.rs) | 183 | 107 | 1.7% |
| [`tokio/src/net/tcp/split_owned.rs`](../../tokio/src/net/tcp/split_owned.rs) | 176 | 294 | 1.6% |
| [`tokio/src/io/interest.rs`](../../tokio/src/io/interest.rs) | 175 | 127 | 1.6% |
| [`tokio/src/io/read_buf.rs`](../../tokio/src/io/read_buf.rs) | 173 | 138 | 1.6% |
| [`tokio/src/net/tcp/listener.rs`](../../tokio/src/net/tcp/listener.rs) | 167 | 259 | 1.5% |
| [`tokio/src/net/unix/split_owned.rs`](../../tokio/src/net/unix/split_owned.rs) | 165 | 219 | 1.5% |
| [`tokio/src/io/ready.rs`](../../tokio/src/io/ready.rs) | 163 | 107 | 1.5% |
| [`tokio/src/io/stdio_common.rs`](../../tokio/src/io/stdio_common.rs) | 161 | 40 | 1.5% |
| [`tokio/src/io/util/buf_stream.rs`](../../tokio/src/io/util/buf_stream.rs) | 140 | 49 | 1.3% |
| [`tokio/src/io/util/read_int.rs`](../../tokio/src/io/util/read_int.rs) | 135 | 3 | 1.2% |
| [`tokio/src/io/util/write_int.rs`](../../tokio/src/io/util/write_int.rs) | 135 | 2 | 1.2% |
| [`tokio/src/net/tcp/split.rs`](../../tokio/src/net/tcp/split.rs) | 118 | 276 | 1.1% |
| [`tokio/src/net/unix/socket.rs`](../../tokio/src/net/unix/socket.rs) | 118 | 129 | 1.1% |
| [`tokio/src/io/util/chain.rs`](../../tokio/src/io/util/chain.rs) | 116 | 15 | 1.1% |
| *…56 smaller files* | 3,407 | 4,618 | 31.2% |
| **Total (86 files)** | **10,904** | **16,548** | 100% |
<!-- /FILES -->

```
io/
├── async_read.rs, async_write.rs, async_buf_read.rs, async_seek.rs   the 4 traits
├── read_buf.rs           ReadBuf: tracks filled / initialized parts of a buffer
├── poll_evented.rs       PollEvented<E>: mio source + Registration → AsyncRead/AsyncWrite
├── async_fd.rs           AsyncFd<T>: any Unix fd made async
├── interest.rs, ready.rs bitflags
├── split.rs, join.rs     generic split (Arc<Mutex<T>>) / join two halves
├── stdin.rs, stdout.rs, stderr.rs, stdio_common.rs, blocking.rs     stdio via the blocking pool
├── seek.rs, bsd/ (POSIX AIO), uring/ (io_uring ops, unstable)
└── util/  (37 files)     *_ext.rs traits; one Future per op: read.rs, read_exact.rs, read_to_end.rs,
                          read_line.rs, read_until.rs, lines.rs, write_all.rs, write_buf.rs, copy*.rs,
                          buf_reader.rs, buf_writer.rs, buf_stream.rs, chain.rs, take.rs, mem.rs (duplex/simplex), …
net/
├── tcp/   listener.rs, stream.rs, socket.rs (TcpSocket), split.rs (borrowed halves), split_owned.rs (Arc halves)
├── udp.rs
├── unix/  listener.rs, stream.rs, datagram/, socket.rs, pipe.rs, ucred.rs, split*.rs
├── windows/named_pipe.rs (the most documented file in Tokio)
├── addr.rs (ToSocketAddrs), lookup_host.rs
```

---

## 4. Data structures

```rust
pub trait AsyncRead  { fn poll_read(self: Pin<&mut Self>, cx, buf: &mut ReadBuf<'_>) -> Poll<io::Result<()>>; }
pub trait AsyncWrite { fn poll_write(..) -> Poll<io::Result<usize>>; fn poll_flush(..); fn poll_shutdown(..);
                       fn poll_write_vectored(..) /* default */; fn is_write_vectored(&self) -> bool; }
pub trait AsyncBufRead { fn poll_fill_buf(..) -> Poll<io::Result<&[u8]>>; fn consume(self: Pin<&mut Self>, amt: usize); }
pub trait AsyncSeek    { fn start_seek(..); fn poll_complete(..) -> Poll<io::Result<u64>>; }

pub struct ReadBuf<'a> {                    // safe reads into possibly-uninitialised memory
    buf: &'a mut [MaybeUninit<u8>],
    filled: usize,                          // bytes holding data
    initialized: usize,                     // bytes known to be initialised (≥ filled)
}

pub(crate) struct PollEvented<E: mio::event::Source> {   // io/poll_evented.rs
    io: Option<E>,                          // the mio socket (Option so it can be taken on drop/into_std)
    registration: Registration,             // link to the I/O driver (Arc<ScheduledIo>)
}
pub struct TcpStream   { io: PollEvented<mio::net::TcpStream> }
pub struct TcpListener { io: PollEvented<mio::net::TcpListener> }
pub struct UdpSocket   { io: PollEvented<mio::net::UdpSocket> }
// UnixStream, UnixListener, UnixDatagram, NamedPipe*: same pattern
pub struct TcpSocket   { inner: socket2::Socket }          // configure before connect/listen

pub struct Interest(usize);  pub struct Ready(usize);      // READABLE | WRITABLE | ERROR | PRIORITY …

// Splitting
pub struct tcp::ReadHalf<'a>(&'a TcpStream);               // zero-cost: TcpStream methods take &self
pub struct tcp::OwnedReadHalf  { inner: Arc<TcpStream> }
pub struct tcp::OwnedWriteHalf { inner: Arc<TcpStream>, shutdown_on_drop: bool }
pub struct io::ReadHalf<T> { inner: Arc<Inner<T>> }       // generic: Inner { stream: Mutex<T>, … }

// Utilities
pub struct BufReader<R> { inner: R, buf: Box<[u8]>, pos: usize, cap: usize, seek_state }
pub struct DuplexStream { read: Arc<Mutex<SimplexStream>>, write: Arc<Mutex<SimplexStream>> }
pub struct SimplexStream { buffer: BytesMut, is_closed: bool, max_buf_size: usize, read_waker, write_waker }
pub struct ReadToEnd<'a, R> { reader, buf: VecWithInitialized<&mut Vec<u8>>, read: usize, … }   // one Future per op
```

---

## 5. How it interacts with the other blocks

```
 user: stream.read(&mut buf).await
   └▶ AsyncReadExt::read → Read<'_, TcpStream> future → TcpStream::poll_read → PollEvented::poll_read
        loop {
          ev = Registration::poll_read_ready(cx)?  ───────────▶ [I/O drv] ScheduledIo::poll_readiness (waker stored)
          mio_stream.read(buf):  Ok(n) → done (short read ⇒ clear_readiness) | WouldBlock ⇒ clear_readiness(ev), retry
        }
 user: listener.accept().await ─▶ Registration::async_io(READABLE, || mio.accept()) ─▶ TcpStream::new_accepted (registers)
 user: TcpStream::connect(addr) ─▶ to_socket_addrs (DNS ⇒ [Blocking pool] if a hostname) ─▶ mio connect ─▶ wait WRITABLE ─▶ take_error()
 user: io::copy(&mut r, &mut w) ─▶ CopyBuffer poll loop over ANY AsyncRead/AsyncWrite (no driver involved)
 user: io::stdin() ─▶ Blocking<std::io::Stdin> ─▶ [Blocking pool] reads in the background
 every op ─▶ coop::poll_proceed ([Tasks])
```

| Other block | Direction | Through |
|---|---|---|
| I/O driver | → | `Registration::{new, poll_ready, poll_io, try_io, async_io, readiness, clear_readiness, deregister}` |
| Blocking pool | → | stdio (`io/blocking.rs`), `lookup_host`/hostname resolution |
| Tasks | → | coop budget per operation |
| fs / process | ← | `fs::File`, `ChildStdin/Stdout/Stderr` implement these traits; process pipes use `PollEvented` |
| `tokio-util` / ecosystem | ← | `Framed`, `ReaderStream`, `compat`, hyper, tonic all speak `AsyncRead/AsyncWrite` |

---

## 6. Basic functions

| Function | File | What it does |
|---|---|---|
| `PollEvented::new / new_with_interest / poll_read / poll_write / poll_write_vectored / into_inner` | `io/poll_evented.rs` | Readiness-loop around a mio source |
| `AsyncReadExt::read / read_exact / read_to_end / read_to_string / read_buf / read_u8..read_f64(_le) / take / chain` | `io/util/async_read_ext.rs` | Each returns a dedicated `Future` struct |
| `AsyncWriteExt::write / write_all / write_buf / write_all_buf / write_vectored / flush / shutdown / write_u8..` | `io/util/async_write_ext.rs` | 〃 |
| `AsyncBufReadExt::read_line / read_until / lines / split / fill_buf / consume` | `io/util/async_buf_read_ext.rs` | 〃 |
| `copy / copy_buf / copy_bidirectional(_with_sizes)` | `io/util/copy*.rs` | Pump bytes between streams |
| `split / join` | `io/split.rs`, `io/join.rs` | Generic halves (lock-based) / combine |
| `duplex(n) / simplex(n)`, `empty / repeat / sink` | `io/util/mem.rs`, … | In-memory streams |
| `stdin / stdout / stderr` | `io/std*.rs` | Async stdio via blocking pool |
| `AsyncFd::new / readable / writable / ready / try_io / poll_read_ready` | `io/async_fd.rs` | Async wrapper for any fd |
| `TcpListener::bind / accept / poll_accept / local_addr / from_std / into_std` | `net/tcp/listener.rs` | Server sockets |
| `TcpStream::connect / peek / split / into_split / readable / writable / ready / try_read / try_write / set_nodelay / set_linger` | `net/tcp/stream.rs` | Stream sockets |
| `TcpSocket::new_v4/v6 / set_reuseaddr / set_send_buffer_size / bind / connect / listen` | `net/tcp/socket.rs` | Pre-connect configuration |
| `UdpSocket::bind / connect / send / recv / send_to / recv_from / peek_from / join_multicast_v4 / set_broadcast` | `net/udp.rs` | Datagrams |
| `UnixStream / UnixListener / UnixDatagram / UnixSocket` + `peer_cred` | `net/unix/*` | Unix sockets |
| `NamedPipeServer / NamedPipeClient / ServerOptions / ClientOptions` | `net/windows/named_pipe.rs` | Windows pipes |
| `lookup_host`, `ToSocketAddrs` | `net/lookup_host.rs`, `net/addr.rs` | DNS (blocking pool for names, inline for literals) |

---

## 7. Flows

**Read path** (`PollEvented::poll_read`): wait readiness → `read()` into `ReadBuf`'s unfilled part → short read ⇒ clear readiness (epoll/kqueue) → `WouldBlock` ⇒ clear and wait again. Every Tokio socket read/write is this loop.

**Two API styles on every socket:**
1. Trait style: `AsyncRead/AsyncWrite` via `poll_*` — needs `&mut self` (or a split half).
2. Readiness style: `readable().await` then `try_read(&buf)` — works with `&self`, so one `Arc<TcpStream>` can be shared by a reader task and a writer task.

**Helper futures:** `stream.read_exact(&mut buf)` returns `ReadExact { reader, buf, … }` whose `poll` calls `poll_read` repeatedly until full. Almost every file in `io/util/` is one such state machine — the easiest Tokio code to read and a common first-contribution area.

**`copy_bidirectional(a, b)`:** two `CopyBuffer`s polled in one future; each direction reads into its buffer, writes it out, and when its reader hits EOF it `shutdown()`s the other side's writer.

---

## 8. Invariants & gotchas

- **`ReadBuf` contract:** an implementor may only *add* filled bytes; uninitialised memory is never exposed to safe code.
- **Cancel safety varies:** `read`, `read_buf`, `accept`, `recv` are cancel-safe (nothing lost if dropped in `select!`); `read_exact`, `read_to_end`, `write_all`, `read_line` are **not** (partial progress is lost). Each method documents it.
- **Writes are buffered by the kernel, not by Tokio** — but `BufWriter` must be `flush()`ed, and `shutdown()` sends FIN.
- **Generic `split()` uses a lock**; prefer `TcpStream::split()` (borrowed, zero-cost) or `into_split()` (`Arc`, owned).
- **Dropping `OwnedWriteHalf` shuts down the write side** (unless `forget()`).
- Sockets are bound to the runtime that registered them; using them after that runtime shuts down errors.
- `from_std` requires the std socket to be **non-blocking** already; otherwise reads block the worker.

---

## 9. Tests & where to start

<!-- TESTS:net_io -->
**62 integration test files · 315 test functions · 8,314 code lines**

[`buffered.rs`](../../tokio/tests/buffered.rs), [`duplex_stream.rs`](../../tokio/tests/duplex_stream.rs), [`io_async_fd.rs`](../../tokio/tests/io_async_fd.rs), [`io_async_fd_memory_leak.rs`](../../tokio/tests/io_async_fd_memory_leak.rs), [`io_async_read.rs`](../../tokio/tests/io_async_read.rs), [`io_buf_reader.rs`](../../tokio/tests/io_buf_reader.rs), [`io_buf_writer.rs`](../../tokio/tests/io_buf_writer.rs), [`io_chain.rs`](../../tokio/tests/io_chain.rs), [`io_copy.rs`](../../tokio/tests/io_copy.rs), [`io_copy_bidirectional.rs`](../../tokio/tests/io_copy_bidirectional.rs), [`io_copy_buf.rs`](../../tokio/tests/io_copy_buf.rs), [`io_driver.rs`](../../tokio/tests/io_driver.rs), [`io_driver_drop.rs`](../../tokio/tests/io_driver_drop.rs), [`io_emscripten.rs`](../../tokio/tests/io_emscripten.rs), [`io_fill_buf.rs`](../../tokio/tests/io_fill_buf.rs), [`io_join.rs`](../../tokio/tests/io_join.rs), [`io_lines.rs`](../../tokio/tests/io_lines.rs), [`io_mem_stream.rs`](../../tokio/tests/io_mem_stream.rs), [`io_panic.rs`](../../tokio/tests/io_panic.rs), [`io_poll_aio.rs`](../../tokio/tests/io_poll_aio.rs), … (+42 more)
<!-- /TESTS -->

**Read in this order:** `io/async_read.rs` + `read_buf.rs` → `io/util/read_exact.rs` (a tiny future) → `io/util/copy.rs` → `io/poll_evented.rs` → `net/tcp/stream.rs` (`connect_mio`, `poll_read_priv`) → `io/util/mem.rs` (duplex).
**Contribution areas seen in history:** new `*_ext` methods, cancel-safety docs, platform socket options (FreeBSD/illumos/Windows), `AsyncFd` improvements, error-path behavior in `lines`/`read_until`.
