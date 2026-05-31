#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = [
    ROOT / "examples" / "environment-state-memory-event.observed.json",
    ROOT / "examples" / "environment-state-memory-event.failed.json",
]
STATES = {"environment_observed", "environment_failed"}


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
    state = source.get("environment_state")
    evidence_refs = source.get("evidence_refs", [])
    receipt_refs = source.get("receipt_refs", [])
    warning_codes = source.get("warning_codes", [])
    failure_codes = source.get("failure_codes", [])

    if data.get("schema_version") != "1.0":
        problems.append("schema_version must be 1.0")
    if not str(data.get("event_id", "")).startswith("environment:state-memory-event:"):
        problems.append("event_id must be environment state memory event")
    if owner.get("plane") != "superconscious":
        problems.append("owner.plane must be superconscious")
    if owner.get("subsystem") != "subconscious":
        problems.append("owner.subsystem must be subconscious")
    if owner.get("repo") != "SocioProphet/superconscious":
        problems.append("owner.repo must be SocioProphet/superconscious")
    if source.get("state_authority") != "Sociosphere":
        problems.append("state_authority must be Sociosphere")
    if state not in STATES:
        problems.append("environment_state is invalid")
    if not str(source.get("workspace_ref", "")).startswith("workspace://"):
        problems.append("workspace_ref must start with workspace://")
    if not str(source.get("environment_profile_id", "")).startswith("environment-sandbox:profile:"):
        problems.append("environment_profile_id must reference environment-sandbox profile")
    if not str(source.get("prophet_platform_response_ref", "")).startswith("environment:validate-change-v2-response:"):
        problems.append("prophet_platform_response_ref must reference validate_change v2 response")
    if not str(source.get("agentplane_sandbox_run_ref", "")).startswith("agentplane:sandbox-run:"):
        problems.append("agentplane_sandbox_run_ref must reference AgentPlane sandbox run")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        problems.append("evidence_refs must be non-empty")
    if not isinstance(receipt_refs, list) or not receipt_refs:
        problems.append("receipt_refs must be non-empty")
    if any(not str(ref).startswith("evidence://") for ref in evidence_refs):
        problems.append("all evidence refs must use evidence://")
    if any(not str(ref).startswith("receipt://") for ref in receipt_refs):
        problems.append("all receipt refs must use receipt://")
    if not isinstance(warning_codes, list):
        problems.append("warning_codes must be a list")
    if not isinstance(failure_codes, list):
        problems.append("failure_codes must be a list when present")

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
        "may_promote_synthetic_to_runtime_parity",
        "may_grant_agent_autonomy",
        "subconscious_is_separate_authority_plane",
    ]
    for field in denied_fields:
        if limits.get(field) is not False:
            problems.append(f"authority limit must deny {field}")

    if state == "environment_observed":
        if memory.get("memory_disposition") != "remember_observed_environment_state":
            problems.append("observed state must remember observed environment state")
        if memory.get("planning_bias") != "advisory_until_runtime_parity":
            problems.append("observed state must stay advisory until runtime parity")
        if failure_codes:
            problems.append("observed state must not include failure codes")
    if state == "environment_failed":
        if memory.get("memory_disposition") != "remember_failed_environment_state":
            problems.append("failed state must remember failed environment state")
        if memory.get("planning_bias") != "report_only_after_failed_environment_validation":
            problems.append("failed state must force report-only planning bias")
        if "environment_validation_failed" not in warning_codes:
            problems.append("failed state must preserve environment_validation_failed")
        if "synthetic_validation_failed" not in failure_codes:
            problems.append("failed state must preserve synthetic_validation_failed")

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
        "validator": "superconscious.environment-state-memory.validator.v1",
        "passed": not failed,
        "results": results,
        "non_claims": [
            "Validator does not implement a live memory backend.",
            "Validator does not issue or verify receipts.",
            "Validator does not authorize execution."
        ]
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print(("PASS" if not failed else "FAIL") + ": environment state memory fixtures")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
