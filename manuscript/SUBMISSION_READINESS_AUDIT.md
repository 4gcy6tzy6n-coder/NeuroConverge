# NMI submission readiness audit

**Assessment date:** 3 October 2026  
**Decision:** internal manuscript candidate; not ready for submission to *Nature Machine Intelligence* as an Article or Analysis. The DMP and newly selected V1 PC→SST synthetic experiments have completed; neither changes the venue-readiness decision. This audit separates presentation and packaging checks from the scientific contribution decision.

## Current manuscript package

| Check | Current evidence | Assessment |
|---|---|---|
| Article structure | Unheaded opening, Abstract, Results, Discussion, Methods, references and six figure legends | Matches the broad NMI Article structure described by the journal; final editorial formatting remains subject to the submission system |
| Main-text size | 3,380 tokens across the introduction, Results and Discussion, using the local Unicode regex tokenizer; Methods, abstract, references, legends and statements excluded | Below the 3,500-word Article limit by this local count; the submission-system count remains authoritative |
| Abstract | 143 tokens by the same local method | Below the 150-word Article limit, with little margin for later edits |
| Display items | Six numbered figures | At the stated six-item Article maximum |
| References | 14 numbered entries | Below the journal's usual 50-reference guidance |
| Claims and units | M2 uses paired training-seed blocks; M5 uses task seeds; DMP and V1 use 30 task-instance seeds per study/family; Fish1.5 is one specimen; outcomes are not pooled | The draft keeps inferential units separate and does not describe synthetic studies as biological validation |
| Supplementary record | Table S3 retains M2/M5; Table S4 reports DMP; Table S5 reports prospective V1; both protocols and verification records are linked | Substantive organization is present; source-to-claim and citation audits remain open |

These are document-level checks, not evidence of venue fit or an editorial decision. The word counts are local estimates, not a substitute for NMI's submission-system count.

## Scientific contribution decision

The project's internal full-scope venue-fit review classifies both NMI Article and Analysis as **NOT_READY**. The separate precedent audit finds high same-dataset/story overlap for Fish1.5, established prior art for connectome reservoir computing, and no demonstrated general connectome-to-AI advantage. The current draft now describes itself as a retrospective, evidence-bounded synthesis rather than a validated transfer theory.

The evidence supports narrower statements:

- The Fish1.5 positive recurrence–persistence association was not supported in 82 neurons from one specimen. The frozen topology-null test had 861 undefined results out of 1,000 and could not estimate its planned P value.
- The published worm result supports a bounded biological motor-state computation, while the project's planned animal-level reanalysis remains blocked by missing identity/stimulus alignment. M2's synthetic post-actuator sign input is not a test of the biological RIM→AIY signal.
- M2's exact realized-state input did not improve the tested controller under hidden reversals; the paired contrast favoured action-only input. This does not establish that the information is intrinsically harmful or unhelpful to an optimal controller.
- M5 shows that preserved input–target correspondence helped the tested local rule. Same-feature ridge and full-input replay had larger correspondence effects and lower aligned error. The ridge comparison is not capacity matched; the tested features were computed from complete trials; and the correspondence intervention changes both training and test pairing. The result therefore does not establish mechanism-specific temporal credit assignment or general transfer.
- The post-result DMP V1 module tested 30 task-instance seeds in each of delayed association, state estimation and contextual decision using a fast–slow model × context-correspondence design. No family passed the positive mechanism-specificity gate. Delayed association failed task viability; state-estimation interaction was negative (−0.00218; Holm-adjusted P = 0.05058); contextual-decision interaction was near zero (+0.00101; adjusted P = 0.77924). The protocol's small-data advantage gate passed only for contextual decision, but its full-data advantage was not detected and its longer-delay loss rose by 0.22096. These are synthetic, post-result project findings.
- The fast–slow architecture is not a novel contribution of this project: a dual-memory spiking architecture was published in *Nature Machine Intelligence* in 2026. The new experiment was inspired by that prior work and does not establish cortical validity, energy efficiency or general transfer.
- The new V1 package used synthetic orientation-channel responses and a figure/ground task; the source paper's released recordings were not analysed. The generic comparator was a linear contextual model, not a strong or capacity-matched neural network.
- In V1, the frozen AP interaction was +0.01603 under a broken-minus-aligned contrast (95% CI, +0.00815 to +0.02357), which is the opposite direction from the protocol narrative. Aligned selective pooling underperformed the global-pool control by 0.02208 AP (95% CI, 0.01664 to 0.02737); the positive specificity gate failed. This is retained with an explicit post-run sign-error amendment.
- M2, M5, DMP and V1 use different tasks and endpoints and cannot be pooled into a general transfer effect. V1's source/task package was selected after earlier project outcomes and overlaps the portfolio's visual modality; it does not create project-level preregistration or independent biological validation.

The central gap is scientific, not typographic: the current portfolio does not demonstrate that a specific biological mechanism provides an artificial advantage beyond generic alternatives, nor does it establish a broadly novel conclusion suitable for NMI. The draft must not be described as submission-ready or as evidence that biologically grounded methods generally improve AI.

## Future evidence that could change the decision

The DMP V1 and prospective V1 studies have now addressed mechanism-by-correspondence questions in synthetic tasks, but they did not close the contribution gap. The V1 run was a new mechanism/task package but not a project-level blind holdout, used a limited generic-comparator set for broad claims, and had a frozen contrast-sign wording error. This authorized pass is complete; it does not include another experiment. Any future research scope would need to resolve these limits rather than repeat or tune these packages. Relevant evidence characteristics would include:

1. an independent, prospective held-out evaluation tied to a clearly specified biological computation;
2. a design that separates mechanism-specific computation from information correspondence, including a mechanism-by-correspondence comparison where scientifically meaningful;
3. transfer to an independent task family or operating regime, rather than another seed set from the same generator;
4. fair generic controls matched on information, data, capacity, optimization opportunity and relevant compute, with the matching dimensions reported;
5. evidence for a consequential advantage, such as sample efficiency or robustness, measured with variation across tasks rather than only across seeds.

These are scientific characteristics, not formal NMI checklist requirements. The completed synthetic runs do not substitute for independent biological evidence if that is needed for the eventual claim. No further run or DMP rescue was performed in this pass.

## Open publication and provenance gates

- Human authors must approve author names, affiliations, contributions, funding, competing-interest declarations, and the final interpretation.
- The writing-assistance and figure-generation disclosure is drafted in the manuscript; the human authors must verify it against journal policy and approve the final wording.
- Dataset records identify published/released sources and listed licenses for the three cited datasets. This does not establish redistribution rights for every imported source file, code package, or historical experiment record.
- Selected source-file hashes are recorded in the repository, but the integrated manuscript does not yet have an owner-approved immutable source snapshot covering every selected claim. The publication-branch crosswalk still contains unresolved record relationships, including C08.
- Public source-to-claim attribution, exact source versions, and reuse permissions need a final item-level audit before any external release.

## Stop condition for this pass

The present pass may close when the internal article and supplement are consistent, the generated Word/PDF files have been visually checked, and the audit clearly states the scientific and provenance limits. That would complete an internal manuscript package; it would not change the **NOT_READY** venue decision. Reopening the experiment program requires a later explicit scope change.

## References used for this audit

- Internal full-project venue-fit decision: `nmi_feedback_routing/summery/PROJECT_FULL_SCOPE_VENUE_FIT_01/README.md`.
- Internal Fish1.5 and connectome precedent audit: `nmi_feedback_routing/results/experiment1/NMI_NOVELTY_PRECEDENT_AUDIT.md`.
- [NMI content types and Article limits](https://www.nature.com/natmachintell/content).
- [NMI initial formatting guidance](https://www.nature.com/natmachintell/submission-guidelines/initial-formatting).
- [NMI authorship and writing-assistance policy](https://www.nature.com/natmachintell/editorial-policies/authorship).
