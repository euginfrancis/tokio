# `tokio::runtime::metrics::histogram` — 26 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Test | 10 |
| Public API | 8 |
| Trait impl | 3 |
| Private helper | 3 |
| Crate-internal | 2 |

## `tokio/src/runtime/metrics/histogram/h2_histogram.rs` (26)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 41 | `default`  | `Default for LogHistogram` | Trait impl | Constructor |  |
| 51 | `from_n_p`  | `LogHistogram` | Private helper | Conversion | Create a Histogram configuration directly from values for `n` and `p`. |
| 61 | `truncate_to_max_value`  | `LogHistogram` | Private helper | Other / internal logic |  |
| 71 | `builder`  | `LogHistogram` | Public API | Constructor | Creates a builder for [`LogHistogram`] |
| 76 | `max_value`  | `LogHistogram` | Public API | Configuration / setter | The maximum value that can be stored before truncation in this histogram |
| 80 | `value_to_bucket`  | `LogHistogram` | Crate-internal | Other / internal logic |  |
| 87 | `bucket_range`  | `LogHistogram` | Crate-internal | Other / internal logic |  |
| 151 | `from`  | `From<LogHistogramBuilder> for LogHistogram` | Trait impl | Conversion |  |
| 175 | `max_error`  | `LogHistogramBuilder` | Public API | Configuration / setter | Set the precision for this histogram This function determines the smallest value of `p` that would satisfy the requested precision such that `2^-p` is less than `precision`. |
| 200 | `precision_exact`  | `LogHistogramBuilder` | Public API | Other / internal logic | Sets the precision of this histogram directly. |
| 211 | `min_value`  | `LogHistogramBuilder` | Public API | Other / internal logic | Sets the minimum duration that can be accurately stored by this histogram. |
| 222 | `max_value`  | `LogHistogramBuilder` | Public API | Configuration / setter | Sets the maximum value that can by this histogram without truncation Values greater than this fall in the final bucket that stretches to `u64::MAX`. |
| 231 | `max_buckets`  | `LogHistogramBuilder` | Public API | Configuration / setter | Builds the log histogram, enforcing the max buckets requirement |
| 245 | `build`  | `LogHistogramBuilder` | Public API | Constructor | Builds the log histogram |
| 271 | `fmt`  | `Display for InvalidHistogramConfiguration` | Trait impl | Formatting |  |
| 284 | `bucket_index`  |  | Private helper | Other / internal logic | Compute the index for a given value + p combination This function does NOT enforce that the value is within the number of expected buckets. |
| 313 | `valid_log_histogram_strategy`  |  | Test | Other / internal logic |  |
| 321 | `log_histogram_settings`  |  | Test | Other / internal logic |  |
| 332 | `log_histogram_settings_maintain_invariants`  |  | Test | Other / internal logic |  |
| 358 | `proptest_log_histogram_invariants`  |  | Test | Other / internal logic |  |
| 420 | `bucket_ranges_are_correct`  |  | Test | Other / internal logic |  |
| 451 | `bucket_computation_spot_check`  |  | Test | Other / internal logic |  |
| 487 | `last_bucket_goes_to_infinity`  |  | Test | Other / internal logic |  |
| 493 | `bucket_offset`  |  | Test | Other / internal logic |  |
| 508 | `max_buckets_enforcement`  |  | Test | Configuration / setter |  |
| 522 | `default_configuration_size`  |  | Test | Other / internal logic |  |

