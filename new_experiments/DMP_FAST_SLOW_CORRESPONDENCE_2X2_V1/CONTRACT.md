# DMP fast–slow pathway × correspondence validation V1

**Project status:** post-result extension to NeuroConverge. M2/M5 and other project outcomes were inspected before this protocol was designed. This is therefore not project-level preregistration or an independent confirmation of the original portfolio. The contract and confirmatory-unit seed schedule will be frozen before this module's outcome run.  
**Scientific object:** a compact fast pathway plus a layer-shared, low-dimensional slow state, following the computational abstraction in Sun et al., *Nature Machine Intelligence* (2026), DOI [10.1038/s42256-026-01255-3](https://doi.org/10.1038/s42256-026-01255-3). This is a source-inspired artificial implementation, not a biological mechanism discovery or a reproduction of that paper's SNN/hardware system.  
**Study ID:** `DMP_FAST_SLOW_CORRESPONDENCE_2X2_V1`

## Question and claim boundary

Does an explicit slow state improve performance specifically when the trial-level slow-context stream is correctly paired with the fast stream and target, and does that conditional effect transfer across three predeclared synthetic task families, training-set sizes, and one longer-delay condition?

A positive result can support only a fast–slow dynamics × correspondence interaction in these synthetic task families. It cannot show that biological provenance caused an advantage, validate cortical biology, establish a universal transfer law, or establish NMI readiness. A negative or mixed result will be reported without tuning or rescue.

## Design

The study is a repeated-measures 2 × 2 factorial for each task family and each task-instance seed:

| Factor | Preserved | Control |
|---|---|---|
| Mechanism (M) | DMP-style fast LIF state plus a fixed, low-dimensional LMU-like slow state | Same LIF network, trainable tensors, state dimension, initialization, optimizer and updates; slow-state transition matrix replaced by a fast-decay matrix with matched input-energy norm |
| Correspondence (C) | Each trial receives its own slow-context stream | Only the slow-context stream is reassigned across trials within the same split by a no-fixed-point derangement. Fast streams, targets and sample counts remain fixed; the context category may coincidentally match after reassignment. |

The four factorial cells are `M+ C+`, `M+ C−`, `M− C+`, and `M− C−`. The same task instance, raw fast streams, targets, base model initialization and train/test split are paired across cells. Train and test correspondence permutations are generated independently. The shuffling changes the cross-stream pairing, not the target labels, and preserves the slow-stream multiset exactly.

### Architecture and fair comparisons

- Hidden layer: 32 leaky integrate-and-fire units, membrane leak β = 0.5, threshold 1.0, reset by subtracting the threshold after a spike; hard threshold forward pass with a fixed fast-sigmoid surrogate derivative for training.
- Slow state: d = 2 fixed LMU-like state dimensions, driven by a learned scalar compression of the input and read into the membrane current. The LMU-like matrices use the Legendre state-space construction and exact zero-order-hold discretization with horizon θ = 32 steps. The slow matrices are fixed during training.
- M− changes only the fixed state-transition matrix to βI; it uses the same fixed input matrix, so its input norm is identical to M+. This removes slow eigenmodes while retaining the auxiliary state and its computation.
- Task heads use the final membrane state and the same loss family within each task. M+ and M− have identical trainable tensor shapes and parameter counts. Initial weights are paired.
- A one-layer generic GRU is a separate strong reference, not part of the factorial. Its hidden width is fixed per output dimension before confirmation to keep trainable parameters within 5% of the DMP model. It receives the same sequence and correspondence manipulation, training examples, optimizer, learning rate, update budget, batch size and stopping rule. Parameter count is matched; exact FLOPs are not claimed to be matched.
- A task-null predictor is reported as the viability bound, not as a fair model comparator. The generator defines the task oracle by construction; its performance is not treated as an empirical model result or used for tuning.

### Task families

All sequences have four input channels and a 64-step training horizon. The confirmatory task-instance unit is a separately sampled generator seed; trial, episode, optimizer initialization and repeated conditions are nested observations.

1. **Delayed paired association.** A four-level context is presented in steps 0–3; a four-level query is presented in steps 36–39. A task-instance-specific, balanced mapping determines one of four classes from the context–query pair. The primary OOD test moves the query to steps 68–71 in a 128-step sequence, doubling the context-to-query gap from 32 to 64 steps.
2. **Partially observed state estimation.** A latent AR(1) state is observed through two noisy channels whose reliability is indicated by a slowly varying context stream. The target is the final latent state; the endpoint is MSE divided by the latent-state variance. The primary OOD test doubles the sequence horizon from 64 to 128 steps without retuning.
3. **Delayed contextual decision.** An early context selects a task-instance-specific mapping from evidence in steps 36–51 to one of four actions. Distractor inputs fill the delay. The target is the oracle action implied by the generator; the endpoint is four-class 0–1 loss. The primary OOD test moves evidence to steps 68–83 in a 128-step sequence, doubling the context-to-evidence gap from 32 to 64 steps.

Generator distributions, class mappings, input noise, seed derivation, and split sizes are fixed in the runner before confirmatory output is generated. Each task-instance seed has 2,048 training trials, 512 IID test trials and 512 longer-delay OOD trials. Nested training prefixes are 128, 512 and 2,048 trials. For each prefix, correspondence is independently broken within that prefix, preserving its exact context-stream multiset and pairing the same prefix rows across C+ and C−. The same held-out test sets are evaluated at all training sizes.

## Training and outcomes

- Two paired model initializations per task instance and factorial cell; results are averaged within task instance before inference.
- Fixed 10 training epochs per fit, batch size 64, Adam with a fixed learning rate of 0.003. No confirmatory seed contributes to tuning, and no learning-rate search is run.
- The independent unit is the task-instance seed (30 per family). Resampling the 512 test trials or optimizer initializations as independent units is prohibited.
- The primary outcome is family-specific: normalized MSE for state estimation and 0–1 loss for the two four-class tasks. Family-specific estimates are not pooled on their raw scale.
- For loss (L), the primary interaction is
  (I = [L(M+,C−)-L(M+,C+)] - [L(M−,C−)-L(M−,C+)]).
  Positive (I) means that the performance cost of breaking correspondence is larger under slow dynamics. The mechanism-specificity gate additionally requires lower loss for M+ than M− in `C+`.
- Three task-family interactions are co-primary. Paired percentile bootstrap intervals resample task-instance seeds and retain all within-unit cells. Two-sided sign-flip P values are adjusted across the three interactions by Holm's method. A cross-task statement requires all three unadjusted 95% paired intervals to remain above zero, all three Holm-adjusted P values below 0.05, and all three viability gates to pass.
- The viability gate is fixed before confirmation: the aligned full-data generic GRU must outperform the task-null predictor on the task-specific primary metric. Failure marks that task family `TASK_GATE_FAILED`; no mechanism interpretation is made for that family.
- Data-scaling analyses use the three nested training sizes. For each family, the unit-level slope of aligned (short-state loss − DMP loss) against log₂(N) is tested by paired sign-flip; the three slope P values are Holm-adjusted. A sample-efficiency claim requires a positive lower 95% interval at N=128, a negative upper 95% interval for the slope, and adjusted P < 0.05. Otherwise results are reported as learning curves without an inductive-bias claim.
- OOD results are secondary and evaluated without refitting. Only the doubled-delay/horizon shift is confirmatory OOD; other shifts are not added after outcome inspection.

## Freeze and execution rules

1. Use development task-instance IDs disjoint from confirmatory IDs. Development is restricted to implementation/integrity checks; the learning rate is fixed at 0.003 and is not selected from confirmatory outcomes.
2. Freeze this contract, runner, verifier, runtime/dependency versions and derived confirmatory seed schedule. Record SHA-256 hashes before generating confirmatory data.
3. Confirm the output directory is empty. The runner refuses to overwrite existing results.
4. Before the outcome run, smoke checks may verify tensor shapes, causal inputs, equal trainable parameter counts, class balance, independent no-fixed-point permutations and exact marginal preservation. Smoke output must not include confirmatory effects.
5. Generate all three families, both correspondence conditions, all sample sizes and all OOD tests in one run. Print progress only, not interim outcome summaries.
6. The verifier independently checks hashes, counts, paired-unit completeness, recalculates all reported metrics and contrasts, and applies multiplicity correction.
7. Any implementation correction after outcome generation is a new V2. Preserve the original contract, code, outputs and incident record; do not tune, drop units or rerun selectively.

## Interpretation ceiling

Even a complete positive result would not establish cortical fast–slow biology, a biological cause of the computational effect, a broad biological-to-AI transfer law, generalization to natural neural data, energy or hardware efficiency, or venue readiness. The selected fast–slow abstraction and broad task class already have substantial published precedent, including DMP-SNN's NMI 2026 results on long-sequence benchmarks and hardware. This module asks a narrower interaction question; it cannot claim novelty for fast–slow memory itself.
