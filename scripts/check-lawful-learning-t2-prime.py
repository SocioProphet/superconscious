#!/usr/bin/env python3
"""Validate Lawful Learning T2' predicate interpretation tables.

Boundary: structural checker only. It does not run harnesses, recompute hash
chains, prove A2 claims, or promote theorem claims.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_PREDICATES = {
    "stokes_multiplier_observed",
    "catalan_jump_coefficient",
    "pairing_preservation",
    "commutator_norm",
    "zeta",
}
REQUIRED_NON_CLAIMS = {
    "does_not_update_runtime_harness",
    "does_not_recompute_hash_chain_head",
    "does_not_prove_A2",
    "does_not_identify_A2_spatial_group",
    "does_not_add_empirical_evidence",
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
        raise ValidationError("registry must be a JSON object")
    return value


def require_nonempty(record: dict[str, Any], key: str, context: str) -> None:
    value = record.get(key)
    if isinstance(value, str) and value.strip():
        return
    raise ValidationError(f"{context}: missing or empty {key}")


def validate_registry(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.t2-prime-predicate-interpretation.v0.1":
        raise ValidationError("unexpected schemaVersion")
    if record.get("recordType") != "T2PrimePredicateInterpretationTable":
        raise ValidationError("unexpected recordType")
    if record.get("gateMinimalityScope") != "T2'":
        raise ValidationError("gateMinimalityScope must be T2'")
    if record.get("principle") != "same numerical predicate, different witness object":
        raise ValidationError("principle must preserve the witness-object distinction")

    scope_refs = record.get("scopeReferences", {})
    if not isinstance(scope_refs, dict):
        raise ValidationError("scopeReferences must be an object")
    for key in ("doctrineDocument", "sourceFaithfulProofNote", "sourceFollowOnNote"):
        require_nonempty(scope_refs, key, "scopeReferences")

    predicates = record.get("predicates")
    if not isinstance(predicates, list):
        raise ValidationError("predicates must be a list")
    observed = {item.get("predicateId") for item in predicates if isinstance(item, dict)}
    missing = REQUIRED_PREDICATES - observed
    extra = observed - REQUIRED_PREDICATES
    if missing:
        raise ValidationError(f"missing required predicates: {sorted(missing)}")
    if extra:
        raise ValidationError(f"unexpected predicates: {sorted(extra)}")

    for item in predicates:
        if not isinstance(item, dict):
            raise ValidationError("predicate entry must be an object")
        pid = item.get("predicateId", "<unknown>")
        for key in ("numericalTarget", "t2WitnessObject", "t2PrimeWitnessObject", "reuseRule"):
            require_nonempty(item, key, f"predicate {pid}")
        if pid == "zeta":
            t2p = item["t2PrimeWitnessObject"].lower()
            if "not an element of so(3)" not in t2p:
                raise ValidationError("zeta T2' interpretation must say it is not an element of SO(3)")

    hash_policy = record.get("hashChainPolicy", {})
    if not isinstance(hash_policy, dict):
        raise ValidationError("hashChainPolicy must be an object")
    if hash_policy.get("headChangeRequired") is not True:
        raise ValidationError("hashChainPolicy.headChangeRequired must be true")
    for key in ("headChangeReason", "futureHeadChangeRule"):
        require_nonempty(hash_policy, key, "hashChainPolicy")

    non_claims = set(record.get("nonClaims", []))
    missing_non_claims = REQUIRED_NON_CLAIMS - non_claims
    if missing_non_claims:
        raise ValidationError(f"missing required non-claims: {sorted(missing_non_claims)}")

    provenance = record.get("provenance", {})
    if not isinstance(provenance, dict):
        raise ValidationError("provenance must be an object")
    for key in ("createdBy", "createdAt", "sourceUploads"):
        if key not in provenance:
            raise ValidationError(f"provenance missing {key}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Lawful Learning T2' predicate interpretation table")
    parser.add_argument(
        "registry",
        nargs="?",
        default="registry/lawful-learning/t2-prime-predicate-interpretation.v0.1.json",
    )
    args = parser.parse_args()

    try:
        validate_registry(load_json(Path(args.registry)))
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    print(f"OK: {args.registry} validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
