# Interpretability Harness Moat Claim

Status: draft v0.1  
Owner: `SocioProphet/superconscious`  
Scope: doctrine boundary for the generalized interpretability harness and Neuronpedia-adjacent evidence consumption  
Non-scope: production runtime, provider API integration, model download, live steering execution, or public claim promotion

## Claim

The defensible moat is not a single Neuronpedia release, a single feature dashboard, or a single steering demo.

The moat is the governed composition layer around interpretability evidence:

```text
provider boundary
+ artifact source lock
+ feature registry identity
+ intervention specification
+ fragment-level evidence
+ non-claim discipline
+ negative fixture coverage
+ composition binding
+ promotion gate
```

This is the part a one-off registry release cannot provide by itself.

## Why Neuronpedia is necessary but insufficient

Neuronpedia-style registries are valuable because they expose feature identities, dashboards, explanations, and model/SAE-specific interpretability artifacts.

They do not, by themselves, prove that a downstream system:

1. has the same model, tokenizer, SAE, transcoder, probe, dataset, or activation cache;
2. has a white-box access mode rather than an output-only hosted-provider path;
3. can reproduce the hidden-state or SAE activation being cited;
4. can safely execute the proposed intervention;
5. has an off-target audit for the intervention;
6. has governance evidence for public claims;
7. preserves non-claims and claim boundaries;
8. separates registry evidence from runtime execution evidence.

The harness therefore consumes Neuronpedia as an upstream evidence source, not as a substitute for local governance.

## The harness advantage

The harness makes interpretability artifacts composable under governance.

A public feature page may answer:

```text
What feature did someone observe?
```

The harness must answer:

```text
Which provider boundary allowed that observation?
Which artifact was source-locked?
Which feature identity was consumed?
Which intervention was specified?
Which fragments were bound?
Which evidence is opaque versus replayable?
Which non-claims block overstatement?
Which checker rejects the unsafe variant?
Which gate would be required before public promotion?
```

That is the operational moat.

## Fourteen-fragment release boundary

A composed interpretability release is bounded as a 14-fragment bundle:

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

The first binding is doctrine-only. It uses opaque `sha256:` references and explicitly refuses runtime receipt lookup, timestamp authenticity, monitor attestation, live provider access, feature activation claims, steering execution, public claim promotion, and Neuronpedia release substitution.

## Moat as negative capability

The strongest signal is not what the harness claims. The strongest signal is what it refuses to claim.

The harness must fail closed when:

- a black-box provider claims hidden-state access;
- a registry-only artifact claims runtime behavior;
- feature steering lacks a model/SAE/probe source lock;
- an intervention lacks off-target audit obligations;
- a public note lacks non-claims;
- a Neuronpedia artifact is treated as a production release certificate;
- a composed release tries to carry live runtime fields through a doctrine-only binding.

This is how the harness converts interpretability from a demo surface into a governed evidence surface.

## Ownership boundary

`superconscious` owns the visible cognition/certificate loop and repo-local doctrine fixtures.

It does not own all canonical schemas forever. Stable vocabulary should move outward only after the local harness has exercised it:

- `ProCybernetica`: governance law, authority, non-claims, promotion doctrine;
- `sociosphere`: estate topology, operator graph, rollout map;
- `policy-fabric`: admission and cancellation policy;
- `agentplane`: runtime execution evidence and replay artifacts;
- `SourceOS-Linux/sourceos-spec`: canonical substrate schemas once stable;
- `ontogenesis`: RDF/JSON-LD/SHACL vocabulary after terms settle.

## Non-claims

This document does not claim that the runtime harness exists.

This document does not claim production white-box execution.

This document does not claim access to provider internals for hosted black-box models.

This document does not claim Neuronpedia artifacts are insufficient as research artifacts.

This document does not claim any feature is safe, causal, or deployable without downstream evidence.

This document does not claim public interpretability notes may be promoted without governance review.

## Implementation hook

The corresponding pre-stage binding lives in:

```text
schemas/composition/interpretability-harness-tier2-binding.v1.json
tests/fixtures/composition/interpretability-harness-tier2-binding.synthetic.json
tests/fixtures/composition/interpretability-harness-tier2-binding.runtime-field.invalid.synthetic.json
scripts/check-interpretability-harness-tier2-binding.py
```

The first implementation target is structural refusal: the binding must accept only opaque 14-fragment composition references and reject runtime-bearing fields.
