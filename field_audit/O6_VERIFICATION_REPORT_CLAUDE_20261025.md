# O-6 non-author verification report

**Verifier:** Claude Code (AI assistant, Anthropic), acting as the lead's delegated non-author verifier.
I authored none of this project's instruments, scripts, coding sheets, or manuscript text. This is an
AI-conducted mechanical verification, not a human sign-off; if the O-6 gate requires a human
counter-signature, this report is the machine-checkable half and should be countersigned by a human
non-author before the gate closes.

**Date:** 2026-10-25 (CST)　**Commit verified (HEAD):** `0dbf8acc2f6711826417075ff2a8d0cd4c17ca45`
**Environment:** macOS, Python 3.12.13, matplotlib 3.10.9, pytest 9.1.1, `pdftotext` available.
**Verification copy:** `~/o6_verify/NeuroConverge` (fresh clone of the repository at HEAD + the
untracked pinned directories copied as the assignment's setup prescribes). Project files were treated
as read-only; all re-runs happened in the clone, and every file a script overwrote was compared
against a pre-run backup and restored. My own code and logs are in `~/o6_verify/work/`.

## Overall verdict

**VERIFIED WITH FINDINGS.** All nine load-bearing numbers in the assignment's target table reproduce
from the raw sheets (the primary headline interval matches after the stated integer rounding; every
other interval matches to one decimal). Five findings, none of which changes a reported number, but two
of which (F1, F2) undermine the manuscript's "one command / scripts committed" reproducibility claim and
should be fixed before submission.

## Target table: expected vs observed

| # | claim | expected | observed | verdict |
| --- | --- | --- | --- | --- |
| 1 | Primary headline E2+ (AI weaker-merge) | 10/16 = 62.5 %, Wilson 95 % CI [39, 82] | 10/16 = 62.5 %, CI [38.6, 81.5] -> [39, 82] | PASS |
| 2 | Validation headline E2+ (AI weaker-merge) | 26/42 = 61.9 %, CI [46.8, 75.0] | 26/42 = 61.9 %, CI [46.8, 75.0] | PASS |
| 3 | T1 in-paper E0 | 16/16 primary; 42/42 validation | 16/16; 42/42 | PASS |
| 4 | Human reading (coder H) headline E2+ | raw H 5/16 = 31.2 %, 20/41 = 48.8 %; weaker(H, AI) 4/16 = 25.0 %, 19/41 = 46.3 % | all four reproduce exactly | PASS |
| 5 | H asymmetry (T2-E2 vs T3-E2) | raw H primary 5/16 vs 4/16; validation 6/42 vs 19/42 | exactly as stated | PASS |
| 6 | In-paper disagreement | 18/80 = 22.5 % primary; 64/210 = 30.5 % validation | 18/80; 64/210 | PASS |
| 7 | H vs AI-merge agreement | 61.2 % primary (80 cells); 58.7 % validation (126 cells) | 49/80 = 61.2 %; 74/126 = 58.7 % | PASS |
| 8 | Reportability items | T1-03 0/16, T3-02 0/16, T2-01 15/16, T1-01 14/16 | exactly as stated | PASS |
| 9 | Kill rule (>= 80 % headline E2+) | never triggered | max observed reading 62.5 % (AI primary); all others lower | PASS |

Additional verified values not in the assignment table: reading 2b (weaker of H and AI merge) headline
E2+ = 4/16 = 25.0 % [10.2, 49.5] primary and 19/41 = 46.3 % [32.1, 61.3] validation; the A/B
headline-map erratum (A 5/16, B 6/16); the H2 embedded control layer (exactly the 10 named
fully-agreed claims); the bound-scorer pipeline (identical outputs; 24 tests pass).

---

## V1 - Artifact integrity

Commands run in `~/o6_verify/NeuroConverge`.

- `git log --oneline -3` -> HEAD `0dbf8ac`, then `5dc70b0`, `3c4811c` (recorded above).
- `shasum -a 256 field_audit/corpus_draw_arxiv_v1.snapshot.jsonl`
  -> `e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee`, exactly the pinned value.
- Manifest check of all 42 validation text layers against
  `pinned_validation_20261025/FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv` (`text_sha256`):
  **42 rows, 42 OK, 0 mismatch, 0 missing**; directory and manifest claim sets are identical.
- Extra: all 42 validation **PDFs** also match `pdf_sha256` (42/42); 18 primary PDFs are present and
  match the primary manifest (19 rows: 16 final claims + 2 excluded candidates + 1 withdrawn record
  whose PDF is 404 by design, `2301.02809v2`).

Verdict: **PASS**.

## V2 - Script re-runs

All commands were run from the repository root of the clone; exit codes and diffs recorded.

| run | exit | observed | verdict |
| --- | --- | --- | --- |
| `python3 field_audit/nmi_format_check.py --selftest` | 0 | `SELFTEST PASS (6 assertions)` | PASS |
| `python3 field_audit/nmi_format_check.py` | 0 | `NMI ARTICLE FORMAT CHECK: PASS` — 3439/3500 main words, abstract 149/150, 6/6 figures, 21/50 refs; one non-blocking WARN about the draft `## Introduction` heading | PASS |
| `python3 field_audit/compute_validation_statistics_20261025.py --selftest` | 0 | `SELFTEST PASS (4 assertions)` | PASS |
| `python3 field_audit/compute_validation_statistics_20261025.py` | 0 | regenerated JSON **byte-identical** to the committed `CODING_sheets_validation/statistics_validation_20261025.json` (`diff` empty) | PASS |
| `python3 field_audit/compute_H3_full_20261025.py` | 0 | output **not identical**: the regenerated JSON lacks the top-level `reading2b_weaker_merge_H_vs_AI` block. All 8 other top-level keys are identical. See F1. | **FAIL (F1)** |
| `python3 field_audit/make_figures.py` | 0 | six PNGs regenerated; all six byte-identical to the pre-run copies; `git status` clean afterwards | PASS |

Extra re-runs (not in the V2 list, run because they back manuscript claims):

- `compute_statistics.py --selftest` passes; the full primary-statistics command produces a JSON
  **semantically identical** to `CODING_sheets_v2/statistics_final_20261024.json` (only JSON object key
  order differs, which is not meaningful).
- `fill_results_numbers.py` reproduces every Results number in the manuscript (T1 16/16, T2 2/12/2,
  T3 2/4/10, T4 6/9/1, T5 1/11/4, headline 10/16 = 62.5 %, E0/E1 6/16 = 37.5 %, disagreement 18/80 =
  22.5 %, all 11 reportability items, kill rule not triggered).
- `run_final_scoring_20261024.py` cannot run in the clean clone (F2); after supplying the three
  untracked bound artefacts it exits 0 and reproduces `adjudication_R_20261024.csv` and
  `reportability_summary_final_20261024.json` **byte-identically**; the bound scorer's test file passes
  **24 tests (7 subtests)**.
- `robustness_survey_exclusion_20261025.py` cannot run in the clean clone (F2); after supplying its
  untracked input it exits 0 and reproduces `ROBUSTNESS_SURVEY_EXCLUSION_20261025.json`
  **semantically identically**.

## V3 - Independent recount (own code, no project imports)

My recount is in `~/o6_verify/work/v3_recount.py`; it reads only the raw CSV sheets and implements the
weaker-grade rule (`min` on E0 < E1 < E2) and the headline rule itself. Per-claim detail is in
`~/o6_verify/work/v3_recount.json`.

**Primary corpus (16 claims, 80 cells/coder).** Recomputed merged distribution:

| transition | E0 | E1 | E2 |
| --- | --- | --- | --- |
| T1 | 16 | 0 | 0 |
| T2 | 2 | 12 | 2 |
| T3 | 2 | 4 | 10 |
| T4 | 6 | 9 | 1 |
| T5 | 1 | 11 | 4 |

- T1 E0 = **16/16**.
- Headline map = **15 x T3 + 1 x T2** (C077 -> T2, using the committed primary merge's tie rule);
  headline E2+ = **10/16 = 62.5 %**.
- In-paper disagreement = **18/80 = 22.5 %** (T5 10, T4 6, T2 2; T1/T3 agree).

**Validation corpus (42 claims, 210 cells/coder).** Recomputed merged distribution:

| transition | E0 | E1 | E2 |
| --- | --- | --- | --- |
| T1 | 42 | 0 | 0 |
| T2 | 6 | 27 | 9 |
| T3 | 6 | 11 | 25 |
| T4 | 16 | 26 | 0 |
| T5 | 6 | 36 | 0 |

- T1 E0 = **42/42**.
- Headline map = **T3 38, T2 3, T4 1**; headline E2+ = **26/42 = 61.9 %**.
- In-paper disagreement = **64/210 = 30.5 %**; external-layer disagreements = **39**.

**Coder H (raw reading).** 206 grade rows + 58 headline rows.

- Primary: T1 E0 16/16; T2 E0/E1/E2 = 1/10/5; T3 = 3/9/4; T4 = 6/7/3; T5 = 8/7/1.
  Headline E2+ = **5/16 = 31.2 %** [14.2, 55.6].
- Validation: T2 = 2/34/6; T3 = 4/19/19; T5 = 17/17/8.
  Headline E2+ = **20/41 = 48.8 %** [34.3, 63.5]; one claim (`2204.07050v7`, headline T1) is outside
  the H2 grade scope and is correctly skipped, giving the 41 denominator.
- Asymmetry: primary T2-E2 **5/16** vs T3-E2 **4/16** (T2 > T3); validation **6/42** vs **19/42**
  (T3 > T2). Exactly as recorded.

**Disagreement-handled reading 2b** (weaker of H and AI merge; independently recomputed because the
committed generator does not emit it — F1):

- Primary headline E2+ = **4/16 = 25.0 %** [10.2, 49.5]; T2-E2 **1/16**, T3-E2 **4/16**.
- Validation headline E2+ = **19/41 = 46.3 %** [32.1, 61.3]; T2-E2 **2/42**, T3-E2 **19/42**.

**Disagreement audit.**

- H vs AI-merge per-cell grade agreement: **49/80 = 61.2 %** primary; **74/126 = 58.7 %** validation.
- AI-disputed cells: primary 18 -> H with A 7, with B 4, neither 7; validation 40 -> with A 20,
  with B 6, neither 14. Reproduces the record.
- Headline-map agreement as computed by the committed H3 script: 51/58. Against the committed primary
  map it is 52/58; see F3.

**A/B erratum check.** From each coder's own headline map and own grades: coder A = 5/16 E0/E1
(31.25 %, claims C008, C028, C036, C045, C077); coder B = 6/16 (37.5 %, those plus C049). This matches
the erratum in `CODING_FINAL_RESULTS_20261024.md` exactly; the merged value (6/16 = 37.5 %) is unaffected.

**H2 embedded control layer.** The set of validation claims on which A and B agree on all of T2, T3 and
T5 is exactly the 10 claims named in the protocol (set equality verified, no extra, none missing).

## V4 - Merge-rule spot check

`random.seed(7)`; universe = the 80 primary (claim, transition) cells, sorted; `random.sample(..., 10)`.
Every sampled merged grade equals the weaker of A and B:

| cell | A | B | weaker | merged file | match |
| --- | --- | --- | --- | --- | --- |
| C028 T2 | E1 | E1 | E1 | E1 | yes |
| C010 T5 | E1 | E2 | E1 | E1 | yes |
| C036 T1 | E0 | E0 | E0 | E0 | yes |
| C006 T2 | E1 | E1 | E1 | E1 | yes |
| C006 T5 | E1 | E2 | E1 | E1 | yes |
| C046 T4 | E1 | E2 | E1 | E1 | yes |
| C008 T3 | E0 | E0 | E0 | E0 | yes |
| C032 T2 | E1 | E1 | E1 | E1 | yes |
| C006 T3 | E2 | E2 | E2 | E2 | yes |
| C045 T5 | E1 | E1 | E1 | E1 | yes |

The validation corpus has no committed merged sheet (the merge lives in the statistics JSON); its
weaker-merge counts were independently reproduced in V3 instead.

Verdict: **PASS** (10/10).

## V5 - Interval check (own Wilson implementation)

Two-sided Wilson score interval, z = 1.959963985:

| quantity | k/n | point | Wilson 95 % (1 dp) | rounded |
| --- | --- | --- | --- | --- |
| Primary headline E2+ | 10/16 | 62.5 % | [38.6, 81.5] | [39, 82] |
| Validation headline E2+ | 26/42 | 61.9 % | [46.8, 75.0] | [47, 75] |
| H raw primary | 5/16 | 31.2 % | [14.2, 55.6] | [14, 56] |
| H raw validation | 20/41 | 48.8 % | [34.3, 63.5] | [34, 64] |
| weaker(H, AI) primary | 4/16 | 25.0 % | [10.2, 49.5] | [10, 50] |
| weaker(H, AI) validation | 19/41 | 46.3 % | [32.1, 61.3] | [32, 61] |

The two assignment intervals match exactly: primary rounds to [39, 82]; validation is [46.8, 75.0].

Verdict: **PASS**.

## V6 - Provenance spot check

Five validation claims, first in sorted order; for each, one human-coded justification was located in
the pinned text layer, and the text file's SHA-256 was checked against the manifest and against the
row's declared `provenance_sha256`.

| claim | text file hash vs manifest | quote located (normalised) | declared hash matches manifest |
| --- | --- | --- | --- |
| 1505.07814v2 | match (`836f1ca5…`) | yes (T2) | yes |
| 1506.03264v1 | match (`0451248e…`) | yes (T2) | yes |
| 1511.04484v2 | match (`06c5e26a…`) | yes (T2) | yes |
| 1702.05596v1 | match (`9d0214fc…`) | yes (T2) | yes |
| 1801.02797v1 | match (`8c4caf11…`) | yes (T2) | yes |

Quote matching used Unicode NFKC normalisation, curly-quote/dash folding and whitespace collapsing.
Primary extension (not required by V6): five primary H quotes (`1711.10563v2`, `1811.09699v1`,
`1903.12517v1`, `2107.14654v1`, `2203.14679v1`) were also located in the coder's text layers (5/5) and
against `pdftotext` output of the pinned PDFs (4/5 exact; the fifth matched the first 40 characters,
then diverged at a truncated hyphenated word "be-"/"between" — a normalisation artefact, not a missing
quote). The full 206/206 quote claim of the O-5 record was **not** re-verified; see "Not run".

Verdict: **PASS** for the five required claims.

## V7 - Chain existence and internal consistency

All six named records exist at HEAD and are consistent with the target numbers:

- `CODING_FINAL_RESULTS_20261024.md`: 18/80 (22.5 %) at line 60; T1 16/16 at line 75; merged headline
  map 15 x T3 + 1 x T2 at line 69; the A/B erratum and 10/16 = 62.5 % at lines 80–88. The erratum's
  per-coder values were independently reproduced (V3).
- `CODING_VALIDATION_RESULTS_20261025.md`: lines 16–23 carry 26/42 = 61.9 % [46.8, 75.0], T1 42/42,
  64/210 = 30.5 %, external disagreement 39. All independently reproduced.
- `VALIDATION_CLAIM_TYPE_ADJUDICATION_20261025_RECORD.md`: line 10 names
  `corpus_validation_v2_adjudicated.csv` (N = 42); line 35 records 35 drawn-kept + 7 replacements. The
  corpus file has exactly 42 rows.
- `ROBUSTNESS_SURVEY_EXCLUSION_20261025.md`: the erratum at lines 3–15 corrects 16 - 2 = 15 to
  16 - 1 = 15; lines 47–51 give 10/15 = 66.7 %, 25/36 = 69.4 %, headline 66.7 %/72.2 %. The committed
  JSON matches these values and was regenerated semantically identically once its untracked input was
  supplied (F2).
- `POSITIVE_CONTROL_PROBE_20261025.md`: line 46 records 3/3 at T2 = E2; `probe_coding.csv` has the
  three nominated claims at T2 = E2. The probe's pinned PDFs/texts are not in a clean clone (F2 note).
- `BINDING_RECORD_V3_20261024.md`: lines 9–12 and 23–28 freeze the scorer/test/registry hashes. The
  three named files' SHA-256 values match the working-tree copies exactly:
  scorer `b7fa04ab…6455e`, tests `c094856b…9829c`, template `77dcda1a…4db6e`. However, the three files
  are untracked and absent from the clean clone (F2).

Additional chain checks: `fill_results_numbers.py` reproduces every Results number; `nmi_format_check.py`
passes; the bound-scoring pipeline reproduces its committed outputs and its 24 tests pass.

Verdict: **PASS on existence and numerical consistency**, with the packaging gap F2.

---

## Findings

### F1 (high) — The committed H3 script does not regenerate the committed H3 JSON

**Assignment expectation:** V2 says `python3 field_audit/compute_H3_full_20261025.py` should produce
output identical to `CODING_sheets_human/H3_READING_20261025.json`.

**Observed:** exit 0, but the regenerated file lacks the top-level `reading2b_weaker_merge_H_vs_AI`
block. The committed file has 9 top-level keys; the regenerated file has 8. The other 8 keys are
identical. File hashes: committed `53175756da043aaf9e92d30509d45c8f2edd33ca31571b84b8936b5b0c39787f`;
regenerated `cb7bcd85391dbe4e4f5a4d260e8e4081772ac719d7211fda9ff35e37e8a40bdc`.

**Reproduction:**
```bash
cd ~/o6_verify/NeuroConverge
cp field_audit/CODING_sheets_human/H3_READING_20261025.json /tmp/h3.json
python3 field_audit/compute_H3_full_20261025.py
diff -u /tmp/h3.json field_audit/CODING_sheets_human/H3_READING_20261025.json
# -> 80 deleted lines, all under "reading2b_weaker_merge_H_vs_AI"
```

**Cause (from history, not repaired):** commit `5dc70b0` appended 80 lines to the JSON and 46 lines to
`O5_H3_RESULTS_20261025.md`, but did not modify `compute_H3_full_20261025.py`.

**Impact:** a routine re-run silently deletes the preregistered disagreement-handled reading
(headline 25.0 %/46.3 %; T2 vs T3 = 1/16 vs 4/16 and 2/42 vs 19/42). The values themselves are correct
— I recomputed them independently from the raw sheets (V3) — but the "one command" reproduction claim
is false for this file. The manuscript's Methods sentence that analysis scripts are committed with the
article is not satisfied for this block.

**Suggested action (for the lead, not done here):** extend `compute_H3_full_20261025.py` to compute and
emit `reading2b`, commit it, and re-run; or commit a separate generator and reference it in
`O5_H3_RESULTS_20261025.md`.

### F2 (high, submission packaging) — The clean verification copy cannot re-run two load-bearing analyses

The assignment's setup (clone + copy untracked pinned dirs) produces a copy in which:

1. **The bound scorer, its tests, and the bound template are absent.** `git ls-files --error-unmatch`
   returns "not a tracked file" for:
   - `field_audit/reportability_score_candidate_v3_candidate.py` (the bound instrument of record;
     SHA-256 `b7fa04ab…6455e` in `BINDING_RECORD_V3_20261024.md`),
   - `field_audit/test_reportability_score_candidate_v3_candidate.py` (`c094856b…9829c`),
   - `field_audit/REPORTABILITY_CODING_TEMPLATE_v2_SOURCE_REGISTRY_CANDIDATE_2026-10-20.csv`
     (`77dcda1a…4db6e`).

   `git log --all -- <each path>` is empty, so they have never been committed. In the clean clone,
   `python3 field_audit/run_final_scoring_20261024.py` fails at line 15 with
   `ModuleNotFoundError: No module named 'reportability_score_candidate_v3_candidate'`. After copying
   the three files from the working tree into the clone, the script exits 0 and reproduces
   `adjudication_R_20261024.csv` and `reportability_summary_final_20261024.json` byte-identically, and
   `python3 -m pytest -q test_reportability_score_candidate_v3_candidate.py` passes 24 tests (7
   subtests). So the instrument is correct; it is simply not in version control. This directly
   contradicts the manuscript's "Software: Python 3 analysis scripts committed with the article"
   (`MANUSCRIPT/ANALYSIS_DRAFT.md:254`) and makes the SI's "executable bound scorer" chain
   unverifiable from a clone.

2. **The R2a robustness script's input is absent.** `python3 field_audit/robustness_survey_exclusion_20261025.py`
   fails with `FileNotFoundError: field_audit/CLAIM_TYPE_ADJUDICATION_20261020.csv`; that CSV is
   untracked (`git ls-files` has no record of it). After copying it from the working tree, the script
   exits 0 and reproduces the committed JSON semantically identically. This is the advisor-closed R2a
   analysis, so its reproducibility should not depend on an untracked file.

3. **Related, lower severity:** the positive-control probe's PDFs/texts are untracked (only
   `MANIFEST.csv`, `NOMINATIONS.csv`, `probe_coding.csv` are tracked), and the prescribed setup does not
   copy them. The probe's recorded grades are inspectable, but the 3/3 claim cannot be re-derived from
   the verification copy without obtaining the papers. The hash manifests do anchor the source bytes.

**Suggested action:** commit the three bound artefacts and `CLAIM_TYPE_ADJUDICATION_20261020.csv`
(exact bytes, then re-check the frozen hashes), and decide whether probe texts belong in the deposited
artifact or are covered by their manifest. No number changes.

### F3 (medium, reporting consistency) — The H3 record's "headline map agreement 51/58" is computed against a different primary headline map than the committed one

The committed primary map is `CODING_sheets_v2/headline_merged.csv`; row `C077,T2`, with the note
"chose weaker of A=T2:E1 B=T3:E1", and `CODING_FINAL_RESULTS_20261024.md:69` records the map as
15 x T3 + 1 x T2 (C077 -> T2). Coder H's own headline for `1811.09699v1` (C077) is **T2**
(`headline_H.csv:17`), so it agrees with the committed map.

The H3 script, however, re-derives the primary map and applies the validation tie rule ("T3 if one
candidate is T3") at `compute_H3_full_20261025.py:48`, producing **T3** for C077. It therefore reports
**51/58** headline-map agreement, whereas against the committed map the agreement is **52/58**.
All validation-map assignments agree between the two derivations; C077 is the only difference.

**Impact:** one line in `O5_H3_RESULTS_20261025.md` section 4 is off by one relative to the committed
primary record. The per-cell agreement figures (61.2 % / 58.7 %) and the disputed-cell counts are
unaffected; the raw-H and reading-2b headline statistics use H's own map and are unaffected.

**Suggested action:** compute the headline-map agreement against `headline_merged.csv` (and the
validation map as committed), or state explicitly which non-committed map the 51/58 refers to. If the
H3 script is to be the single source, reconcile the tie rule with the primary merge record (F4).

### F4 (low, methodological consistency) — The headline tie-break rule differs between the two corpus implementations

`merge_coder_sheets_v2.py:84` resolves a tie between the coders' headline transitions in favour of
**coder A's transition**; `compute_validation_statistics_20261025.py:56-57` resolves a tie in favour of
**T3 if one candidate is T3**. `compute_H3_full_20261025.py` applies the validation rule to both
corpora, which is the cause of F3.

The divergence is immaterial to every E2 count in the record: the only primary tie (C077) has E1 on
both candidate transitions, and the validation ties that differ (e.g. `2503.11299v8`, `2406.15488v1`)
have the same grade on both candidates; `2204.05682v1` is E2 on both. I confirmed the headline E2 counts
are 10/16 and 26/42 under either rule. Still, a single frozen tie rule should be documented for the
successor instrument.

### F5 (low, setup documentation) — The assignment's setup note misstates the track status of `fulltexts/`

`O6_VERIFIER_ASSIGNMENT_20261025.md:105` says the pinned text/PDF directories and the pilot-era
`fulltexts/` folder are intentionally untracked. In fact `field_audit/fulltexts/` is **tracked** (22 files
at HEAD) and a fresh clone already carries it; only the pinned directories are untracked. The extra
`cp -r` is unnecessary. During this run the initial copy left one pilot PDF modified in the clone
(identical size, different bytes); a direct copy corrected it, and the final clone has no tracked
modifications. No effect on any check. Suggest correcting the setup note.

---

## Not run, and why

- **Full 206-quote provenance re-verification.** V6 requires five validation claims; I did those plus
  five primary claims against the text layers and `pdftotext` output. The O-5 record's 206/206 claim is
  therefore partially spot-checked, not fully re-verified.
- **External E3/E4 citation-route verification.** The coder sheets contain external citations; checking
  each against its published source is a separate literature task, not part of V1-V7.
- **Re-download / re-draw from arXiv.** The assignment verifies the frozen artifacts; I checked the
  snapshot hash and the pinned bytes, not network retrieval. The draw scripts were not re-run.
- **Visual re-approval of the six figures.** I verified that `make_figures.py` regenerates the six PNGs
  byte-identically; I did not redo the visual acceptance review.
- **Full re-derivation of every H3 JSON field from an independent implementation.** I re-derived the
  headline statistics, distributions, agreement, disputed cells and reading 2b; the grade-transition
  matrices were spot-checked through the same raw counts but not independently rebuilt cell by cell.

## Verifier's statement

I verified; I did not repair. No project file was modified, moved, or committed. The clone's tracked
tree was clean at the end of the run; every script-overwritten file was restored to its committed bytes.
The findings above are recorded for the lead and the advisor verbatim; a FAILED verdict was not reached
because every load-bearing number reproduces, but F1 and F2 should be resolved before the manuscript's
reproducibility claims are relied upon in review.

**Claude Code (AI assistant)** — 2026-10-25 21:05 CST — HEAD `0dbf8acc2f6711826417075ff2a8d0cd4c17ca45`

---

## Resolution appendix (2026-10-25, post-report)

The findings above are the as-found record and are not deleted. The verifier's statement above
describes the as-found run; the resolutions below were performed after that report, at the lead's
direction, by the lead's office. On the lead's instruction (decisions 1A-5A), the findings were
resolved and recorded in `O6_FINDINGS_RESOLUTION_20261025.md`. Resolution commit:
`253507e9ef2668826ac9d62c339c4f90721a1bcc` on branch `o6-findings-resolution-20261025`.

- **F1 resolved:** `compute_H3_reading2b_20261025.py` now generates the reading 2b block. The chain
  `compute_H3_full_20261025.py` + `compute_H3_reading2b_20261025.py` reproduces
  `H3_READING_20261025.json` byte-for-byte (SHA-256
  `53175756da043aaf9e92d30509d45c8f2edd33ca31571b84b8936b5b0c39787f`); the frozen script was not
  edited. A dated supplement was appended to `O5_H3_RESULTS_20261025.md`.
- **F2 resolved:** the bound scorer, its tests, the bound template, and
  `CLAIM_TYPE_ADJUDICATION_20261020.csv` are committed at `253507e` with the bytes verified against
  `BINDING_RECORD_V3_20261024.md`. In a clean clone of `253507e`, `run_final_scoring_20261024.py`
  and `robustness_survey_exclusion_20261025.py` both exit 0 and reproduce their committed outputs
  (byte-identical / semantically identical), and the bound-scorer tests pass 24/24 (7 subtests).
- **F3/F4 resolved by dated correction:** canonical headline-map agreement against the committed
  primary map is **52/58** (primary 16/16, validation 36/42); the H3-script variant is 51/58, with
  C077 / `1811.09699v1` the only divergence. `compute_H3_headline_agreement_20261025.py` reproduces
  both variants and writes the committed correction record. The tie-break divergence is recorded for
  the successor instrument; no current map or number is changed retroactively.
- **F5 resolved:** the O-6 assignment now states correctly that `field_audit/fulltexts/` is tracked at
  HEAD and only the pinned directories are untracked.
- **No load-bearing number changed.** The target table in this report remains the verified record.
- **O-6 status:** AI non-author verification complete; human non-author counter-signature pending
  (`O6_HUMAN_COUNTERSIGN_REQUEST_20261025.md`). The lead should merge the resolution branch and send
  the report, resolution record, and signed countersignature to the advisor.
