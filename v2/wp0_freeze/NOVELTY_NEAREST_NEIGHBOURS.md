# NOVELTY_NEAREST_NEIGHBOURS — NeuroConverge v2, WP0 (NCV2-002)

**Status: preliminary matrix, written before any v2 experiment exists.** Its job is to stop an
ordinary biological-graph prior being presented as a discovery. Every entry records what the work
already does, what NCV2 could add, and whether the overlap is a genuine collision.

**Method note.** Abstracts were read through the Europe PMC REST API, which returns structured
records with the published abstract text. Where a source was not reachable, that is stated rather
than papered over. **Nothing here is paraphrased from a secondary summary**, and no citation is
recorded as verified unless its DOI resolved to a record this session.

---

## 0. PRIMARY NEAREST NEIGHBOUR — this displaces everything below it

**Creamer MS, Leifer AM, Pillow JW. _Bridging the gap between the connectome and whole-brain activity
in C. elegans._ bioRxiv `10.1101/2024.09.22.614271`, v1 2024-09-23 through **v4 2026-05-18**. Code:
`github.com/Nondairy-Creamer/Creamer_LDS_2026`.**

**Read this session:** all four version records from the bioRxiv API, the v4 abstract verbatim, and the
repository README. This is the *same work* that the joint lead initially listed as two separate
nearest neighbours ("Bridging the gap..." and "Creamer, Leifer & Pillow 2026 preprint revision"); the
2026 item is **v4 of this preprint**, not a second paper.

> "Here, we address this problem using a **connectome-constrained dynamical model of the brain, which
> we fit to whole-brain recordings of neural activity during optogenetic perturbation of single
> neurons**. This dynamical model, **which contains non-zero weights only between anatomically connected
> neurons**, captured causal interactions between all pairs of neurons 82% as well as the
> reproducibility of the perturbation data themselves. ... **Strikingly, alternative models fit using a
> shuffled connectome achieved much lower performance.** Finally, we found that **adding connections
> beyond those in the connectome did not improve** the models ability to capture causal interactions."

**From the repository README:**

* `dynamics_weights`: "W", weight between every neuron in the brain;
* **`mask`: "binary mask which determines which values to learn. this is how we specify the connectome
  constraint"** -- the connectome constraint is a mask over a full weight matrix;
* `dynamics_input_weights`: "H", the effect of optogenetic stimulation on the targeted neuron;
* `quick_start_examples/` demonstrates loading the paper's models and predicting **STAMs, correlations,
  and reconstructing missing neurons**.

### What is therefore ALREADY PUBLISHED and cannot be v2's novelty

| candidate contribution | status | basis |
| --- | --- | --- |
| a connectome-constrained model fit to real whole-brain recordings | **DONE** | v4 abstract |
| **real connectome beating a shuffled connectome** | **DONE** | v4 abstract, "much lower performance" |
| predicting **held-out / missing neurons** from a subset | **DONE** | repository README, `reconstruct missing neurons` |
| adding non-connectome edges does not help | **DONE** | v4 abstract |
| the masked-weight implementation of a connectome constraint | **DONE** | README, `mask` |

$$
\boxed{\text{H1's basic experiment -- real graph versus shuffled graph -- is NOT available as v2's novelty core}}
$$

### What remains, and it must be framed as an ORTHOGONAL axis, not as a better version

The joint lead's acceptance question for the next round is the right one:

> *after fixing the model, the input information and the topology statistics, does a correct
> cross-individual neuron identity correspondence still provide an increment that existing
> connectome-constrained prediction work has not explained?*

**The defensible distinction is that the two designs manipulate different variables.**

| | Creamer et al. | v2 (proposed) |
| --- | --- | --- |
| treatment | the **graph**: real connectome versus shuffled connectome | the **mapping**: correct cross-individual identity versus a lawful mismatch |
| held fixed | the neuron identity assignment, which is **assumed** | **the topology**, which is held fixed by construction (M1/M2 leave the adjacency matrix unchanged) |
| what the design can detect | whether the graph's topology carries information | whether **the correspondence between the graph's nodes and the recorded cells** carries information |
| the interaction | not reported | **structure x mapping**: does the graph's value depend on the mapping being right? |

**Why the manipulation is meaningful only at fixed real topology, which v2 already specifies.** If the
graph is shuffled, a "correct" node-to-cell identity no longer refers to anything real: shuffling the
graph destroys the correspondence the mapping is about. **So the mapping factor is orthogonal to the
shuffled-graph factor by necessity, not by preference.** M1 (class-preserving permutation) and M2
(cross-animal rotation) both leave the adjacency matrix unchanged, which is exactly what makes them a
mapping manipulation rather than a second graph manipulation.

**What this is NOT.** It is not a claim that Creamer's result is wrong, incomplete, or superseded. It
is not a claim that a cross-individual test would be more informative than a within-animal one -- v2's
design is **weaker** on that axis, because the graph and the recording come from different animals. It
is not a claim that the identity question is unexplored in principle; Creamer's mask construction
**has** an identity assumption, and v2's contribution is to make that assumption a **tested factor**
rather than an unexamined premise.

### THE RISK MATERIALISED. Read the decision record.

**Status as of 2026-10-09, after the joint lead supplied the full v4 PDF and it was read in full: the
overlap is TOTAL, not partial.**

Creamer et al. **already perform the identity permutation at fixed topology** -- their Methods state
that the shuffled connectome is *"topologically identical to the original network; we have only permuted
the identity of each node in the graph"* -- they **already use the same connectome files**
(`witvliet_2020_7.csv`, `witvliet_2020_8.csv`, `white_1986_jsh.csv`, `white_1986_n2u.csv`, all from
nemanode.org), and they **already work across 110 animals with 55/55 train-test splits**, reporting that
the learned properties are *"conserved across animals"*.

**Therefore v2's proposed novelty -- hold topology fixed and vary the mapping -- is already published,
on the same inputs, with five times the animals.** The one residual (they do not cross graph-shuffle
with identity-shuffle as a 2 x 2 design) is a methodological refinement, not a new scientific question.

> **Verdict: `PIVOT_OR_STOP` on the H2-centred novelty claim.** Full analysis, quoted passages, the
> coverage table and three lawful options are in
> [`DECISION_RECORD_NOVELTY_REASSESSMENT.md`](DECISION_RECORD_NOVELTY_REASSESSMENT.md).

**What this matrix does NOT retract:** the feasibility finding. An audited, reproducible route to
identity-resolved functional data now exists, backed by files actually downloaded and read. **The
question changed status from "unanswered" to "already answered elsewhere", and those are different
findings.**

**Citation status: all four version records read, v4 abstract read verbatim, repository README read.
Full text NOT read; the data split, the identity handling and the shuffled-graph construction were
NOT inspected and remain owed.**

---

## 1. The second-nearest neighbour, and why it still matters

**Beiran M, Litwin-Kumar A (2025). _Prediction of neural activity in connectome-constrained recurrent
networks._ Nature Neuroscience 28(12):2561-2574. doi `10.1038/s41593-025-02080-4`.** Abstract read
verbatim from Europe PMC (MED 41145885, PMC12648571).

> "we developed a theory of connectome-constrained neural networks in which a 'student' network is
> trained to reproduce the activity of a ground truth 'teacher' ... the two networks have the same
> synaptic weights but different biophysical parameters, reflecting uncertainty in neuronal and
> synaptic properties. **We found that a connectome often does not substantially constrain the
> dynamics of recurrent networks, illustrating the difficulty of inferring function from connectivity
> alone. However, recordings from a small subset of neurons can remove this degeneracy** ... It can
> also prioritize which neurons to record to most effectively inform such predictions."

**With Creamer et al. now primary (section 0), this is the second-nearest neighbour.** It already states the direction v2
might otherwise claim as new: that connectivity alone often does not constrain dynamics, and that a
subset of recordings resolves the degeneracy.

**Three differences that are structural rather than decorative:**

| axis | Beiran & Litwin-Kumar 2025 | what v2 proposes |
| --- | --- | --- |
| ground truth | a **model teacher**; student and teacher share **the same synaptic weights** | **real recordings from a different animal** than the one supplying the graph |
| what is varied | biophysical parameters under a fixed, correct weight matrix | **the topology** (real vs matched rewire) and **the node mapping** (correct vs lawful mismatch) |
| the identity question | the mapping is given; the question is which neurons to record | **the correspondence itself is the treatment**: does a correct, source-confirmable mapping beat a mismatch at fixed topology and fixed capacity |
| estimand | a theory of solution spaces | a **paired, animal-level held-out predictive contrast** with a frozen null |

**Citation status: DOI resolved, abstract read.** Full text not read.

**Overlap risk if v2 does not do the above: HIGH.** A study that merely obtains a real connectome and
a real recording and reports whether a graph-constrained model predicts activity would be a
dataset-level variation on this paper, and the plan forbids presenting that as new.

## 2. The other neighbours

| # | work | what it already does | what v2 could add | collision risk |
| --- | --- | --- | --- | --- |
| 2 | **Suárez LE, et al. (2024). _Connectome-based reservoir computing with the conn2res toolbox._ Nature Communications. doi `10.1038/s41467-024-44900-4`** (abstract read) | an **open-source Python toolbox** for implementing biological networks as artificial networks; reservoir computing as the paradigm | conn2res is an **instrument, not a controlled test**: it does not freeze a degree/module-matched null, and it has no identity-mismatch factor | **LOW as an answer, HIGH as a dependency.** v2 should use it or something equivalent rather than re-implement a reservoir. Re-implementing conn2res would be the "already in this codebase" failure of the ponytail ladder at project scale |
| 3 | **Connectome weight optimisation for C. elegans locomotion (2026). Scientific Reports. doi `10.1038/s41598-026-54384-5`** (abstract read) | *"the model using anatomical connectome weights directly did not achieve that"*; they **jointly optimise synaptic weights** away from anatomy, and release **10 optimised weight sets** | v2 asks the opposite and prior question: **does the un-optimised anatomical graph carry predictive value against a matched null?** This work is a **prior against H1** and must be cited as such, not as a distant neighbour | **LOW as a collision, HIGH as an expectation.** It raises the prior that H1 is null. That is not a reason to avoid the test, but it is a reason not to be surprised |
| 4 | **Witvliet D, et al. (2021). _Connectomes across development reveal principles of brain maturation._ Nature. doi `10.1038/s41586-021-03778-8`** (source page read at nemanode.org) | **eight developmental reconstructions** (L1 x4, L2, L3, adult x2) plus White 1986 compilations; chemical synapses annotated by three annotators with >=2 agreement retained; explicit direction and stability classes | v2 uses these as the **structural prior**, and as a **developmental sensitivity source** | **NONE as a result.** This is a resource, not a competitor. **v2 must never present the existence of these graphs as its contribution** |
| 5 | **Atanas AA, et al. (2023). _Brain-wide representations of behavior spanning multiple timescales and states in C. elegans._ Cell. doi `10.1016/j.cell.2023.07.035`** | the 68-dataset functional collection behind WormWideWeb; NeuroPAL coverage partial (40 of 68); encoding data for all | v2 uses the functional side; the DANDI mirror (`000776`, 38 NWB files, CC-BY-4.0) is the accessible route | **NONE.** Resource, not competitor |
| 6 | **WormID / Sprague DY, et al. (2025). _Unifying community whole-brain imaging datasets enables robust neuron identification..._ Cell Reports Methods. doi `10.1016/j.crmeth.2024.100964`** (abstract read) | harmonises **118 whole-brain datasets from five labs**; trains **CPD, StatAtlas and CRF_ID** to identify neurons across labs, "recovering all human-labeled neurons in some cases" | v2 **depends on** this: the identity mapping that unblocked WP1 comes from the same NWB convention. v2's contribution cannot be "we identify neurons" | **LOW as a collision, and v2 must not claim identification as novel.** The cell-identification problem is solved well enough here; v2's question starts after identity is known |
| 7 | **Fagerholm ED, Brazdil M (2026). _Structure-Dynamics Interdependence: An Information-Theoretic Framework for Neural State Prediction._ Zenodo. doi `10.5281/zenodo.22395352`, CC-BY-4.0, 2026-09-05** | an **information-theoretic framework** relating structure to dynamics for neural state prediction | unknown in detail | **UNRESOLVED — FULL TEXT NOT READ.** The record metadata was retrieved (title, authors, date, licence, one 196 KB PDF) but **every PDF request returned HTTP 403 "unusual traffic from your network"** from Zenodo. **This is recorded as `NOT VERIFIED`, not as "no overlap".** It must be read before any v2 manuscript step |
| 8 | **Linderman S, et al. _Inferring brain-wide interactions using data-constrained recurrent neural network models._ Neuron (2026), S0896-6273(26)00571-4** | **data-constrained RNNs** for inferring brain-wide interactions | v2 constrains by **anatomically measured** structure rather than fitting latent interactions | **MEDIUM — abstract not obtained.** Surfaced by search only; appearance in a result list is not evidence about its content. Recorded as `NOT VERIFIED` |
| 9 | classical **topological ablation** and **evaluation-framework** work cited in the v1 claim ledger (rows C01, and the taxonomy precedents at refs 15-17 of the v1 draft) | topology ablations; evaluation taxonomies; baseline/reporting-bias analyses | v2's contribution is not a new taxonomy; the v1 manuscript already states that the categories are not new | **NONE.** v2 inherits this and must not re-claim it |

## 3. The novelty claim v2 may and may not make

**Permitted**, and only in this form:

> In the specific condition where the connectome and the functional recording come from **different
> animals**, and where the node correspondence between them is itself an experimental factor with a
> **frozen, lawful mismatch construction** and a **frozen matched-topology null**, does the anatomical
> graph carry held-out animal-level predictive value, and does that value depend on the correctness of
> the correspondence?

**Not permitted:**

* presenting a real biological graph prior as the contribution;
* presenting the observation that connectomes under-constrain dynamics as new (Beiran 2025 already
  reports it);
* presenting neuron identification as new (WormID trains three algorithms for it);
* presenting the existence of the Witvliet graphs or the WormWideWeb recordings as a result;
* describing a graph-constrained model that predicts activity, with no matched null and no identity
  factor, as a discovery.

**The honest statement of the increment is narrow and must survive WP2:** *the identity correspondence
is treated as a treatment rather than as an assumption, and the topology contrast is frozen against a
matched null before any outcome is seen.* If WP2 cannot implement the mismatch control lawfully, the
increment collapses to a dataset-level variation on Beiran 2025 and **the sprint verdict should be
PIVOT or STOP, not GO.**

## 4. Verification status of every citation above

| citation | DOI resolved | abstract read | full text read |
| --- | --- | --- | --- |
| Beiran & Litwin-Kumar 2025, Nat Neurosci 28:2561-2574 | yes | **yes** | no |
| Suárez et al. 2024, Nat Commun, conn2res | yes | **yes** | no |
| Sci Rep 2026 connectome weight optimisation | yes | **yes** | no |
| Witvliet et al. 2021, Nature | yes | no (source page read) | no |
| Atanas et al. 2023, Cell | yes | no (dataset page read) | no |
| Sprague et al. 2025, Cell Rep Methods, WormID | yes | **yes** | no |
| Fagerholm & Brazdil 2026, Zenodo | **metadata only** | **NO** | **NO** |
| Linderman et al. 2026, Neuron | not resolved | **NO** | **NO** |

**Two entries are marked `NOT VERIFIED` and must be closed before any claim about novelty is
finalised.** Under the project's own rule, a claim that cannot be verified is recorded as not
verified and not cited as support.

## 5. The v1 cross-reference, now READ and closed

**Status: CLOSED 2026-10-09.** `evidence/NEAREST_NEIGHBOUR_COMPARISON.md` (4,872 B, dated 2026-10-04)
has now been read. Its rows and their bearing on NCV2-RQ:

| v1 row | primary source | bears on NCV2-RQ? |
| --- | --- | --- |
| Connectome-based computation | Suárez et al. 2024; **Beiran & Litwin-Kumar 2025** | **YES, partially** -- the same Beiran citation this matrix treats in section 1. No conflict; the v1 row states that structure-constrained models "already exist", which is consistent and is now superseded by section 0 (Creamer) |
| Biological concept transfer | Hofmann et al. 2025 | no -- about concept-transfer interventions in artificial models |
| Brain-model alignment | Muzellec & Kar 2026 | no -- about prediction direction and alignment claims |
| Mechanism-specific model contrast | Sun et al. 2026 | no -- fast-slow pathways, DMP |
| Operational evaluation taxonomy | Hupkes et al. 2023 | no -- the v1 evidence-decomposition taxonomy |
| Baseline fairness and reporting | McGreivy & Hakim 2024 | **indirectly** -- motivates the comparator-fairness checklist in TASK_SPEC_DRAFT section 2.4 |
| Negative transfer | Wang et al. CVPR 2019 | no -- source/target training transfer |

**Conclusion: no row of the v1 comparison covers NCV2-RQ's specific design** (cross-individual
structure-to-function with a fixed-topology identity-mismatch factor). The v1 document bounds the
**v1 manuscript's** claim about evidence decomposition; it does not bound, and does not anticipate,
the v2 estimand. **The one shared citation is Beiran & Litwin-Kumar 2025, and this matrix already
treats it more strictly than the v1 row does.**

**What the v1 document explicitly disclaims, and v2 inherits:** it states it is "not an exhaustive
novelty review", that "priority and sufficient NMI importance remain unestablished", and that "a
stronger claim of superior audit decisions, predictive transfer conditions or general mechanism
advantage would require its own independent evaluation". **NCV2-002 is that independent evaluation for
the v2 question, and it reaches a harsher conclusion than the v1 document does.**

---

## 6. Historical note: the cross-reference as it stood before being closed

**Status when section 0 was written: OPEN.** The v1 workstream's working tree contains an untracked
`evidence/NEAREST_NEIGHBOUR_COMPARISON.md`. **Action recorded, not taken:** before this matrix is
treated as final, read it and either absorb its rows or state explicitly why they do not bear on
NCV2-RQ.

At the time of writing, the **v1 workstream's working tree** contains an untracked file
`evidence/NEAREST_NEIGHBOUR_COMPARISON.md`, together with `evidence/M0_PROVENANCE_AUDIT.md` and
`manuscript/TECHNICAL_CLOSURE_PLAN.md`. These are another lane's in-flight artifacts and were
**deliberately not read, not modified and not committed here**.

**Why it matters for NCV2-002.** A nearest-neighbour comparison already exists in the v1 tree. It
covers a different question -- the v1 manuscript's positioning against connectome-based computation,
biological concept transfer, brain-model alignment and negative transfer -- but the overlap is
non-empty, and **v2 must not present as new anything that comparison already establishes.**

**Action recorded, not taken:** before this matrix is treated as final, read
`evidence/NEAREST_NEIGHBOUR_COMPARISON.md` and either absorb its rows or state explicitly why they do
not bear on NCV2-RQ. Until then, section 3's permitted novelty statement is **provisional**.

**Note on the defect check.** The pre-commit check for "v1 untouched" initially failed. It was wrong:
it tested whether any path under `manuscript/`, `evidence/`, `workstreams/` or [`../../PROJECT_FREEZE.md`](../../PROJECT_FREEZE.md) was
dirty, which flags the other lane's in-flight edits. The correct test is whether the **last commit
touching that path** is one of this lane's, and by that test every dirty v1 path belongs to another
workstream. The check was corrected rather than the finding suppressed.
