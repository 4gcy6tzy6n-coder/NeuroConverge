# field_audit -- the Route A workstream

**Authority:** `../DECISION_20261018_ROUTE_A_SIGNED.md` (2026-10-18). **Constitution:**
`AUDIT_PREREGISTRATION_v1_FROZEN.md` -- sections 2-6 frozen; changes only by dated owner-visible amendment.

## Status

| phase | state |
| --- | --- |
| authorization | DONE (P1-P3, P5-P7 signed; **P4 dual-coder staffing open -- owner names the coders**) |
| pre-registration | DONE, frozen 2026-10-18 |
| corpus draw | BLOCKED 2026-10-18 by OpenAlex shared-IP daily quota exhaustion (exact error in `DRAW_ATTEMPT_LOG.md`); re-attempts after 00:00 UTC or with an owner-supplied API key. **Corpus is NOT frozen; the 8-week clock has NOT started.** |
| draw review / claim-type adjudication | waiting on the draw |
| coding | waiting on P4 and corpus freeze |
| checklist skeleton | DONE (`REPORTING_CHECKLIST_DRAFT.md`) |

## Files

| file | role |
| --- | --- |
| `AUDIT_PREREGISTRATION_v1_FROZEN.md` | the binding protocol |
| `draw_corpus.py` | the selection script: builds the candidate pool from a pinned OpenAlex snapshot by the frozen mechanical filters, applies stratified draw with caps, writes the corpus list, the register rows and a provenance manifest (query, date, snapshot hash). `--selftest` runs its sabotage-verified checks on fixtures |
| `AUDIT_REGISTER.csv` | the register of record: one row per candidate and per coded claim, with provenance (empty until the draw runs) |
| `CODING_SHEET_TEMPLATE.csv` | the coding instrument, one row per (claim, transition), fields per protocol section 5 |
| `REPORTING_CHECKLIST_DRAFT.md` | the normative artifact's skeleton, drafted before coding per protocol section 7 |
| `DRAW_ATTEMPT_LOG.md` | every draw attempt with its outcome, including failures (a route failure is an instrument fact, recorded, not evidence of absence) |

## Order of operations from here

1. Run `draw_corpus.py --query` once the OpenAlex budget resets (or with an API key). The script writes
   `corpus_draw_v1.csv` + `corpus_draw_v1.manifest.json`; commit = corpus freeze.
2. Claim-type adjudication over the candidate pool, per-candidate reason logged; replacements fire per the
   frozen rule.
3. Owner names the two coders (P4).
4. Coding begins on `CODING_SHEET_TEMPLATE.csv` structure; register rows pinned per paper.
5. Statistics scripts read the coding sheets; section 6's frozen output list is computed, never transcribed.
