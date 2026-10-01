# Project freeze and integration boundaries

**Audit date:** 2026-10-01 (Asia/Shanghai)

## Freeze decision

The publication repository is new and must not absorb either source repository's history. Source experiments and result files remain source-of-record. NeuroConverge may contain only selected paper-level artifacts, source links and hashes.

**Freeze is not yet complete.** The source audit found a public NeuroMotif `main` commit, but NeuroMech has a dirty working tree and the public remote advertises only an `experiment-publication` branch. The local NeuroMech `main` has a different commit and 387 changed/untracked paths at audit time. Those are not interchangeable snapshots. This repository records the mismatch rather than silently promoting one as canonical.

## Observed source identities

| Source | Remote | Observed revision | Working-tree evidence | Freeze status |
|---|---|---|---|---|
| NeuroMotif | `https://github.com/4gcy6tzy6n-coder/NeuroMotif.git` | public `main`: `1adc07ffc735cf458116ca36c9f4875708034d4a` | local publication worktree at this commit was clean when inspected | Candidate snapshot; not an owner-approved freeze |
| NeuroMech | `https://github.com/4gcy6tzy6n-coder/NeuroMech.git` | public `experiment-publication`: `3e5c458f15b2cad7aa6c5703b1827763e84343bb`; local `main`: `555c064f4ff3153c871808c3f191b9934a18eaf5` | local `main` worktree had 387 changed/untracked paths; publication branch worktree had 2 uncommitted paths | Unfrozen; canonical paper/evidence snapshot unresolved |

The requested NeuroConverge remote `https://github.com/4gcy6tzy6n-coder/NeuroConverge.git` returned no advertised heads during this audit. That alone does not distinguish an empty repository from access/visibility limitations.

## Boundaries

1. Never rewrite a historical result to fit the integrated narrative. Correct errors in a new, traceable artifact and preserve the original.
2. Preserve the original unit, task, comparator, preregistration status, corrections and evidence class for every result.
3. Do not pool unlike endpoints into a project-level effect.
4. A public-data or schema block is a boundary, not a biological negative.
5. RR18 and RR19 are separately governed workstreams and are excluded from this initial two-source manuscript scope unless an explicit evidence audit establishes otherwise.
6. No new experiment by default. Lower or remove a claim when existing evidence is insufficient.

## Freeze completion checklist

- [ ] Owner selects the exact NeuroMech source revision/snapshot (public publication branch, local main commit, or a newly finalized source commit).
- [ ] Resolve whether the 387 local changes are excluded, included as a hashed snapshot, or finalized into source history; do not discard them.
- [ ] Confirm NeuroMotif commit and identify which source artifacts, beyond its currently published model/result subset, belong in the paper.
- [ ] Record paper-critical source paths and SHA-256 hashes in the manifests.
- [ ] Run source-to-claim, numerical and rights/licence audits on the selected files.

Until these conditions pass, manifests must identify a candidate snapshot rather than state “frozen.”
