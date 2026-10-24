# Coding final results on the 16-claim corpus (2026-10-24, evening)

Status: the "after both land" pipeline of `CODER_REDISPATCH_PLAN_20261024.md` is executed end to
end. Every number below comes from a fresh run whose output is quoted or whose artifact is named.
AI-role disclosures: the two coders were isolated-context instances (P4 per the 2026-10-19
authority record); the reportability adjudicator and both merge corrections are the lead (same
model family as the coders - correlated-error limitation disclosed; a human adjudicator supersedes
and triggers one-command recomputation).

## 1. Coder A completion

Coder A's continuation was dispatched by this session under the redispatch plan after the quota
window reset (three launches died on the account's model concurrency limit; the fourth and sixth
found quiet windows). Final state, verified by parse and content validation:

- E grid 16 x 5 = 80 rows, R grid 16 x 11 = 176 rows, headline 16 rows; vocabularies, T1-03
  REFERENCED restriction, T5 scope placement, headline vocabulary and every `provenance_sha256`
  against `PINNING_MANIFEST.csv`: PASS for both coders.
- C045 carries "GENRE: review" on every row, as the frozen survey rule requires.

## 2. Corrections applied to sealed coder rows (ledger: `CODING_sheets_v2/CORRECTION_LEDGER_20261024.md`)

- **C-1**: all 176 of coder B's reportability rows declared the SHA-256 of the extracted text
  layer, not the pinned target PDF (verified 16/16). Corrected file `coder_B_R_corrected_20261024.csv`
  rebinds the field to the registry target digest. No status, pointer or note changed.
- **C-2**: 27 of B's rows left `evidence_pointer` empty while B's own `source_locator` carried the
  search statement; the corrected file copies B's own locator text into the pointer field. No
  judgment content changed.
- **C-3**: 1 of A's rows (C077 T4-02) left `note` empty with the justification in its pointer; the
  corrected file `coder_A_R_corrected_20261024.csv` copies A's own pointer text into the note.
- All originals retained byte-for-byte. The corrections exist because the bound scorer validates
  row schema, source-role binding and hash declaration on every row, and would otherwise refuse.

## 3. Registry successor (B3 v2) and bound-scorer run

The v1 registry binds 18 claims; the final corpus is 16, and the scorer refuses claim-set
mismatch (proven in rehearsal). Successor `review_evidence_v3_20261024/SOURCE_REGISTRY_V2_20261024.json`
(claim-keyed, target digests identical to v1 for all 16 retained claims; supplements/cited empty),
binding record `B3_SOURCE_REGISTRY_BINDING_V2_20261024.md`, canonical digest
`0c9303e3ef3e77adad2ffefcb6b5fce22a039cac7a80359c4c804fd5a50efd58`.

`run_final_scoring_20261024.py` ran the bound v3 scorer on A + B-corrected + 39 adjudication rows:
**SCORER: PASS** (claim-set, complete grid, on-disk hash verification of all 16 pinned PDFs,
registry digest, row schema, adjudication completeness). Output:
`CODING_sheets_v2/reportability_summary_final_20261024.json`.

## 4. Adjudication (39 item-level status disagreements)

Both coders agreed on 137/176 items. The 39 disagreements were adjudicated by the lead under the
bound item criteria and COND-3 (a)-(c), each with a dated rationale in
`CODING_sheets_v2/adjudication_R_20261024.csv`. Outcomes: adopted coder A's status 28 times,
coder B's 11 times. **R1 matched-neither count: 0 of 39.** One factual presence dispute was
resolved against the text (C018 T4-01: COCO detection and ADE20K segmentation experiments are
present; coder B's REPORTED adopted).

## 5. E-merge, headline, six outputs, kill rule

`merge_coder_sheets_v2.py` (the frozen weaker-grade rules, 16-claim form):

- In-paper grade disagreements **18/80 (22.5 pct)**; by transition T5 10, T4 6, T2 2; T1 and T3
  fully agree - the same shape as the rehearsal and the pilot.
- **External-layer convention divergence, final size**: A declared E3/E4 on 15 cells with verified
  routes; B declared none under its no-verification convention; the weaker merge resolves all 15
  to the lower grade. Methods disclosure stands. Consequence for the narrative: the pilot's
  "T1 external 14/18 E3" two-layer restatement was a single-coder pilot-sheet finding and is not
  re-derived as a merged statistic on the final corpus, where the merged external layer is E0
  throughout. This difference is disclosed, not hidden.
- Headline disagreements 2/16 (C049, C077), resolved by the frozen weaker-evidence rule; the
  merged headline map is **15 x T3 + 1 x T2** (C077 -> T2).

`compute_statistics.py --sheet A --sheet B --sheet merged --headline headline_merged.csv
--register corpus_draw_arxiv_v1_register.csv --out CODING_sheets_v2/statistics_final_20261024.json`
(selftest passed first, including its named refusal demonstrations):

- **T1 in-paper: 16/16 E0 on A, B and merged** - the pilot's headline negative replicates on the
  final narrowed corpus.
- T2 merged: E1 12, E0 2, E2 2 - the correspondence content remains the least-evidenced
  content transition, as in the pilot.
- T5 scope-match rate: 35/48 = 72.9 pct (48 = 16 claims x 3 sheets).
- Headline E0/E1 share (merged): 6/16 = 37.5 pct (A 37.5, B 31.25).
- **Kill rule: NOT TRIGGERED** - E2+ on the headline transition in 10/16 = 62.5 pct, below the
  80 pct bar of the frozen rule (prereg section 10). The audit proceeds to drafting.

## 6. What is and is not licensed now

Licensed: the frozen six outputs and reportability summaries above, computed under bound
instruments on the admitted 16-claim corpus, with all corrections and adjudications disclosed.
The manuscript's number slots can now be filled from these artifacts and from nothing else.

Not licensed: any pooled number mixing pilot (18) and final (16) corpora; any field-percentage
claim beyond this quota sample (Wilson intervals apply); any external-layer E3 statement on the
final corpus (the merged external layer is E0 by rule); any aggregation of reportability items
into a score (COND-1); any cross-tab without the standing caveat (COND-2). Human gates still
open: the human-coder supersure pass (P0-2) and non-author verification remain owner-side.

## 7. File inventory (this round)

Created: `CODING_sheets_v2/` additions (corrected A/B R sheets, `adjudication_R_20261024.csv`,
`reportability_summary_final_20261024.json`, `merged_E.csv`, `headline_merged.csv`,
`statistics_final_20261024.json`, `CORRECTION_LEDGER_20261024.md`),
`review_evidence_v3_20261024/` (registry V2 + binding record), `run_final_scoring_20261024.py`,
`merge_coder_sheets_v2.py`, this record. Modified by append-only coder work:
`coder_A_E.csv`, `coder_A_R.csv`, `headline_A.csv`. No frozen document was edited.
