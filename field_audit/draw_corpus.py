#!/usr/bin/env python3
"""The Route A corpus draw, implementing the frozen selection rule exactly.

Authority: ../DECISION_20261018_ROUTE_A_SIGNED.md (P3); rule: AUDIT_PREREGISTRATION_v1_FROZEN.md section 3.
The database is OpenAlex (public API, cursor-paged, polite pool). The keyword lists below are part of the
committed query per the frozen rule's operational note - they are not a hidden choice.

What this script does on --query:
  1. fetch works matching the claim-keyword disjunction into snapshot.jsonl (the pinned snapshot);
  2. apply the mechanical filters (window, venue tier, citation floor/deci le, keyword co-presence),
     logging a keep/drop reason per candidate;
  3. assign mechanism families mechanically (adjudication may correct later, with logged reasons);
  4. draw the stratified corpus (target 20; <=3 per family, <=5 per venue; by citation rank);
  5. write corpus_draw_v1.csv, corpus_draw_v1.manifest.json (query, date, snapshot sha256) and register rows.

Nothing here adjudicates claim type - that is draw review under the frozen protocol, logged per candidate,
firing the replacement rule on exclusions. Committing the draw output is corpus freeze.

--selftest runs the sabotage-verified checks on fixtures: every filter must be shown to reject its own error
class, the caps must be shown to bind, and the replacement rule must pick the next-highest-citation claim in
the same stratum. A filter that has never rejected anything is not evidence (the lane rule, applied to this
instrument).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# --- the frozen rule, section 3 (do not edit without a dated owner-visible amendment) ---
WINDOW = ("2015-01-01", "2026-09-30")
TIER3_CITATION_FLOOR = 100
TIER3_DECILE = 0.10
TARGET_SIZE = 20
ACCEPT_RANGE = (15, 25)
FAMILY_CAP = 3
VENUE_CAP = 5
MAILTO = "field-audit@nmi-lane.local"

# Keyword lists: part of the committed query. A candidate must match >=1 BIO_TERM and >=1 AI_TERM in title or
# abstract (case-folded). Family keywords classify the mechanism family mechanically.
BIO_TERMS = (
    "brain-inspired", "neuro-inspired", "neuroscience-inspired", "bio-inspired", "biology-inspired",
    "biologically inspired", "biologically plausible", "connectome", "synaptic", "spiking",
    "neuromorphic", "hippocamp", "hippocampus", "cerebellar", "cortex", "cortical", "hebbian",
    "dopamine", "eligibility trace", "memory consolidation", "memory replay", "neural replay",
    "predictive coding", "reward prediction error", "place cell", "grid cell",
)
AI_TERMS = (
    "neural network", "machine learning", "reinforcement learning", "deep learning",
    "artificial intelligence", "learning system", "robot", "autonomous agent", "intelligent agent",
    "artificial neural", "learning rule", "training algorithm",
)
FAMILY_KEYWORDS = {
    "memory": ("memory consolidation", "memory replay", "neural replay", "hippocamp", "place cell", "grid cell", "hippocampus"),
    "plasticity/learning rules": ("hebbian", "eligibility trace", "plasticity", "synaptic", "reward prediction error", "dopamine"),
    "architecture/connectome": ("connectome", "cortical", "cortex", "brain-inspired architecture", "neural architecture"),
    "attention/coding": ("predictive coding", "attention", "sparse coding"),
    "neuromorphic hardware": ("neuromorphic", "spiking", "loihi", "memristor"),
    # "other" is the fallback
}
TIER1_TOKENS = ("nature", "science", "cell")  # venue display_name startswith any (case-folded)
# Real OpenAlex display names, not abbreviations: "Neural Information Processing Systems",
# "International Conference on Machine Learning", "International Conference on Learning Representations",
# "IEEE/CVF Conference on Computer Vision and Pattern Recognition", "Proceedings of the National Academy
# of Sciences". Abbreviations are kept as fallbacks for variant listings.
TIER2_VENUES = (
    "neural information processing systems", "neurips",
    "conference on machine learning", "icml",
    "learning representations", "iclr",
    "computer vision and pattern recognition", "cvpr",
    "national academy of sciences", "pnas",
)

CANDIDATE_COLUMNS = (
    "candidate_id", "openalex_id", "doi", "title", "venue", "venue_tier", "publication_date",
    "cited_by_count", "mechanism_family", "family_source", "keep", "drop_reason",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def venue_tier(venue_name: str | None) -> int | None:
    """Tier 1: Nature*/Science*/Cell* by display name. Tier 2: the named venues plus PNAS.

    Tier 2's oral-or-spotlight property is NOT mechanically recoverable from OpenAlex: every tier-2 candidate
    is flagged needs_adjudication for it at draw review, per the protocol's adjudication step.
    """
    name = (venue_name or "").strip().casefold()
    if not name:
        return None
    if any(name.startswith(token) for token in TIER1_TOKENS):
        return 1
    if any(token in name for token in TIER2_VENUES):
        return 2
    return 3


def in_window(publication_date: str | None) -> bool:
    if not publication_date:
        return False
    return WINDOW[0] <= publication_date[:10] <= WINDOW[1]


def keyword_hit(text: str, terms) -> str | None:
    folded = (text or "").casefold()
    for term in terms:
        if term in folded:
            return term
    return None


def classify_family(text: str) -> tuple[str, str]:
    """Mechanical family assignment with the matched keyword recorded. Fallback: other."""
    for family, terms in FAMILY_KEYWORDS.items():
        hit = keyword_hit(text, terms)
        if hit:
            return family, f"keyword:{hit}"
    return "other", "fallback"


def candidate_row(work: dict) -> dict:
    title = work.get("title") or ""
    abstract_inverted = work.get("abstract_inverted_index") or {}
    abstract = " ".join(abstract_inverted) if abstract_inverted else ""
    text = f"{title} {abstract}"
    venue = ((work.get("primary_location") or {}).get("source") or {}).get("display_name")
    family, source = classify_family(text)
    bio = keyword_hit(text, BIO_TERMS)
    ai = keyword_hit(text, AI_TERMS)
    tier = venue_tier(venue)
    keep, reason = True, ""
    if not in_window(work.get("publication_date")):
        keep, reason = False, "outside window"
    elif tier is None:
        keep, reason = False, "no venue"
    elif not bio:
        keep, reason = False, "no bio term"
    elif not ai:
        keep, reason = False, "no ai term"
    return {
        "openalex_id": work.get("id", ""),
        "doi": work.get("doi") or "",
        "title": title,
        "venue": venue or "",
        "venue_tier": tier or "",
        "publication_date": work.get("publication_date") or "",
        "cited_by_count": int(work.get("cited_by_count") or 0),
        "mechanism_family": family,
        "family_source": source,
        "_bio_term": bio or "",
        "_ai_term": ai or "",
        "keep": keep,
        "drop_reason": reason,
    }


def tier3_threshold(rows: list[dict]) -> int:
    """Tier 3 = citation floor 100 AND the top decile of the remaining pool's citations.

    The decile is computed over kept tier-3 candidates before the threshold is applied, and the threshold is
    recorded in the manifest so the cut is auditable rather than remembered.
    """
    kept = sorted((r["cited_by_count"] for r in rows if r["venue_tier"] == 3 and r["keep"]), reverse=True)
    if not kept:
        return TIER3_CITATION_FLOOR
    index = max(0, int(len(kept) * TIER3_DECILE) - 1)
    return max(TIER3_CITATION_FLOOR, kept[index])


def apply_tier3_floor(rows: list[dict], threshold: int) -> list[dict]:
    out = []
    for row in rows:
        if row["keep"] and row["venue_tier"] == 3 and row["cited_by_count"] < threshold:
            row = dict(row)
            row["keep"], row["drop_reason"] = False, f"tier3 below threshold ({row['cited_by_count']} < {threshold})"
        out.append(row)
    return out


def stratified_draw(rows: list[dict]) -> tuple[list[dict], list[str]]:
    """Citation-ranked within the kept pool, subject to <=3 per family and <=5 per venue."""
    log = []
    kept = sorted((r for r in rows if r["keep"]), key=lambda r: -r["cited_by_count"])
    selected, family_counts, venue_counts = [], {}, {}
    for row in kept:
        if len(selected) >= TARGET_SIZE:
            break
        family, venue = row["mechanism_family"], row["venue"]
        if family_counts.get(family, 0) >= FAMILY_CAP:
            log.append(f"cap:family:{row['openalex_id']}")
            continue
        if venue_counts.get(venue, 0) >= VENUE_CAP:
            log.append(f"cap:venue:{row['openalex_id']}")
            continue
        selected.append(row)
        family_counts[family] = family_counts.get(family, 0) + 1
        venue_counts[venue] = venue_counts.get(venue, 0) + 1
    return selected, log


def replacement_pick(rows: list[dict], selected: list[dict], excluded_id: str) -> dict | None:
    """The next-highest-citation kept claim in the same stratum (same family, same venue tier).

    The excluded claim is barred from its own replacement: it left the corpus for cause, so it re-enters
    never. (The selftest caught the first draft of this function subtracting the excluded id from the taken
    set, which made the excluded claim its own successor - the exact error class the fixture was built for.)
    """
    excluded = next(r for r in selected if r["openalex_id"] == excluded_id)
    taken = {r["openalex_id"] for r in selected} | {excluded_id}
    pool = [
        r for r in rows
        if r["keep"] and r["openalex_id"] not in taken
        and r["mechanism_family"] == excluded["mechanism_family"]
        and r["venue_tier"] == excluded["venue_tier"]
    ]
    if not pool:
        return None
    return max(pool, key=lambda r: r["cited_by_count"])


def build_query() -> str:
    """The committed disjunction: (bio term) AND (ai term), applied as title-and-abstract search groups.

    OpenAlex has no OR-of-phrases filter, so the query runs per bio term (one request per term, cursor-paged)
    and the AND is enforced locally by keyword_hit in candidate_row. This keeps the snapshot one pinned set of
    raw responses whose URLs are recorded in full in the manifest.
    """
    return json.dumps({"per_bio_term": list(BIO_TERMS), "filter": "title_and_abstract.search",
                       "and_enforced_locally_by": "keyword_hit"})


def fetch_snapshot(out: Path, max_terms: int | None = None) -> list[str]:
    """Fetch one response file per bio term. Returns the URLs fetched. No data is interpreted here."""
    import time
    urls = []
    terms = BIO_TERMS[:max_terms] if max_terms else BIO_TERMS
    with out.open("w", encoding="utf-8") as handle:
        for term in terms:
            cursor = "*"
            while cursor:
                params = urllib.parse.urlencode({
                    "filter": f"title_and_abstract.search:{term}",
                    "per-page": 200, "cursor": cursor, "mailto": MAILTO,
                    "select": "id,doi,title,publication_date,cited_by_count,primary_location,abstract_inverted_index",
                })
                url = f"https://api.openalex.org/works?{params}"
                request = urllib.request.Request(url, headers={"User-Agent": f"route-a-audit ({MAILTO})"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    payload = json.loads(response.read())
                handle.write(json.dumps({"query_term": term, "url": url,
                                         "results": payload.get("results", [])}) + "\n")
                urls.append(url)
                cursor = (payload.get("meta") or {}).get("next_cursor")
                time.sleep(0.2)
    return urls


def works_from_snapshot(snapshot: Path) -> list[dict]:
    seen, works = set(), []
    for line in snapshot.read_text(encoding="utf-8").splitlines():
        block = json.loads(line)
        for work in block.get("results", []):
            wid = work.get("id")
            if wid and wid not in seen:
                seen.add(wid)
                works.append(work)
    return works


def run_query(output_prefix: str = "corpus_draw_v1") -> int:
    snapshot = ROOT / f"{output_prefix}.snapshot.jsonl"
    urls = fetch_snapshot(snapshot)
    rows = [candidate_row(work) for work in works_from_snapshot(snapshot)]
    threshold = tier3_threshold(rows)
    rows = apply_tier3_floor(rows, threshold)
    selected, cap_log = stratified_draw(rows)

    candidates_path = ROOT / f"{output_prefix}_candidates.csv"
    with candidates_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(CANDIDATE_COLUMNS)
        for index, row in enumerate(rows, 1):
            row = dict(row)
            row["candidate_id"] = f"C{index:03d}"
            writer.writerow([row.get(column, "") for column in CANDIDATE_COLUMNS])

    selected_ids = {r["openalex_id"] for r in selected}
    corpus_path = ROOT / f"{output_prefix}.csv"
    with corpus_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("rank",) + CANDIDATE_COLUMNS + ("needs_adjudication",))
        for rank, row in enumerate(sorted(selected, key=lambda r: -r["cited_by_count"]), 1):
            flags = "claim-type;tier2-oral-or-spotlight" if row["venue_tier"] == 2 else "claim-type"
            writer.writerow([rank] + [row.get(column, "") for column in CANDIDATE_COLUMNS] + [flags])

    manifest = {
        "protocol": "AUDIT_PREREGISTRATION_v1_FROZEN.md section 3",
        "draw_date": dt.date.today().isoformat(),
        "query": json.loads(build_query()),
        "urls": urls,
        "snapshot_file": snapshot.name,
        "snapshot_sha256": sha256_file(snapshot),
        "works_deduplicated": len(rows),
        "tier3_threshold": threshold,
        "selected": len(selected),
        "accept_range": ACCEPT_RANGE,
        "cap_log": cap_log,
        "corpus_frozen_on_commit_of": corpus_path.name,
    }
    (ROOT / f"{output_prefix}.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"candidates: {len(rows)} -> selected {len(selected)} (target {TARGET_SIZE}, accept {ACCEPT_RANGE})")
    print(f"snapshot {snapshot.name} sha256 {manifest['snapshot_sha256']}")
    print(f"tier3 threshold {threshold}; committing {corpus_path.name} freezes the corpus")
    return 0


def selftest() -> int:
    """Sabotage-verified checks: each filter rejects its own error class, caps bind, replacement is lawful."""
    def work(title, date="2020-06-01", venue="Nature Machine Intelligence", cites=500, abstract=""):
        return {"id": f"https://openalex.org/W{abs(hash(title)) % 10**8}", "doi": "x", "title": title,
                "publication_date": date, "cited_by_count": cites,
                "primary_location": {"source": {"display_name": venue}},
                "abstract_inverted_index": {w: [0] for w in abstract.split()} if abstract else {}}

    # window filter rejects outside-window and undated
    assert candidate_row(work("Brain-inspired learning rule", date="2014-12-31"))["drop_reason"] == "outside window"
    assert candidate_row(work("Brain-inspired learning rule", date=None))["drop_reason"] == "outside window"
    # keyword co-presence: bio without ai drops, ai without bio drops, both keep
    assert candidate_row(work("Hippocampal replay in the sleeping brain"))["drop_reason"] == "no ai term"
    assert candidate_row(work("Reinforcement learning with curiosity"))["drop_reason"] == "no bio term"
    ok = candidate_row(work("Hippocampal replay improves reinforcement learning"))
    assert ok["keep"] and ok["drop_reason"] == ""
    # venue tiers
    assert venue_tier("Nature Machine Intelligence") == 1
    assert venue_tier("Neural Information Processing Systems") == 2
    assert venue_tier("PNAS") == 2
    assert venue_tier("IEEE Transactions on Something") == 3
    assert venue_tier(None) is None
    # family classification is keyword-recorded, fallback other
    assert classify_family("hippocampal replay")[0] == "memory"
    assert classify_family("hebbian plasticity")[0] == "plasticity/learning rules"
    assert classify_family("generic title")[0] == "other"
    # tier-3 floor: with the decile below the floor, the 100 floor binds
    rows = [candidate_row(work(f"Synaptic rule for reinforcement learning {i}", venue="IEEE X", cites=c))
            for i, c in enumerate([5, 50, 99])]
    assert tier3_threshold(rows) == 100, "floor must bind when the decile is below it"
    assert [r["keep"] for r in apply_tier3_floor(rows, 100)] == [False, False, False]
    # tier-3 decile: ten spaced citations, threshold lands at the top-cited tenth and keeps exactly one
    rows10 = [candidate_row(work(f"Synaptic rule for reinforcement learning {i}", venue="IEEE X", cites=c))
              for i, c in enumerate([500, 450, 400, 350, 300, 250, 200, 150, 100, 50])]
    threshold10 = tier3_threshold(rows10)
    assert threshold10 == 500, f"top decile of ten must be the top citation, got {threshold10}"
    assert [r["keep"] for r in apply_tier3_floor(rows10, threshold10)] == [True] + [False] * 9
    # caps bind: 4 same-family keepers, cap 3 -> 4th logged and skipped
    family_rows = [candidate_row(work(f"Spiking network reinforcement learning {i}", venue=f"Venue{i}", cites=100 - i))
                   for i in range(4)]
    family_rows[3]["mechanism_family"] = family_rows[0]["mechanism_family"]
    selected, log = stratified_draw(family_rows)
    assert len(selected) == 3 and any("cap:family" in entry for entry in log)
    venue_rows = [candidate_row(work(f"Spiking reinforcement learning {i}", venue="One Venue", cites=100 - i))
                  for i in range(6)]
    for index, row in enumerate(venue_rows):  # isolate the venue cap: six distinct families at one venue
        row["mechanism_family"] = f"family{index}"
    selected_v, log_v = stratified_draw(venue_rows)
    assert len(selected_v) == min(VENUE_CAP, TARGET_SIZE) and any("cap:venue" in e for e in log_v)
    # replacement: same family and tier, next-highest citation, never an already-taken id
    pool = [
        candidate_row(work("Hippocampal replay reinforcement learning A", venue="IEEE X", cites=300)),
        candidate_row(work("Hippocampal replay reinforcement learning B", venue="IEEE X", cites=200)),
        candidate_row(work("Spiking circuits reinforcement learning C", venue="IEEE X", cites=900)),
    ]
    pool[0]["mechanism_family"] = pool[1]["mechanism_family"] = "memory"
    pool[2]["mechanism_family"] = "neuromorphic hardware"
    sel = [pool[0], pool[2]]
    pick = replacement_pick(pool, sel, pool[0]["openalex_id"])
    assert pick is not None and pick["openalex_id"] == pool[1]["openalex_id"], "same stratum, next citation"
    # and the tie rule for disagreements is out of scope here; this instrument draws, it does not code
    print("selftest: all checks passed (filters reject their error classes; caps and replacement bind)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", action="store_true", help="run the live draw from OpenAlex")
    group.add_argument("--selftest", action="store_true", help="run the sabotage-verified checks")
    parser.add_argument("--max-terms", type=int, default=None,
                        help="limit bio terms fetched (smoke only; a real draw never uses this)")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.max_terms is not None:
        print("NOTE: --max-terms produces a smoke snapshot, NOT a corpus of record", file=sys.stderr)
    return run_query()


if __name__ == "__main__":
    raise SystemExit(main())
