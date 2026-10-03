# `tokio-macros (crate root)` — 39 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Private helper | 25 |
| Public API | 8 |
| Crate-internal | 4 |
| Trait impl | 2 |

## `tokio-macros/src/entry.rs` (28)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 17 | `from_str`  | `RuntimeFlavor` | Private helper | Conversion |  |
| 37 | `from_str`  | `UnhandledPanic` | Private helper | Conversion |  |
| 45 | `into_tokens`  | `UnhandledPanic` | Private helper | Conversion |  |
| 87 | `new`  | `Configuration` | Private helper | Constructor |  |
| 104 | `set_name`  | `Configuration` | Private helper | Configuration / setter |  |
| 114 | `set_flavor`  | `Configuration` | Private helper | Configuration / setter |  |
| 126 | `set_worker_threads`  | `Configuration` | Private helper | Configuration / setter |  |
| 146 | `set_start_paused`  | `Configuration` | Private helper | Configuration / setter |  |
| 156 | `set_crate_name`  | `Configuration` | Private helper | Configuration / setter |  |
| 165 | `set_unhandled_panic`  | `Configuration` | Private helper | Configuration / setter |  |
| 184 | `macro_name`  | `Configuration` | Private helper | Other / internal logic |  |
| 192 | `build`  | `Configuration` | Private helper | Constructor |  |
| 254 | `parse_int`  |  | Private helper | Other / internal logic |  |
| 270 | `parse_string`  |  | Private helper | Other / internal logic |  |
| 281 | `parse_path`  |  | Private helper | Other / internal logic |  |
| 301 | `parse_bool`  |  | Private helper | Other / internal logic |  |
| 311 | `contains_impl_trait`  |  | Private helper | Other / internal logic |  |
| 340 | `build_config`  |  | Private helper | Constructor |  |
| 440 | `parse_knobs`  |  | Private helper | Other / internal logic |  |
| 577 | `token_stream_with_error`  |  | Private helper | Other / internal logic |  |
| 582 | `main`  |  | Crate-internal | Other / internal logic |  |
| 610 | `is_test_attribute`  |  | Private helper | Accessor / query |  |
| 635 | `test`  |  | Crate-internal | Other / internal logic |  |
| 669 | `attrs`  | `ItemFn` | Private helper | Other / internal logic | Access all attributes of the function item. |
| 675 | `body`  | `ItemFn` | Private helper | Other / internal logic | Get the body of the function item in a manner so that it can be conveniently used with the `quote!` macro. |
| 683 | `into_tokens`  | `ItemFn` | Private helper | Conversion | Convert our local function item into a token stream. |
| 720 | `parse`  | `Parse for ItemFn` | Trait impl | Other / internal logic |  |
| 774 | `to_tokens`  | `ToTokens for Body<'_>` | Trait impl | Conversion |  |

## `tokio-macros/src/lib.rs` (8)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 314 | `main`  |  | Public API | Other / internal logic | Marks async function to be executed by the selected runtime. |
| 378 | `main_rt`  |  | Public API | Other / internal logic | Marks async function to be executed by selected runtime. |
| 607 | `test`  |  | Public API | Other / internal logic | Marks async function to be executed by runtime, suitable to test environment. |
| 622 | `test_rt`  |  | Public API | Other / internal logic | Marks async function to be executed by runtime, suitable to test environment ## Usage #[tokio::test] async fn my_test() { assert!(true); } |
| 631 | `main_fail`  |  | Public API | Other / internal logic | Always fails with the error message below. |
| 645 | `test_fail`  |  | Public API | Other / internal logic | Always fails with the error message below. |
| 658 | `select_priv_declare_output_enum`  |  | Public API | Other / internal logic | Implementation detail of the `select!` macro. |
| 666 | `select_priv_clean_pattern`  |  | Public API | Other / internal logic | Implementation detail of the `select!` macro. |

## `tokio-macros/src/select.rs` (3)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 6 | `declare_output_enum`  |  | Crate-internal | Other / internal logic |  |
| 45 | `clean_pattern_macro`  |  | Crate-internal | Other / internal logic |  |
| 59 | `clean_pattern`  |  | Private helper | Other / internal logic |  |

