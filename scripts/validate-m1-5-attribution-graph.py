#!/usr/bin/env python3
"""Semantic validation for M1.5 attribution graph certificates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(path: Path) -> list[str]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if doc.get("graph_manifest_digest") == doc.get("graph_full_digest"):
        errors.append("graph manifest and full digests must differ")

    edge_ids = set()
    for edge in doc.get("edges", []):
        edge_id = edge.get("edge_id")
        if edge_id in edge_ids:
            errors.append(f"duplicate edge_id: {edge_id}")
        edge_ids.add(edge_id)
        if edge.get("manifest_digest") == edge.get("full_digest"):
            errors.append(f"edge {edge_id} manifest and full digests must differ")

    replay = doc.get("replay_verification") or {}
    state = replay.get("replay_state")
    changed = replay.get("divergent_edges", [])
    if state == "manifest_diverges" and not changed:
        errors.append("manifest_diverges replay requires at least one edge id")
    if state in {"bit_exact_replay", "manifest_matches_latent_diverges"} and changed:
        errors.append("verified replay states must not list changed manifest edges")
    for edge_id in changed:
        if edge_id not in edge_ids:
            errors.append(f"unknown edge id in replay report: {edge_id}")

    assessment = doc.get("implementability_assessment", {})
    claimed = assessment.get("g_claimed_count")
    if isinstance(claimed, int) and claimed != len(edge_ids):
        errors.append("g_claimed_count must equal the number of claimed edges")

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
