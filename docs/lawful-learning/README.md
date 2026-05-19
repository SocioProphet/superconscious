# Lawful Learning

**Status:** H6 replayed capture; doctrine and navigation layer.  
**Origin branch:** `lawful-learning-capture-v1`.  
**Audit disposition:** replay-after-demotion from branch reconciliation audit.  
**Scope:** Directory index and claim-boundary discipline for the lawful-learning framework in `SocioProphet/superconscious`.

## H6 / H4 boundary

This README preserves useful orientation text that was left outside `main`, but updates the claim boundary to match the current hardening posture.

This directory may contain:

```text
doctrine
schema-backed declaration shapes
structural checkers
computational diagnostics
theorem-track candidates
proof-review-required material
exploratory or scoping notes
```

The directory does not, by its existence, claim:

```text
runtime evidence integration
proof-reviewed theorem status
empirical validation of speculative claims
runtime circuit discovery
runtime ablation verification
sourceos-spec promotion
AgentPlane runtime execution
cross-repo authority migration
```

Claim status is controlled by:

```text
docs/audits/2026-05-19-claim-status-ledger.md
docs/audits/2026-05-19-theorem-language-gate.md
docs/audits/2026-05-19-branch-reconciliation.md
```

## What this directory is

This directory is the repo-local home for lawful-learning doctrine and related schema/checker surfaces in `superconscious`.

The framework uses claim tags to keep different epistemic registers separate:

```text
[M] mathematical / provable
[T] typological / structural parallel
[S] speculative / research conjecture
[E] empirical / measured
[G] governance invariant
```

The discipline is:

- every claim should have a tag or equivalent claim-status boundary;
- tag promotion requires explicit evidence;
- mixed-tag claims must be demarcated;
- speculative research remains visible without being promoted;
- mathematical claims require named dependencies and, where theorem-facing, proof review;
- governance invariants name their operational form and must not be treated as world-facts or mathematical theorems.

## Why `superconscious` is the local home

`superconscious` is a visible governed-cognition / trust-surface coordination repo in the SocioProphet estate. Lawful-learning doctrine is relevant here because it governs cognition/control-loop framing, substrates, structure axes, circuits, adapter composition, and learning dynamics.

Stable contracts may promote outward only through the owning authority plane:

- canonical schemas: sourceos-spec or other schema authority after stabilization;
- cross-repo registration: SocioSphere;
- research evidence packs: dedicated evidence/research repos;
- runtime artifacts: AgentPlane or runtime-authority repos;
- governance invariants: ProCybernetica or the relevant governance plane.

`superconscious` may coordinate and record trust surfaces. It must not silently become the authority for schemas, policy, execution, model governance, workspace topology, or runtime audit.

## Current file map

Current and expected surfaces include:

```text
docs/lawful-learning/
├── README.md
├── 00-source-ledger.md
├── 01-framework-substrates-structures-circuits.md
├── 02-categorical-foundations.md
├── 03-lawful-learning-invariants.md
├── 09-t2-prime-polarization-scope.md
├── 10-a2-gate-minimality-scoping.md
├── 11-an-unified-gate-minimality-theorem.md
├── 12-d4-c7-prime-scoping.md
├── 13-d4-representation-inventory.md
├── 14-d4-strategy-b-scoping.md
└── remediation/
```

The numbering gap is intentional historical residue. Missing numbers should not be inferred as missing proof, runtime evidence, or finalized publication surfaces.

## Tag system

### [M] mathematical / provable

A claim that can be derived from explicit premises through accepted formal reasoning. Required field or equivalent: `mathematical_dependency` naming the result, theorem, or property the claim depends on.

Theorem-facing [M] material remains subject to H4 proof-review gates.

### [T] typological / structural parallel

A claim that two structures share an organizational pattern without necessarily sharing mathematical properties. Required field or equivalent: `typological_parallel_target` naming what the claim is parallel to.

### [S] speculative / research conjecture

A claim that proposes a research direction or expected property without proof or measurement. Required field or equivalent: `speculative_test_artifact` naming what would constitute a test.

### [E] empirical / measured

A claim backed by measurement on a defined artifact. Required field or equivalent: `empirical_measurement_ref` naming the measurement record, dataset, or benchmark result.

### [G] governance invariant

A claim that names a structural commitment the system enforces, not a fact about the world. Required field or equivalent: `governance_invariant_ref` naming the operational mechanism that enforces the invariant.

## Hard rules

Promotion rules:

- [T] cannot become [M] without explicit construction and proof review where theorem-facing.
- [S] cannot become [E] without measurement.
- [E] cannot become [M] without proof.
- [G] cannot become [M]; governance invariants are not theorems.
- CI success cannot promote claim status.
- Schema validation cannot promote claim status beyond `schema_validated_shape_only`.

Field requirements:

- Reject [M] without `mathematical_dependency` or equivalent dependency statement.
- Reject [T] without `typological_parallel_target` or equivalent target statement.
- Reject [S] without `speculative_test_artifact` or equivalent test statement.
- Reject [E] without `empirical_measurement_ref` or equivalent measurement reference.
- Reject [G] without `governance_invariant_ref` or equivalent mechanism reference.
- Reject tag-promotion events without the new tag's required evidence.

Subject-specific rules:

- Hopfield-network proof claims require a named energy-function form.
- Sedenion-substrate claims require a named algebraic dependency.
- May-Wigner theorem claims require random-matrix assumptions; otherwise the claim remains [T] or [G].
- Mixed-tag claims require demarcation.

## What this directory does not claim

This directory does not claim:

```text
framework completeness
frontier conjecture truth
schema authority migration
runtime evidence integration
AgentPlane execution
sourceos-spec promotion
proof-reviewed theorem status by default
external source quality attestation
public release readiness
```

The directory creates and preserves discipline. Separate authority planes and later PRs must provide schema promotion, runtime execution, evidence receipts, proof review, or public release authority.
