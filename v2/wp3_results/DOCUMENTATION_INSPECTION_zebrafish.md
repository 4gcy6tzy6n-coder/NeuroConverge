# Documentation inspection: one further published matrix declares more than the audited atlas does

**This addresses R2-M1's third resolution route, which is to show whether the undeclared dimensions are also
absent from the documentation of two or three further published matrices, by document inspection rather than
re-analysis.** **The protocol was committed before any document was read, in
`../PROTOCOL_documentation_inspection.md`.** **The result is a PARTIAL REFUTATION, and it is reported as one.**

## The matrix inspected, and why

**Larval zebrafish whole-brain functional networks, from the Science Advances paper *Structural and genetic
determinants of zebrafish functional brain networks* (doi:10.1126/sciadv.adv7576, PMC12248300, open access).**
**It is the nearest same-kind case in the citing frame: a whole-brain optical functional matrix in a small
organism, computed as the audited atlas is, from calcium imaging.**

**Its own availability statement reads:**

> *"Data and materials availability: All data needed to evaluate the conclusions in the paper are present in the
> paper and/or the Supplementary Materials."*

## The seven dimensions, coded against the paper's own Methods and Results

| # | dimension | declared? | the text |
| --- | --- | --- | --- |
| 1 | signal transform / normalisation | **U** | the paper converts to relative fluorescence change "using the following sequence of operations", but the FC is computed on averaged regional activity without stating a further normalisation |
| 2 | per-observation weighting | **U** | no weighting of observations is stated |
| 3 | time window / epoch | **D** | "during the 10-min spontaneous period" |
| 4 | baseline / reference convention | **U** | the ΔF/F0 sequence is named but the baseline window for the FC is not stated in the passage read |
| 5 | global / common mode | **D** | "regressing out a global signal from regional time series" |
| 6 | node or parcel pool | **D** | "averaged the activity of neurons within each region"; the regional parcellation is the pool |
| 7 | ORDER of operations | **D** | "regressing out a global signal ... BEFORE computing FC", an explicit ordering statement |

**So this matrix declares FOUR of the seven, against the audited atlas's ONE.** **Under the protocol's own
falsification rule this is not a refutation of the claim for this matrix, since four is below six, but it is a
clear counterexample to any claim that these dimensions are UNIVERSALLY undeclared, and it is reported as
such.**

## A second finding, which is a limitation of the census rather than of this matrix

**The paper reports a RELIABILITY figure for the functional quantity:**

> *"Network similarity scores are significantly higher when comparing individuals to themselves [diagonal values
> from matrix in (H)] rather than different individuals [off-diagonal values ...] (P = 3 x 10^-5, t test)."*

**That is an inter-individual agreement test on the functional matrix, which is exactly the quantity the census
codes for.** **The census coded this record N, because the figure is in the Results and NOT in the abstract.**
**The protocol states in advance that the unit is the abstract and that a figure reported only in a Methods or
Results section is invisible to the design.** **This record is the first case where that limitation was tested
against a known instance, and it FAILED to see it.**

**What follows from that, stated exactly:**
* **The measured rate of 0.0 per cent is a rate over ABSTRACTS, and this record shows abstracts undercount the
  true rate.** **The direction of the bias is known: the census is a LOWER BOUND.**
* **The census should be described in the manuscript as a lower bound on the reporting rate, not as the rate.**
* **The 129-record frame was not re-coded at full text, and doing so is a larger study than this one. It is
  named here as the next step rather than implied to be done.**

## What this does to the manuscript's claims

* **The negative finding survives as a lower bound**, and the manuscript must say lower bound.
* **The generalisation from one atlas to derived datasets generally is weakened**, because a same-kind matrix in
  the same frame declares four of the seven and reports reliability. **That is R2-M1's point and this inspection
  is evidence FOR it.**
* **The remedy the paper recommends remains supported**: publishing the specification is cheap, and this paper
  is an existence proof that some groups already do it.

## Limits of this inspection

* **One matrix was inspected, not three.** **The other two named in the protocol, the Human Connectome Project
  and UK Biobank, were not coded: their relevant documentation is a 3.5 MB reference manual and a web showcase,
  and coding them properly is a larger task than this round.** **They are named as not done rather than
  implied to be done.**
* **The coding above was done by reading the paper's own passages, not by re-analysis and not by a second coder.**
* **A dimension marked U means not stated in the passages read; it may be stated elsewhere in the paper.**

## Provenance

* **Protocol:** `../PROTOCOL_documentation_inspection.md`, committed before reading.
* **Source:** Europe PMC full text, PMC12248300; the passages quoted are from the Results and Methods.
* **No matrix was downloaded and no analysis was run. No model was fitted.**
