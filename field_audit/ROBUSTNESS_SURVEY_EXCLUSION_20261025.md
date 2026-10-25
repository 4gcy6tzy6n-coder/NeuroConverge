# Robustness analysis R2a (advisor review 2026-10-25): survey exclusion

Directive: advisor risk R2 - both corpora include survey/review members whose structural E0s
could dilute the primary-research reading; recompute the core results without them. This is a
NAMED ROBUSTNESS ANALYSIS reported beside, never instead of, the frozen primary numbers.

## Frozen exclusion rule (fixed before recomputation)

A claim is excluded iff its own TITLE or ABSTRACT self-identifies as a survey or review
(case-insensitive "survey" / "review" as printed words). Applied mechanically to both corpora;
the exclusion lists below are the check that no primary-research paper is caught by a passing
verb mention (each excluded item was individually confirmed to self-identify as a survey/review
genre paper; two additional coder-A note flags in the validation corpus - 1909.11145v2,
2210.16530v1 - are primary-research papers and are NOT excluded by this rule).

## Excluded

- Primary (2): 2312.07213v4 ("...Human-computer Interaction: A Review"), 2305.11252v1
  ("...artificial neural networks: a review"). n = 16 -> 14 cells-per-transition x 15 claims.
- Validation (6): 1506.03264v1, 1901.03690v3, 2204.07050v7, 2209.10818v2, 2312.09257v2,
  2603.26722v1 (each self-identifies as survey/review in title or abstract). n = 42 -> 36.

## Results (merged grades; script `robustness_survey_exclusion_20261025.py`, JSON alongside)

| measure | primary full (16) | primary no-survey (15) | validation full (42) | validation no-survey (36) |
| --- | --- | --- | --- | --- |
| T1 E0 | 16/16 | 15/15 | 42/42 | 36/36 |
| T2 E2 | 2/16 (12.5%) | 2/15 (13.3%) | 9/42 (21.4%) | 9/36 (25.0%) |
| T2 E1-only | 12/16 | 11/15 | 27/42 | 27/36 (75.0%) |
| T3 E2 | 10/16 (62.5%) | 10/15 (66.7%) | 25/42 (59.5%) | 25/36 (69.4%) |
| headline E2+ | 62.5% (CI 39-82) | 66.7% (CI 41.7-84.8) | 61.9% (CI 46.8-75.0) | 72.2% (CI 56.0-84.2) |
| kill rule (80%) | not triggered | not triggered | not triggered | not triggered |
| T2-vs-T3 controlled gap | 50.0 pts | 53.4 pts | 38.1 pts | 44.4 pts |

## Reading

1. The T2-vs-T3 evidence asymmetry - the advisor-confirmed core finding - is NOT an artifact of
   survey dilution; it STRENGTHENS in every no-survey subset (the surveys' structural E0s sat on
   T2/T4, dragging the utility-side shares down more than the correspondence side).
2. T1 delegation is unchanged at 100 percent in all four subsets.
3. The headline share rises when surveys are excluded (the surveys' headlines were the weakest);
   every point estimate remains below the 80 percent kill bar in every subset. HONEST CAVEAT:
   the no-survey subsets are smaller, their Wilson upper bounds (84.8, 84.2) cross 80 - the
   exclusion trades representativeness of the frozen corpus for a wider interval, and the kill
   rule is defined on, and evaluated on, the frozen corpora as drawn.
4. No frozen number changes; the frozen statistics files are untouched (the statistics script's
   import path gained a main-guard so importing it has no side effects - behaviour verified
   unchanged by re-run before and after).
