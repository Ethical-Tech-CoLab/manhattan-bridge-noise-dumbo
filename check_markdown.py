"""Markdown checks this repository has actually been broken by.

Run before committing:

    python check_markdown.py

Every check here exists because something shipped. The fence check exists
because an opening ```bash and the comment line under it were dropped in
dd3d381, which left fifteen shell comments rendering as top-level headings in
the live table of contents for three phases. Every phase in between reported
"markdown clean", because each phase wrote its own throwaway checker and none
of them counted backticks across a whole document. That is the argument for
this file existing rather than being rewritten each time.
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

DOCS = [
    "README.md",
    "IDEA-CONCEPT.md",
    "PRECEDENT-AND-MATERIALS.md",
    "WILLIAMSBURG-COMPARATOR.md",
    "VISUAL-MODEL-FRAMEWORK.md",
    "FIELD-CAPTURE-PROTOCOL.md",
    "COMMUNITY-EVIDENCE-AUDIT.md",
    "data-collection/README.md",
    "usage/README.md",
]

# Rendered by both GitHub and the site generator, and used deliberately.
ALLOWED_HTML = re.compile(r"</?(sub|sup|br|kbd)\b", re.I)


def slugify(value):
    """Reproduce GitHub's heading anchor algorithm, as build_pages.py does."""
    value = re.sub(r"[^\w\- ]", "", value.strip().lower(), flags=re.UNICODE)
    return value.replace(" ", "-")


def blank(match):
    """Replace a span with spaces, preserving newlines so line numbers hold."""
    return "".join(c if c == "\n" else " " for c in match.group(0))


def check(doc):
    path = os.path.join(ROOT, doc)
    if not os.path.exists(path):
        return ["file is missing"], 0
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()

    # Blank fenced blocks, then inline code spans. A code span may legally
    # straddle a soft line break, so the second pass runs DOTALL. Doing this
    # first is what lets the backtick count below mean anything.
    scan = re.sub(r"^[ \t]*```.*?^[ \t]*```", blank, text, flags=re.S | re.M)
    scan = re.sub(r"`[^`]*`", blank, scan, flags=re.S)

    problems = []
    lines = scan.split("\n")

    for i, line in enumerate(lines, 1):
        # Bold must open and close on one line. Broken five times.
        if line.count("**") % 2:
            problems.append("L%d bold span wraps the line" % i)
        # An unpaired backtick outside a code span means an unterminated fence.
        if line.count("`") % 2:
            problems.append("L%d unpaired backtick, check for a lost fence" % i)
        for m in re.finditer(r"</?[a-zA-Z][^>]*>", line):
            if not ALLOWED_HTML.match(m.group(0)):
                problems.append("L%d inline HTML %s" % (i, m.group(0)[:36]))

    # Every row in a table block carries the same number of cells. Changing
    # the register table's shape silently breaks the site generator.
    block, start = [], 0
    for i, line in enumerate(lines + [""], 1):
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and len(s) > 1:
            if not block:
                start = i
            block.append(len(s.strip("|").split("|")))
        else:
            if len(block) >= 2 and len(set(block)) > 1:
                problems.append("L%d table block has mixed widths %s"
                                % (start, sorted(set(block))))
            block = []

    # Relative links resolve; in-document fragments name a real heading.
    anchors = {slugify(m.group(2))
               for m in re.finditer(r"^(#{1,6})\s+(.+)$", text, re.M)}
    here = os.path.dirname(path)
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        target, _, frag = href.partition("#")
        line_no = text[:m.start()].count("\n") + 1
        if target:
            if not os.path.exists(os.path.normpath(os.path.join(here, target))):
                problems.append("L%d broken link -> %s" % (line_no, href))
        elif frag and frag not in anchors:
            problems.append("L%d dead anchor -> #%s" % (line_no, frag))

    return problems, len(text.split())


def check_register():
    """The method register must parse to contiguous, unique method numbers.

    Deliberately not a hardcoded count. The failure this guards against is a
    malformed, duplicated or dropped row, and contiguity catches all three
    without needing to be edited every time a method is added.
    """
    with io.open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        text = fh.read()
    nums = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) == 5:
                first = re.sub(r"[*\s]", "", cells[0])
                if first.isdigit():
                    nums.append(int(first))
    problems = []
    if not nums:
        return ["register parsed to no rows at all"], 0
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if dupes:
        problems.append("duplicate method numbers %s" % dupes)
    expected = list(range(min(nums), max(nums) + 1))
    missing = sorted(set(expected) - set(nums))
    if missing:
        problems.append("missing method numbers %s" % missing)
    if nums != sorted(nums):
        problems.append("method rows are not in ascending order")
    return problems, len(nums)


def main():
    bad = 0
    for doc in DOCS:
        problems, words = check(doc)
        bad += len(problems)
        status = "clean" if not problems else "%d PROBLEMS" % len(problems)
        print("%-32s %6d words  %s" % (doc, words, status))
        for p in problems[:15]:
            print("      " + p)

    problems, n = check_register()
    bad += len(problems)
    print("\nmethod register: %d rows, %s"
          % (n, "contiguous and unique" if not problems else "INVALID"))
    for p in problems:
        print("      " + p)

    print("TOTAL PROBLEMS: %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
