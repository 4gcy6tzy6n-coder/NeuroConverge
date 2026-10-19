# Amendment 2026-10-19: the corpus draw's data source becomes the arXiv API

**Authority.** The owner's data-source decision, relayed by the project lead on 2026-10-19 as "直接看arxiv就行"
(just use arXiv directly), issued after the OpenAlex route was recorded blocked on an API key
(`DRAW_ATTEMPT_LOG.md`, 2026-10-18 preflight). This is a dated amendment under the frozen protocol's own
section-10 scope-creep rule: `AUDIT_PREREGISTRATION_v1_FROZEN.md` is left as written, and this document
changes only what it names. Nothing else in the protocol moves.

## What changes (protocol section 3 only)

| item | frozen (OpenAlex/Scopus) | amended (arXiv) |
| --- | --- | --- |
| data source | OpenAlex API (key required for cursor paging) or Scopus export | the arXiv API (`export.arxiv.org/api/query`, free, no key, HTTPS) |
| candidate ranking | citation count | arXiv relevance order (the API's own `sortBy=relevance`), recorded in the manifest |
| citation floor / decile | 100 citations, top decile (tier 3) | **removed** - the arXiv API carries no citation data |
| stratification cap 1 | at most 5 per venue | at most 5 per arXiv primary category |
| stratification cap 2 | at most 3 per mechanism family | unchanged |
| window | 2015-01-01 to 2026-09-30 | unchanged (on the v1 `published` date) |
| claim-type criterion, keyword lists | as committed | **unchanged** - the same BIO_TERMS/AI_TERMS lists, the AND enforced locally on real title+abstract text |
| target size, acceptance range, replacement mechanics | 20, 15-25, next-in-stratum | unchanged (stratum = mechanism family x primary category, ranked by fetch order) |
| dual-draw check | scriptable, hash-pinned snapshot | unchanged - the raw Atom responses are the pinned snapshot, hashed and listed by URL in the manifest |

## Character change, stated plainly

The corpus is now **claims declared on arXiv** - preprints, including the preprint versions of later-published
work - not "high-impact published claims". Every downstream wording in the paper must say "arXiv-declared"
and the audit question reads "which inference transitions in arXiv-visible bio-to-AI transfer claims lack
independent empirical support". The advantage is real and recorded: **every corpus item's full text is openly
pinnable**, so protocol section 5's provenance requirement (quotes from a hash-pinned full text) is
satisfiable for every claim - under the OpenAlex venue tiers it would have collided with paywalls at tier 1.
The risk is also recorded: no citation filter means the corpus skews toward visibility rather than measured
impact, and the sensitivity analyses of protocol section 6 gain work to do (the two alternative selection
rules are re-read as category-composition alternatives, stated in the draw manifest when run).

## What does not change

The transition taxonomy T1-T5, the evidence grades E0-E4, the coding protocol and dual-coder requirement
(P4), the six frozen outputs, the statistics script's contract, the stop rules and the kill rule, the
reporting checklist, and the schedule mechanics: **the 8-week clock still starts at the commit of the draw
output, not at this amendment.**

## Execution record

(appended below when the draw runs)

## Execution record (2026-10-19)

`python3 -B draw_arxiv.py --query` ran under this amendment: 22 requests (one transient SSL reset recovered by
the documented retry), 3246 deduplicated works in the pinned snapshot
(`corpus_draw_arxiv_v1.snapshot.jsonl`, sha256 `e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee`),
mechanical filters and stratified caps as amended, **18 claims selected - inside the frozen acceptance range
15-25**. Composition, recorded for the paper's methods section: exactly 3 per mechanism family (the family cap
bound), 8 primary categories (cs.AI 4, cs.NE 4, others 1-3; the category cap never exceeded), publication
years 2017-2026 with 16 of 18 from 2021 on - the relevance-order ranking's recency bias, stated here rather
than smoothed away. Every selected row carries `needs_adjudication: claim-type`; the per-candidate
adjudication log with reasons is the next phase, before any coding begins (P4).

**The commit that carries `corpus_draw_arxiv_v1.csv` is the corpus freeze; the 8-week clock of protocol
section 10 starts at that commit (2026-10-19; schedule bound lands 2026-12-14).**
