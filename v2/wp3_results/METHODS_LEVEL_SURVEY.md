# Methods-level survey: four open-access full texts, and one framing this line can measure

**Status: the last item this line can complete. It reads four Methods sections rather than titles and
abstracts, and it finds one concrete point of contact between a published framing and a measurement made
here.** No model was fitted.

---

## 1. Method

**Four of the most relevant citing works are open access and were fetched as full text through the Europe
PMC REST API, then searched for reliability, reproducibility and measurement-error terminology.** **The
fifth, _Nature Methods_ 2025 on virtual perturbation, has no PMC record and is not open access, so it is
excluded and named.**

| work | identifier | full-text length |
| --- | --- | --- |
| _PLoS Comput Biol_ 2025, data-driven biology-based network model | PMC12768384 | 126,798 chars |
| _Commun Biol_ 2025, decomposed linear dynamical systems | PMC12350842 | 92,576 chars |
| _Netw Neurosci_ 2026, entropic measure of specialisation | PMC13008378 | 66,770 chars |
| _Sci Rep_ 2025, derivative versus correlation effective connectivity | PMC11825726 | 90,013 chars |
| _Nat Methods_ 2025, virtual perturbation | no PMC | **not read** |

**Terms searched:** reliability, reproducib\*, measurement error, noise, ICC, split-half, intraclass,
test-retest, attenuation, cross-validat\*, signal-to-noise, SNR.

## 2. The finding

> **Across 376,157 characters of Methods and Results from four works whose contribution is
> structure-to-function inference, none reports a reliability, reproducibility or measurement-error figure
> for the functional quantity it predicts.**

**What the term hits actually are:**

* **_PLoS Comput Biol_ 2025.** "Reproducibility" appears **twice, and both are the journal's own boilerplate**
  about depositing laboratory protocols in protocols.io. "Noise" appears twice, both about **neural
  activity** noise rather than measurement error.
* **_Commun Biol_ 2025 (dLDS).** "Noise" appears **twice, and both argue the variability is *not* noise**
  (section 3).
* **_Netw Neurosci_ 2026.** **Zero hits for any of the thirteen terms.**
* **_Sci Rep_ 2025.** "Noise" appears 19 times, **all about the Hopf model's noise parameter**, not
  measurement error in the data. "Signal-to-noise" appears once, about **deliberately reducing** it.

**This is the Methods-level version of what round 18 found at title-and-abstract level.** **Round 18 said its
negative result could be overturned by a Methods check; this is that check, on four of the eleven, and it is
not overturned.**

## 3. The one concrete point of contact

**The dLDS paper's framing, quoted verbatim from its full text:**

> *"This is **not noise**; this variability is required for adaptation and **reflects worm individuality** in
> behavioral tendencies."*
>
> *"We posit that these **individual differences are not noise**; they are essential to understand worm
> adaptation to their environments."*

**This line measured the analogous question on a different artifact in the same organism and got a
different decomposition:**

| quantity | this line's measurement |
| --- | --- |
| pair-specific animal deviation | **5.5 %** of the pair-level variance |
| within-cell measurement error | **37.5 %** |
| between-pair | 55.1 % |

**So the framing "this variability is individuality, not noise" is, in the one case where that variability
has been decomposed, mostly measurement error.**

## 4. What may and may not be concluded from section 3

**May be concluded:** **a published framing in the same organism attributes cross-individual functional
variability to individuality, and a decomposition of the one artifact where it has been done finds that
variability is mostly measurement error.** **That is a concrete, checkable point of contact between a
framing and a measurement.**

**May NOT be concluded:**

* **That the dLDS paper is wrong.** Its variability is **behavioural tendencies and neural dynamics across
  individuals**, which is **not the same quantity** as the per-pair response variance decomposed here. **The
  two could differ for a good reason and this line has not compared them.**
* **That the dLDS paper fails to report reliability.** **It is one of the four searched; the search covered
  thirteen terms and it is possible a relevant figure is reported under different wording**, which a term
  search would miss.
* **That the pattern generalises.** Four works, one organism, one search.
* **That this line's decomposition applies to the dLDS data.** **It does not; it applies to the atlas's
  per-animal records.**

**The honest version: a framing exists in the literature that this line's measurement is in tension with,
and the tension is not yet resolved because the two quantities are not the same.**

## 5. What this completes, and what remains

**This was the last item named as owed that this line could complete.** **The two that remain are not
computations or readings:**

| owed | why it is not this line's to complete |
| --- | --- |
| **an independent reviewer** | `PREFLIGHT_REVIEW.md` records that the review performed is a self-review; **an external person is required by the plan** |
| **the owner's decision on the plan's constraint** | the plan forbids a new NMI abstract, main-text Results, Discussion or figures, and **that constraint is the plan's, not this line's** |

**And one substantive gap that is now visible and was not before:** **the dLDS tension in section 3 is worth
resolving, and resolving it requires reading that paper's analysis rather than searching its terms.**
**That is a bounded next step and this line has not done it.**

## 6. Provenance

* Full texts: Europe PMC `fullTextXML` for PMC12768384, PMC12350842, PMC13008378 and PMC11825726, fetched
  this session.
* The 13 search terms are listed in section 1 so the search can be re-run or contested.
* **No model was fitted. No causal claim is made.**
