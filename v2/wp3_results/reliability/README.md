# Reliability audit — analysis scripts

Reproduces `../ATLAS_RELIABILITY_AUDIT.md`. Input: `exported_data.tar.gz` from OSF
`10.17605/OSF.IO/E2SYT`, sha256 `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9b3832f6ce836`,
extracted to a directory of `{i}_{ds_name,gcamp,labels,stim_neurons,stim_volume_i,t}.txt`.

Run order:

1. `01_reliability_zscored.py` — unique-name filter, per-event z-scoring, split-half reliability.
   Writes `RESULT_zscored.json`. **W2** (path to the extracted WT directory) is hard-coded at the top of
   each script and must be edited per machine.
2. `02_reliability_inclusion_filtered.py` — adds the source paper's inclusion rule, two
   operationalisations, and the unfiltered control. Writes `RESULT_inclusion_filtered.json`.

Both need only `numpy`. They do not modify the OSF files. Runtime is roughly 10 and 20 minutes
respectively on the audit machine because each of 113 animals is parsed with `np.loadtxt`.

## Three defects these scripts were written to correct

Recorded here because a silently fixed analysis cannot be audited, and all three changed numbers.

1. **Duplicate-name pooling.** Pairs keyed by `(target, recorded)` name pool physically distinct cells
   whenever a name repeats within one animal, which happens in 84 of 113 WT animals up to 75 times.
   Both scripts now restrict to uniquely-named cells.
2. **Ratio-of-medians.** An early variance decomposition took the median of per-pair between/within
   ratios and reported 0.977; the pooled computation gives 0.099. The median of ratios is not the ratio
   of medians. Only the pooled form is reported.
3. **A biased read-out statistic.** `max(post)` versus `mean(pre)` reported 94 per cent of events rising,
   but a random-column control rose 83 per cent. The fair version uses one statistic on both sides plus
   a per-event empirical null.

## Standing limitation

The scripts read a directory layout that the OSF archive provides; they do **not** download it. No
redistribution of the derived files is made, because no licence permitting it was found.
