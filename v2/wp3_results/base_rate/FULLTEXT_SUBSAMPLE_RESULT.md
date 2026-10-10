# Full-text subsample: two of seven codable full texts report a reliability figure, and the census saw neither

**The parent protocol fixed a subsample rule mechanically -- every record whose ABSTRACT contains a
reliability-family term -- and fixed the falsification criterion before any full text was fetched.** **This is
the coding.**

## The subsample and what was codable

**17 records entered the rule.** **8 of them carry a PMCID and are therefore open access; 7 of those 8 full texts
were retrieved, one failing.** **TEN records in the subsample were NOT codable at full text, and the reason each is not is now
established rather than assumed.** **Nine carry no PMCID, and a query against the Europe PMC search endpoint
returns `isOpenAccess=N, inEPMC=N` for every one of them, so their full text is not available through any
endpoint this environment can reach.** **The tenth carries a PMCID but also returns `isOpenAccess=N`; its
full-text request returns HTTP 500 and the record itself states it is not open access.**

**Of those ten, ONE is covered by a version already coded: PPR62030 is the preprint of 41874539, whose
published version is one of the seven coded above.** **So the genuine unknown is NINE records, and they are
reported as NOT CODABLE rather than counted as N.**

## The coding, from the full texts

| record | PMC | code | the passage |
| --- | --- | --- | --- |
| **40644546** zebrafish | PMC12248300 | **R** | "Network similarity scores are significantly higher when comparing individuals to themselves [diagonal values from matrix in (H)] rather than different individuals [off-diagonal values from matrix in (H)] (P = 3 x 10^-5, t test)." |
| **41874539** mouse V1/HVA | PMC13012721 | **R** | "The NC of individual neuron pairs can be computed using different random subsets of trials, yet reliably converges on similar values ... the variance of NC computed using a subset of trials is explained by the variance in the held-out subset of trials (53 +/- 24 % variance explained; total 204 populations). Each subset contains half of all the trials." |
| 38489379 | PMC10942262 | **N** | reports "common dynamics across animals" and "individual differences" but no reliability figure |
| 38820533 | PMC11168681 | **N** | no reliability figure for a functional quantity |
| 39681671 | PMC11659166 | **N** | no reliability figure |
| 39948086 | PMC11825726 | **N** | compares METHODS for estimating connectivity against ground truth; no reliability figure for a functional quantity |
| 42168461 | PMC13354769 | **N** | no reliability figure |

**R = 2, N = 5, NOT CODABLE = 9, of the 17 in the subsample.**

## The result, and the criterion it triggers

**Subsample R rate = 2/7 = 28.6 per cent.** **Parent-census R rate = 0/125 = 0.0 per cent.**

**The protocol's falsification criterion was: if the subsample rate exceeds the census rate by more than a
factor of ten, the abstract-level census must be described as substantially unrepresentative rather than as a
lower bound.** **Dividing by a zero census rate is undefined, and the criterion is met on any reading: the
census saw NONE of the records that report such a figure, and the subsample found two of them.**

**SO THE MANUSCRIPT MUST STOP CALLING THE CENSUS MERELY A LOWER BOUND, and it now does: it says the census
substantially underrepresents, names the two records it missed, and gives the subsample's rate as the better
estimate for records that mention the concept.**

## What must NOT be claimed from 28.6 per cent

**The subsample was selected FOR mentioning a reliability-family term, so it is a high-rate subsample by
construction and 28.6 per cent is NOT the frame's rate.** **It is an upper-ish estimate for the frame, and the
census's 0.0 per cent is a lower bound, so the frame's true rate lies between them.** **Nothing here estimates
where.**
**The nine not-codable records are the largest remaining unknown: if they behave like the seven codable ones**
**the frame rate rises, and if they behave like the census it does not.** **An attempt was made to resolve
them to published open-access versions by title search; ONE resolved, and it was the duplicate.** **So the
nine are a hard limit of this environment and not a step not yet taken, and reaching them would require
access this line does not have.**

## A screen failed twice before this was coded by reading

**A keyword screen for a functional quantity plus a number found the mouse record and MISSED the zebrafish one,
whose reliability sentence carries no decimal and no per-cent sign.** **A second attempt returned nothing for any
of the seven because its context window was 520 characters and its length filter capped at 500, so it rejected
every candidate it found.** **Both are the same class the corpus documents: a procedure that looks right and
cannot produce what it claims.** **The coding above was produced by printing fixed windows and reading them.**

## Provenance

* **Parent protocol:** `../PROTOCOL_reliability_reporting_base_rate.md`.
* **Subsample rule and criteria:** `../PROTOCOL_fulltext_subsample.md`, committed before any full text was
  fetched.
* **Full texts:** Europe PMC, by PMCID; the seven fetched are in the working set and the queries are the
  `fullTextXML` endpoint.
* **Coder:** this line, ONE coder, stated as a limitation exactly as in the parent protocol.
* **No model was fitted. No causal claim is made.**
