# Audit of the proposed NeuroConverge completion plan

**Audit date:** 2026-10-01. Initial audit of the pasted plan; subsequent user authorization and V1 results are recorded in the final section below.

## Claims that conflict with observed state

| Proposed statement | Audit finding | Evidence / consequence |
|---|---|---|
| NeuroConverge exists but is still empty (`size=0`). | False as of the current audit. Its remote `main` was populated and verified at `b55871dec1207b2c9e8b63270ebcc7871f0feaca`, with tree `ab23be556af6016552ba8b6fa9ed8c38f59616cc`. | `PROJECT_FREEZE.md`; remote push verification recorded in the project history. The pasted statement may describe an earlier time, but it is stale now. |
| Freeze NeuroMotif at `1adc07f` and NeuroMech at `3e5c458`; thereafter cite only those snapshots. | These refs are candidates, not a complete freeze. NeuroMech `experiment-publication` was observed with two local changes; local Route-D `main` includes 387 changed/untracked paths and the V3 portfolio matrix. The publication branch omits exact records used by the initial draft. | `PROJECT_FREEZE.md`, `SOURCE_REPOSITORY_MANIFEST.json`, `PAPER_CRITICAL_SOURCE_SNAPSHOT.json`, and `PUBLICATION_BRANCH_CROSSWALK.csv`. Freezing only `3e5c458` would omit the broader current portfolio and cannot support claims drawn from local Route-D files. |
| The M2 realized-state discriminator is the last decisive biological transfer test. | The contract explicitly labels it an outcome-informed generic synthetic actuator-observability benchmark, not an M2 biological-transfer experiment. Its realized execution signal is not the premotor/corollary-discharge construct in the cited worm biology. | Captured contract: `new_experiments/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/source/summery/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/CONTRACT.md`. It can test a bounded information-estimation question, but a positive or negative result cannot by itself close biological-to-AI transfer. No `RESULTS` file was present in that package at audit. |
| One M5 correspondence experiment would give M2 and M5 a shared project-level estimand. | The proposed within-task aligned-versus-broken contrasts could be useful, but M2 and M5 retain different tasks, outcomes, units, and mechanisms. A shared design principle does not make their numeric effects exchangeable. | Report task-specific contrasts separately; do not pool MSE and timing/accuracy endpoints. No frozen M5 contract or results were provided in the pasted plan. |
| Experimental corpus is 90–95% complete, readiness 50–60%, manuscript 30–40%, etc. | These percentages have no stated denominator, rubric, or auditable scoring source. | Treat as subjective project-management impressions, not verified progress metrics. Use an explicit checklist with completed/partial/missing states instead. |
| NMI Article is a close fit because the work is substantial and multidisciplinary. | Scope fit is not equivalent to editorial contribution or readiness. The current authoritative project contribution and venue audit says Article/Analysis are not admitted or ready; novelty and broad significance remain unresolved. | Do not infer submission competitiveness from work volume or display-item limits. Keep “NMI target” separate from “NMI-ready.” |

## Recommendations that remain reasonable as hypotheses

- A prospective, frozen test of source-to-model information correspondence could strengthen the story if its biological construct, source mapping, controls, task viability, and independent unit are coherent.
- The existing M2 action-belief contract is a potentially useful narrow synthetic discriminator, with its current limits stated above.
- A corresponding M5 test should preserve trial-specific target information and compare source-inspired and generic estimators. It needs a complete contract, feasibility gate, parameter/compute controls, seed plan, and decision rules before any run.
- No new dataset, motif, architecture family, or post-result sweep should be opened just to search for a favorable result. The user explicitly authorized both runs on 1 October 2026; the modules are tracked separately under `new_experiments/` and their scope is limited to the frozen V1 protocols.

## Current conclusion

The initial no-run status has been superseded: the user explicitly authorized both V1 modules on 1 October 2026, and they are now complete and independently verified. The experimental phase is closed.


The next immediately justified work is non-experimental: reconcile the branch crosswalk; decide whether the scientific contribution is an evidence-boundary synthesis or a prospective correspondence study; complete the manuscript/SI and figure source data only after that scope is fixed. Both M2 and M5 V1 runs are now complete and their independent verification passed. M2 found no realized-state benefit over action-conditioned AcRKN (action-only minus realized-state MSE −0.068094; 95% CI [−0.141077, −0.003541]) and reproduced exactly in a second full run. M5 found a bounded CF-local correspondence effect (+0.116588 nMAE; 95% CI [+0.115072, +0.118065]), but generic same-feature ridge and exact replay effects were larger. A post-run audit corrected the generic-RBF “parameter-matched” description. Full reports and caveats are in `new_experiments/`.
