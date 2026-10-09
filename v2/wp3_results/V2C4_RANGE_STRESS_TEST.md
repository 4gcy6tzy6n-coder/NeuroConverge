# V2-C4's range sits in a specification family this grid does not cover, and its inclusion axis is redundant

**Status: a grid over V2-C4's choices, which found that the axis V2-C4's own table lists does nothing in this
dataset, and that the grid's ceiling is 0.44 while V2-C4's ceiling is 0.73 because of a step no grid here
varies.** No model was fitted.

---

## 1. What was asked and why

**V2-C4 was the last live claim never stress-tested.** **Rounds 24 and 28 verified that all four of its values
are Cohen's `d`, which is a notation check.** **Nobody had asked whether the range `0.0852` to `0.7289` is the
range a declared specification grid produces.**

**Round 29 had shown that adding read-outs widened a similar range by 18 points, so the expectation was that
this range would widen.**

## 2. Two decisions taken before running, both recorded

**The read-out axis was dropped before the grid was run.** **If `val_mean = val_sum / post` then
`d_A = diff/SD` is unchanged, because a global scale factor cancels in a ratio.** **So `sum` and `mean` cannot
produce different `d_A` values, and including both would have doubled the table with no new specification.**
**This is round 30's redundancy lesson applied beforehand rather than after.**

**The data are loaded once and cached.** **The first attempt reloaded 113 files totalling 1.2 GB for each of 48
cells and had completed none after two minutes.** **It is retained as `27_v2c4_grid_ATTEMPT1_reload.py`.**

## 3. The grid

**Axes: post-stimulus window of 12, 24 and 48 volumes; baseline from volumes 30 to 60 or 0 to 60; per-cell
normalisation by the cell's own pre-stimulus SD or none; and inclusion requiring at least 10 connected and 50
unconnected pairs per animal or none.**

**All 24 cells give 109 animals.**

| post | baseline | cell norm | `d_A` | `t` |
| --- | --- | --- | --- | --- |
| 12 | 30-60 | none | 0.2218 | 2.32 |
| 12 | 30-60 | **pre-SD** | 0.1404 | 1.47 |
| 12 | 0-60 | none | 0.2044 | 2.13 |
| 12 | 0-60 | **pre-SD** | 0.1382 | 1.44 |
| 24 | 30-60 | none | **0.3998** | 4.17 |
| 24 | 30-60 | **pre-SD** | 0.1083 | 1.13 |
| 24 | 0-60 | none | 0.4052 | 4.23 |
| 24 | 0-60 | **pre-SD** | 0.1080 | 1.13 |
| 48 | 30-60 | none | 0.4114 | 4.29 |
| 48 | 30-60 | **pre-SD** | 0.1015 | 1.06 |
| 48 | 0-60 | none | **0.4408** | 4.60 |
| 48 | 0-60 | **pre-SD** | 0.1013 | 1.06 |

```
this grid's d_A:  0.1013 to 0.4408, range 0.3395
V2-C4's reported: 0.0852 to 0.7289, range 0.6437
```

## 4. Finding one: the inclusion axis is redundant here

**Every cell's value is bit-identical with and without the inclusion rule, because no animal in this dataset
fails the thresholds.** **So the grid is 12 specifications, not 24.**

**And V2-C4's own table lists an inclusion-rule axis.** **If the rule excludes no animal at the specification
it is stated for, then it is not a specification either, and listing it inflates the apparent number of
choices.**

**This is round 30's redundancy lesson recurring, and this time the redundant axis was added by this grid's
author rather than found afterwards.** **The check that catches it is the same one: if two levels of an axis
give bit-identical output, the axis is not a specification.**

## 5. Finding two: V2-C4's ceiling depends on a step no grid here varies

**This grid's maximum is 0.4408. V2-C4's is 0.7289, and it comes from `RESULT_robust_class.json`, produced by
`10_robust_and_class.py`, which applies three steps this grid does not:**

1. **per-cell normalisation by the ACROSS-CELL SD of the difference** (`sd = np.nanmedian(np.nanstd(dv, axis=1))`)
   rather than by the cell's pre-stimulus SD;
2. **common-mode removal** (`cm = np.nanmean(dvs, axis=1, keepdims=True); dev = dvs - cm`);
3. **within-animal standardisation**.

**Step 2 is the one that matters, because round 6 established that common-mode removal changes this estimate
substantially.** **So:**

> **V2-C4's range is a range over a family that includes common-mode removal, and this grid's family excludes
> it. The two families do not overlap at the top: this one tops out at 0.4408 while V2-C4's reaches 0.7289.
> The largest value in V2-C4's range therefore depends on a step that neither V2-C4's table nor this grid
> varies systematically.**

**This does NOT show V2-C4's range to be wrong.** **It shows that its upper end is carried by one specification
whose contribution is not isolated, and that a reader of the range cannot tell how much of the movement from
0.0852 to 0.7289 is the common-mode choice and how much is everything else.**

## 6. What V2-C4's status becomes

**Unchanged as a claim about code versus data: the specification is not recoverable from the file, and that is
demonstrated.** **Narrowed as a claim about a range:**

> **Across twelve specifications that do not include common-mode removal, the animal-level estimate is `d_A`
> 0.101 to 0.441. V2-C4's reported range extends to 0.729, and that extension is attributable to common-mode
> removal, which is one further choice in the pipeline and is not held constant across the four values V2-C4
> reports.**

**The one-line version: the range is real and its upper end is a single unvaried step.**

## 7. What is owed

1. **A grid that includes common-mode removal as an axis,** so the contribution of that step is isolated
   rather than inferred. **Named and not run.**
2. **A check of whether V2-C4's inclusion-rule axis excludes any animal at the specifications it is stated
   for.** **This grid's rule excludes none; V2-C4's four values may use different rules.**
3. **The redundancy check applied to V2-C4's own four-row table**, which this round applied only to its own.

## 8. Provenance

* Script `anatomy/28_v2c4_specification_grid.py`; cached input `v2c4_cache.pkl`, 3,333 events from 110
  animals; output `anatomy/RESULT_v2c4_specification_grid.json`.
* First attempt retained as `anatomy/27_v2c4_grid_ATTEMPT1_reload.py`.
* **No model was fitted. No causal claim is made.**
