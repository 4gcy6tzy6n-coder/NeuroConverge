# Execution incident 01

- First invocation time: after `PRE_RUN_FREEZE.json` was created.
- Failure point: the first seed, before the seed completed and before any result file was written.
- Cause: the runtime is Python 3.9.6, which does not support the Python 3.10 `strict` keyword to `zip`.
- Observed outcome data: none. The process raised `TypeError` before creating a metric row or writing an output file.
- Changes permitted for retry: remove the two `strict=True` keyword arguments and direct the runner to the amendment freeze file. No numerical operation, task parameter, seed, arm, metric, gate, decision rule, or analysis changed.
- Output handling: the empty `results/` directory from the failed invocation was removed before retry. The runner continues to refuse overwriting any non-empty result directory.

The original freeze file is retained. `PRE_RUN_FREEZE_AMENDMENT_01.json` records the revised code hash before retry.
