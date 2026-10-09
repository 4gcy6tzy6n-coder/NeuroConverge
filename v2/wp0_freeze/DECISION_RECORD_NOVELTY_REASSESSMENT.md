# DECISION_RECORD — NCV2-SPRINT-01, novelty reassessment after reading the Creamer v4 full text

**Date:** 2026-10-09. **Trigger:** the joint lead supplied
`2024.09.22.614271v4.full.pdf` (10 pages, 1,971,256 B), which was read in full this session via
`pdftotext -layout` (950 lines, 67,724 characters).

**Verdict: `PIVOT_OR_STOP` on the H2-centred novelty claim.** The claim v2 was built to test is
already published, using **the same connectome files**. This is recorded as the sprint's finding, not
softened into a "narrower contribution" without saying so.

---

## 1. What was read, and the four passages that decide it

**Creamer MS, Leifer AM, Pillow JW.** *Bridging the gap between the connectome and whole-brain activity
in C. elegans.* bioRxiv `10.1101/2024.09.22.614271`, **v4 posted 2026-05-18**, CC-BY-NC 4.0. Princeton
Neuroscience Institute. Code: `github.com/Nondairy-Creamer/Creamer_LDS_2026`.

**Passage 1 -- the identity permutation, which is v2's M1.**

> "**Shuffled-connectome constraint.** We constructed this shuffled connectome by taking the binary
> connection matrix of the connectome and **permuting its rows and columns**. In this way **any given
> neuron is assigned the connectivity pattern of another randomly chosen neuron** in the data set.
> **The resulting network is topologically identical to the original network; we have only permuted the
> identity of each node in the graph.**"

**Passage 2 -- the same manipulation, named as an identity shuffle.**

> "we constrained the dynamics matrix W to the connectome, but **shuffled the neural identities** (Fig
> 3 A iv note the label changes)."

**Passage 3 -- the connectome files, which are the ones v2 downloaded.**

> "**Connectome.** ... the connectome we used was the sum of the matrix of synapse counts from **three
> adult connectomes** and one L4 connectome. All connectomes were taken from **https://www.nemanode.org/
> on November 1st, 2025**. The specific CSVs used were **`white_1986_jsh.csv`, `white_1986_n2u.csv`,
> `witvliet_2020_7.csv`, and `witvliet_2020_8.csv`**."

**Passage 4 -- the animal scale and the cross-animal claim.**

> "**The data set of 110 animals** was split into 5 different subsets of **55 animals in the train set
> and 55 animals in the test set.**"
>
> "the model has learned the functional properties of individual neurons that are unique to each neuron
> and **conserved across animals**."

## 2. The coverage table

| element of the v2 design | Creamer et al. v4 | verdict |
| --- | --- | --- |
| Witvliet adult connectome from NemaNode | **`witvliet_2020_7.csv`, `witvliet_2020_8.csv`, same source, fetched 2025-11-01** | **identical inputs** |
| a connectome-constrained dynamical model | "non-zero weights only between anatomically connected neurons", via a weight `mask` | **done** |
| **v2's M1: identity permutation at fixed topology** | "**topologically identical ... only permuted the identity of each node**" | **DONE -- this is M1** |
| v2's M2: cross-animal identity rotation | "permuting its rows and columns ... assigned the connectivity pattern of another randomly chosen neuron" | **DONE in substance** |
| a shuffled-topology null | "alternative models fit using a shuffled connectome achieved **much lower performance**" | **done** |
| cross-individual generalisation | **110 animals**, 55/55 splits, "conserved across animals" | **done, at 5x v2's animal count** |
| held-out neuron prediction from the rest | "reconstruct held-out neurons", mean correlation 0.25, AVER best at 0.93 | **done** |
| structure specificity | "adding connections beyond those in the connectome did not improve" performance | **done** |

**The honest conclusion: v2's proposed novelty was "hold topology fixed and vary the mapping". Creamer
already holds topology fixed and varies the mapping, calls the result striking, and uses the same two
connectome files.**

## 3. The one residual, stated at its true size

**Residual R: Creamer varies the mapping only on the real graph.** They test identity-shuffle against
real topology; they do **not** cross "graph shuffled" with "identity shuffled" as a 2 x 2 design, so
they do not report a structure x mapping interaction as its own estimand.

**Why this is not a rescue.** It is a **methodological refinement of a result they already report**, not
a new scientific question. v2 would be asking the same question in a factorial layout. **The joint
lead's standard governs: exchanging a dataset or a network is not a sufficient basis for an NMI-level
contribution, and a factorial re-layout of an existing result is weaker than either.**

**A second apparent residual that is also not a rescue.** v2's functional data (`000541`) is a
**different task** -- spontaneous and chemically stimulated calcium imaging in a microfluidic chip, with
**no optogenetic perturbation** -- whereas Creamer's is perturbation-based causal interaction. So v2
would be "the same design logic, a weaker task, and a different dataset". **A weaker task does not
create novelty.**

## 4. What the plan and the lead require now

**Plan:** *if WP1 data are unqualified, do NOT run the biological structure contribution test; **PIVOT
to a clearly identifiable alternative system or narrow to a structure-sensitive prediction study with a
reduced biological claim**, rather than reviving old blocked data.*

**Joint lead, verbatim:** *if such a comparison cannot be constructed, then however well the real graph
predicts, the project must reassess whether it has sufficient independent scientific contribution.*

**Both conditions are now met.** The comparison **can** be constructed; it has **already been
constructed by someone else, and published.**

## 5. Recommendation

> **Do not proceed to WP3 on the H2 novelty basis.** The sprint's deliverable -- proof that an
> answerable scientific question exists with real data, valid controls and independent units -- **is
> still met**, and the data feasibility work stands on its own. **But the question that was going to
> carry the contribution has been answered in the literature, on the same inputs.**

**Three lawful options, in the order this review would rank them:**

1. **PIVOT the data system.** Find a condition Creamer's design cannot address at all -- for example a
   preparation with no perturbation capability and a genuinely different structural source, where the
   *structural prior itself* is the object of inference rather than the mapping. **This requires its own
   feasibility pass, not a relabelling of the current plan.**
2. **NARROW with a reduced biological claim**, per the plan's own second branch: a
   structure-sensitive prediction study that **does not claim an identity or topology increment**, and
   says so in its title. Honest, but **unlikely to be an NMI-level contribution.**
3. **STOP this line** and return the feasibility audit as a negative methodological result: *the
   cross-individual identity-mismatch design is already realised in the literature, on these exact
   connectomes, at 110 animals.* **A well-evidenced negative positioning result is worth more than a
   confirmatory study of a published effect.**

**What this review does NOT recommend: proceeding as though the overlap were partial.** It is not
partial.

## 6. Claim ceiling for anything that follows

* v2 may **not** claim novelty for: connectome-constrained prediction, real-versus-shuffled topology,
  identity-permutation mismatch, cross-animal generalisation, or held-out neuron reconstruction.
* v2 may **not** describe the DANDI and NemaNode resources as its contribution.
* The feasibility work **is** a contribution of this sprint: an audited, reproducible route to
  identity-resolved functional data, with a content-level v1 freeze proof and two `NOT VERIFIED`
  citations recorded rather than guessed.
* **No v2 experiment has been run. No v2 endpoint exists. This document is a positioning decision, not
  a result.**

## 7. Provenance

* Full text read: `pdftotext -layout`, 950 lines, 67,724 characters, from the file the joint lead
  supplied.
* All four quoted passages located by line number in the extraction and quoted verbatim.
* Reproduced against the bioRxiv version record (four versions, v4 = 2026-05-18) and the repository
  README, both fetched this session.
* **The full text has been read; the authors' code has not been executed and their data splits have not
  been independently reproduced from their repository.** That is stated so the finding is not read as
  stronger than it is.
