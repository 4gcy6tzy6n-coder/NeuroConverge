# The specification problem is field-recognised, which raises V2-C4's ceiling

**Status: a literature step that changes what the line's sensitivity finding is evidence FOR.** No model was
fitted.

---

## 1. Why this was needed

**V2-C4 states that the published per-pair values are produced by analysis choices that live in the
pipeline's code and not in its data file, and that re-analysing the same records under defensible choices
moves the animal-level estimate from `d = 0.085` to `0.729`.** Its recorded ceiling was:

> *"the five rows are this line's own constructions, not a systematic sample of published practice."*

**That ceiling is what this section addresses.** The method used was the Europe PMC citation record for the
source, which returns **129 citing works**.

## 2. Three of them establish the field's position

**Currier TA, Clandinin TR (2025), _Cell_. "Infrequent strong connections constrain connectomic predictions
of neuronal function."** Abstract read:

> *"many of these hypotheses have **not been compared with physiological measurements**, obscuring the
> limits of connectome-based functional predictions. ... these predictions are **accurate for some response
> properties**, such as orientation tuning, but are **surprisingly poor for other properties**, such as
> receptive field size. Importantly, **strong synaptic inputs are more functionally homogeneous than
> expected by chance** and exert a disproportionately large influence on postsynaptic responses. Finally,
> we **quantitatively define the subset of connections that best describe** the functional differences
> between cell types."*

**Two things follow.** **First, a 2025 _Cell_ paper's contribution is precisely to compare connectomic
predictions against physiology and to find the comparison property-dependent** -- **this line's question is
recognised and active, not idiosyncratic.** **Second, "strong synaptic inputs are more functionally
homogeneous than expected by chance" is the closest published analogue to the round-6 result that the
connectivity association here is confined to cross-class pairs and absent within same-class pairs.**

**Lynn CW (2026), _Nature Physics_. "Simple input-output dependencies explain neuronal activity."**
Abstract read:

> *"**direct dependencies -- without interactions between inputs -- explain most of the variability in
> neuronal activity.** ... These minimal models, which are **equivalent to logistic artificial neurons**,
> predict complex higher-order dependencies and **recover known features of synaptic connectivity**. The
> inferred neural network is **sparse**, indicating a **highly redundant neural code** that is robust to
> perturbations. ... most neurons can be described by **simple artificial models**."*

**A high-profile 2026 result that simple models explain most activity variability is a strong prior against
any claim that structure carries additional predictive content.** **It is the same prior this line already
recorded from the 2026 Scientific Reports locomotion work and from Beiran & Litwin-Kumar 2025, now in a
third and more prominent form.** **It does not contradict anything measured here, and it bounds how much a
structural-prior claim could be worth.**

**Laasch N, et al. (2025), _Scientific Reports_. "Comparison of derivative-based and correlation-based
methods to estimate effective connectivity in neural networks."** Abstract read:

> *"**no universally accepted method exists** for the inference of effective connectivity, which describes
> how the activity of a neural node mechanistically affects the activity of other nodes. ... we provide a
> **systematic comparison** of different approaches"*

**This is the decisive one for V2-C4.** **The field states that no accepted method exists, and a 2025 paper
whose contribution is to compare methods systematically.**

## 3. What this does to V2-C4's ceiling

**The ceiling said the sensitivity range is this line's own five constructions rather than a sample of
practice. The literature shows the range is an instance of a recognised field-wide condition:**

| V2-C4 element | before | with the literature |
| --- | --- | --- |
| *no accepted method for this inference* | this line's assertion | **stated by the field itself in 2025** |
| *different choices give different answers* | measured here on one dataset | **property-dependent accuracy reported in _Cell_ 2025 on a different species** |
| *the choices are not in the artifact* | measured here | unchanged, and now the more pointed for it |
| *the estimates span 0.085 to 0.729* | **this line's own five rows** | **an illustration of a condition the field acknowledges, not a claim about a distribution** |

> **Upgraded statement for V2-C4: the specification sensitivity measured in this line is not an artefact of
> five arbitrarily chosen constructions. It is a quantified instance of a condition the field itself
> reports -- no accepted method for inferring effective connectivity, and outcome-dependent comparisons --
> and the contribution is to attach numbers to that condition on a specific published artifact.**

**The ceiling does NOT disappear.** **This line still has not sampled published practice systematically, and
the upgraded statement is about the condition being recognised, not about the distribution of published
choices.** **What changes is that the finding is no longer merely local.**

## 4. Two further citing works worth recording

**"Bilateral Neuron Pairs Share Redundant Network Roles Despite Incomplete Connection Symmetry in
_C. elegans_" (2026, _European Journal of Neuroscience_).** **Directly adjacent to the round-6 class
result**, where the connectivity association was null within same-class pairs -- and bilateral pairs are
the principal same-class case. **Not read beyond its title, and recorded as such.**

**"What an atlas-fitted connectome can and cannot do: evolutionary search over interneuron stimulation"
(2026).** **A title that poses this line's question.** **Not read beyond its title, and recorded as such.**

**Both are candidates for the nearest-neighbour matrix, which was assembled before this citation list was
available and does not contain them.**

## 5. What the line should do with this, and what it should not

**Should:** treat the citation list as the entry point to a proper specification survey, and either sample
the analyses reported in the ~20 most relevant citing works or state in the manuscript that the range is
illustrative of a recognised condition rather than a distribution over practice.

**Should not:** present the upgrade as making V2-C4 stronger than it is. **The three abstracts read here are
the field's own statements; none of them is a measurement of what analysts typically do, and this line has
not made one.**

## 6. Provenance

* Citation list: Europe PMC, `/MED/37914938/citations`, 129 works, retrieved this session.
* Abstracts read verbatim through the Europe PMC REST API for the three works in section 2; the two in
  section 4 are recorded by title only and labelled as such.
* **No model was fitted. No causal claim is made.**
