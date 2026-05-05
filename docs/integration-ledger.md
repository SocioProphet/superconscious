# Superconscious Integration Ledger

This ledger tracks absorption of the Superconscious governed cognition loop across the SocioProphet / SourceOS estate.

## Current absorption state

| Lane | Status | Authority repo | Notes |
|---|---|---|---|
| Reference cognition loop | Implemented M1 | `SocioProphet/superconscious` | Deterministic no-network/no-model/no-host-mutation runner emits safe operational trace artifacts. |
| Trust surface protocol | Seeded | `SocioProphet/superconscious` → future `SourceOS-Linux/sourceos-spec` | Superconscious carries seed schema/workflow until canonical trust-surface ownership is promoted. |
| Canonical reasoning schemas | First tranche promoted | `SourceOS-Linux/sourceos-spec` | `ReasoningRun`, `ReasoningEvent`, `ReasoningReceipt`, `ReasoningReplayPlan`, and `ReasoningBenchmark` are promoted with examples and contract-addition docs. |
| Adapter decision object | Deferred | `SourceOS-Linux/sourceos-spec` | Direct `AdapterDecision` promotion was blocked by connector filtering; use `ReasoningRun.adapterRecords` until a narrower future schema is agreed. |
| AgentPlane evidence/replay | Work order open | `SocioProphet/agentplane` | `SocioProphet/agentplane#109`. |
| SocioSphere validation | Work order open | `SocioProphet/sociosphere` | `SocioProphet/sociosphere#274`. |
| sourceosctl inspection | Work order open | `SourceOS-Linux/sourceos-devtools` | `SourceOS-Linux/sourceos-devtools#22`. |
| Runtime planning | Work order open | `SourceOS-Linux/agent-machine` | `SourceOS-Linux/agent-machine#23`. |
| Model routing | Work order open | `SocioProphet/model-router` | `SocioProphet/model-router#12`. |
| Policy admission | Work order open | `SocioProphet/guardrail-fabric` | `SocioProphet/guardrail-fabric#17`. |
| Agent grants | Work order open | `SocioProphet/agent-registry` | `SocioProphet/agent-registry#22`. |
| Terminal product surface | Work order open | `SourceOS-Linux/TurtleTerm` | `SourceOS-Linux/TurtleTerm#6`. |
| Browser product surface | Work order open | `SourceOS-Linux/BearBrowser` | `SourceOS-Linux/BearBrowser#23`. |
| Operator console surface | Work order open | `SourceOS-Linux/agent-term` | `SourceOS-Linux/agent-term#38`. |
| Web product surface | Work order open | `SocioProphet/socioprophet` | `SocioProphet/socioprophet#311`. |
| Socios personalization | Work order open | `SociOS-Linux/socios` | `SociOS-Linux/socios#76`; must remain opt-in with signed intent and proof-of-life. |
| Benchmarks beyond M1 | Not started | `SocioProphet/superconscious` + product/runtime repos | Browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites remain. |

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

1. Update Superconscious emitted artifact names/fields toward canonical `sourceos-spec` naming while preserving M1 compatibility.
2. Add AgentPlane fixture translation for `ReasoningReceipt` and `ReasoningReplayPlan`.
3. Add SocioSphere workspace/source-exposure validation over Superconscious run directories.
4. Add `sourceosctl reasoning validate|inspect|replay-plan|events` commands.
5. Add Agent Machine runtime-plan mock adapter.
6. Replace mock policy/model/grant adapters with real client adapters behind deterministic test doubles.
7. Add product rendering tasks for TurtleTerm, AgentTerm, BearBrowser, and web.
8. Add opt-in Socios personalization dry-run fixtures and model-governance-ledger references.
9. Expand benchmarks beyond M1: browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites.

## Turn estimate

Estimated remaining turns to full bounded absorption: **5–7**.

- **1 turn** for Superconscious canonical-name alignment against `sourceos-spec` contracts.
- **1 turn** for AgentPlane evidence/replay fixture integration.
- **1 turn** for SocioSphere/sourceosctl validation and inspection integration.
- **1 turn** for Agent Machine/model-router/guardrail/registry real adapter stubs.
- **1 turn** for TurtleTerm/BearBrowser/AgentTerm/web rendering fixtures.
- **0–2 turns** for benchmark expansion and Socios personalization dry-run fixtures.

This estimate means full M1/M2 absorption across the active estate, not production-grade autonomous runtime activation.
