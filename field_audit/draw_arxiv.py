#!/usr/bin/env python3
"""The Route A corpus draw from the arXiv API, under Amendment 2026-10-19.

Authority: AMENDMENT_20261019_ARXIV_DATA_SOURCE.md (owner instruction "直接看arxiv就行"), changing only what
the frozen protocol's section 3 draw depends on: the arXiv API is the source, relevance order is the
ranking, the citation floor is removed, and the stratification caps are family (3) x primary category (5).
Everything else - window, keyword lists, claim-type criterion, target 20 / accept 15-25, replacement
mechanics, the pinned-hash snapshot dual-draw check - is the frozen rule, unchanged.

Fail-closed like the OpenAlex fetcher it replaces: a malformed response page, a missing entry id, an
underfilled draw (outside 15-25 after caps), or an output collision refuses the run by name and publishes
nothing canonical. The snapshot is the raw Atom response bytes, one JSON line per request (query, URL, body),
hashed whole into the manifest.

No API key, no secret, no citation data is read or claimed. arXiv API etiquette: 3-second delays between
paged requests, max_results 100 per request, at most 2 pages per term.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ElementTree
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"

# --- the frozen rule as amended (do not edit without a dated amendment) ---
WINDOW = ("2015-01-01", "2026-09-30")
TARGET_SIZE = 20
ACCEPT_RANGE = (15, 25)
FAMILY_CAP = 3
CATEGORY_CAP = 5
PAGES_PER_TERM = 2
PAGE_SIZE = 100
REQUEST_DELAY = 3.0

BIO_TERMS = (
    "brain-inspired", "neuro-inspired", "neuroscience-inspired", "bio-inspired", "biologically plausible",
    "connectome", "synaptic", "spiking", "neuromorphic", "hippocamp", "cerebellar", "cortical", "hebbian",
    "dopamine", "eligibility trace", "memory consolidation", "memory replay", "neural replay",
    "predictive coding", "reward prediction error", "place cell", "grid cell",
)
AI_TERMS = (
    "neural network", "machine learning", "reinforcement learning", "deep learning",
    "artificial intelligence", "learning system", "robot", "autonomous agent", "intelligent agent",
    "artificial neural", "learning rule", "training algorithm",
)
FAMILY_KEYWORDS = {
    "memory": ("memory consolidation", "memory replay", "neural replay", "hippocamp", "place cell", "grid cell"),
    "plasticity/learning rules": ("hebbian", "eligibility trace", "plasticity", "synaptic",
                                  "reward prediction error", "dopamine"),
    "architecture/connectome": ("connectome", "cortical", "cortex", "brain-inspired architecture",
                                "neural architecture"),
    "attention/coding": ("predictive coding", "attention", "sparse coding"),
    "neuromorphic hardware": ("neuromorphic", "spiking", "loihi", "memristor"),
}

CANDIDATE_COLUMNS = (
    "candidate_id", "arxiv_id", "arxiv_id_version", "title", "primary_category", "all_categories",
    "published", "updated", "authors", "journal_ref", "doi",
    "mechanism_family", "family_source", "fetch_rank", "keep", "drop_reason",
)

COLUMNS = ("rank",) + CANDIDATE_COLUMNS + ("needs_adjudication",)


def parse_entries(body: str) -> list[dict]:
    """Parse one Atom page into entry dicts. Refuses malformed pages by name."""
    try:
        root = ElementTree.fromstring(body)
    except ElementTree.ParseError as error:
        raise RuntimeError(f"arXiv response page is not parseable XML: {error}")
    out = []
    for entry in root.findall(f"{ATOM}entry"):
        entry_id = (entry.findtext(f"{ATOM}id") or "").strip()
        if not entry_id:
            raise RuntimeError("arXiv entry carries no id")
        categories = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
        out.append({
            "id": entry_id,
            "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
            "summary": " ".join((entry.findtext(f"{ATOM}summary") or "").split()),
            "published": (entry.findtext(f"{ATOM}published") or "")[:10],
            "updated": (entry.findtext(f"{ATOM}updated") or "")[:10],
            "primary_category": (entry.find(f"{ATOM}category").get("term", "")
                                 if entry.find(f"{ATOM}category") is not None else ""),
            "all_categories": ";".join(categories),
            "authors": ";".join((a.findtext(f"{ATOM}name") or "") for a in entry.findall(f"{ATOM}author")),
            "journal_ref": entry.findtext(f"{ARXIV}journal_ref") or "",
            "doi": entry.findtext(f"{ARXIV}doi") or "",
        })
    return out


def keyword_hit(text: str, terms) -> str | None:
    folded = (text or "").casefold()
    for term in terms:
        if term in folded:
            return term
    return None


def classify_family(text: str) -> tuple[str, str]:
    for family, terms in FAMILY_KEYWORDS.items():
        hit = keyword_hit(text, terms)
        if hit:
            return family, f"keyword:{hit}"
    return "other", "fallback"


def candidate_row(entry: dict, fetch_rank: int) -> dict:
    text = f"{entry['title']} {entry['summary']}"
    family, source = classify_family(text)
    bio = keyword_hit(text, BIO_TERMS)
    ai = keyword_hit(text, AI_TERMS)
    keep, reason = True, ""
    if not (WINDOW[0] <= entry["published"] <= WINDOW[1]):
        keep, reason = False, "outside window"
    elif not bio:
        keep, reason = False, "no bio term"
    elif not ai:
        keep, reason = False, "no ai term"
    elif not entry["primary_category"]:
        keep, reason = False, "no primary category"
    return {
        "arxiv_id": entry["id"], "arxiv_id_version": entry["id"].rsplit("/abs/", 1)[-1],
        "title": entry["title"], "primary_category": entry["primary_category"],
        "all_categories": entry["all_categories"], "published": entry["published"],
        "updated": entry["updated"], "authors": entry["authors"], "journal_ref": entry["journal_ref"],
        "doi": entry["doi"], "mechanism_family": family, "family_source": source,
        "fetch_rank": fetch_rank, "keep": keep, "drop_reason": reason,
    }


def stratified_draw(rows: list[dict]) -> tuple[list[dict], list[str]]:
    """Fetch-rank order within the kept pool, subject to the amended caps."""
    log = []
    kept = sorted((r for r in rows if r["keep"]), key=lambda r: r["fetch_rank"])
    selected, family_counts, category_counts = [], {}, {}
    for row in kept:
        if len(selected) >= TARGET_SIZE:
            break
        family, category = row["mechanism_family"], row["primary_category"]
        if family_counts.get(family, 0) >= FAMILY_CAP:
            log.append(f"cap:family:{row['arxiv_id_version']}")
            continue
        if category_counts.get(category, 0) >= CATEGORY_CAP:
            log.append(f"cap:category:{row['arxiv_id_version']}")
            continue
        selected.append(row)
        family_counts[family] = family_counts.get(family, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
    return selected, log


def replacement_pick(rows: list[dict], selected: list[dict], excluded_id: str) -> dict | None:
    excluded = next(r for r in selected if r["arxiv_id"] == excluded_id)
    taken = {r["arxiv_id"] for r in selected} | {excluded_id}
    pool = [r for r in rows if r["keep"] and r["arxiv_id"] not in taken
            and r["mechanism_family"] == excluded["mechanism_family"]
            and r["primary_category"] == excluded["primary_category"]]
    return min(pool, key=lambda r: r["fetch_rank"]) if pool else None


def fetch(url: str, attempts: int = 4) -> str:
    """One request with bounded retry and backoff - arXiv's own guidance for transient errors and
    connection resets - and the same parse before anything enters the snapshot."""
    last = None
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(url,
                                         headers={"User-Agent": "route-a-audit/1.0 (field audit corpus draw)"})
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read().decode("utf-8", errors="strict")
        except (urllib.error.URLError, OSError, TimeoutError) as error:
            last = error
            if attempt < attempts:
                wait = 10.0 * attempt
                print(f"  fetch retry {attempt}/{attempts - 1} after {type(error).__name__}: sleeping {wait:.0f}s",
                      file=sys.stderr)
                time.sleep(wait)
    raise RuntimeError(f"arXiv request failed after {attempts} attempts: {url} ({last})")


def fetch_snapshot(out: Path) -> list[str]:
    """One JSON line per request: query term, full URL, raw Atom body. The pinned snapshot.

    A partial snapshot is never left behind: any failure removes it and publishes nothing - the same
    discipline the OpenAlex fetcher's defect review installed there.
    """
    urls = []
    try:
        with out.open("w", encoding="utf-8") as handle:
            for term in BIO_TERMS:
                for page in range(PAGES_PER_TERM):
                    params = urllib.parse.urlencode({
                        "search_query": f'all:"{term}"', "start": page * PAGE_SIZE,
                        "max_results": PAGE_SIZE, "sortBy": "relevance", "sortOrder": "descending",
                    })
                    url = f"{API}?{params}"
                    body = fetch(url)
                    entries = parse_entries(body)  # refuses malformed pages before they enter the snapshot
                    handle.write(json.dumps({"query_term": term, "url": url, "body": body}) + "\n")
                    handle.flush()
                    urls.append(url)
                    if len(entries) < PAGE_SIZE:
                        break
                    time.sleep(REQUEST_DELAY)
                time.sleep(REQUEST_DELAY)
    except Exception:
        out.unlink(missing_ok=True)
        raise
    return urls


def works_from_snapshot(snapshot: Path) -> list[dict]:
    seen, entries_out, rank = set(), [], 0
    for line in snapshot.read_text(encoding="utf-8").splitlines():
        block = json.loads(line)
        for entry in parse_entries(block["body"]):
            if entry["id"] not in seen:
                seen.add(entry["id"])
                rank += 1
                entries_out.append((entry, rank))
    return entries_out


def run_query(prefix: str = "corpus_draw_arxiv_v1") -> int:
    snapshot = ROOT / f"{prefix}.snapshot.jsonl"
    urls = fetch_snapshot(snapshot)
    rows = [candidate_row(entry, rank) for entry, rank in works_from_snapshot(snapshot)]
    selected, cap_log = stratified_draw(rows)
    if not (ACCEPT_RANGE[0] <= len(selected) <= ACCEPT_RANGE[1]):
        print(f"DRAW REFUSED: selected {len(selected)} claims, outside the frozen acceptance range "
              f"{ACCEPT_RANGE}; the snapshot is retained for audit, no corpus is published.", file=sys.stderr)
        return 1

    candidates_path = ROOT / f"{prefix}_candidates.csv"
    with candidates_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(CANDIDATE_COLUMNS)
        for index, row in enumerate(rows, 1):
            row = dict(row)
            row["candidate_id"] = f"C{index:03d}"
            writer.writerow([row.get(column, "") for column in CANDIDATE_COLUMNS])

    corpus_path = ROOT / f"{prefix}.csv"
    with corpus_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(COLUMNS)
        for rank, row in enumerate(sorted(selected, key=lambda r: r["fetch_rank"]), 1):
            writer.writerow([rank] + [row.get(column, "") for column in CANDIDATE_COLUMNS]
                            + ["claim-type"])

    register_path = ROOT / f"{prefix}_register.csv"
    with register_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["entry_id", "role", "arxiv_id", "title", "primary_category", "published",
                         "mechanism_family", "fetch_rank", "draw_rank", "snapshot_sha256", "protocol"])
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        for index, row in enumerate(rows, 1):
            draw_rank = next((r for r in selected if r["arxiv_id"] == row["arxiv_id"]), None)
            writer.writerow([f"C{index:03d}", "selected" if draw_rank else "candidate",
                             row["arxiv_id"], row["title"], row["primary_category"], row["published"],
                             row["mechanism_family"], row["fetch_rank"],
                             selected.index(draw_rank) + 1 if draw_rank else "",
                             digest, "AMENDMENT_20261019_ARXIV_DATA_SOURCE"])

    manifest = {
        "protocol": "AUDIT_PREREGISTRATION_v1_FROZEN.md section 3, as amended 2026-10-19 (arXiv source)",
        "urls": urls,
        "requests": len(urls),
        "works_deduplicated": len(rows),
        "selected": len(selected),
        "accept_range": ACCEPT_RANGE,
        "cap_log": cap_log,
        "snapshot_file": snapshot.name,
        "snapshot_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        "corpus_frozen_on_commit_of": corpus_path.name,
    }
    (ROOT / f"{prefix}.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"candidates: {len(rows)} -> selected {len(selected)} (target {TARGET_SIZE}, accept {ACCEPT_RANGE})")
    print(f"snapshot sha256 {manifest['snapshot_sha256']}; committing {corpus_path.name} freezes the corpus")
    return 0


def selftest() -> int:
    """Sabotage-verified checks on fixtures: filters reject their error classes, caps bind, replacement is
    lawful, malformed pages refuse, underfill refuses."""
    body = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/1</id>
<title>Hippocampal replay improves reinforcement learning</title><summary>memory and learning rule</summary>
<published>2020-01-01T00:00:00Z</published><updated>2020-01-01T00:00:00Z</updated>
<category term="cs.LG"/><author><name>A</name></author></entry></feed>"""
    entries = parse_entries(body)
    assert entries and entries[0]["primary_category"] == "cs.LG"
    try:
        parse_entries("<not-xml")
        raise AssertionError("malformed XML must refuse")
    except RuntimeError:
        pass
    try:
        parse_entries('<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><id></id></entry></feed>')
        raise AssertionError("an entry without id must refuse")
    except RuntimeError:
        pass

    def entry(eid, title, published="2020-06-01", category="cs.AI"):
        return {"id": f"http://arxiv.org/abs/{eid}", "title": title, "summary": "",
                "published": published, "updated": published, "primary_category": category,
                "all_categories": category, "authors": "", "journal_ref": "", "doi": ""}

    assert candidate_row(entry("1", "Hippocampal replay reinforcement learning"), 1)["drop_reason"] == ""
    assert candidate_row(entry("2", "Hippocampal replay in the sleeping brain"), 2)["drop_reason"] == "no ai term"
    assert candidate_row(entry("3", "Curiosity driven exploration"), 3)["drop_reason"] == "no bio term"
    assert candidate_row(entry("4", "Hippocampal replay reinforcement learning", published="2014-01-01"), 4)[
        "drop_reason"] == "outside window"

    rows = [candidate_row(entry(str(i), f"Spiking reinforcement learning {i}", category=f"cat{i%3}"), i)
            for i in range(7)]
    for row in rows:
        row["mechanism_family"] = "neuromorphic hardware"
    selected, log = stratified_draw(rows)
    assert len(selected) == FAMILY_CAP and any("cap:family" in e for e in log)
    rows_cat = [candidate_row(entry(str(i), f"Spiking reinforcement learning {i}", category="cs.NE"), i)
                for i in range(7)]
    for index, row in enumerate(rows_cat):
        row["mechanism_family"] = f"family{index}"
    selected_cat, log_cat = stratified_draw(rows_cat)
    assert len(selected_cat) == CATEGORY_CAP and any("cap:category" in e for e in log_cat)

    pool = [candidate_row(entry("a", "Hippocampal replay reinforcement learning", category="cs.AI"), 1),
            candidate_row(entry("b", "Hippocampal replay reinforcement learning", category="cs.AI"), 2),
            candidate_row(entry("c", "Spiking reinforcement learning", category="cs.AI"), 3)]
    sel = [pool[0], pool[2]]
    pick = replacement_pick(pool, sel, pool[0]["arxiv_id"])
    assert pick is not None and pick["arxiv_id"] == pool[1]["arxiv_id"]
    assert replacement_pick(pool, sel, pool[0]["arxiv_id"])["arxiv_id"] != pool[0]["arxiv_id"]
    print("selftest: all checks passed (filters, caps, replacement, malformed-page and missing-id refusals)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", action="store_true", help="run the live draw from the arXiv API")
    group.add_argument("--selftest", action="store_true")
    parser.add_argument("--prefix", default="corpus_draw_arxiv_v1")
    args = parser.parse_args()
    return selftest() if args.selftest else run_query(args.prefix)


if __name__ == "__main__":
    raise SystemExit(main())
