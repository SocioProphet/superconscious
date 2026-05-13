# Generalized Interpretability Harness Architecture

Status: v0.1 contract tranche  
Owner: `SocioProphet/superconscious`  
Scope: certificate orchestration, provider-boundary declaration, source locking, intervention specification, fixture-level validation  
Non-scope: production runtime, canonical schema ownership, model training authority, provider policy authority, public claim admission

## Decision

Superconscious generalizes the current Gemma / Gemma Scope steering pilot into a provider-agnostic interpretability harness.

The harness treats interpretability work as a chain of governed artifacts rather than a single model experiment. A model artifact, SAE artifact, feature, explanation, activation set, steering intervention, causal triad, attribution graph, off-target audit, manifold baseline, implementability curve, robustness certificate, benchmark result, or public note is not authoritative by itself. Each object must carry source identity, evidence, replay class, authority scope, non-claims, and downstream promotion status.

## Why this belongs here

Superconscious owns the visible cognition and certificate loop. It can coordinate interpretability artifacts, evidence summaries, benchmark assertions, replay plans, and policy handoffs without becoming the model lab or the constitutional authority.

The authority split remains plane-based, not layer-based:

- `superconscious`: certificate orchestration, local deterministic fixtures, operator-facing trace semantics;
- `ProCybernetica`: governance law, evidence receipts, authority scopes, composition certificates, promotion and public-claim discipline;
- `sociosphere`: workspace topology, canonical ownership map, cross-repo rollout and governed hypergraph projection;
- `SourceOS-Linux/sourceos-spec`: eventual canonical schemas after stabilization;
- `agentplane`: runtime execution, evidence bundles, receipts, replay;
- `model-governance-ledger`: model lineage, eval reports, drift, consent, model promotion;
- `policy-fabric` / Guardrail Fabric: admission decisions and effectful-action gating;
- `ontogenesis`: ontology, JSON-LD, SHACL, stable vocabulary for features, circuits, claims, and evidence.

## Corrected pilot framing

The current white-box source lock is Gemma, not Gemini:

```text
model: google/gemma-2-9b-it
sae:   google/gemma-scope-9b-it-res
layer: 20
width: 131k
L0:    average_l0_81
```

Gemini-style hosted API access may be represented by this harness, but unless the provider exposes hidden activations or SAE features, it is a black-box provider binding. A black-box binding may support output benchmarking and prompt-only comparisons. It may not claim SAE feature activations, residual-stream access, activation patching, or implementability envelopes over hidden states.

## Harness object model

| Object | Purpose |
| --- | --- |
| `ProviderBinding` | Declares whether a model/provider is white-box, gray-box, black-box, or registry-only, and which observables/interventions are available. |
| `ArtifactSourceLock` | Pins model, tokenizer, SAE, transcoder, probe, dataset, benchmark, registry, or graph artifacts to immutable refs and hashes. |
| `FeatureRegistryEntry` | Stable identity for a feature, concept, latent, probe, or registry-hosted dashboard. |
| `InterventionSpec` | Declares the target, intervention kind, coefficient schedule, position policy, safety policy, and evidence requirements. |
| `BenchmarkRun` | Records task hash, assertions, evaluator class, replay class, and evidence refs. |
| `AttributionGraph` | Edge-level causal structure with manifest and latent digest separation. |
| `PublicInterpretabilityNote` | Public-facing explanation bound to non-claims, evidence refs, and promotion state. |

## Harness flow

```text
ProviderBinding
  -> ArtifactSourceLock
  -> FeatureSearch / FeatureRegistryEntry
  -> WitnessCard
  -> CausalTriad
  -> AttributionGraph
  -> OffTargetAudit
  -> ImplementabilityEnvelope
  -> RobustnessCertificate
  -> BenchmarkRun
  -> GovernanceComposition
  -> PublicInterpretabilityNote
```

The flow preserves the current M0-M5 certificate spine while making it provider-agnostic.

## Fragment composition discipline

A full interpretability release is a Tier 2-style flat composition until recursive composition is deliberately specified elsewhere. The initial fragment set is:

1. `ModelArtifact`
2. `SAEArtifact`
3. `FeatureArtifact`
4. `FeatureExplanation`
5. `FeatureActivationSet`
6. `SteeringIntervention`
7. `CausalTriad`
8. `AttributionGraph`
9. `OffTargetAudit`
10. `ManifoldBaseline`
11. `ImplementabilityCurve`
12. `RobustnessCertificate`
13. `BenchmarkResult`
14. `PublicInterpretabilityNote`

Each fragment needs a digest, source lock or provenance reference where applicable, authority declaration, replay class, non-claims, and evidence receipt reference before it can support a composed public claim.

## Provider classes

### White-box provider

A white-box provider exposes enough internals to support hidden-state, residual-stream, SAE, transcoder, attribution, or activation-patching evidence.

Examples:

- local Hugging Face model with hidden-state access;
- local model with Gemma Scope SAEs;
- local transformer runtime with activation cache and intervention hooks.

### Gray-box provider

A gray-box provider exposes limited structured observables such as logits, token probabilities, tool traces, or provider-side eval traces, but not enough for SAE implementability claims.

### Black-box provider

A black-box provider exposes outputs and prompt-level controls only. It may support behavior benchmarks, prompt-only interventions, refusal-rate measurements, and provider-route evidence. It does not support claims over internal feature directions.

### Registry-only provider

A registry-only provider exposes interpretability artifacts such as feature dashboards, registry entries, public explanations, or public circuit graphs. It can supply evidence refs, but cannot by itself prove runtime behavior unless paired with replayable model execution.

## Constitutional rule

The harness must fail closed when access mode and claim type disagree.

Invalid examples:

- black-box provider claims hidden states;
- hosted output-only model claims SAE feature activation;
- feature steering claim lacks an SAE/transcoder/probe source lock;
- public note lacks non-claims;
- attribution graph lacks replay state;
- implementability claim lacks activation-cache and manifold-baseline evidence;
- runtime steering occurs without policy admission and off-target audit.

## Runtime boundary

This tranche is schema, fixture, and semantic-check only.

It does not claim:

- production white-box runtime;
- provider API integration;
- model download or weight verification;
- live steering execution;
- public claim promotion;
- runtime governance composition;
- canonical schema finality.

## Next implementation steps

1. Stabilize the provider-binding, artifact-source-lock, feature-registry-entry, and intervention-spec schemas.
2. Add cross-file bundle validation linking providers, source locks, features, and interventions.
3. Promote stable schema terms to `SourceOS-Linux/sourceos-spec` or the appropriate standards repo after review.
4. Mirror governance composition in `SocioProphet/ProCybernetica`.
5. Register the estate-level governed interpretability use case in `SocioProphet/sociosphere`.
