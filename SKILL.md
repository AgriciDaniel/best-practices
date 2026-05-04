---
name: best-practices
description: Use when starting a non-trivial code change, planning a diff, reviewing a pull request, debugging a bug, shipping with AI agents, or auditing a slice of work for rigor. Loads the six-cut engineering kernel (read first, write second, verify third), the agent kernel for parallel work, and the stance that makes both load-bearing.
license: MIT
---

# best-practices

read first. write second. verify third.

a meditation. six axioms compressed into something you reread before shipping.
this skill loads the kernel. it does not enforce it. for enforcement, compose
with `obra/superpowers`.

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
  unverified. before a fix, find the root cause. if a task has no verification
  path, refuse it until it does.
- **failure is the spec.** include the security failure path: untrusted input,
  network access, state changes need an explicit blast-radius answer. an undo
  plan is not optional.

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

## the loop

every diff:

1. understand intent before touching keys
2. enumerate blast radius before changing a public surface
3. ship the smallest viable change
4. prove it with tests, prove it again after every fix
5. write the undo plan or do not ship

guessing on any one means stop and investigate.

## composition

- needs **enforcement** for adversarial agents -> add `obra/superpowers`
- needs **iron-law TDD** -> add `superpowers/test-driven-development`
- needs **debugging discipline** -> add `superpowers/systematic-debugging`
- needs **parallel-agent SOP** -> add `superpowers/dispatching-parallel-agents`

this skill is the meditation. those are the enforcement.

## reference

full prose, rationale, and the agent kernel detail (per-change + orchestration
rules) live in the README and `shipping-rules.md` of this repo. this SKILL.md
is the compressed loadable form.

source: github.com/AgriciDaniel/best-practices
