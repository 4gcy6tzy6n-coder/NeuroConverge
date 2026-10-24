# Pipeline rehearsal on the 8 doubly-coded claims (2026-10-24, non-final by construction)

**Status: rehearsal only.** Coder A's continuation (claims C028-C077) waits on the account quota window;
coder B is complete and coder A's batch 1 covers the same 8 claims. This record rehearses the merge and
scoring path on that overlap so the final run, once A lands, is one command with no surprises. No number
here is a result; nothing enters the manuscript.

## E-table merge rehearsal (40 doubly-coded cells)

- In-paper disagreement **8/40 (20.0 percent)** - identical to the pilot rate; T5 carries 6 of 8 (the
  linkage-strength reading is the subjective one), T4 one, T2 one; T1 and T3 fully agree.
- **Headline maps agree on all 8 common claims** (all T3) - unlike the pilot's 6/18 splits. Stability to
  watch, not to bank.
- **External-layer convention divergence, confirmed and named**: A claimed E3 on 3 cells (with citation
  routes); B records E0 throughout under its declared no-verification convention. The weaker-grade merge
  resolves these to E0 mechanically, and the divergence goes to Methods as a disclosed convention difference
  between coders - B's is the stricter, protocol-faithful reading (E3/E4 require verified citations; an
  isolated coder holding only pinned texts cannot verify).

## Reportability format rehearsal

- Both coders' R tables share the bound 15-field header exactly; combined rows so far (A 88 + B 176):
  REPORTED 114 / PARTIAL 107 / NOT_REPORTED 43 / REFERENCED 0.

## Bound-scorer refusal test (instrument check, not a rehearsal of numbers)

Called on the current incomplete state (16 claims expected, 8 single-coder), the bound scorer **refused by
name** at the first gate (`source registry claim IDs must exactly match the sampled claims`) - and the
single-coder grid refusal follows in its validation chain. The instrument can see the incomplete-grid error
class; a green run on the final tables will therefore mean the grid was complete, not that the check was
absent.

## What fires when A lands

1. Grid completion check (80 E rows each; 176 R rows each; 16 headline rows each).
2. `summarize_reportability` with the real registry (source registry built from the coders' T1-03 source
   rows per the bound template) and the frozen expected digest.
3. E-merge under the weaker-grade rule with the R1 matched-neither count and the external-layer disclosure.
4. Six outputs + per-item reportability counts; kill rule and headline on the final corpus.
5. Manuscript number slots fill; nothing before that.
