# Validation corpus acceptance amendment (dated; owner disposition O-8 option a)

Date: 2026-10-25. Owner answer to disposition O-8 (packaged earlier today): **"a"** - accept
N = 42 under a dated amendment. This record is the amendment; the declaring document
(`VALIDATION_CORPUS_RULE_20261023.md`) stands unedited.

## Amendment

The validation-corpus rule's acceptance row

| element | was | now |
| --- | --- | --- |
| size acceptance | 45-75 after replacements | **40-75 after replacements** |

Reason, on the record: the 45 floor was frozen on 2026-10-23 against the pooled 22-query pool
(1,538 eligible candidates). The owner's 2026-10-20 scope ruling (first-query only) postdates
the rule's pool assumption and shrinks the eligible pool to 139 (bands 14/31/94). Under the
unchanged replacement mechanics the first-query maximum is 42: three strata have no same-stratum
spare. The floor is amended once, to 40, with the composition facts recorded in
`VALIDATION_RESUMPTION_20261025.md` and `VALIDATION_CLAIM_TYPE_ADJUDICATION_20261025_RECORD.md`;
no other rule parameter moves (bands 20/20/20 target >=8 required, family cap 4, category cap 6,
fetch_rank order, pilot-disjointness, two-coder coding, weaker-grade merge, kill-rule
recomputation all unchanged).

## Effect

- The validation corpus is FROZEN at **N = 42**: `corpus_validation_v2_adjudicated.csv`
  (35 drawn-kept + 7 stratum-matched replacements, bands 9/16/17), texts pinned and re-hash
  verified in `pinned_validation_20261025/`.
- The coding stop is LIFTED: two isolated-context coders under the frozen instructions
  (E-grade layer, in-paper and external columns, headline map; no reportability layer this
  round - scope frozen in `VALIDATION_RESUMPTION_20261025.md` section 4).
- After both coders: lead adjudication of disagreements (weaker-grade resolution, matched-neither
  count), merge, then the kill-rule and headline recomputation on this corpus, per the frozen
  protocol.

## Inference reminder (carried unchanged)

Field-level wording, if any, requires this validation corpus and its kill-rule check; the
validation corpus does not retroactively convert pilot or final-corpus numbers into
field-level claims.
