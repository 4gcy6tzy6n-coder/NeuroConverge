# Task assignment: non-author verification of a submission-bound evidence audit (O-6)

Issued: 2026-10-25. Hand this document, together with the verification copy (setup below), to
the verifier. You are the independent non-author verifier: you did not author any instrument,
script, or manuscript text in this project, and your job is to check - from the artifacts alone -
that the numbers a journal manuscript claims are actually reproducible.

## What you are verifying

A meta-research manuscript audits bio-to-AI transfer claims across two frozen corpora (16 primary
+ 42 validation papers). Every load-bearing number in it is supposed to be recomputable from
committed artifacts by one command. Your task is to reproduce those numbers, verify the
provenance chains, and try to break the claims - honestly. A discrepancy you find is a FINDING
to record, not a problem to fix: **you verify, you never repair.** If something fails, document
it precisely (file, command, expected, observed) and move on.

## The claimed numbers (your reproduction targets)

| claim | where stated | value to reproduce |
| --- | --- | --- |
| Primary headline E2+ (AI weaker-merge) | manuscript Results; `CODING_sheets_v2/statistics_final_20261024.json` | 10/16 = 62.5 percent, Wilson 95 percent CI [39, 82] |
| Validation headline E2+ (AI weaker-merge) | `CODING_sheets_validation/statistics_validation_20261025.json` | 26/42 = 61.9 percent, CI [46.8, 75.0] |
| T1 in-paper E0 | both corpora | 16/16 primary; 42/42 validation |
| Human reading (coder H) headline E2+ | `CODING_sheets_human/H3_READING_20261025.json` | raw H: 5/16 = 31.2 percent primary, 20/41 = 48.8 percent validation; weaker(H, AI): 4/16 = 25.0 percent, 19/41 = 46.3 percent |
| H asymmetry (T2-E2 vs T3-E2) | `O5_H3_RESULTS_20261025.md` | raw H primary 5/16 vs 4/16; validation 6/42 vs 19/42 |
| In-paper disagreement | both statistics JSONs | 18/80 = 22.5 percent primary; 64/210 = 30.5 percent validation |
| H vs AI-merge agreement | `H3_READING_20261025.json` | 61.2 percent primary (80 cells), 58.7 percent validation (126 cells) |
| Reportability items | `CODING_sheets_v2/reportability_summary_final_20261024.json` | T1-03 = 0/16, T3-02 = 0/16, T2-01 = 15/16, T1-01 = 14/16 |
| Kill rule (>= 80 percent headline E2+) | all readings | never triggered |

## Your checks (execute all; add your own if you see a soft spot)

- **V1 Artifact integrity.** `git log --oneline -3` (record HEAD); recompute sha256 of
  `field_audit/corpus_draw_arxiv_v1.snapshot.jsonl` (pinned value
  `e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee`); verify all 42 files in
  `field_audit/pinned_validation_20261025/texts/` against
  `FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv`.
- **V2 Script re-runs.** Run, in order, recording exit codes and diffs:
  `python3 field_audit/nmi_format_check.py --selftest` then without `--selftest` (expect PASS);
  `python3 field_audit/compute_validation_statistics_20261025.py --selftest` then plain (expect
  output identical to the committed `statistics_validation_20261025.json`);
  `python3 field_audit/compute_H3_full_20261025.py` (expect output identical to
  `CODING_sheets_human/H3_READING_20261025.json`); `python3 field_audit/make_figures.py`
  (expect six PNGs regenerated).
- **V3 Independent recount (the most important check).** Write YOUR OWN counting code (do not
  import or reuse the project's scripts) and recount directly from the raw sheets:
  `CODING_sheets_v2/coder_A_E.csv` + `coder_B_E.csv` (primary), `CODING_sheets_validation/coder_A.csv`
  + `coder_B.csv`, `CODING_sheets_human/coder_H.csv`. Recount at minimum: T1-E0 in both corpora;
  the weaker-merge headline statistic (per claim: take the weaker of the two coders' grades at
  the merged headline transition; count E2) for both corpora; H's T2-E2 and T3-E2 counts.
  Compare against the table above.
- **V4 Merge-rule spot check.** Draw 10 random (seed 7) cells; verify merged grade == the weaker
  of A and B in each.
- **V5 Interval check.** Recompute the Wilson 95 percent interval for 10/16 and 26/42 with your
  own implementation; compare to [39, 82] and [46.8, 75.0].
- **V6 Provenance spot check.** Pick 5 validation claims; locate one quoted justification per
  claim from `CODING_sheets_human/coder_H.csv` in the pinned text file; confirm hash match.
- **V7 Chain existence.** Confirm these records exist and are internally consistent with the
  numbers above: `CODING_FINAL_RESULTS_20261024.md` (incl. the A/B erratum),
  `CODING_VALIDATION_RESULTS_20261025.md`, `VALIDATION_CLAIM_TYPE_ADJUDICATION_20261025_RECORD.md`
  (N = 42), `ROBUSTNESS_SURVEY_EXCLUSION_20261025.md` (16 - 1 = 15 erratum included),
  `POSITIVE_CONTROL_PROBE_20261025.md`, `BINDING_RECORD_V3_20261024.md`.

## Rules

1. Read-only: you may run scripts and write YOUR OWN files, but never modify, move, or commit
   any project file. If a script errors, capture the error - do not patch it.
2. Write your own verification code; reusing the project's code for the recount (V3) would
   defeat the check.
3. Record everything: command, exit code, expected, observed, PASS/FAIL. A check you could not
   run is recorded as NOT RUN with the reason - never silently skipped.
4. Questions about what a number MEANS go to the lead; questions about how to run a script are
   answered by the script's own docstring.

## Deliverable

One file, `field_audit/O6_VERIFICATION_REPORT_<YOURNAME>_<DATE>.md`, containing:
- a one-line overall verdict (VERIFIED / VERIFIED WITH FINDINGS / FAILED);
- one section per check V1-V7 with evidence (commands + outputs, or file+line references);
- a findings section: every discrepancy, however small, with its exact reproduction steps;
- your name, date, and the commit HEAD you verified.

## Effort

Half a day to one day. The integrity checks are quick; the independent recount (V3) is the core
of the work.

## Why this matters

This pass is the project's O-6 gate: the advisor has conditioned support for submission on a
non-author recomputation passing. Your findings go verbatim to the advisor; a FAILED verdict
stops submission until resolved. There is no outcome here that is bad for you to report - the
only failure mode is an incomplete check.

## Setup (the lead runs this before handover; the verifier receives the whole folder)

```bash
cd /Users/yyl/Desktop/workshop
git clone /Users/yyl/Desktop/workshop/NMI/NeuroConverge ~/o6_verify/NeuroConverge
cp -r NMI/NeuroConverge/field_audit/pinned_fulltext_20261020 ~/o6_verify/NeuroConverge/field_audit/
cp -r NMI/NeuroConverge/field_audit/pinned_validation_20261025 ~/o6_verify/NeuroConverge/field_audit/
cp -r NMI/NeuroConverge/field_audit/fulltexts ~/o6_verify/NeuroConverge/field_audit/
```

(The pinned text/PDF directories are intentionally untracked in git - hash manifests are the
anchors - so the clone must be completed with those copies. The pilot-era `fulltexts/` folder is
**tracked** at HEAD (22 files) and a fresh clone already carries it; the `cp -r` line for it is
redundant. Corrected 2026-10-25 after the O-6 verification found the original wording wrong. The
coder_H sheets ARE committed; a fresh clone already carries them.)
