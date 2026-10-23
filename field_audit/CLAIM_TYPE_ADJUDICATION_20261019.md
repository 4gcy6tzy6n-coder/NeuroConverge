# Claim-type adjudication log (2026-10-19): 18 frozen claims ruled, 7 replaced, 18 adjudicated

**Authority.** The frozen protocol section 3's draw-review step, executed by the lead under the 2026-10-19
authority record. Every ruling below was made against the abstract text in the pinned snapshot
(`corpus_draw_arxiv_v1.snapshot.jsonl`, sha256 `e73f72f5...`) - the same bytes anyone can re-read. The frozen
claim-type criterion: the paper must claim, in abstract or title, that a biological mechanism (structure,
circuit, plasticity rule, coding principle, connectome) improves an artificial system's capability; exclusion
(a) removes purely inspirational naming with no mechanistic content.

## Rulings on the frozen 18

| claim | ruling | reason |
| --- | --- | --- |
| 2305.10938v1 (ethical analysis method) | EXCLUDE | claim-type: an ethics-analysis method for brain-inspired AI; no mechanism-improves-capability claim |
| 2207.08533v2 (BrainCog) | EXCLUDE | claim-type: platform/infrastructure contribution; presents building blocks, claims no mechanism result |
| 2303.15935v1 (BIAI meets AGI) | EXCLUDE | claim-type: survey/position; reviews rather than claims |
| 2312.07213v4 (BIAI for HCI) | EXCLUDE | claim-type: survey |
| 2412.08875v1 (BIAI agent towards AGI) | EXCLUDE | claim-type: survey/position |
| 2503.19303v1 (BIMII-Net) | EXCLUDE | exclusion (a): "brain-inspired model" labels an architecture; no biological mechanism is ever named |
| 2305.11252v1 (BI learning review) | EXCLUDE | claim-type: survey |
| the other 11 | KEEP | each names a biological mechanism and claims an artificial-capability improvement at abstract level |

The 11 kept: 2508.18961v1 (TaiBai, event-driven sparsity), 2107.14654v1 (brain-inspired DIL), 2401.15661v2
(bare-minimum PINN architectures), 2309.05263v1 (evolutionary SNN architectures), 2203.14679v1 (spiking
MLP), 2411.09953v2 (spiking diffusion policy), 2601.15865v1 (plasticity/rhythmic-regulation clinical
framework), 2509.00047v1 (internal replay), 2511.17687v2 (CANN path integration), 1711.10563v2 (FearNet),
2311.15474v1 (optoelectronic heterogeneous neuron).

## Replacements (frozen rule: next eligible in the same stratum, fetch-rank order), each ruled on its own abstract

| replacement | replaces | kept because |
| --- | --- | --- |
| 1903.12517v1 | 2305.10938v1 | bio-inspired learning framed on neuroscientific RL links, aimed at improving artificial RL systems |
| 2504.05621v1 | 2303.15935v1 | names cross-regional temporal development (formation, reorganization, pruning) claiming continual multi-function learning at low cost |
| 2301.02809v2 | 2312.07213v4 | names brain learning-and-memory transformation claiming improved DNC reasoning/QA |
| 2406.11778v1 | 2207.08533v2 | brain-inspired recurrent spiking model claiming action-recognition capability |
| 2102.11450v1 | 2412.08875v1 | neuroscience-inspired learning algorithms claimed more power/data-efficient for predictive maintenance |
| 1811.09699v1 | 2503.19303v1 | names the primate attention network, claims improved attention in deep networks |
| 1511.04484v2 | 2305.11252v1 | names synaptic stochasticity, claims efficient learning machines |

## Replacement candidates refused along the way (all reasons on the record)

1810.01620v1 (biological overview post-hoc over standard DL components), 2402.18784v2 (philosophical
position), 2311.14641v2 (interoperability infrastructure), 2401.02429v2 (survey), 1506.03264v1 (perspective),
2312.09257v2 (survey), and three candidates not needed once an earlier rank filled the stratum
(2202.09467v1, 2106.02749v2, 2210.15790v1, 2309.04426v1).

## The adjudicated corpus of record

`corpus_arxiv_adjudicated_v1.csv`: 18 claims, exactly 3 per mechanism family, 8 primary categories, years
2015-2026 (the recency bias of the relevance order is reduced, not removed, by adjudication). Every row
carries `needs_adjudication: done-2026-10-19`. **This file supersedes `corpus_draw_arxiv_v1.csv` as the
corpus of record for the coding phase; the frozen draw stays in the tree unchanged as the draw of record.**

## What the coder phase receives

The 18 adjudicated claims, each with: arXiv id, title, abstract (from the pinned snapshot), family, category,
and - next step - the hash-pinned full text. Coding has not begun; nothing here pre-grades any transition.

## Addendum, same day: one full text unpinnable, one further replacement

`2301.02809v2` returns HTTP 404 on both PDF URL forms (unversioned and versioned) - the paper is not
retrievable, so under the frozen rule it is **uncodable** and the replacement rule fires. Three further
same-stratum candidates were ruled on their pinned abstracts and refused: 2308.12486v2 (a Non-Axiomatic Logic
system under a brain-inspired label - exclusion (a)), 2103.06123v1 (position paper on whole-brain-architecture
AGI methodology), and the already-refused names stand. **2007.04578v1** (rank 192) is taken: an evaluation of
brain-inspired reinforcement-learning algorithms' reliability and generalizability, naming decision-
neuroscience mechanisms and capability claims - an evaluation paper, which the corpus previously lacked. All
18 full texts are now pinned in `fulltexts/` with SHA-256 in `fulltexts/PINNING_MANIFEST.csv`. The corpus of
record remains `corpus_arxiv_adjudicated_v1.csv`, 18 claims, 3 per family.
