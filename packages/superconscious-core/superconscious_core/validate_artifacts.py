#!/usr/bin/env python3
"""Validate Superconscious M1 run artifacts.

This validator is dependency-free and intentionally checks semantic invariants that
matter to the governed cognition loop: safe trace posture, adapter trace presence,
AgentPlane evidence consistency, replay class, benchmark pass state, and local draft
schema availability.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[3]
REQUIRED_ARTIFACTS = [
    "events.jsonl",
    "reasoning-run.json",
    "agentplane-evidence.json",
    "replay-plan.json",
    "benchmark-result.json",
]
REQUIRED_SCHEMAS = [
    "schemas/reasoning-run.draft.schema.json",
    "schemas/reasoning-event.draft.schema.json",
    "schemas/adapter-decision.draft.schema.json",
    "schemas/agentplane-reasoning-evidence.draft.schema.json",
    "schemas/replay-plan.draft.schema.json",
    "schemas/benchmark-result.draft.schema.json",
    "schemas/cognition-operation.draft.schema.json",
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
REQUIRED_ADAPTER_TRACE_KEYS = [
    "workspace",
    "grants",
    "policy",
    "modelRoute",
    "skill",
    "tool",
    "memory",
    "approval",
    "evidence",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def require_keys(obj: Dict[str, Any], keys: Iterable[str], label: str) -> List[str]:
    return [f"{label} missing required key: {key}" for key in keys if key not in obj]


def validate_schema_files(repo_root: Path = REPO_ROOT) -> List[str]:
    errors: List[str] = []
    for rel_path in REQUIRED_SCHEMAS:
        path = repo_root / rel_path
        if not path.exists():
            errors.append(f"missing local draft schema: {rel_path}")
            continue
        try:
            schema = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON schema {rel_path}: {exc}")
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{rel_path}: must declare JSON Schema draft 2020-12")
        if not str(schema.get("$id", "")).startswith("urn:socioprophet:superconscious:schema:"):
            errors.append(f"{rel_path}: must declare Superconscious draft schema URN")
        if "description" not in schema or "Canonical ownership" not in schema.get("description", ""):
            errors.append(f"{rel_path}: must state canonical ownership boundary")
    return errors


def validate_adapter_decision(decision: Dict[str, Any], label: str) -> List[str]:
    errors = require_keys(decision, ["adapter", "decision", "summary", "evidence"], label)
    if decision.get("adapter") and not str(decision.get("adapter")).endswith("Adapter"):
        errors.append(f"{label}.adapter should name an Adapter implementation")
    if decision.get("summary") == "":
        errors.append(f"{label}.summary must not be empty")
    if not isinstance(decision.get("evidence", {}), dict):
        errors.append(f"{label}.evidence must be an object")
    return errors


def validate_run_dir(run_dir: Path) -> List[str]:
    errors: List[str] = []
    errors.extend(validate_schema_files())

    for artifact in REQUIRED_ARTIFACTS:
        if not (run_dir / artifact).exists():
            errors.append(f"missing required artifact: {artifact}")

    if any(error.startswith("missing required artifact:") for error in errors):
        return errors

    events = load_jsonl(run_dir / "events.jsonl")
    reasoning_run = load_json(run_dir / "reasoning-run.json")
    evidence = load_json(run_dir / "agentplane-evidence.json")
    replay = load_json(run_dir / "replay-plan.json")
    benchmark = load_json(run_dir / "benchmark-result.json")

    errors.extend(
        require_keys(
            reasoning_run,
            [
                "kind",
                "specVersion",
                "runId",
                "status",
                "task",
                "safeTrace",
                "adapterTrace",
                "events",
                "artifactRefs",
            ],
            "reasoning-run.json",
        )
    )
    if reasoning_run.get("kind") != "ReasoningRun":
        errors.append("reasoning-run.json kind must be ReasoningRun")
    if reasoning_run.get("status") != "completed":
        errors.append("reasoning-run.json status must be completed")
    if reasoning_run.get("safeTrace", {}).get("rawChainOfThought") != "not-collected":
        errors.append("safeTrace.rawChainOfThought must be not-collected")
    if reasoning_run.get("safeTrace", {}).get("mode") != "operational-trace-only":
        errors.append("safeTrace.mode must be operational-trace-only")
    if not str(reasoning_run.get("runId", "")).startswith("urn:srcos:reasoning-run:"):
        errors.append("reasoning-run.json runId must be a SourceOS reasoning-run URN")

    adapter_trace = reasoning_run.get("adapterTrace", {})
    for key in REQUIRED_ADAPTER_TRACE_KEYS:
        if not adapter_trace.get(key):
            errors.append(f"adapterTrace missing {key}")
        elif isinstance(adapter_trace[key], dict):
            errors.extend(validate_adapter_decision(adapter_trace[key], f"adapterTrace.{key}"))
        else:
            errors.append(f"adapterTrace.{key} must be an object")

    event_types = {event.get("type") for event in events}
    missing_event_types = sorted(REQUIRED_EVENT_TYPES - event_types)
    if missing_event_types:
        errors.append(f"events.jsonl missing event types: {', '.join(missing_event_types)}")
    if len(events) != reasoning_run.get("safeTrace", {}).get("eventCount"):
        errors.append("eventCount does not match events.jsonl length")
    for index, event in enumerate(events, start=1):
        errors.extend(
            require_keys(
                event,
                ["eventId", "runId", "type", "occurredAt", "summary", "traceLevel", "trustLevel"],
                f"events.jsonl line {index}",
            )
        )
        if event.get("runId") != reasoning_run.get("runId"):
            errors.append(f"events.jsonl line {index} runId mismatch")
        if event.get("traceLevel") == "denied":
            errors.append(f"events.jsonl line {index} must not emit denied trace content")

    errors.extend(
        require_keys(
            evidence,
            [
                "kind",
                "runId",
                "taskId",
                "taskHash",
                "status",
                "network",
                "modelCalls",
                "hostMutation",
                "policyDecision",
                "modelRouteDecision",
                "memoryDecision",
                "approvalDecision",
            ],
            "agentplane-evidence.json",
        )
    )
    if evidence.get("kind") != "AgentPlaneReasoningEvidence":
        errors.append("agentplane-evidence.json kind must be AgentPlaneReasoningEvidence")
    if evidence.get("runId") != reasoning_run.get("runId"):
        errors.append("AgentPlane evidence runId mismatch")
    if (
        evidence.get("network") != "none"
        or evidence.get("modelCalls") != "none"
        or evidence.get("hostMutation") != "none"
    ):
        errors.append("M1 evidence must declare no network, no model calls, and no host mutation")

    errors.extend(
        require_keys(
            replay,
            ["kind", "runId", "replayClass", "inputs", "constraints", "adapterReplay", "command"],
            "replay-plan.json",
        )
    )
    if replay.get("kind") != "ReplayPlan":
        errors.append("replay-plan.json kind must be ReplayPlan")
    if replay.get("replayClass") not in {"exact", "evidence-only"}:
        errors.append("M1 replayClass must be exact or evidence-only")
    if replay.get("runId") != reasoning_run.get("runId"):
        errors.append("replay-plan.json runId mismatch")

    errors.extend(
        require_keys(
            benchmark,
            ["kind", "runId", "suite", "passed", "assertions", "evaluatedAt"],
            "benchmark-result.json",
        )
    )
    if benchmark.get("kind") != "BenchmarkResult":
        errors.append("benchmark-result.json kind must be BenchmarkResult")
    if benchmark.get("passed") is not True:
        errors.append("benchmark-result.json must pass")
    if benchmark.get("runId") != reasoning_run.get("runId"):
        errors.append("benchmark-result.json runId mismatch")

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
