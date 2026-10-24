# Biological-to-artificial intelligence transfer: an analysis of evidence supporting mechanistic claims

**Draft status: Introduction, Results, Discussion and Methods carry the post-coding numbers; every
Results number is re-derived by `field_audit/fill_results_numbers.py` from the committed frozen
artifacts.** Working draft for the Nature Machine Intelligence Analysis format (<= 3,500 main
words, abstract 100-150, <= 6 figures, <= 50 references). Figures are specified with their
numbers below; production follows the figure contracts. Author list, affiliations and
correspondence: owner-side.

## Abstract (136 words)

Evidence audits of biological-to-artificial intelligence transfer have concentrated on utility;
the mechanistic pedigree of a design choice is usually accepted as stated. We decompose a frozen,
hash-pinned corpus of 16 arXiv-declared mechanism claims into a five-transition inference chain
and grade, transition by transition, what controlled evidence each paper itself supplies. No
claim evidences its structure-to-computation transition in-paper (16/16 E0): the biological
foundation is delegated by citation. The computation-to-correspondence transition - the content
that makes a system "brain-inspired" - is the chain's least-controlled link (12/16 suggestive
only), while utility comparisons are where controlled evidence concentrates (10/16). A
preregistered kill rule (80 percent controlled headline evidence) was not triggered (62.5
percent, 95 percent CI 39-82). We deliver an item-level, dual-coded reporting standard for the
uncontrolled middle of the chain. The corpus is a first-query candidate sample; no prevalence
claim is made.

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

The audit's premise was itself falsifiable: had 80 percent or more of the corpus's headline claims
carried controlled evidence at their headline transition, the analysis would have reported that
and stopped; the observed share is 62.5 percent (10/16, 95 percent CI 39-82 percent), below the
preregistered bar.
What we report instead is a structure: the biological foundations of these claims are neither demonstrated
in-paper nor unsupported - they are **delegated**, by citation, to an established literature whose specific
support for the invoked computation one coder could verify route-wise for 15 external cells, though the
two-coder protocol could not merge this layer and it enters the analysis only as a disclosed convention
divergence - while the distinctive content of
"brain-inspired", the claimed correspondence between the biological computation and the artificial
component, is the chain's least controlled link (E1 only in 12 of 16 claims). At the headline,
37.5 percent of claims (6/16, 95 percent CI 18-61 percent) rest their abstract's improvement claim
on a transition with no controlled in-paper evidence; the two coders' own headline maps put this at
37.5 and 31.25 percent respectively.
The constructive deliverable is a reporting standard for that middle of the chain: item-level, dual-coded,
with the same expectation of controlled disclosure the field already applies to utility comparisons.

## Results

**The chain, transition by transition (Fig 1).** Under the weaker-grade merge of two independent
coders, the structure-to-computation transition T1 carries no in-paper controlled evidence in any
claim (E0 16/16): every paper in the corpus delegates its biological foundation to citation. The
computation-to-correspondence transition T2 is nearly as thin (E1 12/16, E0 2/16, E2 2/16) - the
claimed instantiation of the invoked computation is, in twelve of sixteen claims, supported only
suggestively, in a single setting with no control named for this transition. Utility comparisons
(T3) are where controlled evidence concentrates (E2 10/16, E1 4/16, E0 2/16). Generality (T4: E1
9/16, E0 6/16, E2 1/16) and scope fidelity (T5: E1 11/16, E2 4/16, E0 1/16) fall between. The
delegation is not absence of biological support: an in-paper E0 records that the paper itself
supplies no evidence for the transition, a different fact from the transition being unevidenced
anywhere (Methods, external layer).

**The correspondence gap (Fig 2).** T2 is the least-controlled content transition in the chain:
its controlled-evidence share (2/16) sits below T3's (10/16) by a factor of five, and below every
other transition's in-paper mass except T1, which is definitionally delegated. T1 and T3 are also
the two transitions on which the coders fully agree (18/80 in-paper disagreements overall,
22.5 percent, fall on T5 (10), T4 (6) and T2 (2)); the correspondence judgements that do disagree
are resolved to the weaker grade, so the gap as reported is the conservative reading.

**Headline reliance (Fig 3).** Fifteen of sixteen abstract improvement claims rest on T3 and one
on T2 (merged map; the coders disagreed on 2/16, resolved by the frozen weaker-evidence rule).
Evaluating each claim at its headline transition, 10/16 (62.5 percent, 95 percent CI 39-82
percent, Wilson interval [17]) carry controlled in-paper evidence; 6/16 (37.5 percent, CI 18-61 percent) rest on E0/E1.
The preregistered kill rule - 80 percent controlled headline evidence ends the analysis with the
opposite conclusion - was not triggered. The T5 scope-match rate on the merged sheet is 11/16
(68.8 percent): five claims' abstract scope exceeds what their evidence setting supports.

**Reportability, item by item (Fig 4).** No item is aggregated into a score (by protocol). Of the
11 items, complete reporting is the rule for naming the biological structure (T1-01: 14/16), the
component-function mapping (T2-01: 15/16), abstract-to-result linkage (T5-01: 14/16) and the
evidence setting (T5-02: 13/16). It collapses exactly where the chain is weakest: a pin-able,
specific source for the structure-computation evidence (T1-03) is complete in 0/16 and reached
REFERENCED in none; an inventory of which attribution controls are present or absent (T3-02) is
complete in 0/16; departures from the biological mechanism (T2-02) are completely listed in 3/16;
scale sensitivity or its explicit absence (T4-02) is complete in 4/16, as is beyond-demonstrated
task-family status (T4-01: 4/16). Input-output statements of the attributed computation (T1-02)
are complete in 9/16; the attribution comparison itself (T3-01) in 9/16.

**Coder agreement and adjudication (Fig 5).** In-paper disagreement is 22.5 percent (18/80), the
reportability item disagreement 22.2 percent (39/176), and 0 of 39 adjudications chose a status
neither coder had recorded. Both coders are isolated-context instances of the same AI assistant:
mechanical isolation is real, error independence is not claimed, and the disagreement statistics
are reported as the honest noise term of one instrument. A human coder pass supersedes and
triggers recomputation by script.

**The reporting standard (Fig 6).** The eleven items, their four statuses and the
source-registration rules - already executable as a bound scorer that refuses an incomplete grid,
an unregistered source or a hash mismatch before computing any count - constitute the deliverable:
a checklist a referee can apply to the middle of the chain today.

## Discussion (frame drafted, numbers as slots)

The pattern - foundations delegated, utility controlled, correspondence asserted -
is consistent with how refereeing works: baseline comparisons are what reviewers already check, so that is
where authors invest controlled evidence. The gap we measure is therefore not a failure of intent but a
**coordination failure of evidentiary standards**: no part of the current review contract asks a paper to
show that its artifact instantiates the computation its title invokes. A T2-standard review would ask
three things the corpus almost never gets: the mapping from each artificial component to the biological
function it claims to instantiate, the departures from that mechanism, and a comparison that attributes
gains to the correspondence rather than to capacity or tuning - the three items whose complete-reporting
counts are 15/16, 3/16 and 9/16 (with the control inventory itself at 0/16).

What this finding does not claim: it is not a prevalence statement about the field (the corpus is a
first-query candidate sample of arXiv-declared mechanism claims, and every proportion above carries its
interval); it passes no judgment on the truth of any mechanism (an in-paper E0 transition may be true -
the finding is about what the papers themselves supply); and it does not evaluate the cited external
literature's support (the external layer could not be merged under the two-coder protocol and is
disclosed as a convention divergence; the pilot-corpus specificity verification, in which 11 of 14
delegated foundations were supported specifically, is reported in the Supplementary as pilot evidence).
The framework's own validity is checked against five workspace projects as calibration case studies
(Supplementary). Limitations are as follows: the quota sample's width (16 claims; Wilson 39-82 percent
on the headline statistic); the same-model coder pair with disclosed correlated-error risk; the
AI-instrument, AI-coding and AI-adjudication roles, each under human supersession; the exclusion of
non-arXiv and non-English literatures; and the absence, by protocol, of any overall reportability score
(aggregation is sealed).

## Methods (drafted; the governance chain as built)

**Protocol and preregistration.** The audit runs under a frozen preregistration (transition taxonomy T1-T5;
evidence grades E0-E4 with in-paper and external layers recorded separately; item-level reportability with a
four-status vocabulary), amended twice by dated owner-visible records: a data-source amendment (arXiv API in
place of a keyed bibliographic API, with the ranking and stratification consequences stated) and a
reportability amendment separating evidence grades from reporting completeness, both with independently
reviewed, hash-bound instruments. Thresholds, outputs and the stop rules - including a preregistered kill
rule under which a corpus-wide majority of controlled headline evidence would have ended the analysis - were
frozen before any claim was scored [18].

**Corpus.** The sixteen audited claims [1-16] come from a relevance-ranked arXiv API draw that pinned 3,246 records (snapshot SHA-256 `e73f72f5...`,
committed as JSONL with per-record provenance); 18 claims were selected under the frozen family and
category caps, adjudicated for claim type with logged replacements, and pinned as PDFs with per-file
SHA-256 manifests and an extracted text layer hashed alongside. The owner's scope ruling narrowed the
corpus to the first query term; the full-text eligibility second review then removed two claims
(record: `ELIGIBILITY_SECOND_REVIEW_20261024.md`), giving the final N = 16 across 8 primary
categories and mechanism families as drawn (2017-2026). Every exclusion and replacement is logged.
The corpus is a candidate sample of arXiv-declared mechanism claims; it
is not representative of the field, and no prevalence claim is made anywhere in this article.

**Coding.** Each claim's five transitions were graded independently by two coders working from the pinned
texts under frozen instructions, with quoted justifications and location pointers. The coders are
isolated-context instances of the same AI assistant: mechanical isolation (separate contexts, no shared
reasoning trace, blindness to all results and to each other) is real; error independence is not claimed, and
the per-transition disagreement statistics are reported as the honest noise term of one instrument. A human
coder pass supersedes this one and triggers recomputation by script; the disclosure and supersession rule
stand as part of the method. Adjudication follows preregistered rules (weaker-grade resolution; one
adjudication record per disputed cell; the count of adjudications matching neither coder is reported).

**External-evidence layer and specificity verification.** For transitions resting on citation,
the cited sources were recorded per claim and the **specificity match** graded on a frozen
three-point scale (supports the specific computation / supports the general phenomenon only /
does not address), separating "the biology is established elsewhere" from "the biology supports
this use of it". On the final corpus the two coders' external conventions diverged - one recorded
15 cells at E3 with verification routes, the other recorded none under its stricter
no-verification rule - and the preregistered weaker merge resolves all of them to E0; the layer
therefore enters Results only through this disclosed divergence, and the specificity
verification (11 of 14 delegated foundations supported specifically, 3 generally, 0 unsupported)
is reported as pilot-corpus evidence in the Supplementary.

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

## References

1. Yi Zeng et al. BrainCog: A Spiking Neural Network based Brain-inspired Cognitive Intelligence Engine for Brain-inspired AI and Brain Simulation. arXiv:2207.08533v2 (2022).
2. Qianpeng Li et al. TaiBai: A fully programmable brain-inspired processor with topology-aware efficiency. arXiv:2508.18961v1 (2025).
3. Bo Yu et al. Brain-inspired AI Agent: The Way Towards AGI. arXiv:2412.08875v1 (2024).
4. Hasan Bayarov Ahmedov et al. Brain-Inspired Deep Imitation Learning for Autonomous Driving Systems. arXiv:2107.14654v1 (2021).
5. Stefano Markidis et al. Brain-Inspired Physics-Informed Neural Networks: Bare-Minimum Neural Architectures for PDE Solvers. arXiv:2401.15661v2 (2024).
6. Wenxuan Pan et al. Brain-inspired Evolutionary Architectures for Spiking Neural Networks. arXiv:2309.05263v1 (2023).
7. Wenshuo Li et al. Brain-inspired Multilayer Perceptron with Spiking Neurons. arXiv:2203.14679v1 (2022).
8. Qianhao Wang et al. Brain-inspired Action Generation with Spiking Transformer Diffusion Policy Model. arXiv:2411.09953v2 (2024).
9. Jingsong Xia et al. A Lightweight Brain-Inspired Machine Learning Framework for Coronary Angiography: Hybrid Neural Representation and Robust Learning Strategies. arXiv:2601.15865v1 (2026).
10. Jina Kim et al. Teaching AI to Remember: Insights from Brain-Inspired Replay in Continual Learning. arXiv:2509.00047v1 (2025).
11. Jieneng Chen et al. Towards Brain-inspired System: Deep Recurrent Reinforcement Learning for Simulated Self-driving Agent. arXiv:1903.12517v1 (2019).
12. Zhangyu Ge et al. Boosting Brain-inspired Path Integration Efficiency via Learning-based Replication of Continuous Attractor Neurodynamics. arXiv:2511.17687v2 (2025).
13. Samuel Schmidgall et al. Brain-inspired learning in artificial neural networks: a review. arXiv:2305.11252v1 (2023).
14. Ronald Kemker et al. FearNet: Brain-Inspired Model for Incremental Learning. arXiv:1711.10563v2 (2017).
15. Yun-Jhu Lee et al. Demonstration of Programmable Brain-Inspired Optoelectronic Neuron in Photonic Spiking Neural Network with Neural Heterogeneity. arXiv:2311.15474v1 (2023).
16. Hossein Adeli et al. Learning to attend in a brain-inspired deep neural network. arXiv:1811.09699v1 (2018).
17. Wilson, E. B. Probable inference, the law of succession, and statistical inference. J. Am. Stat. Assoc. 22, 209-212 (1927).
18. Nosek, B. A., Ebersole, C. R., DeHaven, A. C. & Mellor, D. T. The preregistration revolution. Proc. Natl Acad. Sci. USA 115, 2600-2606 (2018).
