# M5 Outcome Template Mapping

## Status

This document maps certified outcomes to public-note templates.

The purpose is to prevent outcome-shopping after runtime execution.

## Inputs

Template selection depends on:

- M1D off-target audit status;
- M2 Pattern A/B/C implementability classification;
- M3 robustness pattern;
- whether a viable feature was found.

## Priority order

### 1. Off-target damage overrides everything

If M1D reports a critical safety failure, use:

```text
templates/m5/public-note-off-target-damage.md
```

The off-target safety regression is the headline finding even if M2 classifies the steering intervention as in-envelope.

### 2. No viable feature

If M1B/M1C cannot produce a viable feature, use:

```text
templates/m5/public-note-no-viable-feature.md
```

### 3. Pattern A clean

If M2/M3 classify the result as in-envelope and M1D passes, use:

```text
templates/m5/public-note-pattern-a-clean.md
```

### 4. Pattern B clean

If the certified result is boundary-crossing and M1D passes, use:

```text
templates/m5/public-note-pattern-b-clean.md
```

### 5. Pattern C clean

If the certified result is out-of-distribution and M1D passes, use:

```text
templates/m5/public-note-pattern-c-clean.md
```

## Mixed M3 patterns

For mixed cross-layer outcomes, choose the template according to the most safety-relevant non-clean layer:

```text
C beats B beats A
```

If any layer is Pattern C, use Pattern C clean unless off-target damage overrides. If no layer is C but any layer is B, use Pattern B clean. If all layers are A, use Pattern A clean.

## Non-claim boundary

This mapping does not claim runtime execution. It defines publication discipline before runtime results exist.
