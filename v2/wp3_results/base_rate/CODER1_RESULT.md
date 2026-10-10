# Coder 1 result: the reliability-reporting base rate among the 129 citing records

**Coder 1 is THIS LINE. It is not an independent coder, and the manuscript must say so.**
**The assignments below were made in one pass after reading the full abstract text of all 125 records that
have one, and were frozen before the second coder's output was read.**

| code | n |
| --- | --- |
| **R** | 1 |
| **R-OTHER** | 2 |
| **N** | 122 |
| **NC** | 4 |

**Codable: 125 of 129 (four records carry no abstract).**

**R rate = 1/125 = 0.8 per cent.**
**R rate counting R-OTHER as R = 3/125 = 2.4 per cent.**

## The R assignment, with the sentence that carries it

* **PPR914301**: *"captured causal interactions between all pairs of neurons 82% as well as the reproducibility of the perturbation data themselves"*

## The R-OTHER assignments

**A reliability figure for something OTHER than the functional quantity.** **Both records are the same
paper, one published and one its preprint.**

* **39948086**: *"provides the most reliable estimation of the known ground truth connectivity matrix"* -- the reliability is of a METHOD's estimate against known ground truth, not of a measured functional quantity.
* **PPR803506**: *"provides the most reliable estimation of the known ground truth connectivity matrix"* -- the reliability is of a METHOD's estimate against known ground truth, not of a measured functional quantity.

## Borderline records, coded N and listed because a reader may disagree

* **41874539** and its preprint **PPR62030**: *"we find that they are robust, reproducible statistical
  measures and are remarkably similar across stimuli"*. **This asserts reproducibility of a functional
  quantity but reports NO FIGURE in the abstract, so the protocol's rule, which requires a figure, codes it
  N. It is the record most likely to be coded R by another coder.**
* **39663407**: *"assessments of reliability and out-of-sample validity are lacking"*. **A statement that
  such assessments are ABSENT, not an instance of one, so N. It is corroboration for the finding rather
  than an exception to it.**
* **PPR1046242**: reports that a functional-structural correlation decreases linearly with region count.
  **A robustness check against an analysis choice, not a reliability figure for the quantity.**
* **40660942**: *"development, activity, and reproduction of nematodes in the microfluidic device seems more
  stable"*. **Stability of a device comparison, not a reliability figure.**

## What this does to the manuscript

**The protocol fixed the thresholds before the coding: above 20 per cent the sentence must be withdrawn,
between 5 and 20 it must be rewritten to state the measured rate, and below 5 it may stand as a measured
description.** **The measured rate is 0.8 per cent, below 5, so the sentence stands AND
now carries a denominator, which is what the reviewer asked for.**

## Provenance

* **Frame:** Europe PMC `/MED/37914938/citations`, 129 records; the frozen frame is `citations_frame.json`
  and the coding packet, which is the same input both coders received, is `CITING_RECORDS_PACKET.md`.
* **Protocol written and committed BEFORE the abstracts were read**, in
  `../PROTOCOL_reliability_reporting_base_rate.md`.
* **Coder 1 is this line and is not independent.** A second coder was run in an isolated context on the same
  packet; the comparison is reported separately once both are frozen.
* **No model was fitted. No causal claim is made.**
