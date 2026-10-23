# T1 external-source specificity verification (2026-10-23): the AI-first pass, superseded by humans on arrival

**Procedure, frozen before grading.** For each of the 14 externally-anchored claims (merged external layer
E3), the paper's T1 sentence is quoted from the pinned PDF (the coders' extractions, both sheets), the cited
sources are those the two coders verified by independent routes, and the **specificity match** is graded on a
frozen three-point scale: `S-specific` (the source establishes the very computation claimed, at the
specificity used), `S-general` (the source establishes a related general phenomenon, not the specific
computation at that specificity), `S-absent` (the source does not address the claimed link). This is the
AI-executed first pass of the hardening plan section 2; the P0-2 human pass supersedes it wholesale, and
every grade below carries its one-line reason for exactly that re-grading.

## The 14, graded

| claim | the paper's T1 claim (pinned-PDF quote, abbreviated) | cited sources (both coders' routes) | grade | reason |
| --- | --- | --- | --- | --- |
| 1903.12517v1 | dopamine gives basal-ganglia targets phasic reward-prediction-error signals | Schultz, Dayan & Montague 1997, Science 275:1593 | **S-specific** | the canonical source of the exact claim, verbatim-level match |
| 2509.00047v1 | reactivation of neural patterns (replay) protects against catastrophic forgetting | Wilson & McNaughton 1994, Science 265; Ji & Wilson 2007 | **S-specific** | replay discovery plus replication and causal probing; the strongest T1 in the corpus |
| 2511.17687v2 | grid/head-direction path-integration mechanism guides navigation | Hafting et al. 2005, Nature 436; McNaughton et al. 2006 | **S-specific** | the entorhinal PI line is exactly the claimed structure-computation link |
| 1811.09699v1 | attention control per biased competition + parietal spatial prioritization | Desimone & Duncan 1995; Bisley & Goldberg 2010 | **S-specific** | both components specifically established by the cited reviews |
| 2007.04578v1 | the brain combines model-free/model-based RL and arbitrates by context, lateral PFC | Daw et al. 2011; Lee, Shimojo & O'Doherty 2014 | **S-specific** | the arbitration computation is precisely the cited papers' subject |
| 1711.10563v2 | dual-memory model: hippocampal recent / prefrontal remote storage | McClelland, McNaughton & O'Reilly 1995; Kitamura et al. 2017 | **S-general** | complementary-learning-systems and mPFC consolidation are established; FearNet's specific BLA-switching tri-partition is the paper's extension, not the sources' |
| 1511.04484v2 | unreliable vesicle release is a major brain stochasticity source | Katz 1966; Branco & Staras 2009, Nat Rev Neurosci | **S-specific** | release-probability modulation is the review's exact subject |
| 2203.14679v1 | LIF neurons integrate over time, communicating between time steps | Dayan & Abbott 2001 (integrate-and-fire chapters) | **S-specific** | LIF temporal integration is textbook-established; the artifact-side gap lives at T2, not here |
| 2309.05263v1 | cortical motifs perform multisensory fusion, SNR enhancement, balance, amplification, rhythm | Douglas & Martin 2004; Isaacson & Scanziani 2011; Luo 2021 | **S-specific** | standard motif-function assignments from the canonical sources |
| 2311.15474v1 | Hebbian learning exploits neural-dynamics heterogeneity for robust learning | Perez-Nieves et al. 2021, Nat Commun; Gray & McCormick 1996 | **S-specific** (noted) | the match is specific, but the strongest external support is itself computational modeling, not biological experiment - a distinct layer to report |
| 2401.15661v2 | brain architectures prioritize locality, modularity, sparsity | Bullmore & Sporns 2009; Sporns & Betzel 2016 | **S-general** | sparse/modular brain networks are established; the paper's own text calls the inspiration "loose" and no specific computation is claimed for the property |
| 2406.11778v1 | reward-related neurotransmitters control myelination/demyelination | Stevens, Tanner & Fields 1998, J Neurosci | **S-general** | activity-pattern control of myelination is established; the reward-neurotransmitter-specific control claimed is the stronger, unestablished part |
| 2411.09953v2 | spike sequences encode temporal and spatial information | Gerstner & Kistler 2002; Rieke et al. 1997 | **S-specific** | spike coding is the cited texts' exact subject |
| 2508.18961v1 | heterogeneous dendrites causally shape firing; columnar partitioned architecture | Mountcastle 1997; London & Hausser 2005; Mainen & Sejnowski 1996 | **S-specific** | the causal dendrite-firing claim is specifically the cited work |

**Tally: 11 S-specific, 3 S-general, 0 S-absent.** The three S-general cases are named above with the exact
unestablished remainder in each.

## What this does to the finding - the story moves, and the hardening process is why

The coder notes' specificity worry, graded systematically, is **weaker than the notes suggested**: the
delegated biology is usually delegated to sources that genuinely support the specific claim (11/14). The
three-layer T1 picture is now: 18/18 in-paper E0 (delegated) -> 14/18 externally established -> 11/14 of
those at specific match. **T1 is not the corpus's weak link once the external layer is read honestly.**

Where, then, does the chain actually break? The distribution answers: **T2 - correspondence**, the claim
that the artifact instantiates the cited computation, is 12/18 at E1 (stated, never controlled) and only 4/18
E2 - while T3, the baseline comparison the field's referees already check, is 11/18 E2. The distinctive
scientific content of "bio-inspired" - the mapping itself - is the least controlled link in the chain, and
that is where the evidence inversion actually lives. The paper's constructive claim follows directly: the
correspondence claim (T2) deserves the same controlled-evidence standard the field already applies to
utility (T3), and the reporting checklist's T2 lines are where that standard is written down.

**Wordings locked accordingly**: "delegated but usually well-anchored biology; the uncontrolled middle" -
never "unsupported biology". The headline statistics and their definition-dependence stand as reported in
the hardening plan; the pilot carries no field percentages.
