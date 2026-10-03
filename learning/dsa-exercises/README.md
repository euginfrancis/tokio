# Tokio DSA exercises

Small, **safe-Rust** versions of the data structures and algorithms described in
[`../DSA_IN_TOKIO.md`](../DSA_IN_TOKIO.md). Each module mirrors one piece of Tokio and
links to the real file.

```bash
cd learning/dsa-exercises
cargo test
```

How to use them:
1. Read the entry in `DSA_IN_TOKIO.md`.
2. Delete the body of a function here (keep the signature), re-implement it, and make `cargo test` pass.
3. Then read the real Tokio file and compare. What did Tokio do differently, and why (atomics, `unsafe`, no allocation)?

| Module | Mirrors | Guide entry |
|---|---|---|
| `rand` | `tokio/src/util/rand.rs` | A8, A9 |
| `wheel` | `tokio/src/runtime/time/wheel/` | D7, A5, A6, A7 |
| `steal_queue` | `tokio/src/runtime/scheduler/multi_thread/queue.rs` | D4, A1, A2 |
| `task_state` | `tokio/src/runtime/task/state.rs` | D12, A15 |
| `fair_semaphore` | `tokio/src/sync/batch_semaphore.rs` | A11, A12 |
| `ewma` | `tokio/src/runtime/scheduler/multi_thread/stats.rs` | A3 |
