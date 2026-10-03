"""Per-block file/LOC/function/test statistics for learning/components/*.md.

Usage: python3 learning/components/block_stats.py  (from the repo root)
"""
import csv, fnmatch, json, os, subprocess, sys


BLOCKS = {
    "tasks": {
        "src": ["tokio/src/task/*", "tokio/src/runtime/task/*"],
        "tests": ["tokio/tests/task_*", "tokio/tests/coop_*", "tokio/tests/async_send_sync.rs"],
    },
    "time": {
        "src": ["tokio/src/time/*"],
        "tests": ["tokio/tests/time_*"],
    },
    "net_io": {
        "src": ["tokio/src/net/*", "tokio/src/io/*"],
        "tests": ["tokio/tests/io_*", "tokio/tests/net_*", "tokio/tests/tcp_*", "tokio/tests/udp*", "tokio/tests/uds_*", "tokio/tests/buffered.rs", "tokio/tests/duplex_stream.rs", "tokio/tests/unix_*"],
    },
    "sync": {
        "src": ["tokio/src/sync/*"],
        "tests": ["tokio/tests/sync_*"],
    },
    "fs_process_signal": {
        "src": ["tokio/src/fs/*", "tokio/src/process/*", "tokio/src/signal/*"],
        "tests": ["tokio/tests/fs*", "tokio/tests/process_*", "tokio/tests/signal_*"],
    },
    "scheduler": {
        "src": ["tokio/src/runtime/scheduler/*", "tokio/src/runtime/context/*", "tokio/src/runtime/metrics/*",
                "tokio/src/runtime/local_runtime/*", "tokio/src/runtime/tests/*",
                "tokio/src/runtime/builder.rs", "tokio/src/runtime/config.rs", "tokio/src/runtime/context.rs",
                "tokio/src/runtime/driver.rs", "tokio/src/runtime/driver/*", "tokio/src/runtime/dump.rs",
                "tokio/src/runtime/handle.rs", "tokio/src/runtime/id.rs", "tokio/src/runtime/jspi.rs",
                "tokio/src/runtime/mod.rs", "tokio/src/runtime/park.rs", "tokio/src/runtime/runtime.rs",
                "tokio/src/runtime/task_hooks.rs", "tokio/src/runtime/thread_id.rs"],
        "tests": ["tokio/tests/rt_*"],
    },
    "timer_driver": {
        "src": ["tokio/src/runtime/time/*", "tokio/src/runtime/time_alt/*"],
        "tests": [],
    },
    "io_driver": {
        "src": ["tokio/src/runtime/io/*", "tokio/src/runtime/signal/*", "tokio/src/runtime/process.rs"],
        "tests": [],
    },
    "blocking_pool": {
        "src": ["tokio/src/runtime/blocking/*", "tokio/src/blocking.rs"],
        "tests": [],
    },
}


def count(path):
    """Same rules as learning/loc.py: code / `//` comments / doc comments / blank."""
    code = com = doc = blank = 0
    in_block = False
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if in_block:
            com += 1
            in_block = "*/" not in s
        elif not s:
            blank += 1
        elif s.startswith(("///", "//!")):
            doc += 1
        elif s.startswith("//"):
            com += 1
        elif s.startswith("/*"):
            com += 1
            in_block = "*/" not in s
        else:
            code += 1
    return code, com, doc, blank


def main():
    files = subprocess.run(["git", "ls-files", "*.rs"], capture_output=True, text=True).stdout.split()
    fns = list(csv.DictReader(open("learning/functions/functions.csv")))
    out = {}
    for name, spec in BLOCKS.items():
        src = sorted(f for f in files if any(fnmatch.fnmatch(f, g) for g in spec["src"]))
        tests = sorted(f for f in files if any(fnmatch.fnmatch(f, g) for g in spec["tests"]))
        rows = []
        for f in src:
            c, cm, d, b = count(f)
            rows.append({"file": f, "code": c, "comment": cm, "doc": d, "blank": b})
        tcode = sum(count(f)[0] for f in tests)
        tcount = 0
        for f in tests:
            tcount += sum(1 for l in open(f) if l.strip().startswith(("#[test]", "#[tokio::test", "#[cfg_attr(miri, ignore)]#[tokio::test")))
        bf = [r for r in fns if r["file"] in set(src)]
        kinds = {}
        for r in bf:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
        unsafe_lines = sum(open(f).read().count("unsafe ") for f in src)
        out[name] = {
            "files": rows,
            "n_files": len(rows),
            "code": sum(r["code"] for r in rows),
            "doc": sum(r["doc"] + r["comment"] for r in rows),
            "test_files": tests,
            "test_code": tcode,
            "test_fns": tcount,
            "functions": len(bf),
            "kinds": kinds,
            "async_fns": sum(r["async"] == "True" for r in bf),
            "unsafe_fns": sum(r["unsafe"] == "True" for r in bf),
            "unsafe_mentions": unsafe_lines,
        }
    json.dump(out, open("learning/components/block_stats.json", "w"), indent=1)
    total = sum(v["code"] for v in out.values())
    for k, v in out.items():
        print(f"{k:18} files={v['n_files']:4} code={v['code']:6} ({100*v['code']/total:4.1f}%) doc={v['doc']:6} fns={v['functions']:5} "
              f"tests={len(v['test_files']):3} files/{v['test_fns']:4} fns/{v['test_code']:6} loc unsafe={v['unsafe_mentions']}")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Fill the <!-- STATS:x --> / <!-- FILES:x --> / <!-- TESTS:x --> markers in
# learning/components/*.md. Re-running replaces the previous generated block.
# ---------------------------------------------------------------------------
import glob
import re

TOKIO_SRC_CODE = None


def link(path):
    return f"[`{path}`](../../{path})"


def render_stats(name, v):
    global TOKIO_SRC_CODE
    if TOKIO_SRC_CODE is None:
        files = subprocess.run(["git", "ls-files", "tokio/src/*.rs"], capture_output=True, text=True).stdout.split()
        TOKIO_SRC_CODE = sum(count(f)[0] for f in files)
    share = 100 * v["code"] / TOKIO_SRC_CODE if all(r["file"].startswith("tokio/src") for r in v["files"]) else None
    k = v["kinds"]
    internal = k.get("Crate-internal", 0) + k.get("Private helper", 0)
    rows = [
        ("Source files", f"{v['n_files']}"),
        ("Code lines", f"{v['code']:,}" + (f" ({share:.1f}% of `tokio/src`)" if share else "")),
        ("Doc + comment lines", f"{v['doc']:,} ({v['doc'] / max(v['code'], 1):.2f} per code line)"),
        ("Functions", f"{v['functions']:,} — public API {k.get('Public API', 0)}, trait impls {k.get('Trait impl', 0)}, "
                      f"internal {internal}, inline tests {k.get('Test', 0)}"),
        ("`async fn` / `unsafe fn`", f"{v['async_fns']} / {v['unsafe_fns']}"),
        ("`unsafe` occurrences", f"{v['unsafe_mentions']}"),
        ("Integration tests (`tokio/tests`)", f"{len(v['test_files'])} files, {v['test_fns']} test fns, {v['test_code']:,} code lines"
                                               if v["test_files"] else "none dedicated — exercised through other blocks' tests"),
    ]
    out = ["| Metric | Value |", "|---|---|"] + [f"| {a} | {b} |" for a, b in rows]
    return "\n".join(out)


def render_files(name, v, limit=30):
    rows = sorted(v["files"], key=lambda r: -r["code"])
    out = ["| File | Code | Docs+comments | % of block |", "|---|---:|---:|---:|"]
    for r in rows[:limit]:
        out.append(f"| {link(r['file'])} | {r['code']:,} | {r['doc'] + r['comment']:,} | {100 * r['code'] / max(v['code'], 1):.1f}% |")
    if len(rows) > limit:
        rest = rows[limit:]
        out.append(f"| *…{len(rest)} smaller files* | {sum(r['code'] for r in rest):,} | "
                   f"{sum(r['doc'] + r['comment'] for r in rest):,} | {100 * sum(r['code'] for r in rest) / v['code']:.1f}% |")
    out.append(f"| **Total ({len(rows)} files)** | **{v['code']:,}** | **{v['doc']:,}** | 100% |")
    return "\n".join(out)


def render_tests(name, v, limit=20):
    if not v["test_files"]:
        return "_No integration test files are dedicated to this block._"
    out = [f"**{len(v['test_files'])} integration test files · {v['test_fns']} test functions · {v['test_code']:,} code lines**", ""]
    names = [f"[`{f.split('/')[-1]}`](../../{f})" for f in v["test_files"]]
    out.append(", ".join(names[:limit]) + (f", … (+{len(names) - limit} more)" if len(names) > limit else ""))
    return "\n".join(out)


def fill_docs(stats):
    renderers = {"STATS": render_stats, "FILES": render_files, "TESTS": render_tests}
    pat = re.compile(r"<!-- (STATS|FILES|TESTS):(\w+) -->.*?(?:<!-- /\1 -->)?(?=\n)", re.S)
    for path in glob.glob("learning/components/0*.md"):
        text = open(path).read()

        def sub(m):
            kind, name = m.group(1), m.group(2)
            return f"<!-- {kind}:{name} -->\n{renderers[kind](name, stats[name])}\n<!-- /{kind} -->"

        # Remove previously generated content, then regenerate.
        text = re.sub(r"(<!-- (STATS|FILES|TESTS):\w+ -->)\n.*?\n<!-- /\2 -->", r"\1", text, flags=re.S)
        text = pat.sub(sub, text)
        open(path, "w").write(text)


if __name__ == "__main__":
    fill_docs(json.load(open("learning/components/block_stats.json")))
