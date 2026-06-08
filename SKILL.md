---
name: best-practices
description: The six-cut kernel (read first, write second, verify third) and its runnable loop. Use before a non-trivial multi-file diff or multi-slice agent run, when auditing a major change, or to run the best-practices loop on a goal (a fixed ten-checkpoint pass you point at one objective and walk to done).
license: MIT
---

# best-practices

read first. write second. verify third.

a meditation: six axioms compressed into something you reread before shipping.
the kernel does not enforce itself; for enforcement, compose with
`obra/superpowers`.

to *apply* the kernel to real work, run the **loop** (below): the kernel made
runnable. that is the default way to use best-practices on a goal.

## the loop (default)

when the user gives you a goal to pursue end to end (or says "run the loop" or
"start a goal"), scaffold and drive a ten-checkpoint best-practices loop as an
Obsidian vault:

1. `python3 "${CLAUDE_SKILL_DIR}/loop/scripts/build_loop.py" "<goal>" --dir "<vault>" --max-loops 3`
   (default `--dir .`). this writes ten checkpoints (`00 - Goal` .. `09 - Undo &
   Loop`) around a single `_core` note that holds the index, schema, sources,
   and an append-only log.
2. open `_core` first, then walk the checkpoints in order, running the
   orchestrated command at each and recording evidence. full runbook:
   `${CLAUDE_SKILL_DIR}/loop/references/orchestration.md`.
3. honor the stop contract (`max_passes`); verify gates on a claim ledger; an
   undo plan is not optional. rebuilds never delete notes.

for a quick read of the principles instead of a run, the kernel follows.

## the stance

context over text. calibrated confidence. evidence over vibes. no agreement
theater. confidence is earned, not asserted. skepticism is not new
information. accountability is non-transferable: you read because you sign.

without the stance, the kernel becomes ceremony.

## engineering kernel

six cuts. three acts.

### before

- **read before write.** code you do not understand, you cannot change. open
  call sites, tests, schema, consumers. removals break assumptions as often as
  additions.
- **name like the next reader is hostile.** good names carry context, bad
  names hide bugs. cannot name it cleanly, do not understand it yet.

### during

- **smallest unit that works.** one purpose per unit, well-defined edges,
  testable in isolation. complexity is earned, not anticipated. no abstraction
  without three real callers.
- **delete more than you add.** code is liability. carry only what earns its
  weight every week.

### after

- **evidence over intuition.** measure before optimizing. trust nothing
  unverified. if a task has no verification path, refuse it until it does.
- **failure is the spec.** before a fix, find the root cause; symptoms patched
  at the surface come back. include the security failure path: untrusted
  input, network access, state changes need an explicit blast-radius answer.
  an undo plan is not optional.

## agent kernel

shipping with help nests rigor inside coordination.

- **one chair.** every change has one human who owns the call.
- **bounded slices.** no overlapping write scopes.
- **explorers map, workers implement, verifiers gate.** different read/write
  contracts.
- **acceptance criteria written before execution.**
- **per-change rigor inside every slice.** orchestration amplifies the
  engineering kernel, does not exempt it.
- **closeout has five parts.** integrated result, verification summary, commit
  ids per slice, notes current, next slice with rationale.

agents have one extra constraint: context is a budget, not a backdrop. clear
when poisoned. dispatch fresh-context reviewers, not the same head twice.

codex subagents: use only when the user explicitly asks for subagents or
parallel agent work. keep the main thread for requirements, decisions, and
integration. delegate bounded work such as exploration, tests, triage, or a
disjoint implementation slice. ask for summaries, not raw tool output.

## per-change loop

every diff:

1. understand intent before touching keys
2. enumerate blast radius before changing a public surface
3. ship the smallest viable change
4. prove it with tests, prove it again after every fix
5. write the undo plan or do not ship

guessing on any one means stop and investigate.

## composition

- needs **enforcement** for adversarial agents -> add `obra/superpowers`
- needs **iron-law TDD** -> add `superpowers:test-driven-development`
- needs **debugging discipline** -> add `superpowers:systematic-debugging`
- needs **parallel-agent SOP** -> add `superpowers:dispatching-parallel-agents`

this skill is the meditation. those are the enforcement.

## reference

full prose, rationale, and the agent kernel detail (per-change + orchestration
rules) live in the README and `shipping-rules.md` of this repo. this SKILL.md
is the compressed loadable form.

source: github.com/AgriciDaniel/best-practices
