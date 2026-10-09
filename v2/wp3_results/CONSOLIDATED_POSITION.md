# What this analysis line has established, as of round 2

**Status: consolidated position. Four measurements on public data, three self-found defects corrected, one
retraction issued.** No model was fitted anywhere in this line. No biological claim is made.

**Purpose.** To state, in one place and without inflation, what can currently be defended, so that the
next round does not have to reconstruct it from five documents with one of them retracted.

---

## 1. The four measurements

**M1 -- reliability of an atlas entry is low for the bulk of pairs and high only for the best measured.**
Split-half, Spearman-Brown corrected, on the per-animal records behind a published functional atlas:

| under the source paper's own inclusion rule | pairs | `r_full` |
| --- | --- | --- |
| >= 4 measurements (the bulk) | 12,609 | **0.226** |
| >= 10 measurements | 3,456 | 0.502 |
| >= 20 measurements (about 600 pairs) | 638 | **0.819** |

**M2 -- the association between anatomical connectivity and functional response exists, and is stronger
for gap junctions than for chemical synapses at every window tested.** Ratios 1.19, 1.47, 2.14, 2.94,
2.45.

**M3 -- the size of that association is a function of the post-stimulus window.** `d` for chemical
synapses runs **1.154 (1 s) to 3.118 (16 s)**, a factor of **2.70**; for gap junctions **1.370 to 7.629**,
a factor of **5.57**. **No biological fact differs across those five analyses.**

**M4 -- the class control.** Within same-class pairs the association essentially vanishes
(`d = 0.233` for gap junctions) and it lives in cross-class pairs (`d = 2.171`). **Run at one window
only.**

## 2. The claim this supports, and the claim it does not

**Supported, at the strength the evidence carries:**

> **For this atlas, both the reliability of an entry and the size of the association computed from it are
> functions of analysis choices that are not reported as result-bearing. The reliability is
> heterogeneous by a factor that matters (`r_full` 0.23 against 0.82); the association moves by a factor
> of 2.7 to 5.6 on the post-stimulus window alone; and the association is confined to cross-class pairs.
> A reader of the atlas has no way to know any of the three.**

**This is a direct and measured instance of the project's governing question** -- *which evidential
transitions require separate empirical support* -- and it is the first time that question has been put to
real biological data with numbers attached, rather than to synthetic cases.

**Not supported, and written into every document in this line:**

* that the source paper is wrong. Its claims concern **sign, strength, temporal properties and causal
  direction**; this line measures one coarse averaged scalar. **A window dependence in a coarse read-out
  is compatible with a careful multi-property analysis**, and the paper's own reported difficulty
  relating synapse counts to function is consistent with everything measured here.
* that chemical synapses are unimportant. **This claim was made and is retracted** (see
  `RETRACTION_window_dependence.md`); at a 16-second window chemical synapses reach `d = 3.118`.
* that gap junctions carry the effect biologically. The class control leaves them as **cross-class**
  associations only, and C2 selection contamination is strongest in that stratum.
* **what the correct window is.** The sensitivity is demonstrated; **the resolution is not**, and it
  cannot come from the data. It has to come from calcium indicator kinetics and known synaptic delays.

## 3. The defect ledger for this line

**Five defects were found in this project's own analysis, and all five are retained in the record.**

| # | defect | how it showed up | effect on numbers |
| --- | --- | --- | --- |
| 1 | pairs keyed by neuron name pooled physically distinct cells (84 of 113 animals have duplicate names, up to 75) | noticed while checking why reliability looked absurd | unstandardised `r_full` moved from **-0.041 to +0.017** |
| 2 | variance reported as the median of per-pair ratios | pooled computation disagreed 0.977 against 0.099 | discarded the 0.977 form |
| 3 | read-out statistic compared a maximum against a mean | random-column control rose 83 % against the claimed 94 % | replaced with a fair statistic and a per-event null |
| 4 | assumed `aconnectome_default.h5` shares the functional atlas's id order | 1,756 of 1,891 chemical edges mismatched | the invalid run's `d = 4.74` **discarded**; matrices rebuilt by name |
| 5 | **effect size reported from a single post-stimulus window** | **the timescale test** | **headline retracted; `d` for chemical moves 2.70-fold** |

**Two parsing traps are also recorded**, each of which silently produces a wrong answer:
`aconnectome_*.csv` is **tab**-separated, and `anatlas_neuron_positions.txt` stores 303 names
**space**-separated on a `#`-prefixed first line, so a delimited-header reader finds zero names.

## 4. What is still owed before this is a manuscript

1. **A defensible window**, argued from indicator kinetics and synaptic delays, with every contrast
   re-run at it. **Without this the central measurement is a sensitivity study and not an estimate.**
2. **The class control across all windows**, since it currently rests on one.
3. **A reliability proxy that is not the measurement count**, because C2 shows the count is not
   exogenous and the contamination is largest exactly where the effect is largest.
4. **The `unc-31` arm**, untouched so far: 18 animals, 15 usable, which is the only genotype contrast
   the data can support and is severely unbalanced against 112 WT.
5. **A licence determination.** No licence permitting redistribution of the derived records was found;
   **analysis use is unaffected and redistribution is currently not authorised.** This blocks any
   supplementary data deposit.

## 5. Standing assessment

**The line now has a real, measured, falsifiable finding that is not any of the seven negative cases in
the v1 manuscript.** It is methodological rather than biological: it quantifies what an atlas's entries
can support, and shows that the answer depends on choices the atlas does not report.

**It is not yet an NMI paper.** Four things are missing, in order of weight: **the window is unresolved
(item 1)**, the class control is single-window, the reliability proxy is not exogenous, and nothing here
has been through an independent review. **The previous round's verdict that the v1 case synthesis is not
NMI-ready stands unchanged.**
---

> **SPECIFICATION MISMATCH NOTICE, appended 2026-10-09.** Every `d` value in this document was computed
> under a specification that differs from the source's in at least five respects -- window, amplitude
> reference, contiguous-run requirement, derivative criterion and tail handling. The source's actual rule
> is recovered in [`SOURCE_RULE_RECOVERED.md`](SOURCE_RULE_RECOVERED.md). **These numbers are therefore not
> estimates of the paper's quantity and must not be read as such.** The text is left unaltered so the
> mismatch remains auditable.
