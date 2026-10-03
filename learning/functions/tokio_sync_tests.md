# `tokio::sync::tests` — 102 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 102 |

## `tokio/src/sync/tests/atomic_waker.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `basic_usage`  |  | Test | Other / internal logic |  |
| 32 | `wake_without_register`  |  | Test | Wake / park |  |
| 44 | `failed_wake_synchronizes`  |  | Test | Other / internal logic |  |
| 50 | `failed_wake_synchronizes_inner`  |  | Test | Other / internal logic |  |
| 77 | `atomic_waker_panic_safe`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/loom_atomic_waker.rs` (2)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `basic_notification`  |  | Test | Other / internal logic |  |
| 48 | `test_panicky_waker`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/loom_broadcast.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `broadcast_send`  |  | Test | Data movement |  |
| 51 | `broadcast_two`  |  | Test | Data movement |  |
| 96 | `broadcast_wrap`  |  | Test | Data movement |  |
| 145 | `drop_rx`  |  | Test | Lifecycle / ref-count |  |
| 183 | `drop_multiple_rx_with_overflow`  |  | Test | Lifecycle / ref-count |  |

## `tokio/src/sync/tests/loom_list.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `smoke`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/loom_mpsc.rs` (17)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `closing_tx`  |  | Test | Other / internal logic |  |
| 28 | `closing_unbounded_tx`  |  | Test | Other / internal logic |  |
| 46 | `closing_bounded_rx`  |  | Test | Other / internal logic |  |
| 60 | `closing_and_sending`  |  | Test | Other / internal logic |  |
| 87 | `closing_unbounded_rx`  |  | Test | Other / internal logic |  |
| 101 | `dropping_tx`  |  | Test | Other / internal logic |  |
| 119 | `dropping_unbounded_tx`  |  | Test | Other / internal logic |  |
| 137 | `try_recv`  |  | Test | Non-blocking attempt |  |
| 152 | `run`  |  | Test | Runtime/task control |  |
| 193 | `len_nonzero_after_send`  |  | Test | Accessor / query |  |
| 210 | `nonempty_after_send`  |  | Test | Other / internal logic |  |
| 227 | `is_empty_during_close`  |  | Test | Accessor / query |  |
| 241 | `len_during_close_helper`  |  | Test | Accessor / query |  |
| 260 | `len_during_close_0`  |  | Test | Accessor / query |  |
| 265 | `len_during_close_1`  |  | Test | Accessor / query |  |
| 270 | `len_during_close_block_cap`  |  | Test | Accessor / query |  |
| 275 | `len_during_close_block_cap_plus_1`  |  | Test | Accessor / query |  |

## `tokio/src/sync/tests/loom_notify.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 13 | `notify_one`  |  | Test | Wake / park |  |
| 30 | `notify_waiters`  |  | Test | Wake / park |  |
| 51 | `notify_waiters_and_one`  |  | Test | Wake / park |  |
| 80 | `notify_multi`  |  | Test | Wake / park |  |
| 110 | `notify_drop`  |  | Test | Wake / park |  |
| 150 | `notify_waiters_poll_consistency`  |  | Test | Wake / park | Polls two `Notified` futures and checks if poll results are consistent with each other. |
| 151 | `notify_waiters_poll_consistency_variant`  |  | Test | Wake / park |  |
| 192 | `notify_waiters_poll_consistency_many`  |  | Test | Wake / park | Polls two `Notified` futures and checks if poll results are consistent with each other. |
| 193 | `notify_waiters_poll_consistency_many_variant`  |  | Test | Wake / park |  |
| 228 | `notify_waiters_is_atomic`  |  | Test | Wake / park | Checks if a call to `notify_waiters` is observed as atomic when combined with a concurrent call to `notify_one`. |
| 229 | `notify_waiters_is_atomic_variant`  |  | Test | Wake / park |  |
| 277 | `notify_waiters_sequential_notified_await`  |  | Test | Wake / park | Checks if a single call to `notify_waiters` does not get through two `Notified` futures created and awaited sequentially like this: notify.notified().await; notify.notified().await; |

## `tokio/src/sync/tests/loom_oneshot.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `smoke`  |  | Test | Other / internal logic |  |
| 24 | `changing_rx_task`  |  | Test | Other / internal logic |  |
| 60 | `try_recv_close`  |  | Test | Non-blocking attempt |  |
| 74 | `recv_closed`  |  | Test | Data movement |  |
| 98 | `new`  | `OnClose<'a>` | Test | Constructor |  |
| 106 | `poll`  | `Future for OnClose<'_>` | Test | Future impl (poll) |  |
| 115 | `changing_tx_task`  |  | Test | Other / internal logic |  |
| 143 | `checking_tx_send_ok_not_drop`  |  | Test | Other / internal logic |  |
| 154 | `drop`  | `Drop for Msg` | Test | Drop / cleanup |  |
| 190 | `drop_rx_after_poll`  |  | Test | Lifecycle / ref-count |  |

## `tokio/src/sync/tests/loom_rwlock.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 8 | `concurrent_write`  |  | Test | Other / internal logic |  |
| 39 | `concurrent_read_write`  |  | Test | Other / internal logic |  |
| 86 | `downgrade`  |  | Test | Handle / reference plumbing |  |

## `tokio/src/sync/tests/loom_semaphore_batch.rs` (10)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `basic_usage`  |  | Test | Other / internal logic |  |
| 22 | `actor` 🅰 |  | Test | Async operation |  |
| 51 | `release`  |  | Test | Locking / permits |  |
| 70 | `basic_closing`  |  | Test | Other / internal logic |  |
| 95 | `concurrent_close`  |  | Test | Other / internal logic |  |
| 116 | `concurrent_cancel`  |  | Test | Other / internal logic |  |
| 117 | `poll_and_cancel` 🅰 |  | Test | Poll function |  |
| 160 | `batch`  |  | Test | Other / internal logic |  |
| 200 | `release_during_acquire`  |  | Test | Locking / permits |  |
| 217 | `concurrent_permit_updates`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/loom_set_once.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `new`  | `DropCounter` | Test | Constructor |  |
| 21 | `assert_num_drops`  | `DropCounter` | Test | Debugging / tracing |  |
| 27 | `drop`  | `Drop for DropCounter` | Test | Drop / cleanup |  |
| 33 | `set_once_drop_test`  |  | Test | Configuration / setter |  |
| 56 | `set_once_wait_test`  |  | Test | Configuration / setter |  |

## `tokio/src/sync/tests/loom_watch.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 8 | `smoke`  |  | Test | Other / internal logic |  |
| 40 | `wait_for_test`  |  | Test | Runtime/task control |  |
| 66 | `wait_for_returns_correct_value`  |  | Test | Runtime/task control |  |
| 93 | `multiple_sender_drop_concurrently`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/notify.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `notify_clones_waker_before_lock`  |  | Test | Wake / park |  |
| 13 | `clone_w` ⚠ |  | Test | Other / internal logic |  |
| 24 | `drop_w` ⚠ |  | Test | Lifecycle / ref-count |  |
| 28 | `wake` ⚠ |  | Test | Wake / park |  |
| 32 | `wake_by_ref` ⚠ |  | Test | Wake / park |  |
| 52 | `notify_waiters_handles_panicking_waker`  |  | Test | Wake / park |  |
| 60 | `wake_by_ref`  | `ArcWake for PanickingWaker` | Test | Wake / park |  |
| 90 | `notify_simple`  |  | Test | Wake / park |  |
| 107 | `watch_test`  |  | Test | Other / internal logic |  |

## `tokio/src/sync/tests/semaphore_batch.rs` (19)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 10 | `poll_acquire_one_available`  |  | Test | Poll function |  |
| 20 | `poll_acquire_many_available`  |  | Test | Poll function |  |
| 33 | `try_acquire_one_available`  |  | Test | Non-blocking attempt |  |
| 45 | `try_acquire_many_available`  |  | Test | Non-blocking attempt |  |
| 57 | `poll_acquire_one_unavailable`  |  | Test | Poll function |  |
| 81 | `poll_acquire_many_unavailable`  |  | Test | Poll function |  |
| 118 | `try_acquire_one_unavailable`  |  | Test | Non-blocking attempt |  |
| 137 | `try_acquire_many_unavailable`  |  | Test | Non-blocking attempt |  |
| 159 | `poll_acquire_one_zero_permits`  |  | Test | Poll function |  |
| 174 | `max_permits_doesnt_panic`  |  | Test | Configuration / setter |  |
| 181 | `validates_max_permits`  |  | Test | Other / internal logic |  |
| 186 | `close_semaphore_prevents_acquire`  |  | Test | Data movement |  |
| 200 | `close_semaphore_notifies_permit1`  |  | Test | Data movement |  |
| 213 | `close_semaphore_notifies_permit2`  |  | Test | Data movement |  |
| 247 | `cancel_acquire_releases_permits`  |  | Test | Lifecycle / ref-count |  |
| 263 | `release_permits_at_drop`  |  | Test | Locking / permits |  |
| 274 | `wake_by_ref`  | `ArcWake for ReleaseOnDrop` | Test | Wake / park |  |
| 292 | `forget_permits_basic`  |  | Test | Locking / permits |  |
| 301 | `update_permits_many_times`  |  | Test | Other / internal logic |  |

