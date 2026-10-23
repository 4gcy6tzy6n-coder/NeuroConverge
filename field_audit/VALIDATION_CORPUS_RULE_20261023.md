# Validation corpus rule (frozen 2026-10-23, before the validation draw ran)

**Authority.** Hardening plan section 4 (P0-3), per the project lead's 2026-10-23 review. The validation
corpus exists to test whether the pilot's findings survive an independent, year-stratified, larger sample.
Frozen before any validation draw output existed.

| parameter | frozen value |
| --- | --- |
| source | the SAME pinned snapshot as the pilot (`corpus_draw_arxiv_v1.snapshot.jsonl`, sha256 `e73f72f5...`) - no new fetches; the pilot's provenance chain carries the validation unchanged |
| disjointness | the pilot's 18 adjudicated claims are EXCLUDED from the validation pool - the two corpora share nothing, so the validation is genuinely independent |
| size | target 60; acceptance 45-75 |
| year stratification | three bands - 2015-2019, 2020-2022, 2023-2026 - with **20 per band target, >= 8 per band required** (the relevance order's recency bias is corrected here, by construction) |
| caps (within band) | family <= 4, primary category <= 6 |
| ranking | fetch_rank order within band (arXiv relevance, as amended) |
| claim-type criterion, exclusions, replacements, uncodable rule | unchanged from the frozen protocol + arXiv amendment; replacements fire within (band, family, category) |
| adjudication | same procedure as the pilot, by the lead, every reason logged |
| coding | two isolated-context coders on text-extracted pinned full texts (pdftotext, derived .txt hash-pinned beside the PDF); identical frozen instructions |
| inference | pilot numbers become pilot numbers everywhere; field-level wording, if any, requires the validation corpus and its kill-rule check |

## Execution record

(appended when the draw and adjudication run)

## Execution record (draw, same day)

60-free draw from the pinned snapshot: 60 claims, 20/20/20 across the three bands, pilot-disjoint, family cap 4/band, category cap 6/band, ranked by fetch_rank within band. `corpus_validation_draw_v1.csv` is the pre-adjudication pool; claim-type adjudication with logged reasons is the next step, then text-extracted pinning and the two-coder pass.
