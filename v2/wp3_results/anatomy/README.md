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

## Later scripts

* `04_timecourse.py` -- empirical post-stimulus time course, and the measurement that the response
  peaks at 10 s against a 500 ms stimulus. Writes `RESULT_timecourse.json`.
* `06_common_mode.py` -- subtracts the across-cell mean at each timepoint (the global common mode) and
  reports raw against corrected. Writes `RESULT_common_mode.json`.
* `05_common_mode_INVALID_percellnorm.py` -- **RETAINED, DO NOT USE.** It normalised by a per-cell
  pre-stimulus SD computed over only 8 volumes; for near-constant or mostly-missing cells that SD is
  near zero and the result blows up to order 1e11. **This is the sixth self-found defect in this line.**
  The stable normalisation is the event's across-cell SD, used by `01`-`04` and `06`.

**Protocol facts needed to read any of these** (from the source Methods, PMC10632145): the stimulus is
**500 ms** for WT and **300 ms** for `unc-31`; the source excludes events that do not meet its thresholds
for a **contiguous 4 s**; and the inter-stimulus interval is **31.0 s median**, measured from all 113
`stim_volume_i` files.
