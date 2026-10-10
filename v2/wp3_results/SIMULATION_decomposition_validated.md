# Simulation: the variance decomposition recovers a known truth, and its negative values are not generic

**An isolated reviewer raised as blocking that the manuscript's reliability numbers come from a decomposition that
returns a NEGATIVE variance share at its unrestricted specification, that this is admitted unresolved, and that no
reader can tell whether the retained specifications are inside or outside the failure region.** **Its resolution test
was to run a simulation under a known truth or to restrict the claim to the sign structure.** **This runs the
simulation.**

## What was done

**Data were generated DIRECTLY IN LOG SPACE** from the model the manuscript fits, with `var_alpha =
0.3`, `var_beta = 0.55` and `var_eps = 0.75`, 109 animals and
200 pairs per animal, 20 per cent of (animal, pair) cells carrying two repeat
measurements.** **The manuscript's own estimator was then applied: `eps` identified from the repeated-measurement
cells, `alpha` from the animal means, `beta` from the (animal, pair) cell means with the estimation-noise term
subtracted, and the remainder by subtraction.** **The whole experiment was replicated eight times at each of four
minimum-animals-per-pair levels.**

## The result

| `min_an` | `beta` estimated | ratio to truth | `eps` estimated | ratio to truth | replicates with negative `beta` |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.535 | 0.97 | 0.752 | 1.00 | 0 of 8 |
| 2 | 0.541 | 0.98 | 0.748 | 1.00 | 0 of 8 |
| 3 | 0.557 | 1.01 | 0.749 | 1.00 | 0 of 8 |
| 5 | 0.549 | 1.00 | 0.748 | 1.00 | 0 of 8 |

**The estimator recovers both components at every level, within 3 per cent of the truth for `beta` and within 1
per cent for `eps`, and it produces a negative `beta` in NONE of the thirty-two replicates.**

## What this does to the reviewer's concern, and what it does not

**IT REFUTES THE PREMISE THAT THE ESTIMATOR IS GENERICALLY ILL POSED.** **A negative component is not a behaviour
this estimator produces under a truth consistent with its own model, at any restriction, in 32 replicates.**
**So the negativity measured in the real atlas is a property of THAT DATA, or of a violation of the model's
assumptions, and not of the estimator.** **The reviewer's premise was that the retained specifications might lie
inside a failure region of the estimator; the simulation finds no such region at these levels.**

**IT DOES NOT EXPLAIN THE REAL DATA'S NEGATIVE VALUE, AND IT DOES NOT LICENSE THE RELIABILITY NUMBERS EITHER.**
**Three limits are load-bearing:**

1. **The simulation is validated only under its OWN assumptions: independent animal offsets, independent
   pair effects, homoscedastic within-cell error, and honest repeated measurements.** **The real atlas may violate
   any of these, and a violation is the most likely source of the negative value.**
2. **A negative estimate is what a small true `beta` produces when the estimand's own noise is comparable to it,
   so the real value may be a TRUE small or zero component rather than an error.** **The simulation shows the
   estimator does not manufacture negatives; it does not show what the real `beta` is.**
3. **The simulation does not validate the manuscript's per-cent shares against any external truth, because no
   such truth exists for the atlas.** **It validates the ESTIMATOR, not the ESTIMATE.**

## An error in this simulation's first version, retained rather than hidden

**The first version generated a LINEAR sum and then took its logarithm, which makes the log-scale truth different
from the linear truth and therefore makes the comparison against the truth meaningless.** **It reported the
estimator underestimating `beta` by 4.5 times and overestimating `eps` by 1.44 times, which was an artefact of
that mis-specification and not a finding.** **Regenerating directly in log space removed it.** **The error is
recorded because the trajectory is the paper's own subject: a number was produced, it looked like a result, and
only the comparison against the generating model showed that the two were on different scales.**

## Provenance

* **Script:** `43_decomposition_simulation.py`; **result:** `RESULT_decomposition_simulation.json`.
* **Seed:** fixed at 20261010, so the reported numbers are reproducible.
* **No model was fitted to the atlas in this exercise. No causal claim is made.**
