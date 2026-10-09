> **STATUS: THE `d` VALUES HERE ARE z-SCORES, NOT EFFECT SIZES (round 28 census).** The source JSON stores
> `diff / SE`, whose name in the file is `d`. A z-score quoted as an effect size overstates the effect by
> `sqrt(n)`, which here is hundreds. **The largest genuine effect size anywhere in this corpus is 0.7690, so
> any `d` of 2 or more is a z-score.** **See
> [`CENSUS_d_z_versus_d_effect.md`](CENSUS_d_z_versus_d_effect.md).** The numbers stand as statistics; the
> label does not. The text is left unaltered.

---

# CRITICAL: the estimate is not stable, and the inclusion rule may be a collider

**Status: a negative and methodologically central result. It does NOT overturn the source paper, and the
sign reversal it reports may be an artefact of this audit's own construction.** No model was fitted.

---

## 1. The measurement

All three corrections applied together, each justified in earlier documents: the **4-second** post-stimulus
window (fixed by the 500 ms stimulus and the source's stated criterion), **common-mode removal** (the
across-cell mean at each timepoint), and an **event-inclusion rule** modelled on the source's
*"did not meet both thresholds for a contiguous 4 s"*.

```
events 3,380  ->  passing this audit's implementation of the inclusion rule  371  (11.0%)
```

| layer | n | mean | `d` against unconnected |
| --- | --- | --- | --- |
| unconnected | 22,419 | +0.00960 | -- |
| **chemical** | 1,287 | **-0.00884** | **-0.668** |
| gap junction | 721 | +0.07108 | +1.473 |
| both layers | 205 | +0.11430 | +1.557 |

**Cell-class stratification, combined layers:** same-class **`d = +1.162`** (220 against 123);
cross-class **`d = -0.446`** (1,788 against 22,296). **Distance-adjusted, combined: `d = 0.360`.**

## 2. Compare with what the same data gave before the corrections

| analysis | chemical `d` | gap-junction `d` | cross-class | same-class |
| --- | --- | --- | --- | --- |
| 4 s window, no common-mode removal, no inclusion rule | **+1.656** | **+3.546** | **+2.171** | +0.233 |
| 16 s window, no removal, no rule | +3.118 | +7.629 | -- | -- |
| **4 s window, common-mode removed, rule applied** | **-0.668** | **+1.473** | **-0.446** | **+1.162** |

> **The chemical association changes sign; the gap association falls by a factor of 2.4; and the
> same-class and cross-class contrasts exchange places.** Three analysis choices, each defensible, each
> undocumented in the published per-pair matrix, move the answer from a strong positive in both layers to
> a negative chemical effect and a reversed class pattern.

## 3. The reason to distrust section 1's numbers, stated before they are used

**This audit does not know what the source's two thresholds are.** The paper says events *"did not meet
both thresholds for a contiguous 4 s"* were excluded and does not state them in the text this audit read.
**The rule implemented here is therefore this audit's invention**: the targeted cell's post-stimulus
deviation must exceed half its own peak at **every** one of the 8 post-stimulus volumes **and** have a mean
absolute deviation above 1. **That is a guess, and it is not the source's rule.**

**Worse, and more important: an inclusion rule of that kind conditions on a variable downstream of the
treatment.** Requiring the stimulated neuron to respond selects events **because of the outcome**. In a
system where the stimulated cell's response and the recorded cell's response share common causes --
network state, animal arousal, indicator level -- **conditioning on the former induces an association
between connectivity and the latter that is not causal**, the classic collider or selection pattern.
**That mechanism predicts exactly what was observed: the apparent connectivity association weakens,
reverses for chemical synapses, and the class stratification flips.**

**So the sign reversal in section 1 may be a property of this audit's guess rather than of the source's
rule.** Both readings are live and this audit cannot distinguish them:

* **Reading A:** the source's own filtering has this property, in which case the published per-pair values
  are conditioned on a post-treatment variable and the association they carry is not the naive one.
* **Reading B:** the source's rule is different and gentler, and the reversal here is this audit's
  artefact. **This reading is at least as likely and should be assumed until the thresholds are known.**

## 4. What is solid, and what is not

**Solid regardless of which reading holds:**

1. **The measured association is not stable.** Across three defensible choices it changes sign in the
   chemical layer and by a factor of 2.4 in the gap layer. **A reader of the published matrix cannot
   recover which choice produced the value they are reading.**
2. **The event-inclusion rule is outcome-dependent by construction**, in this audit and in any rule of
   the described form. **That is a property of the design, not of the data.**
3. **The reliability measurement from the first document is unaffected** -- it was computed with no
   window, no common-mode removal and no inclusion rule, and measures split-half reproducibility only.
4. **The 500 ms stimulus, the 4-second criterion and the 31-second spacing are facts from the source.**

**Not solid, and not to be used:**

* **Section 1's `d` values as an estimate of anything.** They are the output of one arbitrary
  implementation of an incompletely specified rule. **They are reported because the sensitivity they
  demonstrate is the finding; they are not reported as the effect.**
* **Any claim about which layer carries the association.** The ordering gap > chemical holds in
  section 1 but rests on the same uncertain rule.
* **Any claim that the source paper is wrong.** This audit has not reproduced the source's analysis and
  does not know its thresholds.

## 5. What would settle it

1. **Obtain the source's two thresholds.** They are in the analysis code, which is public:
   `github.com/leiferlab/pumpprobe`, specifically the autoresponse detection in `Fconn.py`, and the
   paper's Supplementary Information. **This is a bounded, concrete task and it is the blocking one.**
2. **Re-run with the actual rule** and report whether the reversal persists.
3. **If it persists, test the collider explanation directly** by re-running the contrast **without** any
   inclusion rule but restricting to the same events by an exogenous criterion (for example, the
   stimulus was delivered on-target), which breaks the conditioning on the outcome.

## 6. Why this is the project's question again, and this time sharply

**The governing question is which evidential transitions require separate empirical support. Here the
transition is from raw per-animal recordings to a per-pair value in a published atlas, and the step that
carries the most weight is an event-inclusion rule that is (a) documented only in prose, (b) stated
without its thresholds, and (c) outcome-dependent, which means it changes the estimand and not merely the
precision.**

**That is a stronger and more specific statement than the window sensitivity alone**, and it is the first
point in this line where the finding is about the *logic* of an analysis step rather than about a number.

## 7. Provenance

* Script `anatomy/07_final_estimate.py`; output `anatomy/RESULT_final_estimate.json`.
* Source protocol quotations from the Europe PMC full text of PMC10632145.
* **No model was fitted. No biological claim is made. Section 1's numbers are marked not-to-be-used as
  an estimate.**
---

> **SPECIFICATION MISMATCH NOTICE, appended 2026-10-09.** Every `d` value in this document was computed
> under a specification that differs from the source's in at least five respects -- window, amplitude
> reference, contiguous-run requirement, derivative criterion and tail handling. The source's actual rule
> is recovered in [`SOURCE_RULE_RECOVERED.md`](SOURCE_RULE_RECOVERED.md). **These numbers are therefore not
> estimates of the paper's quantity and must not be read as such.** The text is left unaltered so the
> mismatch remains auditable.
