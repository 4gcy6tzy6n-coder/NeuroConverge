# PREFLIGHT_REVIEW — NeuroConverge v2, NCV2-007

**Reviewer mode: separate self-review, NOT independent.** The plan requires an independent reviewer
when one is available and requires that a non-independent review be disclosed. **It is disclosed here:
this review was performed by the same process that produced the artifacts.** Its findings are worth
less than an independent review's, and one is still owed before WP3.

**Date of review:** 2026-10-09. **State reviewed:** the v2 tree at `NeuroConverge/v2/`, commits up to
and including the task-spec commit. **No outcome exists to review** — no v2 model has been fitted, no
prediction made, no endpoint computed. That is the correct state for a pre-flight review.

---

## 1. Verdict

> ## `GO_CONDITIONAL`
>
> **Conditional on four items being frozen first, and on one item being recovered.** The sprint's
> stated deliverable — *proof that a scientific question exists which can be answered with real
> biological data, valid controls and independent statistical units* — **is met**. WP3 must not start
> until the four conditions below are closed, because starting earlier would mean starting from a
> design whose endpoint and split are unfixed.

**Why not a clean `GO`.** Four parameters that the plan requires to be frozen before outcomes are still
open, and one data property is still `UNKNOWN`. Freezing them now would mean choosing numbers without
the information needed to choose them.

**Why not `PIVOT` or `STOP`.** Those verdicts are reserved for a design that cannot be built. Here the
design **has been built far enough to download the real files and measure the alignment**: 152 of 176
functional neurons have a named structural counterpart, the identity mapping is explicit inside one
NWB file, and 21 animals give an independent unit. Those are not plans; they are measured facts from
files read this session.

---

## 2. What was verified, and how

| check | method | result |
| --- | --- | --- |
| v1 frozen read-only | 15 v1 files hashed against commit `5d38a5f1ee8e` in `SOURCE_FREEZE_MANIFEST.json`; no v1 path modified by this lane | **PASS** |
| functional identity mapping | decoded `ID_labels` from the `000541` NWB by cumulative offsets; 177 segments, 177 distinct names, 1 empty | **PASS** |
| activity is real, not a placeholder | 200x5 slice of `SignalCalciumImResponseSeries.data`: min 0.0415, max 0.6525, mean 0.1131, std 0.1286 | **PASS** |
| structural data are real | downloaded `neurons.json` (447 cells), `datasets.json` (12 datasets), `witvliet_2020_7.json` (2781 edges), `witvliet_2020_8.json` (2802 edges) | **PASS** |
| the two sides can be joined | name intersection **152/176 = 86.4 %** against `2020_8`; **176/176** against `neurons.json` | **PASS** |
| the 24 gaps are explained, not hand-waved | they are pharyngeal/`I*`/`M*` cells; the Witvliet adult datasets are `type = head`, so the pharynx is out of scope | **PASS with documented exclusion** |
| licence | `000541` is `spdx:CC-BY-4.0`, `dandi:OpenAccess`; NemaNode's redistribution licence is **`UNKNOWN`** | **PARTIAL** |
| independent unit | `subject_id`; 21 animals in `000541` | **PASS** |
| endpoint, split, seeds, threshold | — | **NOT FROZEN** |
| sampling interval | `starting_time = 0.0`, no `rate` on the response series | **UNKNOWN** |

## 3. The four conditions, and one recovery, before WP3

**C1 — recover the sampling interval.** Without it no temporal split can be justified. Source: the
`acquisition/CalciumImageSeries` node, the `000541` source publication, or the file's own metadata.
**Until it is known, the fallback is a neuron-level split, which is a weaker design and must be
declared as a reduction in claim strength, not presented as equivalent.**

**C2 — fix `f_target`, the fraction of neurons held out as targets, by a rule that cannot see target
values, and solely from the number of animals.** Not yet chosen. Choosing it now would be a number
picked for convenience.

**C3 — fix the primary endpoint threshold from the task scale and from the power table**, not by
inheriting any other project's threshold. The plan forbids IRCN's `NRMSE 0.001`, G1's `10 %` and
CBCC's per-seed `MAC 1 %`, and none of them was used. **With 21 animals, an effect of `0.4277` is
detectable at all and `0.6114` is detectable at 80 % power; both values were computed this session, and
an earlier draft mislabelled the latter as the alpha floor.**

**C4 — fix the seed registry and the control-generation seeds**, so that M1, M2 and N1-N3 are
reproducible and no seed is shared between a training initialisation and a control rewire.

**R1 — resolve the NemaNode redistribution licence.** The graphs are used as analysis input, which is
ordinarily fine, but **redistribution rights are `UNKNOWN` and must not be assumed.** The `000541`
side is unambiguous (`CC-BY-4.0`).

**Plus one owed item: the `evidence/NEAREST_NEIGHBOUR_COMPARISON.md` cross-check** recorded in
`NOVELTY_NEAREST_NEIGHBOURS.md` section 5. **The novelty claim is provisional until that file is read
and its rows absorbed or dismissed.**

## 4. Findings by severity

**Blocker — none.** No finding invalidates the sprint's deliverable.

**Major — two:**

* **M-1: the novelty claim is provisional, and it is the load-bearing one.** If the identity-mismatch
  factor cannot be implemented lawfully at fixed topology and capacity, the increment over
  Beiran & Litwin-Kumar 2025 collapses to a dataset-level variation. **The design does specify two
  mismatch constructions (M1 class-preserving permutation, M2 cross-animal rotation) and a floor
  control (M0), and both are constructible in principle from the downloaded data. But neither has been
  built.** Closure: build both on the real graph and confirm that adjacency and parameter count are
  unchanged, by counting.
* **M-2: the 21-animal design is weak.** Detectable standardised effects are large. **A null or an
  inconclusive result is the most likely outcome, and the sprint's framing must not treat that as
  failure.** Closure: none available within this dataset; recorded as a limitation, and the plan's
  permission for a zero or uncertain result is the governing rule.

**Minor — three:**

* **m-1**: `f_target`, seeds and threshold unfrozen (C2-C4). Blocking for WP3, not for the sprint.
* **m-2**: NemaNode licence `UNKNOWN` (R1).
* **m-3**: two nearest-neighbour entries are `NOT VERIFIED` (Fagerholm & Brazdil 2026 and Linderman
  et al. 2026), the former because every Zenodo PDF request returned HTTP 403.

**Observation — two:**

* The L1-L3 Witvliet datasets exist and could support a **developmental** version of the question
  later; they are not used here.
* `000776` (38 worms, Atanas et al.) would roughly double the animal count but every asset is ~26 GB.
  It is a candidate for a later stage, not for this design.

## 5. What has NOT been done, stated plainly

* **No v2 model has been fitted.** No estimator, no baseline, no control graph has been built.
* **No v2 endpoint exists**, and none could, because the endpoint threshold is not fixed.
* **No scientific claim is made here.** The claim ceiling remains `NONE`, exactly as the plan
  requires at this stage: *the first round's most important deliverable is not model accuracy but
  proof that an answerable scientific question exists.*
* **v1 is untouched.** No v1 gate, report or conclusion was modified.
* **Nothing here is a manuscript.** No abstract, no Results prose, no Discussion, no figure was
  written, per the plan's prohibition.

## 6. Sprint item status

| item | verdict |
| --- | --- |
| NCV2-001 isolated tree and v1 freeze | **DONE** |
| NCV2-002 nearest-neighbour novelty matrix | **DONE, provisional** on the v1 cross-check and two `NOT VERIFIED` entries |
| NCV2-003 data feasibility by reading real files | **DONE**, blocker found and then resolved by a better resource |
| NCV2-004 testable animal-level target plus two lawful mismatches | **DONE**, as a draft; both mismatch controls remain unbuilt |
| NCV2-005 constructible matched-topology null | **DONE**, as a draft; three null families specified, non-constructible subset recorded |
| NCV2-006 splits, estimator, leakage tests | **DONE**, as a draft; endpoint and split parameters deliberately left unfrozen |
| NCV2-007 pre-flight review | **THIS DOCUMENT** |

> **Overall: `GO_CONDITIONAL`.** The question is answerable with real data, valid controls and
> independent units — **which is exactly and only what this sprint was asked to establish.** WP3
> remains gated on C1-C4 and R1.

**Review limitation, repeated because it matters:** this is a **separate self-review and not an
independent one**. The plan requires an independent scientific review before results are treated as
claims; that review has not happened.
