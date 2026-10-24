# Correction ledger, 2026-10-24 (opened with entry C-1)

Mechanism per the B3 binding v1 text: any change to sealed coder rows uses new round files and this
ledger, and counts against the two-round bound. Originals are preserved byte-for-byte; corrections
are always new files plus a dated entry here.

## C-1 - coder B reportability sheet: source hash rebinding (2026-10-24)

- **Defect.** All 176 rows of `coder_B_R.csv` declare, in `source_file_sha256`, the SHA-256 of the
  extracted text layer `fulltexts_txt/<arxiv_id_version>.txt`, not the SHA-256 of the pinned target
  paper `fulltexts/<arxiv_id_version>.pdf`. Verified 16/16 claims: the declared digest equals the
  text file's digest in every case. The bound source registry (V1, and the V2 successor) carries the
  PDF digest as `target_sha256`; the bound scorer refuses any TARGET row whose digest differs.
  Coder B's own evidence sheet (`coder_B_E.csv`) uses the PDF digests and is unaffected; coder A's
  reportability sheet is unaffected (0 rows).
- **Defect class.** Mechanical source-binding error in one field. The statuses, evidence pointers,
  item IDs, roles and notes are untouched by the correction; no judgment changes.
- **Action.** `coder_B_R_corrected_20261024.csv` written as a new file: the same 176 rows with
  `source_file_sha256` replaced by the claim's registry target digest (176 fields rewritten, no
  other byte). The original `coder_B_R.csv` is retained unmodified. Downstream scoring consumes the
  corrected file for coder B.
- **Why the text layer was hashable at all.** The text layers are derived artifacts of the pinned
  PDFs (extraction committed 2026-10-24, `22bcb2e`); they are not registered sources. A coder
  quoting from the text layer quotes the target paper's content; the bound schema requires the row
  to bind the target paper's digest, which is the PDF's.
- **Disclosure.** This correction was applied by the lead (2026-10-19 authority record; same-model
  limitation disclosed; human supersedure applies). It is recorded here rather than silently, and
  the disagreement statistics are computed from statuses, which it does not touch.
