# R3 reviewer report, frozen as returned

**Emphasis brief: reproducibility, provenance and adversarial reading.** **Frozen copy sha256
`a8189843c5f0459bca6db6b104df6c121de9c664480a1a989d0835084a65a1b4`, 449 lines, captured by the reviewer at
2026-10-10 11:15:14.** **The reviewer named the revision it reviewed, which R2 did not and which the protocol
requires.**

**Headline as delivered: one blocking Major Concern (R3-M1, the paper's own package is not reproducible by a
reader), six further Major Concerns, eleven Minor Comments. Posture: major revision, with the central
observation publishable and the provenance apparatus not.**

---

## What the reviewer verified independently, and what that establishes

**This section is placed first because it is the only independent verification any of the three reviews
performed, and it came back clean at the artifact layer.**

* **Recomputed the sha256 of all twenty-two artifacts named in `FIGURE_SOURCE_DATA.json` against the prefixes
  recorded there. Twenty-two of twenty-two match, none missing.**
* **Order-axis table matches `RESULT_order_axis.json` to four decimals on all six cells: 0.0958, 0.9685,
  -0.0958, 0.1192, 0.1192, 0.1133.**
* **Section 2.2 isolated sizes match `RESULT_joint_grid_verified.json` at the 24-volume window: -0.3462,
  +0.3378, +0.5706.**
* **Like-for-like block matches `RESULT_fig6.json` exactly, including pair counts 3,540 and 1,560, the 23
  shared cell names, r = 0.0368, r = -0.0064 and the cross-animal bound 0.2084.**
* **Measurement-error range is the union now claimed: 38.7 to 57.1 from the eight-specification grid and 17.3
  from the per-event-weighted arm.**
* **The 5.5 and 46.0 ends of the pair-specific range are the WT sweep at one and ten minimum animals.**
* **The 2.541 GB budget matches `D541_ROUTE_CLOSURE.json` (2.541492652) and the ledger in
  `GENERALISATION_ROUTE_CLOSED.md`.**
* **Confirmed the four superseded-interpretation banners exist and that `CORPUS_INDEX.md` section 2 lists the
  same four documents the draft says carry them.**

**Resolved four DOIs against Crossref, one against DataCite, one against Europe PMC and OSF.**

## Major Concerns

### R3-M1, the paper's own package is not reproducible, BLOCKING YES

**Claim pointer.** "All scripts, result JSONs and the figure source data are committed" (Methods, Software),
and the first line of the draft, "Every number below is committed under `v2/wp3_results/` with its own
provenance section."

**Evidence pointer.** `v2/wp1_data/PATH_LAYOUT.md` sections 1, 2, 3, 5 and 6, and the repository. PATH_LAYOUT
records that twenty-seven of twenty-nine scripts read from absolute paths under `/tmp`, that `/tmp` "is cleared
on reboot, and will never exist on a reviewer's machine", and that the scripts "are therefore not runnable by
anyone but their author". **The reviewer counted the current tree and found forty-nine of the fifty-one
committed analysis scripts under `v2/wp3_results` contain `/tmp` path literals, so the recorded ratio is stale
as well.** PATH_LAYOUT section 6 states that making the scripts path-portable "is not done". Section 3 records
no checksum for the connectome tables and "not verified" for their licence. Section 5 step 3 states of the
NemaNode `neurons.json` input that it "cannot be completed from the recorded sources alone". Section 4 records
its redistribution licence as UNKNOWN. **The pipeline being audited is NEVER IDENTIFIED IN THE MANUSCRIPT AT
ALL**; the only recorded locator is `github.com/leiferlab/pumpprobe` in `WIRESHIFT_STAGE2_WT_AUDIT.md`, with no
version or commit, and no copy is vendored. Section 2.7's acceptance criterion is agreement "against the code's
own intermediate values", which cannot be re-run without the exact revision. **There is no data or code
availability statement anywhere in the draft**, while PATH_LAYOUT section 4 states the exports carry "no licence
permitting redistribution" and "a data deposit is currently not authorised".

**Concern.** A competent reader cannot re-derive the headline numbers from the repository alone. They can verify
the JSONs contain the quoted numbers, which the reviewer did and which holds. They cannot verify the JSONs
correctly re-implement the source pipeline.

**Why it matters.** The central empirical claim is that seven dimensions move the estimate by measured amounts.
If the production chain is not reproducible, those claims rest on unverifiable computation, and the closing
prescription is not met by the paper's own package. **This is the one concern that blocks the case, because the
draft's own first line is a promise it does not keep.**

**Resolution test.** Name the audited pipeline and a pinned commit in Methods. Record a checksum and version for
the connectome tables. Supply a locator and licence for `neurons.json` or drop the cell-class-dependent numbers.
Provide a `paths.py` so the committed scripts run against a documented layout. Add a data and code availability
statement.

### R3-M2, figure provenance, NON-BLOCKING

**Claim pointer.** "All six are rendered by `../figures/make_figures.py`, which reads each series from the
committed result artifact named below and retypes nothing."

**Concern.** Figure 1's values are literals in the script; the script never opens `SPECIFICATION_LEDGER.md`,
which the Figure 1 legend names. Figure 6 is derived by a regex sweep over the whole tree, not by reading
`CORPUS_INDEX.md`, which its legend names. The `NUM` map stops at "twenty-first". **Only one of the eight
artifacts the legends name is among the twenty-two hashed.**

**Resolution test.** Read Figure 1 from the ledger or the JSON behind it, and Figure 6 from `CORPUS_INDEX.md`,
or correct the legends to name what the script actually reads. Extend `check_figure_values.py` so a literal must
be present in the artifact its own panel names, not merely somewhere in the corpus.

### R3-M3, the defect ledger is stale and mispointed, NON-BLOCKING

**Claim pointer.** "seventeen numbered self-found errors" (Abstract), "The count of such events is seventeen
numbered defects, listed in section 2.7 and in Figure 6" (section 2.8).

**Concern.** `CORPUS_INDEX.md` says seventeen, fifth to twenty-first. `CORRECTION_figure_six_was_invented.md`
says "twenty-second self-found defect" and `CORRECTION_joint_grid_check_does_not_pass.md` says
"twenty-third". The reviewer replicated the Figure 6 scan and it finds exactly seventeen because the `NUM` map
has no entry above twenty-first, **so the two later defects cannot appear in the figure the legend calls the
ledger**. Section 2.8's pointer is wrong independently, because section 2.7's table lists six re-implementation
rounds, not the numbered defects. The same paragraph points at section 2.7 for the five invalid runs, which are
in `CORPUS_INDEX.md` section 4 and `tools/README.md`. **And the ledger calls itself self-found while one of its
own documents attributes a finding to a reviewer.**

### R3-M4, section 2.5 mixes pair sets and the 464 is not a sample-size ratio, NON-BLOCKING

**Concern.** `RESULT_unit_check.json` carries `n_conn` 19247 and `n_unconn` 219824, not 195,809.
**195,809 lives in a different artifact, `RESULT_baseline_conventions.json`, as the `n` of a different
specification.** The line's own correction document states the incompatibility: "its unconnected count is
219,824 against the corpus's 195,809, so the pair sets differ and the two z-scores are not comparable."
**And 464 is the square root of the two counts the sentence itself gives: 19,247 + 195,809 = 215,056, whose
square root is 463.7. It is not a sample-size ratio.** The ratio of pair observations to animals is 1,973, and
the recorded quantity in the artifact is `sqrt_n_eff` 188.135. No result JSON carries 464; it appears only in
the prose of the correction document, stated without a derivation.

### R3-M5, the pair-specific range and the sign come from two grids, and the restriction is misnamed, NON-BLOCKING

**Concern.** `RESULT_variance_decomposition_sweep.json` gives the WT arm 5.5 per cent at K = 1 and 46.0 per
cent at K = 10, and its value at the most permissive level is POSITIVE. The negative values are in a different
artifact, `RESULT_eps_specification_grid.json`, whose varied axis is the READ-OUT and not the restriction.
`CORPUS_INDEX.md` carries yet another live range for the same quantity, "21.6 to 35.5 % when excluded".
**The restriction is also misnamed: the artifact's key is `min_an` and the figure script's own axis label is
"minimum animals per pair", while the manuscript, the Figure 4 legend and the Methods all say
minimum-measurements-per-pair.** The read-out, quoted as moving the share by about 13 points, is never defined.

### R3-M6, the reference verification claim is broader than what was done, NON-BLOCKING

**Concern.** The blanket claim is false for three of nine entries on the section's own recorded method: entries
8 and 9 are data records not run through Crossref, and entry 6's DOI was not retrieved. **The stated rationale,
that a DOI belonging to a different paper is caught, is exactly the check that was not run on the data DOI.**
Resolving `10.17605/OSF.IO/E2SYT` returns a DataCite record with creators Dvali Sophie, Leifer Andrew and Randi
Francesco, title "Neural signal propagation atlas of C. elegans", publisher OSF, year 2022, and an EMPTY rights
list. Entry 6's quoted phrases "is not noise" and "reflects worm individuality" are accurate to the source but
**occur in the article body, not in its abstract**, and the manuscript attributes them to "its abstract". The
DOI the entry says was not retrieved is available: `10.1038/s42003-025-08599-3`, authors Yezerets, Mudrik and
Charles.

### R3-M7, the manuscript claimed to be the audited pipeline's authors, NON-BLOCKING

**Claim pointer.** "The published pipeline's own authors are its most informed possible re-implementers."
**Concern.** The draft carried no author list, no affiliations and no competing-interest statement, and the
sentence asserts an identity that nothing in the reviewed material establishes. **Either it is an undeclared
self-audit or it is false.**

**ADDRESSED AT ROUND 66, before this report was received in full.** **The sentence is rewritten to state that
this line is not the pipeline's author and has no relationship to it beyond reading published code and deposited
data, an authorship and competing-interest section has been added, and reference 8's invented attribution
"Pradhan S, et al." has been replaced with the DataCite record's three creators.**

## Minor Comments, summarized

| ID | Issue |
| --- | --- |
| **R3-m1** | three different counts (three, four, five) describe the same withdrawn-or-narrowed set across the manuscript and `CORPUS_INDEX.md` |
| **R3-m2** | the census's "seventy-six fields in five files" does not reconcile: the per-file counts are 18, 20, 12 and 26 (sum 76) for four files, plus a fifth with 15, summing to 91 |
| **R3-m3** | the restriction is called minimum-MEASUREMENTS-per-pair where the artifact's key is `min_an` and the figure says minimum ANIMALS per pair; the read-out is never defined |
| **R3-m4** | `check_figure_values.py`'s skip path returns exit 0, the same as a pass, and its literal test asks only whether a value appears SOMEWHERE in the corpus, so the manuscript's 464 is "found" inside the unrelated decimal 0.4646793470751095 |
| **R3-m5** | the six committed PNGs precede the final state of the script said to render them; no manifest ties a PNG to a script revision or to source hashes |
| **R3-m6** | the Methods claim that TWO redundant axes were found, but only one is ever identified |
| **R3-m7** | the ledger is described as "each named by the correction document", but it includes non-correction documents such as `WINDOW_RESOLVED.md` and `ORDER_AXIS.md` |
| **R3-m8** | the section 6 closing note still says fifteen works at abstract level plus four in full, which describes nineteen readings and contradicts section 1's eleven plus four |
| **R3-m9** | the Limitations say there has been no independent review, but do not disclose that reviewer reports exist in the repository or that a reviewer found the joint-grid defect |
| **R3-m10** | reference 3 omits the issue, which Crossref returns as 16, while the section promises fields "as Crossref returns them" |
| **R3-m11** | the figure legends name bare filenames that live under `wp3_results/anatomy/`, not under `wp3_results/` where the draft's first line says every number is committed |

## Process failing the reviewer recorded

**The draft changed at least three times inside one review window, from 415 to 449 lines, with a commit titled
"The reviewers read two different manuscript revisions, and the drift is recorded rather than smoothed".**
**The manuscript carries no revision identifier, so a reviewer cannot freeze what they reviewed. It should.**

## Recommendation posture

**Major revision, with R3-M1 blocking the paper's own empirical claims.** *"The central observation is worth
publishing... What remains is not a matter of more analysis but of accounting and packaging."* **If the inputs
cannot be pinned, the quantitative claims should be re-scoped to what the repository supports, and the closing
prescription should be softened to acknowledge that the authors' own package, by their own record, is not yet
reproducible.**
