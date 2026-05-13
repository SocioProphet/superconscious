# Lawful Learning Framework: Substrates, Structures, and Circuits

**Status:** Phase 2 canonical framework cleanup.

**Date:** May 13, 2026

**Scope:** Reconstructs the lawful-learning framework from the Phase 1 capture ledger and applies the Phase 2 cleanup rules: explicit claim tagging, behavior-first ordering, shared-trunk protocol naming, frontier-claim boundaries, placeholder formula labeling, and Tier 2 trust-surface alignment.

**Authorial status:** Captures the Heller lawful-learning program. Assistant changes are editorial structuring, cleanup, and governance alignment; the core framework is Michael Heller's work.

## 0. Claim-tag discipline

Every substantive claim in this document is labeled with one or more of the following tags.

```text
[M] Mathematical claim: formal statement, definition, or theorem-grade construction.
[T] Typological claim: architecture, taxonomy, schema, or engineering classification.
[S] Speculative / frontier claim: conjectural, exploratory, or not yet validated.
[E] Empirical claim: requires measured evidence or experiment.
[G] Governance claim: policy, evidence, provenance, promotion, or trust-surface rule.
```

Mixed-tag claims must be sentence-demarcated. A sentence may carry multiple tags only when the claim genuinely depends on both registers. Where a paragraph contains mixed registers, this document separates the sentences and marks each register explicitly.

This document does not silently promote [S] claims to [E] or [M]. Tag promotion requires a future checker and evidence lane.

## 1. Behavior-first framing

[G|T] The invariant object of lawful learning is not an unconstrained parameter vector, an embedding trick, or a substrate metaphor. The invariant object is the set of admissible learning behaviors under declared law, evidence, replay, and promotion constraints.

[T] A lawful-learning system is therefore specified by its behavior surface first:

```text
admissible inputs
admissible outputs
constraint family
substrate declaration
structure declaration
mixture protocol
adapter protocol
circuit registry
claim ledger
evidence surface
promotion rule
non-claim boundary
```

[G] A lawful-learning artifact is not considered publishable unless its law surface and evidence surface are both declared. This is the working doctrine behind the summary equation:

```text
Truth = Law x Evidence
```

[T] In this equation, "Law" means declared constraints, admissibility rules, substrate assumptions, structural choices, and governance gates. [G] "Evidence" means replayable, typed, provenance-bound artifacts that support or limit the claim.

## 2. Substrate axis

[T] The substrate axis declares which algebraic or geometric carrier is being used for a learning component. It is a declaration surface, not a proof by itself.

Phase 2 recognizes the following substrate families:

```text
real
complex
quaternion
octonion
sedenion
hypercomplex family declaration
Poincare / hyperbolic embedding
spectral coordinates
constraint-index coordinates
```

[M] Real and complex substrate declarations can be given ordinary vector-space semantics when the operations used by the model are explicitly defined.

[S] Quaternionic, octonionic, sedenionic, and broader hypercomplex substrate declarations are frontier extensions unless the relevant multiplication, norm, associator, and projection operations are fully specified and tested.

[S] The `zero_divisor_proximity` quantity is currently a placeholder frontier formula. It must not be used as an empirical or mathematical claim until a concrete definition, admissible domain, numerical procedure, and validation test are supplied.

```text
zero_divisor_proximity := PLACEHOLDER[S]
```

[S] The `hurwitz_residual` quantity is currently a placeholder frontier formula. It must not be used as an empirical or mathematical claim until a concrete definition, admissible domain, numerical procedure, and validation test are supplied.

```text
hurwitz_residual := PLACEHOLDER[S]
```

[G] Any trust surface that cites either placeholder must propagate the placeholder status as a non-claim. [G] The lawful-learning trust-surface Tier 2 binding enforces that tag promotion cannot occur at composition time.

Ledger anchors:

```text
claim.substrate.zero-divisor-proximity-formula.S
claim.substrate.hurwitz-residual-formula.S
```

## 3. Structure axis

[T] The structure axis declares the qualitative law family applied to the substrate. The current lawful-learning structure families are:

```text
monotonicity
dominance
complementarity
trapezoid
unimodality
sparsity / support discipline
constraint family registry
circuit registry
```

[M] A constraint family becomes mathematical only when its variables, admissible domain, inequalities, and closure properties are stated precisely.

[T] A constraint family may still be useful typologically before theorem-grade closure is available, but it must remain tagged [T] or [G] rather than promoted to [M].

[S] Hypercomplex Hopfield-style structure is an operational extension candidate, not a settled mathematical result in this framework. It may be used as a design hypothesis for future experiments, but current documents must not claim that hypercomplex Hopfield dynamics are validated, stable, or superior without evidence.

Ledger anchor:

```text
claim.structure.hypercomplex-hopfield.S
```

## 4. Mixture slots

[T] A mixture slot is a typed location where multiple lawful components may be combined under an explicit allocation rule.

[T] Mixture slots are not unconstrained ensembles. They must declare:

```text
slot_id
allowed component classes
allocation rule
conflict rule
fallback rule
non-claim propagation rule
evidence reference rule
```

[G] A mixture slot that composes multiple claims must propagate constituent non-claims or resolve them with declared evidence. [G] This imports the ProCybernetica Tier 2 non-claim invariant into lawful-learning trust surfaces.

[T] A mixture slot can be used for substrate mixing, adapter selection, constraint selection, or circuit-routing selection, provided the relevant law and evidence surfaces are preserved.

## 5. Shared trunk protocol

[T] The phrase "shared trunk" is replaced here by **shared trunk protocol**. The point is not merely that components share a trunk; the point is that trunk-sharing is governed by an explicit protocol.

A shared trunk protocol declares:

```text
trunk_id
shared state boundary
allowed consumers
adapter interface
non-claim propagation
monitoring boundary
evidence receipt rule
freshness rule
promotion rule
```

[G] A shared trunk protocol must prevent a downstream component from silently widening the authority, evidence, or claim status of an upstream component.

[T] A shared trunk protocol may be implemented in a neural model, an agent runtime, a schema registry, or a governance fabric. The protocol claim is typological unless a concrete implementation and test harness are supplied.

Ledger anchor:

```text
claim.adapter.shared-trunk-protocol.T
```

## 6. Adapter DAG

[T] An adapter DAG is the directed acyclic graph through which lawful-learning components connect to substrates, structures, mixture slots, and circuit registries.

The adapter DAG declares:

```text
adapter_id
source component
target component
interface type
state transformation
claim transformation
non-claim propagation
freshness propagation
monitoring relation
```

[G] A lawful adapter cannot silently promote a claim. [G] Promotion from [S] to [E] or [M] requires a separate checker and evidence artifact.

[T] Cycles are prohibited at the adapter DAG layer unless a later document explicitly introduces recursive composition semantics. Current Phase 2 doctrine remains flat-composition compatible.

## 7. Circuit registry

[T] A circuit registry records proposed components, pathways, probes, ablations, and evidence references for lawful-learning circuits.

A circuit registry entry should contain:

```text
circuit_id
substrate declaration
structure declaration
input surface
output surface
adapter dependencies
expected behavior
evidence references
ablation references
non-claims
status tag
```

[E] A circuit is empirically supported only when replayable evidence, ablation or intervention evidence, and off-target checks exist.

[G] The lawful-learning trust-surface Tier 2 binding explicitly does not perform runtime circuit discovery. It only binds declared circuit-registry entries into a trust surface.

[G] The lawful-learning trust-surface Tier 2 binding explicitly does not perform runtime ablation verification. Ablation evidence may be referenced, but validation belongs to a future checker.

## 8. Invariant monitors and mixed-register claims

This section applies the Phase 2 sentence-level demarcation rule to three mixed-register monitors that had been structurally ambiguous.

### 8.1 May-Wigner monitor

[G] The May-Wigner monitor is a governance monitor when used to require evidence, non-claim propagation, and promotion control over stability or spectrum-related assertions.

[T] The May-Wigner monitor is a typological monitor when used to classify a learning component by spectrum, random-matrix analogy, or stability-surface shape.

[S] Any claim that May-Wigner structure explains or guarantees a concrete learning behavior remains speculative until an empirical or mathematical support lane is supplied.

Ledger anchor:

```text
claim.invariant.may-wigner-monitor.G|T
```

### 8.2 Tail-integral audit

[G] The tail-integral audit is a governance audit when used to require declaration of long-tail risk, evidence freshness, and non-claim retention.

[S] The tail-integral audit is speculative when used as a proposed analytic invariant before the actual tail integral, measure, convergence condition, and estimator are specified.

[E] A tail-integral audit becomes empirical only when attached to data, estimator, uncertainty model, and reproducible measurement.

Ledger anchor:

```text
claim.invariant.tail-integral-audit.G|S
```

### 8.3 Composition-superposition allocation

[G] Composition-superposition allocation is a governance rule when used to prevent an ensemble, mixture slot, or shared trunk protocol from silently masking the origin of a claim.

[T] Composition-superposition allocation is a typological rule when used to classify whether behavior is produced by explicit composition, latent superposition, or a hybrid of the two.

[S] Any claim that a specific allocation formula fully separates composition from superposition remains speculative until a concrete estimator and validation lane exist.

Ledger anchor:

```text
claim.invariant.composition-superposition-allocation.G|T
```

## 9. Trust surface

[G] A lawful-learning trust surface is a composition of substrate declarations, structure declarations, mixture slots, adapter DAG entries, circuit registry entries, and the claim ledger.

[T] The trust surface is a composition object. It is governed by the Tier 2 invariant catalog through the lawful-learning trust-surface binding.

Current bound modes:

```text
receipt_integration: hash_bound_reference
authority_scope_analysis: declared_scope_lattice_v1
non_claim_analysis: explicit_propagate_or_resolve_v1
monitor_independence_analysis: declared_monitor_independence_v1
evidence_freshness_analysis: declared_evidence_freshness_v1
```

[G] The binding is doctrine-only. It does not discover circuits, run ablations, promote tags, verify substrates, or promote frontier claims.

Required trust-surface non-claims:

```text
no_runtime_receipt_lookup
no_runtime_non_claim_verification
no_runtime_monitor_attestation
no_timestamp_authenticity
opaque_hashes_not_resolved
no_runtime_circuit_discovery
no_runtime_ablation_verification
no_tag_promotion_at_composition
no_substrate_verification
no_frontier_claim_promotion
```

## 10. Publication and promotion discipline

[G] Publication readiness is not a function of rhetorical coherence alone. It requires a claim ledger, tag discipline, non-claim propagation, evidence references, and a trust-surface binding.

[G] Claims tagged [S] remain frontier claims. They may be preserved, studied, and scaffolded, but they must not be marketed as empirical or mathematical results.

[G] Claims tagged [T] may define useful architecture without being theorem-grade.

[G] Claims tagged [E] require reproducible evidence.

[M] Claims tagged [M] require formal definitions and proof-grade support.

[G] The lawful-learning Phase 6 checker is the first future gate allowed to enforce tag promotion rules mechanically. Until then, this document is a canonical editorial and governance cleanup, not a runtime checker.

## 11. Phase 2 cleanup ledger

The following cleanup actions are applied in this document.

| Cleanup item | Ledger anchor | Phase 2 treatment |
|---|---|---|
| Replace "shared trunk" with "shared trunk protocol" | `claim.adapter.shared-trunk-protocol.T` | Implemented in Section 5 |
| Soften hypercomplex Hopfield claims | `claim.structure.hypercomplex-hopfield.S` | Implemented in Section 3 |
| Mark empty zero-divisor formula as placeholder | `claim.substrate.zero-divisor-proximity-formula.S` | Implemented in Section 2 |
| Mark empty Hurwitz residual formula as placeholder | `claim.substrate.hurwitz-residual-formula.S` | Implemented in Section 2 |
| Demarcate May-Wigner monitor by sentence | `claim.invariant.may-wigner-monitor.G|T` | Implemented in Section 8.1 |
| Demarcate tail-integral audit by sentence | `claim.invariant.tail-integral-audit.G|S` | Implemented in Section 8.2 |
| Demarcate composition-superposition allocation by sentence | `claim.invariant.composition-superposition-allocation.G|T` | Implemented in Section 8.3 |

## 12. Explicit non-claims

This Phase 2 document does not claim:

```text
runtime circuit discovery
runtime ablation verification
tag promotion at composition time
substrate verification
frontier claim promotion
mathematical proof of hypercomplex Hopfield stability
mathematical proof of zero-divisor proximity formula
mathematical proof of Hurwitz residual formula
empirical validation of May-Wigner monitor
empirical validation of tail-integral audit
empirical validation of composition-superposition allocation
```

## 13. Next phases

```text
Phase 3: categorical foundations and composition discipline
Phase 4: trust-surface example using the merged Tier 2 binding
Phase 5: schema lane for lawful-learning trust-surface artifacts
Phase 6: checker for M/T/S/E/G tag discipline and promotion prevention
Phase 7: research capture expansion
Phase 8: cross-repo registration
Phase 9: runtime integration once evidence infrastructure exists
```

Phase 2 is complete when this canonical framework document is merged and the trust-surface validation lane remains green.
