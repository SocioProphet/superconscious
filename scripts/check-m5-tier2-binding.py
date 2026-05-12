#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_NON_CLAIMS = {
    "no_runtime_receipt_lookup",
    "no_runtime_non_claim_verification",
    "no_runtime_monitor_attestation",
    "no_timestamp_authenticity",
    "opaque_hashes_not_resolved",
    "no_runtime_publication_gate",
    "no_peer_review_substitution",
}

FORBIDDEN_RUNTIME_OR_FULL_COMPOSITION_FIELDS = {
    "receipt_integration",
    "authority_scope_analysis",
    "non_claim_analysis",
    "monitor_independence_analysis",
    "evidence_freshness_analysis",
    "evidence_receipt_refs",
    "constituent_authority_chain_refs",
    "composition_authority_chain_ref",
    "composition_rule",
    "composed_authority_scope",
    "execution_status",
    "ledger_entry",
    "runtime_receipt_lookup",
    "resolved_at",
    "monitor_attestation_token",
    "timestamp_authenticity_proof",
    "runtime_publication_gate",
    "publication_gate_passed",
    "peer_review_status",
    "peer_review_substitution",
    "external_publication_approval",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check-m5-tier2-binding.py <fixture.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    non_claims = set(data.get("non_claims", []))
    if non_claims != REQUIRED_NON_CLAIMS:
        missing = sorted(REQUIRED_NON_CLAIMS - non_claims)
        extra = sorted(non_claims - REQUIRED_NON_CLAIMS)
        print(
            f"non_claims must exactly match required M5 doctrine boundary; missing={missing} extra={extra}",
            file=sys.stderr,
        )
        return 1

    forbidden_present = sorted(FORBIDDEN_RUNTIME_OR_FULL_COMPOSITION_FIELDS & set(data))
    if forbidden_present:
        print(
            "M5 Tier 2 binding fixture must remain doctrine-only; forbidden fields present: "
            + ", ".join(forbidden_present),
            file=sys.stderr,
        )
        return 1

    for idx, ref in enumerate(data.get("upstream_certificate_refs", [])):
        opaque_hash = ref.get("opaque_hash", "")
        if not opaque_hash.startswith("sha256:"):
            print(f"upstream_certificate_refs[{idx}].opaque_hash must use sha256: prefix", file=sys.stderr)
            return 1

    publication_hash = data.get("publication_surface_ref", {}).get("opaque_hash", "")
    if not publication_hash.startswith("sha256:"):
        print("publication_surface_ref.opaque_hash must use sha256: prefix", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
