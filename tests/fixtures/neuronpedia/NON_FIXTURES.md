# Neuronpedia Non-Fixtures

Status: rejection-side audit surface for the Neuronpedia v0.1 schema tranche.

This file records fixture candidates that were deliberately not added to `tests/fixtures/neuronpedia/` because they belong to a different validation layer or require runtime authority not present in JSON Schema.

## Why this exists

A fixture suite should document both:

- what is tested; and
- what is deliberately not tested at this layer.

Without this file, reviewers may infer that omitted cases were forgotten rather than intentionally scoped out.

## Current Layer 1 scope

Layer 1 is JSON Schema validation for Neuronpedia schema bumps. It can validate:

- required fields;
- primitive types;
- enum membership;
- `additionalProperties: false` shape constraints;
- schema-local non-claims;
- schema-local decomposition metadata requirements.

Layer 1 cannot validate:

- live source retrieval;
- content-hash match against retrieved bytes;
- verified-source registry membership;
- append-only lock-chain continuity;
- graph-cycle absence across multiple lock records;
- actual correspondence between declared `decomposition_type` and provider artifact contents.

## Deliberately omitted candidates

### `artifact-source-lock.references-unverified-source.invalid.synthetic.json`

Decision: not added.

Reason: `ArtifactSourceLock v0.1` does not carry a schema-level `verification_status` field. Source verification is a runtime concern, not a JSON Schema concern. Adding this as a Layer 1 negative fixture would misrepresent the guarantee: JSON Schema cannot know whether the referenced source is verified by an external authority.

Tracking issue:

- SocioProphet/superconscious#36 — runtime verified-source check

### `artifact-source-lock.circular-reference.invalid.synthetic.json`

Decision: not added.

Reason: `ArtifactSourceLock v0.1` currently validates one lock object at a time. It does not define a graph-walkable lock-chain relation, parent-lock relation, or multi-record cycle semantics. Cycle detection belongs to a Layer 2 runtime or graph validator once lock-chain relations are introduced.

Tracking issue:

- SocioProphet/superconscious#35 — runtime lock-chain consistency

### `artifact-source-lock.content-hash-mismatch.invalid.synthetic.json`

Decision: not added.

Reason: JSON Schema can validate that `source_hash` has the shape `sha256:<64 hex chars>`. It cannot retrieve artifact bytes and prove that the declared hash matches the content. This belongs to runtime verification.

Tracking issue:

- SocioProphet/superconscious#36 — runtime verified-source check

### `artifact-source-lock.references-nonexistent-artifact.invalid.synthetic.json`

Decision: not added.

Reason: `ArtifactSourceLock v0.1` does not currently contain a schema-level artifact registry or resolvable artifact reference field. A dangling-reference check would be a graph/runtime check. It should not be represented as a Layer 1 schema negative until the schema defines the reference relation it can reject.

Tracking issue:

- SocioProphet/superconscious#35 — runtime lock-chain consistency, if implemented as graph relation validation

## SEM-K parallel

This split mirrors the sidecar-authority discipline used elsewhere:

- public artifact structure can signal meaning;
- signed or otherwise authorized verification governs execution;
- schema shape alone does not grant runtime authority.

For this Neuronpedia tranche, JSON Schema fixtures test structural commitments. Runtime/source verification remains Layer 2 and must not be implied by Layer 1 fixture names.

## Rule

Do not add a negative fixture to this subtree unless the schema can actually reject it at Layer 1 for the named reason.

If the failure requires runtime state, external lookup, graph traversal, signed authority, or content retrieval, open or reference a Layer 2 tracking issue instead.
