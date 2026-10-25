# F4 closure: canonical headline tie rule designated (2026-10-26)

Authority: the advisor's stage ruling of 2026-10-25 (relayed by the lead) upgraded O-6 finding F4
to a pre-submission must-close: "至少需要正式指定唯一生效的平局规则、披露 C077 的差异，并使投稿
稿件、结果表和复现程序在该规则下保持一致。可以保留历史结果，但不能留下两个都自称规范的计算版本。"
This record is that designation. No frozen instrument is edited; no committed map is rewritten.

## The two historical rules (as found, both frozen before their own rounds)

- Primary round (`merge_coder_sheets_v2.py`, frozen pre-coding): the **weaker merged grade wins**;
  ties resolve to **coder A's transition**. Committed primary map: 15 x T3 + 1 x T2 (2311.15474v1
  -> T3 by weaker grade, A=T2:E2 vs B=T3:E1; C077/1811.09699v1 -> T2 by the tie rule, E1 vs E1).
- Validation round (`compute_validation_statistics_20261025.py:56-57`, frozen pre-coding):
  headline tie resolved to **T3 preference, otherwise coder A's transition**. Committed
  validation map: T3 38, T2 3, T4 1.

The divergence affects exactly one primary claim: C077 / `1811.09699v1` (A = T2:E1, B = T3:E1 -
an E1 tie). It affects zero E2 counts anywhere (verified by O-6 and re-verified below): headline
E2+ is 10/16 and 26/42 under either rule.

## Designation

**The canonical headline tie rule for this audit is the validation round's rule: on a tie
between the two coders' headline transitions, resolve to T3 if one candidate is T3, otherwise to
coder A's transition.** It governs: the consolidated analysis (H3 and the four-reading table),
every successor coding round, and any re-derivation presented as canonical. The per-round
committed maps remain valid historical results under their own frozen rules, and are labelled as
such wherever they appear; they are not re-computed.

## Disclosure (the C077 difference, stated once and completely)

Under the canonical rule the primary map re-derives as **16 x T3** (both primary disagreements
resolve to T3: 2311.15474v1 by the weaker grade exactly as committed, and C077 by the canonical
tie preference where the committed round resolved it to T2). An earlier draft of this record
wrongly stated 14 x T3 + 2 x T2 - that figure is coder A's own map, not the canonical
re-derivation; corrected here before anything was published from it. Coder H's own headline for
C077 is T2. The claim's headline grade is E1 under every resolution, so the headline statistic
(10/16 = 62.5 percent E2+) is identical, and the validation map reproduces its committed counts
exactly. Every appearance of the primary map must carry this disclosure or use the round-labelled
historical form.

## Consistency verification (fresh output, `verify_tie_rule_canonicality_20261026.py`)

The companion script asserts, from the raw sheets: (1) the validation map re-derived under the
canonical rule reproduces the committed validation counts exactly; (2) the primary map re-derived
under the canonical rule yields the disclosed 16 x T3 with C077 -> T3; (3) headline E2+
counts are identical under both rules in both corpora (10/16, 26/42). Run it before submission;
it must print PASS on all three assertions.

## Script consistency status

- `compute_validation_statistics_20261025.py` and `compute_H3_full_20261025.py` already
  implement the canonical rule (they were the source of the designation).
- `merge_coder_sheets_v2.py` implements the primary round's historical rule (weaker grade first,
  ties to coder A); it is labelled as such in this record and is not edited (its committed output
  is a round result).
- Successor instruments must implement the canonical rule and cite this record.

## Verification output (2026-10-26, fresh)

```
F4 CLOSURE VERIFICATION: PASS (validation map reproduces committed counts under the canonical
rule; primary canonical map = 16xT3 with C077->T3 as disclosed, historical = 15xT3+1xT2;
headline E2+ 10/16 and 26/42 invariant under both rules)
```

(`verify_tie_rule_canonicality_20261026.py`; the script's own first two drafts failed on its own
bugs - a coder-column filter that emptied the headline maps, and a mis-targeted assertion - and
were fixed before this PASS; the failures are in the session log, the fix is in the committed
script.)
