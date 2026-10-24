# Supplementary Information: the framework exercised on known inputs (draft skeleton, 2026-10-24)

**Role per the 2026-10-23 review decision:** the method arc and the five-project calibration are
Supplementary material - they demonstrate that the audit framework detects evidence boundaries it was not
tuned on; they are NOT an independent confirmation of any field-level proportion and carry no weight in the
main text's claims. All numbers below are measured, committed facts (MICA archive, commits `c228e9b`..
`76b42c8`); nothing here is re-measured.

## SI Note 1: five workspace projects as known inputs (calibration)

Five projects in this workspace made bio-to-AI or adaptation claims and measured their own boundaries. Coded
on the same sheet (first-coder pass, awaiting the second coder), their headline-transition grades are:
NeuroMotif T3=E0 (paradigm retired, zero historical positives); IRCN-CBCC T3=E0 (confirmatory failure on 112
sealed seeds); NeuroMech T3=E1 (paradigm retired to an evidence-boundary report); BioMemory T3=E1
(exploratory, negatives retained); MICA T3=E2-negative-at-the-bar (controlled evidence, never clearing the
frozen cell-level bar). The instrument must reproduce these known grades - if it graded any of them E3+, it
would be defective. This is the calibration contract: known inputs, known outputs, instrument validated
against them.

## SI Note 2: the adaptation-value arc (one frozen family, six chained measurements)

On a frozen four-state POMDP family (EX1-v3, horizon 6) with a resource-bounded agent, six chained
measurements bracket when adaptation is worth attempting - each with criteria frozen before its run and hard
cross-checks binding it to its neighbours:

1. **Reachability** (`A_62A_UPDATE_REACHABILITY`): parameter updates can change actions (16 cells) but carry
   0.729 of weight against 48.730 for Q-moved-but-argmax-stable; the chain breaks between Q and the action,
   not between parameters and Q (values-unchanged never occurs).
2. **Sign structure** (`A_62B_BENEFIT_SIGN_CONTROLS`): beneficial updates exist per node (22 cells, best
   +0.0812/step) and harm exists in exactly one place - updating when nothing changed (-0.0218/step).
3. **Passive estimability** (`A_SE_SIGN_ESTIMABILITY`): a frozen likelihood-ratio gate reaches 0.967
   accuracy against a 0.972 abstain baseline - recall zero where updating helps; the change statistic sits at
   0.1-1.7 in-window against a threshold of 4. Passive statistics cannot time or sign the purchase.
4. **The lived probe** (`A_PB_PROBE_UPDATE`): generating the missing observation by acting delivers +0.0205
   at exactly one cell but costs -0.016 to -0.114 per step - priced out 1.3-25x.
5. **The free readout** (`A_BC_BREAKEVEN_CHANNEL`): even a free, perfectly targeted single readout is worth
   at most +0.0192/step (negative in 30 of 48 cells) against a privileged headroom of +0.0747 - the
   conversion limit of one datum through a count refit.
6. **Budget and timing** (`A_KB_QUERY_PACKET`, `A_TR_TIMING_RULE`): an 8-16 bit query packet at the late
   window converts 87.5 percent of privileged value (the arc's only criterion met); the same purchase timed
   by the agent's own gate fires only at the last step, where it is worthless. The working regime exists and
   is not self-activatable.

**What this arc contributes to the main text:** a worked demonstration that the audit's distinction between
delegated foundations, controlled utility and asserted correspondence has teeth - when the same laboratory
turned its own instruments on its own adaptation claims, every positive result arrived with the boundary
conditions named and the failure modes measured. The arc is family-scoped ("no known blocking or major
defect remains within the reviewed scope" is the strongest honest claim) and is presented as method
demonstration, not as evidence about the field.

## SI Note 3: instrument chain (provenance)

[Slot: the full commit/artifact chain - frozen protocol, dated amendments, binding records with hashes,
review records, the recompute STEPS - one table for the reproducibility statement.]
