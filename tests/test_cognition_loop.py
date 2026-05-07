"""Tests for the governed cognition loop over Workspace Operations.

These tests verify all six required cognition operation types, the
read/reflect/propose posture invariants, provenance and admission state on
artifacts, and the inertness/determinism of the mock adapters.
"""

import json
from pathlib import Path

from superconscious_core.adapters import (
    MockLearningLoopAdapter,
    MockPolicyReviewAdapter,
    MockReflectionAdapter,
    MockRemediationProposalAdapter,
    MockRiskSignalAdapter,
    MockWorkspaceOperationObserveAdapter,
)
from superconscious_core.cognition_loop import (
    REQUIRED_COGNITION_OPERATION_TYPES,
    run_cognition,
)

EXAMPLE_TASK = Path("examples/workspace-operation-observe/task.json")

_LOW_RISK_OPERATION = {
    "operationId": "urn:srcos:workspace-operation:low-risk",
    "type": "workspace.metadata.read",
    "status": "completed",
    "sideEffectClass": "read-only",
}

_ELEVATED_OPERATION = {
    "operationId": "urn:srcos:workspace-operation:elevated-risk",
    "type": "workspace.file.write",
    "status": "completed",
    "sideEffectClass": "durable-write",
}


# ---------------------------------------------------------------------------
# Integration tests against the example task
# ---------------------------------------------------------------------------


def test_cognition_loop_emits_required_artifacts(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    required = [
        "cognition-events.jsonl",
        "cognition-run.json",
        "cognition-reflection.json",
        "cognition-remediation-proposal.json",
        "cognition-risk-signal.json",
        "cognition-policy-review-request.json",
        "cognition-learning-loop-record.json",
        "cognition-benchmark-result.json",
    ]
    for name in required:
        assert (run_dir / name).exists(), f"missing artifact: {name}"

    benchmark = json.loads((run_dir / "cognition-benchmark-result.json").read_text(encoding="utf-8"))
    assert benchmark["passed"] is True, benchmark


def test_cognition_loop_events_contain_all_required_operation_types(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    lines = (run_dir / "cognition-events.jsonl").read_text(encoding="utf-8").splitlines()
    event_types = {json.loads(line)["type"] for line in lines if line.strip()}

    assert REQUIRED_COGNITION_OPERATION_TYPES <= event_types, (
        f"missing event types: {REQUIRED_COGNITION_OPERATION_TYPES - event_types}"
    )


def test_cognition_loop_posture_is_read_reflect_propose(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    cognition_run = json.loads((run_dir / "cognition-run.json").read_text(encoding="utf-8"))
    assert cognition_run["cognitionPosture"] == "read-reflect-propose"
    assert cognition_run["directMutation"] is False


def test_cognition_loop_safe_trace_posture(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    cognition_run = json.loads((run_dir / "cognition-run.json").read_text(encoding="utf-8"))
    assert cognition_run["safeTrace"]["mode"] == "operational-trace-only"
    assert cognition_run["safeTrace"]["rawChainOfThought"] == "not-collected"
    assert cognition_run["safeTrace"]["eventCount"] == 6


def test_cognition_reflection_has_provenance_and_admission_state(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    reflection = json.loads((run_dir / "cognition-reflection.json").read_text(encoding="utf-8"))
    assert reflection["admissionState"] == "proposed"
    assert "provenance" in reflection
    assert reflection["provenance"]["agentRef"]
    assert reflection["provenance"]["workspaceRef"]
    assert reflection["provenance"]["taskHash"]


def test_remediation_proposal_routes_through_agentplane_not_direct(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    proposal = json.loads(
        (run_dir / "cognition-remediation-proposal.json").read_text(encoding="utf-8")
    )
    assert proposal["directMutation"] is False
    assert proposal["routedThrough"] == "agentplane"
    assert proposal["admissionState"] == "proposed"


def test_risk_signal_is_auditable(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    risk_signal = json.loads((run_dir / "cognition-risk-signal.json").read_text(encoding="utf-8"))
    # The example task has sideEffectClass=durable-write → elevated risk → signal emitted
    assert risk_signal["signalEmitted"] is True
    assert risk_signal["auditTrail"] == "ledger-facing"
    assert risk_signal["admissionState"] == "proposed"
    assert risk_signal["provenance"]["agentRef"]


def test_policy_review_request_references_guardrail_fabric(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    review_request = json.loads(
        (run_dir / "cognition-policy-review-request.json").read_text(encoding="utf-8")
    )
    assert review_request["reviewRequested"] is True
    assert review_request["policyFabric"] == "guardrail-fabric"
    assert review_request["admissionState"] == "proposed"


def test_learning_loop_record_is_proposal_only(tmp_path: Path) -> None:
    run_dir = run_cognition(EXAMPLE_TASK, tmp_path)

    record = json.loads(
        (run_dir / "cognition-learning-loop-record.json").read_text(encoding="utf-8")
    )
    assert record["admissionState"] == "proposed"
    assert record["learningLoopRef"]
    assert record["provenance"]["taskHash"]


def test_cognition_run_is_deterministic(tmp_path: Path) -> None:
    """The same task must always produce the same run_id (content-addressed)."""
    run_dir_a = run_cognition(EXAMPLE_TASK, tmp_path / "a")
    run_dir_b = run_cognition(EXAMPLE_TASK, tmp_path / "b")

    run_a = json.loads((run_dir_a / "cognition-run.json").read_text(encoding="utf-8"))
    run_b = json.loads((run_dir_b / "cognition-run.json").read_text(encoding="utf-8"))
    assert run_a["runId"] == run_b["runId"]


# ---------------------------------------------------------------------------
# Unit tests for mock cognition adapters
# ---------------------------------------------------------------------------


def test_mock_workspace_operation_observe_adapter_is_read_only() -> None:
    decision = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    assert decision.decision == "observed-read-only"
    assert decision.evidence["sideEffectsApplied"] is False
    assert decision.evidence["operationId"] == _ELEVATED_OPERATION["operationId"]


def test_mock_reflection_adapter_low_risk_operation() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_LOW_RISK_OPERATION)
    reflect = MockReflectionAdapter().reflect(_LOW_RISK_OPERATION, observe)
    assert reflect.decision == "reflected"
    assert reflect.evidence["riskScore"] == "low"
    assert reflect.evidence["remediation"] == "none-required"
    assert reflect.evidence["admissionState"] == "proposed"


def test_mock_reflection_adapter_elevated_risk_operation() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    reflect = MockReflectionAdapter().reflect(_ELEVATED_OPERATION, observe)
    assert reflect.decision == "reflected"
    assert reflect.evidence["riskScore"] == "medium"
    assert reflect.evidence["remediation"] == "review-suggested"
    assert reflect.evidence["admissionState"] == "proposed"


def test_mock_remediation_proposal_adapter_no_action_for_low_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_LOW_RISK_OPERATION)
    reflect = MockReflectionAdapter().reflect(_LOW_RISK_OPERATION, observe)
    remediation = MockRemediationProposalAdapter().propose("urn:srcos:cognition-run:test", reflect)
    assert remediation.decision == "no-action-required"
    assert remediation.evidence["directMutation"] is False
    assert remediation.evidence["routedThrough"] == "agentplane"


def test_mock_remediation_proposal_adapter_emits_proposal_for_elevated_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    reflect = MockReflectionAdapter().reflect(_ELEVATED_OPERATION, observe)
    remediation = MockRemediationProposalAdapter().propose("urn:srcos:cognition-run:test", reflect)
    assert remediation.decision == "proposal-emitted"
    assert remediation.evidence["directMutation"] is False
    assert remediation.evidence["routedThrough"] == "agentplane"
    assert remediation.evidence["proposalRef"]


def test_mock_learning_loop_adapter_records_as_proposal() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    reflect = MockReflectionAdapter().reflect(_ELEVATED_OPERATION, observe)
    record = MockLearningLoopAdapter().record("urn:srcos:cognition-run:test", reflect)
    assert record.decision == "recorded-local-stub"
    assert record.evidence["admissionState"] == "proposed"
    assert record.evidence["riskScore"] == "medium"


def test_mock_risk_signal_adapter_no_signal_for_low_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_LOW_RISK_OPERATION)
    reflect = MockReflectionAdapter().reflect(_LOW_RISK_OPERATION, observe)
    signal = MockRiskSignalAdapter().emit("urn:srcos:cognition-run:test", reflect)
    assert signal.decision == "no-signal"
    assert signal.evidence["signalEmitted"] is False


def test_mock_risk_signal_adapter_emits_signal_for_elevated_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    reflect = MockReflectionAdapter().reflect(_ELEVATED_OPERATION, observe)
    signal = MockRiskSignalAdapter().emit("urn:srcos:cognition-run:test", reflect)
    assert signal.decision == "signal-emitted"
    assert signal.evidence["signalEmitted"] is True
    assert signal.evidence["auditTrail"] == "ledger-facing"
    assert signal.evidence["signalRef"]


def test_mock_policy_review_adapter_not_required_for_low_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_LOW_RISK_OPERATION)
    reflect = MockReflectionAdapter().reflect(_LOW_RISK_OPERATION, observe)
    review = MockPolicyReviewAdapter().request("urn:srcos:cognition-run:test", reflect, "test")
    assert review.decision == "not-required"
    assert review.evidence["reviewRequested"] is False


def test_mock_policy_review_adapter_requests_review_for_elevated_risk() -> None:
    observe = MockWorkspaceOperationObserveAdapter().observe(_ELEVATED_OPERATION)
    reflect = MockReflectionAdapter().reflect(_ELEVATED_OPERATION, observe)
    review = MockPolicyReviewAdapter().request("urn:srcos:cognition-run:test", reflect, "test")
    assert review.decision == "review-requested"
    assert review.evidence["reviewRequested"] is True
    assert review.evidence["policyFabric"] == "guardrail-fabric"
    assert review.evidence["reviewRef"]
