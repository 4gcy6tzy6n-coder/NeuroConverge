# Reviewer R1 report

Manuscript reviewed. `v2/manuscript/MANUSCRIPT_v2_draft.md`. Supporting material consulted, `SPECIFICATION_LEDGER.md`, `ORDER_AXIS.md`, `JOINT_GRID_VERIFIED_NONADDITIVE.md`, `CORPUS_INDEX.md`, `FIGURE_SOURCE_DATA.json`. Where I had to trace a number that a permitted file locates but does not contain, I say so explicitly and name the file.

## Overall assessment

This is not a conventional research paper and I have reviewed it as what it is, a measurement-and-provenance audit of one published derived dataset, written by a group that has spent twenty-two rounds auditing its own analysis line. The subject is live and under-served. The paper's strongest material, the specification ledger, the order axis, the non-additivity of two normalisations, and the reliability decomposition, is genuinely worth publishing in some form, because it attaches numbers to a complaint the field currently makes only in prose.

The manuscript's central case is that the artifact's analysis choices live in code and not in the data file, and that those choices move the headline estimate by more than the estimate's own reported span. On the evidence supplied, that case is largely made, and it is made twice over, once by the specification sweep and once by the demonstration in section 2.7 that the authors themselves could not re-derive the published numbers for six rounds.

What stops me short of endorsing it as it stands is narrower and more fixable than the above suggests. Several of the numbers doing the most rhetorical work are not the numbers their own committed documents support. A measurement-error share is quoted as 37 to 57 per cent in the abstract and the Discussion while the Results says 17 to 57 per cent. A pair-specific component is called negative at the unrestricted specification when the correction document that established the negativity also records that the same restriction yields a positive value under a different read-out. A provenance comparison, "larger than the entire span the original work reports", is anchored to a span that belongs to this line and not to the original work. And the manuscript's account of its own verification, "every intermediate then matched bit for bit", attributes to one grid a check that belongs to another, while the grid that produces section 2.2 fails its own check and the failure is unresolved in the source material.

None of this damages the finding that the specification is unrecoverable. It damages the paper's claim, prominent in the abstract, that every number it prints is committed with its own provenance and that measurement survived while interpretation was revised. A paper about the step from a number to a sentence about the number will be read unusually closely on exactly that step.

Genre is also an unresolved problem. As written, this is a methods-and-metascience contribution of perhaps four thousand words doing the work of a full article, with a defect ledger and a self-audit narrative carrying a large share of the argument. Whether Nature is the right venue is a separate question from whether the work is sound, but the paper does not currently answer it.

## Who would be interested in the results, and why

Methodologists and statisticians working on measurement error, reliability and the unit of analysis in neuroscience, who will recognise the pseudo-replication point and the attenuated-correlation argument and will want the estimators stated more carefully than they are.

Researchers who consume connectomic and functional-connectivity derived matrices, including the C. elegans functional-atlas community, who are the immediate users of the artifact audited here and who may reasonably want to know what they have been fitting models to.

Data stewards, repository operators and journal data-editors, because the constructive remedy the paper proposes, publishing the specification as a table alongside the matrix, is cheap and transfers directly to other derived datasets.

Computational reproducibility researchers and metascience groups, for whom the defect ledger is a detailed case study of how an analysis line's interpretation layer, rather than its computation layer, is where the errors accumulate.

Developers of learned models trained on derived neuroscientific matrices, because the paper's claim that such a model inherits a specification it cannot state is concrete and consequential.

Theoretical neuroscientists interested in whether structural connectivity constrains function will find the paper adjacent to their question, and the paper is careful to say that it does not answer it. That care is appropriate and I would not want it relaxed.

## Major strengths

1. The specification ledger in section 2.1 is the right artifact. Seven dimensions, their levels, their isolated measured sizes and a column recording whether the artifact declares each one. This is the structure the field lacks and it is directly reusable.

2. The decision to test an axis for redundancy before reading its result, and to report that one redundant axis had been added by the authors of this paper, is unusually honest and methodologically correct. It appears in the Methods and in the section 2.6 treatment of the three data transforms.

3. Section 2.2's non-additivity finding is a real and non-obvious measurement. Two normalisations whose isolated contributions nearly cancel produce a joint contribution of +0.571 at the 24-volume window. Whatever the reader concludes about the paper's framing, this result stands on its own.

4. Section 2.3's caveat that the per-cell-first order is a constructed specification and not a description of the artifact is exactly the right disclosure and it is placed where the reader meets the claim rather than buried.

5. Section 2.5's retraction and inversion of the line's own most-quoted claim is handled well. The distinction between a z-score and a Cohen's d, and the observation that their ratio is a definitional identity rather than a measurement, is correct, and the reasoning is transparent.

6. Section 2.8 collects the withdrawals in one table and states which of them appear nowhere else in the draft. A paper whose subject is provenance doing this for its own record is the right instinct.

7. The instrument-verification sequence in section 2.7, comparing a re-implementation against the original's intermediates for one animal at machine precision before accepting a grid, is the correct remedy for the failure class the paper describes, and the paper shows the remedy working.

8. The Limitations paragraph is honest about the single-atlas restriction, about the failed second-dataset fetch including the self-inflicted concurrency error, about the ill-posed component, and about the absence of independent review. Many manuscripts in this space would have buried the third of those.

## For each Major Concern

### R1-M1

Concern ID. R1-M1
Severity. Major
Blocking. No
Axis. Evidence chain, quoted magnitude does not follow from the described computation.
Claim pointer. "within-cell measurement error accounts for 37 to 57 per cent of the variance in a pair's response depending on the specification" (Abstract, manuscript line 25), repeated as "measurement error accounting for 37 to 57 per cent of the variance in a pair's response in this artifact" (Discussion, line 272).
Evidence pointer. `MANUSCRIPT_v2_draft.md` line 145 states "The measurement-error share is 17 to 57 per cent depending on the specification", which is the range the committed correction records (38.7 to 57.1 per cent over eight specifications, in `CORRECTION_eps_is_a_range.md`), but the Abstract lower bound of 37 is not carried by any permitted file. `CORPUS_INDEX.md` section 1, the V2-C3 row, also states 17 to 57 per cent. `FIGURE_SOURCE_DATA.json`, key `V2-C3_three_level_decomposition.shares`, contains only the single value 0.3753.
Concern. The same quantity is given two different lower bounds in two places, and the abstract and the Discussion adopt the narrower one. The 17 per cent lower end is the one the corpus's own corrected range supports. A reader who compares the abstract with the Results will not know which range the paper claims.
Why it matters. The measurement-error share is one of the paper's two headline numbers and it is the number that grounds the constructive recommendation in the Discussion, that the artifact should publish a reliability figure. A range that is quoted inconsistently, and in its narrower form in the most-read part of the paper, weakens exactly the claim that the number is well established. It also invites the reading that the wider 17 per cent end was dropped because it is less dramatic.
Resolution test. State one range with its lower and upper endpoints traced to the specification that produced each. If 17 to 57 is the full range over the specifications the corpus swept, use it in the abstract. If 37 to 57 is the intended range over a declared subset, name the subset in the Results and in the figure legend, and reconcile it against the committed 38.7 to 57.1 per cent correction.

### R1-M2

Concern ID. R1-M2
Severity. Major
Blocking. Yes
Axis. Evidence chain, a bounded, read-out-conditional value reported as a general property of the unrestricted specification.
Claim pointer. "the pair-specific animal component is negative at the unrestricted specification -- an impossible value for a variance share, which bounds which specifications are well posed" (Abstract, lines 26 to 28), and "at the unrestricted specification it goes NEGATIVE" (section 2.4, lines 150 to 151).
Evidence pointer. `CORRECTION_variance_decomposition_specification.md` section 3 reports `beta = 5.5 %` at `K = 1` under its read-out, and `CORRECTION_eps_is_a_range.md` section 2 reports `beta = -10.9 %` at `min_an = 1` under the signed-sum read-out while the same restriction under the window-mean read-out gives `beta = 1.9 %` and is never negative. `SPECIFICATION_LEDGER.md` section 3 states the levels as 1, 2, 3, 5, 10 and reports "5.5 % to 46.0 %, and negative at 1".
Concern. The unrestricted specification is described as ill posed in the abstract without the condition under which that is true. The correction document's own table shows the negativity is a property of the combination of an unrestricted minimum-animals-per-pair and the signed-sum read-out, and that a different read-out at the same restriction yields a small positive value.
Why it matters. The negativity is load-bearing twice. It is used to bound which specifications are well posed, and in the Discussion it is offered as a reason to set the unrestricted specification aside. If ill-posedness is read-out-conditional, then the exclusion is partly a choice of read-out, and the conditional exclusion has to be stated or the argument is circular. It also bears on the abstract's inference from a bounded quantity, the negativity observed in a subset of the grid, to an unbounded statement about the specification class.
Resolution test. Report the sign of the pair-specific component for every cell of the grid, with read-out, window and minimum-animals-per-pair named, and state the negativity as a property of the cells in which it occurs rather than of the unrestricted specification. If the unrestricted specification is to be excluded, show that it is ill posed under every read-out that the corpus considers defensible, or state the read-out on which the exclusion depends.

### R1-M3

Concern ID. R1-M3
Severity. Major
Blocking. Yes
Axis. Measurement validity, component shares from an unconstrained subtraction presented as a variance decomposition.
Claim pointer. "Decomposing the per-animal records behind it, within-cell measurement error accounts for 37 to 57 per cent of the variance in a pair's response" (Abstract, lines 24 to 26), and "the pair-specific animal component is negative ... an impossible value for a variance share".
Evidence pointer. `MANUSCRIPT_v2_draft.md` Methods, lines 321 to 324, "the remaining components obtained by subtraction", and "at the unrestricted specification the subtracted component can be negative". `CORRECTION_variance_decomposition_specification.md` section 3 states the subtraction explicitly, `var_beta = var_total - var_alpha - var_pair - var_eps`. `CORRECTION_eps_is_a_range.md` section 2 contains rows whose four entries sum to 111 per cent and to 100.0 per cent in different rows.
Concern. The percentages are described throughout as shares of a variance, but the components are obtained by subtraction with no non-negativity constraint, so in the rows where a component is negative the four numbers printed are not shares of a common total. The paper registers the impossibility for one component and stops there, while continuing to print positive percentages from the same constrained arithmetic as though they were shares. The Discussion goes further and states that the artifact "reports no reliability for the quantity it publishes" while the paper's own substitute for that reliability is this decomposition.
Why it matters. The decomposition is the paper's answer to the absence of a reliability figure in the artifact. If the substitute cannot be read as a share of variance, it cannot carry that role, and the claim that measurement error accounts for a stated per cent of a pair's response loses its denominator. The Methods describe the model as `y = mu + alpha[animal] + beta[animal, pair] + eps` in log space, with `eps` identified from repeated-measurement cells and the rest by subtraction. A decomposition whose components may be negative is a component-shares model, not a variance decomposition, and it needs to be reported as one, with the identification assumption stated and tested.
Resolution test. Report the components as absolute variances with an uncertainty on each, in place of, or alongside, the percentages. State and test the assumption that within-cell error variance is the same in the repeated-measurement cells used to identify `eps` as in the singly measured cells. Restrict any reported percentage to rows in which every component is non-negative, and label those rows. If the paper wishes to retain the reliability claim, present it as a bound conditional on a declared positivity region rather than as a point percentage.

### R1-M4

Concern ID. R1-M4
Severity. Major
Blocking. Yes
Axis. Evidence chain, verification attributed to the wrong grid, and a grid whose own correctness check the source does not accept.
Claim pointer. "The resolution, in round 40, was to stop hypothesising and instead verify each re-implemented step against the code's own intermediate values for a single animal. Every intermediate then matched bit for bit ... and with the verified sequence the pipeline's own configuration reproduced at `d = 0.7289` and `t = 7.610` against the code's `0.7289` and `7.610`." (section 2.7, lines 220 to 224)
Evidence pointer. `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 2 states that its correctness-check cell, post 24 with no cell normalisation and weighting on, "returns `d_A = 0.7331` and `t = 7.654`, against `09_animal_level.py`'s 0.7289 and 7.610 -- a difference of 0.0042 attributable to a slightly different event set". `ORDER_AXIS.md` section 1 states that the exact match is `w` at post 24 giving 0.7289 and 7.610, that this is the check "this round passes it", and that "Round 41 ... attributed the 0.0042 difference to a 'slightly different event set'. That attribution was wrong: the exact match is available in this grid, and round 41's 0.0042 was an implementation difference it did not find." The 0.5789 interaction and the +0.5706 joint value in section 2.2 come from the joint grid, `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 3.
Concern. The intermediate-value verification and the exact 0.7289 match belong to the order-axis grid, not to the joint grid from which the non-additivity result is drawn. The joint grid's own check differs by 0.0042, and the source records that the explanation offered for that difference was refuted and that the difference remains an unidentified implementation difference. The manuscript's section 2.7 sentence is placed under the claim that "Every value in section 2.1 was produced by re-implementing the pipeline", which the reader will take to cover section 2.2 as well.
Why it matters. Section 2.2 is one of the two results the abstract leads with, and it is the result that licenses the paper's warning that the ledger cannot be read additively. It rests on a grid that failed its own correctness check, and the paper's own provenance narrative conceals rather than discloses that fact, because it reports the other grid's success. The paper's subject is precisely that unverified re-implementation produces wrong numbers. A reader who checks the two committed documents will find the manuscript reporting a failed check as a passed one.
Resolution test. Report the joint grid's own check cell, its value, and the 0.0042 discrepancy, together with the refuted attribution, in the section that presents section 2.2. Either resolve the discrepancy and re-run the grid, or demonstrate the non-additivity on a grid whose check passes, or state the non-additivity as provisional. In all cases attribute each verification to the grid it belongs to.

### R1-M5

Concern ID. R1-M5
Severity. Major
Blocking. Yes
Axis. Measurement validity, a specification dimension measured as conditional produces a magnitude that is not on the same scale as the others.
Claim pointer. "The largest is not a parameter but an ORDER: two defensible normalisations of the same response, applied in the two possible sequences, give animal-level estimates of `d = +0.97` and `d = +0.12` at the same post-stimulus window" (Abstract, lines 17 to 19), and "the order of application | two sequences of two normalisations | 0.02 to 0.85, depending on window" (section 2.1, line 92).
Evidence pointer. `ORDER_AXIS.md` section 5 states "ORDER A is not a pipeline that anyone wrote. It is per-cell normalisation followed by the weighting, and the code does the weighting without any per-cell normalisation. So ORDER A is a CONSTRUCTED specification ... and not a description of the artifact." The same document, section 2, gives the order effect as +0.0234 at post 12, -0.8493 at post 24 and +0.2091 at post 48.
Concern. Two separate difficulties sit inside one sentence. First, the order is not a dimension of the artifact at all, because the artifact does not apply per-cell normalisation, so there is no order to permute in the code's configuration. The order becomes a choice only for a user who has already decided to add per-cell normalisation, which the manuscript concedes in section 2.3 but not in the abstract or in the section 2.1 table. Second, the effect of the order is 0.0234 at one of the three windows, which is smaller than every one of the six other rows in the section 2.1 table, so on the ledger's own units the order is the smallest dimension at that window and the largest at another, and the section 2.1 table quotes a range for it while quoting point values for the rest.
Why it matters. The abstract, the section heading in 2.3 and the Discussion all present the order as the largest dimension. That is true at one window out of three under a configuration the pipeline does not use. The distinction between a dimension of the artifact and a dimension of a hypothetical user's additional choice is the whole difference between the paper's claim and a stronger claim than its evidence supports. The table's mixed convention, a range for one row and scalars for six, also means the rows cannot be compared by reading down the column.
Resolution test. Restrict the order claim to the read-outs under which a reordering is possible, and report the order effect as a function of window rather than as a single range. Add a column or a footnote to the section 2.1 table distinguishing dimensions of the artifact from dimensions introduced by a change the artifact does not make. State explicitly that under the artifact's own configuration the order contribution is zero because one of the two operations is absent. Where the paper reports a headline order effect, state the window at which it holds in the same sentence.

### R1-M6

Concern ID. R1-M6
Severity. Major
Blocking. Yes
Axis. Measurement validity, a stability claim resting on three values, with the sign-changing endpoint flagged by the source as not to be treated as a finding.
Claim pointer. "one sequence is stable across windows to within 0.006 while the other spans 1.064 and changes sign" (Abstract, lines 19 to 20), and "the per-cell-first order gives 0.0958, 0.9685 and -0.0958, a spread of 1.064 and a change of sign" (section 2.3, lines 131 to 132).
Evidence pointer. `ORDER_AXIS.md` section 2 gives the three windows as post 12, 24 and 48 volumes. The same document's section 6 states, of the negative value, "A check of the `cn`-only arm's negative value at post 12 (-0.0358) ... Named, not explained" and `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 6 states of the post-48 cell, "a check of the sign reversal at post 48, where cell normalisation plus weighting gives -0.0958 with `t = -1.000` -- named, not explained, and not to be treated as a finding until the order axis is in."
Concern. The post-48 value of -0.0958 is one of the three endpoints of the spread of 1.064 and it is the source's own example of a cell that is named and not explained. The three windows are also not independent, they are nested intervals beginning at the same post-stimulus volume, so three points are being used to distinguish a stable arm from an unstable one with no interval, no standard error and no smaller window resolution than 12 volumes. The word spread is doing the work of an uncertainty statement.
Why it matters. The stability contrast is the abstract's reason for preferring one ordering, and it is the sentence a reader is most likely to quote. A three-point range that is sensitive to a flagged, unexplained cell, on nested windows, at a single site, over a single atlas, will not bear the claim that one order is stable and the other is not. The paper's own Limitations concede the single atlas. This claim needs the same treatment.
Resolution test. Report the window set as nested and overlapping, and report the order effect and each arm as a function of window rather than as a range across three points. State which arm reverses sign and at which window, with the cell's own flag carried over from the source. Either exclude the flagged post-48 cell from the stability statement or report the statement with and without it. If the word stable is retained, define the criterion the arm has to meet and report the numbers against that criterion.

### R1-M7

Concern ID. R1-M7
Severity. Major
Blocking. No
Axis. Evidence chain, a corpus-internal estimate attributed to the artifact under audit.
Claim pointer. "At a 24-volume window the two orders differ by 0.85 -- larger than any dimension in 2.1 and larger than the entire span the original work reports." (section 2.3, lines 129 to 130, and the same construction in the Abstract at lines 13 to 14).
Evidence pointer. The span of 0.6437 is V2-C4's own range, `0.0852` to `0.7289`, as recorded in `SPECIFICATION_IN_LITERATURE.md` section 3, which tabulates "the estimates span 0.085 to 0.729" against the description "this line's own five rows", and in `SPECIFICATION_LEDGER.md` section 1, which states that V2-C4's range "mixes a weighted pipeline against three unweighted ones" and that "its widest extent comes from mixing two families rather than from varying one".
Concern. The manuscript attributes to the original work a span that the corpus's own documents attribute to this line's five constructions. The V2-C4 range of 0.085 to 0.729 is described in its own source documents as a union over two specification families rather than as a quantity the atlas reports. The abstract's formulation, "move the headline estimate by more than the range the original work reports", therefore rests on a comparison between two quantities that are not of the same kind, a single-window order difference on one hand and a cross-family union of this line's own estimates on the other.
Why it matters. This comparison is the abstract's justification for calling the specification dimensions large, and it is repeated in the Discussion. If the reference span is the audit's own artefact, then the paper is comparing a measured difference against a range it constructed, without saying so. The claim that the dimensions are larger than the effect the source reports is a strong and, if properly supported, important claim. It needs an anchor that belongs to the artifact.
Resolution test. Replace the reference span with a quantity the artifact itself reports, quoted from the artifact or from a document that reads it, or state plainly that the comparison is against this line's own reported range across specifications. If the comparison against this line's range is retained, report it against a single weighting family, since the source documents state that the family-mixed span is not attributable to the choices it lists.

### R1-M8

Concern ID. R1-M8
Severity. Major
Blocking. No
Axis. Measurement validity, an attenuation correction whose reliability term is estimated from two animals and 23 shared cells.
Claim pointer. "Under classical test theory the observed association is attenuated by roughly `sqrt(0.208) = 0.456`, implying a true association near 0.081" (section 2.6, lines 190 to 191), together with "the bound stays between +0.208 and +0.270, always far below the 0.5 that would indicate a reproducible functional quantity" (lines 196 to 198).
Evidence pointer. `FIGURE_SOURCE_DATA.json`, key `V2-C2_fig6_reproduction`, records `n.animals = 2`, `n.shared_cells = 23`, `cross_animal_r_of_correlation_matrix = 0.2084`, and the two per-animal reproductions at `r = 0.0368` with 3,540 pairs and `r = -0.0064` with 1,560 pairs. `CORPUS_INDEX.md` section 1 describes V2-C2 as "reproduced and stress-tested across four specifications; `n = 2` stated".
Concern. The reliability term in the correction is a correlation between two animals over 23 shared cell names, and it is being used as a classical test theory reliability coefficient. Two animals give a reliability estimate with no usable standard error, and the correction constant is estimated from the same specifications whose spread the paper offers as evidence of stability. The arithmetic itself is sound, `0.0368 / 0.456 = 0.081`, but the corrected value inherits the variability of the reliability estimate, and the paper presents it as a point without an interval. The stability claim for the bound, a range from 0.208 to 0.270, is a range across estimators computed on the same two animals and the same 23 cells, and it is quoted as a stability property of the quantity.
Why it matters. The like-for-like comparison is the paper's one direct engagement with the artifact's own published claim, and it is where a reader will look for whether the audit is fair to the source. A corrected magnitude resting on a two-animal reliability estimate is exactly the kind of inference the paper criticises elsewhere when other authors make it.
Resolution test. Report the reliability estimate with the sample it is estimated from and an interval that reflects that sample, or state the correction as illustrative and decline to give a point value. Report how the corrected magnitude moves with the reliability estimator, and state that a range of corrected values computed from a varying constant is not evidence of stability in the corrected quantity. Carry the `n = 2` and 23-cell restriction into the sentence that quotes 0.081, not only into the surrounding paragraph.

### R1-M9

Concern ID. R1-M9
Severity. Major
Blocking. No
Axis. Evidence chain, an unfalsifiable provenance claim and an over-strong survivorship claim.
Claim pointer. "Every intermediate then matched bit for bit" (section 2.7, line 222) and "every MEASUREMENT survived re-examination and every INTERPRETATION attached to one was revised at least once" (Abstract, lines 41 to 42, and section 2.8, lines 249 to 252).
Evidence pointer. `CORPUS_INDEX.md` section 1 and section 4 record an INVALID script that "indexed the connectome by the wrong neuron order, giving an implausible `d = 4.74`", an INVALID script whose per-cell normalisation "divided by a pre-stimulus SD over 8 volumes, blowing up to about `1e11`", and an INVALID weighting arm whose weights "span thirty-one orders of magnitude". `FIGURE_SOURCE_DATA.json` key `excluded` records that the ICC of 0.93 was "inflated by construction". `CORPUS_INDEX.md` section 3 and `FIGURE_SOURCE_DATA.json` key `supporting_reliability` record `noise_frac = 0.4218` alongside `between_animal_r_full = 0.0405`.
Concern. Two claims in the abstract are stated more strongly than the record supports. The survivorship claim is contradicted by the paper's own retained artifacts, which include measurements of 4.74, of order 1e11, and the withdrawn ICC, all of which were measurement errors rather than interpretation errors. The bit-for-bit phrasing of the verification is also stronger than the comparison it describes, since agreement at machine precision was established for one animal and for named intermediates, and the same source records an unresolved 0.0042 difference on another grid.
Why it matters. The distinction between measurement error and interpretation error is the paper's explanatory punchline, and it is what the reader is asked to take away about how this kind of line fails. A punchline that is contradicted by the paper's own ledger is a serious problem in a manuscript whose central selling point is that it shows its own discarded work. The `noise_frac` of 0.4218 is a separate difficulty, since a near-zero between-animal correlation of 0.0405 is hard to reconcile with a 42.2 per cent noise share of the same effect, and the two appear in the same source key without an explanation of which quantity each describes.
Resolution test. Restate the survivorship claim as what the ledger shows, namely that no surviving measurement was later found to be an arithmetic error while several interpretations were revised, and enumerate the measurement-level defects that were found. Attribute the intermediate-value verification to the animal and the intermediates it covered, and state the unresolved discrepancy on the other grid. For the 0.4218 figure, name the quantity it is a noise share of and state whether it is a within-animal or a between-animal reliability, and explain how it coexists with the between-animal correlation of 0.0405.

### R1-M10

Concern ID. R1-M10
Severity. Major
Blocking. No
Axis. Measurement validity, two different quantities compared for size after the paper has shown the comparison is definitional.
Claim pointer. "Measured properly, the pair-level effect size is SMALLER than the animal-level one: 0.022 against 0.421." (section 2.5, lines 168 to 169).
Evidence pointer. `FIGURE_SOURCE_DATA.json` key `V2-C1_unit_inflation` gives the animal-unit values as `0.4145` at `n = 108` for the chemical contrast, `0.7690` at `n = 109` for gap, and `0.7289` at `n = 109` for combined. `0.421` does not appear in that key, and the value nearest to it is the chemical contrast. The pair-unit counterpart recorded in the same key is `d_combined_pair_unit = 11.048`, a z-score. The paper's own source for this retraction, `CORRECTION_unit_inflation_is_significance.md` section 2, states that the ratio is "`sqrt(n)`. It is not a measurement of inflation; it is the definitional consequence of the two denominators differing by the sample size."
Concern. The retraction's replacement sentence is a new cross-quantity comparison. The two numbers differ in unit, and if 0.421 is the chemical contrast then they differ in contrast as well. The paper has just argued that the ratio of these two quantities carries no information because it is definitional, and it then uses their difference to state which is larger. A difference between a z-score over pair measurements and a Cohen's d over animals is a statement about two denominators, not about the size of an association.
Why it matters. This is the correction of the line's most-repeated error, and the paper flags it as a second instance of the paper's own subject, a quantity named `d` meaning two different things. If the corrected sentence contains the same category error in a milder form, the correction is incomplete and a reader who checks the arithmetic against the committed figure data will not be able to reproduce 0.421.
Resolution test. Name the contrast and the unit for each of the two values, give the sample each is computed over, and state whether the two are on a common scale. If they are not, withdraw the size comparison and retain the significance statement, which the paper states correctly and with a defined quantity. Trace 0.421 to its committed artifact or replace it with a value that is traceable.

### R1-M11

Concern ID. R1-M11
Severity. Major
Blocking. No
Axis. Evidence chain, a count presented as if each item were separately documented.
Claim pointer. "We report the full defect ledger -- seventeen numbered self-found errors, each named by the correction document that records it, plus earlier ones referenced in prose and not separately documented" (Abstract, lines 34 to 36).
Evidence pointer. `CORPUS_INDEX.md` section 5 states "Seventeen numbered self-found defects, from the fifth to the twenty-first, each named by its own committed correction document; defects one to four are referenced in prose but have no document that names them." The same section records that the count was previously stated as twenty-one and that "the count was previously stated as twenty-one, which came from a figure whose table was typed from memory". The manuscript also states, of section 2.8, "The count of such events is seventeen numbered defects, listed in section 2.7 and in Figure 6" (lines 246 to 247), while the section 2.7 table contains six rows and Figure 6's declared source is `CORPUS_INDEX.md`.
Concern. The abstract's "each named by the correction document that records it" is contradicted by the source document, which states that four of the defects have no naming document. The abstract's pointer to section 2.7 for the count of seventeen will also mislead, since that section lists six re-implementation rounds. The number appears in the abstract three times over and each appearance points to a different, and in two cases inaccurate, location.
Why it matters. The defect ledger is offered as evidence for the central claim rather than as an appendix, and its count is the item most likely to be quoted. A count whose own source document records that including it required correcting a figure typed from memory is precisely the failure mode the paper documents, so drifting on the count is costly here in a way it would not be elsewhere.
Resolution test. State the count as seventeen numbered defects of which thirteen carry their own correction document, and give the count of prose-only defects separately. Point to `CORPUS_INDEX.md` section 5 as the ledger's location and to Figure 6 as its rendering, rather than to section 2.7, whose table covers the six re-implementation rounds only.

### R1-M12

Concern ID. R1-M12
Severity. Major
Blocking. No
Axis. Evidence chain, a headline superlative that holds at one window out of three.
Claim pointer. "At a 24-volume window the two orders differ by 0.85 -- larger than any dimension in 2.1 and larger than the entire span the original work reports." (section 2.3, lines 129 to 130, and the section heading "2.3 The largest dimension is the order", line 117).
Evidence pointer. `ORDER_AXIS.md` section 3 gives the order effect as `+0.0234` at post 12, `-0.8493` at post 24 and `+0.2091` at post 48. `SPECIFICATION_LEDGER.md` section 3 gives per-cell normalisation as `0.3395`, per-event weighting as `0.3356` and post-stimulus window as `0.2364`.
Concern. This is the window-specific case of R1-M5 and I separate it because the superlative is stated as a property of the paper rather than of a window, in the section heading, in the Abstract and in the Discussion, while the supporting numbers make it true at post 24 only. At post 12 the order effect, 0.0234, is smaller than all six other rows of the ledger, and at post 48 it is comparable to the common-mode entries. The table in 2.1 already concedes the window dependence by quoting the order row as a range, so the paper contains both the concession and the unrestricted superlative.
Why it matters. The superlative is the paper's most quotable sentence and the one that will be checked first. If a reader recomputes from the committed order grid, the heading will look like a selection of the window that supports it, which is the failure mode the paper attributes to the artifact it audits.
Resolution test. Qualify the superlative with the window in the section heading and in the Abstract, or state the order as the largest dimension at one of three windows and describe the window dependence as the finding, which is arguably the stronger and more defensible version of the claim.

### R1-M13

Concern ID. R1-M13
Severity. Major
Blocking. No
Axis. Inference from a bounded quantity to an unbounded one, and a quantity that does not lie on the scale it is compared against.
Claim pointer. "two defensible normalisations of the same response, applied in the two possible sequences, give animal-level estimates of `d = +0.97` and `d = +0.12` at the same post-stimulus window" (Abstract, lines 17 to 19).
Evidence pointer. `ORDER_AXIS.md` sections 2 and 5. Section 5 states that ORDER A is constructed and that the code applies no per-cell normalisation. Section 2 gives ORDER A as `+0.9685` at post 24 and ORDER B as `+0.1192`.
Concern. The abstract describes the two arms as two applications of the same two normalisations, and the reader will take them to be the two sequences of one operation set. The source states that one arm, per-cell first, includes a normalisation the pipeline never performs, so the pipeline's own configuration is the weighting alone. The abstract therefore quantifies the consequence of a change the artifact does not make, a user choosing to add a normalisation and then placing it, and reports it as a property of the artifact's own choices.
Why it matters. A bounded, conditional quantity is being presented as an unbounded claim about the artifact. The distinction is the same one the paper demands of the source, and the paper's own section 2.3 caveat does not travel into the abstract, where the claim will be read. This is also why the order dimension does not sit on the same scale as the six other rows of the section 2.1 table.
Resolution test. State in the Abstract that the comparison is between the artifact's configuration and a user's added normalisation, name the operation set of each arm, and report the effect of the order alone, within an arm where per-cell normalisation is present in both sequences, as the quantity that measures the order.

### R1-M14

Concern ID. R1-M14
Severity. Major
Blocking. No
Axis. Evidence chain, unreproducible relationship between two numbers computed on different pair sets and scales.
Claim pointer. "the between-animal spread is 42.2 per cent measurement noise and 17.7 per cent pair composition, with about 40 per cent unexplained by anything measured" (section 2.8, lines 239 to 240).
Evidence pointer. `FIGURE_SOURCE_DATA.json` key `supporting_reliability` records `split_half_r_full = 0.5266`, `noise_frac = 0.4218`, `signal_frac = 0.5782`, `between_animal_r_full = 0.0405` and `units_within = 33578`. The same key's `cross_animal_reliability_by_strain` values are `0.1196` for NONE, `0.2263` for A_abs2sd and `0.3318` for B_topdecile. `SPECIFICATION_LEDGER.md` section 3 states the spread's decomposition as "42.2 per cent measurement noise, about 40 per cent unexplained".
Concern. A noise share of 42.2 per cent is hard to reconcile with a between-animal correlation of 0.0405 for the same effect, and the paper does not set out how the two are related or on what scale the 42.2 per cent is computed. The manuscript uses the 42.2 figure to narrow a claim about what is reproducible, which makes the identity of the quantity it is a noise share of load-bearing.
Why it matters. The paper's subject is the reliability of a published quantity, and its own reliability numbers should be stated so that they can be checked against each other. Two reliability figures for the same named effect, 0.0405 and 0.5266, that differ by more than an order of magnitude and are not related to each other anywhere in the draft will be read as a gap by any reviewer who works on measurement error.
Resolution test. State what the 42.2 per cent is a noise share of, whether it is within-animal or between-animal, and on what scale. Relate it to the between-animal correlation stated in the same source, or state that the two measure different quantities and give each an explicit definition. If the two cannot be reconciled from the committed artifacts, mark the figure as provisional.

## Minor Comments

### R1-m1

Concern ID. R1-m1
Severity. Minor
Axis. Reporting.
Affected element. Section 2.6, lines 196 to 197, "the reproduction stays between +0.036 and +0.038 in the first animal".
Evidence pointer. `FIGURE_SOURCE_DATA.json` key `V2-C2_fig6_reproduction` gives `fig6_animal0.r = 0.0368` and `fig6_animal1.r = -0.0064`.
Issue. The sentence names the first animal but not the second, and it gives no value for the second animal in the stability statement, although the second animal's reproduction is reported earlier in the section. The reader cannot tell from this sentence that the two animals' reproductions differ in sign.
Required correction. Name both animals and give each one's reproduced value in the stability sentence.

### R1-m2

Concern ID. R1-m2
Severity. Minor
Axis. Reporting.
Affected element. Section 2.8, lines 233 to 234, "Four interpretations this line published in earlier rounds are withdrawn or narrowed", and lines 249 to 252 on the pattern.
Evidence pointer. `CORPUS_INDEX.md` section 5 states "three were withdrawn or narrowed outright" while `FIGURE_SOURCE_DATA.json` key `withdrawn_or_narrowed` lists four entries. The table in section 2.8 has five rows.
Issue. The count of withdrawn or narrowed interpretations appears as four in the manuscript, four in the figure source data and three in the corpus index, and the section 2.8 table has five rows because the ICC withdrawal is listed separately from the four interpretations.
Required correction. Reconcile the count in one place. State whether the ICC withdrawal is included in the four, and align the manuscript, the figure source data and the corpus index.

### R1-m3

Concern ID. R1-m3
Severity. Minor
Axis. Specification description.
Affected element. Section 2.1, line 96, "baseline convention | volumes 30-60, or 0-60 before the stimulus | 0.0295 to 0.0496".
Evidence pointer. `SPECIFICATION_LEDGER.md` section 3 states the same levels and the same range, but reports the second level as "0-60" without the qualifier "before the stimulus", and reports the size as a range without stating which level each endpoint belongs to.
Issue. The size for this dimension is a range whose endpoints are not attributed to levels, so a reader cannot tell whether 0.0295 and 0.0496 are two specifications or a spread within one.
Required correction. State the size of each level against that level, in the manuscript and in the ledger.

### R1-m4

Concern ID. R1-m4
Severity. Minor
Axis. Mechanisms and explanations.
Affected element. Section 2.2, lines 114 to 115, "The reason is that both are normalisations and each rescales the quantity the other operates on, which is why the ORDER is itself a dimension."
Evidence pointer. `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 3 gives the interaction as `-0.1076` at post 12, `+0.5789` at post 24 and `-0.6349` at post 48.
Issue. The stated mechanism is offered as the reason for the interaction, but the interaction it is meant to explain is positive at one window and negative at the other two. A mechanism that is symmetric in the two normalisations cannot by itself explain why the sign flips across windows.
Required correction. State the mechanism as a necessary condition for an interaction and give the additional window-dependent cause of the sign, or restrict the mechanism sentence to the post 24 cell in which it is illustrated.

### R1-m5

Concern ID. R1-m5
Severity. Minor
Axis. Methods completeness.
Affected element. Section 2.2 and section 2.3, and the Methods paragraph on specification grids at lines 313 to 315.
Evidence pointer. `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 2 describes a twelve-cell grid over window, per-cell normalisation and weighting, while `ORDER_AXIS.md` section 2 describes a fifteen-cell grid over five order arms and three windows.
Issue. The Methods state that each dimension was varied alone "and then jointly" but do not report the size, the factors or the order arms of the joint grids, and the two grids the results actually use differ in cell count and in factors.
Required correction. Add the joint grid factors, levels and cell counts to the Methods, and state which grid produces which result.

### R1-m6

Concern ID. R1-m6
Severity. Minor
Axis. Provenance of an unrounded figure.
Affected element. Section 2.6, line 187, "their activity-correlation matrices agree at only `r = +0.2084`", and section 2.6, lines 196 to 197, the bound "between +0.208 and +0.270".
Evidence pointer. `FIGURE_SOURCE_DATA.json` key `V2-C2_fig6_reproduction` gives `cross_animal_r_of_correlation_matrix = 0.20845` and `n.shared_cells = 23`; `CORPUS_INDEX.md` section 3, the `V2C2_STRESS_TEST.md` row, states the bound "ranges 0.208 to 0.270".
Issue. The 0.2084 value and the upper end of the bound are quoted to four and three decimal places from a correlation computed over 23 cells in two animals. The precision is not meaningful at that sample size and the upper end is not traceable to the permitted figures.
Required correction. Report both with two decimals and with the sample beside them, and cite the artifact that produces the 0.270 end.

### R1-m7

Concern ID. R1-m7
Severity. Minor
Axis. Definition of a central quantity.
Affected element. Section 2.4, lines 141 to 143, and the Methods decomposition at lines 321 to 324.
Evidence pointer. `CORRECTION_eps_is_a_range.md` section 2 gives row totals of 111 per cent and of 100.0 per cent; `FIGURE_SOURCE_DATA.json` key `V2-C3_three_level_decomposition` gives one four-component set summing to 100 per cent at `n_units = 192303`.
Issue. The model is described in the narrative as a decomposition of "the per-animal records behind the atlas" into four components, while the underlying unit count and the space in which the model is fitted, log space, appear only in the source documents. In log space the components are additive in log units, not in the response, so a share is a share of log variance.
Required correction. State the space, the unit and the unit count in the Methods, and state that the reported shares are shares of log-scale variance.

### R1-m8

Concern ID. R1-m8
Severity. Minor
Axis. Internal consistency of the ledger and its index.
Affected element. Section 2.1, line 98, "the cell pool the common mode spans | all columns, or the uniquely-named ones | 0.0038".
Evidence pointer. `MANUSCRIPT_v2_draft.md` line 216 gives the same 0.0038 value. `CORPUS_INDEX.md` section 6, item 4c, states that the common-mode cell pool is "measured it at 0.34 in `d_A`, larger than the whole range spanned by window, baseline and normalisation together", while `SPECIFICATION_LEDGER.md` section 3 and the `CORRECTION_cell_pool_refuted.md` row in `CORPUS_INDEX.md` section 3 give 0.0038.
Issue. The ledger index that the Methods and the figure legends point to still carries the superseded 0.34 value for this dimension in its reading instructions, while the manuscript and the specification ledger both use 0.0038. The manuscript's own text also records the 0.0038 against an attributed 0.34 as round 33's error.
Required correction. Correct item 4c of the corpus index to 0.0038, and cross-reference the refutation, so that the document the paper cites as the ledger's source does not contradict the paper.

### R1-m9

Concern ID. R1-m9
Severity. Minor
Axis. Figure traceability.
Affected element. Figure legends 1 to 6, lines 338 to 355, and the Methods sentence "`FIGURE_SOURCE_DATA.json` records a sha256 prefix for each of its twenty-two source artifacts" (lines 326 to 327).
Evidence pointer. `FIGURE_SOURCE_DATA.json` `source_hashes` contains 22 entries, none of which is `RESULT_joint_grid_verified.json`, `RESULT_order_axis.json`, `RESULT_variance_decomposition_sweep.json`, `RESULT_decomposition_weighted.json`, `RESULT_fig6_specification_grid.json` or `CORPUS_INDEX.md`. All six files exist under `v2/wp3_results/anatomy/`.
Issue. The figure legends declare sources outside the figure source data file, so the hash chain the Methods describe does not cover Figures 2, 3, 4 and 6 and part of Figure 5. The claim that the figures retype nothing is therefore not checkable through the mechanism the paper names.
Required correction. Extend the source-hash block to cover every artifact a legend names, or state in the Methods which figures fall outside the hash chain and why.

### R1-m10

Concern ID. R1-m10
Severity. Minor
Axis. Caveat placement.
Affected element. Section 2.3, lines 134 to 137, and the Figure 3 legend at lines 344 to 345.
Evidence pointer. `ORDER_AXIS.md` section 5 and section 6, item 2.
Issue. The constructed-specification caveat appears in the running text, which is the right place for it, but the Figure 3 legend presents the two sequences and their stability without it. A reader who reads the figure and its legend alone will take both arms to be descriptions of the artifact.
Required correction. Add the constructed-specification caveat to the Figure 3 legend.

### R1-m11

Concern ID. R1-m11
Severity. Minor
Axis. Terminology.
Affected element. Abstract, lines 16 to 17, "We measure seven specification dimensions, each by varying it alone and holding the others fixed."
Evidence pointer. `SPECIFICATION_LEDGER.md` section 3 states that isolated contributions were computed "by varying one axis and holding the others fixed". `JOINT_GRID_VERIFIED_NONADDITIVE.md` section 3 shows the dimensions are not additive, and the manuscript's own section 2.2 states this.
Issue. The construct of an isolated contribution is only well defined relative to a declared baseline configuration, and the sections 2.1 numbers are reported as isolated sizes without the baseline being stated, even though the baseline determines the sign and magnitude of each, as section 2.2 demonstrates.
Required correction. State the baseline configuration against which each isolated contribution is measured, and state that isolated contributions are properties of that baseline and not of the dataset.

### R1-m12

Concern ID. R1-m12
Severity. Minor
Axis. Attribution within the demonstration.
Affected element. Abstract, lines 30 to 33, "we attempted to re-derive the artifact's own numbers, and the attempt failed for six consecutive rounds because our re-implementations differed from the original code in ways not visible on reading it."
Evidence pointer. `MANUSCRIPT_v2_draft.md` section 2.7 table, lines 211 to 218, lists rounds 29, 31, 32, 33, 34 and 39.
Issue. The six listed rounds are consecutive in the sense that no listed round falls between them, but they are not consecutive rounds of the line, since rounds 30 and 35 to 38 are omitted from the table. The abstract's "six consecutive rounds" invites the reading that the line failed on six successive attempts without intervening progress.
Required correction. Say "six rounds" and give the round numbers, or state that other rounds intervened.

## Technical failings that need to be addressed before the case is established

R1-M2, the read-out dependence of the pair-specific component, and R1-M3, the treatment of component shares from an unconstrained subtraction as a variance decomposition. These two together determine whether the paper's reliability claim can be made at all in its present form, and I regard them as the most serious items in this report because the paper's remedy section rests on them.

R1-M4, the attribution of the order-axis verification to the joint grid that produces section 2.2, together with the unresolved 0.0042 discrepancy in that grid. Until this is corrected, the paper reports a failed check as a passed one in the section whose stated purpose is to demonstrate verification.

R1-M5, R1-M6 and R1-M12, which are three faces of one problem, the treatment of the order dimension. The order is conditional on an operation the artifact does not perform, its magnitude is 0.0234 at one window and 0.8493 at another, its stability contrast depends on a cell the source flags as not to be treated as a finding, and the superlative that carries it into the Abstract and the Discussion holds at one window of three.

R1-M7 and R1-M13, both of which are comparisons against quantities that do not lie on the scale the comparison assumes, one a corpus-internal range attributed to the artifact, the other a constructed arm presented as a sequence of the artifact's own operations.

R1-M1, R1-M10 and R1-M11 are presentational and traceability failures rather than structural ones. Each is a sentence in the Abstract whose number the committed material does not carry in the form the sentence uses.

Not assessable from the permitted material. The reference identifier verification described in section 6 cannot be checked, since `REFERENCE_IDENTIFIERS.md` was not among the documents I was permitted to read. I record no finding on it. The figure renderings themselves are declared in the legends but were not supplied as images to me, so I make no assessment of the six figures beyond their declared sources. The 464-fold sample-size statement in section 2.5, lines 171 to 173, is not derivable from any figure in the permitted files, and `CORRECTION_unit_inflation_is_significance.md` states the same 464 without a derivation; I record this as not assessable rather than as a concern. The `46.0` per cent upper end of the pair-specific range in section 2.4 is not present in the permitted files, which show the sweep only to `K = 5` at 43.1 per cent; I record this as not assessable.

## Assessment against Nature-style criteria

Originality. The framing, that a derived dataset's specification is a second scientific object with no reporting convention, is not itself new, but the execution is. Enumerating seven dimensions of one published artifact, measuring each, and demonstrating non-additivity between two of them is, as far as the permitted material lets me judge, a novel piece of measurement. The non-additivity result in section 2.2 is the most original single finding.

Scientific importance. Moderate and conditional on the repairs above. The paper does not test a biological hypothesis and does not claim to, which is appropriate. Its importance rests on whether the specification sensitivity and the reliability gap it measures are typical, and the paper correctly concedes that one artifact cannot establish a norm. That concession limits the importance claim to a case study, and the Discussion's recommendation, publish the specification alongside the matrix, is sensible and cheap but not demonstrated to be sufficient. The importance would rise considerably if a second artifact were audited, which the authors attempted and could not complete.

Interdisciplinary readership. Good in principle and poorly served in practice by the current draft. The problem is real for anyone who consumes a derived matrix across systems neuroscience, connectomics and the machine-learning applications the paper invokes in the Discussion. The obstacle is the density of internal corpus referencing. Sections 2.5, 2.7 and 2.8 refer to rounds, correction documents, invalid runs and ledger items that an outside reader cannot resolve, and the defect ledger carries a large share of the argument in a form that reads as laboratory record rather than as a scientific article. A reader from an adjacent field will also need the notation paragraph to be closer to the first use of `d`, since `d` means four things across this line by the paper's own account.

Technical soundness. Mixed. The individual computations I could trace are arithmetically sound, and the auditing methods, the redundancy check, the step verification and the retraction are of high quality. The failures are in the step from computation to claim, which is the paper's own stated subject. The measurement-error range is quoted inconsistently, one component's sign is stated without its condition, the verification narrative attributes one grid's check to another, and two comparisons are made against quantities that are not comparable. None of these invalidates the central finding that the specification is unrecoverable, but together they mean the paper does not currently meet the standard it sets for the artifact it audits.

Readability for nonspecialists. Weak as drafted. The Abstract is compressed to the point where several claims cannot be followed without the Results, and the Results assume familiarity with the corpus's own vocabulary of rounds, ledgers and correction documents. The constructive sections, the Introduction and the Discussion, are clear and would read well if the internal referencing were moved to the Methods and to a supplement. The paper needs a terminology paragraph early, a decision about which material is main text and which is supplementary, and a pass that converts internal provenance into a form an outside reader can follow without opening another file.

## Recommendation posture

Major revision, with the central finding intact and the claim layer needing repair. I want to be clear about the direction of this recommendation, because it is not a rejection of the paper's thesis. The evidence that the analysis choices are not recoverable from the artifact is strong, and the demonstration that the authors themselves could not reconstruct the published values is a more persuasive argument than any of the sensitivity numbers. The order axis and the non-additivity result would make a substantial paper on their own.

What I am asking for is that the paper apply to itself the standard it applies to the source. Three of my Major Concerns, R1-M4, R1-M7 and R1-M11, are cases where the manuscript's account of its own evidence does not match the committed documents it cites. In a manuscript whose argument is that provenance claims must be checkable, these are not presentational matters. R1-M2 and R1-M3 go to the reliability claim, which the paper offers as its constructive contribution in the Discussion, and I do not see how that claim can be retained without either constraining the reported shares or restating them as absolute variances. R1-M5, R1-M6 and R1-M12 require the order dimension to be stated with its conditions and its window, which will make the claim smaller and, in my view, more defensible.

I would want to see a revised version, and I would want the revisions checked against the committed artifacts rather than against the running text, since the running text is what has drifted. If the authors also manage to complete a second-artifact audit, even a partial one, the generalisation paragraph in the Discussion would be transformed, and I would weigh that heavily in favour of publication. As it stands I do not think the paper is publishable in this venue, and I would not want that assessment read as a view that the underlying work is unsound. The work is sound in its measurements and the paper around it is not yet.
