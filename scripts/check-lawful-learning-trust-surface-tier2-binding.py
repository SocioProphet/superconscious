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
    "no_runtime_circuit_discovery",
    "no_runtime_ablation_verification",
    "no_tag_promotion_at_composition",
    "no_substrate_verification",
    "no_frontier_claim_promotion",
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
    "runtime_circuit_discovery",
    "runtime_ablation_verification",
    "tag_promotion_at_composition",
    "substrate_verification",
    "frontier_claim_promotion",
    "promoted_claim_tier",
    "runtime_substrate_check",
    "runtime_discovered_circuits",
}

HASH_REF_FIELDS = (
    "substrate_component_refs",
    "structure_component_refs",
    "mixture_slot_refs",
)

SINGLE_HASH_REF_FIELDS = (
    "adapter_dag_ref",
    "circuit_registry_ref",
    "claim_ledger_ref",
)


def _check_hash_ref(ref: dict, label: str) -> tuple[bool, str]:
    opaque_hash = ref.get("opaque_hash", "")
    if not opaque_hash.startswith("sha256:"):
        return False, f"{label}.opaque_hash must use sha256: prefix"
    return True, ""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check-lawful-learning-trust-surface-tier2-binding.py <fixture.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    non_claims = set(data.get("non_claims", []))
    if non_claims != REQUIRED_NON_CLAIMS:
        missing = sorted(REQUIRED_NON_CLAIMS - non_claims)
        extra = sorted(non_claims - REQUIRED_NON_CLAIMS)
        print(
            f"non_claims must exactly match required lawful-learning doctrine boundary; missing={missing} extra={extra}",
            file=sys.stderr,
        )
        return 1

    forbidden_present = sorted(FORBIDDEN_RUNTIME_OR_FULL_COMPOSITION_FIELDS & set(data))
    if forbidden_present:
        print(
            "lawful-learning Tier 2 binding fixture must remain doctrine-only; forbidden fields present: "
            + ", ".join(forbidden_present),
            file=sys.stderr,
        )
        return 1

    for field in HASH_REF_FIELDS:
        for idx, ref in enumerate(data.get(field, [])):
            ok, message = _check_hash_ref(ref, f"{field}[{idx}]")
            if not ok:
                print(message, file=sys.stderr)
                return 1

    for field in SINGLE_HASH_REF_FIELDS:
        ok, message = _check_hash_ref(data.get(field, {}), field)
        if not ok:
            print(message, file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
