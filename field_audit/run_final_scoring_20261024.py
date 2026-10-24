#!/usr/bin/env python3
"""Final reportability scoring on the 16-claim corpus (2026-10-24).

Applies the two ledger corrections (C-2 B pointers, C-3 A note), builds the 39
adjudication rows from the lead's recorded decisions, and runs the bound v3
scorer with the V2 source registry. Prints the summary and writes the frozen
outputs. No status written by either coder is altered by the corrections.
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, ".")
import reportability_score_candidate_v3_candidate as S

ROOT = pathlib.Path(".").resolve()
ADJUDICATOR = "lead (assistant office, 2026-10-19 authority record; same-model limitation disclosed; human supersedes)"
DATE = "2026-10-24"

# claim, item -> (final status, adopted_from, rationale)
DECISIONS = {
    ("C003","T1-02"): ("PARTIAL","B","Neuron-level input-output dynamics are specified (Eqs. 1-7) and one circuit-level operationalization exists, but the remaining circuit/area-level attributions lack input-output statements."),
    ("C003","T4-01"): ("NOT_REPORTED","A","No statement names task families beyond the demonstrated set as tested or untested; enumerating the demonstrated set is not the item's content."),
    ("C003","T4-02"): ("NOT_REPORTED","A","No scale sensitivity of task performance and no explicit unreported marking; the multi-scale brain simulations are biological-scale demonstrations, not task-performance sensitivity."),
    ("C003","T5-01"): ("REPORTED","B","The abstract's per-category validation claims each map to identifiable results in the body; a separate single overall link is not required by the item."),
    ("C006","T4-01"): ("NOT_REPORTED","A","No statement names task families beyond the demonstrated set as tested or untested."),
    ("C008","T2-02"): ("REPORTED","A","Explicit simplification statement with an enumerable absent set (subcortical areas, fine-grained connectivity) satisfies COND-3(a); the LLM/CNN-level departure axis coder B names is not addressed by the paper but is not required for the item as bound."),
    ("C010","T2-02"): ("PARTIAL","A","One departure admitted in passing (LTC essentially an RNN, Sec 3.2); departures are not enumerated per mapped mechanism and the absent set is not enumerable."),
    ("C010","T5-02"): ("REPORTED","A","Intended scope stated in the abstract; evidence setting, task and scale locatable (Secs 4.1-4.2)."),
    ("C011","T1-02"): ("NOT_REPORTED","B","No input-output statement of an attributed computation exists anywhere; only organizational adjectives are attributed, so no part of the item's content is present."),
    ("C011","T4-01"): ("PARTIAL","B","COND-3(a): an absence statement exists (Sec. 6, initial exploration, simple cases only) but the absent set is not enumerable from it."),
    ("C011","T4-02"): ("PARTIAL","A","One scale sensitivity is reported (unit count vs solution frequency); other scale dimensions and an explicit unreported marking are missing."),
    ("C016","T2-02"): ("PARTIAL","A","Simplifications are locatable but implicit (spiking implementation, NAS constraints); no enumeration of biological departures per motif."),
    ("C016","T4-01"): ("PARTIAL","B","COND-3(a): untested families appear only as non-enumerable open examples."),
    ("C016","T4-02"): ("PARTIAL","B","Channel-width sensitivity is reported (Table V); other scale dimensions and an explicit unreported marking are missing."),
    ("C018","T4-01"): ("REPORTED","B","Task families beyond the headline classification task are explicitly named as tested with results (COCO detection, Table 2; ADE20K segmentation); verified in the text."),
    ("C021","T5-02"): ("REPORTED","A","Intended scope and the evidence setting, task and scale are all stated and locatable."),
    ("C028","T3-01"): ("PARTIAL","A","The comparison that was run is described (Table 4 vs ResNets) but it does not assess attribution to correspondence, and no explicit statement that no attribution comparison was run."),
    ("C028","T3-02"): ("NOT_REPORTED","A","No statement of which attribution controls are present or absent; parameter counts per model are not a control inventory."),
    ("C028","T4-01"): ("PARTIAL","A","One locatable absence statement (multimodal clinical information not yet included) but task families beyond CAG are not enumerated as tested or untested."),
    ("C028","T5-02"): ("PARTIAL","B","Test set and training epochs stated; training-set source and size and test-set provenance are not stated, so the scale element is partially reported."),
    ("C032","T1-02"): ("REPORTED","A","Reactivation of neural patterns protecting from drastic forgetting is a mechanism-to-function input-output statement."),
    ("C032","T4-01"): ("PARTIAL","A","COND-3(a): task-IL is implied untested by the class-IL choice statement but the absent set is not enumerated."),
    ("C036","T1-02"): ("REPORTED","A","The dopamine attribution is stated in signal-to-effect form (phasic reward-prediction-error signaling to basal ganglia targets); subsystem role labels do not reduce it."),
    ("C036","T3-01"): ("PARTIAL","A","The comparison that was run is described but is cross-method racing, not an attribution comparison; no explicit none-run statement."),
    ("C036","T3-02"): ("NOT_REPORTED","A","Only the evaluation protocol is described; no statement of which attribution controls are present or absent."),
    ("C036","T4-02"): ("PARTIAL","A","One scale sensitivity is reported (input resolution 160x120 vs 320x240 with performance consequence); other dimensions and an unreported marking are missing."),
    ("C036","T5-01"): ("REPORTED","A","Abstract claims are tied to named results (Fig. 4 reward trends, Sec. III-D, Table I); operational definition of 'advanced behaviors' is not required by the item."),
    ("C043","T2-02"): ("REPORTED","B","Departures are explicitly stated and locatable (fixed weights vs energy injection, dimensionality-reduced fitting, disregarded roll angle)."),
    ("C043","T4-01"): ("REPORTED","A","Explicit absence statement whose absent set is enumerable from it (complete SLAM with loop closure, edge/neuromorphic deployment)."),
    ("C043","T4-02"): ("REPORTED","B","Scale sensitivity is reported across model resolution, two compute platforms and memory footprint."),
    ("C045","T3-01"): ("PARTIAL","B","GENRE review: comparisons from cited studies are described and locatable, but the review's own attribution assessment is absent - the missing element is named."),
    ("C045","T4-01"): ("REPORTED","A","GENRE review: tested/untested status of task families is reported through the surveyed literature with locatable absence flags (e.g. unresolved cross-task generalization)."),
    ("C045","T5-02"): ("REPORTED","A","GENRE review: intended scope and the surveyed-literature setting are stated and locatable; per-study consolidation is not required by the item."),
    ("C046","T1-02"): ("REPORTED","A","HC and mPFC recall-role statements are mechanism-to-function input-output statements (recent vs remote memory recall)."),
    ("C046","T4-01"): ("REPORTED","A","Untested families are named explicitly and enumerable (unsupervised learning, regression, permutation protocols) beside the tested multi-modal extension."),
    ("C049","T1-02"): ("REPORTED","A","Spiking neurons recognizing spatial and temporal features is a mechanism-to-function input-output statement."),
    ("C049","T4-02"): ("PARTIAL","A","One scale axis is reported (technology node, 45nm vs ASAP 7nm, with device consequences); other dimensions and an unreported marking are missing."),
    ("C077","T1-02"): ("REPORTED","A","Attention enabling prioritized selection and routing of visual inputs is a mechanism-to-function input-output statement."),
    ("C077","T3-01"): ("PARTIAL","A","The described comparison is behavioural (model vs subject fixations), not an attribution comparison, and no explicit statement that none was run."),
}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    reg = json.load(open("review_evidence_v3_20261024/SOURCE_REGISTRY_V2_20261024.json"))
    target = {c: v["target_sha256"] for c, v in reg.items()}
    corpus = {r["claim_id"]: r["arxiv_id_version"] for r in load("corpus_final_16.csv")}

    # C-2: populate B's empty evidence_pointer from its own source_locator text.
    b_rows = load("CODING_sheets_v2/coder_B_R.csv")
    b_fixed = 0
    for x in b_rows:
        x["source_file_sha256"] = target[x["claim_id"]]          # C-1 (already recorded)
        if not x["evidence_pointer"].strip():
            x["evidence_pointer"] = x["source_locator"]           # C-2
            b_fixed += 1
    out = pathlib.Path("CODING_sheets_v2/coder_B_R_corrected_20261024.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(b_rows[0].keys()))
        w.writeheader(); w.writerows(b_rows)

    # C-3: populate A's one empty note from its own evidence_pointer text.
    a_rows = load("CODING_sheets_v2/coder_A_R.csv")
    a_fixed = 0
    for x in a_rows:
        if x["status"] in ("PARTIAL", "NOT_REPORTED") and not x["note"].strip():
            x["note"] = x["evidence_pointer"]                     # C-3
            a_fixed += 1
    out = pathlib.Path("CODING_sheets_v2/coder_A_R_corrected_20261024.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(a_rows[0].keys()))
        w.writeheader(); w.writerows(a_rows)
    print(f"corrections applied: C-2 B pointers {b_fixed}, C-3 A notes {a_fixed}")

    # Build ADJUDICATED rows from the recorded decisions.
    byA = {(x["claim_id"], x["item_id"]): x for x in a_rows}
    byB = {(x["claim_id"], x["item_id"]): x for x in b_rows}
    adj_rows = []
    for (cid, item), (status, side, why) in DECISIONS.items():
        src = byA[(cid, item)] if side == "A" else byB[(cid, item)]
        other = byB[(cid, item)] if side == "A" else byA[(cid, item)]
        adj_rows.append({
            "claim_id": cid, "coder": "ADJUDICATED", "transition": src["transition"],
            "item_id": item, "status": status,
            "evidence_pointer": src["evidence_pointer"],
            "source_file_sha256": target[cid], "source_role": "TARGET", "source_id": "",
            "source_locator": src["source_locator"],
            "note": f"adopted coder {side} status; other coder status {other['status']}",
            "adjudicator": ADJUDICATOR, "adjudication_date": DATE,
            "adjudication_rationale": why,
            "adjudication_source_pointer": f"coder {side} pointer: {src['evidence_pointer'][:120]}",
        })
    out = pathlib.Path("CODING_sheets_v2/adjudication_R_20261024.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(adj_rows[0].keys()))
        w.writeheader(); w.writerows(adj_rows)
    print(f"adjudication rows written: {len(adj_rows)} (adopted A {sum(1 for v in DECISIONS.values() if v[1]=='A')}, adopted B {sum(1 for v in DECISIONS.values() if v[1]=='B')})")

    # Run the bound scorer on A + B-corrected + adjudications.
    paths = {}
    for cid, aid in corpus.items():
        paths[target[cid]] = str((ROOT / "fulltexts" / f"{aid}.pdf").resolve())
    rows = a_rows + b_rows + adj_rows
    try:
        result = S.summarize_reportability(
            claim_ids=list(corpus),
            coders=("A", "B"),
            rows=rows,
            source_paths_by_sha256=paths,
            source_registry_by_claim_id=reg,
            expected_source_registry_sha256="0c9303e3ef3e77adad2ffefcb6b5fce22a039cac7a80359c4c804fd5a50efd58",
        )
    except S.ReportabilityError as e:
        print(f"SCORER REFUSED: {e}")
        return 1
    out = pathlib.Path("CODING_sheets_v2/reportability_summary_final_20261024.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("SCORER: PASS - summary written", out)
    matched_neither = 0
    for (cid, item), (status, side, _) in DECISIONS.items():
        chosen = {byA[(cid, item)]["status"], byB[(cid, item)]["status"]}
        if status not in chosen:
            matched_neither += 1
    print(f"R1 matched-neither count: {matched_neither} of {len(DECISIONS)} adjudications")
    print(json.dumps(result["post_adjudication_counts"], indent=1, sort_keys=True))
    print("disagreement_by_item:", json.dumps(result["disagreement_by_item"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
