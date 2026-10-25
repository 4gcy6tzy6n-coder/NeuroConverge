#!/usr/bin/env python3
"""Fetch the pinned arXiv full texts/PDFs that are intentionally not redistributed in this
repository (rights review 2026-10-26: papers under the default arXiv non-exclusive license and
CC BY-NC-ND are not redistributed; see ARXIV_LICENSE_AUDIT_20261026.csv and pinned_validation_
20261025/ATTRIBUTION.md). arXiv serves these files publicly; this script downloads them for
LOCAL VERIFICATION USE, placing each at the path the audit chain expects and verifying its
SHA-256 against the committed manifest. Nothing is re-distributed by this script.

Manifest-driven and resume-safe: existing verified files are skipped; a failed download leaves
no file behind. Run it once after a fresh clone if you need the full-text-dependent checks
(run_final_scoring_20261024.py, robustness_survey_exclusion_20261025.py, quote checks beyond
the committed permissive texts).

    python3 field_audit/fetch_pinned_from_arxiv.py [--manifests primary,validation]

Rate limit: 3 s between requests (arXiv's stated courtesy rate).
"""
import argparse
import csv
import hashlib
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = {"User-Agent": "NeuroConverge-Route-A-verification-fetch (compliance: local use only)"}
MANIFESTS = {
    "primary": (ROOT / "pinned_fulltext_20261020/FULLTEXT_DOWNLOAD_MANIFEST_20261020.csv",
                "sha256", ROOT / "fulltexts", lambda row: f"{row['arxiv_id_version']}.pdf"),
    "validation": (ROOT / "pinned_validation_20261025/FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv",
                   "pdf_sha256", ROOT / "pinned_validation_20261025/pdfs",
                   lambda row: f"{row['arxiv_id_version']}.pdf"),
}


def fetch(manifest_path, hash_col, out_dir, name_fn):
    rows = list(csv.DictReader(open(manifest_path)))
    todo = []
    for r in rows:
        if r["download_status"] != "open_access_downloaded":
            continue  # withdrawn/failed records have no file by design
        aid = r["arxiv_id_version"]
        out = out_dir / name_fn(r)
        if out.is_file():
            if hashlib.sha256(out.read_bytes()).hexdigest() == r[hash_col]:
                continue  # already present and verified
        todo.append((aid, out, r[hash_col]))
    print(f"{manifest_path.name}: {len(todo)} file(s) to fetch of {len(rows)} rows")
    ok = fail = 0
    for aid, out, want in todo:
        url = f"https://arxiv.org/pdf/{aid}"
        for attempt in (1, 2):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=90) as resp:
                    data = resp.read()
                got = hashlib.sha256(data).hexdigest()
                if got != want:
                    raise ValueError(f"sha256 mismatch (got {got[:12]}... want {want[:12]}...)")
                out_dir.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
                ok += 1
                print(f"  ok {aid} ({len(data)} bytes)")
                break
            except Exception as e:
                note = f"attempt {attempt}: {type(e).__name__}: {str(e)[:100]}"
                if attempt == 2:
                    print(f"  FAIL {aid}: {note}")
                    fail += 1
                else:
                    print(f"  retry {aid}: {note}")
                    time.sleep(5)
        time.sleep(3)
    return ok, fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifests", default="primary,validation")
    args = ap.parse_args()
    total_ok = total_fail = 0
    for name in args.manifests.split(","):
        if name not in MANIFESTS:
            print(f"unknown manifest '{name}'"); return 1
        m = MANIFESTS[name]
        ok, fail = fetch(*m)
        total_ok += ok; total_fail += fail
    print(f"done: {total_ok} fetched+verified, {total_fail} failed")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())
