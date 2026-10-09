> **STATUS: THE PAIR-LEVEL VALUE IS A z-SCORE, NOT AN EFFECT SIZE (round 27).** The pair-level figures in
> this document come from `diff / SE`, while the animal-level figures come from `diff / SD`. **Their ratio is
> `sqrt(n)`, a definitional identity, and the pair-level effect size expressed as a Cohen's `d` is SMALLER
> than the animal-level one, not larger.** The pseudo-replication point stands and the metric describing it
> does not. **Superseded by
> [`CORRECTION_unit_inflation_is_significance.md`](CORRECTION_unit_inflation_is_significance.md).**
> The text is left unaltered.

---

# Notation: two effect sizes share the symbol `d` in this corpus and are not the same quantity

**Status: a notation defect found by a cross-script consistency audit, and its fix. No measurement changed;
no claim changed.** The audit also **cleared** V2-C4's specification range, which was the reason for
running it.

---

## 1. How this was found

**The corpus was audited for cross-script agreement: twenty-one scripts written over twenty-three rounds,
each reporting "the effect". Two documents report `+0.1165` and `+0.1172` for what both call the
animal-level effect, and a third reports `+0.7289`.**

**The audit traced every `d` in the corpus back to the line of code that computes it.** **The finding is
that two different quantities share the symbol, and nothing in the corpus says so.**

## 2. The two quantities, and the code that defines each

**Quantity A -- between-animal paired Cohen's `d`:**

```
d = mean(across-animal differences) / SD(across-animal differences)
```

**Defined in `09_animal_level.py` as `cohens_d_paired = mean/sd` and in `12_inverse_variance_weighting.py`
as the fifth return of `stats(d)`, namely `m/s`. Confirmed numerically: `animal_level.json` gives
`paired_diff = 0.077023` and `sd = 0.105670`, and `0.077023/0.105670 = 0.728902`, exactly the reported
`cohens_d_paired`. Likewise `source_rule.json` gives `61.403601/136.619078 = 0.449451`.**

**Quantity B -- mean of per-animal standardised effects:**

```
for each animal:  standardise its values within itself, then effect = mean(connected) - mean(unconnected)
d_mean          = the mean of those per-animal effects
random-effects  = the inverse-variance pooled version of the same
```

**Defined in `14_per_animal_heterogeneity.py`. `d_mean = +0.1165`, `d_sd = 0.1617`, and the random-effects
pooled value `re = +0.1019`.**

**These are not the same quantity, and the difference is not cosmetic:** **A is a ratio whose denominator is
the spread BETWEEN animals; B is an average whose unit is the spread WITHIN each animal.** **They coincide
only if the two spreads coincide, and here they do not -- the between-animal SD is 0.1057 while the
within-animal standardisation puts each effect in its own animal's SD units.**

## 3. What was checked, and what was cleared

**The audit's reason for running was to test whether V2-C4's specification range mixes the two scales. It
does not.** **All four values in that range come from code computing Quantity A:**

| value | source | scale |
| --- | --- | --- |
| **0.7289** | `09_animal_level.py`, `cohens_d_paired = mean/sd` | **A** |
| **0.4495** | `11b_source_rule.py`, `61.403601/136.619078` | **A** |
| **0.1580** | `12_inverse_variance_weighting.py`, `stats()` returns `m/s` | **A** |
| **0.0852** | same script, the weighted arm | **A** |

> **V2-C4's range of `d` 0.085 to 0.729 is therefore internally consistent, and the claim stands as
> written.**

## 4. The one place the scales ARE mixed, and its status

**`POPULATION_LEVEL_NOT_CIRCUIT_PROPERTY.md` states that the random-effects pooled `d = 0.102` is
*"SMALLER than any single-specification estimate this line produced, 0.4495 and 0.7289"*.**

**`0.102` is Quantity B and `0.4495` and `0.7289` are Quantity A.** **The comparison is cross-scale and the
sentence as written does not support its conclusion.**

**That document already carries a superseded banner from round 12, so the sentence is already marked as
superseded interpretation rather than live claim.** **This note records the specific reason in addition to
that banner, because the banner's reason is different: the banner concerns the population-versus-circuit
framing, and this concerns the arithmetic of the comparison.**

**What survives: the random-effects pooled value `0.1019` and the per-animal distribution behind it are
Quantity B and are unaffected. Only the comparison against the Quantity-A values is withdrawn.**

## 5. The rule this establishes

**In this corpus, `d` alone is ambiguous. Any document quoting an effect size must say which:**

| notation | meaning | where used |
| --- | --- | --- |
| **`d_z`** | **z-score**, `diff/SE` | the pair-unit rows in the specification table, and `RESULT_baseline_conventions.json` and `RESULT_corrected.json` |
| **`d_A`** | **between-animal paired Cohen's `d`**, `mean(diff)/SD(diff)` | the specification sensitivity table, V2-C4 |
| **`d_B`** | **mean of per-animal standardised effects** | the heterogeneity and random-effects analysis, V2-C3's per-animal distribution |

**And the numbers, so a reader can tell which they are looking at without opening a script:**

```
d_A  values in this corpus:  0.7289 (animal level), 0.4495 (source rule), 0.4145 (chemical), 0.7690 (gap),
                             0.1580 (source read-out, unweighted), 0.0852 (inverse-variance weighted),
d_B  values in this corpus:  0.1165 (mean), 0.1052 (median), 0.1019 (random-effects), 0.0825 (fixed-effect)
```

**A value above about 0.4 in this corpus is certainly `d_A`; a value near 0.10 is usually `d_B`. That is a **`11.048` is `d_z`, not `d_A`, and is removed from that list by round 27's correction.**
heuristic for reading, not a definition, and the documents are the authority.**

## 6. What this changes

**Nothing measured.** **V2-C1, V2-C2, V2-C3 and V2-C4 all stand.** **The audit's purpose was to check
V2-C4's range and that range is cleared.**

**What it changes is that three documents describe two different quantities by the same name, and one
superseded document compares them. Both facts are now recorded.**

## 7. Provenance

* Audit: every `d` in the corpus traced to its defining line; `09_animal_level.py` line 110,
  `11b_source_rule.py` line 111, `12_inverse_variance_weighting.py` line 99,
  `14_per_animal_heterogeneity.py`.
* Numerically confirmed: `0.077023/0.105670 = 0.728902`; `61.403601/136.619078 = 0.449451`.
* **No model was fitted. No causal claim is made.**
