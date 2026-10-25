#!/usr/bin/env python3
"""H3 analysis per O5_HUMAN_CODING_PROTOCOL_20261025.md: three readings + disagreement audit.
Run only after coder_H sheets landed (206 + 58 rows, integrity-checked 2026-10-25)."""
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent
E = {"E0":0,"E1":1,"E2":2}
TRANS = ["T1","T2","T3","T4","T5"]

def load(path, coder):
    return {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(path)) if r.get("coder")==coder}

H = load(ROOT/"CODING_sheets_human/coder_H.csv", "H")
A1 = load(ROOT/"CODING_sheets_v2/coder_A_E.csv", "A")
B1 = load(ROOT/"CODING_sheets_v2/coder_B_E.csv", "B")
A2 = load(ROOT/"CODING_sheets_validation/coder_A.csv", "A")
B2 = load(ROOT/"CODING_sheets_validation/coder_B.csv", "B")
import re as _re
_cmap = {}
for _r in csv.DictReader(open(ROOT / "CODING_sheets_v2/coder_A_E.csv")):
    _m = _re.search(r"fulltexts/(\S+)\.pdf$", _r["provenance_file"] or "")
    if _m: _cmap[_r["claim_id"]] = _m.group(1)
A1 = {(_cmap[c], t): r for (c, t), r in A1.items() if c in _cmap}
B1 = {(_cmap[c], t): r for (c, t), r in B1.items() if c in _cmap}
A = {**A1, **A2}; B = {**B1, **B2}
merged = {k: (min((A[k]["in_paper_grade"], B[k]["in_paper_grade"]), key=lambda g: E[g]),
              min((A[k]["external_evidence_grade"], B[k]["external_evidence_grade"]),
                  key=lambda g: {"E0":0,"E3":1,"E4":2}.get(g,0))) for k in A}
hl_H = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_human/headline_H.csv"))}
hl_A1 = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_v2/headline_A.csv"))}
hl_B1 = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_v2/headline_B.csv"))}
hl_A2 = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_validation/headline_A.csv"))}
hl_B2 = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_validation/headline_B.csv"))}
import re as _re2
_cmap2 = {}
for _r in csv.DictReader(open(ROOT / "CODING_sheets_v2/coder_A_E.csv")):
    _m = _re2.search(r"fulltexts/(\S+)\.pdf$", _r["provenance_file"] or "")
    if _m: _cmap2[_r["claim_id"]] = _m.group(1)
hl_A1 = {_cmap2[c]: t for c, t in hl_A1.items() if c in _cmap2}
hl_B1 = {_cmap2[c]: t for c, t in hl_B1.items() if c in _cmap2}
hl_A = {**hl_A1, **hl_A2}; hl_B = {**hl_B1, **hl_B2}
head_merged = {}
for c in hl_A:
    ta, tb = hl_A[c], hl_B[c]
    if ta == tb: head_merged[c] = ta; continue
    ga, gb = merged[(c,ta)][0], merged[(c,tb)][0]
    head_merged[c] = ta if E[ga] < E[gb] else (tb if E[gb] < E[ga] else ("T3" if "T3" in (ta,tb) else ta))

def wilson(k, n, z=1.959963985):
    import math
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*((p*(1-p)/n + z*z/(4*n*n))**0.5)/d
    return [round(100*max(0,c-h),1), round(100*min(1,c+h),1)]

prim_ids = sorted({c for c,t in H if t=="T1"})
val_ids = sorted({c for c,t in H if c not in prim_ids})

def dist(h, ids, ts):
    return {t: dict(Counter(h[(c,t)]["in_paper_grade"] for c in ids if (c,t) in h)) for t in ts}

def headline_stats(h, hlmap, ids, missing_ok=()):
    grades = {}
    skipped = []
    for c in ids:
        t = hlmap.get(c)
        if (c, t) not in h:
            skipped.append((c, t)); continue
        grades[c] = h[(c, t)]["in_paper_grade"]
    n = len(grades)
    e2 = sum(1 for g in grades.values() if g=="E2")
    return {"headline_e2plus": e2, "n_evaluated": n, "skipped_ungraded_headline": skipped,
            "share_pct": round(100*e2/n,1), "wilson95": wilson(e2, n)}

# reading 1: raw H
r1_prim = {"dist": dist(H, prim_ids, TRANS), **headline_stats(H, hl_H, prim_ids)}
r1_val = {"dist": dist(H, val_ids, ["T2","T3","T5"]), **headline_stats(H, hl_H, val_ids)}
# asymmetry under raw H
t2e2 = r1_prim["dist"]["T2"].get("E2",0); t3e2 = r1_prim["dist"]["T3"].get("E2",0)
asym_prim = {"T2_E2": f"{t2e2}/16", "T3_E2": f"{t3e2}/16",
             "direction": "T3>T2" if t3e2>t2e2 else ("T2>T3" if t2e2>t3e2 else "tie")}
v2e2 = r1_val["dist"]["T2"].get("E2",0); v3e2 = r1_val["dist"]["T3"].get("E2",0)
asym_val = {"T2_E2": f"{v2e2}/42", "T3_E2": f"{v3e2}/42",
            "direction": "T3>T2" if v3e2>v2e2 else ("T2>T3" if v2e2>v3e2 else "tie")}
# reading 3: agreement
def agree(cells):
    n = len(cells); a = sum(1 for k in cells if H[k]["in_paper_grade"]==A[k]["in_paper_grade"])
    b = sum(1 for k in cells if H[k]["in_paper_grade"]==B[k]["in_paper_grade"])
    m = sum(1 for k in cells if H[k]["in_paper_grade"]==merged[k][0])
    return {"n": n, "with_A_pct": round(100*a/n,1), "with_B_pct": round(100*b/n,1),
            "with_merge_pct": round(100*m/n,1)}
prim_cells = [(c,t) for c in prim_ids for t in TRANS]
val_cells = [(c,t) for c in val_ids for t in ("T2","T3","T5")]
ag = {"primary_80": agree(prim_cells), "validation_126": agree(val_cells)}
# grade-transition matrix (AI merged -> H) for T2, T3
def matrix(t, ids):
    mat = defaultdict(Counter)
    for c in ids:
        mat[merged[(c,t)][0]][H[(c,t)]["in_paper_grade"]] += 1
    return {k: dict(v) for k, v in sorted(mat.items())}
mtx = {"T2_primary": matrix("T2", prim_ids), "T3_primary": matrix("T3", prim_ids),
       "T2_validation": matrix("T2", val_ids), "T3_validation": matrix("T3", val_ids)}
# disputed-cell outcomes (AI A != B): H matches A / B / neither
def disputed(ids, ts):
    out = Counter(); tot = 0
    for c in ids:
        for t in ts:
            if A[(c,t)]["in_paper_grade"] != B[(c,t)]["in_paper_grade"]:
                tot += 1
                h = H[(c,t)]["in_paper_grade"]
                if h == A[(c,t)]["in_paper_grade"]: out["with_A"] += 1
                elif h == B[(c,t)]["in_paper_grade"]: out["with_B"] += 1
                else: out["neither"] += 1
    return {"total_disputed": tot, **dict(out)}
disp = {"primary": disputed(prim_ids, TRANS), "validation": disputed(val_ids, ("T2","T3","T5"))}
# headline agreement
hl_agree = sum(1 for c in prim_ids+val_ids if hl_H[c]==head_merged[c])
result = {
  "round": "H3_20261025", "coder": "H (delivered via WeChat 2026-10-25; provenance verified 206/206)",
  "reading1_raw_H": {"primary": r1_prim, "validation": r1_val,
    "asymmetry_primary": asym_prim, "asymmetry_validation": asym_val},
  "reading3_agreement": ag,
  "grade_transition_matrix": mtx,
  "disputed_cells": disp,
  "headline_agreement_with_AI_merge": f"{hl_agree}/58",
  "ai_merge_reference": {"primary_headline_e2plus": "10/16 = 62.5%",
                          "validation_headline_e2plus": "26/42 = 61.9%"},
}
out = ROOT/"CODING_sheets_human/H3_READING_20261025.json"
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
print("->", out.name)
