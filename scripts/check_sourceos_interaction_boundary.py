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
SCHEMA = ROOT / "schemas" / "integrations" / "sourceos-interaction-boundary.v1.json"

REQUIRED_BOUNDARIES = {
    "superconscious": "task-cognition-coordinator",
    "sourceos_spec": "canonical-schema-owner",
    "policy_fabric": "policy-admission-authority",
    "agent_registry": "identity-grant-authority",
    "memory_mesh": "memory-context-pack-authority",
    "agentplane": "execution-evidence-replay-authority",
    "model_router": "sourceos-routing-authority",
}

FORBIDDEN_PAYLOAD_TERMS = {
    "chain-of-thought",
    "private reasoning",
    "raw secret",
    "credential dump",
    "unrestricted transcript",
    "unrestricted shell output",
    "browser history dump",
}

REQUIRED_CLAIM_PHRASES = (
    "bounded task context",
    "does not own policy admission",
    "agent grants",
    "memory writeback",
    "model routing",
    "AgentPlane evidence",
    "replay authority",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path) -> None:
    doc = load_json(path)
    schema = load_json(SCHEMA)

    if jsonschema is not None:
        jsonschema.validate(instance=doc, schema=schema)

    boundaries = doc.get("authority_boundaries", {})
    for key, expected in REQUIRED_BOUNDARIES.items():
        if boundaries.get(key) != expected:
            raise AssertionError(f"authority boundary drift for {key}: expected {expected!r}")

    payload_mode = doc.get("payload_mode")
    if payload_mode not in {"metadata-only", "summary", "ref-only", "inline-bounded", "redacted"}:
        raise AssertionError(f"invalid payload mode: {payload_mode!r}")

    serialized = json.dumps(doc, sort_keys=True)
    lowered = serialized.lower()
    for term in FORBIDDEN_PAYLOAD_TERMS:
        if term in lowered:
            raise AssertionError(f"forbidden payload term present: {term!r}")

    claim_boundary = doc.get("claim_boundary", "")
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in claim_boundary:
            raise AssertionError(f"claim_boundary must include {phrase!r}")

    if doc.get("source_interaction_event_ref") == doc.get("result_interaction_event_ref"):
        raise AssertionError("source and result interaction event refs must be distinct")

    if not doc.get("source_interaction_event_ref", "").startswith("urn:srcos:interaction-event:"):
        raise AssertionError("source_interaction_event_ref must be an interaction-event URN")

    if not doc.get("result_interaction_event_ref", "").startswith("urn:srcos:interaction-event:"):
        raise AssertionError("result_interaction_event_ref must be an interaction-event URN")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_sourceos_interaction_boundary.py <fixture.json>", file=sys.stderr)
        return 2
    validate(Path(argv[1]))
    print("sourceos interaction boundary: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
