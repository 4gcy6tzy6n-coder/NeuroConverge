# V2-C2 survives a specification grid, and the grid has a redundant axis

**Status: the first live claim to be stress-tested and confirmed. One axis of the grid varies nothing, which is
recorded because a grid with a redundant axis looks like more testing than it is.** No model was fitted.

---

## 1. Why this claim, and why now

**Rounds 26 to 29 tested V2-C3 three times and V2-C1 once, and every test narrowed the claim.** **V2-C2 was the
only live claim never stress-tested.** **So the same treatment was applied: vary every defensible choice in its
computation and see whether the numbers move.**

**V2-C2 states that the source's own anatomy-versus-spontaneous-activity comparison reproduces at `r = +0.0368`
and `-0.0064` in its two animals, and that the quantity it predicts has cross-animal agreement of only
`r = 0.208` on the 23 shared cells.**

## 2. The grid, and the axis that does nothing

**Three transforms (raw fluorescence, ΔF/F against the session median, z-scored per cell) × two correlation
methods (Pearson, Spearman) × detrending or not.**

**The transform axis is a NO-OP.** **Pearson and Spearman correlations are invariant to per-column affine
transforms, and all three transforms are affine per column, so all three give bit-identical results.**

| transform | method | detrend | `r` animal 0 | `r` animal 1 | **`r` cross-animal** |
| --- | --- | --- | --- | --- | --- |
| **raw** | **pearson** | **no** | **+0.0368** | **-0.0064** | **+0.2084** |
| raw | pearson | yes | +0.0356 | +0.0021 | +0.2612 |
| raw | spearman | no | +0.0381 | +0.0027 | +0.2253 |
| raw | spearman | yes | +0.0356 | +0.0118 | +0.2703 |
| **dff** | **pearson** | **no** | **+0.0368** | **-0.0064** | **+0.2084** |
| dff | pearson | yes | +0.0356 | +0.0021 | +0.2612 |
| dff | spearman | no | +0.0381 | +0.0027 | +0.2253 |
| dff | spearman | yes | +0.0356 | +0.0118 | +0.2703 |
| **z** | **pearson** | **no** | **+0.0368** | **-0.0064** | **+0.2084** |
| z | pearson | yes | +0.0356 | +0.0021 | +0.2612 |
| z | spearman | no | +0.0381 | +0.0027 | +0.2253 |
| z | spearman | yes | +0.0356 | +0.0118 | +0.2703 |

**THE GRID IS FOUR CELLS, NOT TWELVE.** **Recording this matters: the table above has twelve rows and three
distinct results per row-set, and a reader counting rows would overstate the test.**

## 3. What survives

| quantity | range over the four distinct specifications | V2-C2's value |
| --- | --- | --- |
| animal 0's anatomy-activity correlation | **+0.0356 to +0.0381** (range 0.0025) | +0.0368 |
| animal 1's | **-0.0064 to +0.0118** (range 0.0182) | -0.0064 |
| **cross-animal agreement of the target** | **+0.2084 to +0.2703** (range 0.0619) | +0.2084 |

> **V2-C2 is robust.** **The reproduction stays between +0.036 and +0.038 in animal 0 under every
> specification, both animals' values stay near zero, and the cross-animal bound stays between +0.208 and
> +0.270 -- always far below the 0.5 that would indicate a reproducible functional quantity.**

**And V2-C2's own specification is one of the four, and it is the one that reproduces the published values
exactly.**

## 4. The two specifications that move, and what they mean

**Detrending raises the cross-animal agreement from +0.208 to +0.261, and turns animal 1's value from -0.0064
to +0.0021.** **Both moves are small and neither changes a conclusion.**

**Spearman instead of Pearson raises the cross-animal agreement to +0.225 without detrending and +0.270 with
it.** **So the largest value the bound takes is +0.270, which is 0.229 below the 0.5 mark.**

**The direction of the movement is worth noting and is not pursued here: detrending and rank-correlating BOTH
raise cross-animal agreement, which is consistent with the shared slow drift within a session contributing to
agreement rather than contradicting it.** **A single observation, not a finding.**

## 5. The status of the four claims after four rounds of testing

| claim | tested | outcome |
| --- | --- | --- |
| **V2-C1** | round 27-28 | **retracted and inverted** -- a z-score was divided by a Cohen's `d` |
| **V2-C2** | **this round** | **confirmed; the reproduction and the bound are stable across the four distinct specifications** |
| **V2-C3** | rounds 26, 29 | **narrowed twice** -- the pair-specific share is not identified unrestricted, and the measurement-error share is a range, not a point |
| **V2-C4** | rounds 24, 28 | **confirmed; all four values in its range are Cohen's `d`** |

**Two of four confirmed, one narrowed twice, one retracted.** **That ratio is the honest summary of this line's
epistemic state at round thirty, and it is the reason the tests were run.**

## 6. The method note this round contributes

**A specification grid must be checked for redundancy before it is reported.** **Here an entire axis -- three
transforms -- contributed nothing, because the statistic is invariant to it.** **A grid that varies a quantity
the statistic ignores produces a longer table and no more evidence.**

**The test for redundancy: if two levels of an axis give bit-identical output, the axis is not a
specification.** **That is cheap to check and was not checked until the output was read.**

## 7. Provenance

* Script `anatomy/26_fig6_specification_grid.py`; output `anatomy/RESULT_fig6_specification_grid.json`.
* Data: OSF `spont_data_fig6.zip`, two animals, as in round 11.
* **No model was fitted. No causal claim is made.**
