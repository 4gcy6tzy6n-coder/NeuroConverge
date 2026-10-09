# V2-C4's range spans two specification families, and the specification ledger

**Status: V2-C4's headline range mixes a weighted pipeline against three unweighted ones.** **The ledger below
is the structure the manuscript needs: every claim, the dimensions it depends on, and each dimension's
measured size.** No model was fitted.

**This is the seventeenth self-found defect, and the same class as rounds 24 and 27: quantities from
different specification families compared as though they were one range.**

---

## 1. The finding

**V2-C4 states that re-analysing the same records under defensible choices moves the animal-level estimate
across `d` 0.085 to 0.729.** **Tracing each of those four values to the script that produced it:**

| value | producing script | per-event `sd` weighting | family |
| --- | --- | --- | --- |
| **0.7289** | `10_robust_and_class.py` | **yes** (`sd = nanmedian(nanstd(dv, axis=1)); dvs = dv/sd`) | **weighted** |
| **0.4495** | `11b_source_rule.py` | **no** | **unweighted** |
| **0.1580** | `12_inverse_variance_weighting.py` | **no** | **unweighted** |
| **0.0852** | `12_inverse_variance_weighting.py` | **no** | **unweighted** |

**And round 34 measured the weighting's size: it is worth 0.3356 in `d_A`, reproducing the code's 0.7289
exactly when included and giving 0.3933 when omitted.**

> **So V2-C4's range is not a range over comparable choices. Its upper end comes from a pipeline that weights
> each event by the inverse of its across-cell spread, and its lower three ends come from pipelines that do
> not.** **Within the unweighted family the range is 0.085 to 0.450; the 0.729 lies in the other family.**

## 2. What V2-C4's claim becomes

**Unchanged:** *the specification is not recoverable from the data file.* **This round strengthens that rather
than weakening it, by adding a sixth undeclared dimension and by showing that the line's own range mixed two
families without noticing.**

**Corrected:** the range.

> **Re-analysing the same records under defensible choices moves the animal-level estimate across `d` 0.085 to
> 0.450 when the choices are held within one weighting convention, and across 0.39 to 0.73 within the other.
> A further choice -- whether each stimulus event is weighted by the inverse of its across-cell spread -- moves
> the whole family by 0.34, so a range that mixes the two conventions spans 0.085 to 0.729 without that span
> being attributable to the choices it lists.**

**The one-line version: the range is real, and its widest extent comes from mixing two families rather than
from varying one.**

## 3. The specification ledger

**Every dimension this line has found, with its isolated contribution measured by varying that dimension alone
and holding the others fixed, and whether any document declares it.**

### For `d_A`, the animal-level standardised effect

| dimension | levels | isolated size | declared? |
| --- | --- | --- | --- |
| **per-cell normalisation** | none vs pre-stimulus SD | **0.3395** | **no** |
| **per-event weighting** | none vs `1/across-cell SD` | **0.3356** | **no** |
| **post-stimulus window** | 12 / 24 / 48 volumes | **0.2364** | **no** |
| baseline convention | volumes 30-60 vs 0-60 | 0.0295 to 0.0496 | **yes, in the source** |
| common-mode removal | none / scalar / per-volume | 0.0103 to 0.0285 | no |
| common-mode cell pool | all columns vs uniquely-named | **0.0038** | no |
| inclusion rule | none vs >=10 connected, >=50 unconnected | **0.0000** | no |

**Within the unweighted family the grid spans `d_A` 0.1004 to 0.4408; the code's weighted configuration gives
0.7289.**

### For the three-level decomposition's shares

| dimension | levels | isolated size | declared? |
| --- | --- | --- | --- |
| **per-event weighting** | none vs `1/across-cell SD` | **`eps` 13.0 points, `beta` 11.5 points** | **no** |
| read-out | signed sum vs window mean | about 13 points in `eps` | no |
| post-stimulus window | 12 / 24 / 48 volumes | see `RESULT_eps_specification_grid.json` | no |
| minimum animals per pair | 1 / 2 / 3 / 5 / 10 | **`beta` 5.5 % to 46.0 %, and negative at 1** | no |

**Reported `eps` has ranged 17 to 57 per cent across these dimensions, none of which was varied together with
the others until rounds 34 to 36.**

### For the effect's between-animal spread

| dimension | levels | isolated size | declared? |
| --- | --- | --- | --- |
| nine technical covariates | animal-level recording properties | **adjusted `R^2` 0.0025** | no |
| pair-set restriction | K = 1 / 2 / 3 / 5 | **does not change the spread or its signal share** | no |
| pair composition | leave-one-animal-out prediction | **`R^2` 0.1772** | no |

**And the spread's own decomposition: 42.2 per cent measurement noise, about 40 per cent unexplained.**

## 4. What the ledger is for

**It is the structure a manuscript needs, and it did not exist until this round.** **For each claim it states
which dimensions the claim depends on, how large each is, and whether the artifact declares it.**

**Read across the tables, the pattern is the contribution:** **the dimensions that are declared are the small
ones, and the largest -- per-cell normalisation, per-event weighting, the post-stimulus window -- are declared
nowhere.** **The baseline convention, the only dimension the source states, is worth 0.03 to 0.05, while three
undocumented dimensions are each worth 0.24 to 0.34.**

**That is V2-C4's claim, quantified: what a user of the artifact cannot recover from the file is larger than
what they can.**

## 5. What is owed

1. **A grid over the two largest dimensions together** -- per-cell normalisation and per-event weighting --
   since their isolated sizes are nearly equal and their combination is untested.
2. **The four V2-C4 values recomputed in a single family,** so the corrected range in section 2 is measured
   rather than constructed by subtraction.
3. **The two items that remain external:** an independent reviewer, and the owner's decision on the plan's
   constraint.

## 6. Provenance

* `11b_source_rule.py` and `12_inverse_variance_weighting.py` were searched for `sd =`, `/sd`, `nanstd` and
  `nanmedian`; neither applies the weighting. `10_robust_and_class.py` and `07_final_estimate.py` both do, in
  different forms.
* Isolated contributions computed by varying one axis and holding the others fixed, from
  `RESULT_v2c4_specification_grid.json` and `RESULT_v2c4_cellpool_grid.json`.
* **No model was fitted. No causal claim is made.**
