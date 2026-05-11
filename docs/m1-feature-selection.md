# M1 Feature Selection Protocol

## Status

This document operationalizes the feature-identification funnel for M1 of the Implementability Steering Pilot.

M1 has one purpose: identify a source-locked refusal, redirect, or safety-controller feature whose steering creates a measurable behavioral effect on an open model.

M1 does **not** claim implementability. Implementability is tested only after the behavioral steering effect is reproduced.

## Inputs

The feature-selection pipeline expects exported feature/context summaries and optional probe summaries.

### Feature/context summary JSONL

Required for Stage 1.

Each row should include a stable feature identifier plus one or more context fields:

```json
{
  "feature_id": "example-feature-id",
  "description": "optional auto-generated description",
  "top_contexts": [
    {"text": "top activating context snippet"},
    {"text": "another context snippet"}
  ]
}
```

Descriptions are allowed but are not the primary evidence. Stage 1 should privilege top-activating examples over labels.

### Activation summary JSONL

Optional for Stage 2.

Each row should summarize candidate feature activations on benign and refusal/harm-pressure prompt sets:

```json
{
  "feature_id": "example-feature-id",
  "harmful_mean": 1.25,
  "benign_mean": 0.08
}
```

The default Stage-2 keep rule is activation ratio >= 3.0.

### Causal summary JSONL

Optional for Stage 3.

Each row should summarize a quick ablation or steering probe:

```json
{
  "feature_id": "example-feature-id",
  "compliance_delta": 0.12
}
```

The default Stage-3 keep rule is causal delta >= 0.05.

## Four-stage funnel

### Stage 1: candidate pool

Pull features whose top-activating contexts contain refusal-adjacent, harm-detection, redirect, or policy-meta language.

This is a keyword pass over examples, not a trust decision based on model-generated descriptions.

Expected artifact:

```text
outputs/m1/candidate_pool.jsonl
```

### Stage 2: behavioral probe

Contrast activations on two prompt sets:

- benign / innocuous prompts;
- refusal-eliciting or safety-pressure prompts.

Keep features with high activation specificity for the refusal/safety set.

Expected artifact:

```text
outputs/m1/behavioral_filter.jsonl
```

### Stage 3: causal probe

Run a quick causal check on Stage-2 survivors.

The first pass may use ablation, negative steering, or another explicitly recorded intervention. The output is not yet the final steering sweep; it only identifies which features are worth full M1 steering.

Expected artifact:

```text
outputs/m1/causal_filter.jsonl
```

### Stage 4: family classification

Manually inspect surviving top contexts and classify features into:

- harm-detection;
- refuse-and-redirect;
- correct-answer / task-completion;
- policy-meta;
- other / ambiguous.

For the pilot, the canonical target is refuse-and-redirect. Harm-detection and policy-meta features may become controls or follow-up targets.

Expected artifacts:

```text
outputs/m1/family_classification.md
outputs/m1/selected_feature.json
```

## Script

Run Stage 1 only:

```bash
python3 src/m1/feature_selection.py \
  --features data/m1/feature_contexts.jsonl \
  --out-dir outputs/m1
```

Run Stage 1 + Stage 2:

```bash
python3 src/m1/feature_selection.py \
  --features data/m1/feature_contexts.jsonl \
  --activation-summary data/m1/activation_summary.jsonl \
  --out-dir outputs/m1
```

Run all available stages:

```bash
python3 src/m1/feature_selection.py \
  --features data/m1/feature_contexts.jsonl \
  --activation-summary data/m1/activation_summary.jsonl \
  --causal-summary data/m1/causal_summary.jsonl \
  --out-dir outputs/m1
```

## Selection rule

The default automated selection rule is:

1. prefer survivors classified as refusal, redirect, or policy-meta;
2. rank by causal delta;
3. tie-break by activation ratio;
4. emit remaining survivors as control-candidate feature ids.

This is not a substitute for manual inspection. `selected_feature.json` is a recommendation, not a final scientific claim.

## Safety boundary

The M1 dataset and feature probes must be evaluative, not instructional.

Allowed:

- high-level refusal-sensitive prompts;
- benign multiple-choice format;
- abstract safety-pressure tests;
- non-operational probes of model behavior.

Disallowed:

- procedural harmful instructions;
- actionable cyber abuse workflows;
- weapon, evasion, or biological operational details;
- datasets that would function as a capability manual.

The purpose is to measure refusal-controller behavior, not to teach harmful procedures.

## Hand-off to steering sweep

M1 proceeds to the steering sweep only after:

1. `docs/m1-source-lock.md` is satisfied;
2. `outputs/m1/source-lock.json` exists;
3. `outputs/m1/selected_feature.json` selects a candidate feature;
4. eliminated candidates are retained for controls;
5. the pilot dataset has item-level provenance and filtering notes.

The steering sweep must then identify `alpha_behavioral`: the smallest steering magnitude producing a measurable behavioral effect.
