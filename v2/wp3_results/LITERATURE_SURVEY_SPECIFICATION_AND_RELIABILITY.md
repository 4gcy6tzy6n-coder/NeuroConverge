# Specification and reliability in the citing literature: what eleven works do and do not report

**Status: a title-and-abstract level survey of ten citing works, which places this line's contribution and
bounds what may be claimed for it.** No model was fitted.

---

## 1. Method, and its limits stated first

**Eleven works were read at title-and-abstract level, drawn from the 129 citing records of the source by title
relevance to structure-function prediction and to effective-connectivity inference. Abstracts were fetched
through the Europe PMC REST API.**

**What this survey is NOT.** It is **not** a systematic sample, **not** a methods extraction, and **not** a
reading of any paper's Methods section. **It reads titles and abstracts only.** **Anything below that would
require a Methods section is marked as not established.** **This is stated first because the temptation with
a survey of this shape is to over-read it.**

## 2. What the field says about the question itself

**Two works state that the question is open, and they are the strongest motivation this line has found.**

**"Structurally informed models of directed brain connectivity." _Nature Reviews Neuroscience_ (2025).**
Abstract read:

> *"Understanding how one brain region exerts influence over another in vivo is profoundly constrained by
> models used to infer or predict directed connectivity. Although such neural interactions rely on the
> anatomy of the brain, **it remains unclear whether, at the macroscale, structural (or anatomical)
> connectivity provides useful constraints on models of directed connectivity.** Here, we review the current
> state of research"*

**A 2025 review in _Nature Reviews Neuroscience_ states that whether structure usefully constrains directed
connectivity remains unclear.** **That is the field's own framing of this line's question, in the field's
own venue.**

**"What an atlas-fitted connectome can and cannot do: evolutionary search over interneuron stimulation"
(2026).** Abstract read:

> *"The C. elegans connectome is complete, but **which behaviors its wiring can produce, and which it
> cannot, is unknown.** We asked this question in a whole-body simulation whose only adaptive element is a
> learning agent outside the nervous system."*

**The same question, framed as unknown, in 2026, on the same organism.**

## 3. What the field reports about the answer

| work | venue, year | what it reports |
| --- | --- | --- |
| Currier & Clandinin | **_Cell_ 2025** | connectomic predictions are **accurate for some response properties and surprisingly poor for others**; many hypotheses had **not been compared with physiological measurements**; **strong synaptic inputs are more functionally homogeneous than expected by chance** |
| Lynn | **_Nature Physics_ 2026** | **simple input-output dependencies explain most of the variability in neuronal activity**; minimal models equivalent to logistic artificial neurons; inferred network sparse, code highly redundant |
| Laasch et al. | **_Sci Rep_ 2025** | **no universally accepted method exists** for inferring effective connectivity |
| "A data-driven biology-based network model reproduces _C. elegans_ premotor neural dynamics" | **_PLoS Comput Biol_ 2025** | a data-driven model reproduces premotor dynamics; **not read beyond the abstract** |
| "Decomposed Linear Dynamical Systems (dLDS)" | **_Commun Biol_ 2025** | models **instantaneous, context-dependent** dynamics; motivated by tuning being **variable within an individual across time and across individuals** |
| "An entropic measure of diverse specialisation" | **_Netw Neurosci_ 2026** | a network metric combining topological analysis with cell-type and lineage classification; **not read beyond the abstract** |
| "Mapping effective connectivity by virtually perturbing a surrogate brain" | **_Nat Methods_ 2025** | **Neural Perturbational Inference**; traditional EC methods are **invasive or limited in spatial coverage** |
| "Connectome architecture favours within-module diffusion and between-module routing" | 2025 | current communication models **assume every pair communicates by the same principle**, which the paper challenges |
| "Bilateral Neuron Pairs Share Redundant Network Roles Despite Incomplete Connection Symmetry" | **_Eur J Neurosci_ 2026** | bilateral pairs **differ substantially in left-right connections yet occupy similar network roles**, analysed with three graph-theoretic measures |

**The dLDS entry is worth isolating.** Its motivation is that neural tuning is *"highly variable within an
individual across time and **across individuals**"*. **That is the same phenomenon this line measured at 5.5
% pair-specific animal deviation and 37.5 % measurement error, and the dLDS abstract does not separate the
two.** **Recorded as an observation about a title-and-abstract, not as a criticism.**

## 4. The negative result, which is the point

**None of the eleven works reports a reliability, reproducibility or measurement-error figure for the
functional quantity it predicts or infers.**

**That is a title-and-abstract-level observation and it is offered as such.** **A Methods-level check could
overturn it, and this line has not done one.** **But the abstracts of works whose entire contribution is
structure-to-function prediction do not mention how reliable the function side is, and this line has
measured that quantity for one of these artifacts:**

| level | this line's measurement |
| --- | --- |
| **a pair's response** | 55.1 % between pairs, **37.5 % measurement error**, 5.5 % pair-specific animal, 1.9 % animal offset |
| **the connectivity effect** | 42.2 % noise, 57.8 % signal |
| **the atlas's cross-animal agreement** | `r_full = 0.04` on the bulk of pairs |

## 5. What this does to the contribution's placement

**Before this survey, this line could say it had measured things about one artifact.** **After it, the
placement is specific:**

1. **The question is open by the field's own account** -- a 2025 _Nature Reviews Neuroscience_ review and a
   2026 work both say so, in those words.
2. **The answer is contested and property-dependent** -- accurate for some properties, poor for others
   (_Cell_ 2025), while simple models explain most activity variability (_Nature Physics_ 2026).
3. **The inference method is unsettled** -- no accepted method (_Sci Rep_ 2025), and competing traditions
   (_Nat Methods_ 2025).
4. **And the reliability of the thing being predicted is not reported in any of the eleven.**

**This line's contribution sits at (4), and it is the one of the four that nobody in the surveyed set
reports.** **That is a narrower and better-founded claim than "the atlas cannot support a circuit-property
claim", which round 10 made and round 12 withdrew.**

## 6. What must not be claimed from this survey

* **That the field ignores reliability.** Eleven abstracts are not the field. **Papers may report it in
  Methods.**
* **That these eleven are representative.** They were selected by title relevance.
* **That any of these works is wrong.** None was read beyond its abstract.
* **That the question's being open makes this line's answer important.** An open question and a useful
  answer are different things, and **this line's answer is a reliability measurement, not a
  structure-function result.**

## 7. Provenance

* Source citation list: Europe PMC `/MED/37914938/citations`, 129 records.
* Abstracts fetched individually through the Europe PMC REST API this session.
* **The counts, stated exactly.** Section 2 reads two works, section 3 reads seven in its table, and
  three further works (Currier and Clandinin, Lynn, Laasch et al.) were read in round 17 -- a union of
  **twelve distinct works**, of which **eleven** yielded a usable abstract. One intended query failed
  on shell quoting (the apostrophe in *"Analyzing the brain's dynamic response to targeted
  stimulation"*), so that work is **not** included. Section 1's "ten" and the document title's "ten"
  are corrected here to eleven read, twelve intended.
* **No paper's Methods section was read. No model was fitted.**
