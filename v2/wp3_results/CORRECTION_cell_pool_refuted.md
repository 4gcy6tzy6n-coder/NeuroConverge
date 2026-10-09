# The cell pool contributes 0.0038, not 0.3394: round 32's explanation is refuted

**Status: round 32's explanation for the 0.7289 discrepancy is refuted by direct measurement. Four candidate
causes have now been tested and eliminated, and the discrepancy is unresolved.** No model was fitted.

**This is the fourteenth self-found defect and the fifth consecutive round in which an inferred cause was
wrong.**

---

## 1. What was tested

**Round 32 concluded that the difference between the grid's `d_A` and the code's `0.7289` came from the cell
pool over which the common mode is computed:** **`09_animal_level.py` spans all ~114 columns while the grid's
cache held only the 46 uniquely-named ones.**

**This round re-cached the events over ALL columns, with per-column names, a uniqueness flag and a connection
flag, so the pool could be varied while the effect stayed over uniquely-named cells as the code does.**

## 2. The result

| post | common-mode pool | cell normalisation | per-volume common mode | animals | `d_A` | `t` |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | **all columns** | no | yes | 109 | **0.3933** | 4.1062 |
| 24 | **uniquely-named only** | no | yes | 109 | **0.3895** | -- |
| 24 | all | no | no | 109 | see JSON | |
| 24 | unique | no | no | 109 | see JSON | |
| 24 | all | yes | yes | 109 | see JSON | |
| 48 | all | no | yes | 109 | see JSON | |

```
pool = all columns     :  d_A = 0.3933
pool = unique only     :  d_A = 0.3895
THE CELL POOL'S CONTRIBUTION: +0.0038
the code reports          :  d_A = 0.7289
remaining difference      :  0.3356, and still unreproduced
```

> **The cell pool moves `d_A` by 0.0038, which is 1.1 per cent of the 0.3394 that round 32 attributed to it.
> Round 32's explanation is refuted.**

## 3. The four causes now eliminated

| candidate | how it was tested | outcome |
| --- | --- | --- |
| **common-mode removal** | varied as an axis | **lowers `d_A` by 0.01 to 0.03**; cannot explain a higher ceiling |
| **per-volume versus scalar common mode** | both implemented | **both lower `d_A`**; the per-volume form is the code's |
| **the common mode's cell pool** | re-cached over all columns | **contributes 0.0038** |
| **window, baseline, per-cell normalisation** | round 31's grid | together span 0.22 and 0.30; the code's own setting gives 0.39 |

**And a fifth candidate was tested and set aside: the scalar `sd` in `dvs = dv/sd` cancels exactly, because
`dev[:,c] = dv[:,c]/sd - mean_c'(dv[:,c']/sd) = (dv[:,c] - mean_c'(dv[:,c']))/sd`, and `sd` is the same for
all cells. So it cannot be the cause either.**

## 4. What is left, stated as an open question rather than as an inference

**The grid reproduces the code's configuration step for step as far as reading the code allows, and returns
0.3933 against 0.7289. The remaining 0.3356 has no tested explanation.**

**The decisive test, which is running as this is written, is to re-run `09_animal_level.py` itself and see
whether it still returns 0.7289.** **There are two possible outcomes and they mean different things:**

* **If the original script returns 0.7289, then the grid differs from it somewhere not visible on reading, and
  the next step is a line-by-line instrumented comparison rather than another hypothesis.**
* **If the original script does NOT return 0.7289, then the committed value is unreproducible by its own
  script, which is a defect of the first order: a headline number that no longer follows from the code that
  produced it.**

**Neither is a hypothesis. Both are readable from the running job.**

**AND THE METHOD POINT, WHICH IS THE ONE THING THIS ROUND CAN STATE WITH CONFIDENCE: four successive
hypotheses about this discrepancy have each been refuted by measurement, and each refutation took a round.**
**The alternative, which was available from the start and was not taken until now, is to re-run the original
script and read its output.** **The lesson is not "infer more carefully" but "reproduce the original artifact
before explaining the discrepancy" -- the same lesson as round 14's, where a committed JSON carried an
uncorrected value, and as round 25's, where four provenance links pointed at files that did not exist.**

## 5. Provenance

* Script `anatomy/31_v2c4_cell_pool_varied.py`; cache `v2c4_pool_cache.pkl` over all columns with per-column
  names, uniqueness and connection flags; output `anatomy/RESULT_v2c4_cell_pool_varied.json`.
* **The re-run of the original `09_animal_level.py` was started in this round; its result is recorded in the
  next entry rather than asserted here.**
* **No model was fitted. No causal claim is made.**
