# Binding record (2026-10-24): the v3 scorer is bound; B1-B4 executed as approved

**Authority.** The owner's approval relayed by the project lead on 2026-10-24 as "全部批准", covering all
four items of `OWNER_BINDING_REQUEST_V3_20261023.md`. Executed the same day under the 2026-10-19 full-authority
grant. Decline consequences are moot; each item's executed state follows.

## B1 - the scorer is bound

| material | role | sha256 (frozen) |
| --- | --- | --- |
| `reportability_score_candidate_v3_candidate.py` | the bound scoring instrument (the filename keeps its candidate history; these bytes are the instrument of record) | `b7fa04ab4b9e16d1e5baf306e56557dd5a8c7540de6213e494551c38a326455e` |
| `test_reportability_score_candidate_v3_candidate.py` | the bound synthetic failure-class checks | `c094856ba828e87268f8978c7fd025e8275db0bd9516417957d71e592169829c` |

Independent review on record: `REPORTABILITY_V3_INDEPENDENT_REVIEW_20261023.md` (BINDING-READY, four
conditions - all four executed or recorded below).

## B2 - the 15-field schema is the bound row schema

`REPORTABILITY_CODING_TEMPLATE_v2_SOURCE_REGISTRY_CANDIDATE_2026-10-20.csv` supersedes the 13-field v1
template as the bound row schema, recorded as a dated amendment to the 2026-10-20 reportability amendment
(the v1 template stays in the tree as history). Any further field change reopens binding.

## B3 - the source-registry digest is frozen

The bound registry template's sha256 is frozen at
`77dcda1acd507f8fa216b390d6e4c2028c967211cc5e817f2e92f7a4a49fdb6e`. The scorer already refuses rows whose
declared source hashes mismatch; from binding, any edit to the registry template itself forces a visible
re-binding rather than a silent drift.

## B4 - F-2 is recorded, not fixed

The unreachable error message in `_verify_source_files` (minor; both error paths fail closed, error fidelity
only) is recorded as a known defect of the bound instrument. Fixing it reopens a local re-review of that
behaviour and a re-binding - deliberately not taken.

## The remaining coding-entry gates, and today's moves on each

Per the 2026-10-20 amendment's gate list:

1. **Full-text eligibility second review** (C101, C028, C192, replacement closure): dispatched today as an
   isolated-context second review under the standing authority, with the disclosure that an AI-context
   second review is what it is and the human pass supersedes; its record closes or reopens each disposition.
2. **P4 coders named**: under the 2026-10-19 authority record, P4 = the two isolated-context coder instances
   (neither authored any workspace code), with the same-model disclosure in the methods and the
   human-supersedure rule. A later human naming supersedes this record and triggers one-command recomputation.
3. **Independent methods review** of the amended protocol and bound instruments: dispatched today as an
   isolated-context review against the amendment's own adopted text.
4. **Instrument defect review with findings fixed and re-reviewed**: satisfied by the v3 independent review
   plus this binding (F-2 recorded per B4).

Coding starts only when gates 1 and 3 return; nothing is scored today.
