# Independent re-implementation attempt: NOT REPRODUCED in eight attempts, and it names dimensions this line had not measured

**A re-implementer naive to this corpus was given the pipeline's public repository, the deposited wild-type export, and
the paper's stated convention, and was forbidden from reading any of this project's derivations.** **The protocol,
including the stopping rule and the falsification criterion, was committed before launch.**

## The result

**NOT REPRODUCED.** **Stopping condition 2 was met (three distinct end-to-end attempts without reproduction; it made
EIGHT) and condition 4 was also exceeded (one hour).**

| what it ran | value | n |
| --- | --- | --- |
| best on the explicitly COMBINED contrast | **d = 0.7158, t = 7.4387** | 108 |
| best overall across variants (gap-junction-only contrast) | d = 0.7240, t = 7.5589 | 109 |
| literal union, all anatomically connected vs unconnected | d = 0.8730, t = 9.1149 | 109 |
| **the target** | **d = 0.7289, t = 7.610** | **109** |

**Its scan over defensible variants put d between 0.69 and 0.92, and NO defensible combination landed on 0.7289.**

## What it could not obtain, named

**The exact operational definition of the COMBINED measure.** **The paper's stated convention fixes the window, the
baseline and the normalisation, and leaves UNDETERMINED:**

* **(a) which anatomical source and threshold define "connected" -- White 1986, Witvliet 2020, their sum, thresholds
  0, or thresholds of 3 chemical and 2 gap-junction;**
* **(b) whether "combined" is the UNION of chemical and gap-junction pairs or their INTERSECTION;**
* **(c) how trials and pairs are pooled.**

**It reports that these are exactly the degrees of freedom that move the estimate, and that they are not recoverable
from the published convention.**

## What it DID reproduce, exactly

**It found that `t / d = sqrt(109)` holds for the target: `7.610 / 0.7289 = 10.4403 = sqrt(109)`.** **That confirms
n = 109 independently, and confirms that the target is the one-sample statistic on the per-animal contrasts.**
**It is the first independent confirmation of any quantity in this paper, and it confirms the structural claim of
section 2.5 from outside this line.**

**It also could not run the pipeline itself, because `wormdatamodel`/`wormbrain` and the recording folders are not
present; it re-implemented the identity mapping and the connectome loader from the repository source instead.**

## What this does to the manuscript, per the criterion fixed in advance

**The protocol stated: a FIRST-attempt success obliges the manuscript to say that a naive re-implementer succeeded
immediately and that this line's six failures are evidence about this line rather than about the task; a success in
two or three attempts leaves the case study as written with the attempt count reported; and an inability to attempt
for a nameable access reason leaves the scope unchanged.**

**None of those three occurred.** **The re-implementer COULD attempt, DID attempt eight times, and did NOT succeed.**
**So the case study stands as written, and the attempt count is now reported alongside this line's six: an
independent re-implementer, given the public repository, the deposited data and the published convention, made
EIGHT attempts and did not reproduce the target.**

## Two things this changes, and one it does not

**IT ADDS SPECIFICATION DIMENSIONS THIS LINE HAD NOT MEASURED.** **The ledger's seven plus a redundant eighth do not
include the anatomical source and threshold, the union-versus-intersection question, or the pooling of trials and
pairs.** **Those are at least two further undeclared dimensions, and they are named HERE rather than added to the
ledger, because measuring their isolated sizes would be new analysis and this document does not claim it.** **They
are recorded as dimensions the independent attempt found and this line had not enumerated, which is a limit of the
ledger rather than a result.**

**IT CORROBORATES THE CENTRAL CLAIM FROM OUTSIDE.** **The claim is that a pipeline's specification lives in its code
and not in its output.** **An independent party, given the output and the paper's stated convention and nothing else,
spent an hour and eight attempts and could not recover the number, and named the degrees of freedom it could not
resolve.** **That is the claim, demonstrated by someone who had never read this line's work.**

**IT DOES NOT LICENSE CALLING THE ARTIFACT IRRECOVERABLE.** **This line DID reproduce the target, by reading the
code and comparing intermediate values.** **The artifact is recoverable from the code; what is not recoverable is the
specification from the OUTPUT.** **Those are different statements and the manuscript already distinguishes them.**

## Limits of this attempt, stated

* **The re-implementer is a model, not a human, and shares a model family with this line, so a shared blind spot is
  possible.**
* **It could not run the pipeline itself and re-implemented parts of it from source.**
* **Eight attempts in an hour is not the same as eight attempts by a person with different priors.**
* **It is not independent of this line in the sense a review requires.**

## Provenance

* **Protocol:** `../PROTOCOL_independent_reimplementation.md`, committed before launch.
* **Inputs it received:** the pumpprobe repository, `/tmp/osf/w/exported_data`, and the paper's stated convention.
* **Inputs it was forbidden:** every file under `v2/wp3_results`, `v2/wp1_data` and `v2/wp0_freeze`.
* **No model was fitted by this line in this exercise.**
