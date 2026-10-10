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
