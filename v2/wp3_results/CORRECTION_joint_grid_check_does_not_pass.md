# CORRECTION: the joint grid's correctness check does not pass, and the manuscript attributed another grid's pass to it

**Status: an isolated reviewer found, and checking confirmed, that the manuscript's verification section reports
the ORDER grid's successful check while presenting a result that comes from the JOINT grid, whose own check
differs by 0.0042 with a refuted explanation.** No model was fitted.

**This is the twenty-third self-found defect, and it is the most serious one in this corpus, because it affects
one of the two results the abstract leads with and because the paper's subject is exactly this failure.**

---

## 1. What the manuscript said

**Section 2.7, under the heading that presents the six consecutive re-implementation failures:**

> *"The resolution, in round 40, was to stop hypothesising and instead verify each re-implemented step against
> the code's own intermediate values for a single animal. Every intermediate then matched bit for bit -- `sd`
> exact, and `dv`, `dvs`, `cm` and `dev` with a maximum absolute difference of `0.000e+00` -- and with the
> verified sequence the pipeline's own configuration reproduced at `d = 0.7289` and `t = 7.610` against the
> code's `0.7289` and `7.610`."*

**And in the abstract:** *"the attempt failed for six consecutive rounds because our re-implementations differed
from the original code in ways not visible on reading it."*

## 2. What the committed documents say

**`JOINT_GRID_VERIFIED_NONADDITIVE.md` produces the non-additivity result the manuscript reports in section
2.2.** **Its section 2 states:**

> *"returns `d_A = 0.7331` and `t = 7.654`, against `09_animal_level.py`'s 0.7289 and 7.610 -- a difference of
> 0.0042 attributable to a slightly different event set."*

**`ORDER_AXIS.md` section 1 refutes that attribution:**

> *"Round 41 ... attributed the 0.0042 difference to a 'slightly different event set'. **That attribution was
> wrong: the exact match is available in this grid, and round 41's 0.0042 was an implementation difference it
> did not find.**"*

**So the bit-for-bit verification and the exact `0.7289` match belong to the ORDER grid.** **The JOINT grid's
check differs by `0.0042`, its proposed explanation was refuted, and the difference was never identified.**

## 3. Why this is the most serious defect in the corpus

**Three reasons, and the third is the one that matters.**

1. **It affects section 2.2, one of the two results the abstract leads with, and the result that licenses the
   paper's warning that a sensitivity table cannot be read additively.**
2. **It is a provenance failure of exactly the kind the paper documents: a reader who opens both committed
   documents finds the manuscript reporting a failed check as a passed one, in the section whose stated purpose
   is to demonstrate verification.**
3. **The verification narrative was written in round 41, whose own attribution the same round's successor
   refuted.** **So the corpus already contained the refutation when the manuscript was drafted, and the draft
   was assembled from the round-40/41 narrative rather than from the current state of the artifacts.** **This is
   the defect class the line has recorded since round 10, in its most consequential instance.**

## 4. A second defect in the same document, found while checking

**`JOINT_GRID_VERIFIED_NONADDITIVE.md` contradicts itself.** **Its summary states it is "the first grid in seven
rounds whose correctness check passes before its result is read", and its section 2 states that the check
differs by `0.0042`.** **Both cannot be true.** **Its TITLE calls the grid VERIFIED.**

**A dated banner now sits at the top of that document, recording the contradiction and stating that the check
does not pass.** **The body is left intact, because this corpus does not rewrite superseded text.**

## 5. What the manuscript now says

**Section 2.7 distinguishes the two grids, discloses the `0.0042` and the refuted explanation, and states that
the non-additivity in section 2.2 rests on a grid whose check does not pass.** **Section 2.2 carries a
PROVENANCE CAVEAT to the same effect, so a reader who reads only that result meets the limitation where the
result is stated rather than only in the verification section.**

**The non-additivity is reported as PROVISIONAL on the strength of the ORDER grid, where the same pair of
normalisations was measured with a check that passes, rather than on the joint grid whose check failed.**

## 6. What remains unresolved, stated rather than implied

* **The `0.0042` difference itself was never identified.** **Whether the joint grid's non-additivity values
  would change under a corrected implementation is unknown.**
* **The ORDER grid passed its check, so the ORDER result does not inherit this defect, but the ORDER grid does
  not itself measure the two-dimensional interaction that section 2.2 reports.**
* **A corrected joint grid has not been run.**

## 7. Provenance

* **Found by:** the isolated R1 reviewer of this line's three-reviewer self-review at round 62, whose report is
  frozen at `../wp5_governance/review/R1_evidence_chain.md`.
* **Attribution of the finding:** R1 raised the misattribution and the failed check together as its R1-M4,
  marked Blocking. **This line's own adversarial reading in rounds 50 to 60 did not find it, which bounds how
  much the previous ten rounds' self-review was worth.**
* **No model was fitted. No causal claim is made.**
