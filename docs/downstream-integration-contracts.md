# Downstream Integration Contracts

Superconscious is a reference governed cognition loop. Downstream integrations should consume its artifacts and adapter semantics without moving authority out of the owning repositories.

## Artifact contract

Every Superconscious M1 run emits:

```text
events.jsonl
reasoning-run.json
agentplane-evidence.json
replay-plan.json
benchmark-result.json
```

Consumers must treat `reasoning-run.json` as the primary summary artifact and `events.jsonl` as the append-friendly operational trace.

## SourceOS spec

`SourceOS-Linux/sourceos-spec` should promote the draft artifact schemas after M1 stabilizes. Until then, Superconscious local draft schemas are examples and validation aids, not canonical authority.

Expected promoted objects:

- `ReasoningRun`
- `ReasoningEvent`
- `AdapterDecision`
- `AgentPlaneReasoningEvidence`
- `ReplayPlan`
- `BenchmarkResult`

## AgentPlane

`SocioProphet/agentplane` should ingest or translate `agentplane-evidence.json` into its evidence lifecycle.

Required fields:

- `runId`
- `taskId`
- `taskHash`
- `eventStreamHash`
- `policyDecision`
- `modelRouteDecision`
- `memoryDecision`
- `approvalDecision`
- `replayClass`

AgentPlane remains responsible for execution, placement, evidence sealing, and replay authority.

## SocioSphere

`SocioProphet/sociosphere` should use `workspace.lockRef` and `workspace.id` from `reasoning-run.json` to bind runs to workspace state.

Future validation lane:

```text
sociosphere validate-superconscious-run <run-dir>
```

Expected checks:

- workspace lock exists or is declared mock;
- repo role allows Superconscious coordination;
- artifacts do not violate source-exposure rules;
- adapter decisions refer to known authority repos;
- benchmark result is present before promotion.

## sourceosctl / sourceos-devtools

`SourceOS-Linux/sourceos-devtools` should wrap the inspector and validator semantics as:

```text
sourceosctl reasoning validate <run-dir>
sourceosctl reasoning inspect <run-dir>
sourceosctl reasoning replay-plan <run-dir>
sourceosctl reasoning events <run-dir>
```

`sourceosctl` should not become the cognition loop. It should inspect, validate, and operator-render Superconscious artifacts.

## Agent Machine

`SourceOS-Linux/agent-machine` should consume model/runtime/cache planning requests after M1. M1 uses mock routes and no runtime activation.

Future adapter decision should include:

- AgentPod envelope ref;
- runtime profile ref;
- cache posture;
- model residency facts;
- activation decision;
- runtime evidence pointer.

## Model Router and Model Carry

`SocioProphet/model-router` should own route decisions. `SourceOS-Linux/sourceos-model-carry` should own local profile references.

Superconscious should request:

```text
task class
workspace posture
local-first requirement
prompt-egress posture
profile candidates
```

It should receive:

```text
route id
provider class
model/profile ref
local/remote posture
prompt egress decision
evidence hash/ref
```

## Guardrail Fabric / Policy Fabric

Policy admission should eventually replace the mock policy adapter.

Required admissions:

- tool use;
- model route;
- memory write;
- network egress;
- host state change;
- browser control;
- terminal action;
- document/email/calendar action;
- approval escalation.

## Agent Registry

Agent Registry should resolve:

- agent identity;
- role;
- session;
- workspace scope;
- tool grants;
- memory grants;
- model grants;
- skill grants;
- revocation status.

Superconscious must fail closed when grants are missing.

## Product surfaces

TurtleTerm, AgentTerm, BearBrowser, SocioProphet web, and SocioSphere can render the same `reasoning-run.json` as:

- task tree;
- adapter decisions;
- safe operational trace;
- policy/model/memory/approval posture;
- evidence refs;
- replay class;
- benchmark result.

## Non-goals for consumers

Consumers should not require raw private chain-of-thought. They should render safe operational traces only.
