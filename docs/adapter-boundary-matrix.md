# Superconscious Adapter Boundary Matrix

Status: v0.1 documentation. This file does not modify the M1 runner.

Superconscious is the visible governed cognition loop. It coordinates task state, policy requests, model-routing requests, skill activation, tool observations, memory decisions, evidence emission, replay plans, and benchmark results. It does not own schema authority, admission authority, execution/evidence/replay authority, model-governance authority, routing authority, or workspace/registry authority.

This matrix defines what each adapter may request, what it must not do, and which repository owns final authority.

## Boundary doctrine

Superconscious coordinates; it does not authorize.

Superconscious emits safe operational traces; it does not expose raw private chain-of-thought.

Superconscious prepares and records requests; it does not mutate host state, call live tools, open network egress, promote durable memory, or route to models without explicit downstream admission.

Every adapter must remain mockable for deterministic local tests.

## Plane ownership vocabulary

This document uses the same plane ownership vocabulary as the hybrid control-plane reconciliation map:

| Plane | Final authority |
|---|---|
| Schema authority | `SourceOS-Linux/sourceos-spec` |
| Execution/evidence/replay | `SocioProphet/agentplane` |
| Workspace/registry | `SocioProphet/sociosphere` |
| Cancellation/admission | `SocioProphet/policy-fabric` |
| Model governance/consent | `SocioProphet/model-governance-ledger` |
| Routing | `SocioProphet/model-router` |

Superconscious may stage local draft shapes only for deterministic testing. Canonical schema ownership remains in `SourceOS-Linux/sourceos-spec`, with Ontogenesis contributing vocabulary and semantic contract work before promotion.

## Adapter matrix

| Adapter | Superconscious role | Final authority | Allowed in Superconscious | Forbidden in Superconscious |
|---|---|---|---|---|
| `PolicyAdapter` | request admission, cancellation, denial, modification, or escalation for tools, memory, model routes, egress, and side effects | `SocioProphet/policy-fabric` | emit policy request and record returned decision | decide policy locally or override denial |
| `AgentGrantAdapter` | resolve agent/session/tool/model/memory grants | `SocioProphet/sociosphere` for workspace/registry binding; future grant-specific authority may be delegated by registry contract | request grant snapshot and include grant refs in trace | mint grants or silently widen scope |
| `ModelRouteAdapter` | request route class for model/provider use | `SocioProphet/model-router` | record route request/decision | call provider directly or bypass routing/egress policy |
| `ModelGovernanceAdapter` | reference model consent, promotion, personalization, and evaluation receipts | `SocioProphet/model-governance-ledger` | record governance receipt references and consent/provenance refs | authorize training, personalization, promotion, or provider use locally |
| `RuntimeAdapter` | request runtime plan or activation decision | `SocioProphet/agentplane` for execution/evidence/replay; runtime substrate decisions may reference `SourceOS-Linux/agent-machine` through Agentplane-owned plans | describe runtime need and consume runtime decision | launch daemons, open sockets, start containers, execute shell |
| `ToolAdapter` | request or observe tool-use envelope | `SocioProphet/agentplane` | record requested tool, trust level, grant ref, policy ref, and summarized observation | execute live tools in M1 or treat tool output as trusted instruction |
| `MemoryAdapter` | propose memory handling | `SocioProphet/model-governance-ledger` for consent/governance records; `SocioProphet/policy-fabric` for admission | emit memory proposal, source, trust level, and review state | auto-promote untrusted observations or persist private data |
| `EvidenceAdapter` | emit Agentplane-compatible evidence stubs | `SocioProphet/agentplane` for evidence/replay surface; `SocioProphet/sherlock-search` may supply evidence content and diagnostics | emit evidence summaries, source refs, hashes, replay refs | claim final truth or admit evidence without provenance |
| `WorkspaceAdapter` | bind run to workspace lock/topology constraints | `SocioProphet/sociosphere` | read workspace constraints and include refs in trace | change topology, locks, registry, or repo roles |
| `SchemaAdapter` | request contract/schema validation or resolve canonical schema refs | `SourceOS-Linux/sourceos-spec`; Ontogenesis contributes semantic vocabulary and draft contract work before promotion | record schema refs and validation result refs | promote local draft schemas to canonical contracts |
| `ApprovalAdapter` | request operator approval when policy requires it | local operator / enterprise approval lane as required by `SocioProphet/policy-fabric` | record approval class, request, and result | fabricate approval or downgrade approval class |
| `BenchmarkAdapter` | evaluate deterministic local assertions | Superconscious test suite, then downstream CI | assert artifact presence and invariant compliance | treat benchmark success as policy approval |

## Trust-surface obligations

Any future adapter that adds real authority must update `TRUST_SURFACE.yaml` before landing.

Authority changes include:

- adding entrypoints
- adding background services
- adding containers
- opening network listeners
- allowing egress
- writing outside `.runs/`
- reading secrets or credentials
- invoking shell, browser, terminal, or external tools
- calling live model providers
- persisting memory
- modifying workspace topology

## M1 restriction

M1 remains deterministic and inert:

- no network calls
- no model calls
- no host mutation
- no credential access
- no shell execution
- no browser automation
- local JSON/JSONL artifacts only

Changes to the M1 runner require a review issue before implementation.

## Cybernetic loop placement

For the deployable cybernetic loop v0, Superconscious should only orchestrate and record:

```text
TaskInput
  -> evidence request / evidence reference
  -> schema-validation request / result reference
  -> action-proposal request
  -> policy-decision request / result reference
  -> runtime-trace reference
  -> audit-event reference
  -> replay plan
  -> benchmark result
```

The final authority remains distributed:

- Evidence/replay surface: `SocioProphet/agentplane`
- Evidence content and diagnostics: `SocioProphet/sherlock-search`
- Schema authority: `SourceOS-Linux/sourceos-spec`
- Semantic vocabulary and schema drafting before promotion: `SocioProphet/ontogenesis`
- Action proposal and runtime trace: `SocioProphet/agentplane`
- Policy decision / cancellation / admission: `SocioProphet/policy-fabric`
- Model governance, consent, attribution, and audit: `SocioProphet/model-governance-ledger`
- Routing: `SocioProphet/model-router`
- Workspace topology and registry: `SocioProphet/sociosphere`

## Review checklist

Before adding or modifying an adapter, check:

1. Does the adapter introduce new authority?
2. Is that authority already declared in `TRUST_SURFACE.yaml`?
3. Is there a mock implementation for deterministic tests?
4. Does the trace include policy decision, trust level, grant reference, and source provenance?
5. Could the adapter leak secrets, private data, prompts, memory, or raw chain-of-thought?
6. Does the adapter preserve fail-closed behavior on missing policy, missing grants, or unknown trust level?
7. Is the final authority repository clearly named using the plane ownership vocabulary above?

## Non-goals

This document does not implement any adapter.

This document does not change the M1 runner.

This document does not promote local schemas to canonical contracts.

This document does not authorize external tool execution, browser automation, terminal execution, model calls, memory promotion, or network egress.
