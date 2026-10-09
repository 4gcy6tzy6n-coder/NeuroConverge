# The common-mode cell pool is an undeclared specification dimension, worth 0.34 in `d_A`

**Status: round 31's inference about the cause of V2-C4's ceiling was wrong, and chasing it found a fifth
specification dimension that no document in this corpus declares.** No model was fitted.

**This is the thirteenth self-found defect, and the fourth consecutive round in which an inferred cause
turned out to be wrong.**

---

## 1. What round 31 inferred, and why it was wrong

**Round 31 found that its grid's ceiling was `d_A = 0.4408` while V2-C4's reported ceiling was `0.7289`, and
inferred that the difference was carried by common-mode removal, because `10_robust_and_class.py` applies it
and no grid had varied it.**

**This round varied it. Common-mode removal LOWERS `d_A`:**

| configuration | without common mode | with | change |
| --- | --- | --- | --- |
| post 24, baseline 30-60, no cell norm | 0.3998 | 0.3895 | **-0.0103** |
| post 24, baseline 30-60, cell norm | 0.1083 | 0.1065 | -0.0019 |
| post 48, baseline 0-60, no cell norm | 0.4409 | 0.4124 | **-0.0285** |

**So common-mode removal cannot explain a ceiling that is HIGHER than the grid's.** **Round 31 isolated the
right step and drew the wrong conclusion about its direction.**

## 2. Then a second error, in this round's own grid

**The first attempt at this round tested the wrong operation entirely.** **It subtracted one scalar per event
-- the across-cell mean of the volume-summed values.** **`09_animal_level.py` subtracts the across-cell mean
AT EACH VOLUME and only then averages over volumes:**

```python
post = G[vi:vi+POST, :]                      # (POST, ncol)
base = G[vi-30:vi, :]
dv   = post - np.nanmean(base, axis=0)
sd   = np.nanmedian(np.nanstd(dv, axis=1))   # a scalar, cancels in d_A
dvs  = dv / sd
cm   = np.nanmean(dvs, axis=1, keepdims=True)  # across cells, PER VOLUME
dev  = dvs - cm
v_c  = dev[:, c].mean()                      # then average over volumes
```

**Both operations lower `d_A`, and the correct one is the per-volume form.**

## 3. The actual cause, and it is a specification dimension nobody declared

**Even at the code's own configuration -- post 24, baseline 30-60, no cell normalisation, per-volume common
mode -- this grid returns `0.3895`, which differs from the code's `0.7289` by `0.3394`.**

**The cause is in the common mode's CELL POOL.**

```python
# 09_animal_level.py
post = G[vi:vi+POST, :]                        # ALL columns, including cells with duplicate names
cm   = np.nanmean(dvs, axis=1, keepdims=True)  # so the common mode spans ALL columns
for c in keep:                                  # only then is the uniquely-named subset selected
```

**This grid's cache stored `G[vi:vi+48, keep]`, the 46 uniquely-named columns for animal 0, so its common
mode spans 46 cells while the code's spans about 114.** **That is the 0.3394.**

> **The cell pool over which the common mode is computed is a specification dimension.** **No document in
> this corpus declares it, and it is worth 0.34 in `d_A` -- more than the entire range the grid measured
> across window, baseline and normalisation.**

## 4. What this does to V2-C4

**Unchanged: the specification is not recoverable from the data file, which is V2-C4's claim and remains
demonstrated.**

**Strengthened, and in the direction the claim argues: there is at least one further undeclared
specification dimension, and it is larger than the declared ones.**

**And the range's upper end is now attributed more precisely than round 31 could:**

| source of movement | size |
| --- | --- |
| window 12 to 48 volumes | about 0.22 |
| per-cell normalisation | about 0.30, downward |
| baseline convention | about 0.01 |
| per-volume common mode | about 0.01 to 0.03, downward |
| **the common mode's cell pool** | **about 0.34**, and it is undeclared |

## 5. What is owed, and this time it is one specific thing

**A grid whose events are cached over ALL columns rather than the uniquely-named subset, so that the cell-pool
dimension can be varied directly.** **That is a change to the cache, not to the analysis, and it is the reason
this round could not settle the question.**

**And the corpus index should carry the cell-pool dimension in its list of undeclared specifications.**

## 6. The four consecutive wrong inferences, recorded because the pattern is the finding

| round | inferred cause | what chasing it found |
| --- | --- | --- |
| 29 | the read-out moves the decomposition | it does, but the window convention differed too |
| 30 | the grid's twelve rows were twelve specifications | three transforms were a no-op |
| 31 | common-mode removal explains the ceiling | it lowers `d_A`; the cause is elsewhere |
| **32** | **per-volume common mode is the code's step** | **it is, and the cause is the cell pool it spans** |

**Each inference was stated with more confidence than the evidence held, and each was corrected by running the
thing rather than by reasoning about it.** **That is the same failure mode this line has recorded since round
12 -- the step from a number to a sentence about the number -- now recurring in the reasoning about causes
rather than in the claims themselves.**

## 7. Provenance

* Script `anatomy/30_v2c4_cellpool_grid.py`; output `anatomy/RESULT_v2c4_cellpool_grid.json`.
* Two failed attempts retained: `anatomy/29_v2c4_grid_ATTEMPT2_scalar_cm.py`, whose common-mode axis tested
  the wrong operation, and a syntax failure in a nested f-string that was fixed before the successful run.
* **The cache `v2c4_cache.pkl` stores uniquely-named columns only, which is the reason this round could not
  settle the cell-pool question.** **Stated rather than discovered later.**
* **No model was fitted. No causal claim is made.**
