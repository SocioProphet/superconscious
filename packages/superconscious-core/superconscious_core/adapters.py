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
