#!/usr/bin/env python3
"""M1 feature-selection funnel scaffold.

This script implements the non-GPU bookkeeping portions of the four-stage M1
feature-selection protocol. It consumes exported feature/context summaries and
activation/probe summaries, applies deterministic filters, and writes the JSONL
artifacts expected by the M1 issue.

GPU-specific activation extraction, SAE decoding, and intervention hooks belong
in follow-on scripts or notebooks. This script is intentionally data-shape-first:
it makes the funnel auditable before heavy compute begins.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

REFUSAL_PATTERNS = [
    r"\bi\s+cannot\b",
    r"\bi\s+can't\b",
    r"\bi\s+am\s+not\s+able\b",
    r"\bi'm\s+not\s+able\b",
    r"\bi\s+won't\b",
    r"\bi\s+will\s+not\b",
    r"\bnot\s+appropriate\b",
    r"\bcan't\s+assist\b",
    r"\bcannot\s+assist\b",
]

HARM_PATTERNS = [
    r"\bharmful\b",
    r"\bdangerous\b",
    r"\billegal\b",
    r"\bweapon\b",
    r"\bexplosive\b",
    r"\bbypass\b",
    r"\bmalware\b",
    r"\bphishing\b",
    r"\binappropriate\s+request\b",
]

REDIRECT_PATTERNS = [
    r"\binstead\b",
    r"\bi\s+can\s+help\b",
    r"\blet\s+me\s+suggest\b",
    r"\bsafer\s+alternative\b",
    r"\bhowever,?\s+i\s+can\b",
]

POLICY_META_PATTERNS = [
    r"\bas\s+an\s+ai\b",
    r"\bmy\s+guidelines\b",
    r"\bpolicy\b",
    r"\bsafety\s+guidelines\b",
    r"\bcan't\s+provide\b",
]

COMPILED_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "refusal": [re.compile(p, re.IGNORECASE) for p in REFUSAL_PATTERNS],
    "harm_detection": [re.compile(p, re.IGNORECASE) for p in HARM_PATTERNS],
    "redirect": [re.compile(p, re.IGNORECASE) for p in REDIRECT_PATTERNS],
    "policy_meta": [re.compile(p, re.IGNORECASE) for p in POLICY_META_PATTERNS],
}


@dataclass(frozen=True)
class FunnelThresholds:
    min_context_hits: int = 2
    min_activation_ratio: float = 3.0
    min_causal_delta: float = 0.05


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected object row")
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def extract_texts(row: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    for key in ("top_contexts", "contexts", "examples", "top_activating_examples"):
        value = row.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    texts.append(item)
                elif isinstance(item, dict):
                    for text_key in ("text", "context", "snippet", "example"):
                        if isinstance(item.get(text_key), str):
                            texts.append(item[text_key])
                            break
    for key in ("description", "label", "summary"):
        if isinstance(row.get(key), str):
            texts.append(row[key])
    return texts


def match_categories(texts: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {name: 0 for name in COMPILED_PATTERNS}
    for text in texts:
        for name, patterns in COMPILED_PATTERNS.items():
            if any(pattern.search(text) for pattern in patterns):
                counts[name] += 1
    return counts


def feature_id(row: dict[str, Any]) -> str:
    for key in ("feature_id", "feature", "id", "index", "neuron_id"):
        value = row.get(key)
        if value is not None:
            return str(value)
    raise ValueError(f"feature row lacks id field: {row}")


def stage1_candidate_pool(feature_rows: list[dict[str, Any]], thresholds: FunnelThresholds) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for row in feature_rows:
        texts = extract_texts(row)
        category_counts = match_categories(texts)
        total_hits = sum(category_counts.values())
        if total_hits < thresholds.min_context_hits:
            continue
        candidates.append(
            {
                "feature_id": feature_id(row),
                "stage": "candidate_pool",
                "category_counts": category_counts,
                "total_hits": total_hits,
                "source_keys": sorted(k for k in row if k in {"description", "label", "top_contexts", "contexts", "examples", "top_activating_examples"}),
                "selected_text_examples": texts[:5],
            }
        )
    candidates.sort(key=lambda item: (item["total_hits"], item["feature_id"]), reverse=True)
    return candidates


def index_by_feature(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {feature_id(row): row for row in rows}


def mean_from_row(row: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = row.get(key)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, list) and value and all(isinstance(x, (int, float)) for x in value):
            return float(statistics.fmean(value))
    return None


def stage2_behavioral_filter(
    candidates: list[dict[str, Any]],
    activation_rows: list[dict[str, Any]],
    thresholds: FunnelThresholds,
) -> list[dict[str, Any]]:
    by_feature = index_by_feature(activation_rows)
    survivors: list[dict[str, Any]] = []
    for candidate in candidates:
        fid = candidate["feature_id"]
        row = by_feature.get(fid)
        if row is None:
            continue
        harmful = mean_from_row(row, ("harmful_mean", "refusal_mean", "unsafe_mean", "positive_mean", "harm_pressure_mean"))
        benign = mean_from_row(row, ("benign_mean", "innocuous_mean", "safe_mean", "negative_mean"))
        if harmful is None or benign is None:
            continue
        ratio = harmful / max(benign, 1e-9)
        if ratio < thresholds.min_activation_ratio:
            continue
        survivors.append(
            {
                **candidate,
                "stage": "behavioral_filter",
                "harmful_mean": harmful,
                "benign_mean": benign,
                "activation_ratio": ratio,
            }
        )
    survivors.sort(key=lambda item: (item["activation_ratio"], item["total_hits"]), reverse=True)
    return survivors


def stage3_causal_filter(
    behavioral_rows: list[dict[str, Any]],
    causal_rows: list[dict[str, Any]],
    thresholds: FunnelThresholds,
) -> list[dict[str, Any]]:
    by_feature = index_by_feature(causal_rows)
    survivors: list[dict[str, Any]] = []
    for row in behavioral_rows:
        fid = row["feature_id"]
        causal = by_feature.get(fid)
        if causal is None:
            continue
        delta = mean_from_row(causal, ("compliance_delta", "accuracy_delta", "answer_rate_delta", "causal_delta"))
        if delta is None or delta < thresholds.min_causal_delta:
            continue
        survivors.append({**row, "stage": "causal_filter", "causal_delta": delta})
    survivors.sort(key=lambda item: (item["causal_delta"], item["activation_ratio"]), reverse=True)
    return survivors


def family_label(category_counts: dict[str, int]) -> str:
    if not category_counts:
        return "unknown"
    ranked = sorted(category_counts.items(), key=lambda item: item[1], reverse=True)
    top_name, top_count = ranked[0]
    if top_count == 0:
        return "unknown"
    return top_name


def write_family_classification(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# M1 Family Classification", "", "## Survivors", ""]
    if not rows:
        lines.append("No causal-filter survivors. Diagnose feature source, activation probes, or thresholds.\n")
    for row in rows:
        label = family_label(row.get("category_counts", {}))
        lines.extend(
            [
                f"### Feature {row['feature_id']}",
                "",
                f"- proposed family: `{label}`",
                f"- activation ratio: `{row.get('activation_ratio')}`",
                f"- causal delta: `{row.get('causal_delta')}`",
                f"- category counts: `{json.dumps(row.get('category_counts', {}), sort_keys=True)}`",
                "- selected context examples:",
            ]
        )
        for text in row.get("selected_text_examples", [])[:3]:
            compact = " ".join(str(text).split())[:300]
            lines.append(f"  - {compact}")
        lines.append("")
    write_markdown(path, "\n".join(lines))


def select_feature(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "selected": False,
            "reason": "no causal-filter survivors",
        }
    refuse_redirect = [
        row
        for row in rows
        if family_label(row.get("category_counts", {})) in {"refusal", "redirect", "policy_meta"}
    ]
    pool = refuse_redirect or rows
    best = sorted(pool, key=lambda item: (item.get("causal_delta", 0), item.get("activation_ratio", 0)), reverse=True)[0]
    return {
        "selected": True,
        "feature_id": best["feature_id"],
        "proposed_family": family_label(best.get("category_counts", {})),
        "selection_rule": "highest causal_delta then activation_ratio among refusal/redirect/policy_meta survivors; fallback to all survivors",
        "selected_row": best,
        "control_candidate_feature_ids": [row["feature_id"] for row in rows if row["feature_id"] != best["feature_id"]][:10],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True, help="JSONL exported feature/context summaries.")
    parser.add_argument("--activation-summary", type=Path, help="Optional JSONL feature activation summaries for Stage 2.")
    parser.add_argument("--causal-summary", type=Path, help="Optional JSONL causal probe summaries for Stage 3.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/m1"))
    parser.add_argument("--min-context-hits", type=int, default=FunnelThresholds.min_context_hits)
    parser.add_argument("--min-activation-ratio", type=float, default=FunnelThresholds.min_activation_ratio)
    parser.add_argument("--min-causal-delta", type=float, default=FunnelThresholds.min_causal_delta)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    thresholds = FunnelThresholds(
        min_context_hits=args.min_context_hits,
        min_activation_ratio=args.min_activation_ratio,
        min_causal_delta=args.min_causal_delta,
    )

    feature_rows = read_jsonl(args.features)
    candidates = stage1_candidate_pool(feature_rows, thresholds)
    write_jsonl(args.out_dir / "candidate_pool.jsonl", candidates)

    behavioral_rows: list[dict[str, Any]] = []
    if args.activation_summary:
        behavioral_rows = stage2_behavioral_filter(candidates, read_jsonl(args.activation_summary), thresholds)
        write_jsonl(args.out_dir / "behavioral_filter.jsonl", behavioral_rows)

    causal_rows: list[dict[str, Any]] = []
    if args.causal_summary:
        if not behavioral_rows:
            behavioral_rows = candidates
        causal_rows = stage3_causal_filter(behavioral_rows, read_jsonl(args.causal_summary), thresholds)
        write_jsonl(args.out_dir / "causal_filter.jsonl", causal_rows)
        write_family_classification(args.out_dir / "family_classification.md", causal_rows)
        write_json(args.out_dir / "selected_feature.json", select_feature(causal_rows))
    else:
        write_family_classification(args.out_dir / "family_classification.md", behavioral_rows or candidates)
        write_json(args.out_dir / "selected_feature.json", select_feature(behavioral_rows or candidates))

    print(args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
