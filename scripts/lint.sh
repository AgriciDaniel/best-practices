#!/usr/bin/env bash
# scripts/lint.sh — best-practices repo health check.
#
# enforces the rules the audit caught: zero em dashes, valid frontmatter
# under length budgets, valid SVG XML, no kernel drift across the four
# kernel-bearing files. exits non-zero on any failure.
#
# usage: bash scripts/lint.sh
# CI:    runs on push and PR via .github/workflows/lint.yml
# local: install as pre-commit hook with
#        ln -s ../../scripts/lint.sh .git/hooks/pre-commit

cd "$(dirname "$0")/.."

fail=0
pass() { printf "  ok   %s\n" "$1"; }
fail() { printf "  FAIL %s\n" "$1"; fail=1; }

echo "==> em dash sweep (no \\u2014 anywhere in .md or .svg)"
hits=$(grep -rln --include='*.md' --include='*.svg' -P "\x{2014}" . 2>/dev/null || true)
if [[ -n "$hits" ]]; then
  fail "em dashes found in:"
  echo "$hits" | sed 's/^/       /'
else
  pass "zero em dashes"
fi

echo "==> meow reference sweep"
hits=$(grep -rln -i --include='*.md' --include='*.svg' -E '(meow|meowmeow)' . 2>/dev/null || true)
if [[ -n "$hits" ]]; then
  fail "meow refs found in:"
  echo "$hits" | sed 's/^/       /'
else
  pass "zero meow references"
fi

echo "==> SVG XML validation"
python3 - <<'PY'
import sys, glob
import xml.etree.ElementTree as ET
errs = 0
for f in sorted(glob.glob('svg/*.svg')):
    try:
        ET.parse(f)
        print(f"  ok   {f}")
    except Exception as e:
        print(f"  FAIL {f}: {e}")
        errs += 1
sys.exit(1 if errs else 0)
PY
[[ $? -ne 0 ]] && fail=1

echo "==> frontmatter validation (SKILL.md, best-practices.md)"
python3 - <<'PY'
import re, sys
errs = 0
checks = [('SKILL.md', 200), ('best-practices.md', 250)]
for path, max_desc in checks:
    try:
        text = open(path).read()
    except FileNotFoundError:
        print(f"  FAIL {path}: missing"); errs += 1; continue
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        print(f"  FAIL {path}: no frontmatter block"); errs += 1; continue
    fm = m.group(1)
    if 'name:' not in fm:
        print(f"  FAIL {path}: missing name field"); errs += 1
    desc_m = re.search(r'description:\s*(.+)', fm)
    if not desc_m:
        print(f"  FAIL {path}: missing description"); errs += 1; continue
    desc = desc_m.group(1).strip()
    if len(desc) > max_desc:
        print(f"  FAIL {path}: description {len(desc)} chars (max {max_desc})")
        errs += 1
    else:
        print(f"  ok   {path}: description {len(desc)}/{max_desc} chars")
sys.exit(1 if errs else 0)
PY
[[ $? -ne 0 ]] && fail=1

echo "==> kernel drift check (six cuts present in all four kernel files)"
python3 - <<'PY'
import sys
files = ['README.md', 'AGENTS.md', 'SKILL.md', 'best-practices.md']
cuts = [
    'read before write',
    'name like the next reader is hostile',
    'smallest unit that works',
    'delete more than you add',
    'evidence over intuition',
    'failure is the spec',
]
errs = 0
for cut in cuts:
    missing = []
    for f in files:
        try:
            text = open(f).read().lower()
        except FileNotFoundError:
            missing.append(f"{f}(missing)"); continue
        if cut not in text:
            missing.append(f)
    if missing:
        print(f"  FAIL cut '{cut}' missing from: {', '.join(missing)}")
        errs += 1
if not errs:
    print("  ok   all six cuts present in all four kernel files")
sys.exit(1 if errs else 0)
PY
[[ $? -ne 0 ]] && fail=1

echo "==> README install path sanity (no raw.githubusercontent curl on a private repo)"
if grep -E 'curl[^|]*raw\.githubusercontent\.com' README.md > /dev/null 2>&1; then
  fail "README still uses curl against raw.githubusercontent.com (breaks on private repos)"
else
  pass "no curl-against-raw install commands in README"
fi

echo "==> link target sanity (per-cut anchors exist in README)"
python3 - <<'PY'
import sys, re
text = open('README.md').read()
expected = ['read', 'name', 'small', 'delete', 'evidence', 'failure']
missing = [a for a in expected if f'<a id="{a}"></a>' not in text]
if missing:
    print(f"  FAIL missing per-cut anchors: {missing}")
    sys.exit(1)
print("  ok   all six per-cut anchors present in README.md")
PY
[[ $? -ne 0 ]] && fail=1

echo
if [[ $fail -ne 0 ]]; then
  echo "lint FAILED"
  exit 1
fi
echo "lint passed"
