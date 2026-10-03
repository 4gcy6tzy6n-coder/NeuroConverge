# Prospective held-out validation V1: feature-matched PC→SST context

**Study ID:** `PROSPECTIVE_V1_PC_SST_FIGURE_GROUND`
**Protocol status:** prospective within the existing NeuroConverge portfolio; the source mechanism was selected after earlier project outcomes were known. This is not project-level preregistration, an independent-team replication, a wet-lab study, or biological confirmation.
**Source:** Hendricks et al., *Feature-tuned synaptic inputs to somatostatin interneurons drive context-dependent processing*, *Neuron* (2026), DOI [10.1016/j.neuron.2025.12.021](https://doi.org/10.1016/j.neuron.2025.12.021). The paper reports feature-tuned, like-to-like PC→SST functional connectivity and causal SST contribution to orientation-dependent surround suppression in mouse V1. It reports a partial/modulatory VIP contribution as a possibility; this protocol does not claim VIP is irrelevant.

## Question and inference boundary

On a newly specified synthetic figure/ground segmentation task, does feature-matched local inhibitory pooling improve segmentation specifically when each orientation channel is routed to its matching SST-like pool, relative to a capacity-matched nonselective inhibitory control? Does the result persist under a preregistered background-orientation prior shift and across training-set sizes?

The benchmark uses synthetic orientation-tuned population activity, not the source paper's recorded neural responses. A positive result would support only a computation-level result on this synthetic task: feature-selective local inhibition can be useful under the specified signal/task distribution. It would not validate the biological implementation, prove that the source circuit performs pixel segmentation, establish animal-level transfer, or validate a general biological-to-AI law. A null result will be retained as such; no rescue run is authorized by this protocol.

## Frozen task and source-aligned signal

- Each example is an 11×11 spatial field with 8 orientation-tuned PC-like channels (orientation bins are equally spaced over 180°). The response at each location is a noisy soft tuning vector centered on its assigned orientation category. This is a synthetic population code; it is not a copy of source data.
- Each image contains one randomly placed 3×3 square figure. The background orientation is sampled uniformly for training and IID test. The figure orientation is sampled uniformly from the seven alternatives to the background. Pixel-level output is figure membership.
- Each generated task instance has 512 training images, 256 IID test images and 256 OOD images. Training prefixes of 32, 128 and 512 images are nested. OOD shifts only the background-orientation prior to a frozen skewed distribution; the figure remains a uniformly selected non-background orientation.
- The task-instance seed is the independent inference unit (30 independently derived instances). Images and pixels are nested observations. No pixel, orientation bin, or image is counted as an independent task replicate.

## Frozen factorial and comparators

The primary design is a paired 2×2 factorial within each task-instance seed:

| Factor | Aligned/selective condition | Control condition |
|---|---|---|
| Mechanism | Each PC orientation channel excites its matching local SST-like inhibitory pool; the pool subtracts the mean same-channel activity in the 8-neighbour surround. | A scalar, nonselective local inhibitory pool is broadcast across the 8 channels. It uses the same fixed inhibition coefficient and channel count, but has no feature-specific routing. |
| Correspondence | PC channel and SST-pool labels match. | The PC→SST channel assignment uses a frozen no-fixed-point permutation within each task instance; orientation marginals, images, targets and sample counts are unchanged. |

Both factorial arms use the same fixed transform coefficient (0.65) and the same regularized linear discriminant readout, fit independently on the same training examples. There are no trainable mechanism parameters. The separate generic-context reference receives the same PC and neighbour feature maps concatenated (16 features) and uses the same readout family; it is an information-matched reference with more input features, not a parameter-matched causal control. The task-null reference ranks every pixel equally and has expected average precision equal to the figure-pixel prevalence, 9/121.

The correspondence break permutes the surround-to-pool feature assignment only. It does not shuffle targets or images. The nonselective mechanism's pooled activity is invariant to the permutation, providing a negative-control check.

## Endpoints and decision rules

- Primary metric: per-image average precision (AP) for figure pixels, averaged within task-instance seed. Higher is better. No metrics are pooled across distinct endpoint types.
- Primary interaction, on AP scale:
  `I = (AP(selective, broken) - AP(selective, aligned)) - (AP(nonselective, broken) - AP(nonselective, aligned))`.
  Positive I is predicted if alignment specifically benefits feature-selective inhibition. The primary gate requires (i) task viability: generic-context AP exceeds the prevalence null with a paired 95% task-seed interval above zero, (ii) the lower paired 95% interval for I exceeds zero with two-sided sign-flip P<0.05, and (iii) selective/aligned AP exceeds nonselective/aligned AP with lower paired 95% interval above zero. All three are required for a positive mechanism-specificity statement.
- Confidence intervals resample the 30 task-instance seeds as paired units (20,000 percentile bootstrap draws). Two-sided paired sign-flip P values use 100,000 Monte Carlo sign patterns. Both use NumPy `default_rng(20261003)` initialized once in the verifier and consumed first for bootstrap indices, then for sign patterns. Tests are unadjusted because there is one co-primary interaction. Secondary scaling and OOD contrasts are explicitly secondary and do not change the primary gate.
- Scaling: report paired selective-minus-nonselective AP at each nested N and its linear slope against log2(N); do not claim an inductive-bias signature unless the frozen interaction gate passes and the prespecified slope interval excludes zero.
- OOD: report primary-cell AP and factorial interaction on the skewed-background test distribution with paired 95% intervals; descriptive only.
- Report every task seed and all factorial arms. Do not tune coefficient, noise, architecture, seeds or gates after outcome access. Any implementation defect found after execution is an incident; preserve outputs and do not selectively rerun.

## Execution and freeze

1. Freeze this contract, runner, verifier, software versions and derived seed schedule by SHA-256 before generating confirmatory outcome data.
2. Use the exact fixed generator and deterministic feature transform below; no development search is performed.
3. Generate all task instances, factorial arms, training prefixes, IID and OOD results in one complete run. The runner refuses a nonempty output directory and emits no interim aggregate effects.
4. Independently recompute response features, metrics, paired contrasts, intervals, tests, hashes and completeness with the verifier.
5. Preserve all outcomes, including nulls. No DMP V2 or protocol rescue is part of this study.

## Interpretation ceiling

This experiment is synthetic and uses a source-informed abstraction. It tests a new task family after the broader project hypotheses and earlier outcomes were known. It therefore adds an external-to-prior-portfolio mechanism/task package, but it does not erase project-level outcome-informed selection or establish an independent biological transfer validation. The released source-paper data/code are cited but not downloaded or used as observations; the Zenodo archive is approximately 1.76 GB. No new animal work was conducted.
