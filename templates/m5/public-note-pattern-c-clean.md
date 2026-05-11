# Feature steering produces out-of-distribution activations

## Abstract

This note reports an out-of-distribution implementability result for refuse-and-redirect feature steering. The target behavioral effect appears only after the activation state exits the natural activation envelope under the declared metrics.

## One conceptual move

Feature steering needs an implementability test.

## Load-bearing figure

Insert the five-curve plot showing studied-feature steering exceeding the q99 natural-baseline threshold before or at `alpha_behavioral`.

## Result frame

Pattern C: the steering effect is achieved outside the natural activation envelope.

## Interpretation

The result forces revision of simple feature-steering explanations. At behavioral magnitudes, the model may not be exercising its naturally learned feature dynamics; it may be operating in an extrapolative state.

## Limitations

The claim is restricted to the source-locked model, feature, layer set, metrics, and datasets.
