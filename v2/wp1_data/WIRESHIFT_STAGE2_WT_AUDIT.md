# WIRESHIFT — STAGE 2 DATA AUDIT (WT export, authorised by the joint lead)

**Status: prospective. No model has been fitted and no prediction exists beyond the read-out checks
below, which are audits of the *data*, not of any hypothesis.** Every number was measured from files
downloaded and opened this session.

**Download authorised by the joint lead on 2026-10-09 for data audit only.** The joint lead's four
purposes, and one further instruction to record checksums, source, storage, parse failures and licence,
are each answered below.

---

## 0. Corrections to the previous report, adopted

**C1 -- terminology.** The previous report called `0.5061` at `n = 15` "the alpha floor". **The joint
lead's correction is right and is adopted:** under the normal approximation used, `0.5061` is the
standardised effect at which a two-sided `alpha = 0.05` test has **about 50 % power**. It is not a
"floor" in any stronger sense. `0.7234` is the value at **about 80 % power**.

**C2 -- the table does not generalise across designs.** The previous table was for a **single-group
paired** design, `d = (z_{1-alpha/2} + z_power)/sqrt(n)`. **If WireShift compares WT and `unc-31` as two
independent groups, that formula does not apply.** Recomputed this session:

| design | formula | `n = 15` per group: 50 % power | 80 % power | 95 % power |
| --- | --- | --- | --- | --- |
| **A: single-group paired** (the previous table) | `(z_{1-a/2}+z_p)/sqrt(n)` | 0.5061 | **0.7234** | 0.9308 |
| **B: two independent groups** | `(z_{1-a/2}+z_p)*sqrt(2/n_per)` | 0.7157 | **1.0230** | 1.3163 |
| **C: two groups + within-animal repeats**, design effect `DE = 1+(m-1)rho` | B `* sqrt(DE)` | -- | **1.0230 x sqrt(DE)** | -- |

**Design C, `rho = 0.5`:** `m = 5` gives `DE = 3.00` and `d = 1.7719`; `m = 20` gives `DE = 10.50` and
`d = 3.3149`. **Consequence: the choice of design moves the required effect by a factor of 1.4 to 4.6,
so the previous table must not be quoted for a two-group comparison.** No design has been fixed yet, so
**no one number is the current answer, and none is asserted here.**

---

## 1. Purpose 1 -- WT record count, unique animals, file structure

`exported_data.tar.gz`, **523,093,816 B, sha256
`d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9be3832f6ce836`, identical to the OSF metadata
hash.**

```
678 files · 113 unique integer prefixes (0..112) · 113/113 have the complete 6-file set
missing pieces: none · extra files: none · non-.txt files: none
```

> **The paper's `n = 113 animals` is now VERIFIED from the export, not taken on trust.** The previous
> report carried it as unverified; that caveat is closed.

**One acquisition per animal, in both cohorts:** `ds_name` is unique in **113/113** WT records and
**18/18** `unc-31` records, so **no animal is represented by two acquisition folders**. WT spans **51
acquisition dates**, the busiest being 20230314 with 6 animals; `unc-31` spans 8 dates.

## 2. Purpose 2 -- the F3 label-hygiene check, systematically

| quantity | WT (113 animals) | unc-31 (18 animals) |
| --- | --- | --- |
| columns | **14,379** | 2,158 |
| named cells | **8,541 (59.4 %)** | 1,204 (55.8 %) |
| coverage median / mean / range | **63.3 % / 59.6 % / [0.0 %, 90.1 %]** | 61.7 % / 54.1 % / [0.0 %, 77.3 %] |
| animals with **zero** labels | **1** (index 11) | **3** (0, 3, 4) |
| **bare numeric labels** | **39** | 0 |
| other non-name labels | `RMG?` x2, `smthng else`, `OLQV_`, `-`, `AIY?` | `--` |
| animals with duplicated names | **84 / 113** | 14 / 18 |
| duplicated-name instances, median / max | 5.5 / **75** | 4.5 / 32 |

**F3 is confirmed and generalises.** The bare numeric labels and the placeholder strings found in the
two-animal WT sample are **not** sample-specific: 39 bare numbers and five distinct malformed strings
appear across the 113 WT animals. **They are absent from `unc-31`**, which has exactly one malformed
string (`--`). **Whether this asymmetry is biological, pipeline-related, or an artefact of the two
exports' preparation is `UNKNOWN` and is NOT inferred here.**

**The `?` and `_` suffixes** (`RMG?`, `AIY?`, `OLQV_`) are recorded as **malformed rather than
silently accepted or silently dropped**; their intended meaning is `UNKNOWN`.

## 3. Purpose 3 -- strict usability, at the level the joint lead specified

**The joint lead directed: exclude cells that cannot be uniquely determined, or establish an
independent-source disambiguation rule; do not guess by column position.** Two candidate readings were
computed, because the difference is large and the choice is not mine to make.

**Reading X -- whole-animal strict** (animal counted only if it has NO duplicate and NO malformed
label): **WT 23 / 113, unc-31 1 / 18.** Under this reading the `unc-31` arm collapses.

**Reading Y -- cell-level strict** (each ambiguous *cell* excluded, the animal retained), which is what
the joint lead's wording describes:

| quantity | WT | unc-31 |
| --- | --- | --- |
| animals with at least one uniquely-named cell | **112 / 113** | **15 / 18** |
| uniquely-named cells | **7,520 / 14,379 (52.3 %)** | 1,060 / 2,158 (49.1 %) |
| uniquely-named cells per animal, median / range | **64** / [0, 104] | **66** / [0, 94] |
| distinct ambiguous names per animal, median / max | **1** / 10 | **1** / 3 |

> **Reading Y is the operative one and it is far more favourable: the median animal loses only ONE
> distinct name to ambiguity.** Reading X was an over-strict construction by this audit and is recorded
> only so the difference is visible.

**Two-group implication under Reading Y: 112 WT versus 15 `unc-31`, equivalent per-group `n = 26.5`,
and design B at 80 % power needs `d = 0.7703` before any within-animal inflation.** **That is a real but
demanding requirement, and it is not a claim that the study is powered.**

## 4. Purpose 4 -- sentinel meanings, index convention, repeat acquisitions

**The negative sentinels are resolved from the authors' own source code**, which is the
"independent-source disambiguation rule" the joint lead asked for. `github.com/leiferlab/pumpprobe`,
`pumpprobe/Fconn.py` and `pumpprobe/Funatlas.py`:

| sentinel | meaning | source line |
| --- | --- | --- |
| **`-1`** | **default / initial value**, i.e. no target assigned | `self.stim_neurons = -1*np.ones(n_stim, dtype=int)` (Fconn.py:69) |
| **`-2`** | **explicitly excluded**, the artefact "bubble" period | `inst.stim_neurons[bubble_stim:] = -2` (Fconn.py:131, 513); docstring *"are not considered"* (Funatlas.py:180) |
| **`-3`** | **manually flagged special case**, with a complementary label | `self.stim_neurons[m] = -3; self.stim_neurons_compl_labels[i] = ls[1]` (Fconn.py:571-572) |
| both `-1` and `-2` | treated together as "no valid stimulus" | `if inst.stim_neurons[ie] not in [-2,-1]:` (Fconn.py:504) |

**Observed distribution, consistent with those roles:** WT 5,808 stimulus values of which `-2` = 1008
(84 % of negatives), `-1` = 162, `-3` = 28; `-2` appears in 99/113 animals, `-1` in 38, `-3` in 8.
`unc-31`: 1,025 values, `-2` = 89 and `-1` = 86, **no `-3`**.

**Index convention: `0`-based, established by two independent lines of evidence.**

1. **Usage.** The value is used directly as a Python array index, e.g.
   `self.peak_time[selected, target_index_ref] = np.argmax(...)`. A 1-based value would be an
   off-by-one against every such use.
2. **Distribution.** `max(stim) == ncol - 1` in **22 WT and 2 `unc-31` animals**; `max(stim) == ncol`
   in **0 animals of either cohort**; `0` appears in **16/111 WT and 6/18 `unc-31` animals**; **no value
   ever exceeds `ncol - 1`.**

**Independent read-out check, performed because the index convention is load-bearing.** For 411
stimulus events across 8 WT animals, the same statistic (post-window mean minus pre-window mean) was
computed for the indexed column and for every other column at the same event:

* the indexed column sits at **median percentile 84.4 %** of its own event's column distribution, versus
  50 % under a null;
* it exceeds the 95th percentile in **13.4 %** of events, versus 5 % under a null, a **2.7-fold
  enrichment**;
* mean `z = 0.43`.

**Interpretation, stated carefully: the association is real but moderate.** Not every stimulus evokes a
detectable response in the targeted cell, which is precisely why the source paper states that a
measurement is included only if a stimulus event evokes a response in the stimulated neuron.

**A first version of this check was wrong and is recorded.** It compared `max(post window)` against
`mean(pre window)` and reported 94 % rising; **a random-column control rose 83 %**, exposing the
statistic itself as positively biased. The check above uses one statistic for both sides of the
comparison and a per-event empirical null. **The flawed version is not deleted, because a check that
was silently fixed cannot be audited.**

## 5. Provenance, storage, checksums, parse failures, licence

| item | value |
| --- | --- |
| source | OSF node `10.17605/OSF.IO/E2SYT`, file `exported_data.tar.gz`, URL `https://osf.io/download/9mecf/` |
| size | **523,093,816 B** |
| sha256 (measured) | `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9be3832f6ce836` |
| sha256 (OSF metadata) | `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9be3832f6ce836` -- **match** |
| also verified earlier | `exported_data_unc31.tar.gz` 84,924,311 B |
| **total downloaded this project** | **670.5 MB** (wheel 37.8 + raw 24.7 + unc31 84.9 + WT 523.1); **6.7 % of the Stage-2 10 GB budget** |
| parse failures | **none** in the structural pass: 678 files parsed, 113/113 and 18/18 animal sets complete. `nan` values inside `gcamp` are the file's own missing-value encoding, not parse failures, and were handled as such |
| licence | **the OSF node states no licence.** The Nature paper is not open-licensed for redistribution, and **no licence permitting redistribution of these derived files was found. `UNKNOWN`, consistent with the earlier finding. Analysis use is unaffected; redistribution is not authorised.** |

## 6. What this audit does NOT establish

* **No model has been fitted, no prediction exists, and no model fitting is authorised.**
* **It does not fix a design.** Readings X and Y, designs A/B/C, and every power number are options, not
  decisions.
* **It does not establish the `?`/`_`/`--` label semantics or the WT-versus-`unc-31` hygiene asymmetry's
  cause.** Both are `UNKNOWN`.
* **It does not license any biological claim** about `unc-31`, extrasynaptic signalling, or
  structure-function correspondence. Those are the source paper's results.
* **It does not establish novelty**, which remains the hard gate.

## 7. The hard gate: what mechanism hypothesis is not already covered?

The joint lead asks WireShift to name **one mechanism hypothesis that Randi and Creamer have not
tested, with independent predictive content, identifiable from the current animal-level data.**

**The honest position: this audit does not establish novelty, and it must not be read as doing so.**
What it can do is state the candidate precisely enough to be falsified, with its verification step
named.

**Prior art as established in this project:**

* **Randi et al. 2023** measured the atlas, compared WT with `unc-31`, showed propagation differs from
  anatomy, and attributed part of the difference to extrasynaptic signalling. **Descriptive and
  genotype-comparative.**
* **Creamer et al. 2026** fitted a connectome-constrained dynamical model, permuted node identity at
  fixed topology, worked across 110 animals, and reconstructed held-out neurons. **Predictive, but the
  held-out object is the RECORDED cell.**

**The candidate this audit can articulate, and only as a candidate:** *held-out STIMULATION TARGET
generalisation* -- **predict the response to a stimulation target that was never stimulated in that
animal, from stimulations of other targets in that animal and in other animals, conditioned on
genotype.** The held-out object there is the **perturbation**, not the recording, which is a different
estimand from Creamer's.

**Its status is `CANDIDATE, NOVELTY UNVERIFIED`, for three reasons stated rather than hidden:**

1. **Creamer's paper reports "reconstruct missing neurons" and a shuffled-connectome control; whether
   their held-out design also holds out the stimulated target was not verified**, because their methods
   were read at the level of the abstract, the methods excerpt quoted above and the repository README,
   not line by line.
2. **The `unc-31` arm has 15 usable animals against WT's 112**, so any genotype-conditioned comparison
   is severely unbalanced and the design-C inflation applies on top.
3. **The response signal is moderate** (`mean z = 0.43` on the read-out check), which limits how much
   predictive content any held-out-target task can carry at `dt = 0.5 s` calcium resolution.

> **Recommendation: do not start any model fitting on the strength of this audit.** The novelty
> candidate above needs (a) Creamer's held-out design read line by line, and (b) a decision on whether
> 15 versus 112 animals can carry a genotype comparison. **Until both are closed, the data gate is open
> and the science gate is not.**
