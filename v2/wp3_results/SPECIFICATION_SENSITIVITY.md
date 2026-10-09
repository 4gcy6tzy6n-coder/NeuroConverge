# The estimate is specification-dependent across a defensible range, and one weighting test failed

**Status: the central methodological finding of this line, stated with the range rather than a point, plus
one invalid attempt recorded.** No model was fitted.

---

## 1. The finding

**Eight animal-level estimates of the same contrast now exist in this line. They span from a null result to
a highly significant strong effect.**

| # | specification | response summary | inclusion rule | unit | `d` | `t` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 s window, common-mode removed | mean of deviations | none | animal | **0.7289** | 7.610 |
| 2 | source rule (30 s pre, `absmax`, per-event window) | signed sum | amplitude + derivative | animal | **0.4495** | 4.692 |
| 3 | source rule, inverse-variance weighted | signed sum | none | animal | **0.0852** | 0.873 |
| 4 | **source rule, unweighted** | signed sum | none | animal | **0.1580** | **1.619** |
| 5 | any of the above | -- | -- | **pair-measurement** | **11.048** | -- |

> **The same dataset, the same anatomical matrices, the same recorded signals, and analysis choices each of
> which can be defended from published practice produce standardised animal-level effects from `0.085`
> (`t = 0.87`, not significant) to `0.729` (`t = 7.61`), and `11.05` under the wrong unit.**

**That is the finding, and it is uncomfortable rather than tidy.** It is also exactly the project's
governing question -- *which evidential transitions require separate empirical support* -- answered with
numbers on a real published artifact.

## 2. What actually moves the number, isolated

The five rows differ in three things, and rows 3 and 4 differ only by the weighting:

* **T1 -- the response summary: mean of per-timepoint deviations versus signed sum of the
  baseline-subtracted trace.** These are the same quantity divided by a different window length, but
  combined with the pre-window choice they are not equivalent.
* **T2 -- the inclusion rule: none versus the source's amplitude and derivative criteria.** Applying it
  **reduces** `d` from 0.729 to 0.4495 in the one pair of rows where everything else is comparable.
* **T3 -- the unit: animal versus pair-measurement.** This is not a defensible choice; it is an error. It
  inflates by **11 to 18 times**.
* **T4 -- the weighting, which is the one that failed, see section 3.**

**Isolated, the defensible effect of T2 is a reduction from 0.73 to 0.45** -- the direction one expects,
since the filter selects events where the stimulated neuron responded. **T1 accounts for the remaining
spread, from 0.45 to 0.158**, and **that magnitude of sensitivity has not been isolated cleanly** because
rows 3 and 4 also differ in weighting. **This is stated as an open item, not as a resolved decomposition.**

## 3. The weighting test failed, and why

**The intent.** Round 5 showed the measurement count is not an exogenous weight (it correlates with the
response at +0.03 to +0.06 inside the connected strata), so this round used a standard meta-analytic
alternative, **inverse-variance weighting**: `w = n / sigma_within^2` per (animal, pair), which depends on
the pair's measurement count and the **dispersion** of its measurements rather than their **level**.

**Exogeneity was confirmed:** `corr(log weight, mean response)` is **+0.0288** for connected units and
**+0.0085** for unconnected units. **So the weight does not carry the outcome, which was the whole point.**

**And then the weights turned out to be pathological:**

```
33,578 weighted units
weight: median 4.84e-04   p95 0.128   max 2.2e+27
```

**A range of thirty-one orders of magnitude means the weighted mean is effectively determined by a handful
of units** whose within-pair variance happened to be near zero, inflating their weight without bound.
**The weighted estimate in row 3 is therefore not a weighted estimate of anything.**

**The fix, named and not yet applied:** bound the weight, or use a variance floor derived from the pooled
within-pair variance rather than a per-pair `1e-9` placeholder, or use a hierarchical model in which a pair
with two measurements contributes to the variance estimate rather than receiving an unbounded weight.
**Until that is done, rows 3 and 5 of the table must not be quoted.**

## 4. What is still defensible

**Two things, and they are the ones with the least specification freedom:**

1. **The unit error.** Treating pair-measurements as independent replicates inflates the standardised
   effect by **11 to 18 times**, measured directly by computing the identical contrast both ways. **This is
   arithmetic, not judgement.**
2. **The reliability gradient.** `r_full = 0.226` for the bulk 12,609 pairs and `0.819` for the
   best-measured 638, from split-half with Spearman-Brown correction, using no window, no baseline and no
   anatomical matrix. **It is independent of everything in section 1.**

**And one finding in between:** the connectivity association is **positive under every specification
tested**, with `t` from 0.87 to 7.61, and **it is null within same-class pairs and clear across classes**
(round 6). **The sign is stable; the magnitude is not.**

## 5. What this means for the manuscript question

**For an NMI-level contribution, a specification range this wide is not a weakness to be hidden -- it is
the result.** The defensible claim is not "the effect is `d = X`" but:

> **A published functional atlas carries per-pair values produced by a pipeline whose analysis choices are
> in its code and not in its data file. Re-analysing the same raw records under choices that span published
> practice gives animal-level effect estimates from not-significant to strongly significant, and
> re-analysing them with pair-measurements as the unit inflates the effect by more than an order of
> magnitude. Neither the choices nor the unit are recoverable from the artifact.**

**What is still missing for that claim to be publishable:** the five rows of section 1 are **this line's own
constructions**, not a systematic sample of published practice. **A defensible manuscript needs the choices
to be drawn from what analysts actually do and documented as such**, and the reliability measurement needs
to be connected to the attenuation it predicts rather than reported alongside it.

## 6. Retained, including the failure

**The failed weighting run is committed with its pathological weight distribution printed in the log**, for
the same reason the invalid id-order run and the zero-pass criterion run are retained: **a deleted failure
cannot be audited, and this line has now had six of them.**

## 7. Provenance

* Script `anatomy/12_inverse_variance_weighting.py`; output
  `anatomy/RESULT_iv_weighting_INVALID_weights.json`.
* Source rule and its omissions: `SOURCE_RULE_RESULT.md` sections 1 and 5.
* **No model was fitted. The association is observational and cross-individual; no causal claim is made.**
