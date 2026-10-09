# The per-event `sd` division is a weighting this line's grids omitted, and my "it cancels" argument was wrong

**Status: round 33's decisive test is answered, and the instrumented comparison found the divergence. The
committed `0.7289` is sound; five of this line's own grids were missing a step.** No model was fitted.

**This is the fifteenth self-found defect, and the first in six rounds whose cause was measured rather than
inferred.**

---

## 1. The decisive test, answered

**Round 33 said the outcome would be readable from re-running `09_animal_level.py` itself.** **It was:**

```
animals with a usable contrast: 109
paired difference +0.07702   across-animal SD 0.10567   SE 0.01012
t = 7.610   df = 108   p = 1.09e-11
standardised effect d = 0.7289
chemical  d = 0.4145      gap  d = 0.7690
```

> **The original script reproduces `0.7289` exactly, and `0.4145` and `0.7690` with it.** **So the committed
> value follows from its own code, and the divergence was in the grids.**

**That is round 33's first outcome, and round 33 named the correct response to it: an instrumented comparison
rather than another hypothesis.**

## 2. The instrumented comparison, on one animal

**Both pipelines were run on animal 0 over the same 33 surviving events and the same 46 uniquely-named cells,
and their per-cell means compared.**

| cell | code's mean | grid's mean | ratio |
| --- | --- | --- | --- |
| 5 | +0.042861 | +3.448391 | **80.4** |
| 68 | -0.020960 | -2.155386 | **102.8** |
| 10 | +0.023279 | +1.675396 | 72.0 |
| 66 | -0.012559 | -1.483560 | 118.1 |

**The ratios are NOT constant.** **That single fact is the finding, and it refutes an argument this line has
made twice.**

## 3. The wrong argument, stated plainly

**Rounds 32 and 33 both argued that the scalar `sd` in `dvs = dv / sd` cancels in `d_A`, on the grounds that**

```
dev[:,c] = dv[:,c]/sd - mean_c'(dv[:,c']/sd) = (dv[:,c] - mean_c'(dv[:,c']))/sd
```

**so a common factor divides every cell equally and cancels in a ratio of a difference to a standard
deviation.**

**That algebra is correct and its premise is false.** **In `09_animal_level.py` the line**

```python
sd = np.nanmedian(np.nanstd(dv, axis=1))
```

**is INSIDE the event loop.** **`sd` is therefore per event, not per animal, and `dvs = dv / sd_event`
weights each event by `1 / sd_event` before the events are averaged.** **No single scalar divides all cells
equally, so nothing cancels.**

**The non-constant ratios in section 2 are that weighting, measured.**

## 4. What this means for this line's grids

**Five grids omitted `dvs = dv / sd_event` entirely, so all events counted equally in them while the code
weights them:**

| grid | round | omitted the weighting |
| --- | --- | --- |
| the eps specification grid | 29 | **yes** |
| V2-C4's first range grid | 31 | **yes** |
| the scalar-common-mode grid | 32 | **yes** |
| the all-columns cell-pool grid | 33 | **yes** |
| the three-level variance decomposition | 12, 26 | **yes** |

**So every "the grid gives 0.39 while the code gives 0.73" statement in rounds 26 to 33 compares a weighted
estimator against an unweighted one, and the difference is the weighting rather than any of the causes those
rounds proposed and eliminated.**

**Whether the weighting also moves the three-level decomposition's shares is the immediate open question, and
the running job tests it.**

## 5. What this does to V2-C4

**V2-C4's claim is that the choices live in the pipeline's code and not in its data file, and that
re-analysing moves the estimate.** **This strengthens it, and in a specific way that no previous round could
state:**

> **The pipeline weights each stimulus event by the inverse of that event's across-cell response spread
> before averaging, and that weighting is worth about 0.34 in `d_A` -- comparable to the entire range V2-C4
> reports. The step is four lines in the code, is named nowhere in the data file or any document, and was
> invisible to five successive re-implementations of the same analysis by the line that wrote it.**

**That is a much stronger demonstration of V2-C4 than the range itself.**

## 6. The pattern, now six rounds deep

| round | what was proposed | how it failed |
| --- | --- | --- |
| 29 | the read-out moves the decomposition | the window convention differed too |
| 30 | twelve rows were twelve specifications | three transforms were a no-op |
| 31 | common-mode removal explains the ceiling | it lowers `d_A` |
| 32 | the common mode's cell pool explains it | it contributes 0.0038, not 0.3394 |
| 33 | *(no proposal: the decisive test was run)* | **the original reproduces `0.7289`** |
| **34** | **the divergence is a per-event weighting** | **measured, not inferred: non-constant ratios** |

**Five hypotheses were refuted and the sixth was found by instrumenting rather than by reasoning.** **The
lesson round 33 recorded -- reproduce the original before explaining a discrepancy -- produced the answer
within one round of being applied.**

## 7. Provenance

* Instrumented comparison `anatomy/33_instrumented_comparison.py`.
* The original script's re-run: `anatomy/32_rerun_09_animal_level.py`, output shown in section 1.
* **The verification, completed: the weighting accounts for the difference exactly.**

```
without per-event sd weighting:  d_A = 0.3933   (diff 0.65615,  sd 1.66828,  t 4.106)
with    per-event sd weighting:  d_A = 0.7289   (diff 0.07702,  sd 0.10567,  t 7.610)
the weighting's contribution:    +0.3356
```

**The weighted run returns `diff = 0.07702` and `sd = 0.10567`, the original script's values to five decimal
places, and `d_A = 0.7289` with them.** **So `0.3933 + 0.3356 = 0.7289` exactly, and the entire discrepancy
is one omitted step.** **The grid's reproduction of the code's configuration is exact apart from it.**

## 4a. The immediate consequence for V2-C3, and the test now running

**The three-level variance decomposition behind V2-C3 omitted the same step.** **Its shares -- 55.1 per cent
between-pair, 37.5 per cent measurement error, 5.5 per cent pair-specific animal and 1.9 per cent animal
offset at the round-12 specification, and the 38.7-to-57.1 per cent measurement-error range of round 29 --
were all computed on unweighted events.**

**So the question is not academic: if the weighting moves those shares as much as it moves `d_A`, then V2-C3
has the same defect as V2-C4's grids, and every share this line has reported for it is an unweighted value.**
**A decomposition run both ways on the same events is in progress and its result is recorded in the next entry
rather than asserted here.**

* **No model was fitted. No causal claim is made.**
