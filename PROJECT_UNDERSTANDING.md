# Project understanding: NeuroConverge and its two workstreams

**Audit snapshot:** 3 October 2026. This is a project map, not an owner-approved source freeze.

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

These are separate biological and synthetic records. In particular, the source-defined CF-LTD interval transfer experiment is not the same algorithm/task as the eligibility-trace XOR or generator-generalization tests. The M2 action-belief, M5 correspondence, and DMP mechanism × correspondence tests are separate synthetic extensions, not biological replications.

The wider NeuroMech portfolio is substantially larger than the selected M2/M5 examples. The current local evidence ledger also covers M4 (CA3-inspired Hopfield versus exact retrieval), M6 (state-gated inference), M7 (trace/autocorrelation boundaries), M8 (trace horizon versus replay), M9 (recurrent eligibility versus BPTT), M10 (a viability-failed delayed-XOR benchmark), and a Drosophila-inspired synthetic visual stress test. The later local classification refresh adds M11 (a viable latent-state task with a small bounded trace disadvantage) and M12 (an action-conditioned controller whose frozen task-viability gate failed). These outcomes are not interchangeable replications: their tasks, units, architectures, and controls differ. They belong in a full selection/disposition table, even when only some are described in the main Results.

## What the combined evidence means

The strongest defensible synthesis is methodological: separate structure, biological computation, information correspondence, computational sufficiency, mechanism specificity and artificial utility. The cases motivate that retrospective organizing scaffold but do not validate it as a universal hierarchy or transfer law. Local ablation wins need to be read beside the strongest comparator, frozen task criterion, actual inputs and independent unit.

## Source and integration status

- The publication repository is intentionally separate from both source histories.
- NeuroMotif public `main` is `1adc07ffc735cf458116ca36c9f4875708034d4a`; the local publication checkout was clean and includes the M12 result record. The M0 full falsification report and some audit/source-chain records remain local to the NeuroMech workspace, so the public mirror alone is not the entire paper-critical source.
- NeuroMech public `experiment-publication` is `3e5c458f15b2cad7aa6c5703b1827763e84343bb`. The local integrated `main` is `555c064f4ff3153c871808c3f191b9934a18eaf5` but has 387 changed/untracked paths; a separate publication checkout has 2 local changes. The current local Route-D synthesis and evidence-matrix refresh are later scope records and are not represented by that public branch. These snapshots are not interchangeable.
- The project scope is author-directed as complete for evidence selection (no new experiments by default), but the exact artifact freeze is not complete. Scope freeze and immutable artifact freeze are different states.
- NeuroConverge now has a public `main` at commit `b55871dec1207b2c9e8b63270ebcc7871f0feaca`; its tree matches the local integration tree. That publication repo commit does not resolve the source-snapshot discrepancy above.
- Selected M2 and source-defined M5 verifiers passed. The eligibility task has a passing stored post-run verification, but its source checksum list contains stale/unresolved entries. Fish1.5's checksum file also contains stale absolute paths; selected paper-level file hashes are listed separately.
- The complete internal manuscript and six source-linked, visually inspected figure exports are now drafted. Still unresolved: source artifact freeze, exact historical inclusion crosswalk, redistribution rights, authorship/contribution metadata, final attribution and internal author approval. The independent project-level novelty/venue audit still says NMI Article and Analysis are not ready. Current synthetic experiment packages are complete; further variants are outside scope without a separate decision.

## Prospective validation V1 results

The user authorized two prospective synthetic tests on 1 October 2026. M2 action-only minus realized-state MSE under hidden reversals was −0.068094 (paired seed-block bootstrap 95% CI [−0.141077, −0.003541]); the realized-state input was worse on average, while the information-recovery contrast was inconclusive. Two complete runs reproduced scientifically exactly after declared timing exclusions. This answers only the frozen artificial actuator-observability question and does not test the premotor RIM→AIY biological signal.

M5 CF-timed local nMAE(BROKEN) minus nMAE(ALIGNED) was +0.116588 (95% CI [+0.115072, +0.118065], 30/30 task seeds positive). The same-feature generic ridge and exact replay effects were larger (+0.202390 and +0.189552); the generic comparator was not strictly parameter matched. This is a bounded synthetic correspondence result, not evidence for biological CF-LTD or privileged biological provenance.

### DMP mechanism × correspondence extension

The DMP fast–slow package tested three synthetic task families with 30 task-instance seeds each. None passed the frozen positive mechanism-specificity gate: delayed association failed task viability; state estimation favored the short-state control; contextual decision showed near-zero full-data interaction. Contextual decision showed a small-data advantage that decayed with sample size, but it occurred in one family and did not survive a longer-delay shift. These are bounded synthetic results, not a biological replication; see the DMP report and its frozen family-level gates under [new_experiments](new_experiments/README.md).

### Later PC→SST figure–ground transfer test

One additional synthetic package translated a published orientation-tuned PC→SST circuit result into an 11×11 figure–ground task. The paper's neural recordings were not used. The package has 30 independently derived task-instance seeds and 230,400 per-image AP records across IID and skewed-background conditions. Hash, completeness, and permutation-invariance checks passed. At the primary IID N=512 analysis, the generic context comparator exceeded the prevalence null by +0.37219 AP (95% seed-bootstrap CI [+0.36046, +0.38379]); the task-viability gate passed. Selective aligned pooling was −0.02208 AP versus global aligned pooling (95% CI [−0.02737, −0.01664]). The frozen selectivity × correspondence interaction was +0.01603 (95% CI [+0.00815, +0.02357], two-sided sign-flip p=0.00060), opposite to the contract narrative's intended direction; the positive mechanism-specificity gate therefore failed. A post-run amendment documents a sign-description mismatch without changing the frozen contract, code, or outputs. This is a new mechanism/task pairing relative to the named earlier families, but it was chosen after prior project outcomes and remains in the visual domain; it cannot serve as project-level blind prospective validation. The full contract, outputs, verifier, and interpretation amendment are in [PROSPECTIVE_V1](new_experiments/PROSPECTIVE_V1/).

The source paper reports feature-tuned PC→SST inputs and a role for SST cells in orientation-dependent surround suppression ([Hendricks et al., Neuron, 2026](https://doi.org/10.1016/j.neuron.2025.12.021)). The synthetic result does not validate that biological mechanism or establish that correspondence is generally beneficial.

The experiment program is closed at this scope. DMP V2/rescue, further delay or seed sweeps, and additional synthetic variants are not part of the current evidence package. The prospective gap remains: all these studies were designed after prior project outcomes had been inspected, and there is no project-level preregistered or independent biological validation.
