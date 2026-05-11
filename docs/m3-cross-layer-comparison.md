# M3 Cross-Layer Comparison

## Status

M3 tests whether an M2 implementability finding is layer-specific or robust across a small layer set.

The doctrine lane is CI-valid on synthetic fixtures. Runtime execution is pending compute and model/SAE access.

## Schema

```text
schemas/m3/cross-layer-comparison.v1.json
```

## Layer set

The default layer set is:

```text
9, 20, 31
```

Layer 20 is the primary M2 layer. Layers 9 and 31 are early and late witnesses. The goal is not exhaustive coverage; it is a bounded robustness probe.

## What M3 asks

M3 asks whether the same controller-relevant behavior appears with consistent character across depth:

- same feature family;
- same or similar Pattern A/B/C implementability classification;
- compatible `alpha_behavioral` scale;
- explainable divergence if one layer differs.

## Synthetic fixture

```text
tests/fixtures/m3/cross-layer-comparison.synthetic.json
```

The synthetic fixture deliberately uses a mixed-pattern result so the doctrine handles non-clean outcomes.
