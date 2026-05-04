# Integration Map

Superconscious coordinates existing authorities through adapters.

## Canonical flow

```text
SocioSphere workspace lock
  -> Superconscious run context
  -> Agent Registry grant resolution
  -> Guardrail / Policy Fabric admission
  -> Model Router route decision
  -> Skill activation
  -> Tool adapter call
  -> Memory decision
  -> AgentPlane evidence + replay
  -> sourceosctl / TurtleTerm / BearBrowser / web rendering
```

## Adapter contracts

| Adapter | Purpose | Initial M1 implementation |
|---|---|---|
| `WorkspaceAdapter` | Bind run to SocioSphere workspace state and repo topology. | Mock workspace ref. |
| `AgentGrantAdapter` | Resolve agent identity, grants, scopes, and session authority. | Mock allowlisted agent. |
| `PolicyAdapter` | Decide whether tool, model, memory, egress, or side effects are allowed. | Mock fail-closed/allow-safe policy. |
| `ModelRouteAdapter` | Select model profile or deterministic stub. | Mock local deterministic route. |
| `SkillAdapter` | Select and activate skill manifests. | Mock basic-planner skill. |
| `ToolAdapter` | Execute or simulate tools. | Mock echo/summarize tool. |
| `MemoryAdapter` | Propose, reject, or commit memory decisions. | Mock proposal-only memory. |
| `EvidenceAdapter` | Emit AgentPlane-compatible evidence. | Local JSON evidence stub. |
| `BenchmarkAdapter` | Assert run success/failure. | Local deterministic assertions. |
| `ApprovalAdapter` | Request operator/enterprise/signed-intent approvals. | Mock no-approval-needed for safe task. |

## Integration rule

Every adapter must support deterministic local mode. Real adapters may be added later, but tests must not require network, credentials, model providers, browser automation, or host mutation.
