# Advisor remote-review ruling (2026-10-26): technical closure accepted with rights review

The advisor's latest remote review, relayed by the lead and recorded here as the governing gate
state. Verified on GitHub: commits `db2eff0` and `04b6ec5` accessible; the three repairs
confirmed (F4 residue fixed with the erratum trail retained; H3 agreement labels split into
canonical-rule 51/58 vs historical-committed-map 52/58; the counter-sign flow no longer requires
the lead's local machine). The new verification script's dual-label assertion is acknowledged as
covering the error class the previous round actually missed.

## New finding and ruling: redistribution-rights review

The committed full-text layers (e.g. 1505.07814v2, IEEE copyright notice in text) raise a
third-party redistribution question: arXiv's default non-exclusive license does not grant
third-party re-publication rights. Ruling: until the per-paper licenses are confirmed, "uploaded
to GitHub" must not be treated as a rights-cleared public evidence package; for texts without
clear permission, retain version, source URL, SHA-256 and audit results and let authorized
verifiers fetch from the original source; if public texts are withdrawn, check whether git
history still exposes them.
-> **Executed:** `RIGHTS_REVIEW_20261026.md` (visibility finding: repo PUBLIC; license audit
36 non-exclusive / 17 CC-BY / 4 CC-BY-NC-ND / 1 CC-BY-SA; remediation commit removes
non-permissive texts and primary PDFs from HEAD, keeps permissive texts with attribution and
both manifests, adds the fetch-and-verify script; history-decision options recorded).

## Doc-sync item (as ruled, no science impact)

The F4 record's verification note said "three assertions" while the script and the counter-sign
addendum use four. -> Fixed (four, with the fourth's purpose stated).

## Gate state: TECHNICAL_CLOSURE_ACCEPTED_WITH_RIGHTS_REVIEW

| item | state |
| --- | --- |
| F4/H3 canonical-label repairs | accepted (remote-verified) |
| Third-party clone reproduction flow | accepted (verified per report) |
| Public evidence-package rights review | audit done; remediation executed; repo-visibility action + history decision open (owner) |
| O-5 / O-6 human signatures | open |
| Core-narrative ruling | pending the advisor's explicit decision |
| NMI Article | NOT SUBMISSION_READY |

## Standing scientific instruction (the advisor's emphasis, restated)

The fact that coder H's raw reading reverses the primary-corpus T2/T3 asymmetry has not gone
away. The final advisor ruling must make the manuscript present this explicitly: the
AI-weaker-merge result may NOT be described as unconditionally confirmed by human raw coding.
The project remains supported for NMI Article; no new routine experiments are needed - what is
needed is that the final paper faithfully presents the independent human judgment, the
sensitivity of mechanism-evidence definitions, and the reproducible evidence chain.
