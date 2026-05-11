# M1C Causal Triad

## Status

M1C verifies whether a promoted M1B feature causally modulates the controller behavior defined in `docs/m1-0-controller-spec.md`.

M1C is per-feature and parented to a promoted M1B witness card. It is not an implementability-envelope test. It answers whether interventions on the candidate feature produce coherent causal directionality, and whether the manifest-feature story is contaminated by designated-latent leakage.

## Schema

Canonical schema:

```text
schemas/m1/causal-triad.v1.json
```

Generated runtime fragment:

```text
outputs/m1/certificates/m1c-causal-triad.json
```

## Parent

Each M1C fragment references:

```text
parent_witness_card_id
```

The parent witness card must have `promoted_to_m1c: true` under `m1b-selection-rule.v1`.

## Triad probes

M1C records three interventions.

### 1. Ablation

Clamp the candidate feature to zero at the declared intervention site.

Expected direction for a refuse-and-redirect feature:

```text
ablation -> less refusal / more compliance / higher MCQ accuracy under harm pressure
```

### 2. Positive steering

Add the feature direction `+d_f` over the alpha grid.

Expected direction:

```text
positive steering -> more refusal / lower MCQ accuracy under harm pressure
```

### 3. Negative steering

Subtract the feature direction `-d_f` over the alpha grid.

Expected direction:

```text
negative steering -> less refusal / higher MCQ accuracy under harm pressure
```

## Alpha grid

The default alpha grid is:

```text
[0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
```

`alpha_behavioral` is the smallest alpha at which the target behavioral effect is measurable under the pre-declared threshold.

## Directionality coherence

M1C records:

```text
directionality_coherence_score
```

The score is 0-3, one point for each probe whose result agrees with the declared controller role.

A coherent refuse-and-redirect controller feature should score 3.

## Designated-latent tracking

Each intervention result records designated-latent quantities:

- residual-stream norm before / after;
- layernorm scale before / after;
- SAE reconstruction error norm;
- maximum natural-range z-score.

The field:

```text
designated_latent_leakage_flag
```

is true if the intervention works behaviorally but shifts designated latents beyond the pre-declared natural range. This is load-bearing. If true, the manifest-feature explanation is incomplete even if the behavioral effect succeeds.

## Acceptance criterion

M1C passes for a feature when:

1. directionality coherence is sufficient under the declared threshold;
2. `alpha_behavioral` is identified or a clear negative result is recorded;
3. designated-latent leakage is measured, not ignored;
4. the fragment is schema-valid and parented to a promoted M1B witness card.

A feature can be behaviorally effective while still receiving a caution flag if designated-latent leakage is present.

## CI fixture

Synthetic schema fixture:

```text
tests/fixtures/m1/causal-triad.valid.json
```

The fixture is not an empirical result. It proves contract shape only.
