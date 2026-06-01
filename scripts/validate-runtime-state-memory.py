#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = [
    ROOT / "examples" / "runtime-state-memory-event.allocated.json",
    ROOT / "examples" / "runtime-state-memory-event.failed.json",
]
STATES = {"runtime_allocated", "runtime_failed"}


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected object: {path}")
    return data


def validate(data: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    owner = data.get("owner", {})
    source = data.get("source", {})
    memory = data.get("memory_action", {})
    limits = data.get("authority_limits", {})
    state = source.get("runtime_state")
    evidence_refs = source.get("evidence_refs", [])
    receipt_refs = source.get("receipt_refs", [])
    blocking_gaps = source.get("blocking_gaps", [])
    warning_codes = source.get("warning_codes", [])
    failure_codes = source.get("failure_codes", [])

    if data.get("schema_version") != "1.0":
        problems.append("schema_version must be 1.0")
    if not str(data.get("event_id", "")).startswith("runtime:state-memory-event:"):
        problems.append("event_id must be runtime state memory event")
    if owner.get("plane") != "superconscious":
        problems.append("owner.plane must be superconscious")
    if owner.get("subsystem") != "subconscious":
        problems.append("owner.subsystem must be subconscious")
    if owner.get("repo") != "SocioProphet/superconscious":
        problems.append("owner.repo must be SocioProphet/superconscious")
    if source.get("state_authority") != "Sociosphere":
        problems.append("state_authority must be Sociosphere")
    if state not in STATES:
        problems.append("runtime_state is invalid")
    if not str(source.get("workspace_ref", "")).startswith("workspace://"):
        problems.append("workspace_ref must start with workspace://")
    if not str(source.get("environment_profile_id", "")).startswith("environment-sandbox:profile:"):
        problems.append("environment_profile_id must reference environment-sandbox profile")
    if not str(source.get("runtime_run_ref", "")).startswith("agentplane:runtime-sandbox-run:"):
        problems.append("runtime_run_ref must reference AgentPlane runtime sandbox run")
    if not str(source.get("environment_ref", "")).startswith("environment://"):
        problems.append("environment_ref must use environment://")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        problems.append("evidence_refs must be non-empty")
    if not isinstance(receipt_refs, list) or not receipt_refs:
        problems.append("receipt_refs must be non-empty")
    if any(not str(ref).startswith("evidence://") for ref in evidence_refs):
        problems.append("all evidence refs must use evidence://")
    if any(not str(ref).startswith("receipt://") for ref in receipt_refs):
        problems.append("all receipt refs must use receipt://")
    if not isinstance(blocking_gaps, list):
        problems.append("blocking_gaps must be a list")
    if not isinstance(warning_codes, list):
        problems.append("warning_codes must be a list")
    if not isinstance(failure_codes, list):
        problems.append("failure_codes must be a list when present")
    if source.get("runtime_parity_certified") is not False:
        problems.append("runtime parity must remain uncertified")
    if "runtime_parity_not_certified" not in warning_codes:
        problems.append("must preserve runtime_parity_not_certified warning")

    if not isinstance(memory.get("memory_disposition"), str) or not memory.get("memory_disposition"):
        problems.append("memory_disposition must be present")
    if not isinstance(memory.get("recommended_next_action"), str) or not memory.get("recommended_next_action"):
        problems.append("recommended_next_action must be present")
    if not isinstance(memory.get("planning_bias"), str) or not memory.get("planning_bias"):
        problems.append("planning_bias must be present")
    if not isinstance(memory.get("may_route_to_agentplane_evidence"), bool):
        problems.append("may_route_to_agentplane_evidence must be boolean")
    if not isinstance(memory.get("may_route_to_sociosphere_backlog"), bool):
        problems.append("may_route_to_sociosphere_backlog must be boolean")

    denied_fields = [
        "may_execute_environment_actions",
        "may_run_sociosphere_commands",
        "may_issue_or_verify_receipts",
        "may_certify_runtime_parity",
        "may_grant_agent_autonomy",
        "subconscious_is_separate_authority_plane",
    ]
    for field in denied_fields:
        if limits.get(field) is not False:
            problems.append(f"authority limit must deny {field}")

    if state == "runtime_allocated":
        if memory.get("memory_disposition") != "remember_runtime_allocated_not_certified":
            problems.append("runtime_allocated must remember allocated-not-certified state")
        if memory.get("recommended_next_action") != "request_human_review_before_runtime_continuation":
            problems.append("runtime_allocated must request human review")
        if memory.get("planning_bias") != "human_review_until_teardown_and_leak_checks_close":
            problems.append("runtime_allocated must preserve human-review planning bias")
        for gap in ("teardown_not_complete", "leak_check_not_complete"):
            if gap not in blocking_gaps:
                problems.append(f"runtime_allocated must preserve blocking gap {gap}")
        if failure_codes:
            problems.append("runtime_allocated must not include failure codes")
    if state == "runtime_failed":
        if memory.get("memory_disposition") != "remember_runtime_failed_not_certified":
            problems.append("runtime_failed must remember failed-not-certified state")
        if memory.get("recommended_next_action") != "request_operator_review_before_continuation":
            problems.append("runtime_failed must request operator review")
        if memory.get("planning_bias") != "report_only_after_runtime_failure":
            problems.append("runtime_failed must force report-only planning bias")
        for gap in ("runtime_allocation_failed", "teardown_failed", "leak_check_failed"):
            if gap not in blocking_gaps:
                problems.append(f"runtime_failed must preserve blocking gap {gap}")
        if "runtime_validation_failed" not in warning_codes:
            problems.append("runtime_failed must preserve runtime_validation_failed warning")
        if "runtime_allocation_failed" not in failure_codes:
            problems.append("runtime_failed must preserve runtime_allocation_failed failure code")

    if not isinstance(data.get("non_claims"), list) or len(data.get("non_claims", [])) < 3:
        problems.append("non_claims must contain at least three entries")
    return problems


def main() -> int:
    failed = False
    results: dict[str, Any] = {}
    for path in FIXTURES:
        problems = validate(load(path))
        results[str(path.relative_to(ROOT))] = problems
        failed = failed or bool(problems)

    report = {
        "validator": "superconscious.runtime-state-memory.validator.v1",
        "passed": not failed,
        "results": results,
        "non_claims": [
            "Validator does not implement a live memory backend.",
            "Validator does not issue or verify receipts.",
            "Validator does not certify runtime parity."
        ]
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print(("PASS" if not failed else "FAIL") + ": runtime state memory fixtures")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
