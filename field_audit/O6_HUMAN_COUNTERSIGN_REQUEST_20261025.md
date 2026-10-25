# O-6 human counter-signature request (2026-10-25)

**To:** a human non-author verifier (someone who did not author this project's instruments,
scripts, coding sheets, or manuscript text, and did not perform the AI verification).

**Purpose.** O-6 requires an independent non-author recomputation. An AI non-author verification
was completed on 2026-10-25 (`O6_VERIFICATION_REPORT_CLAUDE_20261025.md`) and its findings were
resolved on the lead's instruction (`O6_FINDINGS_RESOLUTION_20261025.md`). The lead has accepted
the AI report as the machine-checkable half of O-6. Your signature is the human half: confirm that
the report's numbers and the resolution record are what they say they are. This is a
**counter-signature of a machine verification**, not a demand that you redo the full audit.

**Materials and commit.**

- AI report: `O6_VERIFICATION_REPORT_CLAUDE_20261025.md`
- Resolution record: `O6_FINDINGS_RESOLUTION_20261025.md`
- Base commit verified by O-6: `0dbf8ac`
- Resolution branch: `o6-findings-resolution-20261025` (code commit `253507e`; the branch also
  carries the resolution records)

**Suggested checks (2-4 hours).**

1. **Read** the AI report and the resolution record. Note the overall verdict
   (VERIFIED WITH FINDINGS) and the five findings.
2. **Recount three load-bearing numbers yourself** from the raw sheets, using your own code or by
   hand, and record expected/observed:
   - primary headline E2+ under the AI weaker merge: **10/16 = 62.5 %**
     (`CODING_sheets_v2/coder_A_E.csv`, `coder_B_E.csv`, `headline_merged.csv`);
   - validation headline E2+ under the AI weaker merge: **26/42 = 61.9 %**
     (`CODING_sheets_validation/coder_A.csv`, `coder_B.csv`, `headline_A.csv`, `headline_B.csv`);
   - in-paper disagreement: **18/80 = 22.5 %** primary.
3. **Run the H3 chain** and confirm it reproduces the committed H3 JSON:

   ```bash
   cd field_audit
   python3 compute_H3_full_20261025.py
   python3 compute_H3_reading2b_20261025.py
   shasum -a 256 CODING_sheets_human/H3_READING_20261025.json
   # expected: 53175756da043aaf9e92d30509d45c8f2edd33ca31571b84b8936b5b0c39787f
   ```

4. **Confirm the clean-clone packaging fix** (the two analyses that previously failed):

   ```bash
   git clone -b o6-findings-resolution-20261025 /Users/yyl/Desktop/workshop/NMI/NeuroConverge ~/o6_countersign/NeuroConverge
   cp -r /Users/yyl/Desktop/workshop/NMI/NeuroConverge/field_audit/pinned_fulltext_20261020 ~/o6_countersign/NeuroConverge/field_audit/
   cp -r /Users/yyl/Desktop/workshop/NMI/NeuroConverge/field_audit/pinned_validation_20261025 ~/o6_countersign/NeuroConverge/field_audit/
   cd ~/o6_countersign/NeuroConverge/field_audit
   python3 run_final_scoring_20261024.py      # expect exit 0
   python3 robustness_survey_exclusion_20261025.py  # expect exit 0
   ```

   (`fulltexts/` is tracked at HEAD; no copy is needed. The pinned directories are the only
   untracked inputs.)
5. **Spot-check three human quotes** from `CODING_sheets_human/coder_H.csv` against the pinned
   text layers in `pinned_validation_20261025/texts/` (suggested claims: `1505.07814v2`,
   `1511.04484v2`, `1702.05596v1` — if a quote is absent, use the next claim and record it).
6. **Read the findings and resolutions.** Confirm that no load-bearing number changed and that
   F1-F5 have the recorded dispositions. If you find a discrepancy, record it; do not repair it.

**Rules.**

- Read-only: run scripts, write your own notes, but do not modify, move, or commit project files.
- If a number does not reproduce, record file, command, expected, observed, and stop; a
  discrepancy is a finding, not something to fix.
- You may ask the lead what a number means; ask the scripts' docstrings how to run them.

**Counter-signature.**

I performed the checks above on the commit and materials named in this request. I confirm that the
load-bearing numbers reproduce and that the resolution record accurately describes the changes.

- Name:
- Affiliation / role:
- Date:
- Checks performed (numbers and commands):
- Discrepancies found (if any):
- Signature:

Return this sheet, with your notes, to the lead. The lead will attach it to the O-6 record and send
the package to the advisor.

---

## Advisor requirements addendum (2026-10-26, stage ruling)

1. The signer must be **uninvolved in the project and in the coding sheets' production** - a
   third researcher who is neither the lead, nor coder Yang (Yang authored the coding sheets and
   is therefore disqualified from countering the verification of those sheets), nor anyone who
   performed the AI verification.
2. The signer **personally executes the six checks**, keeps the **raw outputs and any findings**
   (command logs, diffs), and does not sign on the basis of reading the AI report alone.
3. The lead signs only what the lead has personally reviewed.
4. Return the signed sheet WITH the raw outputs attached; the package goes to the advisor for the
   final gate confirmation.

Post-report context for the signer: the findings F1-F5 in the report were resolved after the
as-found run (commit `253507e`); the resolution record is part of what you are signing. The F4
tie-rule designation (`F4_TIE_RULE_DESIGNATION_20261026.md`) and its verification script
postdate the report; run `python3 field_audit/verify_tie_rule_canonicality_20261026.py` as a
seventh check (expected: PASS on all three assertions).

---

## Addendum 2 (2026-10-26): self-contained remote procedure (replaces the local-path setup)

The advisor's remote review flagged that the original check 4 depended on this machine's local
paths and untracked directories. **Resolved:** the 42 validation text layers are now committed
(commit `04b6ec5`), so every counter-sign check runs from a plain GitHub clone alone. The
self-containment was verified by an actual fresh-clone run: `run_final_scoring_20261024.py`
exit 0; `robustness_survey_exclusion_20261025.py` exit 0; the F4 verification script PASS
(4 assertions); the H3 chain reproduces `H3_READING_20261025.json` byte-for-byte; the format
checker PASS.

**Procedure for the counter-signer (no access to the original machine is needed):**

```bash
git clone https://github.com/4gcy6tzy6n-coder/NeuroConverge.git
cd NeuroConverge/field_audit
# check 2 - your own recount code over the raw sheets (CODING_sheets_v2/, CODING_sheets_validation/, CODING_sheets_human/)
# check 3 - the H3 chain:
python3 compute_H3_full_20261025.py && python3 compute_H3_reading2b_20261025.py
shasum -a 256 CODING_sheets_human/H3_READING_20261025.json
#   expected sha256: 53175756da043aaf9e92d30509d45c8f2edd33ca31571b84b8936b5b0c39787f
# check 4 - packaging, now from the clone alone:
python3 run_final_scoring_20261024.py            # expect exit 0
python3 robustness_survey_exclusion_20261025.py  # expect exit 0
# check 5 - quotes: locate them in pinned_validation_20261025/texts/ (committed)
# check 7 - the F4 gate:
python3 verify_tie_rule_canonicality_20261026.py # expect PASS, 4 assertions
```

Keep your command logs and outputs; attach them to the signed sheet. The primary-corpus PDFs
(`pinned_fulltext_20261020/pdfs/`) remain untracked by size and are covered by their committed
manifest - none of the seven checks requires them.
