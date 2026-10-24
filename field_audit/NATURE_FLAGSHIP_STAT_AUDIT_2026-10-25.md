# Flagship Nature statistical-requirements audit of ANALYSIS_DRAFT.md (2026-10-25)

Authority: the nature-skills checklist
(`skills/nature-statistics/references/nature-article-requirements.md`,
`statistical-reporting.md`, `figure-statistics.md`; repo
`https://github.com/Yuan1z0825/nature-skills`), applied on the owner's instruction to audit
against the flagship-journal (zhengkan) requirements rather than the Analysis-type format.
Scope note kept honest: this audit checks statistical-reporting completeness at initial
submission. It does not claim an editor decision or venue fit; venue choice (NMI Analysis vs
flagship Nature) remains the owner's, and the 2026-10-23 readiness review's venue verdict
stands unless the owner overrides it.

## Actions taken by this audit (before the table)

1. Added the **Statistics paragraph** to Methods (test inventory: none, with reason; unit of
   analysis per n; interval definition: two-sided Wilson score 95 percent; replication:
   dual isolated coding + adjudication; inclusion/exclusion frozen and logged; blinding stated;
   randomization not applicable with reason; no multiplicity question; software statement).
2. Added **Figure legends** stating, per quantitative panel: what is shown, n, unit, interval
   definition, and that the dashed line in Fig 3 is a preregistered decision threshold, not a
   significance threshold.

## Audit table (one row per analysis or panel)

| Analysis/panel | Test and tail | Exact n and replicate unit | Error/interval | Exact P | Test statistic and df | Repeat count | Status |
|---|---|---|---|---|---|---|---|
| Fig 1 grade distributions | none (descriptive census) | n = 16 claims per transition; unit: claim | not applicable (complete enumeration) | none used | not applicable | dual coding, 1 adjudication pass | pass |
| Fig 2 controlled-share counts | none | n = 16 per transition; unit: claim | not applicable | none used | not applicable | as above | pass |
| Fig 3 coder A map share | none | n = 16 claims; unit: claim | Wilson score, two-sided, 95 percent | none used | not applicable | 1 map | pass |
| Fig 3 coder B map share | none | n = 16; unit: claim | Wilson 95 percent two-sided | none used | not applicable | 1 map | pass |
| Fig 3 merged map share + kill rule | preregistered decision threshold 0.80 (not a test) | n = 16; unit: claim | Wilson 95 percent two-sided (18-61) | none used; threshold comparison reported with interval | not applicable | merged from 2 maps by frozen rule | pass |
| Fig 4 reportability counts | none | n = 16 per item, 11 items; unit: claim | not applicable; aggregation sealed by protocol | none used | not applicable | dual coding + adjudication | pass |
| Fig 5 disagreement counts | none | n = 16 per transition (80 cells); unit: claim-transition cell | not applicable | none used | not applicable | 2 coders | pass |
| Reportability disagreement 39/176 | none | n = 176 claim-item cells; unit: cell | not applicable | none used | not applicable | 2 coders + 39 adjudications | pass |
| Matched-neither 0/39 | none | n = 39 adjudications; unit: adjudication | not applicable | none used | not applicable | 1 adjudicator (disclosed) | pass |
| Headline map disagreement 2/16 | none | n = 16; unit: claim | not applicable | none used | not applicable | 2 coders, frozen resolution rule | pass |
| T5 scope-match 11/16 | none | n = 16 merged T5 rows; unit: claim | not applicable | none used | not applicable | merged from 2 coders | pass |
| Reporting Summary form | not applicable | not applicable | not applicable | not applicable | not applicable | not applicable | AUTHOR_INPUT_NEEDED: none of the four listed Portfolio forms (life sciences; behavioural/social; ecology/evolution; named physical-science areas) covers a meta-research audit of published claims; the owner verifies applicability with the editor at submission |

## Items the checklist demands and where each now lives

- Every test and its comparison, tail, unit, replicate structure: Methods, Statistics paragraph
  (the inventory is: none; all analyses descriptive).
- Exact n per statistic: each figure legend and the Statistics paragraph (16 / 80 / 176).
- Error-bar definition: Fig 3 legend (Wilson score, two-sided, 95 percent); all other panels
  state that no interval applies to a census.
- Exact P values where relevant: none exist; stated explicitly rather than left implicit.
- t, F and df: not applicable, no tests; stated.
- Inclusion/exclusion, blinding, randomization, multiplicity: Methods, Statistics paragraph.
- Repeats of representative measurements: not applicable (no wet-lab measurements); dual coding
  and adjudication counts stated as the replication structure.

## Honest boundary

This audit was executed by the lead against the skill's checklist text as cloned 2026-10-25.
The skill itself warns not to claim editor decisions; that boundary is kept. The earlier
Analysis-format pass (`nmi_format_check.py`, PASS) remains valid for the Analysis-type venue;
the two audits are complementary, not redundant.
