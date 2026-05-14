#!/usr/bin/env python3
"""Validate Lawful Learning T2', A2, and unified A_n theorem artifacts.

Structural checker only. It does not run mathematical harnesses, recompute
hash chains, compute the direct A2 Stokes-side coefficient, or implement runtime services.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

T2_REQUIRED_PREDICATES = {
    "stokes_multiplier_observed",
    "catalan_jump_coefficient",
    "pairing_preservation",
    "commutator_norm",
    "zeta",
}
T2_REQUIRED_NON_CLAIMS = {
    "does_not_update_runtime_harness",
    "does_not_recompute_hash_chain_head",
    "does_not_add_empirical_evidence",
    "does_not_compute_A2_coxeter_jump_coefficient",
}
A2_REQUIRED_OPEN_ITEMS = {
    "coxeter_jump_coefficient_A2",
    "a2_harness_skeleton",
    "a2_expanded_proof_note",
}
A2_REQUIRED_NON_CLAIMS = {
    "does_not_complete_direct_stokes_computation",
    "does_not_implement_direct_A2_stokes_observable",
    "does_not_prove_A_n_uniformity",
    "does_not_scope_D_or_E_series",
}
A2_REQUIRED_HARNESS_KEYS = {
    "path",
    "referenceReport",
    "fussCatalanVerification",
    "hashChainHead",
    "status",
    "passedPredicates",
    "computedPredicates",
    "scaffoldPredicates",
}
AN_REQUIRED_TARGETS = {
    "stokes_multiplier_A_n",
    "coxeter_jump_coefficient_A_n",
    "polarization_preservation_A_n",
    "zeta_A_n",
    "zeta_A_n_order_check",
    "rank_structure_predicates",
    "irreducibility_predicate",
}
AN_REQUIRED_OPEN_ITEMS = {
    "coxeter_an_harness_scaffold",
    "direct_stokes_side_A2",
    "direct_stokes_side_A_n",
}
AN_REQUIRED_NON_CLAIMS = {
    "does_not_compute_direct_stokes_coefficients",
    "does_not_implement_parametric_runtime_harness",
    "does_not_scope_D_or_E_series",
    "does_not_supply_proof_assistant_formalization",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected JSON object")
    return value


def require_nonempty(record: dict[str, Any], key: str, context: str) -> None:
    value = record.get(key)
    if isinstance(value, str) and value.strip():
        return
    raise ValidationError(f"{context}: missing or empty {key}")


def validate_t2_registry(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.t2-prime-predicate-interpretation.v0.1":
        raise ValidationError("T2 registry: unexpected schemaVersion")
    if record.get("recordType") != "T2PrimePredicateInterpretationTable":
        raise ValidationError("T2 registry: unexpected recordType")
    if record.get("gateMinimalityScope") != "T2'":
        raise ValidationError("T2 registry: gateMinimalityScope must be T2'")
    if record.get("principle") != "same numerical predicate, different witness object":
        raise ValidationError("T2 registry: principle must preserve witness-object distinction")

    scope_refs = record.get("scopeReferences", {})
    if not isinstance(scope_refs, dict):
        raise ValidationError("T2 registry: scopeReferences must be object")
    for key in ("doctrineDocument", "sourceFaithfulProofNote", "sourceFollowOnNote"):
        require_nonempty(scope_refs, key, "T2 scopeReferences")

    predicates = record.get("predicates")
    if not isinstance(predicates, list):
        raise ValidationError("T2 registry: predicates must be list")
    observed = {item.get("predicateId") for item in predicates if isinstance(item, dict)}
    missing = T2_REQUIRED_PREDICATES - observed
    if missing:
        raise ValidationError(f"T2 registry: missing predicates {sorted(missing)}")
    for item in predicates:
        if not isinstance(item, dict):
            raise ValidationError("T2 registry: predicate entry must be object")
        pid = item.get("predicateId", "<unknown>")
        for key in ("numericalTarget", "t2WitnessObject", "t2PrimeWitnessObject", "reuseRule"):
            require_nonempty(item, key, f"T2 predicate {pid}")
        if pid == "zeta" and "not an element of SO(3)" not in item["t2PrimeWitnessObject"]:
            raise ValidationError("T2 registry: zeta must be marked not an element of SO(3)")

    hash_policy = record.get("hashChainPolicy", {})
    if hash_policy.get("headChangeRequired") is not True:
        raise ValidationError("T2 registry: headChangeRequired must be true")
    for key in ("headChangeReason", "futureHeadChangeRule"):
        require_nonempty(hash_policy, key, "T2 hashChainPolicy")

    missing_non_claims = T2_REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_non_claims:
        raise ValidationError(f"T2 registry: missing nonClaims {sorted(missing_non_claims)}")


def validate_a2_registry(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.a2-gate-minimality-scoping.v0.1":
        raise ValidationError("A2 registry: unexpected schemaVersion")
    if record.get("recordType") != "A2GateMinimalityScopingRecord":
        raise ValidationError("A2 registry: unexpected recordType")
    if record.get("claimStatus") != "structural_theorem":
        raise ValidationError("A2 registry: claimStatus must be structural_theorem")

    candidate = record.get("candidate", {})
    if not isinstance(candidate, dict):
        raise ValidationError("A2 registry: candidate must be object")
    expected = {
        "spatialGroup": "PSU(3)",
        "auxiliaryGroup": "SU(3)",
        "polarizationSpace": "C^3",
        "formType": "Hermitian",
        "centralElement": "omega * I_3",
        "loopClass": "Z/3",
    }
    for key, value in expected.items():
        if candidate.get(key) != value:
            raise ValidationError(f"A2 registry: candidate.{key} must be {value}")

    harness = record.get("harness", {})
    if not isinstance(harness, dict):
        raise ValidationError("A2 registry: harness must be object")
    missing_harness = A2_REQUIRED_HARNESS_KEYS - set(harness)
    if missing_harness:
        raise ValidationError(f"A2 registry: missing harness fields {sorted(missing_harness)}")
    if harness.get("status") != "scaffold_live":
        raise ValidationError("A2 registry: harness.status must be scaffold_live")
    if harness.get("passedPredicates") != 8:
        raise ValidationError("A2 registry: harness must report 8 passing predicates")
    if harness.get("computedPredicates") != 6 or harness.get("scaffoldPredicates") != 2:
        raise ValidationError("A2 registry: harness must report 6 computed and 2 scaffold predicates")

    predicates = record.get("harnessPredicates", [])
    if not isinstance(predicates, list):
        raise ValidationError("A2 registry: harnessPredicates must be list")
    ids = {item.get("predicateId") for item in predicates if isinstance(item, dict)}
    required_predicates = {
        "stokes_multiplier_observed_A2",
        "coxeter_jump_coefficient_A2",
        "hermitian_preservation_A2",
        "gellmann_commutator_norm_A2",
        "zeta_A2",
        "zeta_A2_order_check",
    }
    missing_predicates = required_predicates - ids
    if missing_predicates:
        raise ValidationError(f"A2 registry: missing harness predicates {sorted(missing_predicates)}")
    for item in predicates:
        if item.get("predicateId") == "coxeter_jump_coefficient_A2":
            if item.get("status") != "scaffold_supported_direct_stokes_pending":
                raise ValidationError("A2 registry: Coxeter jump must be scaffold_supported_direct_stokes_pending")
        if item.get("predicateId") == "stokes_multiplier_observed_A2":
            if item.get("status") != "scaffold_value_direct_stokes_pending":
                raise ValidationError("A2 registry: Stokes multiplier must be scaffold_value_direct_stokes_pending")

    open_items = {item.get("itemId") for item in record.get("openItems", []) if isinstance(item, dict)}
    missing_open = A2_REQUIRED_OPEN_ITEMS - open_items
    if missing_open:
        raise ValidationError(f"A2 registry: missing openItems {sorted(missing_open)}")

    missing_non_claims = A2_REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_non_claims:
        raise ValidationError(f"A2 registry: missing nonClaims {sorted(missing_non_claims)}")


def validate_an_registry(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.an-unified-gate-minimality.v0.1":
        raise ValidationError("An registry: unexpected schemaVersion")
    if record.get("recordType") != "AnUnifiedGateMinimalityTheoremRecord":
        raise ValidationError("An registry: unexpected recordType")
    if record.get("claimStatus") != "structural_theorem_pattern":
        raise ValidationError("An registry: claimStatus must be structural_theorem_pattern")

    a1 = record.get("a1ExceptionalBranch", {})
    if not isinstance(a1, dict):
        raise ValidationError("An registry: a1ExceptionalBranch must be object")
    expected_a1 = {
        "spatialGroup": "SO(3)",
        "auxiliaryGroup": "Spin(3)=SU(2)",
        "polarizationSpace": "C^2",
        "formType": "symplectic",
        "centralElement": "-I_2",
    }
    for key, value in expected_a1.items():
        if a1.get(key) != value:
            raise ValidationError(f"An registry: a1ExceptionalBranch.{key} must be {value}")

    branch = record.get("nGreaterEqualTwoBranch", {})
    if not isinstance(branch, dict):
        raise ValidationError("An registry: nGreaterEqualTwoBranch must be object")
    expected_branch = {
        "spatialGroupPattern": "PSU(n+1)",
        "auxiliaryGroupPattern": "SU(n+1)",
        "polarizationSpacePattern": "C^(n+1)",
        "formType": "Hermitian",
        "centralElementPattern": "exp(2*pi*i/(n+1)) * I_(n+1)",
        "loopClassPattern": "Z/(n+1)",
        "jumpCoefficientPattern": "- (n+1)^(n+1) / n^n",
    }
    for key, value in expected_branch.items():
        if branch.get(key) != value:
            raise ValidationError(f"An registry: nGreaterEqualTwoBranch.{key} must be {value}")

    targets = set(record.get("parametricHarnessTargets", []))
    missing_targets = AN_REQUIRED_TARGETS - targets
    if missing_targets:
        raise ValidationError(f"An registry: missing parametricHarnessTargets {sorted(missing_targets)}")

    open_items = {item.get("itemId") for item in record.get("openItems", []) if isinstance(item, dict)}
    missing_open = AN_REQUIRED_OPEN_ITEMS - open_items
    if missing_open:
        raise ValidationError(f"An registry: missing openItems {sorted(missing_open)}")

    missing_non_claims = AN_REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_non_claims:
        raise ValidationError(f"An registry: missing nonClaims {sorted(missing_non_claims)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Lawful Learning T2'/A2/An doctrine artifacts")
    parser.add_argument("--t2", default="registry/lawful-learning/t2-prime-predicate-interpretation.v0.1.json")
    parser.add_argument("--a2", default="registry/lawful-learning/a2-gate-minimality-scoping.v0.1.json")
    parser.add_argument("--an", default="registry/lawful-learning/an-unified-gate-minimality.v0.1.json")
    args = parser.parse_args()

    try:
        validate_t2_registry(load_json(Path(args.t2)))
        validate_a2_registry(load_json(Path(args.a2)))
        validate_an_registry(load_json(Path(args.an)))
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    print("OK: Lawful Learning T2'/A2/An theorem doctrine artifacts validate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
