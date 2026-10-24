# Coder re-dispatch plan (written 2026-10-24 ~10:30, after the quota failure; fires after 14:48 reset)

State at writing: coder A completed 8 of 16 claims (C003-C021, all three files well-formed in
`CODING_sheets_v2/`); coder B wrote nothing. The 5-hour account quota killed both agents on their runs; it
resets 2026-10-24 14:48. This file makes the re-dispatch mechanical and identical in instructions.

## A - continuation (not a restart)

Resume message to the same coder-A context (or, if the context is gone, a fresh agent with this brief):
continue exactly where you stopped - claims C028, C032, C036, C043, C045, C046, C049, C077 - appending to
your existing three files in `CODING_sheets_v2/` (`coder_A_E.csv`, `coder_A_R.csv`, `headline_A.csv`) under
the identical frozen instructions you already read. Do not re-read or re-grade the eight finished claims; do
not read any other coder's files. Same prohibitions. Same summary format on completion.

## B - full run

Fresh isolated agent, the original dispatch verbatim (all 16 claims, four output files, blind to
`CODING_sheets/`, `CODING_sheets_v2/` and every results document).

## Sequencing (to survive the shared quota)

Dispatch B FIRST and alone; when B lands, dispatch A's continuation. One agent at a time, never parallel -
the quota died on two parallel 16-paper runs. If either agent dies again, check the files before assuming
loss (the pilot precedent: files complete, only the summary died), then continue from the last complete
claim.

## After both land

1. Format validation + the bound scorer on the reportability rows (it refuses any grid/hash violation).
2. E-table merge under the standing weaker-grade rule with the disagreement report and R1's
   matched-neither count.
3. Six outputs + reportability item counts (COND-1: no aggregation beyond per-item; COND-2 caveat attached
   to any cross-tab).
4. Kill rule and headline on the final corpus; the manuscript's number slots fill from these.
