"""Adapter contracts for the Superconscious governed cognition loop.

These adapters keep Superconscious thin. Real authority remains in the existing
estate repositories; M1 uses deterministic mock adapters so tests require no
network, model provider, browser, terminal, credentials, or host mutation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Protocol


@dataclass(frozen=True)
class AdapterDecision:
    """Generic decision returned by an adapter."""

    adapter: str
    decision: str
    summary: str
    evidence: Dict[str, Any] = field(default_factory=dict)


class WorkspaceAdapter(Protocol):
    def bind_workspace(self, task: Dict[str, Any]) -> AdapterDecision:
        """Bind a task to a workspace manifest/lock context."""


class AgentGrantAdapter(Protocol):
    def resolve_grants(self, task: Dict[str, Any]) -> AdapterDecision:
        """Resolve agent identity and scoped grants."""


class PolicyAdapter(Protocol):
    def check(self, task: Dict[str, Any], action: str, context: Dict[str, Any]) -> AdapterDecision:
        """Check whether a requested action is allowed."""


class ModelRouteAdapter(Protocol):
    def route(self, task: Dict[str, Any], task_class: str) -> AdapterDecision:
        """Return a model route decision."""


class SkillAdapter(Protocol):
    def activate(self, task: Dict[str, Any], skill_id: str) -> AdapterDecision:
        """Activate a skill under current task context."""


class ToolAdapter(Protocol):
    def observe(self, task: Dict[str, Any], tool_id: str) -> AdapterDecision:
        """Execute or simulate a tool observation."""


class MemoryAdapter(Protocol):
    def decide(self, task: Dict[str, Any], observation: Dict[str, Any]) -> AdapterDecision:
        """Propose, reject, quarantine, or commit a memory decision."""


class EvidenceAdapter(Protocol):
    def emit(self, run_id: str, artifacts: Iterable[str]) -> AdapterDecision:
        """Emit or stage evidence for downstream AgentPlane compatibility."""


class BenchmarkAdapter(Protocol):
    def evaluate(self, run_id: str, assertions: Iterable[Dict[str, Any]]) -> AdapterDecision:
        """Evaluate deterministic benchmark assertions."""


class ApprovalAdapter(Protocol):
    def request(self, task: Dict[str, Any], approval_class: str, reason: str) -> AdapterDecision:
        """Request human/operator/enterprise/signed-intent approval when needed."""


class MockWorkspaceAdapter:
    def bind_workspace(self, task: Dict[str, Any]) -> AdapterDecision:
        workspace = task.get("workspace", {})
        return AdapterDecision(
            adapter="MockWorkspaceAdapter",
            decision="bound-mock-workspace",
            summary="Bound run to mock SocioSphere workspace context.",
            evidence={"workspaceId": workspace.get("id"), "lockRef": workspace.get("lockRef")},
        )


class MockAgentGrantAdapter:
    def resolve_grants(self, task: Dict[str, Any]) -> AdapterDecision:
        agent = task.get("agent", {})
        return AdapterDecision(
            adapter="MockAgentGrantAdapter",
            decision="granted-safe-demo-scope",
            summary="Resolved deterministic demo agent grants.",
            evidence={"agentId": agent.get("id"), "scope": "demo-readonly"},
        )


class MockPolicyAdapter:
    def check(self, task: Dict[str, Any], action: str, context: Dict[str, Any]) -> AdapterDecision:
        policy = task.get("policy", {})
        denied = {
            "network": policy.get("network") == "denied",
            "modelCalls": policy.get("modelCalls") == "denied",
            "hostMutation": policy.get("hostMutation") == "denied",
        }
        if action in {"network", "modelCalls", "hostMutation"} and denied.get(action, False):
            return AdapterDecision(
                adapter="MockPolicyAdapter",
                decision="denied",
                summary=f"Denied {action} under M1 inert policy.",
                evidence={"action": action, "context": context, "policy": policy},
            )
        return AdapterDecision(
            adapter="MockPolicyAdapter",
            decision="allowed-safe-deterministic-mode",
            summary="Allowed safe deterministic local action.",
            evidence={"action": action, "context": context, "policy": policy},
        )


class MockModelRouteAdapter:
    def route(self, task: Dict[str, Any], task_class: str) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockModelRouteAdapter",
            decision="deterministic-stub-route",
            summary="Selected no-provider deterministic route.",
            evidence={
                "taskClass": task_class,
                "routeId": "urn:srcos:model-route:deterministic-stub",
                "provider": "none",
                "modelCalls": "denied",
                "promptEgress": "denied",
            },
        )


class MockSkillAdapter:
    def activate(self, task: Dict[str, Any], skill_id: str) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockSkillAdapter",
            decision="activated",
            summary="Activated deterministic local skill.",
            evidence={"skillId": skill_id, "mode": "deterministic-local", "sideEffects": "none"},
        )


class MockToolAdapter:
    def observe(self, task: Dict[str, Any], tool_id: str) -> AdapterDecision:
        objective = task.get("objective", "")
        return AdapterDecision(
            adapter="MockToolAdapter",
            decision="observed",
            summary="Simulated local tool observation.",
            evidence={
                "toolId": tool_id,
                "sideEffectClass": "none",
                "network": "none",
                "objectiveLength": len(objective),
                "observation": "Superconscious coordinates governed recursive agency through safe operational traces and evidence-backed replay.",
            },
        )


class MockMemoryAdapter:
    def decide(self, task: Dict[str, Any], observation: Dict[str, Any]) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockMemoryAdapter",
            decision="proposal-only",
            summary="Proposed memory note without durable promotion.",
            evidence={"durableWrite": False, "observationRef": observation.get("toolId")},
        )


class MockEvidenceAdapter:
    def emit(self, run_id: str, artifacts: Iterable[str]) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockEvidenceAdapter",
            decision="emitted-local-stub",
            summary="Emitted local AgentPlane-compatible evidence stub.",
            evidence={"runId": run_id, "artifacts": list(artifacts)},
        )


class MockBenchmarkAdapter:
    def evaluate(self, run_id: str, assertions: Iterable[Dict[str, Any]]) -> AdapterDecision:
        assertion_list = list(assertions)
        passed = all(bool(item.get("passed")) for item in assertion_list)
        return AdapterDecision(
            adapter="MockBenchmarkAdapter",
            decision="passed" if passed else "failed",
            summary="Evaluated deterministic benchmark assertions.",
            evidence={"runId": run_id, "passed": passed, "assertions": assertion_list},
        )


class MockApprovalAdapter:
    def request(self, task: Dict[str, Any], approval_class: str, reason: str) -> AdapterDecision:
        if approval_class == "none":
            return AdapterDecision(
                adapter="MockApprovalAdapter",
                decision="not-required",
                summary="No approval required for safe deterministic task.",
                evidence={"approvalClass": approval_class, "reason": reason},
            )
        return AdapterDecision(
            adapter="MockApprovalAdapter",
            decision="blocked",
            summary="Nontrivial approval classes are blocked in M1 deterministic mode.",
            evidence={"approvalClass": approval_class, "reason": reason},
        )


# ---------------------------------------------------------------------------
# Cognition loop adapter protocols (cognition.observe / reflect / propose / …)
# ---------------------------------------------------------------------------


class WorkspaceOperationObserveAdapter(Protocol):
    """Observe a WorkspaceOperation event (read-only; no mutation)."""

    def observe(self, operation: Dict[str, Any]) -> AdapterDecision: ...


class ReflectionAdapter(Protocol):
    """Generate a governed reflection/evaluation artifact for an observed operation."""

    def reflect(self, operation: Dict[str, Any], observation: AdapterDecision) -> AdapterDecision: ...


class RemediationProposalAdapter(Protocol):
    """Propose remediation through AgentPlane / OperationContract (never direct-write)."""

    def propose(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision: ...


class LearningLoopAdapter(Protocol):
    """Record evidence to the systems-learning-loop."""

    def record(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision: ...


class RiskSignalAdapter(Protocol):
    """Emit an auditable risk signal for downstream review."""

    def emit(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision: ...


class PolicyReviewAdapter(Protocol):
    """Request a policy review through Policy Fabric / Guardrail Fabric."""

    def request(self, run_id: str, reflection: AdapterDecision, reason: str) -> AdapterDecision: ...


# ---------------------------------------------------------------------------
# Mock implementations for the cognition loop adapters
# ---------------------------------------------------------------------------

_ELEVATED_SIDE_EFFECT_CLASSES = {"durable-write", "destructive"}


class MockWorkspaceOperationObserveAdapter:
    def observe(self, operation: Dict[str, Any]) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockWorkspaceOperationObserveAdapter",
            decision="observed-read-only",
            summary="Observed WorkspaceOperation event without mutation.",
            evidence={
                "operationId": operation.get("operationId"),
                "type": operation.get("type"),
                "status": operation.get("status"),
                "sideEffectClass": operation.get("sideEffectClass"),
                "sideEffectsApplied": False,
            },
        )


class MockReflectionAdapter:
    def reflect(self, operation: Dict[str, Any], observation: AdapterDecision) -> AdapterDecision:
        risk_score = (
            "medium"
            if operation.get("sideEffectClass") in _ELEVATED_SIDE_EFFECT_CLASSES
            else "low"
        )
        remediation = "review-suggested" if risk_score != "low" else "none-required"
        return AdapterDecision(
            adapter="MockReflectionAdapter",
            decision="reflected",
            summary="Generated governed reflection artifact for workspace operation.",
            evidence={
                "operationId": operation.get("operationId"),
                "evaluationSummary": "Operation completed within expected policy bounds.",
                "riskScore": risk_score,
                "remediation": remediation,
                "admissionState": "proposed",
            },
        )


class MockRemediationProposalAdapter:
    def propose(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision:
        remediation = reflection.evidence.get("remediation", "none-required")
        if remediation == "none-required":
            return AdapterDecision(
                adapter="MockRemediationProposalAdapter",
                decision="no-action-required",
                summary="No remediation required for this operation.",
                evidence={
                    "runId": run_id,
                    "routedThrough": "agentplane",
                    "actionType": "none",
                    "directMutation": False,
                },
            )
        return AdapterDecision(
            adapter="MockRemediationProposalAdapter",
            decision="proposal-emitted",
            summary="Emitted remediation proposal through AgentPlane; no direct mutation.",
            evidence={
                "runId": run_id,
                "routedThrough": "agentplane",
                "actionType": "review-request",
                "proposalRef": f"urn:srcos:remediation-proposal:{run_id.rsplit(':', 1)[-1]}",
                "directMutation": False,
            },
        )


class MockLearningLoopAdapter:
    def record(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision:
        return AdapterDecision(
            adapter="MockLearningLoopAdapter",
            decision="recorded-local-stub",
            summary="Recorded reflection evidence for systems-learning-loop (stub).",
            evidence={
                "runId": run_id,
                "learningLoopRef": "urn:socioprophet:systems-learning-loop:stub",
                "riskScore": reflection.evidence.get("riskScore"),
                "admissionState": "proposed",
            },
        )


class MockRiskSignalAdapter:
    def emit(self, run_id: str, reflection: AdapterDecision) -> AdapterDecision:
        risk_score = reflection.evidence.get("riskScore", "low")
        if risk_score == "low":
            return AdapterDecision(
                adapter="MockRiskSignalAdapter",
                decision="no-signal",
                summary="Risk score is low; no risk signal emitted.",
                evidence={"runId": run_id, "riskScore": risk_score, "signalEmitted": False},
            )
        return AdapterDecision(
            adapter="MockRiskSignalAdapter",
            decision="signal-emitted",
            summary="Emitted auditable risk signal for downstream review.",
            evidence={
                "runId": run_id,
                "riskScore": risk_score,
                "signalEmitted": True,
                "signalRef": f"urn:srcos:risk-signal:{run_id.rsplit(':', 1)[-1]}",
                "auditTrail": "ledger-facing",
            },
        )


class MockPolicyReviewAdapter:
    def request(self, run_id: str, reflection: AdapterDecision, reason: str) -> AdapterDecision:
        remediation = reflection.evidence.get("remediation", "none-required")
        if remediation == "none-required":
            return AdapterDecision(
                adapter="MockPolicyReviewAdapter",
                decision="not-required",
                summary="Policy review not required for this operation.",
                evidence={"runId": run_id, "reason": reason, "reviewRequested": False},
            )
        return AdapterDecision(
            adapter="MockPolicyReviewAdapter",
            decision="review-requested",
            summary="Requested policy review through Policy Fabric / Guardrail Fabric.",
            evidence={
                "runId": run_id,
                "reason": reason,
                "reviewRequested": True,
                "reviewRef": f"urn:srcos:policy-review:{run_id.rsplit(':', 1)[-1]}",
                "policyFabric": "guardrail-fabric",
            },
        )
