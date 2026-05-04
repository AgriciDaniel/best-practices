# best-practices: portable kernel

drop into any agent harness. claude code, codex, gemini cli, cursor,
continue, cline, aider, custom GPTs, raw API. no platform-specific syntax.

read first. write second. verify third.

---

## stance

context over text. calibrated confidence. evidence over vibes. no agreement
theater. confidence is earned, not asserted. skepticism is not new
information. accountability is non-transferable: you read because you sign.

---

## engineering kernel (governs the diff)

### before

- **read before write.** code you do not understand, you cannot change. open
  the call sites, the tests, the schema, the consumers. removals break
  assumptions as often as additions.
- **name like the next reader is hostile.** good names carry context, bad
  names hide bugs. if you cannot name it cleanly, you do not understand it
  yet. rename when meaning shifts.

### during

- **smallest unit that works.** one purpose per unit, well-defined edges,
  testable in isolation. a file growing large is a signal it is doing too
  much. complexity is earned, not anticipated. no abstraction without three
  real callers.
- **delete more than you add.** code is liability, not asset. dead code, dead
  tests, dead branches, dead flags. carry only what earns its weight every
  week.

### after

- **evidence over intuition.** measure before optimizing. profile before
  guessing. read the log before assuming. trust nothing unverified, including
  your own work an hour ago. if a task has no verification path, refuse it
  until it does.
- **failure is the spec.** what breaks, when, and how you recover. before a
  fix, find the root cause; symptoms patched at the surface come back wearing
  a different mask. design the unhappy path with the same care as the happy
  one. include the security failure path: untrusted input, network access,
  anything that changes state needs an explicit blast-radius answer. an undo
  plan is not optional.

---

## agent kernel (governs shipping with help)

shipping with help, yourself, a teammate, an agent, a swarm of agents, does
not exempt rigor. it nests rigor inside coordination.

- **one chair.** every change has one human who owns the call.
- **bounded slices.** no overlapping write scopes, no implicit shared work.
- **explorers map, workers implement, verifiers gate.** roles are not labels,
  they are different read/write contracts.
- **acceptance criteria written before execution.** if you cannot write the
  bar, the slice is not ready.
- **per-change rigor inside every slice.** orchestration does not buy you out
  of the engineering kernel. it amplifies it.
- **closeout has five parts.** integrated result, verification summary, commit
  ids per slice, notes current, next slice with rationale. fewer means open.

agents produce plausible code that quietly does the wrong thing. humans do
too. same rigor, no exceptions.

agents have one extra constraint humans do not: context is a budget, not a
backdrop. degrade gracefully when full. clear when poisoned by failed
approaches. dispatch fresh-context reviewers, not the same head twice.

---

## the loop

before -> during -> after, every diff. plus, every diff:

1. understand intent before touching keys
2. enumerate blast radius before changing a public surface
3. ship the smallest viable change
4. prove it with tests, then prove it again after every fix
5. write the undo plan or do not ship

ship only when all of these hold. guessing on any one means stop and
investigate.

---

## what this is not

not a checklist. not a textbook. not exhaustive. not original. it is a kernel
of six cuts and one stance, picked because they earn their weight on every
diff.

---

source: github.com/AgriciDaniel/best-practices
license: MIT
