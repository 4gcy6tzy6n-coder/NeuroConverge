# Two coders on the full-text dimension packet: 71 per cent agreement, and the falsification outcome flips

**Coder 1 is this line; coder 3 ran in an isolated context on the SAME full-text packet and received only the
protocol and the packet.** **Both codings were produced independently and are reported here rather than
reconciled.**

## The two tables

| dimension | P1 zebrafish, coder 1 | P1, coder 3 | P2 mouse, coder 1 | P2, coder 3 |
| --- | --- | --- | --- | --- |
| 1 transform / normalisation | U | **D** | **D** | **U** |
| 2 per-observation weighting | U | U | U | U |
| 3 time window / epoch | D | D | D | D |
| 4 baseline / reference | U | **D** | D | D |
| 5 global / common mode | D | **U** | D | **U** |
| 6 node or parcel pool | D | D | D | D |
| 7 ORDER of operations | D | D | D | D |
| **total D** | **4** | **5** | **6** | **4** |

**Agreement: 10 of 14 cells, 71 per cent.** **Four cells disagree, all of them on the same two questions: is a
transform declared when the operation sequence is named but its parameters are delegated, and is a common-mode
treatment declared when it is described for an alternative analysis rather than for the reported matrix.**

## The falsification outcome depends on the disagreement

**Coder 1 finds the mouse matrix at SIX of seven, which meets the protocol's criterion for refuting the claim
that these dimensions are generally undeclared.** **Coder 3 finds neither matrix reaches six, so under its coding
the criterion is NOT triggered.** **The outcome of a pre-registered falsification test therefore flips on four
contestable cells out of fourteen, which is the most important thing this comparison establishes.**

**Coder 3 named exactly which cells are decisive, which is better practice than naming only a total: P1 reaches
six if either its global-mode or its weighting cell flips to D, and P2 reaches six if BOTH its transform and its
global-mode cells flip.**

## Two places where coder 3 is right and coder 1 was wrong

**P1 DIMENSION 1: CODER 3 IS RIGHT.** **It quotes a sentence coder 1 did not find: \"Raw fluorescence traces
were then detrended for slow baseline drifts and converted to relative fluorescence change values, DeltaF/F0,
using the following sequence of operations.\"** **That IS a declared transform, and coder 1 coded the dimension U
from the assertion that the only normalisation sentence belonged to a different analysis.** **The sentence exists
and coder 1 missed it.**

**P2 DIMENSION 1: CODER 3'S U IS BETTER ON THE PROTOCOL AS WRITTEN.** **The protocol's decisive clause is that a
dimension counts as declared \"only if the documentation states the choice specifically enough that a reader
could reproduce it without reading the authors' code\".** **The mouse paper delegates the fluorescence-to-spike
transform to a previous paper with no parameters, so a reader CANNOT reproduce it from this documentation.**
**Coder 1 coded D on the strength of the neuropil-correction sentence, which names a step but not the decisive
transform's parameters.**

## What coder 1's coding got right, and what it cannot settle

**Coder 1's reading of the mouse ORDER cell is not disputed: the paper states that the residual is formed by
subtracting the mean response and then that the correlation is computed on it.** **The window, the pool and the
order agree across both coders for both papers.**

**AND THE CODING CANNOT BE SETTLED BY A THIRD CODER, because the disagreement is not about what the papers say
but about how strictly the protocol's reproducibility clause is applied.** **Two coders applying one written rule
to one packet produced tables whose totals differ by two, and by enough to flip a pre-registered test.** **That is
a property of the instrument and it is reported as one.**

## The consequence for the manuscript

**The manuscript currently states that two matrices declare FOUR and SIX and that the second meets the
falsification criterion.** **Under the second coding the counts are FIVE and FOUR and the criterion is not met.**
**The manuscript must therefore NOT carry the criterion's outcome as a finding.** **It carries the weaker and
agreed statement instead: that the two matrices declare five and four or four and six depending on how strictly
the reproducibility clause is read, that both figures exceed the audited atlas's ONE, and that the dimensions are
therefore not universally undeclared while no rate can be quoted from a sample of two.**

## Provenance

* **Packet:** `DIMENSION_CODING_PACKET_v2.md`, verified to contain each paper's Methods.
* **Protocol:** `../PROTOCOL_documentation_inspection.md`, committed before any document was read.
* **Coder 1:** this line, `DIMENSION_CODER1_v2.md`. **Coder 3:** isolated context, this file.
* **Neither coder is independent of the line in the sense a review requires; they are independent of each
  other, which is weaker.**
* **Coder 3 also recorded that the packet's section offsets are first-occurrence offsets of the pointer
  strings rather than section starts, which is a flaw in the packet's index and not in its contents.**
* **No model was fitted. No matrix was downloaded.**
