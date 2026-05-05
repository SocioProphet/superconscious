#!/usr/bin/env python3
"""Validate Superconscious M1 run artifacts.

This validator is dependency-free and intentionally checks semantic invariants that
matter to the governed cognition loop: safe trace posture, adapter trace presence,
AgentPlane evidence consistency, replay class, and benchmark pass state.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_ARTIFACTS = [
    "events.jsonl",
    "reasoning-run.json",
    "agentplane-evidence.json",
    "replay-plan.json",
    "benchmark-result.json",
]
REQUIRED_EVENT_TYPES = {
    "reasoning.run.created",
    "reasoning.workspace.bound",
    "reasoning.grants.resolved",
    "reasoning.policy.checked",
    "reasoning.model.routed",
    "reasoning.skill.activated",
    "reasoning.tool.observed",
    "reasoning.memory.proposed",
    "reasoning.approval.checked",
    "reasoning.evidence.emitted",
    "reasoning.run.completed",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def validate_run_dir(run_dir: Path) -> List[str]:
    errors: List[str] = []
    for artifact in REQUIRED_ARTIFACTS:
        if not (run_dir / artifact).exists():
            errors.append(f"missing required artifact: {artifact}")

    if errors:
        return errors

    events = load_jsonl(run_dir / "events.jsonl")
    reasoning_run = load_json(run_dir / "reasoning-run.json")
    evidence = load_json(run_dir / "agentplane-evidence.json")
    replay = load_json(run_dir / "replay-plan.json")
    benchmark = load_json(run_dir / "benchmark-result.json")

    if reasoning_run.get("kind") != "ReasoningRun":
        errors.append("reasoning-run.json kind must be ReasoningRun")
    if reasoning_run.get("status") != "completed":
        errors.append("reasoning-run.json status must be completed")
    if reasoning_run.get("safeTrace", {}).get("rawChainOfThought") != "not-collected":
        errors.append("safeTrace.rawChainOfThought must be not-collected")
    if reasoning_run.get("safeTrace", {}).get("mode") != "operational-trace-only":
        errors.append("safeTrace.mode must be operational-trace-only")

    adapter_trace = reasoning_run.get("adapterTrace", {})
    for key in ["workspace", "grants", "policy", "modelRoute", "skill", "tool", "memory", "approval", "evidence"]:
        if not adapter_trace.get(key):
            errors.append(f"adapterTrace missing {key}")

    event_types = {event.get("type") for event in events}
    missing_event_types = sorted(REQUIRED_EVENT_TYPES - event_types)
    if missing_event_types:
        errors.append(f"events.jsonl missing event types: {', '.join(missing_event_types)}")
    if len(events) != reasoning_run.get("safeTrace", {}).get("eventCount"):
        errors.append("eventCount does not match events.jsonl length")

    if evidence.get("kind") != "AgentPlaneReasoningEvidence":
        errors.append("agentplane-evidence.json kind must be AgentPlaneReasoningEvidence")
    if evidence.get("runId") != reasoning_run.get("runId"):
        errors.append("AgentPlane evidence runId mismatch")
    if evidence.get("network") != "none" or evidence.get("modelCalls") != "none" or evidence.get("hostMutation") != "none":
        errors.append("M1 evidence must declare no network, no model calls, and no host mutation")

    if replay.get("kind") != "ReplayPlan":
        errors.append("replay-plan.json kind must be ReplayPlan")
    if replay.get("replayClass") not in {"exact", "evidence-only"}:
        errors.append("M1 replayClass must be exact or evidence-only")

    if benchmark.get("kind") != "BenchmarkResult":
        errors.append("benchmark-result.json kind must be BenchmarkResult")
    if benchmark.get("passed") is not True:
        errors.append("benchmark-result.json must pass")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Superconscious run artifact directory.")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    errors = validate_run_dir(args.run_dir)
    if errors:
        print("artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"artifact validation passed: {args.run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
