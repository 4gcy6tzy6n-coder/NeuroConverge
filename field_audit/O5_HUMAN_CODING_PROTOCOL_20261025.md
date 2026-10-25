# O-5 human coding protocol (H1/H2/H3) - frozen 2026-10-25, approved by the advisor's round-3 ruling

Authority: the advisor's round-3 ruling (appended in `ADVISOR_REVIEW_20261025.md`) approved the
three-stage human-coding design and its acceptance criteria. This record freezes the operational
protocol BEFORE any human coder is staffed, so that arrival-to-work requires no in-the-moment
decisions. Declaring documents are unedited.

## Binding requirements (from the ruling, restated as rules)

1. **Blindness.** The human coder works only from the packet (section below): frozen instructions,
   pinned full texts, empty sheets. They never see any AI grade, any merged sheet, any adjudication
   record, any result, or this protocol's analysis sections. The packet directory physically
   contains none of these.
2. **The question.** H3 answers: **does the T2/T3 evidence asymmetry survive independent human
   judgment?** Agreement with AI coding is reported evidence, not the pass criterion. Human coding
   may change main conclusions; it is not a ratification exercise.

## H1 - primary corpus, full blind pass

- Scope: all 16 primary-corpus claims x T1-T5 (80 cells) + one headline transition per claim
  (16 rows). Nothing less.
- Materials: `pinned_fulltext_20261020/` texts (hashes in the pilot manifest), the frozen
  instructions `CODING_INSTRUCTIONS_FROZEN.md` VERBATIM, sheets `CODING_sheets_human/coder_H.csv`
  and `headline_H.csv` (header-only stubs provided).
- Acceptance: 80 cells + 16 headline rows complete, each justification quoting or citing a pinned
  location; sheet passes the mechanical integrity check (row counts, claim-set equality, grade
  vocabulary, T5-only scope_match, provenance hash match).

## H2 - validation corpus, frozen priority scope

- Scope (frozen): all 42 validation claims x {T2, T3, T5} = 126 cells, plus headline rows where
  the coder judges the abstract claim to rest on T2/T3/T5 (42 rows, one per claim, as in the AI
  round). Rationale recorded now: on T2/T3/T5 the two AI coders disputed at least one cell in 32
  claims and fully agreed on exactly 10 claims - the 10 agreed claims (`1505.07814v2`,
  `1909.11145v2`, `1702.05596v1`, `1910.03913v1`, `2210.16530v1`, `2201.02262v1`, `2010.12197v3`,
  `2503.11299v8`, `2503.03084v1`, `2406.15488v1` - complete enumeration of the agreement stratum,
  verified against the committed coder sheets, not a sample) travel as the EMBEDDED NON-DISPUTED
  CONTROL LAYER; no sampling discretion exists.
- Optional extension (coder's choice, recorded): T1/T4 cells on claims where the coder's T2/T3/T5
  grades will have been flagged in H3 (the coder is not told which those are in advance; the
  extension is offered after H1+H2 submission if the lead needs it, with the same blindness).
- Materials: `pinned_validation_20261025/texts/` + `FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv`
  (text_sha256 column), same frozen instructions, same sheets.
- Acceptance: 126 cells complete with justifications; integrity check passes.

## H3 - recomputation, disagreement audit, and the asymmetry question (analysis spec, frozen now)

Computed by `compute_human_reading_20261025.py` (prepared; refuses to run until H1 sheets exist;
selftested on synthetic grades). Three readings, ALL reported, in this order:

1. **Raw human reading (primary).** Coder H's grades alone, no adjudication, no merging with AI:
   per-transition grade distributions on H1 (n=16); the T2/T3 asymmetry contrast (T3 E2 share vs
   T2 E2 share, both corpora where covered); headline shares using H's own headline map; T1 E0
   count. This is the independence test: the asymmetry must hold direction-identically here for
   the finding to be called human-confirmed.
2. **Superseded reading.** Per the frozen human-supersedure rule, human grades REPLACE AI grades
   for every covered cell; corpus-level statistics recomputed on the union (H1 full; H2 cells on
   T2/T3/T5, with the uncovered T1/T4 cells carrying the AI-merged grades and the coverage
   fraction disclosed in the same sentence as any number so produced).
3. **Disagreement audit.** Raw per-cell agreement of H with coder A, with coder B, and with the
   AI weaker-merge; grade-transition matrix (AI merged grade -> H grade) for T2, T3, T5; the
   AI-disputed cells' H outcomes (does H side with A, with B, with neither?); and, where H and the
   AI merge disagree, a lead adjudication record per cell under the same weaker-grade rule, with
   the matched-neither count - the post-adjudication reading is computed and reported BESIDE the
   raw reading, never instead of it.

Pass/fail framing (recorded now, before any human grade exists): the O-5 gate CLOSES when H1+H2
are complete and H3 is reported. The gate's scientific question - asymmetry survival - is answered
by reading 1; any outcome is a reportable result, and a failed replication reopens the manuscript's
main conclusions (per the advisor: human coding may change them).

## Human coder packet (contents; nothing else enters it)

- `CODING_PACKET_HUMAN_20261025.md` (coder-facing README: what to do, in what order, output
  discipline, how to ask questions without breaking blindness).
- `CODING_INSTRUCTIONS_FROZEN.md` (verbatim).
- Pinned text directories + hash manifests for both corpora.
- Empty sheets: `CODING_sheets_human/coder_H.csv`, `CODING_sheets_human/headline_H.csv`
  (header-only stubs, committed now).
- NOT in the packet: any coder_A/coder_B/merged file, any statistics JSON, any record in this
  repository's analysis sections, the probe materials, the robustness analyses.

## Status

H1/H2/H3 protocol frozen; packet staged; H3 instrument prepared and selftested. Gate O-5 remains
BLOCKED on one thing only: a named human coder.

## Amendment (2026-10-25, same day): coder staffing resolved by delegation

The lead has recruited an external researcher as coder H; the lead will NOT code (an earlier
consideration of the lead coding personally is superseded - the lead is result-aware at the
aggregate level, which would have forced a disclosed-limitation reading; delegation preserves
the blindness rule intact). The transmission vehicle is `O5_CODER_ASSIGNMENT_20261025.md`,
which is blindness-safe by construction (no results, no distributions, no expectations, no
disagreement statistics; the T2/T3 asymmetry is nowhere stated in coder-facing material).
Packet completeness verified before handover: all 16 primary PDFs present in
`pinned_fulltext_20261020/pdfs/` (including adjudication replacements C036/1903.12517v1 and
C077/1811.09699v1), all 42 validation text layers present in `pinned_validation_20261025/texts/`.
Handover rule for the lead: copy the packet file list below into a clean folder for the coder;
do not hand over the repository; do not discuss findings with the coder until H1+H2 sheets are
complete and the integrity check has run.

Packet file list (the ONLY items the coder receives):

1. `CODING_PACKET_HUMAN_20261025.md` (README)
2. `CODING_INSTRUCTIONS_FROZEN.md`
3. `pinned_fulltext_20261020/pdfs/` + `pinned_fulltext_20261020/FULLTEXT_DOWNLOAD_MANIFEST_20261020.csv`
4. `pinned_validation_20261025/texts/` + `pinned_validation_20261025/FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv`
5. Empty sheets `CODING_sheets_human/coder_H.csv`, `CODING_sheets_human/headline_H.csv`
6. `O5_CODER_ASSIGNMENT_20261025.md` (this amendment's companion task document)

## Status update (2026-10-25, latest): gate CLOSED by completion

Coder H = Researcher Yang (human-primary, AI-assisted construction, final judgments by Yang -
the lead's relayed answer recorded verbatim in `O5_H3_RESULTS_20261025.md` section 7). H1+H2
delivered, verified (206+58 rows; provenance established), H3 computed including the advisor's
required raw-vs-handled pair. The gate closes on the human-primary ruling, pending advisor
confirmation. The protocol's blindness rule was satisfied in the form that matters for
independence: the coder worked from the packet without repo access, and the measured signature
(40 percent disagreement with the AI merge, 36.2 percent matched-neither on disputed cells,
divergence against the project's own narrative) is that of genuine independent judgment.
