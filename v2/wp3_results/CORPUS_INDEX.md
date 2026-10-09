# Corpus index: what this line asserts, what it withdrew, and where to read each

**Status: the map the corpus did not have. Thirty-eight documents accumulated across twenty-two rounds, four
of them superseded, and until now nothing said which claims are live.** **Written after a corpus-level audit
that searched every document for statements still asserting a withdrawn claim.**

---

## 1. The four claims that are live, and the documents behind each

| claim | one-line statement | primary documents | status |
| --- | --- | --- | --- |
| **V2-C1** | treating pair measurements as replicates inflates the **SIGNIFICANCE** by about `sqrt(n)`, while the pair-level **effect size is smaller** than the animal-level one; the corpus's "11 to 18 times" divided a z-score by a Cohen's `d` | `ANATOMY_FUNCTION_RETEST.md`, `CONFOUND_TESTS.md`, `ANIMAL_LEVEL_ESTIMATE.md`, `ROBUSTNESS_AND_CLASS_AT_ANIMAL_LEVEL.md` | **arithmetic** |
| **V2-C2** | the source's own Fig-6 comparison **reproduces** at `r = +0.0368` and `-0.0064`, and its target has cross-animal agreement of only **`r = 0.208`** to `0.270` on the cells available | `FIG6_LIKE_FOR_LIKE.md`, **`V2C2_STRESS_TEST.md`** | **reproduced and stress-tested across four specifications; `n = 2` stated** |
| **V2-C3** | a pair's response has a **measurement-error share of 38.7 to 57.1 %** across eight specifications, always the largest or second-largest component; the **pair-specific animal share is negative when pairs measured in one animal are included and 21.6 to 35.5 % when excluded**; what is robust is the sign structure, not any share | `CORRECTION_heterogeneity_is_noise.md`, **`CORRECTION_variance_decomposition_specification.md`**, **`CORRECTION_eps_is_a_range.md`** | **measurement-error share solid; pair-specific share narrowed** |
| **V2-C4** | the published values come from choices that live in the pipeline's code, and re-analysing moves the animal-level estimate across **`d` 0.085 to 0.729** | `SOURCE_RULE_RECOVERED.md`, `SPECIFICATION_COMPLETE.md`, `SPECIFICATION_SENSITIVITY.md`, `SPECIFICATION_IN_LITERATURE.md` | **sensitivity solid; sampled practice still owed** |

## 2. The four documents whose interpretation was superseded

**All four are retained unaltered, each now carrying a dated status banner at the top.** **Their measurements
stand; their interpretations do not.** **The titles still state the superseded reading, deliberately, so each
document remains findable by the claim it made.**

| document | the superseded reading | superseded by | when |
| --- | --- | --- | --- |
| `WITHIN_VS_BETWEEN_ANIMAL.md` | the animals differ rather than the measurements being noisy | `CORRECTION_heterogeneity_is_noise.md` | round 12 |
| `POPULATION_LEVEL_NOT_CIRCUIT_PROPERTY.md` | a population-level regularity, not a circuit property | `CORRECTION_heterogeneity_is_noise.md` | round 12 |
| `EFFECT_RELIABILITY_AND_PAIR_COMPOSITION.md` | what is reproducible is which pairs were measured | `PAIR_COMPOSITION_TEST.md` | round 15 |
| `RETRACTION_window_dependence.md` | *(this document is itself a retraction, retained as its own record)* | `WINDOW_RESOLVED.md` | its own date |

## 3. The supporting analyses, and what each constrains

| document | what it measured | what it does to the claims |
| --- | --- | --- |
| `ATLAS_RELIABILITY_AUDIT.md` | split-half reliability by stratum | the gradient the atlas does not report |
| `WINDOW_RESOLVED.md` | the window-dependence retraction and its resolution | bounds V2-C4 |
| `FINAL_ESTIMATE_AND_COLLIDER_WARNING.md` | the estimate and a collider caveat | bounds V2-C1's interpretation |
| `PAIR_COMPOSITION_TEST.md` | composition explains **17.7 %** | reduces the round-14 account |
| `TECHNICAL_COVARIATES.md` | nine covariates explain **0.25 %** adjusted | removes a technical account for the residual |
| `PAIR_SET_RESTRICTION.md` | restricting the pool does not shrink the spread | removes a composition account for the residual |
| `UNC31_ARM.md` | `unc-31` association **+0.0871**, `t = 2.804`; between-arm comparison **underpowered** | a positive result and an uninformative contrast |
| `LITERATURE_SURVEY_SPECIFICATION_AND_RELIABILITY.md` | eleven works, none reporting functional reliability | places the contribution |
| `METHODS_LEVEL_SURVEY.md` | four full texts, 376,157 chars, none reporting it | confirms the placement |
| `FIGURE_SPECIFICATIONS.md` and `FIGURE_SOURCE_DATA.json` | figure-ready data with hashes | how a manuscript would be assembled |
| `CONSOLIDATED_POSITION.md` | the line's position as of its date | **read with the four supersessions in mind** |
| `../wp1_data/PATH_LAYOUT.md` | the four input paths the scripts expect, their provenance, integrity and licences | **read before attempting to re-run anything**; 27 of 29 scripts read from `/tmp/` |
| `V2C2_STRESS_TEST.md` | V2-C2 across four effective specifications, and a redundant grid axis | **the reproduction is stable; the bound ranges 0.208 to 0.270, always far below 0.5; and a grid must be checked for redundancy before it is reported** |
| `CORRECTION_eps_is_a_range.md` | the measurement-error share across eight specifications | **a share from a variance decomposition is a range over a declared specification set, not a point value** |
| `CENSUS_d_z_versus_d_effect.md` | **seventy-six fields across five files store a z-score in a field named `d`**; the four live claims draw on files storing genuine Cohen's `d` | **a `d` of 2 or more in this corpus is a z-score, not an effect size** |
| `NOTATION_two_effect_sizes.md` | two quantities share the symbol `d` | **read before quoting any effect size**: `d_A` is `mean(diff)/SD(diff)` across animals, `d_B` is the mean of per-animal standardised effects |

## 4. The invalid runs, retained on purpose

| artifact | why it is invalid |
| --- | --- |
| `anatomy/00_anatomy_vs_function_INVALID_idorder.py` | indexed the connectome by the wrong neuron order, giving an implausible `d = 4.74` |
| `anatomy/05_common_mode_INVALID_percellnorm.py` | per-cell normalisation divided by a pre-stimulus SD over 8 volumes, blowing up to about `1e11` |
| `anatomy/11_source_rule_ATTEMPT1_scalarbug.py` | collapsed per-cell quantities to scalars, so 0 of 3,333 events passed |
| `anatomy/13a_icc_INVALID_zero_inflation.py` | treated one-measurement units as contributing zero within-variance, inflating the ICC to 0.93 |
| `anatomy/12_inverse_variance_weighting.py` | the weighted arm spans 31 orders of magnitude; **the unweighted arm is valid and is used** |
| four `RESULT_*INVALID*.json` | the results of the above |

**No other document in this repository shows its own discarded work. This corpus does, deliberately.**

## 5. The defect ledger

**Nine self-found measurement defects and thirteen self-inflicted check failures across twenty-two rounds.**
**Every measurement survived re-examination; every interpretation attached to a measurement was revised at
least once, and three were withdrawn or narrowed outright.**

**The failure mode is not the computation. It is the step from a number to a sentence about the number.**

## 6. How to read this corpus

1. **Start at section 1.** Those are the four claims.
2. **Before quoting any other document, check section 2** in case it was superseded.
3. **For any number, go to the result JSON named in its document's provenance section**; the figure source
   data records a hash for each.
4. **Treat everything a superseded document says about interpretation as dated**, and its measurements as
   still standing.
4a. **Before quoting an effect size, check which `d` it is, and apply the arithmetic check: the largest
   genuine effect size in this corpus is 0.7690, so any `d` of 2 or more is a z-score rather than an effect
   size.** `CENSUS_d_z_versus_d_effect.md` and `NOTATION_two_effect_sizes.md` define the four meanings. `NOTATION_two_effect_sizes.md` defines the two;
   a value above about 0.4 in this corpus is the across-animal ratio and a value near 0.10 is usually the
   per-animal mean.
4b. **Before trusting a specification grid, check it for redundancy: if two levels of an axis give
   bit-identical output, that axis is not a specification.** V2-C2's grid had three transforms that produced
   one result, so twelve rows were four specifications.
5. **`v2/tools/check_artifacts.py` will verify any requirement you state against the corpus**, and its README
   documents the thirteen ways it has been wrong.

## 7. What is owed

| item | status |
| --- | --- |
| a specification set drawn from published practice | **read at title-and-abstract and Methods level for 15 works; a systematic sample is still owed** |
| the dLDS tension (round 21) | **named, not resolved** |
| an independent reviewer | **owed, and external to this line** |
| the owner's decision on the plan's constraint forbidding a new NMI abstract, main-text Results, Discussion or figures | **owed, and the plan's to lift** |

## 8. Provenance

* Classification produced by a corpus-level audit that searched all 38 documents for statements still
  asserting a withdrawn claim, and found the four in section 2.
* **The audit's real finding was structural rather than textual: the corpus had no map.** **The banners and
  this index are the fix, and they change no measurement.**
* **No model was fitted. No causal claim is made.**
