# Cairnmark-to-Stele Transition Doctrine v1

**Status:** H6 replayed doctrine; transition vocabulary only.  
**Origin branch:** `turn4-cairnmark-stele-v13`.  
**Audit disposition:** replay-after-demotion from branch reconciliation audit.  
**Scope:** Defines the Cairnmark / Stele transition vocabulary for Superconscious certificate surfaces without promoting the v1.3 schema wrappers from the origin branch.

## H6 / schema-promotion boundary

This document is retained because it contains useful promotion-state vocabulary and migration doctrine. It does not activate v1.3 schemas or change certificate validation.

This document does **not** claim:

```text
v1.3 schema family promoted
v1.3 wrappers adopted
certificate fixtures migrated
cross-field validator implemented
Stele eligibility proven
institutional memory promotion performed
ProCybernetica authority imported
SourceOS/sourceos-spec promotion completed
```

The origin branch included v1.3 transition wrapper schemas. Those schemas are intentionally held out of this replay until a separate schema-review PR reconciles namespace, validator, fixture, and authority-plane implications.

## Purpose

This doctrine defines the transition from Cairnmark candidate artifacts to Stele-grade promoted artifacts across the Superconscious certificate program.

A Cairnmark is a candidate mark: structured enough to review, cite, replay, and test, but not yet promoted into durable institutional memory.

A Stele is a promoted mark: accepted into the governed record with explicit authority, cadence, traceability, and promotion state.

## Turn 4 structural move

F4.1, F4.2, and F4.3 become structurally testable only when all relevant M-series certificates carry and validate the v1.3 additive fields:

```text
authority_layer
promotion_state
reasoning_trace_ref
cadence_classification
```

These fields are intended to let validation distinguish candidate, promoted, rejected, and superseded certificate states without relying on prose outside the artifact.

In this replay, that is a doctrine target, not an implemented validator claim.

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

`reasoning_trace_ref` may be null for migrated legacy fixtures, but new strict fixtures should provide a trace reference when the artifact is promoted, rejected, or superseded.

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

Future validators should enforce:

1. `promoted_stele` requires `authority_layer = institutional_truth`.
2. `rejected` requires non-empty `reasoning_trace_ref`.
3. `superseded` requires non-empty `reasoning_trace_ref` and a supersession or ledger reference when available.
4. A composite certificate cannot be `promoted_stele` if any required fragment is `candidate`, `rejected`, or `superseded` without an explicit override trace.

## Schema hold

The following origin-branch files are not replayed by this PR:

```text
schemas/_common/v1-3-additive-fields.json
schemas/m0/tp.v1.3.json
schemas/m0/training-provenance.v1.3.json
schemas/m1-5/attribution-graph.v1.3.json
schemas/m1/causal-triad.v1.3.json
schemas/m1/implementability-certificate.v1.3.json
schemas/m1/off-target-audit.v1.3.json
schemas/m1/source-lock.v1.3.json
schemas/m1/witness-card.v1.3.json
schemas/m2/implementability-certificate.v1.3.json
schemas/m3/robustness-certificate.v1.3.json
schemas/m5/public-note.v1.3.json
schemas/procybernetica/case.v1.3.json
```

Reason: those files are schema surfaces, not pure doctrine. They require a separate PR with validator behavior, positive/negative fixtures, source authority, and explicit claim-boundary tests.

## Non-claim

A v1.3 field set does not prove the underlying certificate claim. It makes promotion state and authority posture machine-testable only after the schema and validator layer exists.
