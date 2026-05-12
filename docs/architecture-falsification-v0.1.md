# SocioProphet Architecture Falsification Document v0.1

**Doctrine status:** v0.1 draft, May 12, 2026. Integrated into `superconscious/docs/` as the Superconscious-facing falsification doctrine for the artifact / evidence / gate architecture.

## Purpose

This document names the observations that would force structural revision of the three-layer architecture:

```text
artifact layer -> evidence layer -> gate layer -> runtime ecosystem
```

The architecture composes by reference: `graphbrain-contract` NetworkArtifacts flow up to the certificate program; certificates flow up to TritFabric Atlas; Atlas decides promotion; downstream runtime components must respect the gate decision. This remains structurally sound only while each layer is expressive enough to satisfy the layer above it.

The guarded failure mode is not imperfect gate prediction and not unsafe self-optimization. The guarded failure mode is stricter: one layer cannot, in principle, produce what the next layer needs to decide. That is structural inadequacy, and this document names it in advance.

## Layer boundary map

| Boundary | Producer | Consumer | Question |
|---|---|---|---|
| Artifact -> Evidence | `graphbrain-contract` artifacts | Certificate program M0/M1/M1.5/M2/M3/M5 | Can evidence represent the artifact's real provenance, structure, and causal behavior? |
| Evidence -> Gate | Certificate verdicts and invariants | TritFabric Atlas / Gatekeeper / SHACL | Can the gate consume evidence at the same semantic resolution the certificates produce? |
| Gate -> Runtime | Atlas promotion verdicts | memory-mesh, new-hope, slash-topics, sherlock-search, holmes, graphbrain-contract | Do downstream systems treat gate decisions as load-bearing authority? |
| Methodology | This document | Architecture governance | Are the falsification claims themselves empirically testable and kept current? |

## Boundary 1: Artifact layer -> Evidence layer

`graphbrain-contract` emits `NetworkArtifact`, `ArchitectureProbe`, `LayerSurgeryPlan`, `RetrainJob`, and `ModelEvaluationReport`. The certificate program consumes these through M0, M1A-D, M1.5, M2, M3, and M5 certificates.

### Observable F1.1: Behavioral equivalence classes do not cluster

**Statement.** If activation-space behavioral equivalence classes, grouped by causal-effect cosine similarity rather than by SAE feature identity, do not cluster cleanly under any reasonable metric, then the manifest/latent split for M1.5 attribution graphs is fundamentally mis-cut. The failure condition is that within-class effect similarity is statistically indistinguishable from between-class similarity at `p < 0.05` across at least three independent random seeds and at least five behavior types: refusal, sycophancy, deception, jailbreak susceptibility, and instruction-following.

**Meaning.** The manifest claim `this edge mediates behavior X with weight W` assumes that `behavior X` is a coherent equivalence class. If activation-space behaviors do not cluster, the manifest digest hashes a category with no causal reality.

**Forced revision.** Reformulate the M1.5 `manifest` object. Either claims become more fine-grained than behavior labels, for example token-level effects, or the manifest/latent split gains an intermediate `behavioral-binding` layer. `manifest_role: claim | latent_state` becomes `claim | behavioral_binding | latent_state`.

**Fixture test.** Run causal-effect clustering on synthetic and then real Gemma-2-9B-IT activation distributions across the five behavior types using k-means, DBSCAN, multiple seeds, and multiple distance metrics. Compare within-cluster and between-cluster effect similarity.

### Observable F1.2: Artifact identifiers do not survive layer surgery

**Statement.** If a `LayerSurgeryPlan` applied to a `NetworkArtifact` produces a new artifact whose `content_sha256` changes the M0/M1A source-lock binding in ways the certificate program cannot express, then the artifact-to-evidence boundary has a structural gap.

**Meaning.** Layer surgery is supposed to be governed transformation. The parent artifact has known provenance, the surgery is auditable, and the output artifact should have derived provenance referencing both the parent artifact and the surgical operation.

**Forced revision.** Extend M0 with `parent_artifact_ref` and `derivation_operation_ref`. Add `derived_provenance_with_audit` to `provenance_completeness.interpretation`. Extend temporal constraints so parent artifact commitment time precedes derivation operation commitment time.

**Fixture test.** Apply a synthetic `LayerSurgeryPlan` to a fixture Gemma Scope SAE artifact and attempt to construct an M0 certificate for the result. If lineage cannot be represented without ambiguity, F1.2 is realized.

### Observable F1.3: Multi-encoder artifacts do not decompose cleanly

**Statement.** If a single `NetworkArtifact` contains multiple encoder families, such as a neural backbone with an LSI-based topic encoder, and the certificate program cannot produce separate M1A source-locks for each encoder while preserving the composite behavioral certificate, then ProRepresentation's encoder-pluggability claim is structurally unsupported.

**Meaning.** ProRepresentation claims that LSI/LSA/LDA and neural encoders instantiate the same `x -> Encoder -> r -> Head` contract. If multi-encoder artifacts cannot certify by composing per-encoder certificates, the unified contract is insufficient.

**Forced revision.** Add inter-encoder interaction fields to the ProRepresentation encoder contract, add `multi_encoder_decomposition` to the M1 composite implementability certificate, or restrict the doctrine to single-encoder artifacts.

**Fixture test.** Create a fixture `NetworkArtifact` with a Gemma residual stream feeding both a sparse autoencoder and an LSI topic encoder. Attempt to specify a certificate chain without ambiguity or duplicated authority.

## Boundary 2: Evidence layer -> Gate layer

The certificate program produces M0/M1/M1.5/M2/M3/M5 evidence. TritFabric Atlas consumes it through SHACL validation, ONNX round-trip cosine, eval deltas, and fail-closed gate policy.

### Observable F2.1: Certificate verdict resolution exceeds Atlas's decision vocabulary

**Statement.** If certificate verdicts such as `admitted`, `partial`, `rejected`, and `undecided`, plus M2 Pattern A/B/C subdivisions, require Atlas to take a third action such as canary rollout with monitoring, but Atlas only exposes binary admit/deny at the Kubernetes API server, then the verdict vocabulary exceeds gate expressiveness.

**Meaning.** Either certificates produce too much resolution and information is lost before Atlas, or Atlas produces too little resolution and cannot act on certificate semantics.

**Forced revision.** Atlas promotion decisions need at least four explicit states: `admit`, `deny`, `admit_with_canary`, and `admit_with_curator_review`. Argo Rollouts can support the canary infrastructure; the integration gap is the Atlas/Gatekeeper decision protocol.

**Fixture test.** Walk a synthetic Pattern B certificate with `verdict.status: partial` and `verdict.followup_required: canary_with_off_target_monitoring` through the Gatekeeper rule. If Rego cannot distinguish it from `admitted`, F2.1 is realized.

### Observable F2.2: SHACL shapes cannot express constitutional invariants

**Statement.** If certificate constitutional invariants cannot be expressed as fail-closed SHACL constraints at Atlas admission time, then validation-gate composition is incomplete.

The four initial invariants are:

1. model commitment precedes eval-spec commitment;
2. manifest digest differs from full digest by construction;
3. authority concentration index is computed across all fragments;
4. off-target audit precedence subordinates steering success.

**Meaning.** Admission-time validation must not be weaker than design-time schema validation. If key invariants only exist in JSON schema or prose, a malformed certificate can reach the gate.

**Forced revision.** Reformulate invariants into SHACL-expressible forms where possible. Where SHACL is insufficient, add an explicit non-SHACL Rego validation stage rather than pretending the shape layer is complete.

**Fixture test.** Translate each invariant to SHACL. The timestamp relation may be expressible with `sh:lessThan`; authority concentration likely requires SHACL-AF or SPARQL constraints.

### Observable F2.3: Eval delta mapping loses Pattern A/B/C resolution

**Statement.** If Atlas's scalar eval delta can map Pattern B and Pattern C to the same acceptable threshold result, then the gate consumes evidence at lower semantic resolution than the evidence layer produces.

**Meaning.** Pattern C critical failure must fail closed. Pattern B partial should canary. If both can appear as `eval delta within threshold`, the gate is wrong even if it is fail-closed in form.

**Forced revision.** Replace scalar eval delta with a vector-valued structure, at minimum `(on_target_effect, off_target_damage)`, each with separate fail-closed thresholds. Make the M2 Pattern A/B/C to vector mapping part of the certificate-to-Atlas integration schema.

**Fixture test.** Construct Pattern A, Pattern B, and Pattern C synthetic M2 certificates. Map them to the current Atlas eval delta format. If B and C collapse under any reasonable threshold, F2.3 is realized.

## Boundary 3: Gate layer -> Runtime ecosystem

Atlas decides promotion. The runtime ecosystem must treat that decision as authoritative unless an explicit, evidenced override is present.

### Observable F3.1: Downstream components silently override Atlas decisions

**Statement.** If memory-mesh, new-hope, slash-topics, sherlock-search, holmes, or graphbrain-contract can ingest or serve a model artifact whose Atlas verdict is `rejected` or `undecided` without explicit per-component override authority and without recording the override as evidence, then the gate layer is decorative.

**Meaning.** If runtime recall, search, membrane decisions, or agent-facing services can use rejected artifacts, the architecture's opt-in and promotion discipline is bypassed.

**Forced revision.** Each downstream component needs a `promotion_verdict_check` before serving model-derived outputs. The verdict format becomes part of the wire protocol, likely through TriTRPC or the relevant typed RPC contract. Components that cannot perform the check are restricted to non-governed use cases or require their own explicit opt-in gate.

**Fixture test.** Audit recall/search/membrane APIs for verdict checks. Add negative fixtures proving `rejected` and `undecided` artifacts are denied unless an evidenced override is present.

### Observable F3.2: Authority concentration accumulates around a single signer

**Statement.** If the computed authority concentration index across certificate fragments in production exceeds `0.8` for the most-active signing authority, then the multi-party verification structure has collapsed to single-party verification with extra steps.

**Meaning.** A single signing key or team should not be able to dominate the verification chain without the architecture admitting that concentration as a limitation.

**Forced revision.** Either distribute signing authority by certificate kind, declare the system single-party verified as a limitation, or make composites invalid when more than `0.8` of fragments share a signing authority. The third option is the strongest structural fix.

**Fixture test.** Compute a certificate authority graph snapshot across the SocioProphet ecosystem. Fail when the max signer fraction exceeds `0.8`, unless the certificate is explicitly marked as single-party-limited.

## Meta-observables

### Observable M.1: The three-layer decomposition is the wrong cut

If at least three of F1.1, F1.2, F1.3, F2.1, F2.2, and F2.3 are realized within twelve months of architecture deployment, the artifact/evidence/gate decomposition is probably mis-cut. The architecture document must be rewritten, likely with a separate transformation layer or policy layer.

### Observable M.2: Falsification observables are not empirically testable

If the six layer-boundary observables cannot be tested in synthetic-fixture form and require production runtime scale, the falsification methodology is not useful pre-deployment. Each observable must carry a `fixture-testable`, `partial-runtime`, or `runtime-only` annotation.

### Observable M.3: The falsification document itself ossifies

If this document remains structurally unchanged for more than eighteen months while the architecture evolves, it is wrong by omission. Quarterly review is required. If three consecutive quarterly reviews produce no changes, the review process itself must be revised.

## Summary table

| Observable | Boundary | Forces revision of | Testable now? |
|---|---|---|---|
| F1.1 | Artifact -> Evidence | M1.5 manifest/latent trichotomy | Yes, with synthetic activations |
| F1.2 | Artifact -> Evidence | M0 derivation lineage commitments | Yes, with synthetic LayerSurgeryPlan |
| F1.3 | Artifact -> Evidence | ProRepresentation multi-encoder composition | Yes, with synthetic multi-encoder fixture |
| F2.1 | Evidence -> Gate | Atlas promotion decision vocabulary | Yes, with synthetic Pattern B certificate |
| F2.2 | Evidence -> Gate | SHACL companion shapes per invariant | Yes, by attempting SHACL translation |
| F2.3 | Evidence -> Gate | Atlas eval delta format | Yes, with three synthetic M2 certificates |
| F3.1 | Gate -> Runtime | Per-component promotion verdict checks | Partially; runtime audit needed |
| F3.2 | Gate -> Runtime | Authority concentration hard limit | Yes, with current authority graph |
| M.1 | Methodology | Three-layer decomposition | After 12 months of operation |
| M.2 | Methodology | Fixture-testability annotations | Yes, by review |
| M.3 | Methodology | Quarterly review cadence | Yes, by establishing review |

## Superconscious implementation posture

Superconscious does not become the authority for these schemas or gate decisions. Its implementation responsibility is to keep the falsification doctrine visible in the governed cognition loop and to emit safe operational traces that can reference:

- the active architecture-falsification doctrine revision;
- which observables a proposed change resolves, worsens, or newly introduces;
- which fixture tests are required before promotion;
- whether a runtime adapter is allowed to serve a model-derived artifact under the current Atlas verdict.

## Cadence and ownership

Review quarterly. At each review:

1. re-evaluate each observable as relevant, realized, resolved, or retired;
2. add observables when new layer boundaries emerge;
3. run fixture-testable observables that have not been tested recently;
4. update testability annotations as runtime opens;
5. compute the M.1 score: realized structural-boundary observables in the last twelve months.

The same authority that signs M1 composite certificates should sign quarterly revisions of this document. That couples falsification discipline to production discipline.
