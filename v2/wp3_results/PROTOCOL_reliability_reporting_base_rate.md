# PROTOCOL, pre-registered: does the citing literature report a reliability figure for the quantity it predicts?

**Written BEFORE any abstract was read, because the coding rule must not be chosen after seeing what the
coding would find.** **This file exists because an isolated reviewer raised, as blocking, that the manuscript's
negative finding -- that none of the works it read reports a reliability figure for the functional quantity being
predicted -- has no denominator, and that the claim's importance depends entirely on a base rate the paper never
measures.**

---

## 1. The question, stated so that it can come out either way

**Of the works that cite the source atlas, what FRACTION report a reliability, reproducibility, agreement or
measurement-error figure FOR THE FUNCTIONAL QUANTITY THEY USE OR PREDICT?**

**This is deliberately narrow.** **A paper that reports the reliability of its own behavioural assay, or of a
recording rig, or of a segmentation method, does NOT count.** **The quantity must be the functional
connectivity, functional correlation, or functional response that the paper relates to structure.**

**And the question has three possible answers, all of which are reportable:**
* **the rate is LOW, which supports the manuscript's framing;**
* **the rate is HIGH, which refutes it and would require the manuscript's negative finding to be withdrawn;**
* **the rate is INTERMEDIATE, which would make the manuscript's remedy conditional and would weaken the
  motivating paragraph.**

## 2. The sampling frame, fixed before reading

**Frame: the 129 citing records of PMID 37914938 (Randi et al., the source atlas), retrieved from Europe PMC at
`/MED/37914938/citations` on the date recorded in the provenance section below.**

**Census rather than sample.** **All 129 records are in the frame.** **A census removes sampling error and
removes the temptation to report a rate from a subset chosen after the fact.** **If abstracts cannot be retrieved
for some records, they are reported as NOT CODABLE and the denominator is stated with and without them.**

**Recorded fields per citation, retrieved from the citations endpoint and NOT chosen by this line:**
`id`, `source`, `title`, `authorString`, `journalAbbreviation`, `pubYear`, `citedByCount`.

## 3. The coding rule, fixed before reading

**Each record is assigned exactly one code, in this order of precedence.**

| code | meaning |
| --- | --- |
| **R** | **The abstract reports a reliability, reproducibility, agreement, split-half, test-retest, ICC or measurement-error figure FOR THE FUNCTIONAL QUANTITY the paper relates to structure or predicts.** |
| **R-OTHER** | **The abstract reports such a figure, but for something else** (a behavioural assay, an imaging rig, a segmentation method, a behavioural readout, a model's own fit). |
| **N** | **The abstract reports no such figure at all.** |
| **NC** | **Not codable: no abstract available.** |

**The unit is the ABSTRACT, and the coding states that limitation.** **A figure reported only in a Methods
section is not visible to this design and is not counted as R.** **This is the same limitation the earlier
survey states first, and it is retained rather than relaxed.**

**Decided in advance, because these are the cases where a coder could drift:**
* **A paper that reports a correlation BETWEEN animals, or a split-half correlation of the functional matrix,
  counts as R.** **That IS the reliability of the quantity.**
* **A paper that reports only a model's predictive accuracy, a classification score or an R-squared against
  held-out data does NOT count as R.** **Those measure fit, not the reliability of the measured quantity.**
* **A paper that reports error bars or confidence intervals on a functional estimate does NOT count as R unless
  it states that the interval reflects measurement or inter-animal variability rather than sampling of a
  population.**
* **A review, an editorial or a methods paper counts and is coded on the same rule as a primary paper.**
* **A paper whose abstract does not mention the functional quantity at all is coded N, and the number of such
  papers is reported separately, because they are the weakest evidence either way.**

## 4. What will be reported, and what will not

**Reported:**
* **the three codes' counts and the R rate, with the denominator stated and the NC count broken out;**
* **for every R and R-OTHER, the sentence in the abstract that carries the figure, quoted;**
* **the same rate over the four works the earlier survey read in full, if they are in the frame;**
* **and the rate computed two ways, counting R-OTHER as R and counting it as N, since that choice is the one a
  sceptical reader would contest.**

**NOT reported:**
* **any claim that the result extends beyond this frame.** **The frame is the citers of one paper.**
* **any claim about the field as a whole, or about papers that do not cite this source.**
* **any causal explanation of the rate.**

## 5. Falsification criteria, stated in advance

**The manuscript's current sentence must be WITHDRAWN if the R rate exceeds 20 per cent, and REWRITTEN to state
the measured rate if it is between 5 and 20 per cent.** **If the rate is below 5 per cent the sentence may stand
as a measured description rather than as an impression.**

**These thresholds are chosen now, before the coding, so that they cannot be chosen to fit the result.**

## 6. Provenance

* **Frame retrieved:** Europe PMC `/MED/37914938/citations`, 129 records, `format=json`, `pageSize=1000`.
* **Abstracts:** to be retrieved from the Europe PMC search endpoint by `id`, after this protocol was written.
* **Coder:** this line. **It is NOT an independent coder, and the manuscript must say so; a two-coder design
  with a disagreement rate would be stronger and is not what is being done.**
* **No model was fitted. No causal claim is made.**
