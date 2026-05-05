#!/usr/bin/env python3
"""Emit SourceOS-spec-aligned reasoning artifacts from Superconscious M1 artifacts.

The M1 runner preserves compatibility files:

- events.jsonl
- reasoning-run.json
- agentplane-evidence.json
- replay-plan.json
- benchmark-result.json

This canonicalization step writes SourceOS contract-shaped artifacts alongside them:

- reasoning-events.sourceos.jsonl
- reasoning-run.sourceos.json
- reasoning-receipt.json
- reasoning-replay-plan.json
- reasoning-benchmark.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


CANONICAL_ARTIFACTS = [
    "reasoning-events.sourceos.jsonl",
    "reasoning-run.sourceos.json",
    "reasoning-receipt.json",
    "reasoning-replay-plan.json",
    "reasoning-benchmark.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def canonical_events(events: List[Dict[str, Any]], spec_version: str) -> List[Dict[str, Any]]:
    canonical: List[Dict[str, Any]] = []
    for event in events:
        canonical.append(
            {
                "id": event["eventId"],
                "type": "ReasoningEvent",
                "specVersion": spec_version,
                "runRef": event["runId"],
                "eventType": event["type"],
                "summary": event["summary"],
                "traceLevel": event.get("traceLevel", "public-safe"),
                "trustLevel": event.get("trustLevel", "trusted-control-input"),
                "capturedAt": event.get("occurredAt", utc_now()),
            }
        )
    return canonical


def canonical_reasoning_run(
    legacy_run: Dict[str, Any], canonical_event_rows: List[Dict[str, Any]], spec_version: str
) -> Dict[str, Any]:
    agent = legacy_run.get("agent", {})
    workspace = legacy_run.get("workspace", {})
    task = legacy_run.get("task", {})
    artifact_refs = [
        "events.jsonl",
        "reasoning-events.sourceos.jsonl",
        "reasoning-run.json",
        "reasoning-run.sourceos.json",
        "agentplane-evidence.json",
        "reasoning-receipt.json",
        "replay-plan.json",
        "reasoning-replay-plan.json",
        "benchmark-result.json",
        "reasoning-benchmark.json",
    ]
    return {
        "id": legacy_run["runId"],
        "type": "ReasoningRun",
        "specVersion": spec_version,
        "status": legacy_run.get("status", "completed"),
        "task": {
            "id": task.get("taskId", "urn:srcos:reasoning-task:unknown"),
            "title": task.get("title", "Untitled reasoning task"),
            "objectiveHash": task.get("objectiveHash"),
        },
        "agentRef": agent.get("id", "urn:socioprophet:agent:unknown"),
        "workspaceRef": workspace.get("id", "urn:socioprophet:workspace:unknown"),
        "safeTrace": {
            "mode": legacy_run.get("safeTrace", {}).get("mode", "operational-trace-only"),
            "rawPrivateReasoning": "not-collected",
            "eventCount": len(canonical_event_rows),
        },
        "eventRefs": [event["id"] for event in canonical_event_rows],
        "artifactRefs": artifact_refs,
        "adapterRecords": list(legacy_run.get("adapterTrace", {}).values()),
        "startedAt": legacy_run.get("startedAt", utc_now()),
        "completedAt": legacy_run.get("completedAt", utc_now()),
    }


def canonical_receipt(
    legacy_run: Dict[str, Any], legacy_evidence: Dict[str, Any], spec_version: str
) -> Dict[str, Any]:
    run_id = legacy_run["runId"]
    task = legacy_run.get("task", {})
    return {
        "id": f"urn:srcos:receipt:reasoning:{run_id.rsplit(':', 1)[-1]}",
        "type": "ReasoningReceipt",
        "specVersion": spec_version,
        "runRef": run_id,
        "taskRef": task.get("taskId", "urn:srcos:reasoning-task:unknown"),
        "status": legacy_evidence.get("status", legacy_run.get("status", "completed")),
        "traceHash": legacy_evidence.get("eventStreamHash", "sha256:unknown"),
        "coordination": {
            "policy": legacy_evidence.get("policyDecision"),
            "modelRoute": legacy_evidence.get("modelRouteDecision"),
            "memory": legacy_evidence.get("memoryDecision"),
            "approval": legacy_evidence.get("approvalDecision"),
        },
        "replayClass": legacy_evidence.get("replayClass", "exact"),
        "capturedAt": legacy_evidence.get("emittedAt", utc_now()),
    }


def canonical_replay_plan(legacy_run: Dict[str, Any], legacy_replay: Dict[str, Any], spec_version: str) -> Dict[str, Any]:
    run_id = legacy_run["runId"]
    return {
        "id": f"urn:srcos:reasoning-replay-plan:{run_id.rsplit(':', 1)[-1]}",
        "type": "ReasoningReplayPlan",
        "specVersion": spec_version,
        "runRef": run_id,
        "replayClass": legacy_replay.get("replayClass", "exact"),
        "inputs": legacy_replay.get("inputs", {}),
        "constraints": legacy_replay.get("constraints", {}),
        "stepRefs": [event.get("eventId") for event in legacy_run.get("events", []) if event.get("eventId")],
        "capturedAt": legacy_run.get("completedAt", utc_now()),
    }


def canonical_benchmark(legacy_run: Dict[str, Any], legacy_benchmark: Dict[str, Any], spec_version: str) -> Dict[str, Any]:
    run_id = legacy_run["runId"]
    assertions = []
    for assertion in legacy_benchmark.get("assertions", []):
        assertions.append(
            {
                "name": assertion.get("name", "unnamed"),
                "passed": bool(assertion.get("passed")),
                "summary": assertion.get("note") or assertion.get("summary") or assertion.get("name", "assertion"),
            }
        )
    return {
        "id": f"urn:srcos:reasoning-benchmark:{run_id.rsplit(':', 1)[-1]}",
        "type": "ReasoningBenchmark",
        "specVersion": spec_version,
        "runRef": run_id,
        "suite": legacy_benchmark.get("suite", "m1-deterministic-smoke"),
        "passed": bool(legacy_benchmark.get("passed")),
        "assertions": assertions,
        "capturedAt": legacy_benchmark.get("evaluatedAt", utc_now()),
    }


def canonicalize(run_dir: Path, spec_version: str = "2.0.0") -> List[Path]:
    run_dir = run_dir.resolve()
    events = load_jsonl(run_dir / "events.jsonl")
    legacy_run = load_json(run_dir / "reasoning-run.json")
    legacy_evidence = load_json(run_dir / "agentplane-evidence.json")
    legacy_replay = load_json(run_dir / "replay-plan.json")
    legacy_benchmark = load_json(run_dir / "benchmark-result.json")

    canonical_event_rows = canonical_events(events, spec_version)
    outputs = {
        "reasoning-events.sourceos.jsonl": canonical_event_rows,
        "reasoning-run.sourceos.json": canonical_reasoning_run(legacy_run, canonical_event_rows, spec_version),
        "reasoning-receipt.json": canonical_receipt(legacy_run, legacy_evidence, spec_version),
        "reasoning-replay-plan.json": canonical_replay_plan(legacy_run, legacy_replay, spec_version),
        "reasoning-benchmark.json": canonical_benchmark(legacy_run, legacy_benchmark, spec_version),
    }

    written: List[Path] = []
    for name, payload in outputs.items():
        path = run_dir / name
        if name.endswith(".jsonl"):
            write_jsonl(path, payload)  # type: ignore[arg-type]
        else:
            write_json(path, payload)  # type: ignore[arg-type]
        written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit SourceOS canonical reasoning artifacts from a Superconscious run directory.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--spec-version", default="2.0.0")
    args = parser.parse_args()

    try:
        written = canonicalize(args.run_dir, args.spec_version)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"canonicalization failed: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
