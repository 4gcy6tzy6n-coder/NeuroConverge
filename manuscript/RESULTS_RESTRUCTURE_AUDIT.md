# Four-Results rewrite: evidence and editorial audit

**Scope:** Results allocation and claim audit, updated 3 October 2026. No experiments changed or launched. `ARTICLE_DRAFT.md` now contains a complete internal manuscript draft; this file remains the audit trail for the four-section Results rewrite. The prior five-section Results are preserved in `archive/RESULTS_BEFORE_FOUR_SECTION_REWRITE.md`.

## One-sentence argument

The evaluated structural, source-data and synthetic cases separate biological evidence from artificial task utility: the structure assays did not establish their proposed advantage, execution-state access did not improve the tested AcRKN controller, and temporal correspondence helped the fixed local rule while generic alternatives performed better.

This is a case-based observation and methodological proposal. It does not establish necessary and sufficient transfer conditions, a general negative claim about biology, or NMI-level novelty. The existing evidence-bounded title is retained; “boundary conditions for neural transfer” would imply stronger validation than the portfolio provides.

## Paragraph map and evidence allocation

| Section | Main-text sequence and function | Evidence class | Supporting record | Relocated detail |
|---|---|---|---|---|
| R1 | M0 bounded comparison → Fish1.5 association → invalid null and specimen boundary | boundary; qualification | local `PHASE1_FALSIFICATION_REPORT.md`; Fish1.5 `FISH15_PRIMARY_RESULT.json` | SI S3: bootstrap valid draws, null constraints, post-result alternatives, source linkage |
| R2 | Published worm computation → blocked animal analysis → source-derived cerebellar readout and independent CF biology | source support; qualification | Ji 2021; worm schema report; M5 held-out source readout; Garcia-Garcia 2024; Silva 2024 | SI S2: historical readout details, unusable splits, alternative synthetic results |
| R3 | Synthetic construct and pairing → negative primary contrast → unresolved information-specific explanation → stronger references and scope | core result; necessary comparisons; qualification | M2 V1 captured contract, canonical summary and repeated-run comparison | SI S4: all conditions, full diagnostics, timing, hashes |
| R4 | Marginal-preserving correspondence design → viable task and positive primary contrast → stronger alternatives → feature/objective matching and train/test boundary | core result; necessary comparisons; qualification | M5 V1 contract, `primary_result.json`, `per_seed_metrics.csv`, post-run method audit | SI S5: secondary intervals, exact control definitions, comparator correction |

These studies have different outcomes and independent units. There is no pooled effect, meta-analysis, shared biological mechanism, or unified prospective design.

## Locked terminology

| Term | Definition and decision |
|---|---|
| realized-state input | exact sign of the preceding post-actuator displacement in M2 V1; not RIM→AIY premotor information |
| AcRKN | adapted action-conditional recurrent Kalman network cell; not a full reproduction of the original robotics model |
| training-seed block | M2 inferential unit; environment streams paired, closed-loop trajectories may diverge |
| task seed | M5 inferential unit; trials, regimes and arms are repeated observations |
| nMAE | interval mean absolute error divided by 27 bins; lower is better |
| correspondence effect | M5 nMAE(broken) − nMAE(aligned); positive favours alignment |
| feature matched | ridge and local rule share 16 temporal eligibility features; head capacity, objectives and fitting differ |
| neural transfer evidence map | retrospective proposal for Discussion; not a tested hierarchy or transfer law |

## Numerical sources and inference status

- **Fish1.5:** `/Users/yyl/Desktop/workshop/NMI/nmi_feedback_routing/results/experiment1/FISH15_PRIMARY_RESULT.json`, SHA-256 `c99569555ff2ef17844d7002914df5e29cbb3727169bb0caa04ee4a71bc09171`. Retrospective and partially informed; 82 neurons in one specimen; 9,844 valid bootstrap draws; frozen null invalid. No significant negative association or animal-population inference is claimed.
- **M0:** `/Users/yyl/Desktop/workshop/NMI/nmi_feedback_routing/PHASE1_FALSIFICATION_REPORT.md`, SHA-256 `84fda6bd0ab19f733e3be20581fed105d21405cca33fe7b29ac8a463e20dc3eb`. Comparator retains diagonal self-persistence; noise-floor crossover retained in main text. Canonical round-artifact linkage and full public package are incomplete.
- **Cerebellar source readout:** `/private/tmp/neuromech-m5-xor-v2-publish/data/results/M5_CEREBELLAR_CF_LTD_HELDOUT_READOUT_V1/session_summary.csv` and associated contract/report, pinned in `../reproducibility/SELECTED_ARTIFACTS.csv`. Counts independently recomputed as 15/16, 16/16 and ridge>CF 14/16. Held-out squared Pearson correlation, descriptive within-session inference; 78/80 usable splits. Not the distinct real-trial interval-decoding package. Exact Route-D V3 crosswalk remains unresolved.
- **M2 primary and diagnostic numbers:** `../new_experiments/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/runs/canonical_1/summary.json`. 32 paired training-seed blocks. Primary hidden action-only minus realized-state contrast and three diagnostic intervals reported in main text because they bound its interpretation. GRU/PF arm means are descriptive comparisons, not capacity-isolated tests. Revealed zero-crossing interval is not equivalence evidence. No causally identified information penalty.
- **M5 primary/comparators:** `../new_experiments/M5_CORRESPONDENCE_PRESERVED_TIMING_V1/results/primary_result.json` and `per_seed_metrics.csv`. 30 paired task seeds. Primary plus ridge/replay intervals retained; no-trace/shuffle full intervals in SI S5. The primary manipulation changes train and test pairing jointly; not an isolated credit-assignment or evaluation intervention.

Independent read-only review found no four-Results numerical/sign/unit errors and prompted three corrections: remove prospective-validation wording from SI, label the source-readout ridge as non-capacity-matched, and state exact V1 code identity in SI.

Primary citation links in the draft refer to the biological papers and original AcRKN method. Project reanalysis findings are attributed to project records, not to those papers. An independent source audit noted a wrong Cook 2019 journal label in the historical acquisition report; correct metadata are *Nature*, DOI 10.1038/s41586-019-1352-7. That historical file was not silently edited.

## Replacement and relocation log

- Replaced the earlier five Results with four evidence-bearing sections.
- Split the combined V1 section into separate M2 and M5 Results, retaining their distinct estimands.
- Relocated the old placement, CF-LTD interval, XOR and fixed-generator numerical text verbatim to SI S2; no historical finding was deleted from the record.
- Removed the standalone hierarchy Result; the Discussion now labels the evidence map as a proposed methodological synthesis.
- Corrected M2's biologically related information framing to post-actuator observability, and replaced recovery/equivalence language with explicit unresolved diagnostics.
- Retained M5's feature/objective mismatch in the main text; removed parameter-matched wording as an accepted description.
- Added M0's noise-floor crossover and source-readout squared-correlation limitation because both change interpretation.
- Updated the manuscript date and stale figure-export status. Five figure exports were subsequently regenerated from source data, visually inspected, and recorded in `../figures/FIGURE_EXPORT_MANIFEST.json`; ownership and redistribution review remain open.

## Repetition and length audit

Headings introduce bounded conclusions; the body demonstrates each with its separate evidence; Discussion synthesizes them without repeating full statistics. The evidence map is absent as an empirical Result. Word-count method and subsection counts are in `RESULTS_WORD_COUNTS.json`; the Results now contain approximately 1,590 words including headings and the scope preface (the count treats URL components as tokens).

## Remaining limits

The complete internal draft now includes study-level Methods, a revised Discussion, figure legends, availability statements, five source-linked figure exports and source-data tables. Remaining gates are final artifact freeze and source-to-claim reconciliation, reference/attribution review, rights/licensing, author-supplied end matter, and independent contribution/venue assessment. Local file hashes define V1 identity; a base commit alone does not identify all executed source bytes. These gaps do not call for new experiments. Human author review and writing-assistance disclosure remain necessary before any submission decision.
