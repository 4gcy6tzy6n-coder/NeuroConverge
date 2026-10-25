#!/usr/bin/env python3
"""Robustness analysis R2a (advisor review 2026-10-25): recompute the core results with
survey/review claims excluded from BOTH corpora.

Frozen exclusion rule (before any recomputation): a claim is excluded iff its TITLE or ABSTRACT
self-identifies as a survey or review (case-insensitive 'survey' or 'review' as printed words in
the claiming paper's own title/abstract). Verb uses are caught too - the printed exclusion list
is the check: any claim excluded by a passing verb mention must be confirmed here. Surveys have
no own artifact; their structural E0s would dilute the primary-research reading. The exclusion
is a NAMED ROBUSTNESS ANALYSIS reported beside, never instead of, the primary numbers."""
import csv, json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute_validation_statistics_20261025 import merge_sheets, headline_merged, E_ORDER, load

ROOT = Path(__file__).resolve().parent
KW = re.compile(r"\b(survey|review)\b", re.I)

def excluded_ids(corpus_csv, title_abstract_pairs):
    out = []
    for cid, text in title_abstract_pairs:
        if KW.search(text or ""):
            out.append(cid)
    return out

# --- primary corpus (n=16) ---
prim_corpus = list(csv.DictReader(open(ROOT / "corpus_draw_arxiv_v1.csv")))
# abstracts for primary claims come from the adjudication-input extraction used by the pilot;
# titles are in the corpus csv; abstracts from the pinned snapshot via the adjudication input is
# pilot-scoped, so rebuild from the snapshot for primary ids only.
import xml.etree.ElementTree as ET
NS = {"a": "http://www.w3.org/2005/Atom"}
snap_text = (ROOT / "corpus_draw_arxiv_v1.snapshot.jsonl").read_text(errors="replace")
abs_idx = {}
for line in snap_text.splitlines():
    if not line.strip():
        continue
    rec = json.loads(line)
    if rec["query_term"] != "brain-inspired":
        continue
    root = ET.fromstring(rec["body"])
    for e in root.findall("a:entry", NS):
        aid = re.search(r"abs/(\S+)$", e.find("a:id", NS).text.strip()).group(1)
        abs_idx[aid] = re.sub(r"\s+", " ", e.find("a:summary", NS).text or "").strip()
prim_ids = [r["arxiv_id_version"] for r in prim_corpus]
prim_pairs = [(r["arxiv_id_version"], r["title"] + " " + abs_idx.get(r["arxiv_id_version"], ""))
              for r in prim_corpus]
prim_excl = excluded_ids("primary", prim_pairs)
# the primary coding sheets key claims by C-id; recover the C-id -> arxiv id map from the
# coder sheet's provenance_file column (fulltexts/<arxiv_id_version>.pdf)
cmap = {}
for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/coder_A_E.csv")):
    m_ = re.search(r"fulltexts/(\S+)\.pdf$", r["provenance_file"] or "")
    if m_:
        cmap[r["claim_id"]] = m_.group(1)
assert len(cmap) == 16, f"expected 16 C-id mappings, got {len(cmap)}"
merged_E = list(csv.DictReader(open(ROOT / "CODING_sheets_v2/merged_E.csv")))
head_m = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/headline_merged.csv"))}
excl_cids = {c for c, a in cmap.items() if a in prim_excl}
prim_kept_cids = [c for c in cmap if c not in excl_cids]
prim_kept = [cmap[c] for c in prim_kept_cids]
prim_cells = [r for r in merged_E if r["claim_id"] in prim_kept_cids]
prim_dist = {t: Counter(r["in_paper_grade"] for r in prim_cells if r["transition"] == t)
             for t in ("T1", "T2", "T3", "T4", "T5")}
prim_hl = Counter(head_m[c] for c in prim_kept_cids)
prim_hl_grades = {c: next(r["in_paper_grade"] for r in prim_cells
                          if r["claim_id"] == c and r["transition"] == head_m[c]) for c in prim_kept_cids}
prim_e2 = sum(1 for g in prim_hl_grades.values() if g == "E2")

# --- validation corpus (n=42) ---
val_corpus = list(csv.DictReader(open(ROOT / "corpus_validation_v2_adjudicated.csv")))
val_pairs = []
for r in val_corpus:
    t = Path(ROOT / "pinned_validation_20261025" / "texts" / f"{r['arxiv_id_version']}.txt")
    head = t.read_text(errors="replace")[:3000]  # title+abstract region of the text layer
    val_pairs.append((r["arxiv_id_version"], r["title"] + " " + re.sub(r"\s+", " ", head)))
val_excl = excluded_ids("validation", val_pairs)
A = load(ROOT / "CODING_sheets_validation/coder_A.csv", "A")
B = load(ROOT / "CODING_sheets_validation/coder_B.csv", "B")
merged = merge_sheets(A, B)
hl_a = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_validation/headline_A.csv"))}
hl_b = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_validation/headline_B.csv"))}
hm, _ = headline_merged(hl_a, hl_b, merged)
val_kept = [r["arxiv_id_version"] for r in val_corpus if r["arxiv_id_version"] not in val_excl]
val_dist = {t: Counter(merged[(c, t)][0] for c in val_kept) for t in ("T1", "T2", "T3", "T4", "T5")}
val_hl = Counter(hm[c] for c in val_kept)
val_e2 = sum(1 for c in val_kept if merged[(c, hm[c])][0] == "E2")

def wilson(k, n, z=1.959963985):
    import math
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(100 * max(0.0, c - h), 1), round(100 * min(1.0, c + h), 1)]

result = {
    "rule": "title or abstract self-identifies as survey/review (case-insensitive 'survey'|'review')",
    "primary": {"excluded": prim_excl, "n_full": 16, "n_kept": len(prim_kept),
                "dist": {t: dict(v) for t, v in prim_dist.items()},
                "headline_map": dict(prim_hl), "headline_e2plus": prim_e2,
                "headline_e2plus_share_pct": round(100 * prim_e2 / len(prim_kept), 1),
                "headline_e2plus_wilson95_pct": wilson(prim_e2, len(prim_kept))},
    "validation": {"excluded": val_excl, "n_full": 42, "n_kept": len(val_kept),
                   "dist": {t: dict(v) for t, v in val_dist.items()},
                   "headline_map": dict(val_hl), "headline_e2plus": val_e2,
                   "headline_e2plus_share_pct": round(100 * val_e2 / len(val_kept), 1),
                   "headline_e2plus_wilson95_pct": wilson(val_e2, len(val_kept))},
}
out = ROOT / "ROBUSTNESS_SURVEY_EXCLUSION_20261025.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
print("->", out.name)
