# The source's own inclusion rule, implemented and run: the blocking item is closed

**Status: the criterion is implemented, verified on a five-animal harness before the full run, and the
animal-level contrast re-computed under it.** This closes the item that has been named blocking since
round 4. No model was fitted.

---

## 1. What was implemented

Traced in `SOURCE_RULE_RECOVERED.md` and `SPECIFICATION_COMPLETE.md`, all line-numbered to
`pumpprobe/Fconn.py` and `pumpprobe/Funatlas.py`:

| element | value |
| --- | --- |
| pre-stimulus window `shift_vol` | **60 volumes = 30 s** (`delta_t_pre = 30.0`) |
| baseline | the late half of that window, volumes 30-60 |
| analysis window `max_vol_n` | `int((int_btw_stim-5)/dt)`, computed **per event** from the measured inter-stimulus interval, capped at 60 volumes |
| `ampl_thresh`, `ampl_min_time` | 1.0, 5.0 s -> **run of more than 10 contiguous volumes** |
| half-threshold variant | **more than 20 contiguous volumes above `0.5 x` the threshold** |
| `deriv_thresh`, `deriv_min_time` | 1.0, 2.0 s -> **at least 4 volumes** |
| amplitude reference | **`absmax` of the pre-stimulus signal**, per cell |
| response | `sum` of the baseline-subtracted trace over the analysis window |

**Deliberately omitted, and recorded rather than silently skipped:** criterion 2 (the tail rule for
previously-selected neurons, which requires tracking selection across consecutive stimulations),
criterion 2* (the slope check), the exact Savitzky-Golay derivative (`np.gradient` is used instead), and
the NaN criterion. **So this is a close but not exact reproduction, and the differences are stated.**

## 2. Retention is plausible

```
112 animals, 3,333 events  ->  2,230 pass  (66.9 %)
rejections: amplitude criterion 896, derivative criterion 207
```

**Measured on a five-animal harness first — 175 events, 115 passing, 65.7 % — which agreed with the full
run.** The retention is consistent with a rule that keeps events where the stimulated neuron responded,
which the source describes as a requirement for inclusion.

**The binding constraint is the amplitude criterion, not the derivative one:** the derivative count has a
median of 29 to 41 against a threshold of 4, so it almost always passes.

## 3. The result

**Animal-level paired contrast, unit = animal:**

| quantity | value |
| --- | --- |
| animals with both strata | **109** |
| paired difference | **+61.40360** (raw fluorescence units, so not comparable across read-outs) |
| across-animal SD | 136.61908 |
| **`t`** | **4.692** |
| **standardised paired effect** | **`d = 0.4495`** |

## 4. Three animal-level estimates now exist, and they agree in sign and significance

| specification | unit | `d` |
| --- | --- | --- |
| **the source's own rule** (30 s pre-window, `absmax` amplitude and derivative criteria, per-event 52-volume window) | animal | **0.4495** |
| 4 s window, common-mode removed, no inclusion rule | animal | **0.7289** |
| either of the above | **pair-measurement** | **11.048** |

**Under every specification the effect is positive and significant at the animal level, and under the
wrong unit it is inflated by more than an order of magnitude.** Filtering *reduces* the standardised
effect, from 0.73 to 0.45, which is what one expects when the filter selects on the stimulated neuron's
response.

> **The honest summary: on this dataset, anatomical connectivity predicts functional response; the
> standardised animal-level effect is between 0.45 and 0.73 depending on the inclusion rule and window;
> and treating pair-measurements as the unit makes it about 11 to 18 times larger.**

## 5. What this does and does not settle

**Settled:** the implementation gap that invalidated every earlier `d` value is closed for the primary
criteria. **The number `d = 0.4495` is produced by a rule that traces to the source's own code, with its
four omissions named.**

**Not settled:**

* **The four omissions in section 1**, each of which could move the estimate. Criterion 2 in particular
  exists to handle exactly the tail phenomenon this line found independently.
* **The read-out is still not the source's published quantity.** The source reports sign, strength,
  temporal properties and causal direction; this line reports one signed integral over a window.
* **`d = 0.45` has not been compared against the source's own reported effect**, because the source
  reports its result in terms of STAM capture and reproducibility percentages rather than a standardised
  paired effect. **A like-for-like comparison has not been constructed.**
* **The class result and the reliability result have not been re-run under this rule.** Both were
  computed under other specifications.
* **`unc-31` has not been touched at all** in this line.

## 6. A process defect in this line's method, and its fix

**Three consecutive rounds launched a long full-data job and then discovered an implementation bug from
its output.** The corrected pattern, used for the first time in this round and worth keeping: **run the
criterion on a five-animal harness and print internal diagnostics — pass rate, rejection-reason counts,
and the medians of `absmax`, the post-stimulus peak, and the contiguous-run lengths — before launching
the full run.** The harness found the last defect in seconds rather than after eight minutes, and it also
established that the pass rate was plausible rather than zero.

**Five defects were found in the criterion implementation alone:**

| # | defect | symptom |
| --- | --- | --- |
| 1 | per-cell quantities collapsed to scalars (`prev_dr`, `pre_avg_sig`) | 0 of 3,333 events passed |
| 2 | `absmax` used as a cell vector against the target's scalar window | `ValueError: shapes (51,) (114,)` |
| 3 | only the target column passed into the criterion, losing the cell axis | same as 1 |
| 4 | `max_vol_n` not derived per event from the measured interval | would have used a fixed window |
| 5 | no fast harness, so each defect cost a full 8-minute run | three wasted runs |

**All five are recorded; none is deleted.**

## 7. Provenance

* Scripts `anatomy/11_source_rule.py` and the fast harness `anatomy/11a_source_rule_harness.py`;
  output `anatomy/RESULT_source_rule.json`.
* Source rule lines: `pumpprobe/Fconn.py:141, 170, 261, 277-282, 313-319, 348-392, 430-467`;
  `pumpprobe/Funatlas.py:2214, 2426`.
* **No model was fitted. The association is observational and cross-individual; no causal claim is made.**
