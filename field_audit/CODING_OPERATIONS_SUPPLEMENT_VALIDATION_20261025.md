# Coding operations supplement - validation corpus round (2026-10-25)

`CODING_INSTRUCTIONS_FROZEN.md` (2026-10-19) applies VERBATIM and UNEDITED to this round; this
supplement changes only the materials, the output paths, and the round scope, exactly as
`CODING_OPERATIONS_SUPPLEMENT_20261023.md` did for the final-corpus round. Where this supplement
and the frozen instructions differ on a material path or count, this supplement governs the
mechanics and the frozen text governs the grading rules.

## Materials (replaces the frozen document's "Your materials")

1. `field_audit/corpus_validation_v2_adjudicated.csv` - the 42 audited claims
   (arxiv_id_version is the claim_id; band, family, category, record_role included).
2. `field_audit/pinned_validation_20261025/texts/<arxiv_id_version>.txt` - the pinned full-text
   layer of every claim. Hashes: `field_audit/pinned_validation_20261025/FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv`
   (column `text_sha256` is the provenance hash for this round; the PDF hashes are alongside for
   audit). All quotes must come from these text files (cite by section/figure/table markers as
   they appear in the text layer).
3. `field_audit/AUDIT_PREREGISTRATION_v1_FROZEN.md` - the protocol (unchanged).

## Scope of this round

- E-grade layer ONLY: one row per (claim, transition), 42 x 5 = 210 rows, both the in-paper and
  external columns of the frozen sheet, plus the headline map (42 rows).
- NO reportability (R) rows this round - out of scope by the frozen validation protocol
  (`VALIDATION_RESUMPTION_20261025.md` section 4). If you find yourself wanting to fill an R
  sheet, stop: it does not exist this round.
- Coder identity convention: you are coder A or coder B as told in your dispatch; the sheet's
  `coder` column carries that letter; `round` = 1.

## Outputs (exact paths and header)

1. `field_audit/CODING_sheets_validation/coder_<ID>.csv` - header exactly:
   `claim_id,coder,transition,in_paper_grade,external_evidence_grade,external_citation_verified_route,scope_match,justification_quote,provenance_file,provenance_sha256,round,note`
   (identical column semantics to the frozen template; `provenance_file` =
   `field_audit/pinned_validation_20261025/texts/<aid>.txt`; `provenance_sha256` = the row's
   `text_sha256` from the manifest; `scope_match` only on T5 rows).
2. `field_audit/CODING_sheets_validation/headline_<ID>.csv` - header exactly:
   `claim_id,headline_transition` (42 rows).

Incremental-write discipline (kill-safe, as practiced on the final corpus): write the header
first, append one claim's five rows after each claim is graded, and flush. On any restart, read
your own sheet, continue after the last claim_id present, never rewrite existing rows. Work in
corpus file order.
