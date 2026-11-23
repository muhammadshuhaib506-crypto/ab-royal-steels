import math, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

def text_path(fontfile, text, size, x0, baseline, tracking=0):
    f = TTFont(fontfile); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size / upm; x = x0; out = []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None: continue
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (sc, 0, 0, -sc, x, baseline))
        gs[g].draw(tp); out.append(pen.getCommands())
        x += gs[g].width * sc + tracking
    return ' '.join(out), x - tracking

# Mark: three interlaced diamonds
r = 50; sw = 10.5; gap = 4.2
import os
dx, dy = float(os.environ.get("DX","0.62")), float(os.environ.get("DY","1.42"))
centers = [(0, 0), (-dx, dy), (dx, dy)]
def diamond(cx, cy):
    cx, cy = cx * r, cy * r
    return [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
D = [diamond(*c) for c in centers]
def segs(p): return [(p[i], p[(i + 1) % 4]) for i in range(4)]
def inter(a, b):
    (x1, y1), (x2, y2) = a; (x3, y3), (x4, y4) = b
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9: return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    if 0 < t < 1 and 0 < u < 1: return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)), t
    return None
# crossings: list of (shapeA, segA, tA, shapeB, segB, point)
cross = []
for i in range(3):
    for j in range(i + 1, 3):
        for si, s in enumerate(segs(D[i])):
            for sj, t in enumerate(segs(D[j])):
                res = inter(s, t)
                if res: cross.append([i, si, res[1], j, sj, res[0]])
# alternate over/under along each perimeter, starting with top diamond
over = {}
def perim_order(k):
    lst = []
    for idx, c in enumerate(cross):
        if c[0] == k: lst.append((c[1] + c[2], idx))
        elif c[3] == k:
            s = segs(D[k])[c[4]]; p = c[5]
            L = math.dist(s[0], s[1]); tt = math.dist(s[0], p) / L
            lst.append((c[4] + tt, idx))
    return [idx for _, idx in sorted(lst)]
for k in (0, 1, 2):
    order = perim_order(k)
    # find a known assignment to anchor
    start = None
    for n, idx in enumerate(order):
        if idx in over: start = (n, over[idx] == k); break
    if start is None: start = (0, True)
    n0, isover = start
    for n, idx in enumerate(order):
        val = isover if (n - n0) % 2 == 0 else not isover
        if idx not in over:
            c = cross[idx]; other = c[3] if c[0] == k else c[0]
            over[idx] = k if val else other
masks = {0: [], 1: [], 2: []}
for idx, c in enumerate(cross):
    o = over[idx]; u = c[3] if o == c[0] else c[0]
    seg = segs(D[o])[c[1] if o == c[0] else c[4]]
    ang = math.degrees(math.atan2(seg[1][1] - seg[0][1], seg[1][0] - seg[0][0]))
    x, y = c[5]; L = sw * 1.25; Wd = sw + 2 * gap
    masks[u].append(f'<rect x="{x-L/2:.2f}" y="{y-Wd/2:.2f}" width="{L:.2f}" height="{Wd:.2f}" transform="rotate({ang:.2f} {x:.2f} {y:.2f})" fill="#000"/>')
minx = min(p[0] for d in D for p in d) - sw; maxx = max(p[0] for d in D for p in d) + sw
miny = min(p[1] for d in D for p in d) - sw; maxy = max(p[1] for d in D for p in d) + sw

def mark_svg(color, ox, oy, scale, uid):
    parts = []
    defs = []
    for k in range(3):
        pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in D[k])
        if masks[k]:
            defs.append(f'<mask id="{uid}m{k}" maskUnits="userSpaceOnUse" x="{minx-20}" y="{miny-20}" width="{maxx-minx+40}" height="{maxy-miny+40}"><rect x="{minx-20}" y="{miny-20}" width="{maxx-minx+40}" height="{maxy-miny+40}" fill="#fff"/>{"".join(masks[k])}</mask>')
            parts.append(f'<polygon points="{pts}" mask="url(#{uid}m{k})"/>')
        else:
            parts.append(f'<polygon points="{pts}"/>')
    g = f'<g transform="translate({ox:.2f} {oy:.2f}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="miter" stroke-miterlimit="10">{"".join(parts)}</g>'
    return ''.join(defs), g

def build(mark_c, word_c, sub_c, uid, mark_only=False):
    mh = maxy - miny; mw = maxx - minx
    H = 100.0; s = H / mh
    defs, g = mark_svg(mark_c, -minx * s, -miny * s, s, uid)
    if mark_only:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {mw*s:.1f} {H}" role="img" aria-label="AB Royal Steels mark"><defs>{defs}</defs>{g}</svg>'
    tx = mw * s + 22
    p1, end1 = text_path(SRC + 'mont700.ttf', 'AB ROYAL', 46, tx, 52, tracking=1.0)
    wcenter = (tx + end1) / 2
    p2, end2 = text_path(SRC + 'mont500.ttf', 'STEELS', 21, 0, 0, tracking=9.5)
    sx = wcenter - end2 / 2
    p2, _ = text_path(SRC + 'mont500.ttf', 'STEELS', 21, sx, 88, tracking=9.5)
    W = end1 + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H}" role="img" aria-label="AB Royal Steels">'
            f'<defs>{defs}</defs>{g}<path fill="{word_c}" d="{p1}"/><path fill="{sub_c}" d="{p2}"/></svg>')

SRC = sys.argv[1]; OUT = sys.argv[2]
open(OUT + 'logo-white.svg', 'w').write(build('#FFFFFF', '#FFFFFF', '#FFFFFF', 'w'))
open(OUT + 'logo-color.svg', 'w').write(build('#E31824', '#102B55', '#102B55', 'c'))
open(OUT + 'mark-white.svg', 'w').write(build('#FFFFFF', '', '', 'mw', True))
open(OUT + 'mark-red.svg', 'w').write(build('#E31824', '', '', 'mr', True))
print(len(cross), 'crossings', over)
