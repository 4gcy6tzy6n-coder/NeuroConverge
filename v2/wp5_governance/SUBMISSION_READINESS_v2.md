# Submission readiness assessment for the v2 line

**Status: an assessment, not a manuscript.** Written under the plan's hard constraint *"Do not write a new
NMI abstract, main-text Results, Discussion or figures"*. **That constraint and the instruction to drive the
work to NMI publication standard are in tension, and the tension is flagged in section 5 rather than
resolved unilaterally.**

---

## 1. The claim-evidence structure

**Four claims survive thirteen rounds. Each is stated with its evidence, its ceiling and its status.**

| id | claim | evidence | ceiling | status |
| --- | --- | --- | --- | --- |
| **V2-C1** | **Treating neuron-pair measurements as independent biological replicates inflates the standardised connectivity-function effect by 11 to 18 times.** | the identical contrast computed at both units: pair-measurement `d = 11.048`, animal-level `d = 0.7289`; inflation factors 11.2, 17.9, 15.2 | **arithmetic, not inference.** It bounds reporting practice, not biology | **SOLID** |
| **V2-C2** | **The source's own anatomy-versus-spontaneous-activity comparison reproduces, and the quantity it predicts has cross-animal agreement of only `r = 0.208` on the cells available.** | source claim quoted verbatim; reproduction gives `r = +0.0368` and `-0.0064` in its two animals; the two animals' activity correlation matrices agree at `r = 0.2084` on 23 shared cells | **`n = 2` and 23 shared cells.** The comparison is reproduced and bounded; **the bound is not itself generalised** | **SOLID, with the sample size stated** |
| **V2-C3** | **A pair's response decomposes into 55.1 % between-pair, 37.5 % within-cell measurement error, 5.5 % pair-specific animal deviation and 1.9 % homogeneous animal offset.** | three-level decomposition over 192,303 (animal, pair) units, `eps` identified from 38,003 units with repeats | **one atlas, one species, one preparation.** The 37.5 % measurement-error share quantifies an unreported limitation of this artifact | **SOLID** |
| **V2-C4** | **The published per-pair values are produced by analysis choices that live in the pipeline's code and not in its data file, and re-analysing the same records under defensible choices moves the animal-level estimate from `d = 0.085` to `0.729`.** | the source rule recovered line-by-line; five defensible specifications computed | **the five rows are this line's own constructions, not a systematic sample of published practice.** Stated as such in round 8 | **SOLID as a sensitivity; NOT yet solid as a claim about practice** |

**Claims explicitly NOT made, each with its reason:**

* **That the source paper's conclusions are wrong.** Its claims concern sign, strength, temporal properties
  and causal direction; this line measures one coarse averaged association.
* **That the heterogeneity is animal-specific biology.** **Retracted in round 12**: 5.5 % against 37.5 %
  measurement error.
* **Any causal claim.** Connectome and recordings are from **different animals**; mapping class remains
  `CELL_CLASS_ALIGNED_ACROSS_SPECIMENS`.
* **Any generalisation past this atlas, species or preparation.**

## 2. What makes this a contribution rather than a replication

**The v1 manuscript asks which evidential transitions require separate empirical support, across seven
synthetic cases, all negative, and its own closure document concedes the result may be "a descriptive
checklist". This line answers the same question on real data and gets numbers.**

**The transition under test is specific and nameable:** *from a per-pair response value in a published
matrix to an inference about the circuit.* **It requires three supports the artifact does not carry:**

1. **a unit** -- and the artifact's values are routinely analysed at the wrong one, by a factor of 11 to 18;
2. **a reliability** -- and the artifact's values are 37.5 % measurement error, unreported;
3. **a specification** -- and the artifact's window, amplitude reference, contiguous-run requirement,
   derivative criterion and tail handling are all in the code and none in the file.

**Each support is measured, and each failure is quantified.** That is the contribution.

## 3. What remains before submission, ordered

| # | item | why it blocks | effort |
| --- | --- | --- | --- |
| **1** | **A specification set drawn from what analysts actually do** -- survey how published papers analyse this atlas and comparable matrices, and use those choices | **V2-C4's ceiling.** Without it the sensitivity range is this line's own five constructions, which is not a claim about practice | moderate |
| **2** | **A technical-versus-biological test for the between-animal spread of the effect**, by resampling pairs within animals | round 12 identified a **sampling** explanation for `I^2 = 57.3 %` and left it untested | small |
| **3** | **Each claim's figure, as source data plus a specification** -- not as a rendered figure | figures are prohibited by the plan's constraint, but **the manuscript cannot be assembled without knowing what each figure would show** | small |
| **4** | **An independent reviewer** on the frozen claim-evidence table | `PREFLIGHT_REVIEW.md` records that no independent review exists and that the one performed was a self-review | external |

**Items 2 and 3 are within this line's reach. Item 1 requires a literature step. Item 4 does not.**

## 4. The venue question, raised because it affects the claim wording

**The contribution is a quantified methodological audit of a published neurodata artifact.** **It is
neurodata methodology, not a machine-learning advance, and it is not a new biological finding.** **The
NMI Article category calls for a substantial novel research study, and the honest question is whether an
audit of this kind fits it.**

**Three candidates, with the claim wording each implies:**

* **NMI** -- requires the machine-intelligence angle to be foregrounded: **derived datasets as inputs to
  learned models, and what their unstated unit, reliability and specification do to the learned result.**
  **V2-C1 and V2-C4 carry that; V2-C3 does not.**
* **A methods venue** -- the claim is the audit procedure and its demonstration.
* **A specialist neuroscience venue** -- the claim is about this atlas specifically.

**This line cannot choose. It records that the choice changes the claim wording, and that the choice is the
owner's.**

## 5. The constraint tension, flagged rather than resolved

**The governing plan states: *"Do not write a new NMI abstract, main-text Results, Discussion or figures."*
The current instruction is to drive the work *"until it reaches NMI publication standard".***

**The constraint exists so that v2 does not pre-empt the v1/v2 integration decision, and it is honoured
here.** **What has been produced instead is everything a manuscript needs except the prose: a claim-evidence
table with ceilings, a defect ledger of eight self-found measurement defects and twelve self-inflicted check
failures, twenty scripts and eighteen machine-readable results, and this assessment.**

**What the owner must decide:** whether to lift the constraint so that a v2 manuscript can be drafted, or
whether the material is to be handed to a different drafting process. **Both are legitimate; this line
cannot take the decision because the constraint is the plan's.**

## 6. The pattern worth putting in the manuscript's own methods

**Across thirteen rounds, every measurement this line produced survived re-examination, and every
interpretation attached to a measurement was revised at least once. Two published interpretations were
retracted outright.**

**The failure mode is not the computation. It is the step from a number to a sentence about the number.**
**That is itself a finding about this kind of work, and it is the one this line is best placed to report,
because the record of it is retained rather than tidied:**
`anatomy/00_anatomy_vs_function_INVALID_idorder.py`,
`anatomy/05_common_mode_INVALID_percellnorm.py`,
`anatomy/11_source_rule_ATTEMPT1_scalarbug.py`,
`anatomy/12_inverse_variance_weighting.py`,
`anatomy/13a_icc_INVALID_zero_inflation.py`, and four `RESULT_*INVALID*.json` files.

**No other document in this repository shows its own discarded work. This one does, deliberately.**

## 7. Provenance and standing

* **All inputs, checksums and sources are recorded in `WIRESHIFT_STAGE1_DATA_AUDIT.md` and
  `WIRESHIFT_STAGE2_WT_AUDIT.md`; cumulative download about 675 MB against a 10 GB budget.**
* **No licence permitting redistribution of the derived records was found.** Analysis is unaffected;
  **a supplementary data deposit is currently not authorised.**
* **No model was fitted anywhere in this line.**
* **Verification tooling:** `../tools/check_artifacts.py`, with eighteen requirements passing at the time of
  writing, including three absence requirements.
