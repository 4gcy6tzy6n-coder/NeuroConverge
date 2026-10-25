#!/usr/bin/env python3
"""O-5 headline-map agreement correction (dated supplement, 2026-10-25; O-6 findings F3/F4).

`compute_H3_full_20261025.py` re-derives the primary headline map with the *validation* tie rule
(prefer T3 when the coders' candidate transitions tie on the merged grade). The committed primary
map is `CODING_sheets_v2/headline_merged.csv`, produced by `merge_coder_sheets_v2.py` under the
primary merge rule (coder A's transition on a tie): C077 / 1811.09699v1 -> T2. Coder H's own
headline for that claim is T2, so the headline-map agreement against the committed map is 52/58,
not the 51/58 printed by the frozen H3 script.

This script makes the correction reproducible and records both variants:
    canonical (committed maps):  primary 16/16 + validation 36/42 = 52/58
    H3-script variant (re-derived primary map, validation tie rule): 51/58
No other number changes; the per-cell agreement and disputed-cell audit do not use headline maps.

Usage: python3 field_audit/compute_H3_headline_agreement_20261025.py [--selftest]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E_ORDER = {"E0": 0, "E1": 1, "E2": 2}
EXPECTED = {"canonical": {"primary": "16/16", "validation": "36/42", "total": "52/58"},
            "h3_variant": {"primary": "15/16", "validation": "36/42", "total": "51/58"}}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def headline_map(path: Path) -> dict[str, str]:
    return {row["claim_id"]: row["headline_transition"] for row in load_rows(path)}


def merged_grades(sheet_a: list[dict[str, str]], sheet_b: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    by_a = {(row["claim_id"], row["transition"]): row["in_paper_grade"] for row in sheet_a}
    by_b = {(row["claim_id"], row["transition"]): row["in_paper_grade"] for row in sheet_b}
    return {key: (by_a[key] if E_ORDER[by_a[key]] <= E_ORDER[by_b[key]] else by_b[key]) for key in by_a}


def build_maps() -> tuple[dict[str, str], dict[str, str], list[dict[str, str]]]:
    """Return (canonical map, H3-variant primary map, divergence detail)."""
    primary_rows = load_rows(ROOT / "corpus_final_16.csv")
    primary_ids = [row["claim_id"] for row in primary_rows]
    primary_arxiv = {row["claim_id"]: row["arxiv_id_version"] for row in primary_rows}
    validation_ids = [row["arxiv_id_version"] for row in load_rows(ROOT / "corpus_validation_v2_adjudicated.csv")]

    primary_a = load_rows(ROOT / "CODING_sheets_v2/coder_A_E.csv")
    primary_b = load_rows(ROOT / "CODING_sheets_v2/coder_B_E.csv")
    primary_merged = merged_grades(primary_a, primary_b)
    headline_a = headline_map(ROOT / "CODING_sheets_v2/headline_A.csv")
    headline_b = headline_map(ROOT / "CODING_sheets_v2/headline_B.csv")
    committed_primary = headline_map(ROOT / "CODING_sheets_v2/headline_merged.csv")

    def h3_primary_choice(claim: str) -> str:
        ta, tb = headline_a[claim], headline_b[claim]
        if ta == tb:
            return ta
        ga, gb = primary_merged[(claim, ta)], primary_merged[(claim, tb)]
        if E_ORDER[ga] < E_ORDER[gb]:
            return ta
        if E_ORDER[gb] < E_ORDER[ga]:
            return tb
        return "T3" if "T3" in (ta, tb) else ta

    divergence = [
        {"claim": claim, "committed": committed_primary[claim], "h3_derived": h3_primary_choice(claim)}
        for claim in primary_ids if committed_primary[claim] != h3_primary_choice(claim)
    ]

    # Validation map: the committed statistics JSON was produced with the validation tie rule
    # (prefer T3); this script re-derives it from the raw sheets and checks the recorded counts.
    validation_merged = merged_grades(
        load_rows(ROOT / "CODING_sheets_validation/coder_A.csv"),
        load_rows(ROOT / "CODING_sheets_validation/coder_B.csv"),
    )
    validation_a = headline_map(ROOT / "CODING_sheets_validation/headline_A.csv")
    validation_b = headline_map(ROOT / "CODING_sheets_validation/headline_B.csv")
    validation_map: dict[str, str] = {}
    for claim in validation_ids:
        ta, tb = validation_a[claim], validation_b[claim]
        if ta == tb:
            validation_map[claim] = ta
            continue
        ga, gb = validation_merged[(claim, ta)], validation_merged[(claim, tb)]
        if E_ORDER[ga] < E_ORDER[gb]:
            validation_map[claim] = ta
        elif E_ORDER[gb] < E_ORDER[ga]:
            validation_map[claim] = tb
        else:
            validation_map[claim] = "T3" if "T3" in (ta, tb) else ta

    canonical_primary = {primary_arxiv[claim]: committed_primary[claim] for claim in primary_ids}
    variant_primary = {primary_arxiv[claim]: h3_primary_choice(claim) for claim in primary_ids}
    canonical = {**canonical_primary, **validation_map}
    variant = {**variant_primary, **validation_map}
    return canonical, variant, divergence


def agreement(expected: dict[str, str], h_map: dict[str, str], primary_ids: list[str],
              validation_ids: list[str]) -> dict[str, object]:
    def count(ids: list[str]) -> tuple[int, int, list[str]]:
        misses = [claim for claim in ids if h_map.get(claim) != expected.get(claim)]
        return len(ids) - len(misses), len(ids), misses

    p_ok, p_n, p_miss = count(primary_ids)
    v_ok, v_n, v_miss = count(validation_ids)
    return {
        "primary": f"{p_ok}/{p_n}", "validation": f"{v_ok}/{v_n}",
        "total": f"{p_ok + v_ok}/{p_n + v_n}",
        "primary_misses": p_miss, "validation_misses": v_miss,
    }


def compute() -> dict[str, object]:
    canonical, variant, divergence = build_maps()
    h_map = headline_map(ROOT / "CODING_sheets_human/headline_H.csv")
    primary_ids = [row["arxiv_id_version"]
                   for row in load_rows(ROOT / "corpus_final_16.csv")]
    validation_ids = [row["arxiv_id_version"]
                      for row in load_rows(ROOT / "corpus_validation_v2_adjudicated.csv")]
    return {
        "canonical_maps": agreement(canonical, h_map, primary_ids, validation_ids),
        "h3_script_variant": agreement(variant, h_map, primary_ids, validation_ids),
        "primary_map_divergence": divergence,
        "canonical_primary_source": "CODING_sheets_v2/headline_merged.csv",
        "note": "Canonical = committed primary map + committed-validation-rule validation map. "
                "The H3-script variant re-derives the primary map with the validation tie rule; "
                "C077 / 1811.09699v1 is the only divergence. No number outside this agreement count changes.",
    }


def selftest() -> None:
    result = compute()
    checks = [
        ("canonical primary 16/16", result["canonical_maps"]["primary"] == EXPECTED["canonical"]["primary"]),
        ("canonical validation 36/42", result["canonical_maps"]["validation"] == EXPECTED["canonical"]["validation"]),
        ("canonical total 52/58", result["canonical_maps"]["total"] == EXPECTED["canonical"]["total"]),
        ("variant total 51/58", result["h3_script_variant"]["total"] == EXPECTED["h3_variant"]["total"]),
        ("single divergence C077", [d["claim"] for d in result["primary_map_divergence"]] == ["C077"]),
    ]
    failed = [name for name, passed in checks if not passed]
    if failed:
        print("SELFTEST FAIL:", failed)
        raise SystemExit(1)
    print(f"SELFTEST PASS ({len(checks)} assertions)")


def main() -> int:
    result = compute()
    out = ROOT / "CODING_sheets_human/H3_HEADLINE_AGREEMENT_CORRECTION_20261025.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print("->", out.name)
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        raise SystemExit(0)
    raise SystemExit(main())
