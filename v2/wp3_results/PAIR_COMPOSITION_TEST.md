# Pair composition explains 17.7 % of the between-animal spread, not all of it

**Status: a test that answers the question round 14 left open, and that corrects round 14's own wording.**
No model was fitted.

---

## 1. The test

**Round 14 concluded that what is reproducible within an animal is *which pairs it happened to measure*,
and argued that the effect's per-animal value is therefore "reproducible and not biology". That reasoning
was structural; this is the measurement.**

**For each animal, predict its effect using only its pair composition plus each pair's
LEAVE-ONE-ANIMAL-OUT mean response.** Leave-one-out is essential, because predicting an animal's effect
from its own data would be circular. Responses are taken in log space because the raw sums are
heavy-tailed.

| quantity | value |
| --- | --- |
| animals entering | **107** |
| (animal, pair) units with a leave-one-out mean | 166,948 |
| **observed effect** | mean **+0.5726**, SD **0.6142** |
| **composition-predicted effect** | mean **+0.5621**, SD **0.3214** |
| **`corr(predicted, observed)`** | **+0.4209** |
| **`R^2`** | **0.1772** |
| predicted SD / observed SD | 0.5233 |

## 2. What it says

**The two means agree closely, +0.5726 against +0.5621, so pair composition reproduces the effect's
AVERAGE well.** **But the prediction accounts for only 17.7 % of the observed variance, and its spread is
about half the observed spread.**

> **Pair composition is a real contributor to the between-animal spread and is not the explanation for it.**

**So round 14's conclusion was directionally right and quantitatively overstated.** It said the
reproducible component is *which pairs were measured*. **Measured, that component is 17.7 % of the
variance.**

## 3. The accounting, and the part that is not explained

**Combining this round with round 14:**

| component of the effect's between-animal variance | share | source |
| --- | --- | --- |
| **measurement noise** | **42.2 %** | round 14, noise share from `var(m1-m2)/4` |
| **pair composition** | **17.7 %** | this round, `R^2` of the leave-one-out prediction |
| **unexplained** | **about 40 %** | remainder |

**The unexplained portion cannot be assigned by anything this line has run.** Its candidates are
**genuine per-animal biological differences**, **an unmeasured technical factor**, or **an interaction
between composition and pair-specific animal deviation**, and **this line has no measurement that
distinguishes them.**

**In particular, round 12's three-level decomposition measured pair-specific animal deviation at 5.5 % of
the PAIR-level variance, which is not the same quantity as the unexplained 40 % of the EFFECT-level
variance, and the two must not be conflated.** **A pair's value can be nearly animal-independent while the
connected-minus-unconnected contrast varies across animals**, if the pair sets differ in ways composition
alone does not capture.

## 4. The corrected statement, and what it replaces

**Round 14 said:** *"what is reproducible within an animal is WHICH PAIRS IT HAPPENED TO HAVE MEASURED,
not a biological property of the animal's circuit"*.

**Corrected:** *pair composition accounts for about 18 % of the between-animal variance in the effect;
measurement noise accounts for about 42 %; and about 40 % is unexplained by anything measured here, so
neither a composition nor a biological account is presently supported for it.*

**This is weaker than round 14 and it is what the data supports.** Three of this line's claims have now been
narrowed after measurement: the round-9 animal-heterogeneity reading (retracted, round 12), the round-10
population-level framing (weakened, round 12), and now round 14's composition account (reduced from "what is
reproducible" to 17.7 %).

**The pattern continues to hold: every measurement survives, every interpretation narrows.**

## 5. What would resolve the unexplained 40 %

**Two tests, both bounded:**

1. **A pair-set-matched comparison.** Restrict every animal to the SAME set of pairs -- those measured in
   many animals -- so composition is held exactly constant, and recompute the spread. **The cost is a
   smaller and noisier contrast, which the round-14 machinery can price.**
2. **A technical covariate sweep.** Animal-level GCaMP brightness, recording duration, number of events and
   number of identified cells are all available from the per-animal files and none has been tested against
   the effect.

**The second is cheaper and has not been attempted.**

## 6. What is unaffected

* **V2-C1**, the 11-to-18-fold unit inflation: arithmetic, and independent of every decomposition here.
* **V2-C2**, the Fig-6 reproduction and its `r = 0.208` bound: a different read-out entirely.
* **V2-C3**, the three-level decomposition: its result stands; **what this round changes is what may be
  inferred from it about the EFFECT's spread.**
* **The round-14 reliability measurement itself**, `r_full = 0.5266` and signal share 0.578: unaffected.
  **What is corrected is the interpretation of where that signal comes from.**

## 7. Provenance

* Script `anatomy/18_pair_composition.py`; output `anatomy/RESULT_pair_composition.json`.
* Leave-one-animal-out means over 166,948 units; 107 animals with at least 10 connected and 50 unconnected
  pairs carrying a leave-one-out value.
* **No model was fitted. No causal claim is made.**
