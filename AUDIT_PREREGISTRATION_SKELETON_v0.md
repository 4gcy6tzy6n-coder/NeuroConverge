# Field-level bio-to-AI transfer evidence audit: pre-registration skeleton v0

**SUPERSEDED 2026-10-18 by `field_audit/AUDIT_PREREGISTRATION_v1_FROZEN.md`** (the signed, binding text). This
skeleton is kept as the pre-signature draft; the frozen version is the one the protocol's amendment rule
governs.

**Status: SKELETON, nothing frozen.** Every block marked `[FROZEN AFTER OWNER SIGNATURE]` becomes binding only
when the owner signs the proposal `PROPOSAL_20261018_FIELD_AUDIT_ROUTE_A.md` (item P3). Before that signature
this document may be amended freely; after it, any change is a dated amendment, never a silent edit - the rule
every lane in this workspace already runs under.

Companion proposal: `PROPOSAL_20261018_FIELD_AUDIT_ROUTE_A.md`. This skeleton exists so the owner signs a
protocol, not a vibe.

## 1. Research question and article type

Question: across high-impact published claims that a biological mechanism improves an artificial system, which
inference transitions carry independent empirical support, which do not, and what minimum evidence standard
would make the difference visible at publication time?

Article type: Analysis. The unit of analysis is **the inference transition**, not the paper and not the authors.

## 2. The transition taxonomy (the audit's coordinate system)

Every audited claim is decomposed into the canonical chain:

    biological structure -> biological computation -> artificial correspondence -> task utility -> generality

with named transitions:

| id | transition | the question the coder answers |
| --- | --- | --- |
| T1 | structure -> computation | does the paper establish that the cited structure performs the cited computation (with its own evidence, or by citation)? |
| T2 | computation -> correspondence | does the artificial component instantiate that computation, under a stated mapping, or only resemble it? |
| T3 | correspondence -> utility | is the claimed performance gain attributable to the correspondence rather than to capacity, tuning or baselines? |
| T4 | utility -> generality | does the gain survive task families, scales and ablations beyond the demonstrated setting? |
| T5 | any -> claimed scope | does the abstract's claim match the evidence's scope? |

`[FROZEN AFTER OWNER SIGNATURE]` taxonomy wording (T1-T5 definitions above, verbatim).

## 3. Claim corpus selection rule

Order of operations is binding: the rule freezes, then the corpus is drawn, then coding begins. No claim is
added or removed after the draw except by the pre-registered replacement rule.

Proposed defaults, each individually amendable before signature:

| parameter | proposed default |
| --- | --- |
| window | 2015-01-01 to 2026-09-30 |
| venue tiers | tier 1: Nature* (incl. NMI), Science*, Cell*; tier 2: NeurIPS/ICML/ICLR/CVPR oral-or-spotlight, PNAS; tier 3: the top-cited 10 percent of the remainder by citation count at draw date |
| citation floor | 100 citations at draw date for tier 3; none for tiers 1-2 |
| claim type | the paper must claim, in abstract or title, that a biological mechanism (structure, circuit, plasticity rule, coding principle, connectome) improves an artificial system's capability |
| stratification | at most 3 claims per mechanism family (memory, plasticity/learning rules, architecture/connectome, attention/coding, neuromorphic hardware, other), at most 5 per venue |
| exclusions | (a) purely inspirational naming with no mechanistic content, per the T2 wording; (b) claims whose sole evidence is a benchmark the same authors introduced; (c) retracted or withdrawn papers (recorded, not coded) |
| target size | 20 claims, accept 15-25 after replacements |
| replacement rule | the next-highest-citation eligible claim in the same stratum substitutes for any claim excluded post-draw; substitutions logged with reason |
| dual-draw check | the draw is executed by script from a pinned database snapshot (OpenAlex or Scopus export) on a recorded date; the query, snapshot hash and output list are committed before coding |

`[FROZEN AFTER OWNER SIGNATURE]` all parameters in this section.

## 4. Evidence grading scale

| grade | meaning |
| --- | --- |
| E0 | no evidence in the paper; assertion or citation only |
| E1 | suggestive evidence in the paper (one setting, no controls named in the transition) |
| E2 | controlled evidence in the paper (the transition has its own comparison or ablation) |
| E3 | independent evidence exists elsewhere in the literature (registered citation, verified) |
| E4 | independent replication or adversarial evaluation exists (registered citation, verified) |

A transition's recorded grade is the strongest that applies; the coding sheet records both the in-paper grade and
the external-evidence flag so E2-with-external-E3 and E3-alone are distinguishable.

`[FROZEN AFTER OWNER SIGNATURE]` grade definitions.

## 5. Coding protocol

- Two coders work independently per claim; at least one is not an author of any workspace code (proposal item P4).
- Coding sheet fields: claim id; paper metadata (pinned DOI, version, snapshot); verbatim sentence carrying the
  claim; mechanism family; the T1-T5 decomposition; per-transition grade with the two-three line justification
  quoting the paper; external-evidence citations with verification route; scope-match verdict (T5).
- All quotes are copied from a pinned full text (publisher PDF, arXiv version with date, or repository copy);
  the provenance of every quote is a file hash. A claim whose full text cannot be pinned is not coded - it is
  recorded as uncodable and the replacement rule fires.
- Disagreements: per-transition, resolved by discussion if the grades differ by one step, by the pre-registered
  tie rule (take the weaker grade) if more; raw disagreement rate is reported in the paper, overall and per
  transition, and a 10 percent double-coded quality-control sample of the coder agreement is re-checked by the
  non-coding reviewer.
- Coding rounds: at most two correction rounds per claim after the first pass; a third finding reopens the
  claim for owner-visible review rather than another silent pass.

`[FROZEN AFTER OWNER SIGNATURE]` coding-sheet fields, resolution rules, round bound.

## 6. Quantified outputs (decided before any data exist)

1. Distribution of transition grades across the corpus: for each T1-T5, the count of claims at E0-E4.
2. The headline statistic: the share of claims whose **headline-relevant transition** (the one the abstract's
   improvement claim rests on) is at E0 or E1.
3. The scope-match rate (T5 verdicts).
4. Stratified repeats of 1-3 by mechanism family and venue tier.
5. Sensitivity analysis: statistics 1-2 recomputed under the two pre-declared alternative selection rules
   (citation floor 50; tier-2 without oral-or-spotlight restriction) on replacement corpora of the same size.
6. The audit's own reliability numbers: disagreement rates, replacement log, uncodable count.

`[FROZEN AFTER OWNER SIGNATURE]` the list of reported statistics and their definitions.

## 7. The normative artifact: minimum evidence reporting standard

Drafted in skeleton form before coding begins (so the constructive half cannot be postponed), finalized after
the corpus statistics exist. Structure: one checklist line per transition T1-T5 plus one for scope, each line
stating the minimum a publication should report for that transition to be assessable - not the minimum to pass.
The standard is validated against the corpus: applied mechanically, it must separate the E0/E1 claims from the
E2+ claims with a reported confusion table.

## 8. The workspace's own projects: calibration, not corpus

MICA, NeuroMech, IRCN, NeuroMotif and BioMemory results are coded on the same sheet, reported in a separate
section, and excluded from every statistic in section 6. Their role is to show the instrument detects real
evidence boundaries it was not tuned on - the negative results this workspace already owns are exactly known
inputs, so the instrument must reproduce their known grades or the instrument is defective.

## 9. Governance

- Provenance: every coded paper's source (query, snapshot, version, hash) sits in a register file modelled on
  the MICA register (`01_NOVELTY_NEAREST.csv` pattern); every statistic is computed by script from the coding
  sheets, never transcribed by hand.
- Independent verification: before submission, a person who coded nothing re-runs the corpus draw and the
  statistics scripts from the register (the D7 discipline; proposal item P7).
- Frozen-threshold discipline: nothing in sections 2-6 changes after coding begins; a defect found mid-coding is
  recorded and, if it changes a frozen definition, coding halts for an owner-visible dated amendment before
  resuming - the workspace rule, applied one level up.

## 10. Stop rules and schedule

| rule | trigger | action |
| --- | --- | --- |
| corpus freeze | draw script output committed | no additions except the replacement rule |
| coding bound | all claims coded or two correction rounds exhausted | exhausted claims coded as-of-last-round, noted |
| schedule bound | 8 weeks after corpus freeze | draft is written from whatever exists; unstarted analyses are listed as not done, never estimated |
| scope creep bound | any proposal to add a transition type, statistic or corpus stratum after freeze | requires owner signature as a dated amendment |
| kill rule | if the corpus statistics show E2+ on headline transitions in 80 percent or more of claims | the audit's premise is wrong; report that finding to the owner before drafting, and the paper becomes "the field's evidence is better than the framework predicted" or does not proceed |

## 11. What this protocol cannot establish

- It audits published evidence structures, not the truth of any claim: an E0 transition may be true and
  unproven; the finding is about the evidence, never worded as "X is false".
- It does not judge authors, motivations or review quality.
- Citation counts and venue tiers are proxies for impact and carry their own biases; the sensitivity analyses
  bound, but do not remove, this.
- One coder-pair on one corpus is one instrument reading; the disagreement statistics are the honest noise term.
