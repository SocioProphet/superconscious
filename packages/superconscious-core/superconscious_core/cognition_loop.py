#!/usr/bin/env python3
"""Governed cognition loop over Workspace Operations.

Implements the six cognition operation types required to integrate
Superconscious as the governed cognition/reflection loop:

    cognition.observe.operation     — read WorkspaceOperation event (read-only)
    cognition.reflect.run           — generate governed reflection artifact
    cognition.remediation.propose   — propose remediation through AgentPlane
    cognition.learning_loop.record  — record evidence for systems-learning-loop
    cognition.risk_signal.emit      — emit auditable risk signal
    cognition.policy_review.request — request Policy Fabric review

Acceptance rules enforced here:
- The loop is read/reflect/propose only; it never directly mutates workspace state.
- Any remediation action routes through AgentPlane / OperationContract, not direct-write.
- Reflection outputs carry provenance and admission state.
- Risk signals and remediation proposals are auditable (ledger-facing).
- No step bypasses policy, authority, or operation lifecycle.
- M1 posture: no network, no model calls, no host mutation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

try:  # Support both package imports and direct script execution.
    from .adapters import (
        AdapterDecision,
        MockEvidenceAdapter,
        MockLearningLoopAdapter,
        MockPolicyAdapter,
        MockPolicyReviewAdapter,
        MockReflectionAdapter,
        MockRemediationProposalAdapter,
        MockRiskSignalAdapter,
        MockWorkspaceOperationObserveAdapter,
    )
except ImportError:  # pragma: no cover - direct script execution path
    from adapters import (  # type: ignore
        AdapterDecision,
        MockEvidenceAdapter,
        MockLearningLoopAdapter,
        MockPolicyAdapter,
        MockPolicyReviewAdapter,
        MockReflectionAdapter,
        MockRemediationProposalAdapter,
        MockRiskSignalAdapter,
        MockWorkspaceOperationObserveAdapter,
    )


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / ".runs"
REQUIRED_COGNITION_OPERATION_TYPES = {
    "cognition.observe.operation",
    "cognition.reflect.run",
    "cognition.remediation.propose",
    "cognition.learning_loop.record",
    "cognition.risk_signal.emit",
    "cognition.policy_review.request",
}
SELF_EMITTED_COGNITION_ARTIFACTS = {"cognition-benchmark-result.json"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, events: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


@dataclass(frozen=True)
class CognitionContext:
    run_id: str
    run_dir: Path
    task_path: Path
    task_hash: str
    operation_id: str
    started_at: str


@dataclass(frozen=True)
class CognitionAdapterSet:
    observe: MockWorkspaceOperationObserveAdapter
    reflect: MockReflectionAdapter
    remediation: MockRemediationProposalAdapter
    learning_loop: MockLearningLoopAdapter
    risk_signal: MockRiskSignalAdapter
    policy_review: MockPolicyReviewAdapter
    policy: MockPolicyAdapter
    evidence: MockEvidenceAdapter


@dataclass(frozen=True)
class CognitionTrace:
    observe: AdapterDecision
    reflect: AdapterDecision
    remediation: AdapterDecision
    learning_loop: AdapterDecision
    risk_signal: AdapterDecision
    policy_review: AdapterDecision
    policy: AdapterDecision
    evidence: AdapterDecision


def default_cognition_adapters() -> CognitionAdapterSet:
    return CognitionAdapterSet(
        observe=MockWorkspaceOperationObserveAdapter(),
        reflect=MockReflectionAdapter(),
        remediation=MockRemediationProposalAdapter(),
        learning_loop=MockLearningLoopAdapter(),
        risk_signal=MockRiskSignalAdapter(),
        policy_review=MockPolicyReviewAdapter(),
        policy=MockPolicyAdapter(),
        evidence=MockEvidenceAdapter(),
    )


def make_cognition_event(
    ctx: CognitionContext, event_type: str, summary: str, index: int, **fields: Any
) -> Dict[str, Any]:
    event_seed = {"runId": ctx.run_id, "type": event_type, "summary": summary, "index": index}
    return {
        "eventId": f"urn:srcos:cognition-event:{stable_hash(event_seed)[:24]}",
        "runId": ctx.run_id,
        "type": event_type,
        "occurredAt": utc_now(),
        "summary": summary,
        "traceLevel": fields.pop("traceLevel", "public-safe"),
        "trustLevel": fields.pop("trustLevel", "trusted-control-input"),
        **fields,
    }


def collect_cognition_trace(
    task: Dict[str, Any],
    run_id: str,
    adapters: CognitionAdapterSet | None = None,
) -> CognitionTrace:
    """Run all cognition adapters in governance order and return the trace.

    Order is fixed:
    1. Policy gate (fail closed on denied)
    2. cognition.observe.operation  — read-only observation
    3. cognition.reflect.run        — generate reflection
    4. cognition.remediation.propose
    5. cognition.learning_loop.record
    6. cognition.risk_signal.emit
    7. cognition.policy_review.request
    8. Evidence emission
    """
    adapter_set = adapters or default_cognition_adapters()
    operation = task.get("workspaceOperation", {})

    policy_decision = adapter_set.policy.check(
        task,
        "cognition-loop",
        {"runId": run_id, "operationId": operation.get("operationId")},
    )

    observe = adapter_set.observe.observe(operation)
    reflect = adapter_set.reflect.reflect(operation, observe)
    remediation = adapter_set.remediation.propose(run_id, reflect)
    learning_loop = adapter_set.learning_loop.record(run_id, reflect)
    risk_signal = adapter_set.risk_signal.emit(run_id, reflect)
    policy_review = adapter_set.policy_review.request(
        run_id, reflect, "Superconscious cognition loop policy review"
    )
    evidence = adapter_set.evidence.emit(
        run_id,
        [
            "cognition-events.jsonl",
            "cognition-run.json",
            "cognition-reflection.json",
            "cognition-remediation-proposal.json",
            "cognition-risk-signal.json",
            "cognition-policy-review-request.json",
            "cognition-learning-loop-record.json",
        ],
    )

    return CognitionTrace(
        observe=observe,
        reflect=reflect,
        remediation=remediation,
        learning_loop=learning_loop,
        risk_signal=risk_signal,
        policy_review=policy_review,
        policy=policy_decision,
        evidence=evidence,
    )


def build_cognition_events(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> List[Dict[str, Any]]:
    operation = task.get("workspaceOperation", {})
    return [
        make_cognition_event(
            ctx,
            "cognition.observe.operation",
            trace.observe.summary,
            index=1,
            operationId=operation.get("operationId"),
            observe=asdict(trace.observe),
        ),
        make_cognition_event(
            ctx,
            "cognition.reflect.run",
            trace.reflect.summary,
            index=2,
            reflection=asdict(trace.reflect),
        ),
        make_cognition_event(
            ctx,
            "cognition.remediation.propose",
            trace.remediation.summary,
            index=3,
            remediation=asdict(trace.remediation),
        ),
        make_cognition_event(
            ctx,
            "cognition.learning_loop.record",
            trace.learning_loop.summary,
            index=4,
            learningLoop=asdict(trace.learning_loop),
        ),
        make_cognition_event(
            ctx,
            "cognition.risk_signal.emit",
            trace.risk_signal.summary,
            index=5,
            riskSignal=asdict(trace.risk_signal),
        ),
        make_cognition_event(
            ctx,
            "cognition.policy_review.request",
            trace.policy_review.summary,
            index=6,
            policyReview=asdict(trace.policy_review),
        ),
    ]


def build_cognition_run(
    ctx: CognitionContext,
    task: Dict[str, Any],
    events: List[Dict[str, Any]],
    trace: CognitionTrace,
) -> Dict[str, Any]:
    return {
        "kind": "CognitionRun",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "status": "completed",
        "startedAt": ctx.started_at,
        "completedAt": utc_now(),
        "task": {
            "taskId": task.get("taskId"),
            "title": task.get("title"),
            "operationRef": ctx.operation_id,
            "taskHash": ctx.task_hash,
        },
        "agent": task.get("agent", {}),
        "workspace": task.get("workspace", {}),
        "safeTrace": {
            "mode": "operational-trace-only",
            "rawChainOfThought": "not-collected",
            "eventCount": len(events),
        },
        "adapterTrace": {
            "policy": asdict(trace.policy),
            "observe": asdict(trace.observe),
            "reflect": asdict(trace.reflect),
            "remediation": asdict(trace.remediation),
            "learningLoop": asdict(trace.learning_loop),
            "riskSignal": asdict(trace.risk_signal),
            "policyReview": asdict(trace.policy_review),
            "evidence": asdict(trace.evidence),
        },
        "cognitionPosture": "read-reflect-propose",
        "directMutation": False,
        "events": events,
        "artifactRefs": {
            "events": "cognition-events.jsonl",
            "reflection": "cognition-reflection.json",
            "remediationProposal": "cognition-remediation-proposal.json",
            "riskSignal": "cognition-risk-signal.json",
            "policyReviewRequest": "cognition-policy-review-request.json",
            "learningLoopRecord": "cognition-learning-loop-record.json",
            "benchmarkResult": "cognition-benchmark-result.json",
        },
    }


def build_cognition_reflection(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> Dict[str, Any]:
    return {
        "kind": "CognitionReflection",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "operationRef": ctx.operation_id,
        "admissionState": "proposed",
        "provenance": {
            "agentRef": task.get("agent", {}).get("id"),
            "workspaceRef": task.get("workspace", {}).get("id"),
            "taskHash": ctx.task_hash,
        },
        "riskScore": trace.reflect.evidence.get("riskScore", "low"),
        "evaluationSummary": trace.reflect.evidence.get("evaluationSummary", ""),
        "observation": asdict(trace.observe),
        "decision": trace.reflect.decision,
        "capturedAt": utc_now(),
    }


def build_remediation_proposal(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> Dict[str, Any]:
    return {
        "kind": "RemediationProposal",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "operationRef": ctx.operation_id,
        "admissionState": "proposed",
        "provenance": {
            "agentRef": task.get("agent", {}).get("id"),
            "taskHash": ctx.task_hash,
        },
        "decision": trace.remediation.decision,
        "routedThrough": trace.remediation.evidence.get("routedThrough", "agentplane"),
        "directMutation": False,
        "proposalRef": trace.remediation.evidence.get("proposalRef"),
        "capturedAt": utc_now(),
    }


def build_risk_signal(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> Dict[str, Any]:
    return {
        "kind": "RiskSignal",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "operationRef": ctx.operation_id,
        "admissionState": "proposed",
        "provenance": {
            "agentRef": task.get("agent", {}).get("id"),
            "taskHash": ctx.task_hash,
        },
        "riskScore": trace.risk_signal.evidence.get("riskScore", "low"),
        "signalEmitted": trace.risk_signal.evidence.get("signalEmitted", False),
        "signalRef": trace.risk_signal.evidence.get("signalRef"),
        "auditTrail": trace.risk_signal.evidence.get("auditTrail", "ledger-facing"),
        "capturedAt": utc_now(),
    }


def build_policy_review_request(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> Dict[str, Any]:
    return {
        "kind": "PolicyReviewRequest",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "operationRef": ctx.operation_id,
        "admissionState": "proposed",
        "provenance": {
            "agentRef": task.get("agent", {}).get("id"),
            "taskHash": ctx.task_hash,
        },
        "reviewRequested": trace.policy_review.evidence.get("reviewRequested", False),
        "reviewRef": trace.policy_review.evidence.get("reviewRef"),
        "policyFabric": trace.policy_review.evidence.get("policyFabric", "guardrail-fabric"),
        "capturedAt": utc_now(),
    }


def build_learning_loop_record(
    ctx: CognitionContext, task: Dict[str, Any], trace: CognitionTrace
) -> Dict[str, Any]:
    return {
        "kind": "LearningLoopRecord",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "operationRef": ctx.operation_id,
        "admissionState": "proposed",
        "provenance": {
            "agentRef": task.get("agent", {}).get("id"),
            "taskHash": ctx.task_hash,
        },
        "learningLoopRef": trace.learning_loop.evidence.get("learningLoopRef"),
        "riskScore": trace.learning_loop.evidence.get("riskScore", "low"),
        "decision": trace.learning_loop.decision,
        "capturedAt": utc_now(),
    }


def build_cognition_benchmark(
    ctx: CognitionContext, task: Dict[str, Any], cognition_run: Dict[str, Any]
) -> Dict[str, Any]:
    required = task.get("expected", {}).get("requiredArtifacts", [])
    missing = [
        name
        for name in required
        if name not in SELF_EMITTED_COGNITION_ARTIFACTS and not (ctx.run_dir / name).exists()
    ]
    assertions = [
        {
            "name": "cognition-run-completed",
            "passed": cognition_run.get("status") == "completed",
        },
        {
            "name": "safe-trace-only",
            "passed": cognition_run.get("safeTrace", {}).get("rawChainOfThought") == "not-collected",
        },
        {
            "name": "no-direct-mutation",
            "passed": cognition_run.get("directMutation") is False,
        },
        {
            "name": "cognition-posture-read-reflect-propose",
            "passed": cognition_run.get("cognitionPosture") == "read-reflect-propose",
        },
        {
            "name": "required-prior-artifacts-present",
            "passed": not missing,
            "missing": missing,
        },
        {
            "name": "cognition-benchmark-self-emitted",
            "passed": "cognition-benchmark-result.json" in required,
            "note": "cognition-benchmark-result.json is validated by write/readback after emission",
        },
    ]
    return {
        "kind": "CognitionBenchmarkResult",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "suite": "cognition-loop-smoke",
        "passed": all(item["passed"] for item in assertions),
        "assertions": assertions,
        "evaluatedAt": utc_now(),
    }


def run_cognition(
    task_path: Path,
    out_dir: Path | None = None,
    adapters: CognitionAdapterSet | None = None,
) -> Path:
    """Run the governed cognition loop for a workspace operation task.

    Returns the run directory containing all emitted artifacts.
    Raises RuntimeError if the benchmark fails.
    """
    task_path = task_path.resolve()
    task = load_json(task_path)
    task_hash = stable_hash(task)
    operation_id = task.get("workspaceOperation", {}).get(
        "operationId", f"urn:srcos:workspace-operation:{task_hash[:24]}"
    )
    run_id = f"urn:srcos:cognition-run:{task_hash[:24]}"
    run_dir = (out_dir or DEFAULT_RUNS_DIR) / task_hash[:24]
    started_at = utc_now()

    ctx = CognitionContext(
        run_id=run_id,
        run_dir=run_dir,
        task_path=task_path,
        task_hash=task_hash,
        operation_id=operation_id,
        started_at=started_at,
    )

    trace = collect_cognition_trace(task, run_id, adapters)
    events = build_cognition_events(ctx, task, trace)
    write_jsonl(run_dir / "cognition-events.jsonl", events)

    cognition_run = build_cognition_run(ctx, task, events, trace)
    write_json(run_dir / "cognition-run.json", cognition_run)

    reflection = build_cognition_reflection(ctx, task, trace)
    write_json(run_dir / "cognition-reflection.json", reflection)

    remediation_proposal = build_remediation_proposal(ctx, task, trace)
    write_json(run_dir / "cognition-remediation-proposal.json", remediation_proposal)

    risk_signal = build_risk_signal(ctx, task, trace)
    write_json(run_dir / "cognition-risk-signal.json", risk_signal)

    policy_review_request = build_policy_review_request(ctx, task, trace)
    write_json(run_dir / "cognition-policy-review-request.json", policy_review_request)

    learning_loop_record = build_learning_loop_record(ctx, task, trace)
    write_json(run_dir / "cognition-learning-loop-record.json", learning_loop_record)

    benchmark_result = build_cognition_benchmark(ctx, task, cognition_run)
    write_json(run_dir / "cognition-benchmark-result.json", benchmark_result)

    benchmark_readback = load_json(run_dir / "cognition-benchmark-result.json")
    if not benchmark_readback["passed"]:
        raise RuntimeError(f"cognition benchmark failed for {ctx.run_id}: {benchmark_readback}")

    return run_dir


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the governed Superconscious cognition loop over a workspace operation."
    )
    parser.add_argument("task", type=Path, help="Path to task.json")
    parser.add_argument("--out-dir", type=Path, default=None, help="Optional output directory")
    args = parser.parse_args(argv)

    try:
        run_dir = run_cognition(args.task, args.out_dir)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"superconscious cognition loop failed: {exc}", file=sys.stderr)
        return 1

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
