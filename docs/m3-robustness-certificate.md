# M3 Robustness Certificate

## Status

The M3 Robustness Certificate composes the cross-layer comparison and any available transcoder/crosscoder evidence.

It does not claim cross-model generalization. It only reports robustness within the studied model/layer set.

## Schema

```text
schemas/m3/robustness-certificate.v1.json
```

## Outcome patterns

Allowed robustness patterns:

```text
consistent_in_envelope_across_layers
consistent_boundary_crossing_across_layers
consistent_ood_across_layers
mixed_pattern_across_layers
layer_specific_to_primary
no_feature_at_witness_layers
```

## Synthetic status

The default fixture uses `mixed_pattern_across_layers` to force the certificate chain to handle divergence rather than assuming a clean positive result.

## Handoff

M3 feeds M5. M5 chooses the appropriate public-note template based on the M3 robustness pattern and M1D off-target audit status.
