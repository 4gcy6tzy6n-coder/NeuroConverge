# Route A full-text eligibility: isolated-context second review

Date: 2026-10-24
Scope: second review of the three contested full-text eligibility candidates (C028, C101, C192)
against frozen exclusions (b) and (c) of `AUDIT_PREREGISTRATION_v1_FROZEN.md` section 3, and
ruling on the replacement-chain closure under the owner's 2026-10-20 first-query narrowing.

## Independence disclosure (required)

This second review was performed by an AI reviewer in an isolated context with no prior contact
with this project, its code, its coding sheets, or its results. A human reviewer can replace it;
this document does not claim human status. It satisfies the second-review request as an
independent re-derivation, not as the P4-appointed human dual-coder gate of frozen section 5.

Blindness to the coding phase was preserved: no file under `CODING_sheets/`, `CODING_v3_20261023/`,
`review_evidence_v3_20261023/`, `output/`, no `CODING_*`, `CALIBRATION_*`, `RESULTS_*`,
`RECONCILIATION_*`, `HANDOFF_*`, or binding/validation records were read. Only eligibility-stage
artifacts (frozen protocol, owner disposition, draw files, screen CSVs, pinned PDFs) were used.
No existing file was modified; this is the only new file.

Prior-exposure control: the earlier author-side rechecks and the 2026-10-20 AI preliminary
second pass were read as required by the assignment, but each ruling below was derived from the
pinned PDFs and the frozen rule text first; the prior dispositions are compared against at the
end, not adopted.

## Frozen rules applied (verbatim anchors)

- Exclusion (b): "claims whose sole evidence is a benchmark the same authors introduced".
- Exclusion (c): "retracted or withdrawn papers (recorded, not coded)".
- Replacement rule: "the next-highest-citation eligible claim in the same stratum substitutes
  for any claim excluded post-draw; substitutions logged with reason". Per the 2026-10-19 data
  source amendment, stratum = mechanism family x primary category, ranked by fetch order.
- Owner narrowing (2026-10-20): eligible claims are limited to the frozen draw's records whose
  first query term is `brain-inspired`; a replacement that would leave that scope requires a
  separate owner-visible disposition, never a silent broadening.
- Second-review packet instruction for C028: "Do not infer authorship from the missing
  provenance."

Interpretive ruling on "benchmark" (applied uniformly below): the frozen text does not define
"benchmark". Its operative property is the introduction of the evaluation instrument by the same
authors: an evaluation battery that the authors themselves constructed and arranged for the
paper's central comparison is an author-introduced benchmark even when its components are
external; conversely, exclusion (b) fires only when the pinned record affirmatively establishes
that introduction and that the instrument is the sole evidence for the sampled claim. Silence in
the record cannot establish either element.

## Source verification

Pinned PDF SHA-256 values were recomputed before any page was read and match
`pinned_fulltext_20261020/FULLTEXT_DOWNLOAD_MANIFEST_20261020.csv` exactly:

| Candidate | Version | SHA-256 (recomputed = manifest) | Pages read | Main-text boundary established |
| --- | --- | --- | --- | --- |
| C028 | 2601.15865v1 | `0150d52e5e23ec4f3036b8e968de7dc7b1200e7b7b7cc9ca74dd45dc02543611` | 1-12 | main text pp. 1-12; references pp. 12-13; no appendix |
| C101 | 2504.05621v1 | `5976a32d491ab48a9e1f72e64705d1b3bccb34428aa171d3dfe87c300be81dfe` | 1-15 (pp. 15-20 headings only) | main text pp. 1-14; data availability/acknowledgments p. 15; references pp. 15-20; no appendix |
| C192 | 2007.04578v1 | `eed352bc96f9f3b00b14c46d089ce8eaae56c66ec6c5dcfa604ede89bd60c435` | 1-9 (pp. 10-12 headings only) | main text pp. 1-9; references pp. 9-11; supplementary pp. 12-20 NOT read |

The arXiv snapshot was also reverified: `corpus_draw_arxiv_v1.snapshot.jsonl` SHA-256
`e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee` (matches all pinned records).
For C192, the supplementary section (pp. 12 onward) was located by heading and deliberately not
read; no conclusion below uses it. This cures the scope deviation recorded in
`REVIEW_ATTEMPT_SCOPE_DEVIATION_20261020.md` for this review's own extraction.

C114 (`2301.02809v2`) exclusion (c) was checked against `C114_WITHDRAWAL_STATUS_20261020.json`
(official abs page retrieved 2026-10-20, withdrawn marker present, no-PDF marker present,
disposition `EXCLUDE_C_WITHDRAWN`). Confirmed; no (b) assessment is possible or needed for a
withdrawn version.

## Case rulings

### C101 (2504.05621v1) -- ruling: EXCLUDE_B (upheld)

Sampled claim unit (from the title-abstract adjudication): brain cross-region development,
connection reorganization and pruning mechanisms are linked to continual-learning and accuracy
gains -- i.e., the paper's central cross-domain continual-learning capability claim.

Main-text evidence, independently re-read:

- p. 4, section 2.1: "To model the progressive of children cognitive functions, we designed a
  Perception-Motor-Interaction (PMI) cross-domain dataset (as Fig. 1B), which incorporates nine
  tasks spanning three cognitive functions and arranges in a sequentially progressive order from
  simple to complex." The authors state they designed the nine-task battery.
- pp. 6-8, sections 2.3-2.4: pruning, retention, fine-tuning-after-pruning, and
  progression-vs-direct-training results are all reported on that nine-task PMI sequence.
- p. 6: the only comparison with external continual-learning algorithms is explicitly narrowed:
  "we conducted a comparative analysis in the widely studied domain of visual perception" --
  i.e., the first three PMI tasks (sketch, cartoon, photo), a subset of the same author-designed
  arrangement, not a cross-domain evaluation.
- pp. 9-10, section 2.5: connectivity-dynamics analyses again on the PMI nine-task run.
- p. 11, section 4.1: "we have designed a cross-domain perception-motion-interaction multiple
  cognitive function dataset", with external component sources named (PACS-derived images [37],
  DeepMind Control Suite [38], MetaWorld [39]); p. 15 data availability confirms the components
  are public. p. 11 Discussion: the method "breaks the traditional single-domain continual
  learning scenario and realizes perceptual-motor-interactive multiple cognitive task continual
  learning".

Reasoning: the qualifying capability claim is cross-domain (perception-motor-interaction)
continual learning. Its direct empirical support in the main text is exclusively the author-
designed PMI battery: every results subsection that tests the claim (pp. 6-10) runs on that
constructed sequence. External components do not externalize the composite: the nine-task
selection, ordering, and progressive arrangement are the authors' instrument. The visual-only
algorithm comparison (p. 6) cannot support the cross-domain claim, both because it tests only a
subdomain and because its setting is a segment of the same PMI arrangement. No other main-text
evidence for the sampled claim exists. Both elements of exclusion (b) are affirmatively
established by the record.

Boundary: claim-unit specific. A narrower visual-only claim unit would need separate assessment;
it is not the sampled claim. Decision: EXCLUDE_B. This upholds the first-pass `PROVISIONAL_EXCLUDE_B`.

### C028 (2601.15865v1) -- ruling: DO_NOT_EXCLUDE_B, with a recorded provenance limitation

Sampled claim unit: selective neural plasticity and attention-modulated learning are linked to
claimed performance and efficiency in coronary-angiography classification (abstract: the
brain-inspired model "achieves strong and stable performance in binary coronary angiography
classification, yielding competitive accuracy, recall, F1-score, and AUC metrics").

Main-text evidence, independently re-read:

- p. 8, section 3.2, the only description of the evaluation data in the entire main text: "we
  evaluated its performance on an independent test set comprising 120 coronary angiography images
  (60 positive and 60 negative cases)."
- pp. 8-10: test metrics (85.00% accuracy, AUC 0.9372), confusion matrix, baseline comparison
  (ResNet18, ResNet34, quantum-enhanced ResNet18), and training-efficiency results -- all on that
  same 120-image set.
- Full main-text sweep (pp. 1-12): no statement of who assembled, supplied, or published the test
  set; no hospital, collection, ethics, or data-availability statement anywhere; the training/
  validation split's source is likewise never described.

Reasoning: exclusion (b) requires the record to establish that the claim's sole evidence is a
benchmark the same authors introduced. This record establishes neither element. The set is
called an "independent test set", never a benchmark; nothing in the main text attributes it to
the authors or to anyone else. Inferring author introduction from silence is forbidden (frozen
rule's burden of proof, and the packet's explicit instruction). Therefore the exclusion does not
fire; retaining the row as permanently "unresolved" would be wrong too, because the
decision-relevant question -- does the pinned main-text record support exclusion (b)? -- is
decidable now and no additional in-scope evidence source exists (main text only; no
supplementary files were retrieved). Decision: DO_NOT_EXCLUDE_B.

Recorded limitation (carried to the coding phase, not an eligibility fact): the evaluation
instrument's provenance is unverifiable from the pinned record; the entire empirical basis is
one unattributed 120-image test set. This bears on later evidence-verification fields and
scope-match coding and must not be lost; it is a reporting defect of the paper, not a frozen
exclusion trigger on this record.

This agrees with the preliminary second pass's DO_NOT_EXCLUDE_B and resolves the first pass's
`REVIEW_REQUIRED_PROVENANCE` open item.

### C192 (2007.04578v1) -- ruling: EXCLUDE_B (for the sampled generalizability claim unit)

Sampled claim unit: the abstract's capability claim that prefrontal RL (brain-inspired adaptive
combination of model-based and model-free control) "can generalize the learned policy to a wide
range of tasks". This is the claim that qualifies the paper for the corpus; the abstract's other
claim (reliably encoding human latent policies) is a fit/recoverability claim, not a capability
improvement claim, and is treated below only to bound the claim unit.

Main-text evidence, independently re-read:

- p. 1 abstract: the two claims are stated separately -- reliability on 82 human subjects'
  two-stage MDP data; generalizability via "large-scale simulations with 10 different Markov
  decision tasks".
- p. 6, Figure 4 caption: "We created a total of 10 different types of tasks by systematically
  manipulating both task structure and task uncertainty (also see Supplementary Methods)."
- p. 6, section 4.1: the ten-task battery is described as the authors' construction; "Task 1 and
  Task 10 correspond to tasks used in previous studies investigating the brain's RL processes
  [4, 23]" (two of ten configurations; Figure 4(D) labels them [Daw2011] and [Lee2014]).
- p. 6, section 4.2: "the average performance across all the tasks represents the empirical
  generalizability" -- the claim's stated estimand is defined on the author-created battery;
  4,920 simulations = 82 subjects x 6 models x 10 tasks.
- p. 7, Figure 5: the empirical-generalizability comparison of the six models on that battery.
  Notably, on Task 1 (the Daw-2011 anchored task) all six models including PM-pfcRL2 are marked
  FAIL, so the externally anchored task does not itself carry the claim.
- p. 8, Figure 6 and text: information-theoretic episodic-encoding analysis, same ten-task
  battery; p. 8 section 5 Conclusion restates the two-claim structure.
- p. 9, Broader Impact: "We used a dataset of human subjects [23, 15, 18] to fit our models" --
  the 82-subject dataset is externally attributed prior data, used for fitting and the
  reliability test, not as the generalizability test.

Reasoning: for the sampled generalizability claim unit, the direct test in the inspected main
text is the ten-task simulation battery the authors created; the aggregate "empirical
generalizability" measure is defined over it. The reliability result on prior human data tests a
different claim. The prior-study anchoring of Tasks 1 and 10 gives precedent for two task
designs but does not externalize the battery, and no independent evaluation of prefrontal RL's
generalizability appears in the main text. Under the uniform "author-introduced evaluation
instrument" reading of "benchmark" applied above, both elements of exclusion (b) hold.

Boundary: claim-unit specific. A hypothetical narrower claim about reliable human-policy
encoding would not trigger (b) (its evidence is prior-collected human data), but that is not the
qualifying capability claim sampled for this corpus. Decision: EXCLUDE_B. This supports the
first pass's provisional EXCLUDE_B.

## Replacement-chain closure ruling

Question: with C101 and C192 both excluded under (b), is the same-layer replacement chain
within the owner-narrowed scope (first query term `brain-inspired`) exhausted?

Mechanical verification from the pinned snapshot (independently reconstructed): parsing the 40
snapshot pages in file order, assigning global fetch ranks by first occurrence, yields 3,246
unique IDs whose ranks agree with `corpus_draw_arxiv_v1_candidates.csv` for all 3,246 rows
(0 mismatches). The first query term `brain-inspired` contributes exactly the records at fetch
ranks 1-200; every record at rank 201 or later is first-attributed to `neuro-inspired` or a
later query term. C214 is rank 214, first query term `neuro-inspired` -- out of scope, confirmed.

The `other` family x `cs.AI` stratum inside the owner scope (ranks 1-200) contains exactly 15
records, in fetch order:

| rank | record | status |
| --- | --- | --- |
| 1 | C001 2305.10938v1 | frozen draw; title-abstract ineligible (no specific mechanism) |
| 2 | 2003.12353v1 | mechanically filtered out by the frozen draw (`no ai term`); not eligible, cannot substitute |
| 4 | C004 2303.15935v1 | frozen draw; title-abstract ineligible |
| 7 | C007 2312.07213v4 | frozen draw; title-abstract ineligible |
| 36 | C036 1903.12517v1 | replacement for C001; eligible, full-text clear |
| 59 | C059 1810.01620v1 | title-abstract ineligible (no qualifying mechanism) |
| 65 | 2603.15371v1 | mechanically filtered (`no ai term`) |
| 74 | C074 2402.18784v2 | title-abstract ineligible |
| 80 | 2508.17198v1 | mechanically filtered (`no ai term`) |
| 84 | 2012.13529v1 | mechanically filtered (`no ai term`) |
| 101 | C101 2504.05621v1 | replacement for C004; EXCLUDE_B (this review) |
| 114 | C114 2301.02809v2 | replacement for C007; withdrawn, EXCLUDE_C |
| 167 | C167 2308.12486v2 | title-abstract ineligible |
| 175 | C175 2103.06123v1 | title-abstract ineligible |
| 192 | C192 2007.04578v1 | continuation for C007; EXCLUDE_B (this review) |

Ranks 193-200 (the tail of the `brain-inspired` stream) contain no `other` x `cs.AI` records
(they are cs.LG/cs.NE/cs.ET records in other families). After rank 200 no `brain-inspired`
record exists at all. As an independent spot-check of the chain's prerequisites, the abstracts
of C059, C074, C167, and C175 were pulled from the pinned snapshot; each supports its logged
title-abstract ineligibility (inspirational framing without a specific biological mechanism, or
a position paper without demonstrated capability improvement).

Closure verdict:

- C007 chain: C007 (title-abstract out) -> C114 (withdrawn, exclusion c) -> C167, C175
  (title-abstract out) -> C192 (EXCLUDE_B, this review) -> next same-stratum record is C214 at
  rank 214, first query term `neuro-inspired`, outside the owner-approved scope. The chain is
  CLOSED at the owner boundary with the slot unfilled. It is not merely paused for convenience:
  within the narrowed scope no further same-stratum candidate exists in the pinned snapshot.
- C004 chain: C004 (title-abstract out) -> C101 (EXCLUDE_B, this review) -> the only later
  same-stratum in-scope records are C114 (already in the C007 chain, and withdrawn under (c)
  regardless), C167/C175 (ineligible), and C192 (excluded). CLOSED at the owner boundary with
  the slot unfilled.
- No cross-query substitution may be made silently. Using C214 or any later-query record would
  broaden the owner's frozen scope and requires a separate owner-visible dated disposition
  (`OWNER_DISPOSITION_20261020_ARXIV_QUERY_ORDER.md`). This review makes no such substitution.

## Final corpus composition after rulings

16 claims -- inside the frozen acceptance interval 15-25. Composition: 14 title-abstract
eligible frozen-draw records + 2 completed replacements (C036 for C001, C077 for C020); 2
replacement slots (C004, C007) remain unfilled with chains closed at the owner boundary.

| # | claim id | arXiv version | one-line topic |
| --- | --- | --- | --- |
| 1 | C003 | 2207.08533v2 | BrainCog: an SNN-based brain-inspired cognitive-intelligence engine claimed to support AI cognitive functions and brain simulation |
| 2 | C006 | 2508.18961v1 | TaiBai brain-inspired processor with topology-aware energy efficiency at comparable accuracy |
| 3 | C008 | 2412.08875v1 | cortical-region functions and functional connectivity proposed as the basis of a brain-inspired AI agent (conceptual, no empirical benchmark) |
| 4 | C010 | 2107.14654v1 | bilateral brain asymmetry used to design neural-circuit policies claimed to improve autonomous-driving generalization |
| 5 | C011 | 2401.15661v2 | brain-inspired locality, sparsity and modularity yielding smaller accurate physics-informed neural networks |
| 6 | C016 | 2309.05263v1 | brain-region motifs with E/I and cross-module connections evolved for spiking-network architectures |
| 7 | C018 | 2203.14679v1 | leaky-integrate-and-fire spiking communication introduced into MLPs claimed to improve image classification |
| 8 | C021 | 2411.09953v2 | spiking-transformer diffusion policy claimed to improve robotic action generation over transformer baselines |
| 9 | C028 | 2601.15865v1 | selective-plasticity and attention-modulated learning in a lightweight brain-inspired coronary-angiography classifier (test-set provenance unrecorded; limitation carried to coding) |
| 10 | C032 | 2509.00047v1 | brain-inspired replay claimed to reduce continual-learning forgetting |
| 11 | C036 | 1903.12517v1 | brain-inspired trial-and-error with modified replay in deep recurrent RL for simulated self-driving (replaces C001) |
| 12 | C043 | 2511.17687v2 | learning-based replication of continuous-attractor neurodynamics claimed to boost path-integration efficiency |
| 13 | C045 | 2305.11252v1 | review of brain-inspired (synaptic-plasticity) learning mechanisms for artificial networks |
| 14 | C046 | 1711.10563v2 | FearNet hippocampal-prefrontal dual-memory model for incremental learning |
| 15 | C049 | 2311.15474v1 | programmable heterogeneous optoelectronic neuron in a photonic spiking network with expressivity/efficiency claims |
| 16 | C077 | 1811.09699v1 | primate attention-network circuitry implemented in a DNN claimed to improve visual search (replaces C020) |

Excluded and recorded (not coded, per the frozen rules): C001, C004, C007, C020 (title-abstract
claim criterion); C114 (withdrawn, exclusion (c), evidence pinned); C101 (exclusion (b), this
review); C192 (exclusion (b), this review). Screened out during replacement scans: C059, C074,
C167, C175 (title-abstract). Out of scope, not used: C214 (`neuro-inspired`).

## Relation to prior dispositions

| Case | First pass (2026-10-20) | AI preliminary pass (2026-10-20) | This second review |
| --- | --- | --- | --- |
| C101 | PROVISIONAL_EXCLUDE_B | EXCLUDE_B | EXCLUDE_B (upheld, independently derived) |
| C028 | REVIEW_REQUIRED_PROVENANCE | DO_NOT_EXCLUDE_B | DO_NOT_EXCLUDE_B + recorded provenance limitation |
| C192 | provisional EXCLUDE_B, review required | EXCLUDE_B | EXCLUDE_B for the generalizability claim unit |

No disagreement with the preliminary pass's outcomes arose; the rulings above were derived from
the pinned texts and frozen rules, with the prior notes used only for later comparison.

## Limits of this review

- This is a full-text eligibility decision only. No T1-T5 transition, E0-E4 evidence grade, or
  scope-match verdict is assigned here; those belong to the frozen coding protocol with its named
  P4 coders, at least one of whom must not be a workspace-code author. This review does not open
  coding.
- Main text only, per the owner's scope decision. Appendix or supplementary evidence was not
  consulted for any ruling; a later expansion of scope requires a separately recorded decision.
- The C028 provenance limitation is recorded for the coding phase without prejudging any grade.
- The unfilled C004/C007 slots and the count 16 are within the frozen acceptance interval; the
  replacement rule is satisfied by closure at the owner boundary, not waived.
- No experiment, recompute, GPU work, or protocol amendment is authorized by this document.
