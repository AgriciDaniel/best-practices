---
name: goaloop
description: >
  Scaffold and drive a manually invoked Obsidian "goaloop" vault for one explicit goal: a fixed
  10-checkpoint best-practices loop (intent, read, write, verify, gaps, prune, hot, closeout, undo)
  that orchestrates /autoresearch, /research, /deep-research, /save, /wiki-query, and /wiki-lint into
  each stage and feeds fixed checkpoints instead of creating new notes. Use ONLY when the user types
  /goaloop or explicitly asks to scaffold or run a goaloop vault. Not for Claude Code's built-in /goal.
disable-model-invocation: true
argument-hint: '"<goal/topic>" [--dir <vault>] [--max-loops N]'
---

# goaloop

A reusable orchestration layer that turns any goal into a closed best-practices loop.
The loop has ten fixed checkpoints plus a four-node control plane. You **feed** them, you
do not multiply them: each run appends to a checkpoint's run-log and files real artifacts
into a graph-filtered `topics/<slug>/` folder, so the checkpoints never multiply while
history accumulates. A central **Hot** checkpoint holds live working memory. The loop closes
back on itself: an undo plan is not optional.

## The ten checkpoints

`Goal → Read → Map → Write → Verify → Gaps → Prune → Hot → Closeout → Undo & Loop → (back to Goal)`

Each checkpoint embodies one best-practices principle and orchestrates one command.
Full mapping in `references/kernel-map.md`. Exact per-checkpoint behaviour and the loop
control flow in `references/orchestration.md`. **Read `references/orchestration.md`
before driving a loop.**

## The control plane

Four central nodes sit at the heart of the vault (the Karpathy "LLM Wiki" pattern). Each
links every checkpoint, so the graph is a dense, orphan-free star with the control plane at
its center. Open `_core` first.

- **`_core`** — the index and command center: goal, acceptance snapshot, the loop list, and
  links to the rest of the control plane. Navigation routes through here.
- **`_log`** — the append-only chronological record. Closeout (08) prepends one line per pass.
- **`_schema`** — the conventions that govern how every checkpoint behaves.
- **`_sources`** — the raw-layer index over the immutable `topics/<slug>/` artifacts.

Curated notes go in `notes/` and link `[[_core]]`; they grow as satellites around the core.
Raw research stays in `topics/<slug>/`, filtered out of the graph.

## When invoked

1. **Resolve the vault.** Pick or confirm a target directory for this goal. If it has no
   loop yet, scaffold one:
   `python3 "${CLAUDE_SKILL_DIR}/scripts/build_goaloop.py" "<goal text>" --dir "<vault path>" --max-loops 3`
   (default `--dir .`). If it already has a loop, resume by opening `_core.md` (the
   command-center index at the center of the control plane), then its `07 - Hot.md`
   live-state block (cheapest context), then `00 - Goal.md`. Rebuilds default to
   keeping existing notes untouched; pass `--force` to regenerate structure (run-logs are
   preserved). The generator never deletes checkpoint notes.

2. **Walk the loop** as described in `references/orchestration.md`: at each checkpoint run
   the orchestrated command, append a dated run-log line, and link any artifact into
   `topics/<slug>/`. Apply per-change rigor and the stance: evidence over vibes,
   calibrated confidence, trust nothing unverified.

3. **Hot, then Closeout.** Overwrite the `07 - Hot.md` live-state block (never append it).
   Write the five-part closeout in `08 - Closeout.md` and prepend a one-line entry to `_log`.

4. **Undo and decide (bounded).** At `09 - Undo & Loop.md` record the reversal plan, then
   apply the **stop contract**: exit only when every acceptance criterion in `00 - Goal.md`
   has PASS evidence in the `04 - Verify` claim ledger. Otherwise refine intent and loop back
   to `00 - Goal.md`. The loop is bounded by `max_passes` (default 3); if it is reached with
   unmet criteria, **stop and ask the user** rather than looping again. Conditional jumps
   inside a pass: Verify failure returns to Write, remaining HIGH gaps return to Read.

## Reliability gates (non-negotiable)

- **No invented evidence.** Read may never fabricate a source, URL, or quote. If a source
  is not found, say so.
- **Verify is a real gate.** Every material claim enters the `04 - Verify` claim ledger with
  a PASS/FAIL/UNKNOWN verdict backed by a quote or command output. Do not pass Verify with
  any FAIL or UNKNOWN material claim. Closeout may only summarize artifacts that exist.
- **Bounded loop.** Honor `max_passes`; stop and ask when exhausted. Never loop silently.
- **Prune is archive-only.** Never delete directly: write a dry-run manifest, get explicit
  user approval, then move candidates into `_archive/prune/<date>/`. Never touch `00`–`09`,
  the control plane (`_core`/`_log`/`_schema`/`_sources`), `goaloop/`, `scripts/`, or
  `Loop.canvas`.

## Discipline (non-negotiable)

- **Feed, do not create orbs.** Never add new top-level checkpoint notes. New material
  goes into `topics/<slug>/` (filtered out of the graph) and is linked from a checkpoint.
- **Hot is overwrite-only.** The log is append-only at the top. Do not confuse them.
- **One chair.** goaloop owns the call. When it fans work out (research explorers at Read,
  adversarial verifiers at Verify) it writes acceptance criteria before dispatching and
  gates on a verifier that did not produce the work.

## Files (bundled inside this skill)

- `${CLAUDE_SKILL_DIR}/scripts/build_goaloop.py` scaffolds a vault. The script is
  self-contained inside the skill, so it resolves its templates regardless of the cwd.
- `${CLAUDE_SKILL_DIR}/template/checkpoints/00..09.md` are the checkpoint bodies and
  `template/core.md` is the index body; the generator owns titles, frontmatter, and wiring.
  The `_log`/`_schema`/`_sources` hub notes are generated directly by the script.
- `${CLAUDE_SKILL_DIR}/template/CLAUDE.md` is referenced into each goal vault so any session
  can drive it.
