import math

def ellipse_boundary(cx, cy, rx, ry, tx, ty):
    """Point on ellipse boundary along the direction from (cx,cy) toward (tx,ty)."""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return (cx, cy)
    t = 1.0 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return (cx + dx * t, cy + dy * t)

def point_toward(px, py, tx, ty, dist):
    """Point at distance `dist` from (px,py) along direction to (tx,ty)."""
    dx, dy = tx - px, ty - py
    n = math.hypot(dx, dy)
    if n == 0:
        return (px, py)
    return (px + dx / n * dist, py + dy / n * dist)

def text_width(s, size=13.5):
    return len(s) * size * 0.56

# ---------- Use cases ----------
usecases = {
    "A1": ("Register\nPublication", 300, 110),
    "A2": ("Approve\nCo-Authorship", 300, 232),
    "A3": ("Log Equipment\nExpense", 300, 354),
    "A4": ("Submit Grant\nProposal", 300, 476),
    "A5": ("View Fund\nBurn-Up Analytics", 300, 598),
    "C2": ("Export Analytics\nReport", 300, 720),
    "B1": ("Review Grant\nProposal", 630, 110),
    "B2": ("Resolve Authorship\nDispute", 630, 232),
    "B3": ("Monitor Audit\nLedger", 630, 354),
    "C1": ("Check Budget\nBalance", 630, 476),
}

def radii(label):
    lines = label.split("\n")
    w = max(text_width(l) for l in lines)
    rx = max(72, w / 2 + 18)
    ry = 30 if len(lines) == 1 else 40
    return rx, ry

node_r = {k: radii(v[0]) for k, v in usecases.items()}

actors = {
    "Faculty": ("Faculty\nResearcher", 90, 150),
    "Dean": ("Research\nDean", 90, 660),
}

# ---------- associations (actor -- use case), plain solid line ----------
associations = [
    ("Faculty", "A1"), ("Faculty", "A2"), ("Faculty", "A3"),
    ("Faculty", "A4"), ("Faculty", "A5"),
    ("Dean", "B1"), ("Dean", "B2"), ("Dean", "B3"), ("Dean", "A5"),
]

# ---------- include relationships (base -> included) ----------
includes = [("A3", "C1"), ("A4", "C1")]

# ---------- extend relationships (extension -> base) ----------
extends = [("C2", "A5")]

svg_parts = []
W, H = 900, 860
svg_parts.append(
    f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
    f'font-family="Helvetica, Arial, sans-serif">'
)
svg_parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')

# marker defs
svg_parts.append('''
<defs>
  <marker id="arrowOpen" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto">
    <path d="M0,0 L9,5 L0,10" fill="none" stroke="#333333" stroke-width="1.4"/>
  </marker>
</defs>
''')

# system boundary
bx0, by0, bx1, by1 = 178, 40, 760, 772
LEGEND_Y = by1 + 40
svg_parts.append(
    f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="10" ry="10" '
    f'fill="#f7f9fc" stroke="#3b5a8a" stroke-width="1.6"/>'
)
svg_parts.append(
    f'<text x="{(bx0+bx1)/2}" y="{by0+24}" text-anchor="middle" font-size="15" '
    f'font-weight="700" fill="#20365e">Faculty Research Grant &amp; Publication Tracker</text>'
)

# ---- draw associations first (under everything) ----
for a, u in associations:
    alabel, ax, ay = actors[a]
    ulabel, ux, uy = usecases[u]
    rx, ry = node_r[u]
    end = ellipse_boundary(ux, uy, rx, ry, ax, ay)
    start = point_toward(ax, ay, ux, uy, 34)  # start just below actor icon
    svg_parts.append(
        f'<line x1="{start[0]:.1f}" y1="{start[1]:.1f}" x2="{end[0]:.1f}" y2="{end[1]:.1f}" '
        f'stroke="#57657a" stroke-width="1.4"/>'
    )

# ---- include relationships ----
for base, inc in includes:
    blabel, bx, by = usecases[base]
    ilabel, ix, iy = usecases[inc]
    brx, bry = node_r[base]
    irx, iry = node_r[inc]
    p1 = ellipse_boundary(bx, by, brx, bry, ix, iy)
    p2raw = ellipse_boundary(ix, iy, irx, iry, bx, by)
    p2 = point_toward(p2raw[0], p2raw[1], bx, by, -10)  # pull back for arrowhead
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    svg_parts.append(
        f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
        f'stroke="#333333" stroke-width="1.4" stroke-dasharray="6,4" marker-end="url(#arrowOpen)"/>'
    )
    svg_parts.append(
        f'<rect x="{mx-38:.1f}" y="{my-17:.1f}" width="76" height="16" fill="#f7f9fc"/>'
        f'<text x="{mx:.1f}" y="{my-5:.1f}" text-anchor="middle" font-size="11.5" '
        f'font-style="italic" fill="#333333">&#171;include&#187;</text>'
    )

# ---- extend relationships ----
for ext, base in extends:
    elabel, ex, ey = usecases[ext]
    blabel, bx, by = usecases[base]
    erx, ery = node_r[ext]
    brx, bry = node_r[base]
    p1 = ellipse_boundary(ex, ey, erx, ery, bx, by)
    p2raw = ellipse_boundary(bx, by, brx, bry, ex, ey)
    p2 = point_toward(p2raw[0], p2raw[1], ex, ey, -10)
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    svg_parts.append(
        f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
        f'stroke="#333333" stroke-width="1.4" stroke-dasharray="6,4" marker-end="url(#arrowOpen)"/>'
    )
    svg_parts.append(
        f'<rect x="{mx-36:.1f}" y="{my-17:.1f}" width="72" height="16" fill="#f7f9fc"/>'
        f'<text x="{mx:.1f}" y="{my-5:.1f}" text-anchor="middle" font-size="11.5" '
        f'font-style="italic" fill="#333333">&#171;extend&#187;</text>'
    )

# ---- draw use case ellipses on top ----
for key, (label, x, y) in usecases.items():
    rx, ry = node_r[key]
    fill = "#eaf1ff" if key in ("C1", "C2") else "#ffffff"
    svg_parts.append(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx:.1f}" ry="{ry}" fill="{fill}" '
        f'stroke="#20365e" stroke-width="1.6"/>'
    )
    lines = label.split("\n")
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y - (n - 1) * 8 + i * 16 + 4
        svg_parts.append(
            f'<text x="{x}" y="{ty}" text-anchor="middle" font-size="13" fill="#16233f">{ln}</text>'
        )

# ---- draw actors (stick figures) ----
def draw_actor(cx, cy, label):
    parts = []
    head_r = 10
    parts.append(f'<circle cx="{cx}" cy="{cy-24}" r="{head_r}" fill="none" stroke="#20365e" stroke-width="1.8"/>')
    parts.append(f'<line x1="{cx}" y1="{cy-14}" x2="{cx}" y2="{cy+10}" stroke="#20365e" stroke-width="1.8"/>')
    parts.append(f'<line x1="{cx-16}" y1="{cy-4}" x2="{cx+16}" y2="{cy-4}" stroke="#20365e" stroke-width="1.8"/>')
    parts.append(f'<line x1="{cx}" y1="{cy+10}" x2="{cx-14}" y2="{cy+32}" stroke="#20365e" stroke-width="1.8"/>')
    parts.append(f'<line x1="{cx}" y1="{cy+10}" x2="{cx+14}" y2="{cy+32}" stroke="#20365e" stroke-width="1.8"/>')
    lines = label.split("\n")
    for i, ln in enumerate(lines):
        parts.append(
            f'<text x="{cx}" y="{cy+50+i*15}" text-anchor="middle" font-size="12.5" '
            f'font-weight="600" fill="#16233f">{ln}</text>'
        )
    return "".join(parts)

for key, (label, x, y) in actors.items():
    svg_parts.append(draw_actor(x, y, label))

# ---- legend ----
lx, ly = 40, LEGEND_Y
svg_parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+30}" y2="{ly}" stroke="#57657a" stroke-width="1.4"/>')
svg_parts.append(f'<text x="{lx+38}" y="{ly+4}" font-size="11.5" fill="#333">association</text>')
svg_parts.append(f'<line x1="{lx+150}" y1="{ly}" x2="{lx+180}" y2="{ly}" stroke="#333" stroke-width="1.4" stroke-dasharray="6,4" marker-end="url(#arrowOpen)"/>')
svg_parts.append(f'<text x="{lx+188}" y="{ly+4}" font-size="11.5" fill="#333">&#171;include&#187; / &#171;extend&#187; (dashed, directed)</text>')

svg_parts.append("</svg>")

with open("use-case-diagram.svg", "w") as f:
    f.write("".join(svg_parts))

print("SVG written.")
