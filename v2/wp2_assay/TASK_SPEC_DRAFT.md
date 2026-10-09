# TASK_SPEC_DRAFT — NeuroConverge v2, NCV2-004 / NCV2-005 / NCV2-006

**Status: DRAFT, prospective, frozen before any outcome.** No model has been fitted, no prediction
has been made, no endpoint value exists. This document fixes the prediction target, the two lawful
identity-mismatch controls, the matched-topology null, the data splits and the primary estimator. It
is a plan, not a result.

**Provenance of every number quoted here.** Functional side: the NWB file
`sub-20190929-07/sub-20190929-07_ses-20190929_ophys.nwb` from DANDI dandiset `000541`
(`CC-BY-4.0`), downloaded and read this session. Structural side:
`NemaNode/src/server/populate-db/raw-data/{neurons.json, datasets.json,
connections/witvliet_2020_8.json, connections/witvliet_2020_7.json}`, downloaded and read this
session. Nothing below is typed from memory.

---

## 1. NCV2-004 — the prediction target and the two mismatch controls

### 1.1 What the resources actually support, measured

| quantity | value | how measured |
| --- | --- | --- |
| functional neurons in one animal | 177 segments, 176 distinct named identities | decoded `ID_labels` via cumulative offsets |
| calcium trace shape | `(936, 177)` float64 | `SignalCalciumImResponseSeries.data` |
| trace index to identity | `rois -> id -> ID_labels`, one file | `RoiResponseSeries.rois` vs `PlaneSegmentation.id` |
| animal metadata | `subject_id 20190929_07`, strain `OH16230`, stage `YA`, sex `O`, 20.0 C | `general/subject` |
| **stimulus** | `intervals/chemical_stimuli` (`TimeIntervals`) | present |
| **free behaviour** | **NOT PRESENT** — the animal is in a microfluidic chip | searched; no behavioural time series |
| sampling interval | **UNKNOWN** — `starting_time = 0.0`, no `rate` on the response series | must be recovered before any temporal split |
| structural nodes, adult head | 221 (`2020_8`), 224 (`2020_7`) | `{pre} union {post}` |
| **functional names present in the structure** | **152 of 176 (86.4 %)** | name intersection |
| functional names present in `neurons.json` | **176 of 176 (100 %)** | name intersection |
| the 24 structural gaps | `I2L I2R I3 I4 I5 I6 M1 M2L M2R M3L M3R M4 M5 MCL MCR MI NSML NSMR ...` | they are **pharyngeal / pharynx-adjacent**, and the Witvliet adult datasets are **head ganglia only** |
| structural edges, `2020_8` | 2802 connections, `typ` 0 = chemical (directed) or 2 = gap junction (undirected), `syn` = synapse count | read |

### 1.2 The prediction target

**Target T1 (primary): held-out neuron activity prediction within a held-out animal.**

For a target animal `a` that contributed no structural information, predict the calcium trace of a
**pre-specified subset of its neurons** from the traces of the remaining neurons, using a model whose
recurrent coupling is constrained by a graph, and score the held-out neurons.

**Why this target and not behaviour.** The microfluidic preparation removes free behaviour, so a
behavioural target is not constructible from these files. The plan explicitly permits neural-activity
prediction as the primary endpoint. Choosing it is a consequence of the data, and that is stated
rather than hidden.

**Why a subset and not all neurons.** If every neuron is both input and target the task is a
reconstruction, not a prediction. The plan's own guidance is that records from a subset can resolve
degeneracy; here the subset is the **target**, and the complement is the **input**.

**Pre-specification of the split into input and target neurons.** It must be frozen by a rule that
cannot see the target values. The draft rule: **stratify by neuron class, then take a fixed fraction
`f_target` of each class**, with the class-level assignment drawn from a seed declared in the seed
registry. `f_target` is **not yet fixed** and must be chosen from the number of independent animals,
not from any prediction score.

### 1.3 The two lawful identity-mismatch controls

Both must hold **topology fixed and model capacity fixed**. A mismatch that changes the graph or the
parameter count is not a control; it is a second experiment.

**M1 — within-animal class-preserving permutation.** Permute the node labels of the structural graph
among neurons **that share a `classes` value**, keeping the graph's adjacency matrix unchanged as a
matrix. This destroys the specific cell-to-cell correspondence while preserving the degree sequence
within each class. It is constructible whenever **at least two structural nodes share a class**, which
is true for most classes in `neurons.json`; classes with a single member are **not permutable and are
recorded as a non-constructible subset**, not silently dropped.

**M2 — cross-animal identity rotation.** Replace the target animal's identity assignment with **another
animal's** assignment for the same structural graph, restricted to the 152 names present in both. This
is a mismatch that is *real* rather than synthetic — the mapping is a genuine NeuroPAL labelling of a
different worm — so it cannot be dismissed as an artificial perturbation.

**A third control that is a floor, not a mismatch: M0 — no structural constraint.** An
unconstrained recurrent model with the same parameter count. Without M0, a positive M1-vs-correct
result could be an artifact of the model class rather than of the mapping.

**Pre-declared failure of the controls.** If neither M1 nor M2 can be built without changing adjacency
or capacity, then **H2 is not testable and the sprint verdict is PIVOT or STOP**, because the novelty
claim rests entirely on this factor.

---

## 2. NCV2-005 — the matched-topology null

### 2.1 The contrast

Real anatomical graph `G_bio` versus an ensemble of matched controls, evaluated on **the same target**,
**the same input/target neuron split**, **the same estimator**, **the same training budget** and **the
same seeds**.

### 2.2 The three control families, in order of strictness

| family | what it preserves | why it is the right null for that question |
| --- | --- | --- |
| **N1 — degree-preserving directed rewire** | in-degree and out-degree **separately**, and the splitting of weight into the chemical (`typ=0`) and gap-junction (`typ=2`) layers | tests whether the *specific* wiring matters beyond the degree sequence. This is the primary null. |
| **N2 — class-block-preserving rewire** | degrees **and** the number of edges between neuron classes | tests whether the effect is explained by **cell-class composition** rather than by within-class structure. This is the strictest control and the one most likely to kill a naive H1. |
| **N3 — weight-shuffled** | topology fixed, `syn` weights permuted across edges | tests whether the effect is carried by the **synapse-count weighting** rather than the topology |

**NEW, joint-lead requirement 2026-10-09: the two edge classes must NOT be given equal evidentiary
weight, and this is now a design constraint rather than a caveat.** Witvliet et al. state that the
reconstruction of **electrical (gap-junction) connectivity is less complete than that of chemical
synapses**. Consequences that bind the null construction:

1. **The chemical layer is the primary analysis.** The gap-junction layer enters as a **secondary,
   explicitly lower-confidence** analysis, not merged into one adjacency.
2. **Asymmetric rewiring is therefore required, not optional.** N1 must preserve degree **within each
   layer separately**, and must **not** swap a chemical edge for a gap-junction edge; a null that
   treats the two as interchangeable edges of one graph assumes precisely the equal completeness the
   source denies.
3. **Missingness in the gap-junction layer is expected and must be propagated, not ignored.** Because
   the electrical reconstruction is known-incomplete, an absence of a gap junction is **weaker
   evidence of absence** than an absence of a chemical synapse. Any conclusion that rests on
   gap-junction sparsity must carry this asymmetry.
4. **The 2026 Scientific Reports locomotion result is consistent with this caution**: anatomical
   weights used directly did not produce the behaviour, and weights had to be optimised away from
   anatomy.

**Direction handling is explicit and must not be fudged.** Chemical synapses are **directed**; gap
junctions are **undirected**. The graph is therefore not a single matrix. Any rewire must state which
layer it operates on, and N1's degree sequence must be preserved **per layer**; collapsing the two
layers into one symmetric adjacency matrix would destroy the distinction the plan's field list demands
(`adjacency_direction`, `edge_type`) and is **forbidden** here.

### 2.3 The non-constructible subset, recorded

* **Classes with a single structural member cannot be class-permuted** and are excluded from M1's
  permutation while remaining in the graph. If the excluded fraction exceeds a pre-set threshold the
  test is reported as partial.
* **The 24 functional names absent from the adult head connectome** (`I*`, `M*`, pharyngeal) are
  outside the structural graph. They are **excluded from the structural contrast** and their calcium
  traces are **not** used as a silent substitute. The analysed neuron set is therefore **at most 152**,
  and that number is a ceiling, not a target.
* **`white_1986_*` compilations** are not independent specimens in the same sense as the Witvliet
  individuals and are **not** used as additional independent structural units.

### 2.4 Comparator fairness, stated as a checklist

Before any outcome is read, each of these must be true or the comparison is void:

1. identical input and target neuron sets across arms;
2. identical parameter count (verified by counting, not asserted);
3. identical training budget and identical seeds;
4. identical preprocessing of the calcium traces;
5. the same number of matched controls per real graph, and the real graph's score reported against the
   **distribution** of control scores, never against the best or worst single control;
6. multiplicity across the three control families handled by a pre-declared rule.

---

## 3. NCV2-006 — splits, estimator, leakage

### 3.1 The independent unit is the animal

**`000541` supplies 21 animals.** The available unit count is **21**, and this is small. Frames are not
replicates. Neurons are not replicates. Seeds are not replicates. **Nothing in this design may report
an `n` larger than the number of animals for any animal-level claim.**

### 3.2 Splits

* **Development / evaluation split is at the ANIMAL level**, never at the frame or session level.
* Both dandisets `000541` and `000776` carry `subject` identifiers, enabling a **lab-held-out** check
  if both are used; the draft uses `000541` alone and states that a cross-lab split is a **later
  stage**, not part of this sprint.
* **If the sampling interval cannot be recovered**, no temporal split can be justified, and the design
  falls back to splitting by **neuron**, which is a weaker design; that fallback must be recorded as a
  reduction in claim strength rather than presented as equivalent.

### 3.3 Leakage tests, each of which must be run and reported

| test | what it catches |
| --- | --- |
| same-animal crossing | any frame of an evaluation animal appearing in training |
| identity leakage | the identity mapping being derived from the same records used as targets |
| target leakage | any preprocessing statistic (mean, std, percentile normalisation) computed over the target neurons |
| hyperparameter leakage | any hyperparameter chosen by looking at held-out performance |
| seed reuse | the same seed producing both a training initialisation and a control rewire |

**The normalisation leakage test deserves emphasis**: the WormWideWeb schema offers `trace_array`
(z-scored per neuron), `trace_array_F20` and `trace_array_Fmean`. **Per-neuron z-scoring of a target
neuron uses that neuron's own values and is therefore leakage if the target is held out.** Any
normalisation must be per-neuron **within the training half only**, or the design must use
`trace_array_original` and do its own normalisation.

### 3.4 Estimator and endpoint

* **Primary endpoint: held-out per-neuron prediction error**, aggregated to the animal, then compared
  **paired by animal** across arms.
* **Primary contrast: real graph minus the N1 control ensemble.** The **structure x identity
  interaction** (correct mapping minus M1 mismatch, differenced across real and control topologies) is
  the pre-declared test of H2.
* **The endpoint value is deliberately not numerically fixed here.** The plan forbids inheriting
  IRCN's `NRMSE 0.001` or `G1 10 %` or CBCC's per-seed `MAC 1 %`; the threshold must follow from the
  task scale and from what 21 animals can resolve. **Fixing it before the estimator is implemented
  would be a number chosen for convenience, which is exactly what the plan warns against.**

### 3.5 Power

Computed this session rather than asserted, by the standard normal approximation for a paired design
`d = (z_{1-alpha/2} + z_power) / sqrt(n)` with two-sided `alpha = 0.05`:

| animals `n` | standardised effect at 50 % power (the alpha floor) | at 80 % power | at 95 % power |
| --- | --- | --- | --- |
| 8 | 0.6930 | 0.9905 | 1.2745 |
| 10 | 0.6198 | 0.8859 | 1.1399 |
| 15 | 0.5061 | 0.7234 | 0.9308 |
| **21** | **0.4277** | **0.6114** | 0.7866 |
| 30 | 0.3578 | 0.5115 | 0.6581 |
| 50 | 0.2772 | 0.3962 | 0.5098 |

**So with 21 animals, an effect of `mu/sigma_d = 0.4277` is detectable at all, and one of `0.6114` is
detectable with 80 % power.** An earlier draft of this paragraph quoted `0.62` and called it "the
two-sided 0.05 floor"; **that conflated the alpha floor with the 80 % power requirement.** The two
numbers differ, and which one binds depends on the claim: a claim of *detection* needs the floor, a
claim of *adequate power* needs the larger value.

**This is a weak design and must be declared as such.** No amount of frame count changes it. If the
effect of interest is smaller than the 80 % value, the honest outcome is `INCONCLUSIVE`, not `FAIL`.

**CRITICAL AMENDMENT, joint-lead correction 2026-10-09: 21 is the DATASET total, not necessarily the
confirmatory sample size.** The table above assumes all 21 animals enter the paired evaluation. If any
animals are consumed by training, development or model selection, **the confirmatory `n` is smaller and
the table does not apply.** An earlier draft used `n = 21` without stating this assumption; the
assumption is the correction.

**WP2 must therefore report three distinct counts and the hierarchy between them:**

| quantity | meaning | status |
| --- | --- | --- |
| **total animals** | 21, the dataset total | known |
| **training / development animals** | consumed by fitting and model selection | **to be fixed in C4** |
| **effective paired confirmatory animals `n_eff`** | animals entering the paired test | **to be fixed in C4; the power table above must be recomputed for it** |
| **training seeds per animal** | repeated initialisations, **nested within animal, not independent** | to be fixed in C4 |

**The nesting must be explicit:** seeds are nested within animals, animals are nested within the
dataset. **A seed-level standard error computed across seeds on one animal is not an animal-level
standard error**, and reporting it as one would inflate `n` — the exact error the plan forbids when it
says sample size must not be manufactured from frame or neuron counts. **A seed is the same kind of
non-replicate as a frame.**

---

## 3.6 Source licensing: use rights and redistribution rights are separate

**Joint-lead correction 2026-10-09, adopted.** The NemaNode **repository declares GPL-3.0**, but that
is a **software** licence over the code. **It does not transfer to the anatomical matrices the code
loads**, which are third-party reconstructions (White 1986 compilations and Witvliet et al.) and whose
redistribution terms are **`UNKNOWN`**.

| asset | use as analysis input | redistribution |
| --- | --- | --- |
| DANDI `000541` NWB | permitted, `spdx:CC-BY-4.0`, `dandi:OpenAccess` | permitted with attribution |
| NemaNode code | permitted, GPL-3.0 | code licence, not a data licence |
| **the anatomical matrices loaded by that code** | **permitted for analysis** | **`UNKNOWN` -- NOT permitted until resolved** |

**R1 therefore stays OPEN and is not closed by the GPL-3.0 finding.** No copy of an anatomical matrix
may be redistributed, and no derived graph package may be published, until each source's terms are
established. This does not block analysis.

## 4. What this document does NOT do

* It does not fix `f_target`, the seed registry, or the endpoint threshold — those require the
  sampling interval and a power calculation that has not been done.
* It does not run anything. **No v2 model has been fitted; no v2 endpoint exists.**
* It does not claim the design will work. It claims the design is **constructible from real,
  downloaded data**, which is what this sprint was asked to establish.
* It does not present the DANDI or NemaNode resources as a contribution of this project.
