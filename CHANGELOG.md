# changelog

all notable changes to best-practices. format loosely follows keep a changelog;
versions follow semver.

## [1.0.0] - 2026-06-09

first tagged release: the six-cut kernel and its runnable loop.

### added
- the **kernel** the stance, the engineering kernel (six cuts, three acts), and the agent
  kernel, as a claude code skill + slash command + portable `AGENTS.md`.
- the **loop** the kernel made runnable. `/best-practices "<goal>"` scaffolds and drives a
  fixed ten-checkpoint loop (intent, read, write, verify, gaps, prune, hot, closeout, undo)
  as an obsidian vault, around a single `_core` note that holds the index, schema, sources,
  and an append-only log. verify gates on a claim ledger; a stop contract bounds passes; an
  undo plan is not optional; rebuilds never delete notes. self-contained generator, 29 tests.
- visuals `svg/loop.svg` (schematic) and `svg/loop-graph.png` (the live graph).

### notes
- the loop is operationalization, not enforcement. for enforcement, compose with
  [obra/superpowers](https://github.com/obra/superpowers).
