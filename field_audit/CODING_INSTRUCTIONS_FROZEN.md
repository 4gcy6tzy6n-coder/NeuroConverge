# Frozen coding instructions (both coders receive this document verbatim; 2026-10-19)

You are an independent coder on a registered evidence audit. You have no access to the other coder's work, to
any workspace code, or to any prior grading. Your judgments are yours alone; disagreement is expected and
measured, not penalized.

## Your materials

1. `field_audit/corpus_arxiv_adjudicated_v1.csv` - the 18 audited claims (id, title, family, category).
2. `field_audit/fulltexts/<arxiv_id_version>.pdf` - the pinned full text of every claim (hashes in
   `fulltexts/PINNING_MANIFEST.csv`). All quotes must come from these files.
3. `field_audit/AUDIT_PREREGISTRATION_v1_FROZEN.md` - the protocol (sections 2, 4, 5 define your task).

## What you grade, per claim

Decompose each claim into the five transitions and grade each with the evidence scale:

| id | transition | the question you answer |
| --- | --- | --- |
| T1 | structure -> computation | does the paper establish that the cited biological structure performs the cited computation (its own evidence, or citation)? |
| T2 | computation -> correspondence | does the artificial component instantiate that computation under a stated mapping, or only resemble it? |
| T3 | correspondence -> utility | is the claimed performance gain attributable to the correspondence rather than to capacity, tuning or baselines? |
| T4 | utility -> generality | does the gain survive task families, scales and ablations beyond the demonstrated setting? |
| T5 | any -> claimed scope | does the abstract's claim match the evidence's scope? (scope_match: match / mismatch) |

| grade | meaning |
| --- | --- |
| E0 | no evidence in the paper; assertion or citation only |
| E1 | suggestive evidence in the paper (one setting, no controls named for this transition) |
| E2 | controlled evidence in the paper (this transition has its own comparison or ablation) |
| E3 | independent evidence exists elsewhere in the literature (you must cite it; if you cannot verify a specific source, do not claim E3) |
| E4 | independent replication or adversarial evaluation exists (same requirement) |

Record `in_paper_grade` (E0-E2, the paper's own evidence strength for this transition) and
`external_evidence_grade` (E0 if none you can verify, or E3/E4 with the citation in the note). E3/E4 claims
without a verifiable citation in your note are invalid and will be downgraded to E0.

## Rules that keep the audit honest

- Grade what the paper shows, not what you believe: an E0 transition may be true; the finding is about
  evidence. Never word a justification as "X is false".
- The justification (2-3 lines) must quote or cite the specific location (section, figure, table, page).
- If a transition is not applicable because the paper names no biological mechanism for it, grade E0 and say
  so in the note - do not skip rows.
- Headline map: for each claim, name the ONE transition (T1-T5) the abstract's improvement claim most rests
  on. Judgment call; record it in the headline file.
- You are grading the paper's claims about its own artifact. For platform/survey-free corpus items only -
  all 18 adjudicated claims make mechanism claims, so this should not arise; if one does not after reading,
  flag it in the note rather than inventing grades.

## Your outputs (exact filenames; exact header of CODING_SHEET_TEMPLATE.csv)

1. `field_audit/CODING_sheets/coder_<ID>.csv` - one row per (claim, transition), 18 x 5 = 90 rows, columns:
   claim_id, coder, transition, in_paper_grade, external_evidence_grade,
   external_citation_verified_route, scope_match, justification_quote, provenance_file, provenance_sha256,
   round, note. `provenance_sha256` from PINNING_MANIFEST.csv; `round` = 1; `scope_match` only on T5 rows.
   `claim_id` = the arxiv_id_version from the corpus csv.
2. `field_audit/CODING_sheets/headline_<ID>.csv` - columns claim_id, headline_transition (18 rows).

Work claim by claim. Do not communicate with anyone. When both files are written, your task is done.
