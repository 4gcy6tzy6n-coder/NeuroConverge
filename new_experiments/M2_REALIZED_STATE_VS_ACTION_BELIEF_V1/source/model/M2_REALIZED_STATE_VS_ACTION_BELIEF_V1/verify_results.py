#!/usr/bin/env python3
"""Independent verifier for the implementation-only AcRKN smoke report."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
NAME = "M2_REALIZED_STATE_VS_ACTION_BELIEF_V1"
RUNNER = ROOT / "model" / NAME / "run_experiment.py"
VENDOR = (
    ROOT
    / "model"
    / "M2_ACTION_CONDITIONED_RKN_2D_PURSUIT_V1"
    / "vendor"
    / "acrkn_cell.py"
)
CONDITIONS = ("NO_REVERSAL", "HIDDEN_REVERSAL", "REVEALED_REVERSAL")
ACRKN_ARMS = ("ACRKN_ACTION_ONLY", "ACRKN_REALIZED_STATE", "ACRKN_REVERSAL_REVEALED")
GRU_ARMS = ("GRU_ACTION_ONLY", "GRU_REALIZED_STATE")
LEARNED_ARMS = ACRKN_ARMS + GRU_ARMS
ALL_ARMS = LEARNED_ARMS + ("TASK_AWARE_PARTICLE_FILTER",)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(report_path: Path) -> dict:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    assert report["classification"] == "IMPLEMENTATION_ONLY_NO_TASK_OUTCOMES"
    assert report["signal_semantics_status"] == "FROZEN_IN_CONTRACT"
    assert report["smoke_input_semantics"] == "RANDOM_INTERFACE_TENSORS_NOT_EXPERIMENT_FEATURES"
    assert report["causal_order"] == [
        "encode_features_t",
        "posterior_update_t",
        "select_action_t",
        "action_conditioned_predict_t_plus_1",
    ]
    batch = int(report["batch_size"])
    sequence = int(report["sequence_length"])
    assert report["input_shape"] == [batch, sequence, 6]
    assert report["action_shape"] == [batch, sequence]
    assert report["final_prior_mean_shape"] == [batch, 6]
    assert report["final_prior_covariance_shapes"] == [[batch, 3]] * 3
    assert report["encoded_observation_shape"] == [batch, 3]
    assert report["observation_variance_shape"] == [batch, 3]
    assert report["posterior_mean_shape"] == [batch, 6]
    assert report["posterior_covariance_shapes"] == [[batch, 3]] * 3

    records = report["trainable_parameters"]
    recomputed_count = sum(int(record["count"]) for record in records)
    declared_count = int(report["trainable_parameter_count"])
    target = int(report["target_parameter_count"])
    tolerance = int(report["parameter_tolerance"])
    assert recomputed_count == declared_count
    assert abs(declared_count - target) <= tolerance
    assert declared_count == 320
    assert int(report["frozen_parameter_count"]) == 25
    assert records and all(record["gradient_finite"] for record in records)
    assert report["all_trainable_gradients_finite"] is True
    assert report["deterministic_eval_repeat"] is True
    assert report["action_transition_sensitive"] is True
    assert report["runner_sha256"] == sha256(RUNNER)
    assert report["vendored_acrkn_sha256"] == sha256(VENDOR)
    return {
        "status": "PASS",
        "classification": report["classification"],
        "trainable_parameter_count": declared_count,
        "target_parameter_count": target,
        "parameter_tolerance": tolerance,
        "checks": [
            "causal operation order declaration",
            "input/action/belief tensor shapes",
            "independent parameter-count sum",
            "321 +/- 2 budget",
            "finite gradients for every trainable parameter",
            "deterministic eval-mode recurrence",
            "action-conditioned transition sensitivity",
            "runner and vendored-source hashes",
            "no task-outcome classification",
        ],
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def verify_results(results_dir: Path) -> dict:
    manifest = json.loads((results_dir / "manifest.json").read_text())
    summary = json.loads((results_dir / "summary.json").read_text())
    fits = read_csv(results_dir / "fit_manifest.csv")
    episodes = read_csv(results_dir / "episode_metrics.csv")
    seeds = read_csv(results_dir / "seed_summary.csv")
    streams = read_csv(results_dir / "stream_registry.csv")
    gains = read_csv(results_dir / "particle_gain_validation.csv")
    particles = read_csv(results_dir / "particle_diagnostics.csv")
    timings = read_csv(results_dir / "inference_timing.csv")
    diagnostics = read_csv(results_dir / "model_diagnostics.csv")
    assert "not biological transfer" in manifest["classification"]
    nblocks = len(manifest["training_seeds"])
    ntest = int(manifest["test_episodes_per_block_arm_condition"])
    assert manifest["conditions"] == list(CONDITIONS)
    assert manifest["arms"] == list(ALL_ARMS)
    assert len(fits) == nblocks * len(LEARNED_ARMS)
    assert len(episodes) == nblocks * len(CONDITIONS) * len(ALL_ARMS) * ntest
    assert len(seeds) == nblocks * len(CONDITIONS) * len(ALL_ARMS)
    assert len(streams) == nblocks * len(CONDITIONS)
    assert len(gains) == 12
    assert len(particles) == nblocks * len(CONDITIONS) * 3
    assert len(timings) == nblocks * len(CONDITIONS) * len(ALL_ARMS)
    assert len(diagnostics) == nblocks * len(CONDITIONS) * len(ACRKN_ARMS)

    acrkn_counts = {int(row["parameter_count"]) for row in fits if row["arm"] in ACRKN_ARMS}
    gru_counts = {int(row["parameter_count"]) for row in fits if row["arm"] in GRU_ARMS}
    assert len(acrkn_counts) == 1 and abs(next(iter(acrkn_counts)) - 321) <= 2
    assert len(gru_counts) == 1
    assert all(int(row["updates"]) == int(manifest["updates"]) for row in fits)
    expected_tokens = int(manifest["updates"]) * int(manifest["batch_size"]) * 64
    assert all(int(row["training_tokens"]) == expected_tokens for row in fits)
    for row in fits:
        parameters = np.asarray(json.loads(row["parameters_json"]), dtype=float)
        assert len(parameters) == int(row["parameter_count"])
        assert np.isfinite(parameters).all()
        assert np.isfinite(float(row["initial_training_loss"]))
        assert np.isfinite(float(row["final_training_loss"]))

    stream_lookup = {(int(row["seed_block"]), row["condition"]): row for row in streams}
    for block in range(nblocks):
        hidden = stream_lookup[(block, "HIDDEN_REVERSAL")]
        revealed = stream_lookup[(block, "REVEALED_REVERSAL")]
        no_reversal = stream_lookup[(block, "NO_REVERSAL")]
        assert hidden["evaluation_seed"] == revealed["evaluation_seed"]
        assert hidden["paired_stream_group"] == revealed["paired_stream_group"]
        assert no_reversal["evaluation_seed"] != hidden["evaluation_seed"]
        assert float(no_reversal["reversal_probability"]) == 0.0
        assert float(hidden["reversal_probability"]) == float(revealed["reversal_probability"]) == 0.25

    grouped: dict[tuple[int, str, str], list[dict[str, str]]] = {}
    unique = set()
    for row in episodes:
        full_key = (int(row["seed_block"]), row["condition"], row["arm"], int(row["episode_id"]))
        assert full_key not in unique
        unique.add(full_key)
        grouped.setdefault(full_key[:3], []).append(row)
        assert row["condition"] in CONDITIONS and row["arm"] in ALL_ARMS
        for field in ("tracking_mse", "command_energy", "missing_fraction"):
            assert np.isfinite(float(row[field]))
    assert all(len(rows) == ntest for rows in grouped.values())
    recomputed = {
        key: {
            field: float(np.mean([float(row[field]) for row in rows]))
            for field in ("tracking_mse", "command_energy", "missing_fraction")
        }
        for key, rows in grouped.items()
    }
    for row in seeds:
        key = (int(row["seed_block"]), row["condition"], row["arm"])
        assert int(row["n_episodes"]) == ntest
        for field, value in recomputed[key].items():
            assert np.isclose(float(row[field]), value, rtol=1e-11, atol=1e-12)

    def mean(block: int, condition: str, arm: str) -> float:
        return recomputed[(block, condition, arm)]["tracking_mse"]

    primary = [
        mean(block, "HIDDEN_REVERSAL", "ACRKN_ACTION_ONLY")
        - mean(block, "HIDDEN_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(nblocks)
    ]
    revealed = [
        mean(block, "REVEALED_REVERSAL", "ACRKN_REVERSAL_REVEALED")
        - mean(block, "REVEALED_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(nblocks)
    ]
    recovery = [primary[index] - revealed[index] for index in range(nblocks)]
    no_reversal = [
        mean(block, "NO_REVERSAL", "ACRKN_ACTION_ONLY")
        - mean(block, "NO_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(nblocks)
    ]
    assert np.allclose(primary, summary["primary_seed_block_values"], rtol=1e-11, atol=1e-12)
    assert np.allclose(revealed, summary["revealed_gap_seed_block_values"], rtol=1e-11, atol=1e-12)
    assert np.allclose(recovery, summary["information_recovery_seed_block_values"], rtol=1e-11, atol=1e-12)
    assert np.allclose(no_reversal, summary["no_reversal_gap_seed_block_values"], rtol=1e-11, atol=1e-12)
    assert np.isclose(np.mean(primary), summary["primary_summary"]["mean"], rtol=1e-12, atol=1e-12)

    selected = [row for row in gains if row["selected"] == "True"]
    assert len(selected) == 1
    assert float(selected[0]["mean_tracking_mse"]) == min(float(row["mean_tracking_mse"]) for row in gains)
    assert {int(row["particle_count"]) for row in particles} == {64, 128, 256}
    assert all(0 < float(row["mean_ess_fraction"]) <= 1 for row in particles)
    assert all(0 <= float(row["resample_fraction"]) <= 1 for row in particles)
    assert all(float(row["mean_observation_variance"]) > 0 for row in diagnostics)
    assert all(float(row["mean_posterior_variance"]) > 0 for row in diagnostics)

    for filename, record in manifest["outputs"].items():
        path = results_dir / filename
        assert path.stat().st_size == int(record["bytes"])
        assert sha256(path) == record["sha256"]
    source_checks = (
        (ROOT / "summery" / NAME / "CONTRACT.md", "contract_sha256"),
        (RUNNER, "runner_sha256"),
        (ROOT / "model" / NAME / "verify_results.py", "verifier_sha256"),
        (VENDOR, "vendored_acrkn_sha256"),
    )
    for path, key in source_checks:
        assert sha256(path) == manifest[key]
    return {
        "status": "PASS",
        "mode": manifest["mode"],
        "training_seed_blocks": nblocks,
        "fit_rows": len(fits),
        "episode_rows": len(episodes),
        "seed_summary_rows": len(seeds),
        "acrkn_parameter_count": next(iter(acrkn_counts)),
        "gru_parameter_count": next(iter(gru_counts)),
        "checks": [
            "row completeness and unique episode keys",
            "paired hidden/revealed stream identifiers",
            "parameter/update/token accounting",
            "seed-summary and all frozen contrast recomputation",
            "particle gain/ESS/convergence diagnostics",
            "positive AcRKN covariance diagnostics",
            "source and output hashes",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-report", type=Path)
    parser.add_argument("--results-dir", type=Path)
    args = parser.parse_args()
    if (args.smoke_report is None) == (args.results_dir is None):
        parser.error("provide exactly one of --smoke-report or --results-dir")
    result = verify(args.smoke_report) if args.smoke_report is not None else verify_results(args.results_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
