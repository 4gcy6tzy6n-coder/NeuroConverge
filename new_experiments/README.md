# NeuroConverge prospective validation V1

**Authorization:** user selected “按方案推进并运行 M2/M5 实验” on 1 October 2026.

This package holds two distinct synthetic validation modules. Each module must have a frozen protocol, source/code hashes, paired-seed outputs, and independent arithmetic/integrity verification. The modules do not share an outcome or estimand. No combined effect, p-value, or pooled accuracy is defined.

## Module status

| Module | Scientific question | Protocol/status | Interpretation ceiling |
|---|---|---|---|
| M2 realized state vs action belief | Does an explicit execution-state observation improve a particular synthetic controller over action-conditioned inference under hidden reversals? | Two full canonical runs and both verifiers completed; deterministic scientific outputs match after declared timing exclusions. | Synthetic actuator-observability only. It is not the premotor RIM→AIY signal and cannot establish biological transfer or general AI benefit. |
| M5 correspondence-preserved timing | Does preserving trial-specific temporal information change the utility of a source-inspired local learning rule relative to broken correspondence and generic/reference controls? | Frozen run complete; task-viability gate and independent verifier passed. Post-run comparator-matching caveat is recorded in its amendment. | Synthetic algorithmic evidence only. It cannot establish measured cerebellar synaptic dynamics or biological-to-AI transfer. |

## Shared reporting rules

- Report each study's own endpoint, unit, paired contrast and uncertainty; never combine unlike endpoints.
- Keep every prescribed seed and arm in the record. Do not tune or rerun selectively after results.
- A task-viability failure makes downstream transfer contrasts inconclusive under that protocol.
- Report positive, negative, invalid and inconclusive outcomes using the frozen decision rules.
- Both V1 modules are complete and verified. The prospective experimental program is now closed; follow-up variants require a separate explicit scope decision.

## Verified results

- **M2:** In `HIDDEN_REVERSAL`, frozen primary contrast `ACRKN_ACTION_ONLY MSE − ACRKN_REALIZED_STATE MSE = −0.068094` (paired seed-block bootstrap 95% CI `[-0.141077, -0.003541]`, 32 blocks). Realized-state input did not help and was worse on average. The information-recovery contrast was inconclusive; generic GRU and task-aware particle-filter references outperformed AcRKN in all three conditions. Two full runs were scientifically byte-identical after excluding manifest-declared timing fields. See `M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/RUN_REPORT.md`.

M5 result: CF-timed local `nMAE_BROKEN − nMAE_ALIGNED = 0.116588` (95% seed-bootstrap CI `[0.115072, 0.118065]`, 30/30 seeds positive). The task gate passed. The same-feature generic ridge comparator showed a larger correspondence effect (`0.202390`), and the higher-memory exact replay reference was `0.189552`; the RBF comparison is not a strict parameter match (see M5 `POSTRUN_INTERPRETATION_AMENDMENT_01.md`). Thus this establishes a bounded synthetic correspondence effect for that local rule, not a biological-provenance advantage.

Each module folder contains its contract, runner/verifier, source manifest, complete seed-level output, summary, and execution record.
