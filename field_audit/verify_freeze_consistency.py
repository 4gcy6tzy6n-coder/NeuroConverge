#!/usr/bin/env python3
"""Guard the frozen protocol against drift in the draw script's constants.

The frozen selection rule (AUDIT_PREREGISTRATION_v1_FROZEN.md section 3) and the constants embedded in
draw_corpus.py must agree. If either is edited without a dated owner-visible amendment, this check fails by
name. Kept as a permanent runnable check because the alternative - a protocol document and an instrument that
silently disagree - is the failure mode every lane in this workspace has been bitten by.

Run: python3 verify_freeze_consistency.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "AUDIT_PREREGISTRATION_v1_FROZEN.md"

import draw_corpus as D

# (parameter name, the script attribute read at check time, the frozen protocol value). The attribute is
# resolved by name inside check_parameters - a list built at import time would snapshot the value and be
# blind to exactly the tampering this guard exists for, which its own selftest demonstrated.
EXPECTED = [
    ("window", "WINDOW", ("2015-01-01", "2026-09-30")),
    ("tier3 citation floor", "TIER3_CITATION_FLOOR", 100),
    ("tier3 decile", "TIER3_DECILE", 0.10),
    ("target size", "TARGET_SIZE", 20),
    ("accept range", "ACCEPT_RANGE", (15, 25)),
    ("family cap", "FAMILY_CAP", 3),
    ("venue cap", "VENUE_CAP", 5),
]


def protocol_text() -> str:
    return PROTOCOL.read_text(encoding="utf-8")


def check_parameters(text: str) -> list[str]:
    findings = []
    for name, attribute, expected in EXPECTED:
        actual = getattr(D, attribute)
        if actual != expected:
            findings.append(f"{name}: script has {actual!r}, protocol freezes {expected!r}")
    if f"{D.WINDOW[0]} to {D.WINDOW[1]}" not in text:
        findings.append(f"window: protocol text does not state '{D.WINDOW[0]} to {D.WINDOW[1]}'")
    if "100 citations at draw date" not in text:
        findings.append("citation floor: protocol wording changed")
    if "top-cited 10 percent" not in text:
        findings.append("decile: protocol wording changed")
    if "at most 3 claims per mechanism family" not in text or "at most 5 per venue" not in text:
        findings.append("caps: protocol wording changed")
    return findings


def check_wiring() -> list[str]:
    findings = []
    names = {
        "AUDIT_PREREGISTRATION_v1_FROZEN.md", "README.md", "draw_corpus.py", "AUDIT_REGISTER.csv",
        "CODING_SHEET_TEMPLATE.csv", "REPORTING_CHECKLIST_DRAFT.md", "DRAW_ATTEMPT_LOG.md",
    }
    present = {p.name for p in ROOT.iterdir() if p.is_file()}
    missing = names - present
    if missing:
        findings.append(f"workstream files missing: {sorted(missing)}")
    for referenced in ("../DECISION_20261018_ROUTE_A_SIGNED.md", "../PROPOSAL_20261018_FIELD_AUDIT_ROUTE_A.md"):
        if not (ROOT / referenced).is_file():
            findings.append(f"referenced authority document missing: {referenced}")
    return findings


def check_csv_headers() -> list[str]:
    findings = []
    for name, required in (
        # the register keys entries (candidates and claims) by entry_id with a role column; claim_id is the
        # coding sheet's key, joined to the register by candidate/claim correspondence at draw review
        ("AUDIT_REGISTER.csv",
         ("entry_id", "role", "openalex_id", "fulltext_sha256", "status", "status_reason", "date")),
        ("CODING_SHEET_TEMPLATE.csv",
         ("claim_id", "coder", "transition", "in_paper_grade", "external_evidence_grade",
          "scope_match", "justification_quote", "provenance_sha256", "round")),
    ):
        header = (ROOT / name).read_text(encoding="utf-8").splitlines()[0]
        missing = [column for column in required if column not in header]
        if missing:
            findings.append(f"{name}: header lost required columns {missing}")
    return findings


def selftest() -> None:
    """The comparison must be able to see its own error class: a tampered constant is reported by name."""
    original = D.TARGET_SIZE
    try:
        D.TARGET_SIZE = 25  # a silent edit of the kind this guard exists for
        findings = check_parameters(protocol_text())
        assert any("target size" in f for f in findings), "the guard is blind to a tampered constant"
    finally:
        D.TARGET_SIZE = original
    assert check_parameters(protocol_text()) == []


def main() -> int:
    selftest()
    text = protocol_text()
    findings = check_parameters(text) + check_wiring() + check_csv_headers()
    if findings:
        print("FREEZE CONSISTENCY: FAIL")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print("FREEZE CONSISTENCY: PASS")
    print("  parameters: window/floor/decile/target/accept-range/caps agree with the frozen protocol")
    print("  wiring: all seven workstream files and both authority documents present")
    print("  csv: register and coding-sheet headers carry their required columns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
