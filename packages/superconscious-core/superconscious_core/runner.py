#!/usr/bin/env python3
"""Deterministic Superconscious M1 runner.

This runner is intentionally inert:
- no network calls;
- no model calls;
- no shell execution;
- no browser automation;
- no writes outside .runs/ unless --out-dir is provided explicitly.
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
        MockAgentGrantAdapter,
        MockApprovalAdapter,
        MockBenchmarkAdapter,
        MockEvidenceAdapter,
        MockMemoryAdapter,
        MockModelRouteAdapter,
        MockPolicyAdapter,
        MockSkillAdapter,
        MockToolAdapter,
        MockWorkspaceAdapter,
    )
except ImportError:  # pragma: no cover - direct script execution path
    from adapters import (  # type: ignore
        AdapterDecision,
        MockAgentGrantAdapter,
        MockApprovalAdapter,
        MockBenchmarkAdapter,
        MockEvidenceAdapter,
        MockMemoryAdapter,
        MockModelRouteAdapter,
        MockPolicyAdapter,
        MockSkillAdapter,
        MockToolAdapter,
        MockWorkspaceAdapter,
    )


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / ".runs"
SELF_EMITTED_ARTIFACTS = {"benchmark-result.json"}


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
class RunContext:
    run_id: str
    run_dir: Path
    task_path: Path
    task_hash: str
    started_at: str


@dataclass(frozen=True)
class AdapterSet:
    workspace: MockWorkspaceAdapter
    grants: MockAgentGrantAdapter
    policy: MockPolicyAdapter
    model_route: MockModelRouteAdapter
    skill: MockSkillAdapter
    tool: MockToolAdapter
    memory: MockMemoryAdapter
    evidence: MockEvidenceAdapter
    benchmark: MockBenchmarkAdapter
    approval: MockApprovalAdapter


@dataclass(frozen=True)
class AdapterTrace:
    workspace: AdapterDecision
    grants: AdapterDecision
    policy: AdapterDecision
    model_route: AdapterDecision
    skill: AdapterDecision
    tool: AdapterDecision
    memory: AdapterDecision
    evidence: AdapterDecision
    approval: AdapterDecision


def default_adapters() -> AdapterSet:
    return AdapterSet(
        workspace=MockWorkspaceAdapter(),
        grants=MockAgentGrantAdapter(),
        policy=MockPolicyAdapter(),
        model_route=MockModelRouteAdapter(),
        skill=MockSkillAdapter(),
        tool=MockToolAdapter(),
        memory=MockMemoryAdapter(),
        evidence=MockEvidenceAdapter(),
        benchmark=MockBenchmarkAdapter(),
        approval=MockApprovalAdapter(),
    )


def as_event_evidence(decision: AdapterDecision) -> Dict[str, Any]:
    return asdict(decision)


def make_event(ctx: RunContext, event_type: str, summary: str, **fields: Any) -> Dict[str, Any]:
    index = fields.pop("index", 0)
    event_seed = {"runId": ctx.run_id, "type": event_type, "summary": summary, "index": index}
    return {
        "eventId": f"urn:srcos:reasoning-event:{stable_hash(event_seed)[:24]}",
        "runId": ctx.run_id,
        "type": event_type,
        "occurredAt": utc_now(),
        "summary": summary,
        "traceLevel": fields.pop("traceLevel", "public-safe"),
        "trustLevel": fields.pop("trustLevel", "trusted-control-input"),
        **fields,
    }


def collect_adapter_trace(
    task: Dict[str, Any], run_id: str, adapters: AdapterSet | None = None
) -> AdapterTrace:
    adapter_set = adapters or default_adapters()
    workspace = adapter_set.workspace.bind_workspace(task)
    grants = adapter_set.grants.resolve_grants(task)
    policy = adapter_set.policy.check(task, "deterministic-local-run", {"runId": run_id})
    model_route = adapter_set.model_route.route(task, "reference-loop-demo")
    skill = adapter_set.skill.activate(task, "urn:socioprophet:skill:superconscious-basic-planner")
    tool = adapter_set.tool.observe(task, "urn:socioprophet:tool:mock-summarizer")
    memory = adapter_set.memory.decide(task, tool.evidence)
    evidence = adapter_set.evidence.emit(
        run_id,
        ["events.jsonl", "reasoning-run.json", "agentplane-evidence.json", "replay-plan.json"],
    )
    approval = adapter_set.approval.request(
        task,
        "none",
        "M1 deterministic local run has no network, model calls, host mutation, or durable memory write.",
    )
    return AdapterTrace(
        workspace=workspace,
        grants=grants,
        policy=policy,
        model_route=model_route,
        skill=skill,
        tool=tool,
        memory=memory,
        evidence=evidence,
        approval=approval,
    )


def build_events(ctx: RunContext, task: Dict[str, Any], trace: AdapterTrace) -> List[Dict[str, Any]]:
    agent = task.get("agent", {})
    workspace = task.get("workspace", {})
    objective = task.get("objective", "")

    return [
        make_event(
            ctx,
            "reasoning.run.created",
            "Created deterministic Superconscious run.",
            index=1,
            taskId=task.get("taskId"),
            taskHash=ctx.task_hash,
            agentId=agent.get("id"),
            workspaceId=workspace.get("id"),
        ),
        make_event(
            ctx,
            "reasoning.workspace.bound",
            trace.workspace.summary,
            index=2,
            workspace=as_event_evidence(trace.workspace),
        ),
        make_event(
            ctx,
            "reasoning.grants.resolved",
            trace.grants.summary,
            index=3,
            grants=as_event_evidence(trace.grants),
        ),
        make_event(
            ctx,
            "reasoning.policy.checked",
            trace.policy.summary,
            index=4,
            policy=as_event_evidence(trace.policy),
        ),
        make_event(
            ctx,
            "reasoning.model.routed",
            trace.model_route.summary,
            index=5,
            route=as_event_evidence(trace.model_route),
        ),
        make_event(
            ctx,
            "reasoning.skill.activated",
            trace.skill.summary,
            index=6,
            skill=as_event_evidence(trace.skill),
        ),
        make_event(
            ctx,
            "reasoning.tool.observed",
            trace.tool.summary,
            index=7,
            tool=as_event_evidence(trace.tool),
            observation={
                "summary": trace.tool.evidence.get("observation"),
                "objectiveHash": stable_hash(objective),
            },
        ),
        make_event(
            ctx,
            "reasoning.memory.proposed",
            trace.memory.summary,
            index=8,
            memoryDecision=as_event_evidence(trace.memory),
        ),
        make_event(
            ctx,
            "reasoning.approval.checked",
            trace.approval.summary,
            index=9,
            approval=as_event_evidence(trace.approval),
        ),
        make_event(
            ctx,
            "reasoning.evidence.emitted",
            trace.evidence.summary,
            index=10,
            evidence=as_event_evidence(trace.evidence),
            evidenceRefs=["agentplane-evidence.json"],
        ),
        make_event(
            ctx,
            "reasoning.run.completed",
            "Completed deterministic Superconscious run.",
            index=11,
            status="completed",
        ),
    ]


def build_reasoning_run(
    ctx: RunContext, task: Dict[str, Any], events: List[Dict[str, Any]], trace: AdapterTrace
) -> Dict[str, Any]:
    completed_at = utc_now()
    return {
        "kind": "ReasoningRun",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "status": "completed",
        "startedAt": ctx.started_at,
        "completedAt": completed_at,
        "task": {
            "taskId": task.get("taskId"),
            "title": task.get("title"),
            "objectiveHash": stable_hash(task.get("objective", "")),
        },
        "agent": task.get("agent", {}),
        "workspace": task.get("workspace", {}),
        "safeTrace": {
            "mode": "operational-trace-only",
            "rawChainOfThought": "not-collected",
            "eventCount": len(events),
        },
        "adapterTrace": {
            "workspace": as_event_evidence(trace.workspace),
            "grants": as_event_evidence(trace.grants),
            "policy": as_event_evidence(trace.policy),
            "modelRoute": as_event_evidence(trace.model_route),
            "skill": as_event_evidence(trace.skill),
            "tool": as_event_evidence(trace.tool),
            "memory": as_event_evidence(trace.memory),
            "approval": as_event_evidence(trace.approval),
            "evidence": as_event_evidence(trace.evidence),
        },
        "events": events,
        "artifactRefs": {
            "events": "events.jsonl",
            "agentplaneEvidence": "agentplane-evidence.json",
            "replayPlan": "replay-plan.json",
            "benchmarkResult": "benchmark-result.json",
        },
    }


def build_agentplane_evidence(
    ctx: RunContext, task: Dict[str, Any], events: List[Dict[str, Any]], trace: AdapterTrace
) -> Dict[str, Any]:
    return {
        "kind": "AgentPlaneReasoningEvidence",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "taskId": task.get("taskId"),
        "taskHash": ctx.task_hash,
        "status": "completed",
        "sideEffects": "none",
        "network": "none",
        "modelCalls": "none",
        "hostMutation": "none",
        "eventStreamHash": stable_hash(events),
        "policyDecision": trace.policy.decision,
        "modelRouteDecision": trace.model_route.decision,
        "memoryDecision": trace.memory.decision,
        "approvalDecision": trace.approval.decision,
        "replayClass": task.get("expected", {}).get("replayClass", "exact"),
        "emittedAt": utc_now(),
    }


def build_replay_plan(ctx: RunContext, task: Dict[str, Any], trace: AdapterTrace) -> Dict[str, Any]:
    return {
        "kind": "ReplayPlan",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "replayClass": task.get("expected", {}).get("replayClass", "exact"),
        "inputs": {
            "taskPath": str(ctx.task_path),
            "taskHash": ctx.task_hash,
            "mode": "deterministic-local",
        },
        "constraints": {
            "network": "denied",
            "modelCalls": "denied",
            "hostMutation": "denied",
        },
        "adapterReplay": {
            "workspace": trace.workspace.decision,
            "grants": trace.grants.decision,
            "policy": trace.policy.decision,
            "modelRoute": trace.model_route.decision,
            "skill": trace.skill.decision,
            "tool": trace.tool.decision,
            "memory": trace.memory.decision,
            "approval": trace.approval.decision,
        },
        "command": f"python3 packages/superconscious-core/superconscious_core/runner.py {ctx.task_path}",
    }


def build_benchmark_result(ctx: RunContext, task: Dict[str, Any], run_artifact: Dict[str, Any]) -> Dict[str, Any]:
    required = task.get("expected", {}).get("requiredArtifacts", [])
    missing = [
        name
        for name in required
        if name not in SELF_EMITTED_ARTIFACTS and not (ctx.run_dir / name).exists()
    ]
    assertions = [
        {"name": "run-completed", "passed": run_artifact.get("status") == "completed"},
        {
            "name": "safe-trace-only",
            "passed": run_artifact.get("safeTrace", {}).get("rawChainOfThought") == "not-collected",
        },
        {
            "name": "adapter-trace-present",
            "passed": bool(run_artifact.get("adapterTrace", {}).get("policy")),
        },
        {"name": "required-prior-artifacts-present", "passed": not missing, "missing": missing},
        {
            "name": "benchmark-result-self-emitted",
            "passed": "benchmark-result.json" in required,
            "note": "benchmark-result.json is validated by write/readback after emission",
        },
    ]
    return {
        "kind": "BenchmarkResult",
        "specVersion": "0.1.0-draft",
        "runId": ctx.run_id,
        "suite": "m1-deterministic-smoke",
        "passed": all(item["passed"] for item in assertions),
        "assertions": assertions,
        "evaluatedAt": utc_now(),
    }


def run(task_path: Path, out_dir: Path | None = None, adapters: AdapterSet | None = None) -> Path:
    task_path = task_path.resolve()
    task = load_json(task_path)
    task_hash = stable_hash(task)
    run_id = f"urn:srcos:reasoning-run:{task_hash[:24]}"
    run_dir = (out_dir or DEFAULT_RUNS_DIR) / task_hash[:24]
    started_at = utc_now()
    ctx = RunContext(
        run_id=run_id,
        run_dir=run_dir,
        task_path=task_path,
        task_hash=task_hash,
        started_at=started_at,
    )

    trace = collect_adapter_trace(task, run_id, adapters)
    events = build_events(ctx, task, trace)
    write_jsonl(run_dir / "events.jsonl", events)

    reasoning_run = build_reasoning_run(ctx, task, events, trace)
    write_json(run_dir / "reasoning-run.json", reasoning_run)

    agentplane_evidence = build_agentplane_evidence(ctx, task, events, trace)
    write_json(run_dir / "agentplane-evidence.json", agentplane_evidence)

    replay_plan = build_replay_plan(ctx, task, trace)
    write_json(run_dir / "replay-plan.json", replay_plan)

    benchmark_result = build_benchmark_result(ctx, task, reasoning_run)
    write_json(run_dir / "benchmark-result.json", benchmark_result)

    benchmark_result_readback = load_json(run_dir / "benchmark-result.json")
    if not benchmark_result_readback["passed"]:
        raise RuntimeError(f"benchmark failed for {ctx.run_id}: {benchmark_result_readback}")

    return run_dir


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a deterministic Superconscious M1 task.")
    parser.add_argument("task", type=Path, help="Path to task.json")
    parser.add_argument("--out-dir", type=Path, default=None, help="Optional output directory for run artifacts")
    args = parser.parse_args(argv)

    try:
        run_dir = run(args.task, args.out_dir)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"superconscious runner failed: {exc}", file=sys.stderr)
        return 1

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
