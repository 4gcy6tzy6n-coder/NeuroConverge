#!/usr/bin/env python3
"""Frozen DMP fast–slow × correspondence synthetic validation."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
FREEZE = HERE / "PRE_RUN_FREEZE.json"
DEFAULT_OUT = HERE / "results"
FAMILIES = ("DELAYED_ASSOCIATION", "STATE_ESTIMATION", "CONTEXTUAL_DECISION")
SCALES = (128, 512, 2048)
N_UNITS = 30
N_TEST = 512
T_TRAIN = 64
T_OOD = 128
BATCH = 64
EPOCHS = 10
N_INIT = 2
DMP_WIDTH = 32
MEMORY_DIM = 2
GRU_WIDTH = 18
FAST_LEAK = 0.5
THRESHOLD = 1.0
LEARNING_RATE = 0.003
BOOTSTRAPS = 20_000
PERMUTATIONS = 50_000


class SurrogateSpike(torch.autograd.Function):
    @staticmethod
    def forward(ctx, value):
        ctx.save_for_backward(value)
        return (value > 0).to(value.dtype)

    @staticmethod
    def backward(ctx, grad_output):
        (value,) = ctx.saved_tensors
        slope = 5.0
        derivative = 1.0 / (1.0 + slope * torch.abs(value)) ** 2
        return grad_output * derivative


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def array_sha(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


def row_multiset_sha(values: np.ndarray) -> str:
    flat = np.asarray(values).reshape(len(values), -1)
    order = np.lexsort(flat.T[::-1])
    return array_sha(flat[order])


def seed_for(contract_hash: str, *parts: object) -> int:
    raw = "|".join((contract_hash, *(str(x) for x in parts))).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big") % (2**31 - 1)


def legendre_matrices(dim: int = MEMORY_DIM, horizon: float = 32.0) -> tuple[np.ndarray, np.ndarray]:
    a = np.zeros((dim, dim), dtype=np.float64)
    b = np.zeros(dim, dtype=np.float64)
    for i in range(dim):
        b[i] = (2 * i + 1) * ((-1) ** i)
        for j in range(dim):
            a[i, j] = (2 * i + 1) * (-1.0 if i < j else (-1) ** (i - j + 1))
    ac = a / horizon
    bc = b / horizon
    ac_t = torch.as_tensor(ac, dtype=torch.float64)
    abar = torch.matrix_exp(ac_t).numpy()
    bbar = np.linalg.solve(ac, (abar - np.eye(dim)) @ bc)
    return abar.astype(np.float32), bbar.astype(np.float32)


LMU_A, LMU_B = legendre_matrices()


def make_mapping(seed: int) -> np.ndarray:
    return np.random.default_rng(seed).permutation(4).astype(np.int64)


def generate_family(family: str, n: int, steps: int, seed: int,
                    config_seed: int | None = None) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    rng = np.random.default_rng(seed)
    cfg = np.random.default_rng(seed if config_seed is None else config_seed)
    x = np.zeros((n, steps, 4), dtype=np.float32)
    meta: dict[str, object] = {"family": family, "steps": steps}
    if family == "DELAYED_ASSOCIATION":
        context = rng.integers(0, 4, size=n)
        query = rng.integers(0, 4, size=n)
        c_bits = np.stack(((context >> 1) & 1, context & 1), axis=1).astype(np.float32)
        q_bits = np.stack(((query >> 1) & 1, query & 1), axis=1).astype(np.float32)
        x[:, :4, :2] = c_bits[:, None, :] + rng.normal(0, .06, (n, 4, 2)).astype(np.float32)
        query_start = 36 if steps == T_TRAIN else 68
        x[:, query_start : query_start + 4, 2:] = q_bits[:, None, :] + rng.normal(0, .06, (n, 4, 2)).astype(np.float32)
        mapping = make_mapping((seed if config_seed is None else config_seed) ^ 0x51A7)
        y = mapping[(context + query) % 4]
        meta.update({"context": context.tolist(), "mapping": mapping.tolist(), "context_channels": [0, 1]})
    elif family == "STATE_ESTIMATION":
        phi = float(cfg.uniform(.90, .98))
        switch_p = float(cfg.uniform(.015, .045))
        latent = np.zeros((n, steps), dtype=np.float32)
        regime = np.empty((n, steps), dtype=np.int8)
        latent[:, 0] = rng.normal(0, 1, n)
        regime[:, 0] = rng.choice(np.asarray([-1, 1], dtype=np.int8), size=n)
        for t in range(1, steps):
            latent[:, t] = phi * latent[:, t - 1] + rng.normal(0, math.sqrt(1 - phi * phi), n)
            flips = rng.random(n) < switch_p
            regime[:, t] = np.where(flips, -regime[:, t - 1], regime[:, t - 1])
        # The regime indicates which sensor is reliable at each step.
        good1 = regime > 0
        sigma1 = np.where(good1, .25, 1.2)
        sigma2 = np.where(good1, 1.2, .25)
        x[:, :, 0] = latent + rng.normal(size=(n, steps)).astype(np.float32) * sigma1
        x[:, :, 1] = latent + rng.normal(size=(n, steps)).astype(np.float32) * sigma2
        x[:, :, 2] = (regime > 0).astype(np.float32)
        x[:, :, 3] = (regime < 0).astype(np.float32)
        y = latent[:, -1].astype(np.float32)
        meta.update({"phi": phi, "switch_probability": switch_p, "context_channels": [2, 3],
                     "target_variance": float(np.var(y))})
    elif family == "CONTEXTUAL_DECISION":
        context = rng.integers(0, 4, size=n)
        evidence = rng.integers(0, 4, size=n)
        c_bits = np.stack(((context >> 1) & 1, context & 1), axis=1).astype(np.float32)
        e_bits = np.stack(((evidence >> 1) & 1, evidence & 1), axis=1).astype(np.float32)
        x[:, :4, :2] = c_bits[:, None, :] + rng.normal(0, .06, (n, 4, 2)).astype(np.float32)
        # Four evidence votes are spread over the final 16 steps.
        evidence_start = 36 if steps == T_TRAIN else 68
        x[:, evidence_start : evidence_start + 16, 2:] = e_bits[:, None, :] + rng.normal(0, .18, (n, 16, 2)).astype(np.float32)
        mapping = make_mapping((seed if config_seed is None else config_seed) ^ 0xD31C)
        y = mapping[(evidence + 2 * context) % 4]
        meta.update({"context": context.tolist(), "mapping": mapping.tolist(), "context_channels": [0, 1]})
    else:
        raise ValueError(f"unknown task family: {family}")
    return x, np.asarray(y), meta


def derangement(n: int, rng: np.random.Generator, strata: np.ndarray | None = None) -> np.ndarray:
    base = np.arange(n)
    for _ in range(500):
        perm = rng.permutation(n)
        ok = np.all(perm != base)
        if strata is not None:
            ok = ok and np.all(strata[perm] != strata)
        if ok:
            return perm
    # A cyclic rotation of a random sort is guaranteed to have no fixed points.
    order = rng.permutation(n)
    perm = np.empty(n, dtype=np.int64)
    perm[order] = np.roll(order, 1)
    if strata is not None and np.any(strata[perm] == strata):
        groups: dict[int, list[int]] = {}
        for i, value in enumerate(strata.tolist()):
            groups.setdefault(int(value), []).append(i)
        if len(groups) < 2:
            raise ValueError("cannot stratify a correspondence derangement with one stratum")
        labels = sorted(groups)
        for i, value in enumerate(labels):
            src = groups[value]
            dst = groups[labels[(i + 1) % len(labels)]]
            for j, target in enumerate(src):
                perm[target] = dst[j % len(dst)]
    if np.any(perm == base) or (strata is not None and np.any(strata[perm] == strata)):
        raise RuntimeError("failed to construct a valid correspondence derangement")
    return perm


def shuffle_context(x: np.ndarray, family: str, seed: int,
                    strata: np.ndarray | None) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    channels = [2, 3] if family == "STATE_ESTIMATION" else [0, 1]
    perm = derangement(len(x), rng, strata)
    out = x.copy()
    out[:, :, channels] = x[perm][:, :, channels]
    if row_multiset_sha(out[:, :, channels]) != row_multiset_sha(x[:, :, channels]):
        raise RuntimeError("context stream marginal was not preserved")
    return out, perm


def repeat_array(value: np.ndarray, copies: int) -> torch.Tensor:
    return torch.as_tensor(np.repeat(value[None, ...], copies, axis=0), dtype=torch.float32)


def initial_weights(seed: int, copies: int, outputs: int, width: int = DMP_WIDTH) -> dict[str, torch.Tensor]:
    rng = np.random.default_rng(seed)
    def normal(shape, scale):
        # One base initialization per replicate, copied across the 2×2 cells.
        base_shape = shape[1:]
        bases = [rng.normal(0, scale, base_shape).astype(np.float32) for _ in range(copies // 4)]
        values = []
        for base in bases:
            values.extend([base.copy() for _ in range(4)])
        return torch.nn.Parameter(torch.as_tensor(np.stack(values)))
    return {
        "win": normal((copies, width, 4), 0.22),
        "wrec": normal((copies, width, width), 1 / math.sqrt(width)),
        "wx": normal((copies, 1, 4), 0.35),
        "bx": normal((copies, 1), 0.0),
        "wm": normal((copies, width, MEMORY_DIM), 0.18),
        "bu": normal((copies, width), 0.0),
        "wout": normal((copies, outputs, width), 0.20),
        "bout": normal((copies, outputs), 0.0),
    }


def snn_forward(x: torch.Tensor, params: dict[str, torch.Tensor], mechanism: torch.Tensor) -> torch.Tensor:
    # x: [K, batch, time, 4], mechanism: [K, d, d]; all factorial replicas are batched.
    k, batch, steps, _ = x.shape
    dtype, device = x.dtype, x.device
    u = torch.zeros((k, batch, DMP_WIDTH), dtype=dtype, device=device)
    spikes = torch.zeros_like(u)
    memory = torch.zeros((k, batch, MEMORY_DIM), dtype=dtype, device=device)
    bbar_t = torch.as_tensor(LMU_B, dtype=dtype, device=device)[None, None, :].expand(k, 1, -1)
    output = None
    for t in range(steps):
        xt = x[:, :, t, :]
        drive = torch.tanh(torch.bmm(xt, params["wx"].transpose(1, 2)) + params["bx"][:, None, :])
        memory = torch.bmm(mechanism, memory.transpose(1, 2)).transpose(1, 2) + drive * bbar_t
        current = (torch.bmm(xt, params["win"].transpose(1, 2))
                   + torch.bmm(spikes, params["wrec"].transpose(1, 2))
                   + torch.bmm(memory, params["wm"].transpose(1, 2))
                   + params["bu"][:, None, :])
        u = FAST_LEAK * u + current - THRESHOLD * spikes
        spikes = SurrogateSpike.apply(u - THRESHOLD)
        output = u
    return torch.bmm(output, params["wout"].transpose(1, 2)) + params["bout"][:, None, :]


def gru_initial_weights(seed: int, copies: int, outputs: int) -> dict[str, torch.Tensor]:
    rng = np.random.default_rng(seed)
    h = GRU_WIDTH
    # PyTorch-style reset/update/new gate blocks, batched over correspondence and starts.
    def parameter(shape, scale):
        base_shape = shape[1:]
        bases = [rng.normal(0, scale, base_shape).astype(np.float32) for _ in range(copies // 2)]
        values = []
        for base in bases:
            values.extend([base.copy(), base.copy()])
        return torch.nn.Parameter(torch.as_tensor(np.stack(values)))
    return {
        "w_ih": parameter((copies, 3 * h, 4), 0.12),
        "w_hh": parameter((copies, 3 * h, h), 0.10),
        "b_ih": parameter((copies, 3 * h), 0.0),
        "b_hh": parameter((copies, 3 * h), 0.0),
        "wout": parameter((copies, outputs, h), 0.15),
        "bout": parameter((copies, outputs), 0.0),
    }


def gru_forward(x: torch.Tensor, p: dict[str, torch.Tensor]) -> torch.Tensor:
    k, batch, steps, _ = x.shape
    h = GRU_WIDTH
    state = torch.zeros((k, batch, h), dtype=x.dtype, device=x.device)
    for t in range(steps):
        xt = x[:, :, t, :]
        ix = torch.bmm(xt, p["w_ih"].transpose(1, 2)) + p["b_ih"][:, None, :]
        hh = torch.bmm(state, p["w_hh"].transpose(1, 2)) + p["b_hh"][:, None, :]
        xr, xz, xn = ix.chunk(3, dim=-1)
        hr, hz, hn = hh.chunk(3, dim=-1)
        reset = torch.sigmoid(xr + hr)
        update = torch.sigmoid(xz + hz)
        candidate = torch.tanh(xn + reset * hn)
        state = (1 - update) * candidate + update * state
    return torch.bmm(state, p["wout"].transpose(1, 2)) + p["bout"][:, None, :]


def param_count_dmp(outputs: int) -> int:
    return DMP_WIDTH * 4 + DMP_WIDTH**2 + 4 + 1 + DMP_WIDTH * MEMORY_DIM + DMP_WIDTH + outputs * DMP_WIDTH + outputs


def param_count_gru(outputs: int) -> int:
    h = GRU_WIDTH
    return 3 * h * 4 + 3 * h * h + 6 * h + outputs * h + outputs


def fit_factorial(x_train: np.ndarray, y_train: np.ndarray, family: str, n_init: int,
                  seed: int, epochs: int = EPOCHS, batch_size: int = BATCH) -> tuple[dict[str, np.ndarray], int]:
    is_class = family != "STATE_ESTIMATION"
    outputs = 4 if is_class else 1
    copies = n_init * 2 * 2
    # Copy order is init × mechanism × correspondence; M− and M+ share starts.
    x_cells = []
    for init in range(n_init):
        for mech in range(2):
            for corr in range(2):
                x_cells.append(x_train[corr])
    x_np = np.stack(x_cells, axis=0).astype(np.float32)
    xt = torch.as_tensor(x_np)
    if is_class:
        yt_np = np.repeat(np.asarray(y_train, dtype=np.int64)[None, :], copies, axis=0)
        yt = torch.as_tensor(yt_np, dtype=torch.long)
    else:
        yt_np = np.repeat(np.asarray(y_train, dtype=np.float32)[None, :, None], copies, axis=0)
        yt = torch.as_tensor(yt_np)
    params = initial_weights(seed, copies, outputs)
    ctrl_m = FAST_LEAK * np.eye(MEMORY_DIM, dtype=np.float32)
    mats = []
    for _init in range(n_init):
        for mech in range(2):
            for _corr in range(2):
                mats.append(LMU_A if mech == 1 else ctrl_m)
    mechanism = torch.as_tensor(np.stack(mats), dtype=torch.float32)
    optimizer = torch.optim.Adam(list(params.values()), lr=LEARNING_RATE)
    rng = np.random.default_rng(seed ^ 0x77A3)
    n = len(x_train[0])
    for _epoch in range(epochs):
        order = rng.permutation(n)
        for start in range(0, n, batch_size):
            idx = torch.as_tensor(order[start : start + batch_size], dtype=torch.long)
            pred = snn_forward(xt[:, idx], params, mechanism)
            target = yt[:, idx]
            if is_class:
                loss = torch.nn.functional.cross_entropy(pred.reshape(-1, outputs), target.reshape(-1))
            else:
                loss = torch.mean((pred - target) ** 2)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(list(params.values()), 5.0)
            optimizer.step()
    predictions = {}
    # Final inference is performed on paired IID/OOD datasets by evaluate_factorial.
    predictions["params"] = params
    predictions["mechanism"] = mechanism
    return predictions, param_count_dmp(outputs)


def fit_gru(x_train: np.ndarray, y_train: np.ndarray, family: str, n_init: int, seed: int,
            epochs: int = EPOCHS, batch_size: int = BATCH) -> tuple[dict[str, torch.Tensor], int]:
    is_class = family != "STATE_ESTIMATION"
    outputs = 4 if is_class else 1
    copies = n_init * 2
    xt = torch.as_tensor(np.stack([x_train[c] for _ in range(n_init) for c in range(2)], axis=0), dtype=torch.float32)
    if is_class:
        yt = torch.as_tensor(np.repeat(np.asarray(y_train, dtype=np.int64)[None, :], copies, axis=0), dtype=torch.long)
    else:
        yt = torch.as_tensor(np.repeat(np.asarray(y_train, dtype=np.float32)[None, :, None], copies, axis=0))
    p = gru_initial_weights(seed, copies, outputs)
    optimizer = torch.optim.Adam(list(p.values()), lr=LEARNING_RATE)
    rng = np.random.default_rng(seed ^ 0xE01D)
    n = len(x_train[0])
    for _epoch in range(epochs):
        order = rng.permutation(n)
        for start in range(0, n, batch_size):
            idx = torch.as_tensor(order[start : start + batch_size], dtype=torch.long)
            pred = gru_forward(xt[:, idx], p)
            target = yt[:, idx]
            if is_class:
                loss = torch.nn.functional.cross_entropy(pred.reshape(-1, outputs), target.reshape(-1))
            else:
                loss = torch.mean((pred - target) ** 2)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(list(p.values()), 5.0)
            optimizer.step()
    return p, param_count_gru(outputs)


def model_predictions(x_conditions: list[np.ndarray], fit: dict[str, object], family: str, kind: str,
                      n_init: int) -> np.ndarray:
    copies = n_init * (4 if kind == "DMP" else 2)
    x_cells = []
    for _init in range(n_init):
        if kind == "DMP":
            for _mech in range(2):
                x_cells.extend(x_conditions)
        else:
            x_cells.extend(x_conditions)
    xt = torch.as_tensor(np.stack(x_cells, axis=0), dtype=torch.float32)
    if kind == "DMP":
        out = snn_forward(xt, fit["params"], fit["mechanism"])
        # Return init × mechanism × correspondence × trial × output.
        return out.detach().numpy().reshape(n_init, 2, 2, len(x_conditions[0]), -1)
    out = gru_forward(xt, fit)
    return out.detach().numpy().reshape(n_init, 2, len(x_conditions[0]), -1)


def normalize_targets(family: str, y_train: np.ndarray) -> tuple[np.ndarray, float, float]:
    if family != "STATE_ESTIMATION":
        return y_train, 0.0, 1.0
    # The generator has unit stationary latent variance by construction.
    return np.asarray(y_train, dtype=np.float32), 0.0, 1.0


def cell_losses(pred: np.ndarray, y: np.ndarray, family: str) -> np.ndarray:
    if family == "STATE_ESTIMATION":
        return np.mean((pred[..., 0] - y[None, ...]) ** 2, axis=-1)
    labels = np.argmax(pred, axis=-1)
    return np.mean(labels != y[None, ...], axis=-1)


def summary_loss(preds: np.ndarray, y: np.ndarray, family: str) -> float:
    if family == "STATE_ESTIMATION":
        return float(np.mean((preds[..., 0] - y) ** 2))
    return float(np.mean(np.argmax(preds, axis=-1) != y))


def trial_loss_values(preds: np.ndarray, y: np.ndarray, family: str) -> np.ndarray:
    if family == "STATE_ESTIMATION":
        return np.square(preds[:, 0] - y).astype(np.float32)
    return (np.argmax(preds, axis=-1) != y).astype(np.float32)


def add_metric_record(rows: list[dict[str, object]], trial_losses: dict[str, np.ndarray],
                      record: dict[str, object], losses: np.ndarray) -> None:
    key = "__".join((str(record["family"]), f"u{record['unit']}", str(record["model"]),
                     str(record["correspondence"]), f"n{record['n_train']}",
                     str(record["evaluation"]), f"i{record['init']}"))
    if key in trial_losses:
        raise ValueError(f"duplicate trial-loss key: {key}")
    vector = np.asarray(losses, dtype=np.float32)
    record["loss"] = float(np.mean(vector))
    record["trial_loss_key"] = key
    rows.append(record)
    trial_losses[key] = vector


def run_one_unit(family: str, unit: int, contract_hash: str) -> tuple[list[dict[str, object]], dict[str, object], dict[str, np.ndarray]]:
    root_seed = seed_for(contract_hash, family, unit, "data")
    config_seed = seed_for(contract_hash, family, unit, "task_configuration")
    train_base, y_raw, meta = generate_family(family, max(SCALES), T_TRAIN, root_seed, config_seed)
    test_id, y_id, meta_id = generate_family(family, N_TEST, T_TRAIN,
                                             seed_for(contract_hash, family, unit, "test_iid"), config_seed)
    test_ood, y_ood, meta_ood = generate_family(family, N_TEST, T_OOD,
                                                seed_for(contract_hash, family, unit, "test_ood"), config_seed)
    y_id_raw = np.asarray(y_id).copy()
    y_ood_raw = np.asarray(y_ood).copy()
    train_corr_by_n = {n: [train_base[:n]] for n in SCALES}
    test_iid_corr = [test_id]
    test_ood_corr = [test_ood]
    correspondence_checks = {}
    for split, x in (("iid", test_id), ("ood", test_ood)):
        perm_seed = seed_for(contract_hash, family, unit, split, "derangement")
        broken, perm = shuffle_context(x, family, perm_seed, None)
        channels = [2, 3] if family == "STATE_ESTIMATION" else [0, 1]
        fast_channels = [0, 1] if family == "STATE_ESTIMATION" else [2, 3]
        correspondence_checks[split] = {
            "permutation_seed": perm_seed,
            "permutation_sha256": array_sha(perm),
            "fixed_points": int(np.count_nonzero(perm == np.arange(len(perm)))),
            "slow_stream_multiset_sha256_aligned": row_multiset_sha(x[:, :, channels]),
            "slow_stream_multiset_sha256_broken": row_multiset_sha(broken[:, :, channels]),
            "fast_stream_sha256_aligned": array_sha(x[:, :, fast_channels]),
            "fast_stream_sha256_broken": array_sha(broken[:, :, fast_channels]),
        }
        if split == "iid":
            test_iid_corr.append(broken)
        else:
            test_ood_corr.append(broken)
    channels = [2, 3] if family == "STATE_ESTIMATION" else [0, 1]
    fast_channels = [0, 1] if family == "STATE_ESTIMATION" else [2, 3]
    for n in SCALES:
        x = train_base[:n]
        perm_seed = seed_for(contract_hash, family, unit, f"train_{n}", "derangement")
        broken, perm = shuffle_context(x, family, perm_seed, None)
        correspondence_checks[f"train_{n}"] = {
            "permutation_seed": perm_seed,
            "permutation_sha256": array_sha(perm),
            "fixed_points": int(np.count_nonzero(perm == np.arange(len(perm)))),
            "slow_stream_multiset_sha256_aligned": row_multiset_sha(x[:, :, channels]),
            "slow_stream_multiset_sha256_broken": row_multiset_sha(broken[:, :, channels]),
            "fast_stream_sha256_aligned": array_sha(x[:, :, fast_channels]),
            "fast_stream_sha256_broken": array_sha(broken[:, :, fast_channels]),
        }
        train_corr_by_n[n].append(broken)
    records: list[dict[str, object]] = []
    trial_losses: dict[str, np.ndarray] = {}
    instance_manifest = {"family": family, "unit": unit, "task_configuration_seed": config_seed,
                         "train_data_seed": root_seed,
                         "iid_test_seed": seed_for(contract_hash, family, unit, "test_iid"),
                         "ood_test_seed": seed_for(contract_hash, family, unit, "test_ood"),
                         "configuration": {k: v for k, v in meta.items() if k != "context"},
                         "target_sha256": {"train": array_sha(y_raw), "iid": array_sha(y_id_raw),
                                           "ood": array_sha(y_ood_raw)},
                         "correspondence_checks": correspondence_checks,
                         "dmp_seed_shared_across_scales": seed_for(contract_hash, family, unit, "dmp"),
                         "gru_seed_shared_across_scales": seed_for(contract_hash, family, unit, "gru")}
    for n_train in SCALES:
        x_train_corr = train_corr_by_n[n_train]
        y_norm, y_mean, y_scale = normalize_targets(family, y_raw[:n_train])
        y_id = ((y_id_raw - y_mean) / y_scale).astype(np.float32) if family == "STATE_ESTIMATION" else y_id_raw
        y_ood = ((y_ood_raw - y_mean) / y_scale).astype(np.float32) if family == "STATE_ESTIMATION" else y_ood_raw
        fit_seed = seed_for(contract_hash, family, unit, "dmp")
        dmp_fit, dmp_params = fit_factorial(x_train_corr, y_norm, family, N_INIT, fit_seed)
        gru_seed = seed_for(contract_hash, family, unit, "gru")
        gru_fit, gru_params = fit_gru(x_train_corr, y_norm[:n_train], family, N_INIT, gru_seed)
        for shift_name, x_eval_corr, y_eval in (("IID", test_iid_corr, y_id), ("LONGER_DELAY", test_ood_corr, y_ood)):
            predictions = model_predictions(x_eval_corr, dmp_fit, family, "DMP", N_INIT)
            for init_idx in range(N_INIT):
                for mech_idx, mech_name in enumerate(("SHORT_STATE_CONTROL", "DMP_FAST_SLOW")):
                    for corr_idx, corr_name in ((0, "ALIGNED"), (1, "BROKEN")):
                        cell_pred = predictions[init_idx, mech_idx, corr_idx]
                        record = {"family": family, "unit": unit, "model": mech_name, "mechanism": mech_name,
                                  "correspondence": corr_name, "n_train": n_train, "evaluation": shift_name,
                                  "init": init_idx, "n_test": len(y_eval), "trainable_parameters": dmp_params,
                                  "target_mean": y_mean, "target_scale": y_scale}
                        add_metric_record(records, trial_losses, record, trial_loss_values(cell_pred, y_eval, family))
            gru_predictions = model_predictions(x_eval_corr, gru_fit, family, "GRU", N_INIT)
            for init_idx in range(N_INIT):
                for corr_idx, corr_name in ((0, "ALIGNED"), (1, "BROKEN")):
                    record = {"family": family, "unit": unit, "model": "GENERIC_GRU", "mechanism": "REFERENCE",
                              "correspondence": corr_name, "n_train": n_train, "evaluation": shift_name,
                              "init": init_idx, "n_test": len(y_eval), "trainable_parameters": gru_params,
                              "target_mean": y_mean, "target_scale": y_scale}
                    add_metric_record(records, trial_losses, record,
                                      trial_loss_values(gru_predictions[init_idx, corr_idx], y_eval, family))
            if family == "STATE_ESTIMATION":
                null_value = float(np.mean(y_norm))
                null_loss = float(np.mean((y_eval - null_value) ** 2))
            else:
                train_counts = np.bincount(np.asarray(y_norm, dtype=np.int64), minlength=4)
                null_label = int(np.argmax(train_counts))
                null_loss = float(np.mean(np.asarray(y_eval) != null_label))
            null_errors = (np.square(y_eval - null_value).astype(np.float32) if family == "STATE_ESTIMATION"
                           else (np.asarray(y_eval) != null_label).astype(np.float32))
            null_record = {"family": family, "unit": unit, "model": "TASK_NULL", "mechanism": "BOUND",
                           "correspondence": "ALIGNED", "n_train": n_train, "evaluation": shift_name,
                           "init": -1, "n_test": len(y_eval), "trainable_parameters": 0,
                           "target_mean": y_mean, "target_scale": y_scale}
            add_metric_record(records, trial_losses, null_record, null_errors)
    return records, instance_manifest, trial_losses


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def smoke_check() -> dict[str, object]:
    checks = []
    for i, family in enumerate(FAMILIES):
        x, y, _ = generate_family(family, 128, T_TRAIN, 811_001 + i, 811_009 + i)
        broken, perm = shuffle_context(x, family, 811_003 + i, None)
        if np.any(perm == np.arange(len(perm))):
            raise RuntimeError(f"{family}: smoke correspondence permutation contains a fixed point")
        channels = [2, 3] if family == "STATE_ESTIMATION" else [0, 1]
        if row_multiset_sha(broken[:, :, channels]) != row_multiset_sha(x[:, :, channels]):
            raise RuntimeError(f"{family}: correspondence manipulation changed the context marginal")
        dmp, dmp_count = fit_factorial([x, broken], y, family, 1, 811_004 + i, epochs=1, batch_size=32)
        gru, gru_count = fit_gru([x, broken], y, family, 1, 811_005 + i, epochs=1, batch_size=32)
        dmp_out = model_predictions([x[:8], broken[:8]], dmp, family, "DMP", 1)
        gru_out = model_predictions([x[:8], broken[:8]], gru, family, "GRU", 1)
        outputs = 1 if family == "STATE_ESTIMATION" else 4
        if dmp_out.shape != (1, 2, 2, 8, outputs) or gru_out.shape != (1, 2, 8, outputs):
            raise RuntimeError(f"{family}: smoke output shape mismatch: {dmp_out.shape}; {gru_out.shape}")
        if not np.isfinite(dmp_out).all() or not np.isfinite(gru_out).all():
            raise RuntimeError(f"{family}: smoke predictions contain non-finite values")
        if dmp_count != param_count_dmp(outputs) or abs(dmp_count - param_count_gru(outputs)) / dmp_count > .05:
            raise RuntimeError(f"{family}: smoke parameter-count match failed")
        checks.append({"family": family, "shape": "PASS", "finite": "PASS", "marginal": "PASS",
                       "parameters": {"dmp": dmp_count, "gru": gru_count}})
    return {"families": checks, "outcomes_summarized": False}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--smoke", action="store_true", help="run one non-confirmatory unit per family")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.smoke:
        units = (90_001,)
        out = args.output_dir.expanduser().resolve().parent / "smoke"
    else:
        if not FREEZE.exists():
            raise FileNotFoundError(f"freeze manifest must exist before confirmatory run: {FREEZE}")
        freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
        runtime = {"python": sys.version, "numpy": np.__version__, "torch": torch.__version__,
                   "platform": platform.platform(), "torch_threads": torch.get_num_threads(),
                   "deterministic_algorithms": torch.are_deterministic_algorithms_enabled()}
        for key, path in (("runner_sha256", Path(__file__)), ("contract_sha256", HERE / "CONTRACT.md"),
                          ("verifier_sha256", HERE / "verify_results.py")):
            if freeze[key] != digest(path):
                raise RuntimeError(f"{key} differs from the pre-run freeze")
        if freeze["runtime"] != runtime:
            raise RuntimeError("runtime versions/platform differ from the pre-run freeze")
        if (freeze["learning_rate"] != LEARNING_RATE or freeze["epochs"] != EPOCHS
                or freeze["n_units_per_family"] != N_UNITS or freeze["scales"] != list(SCALES)):
            raise RuntimeError("runtime parameters differ from the pre-run freeze")
        units = tuple(range(N_UNITS))
        out = args.output_dir.expanduser().resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"refusing to overwrite nonempty output directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    if args.smoke:
        # Smoke checks use a separate fixed seed and never touch confirmatory units.
        result = smoke_check()
        (out / "SMOKE_COMPLETE.json").write_text(json.dumps(result, indent=2) + "\n")
        print("smoke complete; shape/integrity checks passed; no outcomes summarized", flush=True)
        return
    contract_hash = freeze["contract_sha256"]
    all_rows: list[dict[str, object]] = []
    all_instances: list[dict[str, object]] = []
    all_trial_losses: dict[str, np.ndarray] = {}
    start_time = time.time()
    for family in FAMILIES:
        for unit in units:
            unit_rows, unit_manifest, unit_trial_losses = run_one_unit(family, unit, contract_hash)
            all_rows.extend(unit_rows)
            all_instances.append(unit_manifest)
            all_trial_losses.update(unit_trial_losses)
            print(f"completed {family} unit {unit + 1}/{N_UNITS}", flush=True)
    result_path = out / "unit_metrics.csv"
    write_csv(result_path, all_rows)
    (out / "TASK_INSTANCE_MANIFEST.json").write_text(json.dumps(all_instances, indent=2) + "\n", encoding="utf-8")
    trial_path = out / "TRIAL_LOSSES.npz"
    np.savez_compressed(trial_path, **all_trial_losses)
    trial_index = [{"trial_loss_key": row["trial_loss_key"], **{k: row[k] for k in
                    ("family", "unit", "model", "mechanism", "correspondence", "n_train", "evaluation", "init", "n_test")}}
                   for row in all_rows]
    index_path = out / "TRIAL_LOSS_INDEX.json"
    index_path.write_text(json.dumps(trial_index, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "study_id": "DMP_FAST_SLOW_CORRESPONDENCE_2X2_V1",
        "status": "RUN_COMPLETE_UNVERIFIED",
        "runtime_seconds": time.time() - start_time,
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "deterministic_algorithms": True,
        "torch_threads": torch.get_num_threads(),
        "units_per_family": N_UNITS,
        "rows": len(all_rows),
        "trial_loss_arrays": len(all_trial_losses),
        "contract_sha256": digest(HERE / "CONTRACT.md"),
        "runner_sha256": digest(Path(__file__)),
        "metrics_sha256": digest(result_path),
        "task_instance_manifest_sha256": digest(out / "TASK_INSTANCE_MANIFEST.json"),
        "trial_losses_sha256": digest(trial_path),
        "trial_loss_index_sha256": digest(index_path),
    }
    (out / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"run complete; rows={len(all_rows)}; outcomes remain unverified", flush=True)


if __name__ == "__main__":
    main()
