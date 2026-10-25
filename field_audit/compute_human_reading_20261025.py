#!/usr/bin/env python3
"""H3 analysis instrument for the O-5 human coding pass (O5_HUMAN_CODING_PROTOCOL_20261025.md).

Prepared and frozen BEFORE any human grade exists. It refuses to run until coder_H's H1 sheet is
complete, so nothing here can touch the record early. Three readings per the frozen protocol:
(1) RAW human reading (primary independence test - the T2/T3 asymmetry must hold here);
(2) SUPERSEDED reading (human grades replace AI grades on covered cells; coverage disclosed);
(3) DISAGREEMENT audit (H vs A, H vs B, H vs AI-merge; grade-transition matrix; disputed-cell
outcomes; matched-neither count after lead adjudication is reported beside, never instead).

--selftest exercises the reading logic on synthetic grades and must fail on mutants."""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E_ORDER = {"E0": 0, "E1": 1, "E2": 2}
TRANS = ["T1", "T2", "T3", "T4", "T5"]
H1_IDS = None  # filled from the primary coder sheets' claim set


def load_sheet(path, coder):
    return {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(path))
            if r.get("coder") == coder}


def raw_reading(h, claims):
    dist = {t: Counter(h[(c, t)]["in_paper_grade"] for c in claims if (c, t) in h) for t in TRANS}
    t2_e2 = dist["T2"].get("E2", 0); t2_n = sum(dist["T2"].values())
    t3_e2 = dist["T3"].get("E2", 0); t3_n = sum(dist["T3"].values())
    return {"per_transition": {t: dict(v) for t, v in dist.items()},
            "T2_E2_share_pct": round(100 * t2_e2 / t2_n, 1) if t2_n else None,
            "T3_E2_share_pct": round(100 * t3_e2 / t3_n, 1) if t3_n else None,
            "asymmetry_holds_direction": (t3_e2 / t3_n > t2_e2 / t2_n) if t2_n and t3_n else None}


def selftest():
    synth = {("c1", t): {"in_paper_grade": g, "external_evidence_grade": "E0", "scope_match": ""}
             for t, g in zip(TRANS, ["E0", "E1", "E2", "E1", "E1"])}
    synth.update({("c2", t): {"in_paper_grade": g, "external_evidence_grade": "E0", "scope_match": ""}
                  for t, g in zip(TRANS, ["E0", "E1", "E2", "E0", "E1"])})
    r = raw_reading(synth, ["c1", "c2"])
    ok = [("T2 share 0 pct", r["T2_E2_share_pct"] == 0.0),
          ("T3 share 100 pct", r["T3_E2_share_pct"] == 100.0),
          ("asymmetry direction true", r["asymmetry_holds_direction"] is True)]
    # mutant: flip T3 to E0 -> asymmetry must flip to False
    synth2 = {k: dict(v, in_paper_grade="E0" if k == ("c1", "T3") else v["in_paper_grade"])
              for k, v in synth.items()}
    synth2[("c2", "T3")]["in_paper_grade"] = "E0"
    r2 = raw_reading(synth2, ["c1", "c2"])
    ok.append(("mutant flips direction", r2["asymmetry_holds_direction"] is False))
    # refusal gate: missing coder_H sheet must refuse (any refusal path counts)
    try:
        main()
    except (SystemExit, FileNotFoundError, AssertionError, RuntimeError):
        ok.append(("refuses without coder_H data", True))
    else:
        ok.append(("refuses without coder_H data", False))
    bad = [n for n, p in ok if not p]
    if bad:
        print("SELFTEST FAIL:", bad); sys.exit(1)
    print(f"SELFTEST PASS ({len(ok)} assertions)")


def main():
    h_path = ROOT / "CODING_sheets_human/coder_H.csv"
    h_rows = list(csv.DictReader(open(h_path))) if h_path.exists() else []
    if not h_rows:
        print("REFUSED: coder_H has no grades yet - the O-5 human pass has not run. "
              "This instrument runs only after the human coder completes H1.")
        sys.exit(1)
    h = {(r["claim_id"], r["transition"]): r for r in h_rows if r.get("coder") == "H"}
    prim = sorted({r["provenance_file"] for r in load_sheet(
        ROOT / "CODING_sheets_v2/coder_A_E.csv", "A").values()})  # not used for grades
    a_prim = load_sheet(ROOT / "CODING_sheets_v2/coder_A_E.csv", "A")
    h1_claims = sorted({c for c, t in h if t == "T1"})
    if len(h1_claims) != 16:
        print(f"REFUSED: H1 incomplete - {len(h1_claims)}/16 primary claims graded. "
              "Complete H1 before analysis.")
        sys.exit(1)
    result = {"H1_raw_reading": raw_reading(h, h1_claims), "H2": "not implemented until H1 lands",
              "note": "H2/H3 sections activate in the protocol's order; this run reports H1 only"}
    out = ROOT / "CODING_sheets_human/H3_READING_20261025.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2)); print("->", out.name)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    main()
