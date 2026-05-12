# Quantum / Dependency Calculus Capability Tier v0.1

## Status

This is an opt-in capability tier. It is not a new constitutional invariant and must not be treated as CI-11.

The base architecture remains complete without this tier. Routine M0-M5 certificates, Pneumachinalis events, OpsHistory-style events, policy decisions, and reputation updates do not automatically invoke dependency-control calculus.

## Position

The dependency calculus sits horizontally beside the base architecture as an advanced governance substrate.

```text
Capability tier, opt-in:
  dependency-control graph
  reachability record
  observability partition
  shared dependency ancestry
  cancellation record
  adaptive feedback loop

Base architecture, default:
  Layer 0  wire/runtime substrate
  Layer 1  runtime ecosystem
  Layer 2  artifacts
  Layer 2.5 reasoning operations
  Layer 2.75 operational events
  Layer 3  evidence and certificates
  Layer 4  gates
  Layer 5  reputation
```

## Invocation rule

An artifact invokes this tier only by explicit reference. Absence of a dependency-calculus reference is not an error for ordinary artifacts.

An invoking artifact should carry an invocation object with at least:

```json
{
  "capability_tier": "quantum-dependency-substrate",
  "invocation_scope": "glass_break|planetary_governance|multi_trust_domain|high_consequence_review",
  "dependency_graph_ref": "...",
  "observability_partition_ref": "...",
  "invoked_by": "...",
  "invoked_at": "..."
}
```

## Primary use cases

Glass-break governance: emergency-grade or high-consequence decisions where ordinary review is too slow or too weak to expose dependency conflicts.

High-consequence one-shot decisions: decisions where contradictions, hidden dependencies, or cancellation effects cannot be silently absorbed.

Multi-stakeholder dependency review: cases where shared ancestry, reachability, and observability partitions are needed to prove that no stakeholder dependency is being silently overridden.

Planetary-scale governance substrate: multi-jurisdiction, multi-trust-domain, or civilizational coordination where the base architecture needs explicit dependency calculus to reason about control, observability, and propagation.

## Non-goals

This tier is not mandatory for the common case.

This tier is not a marketing substitute for certificate evidence.

This tier does not make quantum-computational claims unless a later runtime profile explicitly binds to quantum hardware or quantum-simulation primitives.

This tier does not replace M0-M5, ProCybernetica safety cases, TritFabric Atlas gates, SourceOS policy decisions, or Pneumachinalis reputation events.

## Falsification observables

Tier-specific falsification applies only to invoking artifacts.

F8.1: An artifact declares dependency-calculus invocation but lacks a resolvable dependency graph, reachability record, or observability partition.

F8.2: A replayed dependency graph changes reachability or cancellation outcome without producing a superseding review record.

F8.3: A glass-break invocation has no bounded scope, no accountable authority, or no post-hoc review path.

## Opt-in mechanics

Opt-in may occur per artifact, per tenant, per deployment, or per Stele-grade governance flow. The strongest applicable scope wins. Deployment-level enablement does not imply artifact-level invocation; artifacts must still reference the capability tier explicitly.

## Relationship to v1.1 schemas

The v1.1 base schemas do not require dependency-calculus references. That is intentional. They provide the default governance substrate. Bridge schemas may later add optional invocation fields that point to this capability tier when a use case requires it.
