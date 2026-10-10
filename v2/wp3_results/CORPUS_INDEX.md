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
| **V2-C3** | a pair's response has a **measurement-error share of 17 to 57 %** depending on whether events are weighted by their inverse across-cell spread and on window, baseline and normalisation, never the smallest component; the **pair-specific animal share is negative when pairs measured in one animal are included and 21.6 to 35.5 % when excluded**; what is robust is the sign structure, not any share | `CORRECTION_heterogeneity_is_noise.md`, **`CORRECTION_variance_decomposition_specification.md`**, **`CORRECTION_eps_is_a_range.md`** | **measurement-error share solid; pair-specific share narrowed** |
| **V2-C4** | the published values come from choices that live in the pipeline's code, and re-analysing moves the animal-level estimate across **`d` 0.085 to 0.450 within one weighting convention and 0.39 to 0.73 within the other**; the reported 0.085-to-0.729 span mixes the two, and **six dimensions are undeclared while the one declared dimension is the smallest** | `SOURCE_RULE_RECOVERED.md`, `SPECIFICATION_COMPLETE.md`, `SPECIFICATION_SENSITIVITY.md`, `SPECIFICATION_IN_LITERATURE.md`, **`V2C4_RANGE_STRESS_TEST.md`** | **sensitivity solid; its upper end isolated to one step, and a systematic sample of practice still owed** |

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
| `ORDER_AXIS.md` | **the order of application as an explicit axis** | **the exact correctness check passes -- `w` at post 24 reproduces the code's 0.7289 and t=7.610 -- and the order is the largest dimension measured, 0.85 at post 24, with one order stable at 0.12 across windows and the other spanning 1.06 and crossing zero** |
| `V2C4_ALL_FOUR_VALUES_REPRODUCED.md` | **all four of V2-C4's values independently reproduced** | **0.7289 and 0.4495 exact to four decimals, and 0.1580 and 0.0852 across seven fields; the two-family structure is confirmed: unweighted 0.0852 to 0.4495, weighted 0.7289** |
| `../wp1_data/GENERALISATION_ROUTE_CLOSED.md` | the second-dataset generalisation attempt | **closed for this environment after three fetch failures, the third being this line's own concurrent-writer bug; 1.866 GB spent, zero usable files; the extraction is written and de-risked so the analysis can resume if the data arrives by another means** |
| `JOINT_GRID_VERIFIED_NONADDITIVE.md` | the corrected joint grid, from a step verified against the code first | **the two largest dimensions are strongly non-additive: isolated sum -0.008 but joint +0.571; and a declared grid spans -0.096 to +0.966, crossing zero** |
| `RETRACTION_joint_grid_wrong_axis.md` | the joint grid over the two largest dimensions | **withdrawn: it divided by the wrong axis, so its weighting axis is not the code's and its additivity test is void; its per-cell-normalisation numbers stand** |
| `V2C4_RANGE_MEASURED_IN_ONE_FRAMEWORK.md` | V2-C4's specifications measured in one framework | **within a weighting family they span 0.056 unweighted and 0.181 weighted, against a reported span of 0.644; the per-event weighting contributes 0.18 to 0.30 to each** |
| **`SPECIFICATION_LEDGER.md`**, **`V2C4_RANGE_MEASURED_IN_ONE_FRAMEWORK.md`** | **every specification dimension with its isolated measured size, and whether any document declares it** | **the manuscript's structure: the declared dimension is the smallest, and three undeclared ones are each worth 0.24 to 0.34. READ THE SIZES AS A LIST, NOT A BUDGET: they are strongly non-additive, and the order of application is itself a dimension** |
| `CORRECTION_weighting_moves_the_decomposition.md` | the per-event weighting's effect on the three-level decomposition: **`eps` moves 13 points, `beta` 11.5** | **all of V2-C3's reported shares are unweighted values; a choice, not an error, but weighted and unweighted must not be mixed** |
| `CORRECTION_per_event_weighting_omitted.md` | **the per-event `sd` division is a weighting five of this line's grids omitted**, worth about 0.34 in `d_A` | **the code weights each event by 1/its across-cell spread; the grids did not, so every 0.39-versus-0.73 comparison in rounds 26-33 was weighted against unweighted** |
| `CORRECTION_cell_pool_refuted.md` | the cell pool varied directly: **it contributes 0.0038, not 0.3394** | **four candidate causes for the 0.729-versus-0.393 discrepancy eliminated; unresolved; the decisive test is re-running the original script** |
| `CORRECTION_common_mode_cell_pool.md` | the common mode's cell pool, an undeclared specification dimension worth 0.34 in `d_A` | **the pool over which a common mode is computed is a specification; the corpus declares no such thing** |
| `V2C4_RANGE_STRESS_TEST.md` | V2-C4's range across twelve common-mode-free specifications, and a redundant inclusion axis | **the range is real and its upper end is one unvaried step, common-mode removal** |
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

**Twenty-one self-found defects, numbered fifth to twenty-first in the committed correction documents, plus
thirteen self-inflicted check failures recorded in `../tools/README.md`.** **The earlier count here said "nine
measurement defects and thirteen check failures", which was written at round 22 and used a different
taxonomy; it is corrected rather than kept, because a ledger whose own count is stale is an instance of the
defect this corpus documents.**
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
4c. **The pool over which a common mode or a normalisation is computed is itself a specification
4d. **Check the ORDER in which a pipeline applies its normalisations, not only whether it applies them.** Two orderings of the same two normalisations differ by 0.85 at one window while agreeing to 0.02 at another. See `ORDER_AXIS.md`.
   dimension.** `CORRECTION_common_mode_cell_pool.md` measured it at 0.34 in `d_A`, larger than the whole
   range spanned by window, baseline and normalisation together.
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
