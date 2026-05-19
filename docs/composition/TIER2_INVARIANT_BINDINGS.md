# Tier 2 Invariant Bindings for superconscious

## Status

Doctrine-only binding document with source-pinned ProCybernetica reference and explicit schema-only boundary.

This document binds `SocioProphet/superconscious` composition surfaces to the Tier 2 composition invariant family defined in `SocioProphet/ProCybernetica`.

It does not redefine the invariants. It consumes the canonical ProCybernetica doctrine by immutable reference and records which invariant modes this repository adopts, defers, or leaves out of scope.

## Source-pinned reference doctrine

Canonical source:

```text
SocioProphet/ProCybernetica
docs/governance-fabric/TIER2_COMPOSITION_INVARIANTS.md
```

Pinned source state consumed by this binding:

```text
ProCybernetica PR #56: Add Tier 2 composition invariants doctrine
merge_commit_sha: a8e6b47648696658b8fd1d81239953fb2e8f11f0

ProCybernetica PR #57: Add Tier 2 evidence freshness analysis
merge_commit_sha: 173fc92a21e4cf1b2a785365adc992f441910488

consumed_document_version: v1.1 doctrine
consumed_path: docs/governance-fabric/TIER2_COMPOSITION_INVARIANTS.md
```

The PR #56 source establishes the canonical Tier 2 composition invariant pattern, baseline composition certificate invariants, receipt integration, authority scope comparison, non-claim propagation, and monitor independence. The PR #57 source adds `evidence_freshness_analysis` with `declared_evidence_freshness_v1` and keeps the same declared/static Tier 2 boundary.

## Schema-only guarantee

Every binding schema and fixture under `schemas/composition/*tier2-binding*.json` and `tests/fixtures/composition/*tier2-binding*.json` is a **Layer 1 declaration-shape artifact**.

These schemas and fixtures validate only:

```text
composition identity
composition kind
opaque reference shape
bound mode names
required non-claims
forbidden runtime-bearing fields
surface-specific required fields
```

They do **not** perform or claim:

```text
runtime receipt lookup
source hash resolution
artifact existence checks
semantic invariant verification
non-claim evidence verification
monitor attestation
timestamp authenticity
transitive supersession traversal
runtime provider access
runtime circuit discovery
proof review
theorem verification
public claim promotion
full ProCybernetica composition-certificate instantiation
```

A CI-green Tier 2 binding fixture means only that the local declaration shape is valid and that explicit negative fixtures are rejected at the local schema/checker layer. It is not evidence that ProCybernetica has verified the underlying invariant semantics at runtime.

## Adopt / defer / out-of-scope mode table

| Mode | Local disposition | Boundary |
|---|---:|---|
| `receipt_integration: hash_bound_reference` | adopted | Opaque/hash-shaped reference only; no runtime receipt-store lookup. |
| `authority_scope_analysis: declared_scope_lattice_v1` | adopted | Declared mode name only in these local bindings; no runtime or formal scope-lattice proof. |
| `non_claim_analysis: explicit_propagate_or_resolve_v1` | adopted | Binding declares the mode; local binding schemas do not verify resolution evidence. |
| `monitor_independence_analysis: declared_monitor_independence_v1` | adopted | Declared monitor-independence mode only; no runtime monitor attestation. |
| `evidence_freshness_analysis: declared_evidence_freshness_v1` | adopted | Declared freshness mode only; no timestamp authenticity or supersession traversal. |
| `verified_propagate_or_resolve_v2` | deferred | Requires runtime/source evidence semantics not present in this repo. |
| `verified_monitor_independence_v2` | deferred | Requires runtime monitor attestation evidence. |
| `verified_evidence_freshness_v2` | deferred | Requires timestamp or transparency-log proof machinery. |
| `declared_authority_concentration_v1` | deferred | Requires signer/reputation or authority-concentration substrate. |
| `declared_scope_coverage_v1` | deferred | Requires comparable scope-lattice definition beyond this binding surface. |

## Binding semantics

A binding entry declares that a `superconscious` composition surface is governed by one or more ProCybernetica Tier 2 invariant modes.

A binding is not runtime enforcement. It is a doctrine contract: future schema fixtures, public-release compositions, or runtime-produced certificates in this repo must either satisfy the listed invariant modes or explicitly state why the composition is out of scope.

Each binding records:

```text
composition_id
composition_kind
constituent_surface
bound_invariants
implementation_reference
status
non_claims
```

The binding document and local binding schemas are therefore admissibility declarations, not proof artifacts.

## 1. M1 composite certificate binding

### Composition identity

```text
composition_id: superconscious.m1.composite
composition_kind: certificate_fragment_composition
status: doctrine_bound_schema_surface_exists
```

### Constituent surface

The M1 composite composes upstream certificate fragments from the implementability pipeline.

Current and planned constituents include:

```text
M0 training provenance
M1A source-lock
M1B witness card
M1C causal triad
M1.5 attribution graph
M1D off-target audit
M1 composite summary
```

### Bound invariants

```text
receipt_integration: hash_bound_reference
  applies: true
  reason: constituent certificate fragments must remain evidence-bound.
  local_boundary: local M1 binding fixture checks opaque hash shape only.

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: composed certificate authority must not exceed constituent authority.
  local_boundary: local M1 binding fixture declares mode adoption only.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: M1 composite must not silently drop source-lock, witness-card, causal, attribution, or off-target-audit non-claims.
  local_boundary: local M1 binding fixture does not verify propagated/resolved evidence.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent review or independent monitoring is claimed
  reason: independent review is a composition claim and must not collapse into shared-monitor or self-monitor relationships.
  local_boundary: local M1 binding fixture does not attest monitor independence.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: source-locks, witness cards, audits, and attribution graphs may be reused after creation time; stale evidence must be refreshed or acknowledged.
  local_boundary: local M1 binding fixture does not verify timestamp authenticity or freshness windows.
```

### Implementation references

```text
schemas/m1/implementability-certificate.v1.2.json
schemas/m1/source-lock.v1.2.json
schemas/m1/off-target-audit.v1.2.json
schemas/m1-5/attribution-graph.v1.json
schemas/m0/training-provenance.v1.json
schemas/composition/m1-tier2-binding.v1.json
```

### Non-claims

This binding does not claim that current M1 fixtures already instantiate ProCybernetica Tier 2 composition certificates.

This binding does not claim runtime receipt lookup, runtime non-claim verification, runtime monitor attestation, timestamp authenticity, source hash resolution, artifact existence checking, or proof review.

## 2. M5 public note binding

### Composition identity

```text
composition_id: superconscious.m5.public_note
composition_kind: publication_composition
status: doctrine_bound_schema_surface_exists
```

### Constituent surface

The M5 public note composes upstream certificates, claim qualifications, figures, limitations, non-claims, and public-facing publication text.

### Bound invariants

```text
receipt_integration: hash_bound_reference
  applies: true
  reason: public notes must remain bound to the certificate fragments and evidence receipts they summarize.
  local_boundary: local M5 binding fixture checks opaque hash shape only.

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: a public note must not claim broader authority than its upstream certificates support.
  local_boundary: local M5 binding fixture declares mode adoption only.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: public notes are high-risk surfaces for silent non-claim erosion.
  local_boundary: local M5 binding fixture does not verify propagated/resolved evidence.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent review is claimed
  reason: independent review claims must identify distinct, non-self, acyclic monitor relationships.
  local_boundary: local M5 binding fixture does not attest monitor independence.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: publication timing is materially relevant to whether supporting certificates remain current.
  local_boundary: local M5 binding fixture does not verify timestamp authenticity or freshness windows.
```

### Implementation references

```text
schemas/m5/public-note.v1.json
templates/m5/
schemas/composition/m5-tier2-binding.v1.json
```

### Non-claims

This binding does not claim that any public note has been runtime-produced or externally published.

This binding does not claim legal, regulatory, production safety certification, peer-review substitution, runtime publication gating, source hash resolution, artifact existence checking, or public claim promotion.

## 3. Interpretability harness release binding

### Composition identity

```text
composition_id: superconscious.interpretability_harness.release_bundle
composition_kind: full_release_composition
status: doctrine_bound_future_fixture
```

### Constituent surface

The intended release bundle composes a full interpretability harness surface. The expected 14-fragment shape is:

```text
ModelArtifact
SAEArtifact
FeatureArtifact
FeatureExplanation
FeatureActivationSet
SteeringIntervention
CausalTriad
AttributionGraph
OffTargetAudit
ManifoldBaseline
ImplementabilityCurve
RobustnessCertificate
BenchmarkResult
PublicInterpretabilityNote
```

### Bound invariants

```text
receipt_integration: hash_bound_reference
  applies: true
  reason: release bundles must keep every artifact and evidence receipt hash-bound.
  local_boundary: local interpretability-harness binding fixture checks opaque hash shape only.

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: the release bundle must not claim broader interpretability authority than its constituent artifacts support.
  local_boundary: local interpretability-harness binding fixture declares mode adoption only.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: each fragment carries non-claims that must survive into the release bundle unless evidence-resolved.
  local_boundary: local interpretability-harness binding fixture does not verify propagated/resolved evidence.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: true
  reason: release bundles are expected to assert review/monitoring structure.
  local_boundary: local interpretability-harness binding fixture does not attest monitor independence.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: release bundles can combine artifacts produced at different times.
  local_boundary: local interpretability-harness binding fixture does not verify timestamp authenticity or freshness windows.
```

### Implementation references

```text
schemas/interpretability/*
schemas/m1-5/attribution-graph.v1.json
schemas/m2/*
schemas/m3/*
schemas/m5/*
schemas/composition/interpretability-harness-tier2-binding.v1.json
```

### Non-claims

The 14-fragment composition fixture is not implemented by this binding document alone.

This binding only declares the governance contract the future fixture must satisfy.

This binding does not claim runtime provider access, model download, feature activation, live steering execution, hidden-state replay, Neuronpedia API integration, source hash resolution, artifact existence checking, public claim promotion, runtime receipt lookup, monitor attestation, timestamp authenticity, or full ProCybernetica composition-certificate instantiation.

## 4. Lawful-learning trust-surface binding

### Composition identity

```text
composition_id: superconscious.lawful_learning.trust_surface
composition_kind: lawful_learning_trust_surface_declaration
status: doctrine_bound_future_fixture
```

### Constituent surface

The lawful-learning trust surface composes the capture-ledger domains of the lawful-learning framework.

Expected constituent domains include:

```text
Substrate
Structure
Mixture
Adapter
Circuit Registry
Governance integration
Evidence / claim ledger
```

### Bound invariants

```text
receipt_integration: hash_bound_reference
  applies: true
  reason: lawful-learning trust surfaces must bind the claims they aggregate.
  local_boundary: local lawful-learning binding fixture checks opaque hash shape only.

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: a trust surface must not broaden the authority of its constituent claims.
  local_boundary: local lawful-learning binding fixture declares mode adoption only.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: lawful-learning doctrine separates mathematical, typological, speculative, empirical, and governance claims; that separation must not collapse under composition.
  local_boundary: local lawful-learning binding fixture does not verify propagated/resolved evidence or tag promotion.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent monitoring is claimed
  reason: independent monitoring claims require declared monitor independence.
  local_boundary: local lawful-learning binding fixture does not attest monitor independence.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: trust surfaces may compose evidence captured at different times.
  local_boundary: local lawful-learning binding fixture does not verify timestamp authenticity or freshness windows.
```

### Implementation references

```text
docs/lawful-learning/
examples/TRUST_SURFACE.lawful-learning.yaml
schemas/composition/lawful-learning-trust-surface-tier2-binding.v1.json
```

### Non-claims

The lawful-learning trust-surface fixture is not implemented by this binding document alone.

This binding does not promote speculative lawful-learning claims to empirical or mathematical claims.

This binding does not claim runtime circuit discovery, runtime ablation verification, tag promotion at composition time, substrate verification, frontier-claim promotion, source hash resolution, artifact existence checking, runtime receipt lookup, monitor attestation, timestamp authenticity, or proof review.

## Out-of-scope compositions

The following surfaces are not bound by this document until a future PR names them explicitly:

```text
ad hoc research notes
scratchpad documents
unsealed drafts
single-fragment certificates that do not compose upstream fragments
local-only experiments without a publication or certificate surface
```

Absence from this document is not an implicit exemption for a production composition. A production composition must either bind to this doctrine or state a reason for being out of scope.

## Boundary and non-claims

This document does not redefine any Tier 2 invariant. ProCybernetica remains the canonical source.

This document does not add runtime enforcement.

This document does not claim runtime evidence verification, runtime monitor attestation, timestamp authenticity, source hash resolution, artifact existence checking, recursive composition, proof review, theorem verification, or public claim promotion.

This document does not bind compositions not listed above.

## Future extensions

When ProCybernetica lands new Tier 2 invariant modes, this document must be updated to state whether each listed `superconscious` composition adopts, defers, rejects, or leaves out of scope the new mode.

Likely future updates remain deferred until their substrates exist:

```text
verified_propagate_or_resolve_v2
verified_monitor_independence_v2
verified_evidence_freshness_v2
declared_authority_concentration_v1
declared_scope_coverage_v1
```

The next implementation step after this binding is the claim-status ledger required by the damage-audit hardening plan, followed by branch/content reconciliation and theorem-language review.
