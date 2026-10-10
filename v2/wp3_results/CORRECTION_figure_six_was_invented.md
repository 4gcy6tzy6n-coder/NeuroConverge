# CORRECTION: Figure 6 presented an invented defect ledger, and the manuscript's count was wrong

**Status: the manuscript's Figure 6 was drawn from a table typed from memory, and both the names and the round
numbers were wrong. It is now derived from the artifacts, and the manuscript's defect count is corrected from
twenty-one to seventeen numbered defects.** No model was fitted.

**This is the twenty-second self-found defect, and the first found inside the manuscript itself rather than in
an analysis artifact. It is the same class the paper documents: a claim whose provenance was asserted rather
than traced.**

---

## 1. How it was found

**Round 50 began by reading the finished manuscript as a hostile reviewer would.** **The most exposed panel is
Figure 6, because it is the one figure whose data is a LIST rather than a measurement, and lists are easy to
type from memory.**

**They were typed from memory.** **The script's table read, in part:**

```python
defects = [("window convention",29,"re-implementation"), ...,
           ("duplicate-name pooling",8,"measurement"),
           ("ratio of medians",8,"measurement"), ...]
```

**Neither the round numbers nor the grouping came from an artifact.** **Checking them against the committed
documents found that the numbered sequence in this corpus runs fifth to twenty-first, and that the rounds
attached to each defect are different from the ones in the figure — for example the eighth defect's document
is `CORRECTION_heterogeneity_is_noise.md`, which the corpus records at round 26 and the figure labelled
round 8.**

## 2. The corrected derivation, and what it does and does not establish

**Figure 6 now reads each correction document, extracts the defect number that document states for itself, and
plots the defects against that NUMBER — which is the stated discovery order — with the document name as the
label.** **Nothing is typed.**

**Seventeen defects are derivable, numbered fifth to twenty-first, each from a distinct document:**

| # | document | # | document |
| --- | --- | --- | --- |
| 5 | `RETRACTION_window_dependence.md` | 14 | `CORRECTION_cell_pool_refuted.md` |
| 6 | `WINDOW_RESOLVED.md` | 15 | `CORRECTION_per_event_weighting_omitted.md` |
| 7 | `WITHIN_VS_BETWEEN_ANIMAL.md` | 16 | `CORRECTION_weighting_moves_the_decomposition.md` |
| 8 | `CORRECTION_heterogeneity_is_noise.md` | 17 | `SPECIFICATION_LEDGER.md` |
| 9 | `EFFECT_RELIABILITY_AND_PAIR_COMPOSITION.md` | 18 | `V2C4_RANGE_MEASURED_IN_ONE_FRAMEWORK.md` |
| 10 | `CORRECTION_variance_decomposition_specification.md` | 19 | `RETRACTION_joint_grid_wrong_axis.md` |
| 11 | `CORRECTION_unit_inflation_is_significance.md` | 20 | `ORDER_AXIS.md` |
| 12 | `CORRECTION_eps_is_a_range.md` | 21 | `GENERALISATION_ROUTE_CLOSED.md` |
| 13 | `CORRECTION_common_mode_cell_pool.md` | | |

**Defects one to four are referenced in prose but have no document that names them, so the derivable ledger
starts at five.** **The manuscript now says exactly that.**

**And the ROUND is deliberately not plotted.** **A round mentioned inside a document is not reliably the round
of discovery — `GENERALISATION_ROUTE_CLOSED.md` mentions round 26 and was written at round 48 — so an axis
labelled "round in which it was found" would assert something the derivation does not support.** **The first
attempt at this figure did exactly that; it is not repeated.**

## 3. Three derivation defects found while fixing it

**Fixing the figure took three iterations, and each was the same kind of error in a smaller place.**

1. **The first derivation matched `tools/README.md`,** which discusses the defects and would otherwise be
   credited with whichever number its prose happened to mention.
2. **The second excluded `tools/` by path and still matched `anatomy/README.md` and
   `reliability/README.md`.** **It now excludes any file named README, because a README discusses the defects
   and does not define one.**
3. **The first corrected figure still carried the old x-axis label,** asserting a round of discovery that the
   derivation does not support; the axis is now the defect number.

## 4. What this does to the manuscript

**One number changes: the abstract, the methods and the figure legend now say seventeen numbered defects rather
than twenty-one, and add that earlier ones are referenced without separate documentation.**

**Nothing else changes, because nothing else in the manuscript was typed from memory — every other number was
cross-checked against the artifact that produced it.**

**And the incident belongs in the paper's own argument.** **A manuscript about artifacts whose provenance is not
carried in the artifact had a figure whose provenance was not carried in the figure.** **It was caught by the
same method the paper recommends — tracing each value to its source — applied to the paper's own panel. That is
recorded here rather than quietly fixed.**

## 5. Provenance

* Correction applied to `../figures/make_figures.py`; the figure regenerated as `../figures/Fig6_defect_ledger.png`
  and inspected.
* **The derivation returns seventeen documents with no gaps in the sequence from fifth to twenty-first.**
* **No model was fitted. No causal claim is made.**
