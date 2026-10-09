# Census: which `d` in this corpus is an effect size and which is a z-score

**Status: round 27's owed item, completed. Seventy-six fields across four result files store a z-score in a
field named `d`, with no corresponding effect size. The files that carry the line's four live claims store
genuine Cohen's `d`.</** No model was fitted.

---

## 1. Method

**Every field in every result JSON whose name matches `d`, `d_*` or `*_d` was extracted, and the producing
script was located and searched for its definition of the stored quantity.** **Where a script contains both
patterns -- which happens when it correctly computes and stores both a Cohen's `d` and a `t` -- the field was
resolved by reading the write statement rather than by pattern-matching.**

**That last step matters: a first pass flagged twenty fields as ambiguous, and reading the write statements
showed all twenty were correctly separated.** **Recording the false positives is part of the method.**

## 2. The result

| producing file | `d` fields | what `d` is | verdict |
| --- | --- | --- | --- |
| **`RESULT_baseline_conventions.json`** | 18 | **`diff / SE`** | **z-score, mislabelled** |
| **`RESULT_confounds.json`** | 20 | **`diff / SE`** | **z-score, mislabelled** |
| **`RESULT_final_estimate.json`** | 12 | **`diff / SE`** | **z-score, mislabelled** |
| **`RESULT_timescale_class.json`** | 26 | **`diff / SE`** | **z-score, mislabelled** |
| `RESULT_corrected.json` | 15 | `diff / sp` where `sp = sqrt(var/n + var/n)` | **z-score, mislabelled** |
| `RESULT_robust_class.json` | 12 | **`m / s`** (`diff / SD`), with `t` stored separately | **correct** |
| `RESULT_animal_level.json` | 1 | `cohens_d_paired = mean / sd` | **correct** |
| `RESULT_source_rule.json` | 1 | `paired_diff / sd` | **correct** |
| `RESULT_iv_weighting_INVALID_weights.json` | 2 | `m / s` from `stats()` | **correct** |
| `RESULT_per_animal_heterogeneity.json` | 7 | mean of per-animal standardised effects | **correct, different quantity** |
| `RESULT_genotype_unc31.json` | 2 | `cohens_d = mean / sd` | **correct** |
| `RESULT_unit_check.json` | 2 | both, labelled | **correct** |
| `RESULT_invalid_idorder.json` | 1 | `cohens_d` | **INVALID run, retained** |

> **Seventy-six fields across five files store `diff / SE` in a field named `d`, with no effect size stored
> alongside. Every file that carries one of the line's four live claims stores a genuine Cohen's `d`.**

**`RESULT_corrected.json` uses `sp` rather than `se` as the name, but the expression is the same standard
error of a difference, so it belongs in the same group.**

## 3. Why this matters, and why it is narrower than it looked

**It matters because those five files are the sources for the line's early documents, and a z-score quoted as
an effect size overstates the effect by a factor of `sqrt(n)`, which here is hundreds.**

**Documents quoting a mislabelled `d` as an effect size:**

| document | source | example values quoted |
| --- | --- | --- |
| **`ANATOMY_FUNCTION_RETEST.md`** | `RESULT_corrected.json` | `d = 1.4897`, `4.7823`, `2.6933`, `4.0396` |
| **`CONFOUND_TESTS.md`** | `RESULT_confounds.json` | `d = 1.6563`, `3.5346`, `3.0249`, `3.5464` |
| **`FINAL_ESTIMATE_AND_COLLIDER_WARNING.md`** | `RESULT_final_estimate.json` | `d = -0.6676`, `1.4727`, `1.5572` |
| **`WINDOW_RESOLVED.md`** | `RESULT_timescale_class.json` | `d = 1.15` to `7.63` |
| **`RETRACTION_window_dependence.md`** | `RESULT_timescale_class.json` | as above |
| `ANIMAL_LEVEL_ESTIMATE.md` | `RESULT_baseline_conventions.json` | the pair-level `11.048` |

**It is narrower than it looked because the four LIVE claims are clean.** **V2-C1's inflation factor divided
`RESULT_baseline_conventions.json`'s z by `RESULT_robust_class.json`'s Cohen's `d`, which is the defect round
27 corrected.** **V2-C2, V2-C3 and V2-C4 draw on files in the correct group.**

**V2-C4's specification range of `d` 0.085 to 0.729 is therefore unaffected:** **0.7289 from
`RESULT_robust_class.json` is `m/s`, 0.4495 from `RESULT_source_rule.json` is `paired_diff/sd`, and 0.1580
and 0.0852 from `RESULT_iv_weighting_INVALID_weights.json` are `m/s`.** **All four are Cohen's `d`.** **Round
24's conclusion stands and round 27 did not disturb it.**

## 4. The rule this establishes, in the strongest form the corpus permits

**A field named `d` in this corpus means one of four things, and a document quoting one must say which:**

| name | definition | files |
| --- | --- | --- |
| **`d_z`** | `diff / SE` -- a z-score | `baseline_conventions`, `confounds`, `final_estimate`, `timescale_class`, `corrected` |
| **`d_A`** | `mean(diff) / SD(diff)` -- between-animal Cohen's `d` | `robust_class`, `animal_level`, `source_rule`, `iv_weighting` |
| **`d_B`** | mean of per-animal standardised effects | `per_animal_heterogeneity` |
| **`d_c`** | Cohen's `d` computed within each arm | `genotype_unc31`, `unit_check` |

**And the practical check: a `d` above about 1.5 in this corpus is almost certainly `d_z`.** **The largest
genuine effect size anywhere here is `d_A = 0.7690`, for gap junctions.** **Any value of 2 or more is a
z-score.**

**That single heuristic would have caught round 27's defect four rounds earlier: `d = 11.048` is not a
plausible effect size for a neural association, and `ANIMAL_LEVEL_ESTIMATE.md` itself calls `d = 13.8`
"not a plausible biological effect size" while continuing to treat it as one.**

## 5. What is owed

1. **The six documents in section 3 need correction banners naming `d_z`,** in the same form as round 27's.
2. **A one-line addition to `check_artifacts.py`** -- or to the tooling README -- recording the `d_z` versus
   `d_A` distinction so a future requirement can test it.
3. **Nothing else.** **The measurements are unaffected; what changes is the label.**

## 6. Provenance

* Census output `/tmp/osf/d_census.json`; every field traced to a write statement in its producing script.
* **Twenty fields were first flagged ambiguous and resolved by reading the write statements; those false
  positives are recorded in section 1 rather than dropped.**
* **No model was fitted. No causal claim is made.**
