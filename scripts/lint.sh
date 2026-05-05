#!/usr/bin/env bash
# scripts/lint.sh — best-practices repo health check.
#
# enforces the rules the audits caught:
#   - zero em dashes anywhere
#   - zero meow references
#   - all SVGs valid XML
#   - SKILL.md description under 200 chars, slash command under 250
#   - all six kernel cuts present in all four kernel-bearing files
#   - no curl-against-raw install commands in README
#   - all per-cut anchors present in README
#   - workflow has explicit `permissions:` block (defense in depth)
#   - all `uses:` action references SHA-pinned (40 hex chars)
#   - .gitignore covers common secret-file patterns
#
# usage: bash scripts/lint.sh
# CI:    runs on push and PR via .github/workflows/lint.yml
# local: install as pre-commit hook with
#        ln -s ../../scripts/lint.sh .git/hooks/pre-commit
#
# strict mode notes: -u catches unset vars, pipefail catches mid-pipe failures.
# we deliberately do NOT use -e because we want to collect every failure and
# report all of them in a single run, not fail-fast on the first.

set -uo pipefail

cd "$(dirname "$0")/.."

fail=0
pass() { printf "  ok   %s\n" "$1"; }
flag() { printf "  FAIL %s\n" "$1"; fail=1; }

echo "==> em dash sweep (no \\u2014 anywhere in .md or .svg)"
hits=$(grep -rln --include='*.md' --include='*.svg' -P "\x{2014}" . 2>/dev/null || true)
if [[ -n "$hits" ]]; then
  flag "em dashes found in:"
  echo "$hits" | sed 's/^/       /'
else
  pass "zero em dashes"
fi

echo "==> meow reference sweep"
hits=$(grep -rln -i --include='*.md' --include='*.svg' -E '(meow|meowmeow)' . 2>/dev/null || true)
if [[ -n "$hits" ]]; then
  flag "meow refs found in:"
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
rc=$?
[[ $rc -ne 0 ]] && fail=1

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
rc=$?
[[ $rc -ne 0 ]] && fail=1

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
rc=$?
[[ $rc -ne 0 ]] && fail=1

echo "==> README install path sanity (no raw.githubusercontent curl on a private repo)"
if grep -E 'curl[^|]*raw\.githubusercontent\.com' README.md > /dev/null 2>&1; then
  flag "README still uses curl against raw.githubusercontent.com (breaks on private repos)"
else
  pass "no curl-against-raw install commands in README"
fi

echo "==> link target sanity (per-cut anchors exist in README)"
python3 - <<'PY'
import sys
text = open('README.md').read()
expected = ['read', 'name', 'small', 'delete', 'evidence', 'failure']
missing = [a for a in expected if f'<a id="{a}"></a>' not in text]
if missing:
    print(f"  FAIL missing per-cut anchors: {missing}")
    sys.exit(1)
print("  ok   all six per-cut anchors present in README.md")
PY
rc=$?
[[ $rc -ne 0 ]] && fail=1

echo "==> CI workflow security (permissions block + SHA-pinned actions)"
python3 - <<'PY'
import sys, re, glob
errs = 0
for wf in sorted(glob.glob('.github/workflows/*.yml')):
    text = open(wf).read()
    if 'permissions:' not in text:
        print(f"  FAIL {wf}: missing top-level or job-level permissions: block")
        errs += 1
    uses_lines = re.findall(r'uses:\s*([^\s#]+)', text)
    for ref in uses_lines:
        # docker-style local references (./path or docker://) are exempt
        if ref.startswith('.') or ref.startswith('docker://'):
            continue
        # require <owner>/<repo>@<40-hex-sha>
        if not re.match(r'^[\w.-]+/[\w.-]+@[0-9a-f]{40}$', ref):
            print(f"  FAIL {wf}: action '{ref}' is not pinned to a 40-char commit SHA")
            errs += 1
    if errs == 0:
        print(f"  ok   {wf}: permissions present, all actions SHA-pinned")
sys.exit(1 if errs else 0)
PY
rc=$?
[[ $rc -ne 0 ]] && fail=1

echo "==> .gitignore covers common secret-file patterns"
python3 - <<'PY'
import sys
required = ['.env', '*.pem', '*.key', 'id_rsa', '.aws/', 'credentials.json']
try:
    text = open('.gitignore').read()
except FileNotFoundError:
    print("  FAIL .gitignore is missing")
    sys.exit(1)
missing = [p for p in required if p not in text]
if missing:
    print(f"  FAIL .gitignore missing patterns: {missing}")
    sys.exit(1)
print("  ok   .gitignore covers common secret-file patterns")
PY
rc=$?
[[ $rc -ne 0 ]] && fail=1

echo
if [[ $fail -ne 0 ]]; then
  echo "lint FAILED"
  exit 1
fi
echo "lint passed"
