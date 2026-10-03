# `tokio::sync::rwlock` — 57 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Trait impl | 28 |
| Public API | 23 |
| Private helper | 6 |

## `tokio/src/sync/rwlock/owned_read_guard.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `skip_drop`  | `OwnedRwLockReadGuard<T, U>` | Private helper | Combinator / iteration |  |
| 76 | `map`  | `OwnedRwLockReadGuard<T, U>` | Public API | Combinator / iteration | Makes a new `OwnedRwLockReadGuard` for a component of the locked data. |
| 123 | `try_map`  | `OwnedRwLockReadGuard<T, U>` | Public API | Non-blocking attempt | Attempts to make a new [`OwnedRwLockReadGuard`] for a component of the locked data. |
| 164 | `rwlock`  | `OwnedRwLockReadGuard<T, U>` | Public API | Other / internal logic | Returns a reference to the original `Arc<RwLock>`. |
| 172 | `deref`  | `ops::Deref for OwnedRwLockReadGuard<T, U>` | Trait impl | Deref |  |
| 181 | `fmt`  | `fmt::Debug for OwnedRwLockReadGuard<T, U>` | Trait impl | Formatting |  |
| 190 | `fmt`  | `fmt::Display for OwnedRwLockReadGuard<T, U>` | Trait impl | Formatting |  |
| 196 | `drop`  | `Drop for OwnedRwLockReadGuard<T, U>` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/rwlock/owned_write_guard.rs` (13)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `skip_drop`  | `OwnedRwLockWriteGuard<T>` | Private helper | Combinator / iteration |  |
| 86 | `map`  | `OwnedRwLockWriteGuard<T>` | Public API | Combinator / iteration | Makes a new [`OwnedRwLockMappedWriteGuard`] for a component of the locked data. |
| 135 | `downgrade_map`  | `OwnedRwLockWriteGuard<T>` | Public API | Other / internal logic | Makes a new [`OwnedRwLockReadGuard`] for a component of the locked data. |
| 210 | `try_map`  | `OwnedRwLockWriteGuard<T>` | Public API | Non-blocking attempt | Attempts to make a new [`OwnedRwLockMappedWriteGuard`] for a component of the locked data. |
| 269 | `try_downgrade_map`  | `OwnedRwLockWriteGuard<T>` | Public API | Non-blocking attempt | Attempts to make a new [`OwnedRwLockReadGuard`] for a component of the locked data. |
| 320 | `into_mapped`  | `OwnedRwLockWriteGuard<T>` | Public API | Conversion | Converts this `OwnedRwLockWriteGuard` into an `OwnedRwLockMappedWriteGuard`. |
| 359 | `downgrade`  | `OwnedRwLockWriteGuard<T>` | Public API | Handle / reference plumbing | Atomically downgrades a write lock into a read lock without allowing any writers to take exclusive access of the lock in the meantime. |
| 410 | `rwlock`  | `OwnedRwLockWriteGuard<T>` | Public API | Other / internal logic | Returns a reference to the original `Arc<RwLock>`. |
| 418 | `deref`  | `ops::Deref for OwnedRwLockWriteGuard<T>` | Trait impl | Deref |  |
| 424 | `deref_mut`  | `ops::DerefMut for OwnedRwLockWriteGuard<T>` | Trait impl | Deref |  |
| 433 | `fmt`  | `fmt::Debug for OwnedRwLockWriteGuard<T>` | Trait impl | Formatting |  |
| 442 | `fmt`  | `fmt::Display for OwnedRwLockWriteGuard<T>` | Trait impl | Formatting |  |
| 448 | `drop`  | `Drop for OwnedRwLockWriteGuard<T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/rwlock/owned_write_guard_mapped.rs` (9)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 37 | `skip_drop`  | `OwnedRwLockMappedWriteGuard<T, U>` | Private helper | Combinator / iteration |  |
| 85 | `map`  | `OwnedRwLockMappedWriteGuard<T, U>` | Public API | Combinator / iteration | Makes a new `OwnedRwLockMappedWriteGuard` for a component of the locked data. |
| 136 | `try_map`  | `OwnedRwLockMappedWriteGuard<T, U>` | Public API | Non-blocking attempt | Attempts to make a new `OwnedRwLockMappedWriteGuard` for a component of the locked data. |
| 180 | `rwlock`  | `OwnedRwLockMappedWriteGuard<T, U>` | Public API | Other / internal logic | Returns a reference to the original `Arc<RwLock>`. |
| 188 | `deref`  | `ops::Deref for OwnedRwLockMappedWriteGuard<T, U>` | Trait impl | Deref |  |
| 194 | `deref_mut`  | `ops::DerefMut for OwnedRwLockMappedWriteGuard<T, U>` | Trait impl | Deref |  |
| 203 | `fmt`  | `fmt::Debug for OwnedRwLockMappedWriteGuard<T, U>` | Trait impl | Formatting |  |
| 212 | `fmt`  | `fmt::Display for OwnedRwLockMappedWriteGuard<T, U>` | Trait impl | Formatting |  |
| 218 | `drop`  | `Drop for OwnedRwLockMappedWriteGuard<T, U>` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/rwlock/read_guard.rs` (7)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 34 | `skip_drop`  | `RwLockReadGuard<'a, T>` | Private helper | Combinator / iteration |  |
| 80 | `map`  | `RwLockReadGuard<'a, T>` | Public API | Combinator / iteration | Makes a new `RwLockReadGuard` for a component of the locked data. |
| 132 | `try_map`  | `RwLockReadGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`RwLockReadGuard`] for a component of the locked data. |
| 155 | `deref`  | `ops::Deref for RwLockReadGuard<'_, T>` | Trait impl | Deref |  |
| 164 | `fmt`  | `fmt::Debug for RwLockReadGuard<'a, T>` | Trait impl | Formatting |  |
| 173 | `fmt`  | `fmt::Display for RwLockReadGuard<'a, T>` | Trait impl | Formatting |  |
| 179 | `drop`  | `Drop for RwLockReadGuard<'a, T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/rwlock/write_guard.rs` (12)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 38 | `skip_drop`  | `RwLockWriteGuard<'a, T>` | Private helper | Combinator / iteration |  |
| 88 | `map`  | `RwLockWriteGuard<'a, T>` | Public API | Combinator / iteration | Makes a new [`RwLockMappedWriteGuard`] for a component of the locked data. |
| 143 | `downgrade_map`  | `RwLockWriteGuard<'a, T>` | Public API | Other / internal logic | Makes a new [`RwLockReadGuard`] for a component of the locked data. |
| 222 | `try_map`  | `RwLockWriteGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`RwLockMappedWriteGuard`] for a component of the locked data. |
| 287 | `try_downgrade_map`  | `RwLockWriteGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`RwLockReadGuard`] for a component of the locked data. |
| 335 | `into_mapped`  | `RwLockWriteGuard<'a, T>` | Public API | Conversion | Converts this `RwLockWriteGuard` into an `RwLockMappedWriteGuard`. |
| 376 | `downgrade`  | `RwLockWriteGuard<'a, T>` | Public API | Handle / reference plumbing | Atomically downgrades a write lock into a read lock without allowing any writers to take exclusive access of the lock in the meantime. |
| 415 | `deref`  | `ops::Deref for RwLockWriteGuard<'_, T>` | Trait impl | Deref |  |
| 421 | `deref_mut`  | `ops::DerefMut for RwLockWriteGuard<'_, T>` | Trait impl | Deref |  |
| 430 | `fmt`  | `fmt::Debug for RwLockWriteGuard<'a, T>` | Trait impl | Formatting |  |
| 439 | `fmt`  | `fmt::Display for RwLockWriteGuard<'a, T>` | Trait impl | Formatting |  |
| 445 | `drop`  | `Drop for RwLockWriteGuard<'a, T>` | Trait impl | Drop / cleanup |  |

## `tokio/src/sync/rwlock/write_guard_mapped.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 36 | `skip_drop`  | `RwLockMappedWriteGuard<'a, T>` | Private helper | Combinator / iteration |  |
| 85 | `map`  | `RwLockMappedWriteGuard<'a, T>` | Public API | Combinator / iteration | Makes a new `RwLockMappedWriteGuard` for a component of the locked data. |
| 141 | `try_map`  | `RwLockMappedWriteGuard<'a, T>` | Public API | Non-blocking attempt | Attempts to make a new [`RwLockMappedWriteGuard`] for a component of the locked data. |
| 171 | `deref`  | `ops::Deref for RwLockMappedWriteGuard<'_, T>` | Trait impl | Deref |  |
| 177 | `deref_mut`  | `ops::DerefMut for RwLockMappedWriteGuard<'_, T>` | Trait impl | Deref |  |
| 186 | `fmt`  | `fmt::Debug for RwLockMappedWriteGuard<'a, T>` | Trait impl | Formatting |  |
| 195 | `fmt`  | `fmt::Display for RwLockMappedWriteGuard<'a, T>` | Trait impl | Formatting |  |
| 201 | `drop`  | `Drop for RwLockMappedWriteGuard<'a, T>` | Trait impl | Drop / cleanup |  |

