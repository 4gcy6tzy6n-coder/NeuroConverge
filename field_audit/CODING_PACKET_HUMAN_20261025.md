# Human coder packet - README (coder-facing; read this first)

Welcome, and thank you. You are the independent human coder (coder H) for a registered evidence
audit of bio-to-AI transfer claims. Your grades are the independence test of the entire project.

## What you have (and ALL you have)

1. `CODING_INSTRUCTIONS_FROZEN.md` - your grading rules. Follow it verbatim; it defines the five
   transitions (T1-T5), the evidence grades (E0-E4), the in-paper vs external columns, the honesty
   rules, and the quote requirements. Where this README and that document differ, THAT document
   governs grading.
2. Pinned full texts:
   - Primary corpus (16 papers): `pinned_fulltext_20261020/` (the PDFs; hashes in
     `pinned_fulltext_20261020/FULLTEXT_DOWNLOAD_MANIFEST_20261020.csv`).
   - Validation corpus (42 papers): `pinned_validation_20261025/texts/` (text layers; hashes in
     `pinned_validation_20261025/FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv`, column text_sha256).
3. Empty output sheets: `CODING_sheets_human/coder_H.csv` and `CODING_sheets_human/headline_H.csv`.

## Your work, in order

- STAGE H1 first: grade all 16 primary-corpus papers, all five transitions each (80 rows), plus
  one headline transition per paper (16 rows in headline_H.csv). Work claim by claim in the order
  the papers appear in `pinned_fulltext_20261020/FULLTEXT_DOWNLOAD_MANIFEST_20261020.csv`.
- STAGE H2 second: grade the validation corpus on transitions T2, T3, T5 only (42 x 3 = 126
  rows), plus one headline transition per paper (42 rows). You may also record T1/T4 when the
  paper makes them obvious - optional, your choice, never required.
- Append rows as you finish each paper and save. Never rewrite rows already written. If you must
  stop and resume, read your own sheet and continue after the last claim present.

## Sheet columns (already in the header; semantics in the frozen instructions)

claim_id (the arXiv id WITH version, e.g. 2207.08533v2 - it is also the pdf/txt filename),
coder (write H), transition (T1..T5), in_paper_grade (E0/E1/E2), external_evidence_grade (E0, or
E3/E4 only if you can cite and verify the source - else E0),
external_citation_verified_route (empty unless E3/E4), scope_match (only on T5 rows: match or
mismatch), justification_quote (quote or cite the specific section/figure/table), provenance_file
(the relative path of the text/PDF you read), provenance_sha256 (the hash of YOUR file from the
manifest), round (write 1), note (anything else; use it for E3/E4 citations).

## Integrity rules

- Grade what the paper shows, not what you believe. An E0 transition may be true; the audit is
  about evidence, not truth.
- Never look at any other file in the repository. In particular, there are files with prior
  (machine) gradings somewhere in this project: you will not see them, and asking for them ends
  the independence of this test.
- If a paper seems to be a survey with no own system, grade it by the same rules and say so in
  the note.
- Questions about the INSTRUCTIONS (not about expected results) go to the project lead.

## After you finish

Tell the lead "H1 complete" and/or "H2 complete". The lead will run the integrity check and the
analysis; you will get the comparison report when it is ready.
