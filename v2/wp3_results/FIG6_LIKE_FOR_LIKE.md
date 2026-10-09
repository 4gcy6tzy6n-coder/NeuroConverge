# The like-for-like comparison: the source's own Fig-6 comparison, reproduced and bounded

**Status: the manuscript-readiness item that was blocking is done. The source's central anatomy-versus-function
comparison is reproduced from its own data, and its interpretation is bounded by a reliability measurement
the source does not report.** No model was fitted. No causal claim is made.

---

## 1. What the source claims, and where its data is

**Verbatim from the paper:** *"A matrix of bare anatomical weights (synapse counts) was a **poor predictor**
of the correlations of spontaneous activity (left bar, Fig. ...)"*. **So the comparison is
`corr(synapse count, activity correlation)`, and it is not model-based.**

**The spontaneous-activity data for that figure is in the same OSF record this line has been using:
`spont_data_fig6.zip`, 2,402,185 B, and `spont_data_fig6_raw.zip`, 1,114,732 B.** Both downloaded this
session. **They contain TWO animals.**

| animal | recording | `gcamp` shape | duration | strictly-unique named cells |
| --- | --- | --- | --- | --- |
| 0 | `pumpprobe_20220522_171720` | (1200, 87) | 599.5 s | 61 |
| 1 | `pumpprobe_20220522_140320` | (1270, 94) | 634.5 s | 41 |

**Same date, same session prefix, two animals.**

## 2. The reproduction

Anatomical matrix built **by name** from both source tables: 346 names, 3,581 non-zero chemical and 1,459
non-zero gap-junction entries. **Activity correlation matrix per animal, over cells that are uniquely named
and have usable variance. The comparison is over off-diagonal pairs.**

| animal | pairs | **`corr(synapse count, activity correlation)`** | `corr(log1p(synapse), activity)` |
| --- | --- | --- | --- |
| 0 | 3,540 | **+0.0368** | +0.0460 |
| 1 | 1,560 | **-0.0064** | +0.0513 |

> **The source's claim reproduces: both animals give a correlation near zero. `r = +0.037` and `r = -0.006`.**

**Two observations about that reproduction, both recorded rather than smoothed:**

* **The two animals differ in sign.** With `n = 2`, the claim "poor predictor" is the average of two
  near-zero estimates of opposite sign. **That supports the claim and cannot distinguish "consistently
  near zero" from "variable".**
* **The log-transformed comparison is positive in both, +0.046 and +0.051**, so the near-zero linear result
  is not an artefact of the heavy-tailed synapse-count distribution.

## 3. The measurement that bounds the interpretation

**The quantity being predicted is itself only weakly reproducible across these two animals.** Restricted to
the **23 cell names shared by both**, the off-diagonal activity-correlation matrices agree at

> **cross-animal `corr = +0.2084`** (pairwise-correlation SD 0.199 in animal 0 and 0.235 in animal 1).

**So the source's left bar measures anatomy against a target whose own cross-animal reliability is about
0.21.** Anatomy is a fixed matrix; the target is not. **Under classical test theory the observed association
is therefore attenuated by roughly `sqrt(0.208) = 0.456`, implying a true association near
`0.037 / 0.456 = 0.081`.**

**Still small. But the point is not the corrected magnitude — it is that the comparison, as published,
measures anatomy against a quantity that differs between animals and is reported from two of them.**

## 4. The statement this supports

> **The source's finding that anatomical weights are a poor predictor of spontaneous-activity correlation
> structure is reproduced, in both of its two animals (`r = +0.037` and `-0.006`). What the two-animal
> comparison cannot establish is that anatomy fails to predict *the circuit's* correlation structure,
> because the correlation structure is itself only `r = 0.208` reproducible across animals on the 23 cells
> they share. Anatomy is a poor predictor of a given animal's activity correlations, and the target varies
> between animals by more than the predictor explains.**

**This is different from, and weaker than, "the source is wrong". It is a boundary on what the published
comparison can support, and it is measured rather than asserted.**

## 5. Why this completes the blocking item

**Round 10 named three things needed before this line is a manuscript. The first was a like-for-like
comparison against the source's own reported quantity, on the grounds that without it the manuscript would
assert that the atlas cannot support a circuit-property claim while never engaging the claim the atlas
actually makes.**

**That comparison is now done, on the source's own data for its own figure, and it does two things at
once:**

1. **It reproduces the source's result** — so this line is not in the position of contradicting a paper it
   has not checked.
2. **It bounds that result** with a reliability measurement on the very quantity compared, which the source
   does not report.

**And it connects to the 109-animal finding directly.** Round 10 measured `I^2 = 57.3 %` across 109 animals
for the perturbation-based association. **This section measures the analogous thing for the
spontaneous-activity side: the correlation structure is animal-specific.** **The two measurements are on
different read-outs but point the same way, and together they are the manuscript's argument rather than
either alone.**

## 6. What remains owed

1. **The remaining two items from round 10**: a mixed model allowing a **heterogeneous** animal effect, and
   a specification set drawn from what analysts actually do rather than this line's own constructions.
2. **`n = 2` is a hard limit of this comparison.** It cannot be extended within this record: the OSF
   spontaneous-activity data contains two animals. **Whether the source has more that was not deposited is
   `UNKNOWN` and is stated as such.**
3. **The 23-cell overlap is small.** It is what the two animals share after the strictly-unique-name filter,
   and it is the only basis on which the two correlation matrices can be compared. **A larger overlap would
   strengthen section 3 and is not available here.**

## 7. Provenance

* Scripts `anatomy/15_fig6_reproduction.py`; output `anatomy/RESULT_fig6.json`.
* Data: OSF `10.17605/OSF.IO/E2SYT`, files `spont_data_fig6.zip` (2,402,185 B) and
  `spont_data_fig6_raw.zip` (1,114,732 B).
* Source claim: Europe PMC full text of PMC10632145, quoted verbatim in section 1.
* **Cumulative download by this line: about 675 MB, well inside the 10 GB budget.**
* **No model was fitted.**
