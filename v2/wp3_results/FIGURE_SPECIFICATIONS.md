# Figure source data and specifications for the four surviving claims

**Status: the last analytical item within this line's reach, completed. Every number is derived from a
committed result JSON rather than retyped, and every series carries the choices that produced it.** The
plan's constraint forbids rendering figures, so this is what a figure would be drawn from.

---

## 1. What this file is

**`FIGURE_SOURCE_DATA.json`**, produced by `16a_figure_data.py`, which reads the 22 committed result JSONs
and emits, for each surviving claim, the numbers a figure would plot together with the specification that
produced them.**

**Every source JSON's sha256 prefix is recorded in the file**, so a plotted point can be traced to the
artifact that produced it. **Six cross-checks confirm the derived values equal their sources to 1e-9** --
the discipline this line adopted after a committed JSON was found carrying an uncorrected value in round 14.

**Two result files are deliberately excluded and the reasons are written into the data file itself:**

| excluded | reason |
| --- | --- |
| `RESULT_icc_INVALID.json` | the within-animal variance was computed as `var(vs) if len(vs)>1 else 0`, and most (animal, pair) units hold one measurement, so the ICC of 0.93 is inflated by construction |
| `RESULT_iv_weighting_INVALID_weights.json` | the inverse-variance weights span thirty-one orders of magnitude, so the weighted mean is determined by a handful of near-zero-variance units |

## 2. The four figures, and what each carries

### V2-C1 -- the unit inflation

**A paired bar chart, one bar per unit, three contrast panels.** Animal-unit values are read from
`RESULT_robust_class.json` and `RESULT_animal_level.json`: chemical `d = 0.4145`, gap `d = 0.7690`,
combined `d = 0.7289`. The pair-unit counterpart is `d = 11.048`, from `RESULT_corrected.json`.

**Inflation factors 11.2, 17.9 and 15.2.** **Specification:** unit is the animal, each standardised within
itself; read-out is connected mean minus unconnected mean; pre-window 60 volumes with the baseline from
volumes 30-60; analysis window per event, `int((interval - 5)/dt)`, capped at 60 volumes.

### V2-C2 -- the Fig-6 reproduction and its bound

**Two panels.** Left: the reproduction, `r = +0.0368` and `-0.0064` for the two animals. Right: the target's
cross-animal agreement, `r = +0.2084` on 23 shared cells, with 61 and 41 usable cells per animal.

**Specification:** data is `spont_data_fig6.zip` at 2,402,185 B containing two animals; the target is the
off-diagonal activity correlation matrix; the predictor is a synapse-count matrix built by name from both
source tables over 346 names.

### V2-C3 -- the three-level decomposition

**A single stacked bar of four shares.** Between-pair **0.5512**, measurement error **0.3753**,
pair-specific animal **0.0548**, homogeneous animal offset **0.0187**, over 192,303 units.

**Specification:** `y = mu + alpha[animal] + beta[animal,pair] + eps`, with `eps` identified from the units
that have repeats and the rest by subtraction, in log space because the responses span `-3.5e5` to `2.5e5`.

### V2-C4 -- the specification sensitivity

**One point per specification on a common axis**, with the animal unit and the pair unit marked separately.
**The four plotted values, each read from its own JSON:**

| specification | unit | `d` | source |
| --- | --- | --- | --- |
| 4 s window, common-mode removed, no inclusion rule | animal | **0.7289** | `RESULT_animal_level.json` |
| source rule, amplitude and derivative criteria | animal | **0.4495** | `RESULT_source_rule.json` |
| source rule, unweighted sum read-out | animal | **0.1580** | `RESULT_iv_weighting_INVALID_weights.json`, unweighted arm only |
| pair-measurement unit, for contrast | **pair** | **11.048** | `RESULT_corrected.json` |

**The span is `0.158` to `0.729` on the animal unit** -- a factor of
**4.6** -- before the pair-unit value is counted at all.

**The weighted arm is plotted as excluded, not omitted**, so the figure shows that a fifth specification was
computed and why it does not appear.

**And the range carries its validation:** a 2025 _Nature Reviews Neuroscience_ review states that it remains
unclear whether structural connectivity constrains directed-connectivity models, and a 2025 _Scientific
Reports_ paper states that no universally accepted method exists for inferring effective connectivity.
**The sensitivity is an instance of that condition, not an artefact of five arbitrary constructions.**

## 3. Supporting panels

**Two further panels carry the reliability results**, which are not a claim but are load-bearing for all
four:

* **Pair-response reliability by stratum:** within-animal `r_full = 0.5223` over 33,578 units, between-animal
  `r_full = 0.0405` over 15,189 pairs.
* **The effect's own reliability:** `r_full = 0.5266` over 98 animals, with 42.2 % noise and 57.8 % signal.
* **Cross-animal reliability by inclusion rule:** from `RESULT_inclusion_filtered.json`, with the unfiltered
  stratum lowest and the two filtered strata higher -- the gradient the atlas does not report.

## 4. What is withdrawn, recorded in the same file

**Four statements are listed in `withdrawn_or_narrowed`, each with what replaced it:**

| was | now |
| --- | --- |
| the animals differ rather than the measurements being noisy (round 9) | narrowed in round 12: 5.5 % pair-specific animal against 37.5 % measurement error |
| a population-level regularity rather than a circuit property (round 10) | weakened in round 12; the spread is 42.2 % noise and 17.7 % pair composition |
| what is reproducible is which pairs were measured (round 14) | reduced in round 15 to exactly 17.7 % |
| the ICC of 0.93 | withdrawn in round 9 |

**This is in the figure source data rather than in a separate document because a figure assembled without
it would present four claims in a lineage that retracted four others, and a reader has a right to see both
in the same place.**

## 5. What is still owed

1. **The pair-set-matched comparison** -- restrict every animal to the same commonly measured pairs, so
   composition is held exactly constant. **Named in round 15, not run.**
2. **A systematic specification survey at Methods level** -- round 18 read titles and abstracts only, and
   says so.
3. **An independent reviewer** -- `PREFLIGHT_REVIEW.md` records that the review performed is a self-review.
4. **The owner's decision on the plan's constraint**, which forbids a new NMI abstract, main-text Results,
   Discussion or figures, and which is why this is source data and not a figure.

## 6. Provenance

* Generator `16a_figure_data.py`; output `FIGURE_SOURCE_DATA.json`.
* **22 source JSONs hashed; 2 excluded with reasons; 6 cross-checks at 1e-9.**
* **No model was fitted. No causal claim is made.**
