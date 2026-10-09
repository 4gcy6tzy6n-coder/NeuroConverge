> **STATUS: THE `d` VALUES HERE ARE z-SCORES, NOT EFFECT SIZES (round 28 census).** The source JSON stores
> `diff / SE`, whose name in the file is `d`. A z-score quoted as an effect size overstates the effect by
> `sqrt(n)`, which here is hundreds. **The largest genuine effect size anywhere in this corpus is 0.7690, so
> any `d` of 2 or more is a z-score.** **See
> [`CENSUS_d_z_versus_d_effect.md`](CENSUS_d_z_versus_d_effect.md).** The numbers stand as statistics; the
> label does not. The text is left unaltered.

---

# Anatomy-versus-function re-test, and the three confounds that limit it

**Status: RESULT OBTAINED, CONFOUNDED, NOT YET INTERPRETABLE AS A CORRECTION.** This document records
what was measured and, explicitly, what cannot yet be concluded. No model was fitted.

**Relation to the previous document.** `ATLAS_RELIABILITY_AUDIT.md` measured the atlas's per-pair
reliability and named the test that would decide whether the gradient matters: *does the reported
anatomy-versus-function mismatch survive when pairs are weighted by reliability?* **This document runs
that test and reports that it is confounded three ways.**

---

## 1. A first attempt was invalid and is recorded as such

**The first version of this test used the bundled `aconnectome_default.h5`, a `(300, 300)` chemical
matrix and a `(300, 300)` gap-junction matrix, on the assumption that its axes follow the same
`neuron_ids` order as `funatlas.h5`.** Both files are 300 x 300, which made the assumption look safe.

**It is false.** Checked against the source tables, with the `funatlas` order applied:

| source table | edge type | entries matching | entries mismatching |
| --- | --- | --- | --- |
| `aconnectome_witvliet_2020_8.csv` | chemical | 135 | **1,756** |
| `aconnectome_witvliet_2020_8.csv` | electrical | 91 | **209** |
| `aconnectome_white_1986_whole.csv` | chemical | 157 | **2,079** |

**So `aconnectome_default.h5` is not indexed by the functional atlas's id order.** The invalid run also
produced `Cohen's d = 4.74` **on the misaligned matrix** -- **an implausibly large value that is itself
evidence of the misalignment**, and a reminder that a striking number is a reason to check, not to
publish. **That result is discarded and is not used anywhere.**

**The correction:** both anatomical matrices were rebuilt **by neuron name** from the tab-separated
source tables, so that every entry is keyed the way the functional side is keyed.

**Note on file format, recorded because it silently breaks naive parsers:** the files named
`aconnectome_*.csv` are **tab-separated**, not comma-separated. A comma-delimited reader yields a single
column and a `KeyError`, which is how this was caught.

## 2. The corrected measurement

**Anatomical matrices built by name** (edges whose neuron names are absent from the functional atlas's
300 ids are dropped and counted):

| source | chemical non-zero | gap-junction non-zero | dropped edges |
| --- | --- | --- | --- |
| `aconnectome_witvliet_2020_8.csv` | 1,891 | 592 | 313 |
| `aconnectome_white_1986_whole.csv` | 2,236 | 1,132 | 156 |

**Functional side:** 112 animals, **29,279 named pairs**, response z-scored within each stimulus event.
**1,606 pairs have an anatomical connection; 27,673 do not.**

**Contrasts.** "Connected" means a non-zero anatomical entry; "difference" is the connected mean minus
the unconnected mean; `d` is the difference over its standard error.

| contrast | connected | unconnected | difference | `d` |
| --- | --- | --- | --- | --- |
| chemical or gap, unweighted | +0.0050 (n=1,606) | -0.0203 (n=27,673) | **+0.0252** | **1.490** |
| **chemical only**, unweighted | -0.0111 (n=1,293) | -0.0193 (n=27,986) | **+0.0082** | **0.431** |
| **gap junction only**, unweighted | +0.0526 (n=426) | -0.0199 (n=28,853) | **+0.0726** | **2.421** |
| chemical or gap, weighted by measurement count | +0.0383 | -0.0148 | +0.0531 | -- |
| chemical or gap, pairs with >= 10 measurements | +0.0540 (n=480) | -0.0151 (n=6,972) | +0.0692 | 4.782 |
| chemical only, >= 10 measurements | +0.0299 (n=341) | -0.0126 (n=7,111) | +0.0426 | 2.693 |
| gap only, >= 10 measurements | +0.0951 (n=165) | -0.0131 (n=7,287) | +0.1082 | 4.040 |

**What reproduces.** The paper's basic direction reproduces on the per-animal data: **anatomically
connected pairs show a higher functional response than unconnected pairs.**

**What is new and needs care.** Splitting by edge type, the association is **strong for gap junctions
(`d = 2.42`) and weak for chemical synapses (`d = 0.43`)** -- and chemical synapses are the classical
anatomical predictor, and the paper's own subject is where functional propagation departs from anatomy.

## 3. The three confounds, none of which is resolved

**C1 -- edge-type asymmetry is built into the measurement, and this audit has not removed it.**
Chemical edges are directed and were written to one axis only; gap junctions were made symmetric
because electrical coupling is bidirectional. **The functional quantity is directed** (response of the
recorded cell to stimulation of the target). **So the two contrasts are not symmetric measurements of
the same thing, and the gap-versus-chemical comparison in section 2 is not yet a fair one.**

**C2 -- the "well-measured pairs show larger effects" pattern is at least partly selection, and may be
entirely selection.** Pairs with many measurements are the ones the experimenters chose to return to.
**If they returned because they saw a response, then conditioning on measurement count conditions on
the outcome**, and `d = 4.78` for well-measured pairs is not evidence that reliability improves the
anatomical correspondence. **This confound directly threatens the framing of the previous document**,
which proposed reliability weighting as the decisive re-test. **It is now clear that measurement count
is not an exogenous weight.**

**C3 -- proximity and cell-class confounds were not controlled.** Gap-junction partners may be
spatially adjacent or share a cell class, either of which could produce a functional correlation with no
role for the junction. The bundled distributions include cell positions
(`anatlas_neuron_positions.txt`), so this is testable, but **it has not been tested.**

**A fourth limitation, stated for completeness:** the functional response is a coarse scalar
(post-window mean minus pre-window mean at `dt = 0.5 s`), whereas the source atlas characterises sign,
strength, temporal properties and causal direction. **This audit compares only the coarsest of those,
so it cannot speak to the atlas's finer claims.**

## 4. What may and may not be claimed now

**May be claimed.** (a) The per-pair reliability gradient of the previous document stands, as a
measurement, and is unaffected by anything in this document. (b) The paper's basic anatomical
association reproduces on the raw per-animal records. (c) On this coarse read-out, the association is
stronger for gap junctions than for chemical synapses. (d) `aconnectome_default.h5` is not indexed by
the `funatlas.h5` id order -- a concrete interoperability defect in a widely used distribution, recorded
with the counts.

**May NOT be claimed.** That the paper's anatomical-mismatch conclusion is wrong or weakened; that
chemical synapses are unimportant; that reliability weighting changes any published conclusion; that
gap junctions carry the effect biologically rather than through proximity or class. **None of those is
established, and C1-C3 are each sufficient to produce the observed pattern artefactually.**

## 5. The next steps, ordered

1. **Resolve C1** by restricting both contrasts to the undirected sub-graph, or by evaluating chemical
   edges in their stated direction only and comparing against a direction-matched null. **Until this is
   done the edge-type comparison in section 2 should not be quoted.**
2. **Resolve C2** by testing whether measurement count predicts the response *within* connected and
   *within* unconnected pairs separately, and by finding an exogenous reliability proxy rather than
   using the measurement count.
3. **Resolve C3** using `anatlas_neuron_positions.txt` to add distance and cell class as covariates.
4. **Only then** re-run the reliability-weighted version of the paper's own comparison.

## 6. Provenance

* Anatomical sources: `aconnectome_witvliet_2020_8.csv`, `aconnectome_white_1986_whole.csv`,
  `aconnectome_default.h5` from the `wormneuroatlas` wheel, sha256 of the wheel recorded in
  `WIRESHIFT_STAGE1_DATA_AUDIT.md`.
* Functional source: `exported_data.tar.gz`, sha256
  `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9b3832f6ce836`, recorded in
  `WIRESHIFT_STAGE2_WT_AUDIT.md`.
* Analysis script: `anatomy/01_anatomy_vs_function.py`; outputs `anatomy/RESULT_corrected.json` and the
  discarded `RESULT_invalid_idorder.json`.
* **No model was fitted. No biological claim is made. No licence permitting redistribution of the
  derived data was found, so nothing is redistributed.**
---

> **RETRACTION NOTICE, appended 2026-10-09.** The effect sizes in section 2 of this document are
> **window-dependent** and its headline claim is retracted by
> [`RETRACTION_window_dependence.md`](RETRACTION_window_dependence.md). Changing only the post-stimulus
> window moves the chemical association from `d = 1.154` at 1 s to `d = 3.118` at 16 s. **The text above
> is left unaltered so the error remains auditable; read it together with the retraction, which takes
> precedence.**
---

> **SPECIFICATION MISMATCH NOTICE, appended 2026-10-09.** Every `d` value in this document was computed
> under a specification that differs from the source's in at least five respects -- window, amplitude
> reference, contiguous-run requirement, derivative criterion and tail handling. The source's actual rule
> is recovered in [`SOURCE_RULE_RECOVERED.md`](SOURCE_RULE_RECOVERED.md). **These numbers are therefore not
> estimates of the paper's quantity and must not be read as such.** The text is left unaltered so the
> mismatch remains auditable.
