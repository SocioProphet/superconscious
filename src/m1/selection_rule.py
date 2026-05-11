#!/usr/bin/env python3
"""Evaluate M1B witness-card promotion rule v1.

Rule v1 uses four hard gates and one advisory continuous cross-width score.
The cross-width score must be recorded, but it is not a hard promotion gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SELECTION_RULE_VERSION = "m1b-selection-rule.v1"
CONTRASTIVE_RATIO_THRESHOLD = 5.0
PATCHABILITY_MIN_RATIO_THRESHOLD = 0.5
CROSS_WIDTH_NOISE_FLOOR = 0.5


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def witness_data(card: dict[str, Any], name: str) -> dict[str, Any] | None:
    witness = card.get("witnesses", {}).get(name, {})
    if witness.get("status") != "collected":
        return None
    data = witness.get("data")
    return data if isinstance(data, dict) else None


def criterion(name: str, passes: bool, *, hard_gate: bool = True, **details: Any) -> dict[str, Any]:
    return {"name": name, "passes": bool(passes), "hard_gate": hard_gate, **details}


def evaluate(card: dict[str, Any]) -> dict[str, Any]:
    top_contexts = witness_data(card, "top_contexts")
    contrastive = witness_data(card, "contrastive_activation")
    causal = witness_data(card, "preliminary_causal")
    cross_width = witness_data(card, "cross_width_equivalence")
    patchability = witness_data(card, "patchability_profile")
    family = witness_data(card, "family_classification")

    criteria: list[dict[str, Any]] = []

    family_match = None
    if family:
        family_match = family.get("controller_spec_match")
    # Agreement is represented by family classification matching/partially matching controller spec.
    criteria.append(
        criterion(
            "witness_1_6_agreement",
            bool(top_contexts and family_match in {"match", "partial_match"}),
            controller_spec_match=family_match,
        )
    )

    activation_ratio = contrastive.get("activation_ratio") if contrastive else None
    criteria.append(
        criterion(
            "contrastive_ratio_5x",
            bool(activation_ratio is not None and activation_ratio >= CONTRASTIVE_RATIO_THRESHOLD),
            measured_ratio=activation_ratio,
            threshold=CONTRASTIVE_RATIO_THRESHOLD,
        )
    )

    criteria.append(
        criterion(
            "ablation_direction_correct",
            bool(causal and causal.get("passes_direction_check")),
            measured_direction=causal.get("measured_direction") if causal else None,
        )
    )

    patch_summary = patchability.get("patchability_summary") if patchability else None
    min_ratio = patch_summary.get("min_activation_ratio") if isinstance(patch_summary, dict) else None
    patch_pass = bool(patch_summary and patch_summary.get("passes_brittleness_check"))
    criteria.append(
        criterion(
            "patchability_not_pathological",
            patch_pass,
            min_ratio=min_ratio,
            threshold=PATCHABILITY_MIN_RATIO_THRESHOLD,
        )
    )

    cross_score = None
    above_noise = None
    if cross_width:
        cross_score = cross_width.get("cross_width_agreement_score")
        above_noise = cross_width.get("score_above_noise_floor")
    criteria.append(
        criterion(
            "cross_width_agreement_score_above_noise_floor",
            bool(above_noise),
            hard_gate=False,
            measured_score=cross_score,
            threshold=CROSS_WIDTH_NOISE_FLOOR,
            advisory_only=True,
        )
    )

    hard_criteria = [item for item in criteria if item.get("hard_gate")]
    hard_pass = all(item["passes"] for item in hard_criteria)
    promoted = hard_pass
    return {
        "rule_version": SELECTION_RULE_VERSION,
        "criteria": criteria,
        "advisory_scores": {
            "cross_width_agreement_score": cross_score,
            "cross_width_score_above_noise_floor": above_noise,
        },
        "all_hard_criteria_pass": hard_pass,
        "promoted": promoted,
    }


def apply_to_card(card: dict[str, Any]) -> dict[str, Any]:
    evaluation = evaluate(card)
    card.setdefault("promotion_status", {})
    card["promotion_status"]["selection_rule_evaluation"] = evaluation
    card["promotion_status"]["promoted_to_m1c"] = bool(evaluation["promoted"])
    card["promotion_status"]["current_stage"] = "promoted" if evaluation["promoted"] else "rejected"
    card["promotion_status"]["rejection_reason"] = None if evaluation["promoted"] else "one or more hard criteria failed"
    return card


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness_card", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    card = read_json(args.witness_card)
    updated = apply_to_card(card)
    if args.out:
        write_json(args.out, updated)
        print(args.out)
    else:
        print(json.dumps(updated["promotion_status"]["selection_rule_evaluation"], indent=2, sort_keys=True))
    return 0 if updated["promotion_status"]["promoted_to_m1c"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
