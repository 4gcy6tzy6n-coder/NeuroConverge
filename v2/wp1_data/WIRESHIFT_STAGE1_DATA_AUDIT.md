# WIRESHIFT — STAGE 1 DATA AUDIT

**Status: prospective. No model has been fitted, no prediction made, no endpoint computed.** This
audits whether the lightweight resources contain the four things the joint lead's Stage-1 gate requires.
**Every number below was measured from files downloaded and opened this session.**

**Budget compliance:** Stage-1 download cap **500 MB**. **Used: 147.25 MB (29.4 %).**
`wormneuroatlas` wheel 37,760,635 B; OSF `raw_extracted_data` 24,722,663 B; OSF
`exported_data_unc31.tar.gz` 84,924,311 B. **No TB-scale download was attempted and no server was
rented.**

---

## 1. The gate question and its answer

> Does the lightweight data contain **response values, valid cell identity, stimulus information, and
> traceable animal-level statistical provenance**?

| required item | verdict | evidence |
| --- | --- | --- |
| **response values** | **YES** | `{i}_gcamp.txt`, real floats with explicit `nan` for missing; 89 to 160 columns per animal, 4454 timepoints in the sampled WT animal |
| **valid cell identity** | **PARTIAL -- 55.8 %** | `{i}_labels.txt`; **median coverage 61.7 %, mean 54.1 %, range 0.0 % to 77.3 %**; **3 of 18 animals have ZERO labels** |
| **stimulus information** | **YES** | `{i}_stim_neurons.txt` (which neuron) and `{i}_stim_volume_i.txt` (when); **every non-sentinel index is within the column count, 0 out of range** |
| **animal-level provenance** | **YES** | one record set per acquisition; `{i}_ds_name.txt` carries the acquisition path, e.g. `/projects/LEIFER/francesco/pumpprobe/AKSxneuropal/20210824/pumpprobe_20210824_104000/` |
| timestamps / sampling interval | **YES** | `{i}_t.txt`; `dt = 0.5 s` **exactly** (0.0, 0.5, 1.0, ...) |

> **Verdict: `DATA_GATE_OPEN_WITH_CONSTRAINTS`.** The records are **not** cross-animal aggregates, so
> **animal-level train, test and inference are constructible**. Identity is the binding constraint, not
> availability.

## 2. What was read, and how

**Resource A -- `wormneuroatlas` 0.0.7.3** (PyPI, home `github.com/francescorandi/wormneuroatlas`,
author **Francesco Randi**). Wheel downloaded, **extracted as a zip and inspected without installing
it** (ponytail: a wheel is a zip; no environment was modified). 45 entries, 108.2 MB unpacked.

**The functional atlas inside is `wormneuroatlas/data/funatlas.h5`, 18,266,176 B:**

```
neuron_ids           (300,)  |S5        # 300 names, e.g. ADAL ADAR ADEL ADER ADFL ADFR ADLL ADLR
wt / unc31:
    dFF        (300, 300) float64    # aggregated pair response
    dFF_all    (300, 300) object     # RAGGED per-pair replicate list
    kernels    (300, 300) object
    occ1       (300, 300) int64      # source comment: "occurrence matrix: each entry is the length of dFF_all[i,j]"
    q, q_eq    (300, 300) float64
    q_eq_th    ()          float64   # 1.2
```

**MEASURED: `funatlas.h5` has NO ANIMAL DIMENSION.** `occ1` counts **repeated measurements of a pair**,
not animals. WT: 25,345 of 90,000 pairs non-zero, **median 3 and up to 59 replicates**, 130,682
measurements total. unc-31: 10,588 non-zero pairs, median 1, up to 11, 20,849 measurements.

**Consequence, stated plainly: the 300 x 300 atlas is the wrong object for animal-level inference, and
`dFF_all`'s replicates cannot be treated as independent biological samples even though they are
preserved.** This is exactly the trap the joint lead named.

**Resource B -- the OSF repository.** The Randi et al. data availability statement (PMC10632145) names
**`10.17605/OSF.IO/E2SYT`**, "Neural signal propagation atlas of C. elegans", public, created
2022-07-12. Its `raw_extracted_data/` folder and the mutant export were downloaded.

## 3. The per-animal record structure, verified at 18 animals

`exported_data_unc31.tar.gz` contains **109 entries with 18 `gcamp` files, i.e. 18 animals**, matching
the paper's own `(n = 18 animals)` for the mutant. **Every one of the 18 animals has the complete set**
of `ds_name`, `gcamp`, `labels`, `stim_neurons`, `stim_volume_i` and `t` -- **18/18, no missing piece.**

**Identity coverage, measured per animal:**

| animal | columns | named | coverage | duplicate names |
| --- | --- | --- | --- | --- |
| 0 | 91 | 0 | **0.0 %** | -- |
| 1 | 126 | 78 | 61.9 % | 1 |
| 2 | 89 | 60 | 67.4 % | 0 |
| 3 | 82 | 0 | **0.0 %** | -- |
| 4 | 118 | 0 | **0.0 %** | -- |
| 5 | 100 | 72 | 72.0 % | 1 |
| 6 | 116 | 67 | 57.8 % | 3 |
| 7 | 107 | 82 | 76.6 % | **20** |
| 8 | 134 | 100 | 74.6 % | 5 |
| 9 | 110 | 85 | 77.3 % | 2 |
| 10 | 150 | 89 | 59.3 % | 7 |
| 11 | 135 | 83 | 61.5 % | 2 |
| 12 | 131 | 77 | 58.8 % | 9 |
| 13 | 148 | 83 | 56.1 % | **20** |
| 14 | 160 | 108 | 67.5 % | **32** |
| 15 | 111 | 75 | 67.6 % | 4 |
| 16 | 135 | 84 | 62.2 % | **18** |
| 17 | 115 | 61 | 53.0 % | 2 |

**Totals: 2158 columns, 1204 named, 55.8 %.**

## 4. Three findings that actually constrain the design

**F1 -- three animals are completely unlabelled.** Animals **0, 3 and 4** have **zero** nameable cells.
**The usable animal count for any identity-dependent analysis is 15 of 18, not 18.** This must enter any
sample-size statement.

**F2 -- duplicate names break the 1:1 identity premise.** Animal **14** has 108 names but only **76
unique**, i.e. **32 duplicates**; animals 7 and 13 have **20** each. **A repeated name in one recording
means the label file does not resolve which column is which cell**, so a position-based identity
assignment would be a *choice*, not a measurement. **Any v2-style identity-dependent design must either
drop the duplicated cells or record the assignment rule as an assumption.**

**F3 -- the WT `raw_extracted_data` two-animal sample carries junk labels that the mutant export does
not.** The sampled WT animal has **48.2 %** coverage, and among its non-empty labels are **four bare
numbers (`41`, `48`, `48`, `21`) and one placeholder string (`smthng else`)**. The mutant export
contains none of these (its only oddity is `--`). **This is a WT-side label-hygiene problem and it is
recorded as such**; it may or may not generalise to all 113 WT animals, which was **not** verified
because the WT export exceeds the Stage-1 cap.

## 5. Sentinels and units, documented rather than guessed

* **Missing-value sentinel in `stim_neurons`:** negative integers. Observed `-1`, `-2`, `-3`. **The
  meaning of the distinction between them is `UNKNOWN`** and must be established before use; treating
  all negatives as "no stimulus" is an assumption, not a reading.
* **Indices are 1-based or 0-based: `UNKNOWN`.** All non-negative values fall inside the column count,
  which is consistent with either convention, so the range check does **not** disambiguate it.
* **Time base `dt = 0.5 s`** is read directly from `t` and is unambiguous.

## 6. Budget accounting and what is still needed

| resource | size | status |
| --- | --- | --- |
| `wormneuroatlas` wheel | 37,760,635 B | **downloaded** |
| OSF `raw_extracted_data/` (WT, 2 animals) | 24,722,663 B | **downloaded** |
| OSF `exported_data_unc31.tar.gz` (18 animals) | 84,924,311 B | **downloaded** |
| **Stage-1 total** | **147,407,609 B = 147.4 MB** | **29.4 % of the 500 MB cap** |
| OSF `exported_data.tar.gz` (WT subset) | 523,093,816 B | **NOT downloaded -- over the Stage-1 cap** |
| OSF `exported_data_full.tar.gz` (WT full) | 1,143,920,663 B | **NOT downloaded** |
| OSF total repository | ~2.73 GB | **within the 10 GB Stage-2 cap** |
| DANDI 001075 (raw imaging) | ~4.1 TB | **not used, per the joint lead** |

**The WT animal count (paper: `n = 113`) was NOT verified from the export**, because the 523 MB file
exceeds Stage 1's cap. **It is taken from the paper's own text and labelled as such.**

## 7. What this audit does NOT establish

* **No model has been fitted and no prediction exists.** This is a data audit.
* **It does not establish that the identity coverage is sufficient for any particular design.** 55.8 %
  named, 15 of 18 animals usable, and up to 32 duplicates in one animal are the numbers; whether they
  support the intended analysis has not been assessed.
* **It does not establish the meanings of the sentinels or the index base.** Both are `UNKNOWN`.
* **It does not verify the WT side at scale.** Only 2 WT animals were read, within budget.
* **It does not license any claim about `unc-31` biology**, extrasynaptic signalling, or the
  structure-function relation. Those are the source paper's results, not this project's.

## 8. Recommendation to the joint lead

**The Stage-1 gate is satisfied with named constraints, and Stage 2 is affordable:** the whole OSF
repository is ~2.73 GB, far inside the 10 GB cap, so **no TB-scale purchase and no rented server are
required.**

**But two things should be decided before Stage 2 begins, because they change what is possible:**

1. **Whether a design can proceed at ~55.8 % identity coverage with 15 usable animals**, given that this
   project has already established that pairs and frames are not independent replicates. **The power
   table has now been recomputed rather than deferred**, paired design, two-sided `alpha = 0.05`,
   `d = (z_{1-alpha/2} + z_power)/sqrt(n)`:

   | animals `n` | 50 % power (alpha floor) | 80 % power | 95 % power |
   | --- | --- | --- | --- |
   | **21** (the earlier NeuroConverge figure, for comparison) | 0.4277 | 0.6114 | 0.7866 |
   | **18** (all unc-31 animals, if the 3 unlabelled ones could be used) | 0.4620 | 0.6603 | 0.8497 |
   | **15** (unc-31 animals actually usable, F1) | **0.5061** | **0.7234** | 0.9308 |

   **Consequence: losing the three unlabelled animals costs real power.** The detectable standardised
   effect at 80 % power rises from **0.6603 to 0.7234**, an increase of about **9.6 %**. **And note what
   the unit of `n` is here: the animal, not the pair.** The 23,433 or 25,345 measured pairs do **not**
   enter this table and must not, which is the joint lead's own warning and the reason the aggregated
   `funatlas.h5` cannot be used for this purpose.
2. **Whether the WT export (523 MB) may be downloaded**, which would exceed the Stage-1 cap but sit far
   inside the Stage-2 cap of 10 GB. **This is the only way to verify the 113-animal claim and the
   label-hygiene finding F3 at scale.**

**And the governing novelty question from the previous round is untouched by this audit.** Nothing here
shows that a WireShift design is novel; it shows that its data are light, animal-resolved, and
partially identified. **Novelty remains the admission gate, as the joint lead directed.**
