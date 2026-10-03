"""Build a categorized index of every function in the Tokio workspace.

Usage: python3 learning/fn_index.py <repo-root> <out-dir>

A lightweight Rust scanner (not a full parser): it strips comments/strings,
tracks brace depth to know which `impl`/`trait`/`mod` a function lives in,
and classifies each function by component, kind and role.
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

CRATES = ["tokio", "tokio-util", "tokio-stream", "tokio-macros", "tokio-test"]

FN_RE = re.compile(
    r"^\s*(?P<vis>pub(?:\s*\([^)]*\))?\s+)?(?P<quals>(?:(?:const|async|unsafe|extern\s+\"[^\"]*\")\s+)*)fn\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
)
IMPL_RE = re.compile(r"^\s*(?:unsafe\s+)?impl\b")
TRAIT_RE = re.compile(r"^\s*(?:pub(?:\s*\([^)]*\))?\s+)?(?:unsafe\s+)?trait\s+([A-Za-z_][A-Za-z0-9_]*)")
MOD_RE = re.compile(r"^\s*(?:pub(?:\s*\([^)]*\))?\s+)?mod\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{")
MACRO_RULES_RE = re.compile(r"^\s*macro_rules!\s*([A-Za-z_][A-Za-z0-9_]*)")


def strip_code(text):
    """Blank out comments, strings and char literals but keep newlines/columns."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":
            j = text.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
        elif c == "/" and nxt == "*":
            depth, j = 1, i + 2
            while j < n and depth:
                if text.startswith("/*", j):
                    depth += 1
                    j += 2
                elif text.startswith("*/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            out.append("".join(ch if ch == "\n" else " " for ch in text[i:j]))
            i = j
        elif c == "r" and re.match(r'r#*"', text[i:i + 10]) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")):
            m = re.match(r'r(#*)"', text[i:])
            hashes = m.group(1)
            end = text.find('"' + hashes, i + len(m.group(0)))
            end = n if end == -1 else end + 1 + len(hashes)
            out.append("".join(ch if ch == "\n" else " " for ch in text[i:end]))
            i = end
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            j += 1
            out.append('"' + "".join(ch if ch == "\n" else " " for ch in text[i + 1:j - 1]) + '"')
            i = j
        elif c == "'":
            # char literal like 'a' or '\n' (not lifetimes like 'a or 'static)
            m = re.match(r"'(\\.|\\u\{[0-9a-fA-F]+\}|[^\\'])'", text[i:])
            if m:
                out.append(" " * len(m.group(0)))
                i += len(m.group(0))
            else:
                out.append(c)
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def component_of(crate, rel):
    """`tokio/src/runtime/scheduler/multi_thread/worker.rs` -> `runtime::scheduler::multi_thread`."""
    parts = rel.split("/")[2:]  # drop "<crate>/src"
    if len(parts) == 1:
        return f"{crate} (crate root)"
    dirs = parts[:-1]
    # Keep at most three levels so components stay meaningful but not too fine.
    return f"{crate}::" + "::".join(dirs[:3])


TRAIT_ROLES = {
    "Future": "Future impl (poll)",
    "Stream": "Stream impl",
    "AsyncRead": "I/O trait impl",
    "AsyncWrite": "I/O trait impl",
    "AsyncBufRead": "I/O trait impl",
    "AsyncSeek": "I/O trait impl",
    "Drop": "Drop / cleanup",
    "Debug": "Formatting",
    "Display": "Formatting",
    "Clone": "Clone",
    "Default": "Constructor",
    "From": "Conversion",
    "TryFrom": "Conversion",
    "AsRawFd": "OS handle access",
    "AsFd": "OS handle access",
    "AsRawSocket": "OS handle access",
    "AsSocket": "OS handle access",
    "AsRawHandle": "OS handle access",
    "AsHandle": "OS handle access",
    "Error": "Error type",
    "Decoder": "Codec impl",
    "Encoder": "Codec impl",
    "Link": "Intrusive-list link",
    "Schedule": "Scheduler hook",
    "Wake": "Waker",
    "Iterator": "Iterator",
    "Deref": "Deref",
    "DerefMut": "Deref",
    "PartialEq": "Comparison",
    "Eq": "Comparison",
    "PartialOrd": "Comparison",
    "Ord": "Comparison",
    "Hash": "Comparison",
    "Sink": "Sink impl",
}


def role_of(name, trait, quals, sig):
    if trait:
        base = trait.split("<")[0].split("::")[-1].strip()
        if base in TRAIT_ROLES:
            return TRAIT_ROLES[base]
    if name in ("new", "default", "builder", "build") or name.startswith(("new_", "with_", "build_")):
        return "Constructor"
    if name.startswith(("from_", "into_", "to_", "as_")) or name in ("into_inner", "into_std"):
        return "Conversion"
    if name.startswith("poll_") or name == "poll":
        return "Poll function"
    if name.startswith("transition_") or name.startswith("set_") and "state" in sig:
        return "State transition"
    if name.startswith(("try_", "spawn", "block_on", "enter", "shutdown")):
        return {"try_": "Non-blocking attempt"}.get(name[:4], "Runtime/task control")
    if name.startswith(("is_", "has_", "len", "get_", "num_", "capacity")) or name in ("get", "len", "is_empty", "id", "metrics"):
        return "Accessor / query"
    if name.startswith(("wake", "notify", "unpark", "park")):
        return "Wake / park"
    if name.startswith(("lock", "unlock", "acquire", "release", "add_permits", "forget")):
        return "Locking / permits"
    if name.startswith(("send", "recv", "receive", "subscribe", "broadcast", "push", "pop", "insert", "remove", "steal", "take", "close")):
        return "Data movement"
    if name.startswith(("read", "write", "flush", "copy", "fill_buf", "consume", "seek")):
        return "I/O operation"
    if name.startswith(("register", "deregister", "clear_readiness", "ready", "readiness")):
        return "I/O registration"
    if name.startswith(("ref_", "dealloc", "drop_", "cancel", "abort")):
        return "Lifecycle / ref-count"
    if name.startswith(("fmt",)):
        return "Formatting"
    if name.startswith(("set_", "unset_", "enable", "disable", "on_thread", "on_task", "max_", "thread_", "event_interval", "global_queue_interval")) or name in ("set", "store", "reset", "clear", "seed"):
        return "Configuration / setter"
    if name.startswith(("inc_", "incr_", "dec_", "submit", "metrics_", "worker_", "injection_queue", "blocking_queue")) or name.endswith(("_count", "_depth")):
        return "Metrics / counters"
    if name.startswith(("local_addr", "peer_addr", "bind", "connect", "accept", "listen", "socket", "ttl", "nodelay", "linger", "multicast", "broadcast", "join_multicast", "leave_multicast", "shutdown_std")) or name in ("addr",):
        return "Networking"
    if name in ("now", "elapsed", "deadline", "timeout", "sleep", "sleep_until", "interval", "interval_at") or name.startswith(("next_expiration", "level_for", "slot_for", "process_expiration", "reset_at", "tick")):
        return "Time / timers"
    if name in ("initialize", "finalize", "complete", "complete_with_error", "run", "start", "wait", "schedule", "defer", "kill", "begin_shutdown") or name.startswith(("run_", "schedule_", "complete", "finalize", "wait_", "process_", "check_", "start_")):
        return "Runtime/task control"
    if name in ("map", "split", "reunite", "chain", "merge", "extend", "iter", "peek", "next", "drain", "for_each", "project", "borrow", "with") or name.startswith(("map_", "split", "iter_", "peek", "drain", "borrow", "filter", "fold", "chunks", "skip", "take_while")):
        return "Combinator / iteration"
    if name in ("downgrade", "upgrade", "strong_count", "weak_count", "same_channel", "ptr_eq", "clone_inner", "header", "handle", "current", "inner", "token", "semaphore") or name.startswith(("addr_of", "header_", "ptr_")):
        return "Handle / reference plumbing"
    if name.startswith(("const_new", "channel", "create", "open", "unbounded_channel", "pair")):
        return "Constructor"
    if name.startswith(("trace", "assert", "debug_", "dump")):
        return "Debugging / tracing"
    if name.startswith(("blocking_",)):
        return "Blocking (sync) variant"
    if "async" in quals:
        return "Async operation"
    return "Other / internal logic"


def kind_of(vis, in_test, in_trait_def, trait_impl, file_rel, macro):
    if in_test or "/tests/" in file_rel or file_rel.endswith(("/tests.rs", "_test.rs")):
        return "Test"
    if macro:
        return "Inside macro_rules!"
    if in_trait_def:
        return "Trait method (declaration/default)"
    if trait_impl:
        return "Trait impl"
    v = (vis or "").replace(" ", "")
    if v == "pub":
        return "Public API"
    if v.startswith("pub("):
        return "Crate-internal"
    return "Private helper"


def doc_summary(lines, idx):
    """First sentence of the `///` doc block above line idx (0-based)."""
    docs = []
    j = idx - 1
    while j >= 0:
        s = lines[j].strip()
        if s.startswith("///"):
            docs.append(s[3:].strip())
        elif s.startswith("#[") or s.startswith("#!") or s == "" and docs == []:
            if s == "" and docs == []:
                break
        else:
            break
        j -= 1
    docs.reverse()
    text = " ".join(d for d in docs if d and not d.startswith("```"))
    text = text.split(" # ")[0]
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    s = (m.group(1) if m else text).strip()
    return s[:200]


def scan_file(path, crate, rel):
    raw = open(path, encoding="utf-8", errors="replace").read()
    lines = raw.split("\n")
    code = strip_code(raw).split("\n")
    rows = []
    depth = 0
    # stack of (depth_at_open, kind, label, is_test)
    stack = []
    pending = None  # (kind, label, is_test) waiting for "{"
    header = ""
    cfg_test_next = False
    for i, line in enumerate(code):
        s = line.strip()
        if re.match(r"#\[cfg\((all\()?test", s) or s.startswith("#[cfg(all(test") or s == "#[cfg(test)]":
            cfg_test_next = True
        in_test = any(t for (_, _, _, t) in stack)
        in_macro = any(k == "macro" for (_, k, _, _) in stack)
        if pending is None:
            if IMPL_RE.match(line):
                pending = ["impl", None, False]
                header = ""
            elif TRAIT_RE.match(line):
                pending = ["trait", TRAIT_RE.match(line).group(1), False]
                header = ""
            elif MACRO_RULES_RE.match(line):
                pending = ["macro", MACRO_RULES_RE.match(line).group(1), False]
                header = ""
            elif MOD_RE.match(line):
                pending = ["mod", MOD_RE.match(line).group(1), cfg_test_next]
                header = ""
        m = FN_RE.match(line)
        if m:
            ctx_impl = next((lbl for (_, k, lbl, _) in reversed(stack) if k == "impl"), None)
            ctx_trait = next((lbl for (_, k, lbl, _) in reversed(stack) if k == "trait"), None)
            # Is the nearest enclosing item a trait definition?
            nearest = next(((k, lbl) for (_, k, lbl, _) in reversed(stack) if k in ("impl", "trait", "fn")), None)
            trait_impl = None
            self_ty = None
            if nearest and nearest[0] == "impl" and nearest[1]:
                h = nearest[1]
                if " for " in h:
                    trait_impl, self_ty = h.split(" for ", 1)
                else:
                    self_ty = h
            sig = line.strip()
            k = i
            while "{" not in code[k] and ";" not in code[k] and k + 1 < len(code) and k - i < 15:
                k += 1
                sig += " " + code[k].strip()
            quals = m.group("quals") or ""
            name = m.group("name")
            kind = kind_of(m.group("vis"), in_test or cfg_test_next, nearest is not None and nearest[0] == "trait", trait_impl, rel, in_macro)
            owner = (self_ty or (ctx_trait and f"trait {ctx_trait}") or "").strip()
            owner = re.sub(r"\s+", " ", owner)
            trait_clean = re.sub(r"\s+", " ", trait_impl.strip()) if trait_impl else ""
            rows.append({
                "crate": crate,
                "component": component_of(crate, rel),
                "file": rel,
                "line": i + 1,
                "function": name,
                "owner": owner[:80],
                "trait": trait_clean[:60],
                "kind": kind,
                "role": role_of(name, trait_clean, quals, sig),
                "async": "async" in quals,
                "unsafe": "unsafe" in quals,
                "const": "const" in quals,
                "doc": doc_summary(lines, i),
            })
            # Track fn bodies so nested items know their parent.
            if "{" in sig and not sig.rstrip().endswith(";"):
                pending = ["fn", name, False]
                header = ""
        if pending is not None:
            header += " " + line.strip()
        for ch in line:
            if ch == "{":
                depth += 1
                if pending is not None:
                    kind_p, label, is_test = pending
                    if kind_p == "impl":
                        h = header.split("{")[0]
                        h = re.sub(r"^\s*(unsafe\s+)?impl\s*", "", h)
                        h = re.sub(r"\s+where\s+.*$", "", h)
                        # drop leading generics impl<...>
                        if h.startswith("<"):
                            lvl = 0
                            for idx, c2 in enumerate(h):
                                lvl += c2 == "<"
                                lvl -= c2 == ">"
                                if lvl == 0:
                                    h = h[idx + 1:]
                                    break
                        label = h.strip()
                    stack.append((depth, kind_p, label, is_test or cfg_test_next and kind_p == "mod"))
                    pending = None
                    if kind_p in ("mod",):
                        cfg_test_next = False
            elif ch == "}":
                while stack and stack[-1][0] == depth:
                    stack.pop()
                depth -= 1
            elif ch == ";" and pending is not None and pending[0] in ("fn", "trait", "impl"):
                # e.g. trait method declaration without body
                if pending[0] == "fn":
                    pending = None
        if s and not s.startswith("#[") and not MOD_RE.match(line) and cfg_test_next and not s.startswith("mod"):
            # cfg(test) applied to a non-module item: only that item.
            if FN_RE.match(line) is None:
                cfg_test_next = False
            else:
                cfg_test_next = False
    return rows


def main():
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows = []
    for crate in CRATES:
        base = os.path.join(root, crate, "src")
        for dp, _, files in os.walk(base):
            for f in sorted(files):
                if f.endswith(".rs"):
                    p = os.path.join(dp, f)
                    rows.extend(scan_file(p, crate, os.path.relpath(p, root)))
    rows.sort(key=lambda r: (r["component"], r["file"], r["line"]))

    with open(os.path.join(out, "functions.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_comp = defaultdict(list)
    for r in rows:
        by_comp[r["component"]].append(r)

    def pct(a, b):
        return f"{100 * a / b:.1f}%"

    total = len(rows)
    kinds = Counter(r["kind"] for r in rows)
    roles = Counter(r["role"] for r in rows if r["kind"] != "Test")
    crates = Counter(r["crate"] for r in rows)

    idx = []
    idx.append("# Tokio function index\n")
    idx.append("Every function defined under `*/src` of the Tokio crates, categorized automatically by "
               "[`fn_index.py`](../fn_index.py). For hand-written explanations of the important ones, "
               "read [`../HOW_TOKIO_WORKS.md`](../HOW_TOKIO_WORKS.md).\n")
    idx.append(f"**Total functions: {total:,}** (async: {sum(r['async'] for r in rows)}, "
               f"unsafe: {sum(r['unsafe'] for r in rows)}, const: {sum(r['const'] for r in rows)})\n")
    idx.append("## By crate\n\n| Crate | Functions | % |\n|---|---:|---:|")
    for c, n in crates.most_common():
        idx.append(f"| `{c}` | {n:,} | {pct(n, total)} |")
    idx.append("\n## By kind\n\n| Kind | Functions | % | Meaning |\n|---|---:|---:|---|")
    meaning = {
        "Public API": "`pub fn` — callable by users of the crate (if its module is public)",
        "Trait impl": "Implements a trait for a type (`Future::poll`, `Drop::drop`, `Debug::fmt`, …)",
        "Private helper": "No `pub`: used only inside its own module",
        "Test": "Inside `#[cfg(test)]` modules or test-only files",
        "Trait method (declaration/default)": "Declared inside a `trait { … }` block",
        "Inside macro_rules!": "Function written inside a macro body (generated per use)",
    }
    for k, n in kinds.most_common():
        mean = meaning.get(k, "`pub(crate)` / `pub(super)` / `pub(in path)`: shared between Tokio's own modules, invisible to users" if k == "Crate-internal" else "")
        idx.append(f"| {k} | {n:,} | {pct(n, total)} | {mean} |")
    idx.append("\n## By role (non-test)\n\nRole is guessed from the trait being implemented or the function name.\n\n| Role | Functions | % |\n|---|---:|---:|")
    nt = sum(roles.values())
    for k, n in roles.most_common():
        idx.append(f"| {k} | {n:,} | {pct(n, nt)} |")
    idx.append("\n## By component\n\n| Component | Functions | Public API | Trait impls | Internal | Unsafe | Async | Page |\n|---|---:|---:|---:|---:|---:|---:|---|")
    pages = {}
    for comp, rs in sorted(by_comp.items()):
        fname = re.sub(r"[^A-Za-z0-9]+", "_", comp).strip("_") + ".md"
        pages[comp] = fname
        pub = sum(r["kind"] == "Public API" for r in rs)
        ti = sum(r["kind"] == "Trait impl" for r in rs)
        internal = sum(r["kind"].startswith(("Crate-internal", "Private")) for r in rs)
        idx.append(f"| `{comp}` | {len(rs)} | {pub} | {ti} | {internal} | {sum(r['unsafe'] for r in rs)} | {sum(r['async'] for r in rs)} | [{fname}](./{fname}) |")
    with open(os.path.join(out, "README.md"), "w") as fh:
        fh.write("\n".join(idx) + "\n")

    for comp, rs in by_comp.items():
        doc = [f"# `{comp}` — {len(rs)} functions\n", "[← index](./README.md)\n"]
        doc.append("Flags: 🅰 async · ⚠ unsafe · 🅲 const\n")
        files = defaultdict(list)
        for r in rs:
            files[r["file"]].append(r)
        kc = Counter(r["kind"] for r in rs)
        doc.append("| Kind | Count |\n|---|---:|")
        for k, n in kc.most_common():
            doc.append(f"| {k} | {n} |")
        doc.append("")
        for f, frs in files.items():
            doc.append(f"## `{f}` ({len(frs)})\n")
            doc.append("| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |\n|---:|---|---|---|---|---|")
            for r in frs:
                flags = ("🅰" if r["async"] else "") + ("⚠" if r["unsafe"] else "") + ("🅲" if r["const"] else "")
                on = r["owner"]
                if r["trait"]:
                    on = f"{r['trait']} for {r['owner']}"
                on = on.replace("|", "\\|")
                summ = r["doc"].replace("|", "\\|")
                doc.append(f"| {r['line']} | `{r['function']}` {flags} | {('`' + on + '`') if on else ''} | {r['kind']} | {r['role']} | {summ} |")
            doc.append("")
        with open(os.path.join(out, pages[comp]), "w") as fh:
            fh.write("\n".join(doc) + "\n")
    print(f"{total} functions, {len(by_comp)} components")


if __name__ == "__main__":
    main()
