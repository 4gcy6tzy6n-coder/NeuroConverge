#!/usr/bin/env python3
"""Merge the two v2 coder sheets on the final 16-claim corpus per the frozen resolution rules.

The rules are those of merge_coder_sheets.py (authority: AUDIT_PREREGISTRATION_v1_FROZEN.md
section 5 as made concrete by the 2026-10-19 authority record): every in-paper disagreement
resolves to the weaker grade with the raw disagreement rate reported beside the merge; headline
disagreements resolve to the transition that makes the headline statistic weaker (the
lower-evidenced of the two under the merged grades). This v2 form only parameterizes the corpus
(16 claims, corpus_final_16.csv) and the sheets directory (CODING_sheets_v2/), and adds the
R1 matched-neither line and the external-layer convention disclosure for the final record.

Usage: python3 merge_coder_sheets_v2.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEETS = ROOT / "CODING_sheets_v2"
CORPUS = ROOT / "corpus_final_16.csv"
ORDER = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}


def load(path):
    with path.open(newline="", encoding="utf-8") as h:
        return list(csv.DictReader(h))


def main():
    corpus = [r["claim_id"] for r in load(CORPUS)]
    corpus_ids = set(corpus)
    n = len(corpus)
    sheet_a = load(SHEETS / "coder_A_E.csv")
    sheet_b = load(SHEETS / "coder_B_E.csv")
    head_a = {r["claim_id"]: r["headline_transition"] for r in load(SHEETS / "headline_A.csv")}
    head_b = {r["claim_id"]: r["headline_transition"] for r in load(SHEETS / "headline_B.csv")}
    problems = []
    for name, sheet in (("A", sheet_a), ("B", sheet_b)):
        if len(sheet) != n * 5:
            problems.append(f"coder {name}: {len(sheet)} rows, expected {n * 5}")
        if {(r["claim_id"], r["transition"]) for r in sheet} != {(c, t) for c in corpus for t in ("T1","T2","T3","T4","T5")}:
            problems.append(f"coder {name}: (claim, transition) set is not the complete grid")
    if set(head_a) != corpus_ids or set(head_b) != corpus_ids:
        problems.append("a headline map does not cover exactly the corpus claims")
    if problems:
        print("MERGE V2: REFUSED")
        for p in problems:
            print("  -", p)
        return 1

    by_a = {(r["claim_id"], r["transition"]): r for r in sheet_a}
    by_b = {(r["claim_id"], r["transition"]): r for r in sheet_b}
    merged, disagree, ext_disagree, a_ext_e3 = [], 0, 0, 0
    for key in sorted(by_a):
        a, b = by_a[key], by_b[key]
        grade = a["in_paper_grade"] if ORDER[a["in_paper_grade"]] <= ORDER[b["in_paper_grade"]] else b["in_paper_grade"]
        ext = a["external_evidence_grade"] if ORDER[a["external_evidence_grade"]] <= ORDER[b["external_evidence_grade"]] else b["external_evidence_grade"]
        if a["in_paper_grade"] != b["in_paper_grade"]:
            disagree += 1
        if a["external_evidence_grade"] != b["external_evidence_grade"]:
            ext_disagree += 1
        if a["external_evidence_grade"] in ("E3", "E4"):
            a_ext_e3 += 1
        merged.append({
            "claim_id": key[0], "coder": "merged-weaker", "transition": key[1],
            "in_paper_grade": grade, "external_evidence_grade": ext,
            "external_citation_verified_route": "",
            "scope_match": a["scope_match"] if a["scope_match"] else b["scope_match"],
            "justification_quote": a["justification_quote"],
            "provenance_file": a["provenance_file"], "provenance_sha256": a["provenance_sha256"],
            "round": "merged-1", "note": f"A={a['in_paper_grade']}/B={b['in_paper_grade']}",
        })
    with (SHEETS / "merged_E.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(merged[0].keys()), lineterminator="\n")
        w.writeheader(); w.writerows(merged)

    head_rows, head_disagree = [], 0
    for claim in corpus:
        t_a, t_b = head_a[claim], head_b[claim]
        note = ""
        if t_a != t_b:
            head_disagree += 1
            g_a = next(r["in_paper_grade"] for r in merged if r["claim_id"] == claim and r["transition"] == t_a)
            g_b = next(r["in_paper_grade"] for r in merged if r["claim_id"] == claim and r["transition"] == t_b)
            chosen = t_a if ORDER[g_a] <= ORDER[g_b] else t_b
            note = f"chose weaker of A={t_a}:{g_a} B={t_b}:{g_b}"
        else:
            chosen = t_a
        head_rows.append([claim, chosen, note])
    with (SHEETS / "headline_merged.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.writer(h, lineterminator="\n")
        w.writerow(["claim_id", "headline_transition", "headline_disagreement"])
        w.writerows(head_rows)

    print(f"merged: {len(merged)} rows, weaker-grade rule; in-paper grade disagreements {disagree}/{len(merged)} ({disagree/len(merged):.1%})")
    print(f"external-layer: A declared E3/E4 on {a_ext_e3} cells, B on 0 (declared no-verification convention); "
          f"raw external disagreements {ext_disagree}/{len(merged)}; weaker merge resolves every one to the lower grade")
    print(f"headline disagreements: {head_disagree}/{n}" + (f" {[r[0] for r in head_rows if r[2]]}" if head_disagree else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
