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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUNS_DIR = REPO_ROOT / ".runs"


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


def build_events(ctx: RunContext, task: Dict[str, Any]) -> List[Dict[str, Any]]:
    agent = task.get("agent", {})
    workspace = task.get("workspace", {})
    policy = task.get("policy", {})
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
            "reasoning.policy.checked",
            "Checked M1 inert policy posture.",
            index=2,
            decision="allowed-safe-deterministic-mode",
            policy=policy,
        ),
        make_event(
            ctx,
            "reasoning.model.routed",
            "Selected deterministic stub model route.",
            index=3,
            route={
                "routeId": "urn:srcos:model-route:deterministic-stub",
                "provider": "none",
                "modelCalls": "denied",
                "promptEgress": "denied",
            },
        ),
        make_event(
            ctx,
            "reasoning.skill.activated",
            "Activated built-in basic-planner skill.",
            index=4,
            skill={
                "id": "urn:socioprophet:skill:superconscious-basic-planner",
                "mode": "deterministic-local",
                "sideEffects": "none",
            },
        ),
        make_event(
            ctx,
            "reasoning.tool.observed",
            "Simulated local summarization tool result.",
            index=5,
            tool={
                "id": "urn:socioprophet:tool:mock-summarizer",
                "sideEffectClass": "none",
                "network": "none",
            },
            observation={
                "summary": "Superconscious coordinates governed recursive agency through safe operational traces and evidence-backed replay.",
                "objectiveHash": stable_hash(objective),
            },
        ),
        make_event(
            ctx,
            "reasoning.memory.proposed",
            "Proposed non-promoted memory note for operator review.",
            index=6,
            memoryDecision={
                "decision": "proposal-only",
                "durableWrite": False,
                "reason": "M1 does not auto-promote memory.",
            },
        ),
        make_event(
            ctx,
            "reasoning.evidence.emitted",
            "Emitted local AgentPlane-compatible evidence stub.",
            index=7,
            evidenceRefs=["agentplane-evidence.json"],
        ),
        make_event(
            ctx,
            "reasoning.run.completed",
            "Completed deterministic Superconscious run.",
            index=8,
            status="completed",
        ),
    ]


def build_reasoning_run(ctx: RunContext, task: Dict[str, Any], events: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        "events": events,
        "artifactRefs": {
            "events": "events.jsonl",
            "agentplaneEvidence": "agentplane-evidence.json",
            "replayPlan": "replay-plan.json",
            "benchmarkResult": "benchmark-result.json",
        },
    }


def build_agentplane_evidence(ctx: RunContext, task: Dict[str, Any], events: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        "replayClass": task.get("expected", {}).get("replayClass", "exact"),
        "emittedAt": utc_now(),
    }


def build_replay_plan(ctx: RunContext, task: Dict[str, Any]) -> Dict[str, Any]:
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
        "command": f"python3 packages/superconscious-core/superconscious_core/runner.py {ctx.task_path}",
    }


def build_benchmark_result(ctx: RunContext, task: Dict[str, Any], run_artifact: Dict[str, Any]) -> Dict[str, Any]:
    required = task.get("expected", {}).get("requiredArtifacts", [])
    missing = [name for name in required if not (ctx.run_dir / name).exists()]
    assertions = [
        {"name": "run-completed", "passed": run_artifact.get("status") == "completed"},
        {"name": "safe-trace-only", "passed": run_artifact.get("safeTrace", {}).get("rawChainOfThought") == "not-collected"},
        {"name": "required-artifacts-present", "passed": not missing, "missing": missing},
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


def run(task_path: Path, out_dir: Path | None = None) -> Path:
    task_path = task_path.resolve()
    task = load_json(task_path)
    task_hash = stable_hash(task)
    run_id = f"urn:srcos:reasoning-run:{task_hash[:24]}"
    run_dir = (out_dir or DEFAULT_RUNS_DIR) / task_hash[:24]
    started_at = utc_now()
    ctx = RunContext(run_id=run_id, run_dir=run_dir, task_path=task_path, task_hash=task_hash, started_at=started_at)

    events = build_events(ctx, task)
    write_jsonl(run_dir / "events.jsonl", events)

    reasoning_run = build_reasoning_run(ctx, task, events)
    write_json(run_dir / "reasoning-run.json", reasoning_run)

    agentplane_evidence = build_agentplane_evidence(ctx, task, events)
    write_json(run_dir / "agentplane-evidence.json", agentplane_evidence)

    replay_plan = build_replay_plan(ctx, task)
    write_json(run_dir / "replay-plan.json", replay_plan)

    benchmark_result = build_benchmark_result(ctx, task, reasoning_run)
    write_json(run_dir / "benchmark-result.json", benchmark_result)

    if not benchmark_result["passed"]:
        raise RuntimeError(f"benchmark failed for {ctx.run_id}: {benchmark_result}")

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
