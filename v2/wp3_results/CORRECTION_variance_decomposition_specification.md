# CORRECTION: V2-C3's pair-specific component is specification-dependent; only the measurement-error share is robust

**Status: this narrows V2-C3 materially. Its four published numbers reproduce exactly, and one of them turns
out to be an artefact of a specification that is not well-posed.** No model was fitted.

**This is the tenth self-found measurement defect in this line, found by attempting a replication that
failed for a reason that was mine, and it is the most consequential since round 12.**

---

## 1. How this was found

**The line's four claims all rest on one dataset, so a generalisation test was attempted. The DANDI `000541`
record has 21 sessions and each is about 1.4 GB, which is roughly 30 GB against a 10 GB budget, so that route
was closed and recorded as closed.**

**The `unc-31` arm was then used instead: 18 animals, a different genotype, same laboratory and preparation.
Running the decomposition on it produced `beta = -35.7 %`, an impossible negative variance.** **Investigating
that produced the finding below.**

## 2. The four published numbers reproduce exactly

**The replication script had added an atlas-membership filter that V2-C3 does not need** -- the decomposition
is over **all** pairs and never consults connectivity, so requiring both neurons to appear in `funatlas.h5`
was gratuitous. **That alone moved the unit count from 192,303 to 173,954.**

**With the round-12 filter restored, the WT run returns exactly:**

| component | published (round 12) | re-run | units |
| --- | --- | --- | --- |
| between-pair | 55.1 % | **55.1 %** | 192,303 |
| measurement error | 37.5 % | **37.5 %** | |
| pair-specific animal | 5.5 % | **5.5 %** | |
| animal offset | 1.9 % | **1.9 %** | |

> **So the first conclusion is that V2-C3 reproduces and the replication script was the thing that was wrong.
> That is recorded because the opposite was nearly reported.**

## 3. But `beta` is not identified at the specification V2-C3 uses

**The decomposition subtracts: `var_beta = var_total - var_alpha - var_pair - var_eps`.** **`var_pair` is the
variance of pair means, and a pair mean computed from ONE animal is a noisy estimate whose variance inflates
`var_pair` and drives `var_beta` toward zero or below.**

**Restricting to pairs measured in at least `K` animals, in both arms:**

| `K` | WT pairs | WT `beta` | WT `eps` | unc-31 pairs | unc-31 `beta` | unc-31 `eps` |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | 40,699 | **5.5 %** | 37.5 % | 14,751 | **-37.1 %** | 59.8 % |
| **2** | 25,793 | 31.3 % | 37.5 % | 6,643 | **-4.9 %** | 60.5 % |
| **3** | 19,951 | 38.5 % | 37.1 % | 3,222 | 5.1 % | 60.2 % |
| **5** | 13,199 | 43.1 % | 37.9 % | 697 | 7.3 % | 63.0 % |
| **10** | 5,757 | **46.0 %** | 38.5 % | -- | insufficient | -- |

**Two things follow.**

**First, `beta` moves by a factor of eight, from 5.5 % to 46.0 %, as the restriction tightens, and it is
NEGATIVE at `K = 1` and `K = 2` in the mutant arm -- an impossible value for a variance share.** **The
published 5.5 % is therefore not a property of the data; it is the value the subtraction returns when the
noisiest pair means are included.**

**Second, and this is what survives: `eps` is stable.** **37.5 %, 37.5 %, 37.1 %, 37.9 %, 38.5 % across the
whole range in WT, and 59.8 % to 63.0 % in the mutant.**

> **The robust statement is: within-cell measurement error accounts for 37 to 39 % of the variance in a
> pair's response in this atlas, and that share is insensitive to how many animals each pair was measured in.
> The pair-specific animal share is not robust, ranges from 5.5 % to 46.0 %, and can be driven negative by
> the estimator.**

## 4. What this does to V2-C3, and what it does not

**Narrowed:** V2-C3 as stated -- *"55.1 % between-pair, 37.5 % measurement error, 5.5 % pair-specific animal
deviation and 1.9 % homogeneous animal offset"* -- **mixes one robust share with one that is
specification-dependent.** **The corrected statement:**

> **A pair's response decomposes into a between-pair share, a within-cell measurement-error share of 37 to
> 39 %, a pair-specific animal share of 5.5 % to 46.0 % depending on the minimum-animals-per-pair
> restriction, and a homogeneous animal offset of about 1.9 %. The measurement-error share is robust; the
> pair-specific share is not identified at the unrestricted specification, as the negative values in the
> mutant arm demonstrate.**

**Not changed:** the measurement-error share, which is the part round 12's correction turned on, and which
this analysis strengthens by showing it is stable rather than an artefact. **And the fact that the published
numbers reproduce exactly at their own specification.**

## 5. The generalisation attempt, honestly reported

**The decomposition does NOT replicate quantitatively across genotypes.** **`eps` is 37.5 % in WT and 59.8 %
in `unc-31`.**

**Three reasons, all of which bound the comparison, and none of which can be ruled out with this data:**

* **The mutant arm has 15 usable animals against 112**, and 539 events against 3,333, so its pair means are
  far noisier -- which is exactly the condition that inflates `eps` and breaks `beta`.
* **A dense-core-vesicle mutant plausibly has different response variability**, so a difference is not
  necessarily an artefact.
* **The restriction that makes `beta` well-posed in the mutant leaves 697 pairs at `K = 5`,** where the
  estimate is fragile.

**What CAN be said: the decomposition's structure -- a stable measurement-error component that is the second
largest -- appears in both arms when the specification is well-posed, and its magnitude differs.**

## 6. The rule this establishes

**A variance decomposition whose last component is obtained by subtraction must report the restriction under
which the components remain non-negative, and must show the components as a function of it.** **A single
number for a subtracted component, reported without that sweep, can be an artefact of the least reliable
stratum.**

**This line reported one such number in round 12 and this document is the correction.**

## 7. Provenance

* Script `anatomy/23_variance_decomposition_sweep.py`; output
  `anatomy/RESULT_variance_decomposition_sweep.json`.
* The failed replication is retained as `anatomy/22_variance_decomposition_unc31_ATTEMPT1.py` with its
  output, so the path to this finding is visible.
* **The published round-12 numbers were re-derived and match exactly at their own specification.**
* **No model was fitted. No causal claim is made.**
