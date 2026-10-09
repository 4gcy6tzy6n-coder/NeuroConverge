> **STATUS: INTERPRETATION SUPERSEDED (its own date).** This document is retained unaltered as the
> record of a reading that was later withdrawn or narrowed: **the original window-dependence reading**. The measurements in it stand;
> the interpretation does not. **Superseded by [`WINDOW_RESOLVED.md`](WINDOW_RESOLVED.md)**, which takes precedence and records
> that this document is itself the retraction of an earlier reading and is retained as the record of it.
>
> **The title above still states the superseded reading, deliberately, so the document remains findable
> by the claim it made.** Read the body as a dated record and the linked document as current.

---

# CORRECTION AND RETRACTION: the effect size is a function of the post-stimulus window

**Status: this document retracts a headline claim made in two earlier documents of this project, and
replaces it with a measurement that is stable across the choices tested.** No model was fitted.

**This is the fifth self-found defect in this analysis line, and the largest.** It is recorded in full
because the retracted claim was already committed and pushed, and a silently edited history cannot be
audited.

---

## 1. What is retracted

**Retracted claim.** `ANATOMY_FUNCTION_RETEST.md` and `CONFOUND_TESTS.md` both state, as the finding:

> *"on this read-out the association is carried overwhelmingly by the gap-junction layer rather than the
> chemical layer, `d` approximately 3.5 against approximately 0.5-1.7."*

**That sentence is not supported.** `d = 0.5-1.7` for chemical synapses is a property of **the analysis
window used**, not of the chemical layer.

**What replaces it.** The association between anatomical connectivity and functional response grows
**monotonically with the post-stimulus window for both layers**, and the chemical layer reaches
`d = 3.118` at a 16-second window, which is **not weak**. **The gap-versus-chemical ratio is not a
constant either: it ranges from 1.19 to 2.94 across the five windows tested.**

**No biological fact changed between the two analyses. Only the window did.**

## 2. The measurement

Response defined as mean over the post-stimulus window minus mean over a fixed 8-volume pre-stimulus
window, z-scored within each stimulus event, identical in every other respect to the earlier analyses.
Five post-stimulus windows, on the same 112 animals and 29,279 pairs:

| post-stimulus window | chemical `d` | gap-junction `d` | gap / chemical |
| --- | --- | --- | --- |
| 1.0 s (2 volumes) | 1.154 | 1.370 | 1.19 |
| 2.0 s (4 volumes) | 1.317 | 1.932 | 1.47 |
| **4.0 s (8 volumes) -- used by the earlier documents** | **1.656** | **3.546** | 2.14 |
| 8.0 s (16 volumes) | 1.970 | 5.787 | **2.94** |
| 16.0 s (32 volumes) | **3.118** | 7.629 | 2.45 |

**Two facts, both of which the earlier documents got half-right and half-wrong:**

1. **The ordering is stable: gap junction exceeds chemical at every window tested.** 1.19, 1.47, 2.14,
   2.94, 2.45. **This part of the earlier claim survives.**
2. **The magnitudes are not stable at all.** Chemical moves by a factor of **2.70** and gap junction by
   **5.57** across the same five choices. **So "how strong is the connectivity-function association" has
   no single answer on this data; it has an answer per window.**

## 3. The cell-class control, and what it does to the gap claim

Using the 447 class labels in `neurons.json`; 298 of 300 atlas ids have coordinates and class labels.

| layer | connected pairs | of which same-class | same-class contrast | cross-class contrast |
| --- | --- | --- | --- | --- |
| chemical | 1,785 | 56 (3.1 %) | **d = -1.623** (n=56 vs 225) | **d = 1.556** (n=1,729 vs 27,269) |
| gap junction | 755 | 120 (15.9 %) | **d = 0.233** (n=120 vs 161) | **d = 2.171** (n=635 vs 28,363) |

**Reading.** **Within same-class pairs the connectivity association essentially vanishes: `d = 0.233`
for gap junctions and reverses in sign for chemical synapses on a small sample.** The association lives
in **cross-class** pairs. A coherent interpretation is that same-class partners -- left-right homologues
and the like -- co-respond whether or not they are connected, washing out the connectivity signal, while
cross-class connectivity remains informative.

**What this does NOT license:** the chemical same-class reversal is on **56 connected pairs** and is not
interpreted. **The class control was run at the 4-second window only, so it has not been shown to hold
at other windows**, and on the evidence of section 2 there is no reason to assume it does.

## 4. Why this is the finding, and not merely an embarrassment

**The project's governing question is which evidential transitions require separate empirical support.
This is a direct instance, measured rather than asserted.**

> **A published association between anatomical connectivity and neural function, when re-measured from
> the same raw records, changes by a factor of 2.7 to 5.6 depending on the post-stimulus window alone.
> The window is an analysis choice, it is not usually reported as a result-bearing parameter, and on this
> data it determines whether the chemical layer looks negligible or substantial.**

**Combined with the earlier reliability measurement** -- `r_full = 0.23` for the bulk of pairs, 0.82 only
for the best-measured 600 -- **the picture is that both the reliability of an atlas entry and the size of
the association computed from it are functions of unreported analysis choices.**

**What is still not claimed:** that the source paper is wrong. Its claims concern sign, strength,
temporal properties and causal direction, which this audit does not measure. **A window dependence in a
coarse averaged read-out is entirely compatible with a careful multi-property analysis**, and the
paper's own reported difficulty relating synapse counts to function is consistent with everything here.

## 5. Standing limitations, updated

1. **Window dependence is now demonstrated for the association, but the "correct" window is not
   determined.** This audit shows the sensitivity; it does not resolve it. **A defensible choice would
   have to come from the known timescales of calcium indicators and synaptic transmission, not from the
   data.**
2. **The class control was run at one window only.** Extending it across windows is required before the
   cross-class interpretation can be relied on.
3. **Measurement-count contamination (C2) remains**, and is strongest in the gap stratum.
4. **Everything here is one coarse scalar.** Sign, latency and direction are untouched.

## 6. Recommendation to the project, and to any reader of the earlier documents

**`CONFOUND_TESTS.md` section 5 and `ANATOMY_FUNCTION_RETEST.md` section 4 carry a claim that this
document retracts.** They are not rewritten -- **a retraction appended to a wrong claim is more useful
than a quietly corrected one** -- but their section-5 "finding" paragraphs should be read together with
this document, and this document takes precedence.

**Next steps, re-ordered by what the new evidence makes urgent:**

1. **Determine a defensible window** from the calcium indicator's kinetics and reported synaptic delays,
   and re-run every contrast at that window.
2. **Run the class control across all windows.**
3. **Only then** the reliability-weighted contrast.

## 7. Provenance

* Script `anatomy/03_timescale_and_class.py`; output `anatomy/RESULT_timescale_class.json`.
* Same inputs and checksums as the earlier documents; see `CONFOUND_TESTS.md` section 7.
* **No model was fitted. No biological claim beyond the measured contrasts is made.**
---

> **SPECIFICATION MISMATCH NOTICE, appended 2026-10-09.** Every `d` value in this document was computed
> under a specification that differs from the source's in at least five respects -- window, amplitude
> reference, contiguous-run requirement, derivative criterion and tail handling. The source's actual rule
> is recovered in [`SOURCE_RULE_RECOVERED.md`](SOURCE_RULE_RECOVERED.md). **These numbers are therefore not
> estimates of the paper's quantity and must not be read as such.** The text is left unaltered so the
> mismatch remains auditable.
