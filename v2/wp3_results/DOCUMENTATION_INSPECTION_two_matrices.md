# Documentation inspection: a second matrix, and a second instance the abstract-level census missed

**This is the second of the two or three matrices R2-M1's third route asks for.** **The protocol was committed
before any document was read, in `../PROTOCOL_documentation_inspection.md`.**

## The matrix inspected

**Mouse V1 and higher visual areas, from the eLife paper *Visual information is broadcast among cortical areas
in discrete channels* (PMC13012721).** **Chosen because it is the record the census FLAGGED as the one most
likely to be coded R by another coder: its abstract says its noise correlations are "robust, reproducible
statistical measures and are remarkably similar across stimuli", with no figure attached.** **It is a different
species, preparation and modality from the zebrafish case, and its availability statement says data and code
are on GitHub.**

## Finding A: the census missed a SECOND instance, and this one is more explicit

**The paper's body reports reliability for its functional quantity in several places, none of them in the
abstract:**

* **"We find that NCs are a reliable measure at the population level."**
* **"The NC of individual neuron pairs can be computed using different random subsets of trials, yet reliably
  converges on similar values ... the variance of NC computed using a subset of trials is explained by the
  variance in the held-out subset of trials (53 +/- 24 % variance explained; total 204 populations)."** **That
  is a split-half reliability figure with a value and an interval.**
* **"trial-to-trial Pearson correlation of the inferred spike train at 500 ms bin"**, used as a reliability
  measure for spike inference.**
* **"We provided a detailed analysis of the rigor of measuring NCs with calcium imaging and assessed their
  reliability given the imprecision of calcium imaging for inferring spiking activity."**

**The census coded this record N.** **It did so correctly under its rule, because the rule's unit is the
abstract and none of these sentences is in it.** **This is the second known instance in which the abstract-level
unit failed to see a reliability figure, after the zebrafish matrix, and the second is a stronger instance
because the reliability analysis is a stated aim rather than a by-product.**

## Finding B: the dimension coding, and its reliability

| # | dimension | coded | the passage |
| --- | --- | --- | --- |
| 1 | signal transform / normalisation | **U** | the only dF/F hits are in the peer-review response, not in the Methods declaration |
| 2 | per-observation weighting | **U** | the only weighting hits describe the model's Gaussian inputs, not the observations |
| 3 | time window / epoch | **D** | "Noise correlation was defined as the trial-to-trial correlation of residual spike count (1 s time window, if not otherwise stated)" |
| 4 | baseline / reference convention | **U** | "stable baseline" is a recording-selection criterion, not the baseline convention for the correlation |
| 5 | global / common mode | **D** | "Neuropil contamination was corrected by subtracting the common time series (1st PC) of a spherical surrounding mask" |
| 6 | node or parcel pool | **U** | the only pool-like hits are the pupil and the model, not the neural population |
| 7 | ORDER of operations | **U** | "We first evaluated the accuracy" is narrative order, not an ordering declaration for the computation |

**So this matrix declares TWO of the seven, against the zebrafish's FOUR and the audited atlas's ONE.**

**AND THE CODING ITSELF IS THE WEAKEST PART OF THIS INSPECTION, WHICH IS STATED RATHER THAN GLOSSED.** **A
keyword screen produced seven apparent declarations and six of them were false positives: a peer-review
response, a model's parameters, a recording-selection criterion, the pupil, and a narrative transition.** **The
table above was produced by reading the passages, but it was produced by ONE coder, this line, with no second
coder and no preregistered passage-selection rule finer than the protocol's.** **The dimension counts across the
two matrices should therefore be treated as illustrative and not as measurements.**

## What the two inspections together establish

* **These dimensions are NOT universally undeclared, and there are now two counterexamples in the citing frame,
  declaring four and two of the seven.** **The audited atlas declares one.**
* **The variance across the three is large and the sample is two, so no rate should be quoted from it.**
* **The census's abstract-level unit undercounts, and it has now been caught failing twice against known
  instances.** **The direction is known: the census is a LOWER BOUND.**
* **And a same-kind matrix CAN declare its reliability: the eLife paper analyses the rigor of its own functional
  measurement as a stated aim.** **That is evidence for the manuscript's remedy, not against it: the practice
  is achievable, which is what makes its absence elsewhere informative.**

## What is still not done, named rather than implied

* **The protocol named three matrices; two have been inspected.** **The Human Connectome Project and UK Biobank
  were not coded.**
* **The 129-record frame has not been re-coded at full text, which the two missed instances now show would
  change the rate.** **It is the natural next step and it is a larger study than this round.**
* **The dimension coding needs a second coder before its counts can be reported as anything but illustrative.**

## Provenance

* **Protocol:** `../PROTOCOL_documentation_inspection.md`, committed before reading.
* **Sources:** Europe PMC full text, PMC12248300 and PMC13012721.
* **No matrix was downloaded and no analysis was run. No model was fitted.**
