# Path layout: what data the scripts expect, where it comes from, and what is not reproducible

**Status: the layout document the corpus did not have. Twenty-seven of twenty-nine scripts read from
absolute paths under `/tmp/`, and nothing said so.** **This is a record, not a change: no script is edited
and no measurement is affected.**

---

## 1. Why this exists

**A provenance audit of the corpus asked two questions: does every document name a script that exists, and
does every script name a data path that resolves?**

**The first found four broken links, now fixed.** **The second found that 27 of 29 scripts read from
`/tmp/`, which is outside the repository, is cleared on reboot, and will never exist on a reviewer's
machine.** **The scripts are therefore not runnable by anyone but their author, and this document is the
minimum that fixes the record of it.**

## 2. The four input locations, and what each holds

| path | contents | scripts using it | documented source |
| --- | --- | --- | --- |
| **`/tmp/osf/w/exported_data`** | the wild-type atlas export: 113 animals, 678 files, `<i>_{gcamp,labels,stim_neurons,stim_volume_i,t,ds_name}.txt` | **26** | `WIRESHIFT_STAGE2_WT_AUDIT.md` |
| **`/tmp/osf/u/exported_data_unc31`** | the `unc-31` export: 18 animals, same file set | **1** | `WIRESHIFT_STAGE1_DATA_AUDIT.md` |
| **`/tmp/wna/ex/wormneuroatlas/data`** | the connectome tables: `aconnectome_witvliet_2020_7.csv`, `aconnectome_witvliet_2020_8.csv`, `aconnectome_white_1986_whole.csv`, `funatlas.h5`, `cell_lineage.txt`, and others | **24** | `WIRESHIFT_STAGE1_DATA_AUDIT.md` |
| **`/tmp/ncv2/conn`** | **`neurons.json` only** -- cell class, neurotransmitter type, embryonic/head/tail flags | **3** (`03`, `07`, `10`) | `TASK_SPEC_DRAFT.md`, from NemaNode `populate-db/raw-data/` |

**And one path a reader may misread:** **the three scripts declaring `CONN=pathlib.Path("/tmp/ncv2/conn")`
do NOT read connectivity from there.** **They read `neurons.json` for cell classes and take the
connectivity itself from the same `aconnectome_*.csv` files the other 24 scripts use.** **Verified by reading
each of the three.** **So there is one connectome source in this line, not two.**

## 3. Input provenance and integrity, as recorded elsewhere

| input | source | integrity |
| --- | --- | --- |
| wild-type export | OSF `10.17605/OSF.IO/E2SYT`, `exported_data.tar.gz`, 523,093,816 B | **sha256 `d6e7b3d93175b40b7ae17bde2182835e9c2144388142c522ee9b3832f6ce836`**, matches the OSF metadata |
| `unc-31` export | same OSF record, `exported_data_unc31.tar.gz`, 84,924,311 B | size recorded; **checksum not independently verified** |
| connectome tables | `wormneuroatlas` data directory | **no checksum recorded** |
| **`neurons.json`** | **NemaNode `populate-db/raw-data/`, 58,575 B, 447 records, sha256 prefix `c780e0b7cab28b31`** | **checksum first recorded in this document** |

**Download volume across the line: about 675 MB, against the plan's 10 GB Stage-2 budget.**

## 4. Licences, which bound a data deposit but not the analysis

| input | licence | status |
| --- | --- | --- |
| `000541` NWB (identity mapping) | `spdx:CC-BY-4.0`, `dandi:OpenAccess` | **permissive** |
| wild-type and `unc-31` exports | **no licence permitting redistribution was found** | **blocks a supplementary data deposit** |
| connectome tables | `wormneuroatlas` package | not verified |
| **`neurons.json`** | **NemaNode redistribution licence `UNKNOWN`** | **recorded as `PARTIAL` in `PREFLIGHT_REVIEW.md`** |

**Analysis is unaffected by all four; a data deposit is currently not authorised.**

## 5. What a reproducer would have to do

1. **Download `exported_data.tar.gz` and `exported_data_unc31.tar.gz`** from OSF `10.17605/OSF.IO/E2SYT`,
   **verify the wild-type sha256 against section 3**, and extract to `/tmp/osf/w/exported_data` and
   `/tmp/osf/u/exported_data_unc31`.
2. **Place the `wormneuroatlas` data directory at `/tmp/wna/ex/wormneuroatlas/data`.**
3. **Place `neurons.json` at `/tmp/ncv2/conn/neurons.json`,** verifying the sha256 prefix against section 3.
4. **Run the scripts in `wp3_results/anatomy/` and `wp3_results/reliability/` from any directory** -- they
   use absolute paths, so the working directory does not matter.

**Step 3 is the one that cannot be completed from the recorded sources alone:** **`TASK_SPEC_DRAFT.md`
records the NemaNode path within that project but not a URL or a commit, so a reproducer would have to
locate the file.** **That is a genuine gap in this record and is stated rather than glossed.**

## 6. What this document does not fix

* **It does not make the scripts path-portable.** That would be 27 edits against 1 document, and the
  scripts are retained as the exact artifacts that produced the committed results. **A single `paths.py`
  imported by all of them is the right fix if the line is to be packaged for a deposit, and it is not done.**
* **It does not provide the missing URL for `neurons.json`.**
* **It does not verify the `unc-31` checksum or the connectome tables' checksums.**

## 7. Provenance

* Found by a corpus audit that checked, for every document, whether the scripts it names exist, and for
  every script, whether the paths it reads resolve.
* **Four broken provenance links were found and fixed** (`09_animal_level.py` to `09_animal_level.py`,
  `11b_source_rule.py` to `11b_source_rule.py`, `06_common_mode.py` to `06_common_mode.py`,
  `13_within_vs_between_splithalf.py` to `13_within_vs_between_splithalf.py`); **a reader following any of the
  four previously found nothing.**
* **`neurons.json`'s sha256 prefix and the clarification in section 2 are new in this document.**
* **No model was fitted. No measurement changed.**
---

> **BROKEN-CITATION NOTICE, appended round 49.** **Four script names in this document were written
> incorrectly when it was created in round 25** — `05_common_mode.py`, `08_animal_level.py`,
> `11_source_rule.py` and `13_measurement_structure.py` — **and the same round that created it renamed
> them to `06_common_mode.py`, `09_animal_level.py`, `11b_source_rule.py` and
> `13_within_vs_between_splithalf.py`.** **The names are corrected above; the notice records that a
> document whose purpose is to list where things are contained four wrong paths, and that nothing
> checked it for thirty-four rounds.**
