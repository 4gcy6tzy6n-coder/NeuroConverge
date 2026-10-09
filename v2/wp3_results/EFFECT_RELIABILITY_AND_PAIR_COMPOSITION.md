> **STATUS: INTERPRETATION SUPERSEDED (round 15).** This document is retained unaltered as the
> record of a reading that was later withdrawn or narrowed: **what is reproducible is which pairs were measured**. The measurements in it stand;
> the interpretation does not. **Superseded by [`PAIR_COMPOSITION_TEST.md`](PAIR_COMPOSITION_TEST.md)**, which takes precedence and records
> that pair composition accounts for only 17.7 % of the between-animal variance, with 42.2 % measurement noise and about 40 % unexplained, so the composition account is directionally right and quantitatively overstated.
>
> **The title above still states the superseded reading, deliberately, so the document remains findable
> by the claim it made.** Read the body as a dated record and the linked document as current.

---

# The effect is about 55 % reproducible within an animal, and that reproducibility is pair composition

**Status: one measurement, one self-caught factor-of-two error, and a synthesis that reconciles round 12's
correction with round 10's heterogeneity.** No model was fitted.

---

## 1. The measurement

**Per-animal split-half reliability of the connectivity effect itself.** Within each animal, its stimulus
events are randomly halved, the connected-minus-unconnected contrast computed from each half, and the two
halves' effects correlated across animals (Spearman-Brown corrected).

| quantity | value |
| --- | --- |
| animals with enough events | **98** |
| correlation between the two halves' effects | `r = 0.3574` |
| **reliability, corrected to full length** | **`r_full = 0.5266`** |
| half 1 effect | mean +0.1314, SD 0.1989 |
| half 2 effect | mean +0.1049, SD 0.1737 |
| across-animal SD of the full-data effect | 0.1634 |
| SD of the half-difference | 0.2122 |

**And the same quantity from a variance ratio, computed correctly:**

| quantity | value |
| --- | --- |
| noise variance of the full effect, `var(m1 - m2)/4` | 0.011261 |
| total variance of the full effect | 0.026694 |
| **noise share** | **0.4218** |
| **signal share** | **0.5782** |

> **Two independent estimates of the same quantity: `r_full = 0.5266` from the split-half correlation, and
> a signal share of `0.5782` from the variance ratio. They agree to within 0.05.**

## 2. The error caught before it was reported

**The first version computed the noise variance as `var(m1 - m2)/2` and returned a signal share of 0.1563.**
**That is inconsistent with `r_full = 0.5266`, and the inconsistency is what exposed it.**

**The algebra:**

```
var(m1 - m2) = var(m1) + var(m2)                     (independent halves)
             = 2 * var(half-data effect)
             = 2 * 2 * var(full-data effect)          (a half has half the data, so twice the variance)
             = 4 * var(full-data effect)
```

**So the divisor is four, not two, and the first version understated the signal by a factor of two.**
**Corrected: 42.2 % noise, 57.8 % signal.**

**This is the ninth self-found measurement defect in this line, and the first caught by an internal
consistency check against an independent estimate rather than by an anomaly or a self-consistency probe.**
**It is also the reason section 1 reports both estimators: they check each other.**

## 3. The synthesis, which reconciles two rounds that appeared to disagree

**Round 10 measured `I^2 = 57.3 %` for the between-animal spread of the effect and read it as animal
heterogeneity. Round 12 corrected that, on a three-level decomposition giving only 5.5 % pair-specific
animal deviation, to a sampling explanation. This section says the effect is 55 % reproducible within an
animal -- which looks like support for round 10.**

**All three are right, and they measure different things:**

* **The effect is reproducible within an animal (`r_full = 0.527`)** -- **because every one of that animal's
  stimulus events draws on the same set of measured pairs.** The pair composition is fixed within an animal.
* **A pair's response has only 5.5 % pair-specific animal deviation** (round 12) -- so a given pair behaves
  similarly across animals once a homogeneous animal offset and measurement error are removed.
* **Therefore what is reproducible within an animal is WHICH PAIRS IT HAPPENED TO HAVE MEASURED**, not a
  biological property of the animal's circuit.

> **The effect's per-animal value is stably determined by that animal's pair composition. That is
> reproducible and it is not biology.**

**This is the sharpest form of the statement this line can currently make, and it is testable:** **restrict
the effect to pairs measured in many animals, so that pair composition is held roughly constant, and see
whether the between-animal spread survives.** **That test has not been run.**

## 4. What the numbers now say, in one place

| level | within-animal `r_full` | decomposition |
| --- | --- | --- |
| **a pair's response** | 0.5223 (round 9) | 55.1 % between pairs, 37.5 % measurement error, 5.5 % pair-specific animal, 1.9 % animal offset (round 12) |
| **the connectivity effect** | **0.5266** | **42.2 % noise, 57.8 % signal** |

**The two reliabilities are almost identical, 0.5223 and 0.5266.** **The effect inherits the reliability of
the pair responses it is computed from, which is what one expects and is a consistency check the line did
not previously have.**

## 5. What is still owed, unchanged in order

1. **A specification set drawn from what analysts actually do** -- V2-C4's ceiling.
2. **The pair-composition control named in section 3** -- restrict to pairs measured in many animals.
3. **Each claim's figure as source data plus a specification.**
4. **An independent reviewer.**

**Items 1 and 3 are now the only ones with no partial result.**

## 6. Provenance

* Script `anatomy/17_effect_reliability.py`; output `anatomy/RESULT_effect_reliability.json`.
* Read-out, pre-window and analysis-window conventions as in `SOURCE_RULE_RESULT.md`.
* **No model was fitted. No causal claim is made.**
---

> **WITHDRAWN IN PART, appended 2026-10-09.** This document states that *"what is reproducible within an
> animal is WHICH PAIRS IT HAPPENED TO HAVE MEASURED, not a biological property of the animal's circuit"*.
> **The measurement in [`PAIR_COMPOSITION_TEST.md`](PAIR_COMPOSITION_TEST.md) shows pair composition
> accounts for only 17.7 % of the between-animal variance**, with 42.2 % measurement noise and about 40 %
> unexplained. The composition account is therefore **directionally right and quantitatively overstated**.
> **The reliability measurement here (`r_full = 0.5266`, signal share 0.578) is unaffected; only the
> interpretation of where that signal comes from is.** The text is left unaltered.
