# Advisor review record (2026-10-25): NMI Article confirmed as the first submission target

Authority: the advisor's assessment relayed by the project lead on 2026-10-25 (verbatim retained
in the session record; this document records its dispositions). The declaring documents
(`VENUE_DECISION_20261025.md`, `VALIDATION_ACCEPTANCE_AMENDMENT_20261025.md`) stand unedited.

## Advisor verdict (as received)

1. "值得冲击 NMI Article" - worth pursuing; NMI Article is formally established as Route A's
   first submission target. The project has three mutually supporting parts: a clear scientific
   question, replicable empirical findings (both corpora show the same utility-vs-correspondence
   asymmetry), and an independently usable method contribution (five-transition chain, dual-axis
   measurement, executable scorer).
2. NOT yet assessable as "likely to pass review". Three risks decide the outcome:
   - R1 (highest): measurement credibility - both coding rounds are same-model AI instances; a
     real human independent coding pass is required (focus: T2 E1/E2 boundary and T5 claim
     scope). NMI's AI policy requires human responsibility for research judgments.
   - R2 (high): representativeness - one snapshot, first query term, 6 surveys in the validation
     corpus. Requires targeted robustness analyses: (a) recompute core results excluding
     surveys; (b) test whether the instrument can recognize known positive cases with strong
     mechanistic evidence (counters "the scale inherently grades low").
   - R3 (highest): framing - "papers did not redo biology experiments" is NOT the finding and is
     rebuttable (AI research legitimately relies on published neuroscience). The core finding is
     the stable T2-vs-T3 evidence asymmetry (T2 2/16 and 9/42 controlled vs T3 10/16 and 25/42);
     the universal claim is that current evaluation practice validates utility but does not
     validate the correspondence with the cited biological mechanism, and this audit supplies an
     operational supplementary method.
3. Article (not Analysis) confirmed as justified; the final manuscript must foreground the
   reusable measurement method as an independent contribution.

## Dispositions executed (2026-10-25, same day)

| directive | disposition |
| --- | --- |
| R2a: survey-exclusion recomputation | `ROBUSTNESS_SURVEY_EXCLUSION_20261025.md` - mechanical survey rule frozen, both corpora recomputed |
| R2b: positive-case sensitivity of the instrument | `POSITIVE_CONTROL_PROBE_20261025.md` - frozen nomination criterion + prediction, isolated coding run |
| R3: reframing (asymmetry as the core finding; delegation preemption; universal claim) | manuscript revision, same day (abstract, Results lead, Discussion; format checker re-run) |
| R1: human coding pass | owner package O-5 updated with the advisor's focus items; the packet (frozen instructions + sheets) is submission-ready |
| Venue confirmation | recorded here; `VENUE_DECISION_20261025.md` remains the operative record |

## Inference discipline note

The advisor's reframing is consistent with the frozen instruments: the T2-vs-T3 asymmetry is
computed from the same merged sheets already committed; no number changes. The survey exclusion
is a named robustness analysis reported beside, never instead of, the primary numbers.

---

## Round 3 (2026-10-25, later): final ruling on this review series

The advisor confirmed, on the report of commit `957c22f` (independent diff inspection reserved):

- **R2a survey-exclusion robustness: CLOSED.** Two levels correctly separated - the statistics
  were correct (16 - 1 = 15; sole final-corpus survey C045 / 2305.11252v1), the source bookkeeping
  was the defect (pilot 18-draw scanned instead of final-16 membership), and the fix (membership
  from coding sheets + membership assertion) addresses the true error source. Tracked erratum,
  not a results-driven adjustment.
- **R2b positive-control probe: CLOSED.** Amended wording accepted. The probe shows the scorer is
  not structurally barred from awarding high grades to mechanistic-correspondence evidence; it
  does not establish overall classification accuracy or cross-coder stability - both belong to
  O-5, and no further AI probes may be substituted for them.
- **R3 narrative reframing: CLOSED.**
- **O-5: the three-stage protocol is approved** with the acceptance criteria frozen in
  `O5_HUMAN_CODING_PROTOCOL_20261025.md` (H1 full blind primary corpus; H2 pre-agreed validation
  scope incl. pre-drawn non-disputed controls; H3 raw-agreement + grade-transition + asymmetry
  sensitivity under BOTH raw human grades and preregistered disagreement handling). Two binding
  requirements: the human coder never sees AI grades or merged adjudications; the question H3
  answers is whether the T2/T3 asymmetry survives independent human judgment - not whether human
  coding agrees with AI coding.
- **Manuscript: no further expansion** (3,439/3,500). O-5 findings may change main conclusions;
  human coding must not be reduced to a ratification exercise.
- **Gate status**: R2a/R2b/R3 CLOSED; O-5 BLOCKED (staffing); O-6 OPEN; O-4/O-0 OPEN. Next
  priority: O-5 - not new experiments, more literature, or larger samples. If human coding
  supports the core asymmetry and the non-author recomputation passes, the advisor will support
  formal NMI Article submission to external review.
