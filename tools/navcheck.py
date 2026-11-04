"""Check each page's "Next:" link against the nav order in mkdocs.yml.

Reading order is the whole premise of this site, so a Next link pointing
somewhere other than the following nav entry is a real defect — and an easy
one to introduce by inserting a section, since the neighbouring pages don't
change and nothing warns you.

Pages outside the reading sequence (the homepage, glossary, about, reference)
are expected to have no Next link and are listed separately, not flagged.
"""
import re, pathlib, sys

OUTSIDE = {"index.md", "glossary.md", "about/forks.md", "about/about-me.md",
           "reference/gas-costs.md", "reference/fork-history.md"}

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    y = (root / "mkdocs.yml").read_text()
    order = [m.group(1) for m in re.finditer(r':\s*([a-z0-9/-]+\.md)\s*$', y, re.M)]
    bad = 0
    for i, p in enumerate(order[:-1]):
        f = root / "docs" / p
        if not f.exists():
            print(f"  MISSING FILE  {p}"); bad += 1; continue
        m = re.search(r'\*\*Next:\*\* \[([^\]]+)\]\(([^)#]+)', f.read_text())
        if not m:
            if p not in OUTSIDE:
                print(f"  NO NEXT LINK  {p}"); bad += 1
            continue
        got = (f.parent / m.group(2)).resolve()
        want = (root / "docs" / order[i + 1]).resolve()
        if got != want:
            print(f"  WRONG NEXT    {p}")
            print(f"                points at {got.relative_to(root / 'docs')}")
            print(f"                nav says  {order[i + 1]}")
            bad += 1
    print(f"nav/Next consistency: {'clean' if not bad else str(bad) + ' problem(s)'}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
