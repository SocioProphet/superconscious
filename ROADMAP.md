# Superconscious Roadmap

## M1 — Deterministic governed loop foundation

Goal: prove the loop, trace, evidence, replay, and benchmark shape without network, model calls, browser automation, shell execution, or host mutation.

Deliverables:

- repo charter and authority boundaries;
- safe operational trace doctrine;
- threat model;
- deterministic example task;
- local runner that emits five artifacts;
- mock adapters for policy, model route, skill, tool, memory, evidence, and benchmark;
- tests for artifact generation.

Exit criteria:

```text
python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json
```

emits:

```text
.runs/<run-id>/events.jsonl
.runs/<run-id>/reasoning-run.json
.runs/<run-id>/agentplane-evidence.json
.runs/<run-id>/replay-plan.json
.runs/<run-id>/benchmark-result.json
```

## M1.5 — Governed cognition loop over Workspace Operations

Goal: integrate the six required cognition operation types that make Superconscious the
governed cognition/reflection loop for recursive agents (SocioProphet/superconscious#1).

Deliverables:

- `cognition_loop.py` — governed cognition loop with read/reflect/propose posture;
- six mock adapters: `WorkspaceOperationObserve`, `Reflection`, `RemediationProposal`,
  `LearningLoop`, `RiskSignal`, `PolicyReview`;
- eight typed artifacts per run: events, run, reflection, remediation proposal, risk signal,
  policy review request, learning loop record, benchmark;
- deterministic example task (`examples/workspace-operation-observe/task.json`);
- `schemas/cognition-operation.draft.schema.json` local draft schema;
- 20 new tests covering posture invariants, provenance, admission state, and adapter inertness.

Exit criteria:

```text
python3 packages/superconscious-core/superconscious_core/cognition_loop.py examples/workspace-operation-observe/task.json
```

emits:

```text
.runs/<run-id>/cognition-events.jsonl
.runs/<run-id>/cognition-run.json
.runs/<run-id>/cognition-reflection.json
.runs/<run-id>/cognition-remediation-proposal.json
.runs/<run-id>/cognition-risk-signal.json
.runs/<run-id>/cognition-policy-review-request.json
.runs/<run-id>/cognition-learning-loop-record.json
.runs/<run-id>/cognition-benchmark-result.json
```

Constraints maintained:

- Loop is read/reflect/propose; `directMutation` is always `false`.
- Remediation routes through AgentPlane / OperationContract only.
- All artifacts carry provenance and `admissionState: proposed`.
- Risk signals and remediation proposals are auditable (ledger-facing).
- M1 posture: no network, no model calls, no host mutation.

## M2 — Contract promotion

- Promote local draft artifact shapes into `SourceOS-Linux/sourceos-spec`.
- Add examples and schema validation.
- Add AsyncAPI event fragments.
- Add JSON-LD vocabulary terms.
- Update Superconscious to consume generated/validated contract types.

## M3 — AgentPlane evidence integration

- Add AgentPlane-compatible `ReasoningRunArtifact` emission.
- Add replay pointer compatibility.
- Add bundle integration example.
- Add AgentPlane adapter tests.

## M4 — Policy, grants, and model routing adapters

- Integrate Guardrail Fabric / Policy Fabric admission adapter.
- Integrate Agent Registry grant adapter.
- Integrate Model Router route adapter.
- Preserve mock adapters for deterministic local tests.

## M5 — Runtime planning and product surfaces

- Integrate Agent Machine runtime-plan adapter.
- Add `sourceosctl reasoning inspect` target in `sourceos-devtools`.
- Add TurtleTerm / AgentTerm trace tree semantics.
- Add BearBrowser sidecar trace semantics.

## M6 — Benchmarks and red-team fixtures

- Browser task smoke suite.
- Terminal task smoke suite.
- Policy denial suite.
- Memory quarantine suite.
- MCP trust suite.
- Source exposure leak suite.

## M7 — Opt-in personalization lane

- Integrate Socios dry-run orchestration.
- Reference model-governance-ledger consent receipts.
- Add before/after evaluation receipt shape.
- Keep all personalization off by default.
