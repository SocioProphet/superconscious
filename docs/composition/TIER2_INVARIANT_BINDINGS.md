# Tier 2 Invariant Bindings for superconscious

## Status

Doctrine-only binding document.

This document binds `SocioProphet/superconscious` composition surfaces to the Tier 2 composition invariant family defined in `SocioProphet/ProCybernetica`:

```text
docs/governance-fabric/TIER2_COMPOSITION_INVARIANTS.md
```

It does not redefine the invariants. It consumes the canonical ProCybernetica doctrine by reference.

## Reference doctrine

Canonical source:

```text
SocioProphet/ProCybernetica
docs/governance-fabric/TIER2_COMPOSITION_INVARIANTS.md
```

Reference state at time of this binding:

```text
ProCybernetica PR #56: Tier 2 composition invariants doctrine
ProCybernetica PR #57: evidence freshness analysis
```

Merged invariant family consumed here:

```text
baseline composition certificate invariants
receipt_integration: hash_bound_reference
authority_scope_analysis: declared_scope_lattice_v1
non_claim_analysis: explicit_propagate_or_resolve_v1
monitor_independence_analysis: declared_monitor_independence_v1
evidence_freshness_analysis: declared_evidence_freshness_v1
```

## Binding semantics

A binding entry declares that a `superconscious` composition surface is governed by one or more ProCybernetica Tier 2 invariants.

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

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: composed certificate authority must not exceed constituent authority.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: M1 composite must not silently drop source-lock, witness-card, causal, attribution, or off-target-audit non-claims.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent review or independent monitoring is claimed
  reason: independent review is a composition claim and must not collapse into shared-monitor or self-monitor relationships.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: source-locks, witness cards, audits, and attribution graphs may be reused after creation time; stale evidence must be refreshed or acknowledged.
```

### Implementation references

```text
schemas/m1/implementability-certificate.v1.2.json
schemas/m1/source-lock.v1.2.json
schemas/m1/off-target-audit.v1.2.json
schemas/m1-5/attribution-graph.v1.json
schemas/m0/training-provenance.v1.json
```

### Non-claims

This binding does not claim that current M1 fixtures already instantiate ProCybernetica Tier 2 composition certificates.

This binding does not claim runtime receipt lookup, runtime non-claim verification, runtime monitor attestation, or runtime timestamp authenticity.

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

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: a public note must not claim broader authority than its upstream certificates support.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: public notes are high-risk surfaces for silent non-claim erosion.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent review is claimed
  reason: independent review claims must identify distinct, non-self, acyclic monitor relationships.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: publication timing is materially relevant to whether supporting certificates remain current.
```

### Implementation references

```text
schemas/m5/public-note.v1.json
templates/m5/
```

### Non-claims

This binding does not claim that any public note has been runtime-produced or externally published.

This binding does not claim legal, regulatory, or production safety certification.

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

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: the release bundle must not claim broader interpretability authority than its constituent artifacts support.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: each fragment carries non-claims that must survive into the release bundle unless evidence-resolved.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: true
  reason: release bundles are expected to assert review/monitoring structure.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: release bundles can combine artifacts produced at different times.
```

### Implementation references

```text
schemas/interpretability/*
schemas/m1-5/attribution-graph.v1.json
schemas/m2/*
schemas/m3/*
schemas/m5/*
```

### Non-claims

The 14-fragment composition fixture is not implemented in this binding PR.

This binding only declares the governance contract the future fixture must satisfy.

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

authority_scope_analysis: declared_scope_lattice_v1
  applies: true
  reason: a trust surface must not broaden the authority of its constituent claims.

non_claim_analysis: explicit_propagate_or_resolve_v1
  applies: true
  reason: lawful-learning doctrine separates mathematical, typological, speculative, empirical, and governance claims; that separation must not collapse under composition.

monitor_independence_analysis: declared_monitor_independence_v1
  applies: when independent monitoring is claimed
  reason: independent monitoring claims require declared monitor independence.

evidence_freshness_analysis: declared_evidence_freshness_v1
  applies: true
  reason: trust surfaces may compose evidence captured at different times.
```

### Implementation references

```text
docs/lawful-learning/
examples/TRUST_SURFACE.lawful-learning.yaml
```

### Non-claims

The lawful-learning trust-surface fixture is not implemented in this binding PR.

This binding does not promote speculative lawful-learning claims to empirical or mathematical claims.

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

This document does not add new schemas or fixtures.

This document does not claim runtime evidence verification, runtime monitor attestation, timestamp authenticity, or recursive composition.

This document does not bind compositions not listed above.

## Future extensions

When ProCybernetica lands new Tier 2 invariant modes, this document should be updated to state whether each listed `superconscious` composition adopts, defers, or rejects the new mode.

Likely future updates:

```text
verified_propagate_or_resolve_v2
verified_monitor_independence_v2
verified_evidence_freshness_v2
declared_authority_concentration_v1
declared_scope_coverage_v1
```

The next implementation step after this binding should be a concrete fixture or schema extension in `superconscious` that instantiates one bound composition against the ProCybernetica Tier 2 invariant family.
