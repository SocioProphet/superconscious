# M2 Manifold Baseline

## Status

The M2 manifold-baseline fragment records conformal-style calibration for the natural activation envelope.

It uses an activation cache parent and produces per-metric, per-position natural nearest-neighbor baselines.

## Schema

```text
schemas/m2/manifold-baseline.v1.json
```

## Runtime role

Runtime execution splits the cache into reference, calibration, and test partitions. The calibration set defines q50/q90/q95/q99 thresholds for each metric and position type.

## Funding boundary

Synthetic fixtures prove schema shape only. They do not claim empirical coverage or real activation-manifold geometry.
