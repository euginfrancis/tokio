"""Fill the <!-- FILES:key --> / <!-- TESTS:key --> markers in learning/core/**/*.md and
write learning/core/core_stats.json (LOC per component).

Usage (from the repo root):  python3 learning/core/core_stats.py

Re-running replaces previously generated blocks (delimited by `<!-- /KIND -->`).
Counting rules are the same as learning/loc.py (via components/block_stats.count).
"""
import csv, glob, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "components"))
from block_stats import count  # noqa: E402

R = "tokio/src/runtime/"
S = R + "scheduler/"
MT = S + "multi_thread/"
T = "tokio/tests/"

# key -> (source files, test files)
MAP = {
    # ---- task ----
    "t_state":   ([R + "task/state.rs"], [R + "tests/task.rs", R + "tests/task_combinations.rs", T + "task_abort.rs", T + "task_join_set.rs"]),
    "t_cell":    ([R + "task/core.rs"], [R + "tests/task.rs"]),
    "t_raw":     ([R + "task/raw.rs"], [R + "tests/task.rs"]),
    "t_harness": ([R + "task/harness.rs"], [R + "tests/task.rs", R + "tests/task_combinations.rs"]),
    "t_handles": ([R + "task/mod.rs"], [R + "tests/task.rs", R + "tests/task_combinations.rs"]),
    "t_waker":   ([R + "task/waker.rs"], [R + "tests/task.rs"]),
    "t_join":    ([R + "task/join.rs", R + "task/abort.rs", R + "task/error.rs"], [T + "task_abort.rs", T + "task_join_set.rs", T + "task_panic.rs"]),
    "t_owned":   ([R + "task/list.rs", "tokio/src/util/linked_list.rs", "tokio/src/util/sharded_list.rs"], [R + "tests/task.rs", R + "tests/loom_local.rs"]),
    "t_idhooks": ([R + "task/id.rs", R + "task_hooks.rs"], [T + "task_id.rs", T + "task_hooks.rs"]),
    "t_coop":    (["tokio/src/task/coop/mod.rs", "tokio/src/task/coop/consume_budget.rs", "tokio/src/task/coop/unconstrained.rs"], [T + "coop_budget.rs", T + "task_yield_now.rs"]),
    # ---- scheduler ----
    "s_runtime": ([R + "runtime.rs", R + "handle.rs", R + "builder.rs", R + "config.rs"], [T + "rt_basic.rs", T + "rt_common.rs", T + "rt_handle.rs"]),
    "s_context": ([R + "context.rs"] + sorted(glob.glob(R + "context/*.rs")), [T + "rt_common.rs", T + "rt_worker_index.rs"]),
    "s_current": ([S + "current_thread/mod.rs"], [R + "tests/loom_current_thread.rs", T + "rt_basic.rs", T + "rt_common.rs"]),
    "s_mt_state": ([MT + "mod.rs", MT + "handle.rs", S + "mod.rs"], [T + "rt_threaded.rs", R + "tests/loom_multi_thread.rs"]),
    "s_worker":  ([MT + "worker.rs"], [T + "rt_threaded.rs", R + "tests/loom_multi_thread.rs", T + "rt_busy_tick.rs"]),
    "s_queue":   ([MT + "queue.rs", MT + "overflow.rs"], [R + "tests/queue.rs", R + "tests/loom_multi_thread/queue.rs"]),
    "inject":    ([S + "inject.rs"] + sorted(glob.glob(S + "inject/*.rs")), [R + "tests/inject.rs", R + "tests/loom_multi_thread.rs"]),
    "idle":      ([MT + "idle.rs"], [T + "rt_threaded.rs", R + "tests/loom_multi_thread.rs"]),
    "park":      ([MT + "park.rs", "tokio/src/util/try_lock.rs"], [T + "rt_threaded.rs", R + "tests/loom_multi_thread.rs"]),
    "stats":     ([MT + "stats.rs"] + sorted(glob.glob(R + "metrics/*.rs")), [T + "rt_metrics.rs", T + "rt_unstable_metrics.rs"]),
    "block_in_place": ([MT + "worker.rs", R + "context/runtime_mt.rs", "tokio/src/task/blocking.rs"], [T + "rt_threaded.rs", T + "task_blocking.rs", R + "tests/loom_multi_thread.rs"]),
    "defer":     ([S + "defer.rs", "tokio/src/task/yield_now.rs"], [T + "task_yield_now.rs", T + "coop_budget.rs", R + "tests/loom_multi_thread/yield_now.rs"]),
    "shutdown":  ([R + "runtime.rs", MT + "worker.rs", R + "blocking/pool.rs"], [T + "rt_threaded.rs", T + "rt_common.rs", R + "tests/loom_multi_thread/shutdown.rs", R + "tests/task_combinations.rs"]),
    "driver":    ([R + "driver.rs", R + "park.rs", R + "io/driver.rs", R + "signal/mod.rs", R + "process.rs", R + "time/mod.rs"], [T + "rt_common.rs", R + "tests/loom_current_thread.rs"]),
}

TEST_RE = re.compile(r"#\[(?:tokio::)?test\b|#\[cfg_attr\([^\]]*tokio::test")


def read_fns():
    rows = list(csv.DictReader(open("learning/functions/functions.csv")))
    by_file = {}
    for r in rows:
        by_file[r["file"]] = by_file.get(r["file"], 0) + 1
    return by_file


def stats():
    fns = read_fns()
    out = {}
    for key, (src, tests) in MAP.items():
        for f in src + tests:
            if not os.path.exists(f):
                sys.exit(f"missing file for {key}: {f}")
        rows = []
        for f in src:
            c, cm, d, b = count(f)
            rows.append({"file": f, "code": c, "doc": d + cm, "fns": fns.get(f, 0),
                         "inline_tests": len(TEST_RE.findall(open(f).read()))})
        trows = []
        for f in tests:
            c = count(f)[0]
            trows.append({"file": f, "code": c, "tests": len(TEST_RE.findall(open(f).read()))})
        out[key] = {"src": rows, "tests": trows}
    return out


def link(path, depth):
    return f"[`{path}`]({'../' * depth}{path})"


def render_files(key, v, depth):
    rows = v["src"]
    tot = sum(r["code"] for r in rows)
    out = ["| File | Code | Docs+comments | Functions |", "|---|---:|---:|---:|"]
    for r in rows:
        out.append(f"| {link(r['file'], depth)} | {r['code']:,} | {r['doc']:,} | {r['fns']} |")
    if len(rows) > 1:
        out.append(f"| **Total ({len(rows)} files)** | **{tot:,}** | **{sum(r['doc'] for r in rows):,}** | **{sum(r['fns'] for r in rows)}** |")
    return "\n".join(out)


def render_tests(key, v, depth):
    inline = sum(r["inline_tests"] for r in v["src"])
    out = ["| Test file | Test fns | Code lines |", "|---|---:|---:|"]
    for r in v["tests"]:
        out.append(f"| {link(r['file'], depth)} | {r['tests']} | {r['code']:,} |")
    out.append(f"| *inline `#[test]` in the source files above* | {inline} | – |")
    out.append("")
    out.append("_Shared files (e.g. `rt_threaded.rs`) test several components; counts are for the whole file._")
    return "\n".join(out)


RENDER = {"FILES": render_files, "TESTS": render_tests}


def fill(st):
    for path in glob.glob("learning/core/**/*.md", recursive=True):
        text = open(path).read()
        depth = path.count("/")  # learning/core/x/f.md -> 3 levels up to repo root
        text = re.sub(r"(<!-- (FILES|TESTS):\w+ -->)\n.*?\n<!-- /\2 -->", r"\1", text, flags=re.S)

        def sub(m):
            kind, key = m.group(1), m.group(2)
            if key not in st:
                sys.exit(f"{path}: unknown key {kind}:{key}")
            return f"<!-- {kind}:{key} -->\n{RENDER[kind](key, st[key], depth)}\n<!-- /{kind} -->"

        new = re.sub(r"<!-- (FILES|TESTS):(\w+) -->", sub, text)
        if new != text:
            open(path, "w").write(new)


if __name__ == "__main__":
    st = stats()
    json.dump(st, open("learning/core/core_stats.json", "w"), indent=1)
    fill(st)
    tot = {k: sum(r["code"] for r in v["src"]) for k, v in st.items()}
    for k, n in tot.items():
        print(f"{k:16} {n:6}")
