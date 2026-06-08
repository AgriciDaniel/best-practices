# changelog

all notable changes to best-practices. format loosely follows keep a changelog;
versions follow semver.

## [1.0.0] - 2026-06-08

first tagged release. the kernel was already here; this marks it 1.0 and adds the
runnable layer on top.

### added
- **goaloop** the kernel made runnable. a manually-invoked claude code skill that
  scaffolds and drives a fixed ten-checkpoint best-practices loop as an obsidian vault,
  with a karpathy "llm wiki" control plane (`_core` / `_log` / `_schema` / `_sources`).
  ships with a self-contained generator and 33 regression tests.
- `svg/goaloop.svg` loop and control-plane schematic in the repo house style.
- `svg/goaloop-graph.png` the live graph: ten interlinked checkpoints, no orphans.
- a sixth badge, a goaloop readme section framed as the runnable layer, and a version badge.

### notes
- goaloop is operationalization, not enforcement. for enforcement, still compose with
  [obra/superpowers](https://github.com/obra/superpowers).
- the kernel itself (the stance, the engineering kernel, the agent kernel) is unchanged.
