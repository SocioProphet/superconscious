# M2 Activation Cache

## Status

The M2 activation-cache fragment records the activation cache that the implementability envelope test will use.

In the funding-constrained lane, this fragment can be validated on synthetic fixtures. Runtime execution remains pending until model weights, SAE parameters, and compute are available.

## Schema

```text
schemas/m2/activation-cache.v1.json
```

## Runtime role

The cache records residual-stream activations at the declared layer and position classes for the declared natural input mixture.

The cache does not itself classify implementability. It is the parent artifact for the natural-manifold baseline.

## Execution status

A fixture with `execution_status: synthetic_fixture` proves only schema and composition shape.

A runtime cache must use `runtime_executed` or `runtime_partial` and must hash the activation tensor and metadata JSONL.
