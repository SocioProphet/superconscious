# Superconscious Integration Ledger

This ledger tracks absorption of the Superconscious governed cognition loop across the SocioProphet / SourceOS estate.

## Current absorption state

| Lane | Status | Authority repo | Notes |
|---|---|---|---|
| Reference cognition loop | Implemented M1 | `SocioProphet/superconscious` | Deterministic no-network/no-model/no-host-mutation runner emits safe operational trace artifacts. |
| Trust surface protocol | Seeded | `SocioProphet/superconscious` → future `SourceOS-Linux/sourceos-spec` | Superconscious carries seed schema/workflow until canonical trust-surface ownership is promoted. |
| Canonical reasoning schemas | Partially promoted | `SourceOS-Linux/sourceos-spec` | `ReasoningRun`, `ReasoningEvent`, `ReasoningReceipt`, `ReasoningReplayPlan`, and `ReasoningBenchmark` are promoted. |
| Adapter decision object | Deferred | `SourceOS-Linux/sourceos-spec` | Direct `AdapterDecision` promotion was blocked by connector filtering; use `ReasoningRun.adapterRecords` until a narrower future schema is agreed. |
| AgentPlane evidence/replay | Work order open | `SocioProphet/agentplane` | Issue #109. |
| SocioSphere validation | Work order open | `SocioProphet/sociosphere` | Issue #274. |
| sourceosctl inspection | Work order open | `SourceOS-Linux/sourceos-devtools` | Issue #22. |
| Runtime planning | Work order open | `SourceOS-Linux/agent-machine` | Issue #23. |
| Model routing | Work order open | `SocioProphet/model-router` | Issue #12. |
| Policy admission | Work order open | `SocioProphet/guardrail-fabric` | Issue #17. |
| Agent grants | Work order open | `SocioProphet/agent-registry` | Issue #22. |
| Product rendering | Not started | TurtleTerm / AgentTerm / BearBrowser / SocioProphet web | Needs task tree, adapter decisions, replay, and benchmark rendering. |
| Benchmarks beyond M1 | Not started | `SocioProphet/superconscious` + product/runtime repos | Browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites remain. |
| Socios personalization | Not started | `SociOS-Linux/socios` + `SocioProphet/model-governance-ledger` | Must remain opt-in with signed intent and proof-of-life. |

## Open work orders

- `SocioProphet/agentplane#109` — Integrate SourceOS ReasoningRun contracts into AgentPlane evidence and replay.
- `SocioProphet/sociosphere#274` — Add Superconscious ReasoningRun validation lane to SocioSphere.
- `SourceOS-Linux/sourceos-devtools#22` — Add sourceosctl reasoning validation and inspection commands.
- `SourceOS-Linux/agent-machine#23` — Plan Agent Machine runtime adapter for Superconscious ReasoningRun workloads.
- `SocioProphet/model-router#12` — Add ReasoningRun task-class routing contract for Superconscious.
- `SocioProphet/guardrail-fabric#17` — Add policy admission contract for Superconscious ReasoningRun actions.
- `SocioProphet/agent-registry#22` — Add AgentRegistryGrant contract for Superconscious ReasoningRun sessions.

## Next absorption sequence

1. Update Superconscious emitted artifact names/fields toward canonical `sourceos-spec` naming while preserving M1 compatibility.
2. Add AgentPlane fixture translation for `ReasoningReceipt` and `ReasoningReplayPlan`.
3. Add SocioSphere workspace/source-exposure validation over Superconscious run directories.
4. Add `sourceosctl reasoning validate|inspect|replay-plan|events` commands.
5. Add Agent Machine runtime-plan mock adapter.
6. Replace mock policy/model/grant adapters with real client adapters behind deterministic test doubles.
7. Add product rendering tasks for TurtleTerm, AgentTerm, BearBrowser, and web.

## Turn estimate

Estimated remaining turns to full absorption: 5–7.

- 1–2 turns for sourceos-spec cleanup and Superconscious canonical-name alignment.
- 1 turn for AgentPlane evidence/replay integration.
- 1 turn for SocioSphere/sourceosctl validation and inspection.
- 1 turn for Agent Machine/model-router/guardrail/registry real adapter stubs.
- 1–2 turns for product surfaces and benchmark expansion.

This estimate assumes bounded M1/M2 integration, not full production-grade model/runtime activation.
