# Validation corpus claim-type adjudication record (2026-10-25)

Authority: `VALIDATION_RESUMPTION_20261025.md` (P0-3 resumption, Gate 0.5 RUN); criterion and
procedure per `AUDIT_PREREGISTRATION_v1_FROZEN.md` section 3, executed as the pilot's
`CLAIM_TYPE_ADJUDICATION_20261020` pass. Single first pass by an isolated reader agent
(incremental writes), then lead verification of every exclusion and replacement; both passes are
recorded below. The first-pass CSV stands unedited (`VALIDATION_CLAIM_TYPE_ADJUDICATION_20261025.csv`);
the merged lead-verified outcome is `VALIDATION_CLAIM_TYPE_ADJUDICATION_FINAL_20261025.csv`
(59 rows: 46 drawn + 7 adopted replacements + 5 screened replacement candidates + 1 spare);
the corpus list is `corpus_validation_v2_adjudicated.csv` (N = 42).

## Criterion as operationally applied (calibrated to the pilot's own decisions)

The pilot's six ineligible precedents ALL fail on the same element: no biological mechanism
identified ("brain-inspired model without a stated basis", "broad claims, no specific
mechanism"). No pilot case with a stated biological basis was excluded. The operative rule is
therefore: TITLE_ABSTRACT_ELIGIBLE iff the title/abstract (1) names a biological structure,
circuit, plasticity rule, coding principle or connectome at any granularity from "cortical
networks" to "hippocampal-prefrontal dual memory" (the words "brain-inspired" alone never
qualify), and (2) claims an artificial-capability improvement on that basis (hedged or
prospective claims qualify; evidence strength is the E-grading's job, not the screen's).

## Outcome

- First pass: 30 eligible / 16 ineligible. Lead verification: 5 exclusions OVERTURNED to
  eligible (1901.03690v3, 1506.03264v1, 2204.07050v7, 2312.09257v2, 2210.16530v1 - each names a
  specific mechanism; overturn reasons recorded per row), 11 confirmed.
- Replacement scan (frozen rule: within band x mechanism family x primary category, fetch_rank
  order): 18 candidates screened by the lead (full abstracts read). 7 adopted, 4 failed the
  criterion (three HDC-family papers whose only biological anchor is "mimics brain cognition" -
  consistent with the drawn HDTest exclusion - and one "Brain-Inspired Modular Training"
  evaluation that names no biological mechanism), 1 spare eligible-but-unneeded, ranks recorded.
  Three strata have NO same-stratum spare in the first-query pool: cs.CR (attack paper),
  cs.HC (visual analytics), cs.AI architecture 2023-2026 (foundation-agents survey).
- **Final corpus: N = 42** (35 drawn-kept + 7 replacements), bands 9/16/17
  (2015-2019/2020-2022/2023-2026), families unchanged by construction (replacements are
  stratum-matched).

## Stop-rule firing and owner disposition required

The frozen acceptance range is 45-75 AFTER replacements. First-query-only, the ceiling is 42:
35 + 7 (the three empty strata cap it; even the two not-needed eligible spares could not enter,
being rank-lower copies of filled strata). The resumption record's stop rule therefore FIRES:
"if the acceptance range cannot be met after replacements, stop and record; do not relax the
frozen rule." Recorded. The disposition is the owner's (packaged 2026-10-25):

- (a) accept N = 42 under a dated acceptance-range amendment (floor 45 -> 40), same-query
  scope, honest reason: the scope ruling postdates the range and necessarily shrinks it - the
  lead's recommendation;
- (b) authorize the pooled cross-query scope for the validation corpus only (a dated crossing
  of the first-query boundary, restoring 20/20/20 and N ~= 60, at the cost of a
  different sampling frame than the audit corpus - comparability caveat travels into Methods);
- (c) decline the validation pass (kill-rule re-check then rests on the 16-claim final corpus
  alone, with the pilot/validation distinction dropped from the paper's claims).

No coding starts before the disposition. PDF pinning and the novelty scan proceed (they do not
depend on N).
