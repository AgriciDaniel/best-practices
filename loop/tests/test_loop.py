#!/usr/bin/env python3
"""Regression tests for the loop generator. Stdlib only; no framework.

Run:  python3 loop/tests/test_loop.py
Exits non-zero on any failure.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

GEN = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "build_loop.py"
failures = []


def check(name, cond):
    print(("PASS" if cond else "FAIL") + f": {name}")
    if not cond:
        failures.append(name)


def run(args, cwd):
    return subprocess.run([sys.executable, str(GEN), *args], cwd=cwd,
                          capture_output=True, text=True)


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loop_test_"))

    # 1. scaffold
    r = run(["Test goal here", "--dir", str(tmp), "--max-loops", "5"], tmp)
    check("scaffold exits 0", r.returncode == 0)

    notes = sorted(tmp.glob("[0-9][0-9] - *.md"))
    check("exactly 10 checkpoint notes", len(notes) == 10)

    # 2. canvas topology: 10 nodes, 10 ring + 2 feedback edges, ring closes 9->0
    canvas = json.loads((tmp / "Loop.canvas").read_text())
    check("canvas has 11 nodes (10 + core)", len(canvas["nodes"]) == 11)
    check("canvas has 22 edges (10 ring + 10 spokes + 2 feedback)", len(canvas["edges"]) == 22)
    ring_closes = any(e["fromNode"] == "n9" and e["toNode"] == "n0" for e in canvas["edges"])
    check("ring closes 9 -> 0", ring_closes)

    # 3. graph config: filter excludes topics, 10 colorGroups, zero collisions
    graph = json.loads((tmp / ".obsidian" / "graph.json").read_text())
    check("graph filter excludes topics", "-path:topics" in graph["search"])
    files = [p.name for p in tmp.glob("*.md")]
    collisions = sum(
        1 for g in graph["colorGroups"]
        if len([f for f in files if g["query"].split('path:"')[1].rstrip('"') in f]) != 1
    )
    check("11 colorGroups (10 + core), zero collisions",
          len(graph["colorGroups"]) == 11 and collisions == 0)

    # 4. checkpoints interlink via the ring (Karpathy cross-referencing, no orphans)
    loop = [p.stem for p in notes]
    idx = {s: i for i, s in enumerate(loop)}
    ring = set()
    for p in notes:
        for tgt in re.findall(r"\[\[([^\]|]+)", p.read_text()):
            if tgt in idx:
                ring.add(frozenset((p.stem, tgt)))
    check("checkpoints interlink via ring (10 edges)", len(ring) == 10)

    # 4b. central core hub: links every checkpoint (spokes), is graph-visible, notes/ exists
    core = (tmp / "_core.md").read_text()
    core_links = {t for t in re.findall(r"\[\[([^\]|]+)", core) if t in idx}
    check("core links to all 10 checkpoints", len(core_links) == 10)
    check("core node in canvas", any(n.get("id") == "core" for n in canvas["nodes"]))
    check("core spokes to all 10 steps",
          len([e for e in canvas["edges"] if e["fromNode"] == "core" and e["toNode"].startswith("n")]) == 10)
    check("core folds the control plane as sections",
          all(h in core for h in ("## Schema", "## Sources", "## Log")))
    check("core does not link separate hubs",
          not any(f"[[{s}]]" in core for s in ("_log", "_schema", "_sources")))
    check("notes/ folder scaffolded", (tmp / "notes").is_dir())
    check("no stray _index node (core does not link notes/_index)", "notes/_index" not in core)
    excludes = [t[len("-path:"):] for t in graph["search"].split() if t.startswith("-path:")]
    check("core visible (not filtered)", not any(ex in "_core.md" for ex in excludes))
    check("no separate hub files exist",
          not any((tmp / f"{s}.md").exists() for s in ("_log", "_schema", "_sources")))

    # 4c. Karpathy lint: dense interlink, no orphans, no unresolved links
    check("graph hides orphans + unresolved",
          graph["showOrphans"] is False and graph["hideUnresolved"] is True)
    check("each checkpoint links back to the core",
          all("[[_core]]" in (tmp / f"{c}.md").read_text() for c in loop))
    vis = [p for p in tmp.rglob("*.md") if not any(e in str(p) for e in excludes)]
    vnames = {p.stem for p in vis}
    unresolved = [(p.stem, t) for p in vis for t in re.findall(r"\[\[([^\]|#]+)", p.read_text())
                  if t.split("/")[-1] not in vnames and not any(e in t for e in excludes)]
    check("no unresolved / orphan-creating links", not unresolved)

    # 5. the safety gates are present in the rendered notes
    check("stop contract max_passes:5 in 09", "max_passes: 5" in (tmp / "09 - Undo & Loop.md").read_text())
    check("claim ledger in 04", "claim_id" in (tmp / "04 - Verify.md").read_text())
    check("prune archive-only in 06", "Never delete directly" in (tmp / "06 - Prune.md").read_text())
    check("no-invent rule in 01", "Never invent" in (tmp / "01 - Read.md").read_text())

    # 6. --force preserves the appended ## Runs log
    read_note = tmp / "01 - Read.md"
    marker = "SENTINEL run-log line"
    txt = read_note.read_text().replace("## Runs\n", f"## Runs\n- {marker}\n", 1)
    read_note.write_text(txt)
    run(["Test goal here", "--dir", str(tmp), "--force", "--max-loops", "5"], tmp)
    check("--force preserves ## Runs", marker in read_note.read_text())

    # 7. default rebuild keeps notes untouched (run-log still present, no overwrite)
    run(["Test goal here", "--dir", str(tmp)], tmp)
    check("default rebuild keeps run-log", marker in read_note.read_text())

    # 8. --max-loops below 1 is rejected
    bad = run(["Test goal here", "--dir", str(tmp), "--max-loops", "0"], tmp)
    check("--max-loops 0 rejected", bad.returncode != 0)

    # 9. a goal containing a quote stays valid YAML frontmatter
    tq = pathlib.Path(tempfile.mkdtemp(prefix="loop_q_"))
    run(['build a "smart" loop', "--dir", str(tq)], tq)
    gline = next(l for l in (tq / "00 - Goal.md").read_text().splitlines() if l.startswith("goal:"))
    check("goal with a quote yields valid frontmatter",
          json.loads(gline[len("goal:"):].strip()) == 'build a "smart" loop')
    shutil.rmtree(tq, ignore_errors=True)

    # 10. empty goal is rejected
    check("empty goal rejected", run(["", "--dir", str(tmp)], tmp).returncode != 0)

    print()
    shutil.rmtree(tmp, ignore_errors=True)
    if failures:
        print(f"{len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
