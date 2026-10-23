# Calibration first-coder pass: the five workspace projects on the audit sheet

**Status: FIRST CODER PASS, author-coded, 2026-10-18.** Per the frozen protocol section 8, calibration is
dual-coded; this is coder 1's sheet. It is NOT the calibration verdict: until the second, non-author coder
(P4, owner-named) codes the same objects independently, these grades are a draft whose only binding use is
that any second-coder divergence of more than one grade step on any transition flags the instrument's wording
for revision. These rows are excluded from every statistic of protocol section 6.

The audited object is each project's **headline claim as its own record states it** - not a claim invented for
this exercise. Provenance points at the archive artifact; the known-input column states what the archive's own
verdict says the grade must not exceed, which is the instrument-validity requirement of protocol section 8.

## Sheet

### C01 NeuroMotif - "connectome-derived structure improves task-relevant dynamics"

| transition | grade | justification (from the record) |
| --- | --- | --- |
| T1 | E1 | Fish1.5 single-specimen structure-activity correlation measured and failed (rho = -0.1096; NeuroConverge `evidence/CLAIM_EVIDENCE_MATRIX.csv` row for Fish1.5) |
| T2 | E1 | reservoir instantiation with a stated structure-to-model mapping; no controlled variation of the mapping |
| T3 | **E0** | M0 full-connectome reservoir showed no advantage on any task line; the topology null was non-instantiable (861/1000 nulls undefined) - no controlled attribution of any gain to the correspondence exists |
| T4 | E0 | no task family beyond the demonstrated ones; paradigm retired before generality was tested |
| T5 | mismatch | the project itself withdrew to an evidence-boundary report (Route D): the claimed scope exceeds the evidence's scope by the project's own record |

Known input: paradigm RETIRED, zero historical positives. The instrument must not grade T3 above E1.

### C02 NeuroMech - "biological computation mechanisms transfer as usable inductive biases"

| transition | grade | justification |
| --- | --- | --- |
| T1 | E2 | per-mechanism biological evidence cited to specific sources (RIM state feedback, CF-LTD timing) in the mechanism registry |
| T2 | E1 | model-level correspondences stated per mechanism; M-series modules |
| T3 | **E1** | the claim-evidence ledger records limited synthesis-transfer evidence per mechanism with no selective advantage established at population scale; three task lines failed in three different ways (`PROJECT_DECISION_2.md`) |
| T4 | E0 | single-family demonstrations; no cross-family survival |
| T5 | corrected | the active manuscript is the scope correction itself (claims reduced to boundaries) |

Known input: RETIRED to Route D. T3 must not exceed E1.

### C03 MICA - "selective adaptation under mechanism uncertainty improves later decisions at matched budgets"

| transition | grade | justification |
| --- | --- | --- |
| T1 | E2 | the question's biological-mechanism content is thin by design (O/D/R factorization is formal, not anatomical); what T1 asks is answered by the environment contract, not by biology - recorded as a property, and graded E2 only for the formal object |
| T2 | E2 | the correspondence is the count-refit module structure, stated and controlled |
| T3 | **E2** | controlled evidence exists and is negative-at-the-bar: per-node sign structure SB1/SB2 MET at the frozen bar (`A_62B_BENEFIT_SIGN_CONTROLS.csv`), fair-budget separation total (`A_62C_FAIR_BUDGET_COMPARISON.csv`), but the cell-level bar (VB1/FC1) never met, and the boundary is closed from four sides (passive statistics: `71_`; lived probe: `72_`; free channel: `73_`) |
| T4 | E1 | one frozen family (EX1-v3); the CARL and Pendulum lines closed under their own stop rules without establishing generality (67D) |
| T5 | match | the record states the result family-scoped and negative-accepted; no broader claim is carried |

Known input: NEGATIVE_ACCEPTED, family-scoped (`69_` section 63). T3 at E2 with the negative reading is the
grade to reproduce; a second coder grading E0 or E3 flags the wording.

Dated amendment 2026-10-18 (evening): iteration 4 of the method loop landed the arc's first MET criterion
(`74_`, `A_KB_QUERY_PACKET.csv`): an 8-16 bit query packet at the late window converts up to 87.5 percent of
the privileged reference at (O+R, step 4), crossing the inherited bar, while mid-window cells stay under it.
The C03 row's grade stands at E2 - controlled evidence, negative at the cell level - but the justification
now reads "controlled, negative-at-the-bar overall, with a characterized working regime (late-window,
reward-change, packet-fed)" - the strongest honest statement of what the archive holds. The purchase-timing
rule that would test self-activation is proposed, not run (`75_`).

### C04 IRCN (CBCC line) - "budgeted selective computation improves over matched baselines"

| transition | grade | justification |
| --- | --- | --- |
| T1 | E2 | the mechanism is formal (selective computation under budget), defined and controlled in the contracts |
| T2 | E2 | implementation verified against frozen contracts (v0.3.4i: 96/96 calibration, 240/240 confirmation) |
| T3 | **E0** | the comparison contract was non-instantiable (no eligible baseline existed), and the G2 confirmatory comparison on 112 sealed seeds failed in both task families; the line is closed by its own decision record (`DECISION_v0.10.0.md`) |
| T4 | E0 | confirmatory failure precedes any generality test |
| T5 | match | the decision record states no advantage, no novelty, line closed |

Known input: confirmed negative on sealed seeds. T3 must not exceed E0.

### C05 BioMemory - "compartment-constrained associative memory avoids acting on wrongly recovered memory"

| transition | grade | justification |
| --- | --- | --- |
| T1 | E2 | larval MB source audited (`02_SOURCE_AUDIT.md`, PASS_QUALIFIED) with direction and cell identity |
| T2 | E1 | compartment-constrained memory model with a stated mapping; matched-null degeneracy blocks the structure-specific control (Eichler blocks NULL_DEGENERATE) |
| T3 | **E1** | B-EX0 measured the misleading-reminder cost (the only class where memory is worse than no memory) and retrieval dominance; utility (B-U) not yet established, B-G0 novelty unsigned, exploratory phase |
| T4 | E0 | single analytical substrate; no transfer tested |
| T5 | match | the contract's three evidence classes are kept separate; no cross-class claim is carried |

Known input: exploratory, negatives retained, B-G0 unsigned. T3 must not exceed E1.

## Summary and the validity requirement

| project | T1 | T2 | T3 | T4 | T5 |
| --- | --- | --- | --- | --- | --- |
| C01 NeuroMotif | E1 | E1 | E0 | E0 | mismatch |
| C02 NeuroMech | E2 | E1 | E1 | E0 | corrected |
| C03 MICA | E2 | E2 | E2 (negative-at-the-bar) | E1 | match |
| C04 IRCN | E2 | E2 | E0 | E0 | match |
| C05 BioMemory | E2 | E1 | E1 | E0 | match |

The pattern the field corpus will be read against: in all five known inputs, the headline transition T3 sits at
E0-E2 - controlled evidence exists in two of five, converts to a demonstrated advantage in none. If the field
corpus lands markedly higher on T3, that contrast is itself a finding (the workspace may select harder
questions than the field); if it lands the same, the boundary structure is generic. Both readings are
publishable; neither is assumed.

Owed: the second coder's independent pass on this same sheet (P4), after which the disagreement rate is
computed per protocol section 5 and this file's draft status is lifted or the wording revised.

## Dated amendment 2026-10-23: the MICA method-loop chain is complete

This amendment records two events of 2026-10-18 that postdate the C03 amendment above; it changes no grade.

1. **The purchase-timing rule was run, not left proposed.** The C03 amendment's closing sentence is
   superseded on that one point. Under the owner approval recorded in `75_KB_TIMING_RULE_PROPOSAL.md`,
   `A_TR_TIMING_RULE.csv` (64 rows, exact enumeration, zero fitted parameters) returns **TR1 NOT MET and
   TR2 HOLDS**: the declared rule fires only at the last step (firing mass 0.012-0.042), where the packet
   is worth nothing (deltas -0.000002 to -0.000043 per step), because the frozen SE gate opens only at
   step 5 and the step-4 window that converts 87.5 percent of the privileged value is never reached. The
   never-buy control equals no-update exactly, and always-at-step-4 reproduces iteration 4's committed
   fixed-step numbers to 1e-9.
2. **The chain is consolidated.** `76_METHOD_LOOP_TERMINAL_RECORD.md` records the six chained
   measurements and their hard cross-checks: KB1 is the arc's only MET criterion; passive statistics cannot
   sign or time the purchase (iterations 1 and 5), a lived probe costs 1.3-25 times what it delivers (2), a
   single free readout is conversion-limited at +0.0192 per step (3), and mid-window budgets saturate at
   18-26 percent of the privileged reference (4). The boundary is joint in budget and timing, and the named
   missing piece is an in-window change-timing detector.

C03's T3 grade remains E2 with the negative-at-the-bar reading; its justification now reads "controlled,
negative-at-the-bar overall, with a characterized working regime and a measured timing boundary". This is
still coder 1, author-coded. The rows remain excluded from every statistic of protocol section 6, and the
second non-author coder (P4) remains owed.
