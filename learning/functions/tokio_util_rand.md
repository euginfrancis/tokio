# `tokio::util::rand` — 5 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Crate-internal | 4 |
| Public API | 1 |

## `tokio/src/util/rand/rt.rs` (4)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 22 | `new`  | `RngSeedGenerator` | Crate-internal | Constructor | Returns a new generator from the provided seed. |
| 29 | `next_seed`  | `RngSeedGenerator` | Crate-internal | Other / internal logic | Returns the next seed in the sequence. |
| 42 | `next_generator`  | `RngSeedGenerator` | Crate-internal | Other / internal logic | Directly creates a generator using the next seed. |
| 53 | `replace_seed`  | `FastRand` | Crate-internal | Other / internal logic | Replaces the state of the random number generator with the provided seed, returning the seed that represents the previous state of the random number generator. |

## `tokio/src/util/rand/rt_unstable.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 15 | `from_bytes`  | `RngSeed` | Public API | Conversion | Generates a seed from the provided byte slice. |

