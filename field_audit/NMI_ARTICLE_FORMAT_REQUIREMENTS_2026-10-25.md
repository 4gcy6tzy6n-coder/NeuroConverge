# NMI Article-type format requirements (frozen record)

Date frozen: 2026-10-25 (fetched from nature.com 2026-10-25, 00:45-01:05 CST).
Purpose: the frozen format comparator for the manuscript after the venue pivot to the
Nature Machine Intelligence **Article** type (see `VENUE_DECISION_20261025.md`).
This record freezes the requirements BEFORE any Article-mode format claim is made about the
manuscript (freeze-before-measure). It supersedes the Analysis-type format numbers as the
active comparator; the Analysis numbers are retained below for contrast and for the historical
10-23 review, which is not edited.

## Sources (fetched and archived to /tmp during this session)

- Content types (numbers below): `https://www.nature.com/natmachintell/content`
  (reached via the submission-guidelines hub "Content types" link; the /gta/content-types
  URL is a 404).
- Formatting your initial submission: `https://www.nature.com/natmachintell/submission-guidelines/initial-formatting`
- AIP and formatting (production-stage rules): `https://www.nature.com/natmachintell/submission-guidelines/aip-and-formatting`
- Preparing your material (submission completeness): `https://www.nature.com/natmachintell/submission-guidelines/preparing-your-submission`

## Article type (verbatim requirements, quoted from the content-types page)

"An Article is a substantial novel research study, with a complex story often involving
several techniques or approaches."

Format:

- Main text - up to 3,500 words, excluding abstract, Methods, references and figure legends.
- Abstract - up to 150 words, unreferenced.
- Display items - up to 6 items (figures and/or tables).
- Article should be divided as follows:
  - Introduction (without heading)
  - Results
  - Discussion
  - Methods.
- Results and Methods should be divided by topical subheadings; the Discussion does not
  contain subheadings.
- References - as a guideline, we typically recommend up to 50.
- Articles include received/accepted dates.
- Articles may be accompanied by supplementary information.
- Articles are peer reviewed.

## Analysis type (contrast; the format we previously targeted)

"An Analysis is a new analysis of existing data or describes new data obtained in a comparative
analysis that leads to novel and arresting conclusions of importance to a broad audience."

- Main text - up to 3,500 words (excluding abstract, online Methods, references and figure legends).
- Abstract - 100-150 words, unreferenced.
- Display items - up to 6 items (figures and/or tables).
- Same four-part structure and the same subheading rule.
- References - as a guideline, we typically recommend up to 50.

## Deltas that matter for our manuscript

1. **Numbers are identical except the abstract lower bound** (Analysis 100-150; Article
   "up to 150"). Our abstract (145 words) satisfies both. The binding constraints
   (3500 main words, 6 display items, ~50 references) do not change.
2. **Content definition changes**: Article must be framed as "a substantial novel research
   study", not "a new analysis of existing data". Our framing basis: the contribution is a
   frozen, preregistered measurement instrument (transition taxonomy, grade scale, item-level
   reportability checklist, hash-bound scorer, two-coder coding with adjudication) plus its
   first measurements on a frozen corpus - a methods study producing new data, not a re-analysis
   of one existing dataset.
3. **Structure is identical** in all respects but is now Article-binding: Introduction without
   heading; Results and Methods under topical subheadings; Discussion without subheadings.
   The working draft carries an `## Introduction` heading as draft scaffolding; it is removed
   in the submission build (recorded in the venue decision, checked with a WARN not a FAIL).

## Submission-completeness items (Preparing your material page, applies to all types)

- Manuscript file must contain: author names and affiliations (or in the cover letter under
  double-anonymized review); a detailed description of findings with sufficient methods
  information for replication; a reference list; optional Extended Data (max 10 items).
- Methods sections of all original research papers appear in all online versions.
- Cover letter required: importance of the work and fit for the NMI readership; disclosure of
  related manuscripts under consideration; whether an editor was previously consulted;
  double-anonymized author info if applicable.
- Supplementary Information optional, sent to peer reviewers; single combined PDF plus
  csv/Excel for complex tables.
- LLMs do not satisfy authorship criteria; LLM use must be documented in the Methods section
  (our AI-assistance disclosure already does this).
- Data and code: the AIP page requires the paper to "meet our standards for the reporting of
  data and code" at acceptance; data/code availability statements remain owner-side slots.
- Reporting Summary: NMI's own submission pages fetched above do not state a mandatory
  reporting-summary form for this journal (unlike flagship Nature). Applicability remains
  AUTHOR_INPUT_NEEDED at submission time (owner checks the submission system's prompts).

## Production-stage rules already noted (AIP page, for the accepted version)

- Final submission in Word or TeX/LaTeX only (no PDF).
- Numerical references only; references numbered in order: main text, Methods, data
  availability, tables, figure legends, boxes, Extended Data.
- Article titles required in references for long-form types (already our style).
- Figures: 300 dpi minimum, max width 180 mm, 5-7 pt sans-serif labels, error bars defined,
  n numbers and statistical tests stated in legends.
- Up to 10 Extended Data display items permitted; source data encouraged.
