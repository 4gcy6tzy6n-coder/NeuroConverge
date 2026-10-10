# Protocol addendum: documentation inspection of three further published functional matrices

**R2-M1's third resolution route: "show that the same undeclared dimensions are absent from the documentation of
two or three further published matrices, even by document inspection rather than re-analysis".**

**Written BEFORE the documents are read, so the criterion cannot be chosen after seeing them.**

## The matrices, chosen for inspectable documentation rather than convenience

| # | matrix | why chosen | documentation to inspect |
| --- | --- | --- | --- |
| 1 | **Human Connectome Project** resting-state functional connectivity | the most heavily documented functional-connectivity pipeline in existence; if any pipeline declares its specification, this one should | the HCP pipelines repository and reference manual |
| 2 | **UK Biobank** brain imaging functional connectivity | the largest population imaging resource, with a published processing pipeline | the UKB brain imaging documentation |
| 3 | **Larval zebrafish whole-brain functional networks** (the citing work 40644546) | the nearest same-kind case: a whole-brain optical functional matrix in a small organism, as the audited atlas is | its own data/code availability statement |

## The dimensions to look for, generalised from the atlas's seven

**The atlas's seven are specific to its assay. The generalisable set a reader needs in order to re-derive a
published functional matrix is:**

1. **the signal transform or normalisation applied before correlation** (the analogue of per-cell normalisation)
2. **the per-observation or per-event weighting** (the analogue of per-event precision weighting)
3. **the time window or epoch** over which the functional quantity is computed
4. **the baseline or reference convention**
5. **the treatment of a global or common mode** across the matrix
6. **the cell, node or parcel pool** over which any global quantity is computed
7. **the ORDER in which those operations are applied**

## The coding

**For each matrix, each of the seven receives D (declared in the documentation reachable from the artifact's own
availability statement) or U (not declared).** **A dimension counts as D only if the documentation states the
choice specifically enough that a reader could reproduce it without reading the authors' code.** **A sentence
naming the software does NOT count; the software's defaults are not the paper's specification.**

**Falsification criterion, fixed now: if any of the three declares six or seven of the seven, the claim that
these dimensions are generally undeclared is REFUTED for that matrix and must be reported as such.**

## Provenance

* **No re-analysis is performed. No matrix is downloaded. This is document inspection only.**
* **The documents reached and the exact sentence for each D are recorded.**
