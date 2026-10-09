# CORRECTION: the heterogeneity is mostly measurement noise, not animal-specific biology

**Status: this retracts the interpretation given in rounds 9 and 10, on the strength of a decomposition that
separates the components the earlier analyses could not.** No model was fitted.

**This is the eighth self-found defect in this line and the most consequential: an attribution of
measurement noise to biology.**

---

## 1. What is retracted

**Round 9** reported cross-animal `r_full = 0.04` against within-animal `r_full = 0.52` and concluded:

> *"the measurements are not noisy, the animals differ"*, and *"a per-pair value ... is a mean over a
> population, and that population is heterogeneous at the level of individual pairs"*.

**Round 10** built on it, concluding that the connectivity-function association is *"a property of the
population, not of the circuit"*.

**Both attributions are withdrawn, or at least substantially weakened.** The decomposition below shows that
**only 5.5 % of the variance in a pair's response is pair-specific animal deviation, while 37.5 % is
within-cell measurement error.** **The low cross-animal agreement is therefore better explained by
unreliable pair means than by heterogeneous biology.**

## 2. The decomposition, and why it identifies what the earlier attempt could not

**Model:** `y[a,p,i] = mu + alpha[a] + beta[a,p] + eps`, over 192,303 (animal, pair) units.

* **`alpha[a]`** -- a homogeneous animal offset: GCaMP level, dissection quality, baseline scale.
* **`beta[a,p]`** -- a **pair-specific** animal deviation. **This is the biological heterogeneity of interest.**
* **`eps`** -- within-cell measurement error.

**The identification that round 9 got wrong.** Most (animal, pair) cells hold **one** measurement, so `beta`
and `eps` are not separable there. **Round 9 treated those cells as contributing a hard zero to the
within-animal variance, which inflated the ICC to 0.93.** **The correct treatment is to estimate `eps` from
the cells that DO have repeats, and subtract it.**

**Result, in log space** (the responses span `-3.5e5` to `2.5e5` in raw units, so a linear decomposition is
dominated by extremes):

| component | variance | share |
| --- | --- | --- |
| **between pairs** | 9.056 | **55.1 %** |
| **`eps`, within-cell measurement error** | **6.166** | **37.5 %** |
| **`beta`, pair-specific animal deviation** | **0.900** | **5.5 %** |
| **`alpha`, homogeneous animal offset** | 0.307 | 1.9 % |
| total | 16.430 | 100 % |

**`eps` was estimated from 38,003 units with two or more measurements.**

## 3. What this means

**Three readings follow, and they replace the retracted one:**

1. **Pairs genuinely differ from one another** -- 55 % of the variance. That is the real signal, and it is
   what makes any connectivity-function association possible at all.
2. **Measurement error is large** -- 37.5 %. **A single measurement of a pair is a poor estimate of that
   pair's value, which is exactly why cross-animal agreement is low.**
3. **Pair-specific animal biology is small** -- 5.5 %. **A pair's response does not differ much between
   animals beyond what a homogeneous animal offset and measurement error explain.**

> **The corrected statement: cross-animal disagreement in this atlas is driven mainly by measurement error
> in the pair means, not by animal-specific circuit biology. The round-9 and round-10 framings inverted
> that.**

**And the round-10 `I^2 = 57.3 %` for the per-animal effect needs re-reading too.** With pair-specific
animal deviation at only 5.5 %, **the between-animal spread of the effect cannot be mostly biological.**
Its likely sources are **(a) which pairs each animal happened to have measured** and **(b) the
pair-level spread of 55 % combined with that sampling** -- **not** animal-specific circuit differences.
**That is a sampling explanation, and it is testable by resampling pairs within animals, which has not been
done.**

## 4. What survives unchanged

**Two results are untouched, because they do not depend on this decomposition:**

* **The unit error.** Treating pair-measurements as independent replicates inflates the standardised effect
  by **11 to 18 times**. **Arithmetic.**
* **The like-for-like comparison of round 11.** The source's Fig-6 comparison reproduces at `r = +0.037`
  and `-0.006`, and the target's cross-animal agreement is `r = 0.208` on the 23 shared cells. **If anything
  this decomposition makes that measurement MORE important**, because it says the target is unreliable for
  a reason that is measurable.

**And one thing is reinforced:** **the round-1 reliability gradient is now explained rather than merely
reported.** `r_full = 0.226` for the bulk of pairs is low **because `eps` is large relative to the number of
measurements per pair** -- not because the atlas is conceptually wrong and not because animals differ.

## 5. The honest position of the line

**After twelve rounds the defensible results are:**

1. **The unit error: 11 to 18 times inflation.** Arithmetic.
2. **The source's Fig-6 comparison reproduces, and its target has cross-animal reliability 0.21 on the
   cells available.** A like-for-like boundary on a published comparison.
3. **A three-component decomposition: 55 % between pairs, 37.5 % measurement error, 5.5 % pair-specific
   animal deviation.** **The measurement-error share quantifies a limitation of the published atlas that
   the atlas does not report.**
4. **The specification sensitivity: `d` from 0.085 to 0.729 across defensible choices**, because the
   choices live in the pipeline's code and not in its data file.

**And the results that are now withdrawn or weakened:**

* **"The animals differ, not the measurements"** -- **withdrawn, section 1.**
* **"Population-level regularity, not a circuit property"** -- **weakened: the between-animal spread is
  better explained by which pairs were sampled than by biology.**
* **The ICC of 0.93** -- **withdrawn in round 9.**

**This is a thinner scientific result than the previous round claimed, and it is the accurate one.** The
contribution that remains is a **quantified account of what a published atlas's per-pair values can support
and why**, with three independent measurements -- unit, reliability decomposition, and specification -- plus
one like-for-like reproduction and its bound. **It is methodological, it is honest, and it is smaller than
"the circuit is heterogeneous".**

## 6. Defect ledger update

**Eighth self-found defect, and the first that required retracting a published interpretation twice in the
same line.** The seven earlier ones: duplicate-name pooling, ratio-of-medians, a biased read-out statistic,
an invalid id-order assumption, per-cell collapse to scalars, a broadcast error, a zero-pass criterion run,
weights spanning thirty-one orders of magnitude, and the zero-inflated ICC. **All retained.**

**The pattern across twelve rounds is now unambiguous and worth stating in the manuscript's own methods:
every measurement this line has produced has survived re-examination, and every interpretation attached to
a measurement has been revised at least once.** **The failure mode is not the computation. It is the step
from a number to a sentence about the number.**

## 7. Provenance

* Script `anatomy/16_three_level_variance.py`; output `anatomy/RESULT_three_level_variance.json`.
* The retracted documents -- `WITHIN_VS_BETWEEN_ANIMAL.md` and `POPULATION_LEVEL_NOT_CIRCUIT_PROPERTY.md` --
  are **left unaltered with a correction notice appended**, taking precedence.
* **No model was fitted. No causal claim is made.**
