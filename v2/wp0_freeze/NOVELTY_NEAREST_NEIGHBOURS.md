# NOVELTY_NEAREST_NEIGHBOURS — NeuroConverge v2, WP0 (NCV2-002)

**Status: preliminary matrix, written before any v2 experiment exists.** Its job is to stop an
ordinary biological-graph prior being presented as a discovery. Every entry records what the work
already does, what NCV2 could add, and whether the overlap is a genuine collision.

**Method note.** Abstracts were read through the Europe PMC REST API, which returns structured
records with the published abstract text. Where a source was not reachable, that is stated rather
than papered over. **Nothing here is paraphrased from a secondary summary**, and no citation is
recorded as verified unless its DOI resolved to a record this session.

---

## 1. The nearest neighbour, and why it is the one that matters

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

**This is close enough that the burden is on v2 to be specific.** It already states the direction v2
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
