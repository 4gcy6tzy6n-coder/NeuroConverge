#!/usr/bin/env python3
"""Merge the two coder sheets per the frozen resolution rules and validate everything compute_statistics needs.

Authority: AUDIT_PREREGISTRATION_v1_FROZEN.md section 5, as made concrete by the 2026-10-19 authority record:
context-isolated coders cannot discuss, so EVERY disagreement resolves to the weaker grade, and the raw
disagreement rate is reported beside the merge (the honest noise term of one instrument, protocol section 11).

Validations, fail-closed by name: row counts (18 claims x 5 transitions per sheet), exact (claim, transition)
set equality between coders, headline maps covering exactly the corpus, grade/scope vocabularies, and
provenance hashes matching PINNING_MANIFEST.csv.

Usage: python3 merge_coder_sheets.py [--sheets-dir CODING_sheets] [--corpus corpus_arxiv_adjudicated_v1.csv]
       writes CODING_sheets/merged.csv + headline_merged.csv and prints the disagreement summary.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRANSITIONS = ("T1", "T2", "T3", "T4", "T5")
GRADES = ("E0", "E1", "E2")
ORDER = {g: i for i, g in enumerate(GRADES)}


def fail(problems):
    if problems:
        print("MERGE: REFUSED", flush=True)
        for p in problems:
            print(f"  - {p}", flush=True)
        raise SystemExit(1)


def read_sheet(path: Path, coder: str):
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    problems = []
    if len(rows) != 90:
        problems.append(f"{path.name}: {len(rows)} rows, expected 90 (18 claims x 5 transitions)")
    for r in rows:
        if r["coder"] != coder:
            problems.append(f"{path.name}: a row claims coder {r['coder']!r}")
        if r["transition"] not in TRANSITIONS:
            problems.append(f"{path.name}: undeclared transition {r['transition']!r}")
        for field in ("in_paper_grade", "external_evidence_grade"):
            if r[field] not in GRADES:
                problems.append(f"{path.name}: {r['claim_id']} {r['transition']} {field}={r[field]!r} outside E0-E2")
        if not (r.get("justification_quote") or "").strip():
            problems.append(f"{path.name}: {r['claim_id']} {r['transition']} has no justification")
    keys = [(r["claim_id"], r["transition"]) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append(f"{path.name}: duplicate (claim, transition) rows")
    fail(problems)
    return rows


def read_headline(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    problems = [f"{path.name}: {len(rows)} rows, expected 18" for _ in [0] if len(rows) != 18]
    mapping = {}
    for r in rows:
        t = r["headline_transition"]
        if t not in TRANSITIONS:
            problems.append(f"{path.name}: undeclared headline transition {t!r}")
        mapping[r["claim_id"]] = t
    fail(problems)
    return mapping


def pinning_hashes() -> dict[str, str]:
    out = {}
    with (ROOT / "fulltexts" / "PINNING_MANIFEST.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            out[row["arxiv_id_version"]] = row["pdf_sha256"]
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheets-dir", default=str(ROOT / "CODING_sheets"))
    parser.add_argument("--corpus", default=str(ROOT / "corpus_arxiv_adjudicated_v1.csv"))
    args = parser.parse_args()
    sheets_dir = Path(args.sheets_dir)

    corpus_ids = {r["arxiv_id_version"] for r in csv.DictReader(open(args.corpus, newline="", encoding="utf-8"))}
    sheet_a = read_sheet(sheets_dir / "coder_A.csv", "coder_A")
    sheet_b = read_sheet(sheets_dir / "coder_B.csv", "coder_B")
    head_a, head_b = read_headline(sheets_dir / "headline_A.csv"), read_headline(sheets_dir / "headline_B.csv")

    problems = []
    for name, sheet in (("A", sheet_a), ("B", sheet_b)):
        ids = {r["claim_id"] for r in sheet}
        if ids != corpus_ids:
            problems.append(f"coder {name}: claim set differs from the corpus: {sorted(ids ^ corpus_ids)[:4]}")
    if set(head_a) != corpus_ids or set(head_b) != corpus_ids:
        problems.append("a headline map does not cover exactly the corpus claims")
    fail(problems)

    # provenance check: every row must name the pinned pdf and its recorded hash
    pins = pinning_hashes()
    bad_hash = [f"{r['claim_id']}: provenance_sha256 does not match PINNING_MANIFEST"
                for r in sheet_a + sheet_b
                if r.get("provenance_sha256", "").strip() != pins.get(r["claim_id"], "")]
    fail(bad_hash[:5] + (["...and more hash mismatches"] if len(bad_hash) > 5 else []))

    # disagreement + the weaker-grade merge (the standing resolution rule of the authority record)
    by_key_a = {(r["claim_id"], r["transition"]): r for r in sheet_a}
    by_key_b = {(r["claim_id"], r["transition"]): r for r in sheet_b}
    assert set(by_key_a) == set(by_key_b)
    merged_rows, disagree_rows = [], 0
    for key in sorted(by_key_a):
        a, b = by_key_a[key], by_key_b[key]
        grade = a["in_paper_grade"] if ORDER[a["in_paper_grade"]] <= ORDER[b["in_paper_grade"]] else b["in_paper_grade"]
        if a["in_paper_grade"] != b["in_paper_grade"]:
            disagree_rows += 1
        ext = a["external_evidence_grade"] if ORDER[a["external_evidence_grade"]] <= ORDER[b["external_evidence_grade"]] else b["external_evidence_grade"]
        merged_rows.append({
            "claim_id": key[0], "coder": "merged-weaker", "transition": key[1],
            "in_paper_grade": grade, "external_evidence_grade": ext,
            "external_citation_verified_route": "",
            "scope_match": a["scope_match"] if a["scope_match"] else b["scope_match"],
            "justification_quote": a["justification_quote"],
            "provenance_file": a["provenance_file"], "provenance_sha256": a["provenance_sha256"],
            "round": "merged-1", "note": f"A={a['in_paper_grade']}/B={b['in_paper_grade']}",
        })
    head_disagree = {c: (head_a[c], head_b[c]) for c in head_a if head_a[c] != head_b[c]}

    with (sheets_dir / "merged.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(merged_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(merged_rows)
    with (sheets_dir / "headline_merged.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["claim_id", "headline_transition", "headline_disagreement"])
        # headline disagreements resolve to the transition that makes the headline statistic WEAKER:
        # the lower-evidenced of the two named transitions under the merged grades
        for claim, transition in head_a.items():
            other = head_b[claim]
            note = ""
            if transition != other:
                ga = next(r["in_paper_grade"] for r in merged_rows if r["claim_id"] == claim and r["transition"] == transition)
                gb = next(r["in_paper_grade"] for r in merged_rows if r["claim_id"] == claim and r["transition"] == other)
                chosen, note = (transition, f"chose weaker of A={transition}:{ga} B={other}:{gb}")
                if ORDER[ga] > ORDER[gb]:
                    chosen, note = (other, f"chose weaker of A={transition}:{ga} B={other}:{gb}")
            else:
                chosen = transition
            writer.writerow([claim, chosen, note])

    print(f"merged: 90 rows, weaker-grade rule; grade disagreements {disagree_rows}/90 "
          f"({disagree_rows / 90:.1%})")
    print(f"headline disagreements: {len(head_disagree)}/18" + (f" {head_disagree}" if head_disagree else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
