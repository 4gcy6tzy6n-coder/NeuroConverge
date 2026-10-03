# Post-run method audit

The frozen contract calls `GENERIC_MATCHED_RBF` “parameter-matched.” Inspection after the successful run showed that this wording is too strong.

- It is feature matched: both `CF_TIMED_LOCAL` and `GENERIC_MATCHED_RBF` use the identical 16-unit temporal RBF encoder plus bias.
- It is not output-parameter-count matched: the CF arm fits a 28-class softmax matrix (17 × 28 parameters), whereas generic RBF fits one scalar ridge head (17 parameters).
- This is a wording/design limitation, not a code deviation. The implementation was run exactly as frozen and is not changed after outcome inspection.

The comparator still answers whether a generic learner can exploit the same temporal representation, and it did so more effectively with a smaller output head. It cannot isolate learning-rule differences from output-objective differences. Any future strict parameter-matched comparison would require a separately identified, explicitly outcome-informed experiment; none is opened here.
