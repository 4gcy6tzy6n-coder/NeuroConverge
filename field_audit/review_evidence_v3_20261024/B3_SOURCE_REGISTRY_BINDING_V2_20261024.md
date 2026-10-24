# B3 source registry binding v2, 2026-10-24 (registry successor)

Authority: the 2026-10-19 full-authority grant, executed 2026-10-24. This is the visible registry
successor that the B3 v1 binding requires for any registry change ("a visible registry successor,
new canonical/byte digests and binding record"). The trigger is the corpus narrowing from 18 to 16
claims: the eligibility second review closed 2026-10-24 with a final corpus of 16
(`corpus_final_16.csv`, commit `874797f`), and the bound scorer correctly refuses a registry whose
claim IDs do not exactly match the sampled claims - the refusal was demonstrated on 2026-10-24
(`PIPELINE_REHEARSAL_20261024.md`).

- Final claim set: `corpus_final_16.csv`, N=16.
- Registry file: `review_evidence_v3_20261024/SOURCE_REGISTRY_V2_20261024.json`.
- Registry file byte SHA-256: `098c14cee22e647da1eda1059dac255a471c28c0d7c0172c02fd19d54da1639f`.
- Scorer expected canonical registry SHA-256:
  `0c9303e3ef3e77adad2ffefcb6b5fce22a039cac7a80359c4c804fd5a50efd58`.
- Derivation from V1: identical per-claim `target_sha256` values for all 16 retained claims
  (asserted equal to the V1 values and to both coders' declared evidence-sheet digests); the two
  claims removed by the eligibility second review are dropped; supplements and cited sources remain
  empty maps, as in V1, because no such source is registered in this scope.
- Canonicalization: sorted JSON keys, compact comma/colon separators, `ensure_ascii=False`, UTF-8 -
  the bound v3 scorer's own recipe.
- Unchanged: the scorer, its tests, the 15-field row schema (template digest `77dcda1a...`), and the
  F-2 recorded defect. No threshold, item definition or status vocabulary changes here.
- The V1 binding and its 18-claim registry remain on record as history; nothing scored under V1
  enters the final outputs.
