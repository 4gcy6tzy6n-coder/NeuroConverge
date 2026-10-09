# The association is a population-level regularity, not a property of the circuit

**Status: the line's culminating result, with the claim it supports and the claims it does not.** No model
was fitted. The association is observational and cross-individual; **no causal claim is made.**

---

## 1. The result

**Per-animal connectivity-function effect, each animal standardised within itself so that its absolute
fluorescence scale cannot drive the between-animal spread. 109 of 112 animals had enough connected and
unconnected pairs to enter.**

| quantity | value |
| --- | --- |
| animals | **109** |
| median `d` | +0.1052 |
| mean `d` | +0.1165 |
| between-animal SD | **0.1617** |
| range | **[-0.4557, +0.7391]** |
| interquartile range | [+0.0350, +0.1982] |
| **animals with a positive effect** | **90 / 109 (82.6 %)** |
| animals individually significant | 34 / 109 |
| **Cochran's `Q`** | **252.7 on 108 df** |
| **`I^2`** | **57.3 %** |
| `tau` (DerSimonian-Laird) | 0.0886 |
| fixed-effect pooled `d` | +0.0825, 95 % CI [+0.0682, +0.0968] |
| **random-effects pooled `d`** | **+0.1019, 95 % CI [+0.0780, +0.1257]** |
| **95 % prediction interval for a new animal** | **[-0.0734, +0.2771]** |

## 2. What this settles

> **The connectivity-function association is real at the population level and positive in 83 % of animals,
> but the between-animal heterogeneity is substantial (`I^2 = 57.3 %`, `Q/df = 2.34`) and the prediction
> interval for a new animal crosses zero.**

**Three things follow, and they are the contribution:**

1. **Knowing the population average tells you the sign for most animals and predicts nothing reliable about
   any particular one.** **The association is a property of the population, not of the circuit.**
2. **The pooled estimate is smaller than any single-specification estimate this line produced** --
   `d = 0.102` random-effects against 0.4495 and 0.7289 -- because pooling across animals with
   `tau = 0.089` correctly widens the interval and because the per-animal standardisation removes the
   cross-animal scale differences that inflated the earlier figures.
3. **The specification sensitivity of round 8 and the unit inflation of round 5 both survive as separate
   findings.** This result does not replace them; it adds a third axis.

## 3. The coherent claim, stated once

> **A published whole-brain functional atlas presents per-pair response values as though they were
> properties of the circuit. Measured from the per-animal records that the atlas aggregated:
> (i) a pair's response agrees across animals at `r_full = 0.04` while agreeing within an animal at
> `r_full = 0.52`; (ii) the connectivity-function association is positive on average, random-effects
> `d = 0.102`, but substantially heterogeneous, `I^2 = 57.3 %`, with a new-animal prediction interval that
> crosses zero; (iii) treating pair-measurements as independent replicates inflates the effect by 11 to 18
> times; and (iv) the analysis choices that produced the published values live in the pipeline's code and
> not in its data file, moving the estimate across a range from 0.085 to 0.729. **The atlas supports a
> population-level claim. It does not support a circuit-property claim, and nothing in the artifact tells a
> user which of the two they are making.**

**That is a methodological contribution about a real, heavily used published resource, measured rather than
asserted, and it is the first claim in this line that is about an assumption rather than a statistic.**

## 4. The four numbers, and why each is load-bearing

| number | what it rules out |
| --- | --- |
| **cross-animal `r_full = 0.04`** against **within-animal 0.52** | rules out "the measurements are noisy" as the explanation of the atlas's low reliability; **the animals differ** |
| **`I^2 = 57.3 %`, prediction interval crossing zero** | rules out "the atlas value is a stable circuit property with additive noise"; **it is a population mean over a heterogeneous population** |
| **11 to 18 times unit inflation** | rules out "the published effect size is comparable across units"; **it is arithmetic, and one of the two units is simply wrong** |
| **0.085 to 0.729 across specifications** | rules out "the effect size is a fact about the data"; **it is a fact about the data under a specification** |

## 5. What is NOT established, listed so the claim cannot be read as broader

* **That the heterogeneity is biological.** Animal-level differences in GCaMP expression, dissection
  quality, age or indicator state would produce cross-animal disagreement with no pair-specific biology.
  **The per-animal standardisation used here removes a global additive offset and a global scale, and
  nothing more.** **A heterogeneous additive animal offset would survive it.**
* **That the true effect is +0.102.** That is the random-effects pooled estimate under this read-out, this
  window convention and no inclusion rule. **The source's own rule gives 0.4495 at the animal level under a
  different read-out, and the two are not comparable.**
* **That any published conclusion is wrong.** The source's claims concern sign, strength, temporal
  properties and causal direction, and it reports STAM capture and reproducibility percentages. **This line
  measures one coarse averaged association and has not constructed a like-for-like comparison.**
* **That the result generalises past this atlas.** One dataset, one species, one preparation.
* **Anything causal.** The connectome and the recordings are from **different animals**; the mapping class
  remains `CELL_CLASS_ALIGNED_ACROSS_SPECIMENS`.

## 6. What would make this a manuscript

**Three things, in order:**

1. **A like-for-like comparison against the source's own reported quantity**, which requires reading how it
   reports STAMs and reproducibility and reconstructing at least one of those numbers. **Without this, the
   manuscript says the atlas cannot support a circuit-property claim without ever engaging the claim the
   atlas actually makes.**
2. **A technical-versus-biological test for the heterogeneity.** A mixed model with an animal-level random
   intercept tests only a homogeneous offset; **the informative test allows a heterogeneous animal effect
   and asks whether the pair-specific component survives it.**
3. **A specification set drawn from what analysts actually do**, rather than this line's own five
   constructions, since the round-8 range is only as meaningful as the choices it spans.

**Until at least the first is done, the contribution is a well-measured methodological finding about an
artifact, not yet a manuscript.**

## 7. Defect ledger, unchanged and complete

**Nine measurement-or-claim defects and nine self-inflicted check failures are recorded across this line,
all retained.** The measurement defects: duplicate-name pooling, ratio-of-medians, a biased read-out
statistic, an invalid id-order assumption, per-cell collapse to scalars, a broadcast error, a zero-pass
criterion run, weights spanning thirty-one orders of magnitude, and an ICC inflated by mostly-zero within
variance. **Two measurement results and one check result are marked INVALID in the repository rather than
deleted.**

## 8. Provenance

* Script `anatomy/14_per_animal_heterogeneity.py`; output `anatomy/RESULT_per_animal_heterogeneity.json`.
* All 109 per-animal effects are stored individually in the output, so the distribution can be re-examined
  without re-running.
* Read-out, pre-window and analysis-window conventions as in `SOURCE_RULE_RESULT.md`.
* **No model was fitted.**
