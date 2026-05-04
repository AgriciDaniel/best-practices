<p align="center">
  <img src="svg/banner.svg" alt="best-practices: read first. write second. verify third." width="100%"/>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-36BCF7?style=flat-square" alt="MIT"/></a>
  <img src="https://img.shields.io/badge/voice-karpathy--terse-FF6B35?style=flat-square" alt="voice: karpathy-terse"/>
  <img src="https://img.shields.io/badge/six%20cuts-three%20acts-B084CC?style=flat-square" alt="six cuts · three acts"/>
</p>

# best-practices

one kernel for shipping changes. one engineering layer underneath, one agent
layer on top. small enough to reread, dense enough to matter. no fluff, no
theater, no agreement for the sake of agreement.

read first. write second. verify third.

---

## the layers

<p align="center">
  <img src="svg/nest.svg" alt="the stance contains the agent kernel contains the engineering kernel" width="640"/>
</p>

| layer              | governs       | where it lives                                              |
|--------------------|---------------|-------------------------------------------------------------|
| the stance         | how you think | [the stance](#the-stance)                                   |
| agent kernel       | the team      | [shipping-rules.md](shipping-rules.md)                      |
| engineering kernel | the diff      | this README                                                 |

each layer assumes the one below. flatten them and the hierarchy collapses.

---

## engineering kernel

six cuts. three acts. these are the rules that make any of the rest possible.
shipping-rules sits on top.

### before

<table>
<tr>
<td valign="top" width="56"><img src="svg/cut-01-read.svg" width="44"/></td>
<td>

**read before write.** code you do not understand, you cannot change. open the
call sites, the tests, the schema, the consumers. removals break assumptions
as often as additions.

</td>
</tr>
<tr>
<td valign="top" width="56"><img src="svg/cut-02-name.svg" width="44"/></td>
<td>

**name like the next reader is hostile.** good names carry context, bad names
hide bugs. if you cannot name it cleanly, you do not understand it yet. rename
when meaning shifts.

</td>
</tr>
</table>

### during

<table>
<tr>
<td valign="top" width="56"><img src="svg/cut-03-small.svg" width="44"/></td>
<td>

**smallest unit that works.** one purpose per unit, well-defined edges,
testable in isolation. a file growing large is a signal it is doing too much.
complexity is earned, not anticipated. no abstraction without three real
callers.

</td>
</tr>
<tr>
<td valign="top" width="56"><img src="svg/cut-04-delete.svg" width="44"/></td>
<td>

**delete more than you add.** code is liability, not asset. dead code, dead
tests, dead branches, dead flags. carry only what earns its weight every week.

</td>
</tr>
</table>

### after

<table>
<tr>
<td valign="top" width="56"><img src="svg/cut-05-evidence.svg" width="44"/></td>
<td>

**evidence over intuition.** measure before optimizing. profile before
guessing. read the log before assuming. trust nothing unverified, including
your own work an hour ago. before a fix, find the root cause. if a task has
no verification path, refuse it until it does.

</td>
</tr>
<tr>
<td valign="top" width="56"><img src="svg/cut-06-failure.svg" width="44"/></td>
<td>

**failure is the spec.** what breaks, when, and how you recover. design the
unhappy path with the same care as the happy one. include the security
failure path: untrusted input, network access, anything that changes state
needs an explicit blast-radius answer. an undo plan is not optional.

</td>
</tr>
</table>

these six are the kernel. internalize them and the rest of the file reads as
the consequences, not the rules.

---

## agent kernel

shipping with help (yourself, a teammate, an agent, a swarm of agents) does
not exempt rigor. it nests rigor inside coordination.

the full text lives in [shipping-rules.md](shipping-rules.md). the kernel is:

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
approaches. dispatch fresh-context reviewers, not the same head twice. the
reviewer who never wrote the code spots more than the writer who just
finished it.

---

## the stance

context over text. calibrated confidence. evidence over vibes. no agreement
theater. confidence is earned, not asserted. skepticism is not new
information. accountability is non-transferable: you read because you sign.

the stance is what makes the rest of this file work. without it, the kernel
becomes a checklist, and a checklist is ceremony, not rigor. the rules are
load-bearing only when the person reading them is already willing to be
wrong in public.

---

## install

four paths. pick one or stack them.

### claude code: skill (auto-loads on relevant work)

```bash
git clone https://github.com/AgriciDaniel/best-practices.git \
  ~/.claude/skills/best-practices
```

claude code reads `SKILL.md` and auto-injects the kernel when you start a
non-trivial diff, plan a change, review code, or debug. no manual trigger.

### claude code: slash command (explicit invocation)

```bash
mkdir -p ~/.claude/commands
curl -sL https://raw.githubusercontent.com/AgriciDaniel/best-practices/main/best-practices.md \
  -o ~/.claude/commands/best-practices.md
```

then `/best-practices` injects the full kernel, or `/best-practices evidence`
injects just the evidence cut. nine sections addressable: `stance`,
`engineering`, `agent`, `loop`, `read`, `name`, `small`, `delete`, `evidence`,
`failure`.

### cursor / continue / cline / aider / codex / gemini cli

paste `AGENTS.md` (the portable kernel) into your rules file. no
claude-code-specific syntax.

- cursor: `.cursor/rules/best-practices.md`
- continue: `.continuerules`
- cline: `.clinerules`
- aider: `.aider.conf.yml` rules section
- codex / gemini cli / generic: drop in as `AGENTS.md` at repo root

### project-level

add `AGENTS.md` at the repo root. agents read it. humans read it. one source.

---

## how it composes

- needs **enforcement** for adversarial agents (rationalization guards, iron
  laws, red-flag stop-words) -> stack [obra/superpowers](https://github.com/obra/superpowers)
- needs **iron-law TDD** -> `superpowers:test-driven-development`
- needs **debugging discipline** -> `superpowers:systematic-debugging`
- needs **parallel-agent SOP** -> `superpowers:dispatching-parallel-agents`

this kernel is the meditation. those are the enforcement. compose, do not
substitute.

---

## what this is

a meditation. six axioms compressed into something you reread on a monday
morning when you forgot why you ship the way you ship. it works for a person
or an agent who already wants to be rigorous.

## what this is not

- **not a checklist.** checklists rot. kernels compress.
- **not a textbook.** textbooks are for things you forget. this is for things
  you use.
- **not exhaustive.** exhaustive lists are the enemy of rereading. six cuts is
  the point.
- **not an enforcement layer.** there is no iron-law framing here, no
  rationalization-blocking tables, no red-flag stop-words. the kernel will not
  defend itself against an agent that decides to skip steps. for that, compose
  with [obra/superpowers](https://github.com/obra/superpowers) or another
  enforcement-grade ruleset.
- **not a substitute for TDD discipline.** cuts 5 and 6 imply tests, they do
  not mandate red-green-refactor. if you need iron-law TDD, install the
  superpowers `test-driven-development` skill on top of this kernel.
- **not original in the sense of inventing axioms.** original in the sense of
  picking the load-bearing few and naming them clearly.

---

## license

MIT. fork it, rewrite it, ship it under your name. attribution appreciated,
not required.

---

<p align="center">
  <sub>built by <a href="https://github.com/AgriciDaniel">@AgriciDaniel</a> · read first. write second. verify third.</sub>
</p>
