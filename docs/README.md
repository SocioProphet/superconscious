# Superconscious Documentation

Status: documentation index.

Superconscious is the visible governed cognition loop for recursive agents. It coordinates task state, policy requests, model-routing requests, tool observations, memory decisions, evidence emission, replay plans, and benchmark results while preserving authority boundaries.

## Core documents

- [`../README.md`](../README.md) — repository charter, position, trust-surface protocol summary, M1 deliverable, and repo layout.
- [`../ARCHITECTURE.md`](../ARCHITECTURE.md) — authority split, core loop, safe operational trace, adapter boundary, and M1 runtime posture.
- [`../THREAT_MODEL.md`](../THREAT_MODEL.md) — fail-closed posture, trust zones, approval classes, and primary threat classes.
- [`../ROADMAP.md`](../ROADMAP.md) — M1 through M7 roadmap.
- [`trust-surface-protocol.md`](trust-surface-protocol.md) — SourceOS Trust Surface Protocol.
- [`adapter-boundary-matrix.md`](adapter-boundary-matrix.md) — Superconscious adapter boundaries and final-authority split.
- [`neurosymbolic-cognition-position.md`](neurosymbolic-cognition-position.md) — Superconscious posture for CHRONOS-aligned neuro-symbolic cognition.
- [`neurosymbolic-capability-role-matrix.md`](neurosymbolic-capability-role-matrix.md) — allowed and forbidden roles for neuro-symbolic method families.
- [`neurosymbolic-failure-modes.md`](neurosymbolic-failure-modes.md) — authority-drift failure modes that must route to risk or policy review.

## Review priority

For changes that introduce new runtime authority, review in this order:

1. `TRUST_SURFACE.yaml`
2. `THREAT_MODEL.md`
3. `ARCHITECTURE.md`
4. `docs/adapter-boundary-matrix.md`
5. affected adapter or runtime code

For neuro-symbolic capability changes, additionally review:

1. `docs/neurosymbolic-cognition-position.md`
2. `docs/neurosymbolic-capability-role-matrix.md`
3. `docs/neurosymbolic-failure-modes.md`
4. any affected CHRONOS, evidence, policy, schema, or ontology handoff artifact

## Current boundary

M1 remains deterministic and inert. This documentation tranche does not modify the M1 runner and does not authorize network calls, model calls, host mutation, browser automation, terminal execution, durable memory promotion, or external tool execution.
