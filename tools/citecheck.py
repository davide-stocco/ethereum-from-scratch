"""Check in-text citations follow the house style.

Two forms are correct, per the conventions in ROADMAP.md:

    [Wood (2014)](#ref-wood-2014)        author is the subject of the sentence
    [(Nakamoto, 2008)](#ref-nakamoto)    the citation is parenthetical

The failure this catches is a third form that reads fine in a diff and badly
on the page, because only the year becomes a link:

    Szabo [(1997)](#ref-szabo-1997)      <- author outside the link

It went unnoticed on three pages until a reader spotted it, which is the
signature of a fault worth automating rather than remembering.
"""
import re
import sys
import pathlib

BAD = re.compile(r"[A-Z][A-Za-zÀ-ÿ'’-]+(?:\s+et\s+al\.)?\s+\[\((?:\d{4}|[^)]*,\s*\d{4})\)\]")

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    problems = 0
    for f in sorted((root / "docs").rglob("*.md")):
        for i, line in enumerate(f.read_text().split("\n"), 1):
            for m in BAD.finditer(line):
                print(f"  {f.relative_to(root)}:{i}: author sits outside the link — {m.group(0)!r}")
                print("           write [Name (year)](#ref-...) instead")
                problems += 1
    print(f"citation style: {'clean' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
