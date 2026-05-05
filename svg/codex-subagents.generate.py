#!/usr/bin/env python3
"""Generate the Codex subagents SVG diagram."""
from pathlib import Path


W = 1000
H = 480
FONT = "ui-monospace, SFMono-Regular, Menlo, monospace"


def text(x, y, value, size=12, fill="#c9d1d9", weight=None, anchor=None):
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'font-family="{FONT}"',
        f'font-size="{size}"',
        f'fill="{fill}"',
    ]
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    return f"<text {' '.join(attrs)}>{value}</text>"


def rect(x, y, w, h, stroke, fill="none", rx=10, width=1.5):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'stroke="{stroke}" stroke-width="{width}" fill="{fill}"/>'
    )


def line(x1, y1, x2, y2, stroke="#FF6B35", width=2, arrow=False, dash=None):
    attrs = [
        f'x1="{x1}"',
        f'y1="{y1}"',
        f'x2="{x2}"',
        f'y2="{y2}"',
        f'stroke="{stroke}"',
        f'stroke-width="{width}"',
    ]
    if arrow:
        attrs.append('marker-end="url(#cs-arrow)"')
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    return f"<line {' '.join(attrs)}/>"


def node(x, y, w, h, title, lines, color):
    cx = x + w / 2
    parts = [rect(x, y, w, h, color)]
    parts.append(text(cx, y + 28, title, 14, color, "700", "middle"))
    for i, item in enumerate(lines):
        parts.append(text(cx, y + 52 + i * 16, item, 10, "#7d8590", None, "middle"))
    return "\n  ".join(parts)


def generate():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cs-title cs-desc">',
        '  <title id="cs-title">codex subagents: one chair, bounded roles, summarized return</title>',
        '  <desc id="cs-desc">A dark diagram showing a main codex thread delegating bounded work to explorer, worker, and verifier subagents, then receiving summaries for integrated closeout.</desc>',
        f'  <rect width="{W}" height="{H}" fill="#0d1117"/>',
        "  <defs>",
        '    <marker id="cs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#FF6B35"/>',
        "    </marker>",
        "  </defs>",
        f"  {text(32, 36, 'codex subagents: explicit fan-out. bounded work. summarized return.', 13, '#7d8590')}",
        f"  {rect(360, 64, 280, 72, '#FFD700', rx=12, width=2)}",
        f"  {text(500, 94, 'main thread', 15, '#FFD700', '700', 'middle')}",
        f"  {text(500, 114, 'requirements &#183; decisions &#183; integration', 10, '#a39055', None, 'middle')}",
        f"  {line(500, 136, 500, 164, arrow=True)}",
        f"  {rect(80, 166, 840, 54, '#36BCF7', rx=12, width=1.5)}",
        f"  {text(500, 190, 'acceptance bar written before spawn', 13, '#36BCF7', '700', 'middle')}",
        f"  {text(500, 208, 'one prompt names the slices, return format, and whether to wait', 10, '#7aa9c2', None, 'middle')}",
        f"  {line(210, 220, 210, 252, arrow=True)}",
        f"  {line(500, 220, 500, 252, arrow=True)}",
        f"  {line(790, 220, 790, 252, arrow=True)}",
        "  " + node(70, 256, 280, 86, "explorer", ["read-only map", "call sites &#183; tests &#183; unknowns"], "#B084CC"),
        "  " + node(360, 256, 280, 86, "worker", ["single slice", "disjoint write scope"], "#36BCF7"),
        "  " + node(650, 256, 280, 86, "verifier", ["fresh context", "bugs &#183; security &#183; missing tests"], "#FF6B35"),
        f"  {line(210, 342, 210, 374, '#B084CC', 1.5)}",
        f"  {line(500, 342, 500, 374, '#36BCF7', 1.5)}",
        f"  {line(790, 342, 790, 374, '#FF6B35', 1.5)}",
        f"  {line(210, 374, 790, 374, '#7d8590', 1.5)}",
        f"  {line(500, 374, 500, 398, arrow=True)}",
        f"  {rect(280, 406, 440, 36, '#FFD700', rx=10, width=2)}",
        f"  {text(500, 429, 'summaries in. claims verified. closeout complete.', 12, '#FFD700', '700', 'middle')}",
        f"  {text(500, 456, 'do not fan out by default. ask explicitly. keep the main thread clean.', 10, '#7d8590', None, 'middle')}",
        "</svg>",
        "",
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    output = Path(__file__).with_name("codex-subagents.svg")
    svg = generate()
    output.write_text(svg, encoding="utf-8")
    print(f"Generated: {output} ({len(svg.encode('utf-8')):,} bytes)")
