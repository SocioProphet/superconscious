#!/usr/bin/env python3
"""Validate the Lawful Learning D4 Strategy B scoping record.

Structural checker only. It does not prove D4, settle the B1/B2 faithfulness
choice, certify M_6, implement a harness, or compute a Stokes observable.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_OPEN_ISSUES = {
    "faithfulness_convention",
    "M6_lift_order",
    "triality_policy",
    "uniqueness_argument",
}
REQUIRED_NON_CLAIMS = {
    "does_not_prove_D4",
    "does_not_settle_B1_or_B2_faithfulness",
    "does_not_certify_M6_lift",
    "does_not_compute_D4_stokes_observable",
    "does_not_implement_D4_harness",
    "does_not_complete_triality_equivariant_theorem",
}
REQUIRED_PREDICATES = {
    "P1_matrix_stokes_multiplier_D4",
    "P2_order_six_minimality_D4",
    "P3_orthogonal_preservation_D4",
    "P4_nonabelian_so8_commutator_D4",
    "P5_centralizer_or_conjugacy_class_D4",
    "P6_triality_slice_declaration_D4",
    "P7_no_scalar_center_reuse_D4",
    "P8_representation_irreducibility_or_commutant_D4",
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


def validate(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.d4-strategy-b-scoping.v0.1":
        raise ValidationError("unexpected schemaVersion")
    if record.get("recordType") != "D4StrategyBScopingRecord":
        raise ValidationError("unexpected recordType")
    if record.get("claimStatus") != "strategy_scoping":
        raise ValidationError("claimStatus must remain strategy_scoping")

    strategy = record.get("strategy", {})
    if strategy.get("label") != "B" or strategy.get("name") != "non_scalar_auxiliary_element":
        raise ValidationError("strategy must be B / non_scalar_auxiliary_element")

    carrier = record.get("selectedInitialCarrier", {})
    expected_carrier = {
        "structureCarrier": "Spin(8)",
        "polarizationRepresentation": "V = 8_v",
        "formType": "orthogonal",
        "trialityPolicy": "slice_policy_V_first",
    }
    for key, value in expected_carrier.items():
        if carrier.get(key) != value:
            raise ValidationError(f"selectedInitialCarrier.{key} must be {value}")
    if set(carrier.get("trialityConjugates", [])) != {"S+ = 8_s", "S- = 8_c"}:
        raise ValidationError("triality conjugates must be S+ and S-")

    faithfulness = record.get("faithfulnessConvention", {})
    if faithfulness.get("status") != "unsettled":
        raise ValidationError("faithfulnessConvention.status must remain unsettled")
    if faithfulness.get("blockingForTheorem") is not True:
        raise ValidationError("faithfulnessConvention must block theorem promotion")
    option_ids = {item.get("optionId") for item in faithfulness.get("options", []) if isinstance(item, dict)}
    if option_ids != {"B1", "B2"}:
        raise ValidationError("faithfulnessConvention options must be B1 and B2")

    witness = record.get("candidateWitness", {})
    if witness.get("name") != "M_6":
        raise ValidationError("candidate witness must be M_6")
    if witness.get("type") != "non_scalar_order_six_auxiliary_element":
        raise ValidationError("candidate witness type must be non-scalar order-six auxiliary element")
    if witness.get("vectorRepresentationModel") != "diag(R(pi/3), I_6)":
        raise ValidationError("candidate witness vector model must be diag(R(pi/3), I_6)")
    if witness.get("status") != "scoped_not_certified":
        raise ValidationError("M_6 must remain scoped_not_certified")
    checks = set(witness.get("requiredChecks", []))
    for required in ("M_6^6 = I", "M_6^k != I for 1 <= k < 6", "lift order in Spin(8) is certified as 6 rather than 12"):
        if required not in checks:
            raise ValidationError(f"candidate witness missing required check: {required}")

    t2 = record.get("candidateTheoremStatements", {}).get("T2_D4_strategy_B", {})
    if t2.get("status") != "candidate_not_theorem":
        raise ValidationError("T2_D4_strategy_B must remain candidate_not_theorem")
    obligations = set(t2.get("blockingObligations", []))
    for required in ("faithfulness convention B1_or_B2", "certified M_6 lift", "centralizer_or_conjugacy_uniqueness", "triality policy finalization"):
        if required not in obligations:
            raise ValidationError(f"T2_D4_strategy_B missing blocking obligation: {required}")

    harness = record.get("harnessContract", {})
    if harness.get("status") != "specified_not_implemented":
        raise ValidationError("harnessContract.status must be specified_not_implemented")
    if harness.get("replacesScalarCenterPredicates") is not True:
        raise ValidationError("harness must replace scalar-center predicates")
    predicates = set(harness.get("proposedPredicates", []))
    missing_predicates = REQUIRED_PREDICATES - predicates
    if missing_predicates:
        raise ValidationError(f"missing proposed predicates: {sorted(missing_predicates)}")

    open_issues = {item.get("issueId") for item in record.get("openIssues", []) if isinstance(item, dict)}
    missing_issues = REQUIRED_OPEN_ISSUES - open_issues
    if missing_issues:
        raise ValidationError(f"missing open issues: {sorted(missing_issues)}")

    missing_nonclaims = REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_nonclaims:
        raise ValidationError(f"missing nonClaims: {sorted(missing_nonclaims)}")

    provenance = record.get("provenance", {})
    require_nonempty(provenance, "createdBy", "provenance")
    require_nonempty(provenance, "createdAt", "provenance")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate D4 Strategy B scoping")
    parser.add_argument(
        "registry",
        nargs="?",
        default="registry/lawful-learning/d4-strategy-b-scoping.v0.1.json",
    )
    args = parser.parse_args()

    try:
        validate(load_json(Path(args.registry)))
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    print(f"OK: {args.registry} validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
