# Protocol, pre-registered: an independent re-implementation attempt with a stopping rule

**Written BEFORE the attempt is launched, so the stopping rule and the success criterion cannot be chosen after
seeing the outcome.** **R2's resolution test for the self-error ledger offered exactly this as its stronger
option, and its minimal form is: report how long a re-implementer naive to this corpus needed, given only the
artifact and the code, to reproduce one published number.**

---

## 1. The question

**Can a re-implementer who has never seen this line's derivations, given the published pipeline and the deposited
data, reproduce ONE number the audited paper reports -- and how long does it take?**

**The number to reproduce, fixed now: the animal-level standardised effect of the combined contrast, which this
line reproduced exactly at `d = 0.7289` with `t = 7.610`.**

## 2. What the re-implementer receives, and what it does not

**Receives:**
* **the pipeline's public repository locator;**
* **the deposited data's locator and its sha256;**
* **the target number and the two statistics it must match, `d` and `t`, to four decimal places where the
  comparison is exact;**
* **the pipeline's declared convention as the audited paper states it, and NOTHING about which axes this line
  found to matter.**

**Does NOT receive:**
* **this corpus, its correction documents, its specification ledger, or any of its scripts;**
* **any statement of which normalisation, weighting, window, baseline, order or common-mode treatment is
  correct;**
* **any hint that the specification is the difficulty.**

**The re-implementer is told the target is a re-implementation attempt and that it must report its own stopping.**

## 3. The stopping rule, fixed now

**The attempt STOPS when any of these occurs, and the first to occur governs:**

1. **the target number is reproduced to four decimal places;**
2. **THREE distinct re-implementation attempts have been made and none reproduces it;**
3. **the re-implementer concludes it cannot proceed for a reason it can name, such as a missing input or an
   unobtainable code revision;**
4. **a wall-clock budget of one hour of the re-implementer's own work.**

**An "attempt" means one complete end-to-end run producing a number, not one edit.**

## 4. What is recorded, whatever the outcome

* **which of the four stopping conditions occurred;**
* **the number or numbers produced by each attempt;**
* **the sequence of choices the re-implementer made that it believes could have mattered, in its own words;**
* **whether it named the input it could not obtain, if it could not;**
* **and how many attempts it took.**

## 5. The falsification criterion, fixed now

**If the target is reproduced on the FIRST attempt, the manuscript's case-study framing must be strengthened
against itself: it must state that a naive re-implementer succeeded immediately, and that the six failures this
line records are therefore evidence about this line rather than about the difficulty of the task.**

**If it is reproduced in two or three attempts, the case study stands as written and the attempt count is
reported alongside this line's six.**

**If it cannot be attempted for a nameable access reason, that is reported and the case study's scope is
unchanged.**

## 6. Why a subagent is an adequate re-implementer here, and what it is not

**It is naive to this corpus by construction, which is the property under test, and it can read the pipeline's
code and the deposited data.**

**It is NOT independent of this line in the sense a review requires, and it shares a model family with this
line, so a shared blind spot is possible.** **It is also not a human with a human's prior, and its failure modes
differ.** **The result is therefore a bound on difficulty and not a measurement of it.**

## 7. Provenance

* **No model is fitted to the atlas in this exercise beyond the re-implementation itself.**
* **The outcome is committed whatever it is, including a first-attempt success.**
