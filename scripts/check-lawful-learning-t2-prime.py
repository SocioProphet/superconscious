#!/usr/bin/env python3
"""Validate Lawful Learning T2' and A2 scoping doctrine artifacts.

Structural checker only. It does not run mathematical harnesses, recompute
hash chains, prove A2, or promote conjectural claims.
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
    "does_not_prove_A2",
    "does_not_identify_A2_spatial_group",
    "does_not_add_empirical_evidence",
}
A2_REQUIRED_OPEN_ITEMS = {
    "coxeter_jump_coefficient_A2",
    "a2_harness_skeleton",
    "a2_proof_note",
}
A2_REQUIRED_NON_CLAIMS = {
    "does_not_prove_A2",
    "does_not_compute_coxeter_jump_coefficient",
    "does_not_create_runtime_harness",
    "does_not_promote_conjectural_to_mathematical",
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
    if record.get("claimStatus") != "conjectural_scoping":
        raise ValidationError("A2 registry: claimStatus must remain conjectural_scoping")

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

    predicates = record.get("harnessPredicates", [])
    if not isinstance(predicates, list):
        raise ValidationError("A2 registry: harnessPredicates must be list")
    ids = {item.get("predicateId") for item in predicates if isinstance(item, dict)}
    if "coxeter_jump_coefficient_A2" not in ids:
        raise ValidationError("A2 registry: must include blocking coxeter_jump_coefficient_A2 predicate")
    for item in predicates:
        if item.get("predicateId") == "coxeter_jump_coefficient_A2":
            if item.get("status") != "blocking_placeholder":
                raise ValidationError("A2 registry: Coxeter jump must remain blocking_placeholder until computed")

    open_items = {item.get("itemId") for item in record.get("openItems", []) if isinstance(item, dict)}
    missing_open = A2_REQUIRED_OPEN_ITEMS - open_items
    if missing_open:
        raise ValidationError(f"A2 registry: missing openItems {sorted(missing_open)}")

    missing_non_claims = A2_REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_non_claims:
        raise ValidationError(f"A2 registry: missing nonClaims {sorted(missing_non_claims)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Lawful Learning T2'/A2 doctrine artifacts")
    parser.add_argument("--t2", default="registry/lawful-learning/t2-prime-predicate-interpretation.v0.1.json")
    parser.add_argument("--a2", default="registry/lawful-learning/a2-gate-minimality-scoping.v0.1.json")
    args = parser.parse_args()

    try:
        validate_t2_registry(load_json(Path(args.t2)))
        validate_a2_registry(load_json(Path(args.a2)))
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    print("OK: Lawful Learning T2'/A2 doctrine artifacts validate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
