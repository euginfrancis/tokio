# Learning Tokio — study notes

Personal learning material for `tokio-rs/tokio` (snapshot `8667843`). Not part of upstream Tokio; keep this folder off any branch you open a PR from.

| File | What it is |
|---|---|
| [`TOKIO_FUNCTIONAL_GUIDE.md`](./TOKIO_FUNCTIONAL_GUIDE.md) | **Start here.** What Tokio does, every feature area, how the components connect, the main flows (program, task, scheduling, I/O, timers, channels, blocking, cancellation, shutdown), rules, pitfalls and a cheat sheet |
| [`TOKIO_ANALYSIS.md`](./TOKIO_ANALYSIS.md) | Codebase statistics: files, LOC, crates, modules, percentages, architecture overview, contribution workflow |
| [`HOW_TOKIO_WORKS.md`](./HOW_TOKIO_WORKS.md) | **Then this, for internals.** Function-by-function walkthrough in execution order: startup, spawn, task state, worker loop, parking, waking, I/O, timers, coop, sync, blocking, `select!`, shutdown, and an end-to-end request trace |
| [`functions/`](./functions/README.md) | Index of all 5,480 functions, categorized by component, kind (public / internal / trait impl / test) and role, with each function's doc summary. `functions.csv` has the raw data |
| [`DSA_IN_TOKIO.md`](./DSA_IN_TOKIO.md) | 19 data structures + 22 algorithms used in the codebase, with complexity and file references |
| [`dsa-exercises/`](./dsa-exercises) | Runnable safe-Rust mini versions (timer wheel, work-stealing queue, task state, fair semaphore, PRNG, EWMA) — `cargo test` |
| [`loc.py`](./loc.py), [`fn_index.py`](./fn_index.py) | Scripts that regenerate the statistics and the function index |

Regenerate after pulling upstream:
```bash
python3 learning/loc.py . /tmp/rows.json
python3 learning/fn_index.py . learning/functions
```
