# Independent methods review: reportability amendment and bound instruments

Date: 2026-10-24 (dispatched under `BINDING_RECORD_V3_20261024.md`, gate 3)

Reviewer: isolated-context methods reviewer, first contact with this repository.

## 0. Independence and disclosure

- This review was produced by an **AI reviewer in an isolated context**. The reviewer had no prior
  contact with the project, its code, its corpus, or its authors' decisions. A human methods
  reviewer can supersede it; if one does, record the supersession dated, as with the other
  isolated-context records in this lane.
- This is a **methods review only**. It does not judge software correctness of the scorer; separate
  instrument reviews (`REPORTABILITY_V3_INDEPENDENT_REVIEW_20261023.md` and the defect reviews) own
  that. Where this review touches the scorer, it touches only what the protocol text requires of it.
- Materials read in full: the five review targets named below. Bounded supporting reads, listed for
  transparency: `README.md` (repo and `field_audit/`), `OWNER_DISPOSITION_20261020_ARXIV_QUERY_ORDER.md`
  (scope framing for question E), the header row of
  `REPORTABILITY_CODING_TEMPLATE_v1_2026-10-20.csv`, and keyword searches of
  `CODING_INSTRUCTIONS_FROZEN.md` and `CODING_OPERATIONS_SUPPLEMENT_20261023.md` (to check whether
  coder-side conventions already cover identified ambiguities). **No coding sheets, no coding
  results, no corpus full texts were read.** SHA-256 values were computed without reading file
  contents beyond the documents already read.

## 1. Materials reviewed

| document | role | digest verified |
| --- | --- | --- |
| `OWNER_AMENDMENT_REPORTABILITY_2026-10-20.md` | the owner-approved amendment under review | not hash-bound externally |
| `PROPOSED_REPORTABILITY_PROTOCOL_AMENDMENT_CANDIDATE_2026-10-19.md` | adopted operational rules (Sections 5-7) | matches amendment binding `84390e03...` |
| `REPORTABILITY_CHECKLIST_v1_2026-10-20.md` | frozen 11-item map | matches amendment binding `4f996389...` |
| `REPORTABILITY_CODING_TEMPLATE_v2_SOURCE_REGISTRY_CANDIDATE_2026-10-20.csv` | 15-field bound row schema (header-only file) | matches binding-record B3 `77dcda1a...` |
| `BINDING_RECORD_V3_20261024.md` | v3 scorer binding, schema supersession, gate moves | not hash-bound externally |
| `AUDIT_PREREGISTRATION_v1_FROZEN.md` sections 2, 4, 5 (read in full for context) | unchanged E0-E4 / T1-T5 / coding definitions | n/a |

Hash-chain check (supporting, not a software review): every digest recorded in the 2026-10-20
amendment's materials table and in `BINDING_RECORD_V3_20261024.md` reproduces on the current tree,
including the superseded v1 materials retained as history. No drift found anywhere in the chain.
Positive finding: the amendment's table is accurate as history; the instruments of record are the
v3 scorer and the 15-field v2 schema per the binding record.

## 2. Overall verdict

**ACCEPT-WITH-CONDITIONS.**

Reason: the amendment is internally self-consistent and free of circularity; the four-status system
is operable on every (transition, item) cell with no legal dead-end found; the dual-coding and
adjudication rules are fail-closed and recomputable by a third party from raw rows alone; and the
interpretation boundary is stated honestly at the corpus level. One **major** defect remains: the
prohibition on total scores does not explicitly close the per-claim and cross-item aggregation
channel, through which a total score can return under an alias. Three conditions below are cheap,
pre-coding, dated-note-level fixes; none changes a frozen definition. Coding should not begin
until they are recorded.

Severity classes used: blocker / major / minor / observation.

## 3. Findings by review question

### A. Internal consistency of the amendment

**No contradiction or circularity found.** Checked mappings:

- The five adopted requirements map one-to-one onto the candidate's Sections 5/6/7 additions:
  req 2 (statuses, pointer/hash/locator, item-permitted citation, non-silence) equals the candidate's
  Section 5 rules; req 3 (two independent rows per cell, exactly one adjudication iff labels differ,
  refusal rules, raw disagreement) equals the candidate's cardinality text; req 4 equals the
  candidate's Section 6 outputs including the no-total-score rule; req 5 equals the candidate's
  Section 7 freeze-and-verify requirement.
- The amendment's scope statement (amends Sections 5-7; Sections 2-4 and existing Section 6 outputs
  unchanged; descriptive audit; no prevalence or classifier claims) is consistent with the
  candidate's "Amendment boundary" section and with the frozen preregistration sections 2, 4, 5,
  which the amendment does not touch.
- The removal of the Section 7 confusion-table gate is internally consistent with the candidate's
  replacement Section 7, and the permitted descriptive cross-tab is not re-imported as a threshold
  anywhere in these documents.
- The candidate's 12-test note matches the amendment's "12 synthetic tests" statement; the test-count
  history (11 then 12) is dated and explained inside the candidate.

Findings:

- **A-2 (minor) The amendment's bound-instruments table is superseded.** The governing amendment
  binds the v1 scorer and the 13-field v1 template; `BINDING_RECORD_V3_20261024.md` B1-B3 supersedes
  both with the v3 scorer and the 15-field v2 schema, recording itself as a dated amendment to this
  amendment. The chain is documented and hash-verified, but the amendment read alone gives wrong
  operational pointers (req 1 names the v1 row schema). The candidate's Section 5 text also still
  shows the 13-field list; the two added fields (`source_role`, `source_id`) implement, in structured
  form, auditability requirements the candidate itself states ("registered cited-source ID"), so the
  substance is consistent even though the schemas differ between documents. Residual risk is
  mis-citation by a future reader who finds the amendment but not the binding record.
- **A-4 (minor) Gate 4 wording versus execution.** The amendment's gate list requires instrument
  review "with findings fixed and re-reviewed before any corpus coding". The binding record B4
  records finding F-2 as a known defect deliberately **not** fixed (fail-closed, error fidelity
  only), with owner approval. The deviation is dated, visible, and approved, but it does not match
  the gate's own wording. This is a wording-level inconsistency between two dated records, resolved
  by the later owner decision, not a concealed defect.
- **A-5 (observation)** The amendment bound a v1 scorer that same-day instrument review found
  blocking. This is internally consistent only because the amendment simultaneously gated coding on
  defect review; the design (freeze before coding, not freeze at amendment) is what makes the later
  re-binding chain legitimate. Worth stating explicitly so the pattern is not read as an error.

### B. Item-level reportability read separately from E0-E4; alias loopholes

The core constraint is stated consistently in three places (amendment req 4, candidate Section 6,
checklist v1): item-level counts only; no weighted or unweighted overall reportability score; any
reportability-by-E-grade table is descriptive context only; the scope-match verdict may not enter a
reportability score or validation cross-tab. The E-grade side keeps its frozen Section 6 outputs and
its own read mode. The two-table architecture is clearly constrained at its center.

Findings:

- **B-2 (major) Per-claim and cross-item aggregation is not explicitly closed.** "Do not calculate
  a weighted or unweighted overall reportability score" and "do not collapse items into a weighted
  or unweighted overall score" most naturally prohibit corpus-level roll-ups. Nothing in the
  adopted text prohibits: a per-claim count of complete items ("claim C028 complete on 9 of 11
  items"); a mean of per-item complete proportions ("mean item completion"); or a threshold
  classification on such counts ("well-reported: at least 9 of 11"). Each is a total score under an
  alias, each enables ranking claims, and the last re-creates the classifier construct the amendment
  just removed. The Section 6 addition enumerates only per-item outputs but never says "and no other
  aggregation". This is the one genuine loophole found; it is a reporting-time hazard, not a scorer
  defect (the instrument computes itemwise summaries only). Fix is COND-1.
- **B-4 (minor) The permitted cross-tab has no pre-specified caveat text.** The amendment permits a
  reportability-by-E-grade table "only as a labeled descriptive cross-tab", which is a good textual
  rule, but no required caveat is pre-written, and the table is structurally coupled to the E-grade
  axis (see E-3): without a standing caveat, a reader can treat an apparent association as
  validation. Fix is COND-2.
- **B-5 (observation)** The "complete" numerator (REPORTED plus item-permitted REFERENCED) is
  coherent: for 10 of 11 items REFERENCED is impermissible, so complete = REPORTED there; only T1-03
  can add REFERENCED. The two denominators (complete-rate denominator: all sampled claims;
  disagreement denominator: claims with two valid rows) coincide in any admissible dataset because
  summaries are refused on any grid hole. Redundant but defensively correct.

### C. Four-status operability across T1-T5; REFERENCED restricted to T1-03

**No legal dead-end found.** The four statuses partition the presence-of-required-information axis
(none / some / all) with REFERENCED as a T1-03-only alternative route to complete, and assertion-
without-reporting is explicitly NOT_REPORTED. For every (transition, item) cell at least one status
is truthfully applicable, including the hard cells:

- T3-01 / T4-02 (comparison not run; scale sensitivity absent): the item wording's "state that
  explicitly" clause plus the non-silence rule make explicit absence REPORTED and silence
  NOT_REPORTED. Coherent.
- T4-01 with a paper naming no other task families: NOT_REPORTED with a recorded search rule.
- T5-01 for a claim whose basis is entirely external (no in-paper result, figure, or table):
  citation is not permitted for T5-01, so the cell is PARTIAL (link present but not in-paper) or
  NOT_REPORTED. Legal, though it systematically scores external-evidence claims incomplete (see E-3).
- T2-02 where the paper never describes the biological mechanism: NOT_REPORTED; the failure is
  derivative of a T1-01/T1-02 failure (items are deliberately non-independent; T3-02 similarly
  presupposes T3-01's "those comparison controls").

Findings:

- **C-1 (minor) Blanket-versus-enumerated absence is ambiguous.** At T4-01 ("Name task families
  beyond the demonstrated task as tested or untested") a blanket statement "no other task families
  were tested" names zero families but explicitly marks the remainder untested: under the non-silence
  rule that reads as REPORTED, under the item's "name" verb it reads as PARTIAL. The same tension
  exists at T2-02 ("List departures...") for a paper that says only "our model drastically simplifies
  the mechanism" without listing anything. Both cells have defensible answers, so no coder is stuck,
  but two honest coders can systematically diverge; unresolved, this becomes adjudication load and
  inflates the disagreement statistic. Fix is COND-3.
- **C-2 (minor) T1-03 REFERENCED depends on pinning reach, not only on author reporting.**
  REFERENCED requires the cited source pinned by version and hash with the relied-upon information
  locatable in it. Two consequences. (i) An unpinnable citation (book, paywalled legacy journal,
  dataset) makes REFERENCED unavailable; the legal fallback is PARTIAL under its "not inspectable"
  limb with the missing element named. No dead-end, but the T1-03 complete-rate then partially
  measures the audit's own pinning capability rather than the paper's reporting, and no document
  states this interpretive consequence (see R3). (ii) Chain citation: the target cites A, and A's
  evidence is its citation of B. REFERENCED must bind the source the target identifies (A); B is not
  identified by the target, so scoring against B is not available and the cell falls back to PARTIAL.
  This resolution follows from the rules but is not written down; two coders could resolve it
  differently. Fix is COND-3.
- **C-3 (observation)** The T1-03-only REFERENCED permission is not marked in the checklist or the
  template but is derivable from the item wording ("Present **or cite**...") and is stated outright
  in `CODING_OPERATIONS_SUPPLEMENT_20261023.md` ("REFERENCED is allowed only for T1-03"), so coders
  are not left to infer it. No defect; noted so the convention's location is on record.

### D. Dual-coding and adjudication closure; recomputability

**The machinery is closed and recomputable.** From the raw rows alone a third party can recompute
every declared output: cell cardinality (exactly one row per named coder per
(claim, transition, item)); the iff-rule for ADJUDICATED rows (present exactly when the two status
labels differ; forbidden when they agree); the post-adjudication value (common label when agreeing,
adjudicated label when not); the refusal conditions (missing/duplicate rows, unresolved
disagreement, invalid adjudication row); per-item counts by coder and post-adjudication; and the
exact-label disagreement numerator and denominator. Every refusal condition is objective. This is
fail-closed by construction.

On the specific question -- an adjudication label that differs from **both** coder labels:

- **D-2 (minor) Covered as a value rule, not covered as a reported fact.** The rules do not
  constrain the adjudicated status to the coder pair; a third label is legal and "its status is the
  post-adjudication value" remains well-defined, and recomputability survives (the auditor sees all
  three labels). But no output is required to surface how often the adjudicator overrode both
  coders, which is exactly the quantity an auditor of the adjudication process would want. See R1.
- **D-3 (minor) Adjudicator identity and eligibility are unconstrained.** The schema records who
  adjudicated, when, why, and against what source, but the adopted text never says who may
  adjudicate (a third coder, one of the two, the owner, another AI instance). If one of the two
  coders adjudicates their own disagreement, the post-adjudication value inherits that coder's
  influence; acceptable if visible, but the role should be named rather than left to practice. See R1.
- **D-4 (minor) The two P4 coder instances are the same model.** `BINDING_RECORD_V3_20261024.md`
  records P4 as two isolated-context coder instances of the same model, satisfying the frozen
  "at least one not an author of any workspace code" literally, with a committed same-model
  disclosure. The consequence for this amendment's outputs: the reportability disagreement statistic
  measures same-model instance/context agreement, not inter-rater reliability between independent
  humans; correlated errors are expected and a high agreement rate is weaker evidence than it would
  be for two human coders. The disclosure handles honesty; the output labels should carry it too.
  Related: the frozen Section 5 ten percent QC re-check by a non-coding reviewer was written for the
  E-grade sheet; the reportability table does not extend it to its own rows. See R2.
- **D-5 (observation)** When two coders agree on a label but cite different locators, there is no
  status disagreement and no rule harmonizes the locators; both rows are preserved. Acceptable for
  count outputs; the divergence remains inspectable in raw rows.

### E. Conclusion boundary under the owner's narrowed scope

The boundary is **stated honestly at the level claimed**. The amendment (descriptive only; no
prevalence, no evidence-quality, no checklist-validity, no causal, no population claims) composes
correctly with `OWNER_DISPOSITION_20261020_ARXIV_QUERY_ORDER.md` (18 records, all from the first
query term `brain-inspired`, 18 being the cap-constrained maximum, candidate sample until
adjudication, "Do not relabel this as a cross-query or representative sample", replacements paused
if they would broaden scope). The correct joint reading -- item-level counts describe the eligible,
coded subset of the frozen 18 records, hypothesis-generation only -- is derivable from the two
documents together.

Findings:

- **E-3 (minor) The permitted cross-tab is structurally coupled to the E-grade axis, and no
  document says so.** T5-01 demands an in-paper result, figure, or table, while E3/E4 grades credit
  external evidence: external-evidence claims cannot be complete on T5-01 by construction. T1-03 is
  the only item with a complete-via-citation route, mirroring the E3 axis from the other side. Any
  apparent reportability-by-grade association therefore partly reflects construct coupling, not a
  field phenomenon. At n around 13-15 the cross-tab's cells are mostly 0-3 counts. Both facts belong
  in the standing caveat required by COND-2.
- **E-4 (minor) Presentation precision and the denominator's operational definition.** Per-item
  proportions on roughly 14 claims carry wide uncertainty; percentage-only displays imply spurious
  precision. Also, "divided by all sampled claims" needs an operational referent under the
  replacement rule: replacements within the narrowed scope change membership, so the denominator
  should be the final frozen coded claim list, cited by its dated version. See R4.

## 4. Conditions (record before coding begins; dated owner-visible notes; no frozen definition changes)

- **COND-1 (closes B-2, major).** Record a dated clarification extending the no-aggregation rule
  explicitly to: per-claim item totals or counts; cross-item means, indices, or weighted
  combinations; and thresholds or classifications applied to such counts. State that per-item
  outputs, the labeled descriptive cross-tab, and the raw rows are the only permitted aggregations.
- **COND-2 (closes B-4 and E-3).** Pre-write the caveat that must accompany any
  reportability-by-E-grade cross-tab: descriptive only; the sample size and its first-query,
  non-representative provenance; the structural coupling described in E-3; and no test statistics,
  significance values, or accuracy-like numbers derived from it.
- **COND-3 (closes C-1 and C-2).** Record the coder conventions before any paper is scored:
  (a) blanket-absence statements at T4-01 and T2-02 -- state whether a blanket "no other task
  families tested" / "drastic simplification" statement counts as REPORTED (explicit absence) or
  PARTIAL (required enumeration missing), and apply one rule; (b) T1-03 chain citations resolve to
  PARTIAL with the missing element named, never to REFERENCED against a second-order source;
  (c) T1-03 unpinnable cited sources resolve to PARTIAL under the "not inspectable" limb with the
  missing element named. Agreed after coding starts, these would be post-hoc scoring changes.

## 5. Recommendations (non-blocking)

- **R1 (D-2, D-3).** Add one line to the outputs: the count of adjudications whose label matched
  neither coder. Name the adjudicator role and its eligibility (not one of the two coders, or record
  when it is).
- **R2 (D-4).** Label the disagreement statistic as same-model instance agreement wherever it is
  reported, and either extend the frozen ten percent QC re-check to a sample of reportability rows
  (including adjudicated ones) or record why it is not extended.
- **R3 (C-2).** When reporting T1-03, break the non-complete rows down by reason, separating
  PARTIAL-because-unpinnable-citation from other causes, or state the pinning-reach limitation in
  prose.
- **R4 (E-4).** Report per-item results as raw counts and exact fractions with explicit
  denominators; avoid percentage-only displays at this n. Define "all sampled claims" operationally
  as the final frozen coded claim list, cited by dated version.
- **R5 (A-2).** Wherever the 2026-10-20 amendment is cited as governing, cite
  `BINDING_RECORD_V3_20261024.md` with it, so no reader uses the superseded v1 bindings.
- **R6 (A-4).** In future gate wording, distinguish "findings fixed and re-reviewed" from "finding
  recorded as a known non-blocking defect with owner acceptance", so an approved B4-style deviation
  is not a wording mismatch.

## 6. What this review did not do

- No software-correctness assessment of any scorer; that belongs to the instrument reviews of record.
- No reading of coding sheets, coder outputs, results summaries, corpus full texts, or eligibility
  adjudications; conclusions about those stages rest on the documents cited above only.
- No claim that the instrument system is free of unknown defects. The strongest claim supported here
  is: within the reviewed scope, no blocking or major defect remains other than B-2, which COND-1
  closes at the note level.

## 7. Verdict restated

**ACCEPT-WITH-CONDITIONS.** The amended reportability protocol and its bound instrument group are
methodologically sound for the descriptive, item-level purpose the amendment declares, provided
COND-1 through COND-3 are recorded as dated notes before coding begins. This acceptance closes the
"independent methods review" gate of the 2026-10-20 amendment as executed in
`BINDING_RECORD_V3_20261024.md` item 3; it does not by itself start coding, which remains gated on
item 1 (full-text eligibility second review) per that record.
