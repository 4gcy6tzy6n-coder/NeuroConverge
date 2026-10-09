# My own joint grid divided by the wrong axis, so its additivity test is void

**Status: the joint grid's weighting axis implements a different operation from the code's, so its additivity
conclusion is withdrawn. Its per-cell-normalisation numbers are valid and are reported.** No model was fitted.

**This is the nineteenth self-found defect, and the sixth consecutive round in which this line's own
implementation carried the error rather than its reasoning.**

---

## 1. What was run and what it produced

**Round 37's owed item 1: a joint grid over the two largest dimensions, to test whether the ledger's isolated
sizes are additive.** **Twelve cells: post-stimulus window 12, 24 and 48 volumes × per-cell normalisation off
and on × weighting off and on, from the cached all-columns events.**

| post | cell norm | weighted | `d_A` | `t` |
| --- | --- | --- | --- | --- |
| 12 | no | no | 0.2175 | 2.271 |
| 12 | no | yes | 0.1973 | 2.060 |
| 12 | yes | no | 0.1367 | 1.428 |
| 12 | yes | yes | 0.1316 | 1.374 |
| **24** | **no** | **no** | **0.3933** | 4.106 |
| 24 | no | yes | 0.3521 | 3.676 |
| 24 | yes | no | 0.1073 | 1.120 |
| 24 | yes | yes | 0.1067 | 1.114 |
| 48 | no | no | 0.3984 | 4.159 |
| 48 | no | yes | 0.3544 | 3.700 |
| 48 | yes | no | 0.1007 | 1.051 |
| 48 | yes | yes | 0.1002 | 1.047 |

**Its additivity test returned an interaction of +0.0406 at post 24 and declared a substantial interaction.**

## 2. Why that conclusion is withdrawn

**The grid's weighting contributed -0.0412 at post 24. Round 38 measured the same step's contribution at
+0.1767.** **Opposite signs mean the two are not the same operation.**

**The grid's line:**

```python
sd = np.nanmedian(np.nanstd(d, axis=0))
```

**The code's line, in `09_animal_level.py` and `10_robust_and_class.py`:**

```python
sd = np.nanmedian(np.nanstd(dv, axis=1))
```

**`np.nanstd(d, axis=0)` reduces over VOLUMES, giving one value per cell, and its median is the median across
cells of each cell's volume-to-volume SD.** **`np.nanstd(dv, axis=1)` reduces over CELLS, giving one value per
volume, and its median is the median across volumes of each volume's cell-to-cell SD.** **Those are different
quantities and they differ by orders of magnitude, because the cell-to-cell spread within a volume is much
larger than a single cell's volume-to-volume spread.**

**So the grid's weighting axis is not the code's weighting, and any interaction it measures is an interaction
between per-cell normalisation and something else.**

## 3. What is valid in the grid

**The per-cell normalisation axis is implemented as the code implements it, and its numbers stand:**

| post | without cell normalisation | with | contribution |
| --- | --- | --- | --- |
| 12 | 0.2175 | 0.1367 | **-0.0808** |
| 24 | 0.3933 | 0.1073 | **-0.2860** |
| 48 | 0.3984 | 0.1007 | **-0.2977** |

**So per-cell normalisation lowers `d_A` by 0.08 to 0.30, and its effect grows with the window.** **The ledger
records 0.3395 for this dimension from round 31; this grid gives 0.286 to 0.298 at the two longer windows, in
the same range.**

**And the twelve cells' overall span, 0.1002 to 0.3984, is consistent with round 31's grid.**

## 4. What the additivity question now needs

**The test has not been run, because the run that was meant to run it used the wrong axis.** **To run it
correctly, the grid must divide the two-dimensional `dv` array by `np.nanmedian(np.nanstd(dv, axis=1))`,
before any averaging over volumes.**

**And there is a second reason the answer matters, which this round makes visible: the two dimensions are not
independent in the way the ledger implies.** **Both are normalisations, one per cell and one per event, so the
order in which they are applied is itself a choice -- and in the code the per-event weighting is applied to
the raw differences, before the common mode, while per-cell normalisation as this line has implemented it is
applied per cell.** **A joint grid must therefore also record the ORDER, which the ledger does not.**

## 5. The pattern, now six consecutive rounds

| round | whose implementation was wrong |
| --- | --- |
| 29 | the grid's window convention differed from the code's |
| 31 | the grid's family excluded the code's common mode |
| 32 | the grid's common-mode axis tested a scalar instead of the per-volume form |
| 33 | the grid's cache held uniquely-named columns while the code spans all |
| 34 | the grid omitted the per-event weighting entirely |
| **39** | **this grid divided by the wrong axis** |

**Six consecutive rounds, six implementation errors, each found by comparing against the code or against a
previous round's measurement rather than by reasoning.** **The line's own grids are now the least reliable
artifacts it produces, and the ledger that summarises them inherits that.**

**The practical rule this suggests, and which the corpus index should carry: a re-implementation of a step
must be verified against the original's value for that step alone before it is used in any grid.**

## 6. Provenance

* Script `anatomy/37_joint_grid_ATTEMPT1_wrong_axis.py`; output `anatomy/RESULT_joint_grid_ATTEMPT1_wrong_axis.json`.
* **The defect was caught by comparing the weighting axis's contribution against round 38's measured +0.1767,
  which is the check that a re-implementation should have.**
* **No model was fitted. No causal claim is made.**
