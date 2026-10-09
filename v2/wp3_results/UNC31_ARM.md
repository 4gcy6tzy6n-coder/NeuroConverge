# The unc-31 arm: a pre-registered prediction that failed in direction, in a design that cannot test it

**Status: the first analysis of the mutant arm in this line. Its prediction is not supported and the design
is not capable of supporting or refuting it, and both statements are load-bearing.** No model was fitted.

---

## 1. The prediction, registered before the comparison was computed

**The source reports that extrasynaptic signalling, invisible to anatomy, contributes to the gap between
anatomical prediction and measured propagation.**

**`unc-31` is a dense-core-vesicle exocytosis mutant: it lacks neuropeptide release.** **If extrasynaptic
signalling is what fills that gap, then removing it should leave the anatomically mediated part, so the
connectivity-function association should be LARGER in the mutant.**

```
prediction:   d_unc31  >  d_WT
```

**Registered here before the comparison below was computed.**

## 2. The data

**`exported_data_unc31.tar.gz`, 84,924,311 B, 18 animals, all 18 with the complete file set. Three (indices
0, 3 and 4) carry zero uniquely named cells and are unusable, leaving 15; two more fail the minimum pair
counts, so 13 enter.**

| arm | usable | animals entering | events | median unique cells | median volumes |
| --- | --- | --- | --- | --- | --- |
| WT | 112 | **109** | 3,333 | 64 | 3,850 |
| **unc-31** | **15** | **13** | **539** | 70 | 4,470 |

**Both arms are processed by the identical function** -- same pre-window, same per-event analysis window,
same within-animal standardisation, same read-out, same anatomical matrices built by name. **The only
difference is the data directory.**

## 3. The result

| arm | animals | effect mean | SD | `t` | `d` | 95 % CI | positive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **WT** | 109 | **+0.1165** | 0.1617 | 7.523 | 0.7206 | [+0.0861, +0.1469] | 90/109 (82.6 %) |
| **unc-31** | 13 | **+0.0871** | 0.1119 | 2.804 | 0.7778 | [+0.0262, +0.1479] | 10/13 (76.9 %) |

**The pre-registered comparison:**

```
difference   -0.0294   (the WRONG DIRECTION)
SE            0.0347
z            -0.848
one-sided p   0.802
```

## 4. Two statements, and both are required

**First: the prediction is not supported.** The difference is negative, the opposite of what was predicted.

**Second, and this is what stops the first from being a refutation: the design cannot detect a difference of
the size it observed.**

| quantity | value |
| --- | --- |
| unc-31 animals | 13 |
| WT animals | 109 |
| equivalent equal-group `n` | 23.2 |
| **`d` detectable at 80 % power** | **0.8216** |
| **difference observed** | **0.0294** |
| **ratio** | **28** |

> **A difference would have to be about 28 times larger than the observed one to be detectable at this
> sample size. The comparison is therefore uninformative about the prediction, and reporting it as a
> refutation would be a misuse of a null result.**

**For scale: detecting a between-arm difference of `d = 0.5` at 80 % power needs 31 animals per group. The
mutant arm has 13.**

## 5. What the mutant arm does establish

**unc-31's own effect is significantly positive: `+0.0871`, `t = 2.804`, 95 % CI `[+0.0262, +0.1479]`, which
excludes zero, with 10 of 13 animals positive.**

> **The connectivity-function association is present in a dense-core-vesicle exocytosis mutant.**

**This is a positive finding and it does not depend on the between-arm comparison.** **If extrasynaptic
neuropeptide release were the entire mechanism behind the anatomy-function relationship, that relationship
should have been substantially weakened or absent here. It is neither, at least at this sample size.**

**What it does NOT establish:** that extrasynaptic signalling is irrelevant. **The mutant removes dense-core
vesicle release, not all extrasynaptic transmission; the CI is wide; and the arm is one mutant in one
preparation.**

## 6. What would make the comparison informative

| route | requirement |
| --- | --- |
| more mutant animals | about 31 per arm for `d = 0.5`, against 13 available |
| a paired or matched design | the same cells and pair sets in both arms, which the data does not provide |
| a within-animal mutant contrast | not available; the two arms are different animals |

**None is available within this record.** **The mutant arm's value is therefore the positive finding in
section 5, and the negative result in section 3 is recorded with its power attached so it cannot be quoted
without it.**

## 7. What this does to the line

**The four surviving claims are unchanged.** **V2-C1, V2-C2, V2-C3 and V2-C4 are all computed on WT and none
involves the mutant.**

**And one item moves off the owed list:** the `unc-31` arm, untouched since round 7, is now analysed. **Its
outcome is a significant association within the mutant and an underpowered between-arm comparison, and it is
recorded as exactly that.**

## 8. Provenance

* Script `anatomy/21_genotype_unc31.py`; output `anatomy/RESULT_genotype_unc31.json`.
* Data: `exported_data_unc31.tar.gz`, 84,924,311 B, from the same OSF record.
* The prediction is stated in the script's own docstring before the comparison, so the recorded prediction
  is the one that was registered.
* **No model was fitted. No causal claim is made.**
