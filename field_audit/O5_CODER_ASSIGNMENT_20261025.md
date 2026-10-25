# Task assignment: independent human coder (coder H) for a registered evidence audit

Issued: 2026-10-25. Hand this document, together with the coder packet folder, to the coder.
Everything the coder needs is in the packet; this document adds only the task framing, the
effort estimate, and the rules of engagement.

## The task, neutrally stated

You will independently read a set of research papers and grade, for each paper, what evidence
THE PAPER ITSELF supplies at five defined steps of its claim. The grading rules, the five steps
(T1-T5), the grade scale (E0-E4), and the required output format are given verbatim in the
packet file `CODING_INSTRUCTIONS_FROZEN.md` - that document governs; nothing in this assignment
overrides it.

Your grades serve as the independent human check on a measurement pipeline. What that pipeline
produced, and how your grades will compare, is deliberately NOT in your packet: you work without
knowledge of any prior grading, and you will receive the comparison report only after your work
is complete. Your honest independent judgment is the entire value of the exercise - the project
has explicitly committed that your grades may change its conclusions.

## Deliverables

1. `coder_H.csv` - one row per (paper, transition):
   - Stage H1: 16 primary papers x 5 transitions = 80 rows.
   - Stage H2: 42 validation papers x transitions T2, T3, T5 = 126 rows (T1/T4 optional for
     validation papers; record them if the paper makes them obvious, otherwise leave them out -
     this is a stated option, not an omission).
2. `headline_H.csv` - one row per paper: the ONE transition the abstract's improvement claim
   most rests on (16 + 42 rows).
3. Every grade row carries a justification that quotes or cites a specific location (section /
   figure / table) in the paper's text. Rows without location-anchored justifications do not
   pass acceptance.

## Order of work and effort estimate

1. Read `CODING_INSTRUCTIONS_FROZEN.md` twice before grading anything.
2. Stage H1 first (16 papers, all five transitions). Expect roughly 30-60 minutes per paper;
   plan 1-2 days of focused work.
3. Stage H2 second (42 papers, three transitions each). Expect roughly 15-25 minutes per paper;
   plan 1-2 days.
4. Append rows as you finish each paper; never rewrite a row already written. If you split the
   work across days, your sheets carry your progress.

Total: about 206 grade rows plus 58 headline rows. Breaks are fine; blindness is not optional
(see below).

## The blindness rules (binding)

1. Work ONLY from the packet folder. Copy it somewhere convenient if you like, but do not open
   any other file of the project repository, and do not search the repository.
2. The packet contains no prior gradings, no results, and no analysis - by design. Do not ask
   the team what "the AI coders" or "previous passes" concluded; asking ends the independence
   that makes your pass worth doing, and the team will refuse to answer.
3. Questions are welcome only about the INSTRUCTIONS (what a transition means, how to handle an
   edge case) - address them to the project lead, who will answer from the frozen rules without
   disclosing any expectation.
4. Do not look up the papers' citation counts, reviews, or discussions while grading; grade the
   paper in front of you, from its own text.

## Acceptance criteria (checked mechanically on return)

- Row counts complete (80 + 126 grade rows; 16 + 42 headline rows), no duplicate (paper,
  transition) pairs, no missing cells.
- Grade vocabulary respected (E0/E1/E2 in-paper; E0/E3/E4 external; scope_match only on T5).
- Every justification anchored to a location; provenance hash of the file you read filled from
  the packet manifest.
- Sheets parse cleanly (the team provides a one-command integrity check and will run it with
  you if anything fails).

## After submission

The lead runs the analysis and returns to you: your raw-reading summary, your agreement with the
pipeline per cell, the grade-transition matrix, and what your pass changed or confirmed. Your
contribution is acknowledged in the project records and, if the work is submitted for
publication, in the human-verification disclosure (authorship terms are a separate conversation
with the lead).
