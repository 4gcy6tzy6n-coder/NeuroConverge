# From connectome structure to artificial computation: boundary conditions for neural transfer

**NeuroConverge working draft — 1 October 2026. Internal integration draft; not for submission.**

## Abstract (provisional)

Biological inspiration can motivate artificial architectures and learning rules, but biological provenance does not itself establish artificial utility. We integrate two distinct evidence portfolios: NeuroMotif, which tested whether connectome-derived structure supported selected computational behaviors, and NeuroMech, which examined source-grounded computations and their artificial implementations. The tested NeuroMotif assays did not establish a general structure-derived advantage; one retrospective Fish1.5 analysis was limited to a single specimen and its frozen topology-null inference was invalid or indeterminate. In NeuroMech, source-supported motor-state and cerebellar temporal computations were followed by task-specific artificial studies. Some local contrasts favored biologically motivated components, while stronger generic or task-aware alternatives, failed viability criteria, and task-information mismatches bounded interpretation. The two portfolios do not share an estimand and are not pooled. Together they motivate separating structural evidence, computational correspondence, mechanism specificity and artificial utility. This retrospective framework is a proposal for future testing, not a validated law of transfer.

## Introduction

Biological systems are increasingly used to motivate artificial architectures, representations and learning rules. Yet three questions are often conflated: whether a biological structure is reliably characterized, whether it implements a particular computation, and whether an abstraction of that computation improves an artificial task. Evidence for one question does not settle the next.

NeuroMotif and NeuroMech approached different portions of this chain. NeuroMotif asked whether connectome-derived organization related to selected dynamical properties and whether a broader structure-to-AI claim could be supported. NeuroMech examined named biological computations, including motor-state feedback and cerebellar temporal learning, and tested simplified implementations under synthetic tasks. These histories are heterogeneous: they include source literature, source-data analyses, model reproductions, synthetic experiments, negative results, invalid analyses and blocked data paths.

Here we ask: **when does biologically grounded neural computation survive translation into a useful artificial inductive bias?** We treat this as a retrospective evidence audit, not as a pooled test or a claim that the projects were prospectively designed as one study. We organize the evidence around four questions: what the structure tests support; what source evidence identifies as computation; what artificial tests show under their actual controls and task inputs; and what remains a prospective transfer hypothesis.

## Results

### 1. The tested structure-to-dynamics assays did not establish a general advantage

In the frozen NeuroMotif reservoir/interference assay, tested whole-connectome off-diagonal topology did not outperform passive identity-like persistence for value retention. The comparator retains diagonal self-persistence, so this is not a test of recurrence versus no memory. It is a bounded result for the tested task and topology, not evidence that biological topology is generally useless. In a separate retrospective Fish1.5 analysis, the predicted positive recurrence–persistence association was not supported in one specimen (`n=82` neurons; Spearman `rho = -0.1096`, positive-permutation `p = 0.8337`, neuron-bootstrap 95% interval `[-0.2932, 0.1338]`). The combined decision remains indeterminate because 861 of 1,000 frozen topology-null graphs had undefined correlations; no null `p`-value is estimable. Neither result licenses population-level or universal claims.

### 2. Source-supported computation is distinct from graph structure

The NeuroMech motor-feedback line concerns published *C. elegans* evidence for RIM-dependent motor-state representation in AIY and sustained forward thermotaxis (Ji et al., 2021). The construct is premotor/corollary-discharge-like state information, not a direct measure of post-actuator body velocity. Public source tables lack the identity/time alignment needed for the frozen animal-level reanalysis; this is a data-schema boundary, not a biological negative. The cerebellar line uses source data and author-code-derived plasticity weights to study temporal prediction (Garcia-Garcia et al., 2024). Those weights are model-derived, not directly measured synaptic strengths. Independent source evidence for climbing-fibre instructive signals in delay eyeblink conditioning is a distinct biological result (Silva et al., 2024); it does not specify the exact plasticity equation tested here.

### 3. Artificial effects were bounded by task, information and comparator

In one synthetic switching task, sensory-site motor feedback reached 88.94% accuracy versus 82.14% for an equal-parameter output-persistence control, but did not exceed no-feedback (89.05%), a two-unit generic recurrent model (90.21%), or a task-aware Bayes filter (90.30%). The local contrast therefore identifies a placement-dependent trade-off against one comparator, not an overall accuracy advantage.

In the cerebellar source analysis, model-derived weights exceeded uniform weights in 15/16 source sessions and CF-time-shuffled weights in 16/16; a fixed ridge readout exceeded the source-derived projection in 14/16. This supports within-session predictive temporal structure under the modeled analysis. In the separate synthetic interval task, CF-timed LTD did not meet its frozen transfer criterion: mean held-out absolute error was 0.1252 s versus 0.1097 s for no-trace, 0.1252 s for CF-time-shuffled teaching, 0.1030 s for a generic radial-basis representation, and 0.0753 s for the training-label empirical timer. A design audit found that trial-specific timing jitter was independently sampled and not present in the inputs. The outcome bounds this implementation/task pair; it does not test whether the biological rule could use a suitable trial-specific signal.

Two additional M5 eligibility-trace studies use different synthetic objectives and must not be combined with the source-defined CF-LTD interval experiment. In a delayed-XOR classification task (32 seeds), eligibility traces reached 0.6974 accuracy versus 0.5562 for no-trace and one-step truncated backpropagation through time (TBPTT-1), but trailed TBPTT-4 (0.9633) and full backpropagation (0.9996). In a separate fixed-generator classification suite, trace eligibility exceeded no-trace by 0.2284 (95% interval [0.2213, 0.2357]); exact replay nevertheless outperformed eligibility in all 12 generator-by-delay cells (overall means 0.7609 versus 0.5590). These are post-result synthetic demonstrations that eligibility can help against a weak memory control under some task conditions; the stronger replay and gradient-based controls set a lower ceiling on claims. Neither result validates a cerebellar mechanism or establishes general transfer.

The M2, M5 source-readout, source-defined transfer, delayed-XOR and task-generator records are pinned to the NeuroMech `experiment-publication` commit `3e5c458f15b2cad7aa6c5703b1827763e84343bb`. Existing stored-output verifiers passed for M2 and the two source-defined CF-LTD packages; stored verification records are available for the delayed-XOR and generator studies, and selected artifact hashes are recorded in [`SELECTED_ARTIFACTS.csv`](../reproducibility/SELECTED_ARTIFACTS.csv). These packages are post-result exploratory at the project level, and the source-readout summaries are descriptive. This pins the cited study records; it does not resolve the broader NeuroMech mainline/worktree freeze or which additional studies belong in the integrated paper.

### 4. The combined record motivates a transfer-evidence hierarchy

The evidence motivates distinguishing (i) biological structure, (ii) source-supported computation, (iii) information correspondence, (iv) computational sufficiency, (v) mechanism specificity, and (vi) artificial utility. The ordering is an editorial and methodological scaffold inferred retrospectively from these cases. It is not a causal chain, validated scale, necessary-and-sufficient rule, or universal law. Prospective studies must freeze source-to-model correspondence, task information, strong alternatives and independent generalization criteria before outcomes.

## Discussion

The combined evidence does not establish that connectome-derived structure generally fails, nor that biological mechanisms generally improve artificial systems. Instead, it shows why structural description, computational interpretation and artificial utility require separate evidence. NeuroMotif's structure results are bounded to its assays. NeuroMech's source-supported computations do not automatically translate into advantages: the favorable motor-feedback contrast was comparator-specific, and the tested cerebellar transfer task did not meet its frozen criterion under an identified information mismatch.

The strongest common conclusion is methodological. A transfer claim should state which source variable is supported, what information the artificial system receives, which operation is preserved, what task makes that operation useful, and whether the effect survives generic, task-aware and mechanism-targeted comparisons. The evidence hierarchy presented here is a retrospective proposal; these two portfolios do not validate it. Heterogeneous outcomes cannot be pooled into one effect, and negative or blocked outcomes do not generalize beyond their claim scope.

Important work remains before internal review: exact source revisions must be frozen; every numerical statement must be reconciled to source records; the two workstreams' selection rules and inclusion/exclusion dispositions need audit; figure source data and reproduction scripts need to be assembled; supplementary materials and citation metadata need review; and redistribution, licensing, authorship and contribution details remain unresolved. The current draft is a starting integration, not a complete manuscript package.

## Methods (to complete)

Describe retrospective portfolio selection, provenance and outcome-informed status; give source-linked contracts, runner/configuration, seeds, data versions, independent units, uncertainty procedures and comparator definitions for each selected study. Specify the rationale for retaining or excluding every result from the two project portfolios. Report no pooled effect. Reproducibility statements must distinguish published source files, local-only artifacts, unavailable historical environments and verified reruns.

## Figure legends

Provisional legends and source-data requirements are in [`../figures/FIGURE_PLAN.md`](../figures/FIGURE_PLAN.md). Figure exports are not yet generated or verified.

## References

Working references are listed in [`references.bib`](references.bib). Citation placement, completeness and the full related-work review still require audit.
