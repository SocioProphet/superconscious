# Lawful Learning Capture

**Status:** v1 capture. Doctrine layer; no schemas yet.  
**Date:** May 12, 2026  
**Scope:** Captures the lawful-learning framework — substrates, structures,
circuits, mixture slots, adapter machinery, shared-trunk protocols, feature
alignment, lifecycle, and governance integration — under explicit epistemic
discipline. Tags every claim as mathematical [M], typological [T], speculative
[S], empirical [E], or governance [G], with hard rules preventing silent
tag promotion.

## What this capture is

This directory is the canonical home of the lawful-learning framework in
SocioProphet/superconscious. It captures the entire intellectual stack —
including frontier conjectures — without forcing every claim into the same
epistemic register. The discipline is:

- Every claim has a tag (M/T/S/E/G)
- Tag promotion requires explicit evidence
- Mixed-tag claims are demarcated sentence-by-sentence
- Frontier research is marked [S] until measured or proved
- Mathematical claims name their dependencies
- Typological parallels name their targets
- Governance invariants name their operational form

The capture exists to preserve the framework as a coherent intellectual whole
while preventing overclaim drift. Speculative research stays visible without
being promoted to settled fact.

## Why superconscious is the right home

Per the SocioProphet estate ownership map (ProCybernetica PR #49), superconscious
owns the visible cognition / control-loop and trust-surface seed. The lawful-
learning framework is a cognition/control-loop doctrine: substrate axes,
structure axes, circuits, adapter composition, learning dynamics. It belongs
in superconscious as doctrine.

Stable contracts will promote outward by authority boundary:

- Canonical schemas → SourceOS-Linux/sourceos-spec when stable
- Cross-repo registration → SocioSphere
- Research evidence pack → systems-learning-loops
- Runtime artifacts → AgentPlane (Phase 9, runtime should not outrun doctrine)

This README does not specify the framework content. That lives in
`01-framework-substrates-structures-circuits.md` after Phase 2 cleanup,
which is blocked on this capture (Phase 1) landing first.

## File map

```text
docs/lawful-learning/
├── README.md                                           ← this file
├── 00-source-ledger.md                                 ← Phase 1 (this PR)
├── 01-framework-substrates-structures-circuits.md      ← Phase 2 (next PR)
├── 02-categorical-foundations.md                       ← Phase 3 (later PR)
├── 03-lawful-learning-invariants.md                    ← Phase 4 (later PR)
├── 04-frontier-research-conjectures.md                 ← Phase 2 (next PR)
├── 05-word-sense-and-polysemanticity-review.md         ← Phase 2 (next PR)
├── 06-publication-checklist.md                         ← Phase 1 (this PR)
└── 07-claim-ledger.md                                  ← Phase 1 (this PR)
```

## Tag system

Five tags. Each tag has required evidence and a promotion rule.

### [M] mathematical / provable

A claim that can be derived from explicit premises through accepted formal
reasoning. Required field: `mathematical_dependency` naming the result,
theorem, or property the claim depends on. Example: "Modern continuous
Hopfield networks have exponential storage capacity [M; dependency:
Ramsauer et al. 2020, log-sum-exp energy function]."

### [T] typological / structural parallel

A claim that two structures share an organizational pattern without
necessarily sharing mathematical properties. Required field:
`typological_parallel_target` naming what the claim is parallel to.
Example: "Mixture-of-experts routing exhibits a control-plane / data-plane
separation [T; target: traditional networking architectures]."

### [S] speculative / research conjecture

A claim that proposes a research direction or expected property without
proof or measurement. Required field: `speculative_test_artifact` naming
what would constitute a test (an experiment, a fixture, a measurement
protocol). Example: "Sedenion substrates may provide robustness against
adversarial perturbations [S; test_artifact: TBD adversarial fixture
suite on sedenion-Hopfield prototype]."

### [E] empirical / measured

A claim backed by measurement on a defined artifact. Required field:
`empirical_measurement_ref` naming the measurement record, dataset, or
benchmark result. Example: "GPT-2 small SAEs at width 12288 show feature
splitting relative to width 768 [E; measurement_ref: Bloom 2024 feature-
splitting study, gpt2sm-rfs-jb]."

### [G] governance invariant

A claim that names a structural commitment the system enforces, not a
fact about the world. Required field: `governance_invariant_ref` naming
the operational mechanism that enforces the invariant. Example:
"Adapter dependency graphs must be acyclic [G; invariant_ref:
adapter_dag_acyclic check in scripts/check-lawful-learning.py]."

## Hard rules

These are constitutional. The checker in Phase 6 enforces them.

**Promotion rules:**

- [T] cannot become [M] without explicit construction
- [S] cannot become [E] without measurement
- [E] cannot become [M] without proof
- [G] cannot become [M] (governance invariants are not theorems)

**Field requirements:**

- Reject [M] without `mathematical_dependency`
- Reject [T] without `typological_parallel_target`
- Reject [S] without `speculative_test_artifact`
- Reject [E] without `empirical_measurement_ref`
- Reject [G] without `governance_invariant_ref`
- Reject any tag-promotion event without the new tag's required field
  populated with promotion evidence

**Subject-specific rules:**

- Reject Hopfield-network proof claims that lack a named energy-function form
- Reject sedenion-substrate claims that lack a named algebraic dependency
- Reject May-Wigner theorem claims unless random-matrix assumptions are
  explicitly stated; otherwise the claim stays [T] or [G]
- Reject mixed-tag claims unless demarcation is sentence-by-sentence

## Acceptance criteria for Phase 1

- All major framework claims captured in the ledger
- Every claim has a tag
- Every [M] has `mathematical_dependency` populated
- Every [T] has `typological_parallel_target` populated
- Every [S] has `speculative_test_artifact` populated (may be TBD-marked)
- Every [E] has `empirical_measurement_ref` populated
- Every [G] has `governance_invariant_ref` populated
- All frontier claims marked [S] unless already proved or measured
- Source ledger captures provenance for non-original claims
- Publication checklist captures the public-release boundary

## What this capture does NOT claim

- It does NOT claim the framework is complete
- It does NOT claim any [S] frontier conjecture is true
- It does NOT promote any claim above its current tag
- It does NOT establish schemas (Phase 5)
- It does NOT establish checker enforcement (Phase 6)
- It does NOT establish trust-surface examples (Phase 4)
- It does NOT establish runtime evidence integration (Phase 9)
- It does NOT supersede or replace any existing certificate or governance
  artifact in superconscious

The capture creates the discipline. Subsequent phases consume it.
