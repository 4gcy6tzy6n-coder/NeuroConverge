# Pre-submission review setup, round 58

**A three-reviewer assessment of the v2 manuscript, run in isolated contexts under the `nature-reviewer`
protocol.** **This file records the SETUP and the blindness boundary. It is written before any reviewer report
was read, so it cannot have been shaped by one.**

---

## 1. What this is, and what it is not

**It is three independent invocations of a reviewer procedure, each given only the manuscript and its own
emphasis brief, each running in a separate context so that no reviewer read another's report or a shared
concern ledger.**

**IT IS NOT AN INDEPENDENT REVIEW, and must never be reported as satisfying the plan's requirement for one.**
**The three reviewers share a common origin with the manuscript: all four derive from the same line and the
same repository knowledge.** **Role separation is a separation of EMPHASIS, not a separation of ERROR
PROCESSES; three lenses on one body of knowledge do not constitute three bodies of knowledge, and a concern
that all three miss is still missed.** **The plan's owed external reader remains owed.**

## 2. The immutable packet

**Each reviewer received exactly the manuscript path and the same assessment boundary.** **Each received a
different emphasis brief and a different, restricted list of supporting files it was permitted to open.**

| reviewer | emphasis brief (a working lens, not an identity) | permitted supporting files |
| --- | --- | --- |
| **R1** | **the evidence chain and measurement validity** | `SPECIFICATION_LEDGER.md`, `ORDER_AXIS.md`, `JOINT_GRID_VERIFIED_NONADDITIVE.md`, `CORPUS_INDEX.md`, `FIGURE_SOURCE_DATA.json` |
| **R2** | **significance, originality and venue fit** | `CORPUS_INDEX.md`, `LITERATURE_SURVEY_SPECIFICATION_AND_RELIABILITY.md`, `METHODS_LEVEL_SURVEY.md`, `SUBMISSION_READINESS_v2.md`, `AMENDMENT_constraint_lifted.md` |
| **R3** | **reproducibility, provenance and adversarial reading** | `PATH_LAYOUT.md`, `REFERENCE_IDENTIFIERS.md`, `GENERALISATION_ROUTE_CLOSED.md`, `tools/README.md`, `figures/make_figures.py` |

**The restricted lists deliberately OVERLAP ONLY ON `CORPUS_INDEX.md`.** **No reviewer was told what another
would emphasise, and none was given a draft synthesis or a hint about what had already been found.**

**The boundary every reviewer received, verbatim in substance:** a draft with six rendered figures, no
independent review, and every result resting on one atlas because the second-dataset fetch failed.

## 3. Freezing and synthesis rules that will be applied

1. **Each report is frozen as returned.** **No report is shown to another reviewer, and none is edited to
   reduce overlap or to manufacture disagreement.**
2. **Natural duplication is evidence of independent arrival and is reported as such; natural disagreement is
   likewise preserved rather than reconciled.**
3. **A concern is labelled consensus only when at least two reports raise the same underlying concern
   independently.**
4. **The synthesis is written in a separate pass, after all three are frozen, and states the limitation on
   independence in its own text.**

## 4. Why run a self-review at all, given section 1

**Because the previous eight rounds found nine real defects by reading the manuscript adversarially, one at a
time, and a three-lens pass reaches places a single reading does not.** **The self-review's value is diagnostic,
not evidentiary: it can find a defect, and it cannot certify the absence of one.**

## 5. Provenance

* **Protocol:** the `nature-reviewer` skill, applied at round 58.
* **Manuscript revision reviewed:** the draft at commit `cc99cad`.
* **No finding from this review is a publication claim until it is acted on and, where it is a measurement,
  re-verified.**

---

## 6. Revision drift, recorded rather than smoothed

**The three reviewers did not all read the same bytes, and the difference is measurable.**

| reviewer | manuscript revision | size |
| --- | --- | --- |
| **R2** | `cc99cad` | **30,525 bytes** |
| **R1 and R3, at launch** | `efa73dc`, whose manuscript is identical to `cc99cad` | **30,525 bytes** |
| **R1 and R3, which read the file from disk after launch** | `77b50bb` | **31,301 bytes** |

**The cause: this line continued working while the reviews were in flight.** **Round 59 found the quantity with
two ranges by a consistency sweep and fixed it in `0adbb5b`. Round 60 tightened an over-broad literature claim
in `77b50bb`.** **R1 and R3 therefore saw two changes that R2 did not, and R2 saw a revision in which both
defects are present.**

**What this does and does not invalidate.**

* **The three-way comparison IS valid for agreement and disagreement**, because all three launched against the
  same 30,525-byte manuscript and a difference in what they report cannot be caused by the later edits unless
  one of them happens to mention them.
* **R2-M5 is unaffected and remains the strongest evidence in this review.** **R2 raised the two-range conflict
  against a revision in which it existed, and this line found the same conflict independently in the same round
  by a different route.** **That convergence does not depend on which revision R1 or R3 read.**
* **A concern that R2 raised against `cc99cad` may already be fixed at `77b50bb`.** **The synthesis must
  therefore check every R2 concern against the CURRENT manuscript before reporting it as outstanding, and must
  say which revision each finding applies to.**
* **Nothing here licenses re-running R2 against the newer revision.** **A frozen report stays frozen; the
  correction belongs in the synthesis and in the manuscript's own record.**

**The operational lesson, recorded because it is the same class as everything else in this corpus: a report is
bound to the bytes it was written against, and "the manuscript" is not a stable object while the line is still
working on it.** **The setup file said the revision was `cc99cad`; the reviewers read the file, not the commit.**
