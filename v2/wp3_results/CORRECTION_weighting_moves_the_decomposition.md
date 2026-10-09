# The per-event weighting is a sixth undeclared specification dimension, worth 13 points in `eps`

**Status: the weighting moves V2-C3's shares substantially, so every share this line has reported for V2-C3 is
an unweighted value.** **The weighting is a legitimate analysis choice, not an error; what was wrong was
comparing weighted against unweighted.** No model was fitted.

**This is the sixteenth self-found defect.**

---

## 1. Why this was tested

**Round 34 established that `dvs = dv / sd_event` in `09_animal_level.py` is a per-event weighting, that it is
worth `+0.3356` in `d_A`, and that five of this line's grids omitted it.** **One of those five is the
three-level variance decomposition behind V2-C3.**

**So the question was whether the weighting moves those shares as much as it moves `d_A`.** **It does.**

## 2. The result

**Both decompositions were run on the same 3,333 events from 112 animals, over 192,277 (animal, pair) units,
differing only in whether the per-event `sd` division is applied.**

| component | **without the weighting** | **with the weighting** | change |
| --- | --- | --- | --- |
| between-pair | 53.5 % | 55.4 % | +1.9 points |
| **measurement error, `eps`** | **30.2 %** | **17.3 %** | **-13.0 points** |
| **pair-specific animal, `beta`** | **15.6 %** | **27.1 %** | **+11.5 points** |
| animal offset, `alpha` | 0.7 % | 0.2 % | -0.4 points |

> **The weighting moves the measurement-error share by 13 points and the pair-specific animal share by 11.5,
> in opposite directions, and leaves the between-pair share nearly unchanged.**

## 3. What this does to every share V2-C3 has reported

**All of them are unweighted values.** **The record:**

| where | `eps` reported | weighting |
| --- | --- | --- |
| round 12, `RESULT_three_level_variance.json` | 37.5 % | **omitted** |
| round 26, the minimum-animals sweep | 37.5 % to 38.5 % | **omitted** |
| round 29, the eight-specification grid | 38.7 % to 57.1 % | **omitted** |
| **this round, the code's own specification** | **17.3 % with, 30.2 % without** | **measured** |

**So the line's reported measurement-error share has ranged 17 to 57 per cent depending on specifications
that were never varied together, and the single largest mover among them is the one that was omitted from
every grid until now.**

## 4. The honest framing: a choice, not an error

**The per-event `sd` division is a defensible analysis choice.** **It weights each stimulus event by the
inverse of that event's across-cell response spread, which is a reasonable thing to do and is what the source
pipeline does.** **An unweighted analysis is also defensible.**

**What was wrong is that this line's grids computed unweighted values and compared them against the code's
weighted ones, and attributed the difference to the causes those rounds proposed and eliminated.** **Rounds
29, 31, 32 and 33 each spent a round on a hypothesis that the weighting explains in one line.**

## 5. V2-C3's third revision, and what is now stable

**The claim has now been narrowed three times, and this round adds a fourth dimension rather than a fourth
narrowing:**

> **A pair's response decomposes into a between-pair share of 53 to 55 per cent, a within-cell
> measurement-error share of 17 to 57 per cent depending on whether events are weighted by their inverse
> across-cell spread and on the window, baseline and normalisation, a pair-specific animal share of 16 to 27
> per cent under the same conditions, and a homogeneous animal offset under 1 per cent.**

**What remains stable across every specification the line has computed, weighted or not:**

* **measurement error is never the smallest component;**
* **the pair-specific animal component is positive whenever the ill-posed stratum is excluded;**
* **the between-pair share is the largest single component in every run.**

**And the sentence that survives in its original form, from round 12: measurement error is a large share of
the variance in a pair's response in this atlas, and the atlas does not report it.** **It survives because it
names no number, and every number the line has attached to it has moved.**

## 6. The specification dimensions this line has now found, in the order they were discovered

| # | dimension | size | declared anywhere? |
| --- | --- | --- | --- |
| 1 | post-stimulus window | about 0.22 in `d_A` | no |
| 2 | baseline convention | about 0.01 | **yes, in the source** |
| 3 | per-cell normalisation | about 0.30 | no |
| 4 | common-mode removal, and its per-volume form | 0.01 to 0.03 | no |
| 5 | the cell pool the common mode spans | 0.0038 | no |
| **6** | **per-event weighting by inverse across-cell spread** | **0.34 in `d_A`, 13 points in `eps`** | **no** |

**Six undeclared dimensions, and the largest is the one found last.** **This is V2-C4's claim demonstrated
rather than argued: the specification is in the code and not in the file, and the line that wrote the code
needed thirty-six rounds to enumerate them.**

## 7. Provenance

* Script `anatomy/35_decomposition_weighted.py`; output `anatomy/RESULT_decomposition_weighted.json`.
* **The same script's weighted arm reproduces the code's `d_A = 0.7289` exactly, which is the check that the
  weighting is implemented correctly rather than merely included.**
* **No model was fitted. No causal claim is made.**
