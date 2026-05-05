#!/usr/bin/env python3
"""Inspect Superconscious run artifacts in a human-readable form."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def inspect_run_dir(run_dir: Path) -> str:
    reasoning_run = load_json(run_dir / "reasoning-run.json")
    evidence = load_json(run_dir / "agentplane-evidence.json")
    replay = load_json(run_dir / "replay-plan.json")
    benchmark = load_json(run_dir / "benchmark-result.json")
    events = load_jsonl(run_dir / "events.jsonl")

    lines = [
        f"Superconscious run: {reasoning_run.get('runId')}",
        f"Status: {reasoning_run.get('status')}",
        f"Task: {reasoning_run.get('task', {}).get('title')}",
        f"Safe trace: {reasoning_run.get('safeTrace', {}).get('mode')} / rawChainOfThought={reasoning_run.get('safeTrace', {}).get('rawChainOfThought')}",
        f"Events: {len(events)}",
        f"AgentPlane evidence: network={evidence.get('network')} modelCalls={evidence.get('modelCalls')} hostMutation={evidence.get('hostMutation')}",
        f"Replay class: {replay.get('replayClass')}",
        f"Benchmark: {benchmark.get('suite')} passed={benchmark.get('passed')}",
        "",
        "Adapter decisions:",
    ]

    adapter_trace = reasoning_run.get("adapterTrace", {})
    for key in ["workspace", "grants", "policy", "modelRoute", "skill", "tool", "memory", "approval", "evidence"]:
        decision = adapter_trace.get(key, {})
        lines.append(f"- {key}: {decision.get('decision')} — {decision.get('summary')}")

    lines.extend(["", "Event timeline:"])
    for event in events:
        lines.append(f"- {event.get('type')}: {event.get('summary')}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a Superconscious run artifact directory.")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    try:
        print(inspect_run_dir(args.run_dir))
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"artifact inspection failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
