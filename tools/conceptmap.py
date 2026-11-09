"""Draw the concept graph as a page: docs/concept-map.md.

Two levels.

  the map    every page as a bubble, in reading order, with a line to each
             page it depends on — from concepts.yml

  the zoom   click a bubble and a second, granular network opens: the
             concepts INSIDE that page and how they depend on each other —
             from inside.yml, which is hand-authored

The layout is computed here, in Python, not in the browser. That is
deliberate: there is no JavaScript on this page at all. Coordinates are
arithmetic that can be checked here, and every interaction — hover to grow a
bubble and light up its lines, click to open a zoom — is CSS.

    python3 tools/conceptmap.py          report, write nothing
    python3 tools/conceptmap.py --write  regenerate the page

Bubbles are sized to their text rather than being a fixed grid, so a row
holds as many as fit. That is why the layout packs by width.

No line in either picture ever points upward. In the map that is the site's
reading order, enforced by tools/conceptcheck.py. In a zoom it is the order
the page itself explains things in, which is the same promise one level down.

index.md is left out: a prerequisite for nothing, connected to everything.
"""

import re
import sys
import math
import pathlib
import collections

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "concept-map.md"

WIDTH = 780                       # the drawing's width, in user units
MARGIN = 20
LABEL_H = 28                      # the part's name, above its bubbles
BAND_GAP = 34

CHAR = 0.54                       # width of a character, as a fraction of size
MAP_SIZE, MAP_RY = 11.5, 29       # the map: font size and bubble half-height
ZOOM_SIZE, ZOOM_RY = 11, 28
GAP_X, GAP_Y = 14, 26


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


def href(link):
    """A node's link: '#zoom-...', or 'page.md', or 'page.md#anchor'."""
    if link.startswith("#"):
        return link
    target, hashmark, frag = link.partition("#")
    return url(target) + hashmark + frag


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                  .replace('"', "&quot;").replace("'", "&#39;"))


# --------------------------------------------------------------------------
# bubbles

def split(text):
    """One or two lines, balanced, so the bubble stays round rather than long."""
    words = text.split()
    if len(words) < 2 or len(text) <= 13:
        return [text]
    best, score = None, None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        s = max(len(a), len(b)) + abs(len(a) - len(b)) * 0.4
        if score is None or s < score:
            best, score = (a, b), s
    return list(best)


def bubble_rx(lines, size, ry):
    """Half-width that fits the text inside the ellipse, not inside its box.

    An ellipse is narrower than its bounding box everywhere except the middle,
    so a two-line label has to be measured at the height its lines actually
    sit at — otherwise the ends of the longer line fall outside the curve.
    """
    rx = 0
    for i, line in enumerate(lines):
        half = len(line) * size * CHAR / 2
        dy = 0 if len(lines) == 1 else (7 if i == 0 else 7)
        room = math.sqrt(max(0.15, 1 - (dy / ry) ** 2))     # fraction of rx here
        rx = max(rx, half / room)
    return max(44, rx + 11)


def draw(cx, cy, rx, ry, lines, size, cls, link, note, halo):
    """One bubble: an ellipse, its label, its hidden halo, wrapped in a link."""
    ys = [cy + 4] if len(lines) == 1 else [cy - 3, cy + 11]
    text = "".join(
        f'<text class="cm-label" x="{cx:g}" y="{ty:g}" font-size="{size}" '
        f'text-anchor="middle">{esc(line)}</text>'
        for line, ty in zip(lines, ys))
    return (f'<g class="{cls}"><title>{esc(note)}</title>{halo}'
            f'<a href="{link}"><ellipse class="cm-bub" cx="{cx:g}" cy="{cy:g}" '
            f'rx="{rx:g}" ry="{ry}"/>{text}</a></g>')


def pack(items, widths, maxw):
    """Greedy rows: as many bubbles as fit across, then wrap."""
    rows, row, used = [], [], 0.0
    for it in items:
        w = widths[it]
        if row and used + GAP_X + w > maxw:
            rows.append(row)
            row, used = [], 0.0
        used += w + (GAP_X if row else 0)
        row.append(it)
    if row:
        rows.append(row)
    return rows


def link_path(a, b, ra, rb, ry):
    """A dependency, drawn downward, leaving and arriving on the bubble's rim."""
    (x1, y1), (x2, y2) = a, b
    # Spread the attachment point towards the other end, so several lines
    # leaving one bubble do not come out of a single point.
    off1 = max(-ra * 0.62, min(ra * 0.62, (x2 - x1) / 3))
    off2 = max(-rb * 0.62, min(rb * 0.62, (x1 - x2) / 3))
    ey1 = y1 + ry * math.sqrt(max(0.0, 1 - (off1 / ra) ** 2))
    ey2 = y2 - ry * math.sqrt(max(0.0, 1 - (off2 / rb) ** 2))
    sx, ex = x1 + off1, x2 + off2
    if ey2 > ey1:
        dy = (ey2 - ey1) / 2
        return (f"M{sx:.1f},{ey1:.1f} C{sx:.1f},{ey1 + dy:.1f} "
                f"{ex:.1f},{ey2 - dy:.1f} {ex:.1f},{ey2:.1f}")
    # Same row: dip below both bubbles rather than drawing a loop between them.
    sag = 26
    return (f"M{x1:.1f},{y1 + ry:.1f} C{x1:.1f},{y1 + ry + sag:.1f} "
            f"{x2:.1f},{y2 + ry + sag:.1f} {x2:.1f},{y2 + ry:.1f}")


# --------------------------------------------------------------------------
# the map

def the_map(data, bands, edges, insides):
    """Every page as a bubble, parts as horizontal bands."""
    maxw = WIDTH - 2 * MARGIN
    lines = {p: split(data[p]["title"]) for b in bands.values() for p in b}
    rx = {p: bubble_rx(lines[p], MAP_SIZE, MAP_RY) for p in lines}
    widths = {p: 2 * rx[p] for p in rx}

    pos, band_box, y = {}, [], MARGIN
    for name, pages in bands.items():
        top = y
        y += LABEL_H + MAP_RY
        for row in pack(pages, widths, maxw):
            total = sum(widths[i] for i in row) + GAP_X * (len(row) - 1)
            x = MARGIN + (maxw - total) / 2
            for p in row:
                pos[p] = (x + rx[p], y)
                x += widths[p] + GAP_X
            y += 2 * MAP_RY + GAP_Y
        y += -GAP_Y - MAP_RY + BAND_GAP
        band_box.append((name, top, len(pages)))
    h = y - BAND_GAP + MARGIN

    paths, incident = [], collections.defaultdict(list)
    for s, t in edges:
        d = link_path(pos[s], pos[t], rx[s], rx[t], MAP_RY)
        paths.append(f'<path class="cm-edge" d="{d}"/>')
        incident[s].append(d)
        incident[t].append(d)

    out = [f'<svg class="cm-svg" viewBox="0 0 {WIDTH} {h:g}" role="group" '
           f'aria-label="Every written page as a bubble, grouped into parts, '
           f'with {len(edges)} dependency lines. No line points upward.">']
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
    for p, (cx, cy) in pos.items():
        zoomed = p in insides
        note = ("open the concepts inside it" if zoomed
                else f'{len(data[p].get("needs") or [])} prerequisite(s)')
        halo = "".join(f'<path class="cm-halo" d="{d}"/>' for d in incident[p])
        out.append(draw(
            cx, cy, rx[p], MAP_RY, lines[p], MAP_SIZE,
            "cm-node cm-has-zoom" if zoomed else "cm-node",
            f"#zoom-{slug(p)}" if zoomed else url(p),
            f'{data[p]["title"]} — {note}', halo))
    out.append("</svg>")
    return "".join(out)


# --------------------------------------------------------------------------
# a zoom

def zoom(path, data, insides):
    """The concepts inside one page, laid out by how deep they sit.

    Prerequisites borrowed from an earlier page's zoom are drawn too, dashed:
    things this page leans on but does not explain. Clicking one opens the
    zoom it came from.
    """
    nodes = list(insides[path]["inside"])
    local = {n["id"] for n in nodes}

    outside = []
    for n in nodes:
        for d in n.get("needs") or []:
            if ":" in d and d not in {o["id"] for o in outside}:
                fp, fid = d.split(":", 1)
                src = next(m for m in insides[fp]["inside"] if m["id"] == fid)
                outside.append({
                    "id": d, "label": src["label"], "foreign": True,
                    "note": f'From {data[fp]["title"]} — {src["note"]}',
                    "link": f"#zoom-{slug(fp)}", "needs": [],
                })
    nodes = outside + nodes

    # Depth is the longest path from a root, so a bubble always sits below
    # everything it needs. The borrowed ones are roots by construction.
    need = {n["id"]: list(n.get("needs") or []) for n in nodes}
    depth = {}

    def walk(i):
        if i not in depth:
            depth[i] = 1 + max((walk(j) for j in need[i]), default=-1)
        return depth[i]

    for n in nodes:
        walk(n["id"])

    maxw = WIDTH - 2 * MARGIN
    lines = {n["id"]: split(n["label"]) for n in nodes}
    rx = {i: bubble_rx(lines[i], ZOOM_SIZE, ZOOM_RY) for i in lines}
    widths = {i: 2 * rx[i] for i in rx}

    pos, y = {}, MARGIN + ZOOM_RY
    for d in sorted(set(depth.values())):
        tier = [n["id"] for n in nodes if depth[n["id"]] == d]
        for row in pack(tier, widths, maxw):
            total = sum(widths[i] for i in row) + GAP_X * (len(row) - 1)
            x = MARGIN + (maxw - total) / 2
            for i in row:
                pos[i] = (x + rx[i], y)
                x += widths[i] + GAP_X
            y += 2 * ZOOM_RY + GAP_Y
    h = y - GAP_Y - ZOOM_RY + MARGIN

    paths, incident = [], collections.defaultdict(list)
    for n in nodes:
        for dep in n.get("needs") or []:
            d = link_path(pos[dep], pos[n["id"]], rx[dep], rx[n["id"]], ZOOM_RY)
            cls = "cm-edge cm-crossing" if ":" in dep else "cm-edge"
            paths.append(f'<path class="{cls}" d="{d}"/>')
            incident[dep].append(d)
            incident[n["id"]].append(d)

    out = [f'<svg class="cm-svg cm-zoomsvg" viewBox="0 0 {WIDTH} {h:g}" '
           f'role="group" aria-label="The {len(local)} concepts inside '
           f'{esc(data[path]["title"])}, with a line from each to the ones it '
           f'needs first, and {len(outside)} borrowed from earlier pages.">']
    out += paths
    for n in nodes:
        cx, cy = pos[n["id"]]
        halo = "".join(f'<path class="cm-halo" d="{d}"/>' for d in incident[n["id"]])
        out.append(draw(
            cx, cy, rx[n["id"]], ZOOM_RY, lines[n["id"]], ZOOM_SIZE,
            "cm-node cm-outside" if n.get("foreign") else "cm-node",
            href(n["link"]), n["note"], halo))
    out.append("</svg>")
    return "".join(out), len(local), len(paths), len(outside)


# --------------------------------------------------------------------------

def build():
    data, pages, bands, edges, insides = load()
    m = the_map(data, bands, edges, insides)

    zooms = []
    for p in pages:
        if p not in insides:
            continue
        svg, n, e, borrowed = zoom(p, data, insides)
        zooms.append(
            f'<section class="cm-zoom" id="zoom-{slug(p)}">'
            f'<p class="cm-zoomhead"><strong>Inside {esc(data[p]["title"])}</strong> — '
            f'{n} concepts, {e} lines'
            f'{f", and {borrowed} dashed bubbles borrowed from earlier pages" if borrowed else ""}. '
            f'Every bubble is a link. <a href="{url(p)}">Open the page</a> · '
            f'<a href="#the-map">Back to the map</a></p>{svg}</section>')

    body = f"""---
tier: meta
description: Every page on the site as a bubble, with a line to each page you need first — and a second, granular network inside each one.
---

<!-- GENERATED by tools/conceptmap.py from concepts.yml and inside.yml. Do not
     edit by hand: run `python3 tools/conceptmap.py --write` instead. -->

# The concept map

Every page on the site, with a line to each page you have to read first. The
menu down the side can only be a list; this is the shape underneath it.

**Hover a bubble** to read it and light up its own lines. **Click one** to
open the page — or, where the zoom exists, the granular network of concepts
inside it.

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
