# Orchestration: how to drive the loop

Read this before walking a loop. Each checkpoint is a stop where you run one command,
record what happened, and link artifacts. The loop graph never grows: artifacts live in
`topics/<slug>/` which is filtered out of the graph view.

## The control plane

Four central nodes (the Karpathy "LLM Wiki" pattern) hold the loop's state; each links every
checkpoint. Maintain them as you walk:

- **`_core`** — the index. Open first. Reflects goal, acceptance, and the loop list.
- **`_log`** — append-only record. Closeout (08) prepends one dated line per pass.
- **`_schema`** — conventions that govern every checkpoint. Update when a convention changes.
- **`_sources`** — raw-layer index over `topics/<slug>/`. Note new source sets here at Read.

## Per-checkpoint actions

**00 Goal (intent).** Clarify the goal in plain language. Write the acceptance criteria
(the bar for "done") and the scope, constraints, and blast radius into `00 - Goal.md`
before any work. If the vault has no loop, scaffold it first with `build_goaloop.py`.

**01 Read (read first).** Auto-route: version numbers, named APIs, or recent events use
`/research --deep`; broad or strategic topics use `/autoresearch`. Gather at least 3
independent sources, each captured raw into `topics/<slug>/sources/` via the source artifact
template (title, url, retrieved_at, via_command, quoted_evidence). **Never invent a source,
URL, or quote;** if none is found, say so. Append a run-log line to `01 - Read.md`.

**02 Map (smallest unit).** Run `/wiki-query "<goal>"` to see what is already known.
Fill the known vs missing map. Name the single next unit of work. Do not boil the ocean.

**03 Write (name like the reader is hostile).** Synthesize into clean, well-named concept
notes via `/save` and wiki-ingest. File into `topics/<slug>/concepts/`. If you cannot name
a concept cleanly, you do not understand it yet.

**04 Verify (evidence over intuition).** Build a claim ledger at
`topics/<slug>/reports/claim-ledger-<date>.md` covering every material claim from Write
(columns: claim_id, claim, source artifact, verifier command, verdict PASS/FAIL/UNKNOWN,
evidence quote/link). PASS requires a quote or command-output link. Then `/wiki-lint` for
dead links and stale claims. **Do not proceed while any material claim is FAIL or UNKNOWN:**
FAIL returns to **03 Write**; UNKNOWN is removed, scoped explicitly, or sent to **05 Gaps**.

**05 Gaps (failure is the spec).** List gaps, contradictions, unknowns. Find the root
cause, not the symptom. If material gaps remain, jump back to **01 Read** for a targeted
gap-fill pass.

**06 Prune (delete more than you add).** Run `/wiki-lint` for orphans. **Archive-only,
never delete directly:** write a dry-run manifest at `_archive/prune/<date>/manifest.md`,
get explicit user approval, then move candidates into `_archive/prune/<date>/`. Never prune
`00`-`09`, the control plane (`_core`/`_log`/`_schema`/`_sources`), `goaloop/`, `scripts/`,
`Loop.canvas`, or anything outside `topics/<slug>/`.

**07 Hot (working memory).** Overwrite the Live state block with about 500 words: recent
facts, active threads, recent changes. This is a cache, not a journal. Never append it.

**08 Closeout (five parts).** Write integrated result, verification summary, artifact
ids/links, notes-current confirmation, and the next slice with rationale. Prepend a
one-line entry to `_log`. Fewer than five parts means the slice is still open.

**09 Undo & Loop (undo not optional).** Write the reversal plan for this iteration, then
apply the stop contract (below). Exit only when every acceptance criterion has PASS evidence
in the `04 Verify` claim ledger; otherwise refine intent and loop to **00 Goal**. Honor
`max_passes`; if reached with unmet criteria, stop and ask the user. Record pass count,
elapsed, and unmet criteria.

## Stop contract (prevents infinite loops)

- `max_passes` defaults to 3 (override with `--max-loops N` at scaffold, or per the user).
- Exit ONLY when every acceptance criterion in `00 - Goal.md` has PASS evidence in the
  `04 - Verify` claim ledger.
- On reaching `max_passes` with unmet criteria: STOP and ask the user. Never loop silently.
- Closeout (`08`) may only summarize artifacts that exist in run-logs or `topics/<slug>/`.

## Control flow

```
00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → (00 if not met, else exit)
              ▲           │           │
              └─ gaps ────┘           │   (05 → 01)
                    ▲                 │
                    └─ verify fail ───┘   (04 → 03)
```

The two feedback edges are drawn on `Loop.canvas` in red. The main ring is the default
edge color. The 9 → 0 ring edge is the undo/loop closure itself.

## Fan-out (agent kernel)

When a checkpoint needs scale, goaloop is the one chair:
- **Read** dispatches research explorers (map sources, do not synthesize).
- **Verify** dispatches adversarial verifiers (each tries to refute a claim; gate on
  majority). The verifier must not be the agent that wrote the material.
- Write acceptance criteria before dispatching. Bounded slices, no overlapping writes.
- Closeout has five parts or the slice is open.
