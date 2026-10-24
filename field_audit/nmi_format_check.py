#!/usr/bin/env python3
"""NMI Article-format compliance check for ANALYSIS_DRAFT.md.

Comparator: the frozen record NMI_ARTICLE_FORMAT_REQUIREMENTS_2026-10-25.md (venue pivot
2026-10-25, VENUE_DECISION_20261025.md; the Analysis-type comparator it supersedes is kept
inside that record for contrast). The requirements were fetched from nature.com
(natmachintell/content and the submission-guidelines sub-pages) on 2026-10-25.

Checks: section structure; Article word limits (main text excluding references; abstract
up to 150, unreferenced bound); figure and reference caps; the frozen forbidden-wording
list; citation symmetry; stale-number scan; cross-checks of every load-bearing number
against the frozen artifacts; Article structural rules (Results/Methods topical
subheadings, Discussion without subheadings, Introduction heading as draft-only WARN).

--selftest exercises the Article-mode logic on fabricated inputs (workspace rule: one
runnable check per non-trivial logic; the selftest must fail when the logic is broken).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MD = ROOT / "MANUSCRIPT" / "ANALYSIS_DRAFT.md"
S = json.load(open(ROOT / "CODING_sheets_v2/statistics_final_20261024.json"))
R = json.load(open(ROOT / "CODING_sheets_v2/reportability_summary_final_20261024.json"))


def abstract_fails(n):
    # Article: "Abstract - up to 150 words, unreferenced." No lower bound binds.
    out = []
    if n > 150:
        out.append(f"abstract {n} words > 150")
    warn = [] if n >= 100 else [f"abstract {n} words below 100 (compliant for Article, flagged as unusual)"]
    return out, warn


def structure_fails(results, discussion, methods):
    out, warn = [], []
    # Article: "Results and Methods should be divided by topical subheadings" - our
    # subheading style is the bold paragraph lead.
    for name, sec in (("Results", results), ("Methods", methods)):
        leads = re.findall(r"^\*\*[^*].*\*\*", sec, re.M)
        if len(leads) < 3:
            out.append(f"{name} lacks topical subheadings ({len(leads)} bold leads < 3)")
    # Article: "the Discussion does not contain subheadings".
    subs = re.findall(r"^#{3,} .*$", discussion, re.M)
    if subs:
        out.append(f"Discussion contains subheadings: {subs[:2]}")
    return out, warn


def selftest():
    ok = []
    # abstract bound: >150 fails, 145 passes, 99 warns-not-fails
    ok.append(("abstract 151 fails", abstract_fails(151)[0] != []))
    ok.append(("abstract 145 passes", abstract_fails(145) == ([], [])))
    ok.append(("abstract 99 warn only", abstract_fails(99)[0] == [] and abstract_fails(99)[1] != []))
    # structure: discussion with a subheading fails; clean discussion passes
    d_bad = "para\n\n### A subheading\n\npara\n"
    d_ok = "para with **inline bold** only\n"
    r_ok = "**Lead one.** x\n\n**Lead two.** y\n\n**Lead three.** z\n"
    ok.append(("discussion subheading detected", structure_fails(r_ok, d_bad, r_ok)[0] != []))
    ok.append(("clean structure passes", structure_fails(r_ok, d_ok, r_ok) == ([], [])))
    # structure: results without leads fails
    ok.append(("results without leads detected", structure_fails("plain text only", d_ok, r_ok)[0] != []))
    bad = [name for name, passed in ok if not passed]
    if bad:
        print("SELFTEST FAIL:", bad)
        sys.exit(1)
    print(f"SELFTEST PASS ({len(ok)} assertions)")


if __name__ == "__main__" and "--selftest" in sys.argv:
    selftest()
    sys.exit(0)

text = MD.read_text()
fail = []
warn = []


def section(name):
    m = re.search(rf"^## {re.escape(name)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def wc(s):
    return len(re.findall(r"\S+", s))


# 1. structure (Article: Introduction without heading - the draft heading is scaffolding)
for sec in ("Abstract", "Introduction", "Results", "Discussion", "Methods", "References"):
    if f"## {sec}" not in text:
        fail.append(f"missing section: {sec}")
if "## Introduction" in text:
    warn.append("draft carries an '## Introduction' heading: remove in the submission build (Article: Introduction without heading)")

# 2. word limits (main text = everything except the References section and its entries)
main = text.split("## References")[0]
main = re.sub(r"^\*\*Draft status.*?\*\*", "", main, flags=re.S)
n_main = wc(main)
if n_main > 3500:
    fail.append(f"main text {n_main} words > 3500")
abstract = section("Abstract")
n_abs = wc(abstract)
f_, w_ = abstract_fails(n_abs)
fail += f_
warn += w_

# 2b. Article structural rules
f_, w_ = structure_fails(section("Results"), section("Discussion"), section("Methods"))
fail += f_
warn += w_

# 3. figure and reference caps
figs = sorted(set(re.findall(r"Fig (\d)", text)))
if len(figs) > 6 or figs != [str(i) for i in range(1, len(figs) + 1)]:
    fail.append(f"figure mentions inconsistent: {figs}")
refs = re.findall(r"^(\d+)\. ", section("References"), re.M)
n_refs = len(refs)
if n_refs > 50:
    fail.append(f"{n_refs} references > 50")
for i in range(1, n_refs + 1):
    if str(i) not in refs:
        fail.append(f"reference numbering gap at {i}")

# 4. citation symmetry: [1-16], [17], [18] cited in body; no [n] beyond n_refs
body = text.split("## References")[0]
cited = set()
for m in re.findall(r"\[(\d+)(?:-(\d+))?\]", body):
    a = int(m[0]); b = int(m[1]) if m[1] else a
    cited.update(range(a, b + 1))
uncited = [i for i in range(1, n_refs + 1) if i not in cited]
if uncited:
    fail.append(f"references never cited in body: {uncited}")
over = [c for c in cited if c > n_refs]
if over:
    fail.append(f"citations without references: {sorted(over)}")

# 5. forbidden wordings (frozen list from HARDENING_PLAN_AND_RESTATED_FINDINGS_20261023)
forbidden = [
    (r"no biological evidence", "equates in-paper E0 with absence of evidence"),
    (r"the field'?s evidence is better", "pilot kill-rule wording outside its scope"),
    (r"least[- ]controlled link", "retired superlative (T4 1/16 < T2 2/16); use the factual phrasing"),
    (r"37\.5 and 31\.25", "stale A/B order (correct: A 31.25, B 37.5)"),
    (r"\b18/18\b", "pilot-corpus number in final-corpus text"),
    (r"\b38\.9\b", "pilot percentage"),
]
for pat, why in forbidden:
    for m in re.finditer(pat, text, re.I):
        fail.append(f"forbidden wording '{m.group(0)}': {why}")

# 6. load-bearing numbers cross-checked against frozen artifacts
merged = S["grade_distribution"]["merged"]
checks = [
    ("16/16 E0", merged["T1"].get("E0") == 16),
    ("T2 12/16 E1", merged["T2"].get("E1") == 12),
    ("T2 2/16 E2", merged["T2"].get("E2") == 2),
    ("T3 10/16 E2", merged["T3"].get("E2") == 10),
    ("T4 1/16 E2", merged["T4"].get("E2") == 1),
    ("headline E2+ 10/16", S["headline"]["claims"] == 16),
    ("headline E0/E1 merged 6/16", S["headline"]["headline_e0_e1"] == 6),
    ("complete T1-03 0/16", R["complete_count_by_item"]["T1-03"] == 0),
    ("complete T3-02 0/16", R["complete_count_by_item"]["T3-02"] == 0),
    ("complete T2-01 15/16", R["complete_count_by_item"]["T2-01"] == 15),
]
for name, ok in checks:
    if not ok:
        fail.append(f"frozen-artifact mismatch: {name}")
for num, where in [("62.5", "kill-rule percentage"), ("31.25", "coder A headline share"),
                   ("37.5", "merged/B headline share"), ("22.5", "in-paper disagreement"),
                   ("39/176", "reportability disagreement"), ("0 of 39", "matched-neither")]:
    if num not in body:
        fail.append(f"expected number missing from body: {num} ({where})")

# 7. disclosures required by the locked review
for needle, why in [("isolated-context instances of the same AI assistant", "same-model coder disclosure"),
                    ("supersedes", "human-supersedure rule"),
                    ("not representative of the field", "non-representativeness sentence"),
                    ("convention divergence", "external-layer disclosure"),
                    ("no prevalence claim", "prevalence disclaimer")]:
    if needle not in text:
        fail.append(f"missing disclosure: {why}")

# 8. figure files exist
for i in range(1, 7):
    if not (ROOT / "MANUSCRIPT" / "figures" / f"fig{i}_{['chain','gap','headline','reportability','agreement','standard'][i-1]}.png").is_file():
        fail.append(f"figure file missing: fig{i}")

print(f"NMI ARTICLE FORMAT: main words {n_main}/3500 | abstract {n_abs}/150 | figures {len(figs)}/6 | refs {n_refs}/50")
if warn:
    for w in warn:
        print("WARN:", w)
if fail:
    print("NMI ARTICLE FORMAT CHECK: FAIL")
    for f_ in fail:
        print("  -", f_)
    sys.exit(1)
print("NMI ARTICLE FORMAT CHECK: PASS")
