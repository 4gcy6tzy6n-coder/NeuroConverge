# Biological-to-artificial intelligence transfer: an analysis of evidence supporting mechanistic claims

**Draft status: skeleton with drafted Introduction and Methods; every Results/Discussion number is a slot
filled only from the post-coding recomputation.** Working draft for the Nature Machine Intelligence Analysis
format (<= 3,500 main words, abstract 100-150, <= 6 figures, <= 50 references). Author list, affiliations and
correspondence: owner-side.

## Abstract (slot, 100-150 words)

[Drafted after coding; must carry: the first-query corpus and its size; the evidence-chain decomposition
(T1-T5); the headline range with its definition-dependence stated; the delegated-biology finding; the
correspondence (T2) gap as the central result; the item-level reportability deliverable; the explicit
non-representativeness sentence.]

## Introduction (drafted; number-free by construction)

Biological mechanisms are among the most frequently invoked justifications for design choices in artificial
intelligence: spiking dynamics, cortical motifs, hippocampal replay, dopaminergic prediction-error signals
and connectome-derived architectures each anchor a literature in which an artificial system's component is
presented as the inheritor of a biological computation. The claims matter beyond their performance tables.
When a mechanism's biological pedigree is accepted as part of a paper's contribution, the pedigree itself
becomes evidence - and the field's collective belief in which mechanisms transfer becomes, in part, a belief
about how well those pedigrees are supported.

This article asks a narrow question of that literature: **what evidence do bio-to-AI transfer papers
themselves supply, at each step of the inference their titles assert?** We decompose each claim into a
five-transition chain - from the biological structure, through the computation it performs, through the
correspondence between that computation and the artificial component, to the utility and generality of the
resulting system - and audit, item by item, where controlled evidence appears and where it does not.

Three design choices distinguish this audit from a survey. First, the unit of analysis is the **transition**,
not the paper: a paper can hold strong utility evidence and empty correspondence evidence, and the difference
is the finding. Second, evidence is graded **separately from reporting**: an E-grade scale captures what
controlled support exists in the paper (with externally established support recorded as its own layer), while
an item-level reportability coding records what the paper discloses - two weaknesses the literature often
conflates. Third, the corpus is **frozen, versioned and provenance-pinned end to end**: every audited paper
is a hash-pinned arXiv record, every coded judgement traces to a pinned byte range, and every instrument
(transition taxonomy, grade scale, checklist, scoring code) was frozen and independently reviewed before any
claim was scored.

The audit's premise was itself falsifiable: had the corpus's headline claims carried controlled evidence at
nearly every transition, the exercise would have reported that. [Kill-rule sentence lands here post-coding.]
What we report instead is a structure: the biological foundations of these claims are neither demonstrated
in-paper nor unsupported - they are **delegated**, by citation, to an independently established literature
that usually does support the specific computation invoked - while the distinctive content of
"brain-inspired", the claimed correspondence between the biological computation and the artificial
component, is the chain's least controlled link. [Final numbers and their definition-dependence land here.]
The constructive deliverable is a reporting standard for that middle of the chain: item-level, dual-coded,
with the same expectation of controlled disclosure the field already applies to utility comparisons.

## Results (slots)

- **Fig 1 | The claim chain and where evidence sits.** [Grade distributions, T1-T5, both layers; the
  delegated-biology picture with the specificity-verification layer.]
- **Fig 2 | The correspondence gap.** [T2 as the least-controlled transition against T3; per-family repeats.]
- **Fig 3 | Headline reliance.** [Share of claims whose abstract's improvement claim rests on an
  uncontrolled transition; the definition-dependence band; both coders' maps shown separately.]
- **Fig 4 | Reportability by item.** [Item-level complete/incomplete counts, per item, after adjudication;
  no aggregation beyond per-item (COND-1); the caveated descriptive cross-tab if used (COND-2).]
- **Fig 5 | Coder agreement.** [Per-transition disagreement; the same-model isolated-instance disclosure
  prominent; human-supersedure note.]
- **Fig 6 | The reporting standard.** [The checklist as the deliverable; one line per transition.]

## Discussion (frame drafted, numbers as slots)

The pattern - foundations delegated and usually well anchored, utility controlled, correspondence asserted -
is consistent with how refereeing works: baseline comparisons are what reviewers already check, so that is
where authors invest controlled evidence. The gap we measure is therefore not a failure of intent but a
**coordination failure of evidentiary standards**: no part of the current review contract asks a paper to
show that its artifact instantiates the computation its title invokes. [Discussion slots: what a T2-standard
review would ask; what the finding does NOT claim (no field prevalence - first-query corpus; no judgment of
any mechanism's truth); the calibration case study (workspace projects, Supplementary) showing the framework
detects known boundaries; limitations paragraph with the full list from the limitations document.]

## Methods (drafted; the governance chain as built)

**Protocol and preregistration.** The audit runs under a frozen preregistration (transition taxonomy T1-T5;
evidence grades E0-E4 with in-paper and external layers recorded separately; item-level reportability with a
four-status vocabulary), amended twice by dated owner-visible records: a data-source amendment (arXiv API in
place of a keyed bibliographic API, with the ranking and stratification consequences stated) and a
reportability amendment separating evidence grades from reporting completeness, both with independently
reviewed, hash-bound instruments. Thresholds, outputs and the stop rules - including a preregistered kill
rule under which a corpus-wide majority of controlled headline evidence would have ended the analysis - were
frozen before any claim was scored.

**Corpus.** [Slot: the frozen draw's numbers - candidates screened, records drawn, the owner's
scope-narrowing to the first query term, the adjudication and eligibility screens with every exclusion and
replacement logged, the final N and its composition, the provenance chain: query snapshot hash, per-PDF and
per-text-layer SHA-256 manifests.] The corpus is a candidate sample of arXiv-declared mechanism claims; it
is not representative of the field, and no prevalence claim is made anywhere in this article.

**Coding.** Each claim's five transitions were graded independently by two coders working from the pinned
texts under frozen instructions, with quoted justifications and location pointers. The coders are
isolated-context instances of the same AI assistant: mechanical isolation (separate contexts, no shared
reasoning trace, blindness to all results and to each other) is real; error independence is not claimed, and
the per-transition disagreement statistics are reported as the honest noise term of one instrument. A human
coder pass supersedes this one and triggers recomputation by script; the disclosure and supersession rule
stand as part of the method. Adjudication follows preregistered rules (weaker-grade resolution; one
adjudication record per disputed cell; the count of adjudications matching neither coder is reported).

**External-evidence layer and specificity verification.** For transitions resting on citation, the cited
sources were recorded per claim and the **specificity match** graded on a frozen three-point scale (supports
the specific computation / supports the general phenomenon only / does not address), separating "the biology
is established elsewhere" from "the biology supports this use of it".

**Reportability.** Item-level coding under the bound checklist (11 items across T1-T5), four statuses, no
NOT_APPLICABLE, source-pointer rules with per-claim source-role binding, scored by the hash-bound scorer
that validates the row grid, adjudication closure and declared source bytes before computing any count.
Per-item counts and the raw rows are the only aggregations; no overall reportability score exists in this
article by protocol.

**Reproducibility.** Every number is script-computed from committed artifacts (draw scripts, merge and
scoring code under synthetic failure-class checks; manifests pinning snapshot, PDFs, text layers and
instruments); nothing in Results is transcribed by hand. [Slot: data and code availability statements;
the independent verification record.]

## Author contributions, competing interests, data/code availability

[Owner-side; the AI-assistance disclosure per NMI policy: instrument construction, coding passes, and
analysis automation by the disclosed AI workflow, under human direction and with the human-supersedure
rules stated in Methods.]
