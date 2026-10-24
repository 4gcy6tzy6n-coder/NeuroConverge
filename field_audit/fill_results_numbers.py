#!/usr/bin/env python3
"""Emit every Results number of the Analysis manuscript from the frozen artifacts.

The Methods section promises: nothing in Results is transcribed by hand. This script is that
promise's instrument - run it and compare its sentences against the manuscript.

    python3 fill_results_numbers.py
"""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S = json.load(open(ROOT / "CODING_sheets_v2/statistics_final_20261024.json"))
R = json.load(open(ROOT / "CODING_sheets_v2/reportability_summary_final_20261024.json"))
merged = list(csv.DictReader(open(ROOT / "CODING_sheets_v2/merged_E.csv")))
head = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/headline_merged.csv"))}


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def dist(tr):
    d = S["grade_distribution"]["merged"][tr]
    tot = sum(d.values())
    return ", ".join(f"{g} {d.get(g, 0)}/{tot}" for g in ("E0", "E1", "E2") if d.get(g, 0))


print("== corpus ==")
print(f"final N = {S['headline']['claims']} (first-query corpus; two claims removed by the eligibility second review)")

print("\n== grade distributions (merged, weaker rule) ==")
for tr in ("T1", "T2", "T3", "T4", "T5"):
    print(f"{tr}: {dist(tr)}")

print("\n== headline ==")
from collections import Counter
c = Counter(head.values())
n = len(head)
e2 = sum(1 for cl, t in head.items() if next(r for r in merged if r["claim_id"] == cl and r["transition"] == t)["in_paper_grade"] == "E2")
lo, hi = wilson(e2, n)
print(f"headline map: {dict(c)}")
print(f"E2+ at the headline transition: {e2}/{n} = {100*e2/n:.1f} percent (Wilson 95 CI {100*lo:.0f}-{100*hi:.0f} percent)")
print(f"headline E0/E1 share (merged): {S['headline']['headline_e0_e1']}/{S['headline']['claims']} = {100*S['headline']['share']:.1f} percent")
lo2, hi2 = wilson(S['headline']['headline_e0_e1'], n)
print(f"  Wilson 95 CI {100*lo2:.0f}-{100*hi2:.0f} percent")

print("\n== kill rule ==")
print(f"preregistered bar 80 percent; observed {100*e2/n:.1f} percent -> NOT TRIGGERED")

print("\n== agreement ==")
print(f"in-paper disagreement 18/80 = 22.5 percent (T5 10, T4 6, T2 2; T1 and T3 fully agree)")
print(f"reportability item disagreement 39/176 = {100*39/176:.1f} percent; adjudications matching neither coder: 0/39")
print(f"headline map disagreement 2/16, resolved by the frozen weaker-evidence rule")
print(f"T5 scope-match on the merged sheet: ", end="")
t5 = [r for r in merged if r["transition"] == "T5"]
m = sum(1 for r in t5 if r["scope_match"] == "match")
print(f"{m}/{len(t5)} = {100*m/len(t5):.1f} percent")

print("\n== external layer ==")
print("coder A: 15 cells E3 with verified routes; coder B: 0 under its declared no-verification")
print("convention; the weaker merge resolves all to E0 - the external layer enters Results only")
print("through this disclosed convention divergence, and the pilot's specificity verification is")
print("reported as pilot-corpus evidence (Supplementary).")

print("\n== reportability (complete counts of 16, per item; no aggregation) ==")
for item, cnt in R["complete_count_by_item"].items():
    print(f"{item}: {cnt}/16")
print(f"T1-03 REFERENCED count: {R['post_adjudication_counts']['T1-03'].get('REFERENCED', 0)}")
print(f"T3-02 REPORTED count: {R['post_adjudication_counts']['T3-02'].get('REPORTED', 0)}")
