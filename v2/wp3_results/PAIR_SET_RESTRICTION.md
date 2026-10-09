# The pair-set restriction does not shrink the spread, and what that does and does not settle

**Status: the last analytical item named in this line, run. It removes one candidate for the unexplained
spread and does not assign it.** No model was fitted.

---

## 1. The design

**Round 15 found that pair composition explains 17.7 % of the between-animal variance in the connectivity
effect, leaving about 40 % unexplained after measurement noise. Round 15 named this test: restrict every
animal to pairs measured in many animals, so composition is held more nearly constant, and see whether the
spread and its reproducible share fall.**

**Signal and noise are separated with the round-14 machinery:** split each animal's events into halves,
estimate the effect from each half, and take

```
noise variance of the full-data effect = var(m1 - m2)/4
signal share                           = 1 - noise / total
```

## 2. The feasibility probe, which is itself informative

**How many pairs survive each threshold, and how many of those are connected?**

| K | pairs | of which connected | animals |
| --- | --- | --- | --- |
| 1 | 29,395 | 2,308 | 110 |
| 2 | 22,389 | 1,848 | 110 |
| 3 | 18,359 | 1,550 | 110 |
| 5 | 12,751 | 1,106 | 110 |
| 10 | 5,698 | 518 | 109 |

**A pair is measured in a median of 4 animals, p90 of 14 and at most 55.** **So the pool can be shrunk to
roughly 40 % of its size while retaining over a thousand connected pairs, which is what makes the test
feasible at all.** **A true matched design -- the same pair set for every animal -- is not available, because
each animal measured a different subset and the intersection across 110 animals is empty.**

## 3. The result

| K | pairs | connected | animals | effect SD | `r_full` | **signal share** |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | 29,395 | 2,308 | 109 | 0.1617 | 0.5159 | **0.5439** |
| **2** | 22,389 | 1,848 | 109 | 0.1612 | 0.5615 | **0.5901** |
| **3** | 18,359 | 1,550 | 109 | 0.1636 | 0.4647 | **0.5201** |
| **5** | 12,751 | 1,106 | 109 | 0.1661 | 0.5299 | **0.5559** |

> **Both the between-animal spread and its reproducible share are flat across a pair-pool reduction from
> 29,395 to 12,751.**

**The effect SD moves from 0.1617 to 0.1661 -- 2.7 % -- and the signal share from 54.4 % to 55.6 %.** **If pair
composition were driving the spread, restricting the pool should reduce the composition variance and hence
the spread. It does not.**

## 4. What this settles, and the limit that must be stated with it

**Settles: the spread is not primarily driven by which pairs each animal happened to have measured, in the
specific sense that shrinking the available pool does not shrink it.**

**The limit, stated because the design is not what round 15 proposed.** **Round 15 named a pair-set-MATCHED
comparison. This is a pair-set-RESTRICTED one.** **Each animal still uses its own subset of the filtered
pool, so composition still varies between animals at every K; what falls is the size of the pool from which
each animal's subset is drawn.** **A genuinely matched design would need a non-empty intersection across
animals, and section 2 shows there is none.**

**So this is weaker than a matched test and stronger than nothing:** it eliminates the hypothesis that the
spread comes from composition variance that the pool size controls, and it does not eliminate composition
variation that persists within any pool.

## 5. The accounting, updated

| component of the effect's between-animal variance | share | source |
| --- | --- | --- |
| measurement noise | 42.2 % | round 14 |
| pair composition | 17.7 % | round 15, `R^2` of the leave-one-animal-out prediction |
| nine technical covariates | 0.25 % | round 16, adjusted `R^2` |
| **pair-pool restriction** | **does not reduce the spread** | this round |
| **unexplained** | **about 40 %** | remainder |

**Three candidate explanations have now been tested and none accounts for the remainder:** measurement noise
is priced separately at 42.2 %, composition at 17.7 %, and the available technical covariates at 0.25 %.
**The remainder is not assigned, and the candidates are unchanged: genuine per-animal biological
differences, an unmeasured technical factor, or an interaction.**

**Absence of a technical or compositional explanation is still not presence of a biological one**, which is
the error this line retracted in round 12.

## 6. Where the line now stands, after twenty rounds

**Four claims, all with their ceilings, and all four analytical items named as owed in rounds 10 to 15 now
run except the Methods-level literature survey, which is a reading task rather than a computation:**

| item | status |
| --- | --- |
| source-rule reproduction (round 7) | **done** |
| like-for-like Fig-6 comparison (round 11) | **done** |
| three-level decomposition (round 12) | **done** |
| effect reliability and composition (rounds 14-15) | **done** |
| technical covariates (round 16) | **done** |
| specification in the literature (rounds 17-18) | **done at title-and-abstract level** |
| figure source data (round 19) | **done** |
| **pair-set restriction (this round)** | **done** |
| Methods-level specification survey | **owed** |
| independent reviewer | **owed, and external** |
| owner decision on the plan's constraint | **owed, and not this line's to take** |

## 7. Provenance

* Script `anatomy/20_pair_set_restricted.py`; output `anatomy/RESULT_pair_set_restricted.json`.
* Read-out, pre-window and analysis-window conventions as in `SOURCE_RULE_RESULT.md`.
* **No model was fitted. No causal claim is made.**
