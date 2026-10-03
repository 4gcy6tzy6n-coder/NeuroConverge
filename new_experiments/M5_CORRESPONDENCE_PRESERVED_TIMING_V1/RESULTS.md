# M5 correspondence-preserved timing test v1 — results

**Classification:** synthetic, post-hoc project extension executed under a prospective contract frozen before the first outcome run. This is not a preregistered or confirmatory biological experiment.

## Frozen decision

The task-viability gate passed. In the aligned regime, the exact-replay reference had mean normalized MAE (nMAE) `0.07138`, versus `0.25816` for the within-seed constant-median predictor, a `72.35%` relative improvement. Its paired correspondence effect, `nMAE_BROKEN − nMAE_ALIGNED`, was `+0.18955` with paired-seed bootstrap 95% interval `[+0.18691, +0.19223]`.

The prespecified CF primary decision was `CF_CORRESPONDENCE_EFFECT_SUPPORTED`. The source-inspired local rule had mean nMAE `0.14152` in `ALIGNED` and `0.25811` in `BROKEN`, giving a primary correspondence effect of `+0.11659` (95% interval `[+0.11507, +0.11807]`; positive in 30/30 independent task seeds).

## Comparator results

| Arm | Aligned mean nMAE | Broken mean nMAE | Broken − aligned | Paired-seed 95% interval | Positive seeds |
|---|---:|---:|---:|---:|---:|
| CF-timed local | 0.14152 | 0.25811 | +0.11659 | [+0.11507, +0.11807] | 30/30 |
| No trace | 0.25815 | 0.25808 | −0.00007 | [−0.00041, +0.00022] | 19/30 |
| CF-time shuffle | 0.25951 | 0.25831 | −0.00120 | [−0.00251, +0.00007] | 11/30 |
| Generic matched RBF | 0.05664 | 0.25903 | +0.20239 | [+0.20012, +0.20468] | 30/30 |
| Exact replay reference | 0.07138 | 0.26094 | +0.18955 | [+0.18691, +0.19223] | 30/30 |

The CF correspondence effect exceeded the no-trace effect by `0.11666` nMAE and the CF-time-shuffle effect by `0.11779`. Both temporal controls were approximately insensitive to the correspondence manipulation. However, the generic matched RBF effect exceeded the CF effect by `0.08580`, and the exact-replay effect exceeded it by `0.07296`.

The generic RBF is matched to the CF arm's 16-unit temporal encoder, but it is not strictly matched in trainable parameter count: it has one scalar regression head, whereas the CF arm has a 28-class softmax head. The frozen contract's phrase “parameter-matched” is therefore too strong; `POSTRUN_METHOD_AUDIT.md` preserves this correction without altering the contract or outcome.

## Interpretation

This frozen task establishes that trial-specific temporal information was usable and that the fixed CF-inspired local rule exploited it better than either omitting the temporal trace or shuffling teaching-time correspondence. The stronger generic controls exploited the same correspondence more effectively. The result therefore supports the project-level information-correspondence hypothesis in this M5 synthetic case while providing no evidence that biological provenance is required or privileged once the relevant temporal information is available.

The result is limited to the fixed task generator, seed set, temporal encoder, learning rules, and nMAE estimand. It does not validate CF-LTD in vivo, cerebellar mechanism claims, biological timing, cross-species transfer, general sequence learning, or general AI performance. M2 and M5 outcomes must remain separate matched contrasts and must not be pooled.

## Execution and audit notes

The first invocation failed before producing any outcome because Python 3.9 does not accept `zip(..., strict=True)`. The original freeze is retained; `EXECUTION_INCIDENT_01.md` and `PRE_RUN_FREEZE_AMENDMENT_01.json` document the syntax-only correction and revised code hash before the successful run.

NumPy 2.0.2 linked to Apple Accelerate emitted floating-point warnings during finite matrix multiplications. Post-run diagnostics showed all input and output arrays were finite, the matrix product agreed exactly with an independent `einsum` calculation for a reproduced seed, all recorded nMAEs lay in `[0.05331, 0.27499]`, and the independent result verifier passed. See `RUNTIME_NOTE.md`.
