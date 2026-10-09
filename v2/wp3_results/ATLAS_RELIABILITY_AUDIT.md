# Reliability audit of a published functional atlas, from the per-animal records it aggregated

**Status: RESULT OBTAINED, internals under test. This is a measurement on public data, not a model
result.** No predictive model was fitted. Every number was computed this session from files whose
checksums are recorded in `WIRESHIFT_STAGE2_WT_AUDIT.md`.

**Why this document exists.** The project's v1 manuscript asks, across seven synthetic cases, *which
evidential transitions require separate empirical support*. Its own closure document concedes that the
case-based contribution may amount to *"a descriptive checklist"*. **This is the first time that
question is put to real biological data at scale, with a number attached.**

---

## 1. The object under audit and the transition being tested

**Randi F, Sharma AK, Dvali S, Leifer AM (2023). _Neural signal propagation atlas of Caenorhabditis
elegans._ Nature, doi `10.1038/s41586-023-06683-4`.** The paper reports measuring signal propagation in
**23,433 pairs of neurons** by direct optogenetic activation with simultaneous whole-brain calcium
imaging, aggregated into a functional atlas, and concludes that propagation **differs from
anatomy-based model predictions**, with extrasynaptic signalling contributing.

**The evidential transition under test.** A published atlas presents a 300 x 300 matrix whose entries
are per-pair response magnitudes. **The inference from "a pair was measured" to "this entry describes
the nervous system" requires that the entry be reproducible across measurements.** That requirement is
**not** stated or quantified in the atlas. **This audit measures it** using the per-animal records the
aggregation discarded.

## 2. Method, stated so it can be attacked

**Data.** `exported_data.tar.gz`, 113 WT animals, 678 per-animal files, read directly.
**Unit of analysis:** the (stimulated cell, recorded cell) pair, keyed by **neuron name**, because names
are the only cross-animal correspondence available.

**Two pre-processing decisions, both forced by defects found in the data:**

1. **Only uniquely-named cells are used.** Labels contain duplicated names in 84 of 113 animals, up to
   75 instances, so a name-keyed pair would otherwise pool physically distinct cells. **After this
   filter, 112 of 113 animals are usable.**
2. **Responses are z-scored within each stimulus event before pooling.** Absolute dF levels differ by
   more than an order of magnitude across animals (baselines observed from 2.8 to 82.8), so unpooled
   values confound animal-level scale with pair-level signal.

**Response definition.** Post-window mean (8 volumes after the stimulus) minus pre-window mean
(8 volumes before), at `dt = 0.5 s`.

**Reliability estimator.** Split-half: each pair's measurements are randomly halved, the two half-means
correlated across pairs, and the result corrected to full length by Spearman-Brown
`r_full = 2r/(1+r)`. **`r_full` is the reported quantity.**

## 3. Result

**Without applying the source paper's inclusion rule:**

| minimum measurements per pair | pairs | `r` | **`r_full`** |
| --- | --- | --- | --- |
| >= 4 | 18,436 | 0.0636 | **0.120** |
| >= 10 | 7,723 | 0.1771 | **0.301** |
| >= 20 | 2,366 | 0.3832 | **0.554** |

**With the source paper's stated inclusion rule applied** -- *"a stimulus event is required to evoke a
response in the stimulated neuron"* -- operationalised two ways so the choice is visible:

| filter | events kept | `r_full` (>=4) | `r_full` (>=10) | `r_full` (>=20) |
| --- | --- | --- | --- | --- |
| none | 3,380 (100 %) | 0.120 | 0.301 | 0.554 |
| **A: target dF > 2 SD of its own pre-stimulus baseline** | 1,941 (57.4 %) | **0.226** | **0.502** | **0.819** |
| **B: target in the top decile of that event's cell responses** | 1,529 (45.2 %) | **0.332** | **0.649** | **0.846** |

**Variance decomposition after z-scoring: within-measurement 0.832, between-pair 0.192, so only
18.8 % of the variance distinguishes one pair from another.**

## 4. What the numbers do and do not support

**Supported, and this is the finding:**

> **Per-pair reliability in this atlas is strongly heterogeneous and depends on how many times a pair
> was measured. For the bulk of pairs -- 12,609 with 4 or more measurements under the paper's own
> inclusion rule -- full-length reliability is about 0.23. Only for the roughly 600 best-measured pairs
> does it reach 0.82. The atlas presents all entries with equal status; the evidence supports unequal
> confidence.**

**NOT supported, and must not be written:**

* **"The atlas is noise."** Under the paper's inclusion rule the well-measured pairs reach `r_full =
  0.82`, which is good reliability. **The finding is a gradient, not a failure.**
* **"Anatomical mismatch is an artefact."** **This audit did not test that and has no evidence about
  it.** That test is named as the next step in section 6, and until it is run the paper's central claim
  is **neither supported nor contradicted here.**
* **Any criticism of the authors' practice.** Aggregating heterogeneous measurements is standard, and
  the paper's inclusion rule demonstrably improves reliability, which this audit independently
  reproduces.
* **Any biological claim.** None is made.

## 5. Internal checks that were run, including one that failed

**This audit found and fixed three defects in its own analysis. All three are recorded because a silently
corrected check cannot be audited.**

1. **A duplicated-name pooling bug.** The first version keyed pairs by `(target name, recorded name)`
   while 84 of 113 animals carry duplicated names, so one key pooled several distinct physical cells.
   **Fixed by restricting to uniquely-named cells. The headline number moved from `r_full = -0.041` to
   `+0.017` at the unstandardised setting, showing the bug mattered.**
2. **A ratio-of-medians error.** An early variance decomposition reported a between-pair fraction of
   **0.977** by taking the median of per-pair ratios, while the pooled computation gave **0.099**. **The
   median of ratios is not the ratio of medians**; only the pooled form is reported.
3. **A confounded statistic in the stimulus-identity read-out check.** Comparing `max(post)` to
   `mean(pre)` reported 94 % of events rising, but **a random-column control rose 83 %**, exposing the
   statistic as positively biased. Replaced with a single statistic on both sides plus a per-event
   empirical null, which gives median percentile 84.4 % and 2.7-fold enrichment over the 95th
   percentile.

**A confound that changes the headline and was therefore controlled rather than ignored.** The source
paper filters stimulus events by whether the targeted cell responded. **Omitting that filter makes this
audit estimate a lower bound on the atlas's reliability, not the atlas's reliability.** Section 3
therefore reports both, and the filtered numbers are the ones that speak to the atlas.

## 6. The test that decides whether this matters, and which is NOT yet run

**A reliability gradient is only an NMI-level finding if it changes a conclusion someone drew from the
atlas.** The paper's central claim is that functional propagation **differs from anatomy-based
predictions**. The decisive next test is therefore:

> **Reproduce the anatomy-versus-function comparison using the anatomical matrices bundled in the same
> software distribution (`aconnectome_witvliet_2020_7.csv`, `aconnectome_witvliet_2020_8.csv`,
> `aconnectome_white_1986_whole.csv`, all present in the `wormneuroatlas` wheel already downloaded), then
> re-run it weighting each pair by its measured reliability. Does the reported mismatch survive?**

**Three outcomes are possible and all three are publishable:** the mismatch survives weighting (the
paper's claim is robust, and this audit bounds its reliability without disturbing it); the mismatch
weakens or vanishes (a substantive correction); or the weighting is not identifiable from the per-animal
records (a boundary on what the data can settle). **No outcome is assumed.**

## 7. Open items and what is NOT established

* **The anatomy-versus-function re-test above has not been run.** Until it is, this document reports a
  reliability measurement, not a correction to any published conclusion.
* **`-1`/`-2`/`-3` were excluded from response computation** but the **`-3` manually-flagged cases'**
  complementary labels were not used; whether they should be is open.
* **The `?`, `_` and `--` malformed labels were dropped**, so their cells are absent from every count
  here.
* **Only WT was analysed. `unc-31` (18 animals, 15 usable) was not**, so nothing here speaks to the
  genotype comparison.
* **No licence permitting redistribution of these derived files was found**, so the audit reports
  measurements and not redistributed data.
* **This is a measurement on one atlas.** Generalisation to other atlases is a claim this audit does not
  make.
