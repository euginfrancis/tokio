# `tokio-util::sync::cancellation_token` — 17 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 7 |
| Public API | 4 |
| Private helper | 4 |
| Trait impl | 2 |

## `tokio-util/src/sync/cancellation_token/guard.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 14 | `token`  | `DropGuard` | Public API | Handle / reference plumbing | Returns a reference to the cancellation token wrapped by this guard. |
| 23 | `disarm`  | `DropGuard` | Public API | Other / internal logic | Returns stored cancellation token and removes this drop guard instance (i.e. |
| 31 | `drop`  | `Drop for DropGuard` | Trait impl | Drop / cleanup |  |

## `tokio-util/src/sync/cancellation_token/guard_ref.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `token`  | `DropGuardRef<'a>` | Public API | Handle / reference plumbing | Returns a reference to the cancellation token wrapped by this guard. |
| 26 | `disarm`  | `DropGuardRef<'a>` | Public API | Other / internal logic | Returns stored cancellation token and removes this drop guard instance (i.e. |
| 34 | `drop`  | `Drop for DropGuardRef<'_>` | Trait impl | Drop / cleanup |  |

## `tokio-util/src/sync/cancellation_token/tree_node.rs` (11)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 51 | `new`  | `TreeNode` | Crate-internal | Constructor |  |
| 64 | `notified`  | `TreeNode` | Crate-internal | Other / internal logic |  |
| 82 | `is_cancelled`  |  | Crate-internal | Accessor / query | Returns whether or not the node is cancelled |
| 87 | `child_node`  |  | Crate-internal | Other / internal logic | Creates a child node |
| 125 | `disconnect_children`  |  | Private helper | Other / internal logic | Disconnects the given parent from all of its children. |
| 150 | `with_locked_node_and_parent`  |  | Private helper | Constructor | Figures out the parent of the node and locks the node and its parent atomically. |
| 202 | `move_children_to_parent`  |  | Private helper | Other / internal logic | Moves all children from `node` to `parent`. |
| 220 | `remove_child`  |  | Private helper | Data movement | Removes a child from the parent. |
| 249 | `increase_handle_refcount`  |  | Crate-internal | Other / internal logic | Increases the reference count of handles. |
| 263 | `decrease_handle_refcount`  |  | Crate-internal | Other / internal logic | Decreases the reference count of handles. |
| 297 | `cancel`  |  | Crate-internal | Lifecycle / ref-count | Cancels a node and its children. |

