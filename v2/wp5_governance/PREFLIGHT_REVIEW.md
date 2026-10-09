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

---

# ADDENDUM — after the joint lead's review of 2026-10-09

**The joint lead maintained `GO_CONDITIONAL`, approved WP2 protocol design and control construction,
and continued to block WP3.** This addendum records what changed in response, and one finding that
**worsens** the novelty position.

## A1. The novelty position is now worse, not better

**`Creamer MS, Leifer AM, Pillow JW`, bioRxiv `10.1101/2024.09.22.614271`, v4 2026-05-18, code at
`github.com/Nondairy-Creamer/Creamer_LDS_2026`, is now the PRIMARY nearest neighbour** and displaces
Beiran & Litwin-Kumar 2025 into second place. All four version records, the v4 abstract verbatim and
the repository README were read this session.

**What it already publishes**, from the abstract and README: a connectome-constrained dynamical model
fit to real whole-brain recordings; **"alternative models fit using a shuffled connectome achieved
much lower performance"**; that adding non-connectome edges did not improve causal capture; and a
`quick_start_examples/` that reconstructs missing neurons.

**Consequence, stated plainly: H1's basic experiment -- real graph versus shuffled graph -- is
unavailable as v2's novelty core.** The joint lead's own conclusion is adopted.

**What remains is one axis, and it is narrow.** Creamer varies the **graph** while the identity
assignment is an unexamined premise; v2 holds **topology fixed** and varies the **mapping**. These are
orthogonal by necessity, because shuffling a graph destroys the correspondence a "correct identity"
would refer to. The load-bearing claim is therefore the **structure x mapping interaction**, and the
joint lead's acceptance question is adopted as the sprint's governing question.

**If that comparison cannot be built lawfully at fixed topology and fixed capacity, v2 has no
NMI-level contribution here.** That is stated at full strength in
`NOVELTY_NEAREST_NEIGHBOURS.md` section 0.

## A2. The v1 cross-reference is closed

`evidence/NEAREST_NEIGHBOUR_COMPARISON.md` was read. **No row of it covers NCV2-RQ's design.** Its one
shared citation is Beiran & Litwin-Kumar 2025, which this matrix treats more strictly. The v1 document
explicitly disclaims being an exhaustive novelty review and leaves priority unestablished.
**Recorded in `NOVELTY_NEAREST_NEIGHBOURS.md` section 5.** The joint lead's precondition for signing a
novelty conclusion is therefore met on the reading, **though the conclusion itself is now
`NOVELTY_PROVISIONAL -- CLAIM DIFFERENTIATION REQUIRED`**, the lead's own phrasing, and is not a
signature.

## A3. v1 freeze: the check is now content-level, not history-level

**The joint lead's correction is accepted: "the last commit touching a path is not ours" is limited
Git history evidence and cannot exclude uncommitted working-tree edits, indirectly regenerated files,
or branch-sync changes.** A content-level proof was built this session and is stored as
`v2/wp0_freeze/V1_FREEZE_HASH_PROOF.json`, comparing SHA-256 content at three points for all 15 frozen
files:

| level | claim | result |
| --- | --- | --- |
| A | content at the freeze commit equals the recorded hash | **PASS 15/15** |
| B | content at HEAD equals content at the freeze commit | **PASS 15/15** |
| C | working-tree content equals HEAD content (i.e. no uncommitted edit) | **PASS 15/15** |
| D | working-tree content equals the recorded hash | **PASS 15/15** |

**The proof's own limitation is recorded inside the artifact:** it proves the **content of the 15
declared files** is byte-identical. **It does not prove no other v1 file was touched**, because the
manifest freezes a declared set, not the tree. The two claims the lead asked to be separated are now
separated: *"v2 did not modify the frozen evidence"* is proven at content level; *"v2 touched no v1
file at all"* rests on the git-history statement alone and is stated as such.

## A4. Two corrections adopted, two WP2 rulings recorded

**Correction 1, sample size.** 21 is the **dataset** total, **not** the confirmatory `n`. The power
table assumed all 21 enter the paired evaluation; if any animals are consumed by training,
development or model selection the table does not apply. **WP2 must now report total animals,
training/development animals, effective paired confirmatory `n_eff`, and the nesting of seeds within
animals within the dataset.** `TASK_SPEC_DRAFT.md` section 3.5 carries this amendment, including the
statement that **a seed is the same kind of non-replicate as a frame** and that a seed-level standard
error is not an animal-level one.

**Correction 2, the freeze check.** Done, see A3.

**Ruling 1, chemical versus gap junction.** Adopted as a **design constraint, not a caveat**: the
chemical layer is the primary analysis; the gap-junction layer is secondary and explicitly
lower-confidence; N1 must preserve degree **per layer separately** and must **not** swap a chemical
edge for a gap-junction edge; and an absent gap junction is **weaker evidence of absence** than an
absent chemical synapse, because the source states the electrical reconstruction is less complete.
`TASK_SPEC_DRAFT.md` section 2.2 carries this.

**Ruling 2, source licensing.** Adopted. **NemaNode's GPL-3.0 is a software licence and does not
transfer to the anatomical matrices it loads**, whose redistribution terms remain `UNKNOWN`.
**R1 stays OPEN.** Use as analysis input is permitted; **redistribution is not, until resolved.**
`TASK_SPEC_DRAFT.md` section 3.6 carries the use-versus-redistribution table.

## A5. Two `NOT VERIFIED` entries remain `NOT VERIFIED`

**Fagerholm & Brazdil 2026** -- the lead found a *different* 2026 Physical Review E paper by the same
authors on human ultrafast oscillations (`10.1103/jjzp-h5qf`). **It does not match the entry** (which
is a Zenodo record, `10.5281/zenodo.22395352`, titled "Structure-Dynamics Interdependence: An
Information-Theoretic Framework for Neural State Prediction", whose metadata was retrieved but whose
PDF was blocked by HTTP 403). **A same-author paper is not a substitute. Maintained `NOT VERIFIED`.**

**Linderman et al. 2026** -- not uniquely locatable from author and year alone. **Maintained
`NOT VERIFIED`; requires an exact title, DOI or preprint number.**

## A6. Repository visibility: the commits are local only

**The joint lead reports that the connected NeuroConverge GitHub view does not show `01879e3`,
`c358940`, `f6d3650` or `d86c978`, nor the v2 files. That is explained and confirmed:** the branch was
**12 commits ahead of `origin/main` (remote at `9aba389`) and had not been pushed.** The lead's
inability to verify was therefore correct at the time of writing, and **"all seven items complete" was
this lane's report, not an independently verified fact.** Pushing is a publication action and was not
taken unilaterally.

## A7. WP2 rulings accepted as the next round's scope

| item | ruling | next-round obligation |
| --- | --- | --- |
| C1 sampling interval | prioritised | recover from the acquisition series or the source paper; **if only frame indices are recoverable, restrict to discrete-step prediction and do not claim second-scale dynamics** |
| C2 `f_target` | fix inside development data, then freeze | target-neuron selection, missingness handling, identity-match consistency |
| C3 primary threshold | **must freeze** | primary loss, minimum meaningful difference, animal-level interval, power assumptions |
| C4 seed registry | **must freeze** | animal split, model init, random graphs, identity permutation, training config, RNG sources |
| R1 licensing | stays open | use versus redistribution audited separately |
| independent review | outstanding | an outside person reviews the frozen contract, the comparators and the statistical unit |

**Governing question for the next acceptance, adopted verbatim from the joint lead:** after fixing the
model, the input information and the topology statistics, **does a correct cross-individual neuron
identity correspondence still provide an increment that existing connectome-constrained prediction
research has not explained?**

**This addendum does not change the verdict. It remains `GO_CONDITIONAL`:** WP2 design and control
construction approved; WP3 confirmatory work, confirmatory unblinding, post-hoc threshold changes and
formal manuscript writing all remain **not approved**.
