# Tier 2 Binding Schema Boundary

**Status:** binding-boundary clarification.  
**Applies to:** every local Tier 2 binding schema and fixture under:

```text
schemas/composition/*tier2-binding*.json
tests/fixtures/composition/*tier2-binding*.json
```

## Rule

These local binding schemas are **Layer 1 declaration-shape artifacts**. They make governance adoption explicit and machine-checkable at the shape level. They are not execution, proof, source-resolution, or certification artifacts.

## What they validate

The schemas and fixtures may validate:

```text
composition_id
composition_kind
binding_doctrine_version
opaque hash string shape
required component/reference fields
bound Tier 2 mode names
required non_claims
absence of forbidden fields
surface-specific declaration shape
```

## What they do not validate

A passing schema fixture does not claim that referenced artifacts were resolved, receipts were looked up, monitors were attested, timestamps were authenticated, evidence freshness was independently checked, mathematical claims were reviewed, or public claims were promoted.

## CI interpretation

A CI-green local Tier 2 binding fixture means only:

```text
the declaration shape is valid;
the fixture uses the required local non-claims;
local forbidden fields are rejected;
the bound mode names match the adopted ProCybernetica mode names.
```

It does not mean the underlying invariant semantics have been independently checked.

## Local schema surfaces covered

```text
schemas/composition/m1-tier2-binding.v1.json
schemas/composition/m5-tier2-binding.v1.json
schemas/composition/lawful-learning-trust-surface-tier2-binding.v1.json
schemas/composition/interpretability-harness-tier2-binding.v1.json
```

## Maintenance requirement

Any future Tier 2 binding schema added to this repository must either cite this boundary note or carry an equivalent schema-only boundary in its description and fixture non-claims.