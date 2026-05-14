# Superconscious Program Status

## Status date

2026-05-13

## Program role

`SocioProphet/superconscious` is the implementation spine for the Heller Consciousness / implementability-certificate program.

It is a sibling program to `SocioProphet/ProCybernetica`. Superconscious produces interpretability certificates. ProCybernetica ingests completed certificates as governance evidence.

## Current state

```text
doctrine_complete: M1 -> M2 -> M3 -> M5
ci_fixture_complete: M1 -> M2 -> M3 -> M5
lawful_learning_phase_8_registration: complete
runtime_executed: false
empirical_claims: none
```

## Lawful-learning pipeline status

```text
Phase 1-6: superconscious-internal doctrine, schemas, checker, and hardened fixtures  ✓
Phase 7:   systems-learning-loops research evidence pack                             ✓
Phase 8:   sociosphere cross-repo registration                                       ✓
Phase 9:   agentplane runtime evidence integration                                   deferred
```

Phase 8 was completed by:

```text
SocioProphet/sociosphere#337
registry/lawful-learning-lane.yaml
docs/LAWFUL_LEARNING_PHASE8_REGISTRATION.md
```

Phase 8 registration is not schema promotion, runtime execution, evidence authenticity, monitor attestation, or frontier-claim promotion. It is a cross-repo governance registration that names final authority surfaces for lawful-learning lane discovery and future runtime integration.

## Completed doctrine/CI lanes

### M1 — Source lock, witness cards, causal triad, off-target audit

Completed as schema and deterministic-fixture lane:

- M1-0 controller spec;
- M1A source-lock certificate;
- M1B witness-card schema and Option-C cross-width witness scaffold;
- M1C causal-triad schema;
- M1D off-target-audit schema;
- composite M1 implementability certificate schema;
- synthetic fixtures;
- Makefile/CI targets.

### M2 — Implementability envelope

Completed as schema and deterministic-fixture lane:

- activation-cache manifest;
- manifold-baseline calibration;
- implementability-curve five-curve data;
- composite M2 implementability certificate;
- synthetic fixtures;
- metric doctrine.

### M3 — Cross-layer robustness

Completed as schema and deterministic-fixture lane:

- cross-layer comparison;
- transcoder/crosscoder placeholder evidence;
- robustness certificate;
- synthetic fixtures;
- layer-selection rationale.

### M5 — Public-note conditional framing

Completed as schema/template lane:

- public-note schema;
- synthetic fixture;
- five outcome templates;
- outcome-template mapping;
- public-note doctrine.

## CI status

The repository has a certificate CI target:

```bash
make certificate-ci
```

This target composes:

```text
m1-ci
m2-ci
m3-ci
m5-ci
```

The GitHub Actions workflow runs certificate doctrine CI on push and pull request.

## Local CI status

Local clean-checkout execution is not yet verified in this chat.

Required local command:

```bash
cd ~/dev/superconscious && make certificate-ci
```

If this fails, fixing the failure takes priority over adding new doctrine or schemas.

## Runtime gates pending

The empirical/runtime lane remains unopened.

Required runtime sequence:

1. `make m1a-generate && make m1-verify-source-lock` against live Hugging Face metadata.
2. Download and hash model weights and SAE parameters.
3. Run pre-M1B steering sanity check.
4. Populate real M1B witness cards.
5. Run M1C causal triad.
6. Run M1D off-target audit.
7. Compose M1 certificate.
8. Run M2 activation-cache, manifold-baseline, and implementability-curve pipeline.
9. Run M3 cross-layer robustness.
10. Instantiate M5 public note from certified outcome.

## Funding boundary

Current artifacts prove architecture, schema, fixture, and composition discipline. They do not prove empirical behavior of Gemma, Gemma Scope, or any model.

Funding or donated runtime converts synthetic fixtures into runtime-executed certificates.

Approximate runtime ask:

```text
one modern accelerator for M1B/M1C/M1D + M2 primary layer + M3 witness layers
```

## Non-claims

This repository currently does not claim:

- a live Gemma/Gemma Scope steering result;
- a selected refusal feature;
- an in-envelope or out-of-distribution steering classification;
- cross-layer empirical robustness;
- public empirical note readiness;
- production governance runtime;
- lawful-learning runtime evidence integration;
- canonical schema promotion into `sourceos-spec`.

## Next bounded move

Do not add more interpretability doctrine until local `make certificate-ci` has been run on a clean checkout and any failures have been corrected.

For the lawful-learning lane, the next runtime-bearing move is Phase 9 in `SocioProphet/agentplane`, gated on runtime infrastructure and evidence/replay integration.
