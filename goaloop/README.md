# goaloop

The best-practices orchestration loop. Point it at any goal and it scaffolds a closed
ten-checkpoint loop as an Obsidian vault, then drives that loop by orchestrating your
existing commands into each stage.

The spine is the `best-practices` kernel: intent, read first, write second, verify third,
and an undo/loop that bends the line back on itself. The checkpoints are fixed. You feed
them; they never multiply.

## The loop

`Goal → Read → Map → Write → Verify → Gaps → Prune → Hot → Closeout → Undo & Loop → (back to Goal)`

- **Graph view** renders a dense, orphan-free web: the ten checkpoints with a cyclic color
  gradient, interlinked and orbiting a single core.
- **Loop.canvas** lays the ten checkpoints on a circle with the core at the center, plus two
  red feedback chords (verify fail to write, gaps to read).
- **`_core`** is the one central node (the Karpathy "LLM Wiki" pattern as one note): the loop
  index plus `## Schema` (conventions), `## Sources` (raw-layer index), and `## Log`
  (append-only record) sections.
- **topics/<slug>/** holds the real artifacts and is filtered out of the graph, so the
  checkpoints never multiply no matter how much you gather.
- **07 Hot** is the live working-memory checkpoint (overwrite-only). The **`## Log`** section
  of `_core` is the append-only journal.

## Usage

Scaffold a loop for a goal:

```bash
python3 goaloop/scripts/build_goaloop.py "Research AI video editing tools"
# or into its own vault:
python3 goaloop/scripts/build_goaloop.py "Plan the Q3 launch" --dir ~/goals/q3-launch --max-loops 3
```

Then drive it with the skill: `/goaloop "Research AI video editing tools"`.

## Install

Symlink the skill into the Claude Code runtime so `/goaloop` resolves:

```bash
ln -s "$(pwd)/goaloop" ~/.claude/skills/goaloop
```

No dependencies beyond Python 3 stdlib, Obsidian, and the reference commands it
orchestrates (`/autoresearch`, `/research`, `/deep-research`, `/save`, `/wiki-query`,
`/wiki-lint`).

## How it works

- `goaloop/SKILL.md` is the operational entry point.
- `goaloop/references/kernel-map.md` maps each checkpoint to its best-practices principle.
- `goaloop/references/orchestration.md` is the per-checkpoint runbook and control flow.
- `goaloop/template/` holds the checkpoint bodies, the `core.md` index body, and the
  per-vault `CLAUDE.md`.
- `goaloop/scripts/build_goaloop.py` is the scaffolder (circle layout, control-plane hubs,
  cyclic gradient, collision-safe color groups, graph filter).
