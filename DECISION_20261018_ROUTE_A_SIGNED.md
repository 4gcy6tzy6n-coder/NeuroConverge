# Decision record: Route A signed and authorized (2026-10-18)

**Status: authority document.** The owner's signature on `PROPOSAL_20261018_FIELD_AUDIT_ROUTE_A.md` was relayed
by the project lead on 2026-10-18 as "确认签字执行" (confirmed, signed, execute). Items P1-P7 are approved as
proposed. This record binds the scope of what is now authorized; it converts no archived verdict in any lane and
re-opens no closed line.

## What is authorized

| item | authorization |
| --- | --- |
| P1 | The publication route switches to the field-level evidence audit (NMI Analysis target; fallbacks Patterns, TCS). v1's manuscript role becomes framework seed and calibration material. |
| P2 | Literature-side work for this audit is unlocked from the MICA archive ruling's "scientific literature expansion not authorized" clause, for this use only. No MICA verdict, register row or stop rule is re-graded; the archive is cited as it stands. |
| P3 | The pre-registration `AUDIT_PREREGISTRATION_v1_FROZEN.md` is frozen as signed. Sections 2-6 thresholds may change only by dated owner-visible amendment before coding begins. |
| P4 | Dual-coder staffing: **open**. The owner names the coders; at least one must not be an author of workspace code. The coding phase does not start until both are named. The draw and infrastructure phases are not gated on P4. |
| P5 | Venue sequence: Nature Machine Intelligence Analysis, then Patterns, then Trends in Cognitive Sciences. |
| P6 | Schedule and stop rules of the frozen protocol section 10 apply; the 8-week clock starts at corpus freeze (the commit of the draw output), not at this signature. |
| P7 | Governance debts (source-snapshot freeze, crosswalk adjudication, D7 appointment) run in parallel and must close before submission. |

## What remains unauthorized

- No experiments, no seeds, no training, no GPU, in any lane, under this authorization.
- MICA stays independently archived (`PHASE1_EXIT_NO_ADMISSIBLE_ORIGINAL_RQ`); IRCN, NeuroMotif, 67D and CBCC
  stay closed; BioMemory proceeds only under its own lane's standing authorizations, untouched by this document.
- RR18/RR19 stay excluded (PROJECT_FREEZE boundary 5).

## Execution state at signing

1. `field_audit/` is created as this workstream's home inside NeuroConverge (the publication lane). Its README is
   the entry point.
2. The draw script `field_audit/draw_corpus.py` implements the frozen selection rule with self-tests; the
   executed draw, its query log and snapshot hash land in `field_audit/` when the pinned database snapshot is
   obtainable.
3. The first draw attempt on 2026-10-18 was **blocked by an external quota**: the OpenAlex free shared-IP daily
   budget is exhausted (exact error recorded in `field_audit/DRAW_ATTEMPT_LOG.md`). Following the lane's own
   precedent (a route failure is an instrument fact, recorded, not evidence of absence), the draw re-attempts
   after the budget resets at midnight UTC or with an owner-supplied API key. No candidate list exists yet and
   none is improvised from search snippets: the frozen rule requires a scriptable, hash-pinnable snapshot.
4. The corpus is NOT frozen as of this document. Section 10's schedule clock has not started.

## Signature block

Signed (owner ruling relayed by project lead): 2026-10-18, "确认签字执行".
Recorded by: the executing session, 2026-10-18.
