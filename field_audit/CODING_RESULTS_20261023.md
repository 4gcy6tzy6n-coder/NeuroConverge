# Coding-phase results (2026-10-23): the evidence structure is inverted relative to the claim chain

**Status: measured record of the coding phase, both coders' sheets complete, merged per the standing
weaker-grade rule, statistics computed by script from the sheets.** The kill rule of protocol section 10 was
checked before any drafting: 61.1 percent of headline transitions grade E2+, below the 80 percent trigger,
so the audit's premise holds and drafting may proceed.

## The six frozen outputs (from `CODING_sheets/stats.json`, computed by `compute_statistics.py`)

1. **Grade distributions (weaker-grade merge over both coders)**:

| transition | E0 | E1 | E2 | reading |
| --- | --- | --- | --- | --- |
| T1 structure->computation | **18** | 0 | 0 | not one claim establishes its biological-foundations transition with in-paper evidence |
| T2 computation->correspondence | 2 | 12 | 4 | correspondence is mostly suggestive |
| T3 correspondence->utility | 1 | 6 | 11 | the best-evidenced transition - the papers' comparisons live here |
| T4 utility->generality | 7 | 6 | 5 | mixed, leaning weak |
| T5 any->claimed scope | 1 | 17 | 0 | scope evidence is almost never controlled |

2. **Headline statistic**: 7 of 18 claims (38.9 percent) carry their abstract's improvement claim on a
transition at E0 or E1. Per coder before merge: A 7/18, B 5/18.

3. **Scope-match rate**: 72.2 percent of T5 verdicts are `match` (26/36 rows over both coders).

4. **Stratified repeats**: in `stats.json` (`by_family`, `by_tier`); the T1-at-E0 pattern is uniform across
families and categories - no stratum escapes it.

5. **Sensitivity**: not run - the two alternative selection rules were re-read by the arXiv amendment as
category-composition alternatives and were not drawn; recorded as a named missing item, not silently skipped.

6. **Reliability**: two-coder disagreement 18/90 (20.0 percent) overall - T1 0.0, T2 5.6, T3 16.7, T4 27.8,
T5 50.0 percent; headline disagreements 6/18, all of one shape (A named T3 where B named T2), resolved by the
weaker-evidence rule. Replacements in the draw: 8 (7 adjudicated + 1 uncodable). Uncodable: 1. Both coders
are isolated-context instances of the same assistant model - mechanical independence real, error
independence not claimed; the paper's methods section must state this and the human-coder supersedure rule.

## The finding, stated at the strength the sheets support

The corpus's evidence structure is **inverted relative to its claim chain**: the transition every claim
starts from (a named biological mechanism performing a named computation) is the least evidenced in the
papers themselves - universally E0, resting on citation or assertion - while the transition the field's
referees are best equipped to check (does the artifact beat a baseline) is the best evidenced. The chain's
two ends are anchored from outside the paper: biology upstream (by citation to neuroscience) and scope
downstream (by assertion in the abstract). What the papers control is the middle.

This is an arXiv-declared corpus of 18 mechanism claims under the 2026-10-19 amendment: no citation filter,
recency-biased relevance sampling, fully enumerated provenance. The numbers describe this corpus and are
reported with their disagreement rates; they are not a census of the field, and the paper must say so.

## Provenance chain (one line)

frozen protocol -> arXiv amendment (owner instruction, dated) -> pinned snapshot `e73f72f5...` -> draw
(18, in 15-25) -> adjudication (7+1 replacements, every reason logged) -> 18 PDFs hash-pinned -> two coder
sheets (90 rows each, justifications with locations) -> weaker-grade merge (20.0 percent raw disagreement
reported) -> six outputs by script. Nothing transcribed by hand between table and text.
