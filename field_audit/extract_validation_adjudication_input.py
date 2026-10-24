#!/usr/bin/env python3
"""Extract per-candidate title/abstract/query_term from the pinned snapshot for the P0-3
validation claim-type adjudication (VALIDATION_RESUMPTION_20261025.md, Gate 0.5: RUN).

Failure-class checks (a green run on this instrument must be able to fail):
- snapshot sha256 must equal the pinned value (e73f72f5...);
- every candidate in corpus_validation_draw_v1.csv must be found in the snapshot;
- every candidate must appear under the FIRST query term (brain-inspired) - the owner's
  RETAIN-and-NARROW boundary (else exit 1; the resumption record section 2);
- --selftest exercises the first three failure classes on fabricated inputs and must FAIL
  on mutants (wrong hash, missing ID, non-first-query ID).
"""
import csv
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "corpus_draw_arxiv_v1.snapshot.jsonl"
DRAW = ROOT / "corpus_validation_draw_v2.csv"
OUT = ROOT / "VALIDATION_ADJUDICATION_INPUT_20261025.csv"
PINNED_SHA = "e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee"
FIRST_QUERY = "brain-inspired"
NS = {"a": "http://www.w3.org/2005/Atom"}


def load_index(snapshot_text):
    """arxiv abs id -> {query_terms set, title, summary} from per-line Atom feeds."""
    idx = {}
    for line in snapshot_text.splitlines():
        if not line.strip():
            continue
        import json
        rec = json.loads(line)
        qt = rec["query_term"]
        root = ET.fromstring(rec["body"])
        for e in root.findall("a:entry", NS):
            eid = e.find("a:id", NS).text.strip()
            m = re.search(r"abs/(\S+)$", eid)
            if not m:
                continue
            aid = m.group(1)
            ent = idx.setdefault(aid, {"query_terms": set(), "title": "", "summary": ""})
            ent["query_terms"].add(qt)
            ent["title"] = re.sub(r"\s+", " ", e.find("a:title", NS).text or "").strip()
            ent["summary"] = re.sub(r"\s+", " ", e.find("a:summary", NS).text or "").strip()
    return idx


def extract(snapshot_text, candidates, sha):
    """Returns (rows, errors). errors non-empty => refuse."""
    errors = []
    if sha != PINNED_SHA:
        errors.append(f"snapshot sha256 {sha[:12]}... != pinned {PINNED_SHA[:12]}...")
    idx = load_index(snapshot_text)
    rows = []
    for c in candidates:
        aid = c["arxiv_id_version"]
        ent = idx.get(aid)
        if ent is None:
            errors.append(f"candidate {c['candidate_id']} ({aid}) not in snapshot")
            continue
        if FIRST_QUERY not in ent["query_terms"]:
            errors.append(f"candidate {c['candidate_id']} ({aid}) not under first query "
                          f"(terms: {sorted(ent['query_terms'])})")
            continue
        rows.append({
            "candidate_id": c["candidate_id"], "band": c["band"],
            "arxiv_id_version": aid, "query_term": FIRST_QUERY,
            "fetch_rank": c["fetch_rank"], "mechanism_family": c["mechanism_family"],
            "primary_category": c["primary_category"], "title": ent["title"],
            "abstract": ent["summary"],
        })
    return rows, errors


def selftest():
    snapshot_line = ('{"query_term": "brain-inspired", "url": "u", "body": '
                     '"<?xml version=\'1.0\'?><feed xmlns=\\"http://www.w3.org/2005/Atom\\">'
                     '<entry><id>http://arxiv.org/abs/1234.5678v1</id><title>T</title>'
                     '<summary>S</summary></entry></feed>"}')
    other_line = ('{"query_term": "other-term", "url": "u", "body": '
                  '"<?xml version=\'1.0\'?><feed xmlns=\\"http://www.w3.org/2005/Atom\\">'
                  '<entry><id>http://arxiv.org/abs/9999.9999v1</id><title>X</title>'
                  '<summary>Y</summary></entry></feed>"}')
    good = {"candidate_id": "C001", "band": "b", "arxiv_id_version": "1234.5678v1",
            "fetch_rank": "1", "mechanism_family": "f", "primary_category": "cs.AI"}
    ok = []
    # 1. wrong hash refused
    ok.append(("wrong hash refused", extract(snapshot_line, [good], "deadbeef")[1] != []))
    # 2. missing id refused
    missing = dict(good, arxiv_id_version="0000.0000v1")
    ok.append(("missing id refused", extract(snapshot_line, [missing], PINNED_SHA)[1] != []))
    # 3. non-first-query id refused
    otherq = dict(good, candidate_id="C002", arxiv_id_version="9999.9999v1")
    ok.append(("non-first-query refused",
               extract(snapshot_line + "\n" + other_line, [otherq], PINNED_SHA)[1] != []))
    # 4. clean pass
    rows, errs = extract(snapshot_line, [good], PINNED_SHA)
    ok.append(("clean pass", errs == [] and len(rows) == 1 and rows[0]["abstract"] == "S"))
    bad = [n for n, p in ok if not p]
    if bad:
        print("SELFTEST FAIL:", bad)
        sys.exit(1)
    print(f"SELFTEST PASS ({len(ok)} assertions)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    snap_bytes = SNAPSHOT.read_bytes()
    sha = hashlib.sha256(snap_bytes).hexdigest()
    cands = []
    for r in csv.DictReader(open(DRAW)):
        cands.append({
            "candidate_id": r["arxiv_id_version"], "band": r["band"],
            "arxiv_id_version": r["arxiv_id_version"],
            "fetch_rank": r["fetch_rank"], "mechanism_family": r["mechanism_family"],
            "primary_category": r["primary_category"],
        })
    rows, errors = extract(snap_bytes.decode("utf-8", errors="replace"), cands, sha)
    if errors:
        print("EXTRACTION REFUSED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    empty_abs = [r["candidate_id"] for r in rows if not r["abstract"].strip()]
    print(f"extracted {len(rows)}/{len(cands)} candidates -> {OUT.name}; "
          f"empty abstracts: {empty_abs if empty_abs else 'none'}")
