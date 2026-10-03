#!/usr/bin/env python3
"""Independent integrity and unit-level inference verifier for DMP V1."""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
FREEZE = HERE / "PRE_RUN_FREEZE.json"
EXPECTED_FAMILIES = ("DELAYED_ASSOCIATION", "STATE_ESTIMATION", "CONTEXTUAL_DECISION")
EXPECTED_SCALES = (128, 512, 2048)
EXPECTED_UNITS = 30
EXPECTED_TEST = 512
BOOTSTRAPS = 20_000
PERMUTATIONS = 50_000


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bootstrap_ci(values: np.ndarray, seed: int) -> list[float]:
    values = np.asarray(values, dtype=np.float64)
    rng = np.random.default_rng(seed)
    means = np.empty(BOOTSTRAPS, dtype=np.float64)
    for start in range(0, BOOTSTRAPS, 500):
        count = min(500, BOOTSTRAPS - start)
        idx = rng.integers(0, len(values), size=(count, len(values)))
        means[start : start + count] = values[idx].mean(axis=1)
    return [float(v) for v in np.quantile(means, [0.025, 0.975])]


def signflip_p(values: np.ndarray, seed: int) -> float:
    values = np.asarray(values, dtype=np.float64)
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    extreme = 0
    done = 0
    while done < PERMUTATIONS:
        count = min(2_000, PERMUTATIONS - done)
        signs = rng.choice(np.asarray([-1.0, 1.0]), size=(count, len(values)))
        stats = np.abs((signs * values[None, :]).mean(axis=1))
        extreme += int(np.count_nonzero(stats >= observed))
        done += count
    return float((extreme + 1) / (PERMUTATIONS + 1))


def holm_adjust(p_values: list[float]) -> list[float]:
    p = np.asarray(p_values, dtype=np.float64)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    m = len(p)
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[idx]))
        adjusted[idx] = running
    return [float(x) for x in adjusted]


def estimate(values: np.ndarray, seed: int) -> dict[str, object]:
    values = np.asarray(values, dtype=np.float64)
    return {"mean": float(values.mean()), "ci95": bootstrap_ci(values, seed),
            "n_independent_units": int(len(values))}


def markdown_summary(summary: dict[str, object]) -> str:
    lines = [
        "# DMP fast–slow correspondence V1 results",
        "",
        "**Status:** independently recalculated from the stored per-trial losses. This is a post-result project extension with a pre-run-frozen module protocol, not a project-level preregistration or biological validation.",
        "",
        "The primary unit is the synthetic task-instance seed. Families and endpoints are reported separately; raw classification loss and normalized state-estimation MSE are not pooled.",
        "",
        "## Primary 2 × 2 interaction",
        "",
        "Positive values mean the cost of breaking slow-context correspondence is larger for the fast–slow model than for its matched short-state control.",
        "",
        "| Task family | Interaction mean (95% paired task-instance bootstrap CI) | Raw permutation P | Holm-adjusted P | Aligned DMP advantage | Task gate |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in summary["primary_by_family"]:
        i = row["interaction"]
        a = row["aligned_advantage"]
        lines.append(f"| {row['family']} | {i['mean']:.5f} [{i['ci95'][0]:.5f}, {i['ci95'][1]:.5f}] | {row['p_raw']:.5g} | {row['p_holm']:.5g} | {a['mean']:.5f} [{a['ci95'][0]:.5f}, {a['ci95'][1]:.5f}] | {row['task_gate']} |")
    lines += ["", "## Data scaling", "", "| Task family | N=128 DMP advantage (95% CI) | N=512 | N=2048 | Advantage slope per log₂(N) (95% CI) |", "|---|---:|---:|---:|---:|"]
    for row in summary["data_scaling_by_family"]:
        vals = row["advantage_by_n"]
        slope = row["advantage_slope_per_log2_n"]
        lines.append(f"| {row['family']} | {vals['128']['mean']:.5f} [{vals['128']['ci95'][0]:.5f}, {vals['128']['ci95'][1]:.5f}] | {vals['512']['mean']:.5f} [{vals['512']['ci95'][0]:.5f}, {vals['512']['ci95'][1]:.5f}] | {vals['2048']['mean']:.5f} [{vals['2048']['ci95'][0]:.5f}, {vals['2048']['ci95'][1]:.5f}] | {slope['mean']:.5f} [{slope['ci95'][0]:.5f}, {slope['ci95'][1]:.5f}] |")
    lines += ["", "## Longer-delay OOD", "", "Per-family and per-model IID/OOD losses are retained in `SUMMARY.json`. OOD results are secondary and use the unchanged fitted model.", "", "## Interpretation ceiling", "", "A positive interaction would support only the tested computational abstraction in these synthetic tasks. It would not validate cortical biology, prove biological provenance caused an advantage, establish a general transfer law, or make the manuscript NMI-ready. The fast–slow idea and DMP-SNN have substantial published precedent.", ""]
    return "\n".join(lines)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=HERE / "results")
    args = parser.parse_args()
    out = args.results_dir.resolve()
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    run = json.loads((out / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
    metrics_path = out / "unit_metrics.csv"
    task_path = out / "TASK_INSTANCE_MANIFEST.json"
    trial_path = out / "TRIAL_LOSSES.npz"
    index_path = out / "TRIAL_LOSS_INDEX.json"
    if run["status"] != "RUN_COMPLETE_UNVERIFIED":
        raise ValueError("run manifest status is not RUN_COMPLETE_UNVERIFIED")
    for key, path in (("contract_sha256", HERE / "CONTRACT.md"), ("runner_sha256", HERE / "run_experiment.py")):
        if freeze[key] != file_sha(path) or run[key] != file_sha(path):
            raise ValueError(f"frozen file hash mismatch: {key}")
    if freeze["verifier_sha256"] != file_sha(Path(__file__)):
        raise ValueError("verifier hash differs from pre-run freeze")
    expected_files = {
        "metrics_sha256": metrics_path,
        "task_instance_manifest_sha256": task_path,
        "trial_losses_sha256": trial_path,
        "trial_loss_index_sha256": index_path,
    }
    for key, path in expected_files.items():
        if run[key] != file_sha(path):
            raise ValueError(f"output hash mismatch: {key}")

    with metrics_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    instances = json.loads(task_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    trial_archive = np.load(trial_path, allow_pickle=False)
    expected_rows = EXPECTED_UNITS * len(EXPECTED_FAMILIES) * len(EXPECTED_SCALES) * 26
    if len(rows) != run["rows"] or len(rows) != expected_rows:
        raise ValueError(f"unexpected unit-metric row count: {len(rows)}; expected {expected_rows}")
    if len(instances) != EXPECTED_UNITS * len(EXPECTED_FAMILIES):
        raise ValueError(f"unexpected task-instance count: {len(instances)}")
    if len(index) != len(rows) or len(trial_archive.files) != len(rows):
        raise ValueError("unit-metric rows and raw trial-loss arrays are not one-to-one")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    runtime = {"python": sys.version, "numpy": np.__version__, "torch": torch.__version__,
               "platform": platform.platform(), "torch_threads": torch.get_num_threads(),
               "deterministic_algorithms": torch.are_deterministic_algorithms_enabled()}
    if freeze["runtime"] != runtime:
        raise ValueError("verification runtime differs from the pre-run freeze")
    if any(run[key] != freeze["runtime"][key] for key in ("python", "numpy", "torch")):
        raise ValueError("recorded run environment differs from the pre-run freeze")
    index_by_key = {entry["trial_loss_key"]: entry for entry in index}
    if len(index_by_key) != len(index) or set(index_by_key) != set(trial_archive.files):
        raise ValueError("trial-loss index keys are missing, duplicated, or unindexed")

    row_keys = set()
    aggregates = {}
    raw_seed = int(freeze["contract_sha256"][:8], 16)
    for row in rows:
        key = row["trial_loss_key"]
        if key not in trial_archive.files:
            raise ValueError(f"missing trial-loss array: {key}")
        vector = np.asarray(trial_archive[key])
        if len(vector) != EXPECTED_TEST or not np.isfinite(vector).all():
            raise ValueError(f"invalid trial-loss vector: {key}")
        recalculated = float(vector.mean())
        if abs(recalculated - float(row["loss"])) > 1e-7:
            raise ValueError(f"metric does not recalculate from trial loss: {key}")
        if int(row["n_test"]) != EXPECTED_TEST:
            raise ValueError(f"unexpected test count: {key}")
        indexed = index_by_key.get(key)
        if indexed is None or any(str(indexed[name]) != str(row[name]) for name in
                                  ("family", "unit", "model", "mechanism", "correspondence", "n_train", "evaluation", "init", "n_test")):
            raise ValueError(f"trial-loss index identity mismatch: {key}")
        identity = (row["family"], int(row["unit"]), row["model"], row["correspondence"],
                    int(row["n_train"]), row["evaluation"], int(row["init"]))
        if identity in row_keys:
            raise ValueError(f"duplicate metric row: {identity}")
        row_keys.add(identity)
        aggregate_key = identity[:-1]
        aggregates.setdefault(aggregate_key, []).append(recalculated)
    aggregate = {k: float(np.mean(v)) for k, v in aggregates.items()}

    for instance in instances:
        expected_checks = {f"train_{n}" for n in EXPECTED_SCALES} | {"iid", "ood"}
        if set(instance["correspondence_checks"]) != expected_checks:
            raise ValueError(f"correspondence check splits mismatch: {instance['family']} {instance['unit']}")
        for split, check in instance["correspondence_checks"].items():
            if check["fixed_points"] != 0:
                raise ValueError(f"correspondence permutation has fixed points: {instance['family']} {instance['unit']} {split}")
            if check["slow_stream_multiset_sha256_aligned"] != check["slow_stream_multiset_sha256_broken"]:
                raise ValueError(f"slow-context marginal mismatch: {instance['family']} {instance['unit']} {split}")
            if check["fast_stream_sha256_aligned"] != check["fast_stream_sha256_broken"]:
                raise ValueError(f"fast stream changed under correspondence intervention: {instance['family']} {instance['unit']} {split}")
        if instance["family"] not in EXPECTED_FAMILIES or not 0 <= int(instance["unit"]) < EXPECTED_UNITS:
            raise ValueError("unexpected task unit identity")
    expected_instances = {(family, unit) for family in EXPECTED_FAMILIES for unit in range(EXPECTED_UNITS)}
    observed_instances = [(instance["family"], int(instance["unit"])) for instance in instances]
    if len(set(observed_instances)) != len(observed_instances) or set(observed_instances) != expected_instances:
        raise ValueError("task-instance manifest is incomplete or contains duplicates")

    expected_dmp = {"STATE_ESTIMATION": 1286, "DELAYED_ASSOCIATION": 1385, "CONTEXTUAL_DECISION": 1385}
    expected_gru = {"STATE_ESTIMATION": 1315, "DELAYED_ASSOCIATION": 1372, "CONTEXTUAL_DECISION": 1372}
    for family in EXPECTED_FAMILIES:
        for unit in range(EXPECTED_UNITS):
            for n in EXPECTED_SCALES:
                actual = [r for r in rows if r["family"] == family and int(r["unit"]) == unit and int(r["n_train"]) == n]
                if len(actual) != 26:
                    raise ValueError(f"cell count mismatch: {family} unit {unit} n={n}: {len(actual)}")
                for split in ("IID", "LONGER_DELAY"):
                    models = {r["model"] for r in actual if r["evaluation"] == split}
                    if models != {"DMP_FAST_SLOW", "SHORT_STATE_CONTROL", "GENERIC_GRU", "TASK_NULL"}:
                        raise ValueError(f"model/evaluation cell set mismatch: {family} unit {unit} n={n} {split}")
                dmp_counts = {int(r["trainable_parameters"]) for r in actual if r["model"] in ("DMP_FAST_SLOW", "SHORT_STATE_CONTROL")}
                gru_counts = {int(r["trainable_parameters"]) for r in actual if r["model"] == "GENERIC_GRU"}
                if dmp_counts != {expected_dmp[family]} or gru_counts != {expected_gru[family]}:
                    raise ValueError(f"parameter count mismatch: {family} unit {unit} n={n}: {dmp_counts}/{gru_counts}")
                if abs(expected_gru[family] - expected_dmp[family]) / expected_dmp[family] > .05:
                    raise ValueError(f"GRU parameter budget exceeded ±5% for {family}")

    primary_rows = []
    task_gate_p = []
    for fi, family in enumerate(EXPECTED_FAMILIES):
        interactions = []
        aligned_advantages = []
        data_advantages = {n: [] for n in EXPECTED_SCALES}
        slopes = []
        viability = []
        ood_records = {}
        for unit in range(EXPECTED_UNITS):
            def loss(model: str, corr: str, n: int, ev: str) -> float:
                return aggregate[(family, unit, model, corr, n, ev)]
            lp_a = loss("DMP_FAST_SLOW", "ALIGNED", 2048, "IID")
            lp_b = loss("DMP_FAST_SLOW", "BROKEN", 2048, "IID")
            lm_a = loss("SHORT_STATE_CONTROL", "ALIGNED", 2048, "IID")
            lm_b = loss("SHORT_STATE_CONTROL", "BROKEN", 2048, "IID")
            interactions.append((lp_b - lp_a) - (lm_b - lm_a))
            aligned_advantages.append(lm_a - lp_a)
            for n in EXPECTED_SCALES:
                data_advantages[n].append(loss("SHORT_STATE_CONTROL", "ALIGNED", n, "IID")
                                          - loss("DMP_FAST_SLOW", "ALIGNED", n, "IID"))
            slopes.append(float(np.polyfit(np.log2(np.asarray(EXPECTED_SCALES)),
                                           [data_advantages[n][-1] for n in EXPECTED_SCALES], 1)[0]))
            null = loss("TASK_NULL", "ALIGNED", 2048, "IID")
            gru = loss("GENERIC_GRU", "ALIGNED", 2048, "IID")
            viability.append(null - gru)
            for model in ("DMP_FAST_SLOW", "SHORT_STATE_CONTROL", "GENERIC_GRU"):
                for corr in ("ALIGNED", "BROKEN"):
                    key = f"{model}|{corr}"
                    diff = loss(model, corr, 2048, "LONGER_DELAY") - loss(model, corr, 2048, "IID")
                    ood_records.setdefault(key, []).append(diff)
        p_interaction = signflip_p(np.asarray(interactions), raw_seed + fi * 29 + 1)
        p_gate = signflip_p(np.asarray(viability), raw_seed + fi * 29 + 2)
        primary_rows.append({"family": family,
                             "interaction": estimate(np.asarray(interactions), raw_seed + fi * 101 + 1),
                             "aligned_advantage": estimate(np.asarray(aligned_advantages), raw_seed + fi * 101 + 2),
                             "p_raw": p_interaction,
                             "task_gate_improvement_null_minus_gru": estimate(np.asarray(viability), raw_seed + fi * 101 + 3),
                             "task_gate_p_raw": p_gate,
                             "advantage_slope_per_log2_n": estimate(np.asarray(slopes), raw_seed + fi * 101 + 4),
                             "ood_loss_change": {k: estimate(np.asarray(v), raw_seed + fi * 211 + j)
                                                 for j, (k, v) in enumerate(ood_records.items())}})
        primary_rows[-1]["advantage_by_n"] = {str(n): estimate(np.asarray(data_advantages[n]), raw_seed + fi * 101 + 10 + j)
                                               for j, n in enumerate(EXPECTED_SCALES)}
        task_gate_p.append(p_gate)
    adjusted = holm_adjust([float(row["p_raw"]) for row in primary_rows])
    gate_adjusted = holm_adjust(task_gate_p)
    for i, row in enumerate(primary_rows):
        row["p_holm"] = adjusted[i]
        row["task_gate_p_holm"] = gate_adjusted[i]
        gate_pass = (float(row["task_gate_p_holm"]) < .05
                     and float(row["task_gate_improvement_null_minus_gru"]["mean"]) > 0)
        row["task_gate"] = "PASS" if gate_pass else "FAIL"
        interaction_pass = (row["interaction"]["ci95"][0] > 0 and row["p_holm"] < .05)
        aligned_pass = row["aligned_advantage"]["ci95"][0] > 0
        row["mechanism_specificity_gate"] = "PASS" if gate_pass and interaction_pass and aligned_pass else "NOT_MET"
    all_cross_task = all(row["task_gate"] == "PASS" and row["mechanism_specificity_gate"] == "PASS" for row in primary_rows)

    scaling_rows = []
    slope_ps = []
    # The slope p-values use the same paired sign-flip procedure; report them as secondary.
    for i, row in enumerate(primary_rows):
        family = row["family"]
        per_unit = []
        for unit in range(EXPECTED_UNITS):
            values = [aggregate[(family, unit, "SHORT_STATE_CONTROL", "ALIGNED", n, "IID")]
                      - aggregate[(family, unit, "DMP_FAST_SLOW", "ALIGNED", n, "IID")] for n in EXPECTED_SCALES]
            per_unit.append(float(np.polyfit(np.log2(np.asarray(EXPECTED_SCALES)), values, 1)[0]))
        slope_ps.append(signflip_p(np.asarray(per_unit), raw_seed + i * 307 + 1))
    slope_adjusted = holm_adjust(slope_ps)
    for i, row in enumerate(primary_rows):
        row["advantage_slope_p_raw"] = slope_ps[i]
        row["advantage_slope_p_holm"] = slope_adjusted[i]
        small_adv = row["advantage_by_n"]["128"]
        slope = row["advantage_slope_per_log2_n"]
        row["sample_efficiency_gate"] = (
            "PASS" if small_adv["ci95"][0] > 0 and slope["ci95"][1] < 0 and slope_adjusted[i] < .05 else "NOT_MET"
        )
        scaling_rows.append({"family": row["family"], "advantage_by_n": row["advantage_by_n"],
                             "advantage_slope_per_log2_n": slope,
                             "slope_p_raw": slope_ps[i], "slope_p_holm": slope_adjusted[i],
                             "sample_efficiency_gate": row["sample_efficiency_gate"]})

    summary = {
        "study_id": "DMP_FAST_SLOW_CORRESPONDENCE_2X2_V1",
        "status": "VERIFIED",
        "project_level_status": "POST_RESULT_EXTENSION; NOT_PROJECT_PREREGISTRATION",
        "n_units_per_family": EXPECTED_UNITS,
        "families": list(EXPECTED_FAMILIES),
        "primary_by_family": primary_rows,
        "data_scaling_by_family": scaling_rows,
        "cross_task_mechanism_specificity_gate": "PASS" if all_cross_task else "NOT_MET",
        "trial_loss_arrays_recalculated": len(rows),
        "unit_metric_rows": len(rows),
        "independent_verification": {
            "file_hashes": "PASS", "trial_loss_recalculation": "PASS",
            "correspondence_marginals_and_derangements": "PASS", "parameter_counts": "PASS",
            "unit_and_cell_completeness": "PASS", "family_specific_inference": "PASS"
        },
        "interpretation_ceiling": "Synthetic fast–slow dynamics × correspondence results only; no biological validation, universal transfer law, hardware claim, or NMI readiness follows.",
    }
    summary_path = out / "SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    report_path = out / "SUMMARY.md"
    report_path.write_text(markdown_summary(summary), encoding="utf-8")
    verification = {"status": "PASS", "metrics_sha256": file_sha(metrics_path),
                    "trial_losses_sha256": file_sha(trial_path), "summary_sha256": file_sha(summary_path),
                    "verifier_sha256": file_sha(Path(__file__)), "freeze_sha256": file_sha(FREEZE)}
    (out / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    print(f"verification PASS; primary cross-task gate={summary['cross_task_mechanism_specificity_gate']}")


if __name__ == "__main__":
    main()
