#!/usr/bin/env python3
"""Run the frozen synthetic PC→SST figure/ground benchmark."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
K = 8
SIDE = 11
N_TRAIN = (32, 128, 512)
N_SEEDS = 30
N_IID = 256
N_OOD = 256
RIDGE = 0.02
INHIBITION = 0.65
KAPPA = 2.0
NOISE_SD = 0.08
OOD_PROBS = np.array([0.35, 0.25, 0.12, 0.08, 0.07, 0.05, 0.04, 0.04])
CONDITIONS = ("selective_aligned", "selective_broken", "global_aligned", "global_broken", "generic_context")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def derived_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "big")


SEEDS = [derived_seed(f"NeuroConverge:{HERE.name}:confirmatory:{i:03d}") for i in range(N_SEEDS)]


def make_responses(rng: np.random.Generator, n: int, skewed: bool) -> tuple[np.ndarray, np.ndarray]:
    """Return synthetic orientation-tuned PC rates and figure masks."""
    bg_probs = OOD_PROBS if skewed else np.full(K, 1 / K)
    backgrounds = rng.choice(K, size=n, p=bg_probs)
    figures = np.empty(n, dtype=np.int64)
    for i, bg in enumerate(backgrounds):
        choices = np.delete(np.arange(K), bg)
        figures[i] = rng.choice(choices)
    cats = np.broadcast_to(backgrounds[:, None, None], (n, SIDE, SIDE)).copy()
    masks = np.zeros((n, SIDE, SIDE), dtype=bool)
    for i, fc in enumerate(figures):
        top = int(rng.integers(1, SIDE - 4))
        left = int(rng.integers(1, SIDE - 4))
        masks[i, top:top + 3, left:left + 3] = True
        cats[i, top:top + 3, left:left + 3] = fc
    angles = np.arange(K) * (np.pi / K)
    tuning = np.exp(KAPPA * (np.cos(2 * (angles[None, :] - angles[:, None])) - 1.0))
    rates = tuning[cats]
    rates += rng.normal(0.0, NOISE_SD, size=rates.shape)
    rates = np.maximum(rates, 0.001)
    rates /= rates.sum(axis=-1, keepdims=True)
    return rates.astype(np.float32), masks


def neighbour_mean(x: np.ndarray) -> np.ndarray:
    pad = np.pad(x, ((0, 0), (1, 1), (1, 1), (0, 0)), mode="edge")
    out = np.zeros_like(x)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            out += pad[:, 1 + dy:1 + dy + SIDE, 1 + dx:1 + dx + SIDE, :]
    return out / 8.0


def transform(x: np.ndarray, surround: np.ndarray, condition: str, perm: np.ndarray) -> np.ndarray:
    if condition.startswith("selective"):
        routed = surround if condition.endswith("aligned") else surround[..., perm]
        return x - INHIBITION * routed
    pooled = surround.mean(axis=-1, keepdims=True)
    return x - INHIBITION * pooled


def fit_lda(features: np.ndarray, masks: np.ndarray) -> tuple[np.ndarray, float]:
    flat_x = features.reshape(-1, features.shape[-1]).astype(np.float64)
    flat_y = masks.reshape(-1)
    pos, neg = flat_x[flat_y], flat_x[~flat_y]
    mp, mn = pos.mean(axis=0), neg.mean(axis=0)
    cp = (pos - mp).T @ (pos - mp) / max(len(pos), 1)
    cn = (neg - mn).T @ (neg - mn) / max(len(neg), 1)
    cov = (cp + cn) * 0.5 + RIDGE * np.eye(flat_x.shape[1])
    w = np.linalg.solve(cov, mp - mn)
    b = -0.5 * float((mp + mn) @ w)
    return w, b


def average_precision(scores: np.ndarray, truth: np.ndarray) -> float:
    flat_s, flat_y = scores.ravel(), truth.ravel().astype(bool)
    order = np.argsort(-flat_s, kind="mergesort")
    ranked = flat_y[order]
    hits = np.flatnonzero(ranked)
    if not len(hits):
        return 0.0
    precision = (np.arange(len(hits)) + 1) / (hits + 1)
    return float(precision.mean())


def image_ap(model: tuple[np.ndarray, float], features: np.ndarray, masks: np.ndarray) -> list[float]:
    w, b = model
    scores = features @ w + b
    return [average_precision(s, y) for s, y in zip(scores, masks)]


def make_splits(seed: int, perm: np.ndarray):
    rng = np.random.default_rng(seed)
    train_x, train_y = make_responses(rng, max(N_TRAIN), False)
    iid_x, iid_y = make_responses(rng, N_IID, False)
    ood_x, ood_y = make_responses(rng, N_OOD, True)
    train_s = neighbour_mean(train_x)
    iid_s, ood_s = neighbour_mean(iid_x), neighbour_mean(ood_x)
    return (train_x, train_s, train_y), (iid_x, iid_s, iid_y), (ood_x, ood_s, ood_y)


def main() -> None:
    if RESULTS.exists() and any(RESULTS.iterdir()):
        raise SystemExit(f"Refusing to overwrite nonempty result directory: {RESULTS}")
    RESULTS.mkdir(parents=True, exist_ok=True)
    contract = HERE / "CONTRACT.md"
    runner = HERE / "run_experiment.py"
    verifier = HERE / "verify_results.py"
    freeze = {
        "study_id": HERE.name,
        "protocol_sha256": sha256(contract),
        "runner_sha256": sha256(runner),
        "verifier_sha256": sha256(verifier),
        "seed_schedule": SEEDS,
        "runtime": {"python": sys.version, "numpy": np.__version__, "platform": platform.platform()},
        "generator": {"n_seeds": N_SEEDS, "train_sizes": N_TRAIN, "iid_images": N_IID, "ood_images": N_OOD,
                      "grid": SIDE, "channels": K, "ridge": RIDGE, "inhibition": INHIBITION,
                      "kappa": KAPPA, "noise_sd": NOISE_SD, "ood_probs": OOD_PROBS.tolist()},
    }
    (RESULTS / "RUN_FREEZE.json").write_text(json.dumps(freeze, indent=2) + "\n")
    rows = []
    for idx, task_seed in enumerate(SEEDS):
        perm_rng = np.random.default_rng(derived_seed(f"{task_seed}:permutation"))
        offset = int(perm_rng.integers(1, K))
        perm = np.roll(np.arange(K), offset)
        tr, iid, ood = make_splits(task_seed, perm)
        split_data = {"iid": iid, "ood": ood}
        train_x, train_s, train_y = tr
        for n in N_TRAIN:
            prefix_x, prefix_s, prefix_y = train_x[:n], train_s[:n], train_y[:n]
            fits = {}
            for condition in CONDITIONS:
                if condition == "generic_context":
                    tr_feat = np.concatenate([prefix_x, prefix_s], axis=-1)
                else:
                    tr_feat = transform(prefix_x, prefix_s, condition, perm)
                fits[condition] = fit_lda(tr_feat, prefix_y)
            for split_name, (sx, ss, sy) in split_data.items():
                for condition in CONDITIONS:
                    if condition == "generic_context":
                        ev_feat = np.concatenate([sx, ss], axis=-1)
                    else:
                        ev_feat = transform(sx, ss, condition, perm)
                    vals = image_ap(fits[condition], ev_feat, sy)
                    for image_idx, ap in enumerate(vals):
                        rows.append((idx, task_seed, n, condition, split_name, image_idx, ap))
        if (idx + 1) % 5 == 0:
            print(f"Completed task-instance block {idx + 1}/{N_SEEDS}")
    out = RESULTS / "PER_IMAGE_AP.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["task_index", "task_seed", "n_train", "condition", "split", "image_index", "average_precision"])
        w.writerows(rows)
    (RESULTS / "EXECUTION.json").write_text(json.dumps({
        "complete": True, "task_instances": N_SEEDS, "per_image_rows": len(rows),
        "per_image_sha256": sha256(out), "runner_sha256": sha256(runner),
        "protocol_sha256": sha256(contract), "freeze_sha256": sha256(RESULTS / "RUN_FREEZE.json"),
    }, indent=2) + "\n")
    print(f"Wrote complete confirmatory dataset: {len(rows)} per-image endpoint rows")


if __name__ == "__main__":
    main()
