# M1 Doctrine

This document records the load-bearing principles of the M1 interpretability certificate chain.

The current funding-constrained state is explicit: M1 can be doctrine-complete and CI-complete on deterministic fixtures without claiming empirical execution. Runtime execution against live Gemma/Gemma Scope artifacts remains a post-funding gate.

## Principle 1: Off-history retention

Every certificate fragment is retained in the evidence ledger regardless of acceptance outcome.

Rejected witness cards are not deleted, archived away, or treated as noise. A rejected candidate constrains the search space and helps calibrate future selection rules. Rejections are first-class evidence.

## Principle 2: Counterfactual addressability

Every mature certificate declares which counterfactual questions its evidence can answer.

A certificate whose evidence does not answer a declared counterfactual is invalid. A certificate that answers an undeclared counterfactual is incomplete.

Counterfactual addressability is the structural measure of certificate maturity.

## Principle 3: Execution-status honesty

Every certificate must distinguish architectural completeness from empirical execution.

Allowed execution statuses:

```text
doctrine_only
synthetic_fixture
runtime_partial
runtime_executed
failed
```

At the current program stage, many certificates are `synthetic_fixture`: they prove schema and composition shape, not empirical claims.

## Principle 4: Signing-authority transparency

Every certificate fragment records the authority that sealed it.

Composite certificates compute an authority-concentration index. A composite signed by one authority is structurally weaker than one signed by independent parties. The index makes this machine-readable.

## Principle 5: Schema versioning is event-recorded

Schema bumps are recorded as ledger events.

Certificates sealed under v1.0.0 remain valid under their original schema. A certificate needing v1.1.0 fields is resealed and linked to the prior fragment via `supersedes`.

## Principle 6: Off-target failures are headline findings

If M1D detects a critical failure in genuine refusal preservation, the composite M1 certificate must surface that as its headline finding.

A steering intervention that restores MCQ accuracy while weakening genuine refusal is not a clean interpretability success. It is a safety regression.

## Principle 7: Funding boundary

Doctrine-complete and CI-complete does not mean runtime-executed.

The funding ask is therefore bounded: the architecture is built and validated on deterministic fixtures; funding buys runtime execution against locked artifacts, not speculative design.
