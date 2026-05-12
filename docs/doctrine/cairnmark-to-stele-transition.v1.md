# Cairnmark-to-Stele Transition Doctrine v1

## Purpose

This doctrine defines the transition from Cairnmark candidate artifacts to Stele-grade promoted artifacts across the Superconscious certificate program.

A Cairnmark is a candidate mark: structured enough to review, cite, replay, and test, but not yet promoted into durable institutional memory.

A Stele is a promoted mark: accepted into the governed record with explicit authority, cadence, traceability, and promotion state.

## Turn 4 structural move

F4.1, F4.2, and F4.3 are no longer merely doctrinal. They become structurally testable when all M-series certificates carry the v1.3 additive fields:

```text
authority_layer
promotion_state
reasoning_trace_ref
cadence_classification
```

These fields let validation distinguish candidate, promoted, rejected, and superseded certificate states without relying on prose outside the artifact.

## Required states

`promotion_state` must be one of:

```text
candidate
promoted_stele
rejected
superseded
```

`authority_layer` must be one of:

```text
institutional_truth
grounded_schema
commonsense_prior
```

`cadence_classification` must be one of:

```text
microbeat
mesobeat
macrobeat
certificate
```

`reasoning_trace_ref` may be null for migrated legacy fixtures, but new strict fixtures must provide a trace reference when the artifact is promoted, rejected, or superseded.

## Middle-path migration policy

Existing fixtures may migrate with defaults so the historical corpus remains valid.

New fixtures should use strict mode and provide explicit v1.3 fields. Strict validation is the path for empirical falsification pressure.

Default migration values:

```text
authority_layer: grounded_schema
promotion_state: candidate
reasoning_trace_ref: null
cadence_classification: certificate
```

## Cross-field requirements

1. `promoted_stele` requires `authority_layer = institutional_truth`.
2. `rejected` requires non-empty `reasoning_trace_ref`.
3. `superseded` requires non-empty `reasoning_trace_ref` and a supersession or ledger reference when available.
4. A composite certificate cannot be `promoted_stele` if any required fragment is `candidate`, `rejected`, or `superseded` without an explicit override trace.

## Non-claim

A v1.3 field set does not prove the underlying certificate claim. It makes the promotion state and authority posture machine-testable.
