# Reference identifiers, with the query that produced each

**Every PMID and DOI in the manuscript's reference list was read from the Europe PMC REST API, not recalled.**
**This file records the queries so the identifiers are reproducible.**

**Why it exists:** the first version of the manuscript's reference list was written from memory, and six of its
nine identifiers appeared nowhere in the committed survey documents. **Re-querying confirmed the PMIDs and DOIs
were correct and found two missing DOIs and two missing author lists.** **A memory that happens to be right is
not a method.**

---

## The endpoint

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search
    ?query=<url-encoded title query>
    &resultType=core
    &format=json
    &pageSize=1
```

## The queries and their results

| tag | query | pmid | doi | journal | year | authors |
| --- | --- | --- | --- | --- | --- | --- |
| **NatRevNeurosci2025** | `TITLE:"Structurally informed models of directed brain connectivity"` | **39663407** | **10.1038/s41583-024-00881-3** | Nature reviews. Neuroscience | 2025 | **Greaves MD, Novelli L, Mansour L S, Zalesky A, Razi A** |
| **CurrierCell2025** | `TITLE:"Infrequent strong connections constrain connectomic predictions"` | *(none returned)* | *(none returned)* | Cell | 2025 | **Currier TA, Clandinin TR** |
| **LaaschSciRep2025** | `TITLE:"Comparison of derivative-based and correlation-based methods to estimate effective connectivity"` | **39948086** | **10.1038/s41598-025-88596-y** | Scientific reports | 2025 | **Laasch N, Braun W, Knoff L, Bielecki J, Hilgetag CC** |
| **LynnNatPhys2026** | `TITLE:"Simple input-output dependencies explain neuronal activity"` | **42370308** | **10.1038/s41567-026-03306-3** | Nature physics | 2026 | **Lynn CW** |
| **NatMethods2025** | `TITLE:"Mapping effective connectivity by virtually perturbing a surrogate brain"` | **40263586** | **10.1038/s41592-025-02654-x** | Nature methods | 2025 | **Luo Z, Peng K, Liang Z, Cai S, Xu C, Li D, Hu Y, Zhou C, Liu Q** |

**The Currier and Clandinin entry returns no PMID or DOI from this endpoint, which suggests the record is not
in Europe PMC's indexed set for that journal; it is cited by title, journal and year only, and the manuscript
states that it was read at abstract level.**

## What this file does NOT establish

* **The identifiers are correct as returned by the API on the date of the query; they are not independently
  cross-checked against Crossref or the publisher.**
* **The author lists are as the API returned them, including its punctuation.**
* **Nothing here verifies that the quoted sentences appear in the cited works beyond what the abstract-level
  reading recorded in `LITERATURE_SURVEY_SPECIFICATION_AND_RELIABILITY.md` already states.**

---

## Round 58: the same identifiers re-derived from Crossref, which resolves a DOI to a RECORD

**Europe PMC answers "does this identifier exist".** **Crossref's `works/<DOI>` endpoint answers "does this
identifier point at THIS paper", because it returns the metadata of the record the DOI resolves to.** **The
second question is the one that catches a DOI belonging to a different article, so the re-query was run
against Crossref.**

### The full metadata Crossref returned

| # | DOI | vol | issue | pages / article | journal | year | online |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `10.1038/s41586-023-06683-4` | 623 | 7986 | 406-414 | Nature | 2023 | 2023-11-01 |
| 2 | `10.1038/s41583-024-00881-3` | 26 | 1 | 23-41 | Nature Reviews Neuroscience | **2025** | **2024-12-11** |
| 3 | `10.1016/j.cell.2025.05.007` | 188 | | 4366-4381.e14 | Cell | 2025 | |
| 4 | `10.1038/s41598-025-88596-y` | 15 | 1 | **article 5357** | Scientific Reports | 2025 | 2025-02-13 |
| 5 | `10.1038/s41567-026-03306-3` | 22 | 7 | 1152-1159 | Nature Physics | 2026 | 2026-05-18 |
| 7 | `10.1038/s41592-025-02654-x` | 22 | 6 | 1376-1385 | Nature Methods | 2025 | 2025-04-22 |

**All five DOIs resolved with HTTP 200, and every title and first author matched the attribution.** **No DOI
pointed at a different paper.**

### The one field where the sources disagree, and it is not an error

**Reference 2: Europe PMC returns `pubYear` 2025; Crossref returns `issued` 2024-12-11.** **Crossref also
returns `published-online` 2024-12-11 and `published-print` 2025-01.** **Both are right: the article appeared
online in December 2024 and in the January 2025 issue.** **The manuscript cites the issue year, 2025, and
states the discrepancy rather than smoothing it.** **This is the `卷年 != DOI 年` case, and Crossref's
`published-print` is the field that resolves it rather than `issued`.**

### An error this file made in the previous round, corrected here

**The round-57 version said that the Cell entry "returns no PMID or DOI from this endpoint".** **That was
wrong, and the cause was a truncated query: it searched the title `"Infrequent strong connections constrain
connectomic predictions"` and stopped before the words "of neuronal function", which was enough for Crossref's
bibliographic search to miss it and not enough to match it.**

**With the full title both sources return it: `10.1016/j.cell.2025.05.007`, PMID 40460825, *Cell* 188,
4366-4381.e14 (2025); a preprint also exists at `10.1101/2025.03.06.641774`.**

**The lesson is the one this corpus keeps recording: an absence of evidence produced by a query that was too
narrow is not evidence of absence, and the first version of this file treated it as one.**

## What is still not verified

* **Reference 6, the *Communications Biology* paper on decomposed linear dynamical systems, is cited from an
  abstract-level reading, PMC12350842, and its DOI was not retrieved.** **The manuscript states this rather
  than implying verification.**
* **References 8 and 9 are data records, not articles, and were not run through Crossref.**
* **No entry was cross-checked against the publisher's own page, only against Crossref and Europe PMC.**
