# Behavioral Equivalence Classes

## Status

Deferred improvement note for the Heller Consciousness / Superconscious interpretability certificate program.

This is not an active schema change. It is a proposed M1+ v1.2 upgrade to be considered after:

1. `make certificate-ci` remains green on a clean checkout;
2. ProCybernetica Tier 1 schema CI exists;
3. the first runtime M1B pass or a runtime failure provides empirical pressure on the witness-card design.

## Thesis

SAE features-as-directions are representations, not invariants.

The invariant object should be a **behavioral equivalence class**: a cluster of features, directions, or feature-like objects that produce indistinguishable downstream behavioral effects under declared interventions and probes.

## Problem

Current interpretability practice often treats a single SAE dictionary feature as the analytic unit. That is fragile because:

- different SAE seeds can produce different decompositions;
- different widths can split or merge features;
- different L0 targets can change feature granularity;
- feature labels are not canonical;
- a single direction may represent one coordinate chart on a richer behavior.

The result is a representation-dependence problem. A claim framed as “feature F causes behavior B” may really mean “one coordinate in one dictionary participates in a behaviorally stable class.”

## Behavioral equivalence definition

Let `f_i` and `g_j` be feature-like objects from two decompositions, widths, layers, L0 settings, or seeds.

Let:

```text
E(f_i) = ablation / steering effect vector over a declared probe set
```

Two objects are behaviorally equivalent at tolerance `epsilon` if:

```text
similarity(E(f_i), E(g_j)) >= tau
```

under a declared similarity metric, usually cosine similarity over intervention-effect vectors.

The equivalence class is:

```text
BEC_k = { feature-like objects whose effect vectors agree under the declared relation }
```

## Relation to current M1B

M1B Witness 4 is a baby version of this idea.

Current M1B v1:

```text
primary: 131k / L0=81 feature
witness: 16k / L0=91 feature
method: Option C, top-k directional filter + effect-space verification
output: cross_width_agreement_score
```

That score is advisory evidence, not a hard promotion gate.

M1+ v1.2 would generalize this into:

```text
behavioral_equivalence_class_id
behavioral_equivalence_relation
class_members
class_effect_vector_summary
class_stability_score
```

## Proposed schema extension

Future field on M1B witness cards:

```json
{
  "behavioral_equivalence_class": {
    "class_id": "bec-refuse-redirect-0001",
    "relation_version": "behavioral-equivalence-relation.v1",
    "probe_set_ref": {
      "path": "data/m1/harm_pressure_mcq.jsonl",
      "content_sha256": "...",
      "item_count": 100
    },
    "similarity_metric": "cosine_over_ablation_effect_vectors",
    "threshold": 0.7,
    "members": [
      {
        "feature_id": "gemma-scope-9b-it-res-l20-w131k-l081-feature-7",
        "source": "primary",
        "effect_vector_sha256": "..."
      },
      {
        "feature_id": "gemma-scope-9b-it-res-l20-w16k-l091-feature-3",
        "source": "cross_width_witness",
        "effect_vector_sha256": "..."
      }
    ],
    "class_stability_score": 0.83,
    "status": "candidate_class"
  }
}
```

## Algorithm sketch

### Stage 1 — Candidate feature extraction

Use existing M1B Stage 1-3 pipeline to produce candidate features and preliminary effect vectors.

### Stage 2 — Cross-representation search

For each primary feature, find potential matches across available representations:

- width variation;
- L0 variation;
- nearby layers;
- future cross-seed SAE runs;
- future transcoders / crosscoders.

### Stage 3 — Effect-vector clustering

Cluster features by intervention-effect vector similarity over the declared probe set.

The cluster, not the individual feature direction, becomes the analytic primitive.

### Stage 4 — Class-level witness card

Generate an aggregate witness card keyed by `behavioral_equivalence_class_id`.

Individual feature witness cards remain as member evidence.

## Why this matters

Behavioral equivalence classes address a structural weakness in published SAE work: dictionary coordinates are not canonical.

A certificate keyed to a behavioral class is stronger than a certificate keyed only to one feature direction because it says:

```text
This behavior survives changes in representation.
```

That is closer to a Willems-style behavior invariant and closer to the Heller Consciousness doctrine.

## Interaction with ProCybernetica

A completed behavioral equivalence class can enter the Governance Fabric as stronger evidence than a single feature-direction claim.

Potential evidence receipt kind:

```text
evidence_receipt.kind = behavioral_equivalence_class_certificate
```

Governance implication:

- policy can rely more safely on behavior-level evidence;
- feature-direction evidence remains provisional;
- authority concentration can track whether class members were independently verified.

## Risks

### Probe-set dependence

Equivalence is only valid relative to the declared probe set.

A different probe set may split or merge classes.

### Compute cost

Full pairwise ablation-effect matching is expensive. Option C-style gated search should remain the default until compute expands.

### False equivalence

Two features may match on the probe set but diverge on untested contexts.

Patchability and off-target audit should remain required.

### Premature schema churn

Adding this too early would destabilize M1B before runtime validates the current design.

Therefore this remains deferred until M1B runtime evidence or Tier 1 governance schema CI justifies the bump.

## Promotion trigger

Promote this note into an active M1+ v1.2 schema proposal when at least one holds:

1. Runtime M1B finds multiple candidate features with similar causal effects.
2. Runtime M1B fails because single-feature identity is unstable across widths or layers.
3. A second SAE decomposition or cross-seed run becomes available.
4. A governance consumer requires stronger evidence than feature-direction identity.

## Non-claim boundary

This document does not claim behavioral equivalence classes have been computed.

It does not modify the current M1B schema.

It records a deferred upgrade path for making behavior, not representation, the interpretability primitive.
