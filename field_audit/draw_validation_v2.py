#!/usr/bin/env python3
"""Validation corpus draw v2 (P0-3 resumption, VALIDATION_RESUMPTION_20261025.md).

Supersedes corpus_validation_draw_v1 (144c41e): the v1 draw pooled all 22 query terms and so
placed 12 of 60 candidates outside the owner's first-query boundary (RETAIN-and-NARROW,
2026-10-20). v2 draws from the FIRST-QUERY pool only, under the otherwise unchanged frozen
validation rule (VALIDATION_CORPUS_RULE_20261023.md): year bands 2015-2019 / 2020-2022 /
2023-2026, 20-per-band target with >=8 required, family cap 4 and category cap 6 within band,
fetch_rank order within band, pilot-disjoint, acceptance 45-75.

Failure-class checks (--selftest): band-floor refusal (a band below 8 must refuse the whole
draw), acceptance-range refusal, first-query-only enforcement (a pooled record must never enter
the pool), pilot exclusion, cap binding. A green run on an instrument that cannot fail is not
evidence.
"""
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "corpus_draw_arxiv_v1.snapshot.jsonl"
PILOT_DRAW = ROOT / "corpus_draw_arxiv_v1.csv"
PILOT_ADJ = ROOT / "CLAIM_TYPE_ADJUDICATION_20261020.csv"
V1_DRAW = ROOT / "corpus_validation_draw_v1.csv"
OUT = ROOT / "corpus_validation_draw_v2.csv"
PINNED_SHA = "e73f72f564de1c865fdf12d3ec3c8bbd34d2a7483e5c66acb2a83ba2fcac3aee"
FIRST_QUERY = "brain-inspired"
WINDOW = ("2015-01-01", "2026-09-30")
BANDS = (("2015-2019", 2015, 2019), ("2020-2022", 2020, 2022), ("2023-2026", 2023, 2026))
PER_BAND_TARGET, PER_BAND_FLOOR = 20, 8
FAMILY_CAP, CATEGORY_CAP = 4, 6
ACCEPT = (45, 75)
BIO_TERMS = ("brain-inspired", "neuro-inspired", "neuroscience-inspired", "bio-inspired", "biology-inspired",
             "biologically inspired", "biologically plausible", "connectome", "synaptic", "spiking",
             "neuromorphic", "hippocamp", "hippocampus", "cerebellar", "cortex", "cortical", "hebbian",
             "dopamine", "eligibility trace", "memory consolidation", "memory replay", "neural replay",
             "predictive coding", "reward prediction error", "place cell", "grid cell")
AI_TERMS = ("neural network", "machine learning", "reinforcement learning", "deep learning",
            "artificial intelligence", "learning system", "robot", "autonomous agent", "intelligent agent",
            "artificial neural", "learning rule", "training algorithm")
FAMILY_KEYWORDS = {
    "memory": ("memory consolidation", "memory replay", "neural replay", "hippocamp", "place cell", "grid cell", "hippocampus"),
    "plasticity/learning rules": ("hebbian", "eligibility trace", "plasticity", "synaptic", "reward prediction error", "dopamine"),
    "architecture/connectome": ("connectome", "cortical", "cortex", "brain-inspired architecture", "neural architecture"),
    "attention/coding": ("predictive coding", "attention", "sparse coding"),
    "neuromorphic hardware": ("neuromorphic", "spiking", "loihi", "memristor"),
}
NS = {"a": "http://www.w3.org/2005/Atom"}


def parse_snapshot(text):
    """First-query entries in response order; returns [{aid, rank, title, abs, pub, cat}]."""
    out, seen = [], set()
    rank = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec["query_term"] != FIRST_QUERY:
            continue  # the owner boundary: later query terms never enter the v2 pool
        root = ET.fromstring(rec["body"])
        for e in root.findall("a:entry", NS):
            aid = re.search(r"abs/(\S+)$", e.find("a:id", NS).text.strip()).group(1)
            if aid in seen:
                continue
            seen.add(aid)
            rank += 1
            out.append({
                "aid": aid, "rank": rank,
                "title": re.sub(r"\s+", " ", e.find("a:title", NS).text or "").strip(),
                "abs": re.sub(r"\s+", " ", e.find("a:summary", NS).text or "").strip(),
                "pub": (e.find("a:published", NS).text or "")[:10],
                "cat": e.find("{http://arxiv.org/schemas/atom}primary_category", NS).get("term", "")
                        if e.find("{http://arxiv.org/schemas/atom}primary_category", NS) is not None else "",
            })
    return out


def eligible(entry):
    text = (entry["title"] + " " + entry["abs"]).casefold()
    if not (WINDOW[0] <= entry["pub"] <= WINDOW[1]):
        return False, "outside window"
    if not any(t in text for t in BIO_TERMS):
        return False, "no bio term"
    if not any(t in text for t in AI_TERMS):
        return False, "no ai term"
    return True, ""


def family_of(entry):
    text = (entry["title"] + " " + entry["abs"]).casefold()
    for fam, kws in FAMILY_KEYWORDS.items():
        hit = next((k for k in kws if k in text), None)
        if hit:
            return fam, f"keyword:{hit}"
    return "other", "fallback"


def band_of(pub):
    y = int(pub[:4])
    for name, lo, hi in BANDS:
        if lo <= y <= hi:
            return name
    return None


def draw(entries, exclude):
    """The frozen rule: per band, fetch_rank order, family<=4 and category<=6 within band.
    Returns (selected, refused_reason). refusal => selected is None."""
    pool = []
    for e in entries:
        ok, why = eligible(e)
        if not ok or e["aid"] in exclude:
            continue
        fam, fsrc = family_of(e)
        pool.append(dict(e, band=band_of(e["pub"]), fam=fam, fsrc=fsrc))
    pool = [p for p in pool if p["band"]]
    selected = []
    for name, _, _ in BANDS:
        band_pool = sorted((p for p in pool if p["band"] == name), key=lambda p: p["rank"])
        if len(band_pool) < PER_BAND_FLOOR:
            return None, f"band {name} has {len(band_pool)} eligible records, below the frozen floor {PER_BAND_FLOOR}"
        fam_ct, cat_ct = Counter(), Counter()
        taken = 0
        for p in band_pool:
            if taken >= PER_BAND_TARGET:
                break
            if fam_ct[p["fam"]] >= FAMILY_CAP or cat_ct[p["cat"]] >= CATEGORY_CAP:
                continue
            selected.append(p)
            fam_ct[p["fam"]] += 1
            cat_ct[p["cat"]] += 1
            taken += 1
    if not ACCEPT[0] <= len(selected) <= ACCEPT[1]:
        return None, f"draw size {len(selected)} outside frozen acceptance {ACCEPT}"
    return selected, ""


def selftest():
    # family phrase rotation so fixture bands can reach their targets under the family cap
    FAM_PHRASES = ("hippocampal replay", "synaptic plasticity", "cortical connectome",
                   "predictive coding attention", "memristor neuromorphic", "brain-inspired design")

    def ent(aid, rank, i, pub="2021-05-01"):
        cat = ["cs.AI", "cs.NE", "cs.CV", "cs.RO", "cs.LG", "cs.SY"][i % 6]
        return {"aid": aid, "rank": rank, "title": f"{FAM_PHRASES[i % 6]} neural network study {aid}",
                "abs": "deep learning", "pub": pub, "cat": cat}
    ok = []
    # 1. first-query-only: parse_snapshot must skip other query terms
    other = ('{"query_term": "neuro-inspired", "body": "<?xml version=\'1.0\'?><feed xmlns=\\"http://www.w3.org/2005/Atom\\">'
             '<entry><id>http://arxiv.org/abs/1111.1111v1</id><title>Spiking neural network brain</title>'
             '<summary>deep learning</summary><published>2021-01-01T00:00:00Z</published></entry></feed>"}')
    ok.append(("non-first-query excluded from pool", parse_snapshot(other) == []))
    # 2. band floor refusal: 7 early-band records must refuse
    early7 = [ent(f"1901.0000{i}v1", 100 + i, i, pub="2018-01-01") for i in range(7)]
    mid20 = [ent(f"2001.0000{i}v1", 200 + i, i, pub="2021-01-01") for i in range(20)]
    late20 = [ent(f"2301.0000{i}v1", 300 + i, i, pub="2024-01-01") for i in range(20)]
    sel, why = draw(early7 + mid20 + late20, set())
    ok.append(("band floor refusal", sel is None and "2015-2019" in why and "floor" in why))
    # 3. clean draw: 10/20/20 = 50 within acceptance
    early10 = [ent(f"1902.0000{i}v1", 100 + i, i, pub="2018-01-01") for i in range(10)]
    sel, why = draw(early10 + mid20 + late20, set())
    ok.append(("clean 10/20/20 draw", sel is not None and len(sel) == 50))
    bands = Counter(p["band"] for p in sel)
    ok.append(("band sizes honored", bands["2015-2019"] == 10 and bands["2020-2022"] == 20 and bands["2023-2026"] == 20))
    # 4. family cap binds within band: 5 same-family records in one band -> at most 4 taken
    fam5 = [ent(f"1903.0000{i}v1", 80 + i, 0, pub="2017-01-01") for i in range(5)]
    fill = [ent(f"1904.0000{i}v1", 90 + i, 4, pub="2017-01-01") for i in range(6)]
    sel2, _ = draw(fam5 + fill + early10 + mid20 + late20, set())
    fams = Counter(p["fam"] for p in sel2 if p["band"] == "2015-2019")
    ok.append(("family cap 4 binds", fams["memory"] <= 4))
    # 5. pilot exclusion: an excluded aid never enters
    sel3, _ = draw(early10 + mid20 + late20, {early10[0]["aid"]})
    ok.append(("pilot exclusion holds", sel3 is not None and early10[0]["aid"] not in {p['aid'] for p in sel3}))
    # 6. acceptance refusal: 8/8/8 = 24 < 45 must refuse
    tiny = [ent(f"1905.0000{i}v1", 60 + i, i, pub="2018-01-01") for i in range(8)]
    tiny2 = [ent(f"2005.0000{i}v1", 61 + i, i, pub="2021-01-01") for i in range(8)]
    tiny3 = [ent(f"2305.0000{i}v1", 62 + i, i, pub="2024-01-01") for i in range(8)]
    sel4, why4 = draw(tiny + tiny2 + tiny3, set())
    ok.append(("acceptance range refusal", sel4 is None and "acceptance" in why4))
    bad = [n for n, p in ok if not p]
    if bad:
        print("SELFTEST FAIL:", bad)
        sys.exit(1)
    print(f"SELFTEST PASS ({len(ok)} assertions)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    snap = SNAPSHOT.read_bytes()
    sha = hashlib.sha256(snap).hexdigest()
    if sha != PINNED_SHA:
        print(f"REFUSED: snapshot sha256 {sha[:12]}... != pinned")
        sys.exit(1)
    exclude = set()
    for path, col in ((PILOT_DRAW, "arxiv_id_version"), (PILOT_ADJ, "arxiv_id_version")):
        for row in csv.DictReader(open(path)):
            if row.get(col):
                exclude.add(row[col])
    entries = parse_snapshot(snap.decode("utf-8", errors="replace"))
    selected, why = draw(entries, exclude)
    if selected is None:
        print("DRAW REFUSED:", why)
        sys.exit(1)
    # cross-check: fetch_rank must agree with v1 for shared first-query records
    v1_ranks = {r["arxiv_id_version"]: r["fetch_rank"] for r in csv.DictReader(open(V1_DRAW))}
    mism = [(p["aid"], p["rank"], v1_ranks[p["aid"]]) for p in selected
            if p["aid"] in v1_ranks and str(p["rank"]) != v1_ranks[p["aid"]]]
    if mism:
        print(f"REFUSED: fetch_rank disagrees with v1 draw for {len(mism)} records: {mism[:3]}")
        sys.exit(1)
    shared = sum(1 for p in selected if p["aid"] in v1_ranks)
    cols = ["band", "fetch_rank", "arxiv_id_version", "title", "primary_category", "published",
            "mechanism_family", "family_source", "query_term"]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in sorted(selected, key=lambda p: (p["band"], p["rank"])):
            w.writerow({"band": p["band"], "fetch_rank": p["rank"], "arxiv_id_version": p["aid"],
                        "title": p["title"], "primary_category": p["cat"], "published": p["pub"],
                        "mechanism_family": p["fam"], "family_source": p["fsrc"], "query_term": FIRST_QUERY})
    print(f"v2 draw: {len(selected)} claims; bands {dict(Counter(p['band'] for p in selected))}; "
          f"families {dict(Counter(p['fam'] for p in selected))}; "
          f"shared with v1 (first-query part): {shared}; pilot-excluded set: {len(exclude)}; "
          f"snapshot sha verified -> {OUT.name}")
