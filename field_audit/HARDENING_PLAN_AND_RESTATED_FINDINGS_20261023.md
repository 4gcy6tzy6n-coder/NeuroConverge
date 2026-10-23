# Restated findings and the hardening plan (2026-10-23, governing the paper until superseded)

**Authority.** The project lead's 2026-10-23 review of `RESULTS_SUMMARY_20261023.md` against the official NMI
submission requirements is accepted in full and recorded as the governing decision: article type **Analysis**
(proposed title: *Biological-to-artificial intelligence transfer: an analysis of evidence supporting
mechanistic claims*); the method arc and the five-project calibration are **demoted to Supplementary / case
study** - they demonstrate the framework, they are not an independent confirmation of field-level proportions;
no closed project reopens; the three P0 gaps are the critical path. This document restates what the existing
sheets already answer (P0-1's first half, executed same day), records the sensitivity results (P1), and fixes
the execution order for what remains.

## 1. P0-1, first half, from existing data: the two-layer T1 restatement

The frozen sheet always carried both layers; the earlier summary reported only `in_paper_grade`. Both layers,
weaker merge throughout:

| layer | T1 result | meaning |
| --- | --- | --- |
| in-paper | 18/18 E0 | no claim demonstrates its structure->computation transition inside the paper |
| external | **14/18 E3, 4/18 E0** | for most claims, the cited neuroscience is independently established (Schultz-Dayan-Montague 1997; Hafting 2005; Wilson & McNaughton 1994; McClelland et al. 1995; Desimone & Duncan 1995; ...). Coder agreement on presence: 15/18 (A) vs 15/18 (B); 9/18 identical after E3/E4 strength |

**The restated finding - the sentence the paper may carry:**

> The biological-foundations transition is never demonstrated inside the claiming paper (18/18 in-paper E0);
> it is externally anchored for most claims (14/18 E3 under the weaker merge) by citation to independently
> established neuroscience. The field's evidence structure is therefore not "unsupported biology" but
> **delegated biology**: the claim chain begins on rented ground, and the load-bearing question is whether
> the rented source supports the *specific* computation claimed at the specificity used.

That specificity question is exactly what both coders' notes already flag ("external literature documents
[lateralization's] functional advantages ... but does not specify ...", "establishes sparse, modular,
small-world [networks]; the specific computation claimed (local ...)"): the frequent mismatch is at the level
of **specificity**, not existence. The E3 numbers above may not be equated with "the specific claim is
supported" - that is P0-1's second half, below.

## 2. P0-1, second half: the T1 external-source verification round (next)

For each of the 14 externally-anchored claims: extract the coder-cited source(s), restate the paper's T1
sentence verbatim (from the pinned PDF), and grade the **specificity match** on a frozen three-point scale
(supports-the-specific-computation / supports-the-general-phenomenon-only / does-not-address). Output: a
per-claim verification table, added as a third layer. AI-executed first pass by rule; the human expert pass
(P0-2) supersedes.

## 3. P1 sensitivity, executed same day from the sheets

| variant | headline on E0/E1 | headline on E0 only |
| --- | --- | --- |
| coder A's map | 7/18 (38.9%) | 1/18 (5.6%) |
| coder B's map | 6/18 (33.3%) | 2/18 (11.1%) |
| merged map (weaker) | 7/18 (38.9%) | 3/18 (16.7%) |

**Reading, recorded before any drafting:** the qualitative claim - a substantial minority of headline
transitions rest on uncontrolled evidence - holds under every map and both boundary definitions; the
**magnitude is definition-dependent (5.6-38.9 percent)** and the paper must report the range with the
definitions attached, centering neither. The full E0/E1/E2 boundary grid extends this table when the
validation corpus lands.

## 4. P0-2 (human experts) and P0-3 (validation corpus): standing items

- **P0-2** requires one neuroscience-savvy and one ML-savvy human coder plus an arbitration round; this is
  owner-side staffing. Everything is structured for supersession: identical instructions, identical sheets,
  recomputation is one command, and the AI-coder disclosure plus the human-supersedure rule are already in
  the methods section draft.
- **P0-3** validation corpus: target ~60-100 claims under a pre-fixed rule amendment (target 60; family cap
  raised to 10; **year stratification added** - at least 8 claims per publication-year band 2015-2019 /
  2020-2022 / 2023-2026 - because the relevance draw is recent-biased; published-status recorded, not
  filtered). The draw reuses the pinned snapshot where composition allows and adds date-sorted fetches for
  the early bands; coder cost is bounded by text-extraction (pdftotext, derived .txt hash-pinned beside the
  PDF). The 18-claim corpus stays frozen as the pilot; all pilot numbers are re-labelled pilot numbers.

## 5. Kill-rule and wording discipline carried forward

With the two-layer restatement, the following wordings are **forbidden** in the paper: "no biological
evidence", "the mechanisms are unsupported", any field-percentage claim from the pilot alone, and any
sentence that equates in-paper E0 with absence of evidence. The kill rule is re-checked on the validation
corpus, not the pilot.
