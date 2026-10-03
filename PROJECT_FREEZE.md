# Project freeze and integration boundaries

**Audit date:** 2026-10-01 (Asia/Shanghai)

## Freeze decision

The publication repository is new and must not absorb either source repository's history. Source experiments and result files remain source-of-record. NeuroConverge may contain only selected paper-level artifacts, source links and hashes.

**Scope freeze and artifact freeze are different.** The user-directed scope is to synthesize the existing portfolios without launching new experiments. That does not freeze the underlying files. NeuroMotif has a clean public `main` candidate; NeuroMech has a public `experiment-publication` candidate and a much broader local Route-D evidence inventory on a dirty worktree. None alone is a canonical snapshot of every cited record. The integration draft must identify each result's exact source and label unresolved or untracked records; it must not imply that the full source projects are frozen.

## Observed source identities

| Source | Remote | Observed revision | Working-tree evidence | Freeze status |
|---|---|---|---|---|
| NeuroMotif | `https://github.com/4gcy6tzy6n-coder/NeuroMotif.git` | public `main`: `1adc07ffc735cf458116ca36c9f4875708034d4a` | local publication worktree at this commit was clean when inspected | Candidate snapshot; not an owner-approved freeze |
| NeuroMech | `https://github.com/4gcy6tzy6n-coder/NeuroMech.git` | public `experiment-publication`: `3e5c458f15b2cad7aa6c5703b1827763e84343bb`; local `main`: `555c064f4ff3153c871808c3f191b9934a18eaf5` | local `main` worktree had 387 changed/untracked paths; publication branch worktree had 2 uncommitted paths | Unfrozen; canonical paper/evidence snapshot unresolved. The Route-D V3 portfolio matrix does not contain several selected `3e5c458` M2/M5 experiment IDs. |

NeuroConverge is a separate publication repository. Its `main` was pushed and verified at `b55871dec1207b2c9e8b63270ebcc7871f0feaca` (tree `ab23be556af6016552ba8b6fa9ed8c38f59616cc`). This records the initial integration checkpoint; it does not certify the upstream source portfolios as frozen.

## Boundaries

1. Never rewrite a historical result to fit the integrated narrative. Correct errors in a new, traceable artifact and preserve the original.
2. Preserve the original unit, task, comparator, preregistration status, corrections and evidence class for every result.
3. Do not pool unlike endpoints into a project-level effect.
4. A public-data or schema block is a boundary, not a biological negative.
5. RR18 and RR19 are separately governed workstreams and are excluded from this manuscript scope unless an explicit evidence audit establishes otherwise.
6. No new experiment by default. Lower or remove a claim when existing evidence is insufficient.

## Freeze completion checklist

- [ ] Reconcile every paper-critical record against the Route-D matrix and separately document selected `experiment-publication` records that are absent from it.
- [ ] Resolve whether the 387 local changes are excluded, included as a hashed snapshot, or finalized into source history; do not discard them.
- [ ] Confirm NeuroMotif commit and identify which source artifacts, beyond its currently published model/result subset, belong in the paper.
- [ ] Record paper-critical source paths and SHA-256 hashes in the manifests.
- [ ] Run source-to-claim, numerical and rights/licence audits on the selected files; obtain an owner-approved immutable artifact snapshot.

Until these conditions pass, manifests must identify a candidate snapshot rather than state “frozen.”
