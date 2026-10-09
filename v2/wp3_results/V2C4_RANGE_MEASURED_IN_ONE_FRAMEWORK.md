# V2-C4's range measured in one framework: within a family it is 0.056, not 0.644

**Status: V2-C4's four values are remeasured in a single framework, and the reported span of 0.644 turns out
to be about eleven times the span within the unweighted family.** **The range is real and its size comes from
dimensions the table does not name.** No model was fitted.

**This is the eighteenth self-found defect, and it closes round 37's owed item 2.**

---

## 1. What was measured, and the check that the implementation is right

**Round 37 found that V2-C4's range mixes a weighted pipeline against three unweighted ones, and corrected the
claim by subtracting the weighting's known size.** **That correction was constructed rather than measured.**

**This measures it: two specifications implemented in one pass over the data, each computed with and without
the per-event across-cell-SD weighting.**

| specification | weighted | animals | events | diff | SD | **`d_A`** | `t` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **NORULE** | no | 109 | 3,333 | 0.65615 | 1.66828 | **0.3933** | 4.106 |
| **NORULE** | yes | 109 | 3,333 | 0.10469 | 0.18368 | **0.5700** | 5.951 |
| **SOURCE** | no | 109 | 2,230 | 61.40360 | 136.61908 | **0.4495** | 4.692 |
| **SOURCE** | yes | 109 | 2,230 | 6.88451 | 9.16473 | **0.7512** | 7.843 |

**THE IMPLEMENTATION CHECK, AND IT PASSES.** **`SOURCE` with no weighting returns `d_A = 0.4495`, `diff =
61.40360` and `sd = 136.61908`, which are `11b_source_rule.py`'s committed values to four decimal places.**
**So the source rule is reproduced exactly, and the framework's `SOURCE` arm is known to be correct rather
than assumed to be.**

**The `NORULE` weighted arm returns 0.5700 against `10_robust_and_class.py`'s 0.7289.** **The difference is
that this framework computes the weighting denominator after common-mode removal and over the uniquely-named
columns, while `10_robust_and_class.py` computes it before common-mode removal over all columns.**
**That is a further sub-choice within the weighting and is not pursued here; it is named because the two
values are otherwise both labelled weighted.**

## 2. The measurement that matters

```
unweighted family:  d_A = 0.3933 to 0.4495,   a range of 0.0561
weighted   family:  d_A = 0.5700 to 0.7512,   a range of 0.1812
V2-C4 reports:      d_A = 0.0852 to 0.7289,   a span of 0.6437
```

> **Within a single weighting family, the two specifications span 0.056 unweighted and 0.181 weighted. The
> span V2-C4 reports, 0.644, is about eleven times the unweighted within-family span and about 3.6 times the
> weighted one.**

**And the weighting's own contribution is larger than the whole within-family span:**

| specification | without the weighting | with | the weighting's contribution |
| --- | --- | --- | --- |
| NORULE | 0.3933 | 0.5700 | **+0.1767** |
| SOURCE | 0.4495 | 0.7512 | **+0.3017** |

## 3. What V2-C4's claim becomes, third revision

**Unchanged, and now demonstrated rather than argued:**

> **The specification is in the pipeline's code and not in its data file, and the dimensions that move the
> estimate most are the ones the artifact does not name. Six of them are now enumerated with measured sizes,
> and the single one the source declares is the smallest.**

**Corrected, and measured this time:**

> **Within one weighting convention, two specifications that differ in window, baseline, read-out and
> inclusion criteria span `d_A` 0.393 to 0.450. Adding the per-event weighting moves each by 0.18 to 0.30.
> The span of 0.085 to 0.729 that V2-C4 reports is therefore composed mostly of two things it does not list:
> the weighting, and a further change of read-out inside `12_inverse_variance_weighting.py` whose two values,
> 0.1580 and 0.0852, this framework does not reproduce.**

**The one-line version: the range is real, and eleven twelfths of it is choices the range's own table does not
name.**

## 4. What this framework did not do, stated so it is not read as more than it is

* **It does not reproduce `12_inverse_variance_weighting.py`'s 0.1580 and 0.0852.** **Those two values remain
  traceable only to their own script, and they are the two lowest in V2-C4's range.** **So the corrected range
  in section 3 is measured for two of the four values and stated by exclusion for the other two.**
* **It does not resolve the sub-choice inside the weighting that separates 0.5700 from 0.7289.** **Named in
  section 1, not tested.**
* **It is two specifications, not the space of defensible specifications.** **`SPECIFICATION_LEDGER.md`
  records what is known about the space; this is a point in it.**

## 5. V2-C4's status after four rounds of testing

| round | what was tested | outcome |
| --- | --- | --- |
| 24 | are its four values all Cohen's `d`? | **yes** |
| 28 | does the notation audit hold on recount? | **yes** |
| 31 | is its range reproduced by a declared grid? | the grid's family differs; ceiling 0.4408 |
| 37 | does its range mix families? | **yes: 0.729 weighted against three unweighted** |
| **38** | **measured in one framework** | **within-family span 0.056 unweighted, 0.181 weighted; the weighting contributes 0.18 to 0.30 each** |

**V2-C4 has survived four rounds of testing and its claim has been corrected three times, each correction
making it stronger rather than weaker: the specification is not in the file, and the proof is now a measured
enumeration rather than a range whose composition was unknown.**

## 6. Provenance

* Script `anatomy/36_family_2x2.py`; output `anatomy/RESULT_family_2x2.json`.
* **The `SOURCE` unweighted arm reproduces `11b_source_rule.py`'s `d_A`, `diff` and `sd` to four decimals,
  which is the implementation check.**
* **No model was fitted. No causal claim is made.**
