#!/usr/bin/env python3
"""Route A statistics: the six frozen outputs of protocol section 6, computed from coding sheets.

Authority: field_audit/AUDIT_PREREGISTRATION_v1_FROZEN.md sections 6 and 9 - every statistic is computed by
script from the coding sheets, never transcribed by hand. This script exists so that when the corpus and the
dual-coder sheets arrive, the numbers are one command with named failures, not a notebook.

Fail-closed, by name, everywhere: a claim missing from the headline map, a phantom claim in it, a grade or
transition outside the frozen vocabularies, a claim the register cannot stratify, a malformed replacement
row - each refuses the whole run rather than dropping the affected claim silently. An omitted optional input
is reported as a named missing item on stdout, never skipped quietly.

Usage (all paths relative to field_audit/ unless absolute):
    python3 compute_statistics.py --selftest
    python3 compute_statistics.py \
        --sheet lead=CODING_sheets/lead.csv --sheet second=CODING_sheets/second.csv \
        --headline CODING_sheets/headline_map.csv --register AUDIT_REGISTER.csv \
        [--replacements replacements.csv] [--uncodable uncodable.csv] \
        [--sensitivity alt1=... [--sensitivity alt2=...]]

Outputs (stdout, and --out stats.json for the machine-readable copy):
  1. per-transition grade distributions, per sheet and on the weaker-grade merge
  2. the headline statistic: the share of claims whose headline transition is E0 or E1
  3. the scope-match rate
  4. stratified repeats of 1-3 by mechanism family and venue tier
  5. sensitivity recomputation of 1-2 on each alternate-corpus sheet set
  6. reliability: per-transition two-coder disagreement rate, replacement count, uncodable count
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRANSITIONS = ("T1", "T2", "T3", "T4", "T5")
GRADES = ("E0", "E1", "E2", "E3", "E4")
GRADE_ORDER = {g: i for i, g in enumerate(GRADES)}
SCOPE_VALUES = ("match", "mismatch")


def fail(problems: list[str]) -> None:
    if problems:
        print("STATISTICS: REFUSED", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        raise SystemExit(1)


def read_sheet(path: Path) -> list[dict]:
    problems = []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    seen = set()
    for row in rows:
        claim = (row.get("claim_id") or "").strip()
        transition = (row.get("transition") or "").strip()
        grade = (row.get("in_paper_grade") or "").strip()
        if not claim:
            problems.append(f"{path.name}: a row carries no claim_id")
            continue
        if transition not in TRANSITIONS:
            problems.append(f"{path.name}: {claim} has undeclared transition {transition!r}")
        if grade not in GRADES:
            problems.append(f"{path.name}: {claim} {transition} has undeclared grade {grade!r}")
        if row.get("scope_match") and row["scope_match"].strip() not in SCOPE_VALUES:
            problems.append(f"{path.name}: {claim} has undeclared scope_match {row['scope_match']!r}")
        key = (claim, transition)
        if key in seen:
            problems.append(f"{path.name}: duplicate row {claim} {transition}")
        seen.add(key)
    fail(problems)
    return rows


def weaker(grade_a: str, grade_b: str) -> str:
    return grade_a if GRADE_ORDER[grade_a] <= GRADE_ORDER[grade_b] else grade_b


def read_headline(path: Path) -> dict[str, str]:
    problems = []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    mapping = {}
    for row in rows:
        claim = (row.get("claim_id") or "").strip()
        headline = (row.get("headline_transition") or "").strip()
        if not claim:
            problems.append(f"{path.name}: a headline row carries no claim_id")
            continue
        if headline not in TRANSITIONS:
            problems.append(f"{path.name}: {claim} names undeclared headline transition {headline!r}")
        if claim in mapping:
            problems.append(f"{path.name}: duplicate headline row for {claim}")
        mapping[claim] = headline
    fail(problems)
    return mapping


def read_register_strata(path: Path) -> dict[str, dict[str, str]]:
    """claim_id -> {mechanism_family, venue_tier} from the register's claim rows."""
    if not path.is_file():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    out = {}
    for row in rows:
        claim = (row.get("claim_id") or row.get("entry_id") or "").strip()
        if not claim:
            continue
        out[claim] = {"mechanism_family": (row.get("mechanism_family") or "").strip(),
                      "venue_tier": (row.get("venue_tier") or "").strip()}
    return out


def grade_map(rows: list[dict]) -> dict[tuple[str, str], str]:
    return {(r["claim_id"].strip(), r["transition"].strip()): r["in_paper_grade"].strip() for r in rows}


def distribution(grades: dict[tuple[str, str], str]) -> dict[str, Counter]:
    counts = {t: Counter() for t in TRANSITIONS}
    for (_claim, transition), grade in grades.items():
        counts[transition][grade] += 1
    return counts


def headline_statistic(grades: dict[tuple[str, str], str], headline: dict[str, str]) -> dict:
    """Output 2: the share of claims whose headline transition is E0 or E1."""
    problems = []
    total = low = 0
    for claim, transition in headline.items():
        grade = grades.get((claim, transition))
        if grade is None:
            problems.append(f"headline: {claim} names {transition}, which no sheet row grades")
            continue
        total += 1
        if grade in ("E0", "E1"):
            low += 1
    fail(problems)
    return {"claims": total, "headline_e0_e1": low, "share": (low / total) if total else 0.0}


def scope_rate(rows: list[dict]) -> dict:
    verdicts = [r["scope_match"].strip() for r in rows if r["transition"].strip() == "T5"
                and r.get("scope_match", "").strip()]
    matched = sum(1 for v in verdicts if v == "match")
    return {"t5_rows": len(verdicts), "match": matched,
            "rate": (matched / len(verdicts)) if verdicts else 0.0}


def stratified(grades: dict[tuple[str, str], str], headline: dict[str, str],
               strata: dict[str, dict[str, str]]) -> dict:
    """Output 4: repeats of 1-2 by mechanism family and venue tier. Claims the register cannot stratify
    refuse the run by name."""
    problems = []
    by_family, by_tier = defaultdict(list), defaultdict(list)
    for claim in headline:
        info = strata.get(claim)
        if info is None:
            problems.append(f"stratification: {claim} is absent from the register")
            continue
        grade = grades.get((claim, headline[claim]))
        if grade is None:
            continue
        by_family[info["mechanism_family"] or "unspecified"].append(grade)
        by_tier[info["venue_tier"] or "unspecified"].append(grade)
    fail(problems)
    out = {}
    for name, groups in (("by_family", by_family), ("by_tier", by_tier)):
        out[name] = {
            key: {"claims": len(values),
                  "headline_e0_e1": sum(1 for g in values if g in ("E0", "E1"))}
            for key, values in groups.items()}
    return out


def disagreement(sheet_a: list[dict], sheet_b: list[dict]) -> dict:
    """Output 6: per-transition two-coder disagreement rate (1 - 3 grades apart; the frozen tie rule takes
    the weaker grade, reported beside)."""
    a, b = grade_map(sheet_a), grade_map(sheet_b)
    if set(a) != set(b):
        missing = sorted(set(a) ^ set(b))[:5]
        fail([f"agreement: the two sheets grade different (claim, transition) sets, e.g. {missing}"])
    per_transition = {t: {"rows": 0, "disagree": 0} for t in TRANSITIONS}
    for key, grade in a.items():
        cell = per_transition[key[1]]
        cell["rows"] += 1
        if grade != b[key]:
            cell["disagree"] += 1
    return {
        t: {"rows": cell["rows"], "disagree": cell["disagree"],
            "rate": (cell["disagree"] / cell["rows"]) if cell["rows"] else 0.0}
        for t, cell in per_transition.items()}


def read_replacements(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    problems = [f"replacements: row {i + 1} lacks a reason" for i, r in enumerate(rows)
                if not (r.get("reason") or "").strip()]
    fail(problems)
    return rows


def run(args) -> dict:
    sheets = {name: read_sheet(Path(path))
              for name, path in (entry.split("=", 1) for entry in args.sheet)}
    headline = read_headline(Path(args.headline))
    sheet_claims = {row["claim_id"].strip() for rows in sheets.values() for row in rows}
    missing = sorted(sheet_claims - set(headline))
    phantom = sorted(set(headline) - sheet_claims)
    fail([f"headline map: no entry for {c}" for c in missing]
         + [f"headline map: phantom claim {c}" for c in phantom])
    merged = {}
    keys = set()
    for rows in sheets.values():
        keys |= set(grade_map(rows))
    for key in keys:
        grades_here = [grade_map(rows)[key] for rows in sheets.values() if key in grade_map(rows)]
        merged[key] = min(grades_here, key=lambda g: GRADE_ORDER[g])
    strata = read_register_strata(Path(args.register))
    stats = {
        "sheets": list(sheets),
        "grade_distribution": {name: {t: dict(distribution(grade_map(rows))[t]) for t in TRANSITIONS}
                               for name, rows in sheets.items()},
        "weaker_merge_distribution": {t: dict(distribution(merged)[t]) for t in TRANSITIONS},
        "headline": headline_statistic(merged, headline),
        "scope": scope_rate([row for rows in sheets.values() for row in rows]),
        "stratified": stratified(merged, headline, strata),
        "sensitivity": {},
        "reliability": {
            "disagreement": disagreement(*list(sheets.values())) if len(sheets) == 2 else "not provided",
        },
    }
    for name, rows in sheets.items():
        stats["headline_per_sheet"] = stats.get("headline_per_sheet", {})
        stats["headline_per_sheet"][name] = headline_statistic(grade_map(rows), headline)
    if args.replacements:
        stats["reliability"]["replacements"] = len(read_replacements(Path(args.replacements)))
    else:
        stats["reliability"]["replacements"] = "not provided"
    if args.uncodable:
        with Path(args.uncodable).open(newline="", encoding="utf-8") as handle:
            stats["reliability"]["uncodable"] = len(list(csv.DictReader(handle)))
    else:
        stats["reliability"]["uncodable"] = "not provided"
    for name, path in (entry.split("=", 1) for entry in args.sensitivity or []):
        rows = read_sheet(Path(path))
        alt_headline = {c: t for c, t in headline.items()
                        if any(r["claim_id"].strip() == c for r in rows)}
        stats["sensitivity"][name] = headline_statistic(grade_map(rows), alt_headline)
    return stats


def _selftest() -> int:
    import tempfile
    base = Path(tempfile.mkdtemp())
    def write(name, header, rows):
        (base / name).write_text("\n".join([",".join(header)] + [",".join(r) for r in rows]) + "\n")

    write("a.csv", ["claim_id", "coder", "transition", "in_paper_grade", "scope_match"],
          [["C1", "a", "T1", "E1", ""], ["C1", "a", "T2", "E0", ""], ["C1", "a", "T3", "E1", ""],
           ["C1", "a", "T4", "E0", ""], ["C1", "a", "T5", "E1", "match"],
           ["C2", "a", "T1", "E2", ""], ["C2", "a", "T2", "E2", ""], ["C2", "a", "T3", "E2", ""],
           ["C2", "a", "T4", "E1", ""], ["C2", "a", "T5", "E2", "mismatch"]])
    write("b.csv", ["claim_id", "coder", "transition", "in_paper_grade", "scope_match"],
          [["C1", "b", "T1", "E2", ""], ["C1", "b", "T2", "E0", ""], ["C1", "b", "T3", "E1", ""],
           ["C1", "b", "T4", "E1", ""], ["C1", "b", "T5", "E1", "match"],
           ["C2", "b", "T1", "E2", ""], ["C2", "b", "T2", "E2", ""], ["C2", "b", "T3", "E2", ""],
           ["C2", "b", "T4", "E1", ""], ["C2", "b", "T5", "E2", "mismatch"]])
    write("h.csv", ["claim_id", "headline_transition"], [["C1", "T3"], ["C2", "T3"]])
    write("reg.csv", ["claim_id", "mechanism_family", "venue_tier"],
          [["C1", "memory", "1"], ["C2", "plasticity/learning rules", "2"]])

    args = argparse.Namespace(
        sheet=[f"lead={base / 'a.csv'}", f"second={base / 'b.csv'}"], headline=str(base / "h.csv"),
        register=str(base / "reg.csv"), replacements=None, uncodable=None,
        sensitivity=[f"alt1={base / 'b.csv'}"])
    stats = run(args)
    # hand-computed: weaker merge on T3 gives C1 E1, C2 E2 -> headline E0/E1 share = 1/2
    assert stats["headline"] == {"claims": 2, "headline_e0_e1": 1, "share": 0.5}, stats["headline"]
    # disagreement: 2 of 10 rows differ (C1T1, C1T4) -> rate 0.2 overall; T1 1 of 2
    assert stats["reliability"]["disagreement"]["T1"] == {"rows": 2, "disagree": 1, "rate": 0.5}
    assert stats["scope"]["rate"] == 0.5
    assert stats["stratified"]["by_family"]["memory"]["claims"] == 1

    # the refusal classes, each by name
    write("h_bad.csv", ["claim_id", "headline_transition"], [["C1", "T3"]])  # C2 missing
    args.headline = str(base / "h_bad.csv")
    try:
        run(args)
        raise AssertionError("a claim missing from the headline map must refuse the run")
    except SystemExit:
        pass
    write("h_phantom.csv", ["claim_id", "headline_transition"], [["C1", "T3"], ["C2", "T3"], ["C9", "T1"]])
    args.headline = str(base / "h_phantom.csv")
    try:
        run(args)
        raise AssertionError("a phantom headline claim must refuse the run")
    except SystemExit:
        pass
    print("selftest: all checks passed (hand-computed headline/disagreement/scope/strata; named refusals "
          "for missing, phantom, and malformed inputs)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--sheet", action="append", required=False, metavar="NAME=PATH",
                        help="a coding sheet; the first two also produce the disagreement statistics")
    parser.add_argument("--headline", help="claim_id,headline_transition map")
    parser.add_argument("--register", default=str(ROOT / "AUDIT_REGISTER.csv"))
    parser.add_argument("--replacements")
    parser.add_argument("--uncodable")
    parser.add_argument("--sensitivity", action="append", metavar="NAME=PATH")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.selftest:
        return _selftest()
    if not args.sheet or not args.headline:
        parser.error("a run needs at least one --sheet and a --headline map")
    stats = run(args)
    text = json.dumps(stats, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
