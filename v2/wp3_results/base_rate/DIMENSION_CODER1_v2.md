# Dimension coding on the FULL-TEXT packet, coder 1 (this line), version 2

**Coder 1 is THIS LINE.** **This replaces the version-1 coding, which was invalid because the packet was
truncated before the Methods and because coder 1 used material coder 2 never received.**

| # | dimension | zebrafish | mouse V1/HVA |
| --- | --- | --- | --- |
| 1 | signal transform / normalisation | **U** | **D** |
| 2 | per-observation weighting | **U** | **U** |
| 3 | time window / epoch | **D** | **D** |
| 4 | baseline / reference convention | **U** | **D** |
| 5 | global / common mode | **D** | **D** |
| 6 | node or parcel pool | **D** | **D** |
| 7 | ORDER of operations | **D** | **D** |
| | **total D** | **4** | **6** |

## The sentences, from the FULL texts

**Zebrafish (PMC12248300)**
* **3, 6**: "we averaged the activity of neurons within each region of the brain during the 10-min spontaneous
  period ... and then calculated the pairwise correlations between regional signals"; the region is the pool.
* **5, 7**: "regressing out a global signal from regional time series BEFORE computing FC".
* **1 is U**: the only z-scoring sentence in the paper belongs to the coactivation analysis, not to the FC, and no
  transform is stated for the regional signals that are correlated. **A coder counting the raw-trace processing
  as the transform would code D.**
* **4 is U**: no baseline or reference window is stated for the FC.

**Mouse V1/HVA (PMC13012721)**
* **1**: "Two-photon calcium imaging was motion corrected using Suite2p subpixel registration module ... Neuron
  ROIs and cellular calcium traces were extracted ... Neuropil contamination was corrected by subtracting the
  common time series (1st PC) of a spherical surrounding mask of each neuron from the cellular calcium traces.
  Neuropil contamination-corrected calcium traces were then deconvolved using a Markov chain Monte Carlo (MCMC)
  method." **The transform from calcium to the correlated quantity is stated.**
* **3**: "Noise correlation was defined as the trial-to-trial correlation of residual spike count (1 s time
  window, if not otherwise stated)".
* **4**: "after subtracting the mean response to each stimulus of the 72-condition sine-wave drifting gratings" --
  **the mean response is the reference against which the residual is defined, which is the baseline convention.**
* **5**: "Neuropil contamination was corrected by subtracting the common time series (1st PC) of a spherical
  surrounding mask" -- **a common mode across the field, subtracted.**
* **6**: "the mean NCs across a POPULATION were positive and at least five times larger than control data" and
  "only counting reliably responsive neurons used in subsequent analysis"; the population is defined by that
  selection.
* **7**: the residual is defined as "Y_i - Y_bar_i" and "The noise correlation r_sc was computed as the Pearson
  correlation of u_i and u_j" -- **subtraction precedes correlation, an explicit ordering.**
* **2 is U**: no weighting of observations is stated.

## THE RESULT CHANGES THE CONCLUSION, AND THIS IS WHY THE PACKET DEFECT MATTERED

**On the truncated packet the mouse paper appeared to declare two of seven.** **On the full text it declares
SIX.** **The protocol's falsification criterion is that a matrix declaring six or seven refutes the claim that
these dimensions are generally undeclared, and the mouse paper MEETS IT.**

**So the claim is now refuted for one of the two matrices in this small sample, and the manuscript has already
been scoped to say so: it states that these dimensions are not universally undeclared and that its claims are
about this atlas and about an observed rate rather than about necessity.**

**And the zebrafish paper's four, unchanged between the two packings, is the case that shows the middle of the
range.**

## Coder 1's least confident cells, listed rather than hidden

* **Zebrafish 1**: a coder counting the raw-trace processing as the transform codes D, giving five.
* **Zebrafish 4**: a coder treating the fluorescence conversion's own baseline as the reference codes D, giving
  five.
* **Mouse 4**: a coder requiring a named TIME window for the reference rather than a reference DISTRIBUTION codes
  U, giving five.
* **Mouse 6**: a coder treating "population" as too loose to be a pool codes U, giving five.

**Three of those four borderline cells would push a total UP rather than down, so six is if anything the
conservative coding for the mouse matrix.**

## Provenance

* **Packet:** `DIMENSION_CODING_PACKET_v2.md`, 309,157 characters, verified to contain each paper's Methods
  before any coding was done.
* **Protocol:** `../PROTOCOL_documentation_inspection.md`; **the fact that this line substituted the mouse paper
  for two of the protocol's three named matrices is recorded as a deviation in `DIMENSION_CODING_DEFECT.md`.**
* **Coder 1 is this line and is not independent.** **A new second coder is required, because the version-1
  second coder's result is void rather than superseded.**
* **No matrix was downloaded. No analysis was run.**
