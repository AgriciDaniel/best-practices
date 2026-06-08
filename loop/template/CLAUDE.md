# This is a loop vault

A best-practices orchestration loop for one goal. Any Claude session that opens this vault
should drive it the same way.

## Start here every time
1. Open `_core.md` — the single command-center hub. It links every checkpoint and holds the
   loop index plus the `## Schema`, `## Sources`, and `## Log` sections.
2. Read `07 - Hot.md` (the Live state block) for the cheapest current context.
3. Then `00 - Goal.md` for the goal and acceptance criteria.

## The loop
`Goal → Read → Map → Write → Verify → Gaps → Prune → Hot → Closeout → Undo & Loop → back to Goal`

Walk it in order. At each checkpoint run its orchestrated command, append a dated line to
that note's `## Runs` section (newest first), and link any artifact you produce.

## Rules
- **Feed, do not create orbs.** Never add new `NN - *.md` checkpoint notes. The ten
  checkpoints plus `_core` are fixed. Curated notes go in `notes/`; put `[[_core]]` inside
  each and list it in the core's Notes index, so it appears as a satellite around the core
  in the graph. Raw research stays in `topics/<slug>/` (hidden from the graph).
- **`07 - Hot.md` Live state is overwrite-only.** The `## Log` section of `_core` is
  append-only at the top.
- **Verify is a real gate.** Every material claim enters the `04 - Verify` claim ledger with
  a PASS/FAIL/UNKNOWN verdict backed by a quote or command output. Do not pass Verify with
  any FAIL or UNKNOWN material claim. On FAIL go back to Write; UNKNOWN goes to Gaps.
- **No invented evidence.** Read may never fabricate a source, URL, or quote. Closeout may
  only summarize artifacts that exist in run-logs or `topics/<slug>/`.
- **Bounded loop.** Honor `max_passes` in `09 - Undo & Loop.md`; if reached with unmet
  criteria, stop and ask the user. Never loop silently.
- **Prune is archive-only.** Never delete directly: dry-run manifest, explicit approval,
  then move into `_archive/prune/<date>/`. Never touch `00`-`09`, `_core`, `loop/`,
  `scripts/`, or `Loop.canvas`.
- **An undo plan is not optional.** Record it at `09 - Undo & Loop.md` before deciding to
  loop or exit.

## Regenerate the visuals
The loop notes, `Loop.canvas`, and `.obsidian/graph.json` are generated. A plain rebuild
**keeps existing checkpoint notes untouched** (so your run-logs are safe) and only recreates
missing notes plus the canvas and graph config. Pass `--force` to regenerate note structure
from the templates; even then the appended `## Runs` logs are preserved. The generator never
deletes checkpoint notes. Your `topics/` artifacts are never touched.
