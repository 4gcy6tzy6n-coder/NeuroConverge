# O-6 findings resolution record (2026-10-25)

**Authority.** The project lead's decisions on the O-6 report, relayed 2026-10-25 as
"按照你说的做" for options 1A-5A: accept the AI non-author verification as the machine-checkable
half of O-6 and obtain a human counter-signature (1A); add a dated reading-2b generator without
editing the frozen H3 instrument (2A); commit the four missing bound/analysis inputs (3A); adopt the
committed primary headline map as canonical, append a dated correction, and record the tie-break
divergence for the successor instrument (4A); correct the O-6 setup note (5A).

**Prepared by.** Claude Code (AI assistant), at the lead's direction. The verifier's as-found record
is `O6_VERIFICATION_REPORT_CLAUDE_20261025.md`; this record documents only the lead-authorized
resolutions. No finding is deleted, and no load-bearing number changes.

**Base commit.** `0dbf8acc2f6711826417075ff2a8d0cd4c17ca45` (the HEAD verified by O-6).
**Resolution commit.** `253507e9ef2668826ac9d62c339c4f90721a1bcc` on branch
`o6-findings-resolution-20261025` (`fix: resolve O-6 findings F1-F5`).
**Clean-clone check.** `~/o6_resolution_check/NeuroConverge`, a fresh clone of the resolution branch
at `253507e` plus the two untracked pinned directories.

## F1 - reading 2b generator restored

- New `compute_H3_reading2b_20261025.py` computes the preregistered disagreement-handled reading
  (weaker of coder H and the AI weaker-merge per covered cell) from the raw sheets and writes the
  `reading2b_weaker_merge_H_vs_AI` block into `CODING_sheets_human/H3_READING_20261025.json`.
- The frozen `compute_H3_full_20261025.py` was **not** edited. The full chain is now:

  ```bash
  python3 field_audit/compute_H3_full_20261025.py
  python3 field_audit/compute_H3_reading2b_20261025.py
  ```

- Result: the committed H3 JSON is reproduced **byte-for-byte** (SHA-256
  `53175756da043aaf9e92d30509d45c8f2edd33ca31571b84b8936b5b0c39787f`). The script's `--selftest`
  passes 8 assertions (4/16 = 25.0 pct; 19/41 = 46.3 pct; T2/T3 1/16 vs 4/16 and 2/42 vs 19/42;
  weaker-rule checks). O-6 independently recomputed these values from the raw sheets.
- A dated supplement was appended to `O5_H3_RESULTS_20261025.md` recording the chain and the
  unchanged numbers.

## F2 - clean-clone packaging gap closed

The four inputs that were untracked at HEAD are now committed at the resolution commit, with their
bytes unchanged:

| file | SHA-256 |
| --- | --- |
| `reportability_score_candidate_v3_candidate.py` | `b7fa04ab4b9e16d1e5baf306e56557dd5a8c7540de6213e494551c38a326455e` (matches `BINDING_RECORD_V3_20261024.md`) |
| `test_reportability_score_candidate_v3_candidate.py` | `c094856ba828e87268f8978c7fd025e8275db0bd9516417957d71e592169829c` (matches binding) |
| `REPORTABILITY_CODING_TEMPLATE_v2_SOURCE_REGISTRY_CANDIDATE_2026-10-20.csv` | `77dcda1acd507f8fa216b390d6e4c2028c967211cc5e817f2e92f7a4a49fdb6e` (matches binding) |
| `CLAIM_TYPE_ADJUDICATION_20261020.csv` | `1056ca094040ac8138b25aae07c2535d9dbeb44f596a43846b8929b135860f76` (pilot adjudication input to R2a) |

Clean-clone results at `253507e` (pinned dirs copied; no other untracked inputs supplied):

- `python3 field_audit/run_final_scoring_20261024.py` -> exit 0; regenerated
  `adjudication_R_20261024.csv` and `reportability_summary_final_20261024.json` **byte-identical**
  to the committed files.
- `python3 field_audit/robustness_survey_exclusion_20261025.py` -> exit 0; regenerated
  `ROBUSTNESS_SURVEY_EXCLUSION_20261025.json` **semantically identical** (JSON key order only).
- `python3 -m pytest -q field_audit/test_reportability_score_candidate_v3_candidate.py` ->
  **24 passed, 7 subtests passed**.
- The H3 chain above reproduces the H3 JSON byte-for-byte.

This removes the O-6 F2 blocker: the two analyses that previously failed in a clean clone now run
from committed inputs alone. The positive-control probe's PDFs/texts remain untracked by design
(hash manifests are committed); this is unchanged and documented as a manifest-anchored input.

## F3/F4 - headline-map agreement corrected; tie-break divergence recorded

- Canonical value against the committed primary map: **52/58** (primary 16/16, validation 36/42).
- H3-script variant (re-derives the primary map with the validation tie rule): **51/58**; the only
  divergent claim is C077 / `1811.09699v1` (committed map T2, H3-derived map T3). Coder H's own
  headline for it is T2 and agrees with the committed map.
- New `compute_H3_headline_agreement_20261025.py` reproduces both variants; `--selftest` passes 5
  assertions; output is committed as
  `CODING_sheets_human/H3_HEADLINE_AGREEMENT_CORRECTION_20261025.json` (SHA-256
  `e8f17db32ef5d8e26db8c97cc0dafe7b72551471aa857355f40d9ffb10704a6c`).
- A dated correction was appended to `O5_H3_RESULTS_20261025.md` section 4's record. The current
  round's committed maps stand; the successor instrument must freeze one headline tie-break rule
  before coding. No per-cell agreement, disputed-cell count, raw-H reading, or reading-2b number
  changes.

## F5 - setup note corrected

`O6_VERIFIER_ASSIGNMENT_20261025.md` now states that `field_audit/fulltexts/` is tracked at HEAD (22
files) and that only the pinned text/PDF directories are untracked. The redundant `cp -r` line is
annotated as such. No analysis impact.

## Status and remaining owner actions

- F1: **fixed** (generator committed; byte-identical full chain).
- F2: **fixed** (four inputs committed; clean-clone runs pass).
- F3/F4: **fixed by dated correction**; canonical agreement 52/58; tie-break divergence recorded.
- F5: **fixed** (setup note corrected).
- **Owner action 1:** merge branch `o6-findings-resolution-20261025` into `main` (or keep the branch
  as the submission record). The branch contains one fix commit, `253507e`.
- **Owner action 2:** obtain the human non-author counter-signature requested in
  `O6_HUMAN_COUNTERSIGN_REQUEST_20261025.md`. Until then, O-6 is: AI verification complete, human
  signature pending.
- **Owner action 3:** send the O-6 report, this resolution record, and the counter-signature to the
  advisor for the gate confirmation.

## Statement

Every load-bearing number in the O-6 target table is unchanged. This record resolves reproducibility
and record-consistency findings; it does not re-grade any claim and does not replace the verifier's
as-found report.
