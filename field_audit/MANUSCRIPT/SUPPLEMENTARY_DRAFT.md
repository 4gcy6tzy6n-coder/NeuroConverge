# Supplementary Information: the framework exercised on known inputs (draft skeleton, 2026-10-24)

**Role per the 2026-10-23 review decision:** the method arc and the five-project calibration are
Supplementary material - they demonstrate that the audit framework detects evidence boundaries it was not
tuned on; they are NOT an independent confirmation of any field-level proportion and carry no weight in the
main text's claims. All numbers below are measured, committed facts (MICA archive, commits `c228e9b`..
`76b42c8`); nothing here is re-measured.

## SI Note 1: five workspace projects as known inputs (calibration)

Five projects in this workspace made bio-to-AI or adaptation claims and measured their own boundaries. Coded
on the same sheet (first-coder pass, awaiting the second coder), their headline-transition grades are:
NeuroMotif T3=E0 (paradigm retired, zero historical positives); IRCN-CBCC T3=E0 (confirmatory failure on 112
sealed seeds); NeuroMech T3=E1 (paradigm retired to an evidence-boundary report); BioMemory T3=E1
(exploratory, negatives retained); MICA T3=E2-negative-at-the-bar (controlled evidence, never clearing the
frozen cell-level bar). The instrument must reproduce these known grades - if it graded any of them E3+, it
would be defective. This is the calibration contract: known inputs, known outputs, instrument validated
against them.

## SI Note 2: the adaptation-value arc (one frozen family, six chained measurements)

On a frozen four-state POMDP family (EX1-v3, horizon 6) with a resource-bounded agent, six chained
measurements bracket when adaptation is worth attempting - each with criteria frozen before its run and hard
cross-checks binding it to its neighbours:

1. **Reachability** (`A_62A_UPDATE_REACHABILITY`): parameter updates can change actions (16 cells) but carry
   0.729 of weight against 48.730 for Q-moved-but-argmax-stable; the chain breaks between Q and the action,
   not between parameters and Q (values-unchanged never occurs).
2. **Sign structure** (`A_62B_BENEFIT_SIGN_CONTROLS`): beneficial updates exist per node (22 cells, best
   +0.0812/step) and harm exists in exactly one place - updating when nothing changed (-0.0218/step).
3. **Passive estimability** (`A_SE_SIGN_ESTIMABILITY`): a frozen likelihood-ratio gate reaches 0.967
   accuracy against a 0.972 abstain baseline - recall zero where updating helps; the change statistic sits at
   0.1-1.7 in-window against a threshold of 4. Passive statistics cannot time or sign the purchase.
4. **The lived probe** (`A_PB_PROBE_UPDATE`): generating the missing observation by acting delivers +0.0205
   at exactly one cell but costs -0.016 to -0.114 per step - priced out 1.3-25x.
5. **The free readout** (`A_BC_BREAKEVEN_CHANNEL`): even a free, perfectly targeted single readout is worth
   at most +0.0192/step (negative in 30 of 48 cells) against a privileged headroom of +0.0747 - the
   conversion limit of one datum through a count refit.
6. **Budget and timing** (`A_KB_QUERY_PACKET`, `A_TR_TIMING_RULE`): an 8-16 bit query packet at the late
   window converts 87.5 percent of privileged value (the arc's only criterion met); the same purchase timed
   by the agent's own gate fires only at the last step, where it is worthless. The working regime exists and
   is not self-activatable.

**What this arc contributes to the main text:** a worked demonstration that the audit's distinction between
delegated foundations, controlled utility and asserted correspondence has teeth - when the same laboratory
turned its own instruments on its own adaptation claims, every positive result arrived with the boundary
conditions named and the failure modes measured. The arc is family-scoped ("no known blocking or major
defect remains within the reviewed scope" is the strongest honest claim) and is presented as method
demonstration, not as evidence about the field.

## SI Note 3: instrument chain (provenance)

Every stage below names its governing document and its frozen anchor; all anchors are committed in
the article's repository, and every Results number is recomputed by the listed script from these
artifacts alone.

| stage | governing document | frozen anchor |
| --- | --- | --- |
| Preregistration (taxonomy T1-T5, grades E0-E4, kill rule 80 pct) | `AUDIT_PREREGISTRATION_v1_FROZEN.md` | frozen 2026-10-19, unedited |
| Data-source amendment (arXiv; ranking consequences stated) | `AMENDMENT_20261019_ARXIV_DATA_SOURCE.md` | dated amendment |
| Pinned query snapshot | `corpus_draw_arxiv_v1.snapshot.jsonl` | sha256 `e73f72f5...3aee`, 3,246 records |
| Primary corpus freeze (18-draw -> 16 after eligibility) | `corpus_draw_arxiv_v1.csv`; `ELIGIBILITY_SECOND_REVIEW_20261024.md` | commit `874797f`; second review 2026-10-24 |
| Reportability amendment (evidence vs reporting separated) | `OWNER_AMENDMENT_REPORTABILITY_2026-10-20.md` | owner-approved 2026-10-20 |
| Coder conventions (COND-1 no aggregation, COND-2 cross-tab caveat, COND-3 chain citations = PARTIAL) | `METHODS_CONDITIONS_RECORDED_20261024.md` | recorded pre-coding 2026-10-24 |
| Scorer binding (v3; refuses incomplete grids, unregistered sources, hash mismatches) | `BINDING_RECORD_V3_20261024.md` (scorer sha256 `b7fa04ab...6455e`; checks `c094856b...9829c`; registry digest `77dcda1a...db6e`) | owner-approved "B1-B4" 2026-10-24 |
| Independent scorer review | `REPORTABILITY_V3_INDEPENDENT_REVIEW_20261023.md` | BINDING-READY with 4 conditions, all closed |
| Primary-corpus coding artifacts | `CODING_sheets_v2/` (coder sheets, correction ledger C-1/C-2/C-3, adjudication 39 rows, merge) | commit `f4c16e2` |
| Primary-corpus statistics | `CODING_sheets_v2/statistics_final_20261024.json` (+ dated erratum on the per-sheet headline inversion) | `CODING_FINAL_RESULTS_20261024.md` |
| Validation rule (drawn 2026-10-23, scope-corrected 2026-10-25) | `VALIDATION_CORPUS_RULE_20261023.md`; `VALIDATION_RESUMPTION_20261025.md` (v1 draw superseded before coding) | commits `144c41e`, `21eb404` |
| Validation corpus (N = 42) + pinning | `corpus_validation_v2_adjudicated.csv`; `pinned_validation_20261025/` manifests (42 PDF + text sha256 pairs, re-hash verified) | acceptance amendment 2026-10-25 (owner option a) |
| Validation coding + statistics | `CODING_sheets_validation/` (two 210-row coder sheets, headline maps, `statistics_validation_20261025.json`) | commit `136ec7f` |
| Recompute path (reproducibility statement) | `fill_results_numbers.py` (manuscript numbers), `compute_validation_statistics_20261025.py --selftest`, `make_figures.py`, `nmi_format_check.py --selftest` | one command each, all committed |

Chain-citation discipline: this table names documents, not facts - every number in the main text is
produced by the recompute path from the pinned artifacts, and any discrepancy between the two would
fail the format checker's frozen-number cross-checks before submission.

## SI Note 4: pilot-corpus specificity verification of delegated foundations (11/14 specific)

**Status: pilot evidence, superseded in scope by the final corpus.** Before the owner's scope
narrowing to the 16-claim final corpus, the 18-claim pilot corpus's T1 (structure-to-computation)
transitions were all delegated by citation (in-paper E0, 18/18). For the 14 of those 18 whose
cited sources could be graded, each cited source was verified against the claimed computation on a
frozen three-point scale: `S-specific` (the source establishes the very computation claimed, at the
specificity used), `S-general` (the source establishes a related general phenomenon, not the
specific computation at that specificity), `S-absent` (the source does not address the claimed
link). Frozen record: `T1_SPECIFICITY_VERIFICATION_20261023.md` (per-claim table with sources).

**Tally: 11 S-specific, 3 S-general, 0 S-absent.** The three S-general cases, named: FearNet's
tri-partition switch (the cited complementary-learning-systems line establishes the dual-memory
core, not the paper's specific BLA-switching extension); locality/modularity/sparsity as claimed
brain-architecture priorities (the cited network-neuroscience reviews establish sparse modular
brain networks; the paper's own text calls the inspiration loose and claims no specific
computation); and reward-neurotransmitter control of myelination (activity-pattern control of
myelination is established; the reward-transmitter-specific control is the stronger, unestablished
part). One S-specific case carries a noted caveat (the strongest external support for the
heterogeneity-exploitation claim is itself computational modeling, not biological experiment -
reported as its own layer, not folded into the grade).

**Why this is pilot evidence and not a final-corpus statistic.** On the final 16-claim corpus the
two coders' external-evidence conventions diverged (one recorded 15 cells at E3 with verification
routes, the other recorded none under its stricter no-verification rule) and the preregistered
weaker-grade merge resolves all of them to E0; the external layer therefore enters the main text
only through that disclosed convention divergence. The specificity tally above was measured under
the pilot protocol on the pilot corpus and is NOT re-derived as a merged statistic on the final
corpus. It is reported here because it bounds the interpretation of delegation: where the pilot
instrument could verify routes, delegated biology was usually delegated to sources that
specifically support the invoked computation (11/14) - the pilot's three-layer T1 picture (18/18
in-paper E0; 14/18 externally established; 11/14 specifically). Promoting this to a final-corpus
statistic requires a single external-verification convention frozen before coding, a named
successor version, and a fresh pass; none is claimed here. No prevalence claim is made.

## SI Note 5: robustness and positive-control calibration (2026-10-25, advisor-directed)

**Survey exclusion.** Frozen mechanical rule (title or abstract self-identifies as survey/review):
primary corpus 2 of 16 excluded (2312.07213v4, 2305.11252v1), validation corpus 6 of 42 excluded
(1506.03264v1, 1901.03690v3, 2204.07050v7, 2209.10818v2, 2312.09257v2, 2603.26722v1; the two
additional coder-flagged validation claims are primary-research papers and are not excluded). Every
finding is direction-identical without surveys, and the utility-correspondence asymmetry
strengthens: T3 controlled 10/15 (66.7 pct) vs T2 2/15 (13.3 pct) on primary; T3 25/36 (69.4 pct)
vs T2 9/36 (25.0 pct) on validation; T1 remains E0 in all kept claims of both corpora; headline
E2+ rises to 66.7 pct (primary, CI 41.7-84.8) and 72.2 pct (validation, CI 56.0-84.2), every point
estimate still below the 80 pct kill bar (honest caveat: the smaller subsets' interval upper bounds
cross 80; the kill rule is defined on the frozen corpora as drawn). Record:
`ROBUSTNESS_SURVEY_EXCLUSION_20261025.md` + JSON.

**Positive-control probe.** Question: does the instrument award its top in-paper grade when a paper
actually supplies controlled correspondence evidence? Three papers outside both corpora were
nominated under a frozen criterion (abstract explicitly claims the bio-inspired mechanism
ablated/inverted or a matched non-bio control attributed to the mechanism): differentiable
plasticity (1804.02464v3), multi-compartment spiking RL (2301.07275v2), and Global-Workspace RL
transfer (2403.04588v2). Registered prediction: at least 2 of 3 at T2 = E2. Outcome: 3/3 at
T2 = E2 (indeed E2 across T2-T5, headline T3), quotes and cited specifics verified against pinned
texts; hashes re-checked. The positive controls demonstrate that the audit instrument can recognize
controlled evidence of biological-to-artificial computational correspondence; they do not by
themselves establish the instrument's classification accuracy on boundary cases or cross-coder
stability beyond the disagreement statistics reported in the main text - the human-coder
supersession pass addresses the latter. The probe's second reading is on message: even these
strong-correspondence papers carry T1 = E0 - delegation of biological foundations is universal in
this literature, and what separates strong from weak mechanistic papers is whether the
correspondence and its attribution are controlled. The grade definitions were not touched after
coding. Record: `POSITIVE_CONTROL_PROBE_20261025.md` + probe directory with pinned texts,
manifests and coding sheet.
