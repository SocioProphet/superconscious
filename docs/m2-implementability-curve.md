# M2 Implementability Curve

## Status

The M2 implementability-curve fragment records the five-curve steering-distance test.

It is the first M2 artifact that classifies Pattern A/B/C, but only after runtime data exists. Synthetic fixtures are contract tests only.

## Schema

```text
schemas/m2/implementability-curve.v1.json
```

## Five curves

The schema records:

- studied feature steering;
- no intervention;
- random direction;
- alternative feature steering;
- teleportation.

The load-bearing plot is generated from the same data. The certificate should be enough to regenerate the plot.

## Pattern classification

Allowed classifications:

```text
A_in_envelope
B_boundary_crossing
C_out_of_distribution
indeterminate
```

The classification is made at `alpha_behavioral` from the M1C causal triad.
