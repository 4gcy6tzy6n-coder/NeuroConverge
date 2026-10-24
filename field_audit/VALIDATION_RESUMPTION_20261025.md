# P0-3 validation corpus resumption record (dated amendment; declaring documents untouched)

Date: 2026-10-25. Executed by the lead under the standing full-decision-rights grant (2026-10-19).

## 1. Authorization

`RECONCILIATION_20261023.md` recorded the 60-claim validation corpus (drawn 2026-10-23, commit
`144c41e`, rule frozen in `VALIDATION_CORPUS_RULE_20261023.md`) as PAUSED / OUT OF SCOPE pending
fresh owner authorization. That authorization is now given: on 2026-10-25 the owner, on the
lead's gap assessment ("闭合第 1、2 项后，这就是一篇真正的 NMI Article"), instructed
"按照你说的开始", where item 2 of the stated next actions was lifting the P0-3 pause and
re-freezing it as a formal version. The declaring documents are not edited; this record is the
receiving amendment.

## 2. Scope reconciliation (the query-order boundary)

The owner's 2026-10-20 ruling was RETAIN-and-NARROW: first-query scope only, no successor draw.
The validation draw (frozen rule) used the SAME pinned snapshot
(`corpus_draw_arxiv_v1.snapshot.jsonl`, sha256 `e73f72f5...`) with no new fetches. The resumption
therefore crosses no query boundary, PROVIDED every adjudicated candidate carries the first
query term (`brain-inspired`). This is verified mechanically during abstract extraction
(section 4 step 1) and recorded per candidate in the adjudication CSV `query_term` column; any
non-first-query candidate would be excluded with a logged reason and a new owner-visible
disposition.

## 3. Gate 0.5 admission (run / cheaper probe / declined)

Decision: **RUN**, in the frozen order (adjudication -> pinning -> coding -> recomputation),
with the cheap stages first:

- The instruments (taxonomy, grade scale, coding instructions, merge rule, scorer) are frozen,
  hash-bound and battle-tested on the 16-claim final corpus (bound scorer PASS; defect ledger
  closed). No instrument code changes for this run.
- The claim-type adjudication is an interpretation task, not code: single-reviewer title-and-
  abstract pass under the frozen criterion (preregistration section 3: "the paper must claim, in
  abstract or title, that a biological mechanism (structure, circuit, plasticity rule, coding
  principle, connectome) improves an artificial system's capability"), executed exactly as the
  pilot's `CLAIM_TYPE_ADJUDICATION_20261020` pass, with every decision logged with a quoted
  rationale. Cheaper-probe reasoning: adjudication runs on titles+abstracts extracted from the
  pinned snapshot - no PDF is fetched for a candidate before it passes adjudication.
- The new code path for this run is one extraction script (snapshot XML -> per-candidate
  title/abstract/query-term). Its failure-class check: it must refuse (exit non-zero) if any of
  the 60 candidate IDs is missing from the snapshot, if any candidate's query term is not the
  first query term, or if the snapshot hash differs from the pinned value. A mutant run against
  a perturbed ID list must fail.
- PDF pinning reuses the pilot's fetch+hash+pdftotext path unchanged.

## 4. Frozen protocol for the validation pass (v1)

| element | frozen value |
| --- | --- |
| corpus | `corpus_validation_draw_v2.csv` (the v1 draw's successor; see execution log 2026-10-25: v1 pooled all query terms, placing 12 of 60 outside the owner's first-query boundary), adjudicated under the frozen claim-type criterion; replacements within (band, mechanism family, primary category) in fetch_rank order, logged |
| acceptance | 45-75 claims after adjudication+replacements (per the frozen validation rule) |
| pinning | arXiv PDF per surviving claim + SHA-256 manifest; `pdftotext` text layer hashed beside each PDF |
| full-text eligibility | on pinned texts, same exclusions as the pilot (retracted/withdrawn; sole-evidence-own-benchmark), single reviewer, second review before coding entry |
| coding layer | E-grades for all five transitions (T1-T5), two isolated-context coders, identical frozen instructions, in-paper and external layers |
| reportability layer | NOT in this run's scope: the frozen P0-3 definition names the kill rule and headline recomputation only; the R-instrument is already exercised on the final corpus. Adding R to the validation corpus is a named future amendment, not a silent expansion |
| adjudication of disagreements | preregistered weaker-grade resolution; one adjudication record per disputed cell; matched-neither count reported |
| estimand | headline-transition E-grade distribution and the kill-rule check on the validation corpus (80 percent E2+ bar); T1 delegation and T2 thinness as secondary readings; NO field-level prevalence wording beyond what the frozen inference rule admits |
| stop rule | if the acceptance range (45-75) cannot be met after replacements, stop and record; do not relax the frozen rule |
| inference boundary | pilot/final-corpus numbers stay labelled as they are; field-level wording, if any, requires this validation corpus and its kill-rule check (frozen 2026-10-23) |

## 5. Budget and resource claim (estimates, labelled as such)

- Adjudication: one extraction script (seconds) + one reading pass over 60 titles/abstracts
  (first-pass reader agent, incremental CSV writes) + lead verification of every exclusion and
  replacement.
- Pinning: ~60 arXiv PDF fetches, rate-limited, plus pdftotext + manifests (tens of minutes,
  background).
- Coding: 60 claims x 5 transitions x 2 coders = 600 E-grade rows. The 16-claim pass (320 rows)
  spanned several quiet windows under the host model-concurrency limit; this pass is expected to
  span multiple sessions. Incremental per-claim writes make interruption safe, as proven on the
  final corpus.

## 6. Execution log

- 2026-10-25: record frozen; extraction+adjudication admitted (this record). Entries below are
  appended, never rewritten.
- 2026-10-25 (v1 superseded, v2 drawn). The extraction instrument
  (`extract_validation_adjudication_input.py`, selftest 4 assertions PASS) REFUSED the v1 draw:
  12 of its 60 candidates are not under the first query term (they entered the pool from
  `neuro-inspired`, `neuroscience-inspired`, `bio-inspired`, `biologically plausible`,
  `neuromorphic`, `place cell` responses) - a violation of the owner's RETAIN-and-NARROW
  boundary, mechanically caught before any adjudication read a word. The v1 draw (144c41e) is
  therefore SUPERSEDED; its file stands unedited as history. Measured first-query pool (window +
  BIO/AI co-presence, the frozen filter): 200 unique records, 139 eligible = 14 (2015-2019) /
  31 (2020-2022) / 94 (2023-2026). Successor drawn by `draw_validation_v2.py` (selftest 7
  assertions PASS; refusal classes: band floor, acceptance range, non-first-query, pilot
  exclusion, family cap; fetch_rank cross-checked against v1 on the 39 shared records):
  **46 claims, bands 9/17/20, families 11/9/8/8/9/1, 45-75 acceptance met, 24-record
  pilot-exclusion set applied, snapshot sha256 re-verified**. Band notes: 2015-2019 draws 9 of
  14 eligible (family cap binds, pilot overlap), 2020-2022 draws 17 of 31 (caps + pilot
  overlap), 2023-2026 draws its full 20 target. The frozen rule's band parameters (20 target,
  >=8 required) are met without crossing the query boundary; no owner disposition is required.
- 2026-10-25 (adjudication complete; STOP RULE FIRED; owner disposition required). Claim-type
  adjudication executed per the frozen procedure: isolated first-pass reader (30 eligible /
  16 ineligible, incremental CSV writes), then lead verification of every exclusion - 5
  exclusions overturned to eligible (each names a specific biological mechanism; the operative
  rule, calibrated to the pilot's own six ineligible precedents, is recorded in
  VALIDATION_CLAIM_TYPE_ADJUDICATION_20261025_RECORD.md). 11 exclusions confirmed; replacement
  scan within (band, family, category): 18 candidates screened by the lead, 7 adopted, 4 failed
  (three HDC-family "mimics brain cognition" papers and one method-name-only evaluation), 3
  strata have no same-stratum spare. Final corpus N = 42 (35 drawn-kept + 7 replacements,
  bands 9/16/17), first file corpus_validation_v2_adjudicated.csv. The frozen acceptance
  range 45-75 cannot be met first-query-only (ceiling 42): the stop rule in this record's
  section 4 fires as written - corpus frozen pending disposition, no coding. Disposition
  options (a) accept N=42 by dated amendment (lead's recommendation), (b) authorize cross-query
  scope for the validation corpus only, (c) decline the validation pass - packaged to the owner
  2026-10-25. PDF pinning and the novelty scan proceed independently of the disposition.
