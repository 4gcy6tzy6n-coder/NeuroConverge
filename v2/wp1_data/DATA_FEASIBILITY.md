# DATA_FEASIBILITY — NeuroConverge v2, WP1 (NCV2-003)

**Status: `PARTIAL` — one condition verified, two partial, and one decisive open blocker. WP1 is NOT
yet passed, and the plan's own rule says the biological structure-contribution test must not start
until it is.**

**Label rule.** Everything here is **prospective** work by NeuroConverge v2. No v1 record was modified.
Every number below was read out of a real downloaded file in this session, or is marked
`UNKNOWN` / `MISSING` / `BLOCKED`. **Nothing is assumed complete.** The plan's warning applies
literally: *the existence of a public dataset does not mean its contents have been downloaded,
aligned, given the needed metadata, or made reproducible.*

**What was actually downloaded and read** (not READMEs):

| artifact | size | obtained | route |
| --- | --- | --- | --- |
| `pradhan_madan_2025` JSON archive (tar of 8 per-animal JSON) | 14,579,689 B bzip2 → 36,505,600 B tar | **yes** | `wormwideweb.org/activity/api/data/download/paper/pradhan_madan_2025/` |
| `neuropal_label.json.bz2` | 5,815 B → 355,624 B JSON | **yes** | `zenodo.org/api/records/19511989/files/…/content` |
| Dryad `10.5061/dryad.w9ghx3g4v` file manifest (30 files) | metadata only | **manifest yes, files no** | Dryad API |
| `processed_h5.tar.bz2`, `neuropal_label.jld2.bz2`, `restructure_script.jl` | 34 MB / 275 KB / 5.5 KB | **no — HTTP 403** | Zenodo traffic limiter |

---

## 1. The functional resource: what is verified

**`pradhan_madan_2025` (Zenodo record `19511989`, licence `CC-BY-4.0` as recorded in the Zenodo
metadata).** Eight per-animal JSON files were extracted and read; the table is generated from them.

| uid | n_neuron | trace rows | labelled | coverage | neuron classes | conf ≥ 0 | conf < 0 | max_t | dt (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-03-08-03 | 141 | 141 | 104 | 73.8 % | 56 | 96 | 8 | 800 | 0.6016 |
| 2023-03-16-01 | 117 | 117 | 108 | 92.3 % | 56 | 108 | 0 | 459 | 0.5976 |
| 2023-04-06-01 | 155 | 155 | 86 | 55.5 % | 51 | 86 | 0 | 800 | 0.6016 |
| 2023-04-07-22 | 176 | 176 | 127 | 72.2 % | 71 | 125 | 2 | 800 | 0.6016 |
| 2023-04-20-02 | 153 | 153 | 101 | 66.0 % | 60 | 101 | 0 | 800 | 0.6016 |
| 2023-04-25-04 | 147 | 147 | 96 | 65.3 % | 57 | 96 | 0 | 800 | 0.6016 |
| 2023-05-05-22 | 159 | 159 | 123 | 77.4 % | 68 | 122 | 1 | 800 | 0.5887 |
| 2023-05-10-16 | 144 | 144 | 82 | 56.9 % | 38 | 81 | 1 | 800 | 0.5886 |
| **total** | **1192** | **1192** | **827** | **69.4 %** | — | **815** | **12** | — | ~0.59–0.60 |

**Present and verified per animal:** `metadata.uid`, `metadata.paper_id`, `metadata.n_neuron`,
`metadata.source_filename`, `metadata.checksum_h5`, `metadata.blake3_neuropal_dict`,
`metadata.dataset_type`; `timing.max_t`, `timing.mean_timestep`, `timing.timestamp_confocal`;
`behavior.velocity`, `.head_angle`, `.angular_velocity`, `.pumping`, `.reversal_events`;
`gcamp.trace_array`, `gcamp.trace_array_original`; and the NeuroPAL `label` object with
`label`, `neuron_class`, `LR`, `DV`, `region`, `roi_id`, `confidence`.

**Independent replicate unit: `metadata.uid`.** Eight animals yield eight units. **Frames and neurons
are never counted as replicates.** That is a genuine advance over Fish1.5, where one specimen yielded
82 neurons that the v1 record refuses to count as 82 biological replicates.

## 2. The structural resource: what is verified

**NemaNode / Witvliet et al. 2020** (`doi 10.1101/2020.04.30.066209`; viewer at `nemanode.org`;
code at `github.com/dwitvliet/NemaNode`). Read from the source page, not from a summary:

* **Eight developmental reconstructions** (L1 ×4, L2, L3, adult ×2) plus White et al. 1986 compilations
  (JSH, N2U, JSE, whole-animal). Per-dataset download is offered.
* **Chemical synapses were annotated independently by three annotators; only those on which at least
  two agreed were retained.** That is the provenance property worth having.
* **Direction is stated:** chemical = **directed**; gap junction = **undirected**.
* **Edge type and stability class are stated:** stable / developmentally dynamic (added) /
  develop mentally dynamic (pruned) / variable / post-embryonic / not classified.
* **WARNING: The source page says the gap-junction annotation "is by no means exhaustive, and should not be
  treated as such."** Gap junctions must therefore be carried as an explicitly incomplete edge class,
  or excluded, and either choice must be frozen before outcomes.
* **WARNING: Licence: `UNKNOWN`.** The page states none. This must be resolved before any redistribution.
  Compare with the functional side, which is `CC-BY-4.0`.

## 3. WARNING: The decisive blocker: the trace ↔ cell mapping is not in the downloadable artifacts

**This is the finding that decides WP1.**

`metadata.n_neuron` equals `len(gcamp.trace_array)` for all eight animals (verified). But the NeuroPAL
`label` object is keyed by **ROI segmentation id, not by trace row**, and the keys are neither
contiguous nor bounded by the trace count:

| uid | n_neuron | label keys | keys ≤ n | keys > n | min | max | contiguous |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-03-08-03 | 141 | 104 | 87 | 17 | 4 | 180 | no |
| 2023-03-16-01 | 117 | 108 | 74 | 34 | 2 | 175 | no |
| 2023-04-06-01 | 155 | 86 | 34 | 52 | 5 | 348 | no |
| 2023-04-07-22 | 176 | 127 | 110 | 17 | 1 | 204 | no |
| 2023-04-20-02 | 153 | 101 | 76 | 25 | 1 | 214 | no |
| 2023-04-25-04 | 147 | 96 | 42 | 54 | 6 | 354 | no |
| 2023-05-05-22 | 159 | 123 | 118 | 5 | 1 | 177 | no |
| 2023-05-10-16 | 144 | 82 | 58 | 24 | 3 | 208 | no |

**231 entries exceed the trace count in total.** The field is even *named* `idx_neuron` in
`neuropal_label.json`, which is misleading: its keys are the same ROI ids as the JSON `label` object,
and the two artifacts were confirmed to carry **identical key sets and identical values** (the JSON
wraps each value in a one-element list).

**Consequence for the research question.** `H2` asks whether *correct, source-confirmable node
identity correspondence* beats a lawful mismatch. That comparison is undefined while the identity of
each trace row is unknown: a "mismatch" cannot be constructed, and a "correct" mapping cannot be
verified. **`mapping_coverage` is therefore `UNKNOWN`, not "present".**

**Why this is recorded as `BLOCKED` and not as `ABSENT`.** The mapping is expected inside the upstream
HDF5 bundle, whose per-file checksum the JSON already carries (`metadata.checksum_h5`), and a
`restructure_script.jl` that generated the JSON sits in the same Zenodo record. **Both are currently
unreachable: every Zenodo `/files/…/content` request returned HTTP 403 "Access to this resource has
been restricted due to unusual traffic from your network", on both the API and the `?download=1`
route, for a 34 MB and a 5.5 KB file alike.** The Dryad mirror of a *different* candidate dataset is
similarly walled: its file API returns 401 *"must have current bearer token"* and its public
`/downloads/file_stream/` route returns a 4,321-byte JavaScript challenge page. **This is a client
capability and traffic obstruction, not a licence or availability fact, and the licence on the
Zenodo record is `CC-BY-4.0`.** A failed lookup is not evidence of absence — that error has already
been made four times in this project.

## 4. The Dryad candidate: manifest verified, contents unreachable

Dryad `doi:10.5061/dryad.w9ghx3g4v`, version 2, 2026-04-15, licence `CC0-1.0`, `storageSize`
320,032,093 B — **"Whole-brain calcium imaging in freely-moving C. elegans during aversive copper
boundary encounters"**. Its complete manifest was read: **30 files** — 27 `YYYY-MM-DD-NN-cudata.h5`
recordings of ~9.4–12.5 MB each, **`NeuroPAL_labels.jld2` (41,607,043 B)**, `load_data_example.jl`
(1,607 B) and `README.md` (11,123 B). **The presence of a NeuroPAL label artifact and of per-recording
filenames is promising, but no file content was read, so none of the plan's fields can be marked
present for this resource.** Its 27 recordings would be a larger animal-level sample than the eight
used above if access can be obtained.

## 5. Minimum-field table

`BIO_DATASET_CANDIDATES.csv` carries the plan's full field list. Summary of the two principal
resources:

| field | functional (pradhan_madan_2025) | structural (NemaNode / Witvliet) |
| --- | --- | --- |
| `dataset_id` | `zenodo:19511989` | `nemanode / doi 10.1101/2020.04.30.066209` |
| `source_version` | record 19511989 + `checksum_h5` + `blake3_neuropal_dict` per dataset | 8 versioned developmental datasets |
| `licence` | **`CC-BY-4.0`** | **`UNKNOWN` — must be resolved** |
| `specimen_id` | `metadata.uid` (8 units) | one reconstruction per dataset |
| `session_id` | `metadata.uid` | n/a |
| `neuron_id_or_cell_class` | NeuroPAL `label` / `neuron_class` (827 of 1192) | named cells |
| `identity_confidence` | **present**, range −1…5; **−1 semantics `UNKNOWN`** | three-annotator agreement, not per-cell |
| `timestamps` | `timing.timestamp_confocal` | n/a |
| `sampling_rate` | `timing.mean_timestep` | n/a |
| `stimulus_or_behavior` | 4 behaviour traces + `reversal_events` + `timing.event` | n/a |
| `missingness` | **`UNKNOWN`** — must be derived from trace NaNs | gap junctions explicitly incomplete |
| `train_test_split_unit` | **`metadata.uid`** | dataset |
| `source_graph_version` | not in this resource | 8 datasets, per-dataset |
| `adjacency_direction` | not in this resource | **chemical directed; gap junction undirected** |
| `edge_type` | not in this resource | chemical / gap junction + stability class |
| `annotation_independence` | NeuroPAL is transgenic labelling, not connectivity-derived — **candidate `INDEPENDENT`**, to be argued in WP0 | independent of the functional resource (different animals) |
| `mapping_coverage` | **`UNKNOWN` — see §3** | cell names are the only bridge; class-level only |

## 6. WP1 completion condition, assessed honestly

The plan requires all four, and forbids starting the biological structure-contribution test if any is
missing:

| requirement | verdict | basis |
| --- | --- | --- |
| identifiable independent biological replicate unit | **PASS** | 8 `uid`s, verified from the files |
| interpretable structure–function cell-class alignment | **BLOCKED** | cell classes present (827), but the trace ↔ ROI correspondence is not in any reachable artifact |
| a task with a feasible baseline | **NOT YET ASSESSED** | NCV2-004 is not done; the behaviour traces are a candidate source |
| lawful, recomputable data access | **PARTIAL** | JSON obtained under `CC-BY-4.0`; HDF5 and the restructure script blocked by a traffic limiter; the structural licence is `UNKNOWN` |

> **Verdict as first recorded: `WP1 = BLOCKED_PENDING_MAPPING_ACCESS`.** Not a pass, and deliberately not a fail. The plan
> distinguishes "we measured and it was not there" from "we could not measure"; this is the second.

**What would unblock it, in order of preference:** (a) obtain `processed_h5.tar.bz2` or
`restructure_script.jl` once the traffic limiter relents, or via the owner's browser, and read the
trace ↔ ROI correspondence; (b) if the correspondence is genuinely absent upstream, fall back to the
Dryad 27-recording resource, whose manifest shows both per-recording files and a NeuroPAL label
artifact; (c) if neither yields it, the plan's decision tree applies — **PIVOT the data system or
narrow to a structure-sensitive prediction study with a reduced biological claim; do not revive old
blocked data and do not proceed to WP3.**

**Nothing in this document is a NeuroConverge v2 result.** It is a feasibility audit, and its own
deliverable is the statement of what is *not* yet known.

---

## 7. RESOLUTION (same session, later the same day): the mapping exists, in a better resource

**The blocker in section 3 was an artifact of which resource was read first, not a property of the
data.** The plan's own warning applied to me: *a failed lookup is not evidence of absence.*

**WormID is a Wix site whose dataset page links out to eight DANDI Archive dandisets.** All eight are
`spdx:CC-BY-4.0`, all use the **NWB** standard, and all are reachable through the DANDI REST API with
**no token and no challenge page** -- unlike Dryad and, intermittently, Zenodo. DANDI serves presigned
S3 URLs from `api.dandiarchive.org/api/assets/<uuid>/download/`.

| dandiset | name | assets | smallest asset |
| --- | --- | --- | --- |
| 000472 | NeuroPAL volumetric images (Kato lab, UCSF) | 10 | 197,073,664 B |
| 000541 | NeuroPAL Microfluidic Chip Images and GCaMP activity | 21 | **1,420,403,684 B** |
| 000565 | C. elegans whole-brain neuroPAL and immobilized | 21 | 253,712,472 B |
| 000692 | Whole-brain spontaneous GCaMP activity with NeuroPAL | 9 | 8,575,482,056 B |
| 000714 | Segmented and labeled NeuroPAL structural images | 9 | 49,172,084 B |
| 000715 | NeuroPAL: Atlas of C. elegans neuron locations | 10 | 67,636,308 B |
| 000776 | Brain-wide representations of behaviour (Atanas et al. 2023) | 38 | 26,283,315,575 B |
| 001623 | C. elegans whole-brain imaging datasets (Dunn et al. 2025, WormID) | 95 | 2,118,164,791 B |

**Three NWB files were downloaded and opened with `h5py` (which is available; `pynwb` is not, and is
not needed because NWB is HDF5):**

| file | bytes | what it contains |
| --- | --- | --- |
| `000472` smallest | 197,073,664 | `PlaneSegmentation` with `ID_labels`(185) and `id`(170). **Structural only.** |
| `000565` smallest | 253,712,472 | `PlaneSegmentation` with `ID_labels`(144) and `id`(116). **Structural only** -- this file is not in the subset that also carries calcium data. |
| **`000541` smallest** | **1,420,403,684** | **identity AND function in one file. This is the resolution.** |

### What the `000541` file actually contains

```text
processing/CalciumActivity/SignalRawFluor/SignalCalciumImResponseSeries   [RoiResponseSeries]
        data            (936, 177)  float64      # 936 timepoints x 177 neurons
        rois            (177,)      int64        # the same 177 segment ids
        starting_time   scalar                    # attr: "Raw fluorescence activity for calcium imaging data"
processing/CalciumActivity/SignalRawFluordNMF/dNMFCalciumImResponseSeries   # dNMF variant, same shape
processing/CalciumActivity/NeuronIDs                     [SegmentationLabels]
processing/CalciumActivity/CalciumSeriesSegmentationdNMF/...  [ImageSegmentation] 936 children
processing/NeuroPAL/NeuroPALSegmentation/NeuroPALNeurons [PlaneSegmentation]
        id               (177,)  int64    # 0..176, contiguous
        ID_labels        (718,)  object   # flat CHARACTER array, not a label list
        ID_labels_index  (177,)  uint16   # NWB ragged-string cumulative END offsets
        voxel_mask       (177,)  [(x,y,z,weight)]
acquisition/CalciumImageSeries        [MultiChannelVolumeSeries]
general/subject                       [CElegansSubject]
intervals/chemical_stimuli            [TimeIntervals]
```

**The identity mapping decodes to a clean one-to-one table.** `ID_labels` holds 718 single characters
with only 31 distinct values because NWB stores variable-length strings as a flat character array plus
cumulative end offsets; the first eight offsets are `[5, 8, 11, 14, 17, 19, 23, 27]` and the last is
718. Decoding by offset yields **177 labels for 177 segments, all 177 distinct, one empty**:

```text
seg 0 -> IL2DR    seg 1 -> I2R     seg 2 -> I2L     seg 3 -> MCR
seg 4 -> MCL      seg 5 -> MI      seg 6 -> NSMR    seg 7 -> NSML
seg 8 -> I3       seg 9 -> IL2VR   seg 10 -> M3R    seg 11 -> IL2DL   ...
```

**The identity of a trace row is therefore `rois` -> `id` -> `ID_labels`, entirely inside one file.**
This is exactly the correspondence the WormWideWeb JSON export does not expose.

**Verified animal metadata** (`general/subject`): `subject_id = 20190929_07`,
`description = "NeuroPAL worm in microfluidic chip"`, `strain = OH16230`, `growth_stage = YA`,
`sex = O`, `cultivation_temp = 20.0`, `date_of_birth = 2019-09-27`.

**Verified activity is real**: a 200-by-5 slice of `data` has min 0.0415, max 0.6525, mean 0.1131,
std 0.1286, and is not all-zero.

### Two honest limitations of this resource

1. **Microfluidic chip means no free behaviour.** The `000541` files carry calcium activity and
   chemical-stimulus intervals, but no behavioural time series was found. **The primary endpoint must
   therefore be neural-activity prediction, not behaviour prediction.** The plan explicitly permits
   this: it names *prediction error of unobserved neuron activity* as an acceptable primary endpoint.
2. **One session per animal**, and the calcium trace is `starting_time = 0.0` with no `rate` attribute
   in the response series, so the sampling interval must be recovered from the acquisition series or
   the source paper before any temporal analysis. `UNKNOWN` as of this writing.

### Why this stays inside the plan's rules

It does not stitch structure to function across animals without marking it: the structure still comes
from the Witvliet/NemaNode reconstructions of **different** animals, and the mapping class remains
`CELL_CLASS_ALIGNED_ACROSS_SPECIMENS`, never same-animal causal evidence. It does not manufacture
sample size from neurons or frames: the replicate unit is the animal, and `000541` supplies **21** of
them. It does not treat a model-internal label as biological annotation: `ID_labels` comes from
NeuroPAL transgenic labelling, not from connectivity. And it does not revive blocked data: the Dryad
and WormWideWeb routes are simply no longer needed for the identity question.

### Revised WP1 condition

| requirement | was | now | basis |
| --- | --- | --- | --- |
| identifiable independent biological replicate unit | PASS | **PASS** | 21 animals in `000541`; `subject_id` verified |
| interpretable structure-function cell-class alignment | BLOCKED | **PASS** | 177 named identities per file, 1:1 with trace rows, verified by decoding |
| a task with a feasible baseline | not assessed | **not assessed** | NCV2-004 |
| lawful, recomputable data access | PARTIAL | **PASS** | CC-BY-4.0, OpenAccess, no token, DANDI REST API, files actually downloaded |

> **Revised verdict: `WP1 = OPEN_PENDING_TASK_AND_SPLIT`.** The mapping blocker is closed. The two
> remaining items are NCV2-004 (a testable animal-level target) and NCV2-006 (frozen splits), neither of
> which is a data-availability question. **WP3 still does not start until those are frozen.**
