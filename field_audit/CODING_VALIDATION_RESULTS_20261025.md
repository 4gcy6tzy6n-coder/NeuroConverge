# Validation corpus coding results (2026-10-25)

Round: validation_v2 per `VALIDATION_RESUMPTION_20261025.md` (protocol) and
`VALIDATION_ACCEPTANCE_AMENDMENT_20261025.md` (N = 42, owner option a). Coders: two
isolated-context instances of the same AI assistant under the frozen instructions
(`CODING_INSTRUCTIONS_FROZEN.md` + `CODING_OPERATIONS_SUPPLEMENT_VALIDATION_20261025.md`);
mechanical isolation real, error independence NOT claimed; a human coder pass (P0-2 / O-5)
supersedes this round and triggers recomputation by script. Statistics computed by
`compute_validation_statistics_20261025.py` (selftest 4 assertions; weaker-grade merge,
weaker-evidence headline resolution - both rule mutants verified to change output).

## Headline outcomes (the frozen estimand)

| measure | final corpus (n=16) | validation corpus (n=42) |
| --- | --- | --- |
| headline E2+ share | 10/16 = 62.5 pct (CI 39-82) | **26/42 = 61.9 pct (CI 46.8-75.0)** |
| kill rule (80 pct E2+) | not triggered | **not triggered** |
| headline map | T3 15, T2 1 | T3 38, T2 3, T4 1 |
| T1 in-paper E0 | 16/16 | **42/42** |
| T2 controlled (E2) | 2/16 | 9/42 (21.4 pct); E1-only 27/42 (64.3 pct) |
| T3 controlled (E2) | 10/16 (62.5 pct) | 25/42 (59.5 pct) |
| in-paper disagreement | 18/80 = 22.5 pct | 64/210 = **30.5 pct** |
| external disagreement cells | 15 (convention divergence) | 39 |

The preregistered readings all replicate in direction: delegation of biological foundations is
the norm (T1 42/42 E0, matching the pilot's 18/18 and the final corpus's 16/16); controlled
evidence concentrates at the utility transition; the correspondence transition stays
predominantly suggestive-only; the headline statistic lands within 0.6 points of the final
corpus with a materially tighter interval. The kill rule is not triggered on either corpus.

## Honest noise and limitations, on the record

- The two coders disagree on 30.5 percent of in-paper cells (higher than the final corpus's
  22.5 percent), concentrated on T5 (29 cells) and T4 (24), and on the E1/E2 boundary (49 cells
  are A=E1 vs B=E2). Lead spot-checks of boundary cells found honest definitional disagreement
  (both coders cite real comparisons; the weaker-grade merge takes the conservative reading),
  not error - but the rate is the instrument's noise term and is reported as such.
- Both coders are same-model AI instances. This round does NOT substitute for the human-coder
  pass (P0-2 / O-5); the human-supersedure rule stands.
- External layer: 39 disagreement cells; per the preregistered weaker merge these resolve to
  E0. The external-layer convention divergence seen on the final corpus persists here.
- Scope-match is recorded per coder (A 39/42 match, B 34/42); no merged scope statistic is
  computed this round (not part of the frozen validation estimand).
- Six claims are surveys/reviews with no own artifact (flagged by coder A: 1506.03264v1,
  1901.03690v3, 2204.07050v7, 2209.10818v2, 2312.09257v2, 2603.26722v1); graded under the same
  frozen scale as corpus members - the corpus's mixed primary/review composition is carried
  from the draw and is a limitation to state in Methods.
- Inference boundary (unchanged): both corpora are first-query candidate samples; no
  field-level prevalence claim is made anywhere. The validation pass permits the replicated,
  tighter headline reading to be reported, not a field census.

## Artifacts

- Sheets: `CODING_sheets_validation/coder_A.csv` (210 rows), `coder_B.csv` (210 rows),
  `headline_A.csv` / `headline_B.csv` (42 each). Integrity checks (both sheets): row counts,
  claim-set equality with the corpus, grade vocabularies, T5-only scope_match, manifest hash
  match - all pass; quote-authenticity sampling verified against the pinned text layers
  (verbatim hits plus cited-location verification; absence claims verified by probe-miss).
- Statistics: `CODING_sheets_validation/statistics_validation_20261025.json`.
- Manuscript: headline Results sentence, Methods validation paragraph and Discussion noise
  disclosure updated the same day (see git); figure update deferred to the owner's review of
  this record (fig3 gains a validation panel only after that review).
