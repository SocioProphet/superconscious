#!/usr/bin/env python3
"""Phase 6 checker for the lawful-learning lane.

Implements the structural checks specified in Phases 3 and 4, plus the
M/T/S/E/G epistemic tag discipline from the Phase 1 claim-ledger doctrine.

Boundary: this checker is structural. It does not execute training runs,
run circuits, verify cryptographic authenticity, resolve cross-plane evidence,
or decide whether a claim deserves promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

try:
    import yaml  # type: ignore
except Exception as exc:  # noqa: BLE001
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None


class CheckResult:
    def __init__(self) -> None:
        self.passed: list[tuple[str, str]] = []
        self.failed: list[tuple[str, str]] = []
        self.skipped: list[tuple[str, str]] = []

    def ok(self, name: str, detail: str = "") -> None:
        self.passed.append((name, detail))

    def fail(self, name: str, detail: str) -> None:
        self.failed.append((name, detail))

    def skip(self, name: str, reason: str) -> None:
        self.skipped.append((name, reason))

    @property
    def success(self) -> bool:
        return not self.failed

    def report(self) -> str:
        lines: list[str] = []
        for name, detail in self.passed:
            lines.append(f"  PASS  {name}" + (f": {detail}" if detail else ""))
        for name, detail in self.failed:
            lines.append(f"  FAIL  {name}: {detail}")
        for name, reason in self.skipped:
            lines.append(f"  SKIP  {name}: {reason}")
        return "\n".join(lines)


def load_file(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        if yaml is None:
            raise RuntimeError(f"PyYAML is required to load YAML files: {YAML_IMPORT_ERROR}")
        return yaml.safe_load(text)
    if p.suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Unsupported file format: {p.suffix}")


REQUIRED_BY_TAG = {
    "M": "mathematical_dependency",
    "T": "typological_parallel_target",
    "S": "speculative_test_artifact",
    "E": "empirical_measurement_ref",
    "G": "governance_invariant_ref",
}
VALID_TAGS = set(REQUIRED_BY_TAG)


def tags_in(tag_field: str) -> set[str]:
    return set(tag_field.split("|")) if tag_field else set()


def check_epistemic_non_collapse(entry: dict[str, Any], result: CheckResult) -> None:
    claim_id = entry.get("claim_id", "<unknown>")
    tag_field = entry.get("tag", "")
    if not tag_field:
        result.fail("epistemic_non_collapse", f"{claim_id}: missing tag field")
        return

    tags = tags_in(tag_field)
    invalid = tags - VALID_TAGS
    if invalid:
        result.fail("epistemic_non_collapse", f"{claim_id}: unrecognized tag values {invalid}")
        return

    for tag in tags:
        field = REQUIRED_BY_TAG[tag]
        if not str(entry.get(field, "")).strip():
            result.fail("epistemic_non_collapse", f"{claim_id}: tag [{tag}] requires non-empty {field}")
            return

    if "|" in tag_field and not str(entry.get("claim_demarcation", "")).strip():
        result.fail("epistemic_non_collapse", f"{claim_id}: mixed-tag claim requires claim_demarcation")
        return

    if entry.get("status") == "promoted" and not str(entry.get("promotion_rule", "")).strip():
        result.fail("epistemic_non_collapse", f"{claim_id}: promoted claim requires non-empty promotion_rule")
        return

    claim_text = entry.get("claim", "").lower()
    if "hopfield" in claim_text and "M" in tags:
        dependency = entry.get("mathematical_dependency", "").lower()
        if "energy" not in dependency:
            result.fail("epistemic_non_collapse", f"{claim_id}: Hopfield [M] claim must name energy-function form")
            return

    if "sedenion" in claim_text and "M" in tags:
        if not str(entry.get("mathematical_dependency", "")).strip():
            result.fail("epistemic_non_collapse", f"{claim_id}: sedenion [M] claim must name algebraic dependency")
            return

    if ("may-wigner" in claim_text or "may wigner" in claim_text) and "M" in tags:
        dependency = entry.get("mathematical_dependency", "").lower()
        if "random" not in dependency and "gaussian" not in dependency:
            result.fail("epistemic_non_collapse", f"{claim_id}: May-Wigner [M] claim must state random-matrix assumptions")
            return

    result.ok("epistemic_non_collapse", str(claim_id))


def check_adapter_dag_acyclic(dependency_graph: dict[str, list[str]], result: CheckResult) -> None:
    white, gray, black = 0, 1, 2
    color: dict[str, int] = {node: white for node in dependency_graph}
    for deps in dependency_graph.values():
        for dep in deps:
            color.setdefault(dep, white)

    cycle_found: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        if cycle_found:
            return
        color[node] = gray
        path.append(node)
        for neighbor in dependency_graph.get(node, []):
            if color.get(neighbor, white) == gray:
                cycle_start = path.index(neighbor)
                cycle_found.append(path[cycle_start:] + [neighbor])
                return
            if color.get(neighbor, white) == white:
                dfs(neighbor, path)
        path.pop()
        color[node] = black

    for node in list(color):
        if color[node] == white:
            dfs(node, [])
        if cycle_found:
            break

    if cycle_found:
        result.fail("adapter_dag_acyclic", f"Directed cycle detected: {cycle_found[0]}")
    else:
        result.ok("adapter_dag_acyclic")


FORBIDDEN_MANIFEST_INPUTS = {
    "latent_state_A",
    "latent_state_B",
    "internal_state_A",
    "internal_state_B",
    "hidden_state_A",
    "hidden_state_B",
}
REQUIRED_MANIFEST_INPUTS = {"manifest_A", "manifest_B", "composition_rule"}


def check_black_boxing_composes(composition_declaration: dict[str, Any], result: CheckResult) -> None:
    derivation = composition_declaration.get("composed_manifest_derivation", {})
    if not derivation:
        result.skip("black_boxing_composes", "no composed_manifest_derivation field; skipping")
        return

    declared_inputs = set(derivation.get("inputs", []))
    missing = REQUIRED_MANIFEST_INPUTS - declared_inputs
    if missing:
        result.fail("black_boxing_composes", f"composed_manifest derivation missing required inputs: {missing}")
        return

    forbidden_used = FORBIDDEN_MANIFEST_INPUTS & declared_inputs
    if forbidden_used:
        result.fail("black_boxing_composes", f"composed_manifest derivation references latent state: {forbidden_used}")
        return

    result.ok("black_boxing_composes")


def _compute_replay_seal(seal_a: str, seal_b: str, composition_rule: str, boundary_hash: str) -> str:
    combined = f"{seal_a}|{seal_b}|{composition_rule}|{boundary_hash}"
    return hashlib.sha256(combined.encode()).hexdigest()


def check_replay_seal_for_composed_trace(composition_declaration: dict[str, Any], result: CheckResult) -> None:
    seal_decl = composition_declaration.get("composed_replay_seal_derivation", {})
    if not seal_decl:
        result.skip("replay_seal_for_composed_trace", "no composed_replay_seal_derivation field; skipping")
        return

    if seal_decl.get("requires_rerun_A", False):
        result.fail("replay_seal_for_composed_trace", "composed_replay_seal derivation requires rerun_A")
        return
    if seal_decl.get("requires_rerun_B", False):
        result.fail("replay_seal_for_composed_trace", "composed_replay_seal derivation requires rerun_B")
        return

    required = {"seal_A", "seal_B", "composition_rule", "boundary_hash"}
    missing = required - set(seal_decl.get("inputs", []))
    if missing:
        result.fail("replay_seal_for_composed_trace", f"composed_replay_seal derivation missing required inputs: {missing}")
        return

    declared_seal = composition_declaration.get("composed_replay_seal")
    if declared_seal:
        computed = _compute_replay_seal(
            seal_decl["seal_A"],
            seal_decl["seal_B"],
            seal_decl["composition_rule"],
            seal_decl["boundary_hash"],
        )
        if declared_seal != computed:
            result.fail("replay_seal_for_composed_trace", "declared composed_replay_seal does not match computed seal")
            return

    result.ok("replay_seal_for_composed_trace")


def check_may_wigner_monitor_declared(training_run: dict[str, Any], result: CheckResult) -> None:
    monitor = training_run.get("may_wigner_monitor", {})
    required = {"monitor_name", "monitored_quantity", "checkpoint_interval", "threshold_declaration"}
    if not monitor:
        result.fail("may_wigner_monitor_declared", "no may_wigner_monitor field declared")
        return
    missing = required - set(monitor)
    if missing:
        result.fail("may_wigner_monitor_declared", f"missing required fields: {missing}")
        return
    result.ok("may_wigner_monitor_declared")


def check_control_data_plane_separation(system_decl: dict[str, Any], result: CheckResult) -> None:
    control = set(system_decl.get("control_plane_components", []))
    data = set(system_decl.get("data_plane_components", []))
    boundary = set(system_decl.get("boundary_interfaces", []))
    if not control:
        result.fail("control_data_plane_separation", "no control_plane_components declared")
        return
    if not data:
        result.fail("control_data_plane_separation", "no data_plane_components declared")
        return
    overlap = (control & data) - boundary
    if overlap:
        result.fail("control_data_plane_separation", f"undeclared control/data overlap: {overlap}")
        return
    result.ok("control_data_plane_separation")


def check_tail_audit_allocated(audit_plan: dict[str, Any], result: CheckResult) -> None:
    required = {"expected_case_coverage", "tail_allocation_strategy", "tail_scope_declaration"}
    missing = required - set(audit_plan)
    if missing:
        result.fail("tail_audit_allocated", f"audit plan missing tail allocation fields: {missing}")
        return
    if not str(audit_plan.get("tail_allocation_strategy", "")).strip():
        result.fail("tail_audit_allocated", "tail_allocation_strategy must be non-empty")
        return
    result.ok("tail_audit_allocated")


VALID_DISCRETIZATION_TYPES = {"grokking", "phase_transition", "feature_splitting", "loss_cliff", "other"}
REQUIRED_DISCRETIZATION_FIELDS = {"event_type", "detected_at_checkpoint", "timestamp", "declared_cause", "replay_seal"}


def check_emergent_discretization_logged(event_log: list[dict[str, Any]], result: CheckResult) -> None:
    for event in event_log:
        if event.get("event_class") != "discretization":
            continue
        missing = REQUIRED_DISCRETIZATION_FIELDS - set(event)
        if missing:
            result.fail("emergent_discretization_logged", f"discretization event missing required fields: {missing}")
            return
        if event.get("event_type") not in VALID_DISCRETIZATION_TYPES:
            result.fail("emergent_discretization_logged", f"invalid event_type: {event.get('event_type')}")
            return
        if not str(event.get("declared_cause", "")).strip():
            result.fail("emergent_discretization_logged", "declared_cause must be non-empty")
            return
    result.ok("emergent_discretization_logged")


VALID_ALLOCATION_TYPES = {"composition", "superposition", "mixed", "unknown"}


def check_composition_superposition_declared(circuit_decl: dict[str, Any], result: CheckResult) -> None:
    required = {"allocation_type", "allocation_evidence", "allocation_basis"}
    missing = required - set(circuit_decl)
    if missing:
        result.fail("composition_superposition_declared", f"missing allocation fields: {missing}")
        return
    if circuit_decl.get("allocation_type") not in VALID_ALLOCATION_TYPES:
        result.fail("composition_superposition_declared", f"invalid allocation_type: {circuit_decl.get('allocation_type')}")
        return
    if not str(circuit_decl.get("allocation_evidence", "")).strip():
        result.fail("composition_superposition_declared", "allocation_evidence must be non-empty")
        return
    result.ok("composition_superposition_declared")


def check_anti_satisficing_continuation(training_decl: dict[str, Any], run_log: dict[str, Any], result: CheckResult) -> None:
    if not str(training_decl.get("continuation_rule", "")).strip():
        result.fail("anti_satisficing_continuation", "no continuation_rule declared")
        return
    conditions_met = run_log.get("sufficient_conditions_met", [])
    if conditions_met and not run_log.get("continuation_applied", False):
        result.fail("anti_satisficing_continuation", f"sufficient conditions met but continuation not applied: {conditions_met}")
        return
    result.ok("anti_satisficing_continuation")


def check_circuit_registry_entry(entry: dict[str, Any], result: CheckResult) -> None:
    circuit_id = entry.get("circuit_id", "<unknown>")
    if not str(entry.get("discovery_evidence_ref", "")).strip():
        result.fail("circuit_registry_evidence_required", f"{circuit_id}: missing discovery_evidence_ref")
        return
    if not str(entry.get("ablation_evidence_ref", "")).strip():
        result.fail("circuit_registry_evidence_required", f"{circuit_id}: missing ablation_evidence_ref")
        return
    result.ok("circuit_registry_evidence_required", str(circuit_id))
    check_composition_superposition_declared(entry, result)


VALID_ENFORCEMENT_MODES = {"detection_only", "training_time_prevention", "post_training_audit", "deployment_gate"}


def check_forbidden_circuit_declaration(decl: dict[str, Any], result: CheckResult) -> None:
    fid = decl.get("forbidden_circuit_id", "<unknown>")
    enforcement = decl.get("enforcement_mode", "")
    if not enforcement:
        result.fail("forbidden_circuit_enforcement_mode_required", f"{fid}: missing enforcement_mode")
        return
    if enforcement not in VALID_ENFORCEMENT_MODES:
        result.fail("forbidden_circuit_enforcement_mode_required", f"{fid}: invalid enforcement_mode {enforcement}")
        return
    result.ok("forbidden_circuit_enforcement_mode_required", str(fid))


def run_claim_ledger_checks(data: Any, result: CheckResult) -> None:
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
    elif isinstance(data, dict):
        entries = [data]
    else:
        result.fail("claim_ledger_load", f"unexpected claim ledger format: {type(data)}")
        return
    for entry in entries:
        check_epistemic_non_collapse(entry, result)


def run_adapter_dag_checks(data: Any, result: CheckResult) -> None:
    graph = None
    if isinstance(data, dict):
        graph = data.get("adapter_dependency_graph")
        if graph is None and all(isinstance(value, list) for value in data.values()):
            graph = data
    if graph is None:
        result.skip("adapter_dag_acyclic", "no adapter_dependency_graph field found")
        return
    check_adapter_dag_acyclic(graph, result)


def run_composition_checks(data: Any, result: CheckResult) -> None:
    if isinstance(data, dict):
        check_black_boxing_composes(data, result)
        check_replay_seal_for_composed_trace(data, result)


def run_training_run_checks(data: Any, result: CheckResult) -> None:
    if not isinstance(data, dict):
        result.fail("training_run_load", f"unexpected training run format: {type(data)}")
        return
    check_may_wigner_monitor_declared(data, result)
    check_control_data_plane_separation(data, result)
    check_tail_audit_allocated(data, result)
    check_anti_satisficing_continuation(data, data.get("run_log", {}), result)
    check_emergent_discretization_logged(data.get("event_log", []), result)


def run_circuit_registry_checks(data: Any, result: CheckResult) -> None:
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
    elif isinstance(data, dict) and "circuit_id" in data:
        entries = [data]
    else:
        result.skip("circuit_registry_evidence_required", "no recognizable circuit registry structure")
        return
    for entry in entries:
        check_circuit_registry_entry(entry, result)


def run_forbidden_circuit_checks(data: Any, result: CheckResult) -> None:
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "declarations" in data:
        entries = data["declarations"]
    elif isinstance(data, dict) and "forbidden_circuit_id" in data:
        entries = [data]
    else:
        result.skip("forbidden_circuit_enforcement_mode_required", "no recognizable forbidden circuit structure")
        return
    for entry in entries:
        check_forbidden_circuit_declaration(entry, result)


FixtureRunner = Callable[[Any, CheckResult], None]
FIXTURE_DISPATCH: list[tuple[re.Pattern[str], FixtureRunner]] = [
    (re.compile(r"claim.ledger"), run_claim_ledger_checks),
    (re.compile(r"adapter.cycle|adapter.dag"), run_adapter_dag_checks),
    (re.compile(r"composition"), run_composition_checks),
    (re.compile(r"training.run"), run_training_run_checks),
    (re.compile(r"circuit.registry"), run_circuit_registry_checks),
    (re.compile(r"forbidden.circuit"), run_forbidden_circuit_checks),
]
NEGATIVE_FIXTURE_PATTERN = re.compile(r"\.invalid\.")


def run_fixture_file(path: str) -> tuple[bool, str]:
    result = CheckResult()
    is_negative = bool(NEGATIVE_FIXTURE_PATTERN.search(path))
    try:
        data = load_file(path)
    except Exception as exc:  # noqa: BLE001
        return False, f"Failed to load {path}: {exc}"

    name = Path(path).name.lower()
    dispatched = False
    for pattern, runner in FIXTURE_DISPATCH:
        if pattern.search(name):
            runner(data, result)
            dispatched = True
            break

    if not dispatched:
        if isinstance(data, dict) and "tag" in data:
            run_claim_ledger_checks(data, result)
        elif isinstance(data, list) and data and isinstance(data[0], dict) and "tag" in data[0]:
            run_claim_ledger_checks(data, result)
        else:
            return True, f"SKIP {path}: no dispatch rule matched"

    if is_negative:
        if result.failed:
            return True, f"PASS (negative correctly rejected)\n{result.report()}"
        return False, f"FAIL (negative fixture passed all checks)\n{result.report()}"

    if result.success:
        return True, f"PASS\n{result.report()}"
    return False, f"FAIL\n{result.report()}"


def run_fixtures_directory(fixtures_dir: str) -> bool:
    root = Path(fixtures_dir)
    if not root.exists():
        print(f"ERROR: fixtures directory not found: {fixtures_dir}")
        return False
    fixture_files = sorted(
        file for file in root.rglob("*")
        if file.is_file() and file.suffix in (".json", ".yaml", ".yml")
    )
    all_pass = True
    for fixture in fixture_files:
        ok, report = run_fixture_file(str(fixture))
        print(f"[{'PASS' if ok else 'FAIL'}] {fixture.name}")
        if not ok:
            print(report)
            all_pass = False
    return all_pass


def run_trust_surface_checks(data: dict[str, Any]) -> CheckResult:
    result = CheckResult()
    ll = data.get("lawful_learning_trust_surface", data)

    components = ll.get("composition_components", {})
    adapter_dag = components.get("adapter_dag_ref", {})
    if isinstance(adapter_dag, dict) and "dependency_edges" in adapter_dag:
        graph: dict[str, list[str]] = {adapter_id: [] for adapter_id in adapter_dag.get("adapter_ids", [])}
        for edge in adapter_dag.get("dependency_edges", []):
            src = edge.get("from")
            dst = edge.get("to")
            if src and dst:
                graph.setdefault(src, []).append(dst)
        check_adapter_dag_acyclic(graph, result)
    else:
        result.skip("adapter_dag_acyclic", "no structured adapter_dag_ref found in trust surface")

    tier2 = ll.get("tier2_composition_invariants", {})
    required_modes = {
        "non_claim_propagation": "explicit_propagate_or_resolve_v1",
        "monitor_independence": "declared_monitor_independence_v1",
        "evidence_freshness": "declared_evidence_freshness_v1",
        "authority_scope": "declared_scope_lattice_v1",
    }
    for key, expected in required_modes.items():
        entry = tier2.get(key, {})
        mode = entry.get("analysis_mode", "")
        if mode != expected:
            result.fail("tier2_binding_declared", f"{key}: expected {expected}, got {mode}")
        else:
            result.ok("tier2_binding_declared", f"{key}: {mode}")

    required_non_claims = {
        "no_runtime_receipt_lookup",
        "no_runtime_non_claim_verification",
        "no_runtime_monitor_attestation",
        "no_timestamp_authenticity",
        "opaque_hashes_not_resolved",
        "no_runtime_circuit_discovery",
        "no_runtime_ablation_verification",
        "no_tag_promotion_at_composition",
        "no_substrate_verification",
        "no_frontier_claim_promotion",
    }
    missing_non_claims = required_non_claims - set(ll.get("non_claims", []))
    if missing_non_claims:
        result.fail("trust_surface_non_claims", f"missing required non-claims: {missing_non_claims}")
    else:
        result.ok("trust_surface_non_claims")

    expected_invariants = {
        "adapter_dag_acyclic",
        "black_boxing_composes",
        "replay_seal_for_composed_trace",
        "may_wigner_monitor_declared",
        "control_data_plane_separation",
        "tail_audit_allocated",
        "emergent_discretization_logged",
        "composition_superposition_declared",
        "anti_satisficing_continuation",
        "epistemic_non_collapse",
    }
    declared = set(ll.get("lawful_learning_invariants", {}))
    missing = expected_invariants - declared
    if missing:
        result.fail("trust_surface_invariants_declared", f"missing invariants: {missing}")
    else:
        result.ok("trust_surface_invariants_declared")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Lawful-learning Phase 6 checker")
    parser.add_argument("--fixtures", default="tests/fixtures/lawful-learning")
    parser.add_argument("--trust-surface", default="examples/TRUST_SURFACE.lawful-learning.yaml")
    parser.add_argument("--claim-ledger", default=None)
    parser.add_argument("--file", default=None)
    parser.add_argument("--skip-fixtures", action="store_true")
    parser.add_argument("--skip-trust-surface", action="store_true")
    args = parser.parse_args()

    all_pass = True

    if args.file:
        ok, report = run_fixture_file(args.file)
        print(report)
        return 0 if ok else 1

    if args.claim_ledger:
        print(f"\n=== Claim Ledger: {args.claim_ledger} ===")
        result = CheckResult()
        try:
            run_claim_ledger_checks(load_file(args.claim_ledger), result)
            print(result.report())
            all_pass = all_pass and result.success
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: {exc}")
            all_pass = False

    if not args.skip_fixtures:
        print(f"\n=== Fixtures: {args.fixtures} ===")
        all_pass = run_fixtures_directory(args.fixtures) and all_pass

    if not args.skip_trust_surface:
        print(f"\n=== Trust Surface: {args.trust_surface} ===")
        try:
            result = run_trust_surface_checks(load_file(args.trust_surface))
            print(result.report())
            all_pass = all_pass and result.success
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR loading trust surface: {exc}")
            all_pass = False

    print(f"\n{'ALL CHECKS PASSED' if all_pass else 'CHECKS FAILED'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
