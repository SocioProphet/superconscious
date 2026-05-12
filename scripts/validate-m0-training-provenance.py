#!/usr/bin/env python3
"""Semantic validation for M0 training provenance certificates."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_NON_CLAIM = "Does not prove SGD ran correctly."
COMMITMENT_KEYS = [
    "dataset",
    "code",
    "config",
    "seed",
    "base_model",
    "checkpoint",
    "eval_spec",
    "compute_environment",
]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def expected_interpretation(index: float) -> str:
    if index == 1.0:
        return "fully_provenance_certified"
    if 0.625 <= index <= 0.875:
        return "partial_provenance"
    if 0.25 <= index <= 0.5:
        return "minimal_provenance"
    if 0.0 <= index <= 0.125:
        return "no_provenance_external_artifact"
    return "out_of_band"


def validate(path: Path) -> list[str]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    commitments = doc.get("commitments", {})
    missing = [key for key in COMMITMENT_KEYS if key not in commitments]
    if missing:
        errors.append(f"missing commitments: {', '.join(missing)}")

    available = sum(1 for key in COMMITMENT_KEYS if commitments.get(key, {}).get("status") == "available")
    expected_index = available / len(COMMITMENT_KEYS)
    actual_index = doc.get("provenance_completeness", {}).get("index")
    if actual_index is None or abs(float(actual_index) - expected_index) > 1e-9:
        errors.append(f"provenance_completeness.index must equal available_commitments/8 ({expected_index})")

    actual_interpretation = doc.get("provenance_completeness", {}).get("interpretation")
    derived_interpretation = expected_interpretation(expected_index)
    if actual_interpretation != derived_interpretation:
        errors.append(f"provenance_completeness.interpretation must be {derived_interpretation}")

    temporal = doc.get("temporal_constraints", {})
    model_at = temporal.get("model_commitment_at")
    eval_at = temporal.get("eval_spec_commitment_at")
    precedes = temporal.get("model_precedes_eval_spec")
    non_claims = doc.get("non_claims", [])

    if REQUIRED_NON_CLAIM not in non_claims:
        errors.append(f"non_claims must include {REQUIRED_NON_CLAIM!r}")

    if model_at and eval_at:
        if precedes is not (parse_time(model_at) < parse_time(eval_at)):
            errors.append("model_precedes_eval_spec must match timestamp ordering")
    else:
        if precedes is not False:
            errors.append("model_precedes_eval_spec must be false when either timestamp is null")
        if not any("Cannot verify" in claim or "not available" in claim for claim in non_claims):
            errors.append("null temporal commitments require an explicit non-claim about unavailable timestamps")

    external = doc.get("provenance_completeness", {}).get("external_artifact_flag")
    if external:
        unavailable_count = sum(
            1
            for key in COMMITMENT_KEYS
            if commitments.get(key, {}).get("status") in {"publicly_unavailable", "unknown"}
        )
        if unavailable_count == 0:
            errors.append("external artifacts must expose unavailable or unknown upstream commitments")
        if not any("External artifact" in claim for claim in non_claims):
            errors.append("external artifacts require an explicit external-artifact non-claim")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    errors = validate(args.certificate)
    if errors:
        for error in errors:
            print(f"{args.certificate}: {error}", file=sys.stderr)
        return 1
    print(f"OK {args.certificate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
