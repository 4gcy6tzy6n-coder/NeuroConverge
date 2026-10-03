# Post-run interpretation amendment 01

**Recorded:** 2026-10-01, after the single frozen run completed. This is a transparent interpretation correction; no outcomes, code, seeds, arms, protocol, or verifier were changed and no rerun was performed.

The original contract calls `GENERIC_MATCHED_RBF` a “parameter-matched generic comparator.” Inspection of the frozen runner shows that `CF_TIMED_LOCAL` uses a 16-feature RBF encoder with a 28-way linear softmax readout, while `GENERIC_MATCHED_RBF` fits a ridge readout on the same 16 RBF features plus bias. The temporal feature representation is matched, but the trainable/output parameterization and learning procedure are not strictly parameter matched. Therefore:

- Interpret it as a **same-feature generic ridge comparator**, not a parameter-matched architecture control.
- The observed difference between correspondence effects does not establish equivalence, superiority, or specificity under capacity-matched learning.
- `EXACT_REPLAY_REFERENCE` additionally uses the full 40-bin input, so it is explicitly a higher-information/memory reference.
- Preserve `CONTRACT.md` and its pre-run hash unchanged; cite this amendment wherever that comparator is described.

The primary within-arm, paired-seed CF_TIMED_LOCAL contrast and task-viability gate are unaffected by this nomenclature/control-matching issue. The tested synthetic effect remains bounded to the fixed generator and implementation.
