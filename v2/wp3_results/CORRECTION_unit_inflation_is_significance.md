# CORRECTION: the pair-level quantity in V2-C1 is a z-score, not an effect size, and V2-C1 is inverted

**Status: this retracts V2-C1's wording. What pseudo-replication inflates is significance, not the effect
size, and the pair-level effect size is much smaller than the animal-level one.** No model was fitted.

**This is the eleventh self-found measurement defect in this line and the most serious: it concerns the claim
the line reports first and most often.** **It also shows that round 24's notation audit was incomplete.**

---

## 1. How this was found

**Round 26 established that a variance component obtained by subtraction must be reported with the
restriction under which it stays non-negative. Round 27 applied the same treatment to the line's other
numbers: trace every one to the line of code that produces it.**

**Tracing V2-C1's pair-level value found it.**

## 2. What the code actually computes

**`08_baseline_conventions.py`, lines 77 and 78:**

```python
d  = a.mean() - base.mean()
se = np.sqrt(a.var()/a.size + base.var()/base.size)
out[m][k] = {..., "d": float(d/se)}
```

**and `01_anatomy_vs_function.py`:**

```python
d  = m1.mean() - m0.mean()
sp = np.sqrt(m1.var()/m1.size + m0.var()/m0.size)
return label, ..., float(d/sp), ...
```

**Both divide the difference by the STANDARD ERROR. That is a z-score.** **The animal-level value comes from
`09_animal_level.py`:**

```python
cohens_d_paired = mean / sd        # diff over the SD of the across-animal differences
```

**That is a Cohen's `d`.**

**So V2-C1 divides a z-score by an effect size:**

```
z / d  =  (diff / SE) / (diff / SD)  =  SD / SE  =  sqrt(n_effective)
```

> **The ratio is `sqrt(n)`. It is not a measurement of inflation; it is the definitional consequence of the
> two denominators differing by the sample size.**

## 3. The measurement, with its limitation stated

**Both quantities were recomputed at both units from the same records, using the source convention
(`shift_vol = 60`, 24-volume post window, baseline from volumes 30 to 60, no common-mode removal and no
per-cell standardisation):**

| unit | difference | denominator | statistic | **Cohen's `d`** | n |
| --- | --- | --- | --- | --- | --- |
| **pair-measurement** | +0.45123 | SE 0.112983 | `z = 3.9938` | **0.0221** | 19,247 connected, 219,824 unconnected |
| **animal** | +0.62850 | SE 0.143050, SD 1.49349 | `t = 4.3935` | **0.4208** | 109 |

```
z_pair / t_animal              = 0.91      (a ratio of two significances)
d_pair / d_animal              = 0.0524    (a ratio of two effect sizes)
sqrt(n_effective)              = 188.1
```

**THE LIMITATION, STATED FIRST: this re-run does not reproduce the corpus's pair-level `z` of 11.048.**
**Its connected count matches exactly at 19,247, but its unconnected count is 219,824 against the corpus's
195,809, so the pair sets differ and the two z-scores are not comparable.** **What the re-run establishes is
structural: at the pair level, `diff/SE` and `diff/SD` differ by a factor of about `sqrt(n)`, so a value of
the former cannot be compared to a value of the latter regardless of the exact numbers.**

> **The specific numbers above are this re-run's, and the corpus's `z = 11.048` is not claimed to be wrong
> as a z-score. What is claimed is that it is a z-score.**

## 4. What this does to V2-C1

**V2-C1 as written:**

> *"Treating neuron-pair measurements as independent biological replicates inflates the standardised
> connectivity-function effect by 11 to 18 times."*

**Is withdrawn, and it is inverted.** **The pair-level effect size, expressed as a Cohen's `d`, is smaller
than the animal-level one -- 0.022 against 0.421, a factor of about 19 in the other direction.**

**What is true, and what the number 11.048 actually demonstrates:**

> **Treating pair-measurements as independent replicates inflates the SIGNIFICANCE, because the standard
> error is computed over 19,247 pair-measurements rather than 109 animals. The pair-level effect size is not
> inflated; it is diluted, because the pair-level standard deviation is dominated by the variability among
> 219,824 unconnected pair-measurements drawn from different cells across different animals.**

**And the inflation of significance is `sqrt(n)`, which is arithmetic rather than an empirical finding.**
**Stating it as an empirical result -- which the corpus did for four rounds -- presents a definitional
identity as a measurement.**

## 5. What survives of the pseudo-replication point

**The point itself survives, and it is the reason the line's animal-level analysis exists.**

**The line's own `TASK_SPEC_DRAFT.md` section 3.1 states that neuron pairs and frames are not independent
biological replicates.** **`ANATOMY_FUNCTION_RETEST.md` and every earlier document violated that, and the
animal-level analysis corrected it.** **That correction is right.**

**What was wrong was the metric used to describe the size of the error.** **The honest statement is not "the
effect was 15 times too large" but "the significance was computed over a sample 464 times larger than the
number of independent units, so the reported `p`-value corresponded to no real sampling distribution."**

## 6. The notation audit of round 24 was incomplete, and this is the fourth meaning

**Round 24 found two quantities sharing the symbol `d`.** **There are at least four:**

| # | meaning | definition | examples |
| --- | --- | --- | --- |
| **1** | **z-score** | `diff / SE` | **`RESULT_baseline_conventions.json` (11.0484, 4.6414, 13.7957), `RESULT_corrected.json` (1.4897, 4.7823)** |
| **2** | **between-animal Cohen's `d`** | `mean(diff) / SD(diff)` | `RESULT_animal_level.json` (0.7289), `RESULT_robust_class.json` (0.4145, 0.7690), `RESULT_source_rule.json` (0.4495) |
| **3** | **mean of per-animal standardised effects** | `mean` of each animal's own standardised contrast | `RESULT_per_animal_heterogeneity.json` (0.1165, 0.1019) |
| **4** | **inverse-variance weighted Cohen's `d`** | `m/s` of the per-animal differences | `RESULT_iv_weighting_INVALID_weights.json` (0.1580, 0.0852) |

**Round 24's conclusion -- that V2-C4's range of 0.085 to 0.729 is internally consistent -- is CORRECT and
stands, because all four of those values are meanings 2 or 4.** **What round 24 missed is meaning 1, which
appears in the pair-unit row that sits beside that range in `SPECIFICATION_SENSITIVITY.md` and in
`NOTATION_two_effect_sizes.md`'s list of `d_A` values.**

**So the pair-unit 11.048 is NOT a `d_A` value and its placement in that list is wrong.**

## 7. What is owed

1. **`NOTATION_two_effect_sizes.md` must gain meaning 1 and must remove 11.048 from its `d_A` list.**
2. **`SPECIFICATION_SENSITIVITY.md`'s row 5, `SOURCE_RULE_RESULT.md`'s pair row, and
   `ANIMAL_LEVEL_ESTIMATE.md`'s inflation-factor table all present the ratio `z/d` as an effect-size
   inflation and must carry correction notices.**
3. **Every other `d` in the corpus must be re-traced against section 6's four meanings, which this document
   has done for six result files and not exhaustively for all twenty-seven.**

## 8. Provenance

* Script `anatomy/24_unit_check.py`; output `anatomy/RESULT_unit_check.json`.
* Code citations: `08_baseline_conventions.py` lines 77-78, `01_anatomy_vs_function.py` the `compare`
  function, `09_animal_level.py` line 110.
* **The re-run's pair set differs from the corpus's, and that is stated rather than glossed.**
* **No model was fitted. No causal claim is made.**
