<p align="center">
  <img src="svg/banner.svg" alt="best-practices: read first. write second. verify third." width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/AgriciDaniel/meowmeow"><img src="https://img.shields.io/badge/built%20on-meow%20philosophy-B084CC?style=flat-square" alt="built on meow philosophy"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-36BCF7?style=flat-square" alt="MIT"/></a>
  <img src="https://img.shields.io/badge/voice-karpathy--terse-FF6B35?style=flat-square" alt="voice: karpathy-terse"/>
</p>

# best-practices

one kernel for shipping changes. one engineering layer underneath, one agent
layer on top. small enough to reread, dense enough to matter. no fluff, no
theater, no agreement for the sake of agreement.

read first. write second. verify third.

---

## the layers

<p align="center">
  <img src="svg/nest.svg" alt="meow philosophy contains agent kernel contains engineering kernel" width="640"/>
</p>

| layer              | governs       | where it lives                                              |
|--------------------|---------------|-------------------------------------------------------------|
| meow philosophy    | the stance    | [meowmeow](https://github.com/AgriciDaniel/meowmeow)        |
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
your own work an hour ago.

</td>
</tr>
<tr>
<td valign="top" width="56"><img src="svg/cut-06-failure.svg" width="44"/></td>
<td>

**failure is the spec.** what breaks, when, and how you recover. design the
unhappy path with the same care as the happy one. an undo plan is not
optional.

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

---

## meow philosophy (the stance)

context over text. calibrated confidence. evidence over vibes. no agreement
theater. confidence is earned, not asserted. skepticism is not new
information.

if you do not have the [meowmeow](https://github.com/AgriciDaniel/meowmeow)
trigger installed, install it. the philosophy is what makes the rest of this
file work. without it, the kernel becomes a checklist, and a checklist is
ceremony, not rigor.

---

## how to use

drop the file into your agent of choice. one front door, three install paths.

### claude code

```bash
git clone https://github.com/AgriciDaniel/best-practices.git ~/.claude/best-practices
ln -s ~/.claude/best-practices/README.md ~/.claude/CLAUDE.md.d/best-practices.md
```

or paste the engineering kernel section into your `CLAUDE.md` directly.

### cursor / continue / cline / aider

paste the engineering kernel and the agent kernel into your rules file:

- cursor: `.cursor/rules/best-practices.md`
- continue: `.continuerules`
- cline: `.clinerules`
- aider: `.aider.conf.yml` rules section

### portable

`AGENTS.md` is the platform-neutral version of this kernel, designed to drop
into any agent harness with no claude-code-specific syntax.

### project-level

if a project needs the kernel as a constraint, add it as `AGENTS.md` at the
repo root. agents read it. humans read it. one source.

---

## what this is not

- not a checklist. checklists rot. kernels compress.
- not a textbook. textbooks are for things you forget. this is for things you
  use.
- not exhaustive. exhaustive lists are the enemy of rereading. six cuts is the
  point.
- not original in the sense of inventing axioms. original in the sense of
  picking the load-bearing few and naming them clearly.

---

## license

MIT. fork it, rewrite it, ship it under your name. attribution appreciated,
not required.

---

<p align="center">
  <sub>built by <a href="https://github.com/AgriciDaniel">@AgriciDaniel</a> · same kernel as <a href="https://github.com/AgriciDaniel/meowmeow">meowmeow</a> · part of the same family</sub>
</p>
