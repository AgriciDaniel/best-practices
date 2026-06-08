#!/usr/bin/env python3
"""loop — scaffold a best-practices orchestration loop as an Obsidian vault.

Usage:
    python3 scripts/build_loop.py "<goal text>" [--dir <path>]

Emits into <path> (default "."):
  - 10 checkpoint notes (00..09), wired into a closed loop (9 -> 0)
  - Loop.canvas        — stadium/racetrack layout, cyclic gradient, feedback chords
  - .obsidian/graph.json — filter "-path:topics -path:.canvas" + 10 gradient colorGroups
  - topics/<slug>/{sources,concepts,reports}.md — graph-filtered artifact landing notes
  - log.md             — append-only run log (created if missing)

The graph view renders a clean 10-orb loop; artifacts and the canvas are filtered out,
so the loop never grows new orbs no matter how much you feed it.
"""
import argparse
import datetime
import json
import math
import pathlib
import re

# (title, cut) — single source of truth for the loop. Stems are "NN - <title>".
CHECKPOINTS = [
    ("Goal",          "intent"),
    ("Read",          "read before write"),
    ("Map",           "smallest unit that works"),
    ("Write",         "name like the next reader is hostile"),
    ("Verify",        "evidence over intuition"),
    ("Gaps",          "failure is the spec"),
    ("Prune",         "delete more than you add"),
    ("Hot",           "the hot pattern"),
    ("Closeout",      "agent kernel closeout"),
    ("Undo & Loop",   "an undo plan is not optional"),
]
N = len(CHECKPOINTS)

# --- ring geometry (canvas units): 10 checkpoints on a circle, core at center
CARD_W, CARD_H = 260, 120
RING_R = 620.0         # circle radius; neighbor chord ~= 0.62*R keeps cards clear

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent          # loop/scripts/
TEMPLATE_DIR = SCRIPT_DIR.parent / "template" / "checkpoints"  # loop/template/checkpoints/

# feedback chords the kernel implies: (from_idx, to_idx, label)
FEEDBACK = [(4, 3, "fail → rewrite"), (5, 1, "gaps → re-read")]

# central command-center hub (wheel topology: ring of 10 + spokes from the core)
CORE_STEM = "_core"
CORE_COLOR = "#e9e9f0"                 # near-white, reads as the center of the wheel
CORE_RGB = int(CORE_COLOR.lstrip("#"), 16)
CORE_W, CORE_H = 300, 150

# The Karpathy "LLM Wiki" control plane (index / log / schema / sources / raw layer) lives
# as sections INSIDE _core, not as separate nodes. one central core, nothing beside it.


def positive_int(value):
    iv = int(value)
    if iv < 1:
        raise argparse.ArgumentTypeError("--max-loops must be >= 1 (the stop contract needs at least one pass)")
    return iv


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "goal"


def stems():
    return [f"{i:02d} - {title}" for i, (title, _cut) in enumerate(CHECKPOINTS)]


# --- ring layout: 10 checkpoints evenly spaced on a circle, core at the center
def ring_centers():
    """N centers on a circle, node 0 at top (12 o'clock), going clockwise."""
    return [(RING_R * math.cos(-math.pi / 2 + i * 2 * math.pi / N),
             RING_R * math.sin(-math.pi / 2 + i * 2 * math.pi / N)) for i in range(N)]


# --- cyclic gradient (hue wraps 0..360 so node 9 meets node 0 with no seam) -
SAT, LIGHT = 0.62, 0.58


def _hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x),
               (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
    return tuple(round((v + m) * 255) for v in (r, g, b))


def grad_rgb(i):
    return _hsl_to_rgb(360.0 * i / N, SAT, LIGHT)


def grad_hex(i):
    return "#%02x%02x%02x" % grad_rgb(i)


def grad_int(i):
    r, g, b = grad_rgb(i)
    return (r << 16) | (g << 8) | b


# --- notes ------------------------------------------------------------------
def render_note(i, goal, slug, date, max_loops):
    title, cut = CHECKPOINTS[i]
    names = stems()
    prev_i, next_i = (i - 1) % N, (i + 1) % N
    body = (TEMPLATE_DIR / f"{i:02d}.md").read_text(encoding="utf-8")
    body = (body.replace("{{goal}}", goal).replace("{{slug}}", slug)
                .replace("{{date}}", date).replace("{{max_loops}}", str(max_loops)))

    # each checkpoint links its ring neighbours (prev/next) and the core, so the wiki is
    # densely interlinked with no orphans, everything pointing back into _core.
    front = [
        "---", "loop: checkpoint", f"step: {i}", f'title: "{title}"',
        f'cut: "{cut}"', f'prev: "[[{names[prev_i]}]]"', f'next: "[[{names[next_i]}]]"',
        f"goal: {json.dumps(goal)}", f"slug: {slug}", "---", "",
    ]
    nav = (f"---\n↩ [[{CORE_STEM}]]  ·  ◀ [[{names[prev_i]}|{CHECKPOINTS[prev_i][0]}]]"
           f"  ·  [[{names[next_i]}|{CHECKPOINTS[next_i][0]}]] ▶\n")
    return "\n".join(front) + f"# {title}\n\n" + body.rstrip() + "\n\n" + nav


def render_core(goal, slug, date, max_loops):
    """The central hub note: links to all 10 checkpoints (the spokes) plus the notes index."""
    body = (TEMPLATE_DIR.parent / "core.md").read_text(encoding="utf-8")
    loop_index = "\n".join(f"- [[{i:02d} - {t}]] — {cut}" for i, (t, cut) in enumerate(CHECKPOINTS))
    body = (body.replace("{{goal}}", goal).replace("{{slug}}", slug)
                .replace("{{date}}", date).replace("{{max_loops}}", str(max_loops))
                .replace("{{loop_index}}", loop_index))
    front = ["---", "loop: core", 'title: "Core"', f"goal: {json.dumps(goal)}", f"slug: {slug}", "---", ""]
    return "\n".join(front) + "# loop · core\n\n" + body.rstrip() + "\n"


def extract_runs(text):
    """Return the user's run-log lines under '## Runs' (excluding placeholder comments)."""
    i = text.find("## Runs")
    if i < 0:
        return ""
    seg = text[i + len("## Runs"):]
    j = seg.find("\n---\n↩")          # stop before the nav footer
    if j >= 0:
        seg = seg[:j]
    kept = [ln for ln in seg.splitlines() if ln.strip() and not ln.strip().startswith("<!--")]
    return "\n".join(kept)


def write_note(path, fresh, force):
    """Create if missing. If it exists: keep it untouched unless force; on force,
    rebuild from template but PRESERVE the appended run-log so rebuilds never erase history."""
    if not path.exists():
        path.write_text(fresh, encoding="utf-8")
        return "created"
    if not force:
        return "kept"
    preserved = extract_runs(path.read_text(encoding="utf-8"))
    if preserved:
        k = fresh.find("\n---\n↩")
        if k >= 0:
            fresh = fresh[:k] + "\n" + preserved + "\n" + fresh[k:]
    path.write_text(fresh, encoding="utf-8")
    return "rebuilt(+runs)" if preserved else "rebuilt"


def write_core(path, fresh):
    """Rewrite _core from template but PRESERVE its append-only '## Log' tail section."""
    if path.exists():
        old = path.read_text(encoding="utf-8")
        i = old.find("## Log")
        if i >= 0:
            kept = [ln for ln in old[i + len("## Log"):].splitlines()
                    if ln.strip() and not ln.strip().startswith("<!--")]
            if kept:
                k = fresh.find("## Log")
                if k >= 0:
                    nl = fresh.find("\n", k)
                    fresh = fresh[:nl + 1] + "\n".join(kept) + "\n" + fresh[nl + 1:]
    path.write_text(fresh, encoding="utf-8")


# --- canvas -----------------------------------------------------------------
def _side(p_from, p_to):
    dx, dy = p_to[0] - p_from[0], p_to[1] - p_from[1]
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def build_canvas(centers):
    names = stems()
    nodes = [{
        "id": f"n{i}", "type": "file", "file": f"{names[i]}.md",
        "x": round(cx - CARD_W / 2), "y": round(cy - CARD_H / 2),
        "width": CARD_W, "height": CARD_H, "color": grad_hex(i),
    } for i, (cx, cy) in enumerate(centers)]

    edges = []
    for i in range(N):                                   # ring, including 9 -> 0
        j = (i + 1) % N
        fs, ts = _side(centers[i], centers[j])
        edges.append({"id": f"e{i}", "fromNode": f"n{i}", "fromSide": fs,
                      "toNode": f"n{j}", "toSide": ts, "toEnd": "arrow"})
    for k, (a, b, label) in enumerate(FEEDBACK):         # feedback chords (red, labeled)
        fs, ts = _side(centers[a], centers[b])
        edges.append({"id": f"f{k}", "fromNode": f"n{a}", "fromSide": fs,
                      "toNode": f"n{b}", "toSide": ts, "toEnd": "arrow",
                      "color": "1", "label": label})

    # single central core at (0,0) + a spoke to every checkpoint
    nodes.append({"id": "core", "type": "file", "file": f"{CORE_STEM}.md",
                  "x": round(-CORE_W / 2), "y": round(-CORE_H / 2),
                  "width": CORE_W, "height": CORE_H, "color": CORE_COLOR})
    for i, (cx, cy) in enumerate(centers):
        fs, ts = _side((0, 0), (cx, cy))
        edges.append({"id": f"s{i}", "fromNode": "core", "fromSide": fs,
                      "toNode": f"n{i}", "toSide": ts, "toEnd": "arrow"})
    return {"nodes": nodes, "edges": edges}


# --- graph config -----------------------------------------------------------
# Show ONLY the 10 loop notes: exclude artifacts, archive, the product docs, and the log.
GRAPH_FILTER = ("-path:_archive -path:loop/ -path:examples -path:scripts "
                "-path:topics -path:.canvas")

GRAPH_DEFAULTS = {
    "collapse-filter": True, "search": GRAPH_FILTER, "showTags": False,
    "showAttachments": False, "hideUnresolved": True, "showOrphans": False,
    "collapse-color-groups": False, "colorGroups": [], "collapse-display": True,
    "showArrow": True, "textFadeMultiplier": 0, "nodeSizeMultiplier": 1.1,
    "lineSizeMultiplier": 1.1, "collapse-forces": True, "centerStrength": 0.05,
    "repelStrength": 20, "linkStrength": 0.6, "linkDistance": 320, "scale": 1, "close": False,
}


def patch_graph(vault):
    gpath = vault / ".obsidian" / "graph.json"
    cfg = dict(GRAPH_DEFAULTS)
    if gpath.exists():
        try:
            cfg.update(json.loads(gpath.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    cfg["search"] = GRAPH_FILTER
    cfg["showArrow"] = True                       # directed loop — always show arrows
    cfg["hideUnresolved"] = True                  # no dangling/unresolved nodes
    cfg["showOrphans"] = False                    # no orphans
    # force-layout tuning: weak center pull + strong repulsion + long links relaxes the
    # wheel into a round ring around the core (a force sim can only approximate a circle)
    cfg.update({"centerStrength": 0.05, "repelStrength": 20,
                "linkStrength": 0.6, "linkDistance": 320})
    cfg["colorGroups"] = [
        {"query": f'path:"{stem}.md"', "color": {"a": 1, "rgb": grad_int(i)}}
        for i, stem in enumerate(stems())
    ]
    cfg["colorGroups"].append(
        {"query": f'path:"{CORE_STEM}.md"', "color": {"a": 1, "rgb": CORE_RGB}})
    gpath.parent.mkdir(parents=True, exist_ok=True)
    gpath.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


# --- scaffolding ------------------------------------------------------------
def scaffold_topics(vault, slug):
    base = vault / "topics" / slug
    for kind in ("sources", "concepts", "reports"):
        (base / kind).mkdir(parents=True, exist_ok=True)
        landing = base / f"{kind}.md"
        if not landing.exists():
            landing.write_text(
                f"---\ntype: artifact-index\nkind: {kind}\nslug: {slug}\n---\n"
                f"# {kind.title()} — {slug}\n\nArtifacts fed by the loop. "
                f"Filtered out of the graph view.\n", encoding="utf-8")


def scaffold_notes(vault):
    """An empty, graph-visible wiki folder. Notes added here link [[_core]] directly and
    appear as satellites around the core; with no notes the graph stays a clean core + 10."""
    nd = vault / "notes"
    nd.mkdir(exist_ok=True)
    keep = nd / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")


def build(goal, vault, force=False, max_loops=3):
    if not goal.strip():
        raise SystemExit("error: goal must not be empty")
    vault = pathlib.Path(vault).resolve()
    vault.mkdir(parents=True, exist_ok=True)
    slug = slugify(goal)
    date = datetime.date.today().isoformat()

    names = stems()
    status = {}
    for i in range(N):
        fresh = render_note(i, goal, slug, date, max_loops)
        status[names[i]] = write_note(vault / f"{names[i]}.md", fresh, force)

    # _core absorbs index/schema/sources/notes/log; rebuild preserves its append-only Log tail
    write_core(vault / f"{CORE_STEM}.md", render_core(goal, slug, date, max_loops))

    # visuals + config carry no user data, so they are always (re)written
    centers = ring_centers()
    (vault / "Loop.canvas").write_text(json.dumps(build_canvas(centers), indent=2),
                                       encoding="utf-8")
    patch_graph(vault)
    scaffold_topics(vault, slug)
    scaffold_notes(vault)

    print(f"vault: {vault}")
    print(f"goal:  {goal}  (slug: {slug})  max_loops: {max_loops}")
    print(f"core: {CORE_STEM}.md  |  canvas nodes: {N + 1}  |  "
          f"edges: {2 * N + len(FEEDBACK)} (ring {N} + spokes {N} + feedback {len(FEEDBACK)})")
    print("notes: " + ", ".join(f"{k[:2]}:{v}" for k, v in status.items()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("goal", help="the goal/topic this loop pursues")
    ap.add_argument("--dir", default=".", help="vault directory (default: current)")
    ap.add_argument("--max-loops", type=positive_int, default=3,
                    help="loop stop bound baked into 09 (default: 3, must be >= 1)")
    ap.add_argument("--force", action="store_true",
                    help="rebuild existing checkpoint notes from template, preserving their run-logs "
                         "(default: existing notes are kept untouched)")
    args = ap.parse_args()
    build(args.goal, args.dir, force=args.force, max_loops=args.max_loops)
