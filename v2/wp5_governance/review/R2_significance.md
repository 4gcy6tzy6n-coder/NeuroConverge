# R2 reviewer report, frozen as returned

**Emphasis brief: significance, originality and venue fit.** **Frozen at round 60; not shown to R1 or R3, and not
edited after comparison.** **The manuscript revision reviewed was the draft at commit `cc99cad`.**

**Headline as delivered: 9 Major Concerns, 4 of them Blocking (R2-M1 single-atlas scope; R2-M2 own-error ledger
as evidence; R2-M3 negative finding with no base rate; R2-M6 reliability estimator unresolved plus an
abstract/body range conflict). Recommendation posture: major revision before any of the three candidate venues
can be chosen, not rejection.**

---

## Overall assessment

This draft is an unusually honest, unusually well-provenanced methodological audit of one derived neuroscience
dataset. Its measurements are traceable, its invalid runs are retained, and it pre-empts several criticisms I
would normally have to raise. What it does not yet do is establish the case its title and abstract advertise.
The title promises an unstated-specification finding about "a derived neuroscience dataset" as a class. The
evidence is one artifact, one atlas, one laboratory, and the authors say so in their own limitations paragraph.
The dimension sizes are real and interesting; the reliability decomposition is the most valuable single result
and also the least settled, because the estimator is admitted unresolved. Two of the paper's load-bearing
evidentiary moves are introspective. One is a failure of the authors' own re-implementation, which is evidence
about the re-implementers unless an independent reconstruction is shown to fail. The other is an absence of
reliability reporting found in fifteen abstract-level readings, offered without any denominator for how often
such reporting occurs. As a contribution I would publish, this is currently a well-executed single-case audit
carrying a field-level claim it has not earned, and a machine-intelligence claim it never tests.

## Who would be interested in the results, and why

Primary. Analysts who download the Randi et al. atlas and its per-pair matrix and fit anything to it. For them
sections 2.1, 2.2 and 2.4 are directly actionable, because the unit, the weighting, the window and the order
are choices they are also making implicitly.

Secondary. The narrower community working on reliability and measurement error in functional connectivity
estimates, who will care about the 17 to 57 per cent measurement-error share and about the attenuation bound in
section 2.6.

Tertiary. Data-provenance and research-software practitioners, who will recognise the defect ledger as an
unusually candid case report and may find it useful as teaching material.

Marginal. The machine-intelligence readership, which the introduction addresses directly. The paper tells that
reader a model inherits a specification silently and that this matters, but it fits no model and reports no
consequence for any learned result, so there is nothing here for that reader to act on beyond a warning.

The paper's own framing does not identify any of these groups. It addresses "a user" and "a model" in the
abstract and discussion, never names the affected community, and never states which of its three possible
theses it is defending. That is a genuine gap and it is the same gap that leaves the venue question open.

## Major strengths

1. The specification ledger is a clean, quantified artefact. Each dimension carries an isolated size and an
   explicit declared-or-not flag, and the inclusion rule that turned out to move the estimate by 0.0000 is
   reported rather than dropped.
2. The non-additivity result in section 2.2 is the sharpest scientific point in the draft. Two normalisations
   summing to -0.0084 producing +0.5706 jointly is a concrete demonstration that a sensitivity table read as a
   budget misleads, and it is the finding most likely to change a reader's practice.
3. The retraction and narrowing table in section 2.8 is exemplary. A paper about provenance that publishes its
   own withdrawn readings, with the reason each fell, sets a standard most of this literature does not meet.
4. The redundancy check on grid axes, and the report that one redundant axis had been added by these authors,
   is exactly the right discipline and is reported against interest.
5. The notation discipline is documented. The census finding that seventy-six fields in five files store a
   z-score under the name d is the kind of defect that silently corrupts meta-analysis downstream, and the line
   caught its own instance of it.

## Major Concerns

### R2-M1, single-atlas scope, Blocking YES

**Axis** Scientific importance and scope of claim.
**Claim pointer** "We show that for one such dataset, a whole-brain functional atlas of Caenorhabditis elegans,
the analysis choices that produced the published per-pair values are not recoverable from the artifact at all,
and that the dimensions they span move the headline estimate by more than the range the original work reports."
**Evidence pointer** Title and Abstract paragraph 1; section 3 "Limitations, stated plainly"; and
`AMENDMENT_constraint_lifted.md` section 3, which records the second-dataset route closed at 1.866 GB with zero
usable files.
**Concern** The title and abstract generalise from one artifact to "a derived neuroscience dataset" as a
category and to reporting practice in a field. The generalisation test was never run, so no dimension in section
2.1, no interaction in section 2.2 and no order effect in section 2.3 has been shown to recur in any second
dataset, even one from the same laboratory and preparation. The manuscript concedes this in the discussion but
the concession is in one paragraph at the end while the general claim is in the title, the abstract and the
introduction.
**Why it matters** A reader cannot tell whether this is a property of this pipeline, of this laboratory's
exports, of calcium-imaging atlases, or of derived datasets generally. The recommended remedy, publish the
specification alongside the matrix, is cheap regardless, but the claim that the practice is generally absent is
exactly the claim the evidence cannot support.
**Resolution test** Either retitle and rewrite the abstract so the claim is scoped to this artifact and this
class of artifact as a demonstrated case, or obtain a second dataset and show at least one dimension and the
order effect recurring or not recurring. A third route is acceptable and cheap. Show that the same undeclared
dimensions are absent from the documentation of two or three further published matrices, even by document
inspection rather than re-analysis.

### R2-M2, the self-error ledger is not evidence about the artifact, Blocking YES

**Axis** Technical soundness and inferential validity.
**Claim pointer** "Six consecutive re-implementations were wrong, each in a different way, and none of the
errors was visible on reading the code"; and "The published pipeline's own authors are its most informed
possible re-implementers, and the specification still had to be recovered line by line."
**Evidence pointer** Section 2.7 and its table; `CORPUS_INDEX.md` section 4, which states that every one of
these defects was found and corrected by this line; `CORPUS_INDEX.md` section 5.
**Concern** The paper offers its own six consecutive implementation errors as its strongest evidence for the
claim that a specification is not recoverable from its output. That is a claim about the artifact, but the
evidence is a record of this team's process. Nothing in the draft shows that an independent competent
re-implementer, with the same access, would fail at the same rate or at all. The line did eventually recover the
specification exactly, by comparing against the code's own intermediate values until they matched at machine
precision, and the corpus confirms the four target values were reproduced exactly. So the artifact WAS
recoverable by this route, and the record shows the obstacle was the re-implementers' distance from the code,
not the artifact's opacity.
**Why it matters** This is the paper's central demonstration, so if it is evidence about the authors rather than
about the artifact, the demonstration does not run. Section 2.8 partly concedes the direction of travel when it
concludes that the failure mode was never the computation but the step from a number to a sentence about the
number. That conclusion is a finding about this line's own error distribution, and the draft presents it as a
finding about derived datasets.
**Resolution test** Report the error record as a case study of a re-implementation process and state explicitly
that it is not evidence about the artifact's recoverability, or obtain an independent re-implementation attempt
with a preregistered stopping rule and report its outcome. A minimal version is to report how long a
re-implementer naive to this corpus needed, given only the artifact and the code, to reproduce one published
number.

### R2-M3, the negative finding has no denominator, Blocking YES

**Axis** Scientific importance and interpretation of a negative result.
**Claim pointer** "What it does not do, as far as we can establish from eleven works read at title-and-abstract
level and four read in full, is report how reliable the functional quantity being predicted is. None of those
fifteen reports a reliability, reproducibility or measurement-error figure for it."
**Evidence pointer** Section 1 and section 3 paragraph 3; `LITERATURE_SURVEY_SPECIFICATION_AND_RELIABILITY.md`
section 1 ("not a systematic sample") and section 6 (the four things that must not be claimed, including "that
the field ignores reliability"); `METHODS_LEVEL_SURVEY.md` section 4.
**Concern** The negative finding is that reliability is unreported. Its importance depends entirely on the base
rate of reporting, which has not been measured. Fifteen works selected by title relevance from 129 citing
records, read at abstract level, with four Methods-level term searches over thirteen terms, cannot distinguish
a field-wide reporting gap from fifteen individual omissions. The supporting documents themselves forbid the
inference, and the manuscript's own phrasing ("as far as we can establish") signals that the authors know it.
**Why it matters** If ten per cent of this literature omits a reliability figure, an audit of one artifact is a
serviceable anecdote. If eighty per cent do, the same audit is a significant finding. The paper's persuasive
force is entirely a function of a number it does not report.
**Resolution test** Report a denominator. A prespecified sample of the citing literature, coded for whether a
reliability, reproducibility or measurement-error figure for the predicted functional quantity is present,
with an explicit search protocol and a statement of the reporting rate. Until that exists, the negative finding
must be stated as a description of fifteen readings rather than as a property of the literature.

### R2-M4, the principle is not new and the prior literature is not cited, Blocking NO

**Axis** Originality.
**Concern** The thesis that a value must travel with the analysis choices that produced it is long established in
work on data documentation, reproducibility and analytic provenance. The manuscript neither cites that
literature nor distinguishes its contribution from it. What is genuinely new here is the measurement.
**Resolution test** Rewrite the abstract and the first paragraph of section 3 to locate the contribution in the
quantification, and add the relevant prior work on provenance and documentation practice.

### R2-M5, the reliability range disagrees between the abstract and the body, Blocking NO

**Axis** Technical consistency of the headline evidence.
**Claim pointer** "within-cell measurement error accounts for 37 to 57 per cent of the variance in a pair's
response depending on the specification".

**NOTE ADDED AT FREEZING, NOT BY THE REVIEWER.** **This defect is real and was found independently in the same
round by a consistency sweep run while this review was in flight; it is fixed in commit `0adbb5b`, which
postdates the `cc99cad` revision this reviewer saw.** **The convergence is recorded here because it is the
strongest evidence this self-review produced: two routes, one of them an isolated reviewer, arrived at the same
defect without contact.**

**Concern** The abstract's lower bound of 37 per cent does not match the body's lower bound of 17 per cent, and
the corpus index records 17 per cent as the live range. Both 37.5 and 57 are attested as specification-specific
values, so the abstract appears to have taken the point estimate as its floor.
**Why it matters** This is the paper's second headline number and the one most likely to be quoted. A range
whose lower bound differs between the abstract and the body is exactly the defect the paper is about.
**Resolution test** State one range, the specification index that defines it, and the single-specification value
separately.

### R2-M6, the reliability estimator is unresolved where it is used, Blocking YES

**Axis** Technical soundness of the central reliability claim.
**Claim pointer** "The pair-specific animal component is not robust in the same way: it ranges from 5.5 to 46.0
per cent depending on a minimum-measurements-per-pair restriction, and at the unrestricted specification it
goes NEGATIVE, an impossible value for a variance share."
**Concern** The variance decomposition is the source of the paper's reliability numbers, and it is admitted to
be unresolved. A four-component decomposition that returns a negative variance share at its unrestricted
specification is not identified at that specification. The paper's response is to interpret the negativity as
evidence that the specification is ill posed, which is defensible as an observation but is not a validation of
the estimator at the specifications where it is retained.
**Resolution test** Report a simulation or split-half validation of the decomposition under a known truth, or
restrict the claim to the sign structure and the ordering of the components, which the paper itself says is what
is robust. Alternatively, predeclare the restriction, justify it independently of the result, and report the
decomposition as conditional on it throughout, including in the abstract.

### R2-M7, the largest dimension depends on one window, Blocking NO

**Axis** Framing and scope of the largest reported dimension.
**Concern** The headline dimension is a comparison between a specification the pipeline uses and one it does not,
measured at a single window where the two diverge and reported as the largest of seven. At the 12-volume window
the same comparison contributes 0.0234, roughly a fifteenth of the 24-volume value. The comparison turns on a
choice the paper concedes users may never face in this form.
**Resolution test** Move the constructed-specification caveat into the abstract, report the order effect with the
window it depends on rather than as a single ranking, and state whether the 24-volume divergence has a mechanism.

### R2-M8, the machine-intelligence consequence is asserted and never demonstrated, Blocking NO

**Axis** Interdisciplinary readership and machine-intelligence relevance.
**Concern** The paper opens with the consequence for learned models and returns to it in the discussion, but no
model is fitted and no consequence for any learned result is measured. The claim is asserted in the register of
a result three times and demonstrated zero times.
**Why it matters** This is the crux of the venue question.
**Resolution test** Either demonstrate the downstream consequence, for example by fitting a simple model or a
standard analysis to the matrix under two defensible specifications and reporting how the result moves, or drop
the learned-model framing to a single sentence and reposition the contribution as an audit.

### R2-M9, the defect ledger is not enumerable from the manuscript, Blocking NO

**Axis** Readability for nonspecialists and integrity of the claim structure.
**Claim pointer** "The count of such events is seventeen numbered defects, listed in section 2.7 and in Figure 6."
**Concern** The abstract asserts that all seventeen defects are each named by a document, the corpus index says
the first four are not, and section 2.8 says the seventeen are listed in section 2.7, whose table contains six
rows and an entirely different numbering. A reader cannot reconstruct the ledger from the manuscript.
**Resolution test** Enumerate the seventeen defects in the manuscript or in a supplementary table with their own
IDs, reconcile the round numbers in the section 2.7 table against the defect numbering, and correct the
abstract's claim.

## Minor Comments

### R2-m1, the order dimension is not varied alone
**Affected element** Abstract paragraph 2. **Issue** The abstract's uniform phrasing ("each by varying it alone
and holding the others fixed") overstates the uniformity of the design, since the order dimension couples two
normalisations and is reported as a function of window. **Required correction** Say in the abstract that six
dimensions were varied in isolation and the order dimension was measured jointly with the window.

### R2-m2, "the three largest are stated nowhere"
**Affected element** Section 2.1 final sentence. **Issue** Supported for the two normalisation dimensions but
only partly for the order dimension, which is not a level of a declared parameter but a feature of how two
undeclared ones are sequenced. **Required correction** Reword to state that the three largest contributions come
from dimensions the artifact does not declare, and note that one of the three is partly a constructed
comparison.

### R2-m3, two quantities near 0.34, and a superseded figure in the corpus index
**Affected element** Section 2.1 table, the precision-weighting row (0.3356) and the cell-pool row (0.0038), and
Figure 1. **Issue** Two distinct quantities are both approximately 0.34, and the corpus itself carries a
correction in which one was mistaken for the other. A reader cannot tell from the manuscript which value belongs
to which axis, and `CORPUS_INDEX.md` section 6 item 4c still asserts the superseded figure. **Required
correction** State in the section 2.1 caption and the Figure 1 legend which source artifact fixes each row, and
state that the cell-pool axis was separately tested and contributed 0.0038.

### R2-m4, the 0.5 reliability threshold is unsourced
**Affected element** Section 2.6. **Issue** The 0.5 threshold is asserted without a source or a rationale.
**Required correction** Cite the convention or state that 0.5 is used only as a descriptive reference point.

### R2-m5, no sample sizes in the abstract
**Affected element** Abstract paragraph 4 and section 2.6. **Issue** The abstract reports no sample sizes, so the
reliability range reads as a property of the atlas rather than a measurement over specific units. **Required
correction** Add the unit counts and the number of specifications to the abstract's reliability sentence.

### R2-m6, the Communications Biology entry is unresolved
**Affected element** Section 6 entry 6. **Issue** A published claim is anchored to a reference with no DOI and no
author list, and this is the reference carrying the paper's one framing-tension paragraph. **Required
correction** Resolve the entry to a full record before submission.

### R2-m7, the licence position is by reference only
**Affected element** Section 4, Data. **Issue** The manuscript does not state the licence position on its external
input or the redistribution position on the derived records, and it points the reader to a path inside the
repository rather than reporting the fact. **Required correction** State the licence of each external input and
whether any derived record can be redistributed, in the manuscript.

### R2-m8, notation relaxed in the abstract
**Affected element** Abstract paragraph 2. **Issue** The abstract reports d values without the subscripted form
the Methods uses deliberately. **Required correction** Use the subscripted notation consistently.

### R2-m9, the 109-animal denominator is unexplained
**Affected element** Section 2.5 against section 4. **Issue** The animal count used for the unit-error arithmetic
differs from the export count (113 and 18) and the reason is not given. **Required correction** State why 109 and
which animals are excluded.

### R2-m10, the round-34 table row may be misread as the source's published figure
**Affected element** Section 2.7 table. **Issue** "against 0.7289" is this line's reproduction of the pipeline's
configuration, not a number the published paper reports. **Required correction** Label the reference values as
this line's reproduction.

## Technical failings that need to be addressed before the case is established

R2-M1, R2-M2, R2-M3, R2-M6 (blocking) and R2-M5, R2-M9 (non-blocking but integrity-relevant). The two items
named as owed in `CORPUS_INDEX.md` section 7, an independent reviewer and the owner's venue decision, are
external to this review and are recorded as outstanding.

## Assessment against Nature-style criteria

**Originality.** Low on principle, moderate on measurement. The proposal that analysis choices should travel
with derived values is established in the data-documentation and reproducibility literature, which the
manuscript does not cite. **Scientific importance.** Moderate and local. **Interdisciplinary readership.**
Currently not met; the learned-model consequence is asserted and never measured. **Technical soundness.** Mixed
but above average in transparency and below average in closure. **Readability for nonspecialists.** Reasonable
in the abstract and discussion, weaker in Results; the private identifier vocabulary and the density of
self-referential correction talk will slow a general reader.

## Recommendation posture

Major revision before the venue question can be answered, not rejection. Three actions would change the posture:
scope the title and abstract to the artifact and state the general claim as a hypothesis; settle the reliability
estimator or restrict the claim to the sign structure; then choose the venue, because the choice changes which
of the three papers in this draft is being submitted. If the venue is a methods or data journal and the audit
procedure is the claim, the machine-intelligence framing in section 1 can be cut and the paper is close to
defensible. If the venue is NMI, the learned-model consequence has to be demonstrated rather than asserted, and
on this evidence that is new work rather than revision.
