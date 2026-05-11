# M2 Metric Stack

## Status

This document names the metric stack used by the M2 implementability envelope.

The funding-constrained lane records metric doctrine and schema contracts. Runtime execution will populate actual distances.

## Metrics

### Layernorm Euclidean

Distance after the layernorm projection consumed by the next block.

### Cosine

Directional distance in residual-stream space.

### Readout-weighted Euclidean

Distance weighted by downstream read-in operators.

### Jacobian-weighted

Local sensitivity of downstream loss or logits to activation perturbation.

### Logit-effect

Distance between downstream logit deltas induced by candidate activations.

### Feature-coordinate

Distance after SAE encoding, used to compare raw activation geometry with sparse-feature geometry.

## Interpretation doctrine

Metric disagreement is evidence, not noise.

- Geometrically OOD but functionally in-envelope: unusual representation, possibly benign.
- Geometrically in-envelope but functionally OOD: high-priority warning.
- Feature-coordinate in-envelope but raw/functionally OOD: SAE artifact suspicion.
- All metrics OOD: strong evidence of unnatural steering regime.
