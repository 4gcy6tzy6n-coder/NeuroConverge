#!/usr/bin/env python3
"""Validation-corpus statistics per the frozen protocol (VALIDATION_RESUMPTION_20261025.md
section 4 + VALIDATION_ACCEPTANCE_AMENDMENT_20261025.md): weaker-grade merge of two coders,
merged headline map (weaker-evidence resolution), kill-rule check (80 percent E2+ at headline),
disagreement rates. Selftest exercises the merge and headline rules on mutants."""
import csv, json, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
E_ORDER = {"E0": 0, "E1": 1, "E2": 2}
TRANS = ["T1", "T2", "T3", "T4", "T5"]

def load(path, coder):
    rows = list(csv.DictReader(open(path)))
    return {(r["claim_id"], r["transition"]): r for r in rows if r["coder"] == coder}

def merge(a, b):
    """Weaker-grade merge per cell for in_paper and external; returns merged dict."""
    out = {}
    for k in a:
        ra, rb = a[k], b[k]
        out[k] = {
            "in": min(ra["in_paper_grade"], rb["in_paper_grade"], key=lambda g: E_ORDER.get(g, 0)),
            "ext": min(ra["external_evidence_grade"], rb["external_evidence_grade"],
                       key=lambda g: E_ORDER.get(g, 0) if g in E_ORDER else (3 if g in ("E3","E4") else 0)),
        }
    return out

def ext_key(g):
    # external scale: E0 < E3 < E4 for the weaker merge
    return {"E0": 0, "E3": 1, "E4": 2}[g] if g in ("E0","E3","E4") else 0

def merge_sheets(a_rows, b_rows):
    merged = {}
    for k in a_rows:
        merged[k] = (min((a_rows[k]["in_paper_grade"], b_rows[k]["in_paper_grade"]), key=lambda g: E_ORDER.get(g, 0)),
                     min((a_rows[k]["external_evidence_grade"], b_rows[k]["external_evidence_grade"]), key=ext_key))
    return merged

def headline_merged(hl_a, hl_b, merged):
    """Per frozen rule: where coders disagree, the claim rests on the candidate transition
    with the WEAKER merged in-paper grade (ties -> the coder pair's T3 preference if one is
    T3, else A's choice; recorded)."""
    out = {}
    notes = []
    for cid in hl_a:
        ta, tb = hl_a[cid], hl_b[cid]
        if ta == tb:
            out[cid] = ta
            continue
        ga, gb = merged[(cid, ta)][0], merged[(cid, tb)][0]
        if E_ORDER[ga] < E_ORDER[gb]:
            pick = ta
        elif E_ORDER[gb] < E_ORDER[ga]:
            pick = tb
        elif "T3" in (ta, tb):
            pick = "T3"
        else:
            pick = ta
        out[cid] = pick
        notes.append(f"{cid}: A={ta}({ga}) B={tb}({gb}) -> {pick}")
    return out, notes

def selftest():
    a = {("c1","T1"): {"in_paper_grade":"E2","external_evidence_grade":"E0"},
         ("c1","T3"): {"in_paper_grade":"E1","external_evidence_grade":"E0"},
         ("c1","T2"): {"in_paper_grade":"E1","external_evidence_grade":"E0"},
         ("c1","T4"): {"in_paper_grade":"E1","external_evidence_grade":"E0"},
         ("c1","T5"): {"in_paper_grade":"E1","external_evidence_grade":"E0"}}
    b = {("c1","T1"): {"in_paper_grade":"E0","external_evidence_grade":"E3"},
         ("c1","T3"): {"in_paper_grade":"E2","external_evidence_grade":"E0"},
         ("c1","T2"): {"in_paper_grade":"E0","external_evidence_grade":"E0"},
         ("c1","T4"): {"in_paper_grade":"E2","external_evidence_grade":"E0"},
         ("c1","T5"): {"in_paper_grade":"E0","external_evidence_grade":"E0"}}
    m = merge_sheets(a, b)
    ok = [("weaker in-paper merge", m[("c1","T1")][0] == "E0" and m[("c1","T3")][0] == "E1"),
          ("weaker external merge", m[("c1","T1")][1] == "E0")]
    hl_a = {"c1": "T3"}; hl_b = {"c1": "T1"}
    hm, notes = headline_merged(hl_a, hl_b, m)
    ok.append(("headline weaker-grade pick", hm["c1"] == "T1"))  # T1 merged E0 < T3 merged E1
    hl_b2 = {"c1": "T4"}  # T4 merged E1 ties T3 E1 -> T3 preference
    hm2, _ = headline_merged(hl_a, hl_b2, m)
    ok.append(("headline tie -> T3", hm2["c1"] == "T3"))
    bad = [n for n, p in ok if not p]
    if bad:
        print("SELFTEST FAIL:", bad); sys.exit(1)
    print(f"SELFTEST PASS ({len(ok)} assertions)")

if __name__ == "__main__" and "--selftest" in sys.argv:
    selftest(); sys.exit(0)

def main():
    A = load(ROOT / "CODING_sheets_validation/coder_A.csv", "A")
    B = load(ROOT / "CODING_sheets_validation/coder_B.csv", "B")
    corpus = [r["arxiv_id_version"] for r in csv.DictReader(open(ROOT / "corpus_validation_v2_adjudicated.csv"))]
    hl_a = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_validation/headline_A.csv"))}
    hl_b = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_validation/headline_B.csv"))}
    assert set(A) == set(B) and len(A) == 210, "sheet mismatch"
    merged = merge_sheets(A, B)
    hm, hnotes = headline_merged(hl_a, hl_b, merged)

    # distributions
    per_t = {t: Counter() for t in TRANS}
    for (cid, t), (ing, extg) in merged.items():
        per_t[t][ing] += 1
    disagree_cells = [(k, A[k]["in_paper_grade"], B[k]["in_paper_grade"]) for k in A if A[k]["in_paper_grade"] != B[k]["in_paper_grade"]]
    ext_disagree = [k for k in A if A[k]["external_evidence_grade"] != B[k]["external_evidence_grade"]]
    hl_disagree = [c for c in corpus if hl_a[c] != hl_b[c]]
    # headline E2+ share and kill rule
    headline_grades = {c: merged[(c, hm[c])][0] for c in corpus}
    n_e2plus = sum(1 for g in headline_grades.values() if g == "E2")
    n_e0e1 = sum(1 for g in headline_grades.values() if g in ("E0", "E1"))
    kill = (n_e2plus / len(corpus)) >= 0.80
    # Wilson interval (same routine as final corpus)
    def wilson(p, n, z=1.959963985):
        import math
        if n == 0: return (0.0, 1.0)
        d = 1 + z*z/n
        c = (p + z*z/(2*n)) / d
        h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
        return (max(0.0, c - h), min(1.0, c + h))
    share = n_e2plus / len(corpus)
    lo, hi = wilson(share, len(corpus))
    scope_a = Counter(A[(c, "T5")]["scope_match"] for c in corpus)
    scope_b = Counter(B[(c, "T5")]["scope_match"] for c in corpus)

    result = {
        "round": "validation_v2_20261025", "n_claims": len(corpus),
        "per_transition_merged": {t: dict(per_t[t]) for t in TRANS},
        "in_paper_disagreement": {"cells": len(disagree_cells), "of": 210,
                                  "rate_pct": round(100 * len(disagree_cells) / 210, 1),
                                  "by_transition": dict(Counter(k[1] for k, _, _ in disagree_cells))},
        "external_disagreement_cells": len(ext_disagree),
        "headline_disagreements": {"n": len(hl_disagree), "resolutions": hnotes},
        "headline_merged_map": dict(Counter(hm[c] for c in corpus)),
        "headline_e2plus": n_e2plus, "headline_e0_e1": n_e0e1,
        "headline_e2plus_share_pct": round(100 * share, 1),
        "headline_e2plus_wilson95_pct": [round(100 * lo, 1), round(100 * hi, 1)],
        "kill_rule_80pct_e2plus": {"triggered": kill, "bar_pct": 80},
        "scope_match_per_coder": {"A": dict(scope_a), "B": dict(scope_b)},
    }
    out = ROOT / "CODING_sheets_validation/statistics_validation_20261025.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print("->", out.name)


if __name__ == "__main__":
    main()
