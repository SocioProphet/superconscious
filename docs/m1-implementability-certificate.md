# M1 Implementability Certificate

## Status

The M1 Implementability Certificate is the composite artifact that closes the M1 certificate chain.

It does **not** certify M2 implementability-envelope status. It certifies that a source-locked feature-steering target has passed, failed, or been blocked by the M1 chain:

```text
M1-0 controller spec
M1A source lock
M1B witness cards
M1C causal triad
M1D off-target audit
```

Only after this composite certificate is sealed does M2 begin calibrated activation-manifold testing.

## Schema

Canonical schema:

```text
schemas/m1/implementability-certificate.v1.json
```

Generated runtime fragment:

```text
outputs/m1/certificates/m1-implementability-certificate.json
```

## Inputs

The composite certificate references:

- one M1A source-lock fragment;
- zero or more M1B witness-card fragments;
- zero or more M1C causal-triad fragments;
- zero or more M1D off-target-audit fragments;
- the controller-spec reference;
- the evidence ledger.

It should be valid even when M1 fails. A clean negative result is still a scientific result.

## Result fields

The composite records:

```text
m1_result
```

with:

- runtime status;
- sanity-check status;
- promoted feature count;
- causal-triad pass count;
- off-target audit pass count;
- critical safety failures;
- pass/fail for M1 acceptance;
- headline finding.

## M2 handoff

The composite records:

```text
m2_handoff
```

with:

- readiness for M2;
- selected feature ids;
- alpha_behavioral by feature;
- blocking reasons.

If M1D flags a critical safety failure, `ready_for_m2` may be false even if M1C found a strong behavioral steering effect. In that case, the headline result is the off-target safety regression.

## Conditional outcomes

### Case A: M1 passes cleanly

At least one feature is promoted by M1B, shows coherent causal triad behavior in M1C, and passes M1D off-target audit.

M2 can begin on the selected feature and `alpha_behavioral`.

### Case B: M1 fails at sanity or feature selection

No viable source-locked feature is identified.

The certificate records the failure and blocks M2. The program then revisits source-lock parameters, layer, width, L0, or candidate direction construction.

### Case C: M1C succeeds but M1D flags safety regression

The feature-steering intervention works on the target MCQ behavior but damages safety or adjacent capabilities.

The headline finding is the safety regression. M2 is optional and should not obscure the M1D result.

## CI fixture

Synthetic schema fixture:

```text
tests/fixtures/m1/implementability-certificate.valid.json
```

The fixture is not an empirical result. It proves contract shape only.
