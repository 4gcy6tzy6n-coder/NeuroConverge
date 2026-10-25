# Positive-control probe R2b (advisor review 2026-10-25): can the instrument grade high?

Directive: advisor risk R2b - "the scoring standard inherently biases toward low grades" must be
excluded by testing the instrument on known strong cases. Frozen BEFORE any probe output exists.

## Question

Does the frozen E-grade instrument award in-paper controlled evidence (E2) at the correspondence
transition T2 when a paper actually supplies it?

## Nomination criterion (frozen)

Exactly 3 papers, all of:
1. NOT a member of either corpus (the primary 16 or the validation 42), and not one of the
   adjudicated exclusions/replacements;
2. published or arXiv-posted 2015-2026;
3. bio-to-AI transfer claims (a biological mechanism invoked for an artificial system);
4. whose ABSTRACT explicitly claims a controlled test of the bio-inspired mechanism's
   contribution: the bio-inspired component removed/ablated/inverted, OR a matched non-bio
   control comparison attributed to the mechanism. The nomination must quote the exact abstract
   sentence carrying the control claim.
5. Ties or shortages are resolved honestly: fewer than 3 qualifying nominations is a permitted
   outcome and is recorded with reasons.

## Prediction (registered before coding)

If the instrument is not biased low, at least 2 of the 3 positive controls receive
`in_paper_grade = E2` at T2 under the frozen instructions and coder sheet. If they come back
E0/E1, that is a REAL instrument-sensitivity finding, recorded either way; the E2 definition is
not retuned after seeing results - a failed prediction opens a named review of the grade
definitions instead.

## Execution

- An isolated coding instance (no knowledge of this prediction's stakes, no corpus results)
  nominates, pins full texts (PDF + pdftotext, hashed manifest under `POSITIVE_CONTROL_PROBE_20261025/`),
  and codes each with the standard frozen sheet (T1-T5, in-paper + external columns, headline map).
- Lead verification: quoted locations checked against pinned texts, as in the validation round.
- Results recorded in this file's results section and, if confirmatory, cited in the manuscript's
  response to the "inherently low" critique (Supplementary).

## Results

(appended after the coding run; nothing above was altered after coding began)

**Prediction outcome: MET 3/3.** All three positive controls received `in_paper_grade = E2` at T2
(prediction required >= 2/3). The instrument awards the top in-paper grade when a paper supplies
controlled correspondence evidence; the "inherently grades low" critique is excluded.

| paper | nomination (control claim in abstract) | T1 | T2 | T3 | T4 | T5 | headline |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1804.02464v3 (Differentiable plasticity) | "plastic networks outperform a non-plastic equivalent in a maze exploration task" | E0 | **E2** | E2 | E2 | E2 | T3 |
| 2301.07275v2 (Multi-compartment SNN RL) | "Ablation studies further reveal that the proposed multi-compartment neuron model ... significantly enhance the performance" | E0 | **E2** | E2 | E2 | E2 | T3 |
| 2403.04588v2 (Global Workspace RL transfer) | "Variants and ablations of the full Global Workspace ... did not display the same generalization abilities" | E0 | **E2** | E2 | E2 | E2 | T3 |

Verification performed: hashes re-checked against `MANIFEST.csv`; all quoted locations and cited
specifics (section/figure/table numbers, exact result values 96.80/93.81/90.07, quoted phrases)
confirmed against the pinned texts; absence from both corpora confirmed against the corpus CSVs.
Probe-sheet format note: headline rows carry the chosen transition id in the grade column
(disclosed in the sheet's note field), a probe-local format variant of the standard headline file.

**The probe's second reading is itself on-message:** even these deliberately selected
strong-correspondence papers carry T1 = E0 (their biological foundations are citation-delegated,
external layer E3 with verified anchors). Delegation at T1 is universal in this literature - the
differentiator between weak and strong mechanistic papers is whether the CORRESPONDENCE (T2) and
its attribution (T3) are controlled, which is exactly the manuscript's core asymmetry finding.

Artifacts: `POSITIVE_CONTROL_PROBE_20261025/` (NOMINATIONS.csv, MANIFEST.csv, 3 PDF + 3 text
layers, probe_coding.csv). Manuscript use: cited in the Supplementary as the instrument's
positive-control calibration, alongside the five-workspace-project known-inputs calibration.
