"""Draw concepts.yml as a page: docs/concept-map.md.

Two pictures, both generated from the same data:

  overview   one box per part, with the number of dependencies running
             between each pair of parts — the shape of the thing
  detail     one box per page, laid out in reading order, with all 79
             dependency edges drawn

The layout is computed here, in Python, not in the browser. That is
deliberate: there is no JavaScript on this page at all. Coordinates are
arithmetic I can check, and the interaction — click a part to isolate it,
hover a page to light up its dependencies — is done with CSS `:target` and
`:hover` alone. A reader with scripts blocked loses nothing but the dimming.

    python3 tools/conceptmap.py          report, write nothing
    python3 tools/conceptmap.py --write  regenerate the page

The one visual claim worth making: **no line in the detail picture ever
points upward.** Every dependency runs from an earlier page to a later one,
which is the site's first rule. tools/conceptcheck.py enforces it; this
page is where you can see it.

index.md is left out. It is a prerequisite for nothing and would sit at the
top of the picture connected to everything, which says nothing.
"""

import re
import sys
import pathlib
import collections

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "concept-map.md"

NODE_W, NODE_H = 170, 40          # a page box
GAP_X, GAP_Y = 20, 16             # between boxes
PER_ROW = 4                       # boxes per row inside a part
LABEL_H = 28                      # the part's name, above its boxes
BAND_GAP = 40                     # between parts
MARGIN = 20

BOX_W, BOX_H = 330, 46            # a part box, in the overview
BOX_PITCH = 92


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
    return pages_data, pages, bands, edges


def url(path):
    """Final site URL, relative to /concept-map/ (use_directory_urls is on)."""
    return "../" + path[:-3].replace("/index", "/") + "/"


def wrap(title):
    """At most two lines, because a third does not fit in 40px."""
    words, lines, cur = title.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= 23 or not cur:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > 2:                      # fold the tail into line two
        lines = [lines[0], " ".join(lines[1:])]
        if len(lines[1]) > 26:
            lines[1] = lines[1][:25].rstrip() + "…"
    return lines


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


def node_text(x, y, lines):
    """Centred label. Two lines sit either side of the middle; one is centred."""
    cx, out = x + NODE_W / 2, []
    if len(lines) == 1:
        ys = [y + NODE_H / 2 + 4]
    else:
        ys = [y + NODE_H / 2 - 4, y + NODE_H / 2 + 10]
    for line, ty in zip(lines, ys):
        out.append(f'<text class="cm-label" x="{cx:g}" y="{ty:g}" font-size="11.5" '
                   f'text-anchor="middle">{esc(line)}</text>')
    return "".join(out)


def port(box, col, row):
    """Where along a box's edge a line leaves or arrives.

    Not the centre. Every line leaving a box from the same point produces one
    thick stripe that says nothing about how many there are, and two boxes in
    the same column produce a vertical that cannot be told from a box border.
    So the attachment point is spread across the box according to the column
    at the other end, and nudged by that end's row to separate the ties.
    """
    frac = 0.22 + 0.56 * col / (PER_ROW - 1)
    return box[0] + NODE_W * frac + (row % 3 - 1) * 5


def curve(src, dst):
    """A dependency, drawn downward. Same-row pairs arc underneath instead.

    src and dst are (x, y, column, row).
    """
    if dst[1] > src[1]:
        x1, y1 = port(src, dst[2], dst[3]), src[1] + NODE_H
        x2, y2 = port(dst, src[2], src[3]), dst[1]
        dy = (y2 - y1) / 2
        return f"M{x1:g},{y1:g} C{x1:g},{y1 + dy:g} {x2:g},{y2 - dy:g} {x2:g},{y2:g}"
    # Same row: both boxes sit at one height, so the line dips below them in a
    # shallow U. Anything else here draws a loop, which reads as a knot.
    x1, x2 = src[0] + NODE_W * 0.7, dst[0] + NODE_W * 0.3
    y = src[1] + NODE_H
    sag = 20 + 6 * ((dst[0] - src[0]) / (NODE_W + GAP_X) - 1)
    return (f"M{x1:g},{y:g} C{x1:g},{y + sag:g} {x2:g},{y + sag:g} {x2:g},{y:g}")


def detail(data, bands, edges):
    """One box per page, parts as horizontal bands, every edge drawn."""
    inner = PER_ROW * NODE_W + (PER_ROW - 1) * GAP_X
    pos, band_of, y = {}, {}, MARGIN
    band_box = []
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
        band_box.append((name, top, y - top, len(pages)))
        y += BAND_GAP
    w, h = inner + 2 * MARGIN, y - BAND_GAP + MARGIN

    # Edges first, so boxes sit on top of them.
    paths = []
    incident = collections.defaultdict(list)
    for s, t in edges:
        cls = f"cm-edge cm-from-{band_of[s]} cm-to-{band_of[t]}"
        p = curve(pos[s], pos[t])
        paths.append(f'<path class="{cls}" d="{p}"/>')
        incident[s].append(p)
        incident[t].append(p)

    out = [f'<svg class="cm-svg" viewBox="0 0 {w:g} {h:g}" role="group" '
           f'aria-label="Every written page as a box, grouped into the four parts '
           f'written so far, with {len(edges)} dependency lines. No line points upward.">']
    out += paths
    # The part names go ON TOP of the lines, each on an opaque chip. Drawn
    # after the paths for that reason: underneath, a dozen dependencies cross
    # the words and the label stops being readable.
    for name, top, bh, n in band_box:
        label = f"{name.upper()} · {n}"
        out.append(
            f'<rect fill="var(--md-default-bg-color)" x="{MARGIN - 4}" '
            f'y="{top + 2}" width="{len(label) * 10.5 * 0.52 + 10:.0f}" height="16"/>'
            f'<text class="cm-band" x="{MARGIN}" y="{top + 13}" font-size="10.5">'
            f'{esc(name.upper())} <tspan class="cm-count">· {n}</tspan></text>')
    for p, (x, yy, _c, _r) in pos.items():
        bi, title = band_of[p], data[p]["title"]
        # Each box carries hidden copies of its own edges. Hovering the box
        # shows them — a highlight with no script behind it.
        halo = "".join(f'<path class="cm-halo" d="{d}"/>' for d in incident[p])
        out.append(
            f'<g class="cm-node cm-part-{bi}"><title>{esc(title)} — '
            f'{len(data[p].get("needs") or [])} prerequisite(s)</title>{halo}'
            f'<a href="{url(p)}">'
            f'<rect class="cm-box" x="{x:g}" y="{yy:g}" width="{NODE_W}" '
            f'height="{NODE_H}" rx="5"/>{node_text(x, yy, wrap(title))}</a></g>')
    out.append("</svg>")
    return "".join(out), len(band_box)


def overview(bands, edges, data):
    """One box per part, with the dependency count between each pair."""
    names = list(bands)
    pi = {n: i for i, n in enumerate(names)}
    cross, intra = collections.Counter(), collections.Counter()
    for s, t in edges:
        a, b = pi[data[s]["part"]], pi[data[t]["part"]]
        (intra if a == b else cross)[(a, b)] += 1

    lanes = sorted(cross, key=lambda k: (k[1] - k[0], k[0]))
    far = [k for k in lanes if k[1] - k[0] > 1]
    w = MARGIN * 2 + BOX_W + 40 + 34 * len(far)
    h = MARGIN * 2 + (len(names) - 1) * BOX_PITCH + BOX_H + 10
    x0 = MARGIN
    ys = [MARGIN + i * BOX_PITCH for i in range(len(names))]

    out = [f'<svg class="cm-svg cm-overview" viewBox="0 0 {w:g} {h:g}" role="group" '
           f'aria-label="The four written parts as four boxes in reading order, '
           f'with the number of dependencies running between each pair.">']
    for (a, b), c in sorted(cross.items()):
        y1, y2 = ys[a] + BOX_H, ys[b]
        if b - a == 1:
            x = x0 + BOX_W / 2
            out.append(f'<path class="cm-lane" d="M{x:g},{y1:g} L{x:g},{y2:g}"/>')
            out.append(f'<text class="cm-lanenum" x="{x + 8:g}" font-size="11" '
                       f'y="{(y1 + y2) / 2 + 4:g}">{c}</text>')
        else:
            off = x0 + BOX_W + 16 + 34 * far.index((a, b))
            out.append(f'<path class="cm-lane" d="M{x0 + BOX_W:g},{ys[a] + BOX_H / 2:g} '
                       f'C{off:g},{ys[a] + BOX_H / 2:g} {off:g},{ys[b] + BOX_H / 2:g} '
                       f'{x0 + BOX_W:g},{ys[b] + BOX_H / 2:g}"/>')
            out.append(f'<text class="cm-lanenum" x="{off + 5:g}" font-size="11" '
                       f'y="{(ys[a] + ys[b]) / 2 + BOX_H / 2 + 4:g}">{c}</text>')
    for i, name in enumerate(names):
        inside = intra[(i, i)]
        out.append(
            f'<a href="#part-{i}"><g class="cm-partbox">'
            f'<title>{esc(name)} — {len(bands[name])} pages, {inside} '
            f'dependencies inside the part. Click to isolate it below.</title>'
            f'<rect class="cm-box" x="{x0}" y="{ys[i]}" width="{BOX_W}" '
            f'height="{BOX_H}" rx="6"/>'
            f'<text class="cm-partname" x="{x0 + 14}" y="{ys[i] + 20}" '
            f'font-size="13">{esc(name)}</text>'
            f'<text class="cm-partmeta" x="{x0 + 14}" y="{ys[i] + 36}" font-size="10.5">'
            f'{len(bands[name])} pages · {inside} inside</text></g></a>')
    out.append("</svg>")
    return "".join(out), cross, intra, names


def build():
    data, pages, bands, edges = load()
    det, nbands = detail(data, bands, edges)
    ov, cross, intra, names = overview(bands, edges, data)

    biggest = max(cross.items(), key=lambda kv: kv[1])
    deepest = max(pages, key=lambda p: len(data[p].get("needs") or []))
    reused = collections.Counter(s for s, _ in edges).most_common(1)[0]

    anchors = "".join(f'<span class="cm-target" id="part-{i}"></span>'
                      for i in range(nbands))
    links = " · ".join(f'<a href="#part-{i}">{esc(n)}</a>'
                       for i, n in enumerate(names))

    body = f"""---
tier: 1
description: Every page on the site as a box, with a line to each page you need first — the dependency graph the menu cannot show.
---

<!-- GENERATED by tools/conceptmap.py from concepts.yml. Do not edit by hand:
     run `python3 tools/conceptmap.py --write` instead. -->

# The concept map

**[Permanent](about/forks.md).** This describes the order of the explanation,
not the protocol.

The menu down the left is a **tree**: one page after another, seven parts, a
single path from the beginning to the end. It has to be, because you read in
one order. But the ideas underneath it are not a tree. [Keccak-256](crypto/keccak256.md)
is a prerequisite for pages in three different parts. [Addresses](crypto/addresses.md)
is needed by {len([1 for s, _ in edges if s == 'crypto/addresses.md'])} later pages.
No list down the side of a screen can show that, so here it is drawn.

!!! definition "Prerequisite"

    A line from one box to another means: **the first page cannot be
    understood before the second.** Not "is mentioned by" — several pages
    link backwards merely to clarify something, and those links are
    deliberately absent here. {len(edges)} lines survived that judgement
    across {len(pages)} pages.

## The shape of it

Four of the seven parts are written. Each box is one part; each number is how
many dependencies run between that pair of parts.

<figure class="cm-fig">{ov}<figcaption>Dependencies between the parts. Click
any part to isolate it in the picture below.</figcaption></figure>

Every pair of parts is connected. That is the point of the drawing: if the
parts were self-contained chapters you could read in any order, most of these
lanes would be empty. The heaviest is **{esc(names[biggest[0][0]])} →
{esc(names[biggest[0][1]])}** with {biggest[1]}, which is why nothing about
what Ethereum *holds* could be written before the material on who can *act*.

## Every page

Same data, one box per page, in reading order. **Hover a box** to light up
everything it depends on and everything that depends on it; **click** it to
open the page.

Show only: {links} · <a href="#every-page">everything</a>

{anchors}<figure class="cm-fig cm-detail">{det}<figcaption>All {len(pages)} written
pages and all {len(edges)} dependencies. Every line runs downward.</figcaption></figure>

## What the picture is evidence of

**No line points upward.** Every dependency runs from a page earlier in the
reading order to a later one, and that is not a drawing convention — it is the
one promise this site makes on its [front page](index.md), that nothing is
explained before the things it rests on. A single upward line would be a
reading-order bug: a page leaning on something nobody has met yet. It is
checked mechanically on every deploy, by `tools/conceptcheck.py`, which
refuses the build if any dependency points forward.

That such an order exists at all is not guaranteed. A set of dependencies can
be laid out in a single line **if and only if it contains no cycle**
[(Kahn, 1962)](#ref-kahn-1962) — and if two pages each needed the other
first, no reading order could exist and the site would have to merge them or
admit a forward reference. So far none do.

**The lower boxes are heavier.** [{esc(data[deepest]["title"])}]({deepest})
sits on {len(data[deepest].get("needs") or [])} earlier pages — the most of any
page. That is the cost of the order: later pages are cheap to write and
expensive to arrive at.

**A few pages are load-bearing.** [{esc(data[reused[0]]["title"])}]({reused[0]})
is a prerequisite for {reused[1]} others. Pages like that one are where an
error would do the most damage, so they are the ones worth re-reading.

## Recap

- The menu is **one reading order**; the dependencies are a **graph**, and the two cannot be the same drawing.
- A line means **you need that page first** — not merely that one page mentions the other. Clarifying links were pruned by hand.
- Every pair of written parts is connected, so the parts are **not** independent chapters.
- **Nothing points upward.** That is the site's one structural promise, and it is machine-checked on every deploy.
- The picture is generated from `concepts.yml`, so it cannot drift from the pages it describes.

---

## References

<div class="sources" markdown>

- <a id="ref-kahn-1962"></a>**Kahn, A. B.** (1962). *Topological sorting of large networks.* Communications of the ACM 5(11), 558–562. The algorithm behind the claim this page makes: a set of dependencies can be put in a single order if and only if it contains no cycle. A reading order is exactly a topological sort of the graph drawn here. <https://doi.org/10.1145/368996.369025>

</div>
"""
    return body, len(pages), len(edges)


def main():
    body, npages, nedges = build()
    old = PAGE.read_text() if PAGE.exists() else ""
    if "--write" in sys.argv:
        PAGE.write_text(body)
        print(f"concept map: written — {npages} pages, {nedges} edges, "
              f"{len(body)} bytes")
        return 0
    print(f"concept map: {npages} pages, {nedges} edges — "
          f"{'up to date' if body == old else 'OUT OF DATE, re-run with --write'}")
    return 0 if body == old else 1


if __name__ == "__main__":
    sys.exit(main())
