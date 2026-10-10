# Unstated specifications in a derived neuroscience dataset: seven dimensions worth more than the effect they qualify

**Draft, v2 line. Every number below is committed under `v2/wp3_results/` with its own provenance section.
No number is introduced here that is not already there.**

---

## Abstract

**Derived datasets are increasingly used as ground truth and as inputs to learned models, and their provenance
is usually reported in terms of files, checksums and licences.** **We show that for one such dataset — a
whole-brain functional atlas of *Caenorhabditis elegans* — the analysis choices that produced the published
per-pair values are not recoverable from the artifact at all, and that the dimensions they span move the
headline estimate by more than this audit's own widest range across specifications, 0.6437 — a range that
mixes a weighted pipeline against three unweighted ones and is therefore this audit's construction rather than
a quantity the source reports.**

**We measure seven specification dimensions against a declared baseline configuration, six by varying one axis
and holding the others fixed. The largest at one window is not a parameter but an ORDER, and the finding is
window-dependent: two normalisations of the same response, applied in the two possible sequences, give
animal-level estimates of `d = +0.97` and `d = +0.12` at a 24-volume window, where they differ by 0.85, while
at a 12-volume window the same comparison contributes 0.0234 and is the smallest of the seven. One of the two
arms is a constructed specification rather than a description of the artifact, because the pipeline applies the
weighting without any per-cell normalisation, so the order is a choice a user faces only after deciding to add
one. One sequence's three-window spread is 0.006 and the other's is 1.064, but that contrast rests on three
nested windows and on a sign-changing cell the source flags as not to be treated as a finding.**

**Four further dimensions — per-cell normalisation (0.34), per-event precision weighting (0.34), post-stimulus
window (0.24) and baseline convention (0.03 to 0.05) — are each measured, and the dimensions are strongly
non-additive: two of them whose isolated contributions sum to `-0.008` combine to `+0.571`.**

**The artifact reports no reliability for the quantity it publishes. Decomposing the per-animal records behind
it, within-cell measurement error accounts for 17 to 57 per cent of the variance in a pair's response
depending on the specification, and is never the smallest component, while the pair-specific animal component
is negative at ONE unrestricted specification, which is impossible for a SHARE of a common total and is
therefore a property of the estimator rather than of the animal: the four components are obtained by
subtraction with no non-negativity constraint, so when one is negative the others are not shares of one
variance. **The negativity is also READ-OUT CONDITIONAL: at the same unrestricted minimum it occurs under
the signed-sum read-out, where `beta` is -10.9, -8.1, -8.1 and -7.5 per cent across four specifications,
and does NOT occur under the mean-over-the-window read-out, where the same restriction gives +1.9, +6.1,
+6.1 and +6.7 per cent.** **So the unrestricted specification is ill posed under one of the two read-outs
this line treats as defensible and well posed under the other, and any exclusion of it is partly a choice
of read-out rather than a property of the data.**.**

**Finally, and as a demonstration rather than a claim: we attempted to re-derive the artifact's own numbers,
and the attempt failed for six consecutive rounds because our re-implementations differed from the original
code in ways not visible on reading it. The published pipeline's own authors are its most informed possible
re-implementers, and the specification still had to be recovered line by line. We report the full defect
ledger -- seventeen numbered self-found errors, each named by the correction document that records it, plus
earlier ones referenced in prose and not separately documented -- because it is the evidence for the claim
rather than an appendix to it.**

**We also report our own corrections, because they are the same phenomenon: four interpretations this line
published earlier are withdrawn or narrowed, including a claim that the unit error inflated the effect by
11 to 18 times (it did not; the ratio was a z-score over a Cohen's `d`), and every one is retained in the
record rather than deleted.** **Across the work, the pattern is asymmetric in a specific way. The line made at least five
MEASUREMENT-level errors, and all five were caught by instrument checks before their numbers were used: a
connectome indexed by the wrong neuron order gave an implausible `d = 4.74`; a per-cell normalisation
divided by a baseline SD over 8 volumes and blew up to about `1e11`; a collapse of per-cell quantities to
scalars let 0 of 3,333 events pass; a zero-inflated within-variance raised an intraclass correlation to
0.93; and inverse-variance weights spanned thirty-one orders of magnitude. All five are retained as
`INVALID` artifacts. Every measurement that SURVIVED those checks then withstood re-examination, while
every INTERPRETATION attached to one was revised at least once.**

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
establish, is state how reliable the functional quantity being predicted is.** **Of eleven works read at
title-and-abstract level, none states a reliability, reproducibility or measurement-error figure for it in
its TITLE OR ABSTRACT; of four read in full, none reports one in its text.** **That is a statement about what
these fifteen documents say where we read them, and not a claim about the literature: a figure reported only
in a Methods section would not be seen by an abstract-level reading, and our own survey document states that
as the first thing this design cannot establish.**

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
why the ORDER is itself a dimension.** **PROVENANCE CAVEAT: this joint grid's own correctness cell returns
`d = 0.7331` against the code's `0.7289`, a difference of `0.0042` whose proposed explanation was refuted
and which was never identified; the exact-match verification belongs to the ORDER grid. The non-additivity
figure is therefore reported as provisional. See section 2.7.**

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
this line's own widest reported range across specifications, 0.6437.** **PROVENANCE CAVEAT: that reference
range is NOT a quantity the source paper reports.** **It is this audit's own span from 0.0852 to 0.7289, and
`SPECIFICATION_LEDGER.md` records that it "mixes a weighted pipeline against three unweighted ones", so its
widest extent comes from mixing two families rather than from varying the choices it lists.** **An earlier
draft of this manuscript called it "the entire span the original work reports", which was an attribution
error: the span belongs to this audit and not to the source.** **Their stability differs as much as their values: the
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
component.** **That range is the union of two grids: an eight-specification grid over the read-out and the
post-stimulus window gave 38.7 to 57.1 per cent, and adding the per-event weighting widened the lower bound to
17 per cent.** **An earlier draft of this manuscript quoted 37 to 57 per cent in its abstract and discussion,
which matched neither grid; the correct figures are 38.7 and 17, and both are stated here so the arithmetic is
checkable.** **Its value depends on the precision weighting (13.0 points), the read-out (about 13 points), the
window and the normalisations.**

**The pair-specific animal component is not robust in the same way: it ranges from 5.5 to 46.0 per cent
depending on a minimum-measurements-per-pair restriction, and at the unrestricted specification it goes
NEGATIVE under one of the two read-outs, which is impossible for a share of a common total.** **The four components are obtained by
subtraction with no non-negativity constraint, so a negative term means the printed percentages are component
contributions and not shares of one variance; at the sharpest specification the positive terms alone reach 111.0
per cent.** **That negativity is informative rather than merely
inconvenient: it marks the specification as ill posed, because a pair mean computed from a single animal
inflates the between-pair term and drives the subtracted component below zero.**

**The condition is not incidental, and the committed grid shows it.** `CORRECTION_eps_is_a_range.md` carries sixteen specifications and the `beta` sign depends on the read-out at the unrestricted minimum:

| read-out | `min_an` | `beta` across four specifications | sign |
| --- | --- | --- | --- |
| signed sum over the window | 1 | -10.9, -8.1, -8.1, -7.5 per cent | **all negative** |
| mean over the window | 1 | +1.9, +6.1, +6.1, +6.7 per cent | all positive |
| signed sum over the window | 3 | +21.6, +24.4, +24.4, +25.4 per cent | all positive |
| mean over the window | 3 | +32.2, +34.7, +34.7, +35.5 per cent | all positive |

**So the ill-posedness is a property of the PAIR of an unrestricted minimum and the signed-sum read-out, and not of the unrestricted minimum alone.** **An earlier version of this manuscript described it as a property of the unrestricted specification, which is what an isolated reviewer correctly challenged.**

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
the code's own intermediate values for a single animal.** **For the order grid, every intermediate then matched
bit for bit — `sd` exact, and `dv`, `dvs`, `cm` and `dev` with a maximum absolute difference of `0.000e+00` —
and with that verified sequence the pipeline's own configuration reproduced at `d = 0.7289` and `t = 7.610`
against the code's `0.7289` and `7.610`.**

**That verification belongs to the ORDER grid and NOT to the joint grid that produces the non-additivity
result in section 2.2, and the distinction must be stated because the two grids did not both pass.**
**The joint grid's own correctness cell returns `d = 0.7331` and `t = 7.654` against the code's `0.7289`
and `7.610`, a difference of `0.0042`, and the explanation first offered for it — a slightly different
event set — was refuted: the exact match is available, and the `0.0042` is an implementation difference
that was never identified.** **So the non-additivity result in section 2.2 rests on a grid whose own check
does not pass, and `JOINT_GRID_VERIFIED_NONADDITIVE.md` states both that its check passes and that it
differs by `0.0042`, which is a contradiction in that document and not a qualification of the result.**
**We report the non-additivity as provisional on the strength of the ORDER grid, where the same pair of
normalisations was measured with a check that passes, rather than on the joint grid whose check failed.**

**We also failed to explain the discrepancy four times before doing that, each time by proposing a cause and
testing it, and each proposed cause was refuted.** **We report that sequence in the defect ledger, because
four refuted hypotheses followed by one measurement is a description of the specification problem from the
inside.**

### 2.8 Corrections and withdrawals, which the reader needs in one place

**A paper whose subject is provenance must show its own.** **Four interpretations this line published in
earlier rounds are withdrawn or narrowed, and three of them are not visible anywhere else in this draft.**

| was published | status | why |
| --- | --- | --- |
| **"treating pair measurements as replicates inflates the standardised effect by 11 to 18 times"** | **retracted, and inverted** | the pair-level quantity is `diff / SE`, a z-score, while the animal-level one is `diff / SD`; their ratio is `sqrt(n)`, a definitional identity. **The pair-level effect size is smaller, 0.022 against 0.421.** (section 2.5) |
| **"the measurements are not noisy, the animals differ"** | **retracted** | a three-level decomposition gives **5.5 per cent** pair-specific animal deviation against **37.5 per cent** within-cell measurement error, so the cross-animal disagreement is better explained by unreliable pair means than by heterogeneous biology. |
| **"the association is a property of the population, not of the circuit"** | **narrowed** | the between-animal spread is 42.2 per cent measurement noise and 17.7 per cent pair composition, with about 40 per cent unexplained by anything measured; **nine technical covariates account for 0.25 per cent of it, adjusted.** |
| **"what is reproducible within an animal is which pairs it happened to have measured"** | **narrowed** | measured, that component is **17.7 per cent** of the between-animal variance, not the whole of it. |
| **an intraclass correlation of 0.93** | **withdrawn before use** | the within-animal variance was computed as `var(vs) if len(vs) > 1 else 0`, and most (animal, pair) cells hold one measurement, so the value was inflated by construction. **The tell was that per-animal centring left it identical to four decimals, which centring must change.** |

**Every one of these is retained in the line's own record rather than deleted: the correction documents are
committed, the invalid scripts and result files carry `INVALID` markers, and four documents carry a dated
banner at the top naming the reading that was superseded.** **The count of such events is seventeen numbered
defects, listed in section 2.7 and in Figure 6.**

**And we state the pattern plainly, because it bears on how the rest of this draft should be read, and
because an earlier version of this sentence overclaimed it.** **The line made at least five measurement-level
errors, listed in section 2.7 and retained as `INVALID` artifacts, and every one of them was caught by an
instrument check BEFORE its number was used -- the wrong-neuron-order connectome, the exploding per-cell
normalisation, the scalar collapse that passed 0 of 3,333 events, the zero-inflated intraclass correlation,
and the weights spanning thirty-one orders of magnitude.** **Every measurement that survived those checks
then withstood re-examination, and every interpretation attached to a surviving measurement was revised at
least once.** **The asymmetry is therefore about WHERE the errors were caught, not about whether they
occurred: measurement errors were caught by the instrument, and interpretation errors were caught only by
later measurement.** **The failure mode was never the computation; it was the step from a number to a
sentence about the number.**

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
measurement error accounting for 17 to 57 per cent of the variance in a pair's response in this artifact, and
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
`aconnectome_white_1986_whole.csv`. Cell-class labels from NemaNode's `neurons.json`, which is an EXTERNAL dependency rather than a file in
this repository; its size, sha256 prefix, provenance and licence status are recorded in
`../wp1_data/PATH_LAYOUT.md`. Cumulative download across the line, including failed
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

**Variance decomposition, and what it can and cannot be read as.** `y = mu + alpha[animal] + beta[animal, pair] + eps`, in log space, with `eps` identified from the (animal, pair) cells holding two or more measurements and the remaining three components obtained BY SUBTRACTION with no non-negativity constraint, so `beta` can be negative. **This matters for how the output may be described.** **When every component is non-negative the four numbers are shares of a common total and sum to 100 per cent.** **When `beta` is negative they do NOT: the four values still add to about 100 per cent, but the positive components alone exceed 100, at one specification reaching 111.0 per cent because `beta` is -10.9 per cent.** **A negative component therefore means the four numbers are a component decomposition with a negative term, and NOT four shares of one variance.** **The decomposition is reported as a function of the minimum-measurements-per-pair restriction because at the unrestricted specification the subtracted component can be negative, and every percentage in this paper that comes from a row with a negative component is labelled as a component share rather than a variance share.**

**Software.** Python 3.12 with numpy and h5py. **All scripts, result JSONs and the figure source data are
committed; `FIGURE_SOURCE_DATA.json` records a sha256 prefix for each of its twenty-seven source artifacts,
and those twenty-seven now include every artifact the figure legends below name, which an earlier version did
not: six of the seven legend sources, including the order grid, the joint grid and the specification ledger,
were outside the hash chain while the text claimed the chain covered the figures. The file does not carry its
own hash, because writing the value changes the file.**
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

---

## 6. References

**Every entry below was verified against the Crossref REST API (`api.crossref.org/works/<DOI>`), which both
resolves the DOI and returns the record it points to, so a DOI that exists but belongs to a different paper is
caught.** **The queries, the returned metadata and the two fields where sources disagree are recorded in
`../wp3_results/REFERENCE_IDENTIFIERS.md`.** **Volumes, issues, pages or article numbers are as Crossref
returns them.**

1. **Randi F, Sharma AK, Dvali S, Leifer AM.** Neural signal propagation atlas of *Caenorhabditis elegans*.
   *Nature* **623**(7986), 406-414 (2023). doi:10.1038/s41586-023-06683-4. **The source artifact this paper
   audits.**
2. **Greaves MD, Novelli L, Mansour L. S, Zalesky A, Razi A.** Structurally informed models of directed brain
   connectivity. *Nature Reviews Neuroscience* **26**(1), 23-41 (2025). doi:10.1038/s41583-024-00881-3.
   **Quoted in section 1: "it remains unclear whether, at the macroscale, structural (or anatomical)
   connectivity provides useful constraints on models of directed connectivity".**
   **NOTE ON THE YEAR: Crossref gives the online date as 2024-12-11 and the print issue as 2025-01; Europe PMC
   returns 2025. The issue year, 2025, is used here, and the discrepancy is recorded rather than smoothed.**
3. **Currier TA, Clandinin TR.** Infrequent strong connections constrain connectomic predictions of neuronal
   function. *Cell* **188**, 4366-4381.e14 (2025). doi:10.1016/j.cell.2025.05.007, PMID 40460825. **Quoted in
   section 1: connectomic predictions are accurate for some response properties and "surprisingly poor" for
   others.**
4. **Laasch N, Braun W, Knoff L, Bielecki J, Hilgetag CC.** Comparison of derivative-based and
   correlation-based methods to estimate effective connectivity in neural networks. *Scientific Reports*
   **15**(1), article 5357 (2025). doi:10.1038/s41598-025-88596-y, PMID 39948086. **Quoted in section 1: "no
   universally accepted method exists" for inferring effective connectivity.**
5. **Lynn CW.** Simple input-output dependencies explain neuronal activity. *Nature Physics* **22**(7),
   1152-1159 (2026). doi:10.1038/s41567-026-03306-3, PMID 42370308. **Cited in section 3 as a prior against
   claims that structure carries additional predictive content beyond simple input-output dependencies.**
6. **A *Communications Biology* paper on decomposed linear dynamical systems** (2025), PMC12350842. **Cited in
   section 3 as an adjacent framing in tension with section 2.4: its abstract states that cross-individual
   variability "is not noise" but "reflects worm individuality".** **This entry was NOT verified against
   Crossref: it is cited from an abstract-level reading and its DOI was not retrieved. The two quantities are
   not the same and this paper does not resolve the tension.**
7. **Luo Z, Peng K, Liang Z, Cai S, Xu C, Li D, Hu Y, Zhou C, Liu Q.** Mapping effective connectivity by
   virtually perturbing a surrogate brain. *Nature Methods* **22**(6), 1376-1385 (2025).
   doi:10.1038/s41592-025-02654-x, PMID 40263586. **Read at abstract level only; not open access, so its
   methods were not inspected.**
8. **Pradhan S, *et al.*** The wild-type and *unc-31* atlas exports analysed here. OSF record
   doi:10.17605/OSF.IO/E2SYT. **The derived data this paper audits.**
9. **DANDI dandiset 000541.** Whole-brain NeuroPAL calcium imaging with chemical stimulation, 21 sessions,
   `CC-BY-4.0`. **The second dataset the generalisation test in section 3 was designed for; the fetch failed
   and the route is closed.**

**Where these identifiers come from, and the defect this section already had.** **The first version of this
list was written from memory, and six of its nine identifiers appeared nowhere in the committed survey
documents, because those documents record abstracts rather than identifiers.** **Re-deriving them from Europe
PMC confirmed the PMIDs and DOIs were correct but found two missing DOIs and two missing author lists; then
re-deriving them from Crossref, which resolves the DOI to a RECORD rather than merely returning a hit, found
that the Cell entry's identifier was available after all and that the manuscript had no volumes, issues or
pages.** **A memory that happens to be right is not a method.**

**A note on citation practice, which differs from the conventions above.** **The fifteen works in the
literature survey were read at title-and-abstract level, and four in full text; the survey's own document
records which is which, and the negative finding in it -- that none of the fifteen reports a reliability figure
for the functional quantity it predicts -- is a title-and-abstract observation rather than a Methods-level one,
and is stated as such in `../wp3_results/LITERATURE_SURVEY_SPECIFICATION_AND_RELIABILITY.md` and
`../wp3_results/METHODS_LEVEL_SURVEY.md`.**
