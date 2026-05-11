# M3 Layer Selection Rationale

## Status

M3 uses a bounded three-layer robustness set.

## Default set

```text
Layer 9  — early witness
Layer 20 — primary layer
Layer 31 — late witness
```

## Rationale

Layer 20 is the M2 source-locked target. Layers 9 and 31 bracket it without multiplying runtime cost beyond a tractable 3x expansion.

This is not a claim that these layers are canonical or exhaustive. It is a disciplined robustness probe under the funding constraint.

## Runtime boundary

Runtime M3 requires one activation-cache / manifold-baseline / implementability-curve run per layer.
