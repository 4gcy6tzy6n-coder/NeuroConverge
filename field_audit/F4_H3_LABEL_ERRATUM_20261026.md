# F4/H3 label erratum (2026-10-26): the headline-agreement labels under the canonical rule

Authority: the advisor's remote review of 2026-10-26 (relayed by the lead), which found that the
F4 designation and the H3 headline-agreement record used the word "canonical" for two different
rules. This erratum aligns the labels; the frozen JSONs stand untouched as as-found records.

## The two numbers, now labelled once and permanently

| agreement of coder H's headline map with... | value | label |
| --- | --- | --- |
| the **historical committed maps** (primary: tie -> coder A, 15 x T3 + 1 x T2; validation: the committed T3-preference map) | **52/58** | historical-committed-map agreement |
| the **F4-designated canonical rule** (tie -> T3 preference, then coder A; primary map 16 x T3) | **51/58** | canonical-rule agreement |

Mechanism (one claim, fully stated): C077 / `1811.09699v1` - coder H chose T2; the historical
primary rule also resolved T2 (agree); the canonical rule resolves the E1 tie to T3 (disagree).
The six validation misses are identical under both labels.

## Dispositions

1. `H3_HEADLINE_AGREEMENT_CORRECTION_20261025.json` is **not edited** (as-found record; its
   "canonical_maps" key henceforth reads as "historical-committed-map agreement" per this
   erratum, and its "h3_script_variant" key as "canonical-rule agreement"). Any future citation
   uses this erratum's labels.
2. `O5_H3_RESULTS_20261025.md` section 4's "51/58" is the canonical-rule number and is correct
   as written; the 52/58 figure quoted anywhere without a label must carry the historical label
   from this erratum.
3. The gap the advisor identified - the F4 verification script checked maps and E2 counts but
   not the agreement labels - is closed: `verify_tie_rule_canonicality_20261026.py` now carries
   **assertion 4** (canonical-rule agreement = 51/58; historical-committed-map agreement =
   52/58; canonical must be the lower number), and passes all four assertions.
4. No load-bearing number changes. The manuscript has not quoted either figure.

## Verification output (fresh)

```
F4 CLOSURE VERIFICATION: PASS (validation map reproduces committed counts; primary canonical
16xT3 / historical 15xT3+1xT2; E2 10/16 and 26/42 invariant; H-vs-AI headline agreement:
canonical rule 51/58, historical committed maps 52/58 - labels per F4 designation)
```
