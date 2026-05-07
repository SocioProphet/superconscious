# Superconscious Integration Ledger

This ledger tracks absorption of the Superconscious governed cognition loop across the SocioProphet / SourceOS estate.

## Current absorption state

| Lane | Status | Authority repo | Notes |
|---|---|---|---|
| Reference cognition loop | Implemented M1 | `SocioProphet/superconscious` | Deterministic no-network/no-model/no-host-mutation runner emits safe operational trace artifacts. |
| Canonical artifact emission | Implemented M1/M2 bridge | `SocioProphet/superconscious` | `canonicalize_artifacts.py` emits SourceOS-shaped artifacts alongside compatibility artifacts. |
| Trust surface protocol | Seeded | `SocioProphet/superconscious` → future `SourceOS-Linux/sourceos-spec` | Superconscious carries seed schema/workflow until canonical trust-surface ownership is promoted. |
| Canonical reasoning schemas | First tranche promoted | `SourceOS-Linux/sourceos-spec` | `ReasoningRun`, `ReasoningEvent`, `ReasoningReceipt`, `ReasoningReplayPlan`, and `ReasoningBenchmark` are promoted with examples and contract-addition docs. |
| Adapter decision object | Deferred | `SourceOS-Linux/sourceos-spec` | Direct `AdapterDecision` promotion was blocked by connector filtering; use `ReasoningRun.adapterRecords` until a narrower future schema is agreed. |
| AgentPlane evidence/replay | PR open | `SocioProphet/agentplane` | `SocioProphet/agentplane#123` adds read-only canonical artifact import validation; issue `#109` remains the work-order root. |
| SocioSphere validation | PR open | `SocioProphet/sociosphere` | `SocioProphet/sociosphere#292` adds read-only workspace/source-exposure validation; issue `#274` remains the work-order root. |
| sourceosctl inspection | PR open | `SourceOS-Linux/sourceos-devtools` | `SourceOS-Linux/sourceos-devtools#24` adds `sourceosctl reasoning validate|inspect|replay-plan|events`; issue `#22` remains the work-order root. |
| Runtime planning | PR open | `SourceOS-Linux/agent-machine` | `SourceOS-Linux/agent-machine#27` adds deterministic no-activation runtime-plan fixture; issue `#23` remains the work-order root. |
| Model routing | PR open | `SocioProphet/model-router` | `SocioProphet/model-router#14` adds deterministic task-class route fixture; issue `#12` remains the work-order root. |
| Policy admission | PR open | `SocioProphet/guardrail-fabric` | `SocioProphet/guardrail-fabric#22` adds deterministic M1 policy-admission fixture; issue `#17` remains the work-order root. |
| Agent grants | PR open | `SocioProphet/agent-registry` | `SocioProphet/agent-registry#28` adds deterministic grant fixture; issue `#22` remains the work-order root. |
| Terminal product surface | Work order open | `SourceOS-Linux/TurtleTerm` | `SourceOS-Linux/TurtleTerm#6`. |
| Browser product surface | Work order open | `SourceOS-Linux/BearBrowser` | `SourceOS-Linux/BearBrowser#23`. |
| Operator console surface | Work order open | `SourceOS-Linux/agent-term` | `SourceOS-Linux/agent-term#38`. |
| Web product surface | Work order open | `SocioProphet/socioprophet` | `SocioProphet/socioprophet#311`. |
| Socios personalization | Work order open | `SociOS-Linux/socios` | `SociOS-Linux/socios#76`; must remain opt-in with signed intent and proof-of-life. |
| Benchmarks beyond M1 | Not started | `SocioProphet/superconscious` + product/runtime repos | Browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites remain. |

## Artifact sets

Compatibility artifacts emitted by the M1 runner:

```text
events.jsonl
reasoning-run.json
agentplane-evidence.json
replay-plan.json
benchmark-result.json
```

Canonical SourceOS artifacts emitted by the canonicalization layer:

```text
reasoning-events.sourceos.jsonl
reasoning-run.sourceos.json
reasoning-receipt.json
reasoning-replay-plan.json
reasoning-benchmark.json
```

## Active pull requests

- `SocioProphet/agentplane#123` — Import Superconscious ReasoningRun artifacts into AgentPlane validation.
- `SourceOS-Linux/sourceos-devtools#24` — Add sourceosctl reasoning inspection and validation commands.
- `SocioProphet/sociosphere#292` — Validate Superconscious ReasoningRun artifacts in SocioSphere.
- `SourceOS-Linux/agent-machine#27` — Add Superconscious ReasoningRun runtime-plan fixture.
- `SocioProphet/model-router#14` — Add Superconscious ReasoningRun task-class route fixture.
- `SocioProphet/guardrail-fabric#22` — Add Superconscious ReasoningRun policy admission fixture.
- `SocioProphet/agent-registry#28` — Add Superconscious ReasoningRun grant fixture.

## Open work orders

- `SocioProphet/agentplane#109` — Integrate SourceOS ReasoningRun contracts into AgentPlane evidence and replay.
- `SocioProphet/sociosphere#274` — Add Superconscious ReasoningRun validation lane to SocioSphere.
- `SourceOS-Linux/sourceos-devtools#22` — Add sourceosctl reasoning validation and inspection commands.
- `SourceOS-Linux/agent-machine#23` — Plan Agent Machine runtime adapter for Superconscious ReasoningRun workloads.
- `SocioProphet/model-router#12` — Add ReasoningRun task-class routing contract for Superconscious.
- `SocioProphet/guardrail-fabric#17` — Add policy admission contract for Superconscious ReasoningRun actions.
- `SocioProphet/agent-registry#22` — Add AgentRegistryGrant contract for Superconscious ReasoningRun sessions.
- `SourceOS-Linux/TurtleTerm#6` — Render Superconscious ReasoningRun task tree and evidence in TurtleTerm.
- `SourceOS-Linux/BearBrowser#23` — Render Superconscious ReasoningRun traces in BearBrowser sidecar.
- `SourceOS-Linux/agent-term#38` — Render Superconscious ReasoningRun traces in AgentTerm operator console.
- `SocioProphet/socioprophet#311` — Render Superconscious ReasoningRun cognition/evidence panel in SocioProphet web.
- `SociOS-Linux/socios#76` — Add opt-in Superconscious personalization orchestration lane.

## Upstream contract tranche

Promoted into `SourceOS-Linux/sourceos-spec`:

- `schemas/ReasoningRun.json`
- `schemas/ReasoningEvent.json`
- `schemas/ReasoningReceipt.json`
- `schemas/ReasoningReplayPlan.json`
- `schemas/ReasoningBenchmark.json`
- `examples/reasoning_run.json`
- `examples/reasoning_event.json`
- `examples/reasoning_receipt.json`
- `examples/reasoning_replay_plan.json`
- `examples/reasoning_benchmark.json`
- `docs/contract-additions/reasoning-run-contracts.md`
- `schemas/reasoning-contracts.README.md`

## Next absorption sequence

1. Merge/validate the seven active PRs: AgentPlane, sourceosctl, SocioSphere, Agent Machine, Model Router, Guardrail Fabric, and Agent Registry.
2. Add product rendering fixtures for TurtleTerm, AgentTerm, BearBrowser, and web.
3. Add opt-in Socios personalization dry-run fixtures and model-governance-ledger references.
4. Expand benchmarks beyond M1: browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites.

## Turn estimate

Estimated remaining turns to full bounded absorption: **2–4**.

- **1 turn** for merge/readiness checks and follow-up fixes on the seven active PRs.
- **1 turn** for TurtleTerm/BearBrowser/AgentTerm/web rendering fixtures.
- **0–2 turns** for benchmark expansion and Socios personalization dry-run fixtures.

This estimate means full M1/M2 absorption across the active estate, not production-grade autonomous runtime activation.
