#!/usr/bin/env python3
"""Frozen M5 correspondence-preserved timing simulation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
FREEZE_PATH = ROOT / "PRE_RUN_FREEZE_AMENDMENT_01.json"
RESULTS_DIR = ROOT / "results"

SEEDS = tuple(range(51000, 51030))
N_TRAIN = 1200
N_TEST = 400
N_TIME = 40
TARGET_MIN = 6
TARGET_MAX = 33
TARGET_RANGE = TARGET_MAX - TARGET_MIN
N_TARGETS = TARGET_RANGE + 1
PULSE_WIDTH = 2.25
TIMING_NOISE_SD = 1.5
OBS_NOISE_SD = 0.20
N_RBF = 16
RBF_WIDTH = 2.75
LEARNING_RATE = 0.08
RIDGE = 0.01
BOOTSTRAP_DRAWS = 20000
ARMS = (
    "CF_TIMED_LOCAL",
    "NO_TRACE",
    "CF_TIME_SHUFFLE",
    "GENERIC_MATCHED_RBF",
    "EXACT_REPLAY_REFERENCE",
)
REGIMES = ("ALIGNED", "BROKEN")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_freeze() -> dict:
    freeze = json.loads(FREEZE_PATH.read_text())
    for rel, expected in freeze["frozen_files_sha256"].items():
        observed = sha256(ROOT / rel)
        if observed != expected:
            raise RuntimeError(f"freeze mismatch for {rel}: {observed} != {expected}")
    return freeze


def derangement(rng: np.random.Generator, n: int) -> np.ndarray:
    base = np.arange(n)
    for _ in range(100):
        p = rng.permutation(n)
        if np.all(p != base):
            return p
    return np.roll(base, 1)


def generate_split(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    target = rng.integers(TARGET_MIN, TARGET_MAX + 1, size=n, endpoint=False)
    centre = target + rng.normal(0.0, TIMING_NOISE_SD, size=n)
    time = np.arange(N_TIME, dtype=np.float64)[None, :]
    pulse = np.exp(-0.5 * ((time - centre[:, None]) / PULSE_WIDTH) ** 2)
    x = pulse + rng.normal(0.0, OBS_NOISE_SD, size=(n, N_TIME))
    return x.astype(np.float64), target.astype(np.int64)


def rbf_features(x: np.ndarray) -> np.ndarray:
    centres = np.linspace(0.0, N_TIME - 1.0, N_RBF)
    time = np.arange(N_TIME, dtype=np.float64)
    basis = np.exp(-0.5 * ((time[:, None] - centres[None, :]) / RBF_WIDTH) ** 2)
    positive = np.maximum(x, 0.0)
    features = positive @ basis
    norms = np.linalg.norm(features, axis=1, keepdims=True)
    return features / np.maximum(norms, 1e-12)


def no_trace_features(x: np.ndarray) -> np.ndarray:
    return np.column_stack((x[:, -1], x.mean(axis=1)))


def softmax(z: np.ndarray) -> np.ndarray:
    z = z - np.max(z)
    exp = np.exp(z)
    return exp / exp.sum()


def online_predict(
    train_features: np.ndarray,
    train_target: np.ndarray,
    test_features: np.ndarray,
    teaching_target: np.ndarray | None = None,
) -> np.ndarray:
    train_aug = np.column_stack((train_features, np.ones(len(train_features))))
    test_aug = np.column_stack((test_features, np.ones(len(test_features))))
    weights = np.zeros((train_aug.shape[1], N_TARGETS), dtype=np.float64)
    labels = train_target if teaching_target is None else teaching_target
    for feature, target in zip(train_aug, labels):
        probabilities = softmax(feature @ weights)
        error = -probabilities
        error[int(target) - TARGET_MIN] += 1.0
        weights += LEARNING_RATE * np.outer(feature, error)
    probabilities = np.apply_along_axis(softmax, 1, test_aug @ weights)
    bins = np.arange(TARGET_MIN, TARGET_MAX + 1, dtype=np.float64)
    return probabilities @ bins


def ridge_predict(train_features: np.ndarray, train_y: np.ndarray, test_features: np.ndarray) -> np.ndarray:
    a = np.column_stack((train_features, np.ones(len(train_features))))
    b = np.column_stack((test_features, np.ones(len(test_features))))
    penalty = np.eye(a.shape[1]) * RIDGE
    penalty[-1, -1] = 0.0
    weights = np.linalg.solve(a.T @ a + penalty, a.T @ train_y.astype(np.float64))
    return np.clip(b @ weights, TARGET_MIN, TARGET_MAX)


def nmae(prediction: np.ndarray, target: np.ndarray) -> float:
    return float(np.mean(np.abs(prediction - target)) / TARGET_RANGE)


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    indices = rng.integers(0, len(values), size=(BOOTSTRAP_DRAWS, len(values)))
    means = values[indices].mean(axis=1)
    lo, hi = np.quantile(means, [0.025, 0.975])
    return float(lo), float(hi)


def run_seed(seed: int) -> list[dict]:
    rng = np.random.default_rng(seed)
    train_x, train_y = generate_split(rng, N_TRAIN)
    test_x, test_y = generate_split(rng, N_TEST)
    train_break = derangement(rng, N_TRAIN)
    test_break = derangement(rng, N_TEST)
    cf_shuffle = derangement(rng, N_TRAIN)

    train_rbf = rbf_features(train_x)
    test_rbf = rbf_features(test_x)
    train_current = no_trace_features(train_x)
    test_current = no_trace_features(test_x)
    rows: list[dict] = []

    for regime in REGIMES:
        y_train = train_y if regime == "ALIGNED" else train_y[train_break]
        y_test = test_y if regime == "ALIGNED" else test_y[test_break]
        predictions = {
            "CF_TIMED_LOCAL": online_predict(train_rbf, y_train, test_rbf),
            "NO_TRACE": online_predict(train_current, y_train, test_current),
            "CF_TIME_SHUFFLE": online_predict(train_rbf, y_train, test_rbf, y_train[cf_shuffle]),
            "GENERIC_MATCHED_RBF": ridge_predict(train_rbf, y_train, test_rbf),
            "EXACT_REPLAY_REFERENCE": ridge_predict(train_x, y_train, test_x),
        }
        constant = np.full(N_TEST, np.median(y_train), dtype=np.float64)
        constant_nmae = nmae(constant, y_test)
        input_hash = hashlib.sha256(train_x.tobytes() + test_x.tobytes()).hexdigest()
        target_hash = hashlib.sha256(y_train.tobytes() + y_test.tobytes()).hexdigest()
        for arm in ARMS:
            rows.append(
                {
                    "seed": seed,
                    "regime": regime,
                    "arm": arm,
                    "nmae": nmae(predictions[arm], y_test),
                    "constant_median_nmae": constant_nmae,
                    "train_input_sha256": input_hash,
                    "regime_targets_sha256": target_hash,
                }
            )
    return rows


def main() -> None:
    freeze = verify_freeze()
    if RESULTS_DIR.exists() and any(RESULTS_DIR.iterdir()):
        raise RuntimeError("results directory is not empty; frozen run will not overwrite outcomes")
    RESULTS_DIR.mkdir(exist_ok=True)

    rows = [row for seed in SEEDS for row in run_seed(seed)]
    metrics_path = RESULTS_DIR / "per_seed_metrics.csv"
    with metrics_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lookup = {(int(r["seed"]), r["regime"], r["arm"]): float(r["nmae"]) for r in rows}
    contrast_rows = []
    bootstrap_rng = np.random.default_rng(2026100105)
    effects = {}
    for arm in ARMS:
        values = np.array(
            [lookup[(seed, "BROKEN", arm)] - lookup[(seed, "ALIGNED", arm)] for seed in SEEDS]
        )
        lo, hi = bootstrap_ci(values, bootstrap_rng)
        effects[arm] = {
            "mean_broken_minus_aligned_nmae": float(values.mean()),
            "bootstrap_95_ci": [lo, hi],
            "positive_seed_count": int(np.sum(values > 0)),
            "n_seeds": len(SEEDS),
        }
        for seed, value in zip(SEEDS, values):
            contrast_rows.append({"seed": seed, "arm": arm, "broken_minus_aligned_nmae": float(value)})

    contrasts_path = RESULTS_DIR / "per_seed_correspondence_effects.csv"
    with contrasts_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(contrast_rows[0]))
        writer.writeheader()
        writer.writerows(contrast_rows)

    aligned_replay = np.array([lookup[(s, "ALIGNED", "EXACT_REPLAY_REFERENCE")] for s in SEEDS])
    aligned_constant = np.array(
        [
            float(next(r["constant_median_nmae"] for r in rows if int(r["seed"]) == s and r["regime"] == "ALIGNED"))
            for s in SEEDS
        ]
    )
    relative_improvement = float(1.0 - aligned_replay.mean() / aligned_constant.mean())
    replay_ci = effects["EXACT_REPLAY_REFERENCE"]["bootstrap_95_ci"]
    gate_pass = relative_improvement >= 0.25 and replay_ci[0] > 0.0
    cf_ci = effects["CF_TIMED_LOCAL"]["bootstrap_95_ci"]
    if not gate_pass:
        decision = "TASK_GATE_FAILED__NO_MECHANISTIC_INTERPRETATION"
    elif cf_ci[0] > 0.0:
        decision = "CF_CORRESPONDENCE_EFFECT_SUPPORTED"
    elif cf_ci[1] < 0.0:
        decision = "CF_CORRESPONDENCE_EFFECT_REVERSED"
    else:
        decision = "CF_CORRESPONDENCE_EFFECT_NOT_DETECTED"

    primary = {
        "status": "FROZEN_RUN_COMPLETE",
        "classification": "synthetic post-hoc project extension; prospective contract frozen before first outcome run",
        "outcome": "normalized mean absolute error (lower is better)",
        "primary_estimand": "paired task-seed mean nMAE(BROKEN) - nMAE(ALIGNED) for CF_TIMED_LOCAL",
        "task_viability": {
            "passed": gate_pass,
            "aligned_exact_replay_relative_improvement_vs_constant": relative_improvement,
            "required_relative_improvement": 0.25,
            "exact_replay_effect_ci_lower_must_exceed_zero": replay_ci,
        },
        "effects": effects,
        "decision": decision,
        "interpretation_ceiling": "synthetic fixed-task artificial result only; no biological validation or general AI claim",
    }
    (RESULTS_DIR / "primary_result.json").write_text(json.dumps(primary, indent=2) + "\n")

    manifest = {
        "freeze": freeze,
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "regimes": list(REGIMES),
        "fixed_parameters": {
            "n_train": N_TRAIN,
            "n_test": N_TEST,
            "n_time": N_TIME,
            "target_min": TARGET_MIN,
            "target_max": TARGET_MAX,
            "pulse_width": PULSE_WIDTH,
            "timing_noise_sd": TIMING_NOISE_SD,
            "observation_noise_sd": OBS_NOISE_SD,
            "n_rbf": N_RBF,
            "rbf_width": RBF_WIDTH,
            "learning_rate": LEARNING_RATE,
            "ridge": RIDGE,
            "bootstrap_draws": BOOTSTRAP_DRAWS,
        },
        "numpy_version": np.__version__,
        "output_sha256": {
            "per_seed_metrics.csv": sha256(metrics_path),
            "per_seed_correspondence_effects.csv": sha256(contrasts_path),
            "primary_result.json": sha256(RESULTS_DIR / "primary_result.json"),
        },
    }
    (RESULTS_DIR / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(primary, indent=2))


if __name__ == "__main__":
    main()
