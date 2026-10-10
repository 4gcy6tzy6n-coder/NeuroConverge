# Protocol addendum, pre-registered: full-text re-coding of a bounded subsample

**Committed BEFORE any full text is fetched, because the subsample rule and the coding rule must not be chosen
after seeing what the coding would find.** **It is an addendum to `PROTOCOL_reliability_reporting_base_rate.md`,
which fixed the census and the abstract-level rule.**

---

## 1. Why this addendum exists

**The census coded ABSTRACTS, and two documentation inspections have now caught that unit failing against known
instances: the zebrafish matrix reports an inter-individual agreement test and the mouse V1/HVA matrix reports a
split-half reliability of 53 +/- 24 per cent variance explained, and both figures are in the body and not in the
abstract.** **So the abstract-level rate is a LOWER BOUND, and the question this addendum asks is how much lower
it is.**

## 2. The subsample rule, fixed before any full text is read

**A record enters the subsample if its ABSTRACT contains at least one term from the reliability family:**

```
reliab*  reproduc*  test-retest  split-half  intraclass  ICC  measurement error  measurement noise
repeatab*  inter-animal  inter-individual  cross-animal  cross-subject  agreement
```

**This is a PRE-SPECIFIED, MECHANICAL rule.** **It is deliberately the WIDEST cheap screen: it takes every
record that even mentions the concept, so a figure in the body of such a record is the most likely kind of miss.**
**It cannot be gamed, because a record that does not mention the concept in its abstract is excluded by a rule
written before the full texts were fetched.**

**The subsample is expected to be small, on the order of fifteen records, which makes full-text coding feasible.**

## 3. The coding rule for this stage, unchanged in substance

**The same four codes, applied to the FULL TEXT rather than the abstract: R, R-OTHER, N, NC.**

**The decisive rule is unchanged: a code of R requires a reliability, reproducibility, agreement, split-half,
test-retest, ICC or measurement-error FIGURE for the FUNCTIONAL QUANTITY the paper relates to structure.** **An
adjective with no figure is not R. A figure for a model's fit, a method's accuracy, a behavioural assay or an
imaging rig is R-OTHER.** **A stated aim to analyse reliability, without a figure, is not R.**

**One clarification this stage needs, fixed now:** **a figure reported in a FIGURE, a figure caption, a
supplementary result, or a peer-review response that states what was done all count as "in the full text".** **A
reviewer's SUGGESTION that something should be reported does not count.**

## 4. Falsification criteria, fixed before the coding

* **If the subsample's R rate exceeds the whole-census rate by more than a factor of ten, the abstract-level
  census must be described in the manuscript as substantially unrepresentative rather than as a lower bound,
  and the full-text rate must be reported instead.**
* **If it exceeds it by less than that, the census stands as a lower bound and the subsample's rate is reported
  as the better estimate for records that mention the concept.**

## 5. What will and will not be claimed

**Will be claimed:** **the R rate among the records whose abstracts mention a reliability-family term, coded at
full text, and the ratio of that rate to the census rate.**

**Will NOT be claimed:** **that the subsample rate is the field's rate.** **The subsample is selected for
mentioning the concept, so it is a HIGH-RATE subsample by construction and its rate is an UPPER-ish estimate for
the frame, not a random-sample estimate.**

## 6. Provenance

* **Parent protocol:** `PROTOCOL_reliability_reporting_base_rate.md`.
* **Frame:** the same 129 citing records; the same `citations_frame.json`.
* **Coder:** this line, one coder, stated as a limitation exactly as in the parent protocol.
