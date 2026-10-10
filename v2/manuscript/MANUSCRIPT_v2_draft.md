# Unstated specifications in a derived neuroscience dataset: seven dimensions worth more than the effect they qualify

**Draft, v2 line. Every number below is committed under `v2/wp3_results/` with its own provenance section.
No number is introduced here that is not already there.**

---

## Abstract

**Derived datasets are increasingly used as ground truth and as inputs to learned models, and their provenance
is usually reported in terms of files, checksums and licences.** **We show that for one such dataset — a
whole-brain functional atlas of *Caenorhabditis elegans* — the analysis choices that produced the published
per-pair values are not recoverable from the artifact at all, and that the dimensions they span move the
headline estimate by more than the range the original work reports.**

**We measure seven specification dimensions, each by varying it alone and holding the others fixed. The
largest is not a parameter but an ORDER: two defensible normalisations of the same response, applied in the
two possible sequences, give animal-level estimates of `d = +0.97` and `d = +0.12` at the same post-stimulus
window, and one sequence is stable across windows to within 0.006 while the other spans 1.064 and changes sign.
Four further dimensions — per-cell normalisation (0.34), per-event precision weighting (0.34), post-stimulus
window (0.24) and baseline convention (0.03 to 0.05) — are each measured, and the dimensions are strongly
non-additive: two of them whose isolated contributions sum to `-0.008` combine to `+0.571`.**

**The artifact reports no reliability for the quantity it publishes. Decomposing the per-animal records behind
it, within-cell measurement error accounts for 37 to 57 per cent of the variance in a pair's response
depending on the specification, and is never the smallest component, while the pair-specific animal component
is negative at the unrestricted specification — an impossible value for a variance share, which bounds which
specifications are well posed.**

**Finally, and as a demonstration rather than a claim: we attempted to re-derive the artifact's own numbers,
and the attempt failed for six consecutive rounds because our re-implementations differed from the original
code in ways not visible on reading it. The published pipeline's own authors are its most informed possible
re-implementers, and the specification still had to be recovered line by line. We report the full defect
ledger, seventeen numbered self-found errors, because it is the evidence for the claim rather than an appendix to
it.**

**Nothing here is a claim about the biology. The atlas's conclusions may well be correct; we show only that
they are not reconstructible from the artifact, and we quantify what that costs.**

---

## 1. Introduction

**A derived dataset is a scientific object with two parts: the measurements it contains and the analysis that
turned raw recordings into them.** **Conventions for the first part are mature — files, checksums, licences,
accessions — and conventions for the second are not.** **A user who downloads a matrix of per-pair values
receives the numbers and, typically, no record of the windows, normalisations, weightings, filters and orders
that produced them.**

**This matters more as such datasets become inputs to learned models, because a model fitted to a derived
matrix inherits its specification silently.** **It also matters for interpretation: a value that is a mean over
a heterogeneous quantity supports a different claim from a value that is a property of a circuit.**

**The question is not hypothetical in this literature.** **A 2025 review in *Nature Reviews Neuroscience*
states that "it remains unclear whether, at the macroscale, structural (or anatomical) connectivity provides
useful constraints on models of directed connectivity".** **A 2025 *Cell* paper compares connectomic
predictions against physiology and finds them accurate for some response properties and "surprisingly poor"
for others.** **A 2025 *Scientific Reports* paper states that "no universally accepted method exists" for
inferring effective connectivity.** **And a 2026 *Nature Physics* paper reports that simple input-output
dependencies explain most of the variability in neuronal activity.**

**So the field acknowledges that the inference is unsettled.** **What it does not do, as far as we can
establish from eleven works read at title-and-abstract level and four read in full, is report how reliable the
functional quantity being predicted is.** **None of those fifteen reports a reliability, reproducibility or
measurement-error figure for it.**

**We examine one such artifact in detail: a whole-brain functional atlas of the nematode
*Caenorhabditis elegans*, together with the pipeline that produced it.** **We ask a narrow question — what
would a user have to know to reproduce these numbers, and is it in the file — and we find the answer is that
they would have to read the code, that the dimensions involved are larger than the effect, and that this is
demonstrable because we ourselves failed to reconstruct it for six consecutive rounds.**

---

## 2. Results

### 2.1 The specification is in the pipeline's code and not in its data file

**We enumerated every analysis choice in the pipeline that produced the atlas's per-pair values and measured
each one's contribution by varying it alone and holding the others fixed, at the animal unit.** **Seven
dimensions move the animal-level standardised effect `d_A`:**

| dimension | levels | isolated size in `d_A` | declared in the artifact? |
| --- | --- | --- | --- |
| **order of application** | two sequences of two normalisations | **0.02 to 0.85, depending on window** | **no** |
| per-cell normalisation | none, or by the cell's pre-stimulus SD | **0.3395** | no |
| per-event precision weighting | none, or by the inverse of the event's across-cell spread | **0.3356** | no |
| post-stimulus window | 12, 24 or 48 volumes | **0.2364** | no |
| baseline convention | volumes 30–60, or 0–60 before the stimulus | 0.0295 to 0.0496 | **yes, in the source** |
| common-mode removal | none, scalar, or per volume | 0.0103 to 0.0285 | no |
| the cell pool the common mode spans | all columns, or the uniquely-named ones | 0.0038 | no |

**The one dimension the source states — its baseline convention — is the smallest of the seven by an order of
magnitude.** **The three largest are stated nowhere.**

**We also tested an eighth candidate, an inclusion rule requiring at least ten connected and fifty unconnected
pairs per animal, and found it changes `d_A` by 0.0000, because no animal in this dataset fails the
thresholds.** **We report it because a table that lists a dimension which does nothing overstates the number of
choices, and we made that error ourselves before checking.**

### 2.2 The dimensions do not add

**A reader who treated the table in 2.1 as a budget would be wrong.** **At a 24-volume window, per-cell
normalisation contributes `-0.3462` and the precision weighting `+0.3378`, summing to `-0.0084`; applied
together they give `+0.5706`.** **The interaction, `+0.5789`, is larger than either isolated effect.**

**The reason is that both are normalisations and each rescales the quantity the other operates on, which is
why the ORDER is itself a dimension.**

### 2.3 The largest dimension is the order

**Two sequences of the same two normalisations — per-cell first, or precision weighting first — differ only in
which array the weighting's denominator is computed from, and they coincide only if every cell's scale is
equal.**

| window | per-cell then weighting | weighting then per-cell | **the order's contribution** |
| --- | --- | --- | --- |
| 12 volumes | +0.0958 | +0.1192 | +0.0234 |
| **24 volumes** | **+0.9685** | **+0.1192** | **-0.8493** |
| 48 volumes | **-0.0958** | +0.1133 | +0.2091 |

**At a 24-volume window the two orders differ by 0.85 — larger than any dimension in 2.1 and larger than the
entire span the original work reports.** **Their stability differs as much as their values: the
weighting-first order gives 0.1192, 0.1192 and 0.1133 across the three windows, a spread of 0.006, while the
per-cell-first order gives 0.0958, 0.9685 and -0.0958, a spread of 1.064 and a change of sign.**

**One caveat must travel with this.** **The per-cell-first order is a constructed specification: the pipeline
does the weighting without any per-cell normalisation, so that arm is not a description of the artifact.**
**What makes the comparison meaningful is that a user who chooses to add per-cell normalisation must then
decide where to put it, and the two placements are not equivalent. The difference is 0.85.**

### 2.4 The artifact reports no reliability, and measurement error is a large share of what it publishes

**We decomposed the per-animal records behind the atlas into four components: a between-pair component, a
per-animal offset, a pair-specific animal component, and within-cell measurement error, the last identified
from the (animal, pair) cells holding repeat measurements.**

**The measurement-error share is 17 to 57 per cent depending on the specification, and it is never the smallest
component.** **Its value depends on the precision weighting (13.0 points), the read-out (about 13 points), the
window and the normalisations.**

**The pair-specific animal component is not robust in the same way: it ranges from 5.5 to 46.0 per cent
depending on a minimum-measurements-per-pair restriction, and at the unrestricted specification it goes
NEGATIVE — an impossible value for a variance share.** **That negativity is informative rather than merely
inconvenient: it marks the specification as ill posed, because a pair mean computed from a single animal
inflates the between-pair term and drives the subtracted component below zero.**

**What is robust across every specification we computed is the sign structure: measurement error is always the
largest or second-largest component, and the pair-specific animal component is positive whenever pairs
measured in a single animal are excluded.**

### 2.5 The unit error is arithmetic, and we initially mis-measured it

**A contrast computed with pair-measurements as the unit rather than animals has a standard error computed
over 19,247 connected and 195,809 unconnected measurements rather than over 109 animals.** **This is
pseudo-replication and it is worth stating precisely.**

**We initially reported that this inflates the standardised effect by 11 to 18 times, and that is wrong.** **The
pair-level quantity in the pipeline is `diff / SE`, a z-score, while the animal-level quantity is
`diff / SD`, a Cohen's `d`; their ratio is `SD / SE = sqrt(n)` and is a definitional identity rather than a
measurement.** **Measured properly, the pair-level effect size is SMALLER than the animal-level one: 0.022
against 0.421.**

**The correct statement is therefore about significance and not about effect size: the reported `p`-value
corresponds to a sample roughly 464 times larger than the number of independent units.** **The
pseudo-replication point itself stands, and it is the reason an animal-level analysis exists in this line at
all.**

**We report the error rather than the correction alone because it is a second instance of the paper's subject:
a quantity named `d` meant two different things, and the ambiguity survived four rounds of internal review.**

### 2.6 A like-for-like comparison against the source's own reported quantity

**The original work states that "a matrix of bare anatomical weights (synapse counts) was a poor predictor of
the correlations of spontaneous activity".** **Its spontaneous-activity data, in the same repository, contains
two animals.**

**We reproduce the comparison: `r = +0.0368` and `-0.0064` over 3,540 and 1,560 pairs respectively, near zero
in both as the source reports.** **And we bound it: restricted to the 23 cell names the two animals share, their
activity-correlation matrices agree at only `r = +0.2084`.**

**So the published comparison measures anatomy against a target whose own cross-animal reliability is about
0.21.** **Under classical test theory the observed association is attenuated by roughly `sqrt(0.208) = 0.456`,
implying a true association near 0.081 — still small, and the point is not the corrected magnitude but that the
comparison, as published, measures anatomy against a quantity that differs between animals and is reported
from two of them.**

**Both quantities are stable across the distinct specifications we could vary (Pearson or Spearman
correlation, with or without detrending): the reproduction stays between +0.036 and +0.038 in the first animal,
and the bound stays between +0.208 and +0.270, always far below the 0.5 that would indicate a reproducible
functional quantity.** **We note that our grid's third axis, three data transforms, changes nothing at all,
because correlations are invariant to per-column affine transforms — a redundant axis we had to check for
rather than assume.**

### 2.7 The demonstration: six consecutive failures to re-derive the artifact's own numbers

**The claim of this paper is that a pipeline's specification is not recoverable from its output.** **The
strongest evidence we can offer is that we tried to recover it, and failed repeatedly.**

**Every value in section 2.1 was produced by re-implementing the pipeline.** **Six consecutive
re-implementations were wrong, each in a different way, and none of the errors was visible on reading the
code:**

| round | the error | how it surfaced |
| --- | --- | --- |
| 29 | our window convention differed from the code's | the value moved by 18 points |
| 31 | our grid's family excluded the code's common mode | ceiling 0.44 against the code's 0.73 |
| 32 | our common-mode axis tested a scalar where the code removes a per-volume mean | the contribution had the wrong sign |
| 33 | our cache held only uniquely-named columns where the code spans all | 0.0038 against an attributed 0.34 |
| 34 | our grid omitted the per-event weighting entirely | 0.3933 against 0.7289 |
| 39 | our weighting divided by an array reduced over volumes where the code reduces over cells | the contribution changed sign again |

**The resolution, in round 40, was to stop hypothesising and instead verify each re-implemented step against
the code's own intermediate values for a single animal.** **Every intermediate then matched bit for bit — `sd`
exact, and `dv`, `dvs`, `cm` and `dev` with a maximum absolute difference of `0.000e+00` — and with the
verified sequence the pipeline's own configuration reproduced at `d = 0.7289` and `t = 7.610` against the
code's `0.7289` and `7.610`.**

**We also failed to explain the discrepancy four times before doing that, each time by proposing a cause and
testing it, and each proposed cause was refuted.** **We report that sequence in the defect ledger, because
four refuted hypotheses followed by one measurement is a description of the specification problem from the
inside.**

---

## 3. Discussion

**The atlas's scientific conclusions may be correct.** **Nothing in this paper bears on whether connectomic
structure predicts function in *C. elegans*; we measured an artifact, not the animal.** **What we show is that
the artifact does not carry the information a user would need to reconstruct the values it publishes, and we
quantify the cost.**

**Three things follow, and they differ in how far they travel.**

**The first is specific and arithmetic.** **When a derived matrix is passed to a model or an analyst, the unit
of analysis and the reliability of the values are not cosmetic; here they change the answer by more than the
reported effect, and one specification makes the association's sign inconsistent across a grid of three
defensible dimensions.**

**The second concerns reporting practice.** **Fifteen works in this literature, read at abstract or full-text
level, none report a reliability figure for the functional quantity they predict.** **Our decomposition finds
measurement error accounting for 37 to 57 per cent of the variance in a pair's response in this artifact, and
the artifact reports no such figure.** **We cannot say whether that is typical — fifteen works and one artifact
do not establish a norm — but we can say that in the one case where it has been measured, the number is
large.** **And we note one adjacent framing in tension with it: a 2025 *Communications Biology* paper on the
same organism states that cross-individual variability "is not noise" but rather "reflects worm
individuality".** **That is a different quantity from ours, measured on different data, and we have not
compared them; we record the tension and not a resolution.**

**The third concerns derived datasets as inputs to learned models.** **If a pipeline's specification is not in
its output, then a model trained on that output has inherited a specification it cannot state, and a
re-analysis cannot determine what the model was fitted to.** **The remedy is cheap and we do not know why it is
not universal: publish the specification alongside the matrix — the windows, the normalisations, their order,
the weightings, the filters, and a reliability figure for the published quantity.** **The seven dimensions in
section 2.1 would fit in a table smaller than the provenance section of most data-availability statements.**

**Limitations, stated plainly.** **The generalisation test we designed for a second dataset, from the same
laboratory with a different preparation, could not be run: the download failed three times, the third time
because of a concurrency error of our own, costing 1.866 GB with no usable files.** **So every result here
rests on one atlas, and we do not know how far any of it travels.** **The measurement-error share is a range
over the specifications we varied and not a property of the preparation.** **The pair-specific component is
ill posed at the unrestricted specification and we have not resolved the estimator.** **And we have had no
independent review: the review recorded in `PREFLIGHT_REVIEW.md` is this line's own.**

---

## 4. Methods

**Data.** The wild-type atlas export and its `unc-31` counterpart (OSF `10.17605/OSF.IO/E2SYT`;
`exported_data.tar.gz` 523,093,816 B, sha256 `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9b3832f6ce836`;
113 and 18 animals). Connectome tables built by name from `aconnectome_witvliet_2020_8.csv` and
`aconnectome_white_1986_whole.csv`. Cell-class labels from `neurons.json`, whose provenance and licence status
are recorded in `../wp1_data/PATH_LAYOUT.md`. Cumulative download across the line, including failed
attempts, 2.541 GB against a 10 GB cap.

**Effect size.** `d_A = mean(across-animal differences) / SD(across-animal differences)`, computed at the
animal unit with each animal's connected-minus-unconnected contrast. **Where a z-score (`diff / SE`) appears in
an intermediate artifact it is labelled as such; `NOTATION_two_effect_sizes.md` records that `d` means four
different things across this line's artifacts, and the census in `CENSUS_d_z_versus_d_effect.md` located
seventy-six fields in five files where it is a z-score.**

**Specification grids.** Each dimension was varied alone with the others fixed, and then jointly. **Every axis
was checked for redundancy before its results were read: an axis whose levels give bit-identical output is not
a specification. Two such axes were found, and one of them had been added by the authors of this paper.**

**Step verification.** A re-implemented step was accepted only after comparison against the original's
intermediate values for a single animal — `sd`, `dv`, `dvs`, `cm`, `dev` and the per-cell value — with
agreement required at machine precision.

**Variance decomposition.** `y = mu + alpha[animal] + beta[animal, pair] + eps`, in log space, with `eps`
identified from the (animal, pair) cells holding two or more measurements and the remaining components
obtained by subtraction. **The decomposition is reported as a function of the minimum-measurements-per-pair
restriction, because at the unrestricted specification the subtracted component can be negative.**

**Software.** Python 3.12 with numpy and h5py. **All scripts, result JSONs and the figure source data are
committed; `FIGURE_SOURCE_DATA.json` records a sha256 prefix for each of its twenty-two source artifacts.**
**Seventeen numbered self-found defects and the invalid runs that produced some of them are retained rather
than deleted, under `v2/wp3_results/`.**

---

## 5. Figure legends

**All six are rendered by `../figures/make_figures.py`, which reads each series from the committed
result artifact named below and retypes nothing.**

**Figure 1 — the specification ledger.** Seven dimensions, each with its isolated contribution, marked by
whether the artifact declares it. Source: `SPECIFICATION_LEDGER.md`, `FIGURE_SOURCE_DATA.json`. Rendered file: `../figures/Fig1_specification_ledger.png`.

**Figure 2 — non-additivity.** Isolated contributions against the joint effect for the two largest dimensions,
at three windows. Source: `RESULT_joint_grid_verified.json`. Rendered file: `../figures/Fig2_nonadditivity.png`.

**Figure 3 — the order is the largest dimension.** The two sequences across three windows, with the stability
of each marked. Source: `RESULT_order_axis.json`. Rendered file: `../figures/Fig3_order.png`.

**Figure 4 — the decomposition.** Four components as a function of the minimum-measurements-per-pair
restriction, with the negative region marked as ill posed. Source:
`RESULT_variance_decomposition_sweep.json`, `RESULT_decomposition_weighted.json`. Rendered file: `../figures/Fig4_decomposition.png`.

**Figure 5 — the like-for-like comparison and its bound.** The reproduction in two animals and the target's
cross-animal agreement. Source: `RESULT_fig6.json`, `RESULT_fig6_specification_grid.json`. Rendered file: `../figures/Fig5_like_for_like.png`.

**Figure 6 — the defect ledger.** Seventeen numbered self-found defects against the discovery order each document states for itself
in a measurement, an interpretation, or a re-implementation. Source: `CORPUS_INDEX.md`. Rendered file: `../figures/Fig6_defect_ledger.png`.
