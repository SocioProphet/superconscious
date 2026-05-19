# Lawful Learning Source Ledger

**Status:** H6 replayed capture; source-provenance doctrine, not runtime evidence.  
**Origin branch:** `lawful-learning-capture-v1`.  
**Audit disposition:** replay-after-demotion from branch reconciliation audit.  
**Purpose:** Records provenance anchors for non-original claims in the lawful-learning framework. Used by claim-ledger, publication-checklist, and later evidence-pack work as a source map. This file does not verify, fetch, or certify the sources.

## H6 / H4 boundary

This ledger is retained because it contains useful source-provenance structure that was left outside main. It is not a citation-completeness proof and does not promote any claim.

This file does **not** claim:

```text
source quality attested
source existence runtime-checked
citation completeness proved
claim truth verified
mathematical theorem proved
empirical measurement reproduced
runtime evidence integration completed
```

Any [M], [T], [S], [E], or [G] claim that cites this ledger must still satisfy the claim-status rules in:

```text
docs/audits/2026-05-19-claim-status-ledger.md
docs/audits/2026-05-19-theorem-language-gate.md
```

## Source taxonomy

Sources are organized by claim domain and dependency relationship.

### Hopfield network proof line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.hopfield.classical-1982` | Hopfield 1982 | Classical Hopfield network, binary states, energy descent to fixed points | Foundational; cited for energy-function form |
| `src.hopfield.modern-continuous-2020` | Ramsauer et al. 2020 | Modern continuous Hopfield, log-sum-exp energy, exponential storage capacity, attention equivalence | Required for any [M] Hopfield proof claim in this framework |
| `src.hopfield.universal-2021` | Krotov & Hopfield 2021 | Universal Hopfield model | Cited for energy-function generalizations |

### Hypercomplex algebra line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.hypercomplex.cayley-dickson` | classical | Cayley-Dickson construction: complex → quaternion → octonion → sedenion → ... | Required for any sedenion claim; names the construction depth |
| `src.hypercomplex.octonion-properties` | classical | Octonions: non-commutative, non-associative, alternative, no zero divisors | Required to distinguish octonion claims from sedenion claims |
| `src.hypercomplex.sedenion-zero-divisors` | classical | Sedenions: non-commutative, non-associative, non-alternative, have zero-divisor pairs | Required for any sedenion-substrate [M] claim; names the specific algebraic property |
| `src.hypercomplex.hurwitz-theorem` | Hurwitz 1898 | The only normed division algebras over the reals are R, C, H, O | Required for `hurwitz_residual` claims |

### Stability and dynamical-systems line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.stability.may-wigner-1972` | May 1972; Wigner | Random matrix stability threshold; community matrices of size N with connectivity C and standard deviation sigma stable iff sigma*sqrt(NC) < 1 | Required for any [M] May-Wigner application; assumes random Gaussian connectivity and weak coupling |
| `src.stability.lyapunov-classical` | classical | Lyapunov stability for nonlinear systems | Used for non-random-matrix stability claims |

### Mechanistic interpretability line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.mech-interp.elhage-2022` | Elhage et al. 2022 | Mathematical framework for transformer circuits | Cited for circuit construction patterns |
| `src.mech-interp.bricken-2023` | Bricken et al. 2023 | Towards monosemanticity: SAEs on transformer features | Foundational SAE application reference |
| `src.mech-interp.elhage-toy-superposition-2022` | Elhage et al. 2022 | Toy models of superposition | Required for any superposition [M] or [T] claim |
| `src.mech-interp.lindsey-circuit-tracer` | Lindsey et al. 2024 | Anthropic circuit tracing methodology | Required for circuit-tracing [T] parallel claims |
| `src.mech-interp.olsson-induction-2022` | Olsson et al. 2022 | Induction heads and in-context learning circuits | Required for induction-head circuit references |
| `src.mech-interp.wang-ioi-2022` | Wang et al. 2022 | Indirect-object-identification circuit in GPT-2 small | Required for IOI circuit references |

### Compositional structure line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.compositional.fong-spivak-2019` | Fong & Spivak 2019 | Seven Sketches: cospans, pushouts, open networks, black-boxing | Required for any categorical foundation [M] claim |
| `src.compositional.baez-pollard-2017` | Baez & Pollard 2017 | Black-boxing as a functor | Required for `black_boxing_composes` invariant |

### Information-geometric / loss-landscape line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.loss-landscape.li-2018` | Li et al. 2018 | Visualizing the loss landscape of neural nets | Foundational reference for loss-landscape claims |
| `src.loss-landscape.dauphin-2014` | Dauphin et al. 2014 | Identifying and attacking the saddle point problem | Cited for saddle-point analysis |

### Mixture and dropout architecture line

| source_id | author / year | claim line | dependency |
|---|---|---|---|
| `src.moe.shazeer-2017` | Shazeer et al. 2017 | Sparsely-gated mixture-of-experts routing | Required for [M] MoE sparse-routing claims |
| `src.moe.fedus-2022` | Fedus et al. 2022 | Switch Transformer sparse expert routing | Required for modern transformer MoE references |
| `src.dropout.gal-ghahramani-2016` | Gal & Ghahramani 2016 | Dropout as approximate Bayesian inference | Required for dropout-as-Bayesian-approximation claims |

### Empirical SAE / circuit references

These are external artifacts referenced by [E] claims. Full inventory belongs in an evidence pack. The entries here are minimal records required for claim-ledger `empirical_measurement_ref` fields.

| source_id | release | claim line | dependency |
|---|---|---|---|
| `src.sae.gemma-scope` | Google GemmaScope | SAE family for Gemma-2 models | Source for any GemmaScope [E] claim |
| `src.sae.llama-scope` | OpenMOSS Llama-Scope | SAE family for Llama-3.1-8B | Source for any Llama-Scope [E] claim |
| `src.sae.gpt2sm-res-jb` | Bloom 2024 | Canonical GPT-2 small residual SAEs | Foundational SAE empirical reference |
| `src.sae.gpt2sm-rfs-jb` | Bloom 2024 | GPT-2 small residual feature-splitting / cross-width SAE study | Source for cross-width feature-splitting [E] claims |
| `src.benchmark.axbench` | Stanford NLP / pyvene.ai | Steering baseline benchmark | Required for any steering-effectiveness [E] claim on Gemma-2-9B-IT |

## Source classes

Each source has a class that affects how it may be cited:

- **`foundational`**: published, peer-reviewed, widely accepted. Citable in any tag context including [M] only for the specific accepted result being used.
- **`peer_reviewed`**: published in a peer-reviewed venue. Citable in [M] for the specific results proved.
- **`preprint`**: arXiv or equivalent, not peer-reviewed. Citable in [M] only for specific constructively proved results; otherwise [T] or weaker.
- **`technical_report`**: institutional release with detailed methodology. Citable in [M] only for constructive results; otherwise [T], [E], or [G] depending on use.
- **`blog_post`**: LessWrong, distill.pub, or similar. Citable in [T] or [S] generally; in [M] only for results that have been independently formalized.
- **`empirical_artifact`**: a published model, SAE, dataset, or benchmark. Citable in [E], not [M], unless a separate proof exists.

A future machine-readable source-class file may be added later. Until then, this markdown ledger is an index, not an enforcement surface.

## What this ledger does NOT do

- It does not exhaustively cite every reference in the lawful-learning framework.
- It does not attest to source quality beyond the class notes above.
- It does not replace per-claim citation in framework docs.
- It does not establish citation discipline for promoted contracts in sourceos-spec or runtime evidence in AgentPlane.
- It does not validate source URLs, hashes, licenses, or source availability.
- It does not permit any [S] speculative claim to become [E] or [M].
- It does not permit any [G] governance invariant to become [M].

## Handoff

This file is retained as the first source-provenance index. Any future claim-ledger or publication checklist should cite source IDs from this file while preserving the claim-status boundaries above.
