# Post-run interpretation amendment — PROSPECTIVE_V1

**Purpose.** Record a directional wording error in the frozen primary contrast without changing the contract, runner, verifier, confirmatory seeds, outputs, or gate after outcome access.

## Error identified

The contract defines the AP interaction as `(AP(selective, broken) - AP(selective, aligned)) - (AP(global, broken) - AP(global, aligned))`, then says a positive value is predicted if alignment benefits the selective circuit. Because average precision is higher-is-better, the prose has the sign reversed: an alignment benefit predicts a *negative* value under this contrast order. The frozen gate required the interaction's lower interval to be above zero, in conflict with its stated biological prediction. This is a protocol interpretation error, not an implementation change.

The contract's descriptive study ID is `PROSPECTIVE_V1_PC_SST_FIGURE_GROUND`; the generated run-freeze metadata uses the directory label `PROSPECTIVE_V1`. This metadata naming mismatch does not change the runner, seed schedule, outcomes or verifier checks.

## Frozen result and correct directional interpretation

The two-sided task-instance interaction estimate was **+0.01603 AP** (paired 95% bootstrap CI **0.00815 to 0.02357**, Monte Carlo two-sided sign-flip *P* = **0.00060**). Under the written contrast formula and higher-is-better AP, this means correspondence breaking increased performance under selective routing relative to the global-pool arm, opposite to the narrative prediction that aligned correspondence should help.

At N=512 IID, selective/aligned AP was **0.42202** and global/aligned AP was **0.44409**. Their paired difference (selective minus global) was **−0.02208** (95% CI **−0.02737 to −0.01664**). The synthetic task passed its viability check: the generic-context reference exceeded the 9/121 prevalence null by **0.37219 AP** (95% CI **0.36046 to 0.38379**). However, the aligned selective circuit was worse than the aligned global-pool control, so the prespecified positive mechanism-specificity gate **did not pass**. The selective/global gap did not show a reliable training-size trend (slope **+0.00091 AP per log2(N)**, 95% CI **−0.00108 to +0.00291**, two-sided *P* = **0.376**). The secondary skewed-background OOD interaction was also positive (**+0.01692**, 95% CI **+0.00553 to +0.02913**), again opposite to the stated alignment-benefit prediction.

The verifier's `gate_pass=false` remains the governing decision. The interaction is reported as a two-sided difference in the opposite direction; it is not recoded as a positive transfer result. No rerun or post-result tuning was done.

## Scope and remaining limitations

This package used synthetic orientation-tuned population activity; the source paper's 1.76 GB Zenodo data/code archive was cited but not used as observations. The package is prospective relative to its own synthetic outcome run and introduces a new feature-matched PC→SST abstraction and figure/ground task, but its selection followed earlier NeuroConverge results. The visual sensory domain also overlaps prior synthetic-visual work in the broader project, even though the circuit and segmentation task differ. This is therefore not an independent project-level replication or biological validation. The external generic comparator is a linear context model with more input features, not a strong neural network or parameter-matched model; claims about broad comparator robustness are not supported.
