#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except Exception:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "integrations" / "tritfabric-advisory-consumption.v1.json"
REQUIRED_PROHIBITIONS = {
    "model-promotion",
    "community-eligibility-final-authority",
    "adapter-validation",
    "economic-credit-creation",
    "serve-deployment",
    "contract-override",
    "execution-authorization",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path) -> None:
    doc = load_json(path)
    schema = load_json(SCHEMA)
    if jsonschema is not None:
        jsonschema.validate(instance=doc, schema=schema)
    boundaries = doc.get("authority_boundaries", {})
    if boundaries.get("superconscious") != "advisory-coordinator":
        raise AssertionError("Superconscious must remain advisory-coordinator")
    if boundaries.get("tritfabric") != "implementation-contract-owner":
        raise AssertionError("TritFabric must remain implementation-contract-owner")
    prohibitions = set(doc.get("prohibited_authority", []))
    missing = REQUIRED_PROHIBITIONS - prohibitions
    if missing:
        raise AssertionError(f"missing prohibited authority entries: {sorted(missing)}")
    claim_boundary = doc.get("claim_boundary", "")
    for required_phrase in ("advisory", "does not own"):
        if required_phrase not in claim_boundary:
            raise AssertionError(f"claim_boundary must state {required_phrase!r}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_tritfabric_advisory_consumption.py <fixture.json>", file=sys.stderr)
        return 2
    validate(Path(argv[1]))
    print("tritfabric advisory boundary: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
