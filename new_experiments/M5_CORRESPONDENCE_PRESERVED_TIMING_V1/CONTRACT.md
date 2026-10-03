# M5 correspondence-preserved timing test v1

**Status:** `POST_HOC_PROJECT_EXTENSION__PROSPECTIVE_CONTRACT_FROZEN_BEFORE_FIRST_OUTCOME_RUN`

## Scientific question

When trial-specific temporal input carries the target interval, does preserving that input–target correspondence change the performance of a fixed, source-inspired CF-timed local learning rule? The matched counterfactual preserves the complete input and target marginals but shuffles their trial-level relationship.

This is a synthetic artificial-learning experiment proposed after inspecting earlier M5 results. It is neither preregistered nor confirmatory. It does not test a biological cerebellum, measured climbing-fibre activity, measured LTD, or a biological causal mechanism.

## Frozen task

- Thirty independent task seeds: integers 51000–51029.
- Each seed has 1,200 training and 400 held-out trials.
- A trial has 40 time bins and a target interval in integer bins 6–33 inclusive.
- The scalar temporal input is a Gaussian pulse whose centre is the target interval plus Gaussian timing noise (SD 1.5 bins), with additive observation noise (SD 0.20). Pulse width is 2.25 bins.
- `ALIGNED` uses each temporal input with its generating target interval.
- `BROKEN` applies a deterministic within-split permutation to the target intervals. The input arrays and the target multiset are therefore exactly identical to `ALIGNED`; only trial-level correspondence changes. Training and test targets are shuffled independently. A cyclic fallback prevents an identity permutation if necessary.
- Train and test trials are independently generated within each seed.
- No task parameter, model parameter, seed, arm, or decision threshold may change after outcome inspection.

## Frozen arms

All arms predict the target interval. All are evaluated on the same held-out trials within seed and regime.

1. `CF_TIMED_LOCAL`: a fixed 16-unit temporal RBF eligibility encoder followed by a 28-way linear softmax readout. One online pass applies a local three-factor delta update when the trial's CF-like teaching event supplies the target-time error. The encoder and update rule are fixed across regimes. This is source-inspired terminology for an artificial eligibility-gated rule, not a literal LTD model.
2. `NO_TRACE`: the same online softmax update and 28-way output, using only the final-bin input, trial mean, and a bias term. It does not retain the temporal eligibility profile.
3. `CF_TIME_SHUFFLE`: identical to `CF_TIMED_LOCAL`, except a fixed within-training-set permutation assigns CF teaching times to eligibility vectors. Evaluation uses the actual regime targets. This destroys teaching-time correspondence without changing eligibility or target marginals.
4. `GENERIC_MATCHED_RBF`: batch ridge regression on exactly the same 16 temporal RBF eligibility features plus bias used by `CF_TIMED_LOCAL`. It is the parameter-matched generic comparator; ridge coefficient is fixed at 0.01.
5. `EXACT_REPLAY_REFERENCE`: batch ridge regression on the complete 40-bin temporal input plus bias. It is a higher-memory/reference comparator and is not capacity matched.

Fixed online learning rate is 0.08. Online weights start at zero. Trial order is generated once per seed and is shared across paired regimes and online arms. No epochs, hyperparameters, or model variants are selected from results.

## Outcome, independent unit, and estimands

- Sole performance outcome: normalized mean absolute error (`nMAE`), equal to interval MAE divided by 27 bins. Lower is better.
- Independent unit: task seed. Trials, regimes, and arms are paired repeated observations, not independent units.
- Primary M5 estimand: for `CF_TIMED_LOCAL`, seed-level `nMAE_BROKEN − nMAE_ALIGNED`, averaged over the 30 seeds. Positive values mean preserved correspondence improved performance.
- The same paired correspondence effect is reported for every comparator. Effects are never pooled with M2 or with a different outcome metric.
- Uncertainty: a deterministic 20,000-draw paired seed bootstrap, resampling the 30 seed-level contrasts. Percentile 95% intervals are reported.
- Descriptive specificity contrasts compare the CF correspondence effect with the corresponding effects for `NO_TRACE`, `CF_TIME_SHUFFLE`, `GENERIC_MATCHED_RBF`, and `EXACT_REPLAY_REFERENCE`. They do not redefine the primary estimand.

## Task-viability gate

The timing task is viable only if both conditions hold:

1. In `ALIGNED`, `EXACT_REPLAY_REFERENCE` improves mean nMAE by at least 25% relative to the within-seed constant-median predictor.
2. The 95% paired-seed bootstrap interval for the exact-replay correspondence effect is entirely above zero.

If either condition fails, all mechanism-facing contrasts are recorded but classified `TASK_GATE_FAILED__NO_MECHANISTIC_INTERPRETATION`.

## Frozen decisions and falsification

Subject to the task-viability gate:

- `CF_CORRESPONDENCE_EFFECT_SUPPORTED` only if the CF primary 95% interval is entirely above zero.
- `CF_CORRESPONDENCE_EFFECT_NOT_DETECTED` if that interval includes zero.
- `CF_CORRESPONDENCE_EFFECT_REVERSED` if that interval is entirely below zero.
- No mechanism-specific privilege is claimed merely because the CF interval is positive. If matched RBF or exact replay has a comparable or larger effect, correspondence is useful but biological provenance is unnecessary for exploiting it in this task.
- A nonpositive CF effect falsifies the narrow hypothesis that this frozen local rule benefits from preserved correspondence in this frozen task. It does not falsify biological CF-LTD.

## Stop rule and interpretation ceiling

Run this frozen contract once. Do not tune, rescue, replace arms, remove seeds, or change the viability gate after observing results. Any future follow-up must receive a new identifier and be explicitly outcome informed.

Every result is limited to this synthetic task, fixed generator, fixed model implementations, and fixed seed set. No result constitutes biological validation, evidence for cerebellar LTD in vivo, cross-species generality, or general AI superiority.
