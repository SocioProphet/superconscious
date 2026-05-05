from superconscious_core.adapters import (
    MockAgentGrantAdapter,
    MockApprovalAdapter,
    MockBenchmarkAdapter,
    MockMemoryAdapter,
    MockModelRouteAdapter,
    MockPolicyAdapter,
    MockSkillAdapter,
    MockToolAdapter,
    MockWorkspaceAdapter,
)


TASK = {
    "agent": {"id": "urn:socioprophet:agent:test"},
    "workspace": {"id": "urn:socioprophet:workspace:test", "lockRef": "mock://lock"},
    "objective": "test objective",
    "policy": {
        "network": "denied",
        "modelCalls": "denied",
        "hostMutation": "denied",
        "memoryPromotion": "proposal-only",
    },
}


def test_mock_adapters_are_inert_and_deterministic() -> None:
    assert MockWorkspaceAdapter().bind_workspace(TASK).decision == "bound-mock-workspace"
    assert MockAgentGrantAdapter().resolve_grants(TASK).decision == "granted-safe-demo-scope"
    assert MockPolicyAdapter().check(TASK, "deterministic-local-run", {}).decision == "allowed-safe-deterministic-mode"
    assert MockPolicyAdapter().check(TASK, "network", {}).decision == "denied"
    assert MockModelRouteAdapter().route(TASK, "reference-loop-demo").evidence["provider"] == "none"
    assert MockSkillAdapter().activate(TASK, "skill").evidence["sideEffects"] == "none"
    assert MockToolAdapter().observe(TASK, "tool").evidence["network"] == "none"
    assert MockMemoryAdapter().decide(TASK, {"toolId": "tool"}).decision == "proposal-only"
    assert MockApprovalAdapter().request(TASK, "none", "safe").decision == "not-required"


def test_mock_benchmark_adapter_fails_closed_on_failed_assertion() -> None:
    decision = MockBenchmarkAdapter().evaluate(
        "run",
        [
            {"name": "ok", "passed": True},
            {"name": "bad", "passed": False},
        ],
    )
    assert decision.decision == "failed"
    assert decision.evidence["passed"] is False
