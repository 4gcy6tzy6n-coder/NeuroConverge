# M5 correspondence-preserved timing v1

This directory is a self-contained, audited synthetic experiment testing whether trial-level temporal input–target correspondence changes the value of a fixed M5 source-inspired learning rule.

- `CONTRACT.md`: frozen scientific and statistical contract.
- `PRE_RUN_FREEZE.json`: original pre-run hashes.
- `EXECUTION_INCIDENT_01.md`: pre-outcome Python compatibility failure.
- `PRE_RUN_FREEZE_AMENDMENT_01.json`: syntax-only refreeze used by the successful run.
- `run_experiment.py`: standalone deterministic simulation and analysis.
- `verify_results.py`: independent provenance, completeness, finite-value, and arithmetic checks.
- `RESULTS.md`: bounded result narrative.
- `RUNTIME_NOTE.md`: retained NumPy/Accelerate warning audit.
- `POSTRUN_METHOD_AUDIT.md`: post-run correction that RBF matching is at the encoder, not output parameter-count, level.
- `results/per_seed_metrics.csv`: every seed × regime × arm metric.
- `results/per_seed_correspondence_effects.csv`: every paired seed × arm effect.
- `results/primary_result.json`: gate, estimates, intervals, and frozen decision.
- `results/run_manifest.json`: parameters, environment, and output hashes.
- `results/POSTRUN_VERIFICATION.json`: independent verification status.

Re-running `run_experiment.py` in this populated directory is intentionally refused. The result is a synthetic post-hoc project extension and carries no biological-validation claim.
