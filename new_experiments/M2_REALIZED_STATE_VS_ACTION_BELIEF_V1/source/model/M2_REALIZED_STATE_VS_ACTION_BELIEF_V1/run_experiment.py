#!/usr/bin/env python3
"""Reusable causal AcRKN policy adapter and implementation-only smoke check.

The smoke command checks only the controller interface, tensor shapes,
gradients, determinism, and the frozen 321 +/- 2 trainable-parameter budget.
The canonical command runs the generic synthetic benchmark frozen in CONTRACT.md.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[2]
NAME = "M2_REALIZED_STATE_VS_ACTION_BELIEF_V1"
VENDOR_DIR = ROOT / "model" / "M2_ACTION_CONDITIONED_RKN_2D_PURSUIT_V1" / "vendor"
VENDOR_SOURCE = VENDOR_DIR / "acrkn_cell.py"
sys.path.insert(0, str(VENDOR_DIR))
from acrkn_cell import AcRKNCell  # noqa: E402

CONDITIONS = ("NO_REVERSAL", "HIDDEN_REVERSAL", "REVEALED_REVERSAL")
ACRKN_ARMS = ("ACRKN_ACTION_ONLY", "ACRKN_REALIZED_STATE", "ACRKN_REVERSAL_REVEALED")
GRU_ARMS = ("GRU_ACTION_ONLY", "GRU_REALIZED_STATE")
LEARNED_ARMS = ACRKN_ARMS + GRU_ARMS
ALL_ARMS = LEARNED_ARMS + ("TASK_AWARE_PARTICLE_FILTER",)
FULL_SEEDS = tuple(range(950000, 950032))
T = 64
TARGET_RHO, TARGET_SD, OBS_SD = 0.91, 0.055, 0.14
DROP_FRAC, DROP_BURST = 0.50, 8.0
ACTUATION_GAIN, TRAIN_MAX_REVERSE = 0.40, 0.25
BOOTSTRAPS, BOOTSTRAP_SEED = 20_000, 7_813_921
PF_COUNTS, PF_MAIN_COUNT = (64, 128, 256), 256
PF_KP, PF_KD = (0.45, 0.70, 0.95, 1.20), (0.00, 0.15, 0.30)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AcConfig:
    num_basis = 1
    bandwidth = 2
    trans_net_hidden_units: list[int] = []
    control_net_hidden_units = [26]
    trans_net_hidden_activation = "Tanh"
    control_net_hidden_activation = "Tanh"
    learn_trans_covar = True
    trans_covar = 0.1
    learn_initial_state_covar = True
    initial_state_covar = 1.0
    learning_rate = 0.003
    enc_out_norm = "none"
    clip_gradients = True
    never_invalid = False


class CausalAcRKNPolicy(nn.Module):
    """Causal observation-update, policy-readout, action-predict adapter.

    At time t the adapter encodes information available at or before t,
    updates the belief, selects action a_t, then uses the vendored AcRKN
    action-conditioned transition to predict the prior belief for t+1.

    The six feature meanings are frozen in CONTRACT.md. The adapter itself is
    feature-agnostic so it can be interface-tested without constructing
    semantically meaningful plant inputs.
    """

    input_dim = 6
    latent_observation_dim = 3
    action_dim = 1

    def __init__(self, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.cell = AcRKNCell(self.latent_observation_dim, self.action_dim, config=AcConfig())
        # A one-element softmax is identically one. Freeze these otherwise
        # mathematically inert weights instead of counting them as padding.
        for parameter in self.cell._coefficient_net.parameters():
            parameter.requires_grad_(False)
        self.observation_encoder = nn.Linear(self.input_dim, self.latent_observation_dim)
        self.log_observation_variance = nn.Parameter(torch.full((self.latent_observation_dim,), -0.7))
        self.policy_head = nn.Sequential(
            nn.Linear(2 * self.latent_observation_dim, 3), nn.Tanh(), nn.Linear(3, self.action_dim)
        )
        self.initial_mean = nn.Parameter(torch.zeros(2 * self.latent_observation_dim))
        self.initial_upper_raw = nn.Parameter(torch.zeros(self.latent_observation_dim))
        self.initial_lower_raw = nn.Parameter(torch.zeros(self.latent_observation_dim))
        self.initial_side_raw = nn.Parameter(torch.zeros(self.latent_observation_dim))

    def trainable_parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if parameter.requires_grad)

    def frozen_parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if not parameter.requires_grad)

    def initial_belief(self, batch_size: int):
        upper = torch.nn.functional.softplus(self.initial_upper_raw) + 1e-3
        lower = torch.nn.functional.softplus(self.initial_lower_raw) + 1e-3
        side = 0.5 * torch.tanh(self.initial_side_raw) * torch.sqrt(upper * lower)
        return self.initial_mean.expand(batch_size, -1), [
            upper.expand(batch_size, -1),
            lower.expand(batch_size, -1),
            side.expand(batch_size, -1),
        ]

    def step(self, features_t: torch.Tensor, prior_mean, prior_covariance):
        if features_t.ndim != 2 or features_t.shape[1] != self.input_dim:
            raise ValueError(
                f"features_t must have shape [batch, {self.input_dim}], got {tuple(features_t.shape)}"
            )
        encoded = self.observation_encoder(features_t)
        observation_variance = (
            torch.nn.functional.softplus(self.log_observation_variance) + 1e-4
        ).expand(features_t.shape[0], -1)
        valid = torch.ones((features_t.shape[0], 1), dtype=torch.bool, device=features_t.device)
        posterior_mean, posterior_covariance = self.cell._masked_update(
            prior_mean, prior_covariance, encoded, observation_variance, valid
        )
        action_t = torch.tanh(self.policy_head(posterior_mean)).squeeze(-1)
        next_prior_mean, next_prior_covariance = self.cell._predict(
            posterior_mean, posterior_covariance, action_t[:, None]
        )
        diagnostics = {
            "encoded_observation": encoded,
            "observation_variance": observation_variance,
            "posterior_mean": posterior_mean,
            "posterior_covariance": posterior_covariance,
        }
        return action_t, next_prior_mean, next_prior_covariance, diagnostics


def shapes(values) -> list[list[int]]:
    return [list(value.shape) for value in values]


def implementation_smoke() -> dict:
    """Exercise implementation invariants without simulating task outcomes."""
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    batch_size, sequence_length = 5, 4
    generator = torch.Generator().manual_seed(2_950_001)
    features = torch.randn(batch_size, sequence_length, 6, generator=generator)
    model = CausalAcRKNPolicy(seed=2_950_101)
    model.eval()
    count = model.trainable_parameter_count()
    if abs(count - 321) > 2:
        raise AssertionError(f"trainable count {count} violates 321 +/- 2")

    prior_mean, prior_covariance = model.initial_belief(batch_size)
    actions, diagnostic = [], None
    for step_index in range(sequence_length):
        action, prior_mean, prior_covariance, diagnostic = model.step(
            features[:, step_index], prior_mean, prior_covariance
        )
        actions.append(action)
    stacked_actions = torch.stack(actions, dim=1)
    assert diagnostic is not None
    loss = stacked_actions.square().mean() + prior_mean.square().mean() + sum(
        value.mean() for value in prior_covariance
    )
    loss.backward()
    missing_gradients = [
        name
        for name, parameter in model.named_parameters()
        if parameter.requires_grad and parameter.grad is None
    ]
    if missing_gradients:
        raise AssertionError(f"trainable parameters without a gradient path: {missing_gradients}")

    repeat_prior, repeat_covariance = model.initial_belief(batch_size)
    repeat_actions = []
    with torch.no_grad():
        for step_index in range(sequence_length):
            action, repeat_prior, repeat_covariance, _ = model.step(
                features[:, step_index], repeat_prior, repeat_covariance
            )
            repeat_actions.append(action)
    deterministic = torch.equal(stacked_actions.detach(), torch.stack(repeat_actions, dim=1))
    if not deterministic:
        raise AssertionError("eval-mode repeat was not deterministic")

    with torch.no_grad():
        positive_action_prior, _ = model.cell._predict(
            diagnostic["posterior_mean"],
            diagnostic["posterior_covariance"],
            torch.full((batch_size, 1), 0.5),
        )
        negative_action_prior, _ = model.cell._predict(
            diagnostic["posterior_mean"],
            diagnostic["posterior_covariance"],
            torch.full((batch_size, 1), -0.5),
        )
    action_transition_sensitive = not torch.equal(positive_action_prior, negative_action_prior)
    if not action_transition_sensitive:
        raise AssertionError("vendored transition did not respond to the action input")

    records = [
        {
            "name": name,
            "shape": list(parameter.shape),
            "count": parameter.numel(),
            "gradient_finite": bool(torch.isfinite(parameter.grad).all()),
        }
        for name, parameter in model.named_parameters()
        if parameter.requires_grad
    ]
    return {
        "status": "PASS",
        "classification": "IMPLEMENTATION_ONLY_NO_TASK_OUTCOMES",
        "smoke_input_semantics": "RANDOM_INTERFACE_TENSORS_NOT_EXPERIMENT_FEATURES",
        "adapter": "CausalAcRKNPolicy",
        "causal_order": [
            "encode_features_t",
            "posterior_update_t",
            "select_action_t",
            "action_conditioned_predict_t_plus_1",
        ],
        "batch_size": batch_size,
        "sequence_length": sequence_length,
        "input_shape": list(features.shape),
        "action_shape": list(stacked_actions.shape),
        "final_prior_mean_shape": list(prior_mean.shape),
        "final_prior_covariance_shapes": shapes(prior_covariance),
        "encoded_observation_shape": list(diagnostic["encoded_observation"].shape),
        "observation_variance_shape": list(diagnostic["observation_variance"].shape),
        "posterior_mean_shape": list(diagnostic["posterior_mean"].shape),
        "posterior_covariance_shapes": shapes(diagnostic["posterior_covariance"]),
        "trainable_parameter_count": count,
        "target_parameter_count": 321,
        "parameter_tolerance": 2,
        "frozen_parameter_count": model.frozen_parameter_count(),
        "trainable_parameters": records,
        "all_trainable_gradients_finite": all(record["gradient_finite"] for record in records),
        "deterministic_eval_repeat": deterministic,
        "action_transition_sensitive": action_transition_sensitive,
        "runner_sha256": sha256(Path(__file__)),
        "vendored_acrkn_sha256": sha256(VENDOR_SOURCE),
        "signal_semantics_status": "FROZEN_IN_CONTRACT",
    }


@dataclass(frozen=True)
class RunConfig:
    seeds: tuple[int, ...]
    updates: int
    batch_size: int
    test_episodes: int
    mode: str


class GRUPolicy(nn.Module):
    """Exactly matched generic recurrent control pair."""

    def __init__(self, seed: int):
        super().__init__()
        torch.manual_seed(seed)
        self.cell = nn.GRUCell(6, 7)
        self.policy_head = nn.Linear(7, 1)

    def initial_state(self, batch_size: int):
        return torch.zeros(batch_size, 7)

    def step(self, features_t: torch.Tensor, hidden: torch.Tensor):
        hidden = self.cell(features_t, hidden)
        return torch.tanh(self.policy_head(hidden)).squeeze(-1), hidden

    def trainable_parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if parameter.requires_grad)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"empty table: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_streams(seed: int, n: int, reversal_probability: float | None) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    target = np.zeros((n, T), np.float32)
    target[:, 0] = rng.uniform(-1.0, 1.0, n)
    target_velocity = rng.normal(0.0, TARGET_SD, n).astype(np.float32)
    for step_index in range(1, T):
        target_velocity = TARGET_RHO * target_velocity + rng.normal(0.0, TARGET_SD, n)
        target[:, step_index] = target[:, step_index - 1] + target_velocity
    observation_noise = rng.normal(0.0, OBS_SD, (n, T)).astype(np.float32)
    if reversal_probability is None:
        probabilities = rng.uniform(0.0, TRAIN_MAX_REVERSE, n).astype(np.float32)
    else:
        probabilities = np.full(n, reversal_probability, np.float32)
    reversals = rng.random((n, T)) < probabilities[:, None]
    available = np.ones((n, T), bool)
    probability_leave = 1.0 / DROP_BURST
    probability_enter = DROP_FRAC / (1.0 - DROP_FRAC) * probability_leave
    missing = rng.random(n) < DROP_FRAC
    for step_index in range(T):
        if step_index:
            draw = rng.random(n)
            missing = np.where(missing, draw >= probability_leave, draw < probability_enter)
        available[:, step_index] = ~missing
    return {
        "target": target,
        "observation_noise": observation_noise,
        "reversal_probability": probabilities,
        "reversals": reversals,
        "available": available,
    }


def modality(arm: str) -> str:
    if arm.endswith("REALIZED_STATE"):
        return "REALIZED_STATE"
    if arm == "ACRKN_REVERSAL_REVEALED":
        return "REVERSAL_EVENT"
    return "ACTION_ONLY"


def learned_rollout(
    model: CausalAcRKNPolicy | GRUPolicy,
    arm: str,
    streams: dict[str, np.ndarray],
    reveal_reversal: bool,
    require_grad: bool,
) -> dict[str, torch.Tensor]:
    target = torch.from_numpy(streams["target"])
    noise = torch.from_numpy(streams["observation_noise"])
    available = torch.from_numpy(streams["available"])
    reversals = torch.from_numpy(streams["reversals"])
    n = target.shape[0]
    position = torch.zeros(n)
    previous_command = torch.zeros(n)
    previous_realized_sign = torch.zeros(n)
    previous_reversal_code = torch.zeros(n)
    auxiliary_available = torch.zeros(n, dtype=torch.bool)
    visual_gap = torch.zeros(n)
    if isinstance(model, CausalAcRKNPolicy):
        state = model.initial_belief(n)
    else:
        state = model.initial_state(n)
    squared_errors, command_energies = [], []
    observation_variances, posterior_variances = [], []
    mode = modality(arm)
    context = torch.enable_grad() if require_grad else torch.no_grad()
    with context:
        for step_index in range(T):
            relative = target[:, step_index] - position
            observation = torch.where(
                available[:, step_index], relative + noise[:, step_index], torch.zeros_like(relative)
            )
            visual_gap = torch.where(
                available[:, step_index],
                torch.zeros_like(visual_gap),
                torch.clamp(visual_gap + 1.0 / 16.0, max=1.0),
            )
            if mode == "REALIZED_STATE":
                auxiliary, auxiliary_valid = previous_realized_sign, auxiliary_available
            elif mode == "REVERSAL_EVENT" and reveal_reversal:
                auxiliary, auxiliary_valid = previous_reversal_code, auxiliary_available
            else:
                auxiliary = torch.zeros_like(previous_command)
                auxiliary_valid = torch.zeros_like(auxiliary_available)
            features = torch.stack(
                (
                    observation,
                    available[:, step_index].float(),
                    auxiliary,
                    auxiliary_valid.float(),
                    previous_command,
                    visual_gap,
                ),
                dim=-1,
            )
            if isinstance(model, CausalAcRKNPolicy):
                command, next_mean, next_covariance, diagnostics = model.step(features, *state)
                state = (next_mean, next_covariance)
                observation_variances.append(diagnostics["observation_variance"].mean(dim=1))
                posterior_variances.append(
                    (diagnostics["posterior_covariance"][0] + diagnostics["posterior_covariance"][1]).mean(dim=1)
                )
            else:
                command, state = model.step(features, state)
            squared_errors.append(relative.square())
            command_energies.append(command.square())
            execution_sign = torch.where(
                reversals[:, step_index], -torch.ones_like(command), torch.ones_like(command)
            )
            displacement = ACTUATION_GAIN * command * execution_sign
            position = position + displacement
            previous_realized_sign = torch.sign(displacement).detach()
            previous_reversal_code = torch.where(
                reversals[:, step_index], torch.ones_like(command), -torch.ones_like(command)
            )
            auxiliary_available = torch.ones_like(auxiliary_available)
            previous_command = command
    result = {
        "tracking_mse": torch.stack(squared_errors, dim=1).mean(dim=1),
        "command_energy": torch.stack(command_energies, dim=1).mean(dim=1),
        "missing_fraction": 1.0 - available.float().mean(dim=1),
    }
    if observation_variances:
        result["observation_variance"] = torch.stack(observation_variances, dim=1).mean(dim=1)
        result["posterior_variance"] = torch.stack(posterior_variances, dim=1).mean(dim=1)
    return result


def build_model(arm: str, training_seed: int):
    family_seed = training_seed + (41_001 if arm.startswith("ACRKN") else 42_001)
    return CausalAcRKNPolicy(family_seed) if arm.startswith("ACRKN") else GRUPolicy(family_seed)


def train_one(arm: str, training_seed: int, config: RunConfig):
    model = build_model(arm, training_seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    losses = []
    start = time.perf_counter()
    for update_index in range(config.updates):
        stream_seed = training_seed + 8_000_000 + update_index * 7_919
        streams = make_streams(stream_seed, config.batch_size, reversal_probability=None)
        model.train()
        result = learned_rollout(
            model,
            arm,
            streams,
            reveal_reversal=(arm == "ACRKN_REVERSAL_REVEALED"),
            require_grad=True,
        )
        loss = result["tracking_mse"].mean()
        if not torch.isfinite(loss):
            raise FloatingPointError(f"non-finite training loss for {arm}, seed {training_seed}, update {update_index}")
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()
        losses.append(float(loss.detach()))
    model.eval()
    return model, {
        "training_seed": training_seed,
        "arm": arm,
        "parameter_count": model.trainable_parameter_count(),
        "updates": config.updates,
        "batch_size": config.batch_size,
        "sequence_length": T,
        "training_tokens": config.updates * config.batch_size * T,
        "learning_rate": 0.003,
        "initial_training_loss": float(np.mean(losses[: min(10, len(losses))])),
        "final_training_loss": float(np.mean(losses[-min(10, len(losses)) :])),
        "training_seconds": time.perf_counter() - start,
        "parameters_json": json.dumps(
            [
                float(value)
                for parameter in model.parameters()
                if parameter.requires_grad
                for value in parameter.detach().reshape(-1)
            ],
            separators=(",", ":"),
        ),
    }


def systematic_resample(weights: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    locations = (rng.random() + np.arange(len(weights))) / len(weights)
    return np.searchsorted(np.cumsum(weights), locations, side="right")


def particle_filter_rollout(
    streams: dict[str, np.ndarray],
    condition: str,
    particle_count: int,
    kp: float,
    kd: float,
    seed: int,
) -> tuple[dict[str, np.ndarray], dict[str, float]]:
    rng = np.random.default_rng(seed)
    target = streams["target"]
    noise = streams["observation_noise"]
    available = streams["available"]
    actual_reversals = streams["reversals"]
    probabilities = streams["reversal_probability"]
    n = len(target)
    target_particles = rng.uniform(-1.0, 1.0, (n, particle_count))
    target_velocity_particles = rng.normal(0.0, TARGET_SD, (n, particle_count))
    agent_particles = np.zeros((n, particle_count))
    agent_velocity_particles = np.zeros((n, particle_count))
    weights = np.full((n, particle_count), 1.0 / particle_count)
    actual_agent_position = np.zeros(n)
    previous_command = np.zeros(n)
    squared_errors, command_energies = np.empty((n, T)), np.empty((n, T))
    ess_total, ess_count, resamples = 0.0, 0, 0
    start = time.perf_counter()
    for step_index in range(T):
        if step_index:
            target_velocity_particles = TARGET_RHO * target_velocity_particles + rng.normal(
                0.0, TARGET_SD, (n, particle_count)
            )
            target_particles += target_velocity_particles
            if condition == "REVEALED_REVERSAL":
                particle_reversals = np.broadcast_to(
                    actual_reversals[:, step_index - 1, None], (n, particle_count)
                )
            else:
                particle_reversals = rng.random((n, particle_count)) < probabilities[:, None]
            execution_sign = np.where(particle_reversals, -1.0, 1.0)
            agent_velocity_particles = ACTUATION_GAIN * previous_command[:, None] * execution_sign
            agent_particles += agent_velocity_particles
        relative = target[:, step_index] - actual_agent_position
        observation = relative + noise[:, step_index]
        for episode_index in np.flatnonzero(available[:, step_index]):
            predicted = target_particles[episode_index] - agent_particles[episode_index]
            log_likelihood = -0.5 * ((observation[episode_index] - predicted) / OBS_SD) ** 2
            log_likelihood -= np.max(log_likelihood)
            updated = weights[episode_index] * np.exp(log_likelihood)
            total = updated.sum()
            weights[episode_index] = updated / total if total > 0 else 1.0 / particle_count
        effective_size = 1.0 / np.square(weights).sum(axis=1)
        ess_total += float(effective_size.sum())
        ess_count += n
        for episode_index in np.flatnonzero(effective_size < particle_count / 2):
            indices = systematic_resample(weights[episode_index], rng)
            target_particles[episode_index] = target_particles[episode_index, indices]
            target_velocity_particles[episode_index] = target_velocity_particles[episode_index, indices]
            agent_particles[episode_index] = agent_particles[episode_index, indices]
            agent_velocity_particles[episode_index] = agent_velocity_particles[episode_index, indices]
            weights[episode_index].fill(1.0 / particle_count)
            resamples += 1
        estimated_error = np.sum(weights * (target_particles - agent_particles), axis=1)
        estimated_agent_velocity = np.sum(weights * agent_velocity_particles, axis=1)
        command = np.tanh(kp * estimated_error - kd * estimated_agent_velocity)
        squared_errors[:, step_index] = relative**2
        command_energies[:, step_index] = command**2
        actual_sign = np.where(actual_reversals[:, step_index], -1.0, 1.0)
        actual_agent_position += ACTUATION_GAIN * command * actual_sign
        previous_command = command
    return {
        "tracking_mse": squared_errors.mean(axis=1),
        "command_energy": command_energies.mean(axis=1),
        "missing_fraction": 1.0 - available.mean(axis=1),
    }, {
        "mean_ess": ess_total / ess_count,
        "mean_ess_fraction": ess_total / ess_count / particle_count,
        "resample_fraction": resamples / (n * T),
        "inference_seconds": time.perf_counter() - start,
    }


def select_particle_gains(config: RunConfig):
    validation_seeds = (850_001, 850_002, 850_003, 850_004)
    validation_n = 32
    rows = []
    for kp in PF_KP:
        for kd in PF_KD:
            outcomes = []
            for seed in validation_seeds:
                streams = make_streams(seed, validation_n, 0.25)
                metrics, _ = particle_filter_rollout(
                    streams, "HIDDEN_REVERSAL", 64, kp, kd, seed + 50_000
                )
                outcomes.extend(metrics["tracking_mse"].tolist())
            rows.append(
                {
                    "kp": kp,
                    "kd": kd,
                    "validation_seed_count": len(validation_seeds),
                    "validation_episode_count": len(outcomes),
                    "mean_tracking_mse": float(np.mean(outcomes)),
                }
            )
    selected_index = min(
        range(len(rows)), key=lambda index: (rows[index]["mean_tracking_mse"], rows[index]["kp"], rows[index]["kd"])
    )
    for index, row in enumerate(rows):
        row["selected"] = index == selected_index
    selected = rows[selected_index]
    return float(selected["kp"]), float(selected["kd"]), rows


def bootstrap(values: list[float]) -> dict:
    array = np.asarray(values, float)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    samples = array[rng.integers(0, len(array), (BOOTSTRAPS, len(array)))].mean(axis=1)
    return {
        "mean": float(array.mean()),
        "ci95_low": float(np.quantile(samples, 0.025)),
        "ci95_high": float(np.quantile(samples, 0.975)),
        "n_seed_blocks": len(array),
    }


def evaluation_seed(seed_block: int, condition: str) -> int:
    return 31_000_000 + seed_block * 10_000 + (0 if condition == "NO_REVERSAL" else 1_000)


def run_experiment(output_dir: Path, config: RunConfig) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if abs(CausalAcRKNPolicy(0).trainable_parameter_count() - 321) > 2:
        raise AssertionError("AcRKN budget failure")
    if GRUPolicy(0).trainable_parameter_count() != GRUPolicy(1).trainable_parameter_count():
        raise AssertionError("GRU matching failure")
    selected_kp, selected_kd, gain_rows = select_particle_gains(config)
    fits, episodes, streams_table = [], [], []
    particle_rows, timing_rows, model_rows = [], [], []
    run_start = time.time()
    for seed_block, training_seed in enumerate(config.seeds):
        print(f"training seed block {seed_block + 1}/{len(config.seeds)}", flush=True)
        models = {}
        for arm in LEARNED_ARMS:
            models[arm], fit = train_one(arm, training_seed, config)
            fits.append(fit)
        if len({models[arm].trainable_parameter_count() for arm in ACRKN_ARMS}) != 1:
            raise AssertionError("AcRKN arm counts differ")
        if len({models[arm].trainable_parameter_count() for arm in GRU_ARMS}) != 1:
            raise AssertionError("GRU arm counts differ")
        for condition in CONDITIONS:
            eval_seed = evaluation_seed(seed_block, condition)
            probability = 0.0 if condition == "NO_REVERSAL" else 0.25
            streams = make_streams(eval_seed, config.test_episodes, probability)
            streams_table.append(
                {
                    "seed_block": seed_block,
                    "training_seed": training_seed,
                    "condition": condition,
                    "evaluation_seed": eval_seed,
                    "paired_stream_group": f"block-{seed_block}-{'p0' if probability == 0 else 'p025'}",
                    "reversal_probability": probability,
                    "episodes": config.test_episodes,
                }
            )
            metrics_by_arm = {}
            for arm in LEARNED_ARMS:
                start = time.perf_counter()
                result = learned_rollout(
                    models[arm],
                    arm,
                    streams,
                    reveal_reversal=(condition != "HIDDEN_REVERSAL"),
                    require_grad=False,
                )
                elapsed = time.perf_counter() - start
                metrics_by_arm[arm] = {key: value.detach().numpy() for key, value in result.items()}
                timing_rows.append(
                    {
                        "seed_block": seed_block,
                        "condition": condition,
                        "arm": arm,
                        "episodes": config.test_episodes,
                        "inference_seconds": elapsed,
                    }
                )
                if arm in ACRKN_ARMS:
                    model_rows.append(
                        {
                            "seed_block": seed_block,
                            "condition": condition,
                            "arm": arm,
                            "mean_observation_variance": float(np.mean(metrics_by_arm[arm]["observation_variance"])),
                            "mean_posterior_variance": float(np.mean(metrics_by_arm[arm]["posterior_variance"])),
                        }
                    )
            for particle_count in PF_COUNTS:
                metrics, diagnostics = particle_filter_rollout(
                    streams,
                    condition,
                    particle_count,
                    selected_kp,
                    selected_kd,
                    eval_seed + particle_count * 101,
                )
                particle_rows.append(
                    {
                        "seed_block": seed_block,
                        "condition": condition,
                        "evaluation_seed": eval_seed,
                        "particle_count": particle_count,
                        "kp": selected_kp,
                        "kd": selected_kd,
                        "mean_tracking_mse": float(np.mean(metrics["tracking_mse"])),
                        **diagnostics,
                    }
                )
                if particle_count == PF_MAIN_COUNT:
                    metrics_by_arm["TASK_AWARE_PARTICLE_FILTER"] = metrics
                    timing_rows.append(
                        {
                            "seed_block": seed_block,
                            "condition": condition,
                            "arm": "TASK_AWARE_PARTICLE_FILTER",
                            "episodes": config.test_episodes,
                            "inference_seconds": diagnostics["inference_seconds"],
                        }
                    )
            for arm, metrics in metrics_by_arm.items():
                for episode_index in range(config.test_episodes):
                    episodes.append(
                        {
                            "seed_block": seed_block,
                            "training_seed": training_seed,
                            "condition": condition,
                            "evaluation_seed": eval_seed,
                            "episode_id": episode_index,
                            "arm": arm,
                            "tracking_mse": float(metrics["tracking_mse"][episode_index]),
                            "command_energy": float(metrics["command_energy"][episode_index]),
                            "missing_fraction": float(metrics["missing_fraction"][episode_index]),
                        }
                    )
        print(f"finished seed block {seed_block + 1}/{len(config.seeds)}", flush=True)

    seed_summaries = []
    for seed_block in range(len(config.seeds)):
        for condition in CONDITIONS:
            for arm in ALL_ARMS:
                rows = [
                    row
                    for row in episodes
                    if row["seed_block"] == seed_block and row["condition"] == condition and row["arm"] == arm
                ]
                seed_summaries.append(
                    {
                        "seed_block": seed_block,
                        "condition": condition,
                        "arm": arm,
                        "n_episodes": len(rows),
                        "tracking_mse": float(np.mean([row["tracking_mse"] for row in rows])),
                        "command_energy": float(np.mean([row["command_energy"] for row in rows])),
                        "missing_fraction": float(np.mean([row["missing_fraction"] for row in rows])),
                    }
                )

    def mean(block: int, condition: str, arm: str) -> float:
        return float(
            next(
                row["tracking_mse"]
                for row in seed_summaries
                if row["seed_block"] == block and row["condition"] == condition and row["arm"] == arm
            )
        )

    primary = [
        mean(block, "HIDDEN_REVERSAL", "ACRKN_ACTION_ONLY")
        - mean(block, "HIDDEN_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(len(config.seeds))
    ]
    revealed_gap = [
        mean(block, "REVEALED_REVERSAL", "ACRKN_REVERSAL_REVEALED")
        - mean(block, "REVEALED_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(len(config.seeds))
    ]
    recovery = [primary[index] - revealed_gap[index] for index in range(len(config.seeds))]
    no_reversal_gap = [
        mean(block, "NO_REVERSAL", "ACRKN_ACTION_ONLY")
        - mean(block, "NO_REVERSAL", "ACRKN_REALIZED_STATE")
        for block in range(len(config.seeds))
    ]
    summary = {
        "experiment": NAME,
        "classification": "generic synthetic actuator-observability benchmark; not biological transfer",
        "mode": config.mode,
        "training_seed_blocks": len(config.seeds),
        "primary_estimand": "ACRKN_ACTION_ONLY MSE - ACRKN_REALIZED_STATE MSE in HIDDEN_REVERSAL",
        "primary_seed_block_values": primary,
        "primary_summary": bootstrap(primary),
        "revealed_gap_seed_block_values": revealed_gap,
        "revealed_gap_summary": bootstrap(revealed_gap),
        "information_recovery_seed_block_values": recovery,
        "information_recovery_summary": bootstrap(recovery),
        "no_reversal_gap_seed_block_values": no_reversal_gap,
        "no_reversal_gap_summary": bootstrap(no_reversal_gap),
        "mean_mse_by_condition_arm": {
            condition: {
                arm: float(
                    np.mean(
                        [row["tracking_mse"] for row in seed_summaries if row["condition"] == condition and row["arm"] == arm]
                    )
                )
                for arm in ALL_ARMS
            }
            for condition in CONDITIONS
        },
        "acrkn_parameter_count": CausalAcRKNPolicy(0).trainable_parameter_count(),
        "gru_parameter_count": GRUPolicy(0).trainable_parameter_count(),
        "particle_filter": {
            "selected_kp": selected_kp,
            "selected_kd": selected_kd,
            "main_particle_count": PF_MAIN_COUNT,
            "convergence_particle_counts": list(PF_COUNTS),
            "validation_streams_disjoint": True,
        },
        "claim_boundary": "post-actuator observability in one synthetic plant; no biological or general-AI claim",
    }
    tables = {
        "fit_manifest.csv": fits,
        "episode_metrics.csv": episodes,
        "seed_summary.csv": seed_summaries,
        "stream_registry.csv": streams_table,
        "particle_gain_validation.csv": gain_rows,
        "particle_diagnostics.csv": particle_rows,
        "inference_timing.csv": timing_rows,
        "model_diagnostics.csv": model_rows,
    }
    for filename, rows in tables.items():
        write_csv(output_dir / filename, rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    output_names = tuple(tables) + ("summary.json",)
    manifest = {
        "experiment": NAME,
        "classification": summary["classification"],
        "mode": config.mode,
        "contract_sha256": sha256(ROOT / "summery" / NAME / "CONTRACT.md"),
        "runner_sha256": sha256(Path(__file__)),
        "verifier_sha256": sha256(ROOT / "model" / NAME / "verify_results.py"),
        "vendored_acrkn_sha256": sha256(VENDOR_SOURCE),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "device": "CPU",
        "threads": 1,
        "training_seeds": list(config.seeds),
        "updates": config.updates,
        "batch_size": config.batch_size,
        "sequence_length": T,
        "test_episodes_per_block_arm_condition": config.test_episodes,
        "conditions": list(CONDITIONS),
        "arms": list(ALL_ARMS),
        "duration_seconds": time.time() - run_start,
        "nondeterministic_fields": [
            "manifest.duration_seconds",
            "fit_manifest.training_seconds",
            "inference_timing.inference_seconds",
            "particle_diagnostics.inference_seconds",
        ],
        "outputs": {
            filename: {
                "bytes": (output_dir / filename).stat().st_size,
                "sha256": sha256(output_dir / filename),
            }
            for filename in output_names
        },
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": "COMPLETE", "output_dir": str(output_dir), "primary": summary["primary_summary"]}, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--quick-check", action="store_true")
    args = parser.parse_args()
    if args.implementation_smoke:
        rendered = json.dumps(implementation_smoke(), indent=2) + "\n"
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return
    if args.output is not None:
        parser.error("--output applies only to --implementation-smoke")
    config = (
        RunConfig((1_960_000, 1_960_001), 3, 4, 8, "QUICK_IMPLEMENTATION_CHECK")
        if args.quick_check
        else RunConfig(FULL_SEEDS, 160, 32, 128, "FULL_CANONICAL")
    )
    default = ROOT / "data" / "results" / NAME / ("quick_check" if args.quick_check else "canonical")
    run_experiment(args.output_dir or default, config)


if __name__ == "__main__":
    main()
