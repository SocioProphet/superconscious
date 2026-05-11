# M1 Data Directory

This directory holds local, non-authoritative data inputs for M1 of the Implementability Steering Pilot.

Large generated outputs, activation caches, model weights, SAE parameter files, and nearest-neighbor indexes should not be committed here.

## Expected local inputs

### `feature_contexts.jsonl`

Exported feature/context summaries for Stage 1 of feature selection.

Minimal row shape:

```json
{
  "feature_id": "layer20-width131k-feature-id",
  "description": "optional generated label",
  "top_contexts": [
    {"text": "top activating context snippet"}
  ]
}
```

Descriptions may be present, but Stage 1 should privilege top-activating examples over generated labels.

### `activation_summary.jsonl`

Optional Stage-2 summaries comparing benign and refusal/safety-pressure prompt sets.

Minimal row shape:

```json
{
  "feature_id": "layer20-width131k-feature-id",
  "harmful_mean": 1.25,
  "benign_mean": 0.08
}
```

### `causal_summary.jsonl`

Optional Stage-3 summaries from a quick ablation or steering probe.

Minimal row shape:

```json
{
  "feature_id": "layer20-width131k-feature-id",
  "compliance_delta": 0.12
}
```

## Generated outputs

Generated outputs should be written under:

```text
outputs/m1/
```

Expected generated files:

```text
outputs/m1/source-lock.json
outputs/m1/candidate_pool.jsonl
outputs/m1/behavioral_filter.jsonl
outputs/m1/causal_filter.jsonl
outputs/m1/family_classification.md
outputs/m1/selected_feature.json
```

## Safety boundary

M1 data must be evaluative, not instructional.

Do not commit operational harmful instructions, exploitable cyber procedures, weaponization instructions, biological protocols, or any dataset that functions as a capability manual. The pilot tests refusal-controller behavior and steering mechanics, not harmful task execution.
