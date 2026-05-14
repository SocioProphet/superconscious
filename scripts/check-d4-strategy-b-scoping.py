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
    "stokes_observable_declaration",
}
REQUIRED_OPEN_QUESTIONS = {
    "Q1_C6_prime_content",
    "Q2_fuss_catalan_verifier_scope",
    "Q3_four_CI_lanes_scope",
    "Q4_strategy_A_status",
    "Q5_class_declaration_sufficiency",
}
REQUIRED_NON_CLAIMS = {
    "does_not_prove_D4",
    "does_not_settle_B1_or_B2_faithfulness",
    "does_not_certify_M6_lift",
    "does_not_select_M6_conjugacy_class",
    "does_not_compute_D4_stokes_observable",
    "does_not_implement_D4_harness",
    "does_not_complete_triality_equivariant_theorem",
    "does_not_computer_algebra_verify_26_class_count",
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
FORBIDDEN_INCOHERENT_STATES = {
    "B1_with_full_S3_triality",
    "B1_with_lift_order_as_theorem_blocking_harness_pin",
    "B2_with_plus_minus_I_only_scalar_center_check",
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


def ids(items: list[Any], key: str) -> set[str]:
    return {str(item.get(key)) for item in items if isinstance(item, dict)}


def require_set_contains(actual: set[str], required: set[str], context: str) -> None:
    missing = required - actual
    if missing:
        raise ValidationError(f"{context}: missing {sorted(missing)}")


def validate_carrier_pin_coupling(record: dict[str, Any]) -> None:
    coupling = record.get("carrierPinCoupling")
    if not isinstance(coupling, dict):
        raise ValidationError("carrierPinCoupling must be present")
    if coupling.get("upstreamPin") != "faithfulnessConvention":
        raise ValidationError("carrierPinCoupling.upstreamPin must be faithfulnessConvention")

    b1 = coupling.get("B1", {})
    b2 = coupling.get("B2", {})
    if b1.get("liftOrder") != "out_of_scope_for_harness":
        raise ValidationError("B1 liftOrder must be out_of_scope_for_harness")
    if b1.get("triality") != "residual_Out_SO8_Z2_not_full_triality":
        raise ValidationError("B1 triality must be residual Out(SO8), not full triality")
    if b1.get("scalarCenter") != "plus_minus_I_only":
        raise ValidationError("B1 scalar center check must be plus_minus_I_only")
    hygiene = b1.get("hygieneObligation")
    if not isinstance(hygiene, dict):
        raise ValidationError("B1 must carry a hygiene obligation")
    if "V_tensor_algebra" not in set(hygiene.get("permittedCarriers", [])):
        raise ValidationError("B1 hygiene must permit only tensor-algebra carrier use")
    forbidden_carriers = set(hygiene.get("forbiddenCarriers", []))
    require_set_contains(
        forbidden_carriers,
        {"half_spin_S_plus", "half_spin_S_minus", "triality_paired"},
        "B1 hygiene forbiddenCarriers",
    )

    if b2.get("liftOrder") != "load_bearing":
        raise ValidationError("B2 liftOrder must be load_bearing")
    if b2.get("triality") != "full_S3_triality_available":
        raise ValidationError("B2 triality must be full_S3_triality_available")
    if b2.get("scalarCenter") != "full_ZSpin8_Z2xZ2":
        raise ValidationError("B2 scalar center check must use full Spin(8) center")
    if b2.get("hygieneObligation") is not None:
        raise ValidationError("B2 hygieneObligation must be null")

    incoherent = set(coupling.get("forbiddenIncoherentStates", []))
    require_set_contains(incoherent, FORBIDDEN_INCOHERENT_STATES, "carrierPinCoupling.forbiddenIncoherentStates")


def validate_spin8_center(record: dict[str, Any]) -> None:
    center = record.get("spin8Center")
    if not isinstance(center, dict):
        raise ValidationError("spin8Center must be present")
    if center.get("center") != "Z/2 x Z/2":
        raise ValidationError("Spin(8) center must be Z/2 x Z/2")
    if center.get("kernelSpin8ToSO8") != "<epsilon>":
        raise ValidationError("kernel Spin(8)->SO(8) must be <epsilon>")
    elements = center.get("nontrivialCentralElements", [])
    if not isinstance(elements, list) or len(elements) != 3:
        raise ValidationError("Spin(8) must record exactly three nontrivial central elements")
    element_ids = ids(elements, "id")
    require_set_contains(element_ids, {"epsilon", "epsilon_prime", "epsilon_double_prime"}, "spin8Center elements")
    if center.get("trialityAction") != "S3_permutes_nontrivial_central_elements":
        raise ValidationError("Spin(8) triality action must permute the nontrivial central elements")


def validate_order_six_inventory(record: dict[str, Any]) -> None:
    inventory = record.get("orderSixConjugacyInventory")
    if not isinstance(inventory, dict):
        raise ValidationError("orderSixConjugacyInventory must be present")
    if inventory.get("so8DerivedClassCount") != 26:
        raise ValidationError("SO(8) derived class count must be recorded as 26")
    if inventory.get("verificationStatus") != "derived_not_computer_algebra_verified":
        raise ValidationError("26-class enumeration must remain marked not computer-algebra verified")
    if inventory.get("requiresIndependentVerificationBeforeRegistryCitation") is not True:
        raise ValidationError("26-class enumeration must require independent verification before registry citation")
    if inventory.get("selectedClassStatus") != "undeclared":
        raise ValidationError("selected M6 conjugacy class must remain undeclared")
    if inventory.get("blockingForUniquenessPredicate") is not True:
        raise ValidationError("undeclared conjugacy class must block uniqueness predicate")
    candidate_ids = ids(inventory.get("namedCandidateRegions", []), "id")
    require_set_contains(candidate_ids, {"purely_primitive", "coxeter_flavored", "balanced"}, "named candidate regions")


def validate_stokes_pin(record: dict[str, Any]) -> None:
    stokes = record.get("stokesObservablePin")
    if not isinstance(stokes, dict):
        raise ValidationError("stokesObservablePin must be present")
    if stokes.get("status") != "undeclared":
        raise ValidationError("D4 Stokes observable pin must remain undeclared")
    if stokes.get("dataShape") != "tuple_with_cyclic_product_constraint_not_single_class_by_default":
        raise ValidationError("Stokes data shape must be tuple/product-constraint, not single class by default")
    declarations = set(stokes.get("requiredDeclarations", []))
    require_set_contains(
        declarations,
        {
            "poincare_rank",
            "leading_spectrum",
            "product_constraint_convention",
            "conjugation_gauge",
            "single_generator_vs_full_tuple_observable",
        },
        "stokes requiredDeclarations",
    )
    if stokes.get("blockingForHarnessObservable") is not True:
        raise ValidationError("undeclared D4 Stokes observable must block harness observable")


def validate(record: dict[str, Any]) -> None:
    if record.get("schemaVersion") != "lawful-learning.d4-strategy-b-scoping.v0.1":
        raise ValidationError("unexpected schemaVersion")
    if record.get("recordType") != "D4StrategyBScopingRecord":
        raise ValidationError("unexpected recordType")
    if record.get("claimStatus") != "strategy_scoping":
        raise ValidationError("claimStatus must remain strategy_scoping")
    if record.get("remediationDossier") != "docs/lawful-learning/remediation/d4-strategy-b-remediation-dossier-v0.1.md":
        raise ValidationError("record must cite the D4 Strategy B remediation dossier")

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
    options = {item.get("optionId"): item for item in faithfulness.get("options", []) if isinstance(item, dict)}
    if set(options) != {"B1", "B2"}:
        raise ValidationError("faithfulnessConvention options must be B1 and B2")
    if options["B1"].get("liftOrderPinStatus") != "out_of_scope_for_harness":
        raise ValidationError("B1 lift order pin status must be out_of_scope_for_harness")
    if options["B1"].get("trialityPolicyShape") != "residual_Out_SO8_Z2_not_full_triality":
        raise ValidationError("B1 triality policy shape must be residual Out(SO8)")
    if options["B1"].get("scalarCenterCheck") != "test_against_plus_minus_I_only":
        raise ValidationError("B1 scalar center check must be plus/minus I only")
    if options["B2"].get("liftOrderPinStatus") != "load_bearing":
        raise ValidationError("B2 lift order pin status must be load_bearing")
    if options["B2"].get("trialityPolicyShape") != "full_S3_triality_available":
        raise ValidationError("B2 triality policy shape must be full S3")
    if options["B2"].get("scalarCenterCheck") != "test_against_full_ZSpin8":
        raise ValidationError("B2 scalar center check must use full Spin(8) center")

    validate_carrier_pin_coupling(record)
    validate_spin8_center(record)
    validate_order_six_inventory(record)
    validate_stokes_pin(record)

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
    for required in (
        "faithfulness convention B1_or_B2",
        "certified M_6 lift",
        "centralizer_or_conjugacy_uniqueness",
        "triality policy finalization",
        "stokes_observable_declaration",
    ):
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
    hidden = harness.get("hiddenPredicateParameters")
    if not isinstance(hidden, dict):
        raise ValidationError("harnessContract.hiddenPredicateParameters must be present")
    if hidden.get("P4_nonabelian_so8_commutator_D4") != "requires_commutator_witness_W_as_input":
        raise ValidationError("P4 must declare the commutator witness parameter")
    if hidden.get("P7_no_scalar_center_reuse_D4") != "center_set_depends_on_B1_or_B2":
        raise ValidationError("P7 must declare B-dependent center set")

    open_issues = ids(record.get("openIssues", []), "issueId")
    require_set_contains(open_issues, REQUIRED_OPEN_ISSUES, "openIssues")

    open_questions = ids(record.get("openQuestions", []), "questionId")
    require_set_contains(open_questions, REQUIRED_OPEN_QUESTIONS, "openQuestions")

    missing_nonclaims = REQUIRED_NON_CLAIMS - set(record.get("nonClaims", []))
    if missing_nonclaims:
        raise ValidationError(f"missing nonClaims: {sorted(missing_nonclaims)}")

    provenance = record.get("provenance", {})
    require_nonempty(provenance, "createdBy", "provenance")
    require_nonempty(provenance, "createdAt", "provenance")
    require_nonempty(provenance, "updatedAt", "provenance")
    if provenance.get("remediationSource") != "d4-strategy-b-remediation-dossier-v0.1":
        raise ValidationError("provenance must cite remediation source")


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
