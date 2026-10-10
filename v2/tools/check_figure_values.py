"""Every data literal in a figure script must appear in the artifact that is supposed to source it.

Exit codes: 0 = every literal traced, N = N literals untraceable, 3 = SKIPPED because the corpus was not visible.
The third status exists because an isolated reviewer found that returning 0 for the skip made it
indistinguishable from a pass at the level a commit gate reads.

Round 50 found Figure 6's table typed from memory: both the defect names and their round numbers were
invented.  Round 53 scanned the remaining figure script and found Figure 1's thirteen data literals ARE all
traceable, and one apparent stray (0.505) is the y-position of a text label rather than data.

That scan is worth keeping, because a typed value can drift from its source silently.  This script does not
GENERATE the figures; it checks that a script's numeric literals exist somewhere in the corpus, so a value
that was invented or has drifted is caught before anyone renders it.
"""
import re, pathlib, sys

# line-level exclusions: styling and layout parameters are not data
STYLE = re.compile(r"(figsize|ms=|lw=|fontsize|linewidth|width=|alpha=|color=|ncol|dpi|savefig|"
                   r"set_xlim|set_ylim|set_xticks|set_yticks|axhline|axvline|text\(|locs|"
                   r"arange|randint|seed|rcParams|fig,|plt\.|markersize|s=|ha=|va=)")
# numeric literals that look like data: three or more decimals
NUMLIT = re.compile(r"(?<![\w.])(\d+\.\d{2,})(?![\w])")

def data_literals(script: pathlib.Path):
    out = []
    for i, line in enumerate(script.read_text().split("\n"), 1):
        s = line.strip()
        if s.startswith("#") or STYLE.search(line):
            continue
        for m in NUMLIT.finditer(line):
            out.append((i, m.group(1), s[:100]))
    return out

def corpus(root: pathlib.Path):
    text = ""
    for p in list(root.rglob("*.md")) + list(root.rglob("*.json")):
        if "figures" in p.parts or "tools" in p.parts:
            continue
        try:
            text += p.read_text(errors="replace") + "\n"
        except Exception:
            pass
    return text

def main():
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("v2")
    scripts = sorted(root.glob("figures/*.py"))
    if not scripts:
        print("  SKIP: no figure scripts found under <root>/figures/", file=sys.stderr)
        return 0                      # a check that cannot see its input skips, never passes silently
    hay = corpus(root)
    # A check that cannot see its input must SKIP with a reason, never report a failure it cannot distinguish
    # from a real mismatch.  Found by mutating the --root to a tree with no artifacts: without this guard the
    # script reported all fourteen literals as untraceable, which conflates "the artifact disagrees" with
    # "there are no artifacts".
    if len(hay) < 10000:
        print(f"  SKIP: the artifact corpus under {root} is {len(hay)} chars, too small to verify against.",
              file=sys.stderr)
        print(f"  SKIP REASON: the check cannot see its input; this is NOT a pass.", file=sys.stderr)
        # A DISTINCT exit status, because an isolated reviewer recorded that returning 0 made the skip
        # indistinguishable from a pass at the level a commit gate reads.
        return 3
    fails = 0
    for s in scripts:
        lits = data_literals(s)
        print(f"  {s.name}: {len(lits)} data literals")
        for ln, v, src in lits:
            if v not in hay:
                print(f"    FAIL  L{ln}  {v}  not found in any artifact")
                print(f"            {src}")
                fails += 1
    print(f"\n  {fails} literal(s) not traceable to an artifact")
    return fails

if __name__ == "__main__":
    sys.exit(main())
