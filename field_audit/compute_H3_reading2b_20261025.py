#!/usr/bin/env python3
"""O-5 reading 2b generator (dated supplement, 2026-10-25).

The frozen H3 instrument `compute_H3_full_20261025.py` emits readings 1 and 3 only. The
preregistered disagreement-handled reading (reading 2b: per covered cell, the weaker of coder H's
grade and the AI weaker-merge grade) was appended to `CODING_sheets_human/H3_READING_20261025.json`
in commit 5dc70b0 without a generator, so a re-run of the frozen script silently deleted it
(O-6 finding F1). This script restores the missing link without editing the frozen instrument:

    python3 field_audit/compute_H3_full_20261025.py
    python3 field_audit/compute_H3_reading2b_20261025.py

The second command recomputes reading 2b from the raw sheets and writes it into the committed H3
JSON. The two commands together reproduce the committed file byte-for-byte; no number changes.

Selftest (frozen values, run before relying on output):
    python3 field_audit/compute_H3_reading2b_20261025.py --selftest
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E_ORDER = {"E0": 0, "E1": 1, "E2": 2}
TRANS = ["T1", "T2", "T3", "T4", "T5"]
# Frozen reading-2b values (H3_READING_20261025.json, section 7 of O5_H3_RESULTS_20261025.md).
EXPECTED = {
    "primary": {"headline_e2plus": 4, "n": 16, "T2_E2": "1/16", "T3_E2": "4/16"},
    "validation": {"headline_e2plus": 19, "n": 41, "T2_E2": "2/42", "T3_E2": "19/42"},
}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def index_rows(rows: list[dict[str, str]], coder: str) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["claim_id"], row["transition"]): row for row in rows if row["coder"] == coder}


def weaker(a: str, b: str) -> str:
    """Frozen weaker-grade rule: E0 < E1 < E2."""
    return a if E_ORDER[a] <= E_ORDER[b] else b


def wilson(k: int, n: int, z: float = 1.959963985) -> list[float]:
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [round(100 * max(0.0, centre - half), 1), round(100 * min(1.0, centre + half), 1)]


def build_inputs() -> tuple[
    dict[tuple[str, str], str], dict[tuple[str, str], dict[str, str]],
    list[str], list[str], dict[str, str]
]:
    """Return (AI merged grades, H sheet, primary ids, validation ids, H headline map)."""
    primary_map = {
        row["claim_id"]: row["arxiv_id_version"]
        for row in load_rows(ROOT / "corpus_final_16.csv")
    }
    a_primary = index_rows(load_rows(ROOT / "CODING_sheets_v2/coder_A_E.csv"), "A")
    b_primary = index_rows(load_rows(ROOT / "CODING_sheets_v2/coder_B_E.csv"), "B")
    ai_merged: dict[tuple[str, str], str] = {}
    for (claim, transition), row_a in a_primary.items():
        if claim not in primary_map:
            raise RuntimeError(f"primary claim {claim} is absent from corpus_final_16.csv")
        row_b = b_primary[(claim, transition)]
        ai_merged[(primary_map[claim], transition)] = weaker(
            row_a["in_paper_grade"], row_b["in_paper_grade"]
        )

    a_validation = index_rows(load_rows(ROOT / "CODING_sheets_validation/coder_A.csv"), "A")
    b_validation = index_rows(load_rows(ROOT / "CODING_sheets_validation/coder_B.csv"), "B")
    for key, row_a in a_validation.items():
        row_b = b_validation[key]
        ai_merged[key] = weaker(row_a["in_paper_grade"], row_b["in_paper_grade"])

    h_sheet = index_rows(load_rows(ROOT / "CODING_sheets_human/coder_H.csv"), "H")
    primary_ids = sorted({row["arxiv_id_version"] for row in load_rows(ROOT / "corpus_final_16.csv")})
    validation_ids = sorted(
        {row["arxiv_id_version"] for row in load_rows(ROOT / "corpus_validation_v2_adjudicated.csv")}
    )
    h_headline = {
        row["claim_id"]: row["headline_transition"]
        for row in load_rows(ROOT / "CODING_sheets_human/headline_H.csv")
    }
    return ai_merged, h_sheet, primary_ids, validation_ids, h_headline


def distribution(
    ids: list[str], transitions: list[str],
    h_sheet: dict[tuple[str, str], dict[str, str]], ai_merged: dict[tuple[str, str], str]
) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for transition in transitions:
        counter: Counter[str] = Counter()
        for claim in ids:
            key = (claim, transition)
            if key in h_sheet and key in ai_merged:
                counter[weaker(h_sheet[key]["in_paper_grade"], ai_merged[key])] += 1
        out[transition] = dict(counter)
    return out


def headline_stats(
    ids: list[str], h_sheet: dict[tuple[str, str], dict[str, str]],
    ai_merged: dict[tuple[str, str], str], h_headline: dict[str, str]
) -> dict[str, object]:
    grades: dict[str, str] = {}
    skipped: list[list[str]] = []
    for claim in ids:
        transition = h_headline.get(claim)
        key = (claim, transition)
        if transition is not None and key in h_sheet and key in ai_merged:
            grades[claim] = weaker(h_sheet[key]["in_paper_grade"], ai_merged[key])
        else:
            skipped.append([claim, transition])
    e2 = sum(1 for grade in grades.values() if grade == "E2")
    n = len(grades)
    return {
        "headline_e2plus": e2,
        "n": n,
        "skipped": skipped,
        "share_pct": round(100 * e2 / n, 1),
        "wilson95": wilson(e2, n),
    }


def asymmetry(
    ids: list[str],
    h_sheet: dict[tuple[str, str], dict[str, str]], ai_merged: dict[tuple[str, str], str]
) -> dict[str, str]:
    def e2_count(transition: str) -> int:
        total = 0
        for claim in ids:
            key = (claim, transition)
            if key in h_sheet and key in ai_merged:
                total += weaker(h_sheet[key]["in_paper_grade"], ai_merged[key]) == "E2"
        return total

    t2, t3 = e2_count("T2"), e2_count("T3")
    direction = "T3>T2" if t3 > t2 else ("T2>T3" if t2 > t3 else "tie")
    return {"T2_E2": f"{t2}/{len(ids)}", "T3_E2": f"{t3}/{len(ids)}", "direction": direction}


def compute_reading2b() -> dict[str, object]:
    ai_merged, h_sheet, primary_ids, validation_ids, h_headline = build_inputs()
    return {
        "primary": {
            "dist": distribution(primary_ids, TRANS, h_sheet, ai_merged),
            **headline_stats(primary_ids, h_sheet, ai_merged, h_headline),
        },
        "validation": {
            "dist": distribution(validation_ids, ["T2", "T3", "T5"], h_sheet, ai_merged),
            **headline_stats(validation_ids, h_sheet, ai_merged, h_headline),
        },
        "asymmetry": {
            "primary": asymmetry(primary_ids, h_sheet, ai_merged),
            "validation": asymmetry(validation_ids, h_sheet, ai_merged),
        },
    }


def selftest() -> None:
    reading = compute_reading2b()
    checks: list[tuple[str, bool]] = []
    for corpus, expected in EXPECTED.items():
        block = reading[corpus]
        checks.append((f"{corpus} headline E2+ {expected['headline_e2plus']}/{expected['n']}",
                       block["headline_e2plus"] == expected["headline_e2plus"] and block["n"] == expected["n"]))
        asym = reading["asymmetry"][corpus]
        checks.append((f"{corpus} T2 {expected['T2_E2']}", asym["T2_E2"] == expected["T2_E2"]))
        checks.append((f"{corpus} T3 {expected['T3_E2']}", asym["T3_E2"] == expected["T3_E2"]))
    checks.append(("weaker rule E1 vs E2 -> E1", weaker("E1", "E2") == "E1"))
    checks.append(("weaker rule E0 vs E1 -> E0", weaker("E0", "E1") == "E0"))
    failed = [name for name, passed in checks if not passed]
    if failed:
        print("SELFTEST FAIL:", failed)
        raise SystemExit(1)
    print(f"SELFTEST PASS ({len(checks)} assertions)")


def main() -> int:
    target = ROOT / "CODING_sheets_human/H3_READING_20261025.json"
    if not target.exists():
        print(f"REFUSED: {target.name} is absent; run compute_H3_full_20261025.py first.")
        return 1
    base = json.loads(target.read_text(encoding="utf-8"))
    required = {"round", "coder", "reading1_raw_H", "reading3_agreement",
                "grade_transition_matrix", "disputed_cells",
                "headline_agreement_with_AI_merge", "ai_merge_reference"}
    missing = sorted(required - set(base))
    if missing:
        print(f"REFUSED: {target.name} is not the compute_H3_full output (missing {missing}).")
        return 1
    base["reading2b_weaker_merge_H_vs_AI"] = compute_reading2b()
    target.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {target.relative_to(ROOT)}: reading2b restored")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        raise SystemExit(0)
    raise SystemExit(main())
