# M2 realized-state versus action-conditioned belief: canonical run report

## Status

`PASS` for execution integrity and exact scientific reproducibility. The primary result does not support a realized-state advantage in the frozen task.

This experiment is a generic synthetic actuator-observability benchmark and an outcome-informed exploratory follow-up. It is not an M2 biological-transfer experiment. Its post-actuator execution measurement is not interchangeable with the premotor/corollary-discharge signal in the motivating biology.

## Frozen design and environment

- 32 paired training-seed blocks: `950000`–`950031`
- 5 learned arms, each trained for 160 optimizer updates with batch size 32 and sequence length 64
- 3 held-out conditions and 128 episodes per seed block, arm, and condition
- 1 task-aware particle-filter reference, evaluated at 64, 128, and 256 particles
- Python 3.9.6, NumPy 2.0.2, PyTorch 2.8.0, CPU, one thread, deterministic algorithms enabled
- AcRKN arms: 320 trainable parameters; GRU arms: 323 trainable parameters

## Primary and falsification results

The frozen primary contrast is `ACRKN_ACTION_ONLY MSE - ACRKN_REALIZED_STATE MSE` under `HIDDEN_REVERSAL`; positive values favor direct realized-state measurement.

| Contrast | Mean | Paired seed-block bootstrap 95% interval | Interpretation |
| --- | ---: | ---: | --- |
| Primary hidden-reversal contrast | -0.06809 | [-0.14108, -0.00354] | Realized-state input performed worse on average; no demonstrated benefit |
| Revealed reversal-event arm minus realized-state arm | 0.00199 | [-0.08968, 0.08165] | Information-recovery control approached the realized-state arm |
| Information-recovery contrast | -0.07009 | [-0.15282, 0.00371] | Does not establish an information-specific realized-state advantage |
| No-reversal action-only minus realized-state gap | -0.04191 | [-0.10135, 0.02193] | Compatible with zero, but the negative point estimate cautions about input-path/training imbalance |

Mean held-out tracking MSE (lower is better):

| Condition | AcRKN action only | AcRKN realized state | AcRKN reversal revealed | GRU action only | GRU realized state | Particle filter |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No reversal | 1.25770 | 1.29961 | 1.32200 | 0.84328 | 0.84643 | 0.66702 |
| Hidden reversal | 2.43809 | 2.50618 | 3.59910 | 1.86456 | 1.84687 | 1.44413 |
| Revealed reversal | 2.43809 | 2.50618 | 2.50817 | 1.86456 | 1.84687 | 1.38134 |

The generic GRU and task-aware particle-filter references outperform the AcRKN arms in all three conditions. The particle filter used disjoint validation streams to select `k_p=1.2` and `k_d=0.15`; mean MSE improved from 1.18785 at 64 particles to 1.16416 at 256 particles across conditions and blocks.

## Commands and runtime

Commands were run from `source/`:

```text
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/run_experiment.py --implementation-smoke --output ../runs/implementation_smoke.json
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/verify_results.py --smoke-report ../runs/implementation_smoke.json
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/run_experiment.py --output-dir ../runs/canonical_1
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/verify_results.py --results-dir ../runs/canonical_1
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/run_experiment.py --output-dir ../runs/canonical_2
python3 model/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/verify_results.py --results-dir ../runs/canonical_2
python3 ../compare_runs.py ../runs/canonical_1 ../runs/canonical_2 --output ../runs/reproducibility_comparison.json
```

- Canonical run 1: 748.60 s wall time (`manifest.duration_seconds=747.2342`)
- Canonical run 2: 742.92 s wall time (`manifest.duration_seconds=741.5449`)
- Both independent verifier runs: `PASS`
- Each run contains 160 fit rows, 73,728 episode rows, and 576 seed-summary rows

## Reproducibility result

The two complete runs have byte-identical deterministic files, including `summary.json`, all episode metrics, all seed summaries, stream identifiers, gain validation, and model diagnostics. After removing only the four timing fields declared by each run manifest, the fit, inference-timing, particle-diagnostic, and manifest records also match exactly. See `runs/reproducibility_comparison.json`.

## Provenance and limitations

The exact source snapshot is retained under `source/`; `SOURCE_PROVENANCE.json` records SHA-256 values. The NeuroMech source checkout remained unchanged by these runs. Its base HEAD was `3e5c458f15b2cad7aa6c5703b1827763e84343bb`, but the captured contract was modified and the experiment runner/verifier were untracked. Therefore the byte hashes, rather than the base commit alone, define this experiment version.

The result is bounded to one synthetic plant, an exact uncorrupted post-actuator sign signal, one training budget, and the specified architectures. No corruption/delay robustness test was run. The experiment does not show what RIM→AIY encodes, does not confirm biological-to-AI transfer, and does not support a general AI or NMI-readiness claim.
