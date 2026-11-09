"""Build and maintain concepts.yml — the site's dependency graph.

The menu is a tree: one reading order, seven parts. The concepts underneath it
are a graph — Keccak-256 is a prerequisite for eight later pages across three
parts, which no linear menu can express. This file holds that graph.

    python3 tools/concepts.py          show what would change
    python3 tools/concepts.py --write  apply it

**Edges are proposed from links and kept by hand.** A link between two pages is
not always a dependency: *Accounts* links to *Seed phrases* only to say an
account is not a wallet, which is a clarification rather than a prerequisite.
So this script proposes candidates and never deletes a curated edge — pruning
is a judgement it has no business making.

Re-running it is therefore safe. It adds new pages, lists newly-linked
candidates for review, and reports curated edges that no longer have a link
behind them (which may be correct — a real dependency the prose stopped
mentioning).

`promises` are deliberately not stored. A forward link means "covered later in
X", which is derivable from the pages at any time and needs no curation.
"""

import re
import sys
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "concepts.yml"

# Linked from nearly everywhere and prerequisites for nothing. Left out, or
# they dominate the graph and say nothing about dependency.
REFERENCE = {
    "glossary.md", "about/forks.md", "about/about-me.md",
    "reference/fork-history.md",
}


def nav():
    """Reading order, part, and title for every page, from mkdocs.yml."""
    text = (ROOT / "mkdocs.yml").read_text().split("\nnav:", 1)[1]
    pages, part, title, current = [], {}, {}, None
    for line in text.split("\n"):
        top = re.match(r"^  - ([^:\n]+):\s*$", line)
        if top:
            current = top.group(1)
        entry = re.match(r"^\s+- (.+?): ([a-z0-9/-]+\.md)\s*$", line)
        if entry and entry.group(2) not in part:
            path = entry.group(2)
            pages.append(path)
            part[path] = current or "Home"
            title[path] = entry.group(1).strip("'\"")
    return pages, part, title


def summary(path):
    """The page's own frontmatter description — no second source of truth."""
    m = re.search(r"^description:\s*(.+)$", (DOCS / path).read_text(), re.M)
    return m.group(1).strip() if m else ""


def linked_prerequisites(pages):
    """Backward links, as candidate dependencies."""
    index = {p: i for i, p in enumerate(pages)}
    out = {}
    for p in pages:
        f = DOCS / p
        if not f.exists() or "not written yet" in f.read_text():
            continue
        found = set()
        for href in set(re.findall(r"\]\((\.\.?/[^)#\" ]+\.md|[a-z0-9-]+\.md)",
                                   f.read_text())):
            try:
                rel = str(((f.parent / href).resolve()).relative_to(DOCS.resolve()))
            except ValueError:
                continue
            if rel == p or rel not in index or rel in REFERENCE:
                continue
            if index[rel] < index[p]:
                found.add(rel)
        out[p] = found
    return out


def main():
    write = "--write" in sys.argv
    pages, part, title = nav()
    candidates = linked_prerequisites(pages)
    existing = yaml.safe_load(DATA.read_text())["pages"] if DATA.exists() else {}

    data, added, new_edges, unbacked = {}, [], [], []
    for p in pages:
        if p in REFERENCE or not (DOCS / p).exists():
            continue
        if "not written yet" in (DOCS / p).read_text():
            continue
        prior = existing.get(p)
        if prior is None:
            added.append(p)
            needs = sorted(candidates.get(p, ()))
        else:
            needs = list(prior.get("needs") or [])
            for c in sorted(candidates.get(p, ())):
                if c not in needs:
                    new_edges.append((p, c))
            for n in needs:
                if n not in candidates.get(p, ()):
                    unbacked.append((p, n))
        data[p] = {
            "title": title[p],
            "part": part[p],
            "summary": summary(p),
            "needs": needs,
        }

    print(f"  pages in graph: {len(data)}")
    print(f"  dependency edges: {sum(len(v['needs']) for v in data.values())}")
    if added:
        print(f"\n  NEW PAGES, edges proposed from their links ({len(added)}):")
        for p in added:
            print(f"    {p}  -> needs {data[p]['needs'] or 'nothing'}")
    if new_edges:
        print(f"\n  NEW CANDIDATE EDGES — review, then add by hand if real ({len(new_edges)}):")
        for s, t in new_edges:
            print(f"    {s}  now links back to  {t}")
    if unbacked:
        print(f"\n  CURATED EDGES WITH NO LINK BEHIND THEM ({len(unbacked)}):")
        print("    (may be correct — a real dependency the prose stopped mentioning)")
        for s, t in unbacked:
            print(f"    {s}  ->  {t}")

    if write:
        header = ("# The site's concept dependency graph. Generated by\n"
                  "# tools/concepts.py and then pruned by hand: a link between two\n"
                  "# pages is not always a dependency, so edges are proposed from\n"
                  "# links and kept by judgement. Checked by tools/conceptcheck.py.\n"
                  "#\n"
                  "# 'needs' means: this page cannot be understood before that one.\n"
                  "# Forward references are not stored — they are derivable.\n\n")
        DATA.write_text(header + yaml.safe_dump({"pages": data}, sort_keys=True,
                                                allow_unicode=True, width=100))
        print(f"\n  written: {DATA.relative_to(ROOT)}")
    elif added or new_edges or unbacked:
        print("\n  (nothing written — re-run with --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
