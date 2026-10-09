#!/usr/bin/env python3
"""Reusable artifact checker for the NeuroConverge v2 line.

Written after five consecutive rounds in which the ONLY failed checks were the checks themselves.
The four failure modes, all now handled by construction:

  1. whitespace            -- a phrase broken by a line wrap never matched.  Everything is normalised
                              to single spaces before matching, on both sides.
  2. wrong file            -- a sentence from one document searched for in another.  Each requirement
                              must name its own file or say ALL.
  3. wording drift         -- "should not" checked as "must not".  Requirements accept a LIST of
                              alternative substrings, so intent is testable without demanding one
                              phrasing.
  4. undiagnosable failure -- a bare FAIL gave no clue.  On failure the checker prints where it
                              searched, how many characters, and the closest near-miss it can find.

Usage:
    python3 check_artifacts.py <<'SPEC'
    # one requirement per line:  FILE :: label :: substr1 | substr2 | ...
    # FILE is a path relative to v2/, or ALL to search every text artifact.
    # Alternatives are separated by ';;'  (NOT '|', which regex needles need).
    # Prefix the label with '!' to require ABSENCE instead of presence.
    # A needle written  re:<pattern>  is treated as a regular expression (multiline).
    # A needle written  num:<value>   matches a number with 5e-4 relative tolerance, so a rounded
    #                                 figure quoted in prose matches its full-precision JSON value.
    ALL :: the animal is the unit :: Unit: the animal | the unit is the animal
    wp3_results/X.md :: some number :: 0.7289
    SPEC

Exit code is the number of failed requirements, so it can gate a commit.
"""
import sys, pathlib, re, difflib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = (".md", ".json", ".csv", ".py", ".yaml", ".yml", ".txt")


def norm(s: str) -> str:
    """Collapse all whitespace, so a phrase broken across lines still matches."""
    return re.sub(r"\s+", " ", s)


def collect(which: str) -> tuple[str, str]:
    """Return (normalised text, human description of what was searched)."""
    if which.upper() == "ALL":
        parts, names = [], []
        for p in sorted(ROOT.rglob("*")):
            if p.is_file() and p.suffix in TEXT_SUFFIXES:
                try:
                    parts.append(p.read_text(errors="replace"))
                    names.append(str(p.relative_to(ROOT)))
                except Exception:
                    pass
        return norm("\n".join(parts)), f"ALL ({len(names)} files)"
    p = (ROOT / which) if not pathlib.Path(which).is_absolute() else pathlib.Path(which)
    if not p.exists():
        return "", f"{which} (MISSING)"
    return norm(p.read_text(errors="replace")), which


def near_miss(hay: str, needles: list[str], width: int = 60) -> str:
    """Find the closest thing in hay to any needle, so a failure is diagnosable."""
    words = [w for n in needles for w in n.split() if len(w) > 3]
    if not words or not hay:
        return "(nothing to compare)"
    best = (0.0, "")
    for w in words[:12]:
        for m in re.finditer(re.escape(w), hay):
            frag = hay[max(0, m.start() - width): m.start() + width]
            r = difflib.SequenceMatcher(None, w, w).ratio()
            if r >= best[0]:
                best = (r, frag)
        if best[0] > 0:
            break
    return best[1] if best[1] else "(no word from the requirement found at all)"


def main() -> int:
    spec = sys.stdin.read().strip().splitlines()
    reqs = [l for l in spec if l.strip() and not l.strip().startswith("#")]
    failures = 0
    for line in reqs:
        parts = [x.strip() for x in line.split("::")]
        if len(parts) != 3:
            print(f"BAD SPEC LINE: {line!r}"); failures += 1; continue
        which, label, alts = parts
        # a leading '!' on the label means the requirement is ABSENCE, not presence
        absent = label.startswith("!")
        if absent:
            label = label.lstrip("! ").strip()
        # separator is ';;' NOT '|', because a regex needle needs '|' for alternation
        needles = [a.strip() for a in alts.split(";;") if a.strip()]
        hay, desc = collect(which)
        # a needle written  re:<pattern>  is a REGEX, so a requirement can be context-aware.
        # This matters: a plain substring test cannot tell a placeholder from a sentence ABOUT
        # placeholders, which is this project's known "guard satisfied by a substring" defect class.
        def matches(n: str) -> bool:
            if n.startswith("re:"):
                try:
                    return re.search(n[3:], hay, re.M) is not None
                except re.error:
                    return False
            if n.startswith("num:"):
                # numeric match with tolerance: a rounded value in a document and the full-precision
                # value in a JSON are the SAME fact, and a substring test cannot see that.
                try:
                    want = float(n[4:])
                except ValueError:
                    return False
                tol = max(5e-4, abs(want) * 5e-4)
                for m in re.finditer(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", hay):
                    try:
                        if abs(float(m.group(0)) - want) <= tol:
                            return True
                    except ValueError:
                        pass
                return False
            return norm(n) in hay
        hits = [n for n in needles if matches(n)]
        if absent:
            ok = not hits
            found = hits
        else:
            ok = bool(hits)
            found = [hits[0]] if hits else []
        if ok:
            print(f"  OK    {label}" + ("  [absence]" if absent else ""))
        else:
            failures += 1
            print(f"  FAIL  {label}")
            print(f"          searched : {desc}  ({len(hay)} chars)")
            want = "NONE of" if absent else "one of"
            print(f"          wanted   : {want} {needles}")
            if absent:
                print(f"          FOUND    : {found}")
            print(f"          nearest  : ...{near_miss(hay, needles)}...")
    total = len(reqs)
    print(f"\n  {total - failures}/{total} passed")
    return failures


if __name__ == "__main__":
    sys.exit(main())
