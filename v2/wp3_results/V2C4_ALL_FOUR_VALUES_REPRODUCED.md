# All four of V2-C4's values are now independently reproduced

**Status: round 38's last owed item is closed. The two values that were traceable only to their own script now
reproduce field by field, and the two-family structure round 37 inferred is confirmed.** No model was fitted.

---

## 1. What was run

**`12_inverse_variance_weighting.py` was re-run unmodified, in the manner round 34 established: re-run the
original before explaining anything about it.** **It produces V2-C4's two lowest values.**

**Its pipeline, read from the file rather than inferred:**

```
read-out   : signed sum from 60 volumes before the stimulus to the end of the per-event window
             (the source convention, with NO amplitude or derivative criteria)
unit rule  : a (animal, pair) cell enters only if it holds two or more measurements, so its
             within-variance is estimable
weight     : w = n / s_within^2
animal     : weighted mean of connected minus weighted mean of unconnected, per animal
```

## 2. The reproduction

| field | re-run | committed | |
| --- | --- | --- | --- |
| animals | 105 | 105 | **OK** |
| units | 33,578 | 33,578 | **OK** |
| **`d_unweighted`** | **0.1580** | 0.15798182543851905 | **OK** |
| **`t_unweighted`** | **1.619** | 1.6188319871849282 | **OK** |
| **`d_iv_weighted`** | **0.0852** | 0.08521128158749058 | **OK** |
| **`t_iv_weighted`** | **0.873** | 0.8731558071313357 | **OK** |
| `change_pct` | **-46.1** | -46.06260476420954 | **OK** |
| `corr(weight, mean response)` connected | **+0.0288** | 0.028839049759143014 | **OK** |

**Seven fields, all matching.**

## 3. The elapsed record: all four values reproduced

| value | producing script | reproduced in | agreement |
| --- | --- | --- | --- |
| **0.7289** | `10_robust_and_class.py` | round 42, the `w` arm | **exact to four decimals** |
| **0.4495** | `11b_source_rule.py` | round 38, the `SOURCE` arm | **exact to four decimals** |
| **0.1580** | `12_inverse_variance_weighting.py` | **this round** | **seven fields** |
| **0.0852** | `12_inverse_variance_weighting.py` | **this round** | **seven fields** |

> **V2-C4's range is now fully measured rather than partly inherited.**

## 4. And the family structure is confirmed

**Round 37 inferred from reading the code that 0.7289 comes from a weighted pipeline and the other three from
unweighted ones, and round 38 measured the weighting's size at 0.18 to 0.30.** **This round confirms the
inference directly:** **`12_inverse_variance_weighting.py` contains no per-event `sd` division -- it was
searched for `sd =`, `/sd`, `nanstd` and `nanmedian` in round 37 -- and both of its values are unweighted.**

**So the family assignment is now:**

| family | values | span |
| --- | --- | --- |
| **unweighted** | **0.0852, 0.1580, 0.4495** | **0.0852 to 0.4495, a span of 0.3643** |
| **weighted** | **0.7289** | one value |

**And the corrected statement of V2-C4's range stands as round 38 measured it: the reported span of 0.6437
mixes the two families, and within the unweighted family the span is 0.3643.**

## 5. What this closes, and the state of the owed list

**Round 38 named three things it had not done.** **This closes the first two:**

| round-38 owed item | status |
| --- | --- |
| reproduce `12_inverse_variance_weighting.py`'s 0.1580 and 0.0852 | **closed, this round, seven fields** |
| resolve the sub-choice inside the weighting that separates 0.5700 from 0.7289 | **closed in round 40: the code computes `sd` before the common mode and over all columns; doing that reproduces 0.7289 exactly** |
| a grid over the two largest dimensions | **run in rounds 41 and 42, which found the dimensions are non-additive and that their ORDER is the largest dimension measured** |

**And the owed list is now:**

| item | since | why it is not this line's |
| --- | --- | --- |
| **an independent reviewer** | round 10, **34 rounds** | the plan requires an external person, and `PREFLIGHT_REVIEW.md` records that the review performed is this line's own |
| **the owner's decision on the plan's constraint** | round 13, **31 rounds** | the constraint forbidding a new NMI abstract, main-text Results, Discussion and figures is the plan's, and only the owner can lift it |

## 6. One further observation this round makes available, and does not pursue

**`corr(weight, mean response)` is +0.0288 in the connected stratum and +0.0085 in the unconnected one.** **The
script's own docstring states the reason it computes this: the inverse-variance weight should be exogenous to
the mean response, and the author notes that the measurement count was not (+0.03 to +0.06) while this one
is.** **Both are small and the point stands as the script makes it.** **Recorded because it is a check the
line performed on itself in round 12 and has not revisited.**

## 7. Provenance

* Re-run of `anatomy/12_inverse_variance_weighting.py` unmodified; output compared field by field against
  `anatomy/RESULT_iv_weighting_INVALID_weights.json`.
* **The `INVALID_weights` marker stands and this round does not remove it: the weights span thirty-one orders
  of magnitude, so the weighted arm remains uninterpretable.** **What this round establishes is that the file
  reproduces, which is a separate question from whether its weighted arm means anything.**
* **No model was fitted. No causal claim is made.**
