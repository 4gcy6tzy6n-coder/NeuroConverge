# Reportability v3 candidate scorer: independent instrument review

Date: 2026-10-23

Reviewer: isolated-context independent reviewer for Route A evidence audit. This is my first
contact with this repository; I have no prior involvement with any NMI lane, no authored code
under review, and no conflict to disclose. I read only project documents; no corpus paper,
full text, coding sheet, or claim row was opened at any point.

Review target:

- `field_audit/reportability_score_candidate_v3_candidate.py` (sha256
  `b7fa04ab4b9e16d1e5baf306e56557dd5a8c7540de6213e494551c38a326455e`)
- `field_audit/test_reportability_score_candidate_v3_candidate.py` (sha256
  `c094856ba828e87268f8978c7fd025e8275db0bd9516417957d71e592169829c`)

Both hashes recomputed on 2026-10-23 and match the newest recorded values in
`REPORTABILITY_V3_SOURCE_CHECK_ORDER_DEFECT_REVIEW_2026-10-20.md` and
`REPORTABILITY_INSTRUMENT_INDEPENDENT_REVIEW_PACKET_2026-10-20.md`. All other materials
compared against their recorded hashes also match (owner amendment `7ea89842...`, adopted
protocol candidate `84390e03...`, checklist v1 `4f996389...`, v1 template `c1d3fbd4...`,
v2 source-registry template `77dcda1a...`). The received bytes are the reviewed bytes.

## Verdict

**BINDING-READY**, subject to the four binding conditions in the "Binding conditions" section.

Reason in one paragraph: within the reviewed scope, v3 faithfully implements the five owner
adoption requirements in operational behavior (requirements 2-5 fully; requirement 1's row
schema via a documented 15-field extension of the owner-bound 13-field v1 template); all three
previously reviewed defect classes (SOURCE_ROLE_BINDING, V3_POINTER_BINDING,
V3_SOURCE_CHECK_ORDER) are verified fixed by independently constructed negative fixtures, not
just by the shipped suite; the shipped suite passes 24/24 under CPython 3.12.13 and two of its
load-bearing assertions were proven defect-sensitive by single-difference mutation; my own
44-probe synthetic battery found no path that emits a summary from malformed input. One new
minor code defect (unreachable error message) and one major governance gap (the row-schema
extension is not yet owner-ratified) were found; both are recorded below. Neither is an
instrument correctness defect that could let invalid rows be summarized, so neither forces
NOT-READY; both must be discharged or recorded in the binding act itself.

This verdict covers software correctness of the candidate instrument against the adopted
protocol text on synthetic inputs. It is not scientific validation of the checklist, not
validation of the checklist as a classifier, and not authorization for corpus coding.

## Task A: adoption-requirement conformance

| # | Requirement (owner amendment, 2026-10-20) | v3 behavior (code + probe evidence) | Verdict |
| --- | --- | --- | --- |
| 1 | Evidence and reportability coding in separate tables | `FIELDS` carries no E-grade column; smuggling `evidence_grade` into a row is rejected as schema mismatch (probe D9). The scorer cannot ingest E0-E4 tables. | PASS |
| 1 | Item map = `REPORTABILITY_CHECKLIST_v1_2026-10-20.md` | `ITEM_TRANSITION` contains exactly the 11 checklist items T1-01..T5-02 with matching transitions; item/transition mismatch and unknown items are named errors (probes D21, D22). | PASS |
| 1 | Row schema = `REPORTABILITY_CODING_TEMPLATE_v1_2026-10-20.csv` (13 fields) | v3 hard-requires the 15-field `REPORTABILITY_CODING_TEMPLATE_v2_SOURCE_REGISTRY_CANDIDATE_2026-10-20.csv` (adds `source_role`, `source_id` after `source_file_sha256`; all 13 v1 columns retained by name). Rows in the v1 schema are rejected as `row schema mismatch: missing=['source_role','source_id']`. | DEVIATION - see F-1 |
| 2 | Exactly four statuses; `NOT_APPLICABLE` forbidden | `STATUSES` is exactly the four; membership is exact-match, so `NOT_APPLICABLE` (D3), lowercase `reported` (D4), and whitespace-padded ` REPORTED` (D5) are all rejected as invalid status. | PASS |
| 2 | Item-permitted citation | `REFERENCE_ALLOWED = {"T1-03"}` matches the only cite-permitting checklist item; REFERENCED on T1-02 or T2-01 is rejected (D8, suite). | PASS |
| 2 | Evidence-pointer / source-hash / source-locator rules | Nonempty pointer and locator on every row; 64-char lowercase-hex digest required (D12); REFERENCED requires the structured pointer `target_locator=<loc>;cited_source_id=<id>` with nonempty locator and ID match (B2a-d reject, B2e accepts). | PASS |
| 2 | Status-specific source binding (target / registered supplement / registered cited source) | Enforced per claim via the registry: NOT_REPORTED must bind the target (B1e, D10); TARGET must use the claim's target hash with empty `source_id` (B1a, D11); SUPPLEMENT only for REPORTED/PARTIAL and only a registered ID+hash (B1b, B1c); REFERENCED must bind a registered cited ID+hash (B1d, D26); a cited source cannot be used with REPORTED status (B1g). Registry digest must match the supplied expected digest (B1f). | PASS |
| 2 | Non-silence (no compliance inferred from silence) | PARTIAL and NOT_REPORTED require a nonempty, non-whitespace note naming the missing element / search rule (D6). The scorer cannot judge note content truthfulness; that stays a human review duty (documented by the authors). | PASS (instrument-level) |
| 3 | Exactly two independent coder rows per (claim, transition, item) | Exact-set grid equality over claims x 11 items; any missing cell is a named refusal (D1); per-(key, coder) duplicates refused, including duplicate ADJUDICATED rows (D7); rowset must be exactly the two coder names, optionally plus ADJUDICATED. | PASS |
| 3 | Exactly one adjudication row iff labels differ | Disagreement without adjudication refused (D15, suite); agreement with adjudication refused as unneeded (suite); adjudication fields must be complete and dated ISO YYYY-MM-DD on ADJUDICATED rows (D24) and blank on coder rows (D25). | PASS |
| 3 | Refuse missing/duplicate/unresolved; report raw disagreement | Every refusal path raises `ReportabilityError` before any summary; raw per-coder labels are preserved in `raw_counts_by_coder` even when the adjudicator picks a third label (D16/D16b); `disagreement_by_item` reports exact-label numerator and denominator. | PASS |
| 4 | Item-level counts by coder and after adjudication; complete count and denominator; no overall score | Result keys are exactly: claim_count, source_registry_sha256, item_ids, raw_counts_by_coder, post_adjudication_counts, complete_count_by_item, denominator_by_item, disagreement_by_item (verified by set equality, D20b). No total, share, percentage, or score key exists; complete = REPORTED plus permitted REFERENCED. | PASS |
| 5 | Verify row grid / adjudication validity / declared source hashes before summaries | Execution order in `summarize_reportability`: per-row validation -> grid completeness -> adjudication validity -> `_verify_source_files` (reads and hashes every pinned file for every distinct declared digest, including ADJUDICATED rows) -> only then are counters created and filled. Verified by trace, by an independent Counter sentinel (zero constructions before the hash-mismatch refusal, B3b), and by mutation M2 below. | PASS |

Interpretation notes for two denominators (recorded as observations F-5, F-6): the disagreement
denominator is implemented as the number of sampled claims per item, which equals the protocol's
"claims with two valid independent rows for that item" because the scorer refuses any incomplete
grid; and `complete_count_by_item` is computed from the post-adjudication status only, with
per-coder completeness derivable from `raw_counts_by_coder`. Both are consistent readings of the
adopted text under the fail-closed grid.

## Task B: regression of the three reviewed defect classes

All fixtures below were constructed by me in a scratch directory (`/tmp/rv3_review`), importing
the repository scorer read-only. Each uses fabricated rows and temporary synthetic files.

### SOURCE_ROLE_BINDING (v2 accepted any locally pinned hash for any role)

| Probe | Input class | Result |
| --- | --- | --- |
| B1a | REPORTED/TARGET row pointing at a second, locally pinned and byte-verified file | REJECTED: `TARGET source role must bind the claim's target paper` |
| B1b | SUPPLEMENT with unregistered ID (the hash itself is pinned and registered under a different ID) | REJECTED: `SUPPLEMENT source role must bind a registered supplement ID and hash` |
| B1c | SUPPLEMENT with registered ID but mismatched hash | REJECTED (same named class) |
| B1d | REFERENCED (T1-03) with unregistered cited ID | REJECTED: `REFERENCED must bind a registered cited source ID and hash` |
| B1e | NOT_REPORTED bound to a different locally valid file | REJECTED: `NOT_REPORTED must bind the claim's target paper` |
| B1f | Registry whose canonical digest differs from the supplied expected digest | REJECTED: `source registry hash does not match the owner-bound digest` |
| B1g | REPORTED status attempting to ride a cited source | REJECTED: `source role 'CITED_SOURCE' is not permitted for status REPORTED` |

Verdict: the v2 defect class (a well-formed row pointing at any hash in the global map) is
closed. Role identity, not just byte identity, is now enforced per claim.

### V3_POINTER_BINDING (REFERENCED pointer only needed to be nonempty)

| Probe | Input class | Result |
| --- | --- | --- |
| B2a | Generic unrelated pointer | REJECTED: `REFERENCED evidence_pointer must bind target citation location and registered source ID` |
| B2b | Structured pointer naming a wrong source ID | REJECTED (same class) |
| B2c | Structured pointer with empty target locator | REJECTED (same class) |
| B2d | Pointer with a near-miss marker (`cited_id=`) | REJECTED (same class) |
| B2e | Well-formed structured pointer | ACCEPTED (positive control) |

Verdict: repaired as claimed. The scorer validates the declared structure and ID match; it
cannot verify the locator truthfully names a citation in the target paper, which the repair
record itself states remains a human judgment.

### V3_SOURCE_CHECK_ORDER (counters were initialized before source-byte verification)

| Probe | Method | Result |
| --- | --- | --- |
| B3a | Pinned file mutated after pinning; summarize called | REJECTED: `bound source file hash mismatch` |
| B3b | Same, with the module-level `Counter` replaced by a sentinel that records any construction | Hash-mismatch refusal raised with ZERO Counter constructions - counters cannot run before byte verification |

Verdict: repaired as claimed, and confirmed by mutation M2 below.

## Task C: shipped suite run and perturbation of two assertions

Suite run (pristine files, in place): `python3 -m unittest test_reportability_score_candidate_v3_candidate -v`
under CPython 3.12.13 -> **24 tests, all OK**, matching the recorded count and hashes.
`py_compile` passes for both modules.

Perturbation (single-difference mutations of scorer copies in `/tmp/rv3_review`, suite unchanged):

- **M1** - reverted `_validate_referenced_pointer` to nonempty-only checking (the pre-repair
  behavior). Result: exactly `test_referenced_pointer_must_bind_target_citation_location_and_source_id`
  fails, 3 subtest failures (`ReportabilityError not raised`). The pointer assertion is
  defect-sensitive. Honest note: my first M1 attempt added an early return for empty pointers
  and changed nothing (empty pointers are already refused upstream, so the added branch was dead
  code); the suite correctly stayed green under that non-mutation, and I re-applied the true
  reversion before accepting the result.
- **M2** - moved the `_verify_source_files` call from before counter construction to immediately
  before the result dict is built (undoing the ordering repair). Result: exactly
  `test_source_bytes_are_verified_before_summary_counts` fails (the patched Counter sentinel
  fires). The ordering assertion is defect-sensitive.

Both sampled assertions can genuinely fail; neither is tautological.

## Task D: independent edge-case probes (44 checks total)

Baseline positive P0 passes. Full battery result: 42 of my probes PASS, one (D20) initially
failed due to my own fixture error (registry did not cover the second claim; corrected rerun
PASSES), and one (D19) surfaced the new minor defect below. The complete runnable battery is
preserved at `/tmp/rv3_review/probes.py`; classes covered:

- Empty inputs: empty rows table -> named grid refusal (D1); empty claim list -> named refusal (D2).
- Status vocabulary: `NOT_APPLICABLE`, lowercase, whitespace-padded, all refused (D3-D5);
  whitespace-only PARTIAL note refused (D6).
- Adjudication completeness: duplicate ADJUDICATED row refused (D7); two disagreements with only
  one adjudicated -> refusal naming the unresolved key (D15); adjudication to a third label
  accepted with raw labels preserved and completeness following the adjudicated label (D16/D16b);
  impossible calendar month refused (D24); adjudication fields on a coder row refused (D25).
- Hash/file binding: uppercase hex refused (D12); directory bound as the source path -> refused
  (D19, see F-2); the same physical file declared under a second incorrect digest -> refused by
  the registry-role check before byte reading (D27); a byte-identical twin file verifies, which
  is correct because the contract binds bytes, not paths (D18a).
- Claim/sample integrity: duplicate claim IDs in the sample refused (D13); row for an unsampled
  claim refused (D23); registry claim set must equal the sample exactly (suite + my D20 rerun).
- Structure: unknown item, item/transition mismatch refused (D21/D22); E-grade field refused
  (D9); REFERENCED restricted to T1-03 including within-transition near-miss T1-02 (D8); coder
  roles confined to the two named coders plus ADJUDICATED (D14, D25); two-claim mixed grid via a
  generator input produces the exact result key set with per-claim denominators and no score
  key (D20/D20b).
- Documented behavior limits: an unused registered hash (cited source never referenced by any
  row) is never byte-verified and passes without a pinned file (D17, observation F-4).

## Findings register

Severity scale: blocker / major / minor / observation. "Blocker/major" would force NOT-READY
until fixed; the two items below graded major/minor are, respectively, a binding-act
prerequisite rather than an instrument defect, and an error-fidelity defect with fail-closed
behavior intact.

| ID | Severity | Finding | Evidence | Required action |
| --- | --- | --- | --- | --- |
| F-1 | major (governance / binding prerequisite, not a code defect) | The owner amendment's requirement 1 names the 13-field v1 template CSV as the row schema; v3 requires the 15-field v2 source-registry candidate template and hard-rejects v1-schema rows. The two new columns (`source_role`, `source_id`) are exactly what the SOURCE_ROLE_BINDING repair needs and are documented and hash-recorded, but they are not yet owner-ratified. Until ratified, the amendment text and the instrument disagree. | `FIELDS` vs both CSV headers; D9-style missing-column rejection | The owner binding for v3 must explicitly supersede the v1 template reference with the v2 source-registry template (or a successor) and add v3 scorer, v3 tests, and the template to the bound-materials hash table. |
| F-2 | minor (new, found by this review) | Unreachable error message in `_verify_source_files`: `raise ReportabilityError(f"bound source file is missing: {path}")` sits inside the `try` whose `except (OSError, TypeError, ValueError)` also catches `ReportabilityError` (a `ValueError` subclass), so the missing-file class always surfaces wrapped as `cannot read bound source file for <hash>`. The path detail is lost and the two classes (missing vs unreadable) are indistinguishable in the message. Fail-closed behavior is intact: a named `ReportabilityError` naming the hash is still raised before any summary. | D19: bound directory and chmod-000 file produce the identical wrapped message | Optional fix before binding (one-line: raise outside the try or catch `ReportabilityError` and re-raise). Any fix changes the scorer hash and reopens review of that changed behavior only. Recording it unfixed in the binding is also acceptable. |
| F-3 | observation | Expected-registry-digest circularity: the scorer checks the supplied registry against a caller-supplied digest; it cannot establish the digest's authority. The test suite itself passes a self-computed digest. | Code trace; test helper `registry_hash` | The binding record must freeze the expected canonical-registry digest together with the claim set it covers. |
| F-4 | observation | Byte verification covers only digests declared in rows; registered-but-unused supplement/cited hashes (and a target hash when every row binds a supplement) are trusted solely via the registry digest. | D17 | State this scope in the binding record; optionally require the registry producer to verify all registered files at manifest build time. |
| F-5 | observation | Disagreement denominator is the number of sampled claims per item; equals the protocol's "claims with two valid independent rows" because incomplete grids are refused outright. | Code + D15 | None; record the equivalence at binding. |
| F-6 | observation | `complete_count_by_item` is post-adjudication only; per-coder completeness is derivable from `raw_counts_by_coder`. | D16b | None; acceptable reading of the amendment's singular "the complete count". |
| F-7 | observation | `evidence_pointer` must be nonempty on every row, slightly stricter than the protocol text (which specifies pointer content only for REFERENCED). Identical to the owner-bound v1 scorer's behavior, so inherited rather than new, and fail-closed in direction. | v1 scorer line 79; v3 line 90 | None. |
| F-8 | observation | `coders` must be a Python tuple; a two-element list is refused. API strictness only. | D14 | None. |
| F-9 | observation | When multiple declared hashes are bad, which mismatch is reported first follows set-iteration order (nondeterministic selection, deterministic message per hash). | Code trace | None; cosmetic. |
| F-10 | observation | The adjudicator may record a third status label distinct from both coder labels; the protocol text does not forbid it and the suite itself exercises it (REPORTED/PARTIAL -> NOT_REPORTED). Raw labels remain preserved. | D16 | If the owner intends adjudication to be confined to the two observed labels, record that as a protocol clarification at binding; no code change implied by the current text. |
| F-11 | observation | "Preserve both records" is a data-management duty: the scorer consumes a complete row set and preserves both labels in its outputs, but physical row retention lives in the coding sheets, outside the instrument. | Design | Ensure the coding workflow stores original coder rows untouched before any summarize call. |

## Binding conditions

The candidate is BINDING-READY provided the owner binding record:

1. Ratifies the 15-field row schema (F-1), superseding the v1 template reference in requirement 1,
   and binds the v3 scorer, v3 test suite, and template by fresh hash.
2. Freezes the expected canonical source-registry digest and the claim set it covers (F-3), noting
   the byte-verification scope (F-4).
3. Records F-2 (minor) either as accepted-as-is or fixes it first, with the hash refresh and a
   bounded re-review of that one behavior.
4. Leaves the remaining coding-admission gates (second review of full-text eligibility, P4 coder
   naming with the non-author condition, methods review acceptance) exactly as the owner amendment
   states them; this instrument review does not discharge any of them.

## Review environment and commands

- Machine: macOS darwin 25.2.0 arm64; CPython 3.12.13 (the same minor version the repair records
  cite). Working directory `/Users/yyl/Desktop/workshop/NMI/NeuroConverge/field_audit`; scratch
  work in `/tmp/rv3_review` (mutation copies and the probe battery). Repository imports ran with
  `PYTHONDONTWRITEBYTECODE=1`; no repository file was modified, and both v3 hashes were re-verified
  identical after all runs.
- `shasum -a 256` over all nine compared materials (values recorded above and in the packet).
- `python3 -m unittest test_reportability_score_candidate_v3_candidate -v` -> 24 OK.
- `python3 -m py_compile` on scorer and test -> OK.
- Mutation runs in `/tmp/rv3_review/mut1` (pointer reversion) and `/tmp/rv3_review/mut2`
  (ordering reversion) -> 3 and 1 failures respectively, each confined to the targeted assertion.
- `python3 /tmp/rv3_review/probes.py` -> 44 checks: 42 PASS, 1 fixture-error corrected and
  re-run PASS (D20), 1 real finding (D19 -> F-2).

## Boundary statement

This is a static-plus-synthetic instrument review. It establishes that, within the reviewed
scope, no known blocking or major software defect remains in the v3 candidate scorer's
validation and summarization behavior, and that the three previously reviewed defect classes are
repaired. It does not establish scientific validity of the checklist, does not validate the
checklist as a classifier of anything, and no corpus claim was scored, read, or opened. Software
correctness is not scientific evidence.
