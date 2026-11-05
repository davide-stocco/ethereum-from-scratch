"""Check the glossary is alphabetical within each letter section.

Added because I introduced two ordering faults myself — "Genesis" before
"Gas", then "Beige Paper" before "Balance" — and a third was already there
unnoticed. The glossary is the one page a reader scans rather than reads, so
order is the whole of its usability.

Compares case-insensitively, which is how a reader looks: "gwei" belongs with
the G entries, not after them, and "wei" before "White Paper".
"""
import re
import sys
import pathlib

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    text = (root / "docs" / "glossary.md").read_text()
    problems = 0
    sections = re.split(r"\n## ([A-Z])\n", text)
    for i in range(1, len(sections), 2):
        letter, body = sections[i], sections[i + 1]
        names = re.findall(r"^\*\*([^*]+)\*\*\{", body, re.M)
        want = sorted(names, key=str.casefold)
        if names != want:
            print(f"  section {letter} is out of order")
            print(f"    found: {names}")
            print(f"    want:  {want}")
            problems += 1
        for n in names:
            if n[0].upper() != letter:
                print(f"  section {letter} contains '{n}', which belongs under {n[0].upper()}")
                problems += 1
    print(f"glossary order: {'clean' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
