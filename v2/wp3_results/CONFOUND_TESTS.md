# The three confounds, tested: two are dismissed and one is quantified

**Status: confounds addressed with measurements. One new substantive finding, with its limits stated.**
This resolves the three open items of `ANATOMY_FUNCTION_RETEST.md` and, in doing so, changes what the
finding is.

**No model was fitted. No biological claim beyond the measured contrast is made.**

---

## 1. What was run

Three controls on the same functional matrix as before (112 animals, 41,106 named pairs, responses
z-scored within each stimulus event), against anatomical matrices now **merged from both source tables**
to increase coverage:

```
merged witvliet_2020_8 + white_1986_whole :  chemical non-zero 3,150   gap-junction non-zero 1,427
functional matrix, off-diagonal and finite: 29,279 pairs
cell positions: 303 names, 303 coordinate rows; 298 of the 300 funatlas ids have coordinates
                (missing: AWCOF, AWCON)
```

**A parsing note recorded because it silently produced a wrong answer.** `anatlas_neuron_positions.txt`
stores its names **space-separated on a `#`-prefixed first line**, with the coordinates on the following
lines tab-separated. A reader that treats line 1 as a delimited header finds **zero** matching names and
would conclude no positions are available. **The file has 303 names, not none.**

## 2. C3 -- proximity. DISMISSED as the explanation.

**The concern was real and the data confirm it:** anatomically connected pairs **are** closer.

| contrast | mean distance, connected | mean distance, unconnected | difference |
| --- | --- | --- | --- |
| chemical | 0.494 | 0.731 | **-0.237** |
| gap junction | 0.289 | 0.728 | **-0.439** |
| chemical or gap | 0.427 | 0.742 | -0.315 |

**But adjusting for distance does not remove the association.** Regressing response on distance across
all pairs with coordinates and contrasting the residuals:

| contrast | connected | unconnected | raw difference | **distance-adjusted difference** | `d` |
| --- | --- | --- | --- | --- | --- |
| chemical | 1,785 | 27,204 | +0.0275 | **+0.0272** | 1.656 |
| gap junction | 755 | 28,234 | +0.0809 | **+0.0803** | 3.535 |
| chemical or gap | 2,314 | 26,675 | +0.0440 | **+0.0436** | 3.025 |

**The adjustment changes the estimate in the third decimal place.** Proximity is strongly confounded
with connectivity but **is not the mechanism producing the association.**

## 3. C1 -- edge-type asymmetry. ADDRESSED, and the difference survives.

**The concern:** chemical edges were written to one axis while gap junctions were symmetrised, so the
two contrasts were not symmetric measurements.

**The control:** restrict the chemical contrast to **reciprocal** chemical edges -- pairs with a chemical
connection in **both** directions -- which is the most conservative directed comparison available, and
compare against the gap-junction contrast, which is undirected by construction.

| contrast | connected pairs | difference | `d` |
| --- | --- | --- | --- |
| gap junction, undirected | 755 | **+0.0806** | **3.546** |
| chemical, **reciprocal only** | 569 | **+0.0143** | **0.558** |

**The gap-versus-chemical difference survives the conservative restriction.** On this read-out the
association with anatomical connectivity is roughly **six times weaker for chemical synapses than for
gap junctions**, and the chemical effect does not vanish, it is simply small.

## 4. C2 -- selection on measurement count. REAL, and now quantified rather than waved away.

**The concern:** pairs measured many times are the ones experimenters returned to; if they returned
because they saw a response, then measurement count carries outcome information and is not an exogenous
reliability weight. **This mattered because the previous document proposed reliability weighting as the
decisive re-test.**

**Measured within each stratum:**

| stratum | pairs | `corr(measurement count, response)` | quartile means, low to high count |
| --- | --- | --- | --- |
| chemical | 1,785 | **+0.0297** | -0.0241, -0.0041, +0.0030, +0.0429 |
| gap junction | 755 | **+0.0588** | +0.0154, +0.0176, +0.0583, **+0.1323** |
| unconnected | 26,965 | **+0.0042** | -0.0297, -0.0235, -0.0192, -0.0190 |

**Reading.** In unconnected pairs the correlation is essentially zero, so measurement count is not
globally aligned with response. **In connected pairs it is positive: +0.030 for chemical and +0.059 for
gap junction, and for gap junctions the top quartile response is 8.6 times the bottom quartile.**

> **Conclusion: measurement count is not an exogenous weight, and the contamination is stratum-specific
> -- negligible where there is no anatomical connection, small for chemical edges, and substantial for
> gap junctions. Any reliability-weighted version of these contrasts must therefore report the
> unweighted result alongside, and must not present weighting as removing an unrelated nuisance.**

## 5. What the measurement now says

**The finding, stated at the strength the evidence supports:**

> **In the per-animal records, anatomical connectivity predicts the functional response measured at
> `dt = 0.5 s`, and on this read-out the association is carried overwhelmingly by the gap-junction layer
> rather than the chemical layer: `d` approximately 3.5 against approximately 0.5-1.7. The contrast is
> robust to adjusting for inter-neuron distance and to restricting the chemical contrast to reciprocal
> edges.**

**The three limits that keep this from being a stronger claim, all of them live:**

1. **The read-out is one coarse scalar.** It is the post-window mean minus the pre-window mean over 8
   volumes. **The source atlas characterises sign, strength, temporal properties and causal direction.
   Nothing here speaks to those, and a timescale explanation for the chemical weakness is not excluded:
   a 4-second window may simply be too slow or too short to capture a chemical relay.** **This is the
   single most important limitation and it is not resolved.**
2. **Cell class was not controlled.** Gap-junction partners are frequently same-class or left-right
   partners. Distance is now controlled; **class is not**, and the bundled `cell_lineage.txt` and
   `neurons.json` class labels make it testable.
3. **C2's contamination applies to the gap stratum specifically**, which is where the effect is largest.
   **The gap effect should therefore be read as an upper bound pending a design that does not select on
   measurement count.**

**Still not claimed, and now for a sharper reason:** that the source paper's conclusion is wrong. **The
paper's claim concerns how functional propagation departs from anatomy across sign, strength, latency
and direction. This audit measures one coarse average and finds the electrical layer dominating it.
Those are compatible, and the paper's own reported difficulty in relating synapse counts to function is
consistent with the weak chemical association measured here.**

## 6. Next steps, revised in light of section 5

1. **Add the cell-class control** using the bundled `neurons.json` class labels and
   `cell_lineage.txt`. **Highest priority: it is the last uncontrolled confound on the gap result.**
2. **Test the timescale explanation** by computing the response at several post-stimulus windows
   (shorter and longer than 8 volumes) and asking whether the chemical association grows with lag.
   **This distinguishes "chemical synapses are weak" from "the window is wrong", which section 5
   limitation 1 leaves open.**
3. **Only then** re-run the reliability-weighted contrast with the C2 caveat reported.

## 7. Provenance and reproducibility

* Script: `anatomy/02_confounds_C1_C2_C3.py`; output `anatomy/RESULT_confounds.json`.
* Anatomical sources: `aconnectome_witvliet_2020_8.csv` and `aconnectome_white_1986_whole.csv`
  (**tab-separated**), plus `anatlas_neuron_positions.txt` (**space-separated header**), all from the
  `wormneuroatlas` wheel whose sha256 is in `../../wp1_data/WIRESHIFT_STAGE1_DATA_AUDIT.md`.
* Functional source: `exported_data.tar.gz`, sha256
  `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9be3832f6ce836`, per
  `../../wp1_data/WIRESHIFT_STAGE2_WT_AUDIT.md`.
* **No redistribution of the derived data.** No licence permitting it was found.
---

> **RETRACTION NOTICE, appended 2026-10-09.** The effect sizes in section 5 of this document are
> **window-dependent** and its headline claim is retracted by
> [`RETRACTION_window_dependence.md`](RETRACTION_window_dependence.md). Changing only the post-stimulus
> window moves the chemical association from `d = 1.154` at 1 s to `d = 3.118` at 16 s. **The text above
> is left unaltered so the error remains auditable; read it together with the retraction, which takes
> precedence.**
