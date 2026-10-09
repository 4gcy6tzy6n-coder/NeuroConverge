# Anatomy-versus-function re-test

`01_anatomy_vs_function.py` builds the anatomical matrices **by neuron name** from the tab-separated
source tables and contrasts connected against unconnected pairs. Writes `RESULT_corrected.json`.

**The files named `aconnectome_*.csv` are TAB-separated, not comma-separated.** A comma-delimited
reader yields one column and a `KeyError`.

`00_anatomy_vs_function_INVALID_idorder.py` and `RESULT_invalid_idorder.json` are **retained
deliberately and must not be used.** They assume `aconnectome_default.h5` is indexed by the
`funatlas.h5` neuron-id order. It is not: against the source tables, 1,756 of 1,891 witvliet chemical
edges and 209 of 300 electrical edges mismatch under that assumption. The invalid run produced
`Cohen's d = 4.74`, an implausibly large value that is itself evidence of the misalignment. **A silently
deleted wrong analysis cannot be audited; a retained one can.**

Inputs and their checksums are recorded in `../../wp1_data/WIRESHIFT_STAGE1_DATA_AUDIT.md` (wheel) and
`../../wp1_data/WIRESHIFT_STAGE2_WT_AUDIT.md` (functional export). No redistribution of the derived data
is made, because no licence permitting it was found.
