"""Check concepts.yml against the site, and check the site's first rule.

Four things:

  coverage  every written page is in the graph, and nothing is in the graph
            that is not a written page

  targets   every 'needs' entry names a real page

  ORDER     no page needs one that comes LATER in the reading order

  summary   each entry's summary still matches that page's frontmatter
            description, so the data cannot quietly drift from the pages

The order check is the point of the file. "Nothing is explained before its
prerequisites" is the site's first rule, stated on the homepage, and until now
it was enforced by reading. If a curated dependency ever points forward, the
reading order has a genuine bug — a page leaning on something nobody has met.
"""

import re
import sys
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REFERENCE = {"glossary.md", "about/forks.md", "about/about-me.md",
             "reference/fork-history.md"}


def main():
    data_file = ROOT / "concepts.yml"
    if not data_file.exists():
        print("concept graph: concepts.yml missing — run tools/concepts.py --write")
        return 1

    text = (ROOT / "mkdocs.yml").read_text().split("\nnav:", 1)[1]
    order = []
    for line in text.split("\n"):
        m = re.match(r"^\s+- .+?: ([a-z0-9/-]+\.md)\s*$", line)
        if m and m.group(1) not in order:
            order.append(m.group(1))
    index = {p: i for i, p in enumerate(order)}

    written = {p for p in order
               if p not in REFERENCE and (DOCS / p).exists()
               and "not written yet" not in (DOCS / p).read_text()}

    pages = yaml.safe_load(data_file.read_text())["pages"]
    problems = 0

    for p in sorted(written - set(pages)):
        print(f"  MISSING   {p} is written but not in the graph")
        problems += 1
    for p in sorted(set(pages) - written):
        print(f"  STALE     {p} is in the graph but not a written page")
        problems += 1

    for p, entry in sorted(pages.items()):
        for n in entry.get("needs") or []:
            if n not in index:
                print(f"  BAD EDGE  {p} needs '{n}', which is not a page in the nav")
                problems += 1
            elif p in index and index[n] > index[p]:
                print(f"  ORDER     {p} needs {n}, which comes LATER in the reading order")
                problems += 1
        if p in written:
            m = re.search(r"^description:\s*(.+)$", (DOCS / p).read_text(), re.M)
            live = m.group(1).strip() if m else ""
            if live and live != (entry.get("summary") or "").strip():
                print(f"  DRIFTED   {p}: summary no longer matches the page's description")
                problems += 1

    edges = sum(len(v.get("needs") or []) for v in pages.values())
    print(f"concept graph: {len(pages)} pages, {edges} edges — "
          f"{'clean' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
