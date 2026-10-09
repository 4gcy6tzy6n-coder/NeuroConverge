# Technical covariates do not explain the effect's between-animal spread

**Status: a test that narrows the unexplained portion without eliminating it, and a multiplicity point
recorded rather than glossed.** No model was fitted.

---

## 1. The test

**Round 15 left about 40 % of the between-animal variance in the connectivity effect unexplained by
measurement noise (42.2 %) or pair composition (17.7 %).** **This asks whether a technical property of the
recording accounts for it. Every covariate is read from the per-animal files the atlas exported, so none
requires new data.**

**100 animals entered. The effect has mean +0.1172 and SD 0.1559 in this subset.**

| covariate | median | `corr` with effect | `r^2` | `p` |
| --- | --- | --- | --- | --- |
| recording duration (volumes) | 3,850 | +0.0939 | 0.009 | 0.353 |
| event count | 33 | -0.0737 | 0.005 | 0.466 |
| identified-cell count | 68.5 | **-0.2523** | 0.064 | **0.0113** |
| NaN fraction | 0.0228 | -0.0994 | 0.010 | 0.325 |
| median GCaMP level | 19.35 | +0.1906 | 0.036 | 0.058 |
| GCaMP interquartile range | 23.16 | +0.1772 | 0.031 | 0.078 |
| **fraction of identified cells in the connectome** | 0.9615 | **-0.2321** | 0.054 | **0.0202** |
| connected pairs per animal | 179 | **-0.2193** | 0.048 | **0.0284** |
| unconnected pairs per animal | 1,839 | **-0.2103** | 0.044 | **0.0358** |

**All nine together, in a multiple regression on standardised covariates:**

| quantity | value |
| --- | --- |
| animals | 100 |
| `R^2` | **0.0931** |
| **`R^2` adjusted for 9 degrees of freedom** | **0.0025** |

## 2. What it says

> **Nine technical covariates together account for 9.3 % of the between-animal variance in the effect, and
> after correcting for the nine degrees of freedom, 0.25 %.**

**So the technical explanation is not supported for this portion.** **More precisely: none of the technical
properties available in the exported files -- recording duration, event count, cell count, GCaMP level,
GCaMP variability, missingness, connectome coverage, or the counts of connected and unconnected pairs --
accounts for the unexplained spread.**

**The remaining candidates are unchanged and none is established: genuine per-animal biological
differences, an unmeasured technical factor, or an interaction between composition and pair-specific
animal deviation.**

## 3. The multiplicity point, recorded rather than glossed

**Four covariates reach nominal significance -- `n_cells` at `p = 0.0113`, `frac_in_connectome` at 0.0202,
`n_conn` at 0.0284 and `n_unconn` at 0.0358 -- with `r^2` between 0.044 and 0.064.** **With nine tests, a
Bonferroni threshold is `0.05/9 = 0.0056`, and none reaches it.** **A Benjamini-Hochberg pass at
`q = 0.05` also retains none, since the smallest `p` is 0.0113 against a first-rank threshold of
`0.05 x 1/9 = 0.0056`.**

**So the nominal significances are consistent with multiple testing and are not reported as findings.**
**This is stated because four `p`-values below 0.05 in a table invite exactly that misreading.**

**And the adjusted-`R^2` of 0.0025 settles it independently of any individual test:** with nine predictors
and 100 animals, an in-sample `R^2` of 0.093 is what one expects from noise alone.

## 4. The revised accounting

| component of the effect's between-animal variance | share | source |
| --- | --- | --- |
| **measurement noise** | **42.2 %** | round 14, `var(m1-m2)/4` |
| **pair composition** | **17.7 %** | round 15, `R^2` of the leave-one-animal-out prediction |
| **nine technical covariates** | **0.25 %** | this round, adjusted `R^2` |
| **unexplained** | **about 40 %** | remainder |

**The unexplained portion is now narrower in what it can be, without being assigned.**

## 5. What this does and does not change

**Changes.** The technical explanation for the unexplained 40 % is **substantially weakened**: the
available technical properties are not it. **A reader who assumed "different animals just have different
GCaMP levels" must now account for the fact that GCaMP level explains 3.6 % of the effect's variance and
does not survive multiplicity.**

**Does not change.** Nothing in sections 1 to 3 alters:
**V2-C1** (the 11-to-18-fold unit inflation, arithmetic);
**V2-C2** (the Fig-6 reproduction and its `r = 0.208` bound);
**V2-C3** (the three-level pair-level decomposition, whose result stands);
or the round-14 reliability measurement (`r_full = 0.5266`, signal share 0.578).

**And this does NOT support a biological explanation for the 40 %.** **It removes one class of
explanation, not more.** **Absence of a technical explanation is not presence of a biological one**, which
is the same error this line retracted in round 12.

## 6. What remains owed

1. **A specification set drawn from what analysts actually do** -- V2-C4's ceiling, and the only item with
   no partial result.
2. **The pair-set-matched comparison** -- restrict every animal to the same commonly measured pairs, so
   composition is held exactly constant.
3. **Each claim's figure as source data plus a specification.**
4. **An independent reviewer.**

## 7. Provenance

* Script `anatomy/19_technical_covariates.py`; output `anatomy/RESULT_technical_covariates.json`.
* Read-out, pre-window and analysis-window conventions as in `SOURCE_RULE_RESULT.md`.
* Multiplicity: Bonferroni `0.05/9` and Benjamini-Hochberg at `q = 0.05` both applied; neither retains a
  covariate.
* **No model was fitted. No causal claim is made.**
