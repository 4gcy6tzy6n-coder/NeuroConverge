# Venue decision record: NMI Article (zhengkan), Analysis type abandoned

Date of decision: 2026-10-25 (owner instruction received 2026-10-24 late evening CST).
Recording session: the NMI session acting under the 2026-10-19 full-decision-rights grant.
This is a dated amendment record. No frozen document is edited by this record.

## Owner instruction (verbatim)

"旗舰正刊，要不也就是NMI正刊而不是analysis,放弃analysis，我们专向正刊"

(Flagship regular research journal - here: the NMI regular Article type rather than the
Analysis article type. Abandon Analysis; we pivot to the regular Article type.)

This follows the same session's earlier instruction to re-check the manuscript with the
nature skill against regular-journal rather than Analysis requirements
(nature-skills repository, github.com/Yuan1z0825/nature-skills; flagship statistical
audit already executed and recorded in `NATURE_FLAGSHIP_STAT_AUDIT_2026-10-25.md`).

## Decision

1. **Target article type: Nature Machine Intelligence Article** (regular research article,
   "substantial novel research study").
2. **The Analysis article type is abandoned** as the submission target.
3. Active format comparator: `NMI_ARTICLE_FORMAT_REQUIREMENTS_2026-10-25.md` (frozen
   2026-10-25 before any Article-mode format claim; sources and verbatim numbers there).

## What this supersedes (items of the 2026-10-23 readiness review's format lock)

The 10-23 review locked the Analysis type and an Analysis-type title. Superseded items:

- Article-type choice (was: Analysis).
- Title. Was: "Biological-to-artificial intelligence transfer: an analysis of evidence
  supporting mechanistic claims". Adopted for the Article draft:
  **"Biological-to-artificial intelligence transfer: a transition-level audit of evidence
  supporting mechanistic claims"** (minimal diff; keeps the locked framing phrase and
  replaces "an analysis of" - which named the abandoned article type - with the
  instrument-forward wording). The owner may veto or amend in the owner package review.

Items NOT superseded (unchanged and still binding): all content findings, all frozen
numbers and instruments, the forbidden-wording list, the disclosure requirements, the
word/display/reference caps (identical between the two types except the abstract lower
bound, which the Article type relaxes), the kill-rule reporting, and every artifact
commit. The 10-23 review document itself stands unedited as history.

## Compliance position of the current manuscript (measured against the frozen record)

Checked by `field_audit/nmi_format_check.py` in Article mode after this record:

- Main text: 2,937 words / 3,500 limit (unchanged comparator; measured by the Article-mode
  checker after this record, header included as in the prior convention).
- Abstract: 145 words / up to 150 (Article bound; the Analysis lower bound of 100 no
  longer binds).
- Display items: 6 figures / 6.
- References: 18 / guideline 50.
- Structure: Results and Methods carry topical subheadings; the Discussion carries none;
  the working draft's `## Introduction` heading is draft scaffolding to be removed in the
  submission build (checker emits WARN, not FAIL).
- Article framing basis (the one substantive requirement change): the paper presents a
  preregistered, hash-bound measurement instrument and its first dual-coded measurements -
  a novel research study in science-of-science methodology - rather than a re-analysis of
  an existing dataset. No content rewrite is required by the pivot; the title change above
  and the framing already present in Introduction/Methods carry the Article positioning.

## Residual owner-side items touched by this pivot

- Title veto window (above).
- Cover letter (required at submission; lists importance/fit, related manuscripts, prior
  editor contact) - owner-side.
- Reporting Summary applicability at submission time (the NMI pages fetched 2026-10-25
  state no mandatory form for this journal; the submission system's prompts decide -
  AUTHOR_INPUT_NEEDED, carried in the owner package).
- Author list, affiliations, data/code availability statements (already owner-side).
