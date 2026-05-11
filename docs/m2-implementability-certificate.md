# M2 Implementability Certificate

## Status

The M2 Implementability Certificate composes the M2 activation cache, manifold baseline, and implementability curve fragments with the M1 certificate.

It is the first composite certificate that can claim a Pattern A/B/C implementability result, but only when `execution_status` is runtime-executed or runtime-partial with explicit limitations.

## Schema

```text
schemas/m2/implementability-certificate.v1.json
```

## Synthetic status

A synthetic M2 certificate is a funding/demo artifact. It proves the architecture composes; it does not claim a live model result.

## Runtime status

A runtime M2 certificate must bind to:

- a sealed M1 certificate;
- runtime activation cache;
- calibrated manifold baseline;
- implementability curve;
- Pattern A/B/C classification;
- explicit non-claims.

## Handoff

M2 hands off to M3 for cross-layer robustness and broader representation stability.
