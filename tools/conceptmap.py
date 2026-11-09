"""Draw the concept graph as a page: docs/concept-map.md.

Two levels.

  the map    every page as a box, in reading order, with a line to each page
             it depends on — from concepts.yml

  the zoom   click a box and a second, granular network opens: the concepts
             INSIDE that page and how they depend on each other — from
             inside.yml, which is hand-authored

The layout is computed here, in Python, not in the browser. That is
deliberate: there is no JavaScript on this page at all. Coordinates are
arithmetic that can be checked here, and every interaction — hover to light
up a box's own lines, click to open a zoom — is CSS `:hover` and `:target`.

    python3 tools/conceptmap.py          report, write nothing
    python3 tools/conceptmap.py --write  regenerate the page

No line in either picture ever points upward. In the map that is the site's
reading order, enforced by tools/conceptcheck.py. In a zoom it is the order
the page itself explains things in, which is the same promise one level down.

index.md is left out: a prerequisite for nothing, connected to everything.
"""

import re
import sys
import pathlib
import collections

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "concept-map.md"

NODE_W, NODE_H = 170, 40          # a page box, on the map
GAP_X, GAP_Y = 20, 16
PER_ROW = 4
LABEL_H = 28
BAND_GAP = 40
MARGIN = 20

ZW, ZH = 152, 38                  # a concept box, inside a zoom
ZGX, ZGY = 18, 22
ZPER_ROW = 4


# --------------------------------------------------------------------------
# data

def load():
    """Pages in reading order, their part, and the curated dependencies."""
    pages_data = yaml.safe_load((ROOT / "concepts.yml").read_text())["pages"]
    nav = (ROOT / "mkdocs.yml").read_text().split("\nnav:", 1)[1]
    order = []
    for m in re.finditer(r"^\s+- .+?: ([a-z0-9/-]+\.md)\s*$", nav, re.M):
        if m.group(1) not in order:
            order.append(m.group(1))
    pages = [p for p in order if p in pages_data and p != "index.md"]
    bands = collections.OrderedDict()
    for p in pages:
        bands.setdefault(pages_data[p]["part"], []).append(p)
    edges = []
    for p in pages:
        for n in pages_data[p].get("needs") or []:
            if n in pages_data and n != "index.md":
                edges.append((n, p))
    f = ROOT / "inside.yml"
    insides = yaml.safe_load(f.read_text())["pages"] if f.exists() else {}
    return pages_data, pages, bands, edges, insides


def url(path):
    """Final site URL, relative to /concept-map/ (use_directory_urls is on)."""
    return "../" + path[:-3].replace("/index", "/") + "/"


def slug(path):
    return path[:-3].replace("/", "-")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                  .replace('"', "&quot;").replace("'", "&#39;"))


def wrap(title, limit):
    """At most two lines, because a third does not fit in a box this high."""
    lines, cur = [], ""
    for w in title.split():
        if len(cur) + len(w) + 1 <= limit or not cur:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]
        if len(lines[1]) > limit + 3:
            lines[1] = lines[1][:limit + 2].rstrip() + "…"
    return lines


def label(x, y, w, h, lines, size):
    cx, out = x + w / 2, []
    ys = [y + h / 2 + 4] if len(lines) == 1 else [y + h / 2 - 4, y + h / 2 + 10]
    for line, ty in zip(lines, ys):
        out.append(f'<text class="cm-label" x="{cx:g}" y="{ty:g}" font-size="{size}" '
                   f'text-anchor="middle">{esc(line)}</text>')
    return "".join(out)


# --------------------------------------------------------------------------
# the map

def port(box, col, row):
    """Where along a box's edge a line leaves or arrives.

    Not the centre. Every line leaving from the same point makes one thick
    stripe that says nothing about how many there are, and two boxes in the
    same column make a vertical indistinguishable from a box border. So the
    attachment point is spread by the column at the other end, and nudged by
    that end's row to separate the ties.
    """
    frac = 0.22 + 0.56 * col / (PER_ROW - 1)
    return box[0] + NODE_W * frac + (row % 3 - 1) * 5


def curve(src, dst):
    """A dependency, drawn downward. src and dst are (x, y, column, row)."""
    if dst[1] > src[1]:
        x1, y1 = port(src, dst[2], dst[3]), src[1] + NODE_H
        x2, y2 = port(dst, src[2], src[3]), dst[1]
        dy = (y2 - y1) / 2
        return f"M{x1:g},{y1:g} C{x1:g},{y1 + dy:g} {x2:g},{y2 - dy:g} {x2:g},{y2:g}"
    # Same row: both boxes sit at one height, so dip below them in a shallow
    # U. Anything else here draws a loop, which reads as a knot.
    x1, x2 = src[0] + NODE_W * 0.7, dst[0] + NODE_W * 0.3
    y = src[1] + NODE_H
    sag = 20 + 6 * ((dst[0] - src[0]) / (NODE_W + GAP_X) - 1)
    return f"M{x1:g},{y:g} C{x1:g},{y + sag:g} {x2:g},{y + sag:g} {x2:g},{y:g}"


def the_map(data, bands, edges, insides):
    """Every page as a box, parts as horizontal bands, every edge drawn."""
    inner = PER_ROW * NODE_W + (PER_ROW - 1) * GAP_X
    pos, band_of, band_box, y = {}, {}, [], MARGIN
    for bi, (name, pages) in enumerate(bands.items()):
        rows = -(-len(pages) // PER_ROW)
        top = y
        row_no = sum(-(-len(v) // PER_ROW) for v in list(bands.values())[:bi])
        y += LABEL_H
        for i, p in enumerate(pages):
            r, c = divmod(i, PER_ROW)
            n = min(PER_ROW, len(pages) - r * PER_ROW)
            row_w = n * NODE_W + (n - 1) * GAP_X
            x = MARGIN + (inner - row_w) / 2 + c * (NODE_W + GAP_X)
            pos[p] = (x, y + r * (NODE_H + GAP_Y), c, row_no + r)
            band_of[p] = bi
        y += rows * NODE_H + (rows - 1) * GAP_Y
        band_box.append((name, top, len(pages)))
        y += BAND_GAP
    w, h = inner + 2 * MARGIN, y - BAND_GAP + MARGIN

    paths, incident = [], collections.defaultdict(list)
    for s, t in edges:
        d = curve(pos[s], pos[t])
        paths.append(f'<path class="cm-edge" d="{d}"/>')
        incident[s].append(d)
        incident[t].append(d)

    out = [f'<svg class="cm-svg" viewBox="0 0 {w:g} {h:g}" role="group" '
           f'aria-label="Every written page as a box, grouped into parts, with '
           f'{len(edges)} dependency lines. No line points upward.">']
    out += paths
    # Part names go ON TOP of the lines, on opaque chips: underneath, a dozen
    # dependencies cross the words and the label stops being readable.
    for name, top, n in band_box:
        text = f"{name.upper()} · {n}"
        out.append(
            f'<rect fill="var(--md-default-bg-color)" x="{MARGIN - 4}" '
            f'y="{top + 2}" width="{len(text) * 10.5 * 0.52 + 10:.0f}" height="16"/>'
            f'<text class="cm-band" x="{MARGIN}" y="{top + 13}" font-size="10.5">'
            f'{esc(name.upper())} <tspan class="cm-count">· {n}</tspan></text>')
    for p, (x, yy, _c, _r) in pos.items():
        title = data[p]["title"]
        zoom = p in insides
        href = f"#zoom-{slug(p)}" if zoom else url(p)
        note = ("open the concepts inside it" if zoom
                else f'{len(data[p].get("needs") or [])} prerequisite(s)')
        # Each box carries hidden COPIES of its own lines. CSS cannot select
        # "the line ending where I am pointing", so the box owns them.
        halo = "".join(f'<path class="cm-halo" d="{d}"/>' for d in incident[p])
        out.append(
            f'<g class="cm-node{" cm-has-zoom" if zoom else ""}">'
            f'<title>{esc(title)} — {note}</title>{halo}<a href="{href}">'
            f'<rect class="cm-box" x="{x:g}" y="{yy:g}" width="{NODE_W}" '
            f'height="{NODE_H}" rx="5"/>'
            f'{label(x, yy, NODE_W, NODE_H, wrap(title, 23), 11.5)}</a></g>')
    out.append("</svg>")
    return "".join(out)


# --------------------------------------------------------------------------
# a zoom

def layers(nodes):
    """Longest path from a root, so a box always sits below everything it needs."""
    need = {n["id"]: [i for i in (n.get("needs") or [])] for n in nodes}
    depth, seen = {}, set()

    def walk(i):
        if i in depth:
            return depth[i]
        if i in seen:                      # a cycle would be an authoring bug
            raise ValueError(f"inside.yml: '{i}' depends on itself")
        seen.add(i)
        depth[i] = 1 + max((walk(j) for j in need[i]), default=-1)
        return depth[i]

    return {n["id"]: walk(n["id"]) for n in nodes}


def zoom(path, data, entry):
    """The concepts inside one page, laid out by how deep they sit."""
    nodes = entry["inside"]
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        for d in n.get("needs") or []:
            if d not in by_id:
                raise ValueError(f"inside.yml ({path}): '{n['id']}' needs unknown '{d}'")
    depth = layers(nodes)

    inner = ZPER_ROW * ZW + (ZPER_ROW - 1) * ZGX
    pos, y = {}, MARGIN
    for d in sorted(set(depth.values())):
        tier = [n["id"] for n in nodes if depth[n["id"]] == d]
        for r in range(-(-len(tier) // ZPER_ROW)):
            row = tier[r * ZPER_ROW:(r + 1) * ZPER_ROW]
            row_w = len(row) * ZW + (len(row) - 1) * ZGX
            for c, i in enumerate(row):
                pos[i] = (MARGIN + (inner - row_w) / 2 + c * (ZW + ZGX), y)
            y += ZH + ZGY
    w, h = inner + 2 * MARGIN, y - ZGY + MARGIN

    paths, incident = [], collections.defaultdict(list)
    for n in nodes:
        for dep in n.get("needs") or []:
            (x1, y1), (x2, y2) = pos[dep], pos[n["id"]]
            x1, x2 = x1 + ZW / 2, x2 + ZW / 2
            y1, y2 = y1 + ZH, y2
            dy = (y2 - y1) / 2
            d = (f"M{x1:g},{y1:g} C{x1:g},{y1 + dy:g} "
                 f"{x2:g},{y2 - dy:g} {x2:g},{y2:g}")
            paths.append(f'<path class="cm-edge" d="{d}"/>')
            incident[dep].append(d)
            incident[n["id"]].append(d)

    out = [f'<svg class="cm-svg cm-zoomsvg" viewBox="0 0 {w:g} {h:g}" role="group" '
           f'aria-label="The {len(nodes)} concepts inside {esc(data[path]["title"])}, '
           f'with a line from each to the ones it needs first.">']
    out += paths
    for n in nodes:
        x, yy = pos[n["id"]]
        halo = "".join(f'<path class="cm-halo" d="{d}"/>' for d in incident[n["id"]])
        body = (f'<rect class="cm-box" x="{x:g}" y="{yy:g}" width="{ZW}" '
                f'height="{ZH}" rx="5"/>'
                f'{label(x, yy, ZW, ZH, wrap(n["label"], 21), 11)}')
        if n.get("page"):
            body = f'<a href="{url(n["page"])}">{body}</a>'
        out.append(f'<g class="cm-node"><title>{esc(n["note"])}'
                   f'{"  →  " + esc(data[n["page"]]["title"]) if n.get("page") else ""}'
                   f'</title>{halo}{body}</g>')
    out.append("</svg>")
    return "".join(out), len(nodes), len(paths)


# --------------------------------------------------------------------------

def build():
    data, pages, bands, edges, insides = load()
    m = the_map(data, bands, edges, insides)

    zooms = []
    for p in pages:
        if p not in insides:
            continue
        svg, n, e = zoom(p, data, insides[p])
        zooms.append(
            f'<section class="cm-zoom" id="zoom-{slug(p)}">'
            f'<p class="cm-zoomhead"><strong>Inside {esc(data[p]["title"])}</strong> — '
            f'{n} concepts, {e} lines. A box with a link opens the page that '
            f'explains it properly. <a href="{url(p)}">Open the page</a> · '
            f'<a href="#the-map">Back to the map</a></p>{svg}</section>')

    body = f"""---
tier: meta
description: Every page on the site as a box, with a line to each page you need first — and a second, granular network inside each one.
---

<!-- GENERATED by tools/conceptmap.py from concepts.yml and inside.yml. Do not
     edit by hand: run `python3 tools/conceptmap.py --write` instead. -->

# The concept map

Every page on the site, with a line to each page you have to read first. The
menu down the side can only be a list; this is the shape underneath it.

**Hover a box** to light up its own lines. **Click one** to open the page —
or, where the zoom exists, the granular network of concepts inside it.

<figure class="cm-fig" id="the-map">{m}</figure>

{"".join(zooms)}
"""
    return body, len(pages), len(edges), len(zooms)


def main():
    body, npages, nedges, nzooms = build()
    old = PAGE.read_text() if PAGE.exists() else ""
    if "--write" in sys.argv:
        PAGE.write_text(body)
        print(f"concept map: written — {npages} pages, {nedges} edges, "
              f"{nzooms} zoom(s)")
        return 0
    print(f"concept map: {npages} pages, {nedges} edges, {nzooms} zoom(s) — "
          f"{'up to date' if body == old else 'OUT OF DATE, re-run with --write'}")
    return 0 if body == old else 1


if __name__ == "__main__":
    sys.exit(main())
