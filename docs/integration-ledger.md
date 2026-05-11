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
| sourceosctl inspection | Merged | `SourceOS-Linux/sourceos-devtools` | `SourceOS-Linux/sourceos-devtools#24` merged; issue `#22` closed. Adds `sourceosctl reasoning validate|inspect|replay-plan|events`. |
| Model routing | Merged | `SocioProphet/model-router` | `SocioProphet/model-router#14` merged; issue `#12` closed. Adds deterministic no-provider task-class route fixture. |
| Policy admission | Merged | `SocioProphet/guardrail-fabric` | `SocioProphet/guardrail-fabric#22` merged; issue `#17` closed. Adds deterministic M1 policy-admission fixture. |
| Agent grants | Merged | `SocioProphet/agent-registry` | `SocioProphet/agent-registry#29` merged; stale `#28` closed; issue `#22` closed. Adds deterministic grant fixture. |
| SocioSphere validation | Merged | `SocioProphet/sociosphere` | `SocioProphet/sociosphere#316` merged; stale `#292` closed; issue `#274` closed. Adds workspace/source-exposure validation lane. |
| AgentPlane evidence/replay | Open / needs current-main rebuild | `SocioProphet/agentplane` | `SocioProphet/agentplane#123` is open but diverged behind current main. Needs rebuild before merge. |
| Runtime planning | Open / connector-blocked rebuild | `SourceOS-Linux/agent-machine` | `SourceOS-Linux/agent-machine#27` had green checks after fixture move, but branch diverged; current-main rebuild hit connector filtering on runtime-plan fixture content. |
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

## Merged pull requests

- `SourceOS-Linux/sourceos-devtools#24` — Add sourceosctl reasoning inspection and validation commands.
- `SocioProphet/model-router#14` — Add Superconscious ReasoningRun task-class route fixture.
- `SocioProphet/guardrail-fabric#22` — Add Superconscious ReasoningRun policy admission fixture.
- `SocioProphet/agent-registry#29` — Add Superconscious ReasoningRun grant fixture.
- `SocioProphet/sociosphere#316` — Validate Superconscious ReasoningRun artifacts in SocioSphere.

## Open pull requests / blockers

- `SocioProphet/agentplane#123` — Import Superconscious ReasoningRun artifacts into AgentPlane validation. Open but stale/diverged; needs current-main rebuild.
- `SourceOS-Linux/agent-machine#27` — Add Superconscious ReasoningRun runtime-plan fixture. Open; original branch validated after fixture move, but current-main rebuild was connector-filtered.

## Open work orders

- `SocioProphet/agentplane#109` — Integrate SourceOS ReasoningRun contracts into AgentPlane evidence and replay.
- `SourceOS-Linux/agent-machine#23` — Plan Agent Machine runtime adapter for Superconscious ReasoningRun workloads.
- `SourceOS-Linux/TurtleTerm#6` — Render Superconscious ReasoningRun task tree and evidence in TurtleTerm.
- `SourceOS-Linux/BearBrowser#23` — Render Superconscious ReasoningRun traces in BearBrowser sidecar.
- `SourceOS-Linux/agent-term#38` — Render Superconscious ReasoningRun traces in AgentTerm operator console.
- `SocioProphet/socioprophet#311` — Render Superconscious ReasoningRun cognition/evidence panel in SocioProphet web.
- `SociOS-Linux/socios#76` — Add opt-in Superconscious personalization orchestration lane.

## Closed work orders

- `SourceOS-Linux/sourceos-devtools#22` — Completed by `#24`.
- `SocioProphet/model-router#12` — Completed by `#14`.
- `SocioProphet/guardrail-fabric#17` — Completed by `#22`.
- `SocioProphet/agent-registry#22` — Completed by `#29`.
- `SocioProphet/sociosphere#274` — Completed by `#316`.

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

1. Rebuild `SocioProphet/agentplane#123` on current mainline and merge after green checks.
2. Resolve `SourceOS-Linux/agent-machine#27` with a connector-safe current-main fixture or alternate validator pattern.
3. Add product rendering fixtures for TurtleTerm, AgentTerm, BearBrowser, and web.
4. Add opt-in Socios personalization dry-run fixtures and model-governance-ledger references.
5. Expand benchmarks beyond M1: browser, terminal, repo, office, MCP, memory, policy, model-route, and replay suites.

## Turn estimate

Estimated remaining turns to full bounded absorption: **2–3**.

- **1 turn** for AgentPlane rebuild and Agent Machine unblock/replacement.
- **1 turn** for TurtleTerm/BearBrowser/AgentTerm/web rendering fixtures.
- **0–1 turn** for benchmark expansion and Socios personalization dry-run fixtures.

This estimate means full M1/M2 absorption across the active estate, not production-grade autonomous runtime activation.
