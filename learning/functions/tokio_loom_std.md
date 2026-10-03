# `tokio::loom::std` — 74 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 55 |
| Trait impl | 18 |
| Private helper | 1 |

## `tokio/src/loom/std/atomic_u16.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `new` 🅲 | `AtomicU16` | Crate-internal | Constructor |  |
| 28 | `unsync_load` ⚠ | `AtomicU16` | Crate-internal | Other / internal logic | Performs an unsynchronized load. |
| 36 | `deref`  | `Deref for AtomicU16` | Trait impl | Deref |  |
| 44 | `fmt`  | `fmt::Debug for AtomicU16` | Trait impl | Formatting |  |

## `tokio/src/loom/std/atomic_u32.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `new` 🅲 | `AtomicU32` | Crate-internal | Constructor |  |
| 28 | `unsync_load` ⚠ | `AtomicU32` | Crate-internal | Other / internal logic | Performs an unsynchronized load. |
| 36 | `deref`  | `Deref for AtomicU32` | Trait impl | Deref |  |
| 44 | `fmt`  | `fmt::Debug for AtomicU32` | Trait impl | Formatting |  |

## `tokio/src/loom/std/atomic_u64_as_mutex.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `load`  | `AtomicU64` | Crate-internal | Other / internal logic |  |
| 26 | `store`  | `AtomicU64` | Crate-internal | Configuration / setter |  |
| 30 | `fetch_add`  | `AtomicU64` | Crate-internal | Other / internal logic |  |
| 37 | `fetch_or`  | `AtomicU64` | Crate-internal | Other / internal logic |  |
| 44 | `compare_exchange`  | `AtomicU64` | Crate-internal | Other / internal logic |  |
| 61 | `compare_exchange_weak`  | `AtomicU64` | Crate-internal | Other / internal logic |  |
| 73 | `default`  | `Default for AtomicU64` | Trait impl | Constructor |  |

## `tokio/src/loom/std/atomic_u64_static_const_new.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 7 | `new` 🅲 | `AtomicU64` | Crate-internal | Constructor |  |

## `tokio/src/loom/std/atomic_u64_static_once_cell.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `new`  | `AtomicU64` | Crate-internal | Constructor |  |
| 19 | `new` 🅲 | `StaticAtomicU64` | Crate-internal | Constructor |  |
| 26 | `load`  | `StaticAtomicU64` | Crate-internal | Other / internal logic |  |
| 30 | `fetch_add`  | `StaticAtomicU64` | Crate-internal | Other / internal logic |  |
| 37 | `compare_exchange_weak`  | `StaticAtomicU64` | Crate-internal | Other / internal logic |  |
| 54 | `inner`  | `StaticAtomicU64` | Private helper | Handle / reference plumbing |  |

## `tokio/src/loom/std/atomic_usize.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `new` 🅲 | `AtomicUsize` | Crate-internal | Constructor |  |
| 28 | `unsync_load` ⚠ | `AtomicUsize` | Crate-internal | Other / internal logic | Performs an unsynchronized load. |
| 32 | `with_mut`  | `AtomicUsize` | Crate-internal | Constructor |  |
| 38 | `fetch_update`  | `AtomicUsize` | Crate-internal | Other / internal logic |  |
| 55 | `deref`  | `ops::Deref for AtomicUsize` | Trait impl | Deref |  |
| 63 | `deref_mut`  | `ops::DerefMut for AtomicUsize` | Trait impl | Deref |  |
| 70 | `fmt`  | `fmt::Debug for AtomicUsize` | Trait impl | Formatting |  |

## `tokio/src/loom/std/barrier.rs` (6)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 64 | `fmt`  | `fmt::Debug for Barrier` | Trait impl | Formatting |  |
| 85 | `new`  | `Barrier` | Crate-internal | Constructor | Creates a new barrier that can block a given number of threads. |
| 132 | `wait`  | `Barrier` | Crate-internal | Runtime/task control | Blocks the current thread until all threads have rendezvoused here. |
| 153 | `wait_timeout`  | `Barrier` | Crate-internal | Runtime/task control | Blocks the current thread until all threads have rendezvoused here for at most `timeout` duration. |
| 196 | `fmt`  | `fmt::Debug for BarrierWaitResult` | Trait impl | Formatting |  |
| 220 | `is_leader`  | `BarrierWaitResult` | Crate-internal | Accessor / query | Returns `true` if this thread is the "leader thread" for the call to [`Barrier::wait()`]. |

## `tokio/src/loom/std/mod.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 40 | `seed`  |  | Crate-internal | Configuration / setter |  |
| 85 | `num_cpus`  |  | Crate-internal | Accessor / query |  |
| 108 | `num_cpus`  |  | Crate-internal | Accessor / query |  |
| 115 | `yield_now`  |  | Crate-internal | Other / internal logic |  |

## `tokio/src/loom/std/mutex.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `new`  | `Mutex<T>` | Crate-internal | Constructor |  |
| 16 | `const_new` 🅲 | `Mutex<T>` | Crate-internal | Constructor |  |
| 21 | `lock`  | `Mutex<T>` | Crate-internal | Locking / permits |  |
| 29 | `try_lock`  | `Mutex<T>` | Crate-internal | Non-blocking attempt |  |

## `tokio/src/loom/std/parking_lot.rs` (23)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 50 | `new`  | `Mutex<T>` | Crate-internal | Constructor |  |
| 56 | `const_new` 🅲 | `Mutex<T>` | Crate-internal | Constructor |  |
| 61 | `lock`  | `Mutex<T>` | Crate-internal | Locking / permits |  |
| 66 | `try_lock`  | `Mutex<T>` | Crate-internal | Non-blocking attempt |  |
| 73 | `get_mut`  | `Mutex<T>` | Crate-internal | Accessor / query |  |
| 83 | `deref`  | `Deref for MutexGuard<'a, T>` | Trait impl | Deref |  |
| 89 | `deref_mut`  | `DerefMut for MutexGuard<'a, T>` | Trait impl | Deref |  |
| 95 | `new`  | `RwLock<T>` | Crate-internal | Constructor |  |
| 99 | `read`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 103 | `try_read`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |
| 109 | `write`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 113 | `try_write`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |
| 122 | `deref`  | `Deref for RwLockReadGuard<'a, T>` | Trait impl | Deref |  |
| 129 | `deref`  | `Deref for RwLockWriteGuard<'a, T>` | Trait impl | Deref |  |
| 135 | `deref_mut`  | `DerefMut for RwLockWriteGuard<'a, T>` | Trait impl | Deref |  |
| 142 | `new`  | `Condvar` | Crate-internal | Constructor |  |
| 147 | `notify_one`  | `Condvar` | Crate-internal | Wake / park |  |
| 152 | `notify_all`  | `Condvar` | Crate-internal | Wake / park |  |
| 157 | `wait`  | `Condvar` | Crate-internal | Runtime/task control |  |
| 166 | `wait_timeout`  | `Condvar` | Crate-internal | Runtime/task control |  |
| 180 | `fmt`  | `fmt::Display for MutexGuard<'a, T>` | Trait impl | Formatting |  |
| 186 | `fmt`  | `fmt::Display for RwLockReadGuard<'a, T>` | Trait impl | Formatting |  |
| 192 | `fmt`  | `fmt::Display for RwLockWriteGuard<'a, T>` | Trait impl | Formatting |  |

## `tokio/src/loom/std/rwlock.rs` (5)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 11 | `new`  | `RwLock<T>` | Crate-internal | Constructor |  |
| 16 | `read`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 24 | `try_read`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |
| 33 | `write`  | `RwLock<T>` | Crate-internal | I/O operation |  |
| 41 | `try_write`  | `RwLock<T>` | Crate-internal | Non-blocking attempt |  |

## `tokio/src/loom/std/unsafe_cell.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 5 | `new` 🅲 | `UnsafeCell<T>` | Crate-internal | Constructor |  |
| 10 | `with`  | `UnsafeCell<T>` | Crate-internal | Combinator / iteration |  |
| 15 | `with_mut`  | `UnsafeCell<T>` | Crate-internal | Constructor |  |

