#!/usr/bin/env python3
"""Validate Superconscious SVF validation-history fixtures.

This validator checks memory-event shape and authority boundaries. It does
not execute SVF actions, run Sociosphere, issue receipts, or grant autonomy.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "svf-validation-history-event.selected-missing-observation.json"

STATUSES = {
    "validated_observed",
    "selected_missing_observation",
    "failed_observed",
    "stale_observation",
    "not_configured",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def result(check_id: str, passed: bool, diagnostics: list[str] | None = None) -> dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "diagnostics": diagnostics or []}


def validate() -> dict[str, Any]:
    data = load(FIXTURE)
    results: list[dict[str, Any]] = []

    results.append(result("schema-version", data.get("schema_version") == "1.0"))
    results.append(result("event-id", str(data.get("event_id", "")).startswith("svf:validation-history-event:"), [str(data.get("event_id"))]))

    owner = data.get("owner", {})
    results.append(result("owner-plane", owner.get("plane") == "superconscious", [str(owner.get("plane"))]))
    results.append(result("owner-subsystem", owner.get("subsystem") == "subconscious", [str(owner.get("subsystem"))]))
    results.append(result("owner-repo", owner.get("repo") == "SocioProphet/superconscious", [str(owner.get("repo"))]))

    source = data.get("source", {})
    status = source.get("validation_status")
    results.append(result("source-repo", "/" in str(source.get("repo", "")), [str(source.get("repo"))]))
    results.append(result("source-ref", isinstance(source.get("ref"), str) and len(source["ref"]) > 0))
    results.append(result("selected-plans", isinstance(source.get("selected_plans"), list) and len(source.get("selected_plans", [])) > 0))
    results.append(result("validation-status", status in STATUSES, [str(status)]))
    results.append(result("warning-codes-list", isinstance(source.get("warning_codes"), list)))
    results.append(result("observed-commands-list", isinstance(source.get("observed_validation_commands"), list)))
    results.append(result("receipt-refs-list", isinstance(source.get("receipt_refs"), list)))
    results.append(result("failure-taxonomy-list", isinstance(source.get("failure_taxonomy"), list)))

    memory = data.get("memory_action", {})
    results.append(result("memory-disposition", memory.get("memory_disposition") == "remember_validation_debt", [str(memory.get("memory_disposition"))]))
    results.append(result("recommended-next-action", isinstance(memory.get("recommended_next_action"), str) and len(memory["recommended_next_action"]) > 0))
    results.append(result("planning-bias", memory.get("planning_bias") == "report_only_until_observed", [str(memory.get("planning_bias"))]))
    results.append(result("agentplane-route-boolean", isinstance(memory.get("may_route_to_agentplane_evidence"), bool)))
    results.append(result("sociosphere-route-boolean", isinstance(memory.get("may_route_to_sociosphere_backlog"), bool)))

    limits = data.get("authority_limits", {})
    denied_fields = [
        "may_execute_svf_actions",
        "may_run_sociosphere_commands",
        "may_issue_or_verify_receipts",
        "may_promote_advisory_to_blocking",
        "may_grant_agent_autonomy",
        "subconscious_is_separate_authority_plane",
    ]
    for field in denied_fields:
        results.append(result(f"authority-denied:{field}", limits.get(field) is False, [str(limits.get(field))]))

    if status == "selected_missing_observation":
        warnings = set(source.get("warning_codes", [])) if isinstance(source.get("warning_codes"), list) else set()
        results.append(result("missing-observation-warning", "validation_observation_missing" in warnings, sorted(warnings)))
        results.append(result("missing-observation-no-observed-commands", source.get("observed_validation_commands") == [], [str(source.get("observed_validation_commands"))]))
        results.append(result("missing-observation-no-receipts", source.get("receipt_refs") == [], [str(source.get("receipt_refs"))]))
        results.append(result("missing-observation-report-only", memory.get("planning_bias") == "report_only_until_observed", [str(memory.get("planning_bias"))]))

    results.append(result("non-claims-present", isinstance(data.get("non_claims"), list) and len(data.get("non_claims", [])) >= 3))

    passed = all(item["passed"] for item in results)
    return {
        "validator": "superconscious.svf-validation-history.validator.v1",
        "passed": passed,
        "result_count": len(results),
        "results": results,
    }


def main() -> int:
    validation = validate()
    print(json.dumps(validation, indent=2, sort_keys=True))
    if not validation["passed"]:
        print("FAIL: SVF validation history", file=sys.stderr)
        return 1
    print("PASS: SVF validation history")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
