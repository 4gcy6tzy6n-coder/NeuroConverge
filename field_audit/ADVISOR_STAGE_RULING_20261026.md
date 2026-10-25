# Advisor stage ruling record (2026-10-25 late, recorded 2026-10-26)

The advisor's stage decision, relayed verbatim by the lead and recorded here as the governing
gate state. Declaring documents unedited.

## The ruling (dispositions)

1. O-6 "VERIFIED WITH FINDINGS" accepted as the reported technical verification result; the fix
   merge accepted. The submission gate is NOT declared fully closed.
2. The round's most important progress is named: the clean-clone review found and fixed the
   substantive defect that the bound scorer and its tests had never entered version control -
   uncaught, the manuscript's end-to-end reproducibility claim would not have stood.
3. The 51/58 -> 52/58 headline-agreement correction is a mandatory public record (statistical
   implementation erratum). It does not change T2/T3 E2 counts, but the two headline tie rules
   are not yet unified and must not be ignored on the grounds that core conclusions are
   unchanged. **F4 is upgraded to a pre-submission must-close**: formally designate the single
   canonical tie rule, disclose the C077 difference, and make the submission manuscript, results
   tables and reproduction scripts consistent under that rule. Historical results may be
   retained; two computations may not both claim canonical status.
   -> **Executed 2026-10-26:** `F4_TIE_RULE_DESIGNATION_20261026.md` (canonical rule = weaker
   merged grade first, ties to T3 preference then coder A; C077 disclosed; canonical primary map
   16 x T3, historical 15 x T3 + 1 x T2, E2 counts invariant) with the passing verification
   script `verify_tie_rule_canonicality_20261026.py`.
4. The project has entered the final human-responsibility confirmation stage - not a stage for
   more algorithm experiments.

## The gate table (as ruled)

| item | ruling |
| --- | --- |
| O-5 human coding data | received; hashes checked; awaiting real annotator + lead signatures |
| O-6 AI non-author verification | VERIFIED WITH FINDINGS; nine load-bearing numbers unchanged |
| F1-F5 fixes | accepted as recorded; F4 rule consistency must be confirmed pre-submission (now executed, above) |
| O-6 third-party human counter-sign | **BLOCKED - awaiting a qualified independent verifier** |
| Advisor final gate | awaiting the signature package, the verification package, and the manuscript decision points, all complete |
| NMI Article | remains the first submission target; **NOT authorized to be marked SUBMISSION_READY** |

## Counter-signature requirements (as ruled)

- Signer: a third researcher uninvolved in the project and uninvolved in producing the coding
  sheets. Yang may sign the O-5 coding work but NOT the O-6 verification of that work. The lead
  signs only what the lead has personally reviewed.
- The signer personally executes the six checks, retains raw outputs and findings, and does not
  sign from reading the AI report alone.
  -> Added verbatim to `O6_HUMAN_COUNTERSIGN_REQUEST_20261025.md` (addendum), with the F4
  verification script added as a seventh check.

## The three science-expression questions (advisor's final confirmation, after counter-sign)

1. Is the composition contrast described accurately?
2. Does the headline interval avoid over-generalization?
3. Is the human coder's identity and scope of participation adequately disclosed?

## Remote-visibility note

The advisor checked the remote NeuroConverge repository and could not find merge commit
`3e27c30` or the O-6 counter-sign files - local main was 49 commits ahead of origin. Local
verification is not negated, but the advisor cannot independently certify the latest local
worktree and merge state until it is pushed. Push executed 2026-10-26 (see the gate log below).

## Decision

**Approved to enter the final human counter-signature stage. NOT approved to skip that stage
and submit.** The questions that now decide NMI submission quality are no longer whether the
experiments suffice, but whether the measurements reproduce under an independent researcher,
whether research responsibility is genuinely confirmed, and whether the final manuscript's
claims match the evidence exactly.
