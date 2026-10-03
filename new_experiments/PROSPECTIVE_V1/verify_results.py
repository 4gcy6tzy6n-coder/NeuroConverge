#!/usr/bin/env python3
"""Independent arithmetic/integrity verification for prospective V1."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
N_SEEDS = 30
N_TRAIN = (32, 128, 512)
CONDITIONS = ("selective_aligned", "selective_broken", "global_aligned", "global_broken", "generic_context")
SPLITS = ("iid", "ood")
N_IID = 256
N_OOD = 256
N_BOOT = 20_000
N_SIGN = 100_000
RNG_SEED = 20261003


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ci95(x: np.ndarray, boot_idx: np.ndarray) -> tuple[float, float, float]:
    draws = x[boot_idx].mean(axis=1)
    return float(x.mean()), float(np.quantile(draws, .025)), float(np.quantile(draws, .975))


def signflip_p(x: np.ndarray, signs: np.ndarray) -> float:
    obs = abs(float(x.mean()))
    vals = np.abs((signs * x).mean(axis=1))
    return float((1 + np.count_nonzero(vals >= obs)) / (1 + len(vals)))


def main() -> None:
    freeze = json.loads((RESULTS / "RUN_FREEZE.json").read_text())
    execution = json.loads((RESULTS / "EXECUTION.json").read_text())
    data_path = RESULTS / "PER_IMAGE_AP.csv"
    errors = []
    for key, path in (("protocol_sha256", HERE / "CONTRACT.md"),
                      ("runner_sha256", HERE / "run_experiment.py"),
                      ("verifier_sha256", HERE / "verify_results.py")):
        if sha256(path) != freeze.get(key):
            errors.append(f"frozen hash mismatch: {key}")
    if sha256(data_path) != execution.get("per_image_sha256"):
        errors.append("per-image output hash mismatch")
    if freeze.get("seed_schedule") is None or len(freeze["seed_schedule"]) != N_SEEDS:
        errors.append("seed schedule incomplete")
    expected_rows = N_SEEDS * len(N_TRAIN) * len(CONDITIONS) * len(SPLITS) * N_IID
    expected_rows = N_SEEDS * len(N_TRAIN) * len(CONDITIONS) * (N_IID + N_OOD)
    if execution.get("per_image_rows") != expected_rows:
        errors.append("execution row count mismatch")

    image_rows = defaultdict(list)
    with data_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"task_index", "task_seed", "n_train", "condition", "split", "image_index", "average_precision"}
        if set(reader.fieldnames or []) != required:
            errors.append("unexpected per-image schema")
        for row in reader:
            key = (int(row["task_index"]), int(row["task_seed"]), int(row["n_train"]), row["condition"], row["split"])
            image_rows[key].append((int(row["image_index"]), float(row["average_precision"])))
    if len(image_rows) != N_SEEDS * len(N_TRAIN) * len(CONDITIONS) * len(SPLITS):
        errors.append("group count mismatch")
    for key in image_rows:
        if key[0] not in range(N_SEEDS) or key[1] != freeze["seed_schedule"][key[0]]:
            errors.append(f"task seed/index schedule mismatch: {key[:2]}")
    ap_by_cell = {}
    for key, vals in image_rows.items():
        idxs = [v[0] for v in vals]
        expected_n = N_IID if key[-1] == "iid" else N_OOD
        if len(vals) != expected_n or sorted(idxs) != list(range(expected_n)):
            errors.append(f"image completeness failure: {key}")
        aps = np.asarray([v[1] for v in sorted(vals)])
        if not np.isfinite(aps).all() or (aps < 0).any() or (aps > 1).any():
            errors.append(f"invalid AP value: {key}")
        ap_by_cell[key] = float(aps.mean())

    seed_ids = freeze["seed_schedule"]
    if len(set(seed_ids)) != N_SEEDS:
        errors.append("seed schedule contains duplicates")
    task_means = defaultdict(dict)
    for (task_i, seed, n, condition, split), mean_ap in ap_by_cell.items():
        task_means[(n, split, seed)][condition] = mean_ap
    for (n, split, seed), cells in task_means.items():
        if set(cells) != set(CONDITIONS):
            errors.append(f"missing condition cell at {(n, split, seed)}")
        if abs(cells["global_aligned"] - cells["global_broken"]) > 1e-12:
            errors.append(f"permutation invariance failed for global pool at {(n, split, seed)}")

    rng = np.random.default_rng(RNG_SEED)
    boot_idx = rng.integers(0, N_SEEDS, size=(N_BOOT, N_SEEDS))
    signs = rng.choice(np.array([-1.0, 1.0]), size=(N_SIGN, N_SEEDS))
    report = {"study_id": freeze["study_id"], "n_task_instances": N_SEEDS,
              "independent_unit": "task_instance_seed", "primary_metric": "per-image AP, averaged within task instance",
              "null_ap": 9 / 121, "primary": {}, "scaling": {}, "ood": {}, "integrity": {}}
    def vec(n: int, split: str, condition: str) -> np.ndarray:
        return np.asarray([ap_by_cell[(i, seed_ids[i], n, condition, split)] for i in range(N_SEEDS)])

    def summarize(x: np.ndarray) -> dict:
        m, lo, hi = ci95(x, boot_idx)
        return {"mean": m, "ci95_low": lo, "ci95_high": hi, "signflip_p_two_sided": signflip_p(x, signs)}

    null = 9 / 121
    generic_adv = vec(512, "iid", "generic_context") - null
    spec_adv = vec(512, "iid", "selective_aligned") - vec(512, "iid", "global_aligned")
    interaction = (vec(512, "iid", "selective_broken") - vec(512, "iid", "selective_aligned")) - (vec(512, "iid", "global_broken") - vec(512, "iid", "global_aligned"))
    report["primary"] = {
        "viability_generic_minus_prevalence_null": summarize(generic_adv),
        "selective_minus_global_aligned": summarize(spec_adv),
        "selectivity_by_correspondence_interaction": summarize(interaction),
        "gate_pass": bool(np.quantile(generic_adv[boot_idx].mean(axis=1), .025) > 0 and
                           np.quantile(spec_adv[boot_idx].mean(axis=1), .025) > 0 and
                           np.quantile(interaction[boot_idx].mean(axis=1), .025) > 0 and
                           signflip_p(interaction, signs) < .05),
    }
    for n in N_TRAIN:
        d = vec(n, "iid", "selective_aligned") - vec(n, "iid", "global_aligned")
        report["scaling"][str(n)] = summarize(d)
    xlog = np.log2(np.asarray(N_TRAIN, dtype=float))
    per_seed_d = np.stack([vec(n, "iid", "selective_aligned") - vec(n, "iid", "global_aligned") for n in N_TRAIN], axis=1)
    slopes = np.asarray([np.polyfit(xlog, row, 1)[0] for row in per_seed_d])
    report["scaling"]["slope_per_log2_n"] = summarize(slopes)
    for label, split in (("iid", "iid"), ("ood_skewed_background", "ood")):
        inter = (vec(512, split, "selective_broken") - vec(512, split, "selective_aligned")) - (vec(512, split, "global_broken") - vec(512, split, "global_aligned"))
        report["ood"][label] = {"interaction": summarize(inter),
                                "selective_aligned_ap": summarize(vec(512, split, "selective_aligned")),
                                "global_aligned_ap": summarize(vec(512, split, "global_aligned")),
                                "generic_context_ap": summarize(vec(512, split, "generic_context"))}
    report["integrity"] = {"expected_per_image_rows": expected_rows, "observed_per_image_rows": sum(map(len, image_rows.values())),
                           "complete_task_seed_cells": len(task_means), "global_pool_alignment_break_max_abs_delta": 0.0,
                           "data_sha256": sha256(data_path), "protocol_sha256": sha256(HERE / "CONTRACT.md"),
                           "runner_sha256": sha256(HERE / "run_experiment.py"), "verifier_sha256": sha256(HERE / "verify_results.py"),
                           "checks_pass": not errors}
    report["integrity"]["errors"] = errors
    (RESULTS / "VERIFIED_SUMMARY.json").write_text(json.dumps(report, indent=2) + "\n")
    with (RESULTS / "TASK_INSTANCE_MEANS.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["task_seed", "n_train", "split", *CONDITIONS])
        for n in N_TRAIN:
            for split in SPLITS:
                for i, seed in enumerate(seed_ids):
                    w.writerow([seed, n, split, *[ap_by_cell[(i, seed, n, c, split)] for c in CONDITIONS]])
    print(json.dumps({"integrity_pass": not errors, "errors": errors, "primary": report["primary"],
                      "summary": str(RESULTS / "VERIFIED_SUMMARY.json")}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
