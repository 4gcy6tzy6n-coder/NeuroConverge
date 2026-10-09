# HYPOTHESES — NeuroConverge v2, WP0 (NCV2-002)

**Status: prospective. Frozen before any v2 outcome exists.** No v2 experiment has been run, no v2
model has been fitted, and no v2 endpoint value has been computed. Nothing in this document is a
result.

**Label rule.** v2 work is **prospective**. All v1 material referenced below is **retrospective and
outcome-informed**, and is used only as prior experience or as a comparator lesson, never as v2
evidence.

---

## 1. The main question, carried verbatim

**NCV2-RQ.** *Under real-data conditions in which biological structure and functional signal are NOT
the same observed object, can connectome-derived topological constraint produce reproducible
independent predictive value relative to alternative topologies matched for information content,
training resources and structural complexity; and if so, does that value depend on valid neuron
identity correspondence and on task context?*

**This is a falsifiable empirical question that does not assume the biological graph wins.** A null
outcome is a permitted and publishable outcome of the sprint; the plan's completion standard requires a
complete data-method-counterfactual-inference-unit-limitation-replication package even when the result
is zero or uncertain.

## 2. The hypothesised statements

### H1 — real structure increment

**Statement.** In held-out prediction of a functional target in an animal that contributed no
structural information, an audited biological topology as a constraint yields additional conditional
predictive value over structure-matched control topologies.

**Falsified by.** No improvement over the strongest matched control under the frozen endpoint and
inference rule. **The permitted wording on failure is exactly: _under the current task and model, no
independent topological increment was detected._ Not "biological structure is useless."**

**Why it is not assumed true.** The nearest neighbour already reports that a connectome often does not
substantially constrain the dynamics of a recurrent network (Beiran & Litwin-Kumar 2025, abstract read
verbatim), and a 2026 C. elegans locomotion study reports that using anatomical connectome weights
**directly** did not produce the behaviour and required jointly optimising weights away from anatomy
(`10.1038/s41598-026-54384-5`, abstract read verbatim). **The realistic prior is that H1 may be null.**

### H2 — role of identity correspondence

**Statement.** Holding topology and model complexity fixed, a correct, source-confirmable node
identity mapping yields a task-relevant increment over a lawful mismatched mapping.

**Why this is the load-bearing hypothesis.** It is the axis on which the sprint's novelty rests
(see `NOVELTY_NEAREST_NEIGHBOURS.md` section 3). Within-one-file identity is now known to be
available: the DANDI `000541` NWB carries `rois -> id -> ID_labels` for 177 segments with 177
distinct named identities, verified by decoding. **So a correct mapping can be constructed and a
mismatch can be constructed lawfully, which is what makes H2 testable rather than rhetorical.**

**Falsified by.** A mismatch performing as well as the correct mapping. **Required handling of
uncertainty:** if identity uncertainty exists in the source, a noise and uncertainty sensitivity
analysis is required, and **a mapping error must not be reported as evidence that the biological
mechanism is invalid.**

### H3 — identifiability evidence upgrade

**Statement.** A pre-frozen source-mapping-comparator adjudication procedure can distinguish
supportable from unsupportable scientific claims in **cases not used in its development**, and the
distinction is re-checkable by an independent auditor from raw outputs.

**Explicit limitation, from the plan.** H3 does **not** assert superiority over existing review
checklists and must be compared against established comparator-design norms. **If it works only on
cases this project already knows, it is operational tidying and not a general new theory.**

## 3. Boundary conditions that travel with every statement

1. **H1 and H2 are predictive effects under observational data and models. They are not direct
   biological causal interventions.**
2. **Cross-individual connectome-to-function alignment supports at most a cell-class / atlas-level
   structural prior.** It must **never** be called same-animal, synapse-level functional causal
   evidence. The mapping class for the WP1 resources is `CELL_CLASS_ALIGNED_ACROSS_SPECIMENS`.
3. **A null is not a universal law.** No outcome licenses "biological structure is generally
   useless" or "biological mechanisms generally improve AI".
4. **The evidence hierarchy used here is a retrospective organising scaffold, not a validated
   instrument.**
5. **Software correctness is not scientific evidence.** A green test suite satisfies no
   preregistration, comparator or sample-size requirement.

## 4. Separated endpoints, fixed before outcomes

The plan requires three endpoints to be reported **separately and never merged into one PASS**:

| endpoint | what it asks | unit |
| --- | --- | --- |
| **Biological source** | coverage of cell identity, animal/session, time and behaviour labels; independence of the structural edge source; interpretability of the graph mapping | dataset / animal |
| **Model** | preregistered held-out prediction loss, calibration or dynamics-correlation metrics defined on **animals or sessions**; the structure x identity interaction | **animal** |
| **Evidence adjudication** | under the frozen rules, which claim ceiling the experiment supports, with identifiable failure types pre-declared | claim |

**Non-negotiable unit rule.** **Frames and neurons are never independent replicates.** A single
animal's frames do not become n independent samples by being many. Model seeds on one animal are not
independent biological samples. `000541` supplies **21 animals**; that is the replicate count available
for a within-dataset design, and it is small.

## 5. What would make the sprint STOP rather than proceed

Pre-declared, so that the decision cannot be made after seeing an outcome:

* **No lawful way to construct the mismatch control** at fixed topology and fixed capacity. If a
  mismatch necessarily changes input scale, dimensionality or label distribution, then H2 is not
  testable and the novelty claim collapses to a dataset-level variation on Beiran 2025.
* **No constructible matched-topology null** (for example, if degree- and module-preserving rewiring
  cannot be generated for the available graphs without destroying the very property under test).
* **Leakage that cannot be removed** — the same animal's frames crossing a train/test boundary, or
  the identity mapping being derived from the target being predicted.
* **Insufficient independent units** for the frozen effect size, with no lawful way to acquire more.

**In any of these cases the plan's decision tree applies: PIVOT the data system, or narrow to a
structure-sensitive prediction study with a reduced biological claim. Do not revive old blocked data
and do not proceed to WP3.**

## 6. Inheritance rule from v1

**v1 frozen results are read-only.** New work lives under `NeuroConverge/v2/` and never retroactively
edits a v1 gate, report or scientific conclusion. In particular, the following v1 lessons enter as
**prior experience only**:

* a blocked public-data analysis is a boundary, **not** a biological negative;
* one specimen's neurons are not that many biological replicates (Fish1.5 precedent);
* "inputs complete" is not "transformation reproduced";
* more observable information did not by itself buy utility in the v1 M2 case — which is exactly the
  question H1 re-poses with a structure-matched null.

## 7. Standing

| item | status |
| --- | --- |
| NCV2-RQ | fixed, verbatim above |
| H1 / H2 / H3 | fixed, with the boundary conditions in section 3 |
| endpoints | separated, unit fixed as animal |
| stop conditions | pre-declared, section 5 |
| any v2 outcome computed | **NONE** |
| any v2 model fitted | **NONE** |
| WP1 data feasibility | `OPEN_PENDING_TASK_AND_SPLIT` after the DANDI resolution |
| nearest-neighbour matrix | preliminary; two entries marked `NOT VERIFIED` |
