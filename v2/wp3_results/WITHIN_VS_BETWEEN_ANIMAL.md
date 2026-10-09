> **STATUS: INTERPRETATION SUPERSEDED (round 12).** This document is retained unaltered as the
> record of a reading that was later withdrawn or narrowed: **the animals differ rather than the measurements being noisy**. The measurements in it stand;
> the interpretation does not. **Superseded by [`CORRECTION_heterogeneity_is_noise.md`](CORRECTION_heterogeneity_is_noise.md)**, which takes precedence and records
> that see the appended notice; the measurements stand and the interpretation is withdrawn.
>
> **The title above still states the superseded reading, deliberately, so the document remains findable
> by the claim it made.** Read the body as a dated record and the linked document as current.

---

# Within-animal reproducibility versus cross-animal agreement, and a bug that invalidates the ICC

**Status: one finding is sound and important; one computation is buggy and its result is withdrawn before
it was ever claimed.** No model was fitted.

---

## 1. The sound finding

**Split-half reliability of the per-pair functional response, computed two ways on the same 112 animals,
3,333 events and 29,395 pairs:**

| what is split | units | `r` | **`r_full`** (Spearman-Brown) |
| --- | --- | --- | --- |
| **the repeated measurements of a pair WITHIN one animal** | 33,578 | 0.3535 | **0.5223** |
| **the animals in which a pair was measured** (pairs in >= 4 animals) | 15,189 | 0.0206 | **0.0405** |

> **A neuron pair's functional response is moderately reproducible when the same animal is measured
> again, and essentially unreproducible across animals.**

**This is a different statement from the one this line has been carrying since round 1, and it is a better
one.** Round 1 reported "the atlas's per-pair reliability is `r_full = 0.226` for the bulk of pairs". That
number was a **cross-animal** split-half. **Read alone it suggests measurement noise. Read against the
within-animal figure, it says something else: the measurements are not noisy, the animals differ.**

**And that changes what the atlas is.** A per-pair value in a 300 x 300 matrix built from 113 animals is a
**mean over a population**, and on this evidence the population is heterogeneous at the level of individual
pairs. **The atlas entry is therefore not a fixed property of the circuit, and how well it describes any
one animal is not recoverable from the atlas.**

**Why this matters for the evidential-transition question.** The transition from "a per-pair value measured
in 113 animals" to "a property of the *C. elegans* connectome" assumes the pairs are **exchangeable** across
animals. **The two `r_full` values measure how badly that assumption fails at the level of a single pair,
and they are the first numbers this line has produced that bear directly on an assumption rather than on a
statistic.**

## 2. The bug, found before the claim was made

**A variance decomposition was computed to express the same thing as an intraclass correlation, and it
returned ICC = 0.9311.** Two checks made it untrustworthy before it was used:

**Check 1 -- per-animal centering changed nothing.**

| version | ICC |
| --- | --- |
| raw | 0.9311 |
| per-animal centred | **0.9311** (identical to four decimals) |
| per-animal standardised | 0.9061 |

**Centring by animal must change the between-animal term**, because it subtracts a different constant per
animal. **Identity to four decimals is a bug signature, not a result.**

**Check 2 -- the cause.** The within-animal term was computed as

```python
ws = [np.var(vs) if len(vs) > 1 else 0.0 for vs in arms.values()]
```

**and the majority of (animal, pair) units contain exactly ONE measurement** -- median 1, p90 2, maximum 5
-- because each stimulation targets a single neuron, so a given ordered pair is usually measured once per
animal. **Those units contribute a hard zero to the within-animal variance.** **`mean(W) = 7.32e4` is
therefore a mean over a vector that is mostly zeros, and `ICC = mean(B)/(mean(B)+mean(W))` is inflated by
construction.**

> **The ICC of 0.9311 is withdrawn. It was never published as a finding, and the reason it is recorded here
> is that it came within one step of being published as one.**

**The correct computation** requires either a mixed model in which a unit with one observation contributes
to the residual variance rather than to a zero, or restriction to pairs where both components are
estimable in every animal. **Neither has been run.**

## 3. What is and is not established

**Established:**

* **Within-animal `r_full = 0.5223`, cross-animal `r_full = 0.0405`**, both from proper split-halves with
  Spearman-Brown correction, on 33,578 and 15,189 units respectively.
* **The measurement structure:** per (animal, pair) the measurement count is median **1**, p90 **2**,
  maximum **5**; per pair pooled over animals, 29,395 pairs with 15,189 measured in at least four animals.
  **So the atlas's replication is overwhelmingly ACROSS animals, not within.**
* **The round-1 reliability gradient is unaffected** but now needs re-reading: it measures cross-animal
  agreement, so its low value for the median pair reflects animal heterogeneity as much as anything.

**Not established:**

* **The ICC.** Withdrawn, section 2.
* **That the heterogeneity is biological rather than technical.** Animal-level differences in GCaMP
  expression, dissection quality, age or indicator state would produce cross-animal disagreement with no
  pair-specific biology. **The per-animal standardisation (ICC 0.9061 from the same buggy estimator) is not
  a valid test of this**, and a proper one has not been run.
* **Whether the heterogeneity is pair-specific at all.** That is exactly what a corrected variance
  decomposition or mixed model must answer, and it is now the natural next step.

## 4. The consequence for the manuscript question

**Round 8 concluded that the effect estimate is specification-dependent across a defensible range.** This
round adds a second, independent axis: **the quantity being estimated may not be a property of the
circuit at all.**

**If a pair's response differs across animals by more than it agrees, then "the connectivity-function
association" is an association between a connectome from one animal and a response averaged over 113
others, and `d = 0.45` is a population-average association whose per-animal value has not been estimated.**
**That is a stronger and more specific statement than a sensitivity range, and it is testable: the
association can be computed per animal and its distribution examined.**

**That is the next step, and it is bounded.**

## 5. Defect ledger update

**This is the seventh self-found defect in this line and the first found by a self-consistency check rather
than by an anomaly.** The check was: *does an operation that must change a term actually change it?*
**Centring by group is such an operation, and it did not.**

**The five earlier implementation defects in the criterion, the id-order error, the scalar collapse, the
zero-pass run, the 1e11 blow-up and the pathological weights are all retained in the repository.** **So is
this one, with the ICC value printed so that it cannot be reused without the reason it is wrong.**

## 6. Provenance

* Scripts `anatomy/13_measurement_structure.py` (within versus between split-half, sound) and
  `anatomy/13a_icc_INVALID_zero_inflation.py` (the buggy variance decomposition, retained with an INVALID
  marker).
* Read-out and inclusion conventions as in `SOURCE_RULE_RESULT.md`.
* **No model was fitted. The association is observational and cross-individual; no causal claim is made.**
---

> **INTERPRETATION RETRACTED, appended 2026-10-09.** The reading in this document -- that the animals
> differ rather than the measurements being noisy -- is **withdrawn**. A three-level decomposition
> separating a homogeneous animal offset, a pair-specific animal deviation and within-cell measurement
> error gives **5.5 % pair-specific animal deviation against 37.5 % measurement error**, so the low
> cross-animal agreement is better explained by unreliable pair means than by heterogeneous biology. See
> [`CORRECTION_heterogeneity_is_noise.md`](CORRECTION_heterogeneity_is_noise.md), which takes precedence.
> **The measurements in this document are unaffected; the interpretation is.** The text is left unaltered.
