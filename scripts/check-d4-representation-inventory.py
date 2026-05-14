#!/usr/bin/env python3
"""Validate the Lawful Learning D4 representation inventory.

Structural checker only. It does not prove a D4 theorem, select Strategy B,
construct M_6, implement a D4 harness, or compute Stokes observables.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_CENTER_ELEMENTS = {"1", "epsilon", "delta", "epsilon_delta"}
REQUIRED_EIGHT_DIM_REPS = {"V (vector)", "S+ (spinor+)", "S- (spinor-)"}
REQUIRED_STRATEGIES = {"A", "B", "C"}
REQUIRED_REJECTED_INVALIDS = {
    "spin_8_center_is_cyclic_Z_6",
    "spin_8_has_faithful_6_dimensional_complex_representation",
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


def validate_inventory(record: dict[str, Any]) -> None:
    if record.get("schema_version") != "v0.1":
        raise ValidationError("unexpected schema_version")
    if record.get("doctrine") != "lawful-learning":
        raise ValidationError("doctrine must be lawful-learning")
    if record.get("claim_id") != "d4-representation-inventory":
        raise ValidationError("claim_id must be d4-representation-inventory")
    if record.get("claim_status") != "research_scoping":
        raise ValidationError("claim_status must be research_scoping")

    group = record.get("group", {})
    if not isinstance(group, dict):
        raise ValidationError("group must be an object")
    expected_group = {
        "name": "Spin(8)",
        "type": "compact_simple_simply_connected",
        "rank": 4,
        "dimension": 28,
        "cartan_type": "D_4",
        "coxeter_number": 6,
        "weyl_group_order": 192,
    }
    for key, value in expected_group.items():
        if group.get(key) != value:
            raise ValidationError(f"group.{key} must be {value}")

    center = group.get("center", {})
    if center.get("isomorphism") != "Z/2 x Z/2":
        raise ValidationError("Spin(8) center must be Z/2 x Z/2")
    if center.get("order") != 4:
        raise ValidationError("Spin(8) center order must be 4")
    if center.get("is_cyclic") is not False:
        raise ValidationError("Spin(8) center must be marked non-cyclic")
    center_elements = {item.get("name") for item in center.get("elements", []) if isinstance(item, dict)}
    if center_elements != REQUIRED_CENTER_ELEMENTS:
        raise ValidationError(f"center elements mismatch: {sorted(center_elements)}")
    for item in center.get("elements", []):
        if item.get("name") != "1" and item.get("order") != 2:
            raise ValidationError("all nontrivial Spin(8) center elements must have order 2")

    outer = group.get("outer_automorphism_group", {})
    if outer.get("name") != "S_3" or outer.get("order") != 6:
        raise ValidationError("outer automorphism group must be S_3 of order 6")
    if outer.get("is_exceptional") is not True:
        raise ValidationError("triality must be marked exceptional")

    obstruction = record.get("structural_obstruction", {})
    if obstruction.get("name") != "no_cyclic_Z_6_in_center_or_pi_1":
        raise ValidationError("structural obstruction must be no_cyclic_Z_6_in_center_or_pi_1")
    text = (obstruction.get("description") or "") + " " + (obstruction.get("consequence") or "")
    if "no element of order 3 or 6" not in text:
        raise ValidationError("structural obstruction must explicitly rule out order 3 or 6 in the center")

    catalog = record.get("representation_catalog", {})
    if catalog.get("all_real_type") is not True:
        raise ValidationError("representation catalog must mark all listed reps real type")
    irreps = catalog.get("irreducibles", [])
    if not isinstance(irreps, list):
        raise ValidationError("irreducibles must be a list")
    names = {item.get("name") for item in irreps if isinstance(item, dict)}
    missing_reps = REQUIRED_EIGHT_DIM_REPS - names
    if missing_reps:
        raise ValidationError(f"missing three 8-dimensional triality reps: {sorted(missing_reps)}")
    for name in REQUIRED_EIGHT_DIM_REPS:
        match = next(item for item in irreps if item.get("name") == name)
        if match.get("dim") != 8 or match.get("fs_indicator") != 1:
            raise ValidationError(f"{name} must be 8-dimensional real type")
    for item in irreps:
        if item.get("fs_indicator") != 1:
            raise ValidationError("all listed Spin(8) irreps must have FS indicator +1")

    dim6 = record.get("dimension_6_question", {})
    if dim6.get("claim") != "no_faithful_6_dim_complex_rep_of_Spin_8":
        raise ValidationError("dimension_6_question must reject faithful 6-dimensional Spin(8) reps")
    if "does not extend" not in dim6.get("consequence", ""):
        raise ValidationError("dimension_6_question must state A_n dimension pattern does not extend")

    strategies = record.get("strategies", [])
    labels = {item.get("label") for item in strategies if isinstance(item, dict)}
    if labels != REQUIRED_STRATEGIES:
        raise ValidationError(f"strategies must be exactly A, B, C; got {sorted(labels)}")
    by_label = {item["label"]: item for item in strategies if isinstance(item, dict) and "label" in item}
    if by_label["B"].get("harness_P1_type") != "8x8_matrix":
        raise ValidationError("Strategy B must move P1 to an 8x8 matrix check")
    if by_label["B"].get("ad_hoc_level") != "low":
        raise ValidationError("Strategy B must be marked low ad-hocness")
    if by_label["A"].get("V_dim_minimum") != 8:
        raise ValidationError("Strategy A must preserve 8-dimensional minimum")

    assessment = record.get("comparative_assessment", {})
    if assessment.get("primary_recommendation") != "B":
        raise ValidationError("primary recommendation must be Strategy B")
    if set(assessment.get("backup_candidates", [])) != {"A", "C"}:
        raise ValidationError("backup candidates must be A and C")

    next_deliverable = record.get("next_concrete_deliverable", {})
    if next_deliverable.get("filename") != "docs/lawful-learning/14-d4-strategy-b-scoping.md":
        raise ValidationError("next concrete deliverable must be 14-d4-strategy-b-scoping.md")
    if next_deliverable.get("registry") != "registry/lawful-learning/d4-strategy-b-scoping.v0.1.json":
        raise ValidationError("next concrete registry must be d4-strategy-b-scoping.v0.1.json")

    rejected = set(record.get("rejected_invalid_claims_referenced", []))
    missing_rejected = REQUIRED_REJECTED_INVALIDS - rejected
    if missing_rejected:
        raise ValidationError(f"missing rejected invalid claims {sorted(missing_rejected)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate D4 representation inventory")
    parser.add_argument(
        "registry",
        nargs="?",
        default="registry/lawful-learning/d4-representation-inventory.v0.1.json",
    )
    args = parser.parse_args()

    try:
        validate_inventory(load_json(Path(args.registry)))
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    print(f"OK: {args.registry} validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
