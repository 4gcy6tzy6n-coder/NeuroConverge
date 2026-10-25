#!/usr/bin/env python3
"""F4 closure verification (F4_TIE_RULE_DESIGNATION_20261026.md): assert the canonical headline
tie rule (T3 preference, else coder A) against the committed maps. Exits non-zero on any failure."""
import csv, json, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
E = {"E0":0,"E1":1,"E2":2}

def hl(path, coder=None):
    # headline sheets carry no coder column; the file name is the coder identity
    return {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(path))}

def merged_grade(A, B, k):
    return min((A[k]["in_paper_grade"], B[k]["in_paper_grade"]), key=lambda g: E[g])

def resolve(hlA, hlB, A_, B_, tie):
    # both rounds: the weaker merged grade wins; ties break per the round rule
    out = {}
    for c in hlA:
        ta, tb = hlA[c], hlB[c]
        if ta == tb: out[c] = ta; continue
        ga, gb = E[merged_grade(A_, B_, (c, ta))], E[merged_grade(A_, B_, (c, tb))]
        if ga < gb: out[c] = ta
        elif gb < ga: out[c] = tb
        elif tie == "canonical": out[c] = "T3" if "T3" in (ta, tb) else ta
        else: out[c] = ta
    return out

fail = []
# validation
A2 = {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(ROOT/"CODING_sheets_validation/coder_A.csv"))}
B2 = {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(ROOT/"CODING_sheets_validation/coder_B.csv"))}
hlA2 = hl(ROOT/"CODING_sheets_validation/headline_A.csv", "A")
hlB2 = hl(ROOT/"CODING_sheets_validation/headline_B.csv", "B")
vmap = resolve(hlA2, hlB2, A2, B2, "canonical")
vcounts = Counter(vmap.values())
V = json.load(open(ROOT/"CODING_sheets_validation/statistics_validation_20261025.json"))
if dict(vcounts) != V["headline_merged_map"]:
    fail.append(f"validation map under canonical rule {dict(vcounts)} != committed {V['headline_merged_map']}")
# primary
A1raw = list(csv.DictReader(open(ROOT/"CODING_sheets_v2/coder_A_E.csv")))
import re
cmap = {}
for r in A1raw:
    m = re.search(r"fulltexts/(\S+)\.pdf$", r["provenance_file"] or "")
    if m: cmap[r["claim_id"]] = m.group(1)
A1 = {(cmap[r["claim_id"]], r["transition"]): r for r in A1raw if r["claim_id"] in cmap}
B1raw = list(csv.DictReader(open(ROOT/"CODING_sheets_v2/coder_B_E.csv")))
B1 = {(cmap[r["claim_id"]], r["transition"]): r for r in B1raw if r["claim_id"] in cmap}
hlA1 = {cmap[r["claim_id"]]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_v2/headline_A.csv")) if r["claim_id"] in cmap}
hlB1 = {cmap[r["claim_id"]]: r["headline_transition"] for r in csv.DictReader(open(ROOT/"CODING_sheets_v2/headline_B.csv")) if r["claim_id"] in cmap}
pmap = resolve(hlA1, hlB1, A1, B1, "canonical")
pcounts = Counter(pmap.values())
if pcounts != Counter({"T3": 16}):
    fail.append(f"primary map under canonical rule {dict(pcounts)} != disclosed 16xT3")
if pmap.get("1811.09699v1") != "T3":
    fail.append("C077/1811.09699v1 must resolve to T3 under the canonical rule")
# E2 invariance under both rules
pmap_h = resolve(hlA1, hlB1, A1, B1, "historical")
vmap_h = resolve(hlA2, hlB2, A2, B2, "historical")
def headline_e2(map_, A_, B_):
    n = len(map_); e2 = sum(1 for c, t in map_.items()
                            if merged_grade(A_, B_, (c, t)) == "E2")
    return e2, n
e2p_c, np_ = headline_e2(pmap, A1, B1)
e2p_h, _ = headline_e2(pmap_h, A1, B1)
e2v_c, nv_ = headline_e2(vmap, A2, B2)
e2v_h, _ = headline_e2(vmap_h, A2, B2)
if Counter(pmap_h.values()) != Counter({"T3": 15, "T2": 1}):
    fail.append(f"historical primary map {dict(Counter(pmap_h.values()))} != committed 15xT3+1xT2")
if not (e2p_c == e2p_h == 10 and np_ == 16): fail.append(f"primary headline E2 not invariant: canonical {e2p_c}, historical {e2p_h}")
if not (e2v_c == e2v_h == 26 and nv_ == 42): fail.append(f"validation headline E2 not invariant: canonical {e2v_c}, historical {e2v_h}")
if fail:
    print("F4 CLOSURE VERIFICATION: FAIL"); [print("  -", f) for f in fail]; sys.exit(1)
print("F4 CLOSURE VERIFICATION: PASS (validation map reproduces committed counts under the canonical rule; primary canonical map = 16xT3 with C077->T3 as disclosed, historical = 15xT3+1xT2; headline E2+ 10/16 and 26/42 invariant under both rules)")
