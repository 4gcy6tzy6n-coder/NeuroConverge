# CORRECTION: the measurement-error share is 38.7 % to 57.1 %, not 37 % to 39 %

**Status: this narrows the surviving claim of round 26. The part of that claim about insensitivity to the
minimum-animals-per-pair restriction is confirmed; the part quoting a 37 to 39 per cent range is too narrow
by a factor of about two in its width.** No model was fitted.

**This is the twelfth self-found measurement defect in this line, and the second in a row found by testing the
line's own previous correction rather than its original claims.**

---

## 1. What round 26 claimed, and what this tests

**Round 26 concluded:**

> *"within-cell measurement error accounts for 37 to 39 % of the variance in a pair's response in this atlas,
> and that share is insensitive to how many animals each pair was measured in. The pair-specific animal share
> is not robust."*

**It varied one thing: the minimum number of animals per pair.** **It did not vary the response read-out, the
post-stimulus window length, or whether values are standardised per cell.**

**This sweeps those.** **Eight specifications: `signed sum` versus `mean` over the window; 12, 24 and 48
volumes; and no per-cell normalisation versus division by each cell's own median absolute deviation, at one
window.**

## 2. The result

| read-out | post window | cell normalisation | `min_an` | units | between-pair | **`eps`** | `beta` | animal offset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sum | 12 | none | 1 | 192,303 | 52.4 % | **57.1 %** | **-10.9 %** | 1.5 % |
| sum | 12 | none | 3 | 165,713 | 20.6 % | **56.4 %** | 21.6 % | 1.5 % |
| sum | 24 | none | 1 | 192,303 | 53.3 % | **52.9 %** | **-8.1 %** | 1.9 % |
| sum | 24 | none | 3 | 165,713 | 21.8 % | **51.9 %** | 24.4 % | 1.9 % |
| sum | 24 | **mad** | 1 | 192,303 | 53.3 % | 52.9 % | -8.1 % | 1.9 % |
| sum | 24 | **mad** | 3 | 165,713 | 21.8 % | 51.9 % | 24.4 % | 1.9 % |
| sum | 48 | none | 1 | 192,303 | 53.9 % | **51.7 %** | -7.5 % | 2.0 % |
| sum | 48 | none | 3 | 165,713 | 22.0 % | 50.6 % | 25.4 % | 2.0 % |
| mean | 12 | none | 1 | 192,201 | 50.7 % | **45.9 %** | 1.9 % | 1.5 % |
| mean | 12 | none | 3 | 165,642 | 21.0 % | 45.4 % | 32.2 % | 1.5 % |
| mean | 24 | none | 1 | 192,201 | 51.1 % | **40.5 %** | 6.1 % | 2.4 % |
| mean | 24 | none | 3 | 165,642 | 23.0 % | 40.0 % | 34.7 % | 2.3 % |
| mean | 24 | **mad** | 1 | 192,201 | 51.1 % | 40.5 % | 6.1 % | 2.4 % |
| mean | 24 | **mad** | 3 | 165,642 | 23.0 % | 40.0 % | 34.7 % | 2.3 % |
| mean | 48 | none | 1 | 192,201 | 51.9 % | **38.9 %** | 6.7 % | 2.5 % |
| mean | 48 | none | 3 | 165,642 | 23.3 % | 38.7 % | 35.5 % | 2.5 % |

```
eps  across specifications:  38.7 %  to  57.1 %     range 18.4 points
beta across specifications: -10.9 %  to  35.5 %     range 46.5 points
```

## 3. What this establishes

**Three findings, and the first contradicts round 26's wording.**

**First, `eps` is not a narrow constant.** **38.7 % to 57.1 % across eight defensible specifications.** **The
read-out alone moves it about thirteen points: the signed sum gives 50.6 to 57.1 %, the mean over the window
gives 38.7 to 45.9 %.**

**Second, the insensitivity round 26 found is real.** **At a fixed read-out and window, moving `min_an` from 1
to 3 changes `eps` by at most 1.0 point. That part of round 26 stands.**

**Third, and this is what survives as the robust statement: at `min_an = 3`, `beta` is positive in ALL EIGHT
specifications, 21.6 % to 35.5 %, whereas at `min_an = 1` it is negative in five of eight, -10.9 % to +6.7 %.**

> **The sign structure is robust; no particular share is.** **Measurement error is the largest or
> second-largest component in every specification, and the pair-specific animal component is positive in
> every specification once pairs measured in a single animal are excluded.**

## 4. A limitation of this sweep, stated because it is real

**This grid does not reproduce round 26's exact specification.** **Its `sum` branch sums the baseline-corrected
signal from the stimulus volume over the post window, whereas round 26 summed from `SHIFT = 60` volumes
before the stimulus to the end of a per-event analysis window.** **Those are different windows, which is why
this grid's `sum` gives `eps` of 51 to 57 % while round 26 reported 37.5 %.**

**So this sweep shows that the read-out and window move `eps` considerably; it does not show which value round
26's exact convention would give if re-run, because it did not re-run it.** **That is owed and named.**

## 5. The corrected statement for V2-C3

**Round 26's corrected statement read:**

> *"...a within-cell measurement-error share of 37 to 39 %, a pair-specific animal share of 5.5 % to 46.0 %
> depending on the minimum-animals-per-pair restriction..."*

**It becomes:**

> **A pair's response decomposes into a between-pair share of roughly 20 to 54 %, a within-cell
> measurement-error share of 38.7 to 57.1 %, a pair-specific animal share that is negative when pairs
> measured in one animal are included and positive, 21.6 to 35.5 %, when they are excluded, and a
> homogeneous animal offset of 1.5 to 2.5 %. What is robust is the sign structure: measurement error is
> always the largest or second-largest component, and the pair-specific animal component is positive once
> the ill-posed stratum is excluded.**

**And the finding that survives in its original form is the one round 12 turned on and round 26 confirmed:**
**measurement error is a large share of the variance in a pair's response in this atlas, and the atlas does
not report it.** **That statement needs no particular number.**

## 6. The pattern, now with two instances

**Round 26 tested round 12's claim and narrowed it.** **Round 29 tested round 26's claim and narrowed it
again.** **Each correction's surviving part is a sign or a magnitude class, not a point value.**

**The rule this suggests, and which the corpus index should carry: a share obtained from a variance
decomposition should be reported as a range over a declared specification set, with the declaration
included, because the read-out and window can move it more than the restriction does.**

## 7. Provenance

* Script `anatomy/25_eps_specification_grid.py`; output `anatomy/RESULT_eps_specification_grid.json`.
* The first attempt failed with a broadcasting error -- `mad` was computed over the uniquely-named subset
  while `dv` spanned all columns, shapes (46,) against (114,) -- and is retained as
  `anatomy/25_eps_grid_ATTEMPT1_broadcast.py`. **The same defect class as round 9's; the shape mismatch
  between a full-column array and a subset array recurs in this codebase.**
* **No model was fitted. No causal claim is made.**
