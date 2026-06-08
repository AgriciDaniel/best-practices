# Kernel map: best-practices to the 10 checkpoints

Source: the `best-practices` skill (github.com/AgriciDaniel/best-practices).
Kernel: `intent → read first → write second → verify third → (undo / loop)`.
Six cuts, three acts, one kernel, agents and humans same rigor.

| # | Checkpoint | Principle | Orchestrates | Feeds |
|---|------------|-----------|--------------|-------|
| 0 | Goal | intent. acceptance criteria written before execution | goaloop entry | goal, scope, success bar, constraints, blast radius |
| 1 | Read | act 1 read first. cut 1 read before write | `/autoresearch` or `/research` | run-log, `topics/<slug>/sources` |
| 2 | Map | cut 3 smallest unit that works. enumerate blast radius | `/wiki-query` | known vs missing, next smallest unit |
| 3 | Write | act 2 write second. cut 2 name like the next reader is hostile | `/save`, wiki-ingest | run-log, `topics/<slug>/concepts` |
| 4 | Verify | act 3 verify third. cut 5 evidence over intuition | `/deep-research`, `/wiki-lint` | verdicts. feedback to Write on fail |
| 5 | Gaps | cut 6 failure is the spec. root cause not symptom | analysis | gap list. feedback to Read if gaps remain |
| 6 | Prune | cut 4 delete more than you add | `/wiki-lint` orphans | dry-run manifest + archived candidates (archive-only, after approval) |
| 7 | Hot | the hot-cache pattern as live working memory | overwrite | recent facts, active threads, recent changes |
| 8 | Closeout | agent kernel: five-part closeout | synthesis | result, verification, artifact ids, notes current, next slice |
| 9 | Undo & Loop | an undo plan is not optional | decision | keep or roll back. met means exit, else loop to Goal |

## The control plane (Karpathy "LLM Wiki")
Four central nodes hold the loop's state, each linking every checkpoint: `_core` (index),
`_log` (append-only record), `_schema` (conventions), `_sources` (raw-layer index). Closeout
prepends to `_log`; Read notes new source sets in `_sources`.

## The three acts land on 1, 3, 4
Read first (1), write second (3), verify third (4). The other orbs are the cuts and the
agent kernel wrapped around those acts so the loop is safe to run repeatedly.

## The stance underneath all of it
Context over text. Calibrated confidence. Evidence over vibes. No agreement theater.
Confidence is earned, not asserted. Accountability is non-transferable: you read because
you sign. Agents produce plausible work that quietly does the wrong thing; humans do too;
same rigor, no exceptions.
