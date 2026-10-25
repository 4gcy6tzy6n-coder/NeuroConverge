# Public-distribution rights review (2026-10-26)

Authority: the advisor's remote review (2026-10-26) flagged that committed full-text layers may
infringe third-party redistribution rights, and set the gate state
`TECHNICAL_CLOSURE_ACCEPTED_WITH_RIGHTS_REVIEW`. This record executes the rights review and
remediation. It concerns publication compliance only - no result, grade, or hash in the audit
chain changes.

## Findings

1. **The repository is PUBLIC.** HTML probe `https://github.com/4gcy6tzy6n-coder/NeuroConverge`
   returns 200 unauthenticated. Every committed full text was therefore publicly redistributable
   until this review.
2. **License audit (58 papers; `ARXIV_LICENSE_AUDIT_20261026.csv`, fetched from arXiv abstract
   pages 2026-10-26):** 36 papers under the default arXiv **non-exclusive-distrib 1.0** license
   (no third-party redistribution right), 17 under **CC BY 4.0**, 4 under **CC BY-NC-ND 4.0**
   (held for review: no-derivatives makes even a format shift questionable), 1 under **CC BY-SA
   4.0**. Spot confirmation: 1505.07814 (the advisor's example) carries the IEEE copyright notice
   in its own text and the non-exclusive license on its abs page.
3. **Exposure inventory at HEAD:** 42 validation text layers (committed `04b6ec5`) and 21 primary
   PDFs (`field_audit/fulltexts/`, tracked since the pilot). Both removed from HEAD in the
   remediation commit below; **git history still contains them** (see the history-decision item).

## Remediation executed (this commit)

- Removed from HEAD: the 27 validation text layers of non-permissive papers (36 + 4 non-permissive
  across both corpora; 15 permissive validation texts remain), and all 21 primary PDFs.
- Kept at HEAD: the 15 CC-BY/CC-BY-SA validation text layers with
  `pinned_validation_20261025/ATTRIBUTION.md` (per-paper source + license attribution), both
  download manifests (the hash anchors), and every derived artifact (grades, adjudications,
  statistics, records).
- New `fetch_pinned_from_arxiv.py`: manifest-driven, resume-safe, sha-verified download of the
  non-redistributed files from arXiv for LOCAL VERIFICATION USE. Verified: a re-downloaded PDF
  (2207.08533v2, 18,566,354 bytes) matches the pinned sha256 exactly - arXiv versioned PDFs are
  byte-stable, so fetch-and-verify restores the full evidence chain for any authorized verifier.
- Verifier impact: the clean-clone chain gains one step (`python3 field_audit/fetch_pinned_from_
  arxiv.py`, network, ~4 minutes) before the full-text-dependent checks
  (`run_final_scoring_20261024.py`, `robustness_survey_exclusion_20261025.py`, quote checks
  beyond the committed permissive texts). Everything else remains clone-only.

## Open decisions (owner/advisor)

1. **Repository visibility (recommended immediate action):** set the GitHub repository to private
   while non-permissive files remain in its git history. This is a two-click owner action and
   stops ongoing public redistribution without touching the working tree or the verification
   chain.
2. **History exposure:** the removed files remain retrievable from git history. Options:
   (a) private repo makes this moot for access; (b) history rewrite (invalidates the advisor's
   cited commit links; requires force-push coordination); (c) build the eventual public evidence
   deposit as a FRESH, curated repository (code + manifests + metadata + grades + permissively
   licensed texts only) rather than ever publishing this working history. The lead's
   recommendation is (c), with (a) executed immediately.
3. **Re-inclusion:** if the owner later confirms permission for any non-permissive paper (or the
   NC-ND four), its text/PDF may re-enter HEAD with an attribution line.
