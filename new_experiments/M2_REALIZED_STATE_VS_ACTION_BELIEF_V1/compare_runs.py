#!/usr/bin/env python3
"""Compare two M2 canonical runs after removing declared timing fields only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_NONDETERMINISTIC_FIELDS = [
    "manifest.duration_seconds",
    "fit_manifest.training_seconds",
    "inference_timing.inference_seconds",
    "particle_diagnostics.inference_seconds",
]
TIMING_COLUMNS = {
    "fit_manifest.csv": "training_seconds",
    "inference_timing.csv": "inference_seconds",
    "particle_diagnostics.csv": "inference_seconds",
}
DETERMINISTIC_FILES = (
    "summary.json",
    "episode_metrics.csv",
    "seed_summary.csv",
    "stream_registry.csv",
    "particle_gain_validation.csv",
    "model_diagnostics.csv",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv_without(path: Path, excluded_column: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {key: value for key, value in row.items() if key != excluded_column}
        for row in rows
    ]


def normalized_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest["nondeterministic_fields"] != EXPECTED_NONDETERMINISTIC_FIELDS:
        raise AssertionError(
            f"unexpected nondeterministic field declaration in {path}: "
            f"{manifest['nondeterministic_fields']}"
        )
    manifest.pop("duration_seconds")
    for filename in TIMING_COLUMNS:
        manifest["outputs"].pop(filename)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_a", type=Path)
    parser.add_argument("run_b", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report: dict[str, object] = {
        "status": "PASS",
        "comparison": "SCIENTIFIC_OUTPUTS_EXACT_AFTER_DECLARED_TIMING_EXCLUSIONS",
        "run_a": str(args.run_a.resolve()),
        "run_b": str(args.run_b.resolve()),
        "declared_nondeterministic_fields": EXPECTED_NONDETERMINISTIC_FIELDS,
        "deterministic_files": {},
        "normalized_timing_files": {},
    }

    manifest_a = normalized_manifest(args.run_a / "manifest.json")
    manifest_b = normalized_manifest(args.run_b / "manifest.json")
    if manifest_a != manifest_b:
        raise AssertionError("normalized manifests differ")
    report["normalized_manifest_sha256"] = sha256_bytes(
        json.dumps(manifest_a, sort_keys=True, separators=(",", ":")).encode()
    )

    deterministic = report["deterministic_files"]
    assert isinstance(deterministic, dict)
    for filename in DETERMINISTIC_FILES:
        data_a = (args.run_a / filename).read_bytes()
        data_b = (args.run_b / filename).read_bytes()
        if data_a != data_b:
            raise AssertionError(f"deterministic file differs: {filename}")
        deterministic[filename] = {
            "bytes": len(data_a),
            "sha256": sha256_bytes(data_a),
        }

    normalized = report["normalized_timing_files"]
    assert isinstance(normalized, dict)
    for filename, timing_column in TIMING_COLUMNS.items():
        rows_a = read_csv_without(args.run_a / filename, timing_column)
        rows_b = read_csv_without(args.run_b / filename, timing_column)
        if rows_a != rows_b:
            raise AssertionError(f"scientific columns differ after timing exclusion: {filename}")
        encoded = json.dumps(rows_a, sort_keys=True, separators=(",", ":")).encode()
        normalized[filename] = {
            "excluded_column": timing_column,
            "rows": len(rows_a),
            "normalized_sha256": sha256_bytes(encoded),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
