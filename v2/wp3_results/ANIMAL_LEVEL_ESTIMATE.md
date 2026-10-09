# The unit is the animal: a 19-fold pseudo-replication inflation, and the effect that survives it

**Status: the first defensible effect estimate in this line, and the identification of the error that
inflated every previous one.** The read-out still differs from the source's in ways stated in section 6.

**No model was fitted. The claim is a predictive association under observational data, not a causal
intervention.**

---

## 1. What was measured

**Unit: the animal.** For each of 112 animals, the mean common-mode-corrected response of its anatomically
connected pairs and of its unconnected pairs, over a 24-volume (12 s) post-stimulus window with a
30-second pre-stimulus baseline taken from its late half (the source's convention, `shift_vol = 60`,
`baseline_range = [30, 60]`). **109 animals yielded both strata.**

**Contrast: paired across animals.**

| quantity | value |
| --- | --- |
| connected mean | +0.08796 |
| unconnected mean | +0.01094 |
| **paired difference** | **+0.07702** |
| across-animal SD of the difference | 0.10567 |
| standard error | 0.01012 |
| **`t` (df = 108)** | **7.610** |
| **`p`** | **1.09e-11** |
| **standardised effect, paired** | **`d = 0.7289`** |

**By layer, same procedure:**

| layer | animals | difference | `d` | `t` | `p` |
| --- | --- | --- | --- | --- | --- |
| chemical synapse | 108 | +0.04753 | **0.4145** | 4.307 | 3.68e-05 |
| gap junction | 109 | +0.12856 | **0.7690** | 8.028 | 1.31e-12 |

**Both layers show a positive association at the animal level, and the gap-junction association is
larger.** The ordering matches what every earlier, wrongly-united analysis found; **the magnitudes do
not, and the earlier ones are wrong.**

## 2. The error that produced every previous number in this line

**The identical contrast, computed with pair-measurements as the unit instead of animals, gives:**

| unit | chemical `d` | gap-junction `d` | connected `d` |
| --- | --- | --- | --- |
| **pair-measurements** (n = 195,809 unconnected) | **4.641** | **13.796** | **11.048** |
| **animals** (n = 109) | **0.4145** | **0.7690** | **0.7289** |
| **inflation factor** | **11.2x** | **17.9x** | **15.2x** |

**A `d` of 13.8 is not a plausible biological effect size**, and it is the direct consequence of treating
~196,000 pair-measurements drawn from 3,333 stimulus events in 112 animals as independent observations.
The standard error collapses because the denominator is `sqrt(195809)` instead of `sqrt(109)`.

> **This is the project's own standing warning -- that neuron pairs and frames are not independent
> biological replicates -- applied to the project's own analysis. The warning was written into
> `TASK_SPEC_DRAFT.md` section 3.1 in an earlier phase and then violated here for four rounds.**

**The consequence for the record:** every `d` in `ANATOMY_FUNCTION_RETEST.md`, `CONFOUND_TESTS.md`,
`RETRACTION_window_dependence.md`, `WINDOW_RESOLVED.md` and `FINAL_ESTIMATE_AND_COLLIDER_WARNING.md` is
inflated by roughly one order of magnitude by this error alone, **in addition to** the specification
mismatch already recorded. **They are retained with notices; they must not be used.**

## 3. Why the result in section 1 is credible

* **The unit is the animal**, which is the independent biological replicate, and it is the unit the
  project's own power table is written in. **`n = 109` with a paired `d = 0.729` clears the 80 %-power
  threshold for this design, `(1.96+0.84)/sqrt(109) = 0.268`, by a wide margin.**
* **The effect size is in a biologically plausible range.** Nothing here requires explaining an effect of
  14 standard deviations.
* **The baseline convention makes little difference**, measured this session: a 61-volume pre-window with
  a late-half baseline gives connected `d = 11.05`, a 8-volume pre-window gives 12.46, and a 61-volume
  pre-window with a full baseline gives 9.76 at the pair level. **So the round-5 root-cause hypothesis --
  that the apparent slow rise came from a contaminated baseline -- is NOT supported**, and the effect
  survives all three conventions. **That hypothesis is withdrawn here.**
* **The direction and the layer ordering agree with the source's own reported finding** that anatomical
  connectivity relates to functional propagation.

## 4. The 30-second pre-window, and what it did and did not fix

**The source's convention was recovered from the code: `delta_t_pre = 30.0` (`Funatlas.py:2214`), so
`shift_vol = 60` volumes, with the baseline taken from `[shift_vol//2, shift_vol]`, i.e. 15 to 30 seconds
before the stimulus.**

**Section 3 shows the effect is not baseline-sensitive at the pair level.** What the 30-second pre-window
does change is **which events are usable**: requiring 60 volumes of history and a 24-volume post-window
reduced 3,380 events to 3,333, a small loss. **So the source's long pre-window is affordable and should be
used, but it is not the explanation for anything.**

## 5. What this does and does not establish

**Established, at the animal level, in this dataset, with this read-out:**

> **Anatomically connected neuron pairs show a higher functional response than unconnected pairs, by a
> standardised paired effect of `d = 0.729` across 109 animals (`p = 1.1e-11`), with the association
> larger for gap junctions (`d = 0.769`) than for chemical synapses (`d = 0.415`).**

**Not established:**

* **Any causal claim.** This is an observational association; the structural and functional data come from
  **different animals**, so no same-animal synaptic causal statement is available. **The mapping class
  remains `CELL_CLASS_ALIGNED_ACROSS_SPECIMENS`.**
* **That this is the source paper's quantity.** The read-out still omits the source's inclusion rule
  entirely: no `absmax` amplitude criterion, no contiguous-run requirement, no derivative criterion, no
  tail criterion, no slope check. **The section-5 implementation task of `SPECIFICATION_COMPLETE.md`
  remains outstanding and is still the correct next step.**
* **Independence of the two strata.** Connected and unconnected pairs within one animal share events,
  cells and indicator state; **the paired test accounts for the animal, not for within-animal
  dependence.** The reported `p` is therefore optimistic and is reported as a description of the
  contrast, not as a calibrated inference.
* **That the class and selection confounds are resolved.** Cell class was controlled only at the pair
  level in an earlier round and not re-run here; and measurement count is known to be non-exogenous.

## 6. What is now owed, in order

1. **Re-run section 1's contrast with the source's actual inclusion rule** (`SPECIFICATION_COMPLETE.md`
   section 5), which is the only way the number becomes comparable to the published one.
2. **Re-run the class control at the animal level**, since the earlier class result was pair-level and
   therefore inflated in the same way.
3. **Handle within-animal dependence properly** -- a mixed model or a cluster-robust standard error with
   the animal as the cluster -- rather than the simple paired `t` used here.
4. **Then** the reliability-weighted version, if it is still worth doing.

## 7. Provenance

* Script `anatomy/09_animal_level.py`; outputs `anatomy/RESULT_animal_level.json` and
  `anatomy/RESULT_baseline_conventions.json`.
* Anatomical and functional inputs and their checksums: `CONFOUND_TESTS.md` section 7.
* Source `shift_vol` and baseline convention: `pumpprobe/Fconn.py:170, 256` with
  `pumpprobe/Funatlas.py:2214`.
* **No model was fitted. No biological claim beyond the measured association is made.**
---

> **CAVEAT CORRECTED, appended 2026-10-09.** Section 5 states that the reported `p` is "therefore
> optimistic" because within-animal dependence is not modelled. **That caution is withdrawn by
> [`ROBUSTNESS_AND_CLASS_AT_ANIMAL_LEVEL.md`](ROBUSTNESS_AND_CLASS_AT_ANIMAL_LEVEL.md) section 1:**
> re-computed with each animal weighted by its pair counts, the weighted and unweighted `t` agree closely
> and the weighting moves the gap-junction statistic further from the null, so **the animal-level paired
> test does account for the dependence that matters.** The pairs are still not independent replicates --
> the inflation factor of 11 to 18 times measured above is real -- but **that caution belongs to the wrong
> unit, not to this one.** The text is left unaltered.
