#!/usr/bin/env python3
"""Build Witness 4: cross-width agreement for M1B witness cards.

M1B v1 uses Option C: gated exhaustive matching.

1. Direction-space filter: select top-k 16k witness features whose decoder
   directions are most similar to the 131k primary feature decoder direction.
2. Effect-space verification: among those top-k candidates, select the feature
   whose precomputed ablation-effect vector has highest cosine similarity to
   the primary feature's ablation-effect vector.

This module consumes precomputed JSON/JSONL summaries. It does not load model
weights, SAE params, or run ablations. Runtime modules populate those summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

DEFAULT_TOP_K = 10
DEFAULT_NOISE_FLOOR = 0.5
L0_REGIME_NOTE = (
    "Primary and witness SAEs operate at different canonical L0s "
    "(131k average_l0_81 vs 16k average_l0_91). Cross-width agreement is "
    "continuous advisory evidence for M1B v1, not a hard promotion gate."
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(value)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def vector_from_row(row: dict[str, Any], keys: Iterable[str]) -> list[float]:
    for key in keys:
        value = row.get(key)
        if isinstance(value, list) and all(isinstance(item, (int, float)) for item in value):
            return [float(item) for item in value]
    raise ValueError(f"row lacks vector in keys {list(keys)}: feature={row.get('feature_index') or row.get('feature_id')}")


def feature_index(row: dict[str, Any]) -> int:
    for key in ("feature_index", "feature", "feature_id", "index"):
        value = row.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    raise ValueError(f"row lacks integer feature index: {row}")


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"vector length mismatch: {len(a)} != {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_primary(primary_rows: list[dict[str, Any]], target_index: int) -> dict[str, Any]:
    for row in primary_rows:
        if feature_index(row) == target_index:
            return row
    raise ValueError(f"primary feature_index not found: {target_index}")


def build_cross_width_witness(
    *,
    primary_feature: dict[str, Any],
    witness_rows: list[dict[str, Any]],
    top_k: int,
    noise_floor: float,
    test_set_ref: dict[str, Any],
) -> dict[str, Any]:
    primary_direction = vector_from_row(primary_feature, ("decoder_direction", "direction_vector", "decoder"))
    primary_effect = vector_from_row(primary_feature, ("ablation_effect_vector", "effect_vector", "effects"))
    primary_index = feature_index(primary_feature)

    direction_matches: list[dict[str, Any]] = []
    for row in witness_rows:
        try:
            witness_direction = vector_from_row(row, ("decoder_direction", "direction_vector", "decoder"))
            direction_score = cosine(primary_direction, witness_direction)
        except ValueError:
            continue
        direction_matches.append(
            {
                "row": row,
                "feature_index": feature_index(row),
                "direction_cosine_similarity": direction_score,
            }
        )

    direction_matches.sort(key=lambda item: item["direction_cosine_similarity"], reverse=True)
    top_matches = direction_matches[:top_k]

    best: dict[str, Any] | None = None
    top_directional_matches: list[dict[str, Any]] = []
    for rank, match in enumerate(top_matches, start=1):
        row = match["row"]
        effect_score: float | None = None
        effect_hash: str | None = None
        try:
            witness_effect = vector_from_row(row, ("ablation_effect_vector", "effect_vector", "effects"))
            effect_score = cosine(primary_effect, witness_effect)
            effect_hash = sha256_json(witness_effect)
        except ValueError:
            effect_score = None
        entry = {
            "rank": rank,
            "matched_feature_index": match["feature_index"],
            "direction_cosine_similarity": match["direction_cosine_similarity"],
            "effect_cosine_similarity": effect_score,
        }
        top_directional_matches.append(entry)
        if effect_score is not None and (best is None or effect_score > best["effect_cosine_similarity"]):
            best = {
                **entry,
                "ablation_effect_vector_sha256": effect_hash,
            }

    agreement = best["effect_cosine_similarity"] if best else None
    return {
        "status": "collected" if best else "failed",
        "data": {
            "compute_pattern": "option-c-gated-exhaustive",
            "directional_top_k": top_k,
            "primary_sae": {
                "width": "131k",
                "l0_directory": "average_l0_81",
                "feature_index": primary_index,
                "ablation_effect_vector_sha256": sha256_json(primary_effect),
            },
            "witness_sae": {
                "width": "16k",
                "l0_directory": "average_l0_91",
                "matched_feature_index": best["matched_feature_index"] if best else None,
                "cosine_similarity": agreement,
                "ablation_effect_vector_sha256": best["ablation_effect_vector_sha256"] if best else None,
            },
            "top_directional_matches": top_directional_matches,
            "l0_regime_note": L0_REGIME_NOTE,
            "cross_width_agreement_score": agreement,
            "noise_floor_threshold": noise_floor,
            "score_above_noise_floor": bool(agreement is not None and agreement >= noise_floor),
            "advisory_only": True,
            "deferred_widths": ["65k", "1M"],
            "deferred_to_milestone": "M3",
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary-summaries", type=Path, required=True, help="JSONL rows for 131k candidate features.")
    parser.add_argument("--witness-summaries", type=Path, required=True, help="JSONL rows for 16k witness features.")
    parser.add_argument("--feature-index", type=int, required=True)
    parser.add_argument("--test-set-ref", type=Path, required=True, help="JSON object with path/content_sha256/item_count.")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--noise-floor", type=float, default=DEFAULT_NOISE_FLOOR)
    parser.add_argument("--out", type=Path, default=Path("outputs/m1/witnesses/cross_width_equivalence.json"))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    primary_rows = read_jsonl(args.primary_summaries)
    witness_rows = read_jsonl(args.witness_summaries)
    primary = find_primary(primary_rows, args.feature_index)
    result = build_cross_width_witness(
        primary_feature=primary,
        witness_rows=witness_rows,
        top_k=args.top_k,
        noise_floor=args.noise_floor,
        test_set_ref=read_json(args.test_set_ref),
    )
    write_json(args.out, result)
    print(args.out)
    return 0 if result["status"] == "collected" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
