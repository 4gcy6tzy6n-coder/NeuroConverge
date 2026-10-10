# Dimension coding, coder 1 (this line), frozen before the second coder's output was read

**Coder 1 is THIS LINE and is not independent.** **The second coder received the same packet without coder 1's
assignments, so it cannot be anchored by them.**

| # | dimension | zebrafish | mouse V1/HVA |
| --- | --- | --- | --- |
| 1 | signal transform / normalisation | **U** | **U** |
| 2 | per-observation weighting | **U** | **U** |
| 3 | time window / epoch | **D** | **D** |
| 4 | baseline / reference convention | **U** | **U** |
| 5 | global / common mode | **D** | **D** |
| 6 | node or parcel pool | **D** | **U** |
| 7 | ORDER of operations | **D** | **U** |
| | **total D** | **4** | **2** |

## The sentences coder 1 relied on

**Zebrafish**
* **3**: "averaged the activity of neurons within each region of the brain during the 10-min spontaneous period"
* **5**: "regressing out a global signal from regional time series"
* **6**: "averaged the activity of neurons within each region" -- the region is the pool
* **7**: "regressing out a global signal from regional time series BEFORE computing FC"

**Mouse V1/HVA**
* **3**: "Noise correlation was defined as the trial-to-trial correlation of residual spike count (1 s time
  window, if not otherwise stated)"
* **5**: "Neuropil contamination was corrected by subtracting the common time series (1st PC) of a spherical
  surrounding mask of each neuron"

## Borderline cells, coded U and listed

* **Mouse dimension 1**: the only dF/F hits are in the peer-review response rather than in a Methods
  declaration. **A response that states what was done could count; this one discusses another group's result.**
* **Mouse dimension 6**: the only pool-like hits are the pupil and a model's components, not the neural
  population. **Genuinely U.**
* **Mouse dimension 7**: "We first evaluated the accuracy" is narrative order, not an ordering declaration for
  the computation. **Genuinely U.**
* **Zebrafish dimension 4**: the paper names a dF/F0 conversion "sequence of operations" but the baseline window
  for the correlation is not stated in the passage read. **Borderline; a fuller reading of its supplement might
  make it D.**
* **Zebrafish dimension 1**: the dF/F0 conversion IS a signal transform and IS named. **Coded U because the
  passage did not state the baseline or the exact operation sequence for the correlation; a coder applying the
  rule more loosely would code D.** **This is coder 1's least confident cell.**

## Provenance

* **Packet:** `DIMENSION_CODING_PACKET.md`, the same input both coders received.
* **Protocol:** `../PROTOCOL_documentation_inspection.md`, committed before any document was read.
* **No matrix was downloaded. No analysis was run.**
