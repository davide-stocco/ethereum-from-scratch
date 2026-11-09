"""Check inside.yml — the second level of the concept map.

Six things:

  link      every concept HAS a link, and it resolves: the page exists and
            is written, and an #anchor is a heading that really is there
  ids       unique within a page
  local     every local prerequisite names a concept on the same page
  foreign   every 'page.md:id' names a concept that exists, on a page that
            has a zoom, and that comes EARLIER in reading order
  cycles    no concept depends on itself, directly or through others
  pages     every page with concepts is a written page in the graph

The link check is the load-bearing one. The rule for this file is that a box
nobody can click does not go in, because a box with no destination is a
private note rather than a map. Anchors are computed with the same algorithm
python-markdown uses for heading ids — verified against the built site, 336
headings, no mismatches — so a renamed heading is caught here rather than by
a reader hitting a link that scrolls nowhere.
"""

import re
import sys
import pathlib
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def slugify(text):
    """markdown.extensions.toc.slugify, which is what generates heading ids."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def anchors(path):
    """Every heading id on a page."""
    out = set()
    for m in re.finditer(r"^#{2,6} (.+)$", (DOCS / path).read_text(), re.M):
        out.add(slugify(re.sub(r"`|\*", "", m.group(1)).strip()))
    return out


def reading_order():
    nav = (ROOT / "mkdocs.yml").read_text().split("\nnav:", 1)[1]
    order = []
    for m in re.finditer(r"^\s+- .+?: ([a-z0-9/-]+\.md)\s*$", nav, re.M):
        if m.group(1) not in order:
            order.append(m.group(1))
    return {p: i for i, p in enumerate(order)}


def main():
    f = ROOT / "inside.yml"
    if not f.exists():
        print("inside.yml: missing")
        return 1
    pages = yaml.safe_load(f.read_text())["pages"]
    order = reading_order()
    problems = 0

    for path, entry in pages.items():
        if path not in order:
            print(f"  NO SUCH PAGE  {path} is not in the nav")
            problems += 1
            continue
        if not (DOCS / path).exists() or "not written yet" in (DOCS / path).read_text():
            print(f"  NOT WRITTEN   {path} has concepts but is still a stub")
            problems += 1
            continue

        ids = [n["id"] for n in entry["inside"]]
        for i in sorted({i for i in ids if ids.count(i) > 1}):
            print(f"  DUPLICATE ID  {path}: '{i}' is used more than once")
            problems += 1

        for n in entry["inside"]:
            where = f"{path}:{n['id']}"
            link = n.get("link")
            if not link:
                print(f"  NO LINK       {where} — every concept must be clickable")
                problems += 1
            else:
                target, _, frag = link.partition("#")
                if target not in order or not (DOCS / target).exists():
                    print(f"  BAD LINK      {where} -> '{target}' is not a page")
                    problems += 1
                elif frag and frag not in anchors(target):
                    print(f"  DEAD ANCHOR   {where} -> '{link}': no such heading")
                    problems += 1

            for d in n.get("needs") or []:
                if ":" not in d:
                    if d not in ids:
                        print(f"  BAD NEED      {where} needs '{d}', not on this page")
                        problems += 1
                    continue
                fp, fid = d.split(":", 1)
                if fp not in pages:
                    print(f"  BAD NEED      {where} needs '{d}', but {fp} has no concepts")
                    problems += 1
                elif fid not in [m["id"] for m in pages[fp]["inside"]]:
                    print(f"  BAD NEED      {where} needs '{d}', no such concept")
                    problems += 1
                elif order.get(fp, 0) >= order[path]:
                    print(f"  ORDER         {where} needs '{d}', which is NOT earlier "
                          f"in the reading order")
                    problems += 1

        # Cycles, within the page. Across pages the order check already
        # forbids them: a cycle would need an edge pointing forward.
        need = {n["id"]: [d for d in (n.get("needs") or []) if ":" not in d]
                for n in entry["inside"]}
        state = {}

        def walk(i):
            if state.get(i) == "done":
                return False
            if state.get(i) == "open":
                return True
            state[i] = "open"
            hit = any(walk(j) for j in need.get(i, []))
            state[i] = "done"
            return hit

        for i in ids:
            if walk(i):
                print(f"  CYCLE         {path}: '{i}' depends on itself")
                problems += 1
                break

    n = sum(len(v["inside"]) for v in pages.values())
    e = sum(len(m.get("needs") or []) for v in pages.values() for m in v["inside"])
    print(f"inside the pages: {len(pages)} zoom(s), {n} concepts, {e} links — "
          f"{'clean' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
