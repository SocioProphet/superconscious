# SVF Validation-History Consumer

Status: consumer contract doctrine  
Plane: Superconscious / Subconscious validation-memory consumer  
Upstream authority: SocioProphet/ProCybernetica SVF policy primitive  
Workspace registry: SocioProphet/sociosphere SVF workspace registry

## Purpose

This document defines how Superconscious consumes Sovereign Validation Fabric (SVF) validation history.

Subconscious is part of Superconscious. In this context, Subconscious may optimize recursive inference over validation history, failure patterns, missing-observation patterns, and plan usefulness. Superconscious governs the recursive agency boundary around that memory.

The consumer is read-only. It does not authorize execution, mutate policy, execute Sociosphere runner commands, certify receipts, or promote advisory validation results.

## Placement

Superconscious coordinates task trees, safe operational traces, skill activation, tool use, memory decisions, model routing, policy admission, approvals, benchmarks, replay plans, and AgentPlane-compatible evidence. It does not become the authority for schemas, execution, runtime placement, model governance, or workspace topology.

SVF validation-history consumption fits that boundary: Superconscious may remember and reason about validation outcomes, but authority remains upstream.

## Inputs

The first consumer may ingest validation-history events with:

- repo;
- ref;
- selected Plan ids;
- validation status;
- missing-observation warning codes;
- observed validation command refs;
- receipt refs;
- failure taxonomy;
- age/staleness;
- recommended next action;
- non-claims.

The first tranche is fixture-backed only.

## Allowed use

Superconscious/Subconscious may use validation history to:

- remember that a repo has missing observed validation;
- flag recurring validator failures;
- recommend deterministic validation before autonomous continuation;
- bias future planning toward lower-risk, report-only behavior;
- summarize plan usefulness and validation debt;
- route memory to AgentPlane evidence and Sociosphere backlog summaries.

## Disallowed use

Superconscious/Subconscious must not:

- execute SVF Actions;
- run Sociosphere commands;
- create, sign, or verify receipts;
- mark a Plan as validated without observed evidence;
- promote advisory validation to blocking validation;
- mutate ProCybernetica, Sociosphere, or downstream repo policy;
- override guardrail-fabric or policy-fabric;
- grant agent autonomy from validation history alone.

## Initial memory statuses

The first contract recognizes:

- `validated_observed` — observed validation evidence or receipt reference exists;
- `selected_missing_observation` — a Plan was selected but no observation exists;
- `failed_observed` — observed validation failed;
- `stale_observation` — evidence exists but is outside the accepted age window;
- `not_configured` — no applicable SVF profile or Plan exists.

## Non-claims

This document does not implement a live memory backend.

This document does not issue or verify receipts.

This document does not authorize execution.

This document does not make Subconscious a separate authority plane.
