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

## 3. What remains before submission, ordered, as of round 80

**Three of the four items this section listed have been done, and the list is rewritten rather than annotated.**

| # | item | status |
| --- | --- | --- |
| **1** | a specification set drawn from what analysts actually do | **DONE, two ways.** Internally, `SPECIFICATION_LEDGER.md` measures seven dimensions and an eighth redundant one. Externally, a pre-registered census of all 129 citing records measured the reliability-reporting rate, and two documentation inspections coded two further published matrices. |
| **2** | a technical-versus-biological test for the between-animal spread | **DONE.** The three-level decomposition separates measurement error from pair composition, and nine technical covariates account for 0.25 per cent adjusted. A simulation under a known truth validates the estimator. |
| **3** | each claim's figure | **DONE.** Six figures are rendered into `../figures/`, each verified by resolving its declared source, with a render manifest recording the script hash and the commit. |
| **4** | an independent reviewer | **STILL OWED.** `PREFLIGHT_REVIEW.md` records that the review performed is this line's own. Three further reports exist under `review/`, generated in isolated contexts under a three-lens protocol; **their role separation is a separation of EMPHASIS and not of error processes, so they are a self-review and are not independent.** **One of them found the failed joint-grid check that sections 2.2 and 2.7 now disclose, which is what the protocol was for, and it does not make the review independent.** |

**So one item remains, and it is not within this line's reach.**

## 4. The venue question, which is the only decision still outstanding

**The contribution is a quantified methodological audit of a published neurodata artifact.** **It is neurodata
methodology, not a machine-learning advance, and it is not a new biological finding.**

**Three candidates, with the claim wording each implies, and with what each would now require:**

* **NMI. Foregrounds derived datasets as inputs to learned models and what their unstated unit, reliability and
  specification do to the learned result.** **WHAT IT REQUIRES: a demonstration. An isolated reviewer put it
  exactly: the manuscript "opens with the consequence for learned models and returns to it in the discussion,
  but no model is fitted and no consequence for any learned result is measured. The claim is asserted in the
  register of a result three times and demonstrated zero times."** **That demonstration is new work and would
  only be worth doing for this venue.**
* **A methods venue. The claim is the audit procedure and its demonstration.** **WHAT IT REQUIRES: the
  machine-intelligence framing in section 1 cut to a sentence, and the title and abstract scoped to this
  artifact and this class of artifact. Both are mechanical.** **The measurements, the ledger, the census and the
  simulation all stand as they are.**
* **A specialist neuroscience venue. The claim is about this atlas specifically.** **WHAT IT REQUIRES: the same
  rescoping, with less emphasis on the general procedure.**

**This line cannot choose, because the choice changes the CLAIM and not the wording, and because the answer
determines whether the largest remaining piece of work should be done at all.**

## 5. The constraint, and how it was resolved

**The governing plan stated: *"Do not write a new NMI abstract, main-text Results, Discussion or figures."***
**On the owner's instruction of round 58 the constraint was LIFTED for the v2 line, and the crossing is recorded
as a dated amendment in `../manuscript/AMENDMENT_constraint_lifted.md` with the declaring document left
intact, as this workspace requires.**

**What the lift authorised and what it did not are stated in that amendment.** **It did not authorise any edit to
the frozen v1, any change to a v2 measurement, or the reinstatement of any withdrawn claim.** **The manuscript
states its own withdrawals in one place, in section 2.8, including the four that appear nowhere else in the
draft.**

**And what the lift produced is now a complete draft rather than a claim-evidence table: 683 lines, six
figures, nine references verified by resolving each DOI to a record, an authorship and competing-interest
statement, and a data and code availability statement that records what cannot be deposited and why.**

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
