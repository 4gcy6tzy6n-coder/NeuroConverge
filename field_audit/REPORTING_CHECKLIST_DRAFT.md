# Minimum evidence reporting standard for bio-to-AI transfer claims (draft skeleton)

**Status: DRAFT SKELETON, required to exist before coding begins** (frozen protocol section 7). Finalized only
after the corpus statistics exist. Each line states the minimum a publication should **report** for a
transition to be assessable - explicitly not the minimum to pass: a paper that reports everything and honestly
shows a weak transition is compliant; a paper that claims a strong transition and reports nothing is not.

Validation requirement (frozen): applied mechanically to the coded corpus, the standard must separate E0/E1
claims from E2+ claims with a reported confusion table.

## T1 structure -> computation

- [ ] the biological structure is named specifically enough to be checkable (circuit, region, cell type,
      plasticity rule - not "the brain")
- [ ] the computation attributed to that structure is stated as an input-output statement
- [ ] the evidence that the structure performs that computation is either presented or cited to a specific
      source (assertion-only is gradeable but must be visible as assertion-only)

## T2 computation -> correspondence

- [ ] the mapping between biological computation and artificial component is stated (which element implements
      which function), beyond naming resemblance
- [ ] departures from the biological mechanism are listed (what was simplified away, and known)

## T3 correspondence -> utility

- [ ] the comparison that attributes the gain to the correspondence: capacity/parameter-matched baselines,
      an ablation removing the bio-derived element, or an equivalent-control task
- [ ] the claim states which of those it has and which it lacks

## T4 utility -> generality

- [ ] task families beyond the demonstrated one are named as tested or as untested
- [ ] scale sensitivity (parameters, data, horizon) is reported or marked unreported

## T5 claimed scope

- [ ] the abstract's claim is traceable to a specific result (which figure/table carries it)
- [ ] the claim's scope qualifiers (task, scale, setting) match the evidence's scope

## One line per claim, machine-checkable

The final standard ships as a checklist a reader can apply to an abstract in under ten minutes; each item is
binary (reported / not reported), and the confusion table against the audit's E-grades is reported in the
paper, not implied.
