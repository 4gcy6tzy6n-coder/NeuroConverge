# Owner binding request: the v3 reportability scorer (2026-10-23, one signature)

**What is being asked.** One dated owner signature that (1) binds the v3 candidate scorer as the scoring
instrument for the reportability protocol, (2) approves the row-schema extension it requires, (3) freezes the
expected source-registry digest, and (4) records the one minor defect as recorded-not-fixed. Declining or
amending any item is a recorded outcome; nothing is bound without this page.

## The chain this signature completes

- The owner-approved reportability amendment (2026-10-20) froze the protocol and required the scorer, form
  and synthetic checks to be frozen and reviewed before coding.
- The scorer line ran v1 (blocking date-format defect) -> v2 (blocking source-role-binding defect) -> **v3**,
  each repaired against its named defect review.
- The independent isolated-context review of v3 (2026-10-23) concludes **BINDING-READY with four binding
  conditions**: requirements 2-5 of the amendment verified PASS (including the dual-coder grid enforcement,
  the four-status vocabulary, the no-overall-score rule, and hash-verification-before-any-counting, the last
  confirmed by an independent sentinel); all three declared v2/v3 defects regression-verified by synthetic
  counter-example; the test suite mutation-checked for real (with the reviewer's own first dead mutation
  honestly discarded and redone); 44 boundary probes; **one new minor defect (F-2: an unreachable error
  message - fail-closed behaviour intact, error fidelity lost)** and **one major governance item (F-1: v3
  requires the 15-field v2-source-registry row schema, not the owner-bound 13-field v1 template - a schema
  extension the owner never approved)**.

## The four items the signature decides

| item | decision requested | consequence if declined |
| --- | --- | --- |
| B1. bind v3 | bind `reportability_score_candidate_v3_candidate.py` (sha256 `b7fa04ab...`) and its test file (sha256 `c094856b...`) as the frozen scoring instrument | coding stays paused; v3 returns to candidate status with the review on record |
| B2. approve the 15-field schema | the 15-field v2-source-registry template becomes the bound row schema (superseding the 13-field v1 template bound on 2026-10-20), recorded as a dated amendment to the reportability amendment | v3 cannot be bound as-is; a v4 restricted to the 13-field schema would be required |
| B3. freeze the registry digest | the expected SHA-256 of the source-registry CSV is frozen at binding time, so any later registry edit forces a visible re-binding | the registry remains mutable, weakening provenance |
| B4. F-2 disposition | record F-2 as known-minor, not fixed (fixing reopens a local re-review of that behaviour; the loss is error-message fidelity only, both error paths still fail closed) | the owner may instead require the fix and the local re-review |

## Not affected by this signature

The remaining coding-entry gates stand independently: the full-text eligibility second review (C101, C028,
C192, replacement closure), the P4 coder appointments, and the methodology review named in the amendment.
This page binds an instrument; it authorizes no coding and touches no corpus row.
