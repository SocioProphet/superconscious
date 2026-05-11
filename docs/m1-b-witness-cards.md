# M1B Witness Cards

## Status

M1B turns feature selection into auditable witness cards.

A witness card is generated per candidate feature. It is not only a row in a filter table; it is a certificate-ready object that accumulates evidence across contexts, activation probes, preliminary causal probes, cross-width matching, patchability, and family classification.

## Schema

Canonical schema:

```text
schemas/m1/witness-card.v1.json
```

Each card declares:

- parent M1A fragment;
- controller-spec reference;
- feature identity;
- six witnesses;
- promotion status;
- ledger entry.

## Staged lifecycle

### Stage 1: candidate pool

Only Witness 1 is populated.

Witness 1:

```text
top_contexts
```

This records top-activating contexts, keyword scores, analyst description, and redacted sample contexts.

Descriptions and labels are weak evidence. Top contexts are the primary evidence.

### Stage 2: contrastive activation

Witness 2 is populated.

Witness 2:

```text
contrastive_activation
```

This compares feature activation on benign and refusal/safety-pressure prompt sets, including activation ratio and bootstrap interval.

### Stage 3: preliminary causal probe

Witness 3 is populated.

Witness 3:

```text
preliminary_causal
```

This records a small ablation or steering probe before the full M1C causal triad.

### Stage 4: cross-width equivalence

Witness 4 is populated.

Witness 4:

```text
cross_width_equivalence
```

For M1B v1, cross-width comparison is restricted to the public 9B-IT residual release:

```text
primary: google/gemma-scope-9b-it-res/layer_20/width_131k/average_l0_81
witness: google/gemma-scope-9b-it-res/layer_20/width_16k/average_l0_91
```

The original 2-of-4 robustness idea is deferred to M3 because 65k and 1M widths are not available in the 9B-IT residual release. Using PT widths in M1B would introduce a model-regime shift and weaken the witness.

M1B v1 selection rule: the 16k witness match must pass the declared cosine threshold.

### Stage 5: patchability

Witness 5 is populated.

Witness 5:

```text
patchability_profile
```

This records whether the feature survives controlled prefix/suffix perturbations of its top contexts.

### Final classification

Witness 6 is populated.

Witness 6:

```text
family_classification
```

The analyst classifies the feature as harm-detection, refuse-and-redirect, correct-answer, task-completion, policy-meta, off-target, or ambiguous.

## Promotion rule

Rule version:

```text
m1b-selection-rule.v1
```

A candidate is promoted to M1C if:

1. Witness 1 and Witness 6 agree: top-context interpretation matches family classification.
2. Contrastive activation ratio is at least 5x.
3. Preliminary ablation direction is correct for the declared family.
4. Cross-width witness match passes threshold against the 16k layer-20 witness SAE.
5. Patchability is not pathologically brittle.

A rejected card is still useful. Rejected cards preserve the negative evidence and can become controls.

## Certificate fragment

M1B will later aggregate witness cards into:

```text
outputs/m1/certificates/m1b-witness-cards.json
```

That aggregate fragment should include:

- parent M1A fragment id;
- controller spec id;
- all witness-card hashes;
- promoted candidate list;
- rejected candidate list;
- selection-rule version;
- ledger event.

## Runtime boundary

This schema can be landed before runtime access. Runtime execution is still required to populate Witnesses 2-5.

Pre-M1B sanity check remains the first runtime gate. If no steering effect moves under the locked source target, M1B execution is suspended and the source lock is revisited.
