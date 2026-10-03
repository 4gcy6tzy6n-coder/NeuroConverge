#!/usr/bin/env python3
"""Independent arithmetic and provenance verification for the frozen M5 run."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
EXPECTED_SEEDS = set(range(51000, 51030))
EXPECTED_ARMS = {
    "CF_TIMED_LOCAL",
    "NO_TRACE",
    "CF_TIME_SHUFFLE",
    "GENERIC_MATCHED_RBF",
    "EXACT_REPLAY_REFERENCE",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    freeze = json.loads((ROOT / "PRE_RUN_FREEZE_AMENDMENT_01.json").read_text())
    for rel, expected in freeze["frozen_files_sha256"].items():
        assert sha256(ROOT / rel) == expected, f"frozen file changed: {rel}"

    manifest = json.loads((RESULTS / "run_manifest.json").read_text())
    for rel, expected in manifest["output_sha256"].items():
        assert sha256(RESULTS / rel) == expected, f"output hash mismatch: {rel}"

    with (RESULTS / "per_seed_metrics.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 30 * 2 * 5
    assert {int(r["seed"]) for r in rows} == EXPECTED_SEEDS
    assert {r["arm"] for r in rows} == EXPECTED_ARMS
    assert {r["regime"] for r in rows} == {"ALIGNED", "BROKEN"}
    assert all(np.isfinite(float(r["nmae"])) for r in rows)
    assert all(np.isfinite(float(r["constant_median_nmae"])) for r in rows)
    assert all(0.0 <= float(r["nmae"]) <= 1.0 for r in rows)

    grouped: dict[tuple[int, str], dict[str, float]] = defaultdict(dict)
    input_hashes: dict[tuple[int, str], str] = {}
    for r in rows:
        key = (int(r["seed"]), r["arm"])
        grouped[key][r["regime"]] = float(r["nmae"])
        input_hashes[(int(r["seed"]), r["regime"])] = r["train_input_sha256"]
    for seed in EXPECTED_SEEDS:
        assert input_hashes[(seed, "ALIGNED")] == input_hashes[(seed, "BROKEN")]

    with (RESULTS / "per_seed_correspondence_effects.csv").open(newline="") as f:
        saved_contrasts = list(csv.DictReader(f))
    assert len(saved_contrasts) == 30 * 5
    saved = {(int(r["seed"]), r["arm"]): float(r["broken_minus_aligned_nmae"]) for r in saved_contrasts}
    for key, regimes in grouped.items():
        recomputed = regimes["BROKEN"] - regimes["ALIGNED"]
        assert np.isclose(saved[key], recomputed, rtol=0.0, atol=1e-14)

    primary = json.loads((RESULTS / "primary_result.json").read_text())
    for arm in EXPECTED_ARMS:
        values = np.array([saved[(seed, arm)] for seed in sorted(EXPECTED_SEEDS)])
        reported = primary["effects"][arm]
        assert np.isclose(values.mean(), reported["mean_broken_minus_aligned_nmae"], atol=1e-14)
        assert int(np.sum(values > 0)) == reported["positive_seed_count"]

    verification = {
        "status": "PASS",
        "checks": [
            "contract and run code match pre-run frozen SHA-256 values",
            "all 30 seeds x 2 regimes x 5 arms are present exactly once",
            "all recorded performance values are finite and within the normalized 0-1 range",
            "ALIGNED and BROKEN input hashes match within every seed",
            "all 150 paired seed-arm correspondence effects recompute exactly",
            "reported arm means and positive-seed counts recompute exactly",
            "result files match the run-manifest SHA-256 values",
        ],
    }
    (RESULTS / "POSTRUN_VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
