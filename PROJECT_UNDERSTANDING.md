# Project understanding: NeuroConverge and its two workstreams

**Audit snapshot:** 1 October 2026. This is a project map, not an owner-approved source freeze.

## The integrated question

NeuroConverge asks when a biological observation can support an artificial design choice and when that choice yields measurable utility. That question has at least four distinct evidence stages: (1) a biological structure or signal is reliably characterized; (2) a computation is supported by biological source evidence; (3) an artificial model receives information corresponding to that computation; and (4) the model gains utility against fair, strong alternatives. Passing one stage does not imply passing the next.

The two source projects occupy different parts of this question. They were not originally one prospective experiment, do not share a common outcome or estimand, and cannot be pooled into a project-level effect.

## Workstream A — NeuroMotif: connectome structure and dynamics

**Question:** Does tested connectome-derived organization explain or improve selected dynamical behaviors?

- In the frozen reservoir/interference assay, the tested whole-connectome off-diagonal topology did not outperform passive identity-like persistence on value retention. Because the control keeps diagonal state persistence, this is specifically a test of the added off-diagonal topology in that task.
- The retrospective Fish1.5 analysis covered a single specimen (`n=82` neurons). The predicted positive recurrence–persistence association was not supported (`rho=-0.1096`, positive-permutation `p=0.8337`, neuron-bootstrap 95% interval `[-0.2932, 0.1338]`). The frozen topology null was invalid/indeterminate because 861/1,000 correlations were undefined.
- The supportable conclusion is bounded: these tested analyses do not establish a general connectome-derived computational advantage. They do not establish that biological structure is generally useless.

## Workstream B — NeuroMech: source computation and artificial transfer

**Question:** Which biological computations are source-supported, and what survives when abstracted into artificial tasks?

- **Motor feedback:** published *C. elegans* evidence supports RIM-dependent motor-state information reaching AIY and a role in sustained forward thermotaxis. The biological signal is premotor/corollary-discharge-like; it should not be renamed measured post-actuator body velocity. Public data schema blocked the planned animal-level reanalysis, which is missing information rather than a negative result.
- **Synthetic M2 placement test:** sensory-site feedback had 88.94% accuracy vs 82.14% for equal-parameter output persistence at hazard 0.05, but did not beat no-feedback (89.05%), a generic two-unit RNN (90.21%) or a task-aware Bayes filter (90.30%). This is a comparator-specific placement trade-off in one synthetic task, not a general AI advantage or biological validation.
- **Cerebellar source-data analysis:** CF-LTD weights are reconstructed/model-derived, not directly measured synaptic strengths. They had descriptive within-session predictive structure across 16 sessions; a fixed ridge readout was stronger on average. Sessions are not independent animals.
- **Source-defined CF-LTD transfer:** in a separate synthetic interval task, the frozen criterion failed. Mean MAE was 0.1252 s for CF-LTD vs 0.1097 s no-trace, 0.1252 s timing-shuffled, 0.1030 s generic RBF and 0.0753 s empirical timer. Independent target jitter was absent from model inputs, so this bounds that implementation/task pairing.
- **Eligibility trace, delayed XOR:** 32-seed synthetic classification accuracy was 0.6974 for eligibility, 0.5562 for no-trace/TBPTT-1, 0.9633 for TBPTT-4 and 0.9996 for full BPTT. Trace helps against a weak short-memory baseline and loses to longer/full gradient methods.
- **Eligibility trace, fixed-generator suite:** the trace beat no-trace on average by 0.2284 (95% interval [0.2213, 0.2357]) across three fixed input generators. Exact replay beat trace in all 12 generator-by-delay cells (overall accuracy 0.7609 vs 0.5590). This is limited generator variation under one classification objective, not broad task generalization.

These are separate biological and synthetic records. In particular, the source-defined CF-LTD interval transfer experiment is not the same algorithm/task as the eligibility-trace XOR or generator-generalization tests.

## What the combined evidence means

The strongest defensible synthesis is methodological: separate structure, biological computation, information correspondence, computational sufficiency, mechanism specificity and artificial utility. The cases motivate that retrospective organizing scaffold but do not validate it as a universal hierarchy or transfer law. Local ablation wins need to be read beside the strongest comparator, frozen task criterion, actual inputs and independent unit.

## Source and integration status

- The publication repository is intentionally separate from both source histories.
- NeuroMotif public `main` was observed at `1adc07ffc735cf458116ca36c9f4875708034d4a`; local publication checkout was clean at audit time, but may not include every paper-critical local artifact.
- NeuroMech public `experiment-publication` was observed at `3e5c458f15b2cad7aa6c5703b1827763e84343bb`. Local `main` was at `555c064f4ff3153c871808c3f191b9934a18eaf5` with 387 changed/untracked paths; a publication checkout had 2 local changes. These snapshots are not interchangeable and the source owner has not selected the canonical integration snapshot.
- The NeuroConverge remote advertised no heads on the checked attempt; empty vs private/inaccessible remains unknown.
- Selected M2 and source-defined M5 verifiers passed. The eligibility task has a passing stored post-run verification, but its source checksum list contains stale/unresolved entries. Fish1.5's checksum file also contains stale absolute paths; selected paper-level file hashes are listed separately.
- Source freeze, exact portfolio inclusion/exclusion, source-data rights, figure exports, complete Methods, authorship/contribution metadata, and final repository publication remain unresolved. No new experiments are required to state the bounded synthesis; unresolved claims should be narrowed or retained for later audit.
