"""Check that every reference is cited and every citation has a reference.

Each page lists its sources at the foot with an explicit anchor, and cites them
inline as [(Author, year)](#ref-author-year). Two things can go wrong, both
invisible in a diff:

  orphan   a source in the bibliography that no sentence cites — usually a
           reference that survived an edit after the claim it supported was
           cut, which leaves the page looking better sourced than it is

  missing  a citation pointing at an anchor that does not exist — a dead link
           in the middle of an argument

Also checks the bibliography is sorted by surname, which is the house style.

Written because the equivalent inline check fired three times in one day and
I committed over it each time. A check that can be read past is not a check.
"""
import re
import sys
import pathlib
import unicodedata


def sortkey(name):
    """Compare the way a person alphabetises a bibliography.

    Codepoint order gets two things wrong that look like faults and are not:
    lowercase sorts after uppercase, so "ethereum.org" lands after "Kadianakis";
    and accented letters sort after every unaccented one, so "Böhme" lands
    after "Buterin". Strip the accents and fold the case first.
    """
    stripped = "".join(c for c in unicodedata.normalize("NFD", name)
                       if not unicodedata.combining(c))
    return stripped.casefold()

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    problems = 0
    for f in sorted((root / "docs").rglob("*.md")):
        text = f.read_text()
        rel = f.relative_to(root)
        defined = set(re.findall(r'<a id="(ref-[^"]+)"></a>', text))
        cited = set(re.findall(r'\]\(#(ref-[^)]+)\)', text))
        for a in sorted(defined - cited):
            print(f"  ORPHAN   {rel}: '{a}' is in the bibliography, cited nowhere")
            problems += 1
        for a in sorted(cited - defined):
            print(f"  MISSING  {rel}: citation points at '{a}', which is not defined")
            problems += 1
        surnames = re.findall(r'</a>\*\*([^,*]+)', text)
        if surnames != sorted(surnames, key=sortkey):
            print(f"  UNSORTED {rel}: bibliography is not in surname order")
            print(f"           {surnames}")
            problems += 1
    print(f"reference integrity: {'clean' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
