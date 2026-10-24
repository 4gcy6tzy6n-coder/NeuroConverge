#!/usr/bin/env python3
"""Pin the 42 adjudicated validation-corpus claims: exact-version arXiv PDF + derived text layer,
each SHA-256 hashed, manifest appended per file (kill-safe). Layout follows pinned_fulltext_20261020.
Failures are recorded as failures; nothing is silently skipped."""
import csv, hashlib, subprocess, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus_validation_v2_adjudicated.csv"
OUT = ROOT / "pinned_validation_20261025"
MAN = OUT / "FULLTEXT_DOWNLOAD_MANIFEST_20261025.csv"
UA = {"User-Agent": "NeuroConverge-Route-A-field-audit (validation corpus pinning)"}

claims = list(csv.DictReader(open(CORPUS)))
done = {}
if MAN.exists():
    for r in csv.DictReader(open(MAN)):
        done[r["arxiv_id_version"]] = r["download_status"]
if not MAN.exists():
    with MAN.open("w", newline="") as f:
        csv.writer(f).writerow(["arxiv_id_version","record_role","source_url","download_status",
                                "content_type","bytes","pdf_sha256","text_sha256","note"])
mf = MAN.open("a", newline="")
mw = csv.writer(mf)
n_ok = n_fail = n_skip = 0
for c in claims:
    aid = c["arxiv_id_version"]
    if aid in done and done[aid] == "open_access_downloaded":
        n_skip += 1
        continue
    url = f"https://arxiv.org/pdf/{aid}"
    pdf_path = OUT / "pdfs" / f"{aid}.pdf"
    txt_path = OUT / "texts" / f"{aid}.txt"
    status, ctype, nbytes, ph, th, note = "download_failed", "", 0, "", "", "both attempts failed"
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            if b"%PDF" not in data[:1024]:
                raise ValueError("not a PDF payload")
            pdf_path.write_bytes(data)
            subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf_path), str(txt_path)],
                           check=True, capture_output=True)
            ph = hashlib.sha256(data).hexdigest()
            th = hashlib.sha256(txt_path.read_bytes()).hexdigest()
            status, nbytes, note = "open_access_downloaded", len(data), "exact-version PDF; pdftotext UTF-8"
            break
        except Exception as e:
            note = f"attempt {attempt}: {type(e).__name__}: {str(e)[:120]}"
            time.sleep(4 * attempt)
    mw.writerow([aid, c["record_role"], url, status, ctype, nbytes, ph, th, note])
    mf.flush()
    n_ok += status == "open_access_downloaded"
    n_fail += status != "open_access_downloaded"
    time.sleep(1.2)
mf.close()
print(f"pinning done: ok={n_ok} fail={n_fail} skip(already)={n_skip} of {len(claims)}")
sys.exit(1 if n_fail else 0)
