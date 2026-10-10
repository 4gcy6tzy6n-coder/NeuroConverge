# Two-coder comparison and adjudication of the reliability-reporting base rate

**Coder 1 is this line; coder 2 ran in an isolated context on the SAME packet, having read only the protocol
and the records.** **Both were frozen before comparison.** **The disagreement is reported rather than
smoothed, because it is the reason a two-coder design was used.**

## The two codings, before adjudication

| code | coder 1 (this line) | coder 2 (isolated) |
| --- | --- | --- |
| **R** | 1 | 0 |
| **R-OTHER** | 2 | 1 |
| **N** | 122 | 124 |
| **NC** | 4 | 4 |

**Coder 1 R rate: 1/125 = 0.8 per cent.**
**Coder 2 R rate: 0/125 = 0.0 per cent.**

**They disagree on 3 record(s): 39948086, PPR803506, PPR914301.**

## The disagreement, and why coder 2 is right

**Both coders agree that PPR914301, the connectome-constrained dynamical model of the C. elegans brain, is the
only record in the frame carrying any reliability-type figure.** **They disagree on whether it is an R or an
R-OTHER.** **The sentence is:**

> *"This dynamical model ... captured causal interactions between all pairs of neurons 82% as well as the
> reproducibility of the perturbation data themselves."*

**CODER 2 IS RIGHT AND CODER 1 WAS WRONG.** **The 82 per cent is the MODEL's fit, expressed against the
reproducibility of the data as a CEILING.** **It measures how well a model captures interactions, not how
reliably the functional quantity itself is measured. The figure for the functional quantity is the ceiling, and
it is not reported as a number.** **Coder 1 treated the presence of a figure as sufficient without asking what
the figure measures, which is the same failure the manuscript documents elsewhere.**

**The second disagreement is the same kind in the other direction.** **Coder 1 coded 39948086 and its preprint
as R-OTHER on the strength of the phrase "provides the most reliable estimation of the known ground truth
connectivity matrix". Coder 2 coded N, because the protocol requires a FIGURE and "most reliable" is an
adjective with no number attached.** **Coder 2 is right on the protocol as written.**

## Adjudicated result

| code | n |
| --- | --- |
| **R** | 0 |
| **R-OTHER** | 1 |
| **N** | 124 |
| **NC** | 4 |

**Codable: 125 of 129.**
**R rate = 0/125 = 0.0 per cent.**
**R rate counting R-OTHER as R = 1/125 = 0.8 per cent.**

**The pre-registered thresholds: above 20 per cent withdraw the sentence, 5 to 20 rewrite it to state the
rate, below 5 it may stand as a measured description.** **At 0.8 per cent it
stands either way the R-OTHER question is decided, so the disagreement does not change the manuscript's
conclusion.**

## Both coders' shared findings

* **The frame contains 14 apparent duplicate pairs**, a published article and its preprint. **This is a property
  of the Europe PMC citation endpoint and not a coding error, and it does not change the rate.**
* **Approximately 16 of 125 abstracts do not mention the functional quantity at all** (optics, instrumentation,
  transport, transcriptomics, philosophy), which both coders recorded separately as the weakest evidence
  either way.
* **The unit is the abstract.** **A reliability figure reported only in a Methods section is invisible to this
  design and is not counted, which is the limitation the protocol states first.**

## Provenance

* **Protocol:** `../PROTOCOL_reliability_reporting_base_rate.md`, committed before any abstract was read.
* **Coder 1:** `CODER1_RESULT.md`, frozen before coder 2's output was read.
* **Coder 2:** an isolated context that received only the protocol and `CITING_RECORDS_PACKET.md`. **It reported
  one self-correction in its own counts line, from NC = 3 to NC = 4, which is retained in the record.**
* **Neither coder is independent of the line in the sense the plan requires for review; they are independent of
  EACH OTHER, which is a weaker and different guarantee.**
* **No model was fitted. No causal claim is made.**
