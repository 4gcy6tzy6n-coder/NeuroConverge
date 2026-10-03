# NeuroConverge

**Integrating Connectome Structure, Neural Computation, and Artificial Intelligence**

Working paper title: **Evidence boundaries in transferring biological computation to artificial systems**

NeuroConverge is a publication-level synthesis of two source projects. NeuroMotif contributes bounded structure-to-dynamics evidence; NeuroMech contributes source-grounded mechanism and artificial-transfer studies. The purpose is to test what the combined record supports, while keeping distinct studies and their evidence classes separate. This repository does not merge source Git histories or replace either source of record.

For a concise map of the full project and its two workstreams, see [PROJECT_UNDERSTANDING.md](PROJECT_UNDERSTANDING.md).

## Central question

When does biologically grounded neural computation survive translation into a useful artificial inductive bias?

The current evidence does not establish that connectome structure is universally insufficient, nor that biological computation generally improves AI. It supports a narrower retrospective synthesis: in the tested NeuroMotif assays, the proposed structural advantage was not established; in NeuroMech, biological source evidence and artificial results are separable, and transfer effects depend on the tested task, information available to the model, and comparator. This project-level framing remains a hypothesis-generating synthesis, not a validated universal law.

## Workstreams

- **NeuroMotif — structure and dynamics:** [source manifest](workstreams/neuromotif_manifest/README.md)
- **NeuroMech — biological computation and artificial transfer:** [source manifest](workstreams/neuromech_manifest/README.md)

The user-authorized prospective V1 tests are complete and the experiment program is closed. This includes the M2/M5 tests, the three-family DMP correspondence package, and a later PC→SST synthetic figure–ground transfer test. The PC→SST test is a new mechanism/task pairing, but it was selected after prior project outcomes and remains in the visual domain; it is not an independent, project-level blind validation. Its pre-run contract, complete synthetic outputs, verifier, and post-run interpretation amendment are in `new_experiments/PROSPECTIVE_V1/`. The primary mechanism-specificity gate failed. The source artifacts are still not frozen. NeuroMech has two divergent evidence views: public `experiment-publication` and the broader local Route-D portfolio. See [PROJECT_FREEZE.md](PROJECT_FREEZE.md) and [the publication-branch crosswalk](evidence/PUBLICATION_BRANCH_CROSSWALK.csv); rows without exact Route-D matches remain candidates, not adjudicated manuscript evidence.

## Package map

- `manuscript/` — integrated manuscript candidate (Markdown and Word), references and supplementary manuscript source.
- `figures/` — six generated main figures with CSV source data, vector/review exports, geometry audits and SHA-256 manifest.
- `evidence/` — claim–evidence matrix, experiment selection and claim ceiling.
- `workstreams/` — source repository identity, commit and canonical artifact links.
- `supplementary/` — selected extended results, negative results, robustness and provenance.
- `new_experiments/` — frozen M2/M5 and DMP synthetic V1 protocols, plus the later PC→SST transfer test, outputs, hashes, and verification records.
- `reproducibility/` — code/data manifests, environment notes and audit status.

## Current status

The internal manuscript candidate now follows an unheaded Introduction, Results, Discussion and detailed Methods, with numbered references, figure legends, availability/declaration statements and an exported Word file. Six source-linked figures have been generated and visually inspected. All current synthetic experiment packages are closed. In the later PC→SST test, the generic context model passed the viability gate, but selective pooling did not beat global pooling and the frozen mechanism-specificity contrast had the opposite sign from the intended biological prediction; this does not support a positive mechanism-specific transfer claim. The run was synthetic and did not use the paper's neural recordings. The package documents a contract wording/sign mismatch without changing or rerunning the frozen analysis. This test is new relative to the named prior task families, but was selected after earlier project outcomes and overlaps their visual domain, so it does not resolve the project-level prospective-validation gap. This is not a submission-ready package: source artifact freeze, exact historical inclusion crosswalk, redistribution rights, author-supplied information, final attribution and NMI contribution/novelty assessment remain open. The current venue audit does not admit the project as NMI-ready.
