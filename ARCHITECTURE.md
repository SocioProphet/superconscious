# Superconscious Architecture

Superconscious is a reference cognition/control-loop implementation. It is intentionally thin: it coordinates existing authorities instead of replacing them.

## Authority split

| Concern | Authority repo | Superconscious role |
|---|---|---|
| Contracts and vocabulary | `SourceOS-Linux/sourceos-spec` | Consume and validate; temporarily stage local draft schemas only before promotion. |
| Execution, placement, evidence, replay | `SocioProphet/agentplane` | Emit AgentPlane-compatible evidence and replay plans. |
| Workspace topology and registry governance | `SocioProphet/sociosphere` | Bind runs to workspace lock, repo roles, and topology constraints. |
| Runtime substrate | `SourceOS-Linux/agent-machine` | Request runtime plans and activation decisions through adapters. |
| Local model profile carriage | `SourceOS-Linux/sourceos-model-carry` | Use local model profile refs and route classes. |
| Model routing | `SocioProphet/model-router` | Request model route decisions. |
| Model consent / promotion | `SocioProphet/model-governance-ledger` | Reference receipts and contracts; never authorize training locally. |
| Policy admission | `SocioProphet/guardrail-fabric` / Policy Fabric | Request admissions for tools, memory, model routes, side effects, and egress. |
| Agent grants | `SocioProphet/agent-registry` | Resolve agent identity, workspace, session, skill, tool, model, and memory grants. |
| Operator CLI | `SourceOS-Linux/sourceos-devtools` | Provide inspectable outputs for `sourceosctl reasoning ...`. |
| Terminal/browser surfaces | TurtleTerm, AgentTerm, BearBrowser | Provide trace tree and adapter semantics. |
| Opt-in automation | `SociOS-Linux/socios` | Reference signed opt-in orchestration; never bypass proof-of-life or consent. |

## Falsification doctrine

Superconscious carries the estate-facing falsification doctrine at [`docs/architecture-falsification-v0.1.md`](docs/architecture-falsification-v0.1.md).

This doctrine does not make Superconscious the authority for artifact schemas, certificate semantics, Atlas promotion, SHACL validation, or runtime serving decisions. It defines the observations that would prove the current artifact / evidence / gate cut is structurally inadequate and therefore force revision in the proper owner repositories.

Superconscious uses the doctrine in three limited ways:

- safe operational traces can reference which falsification observable a proposed change resolves, worsens, or introduces;
- benchmark and red-team fixtures can be grouped by falsification observable;
- adapters can expose whether a runtime path is respecting Atlas promotion verdicts before serving governed artifacts.

The initial falsification boundaries are:

```text
Artifact -> Evidence: graphbrain-contract artifacts into M0/M1/M1.5/M2/M3/M5 certificates
Evidence -> Gate: certificate verdicts and invariants into TritFabric Atlas / SHACL / Gatekeeper
Gate -> Runtime: Atlas decisions into memory-mesh, new-hope, slash-topics, sherlock-search, holmes, graphbrain-contract
Methodology: fixture-testability, quarterly review, and decomposition failure criteria
```

## Core loop

```text
TaskInput
  -> RunContext
  -> ReasoningRun.created
  -> ReasoningTask.started
  -> PolicyCheck.requested
  -> PolicyCheck.decided
  -> ModelRoute.requested
  -> ModelRoute.decided
  -> SkillActivation.selected
  -> ToolUse.requested
  -> ToolUse.observed
  -> MemoryDecision.proposed
  -> Evidence.emitted
  -> ReplayPlan.emitted
  -> BenchmarkResult.emitted
  -> ReasoningRun.completed | failed | cancelled | blocked
```

## Safe operational trace

Superconscious emits safe operational traces, not raw private chain-of-thought. The trace records operational facts:

- task decomposition;
- selected skill;
- tool requested;
- tool result summary;
- policy decision;
- model route decision;
- memory write proposal;
- approval request and result;
- execution evidence;
- benchmark result;
- replay pointer;
- final summary.

## Adapter boundary

All integration points are adapters. Superconscious core should run with mock adapters in local deterministic mode.

```text
PolicyAdapter
AgentGrantAdapter
ModelRouteAdapter
RuntimeAdapter
ToolAdapter
MemoryAdapter
EvidenceAdapter
WorkspaceAdapter
ApprovalAdapter
BenchmarkAdapter
```

## M1 runtime posture

M1 must be safe by default:

- no network calls;
- no model calls;
- no host mutation;
- no credential access;
- no direct shell execution;
- no browser automation;
- no durable memory promotion without explicit memory decision;
- deterministic output suitable for test and replay.

## Event and artifact shape

M1 emits JSON artifacts under `.runs/<run-id>/`:

```text
events.jsonl
reasoning-run.json
agentplane-evidence.json
replay-plan.json
benchmark-result.json
```

These local draft artifacts exist to harden the loop. Canonical schema promotion belongs in `SourceOS-Linux/sourceos-spec`.
