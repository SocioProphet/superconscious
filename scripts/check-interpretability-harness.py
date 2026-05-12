#!/usr/bin/env python3
"""Semantic checks for the v0 interpretability harness fixtures.

The JSON Schemas validate local shape. This script validates cross-file and
claim-admissibility invariants that schema-local checks cannot fully see.

Rules enforced in this v0 tranche:

- black-box providers may not expose hidden-state, residual-stream, attention,
  SAE, or transcoder observables;
- black-box providers may not expose feature-steering, activation-patching, or
  activation-addition interventions;
- registry-only providers may not claim live runtime execution or internal
  replay;
- provider refs in source locks, feature entries, and interventions must point
  to declared providers;
- source-lock refs in feature entries and interventions must point to declared
  source locks;
- feature-entry refs in interventions must point to declared feature entries;
- feature steering requires white-box access plus at least one SAE, transcoder,
  or probe source lock;
- activation patching requires white-box access plus a model or activation-cache
  source lock;
- prompt-only interventions must target prompts and must not carry source-lock
  requirements;
- files with `.invalid.` in the filename must fail at least one semantic rule;
- files without `.invalid.` must pass all semantic rules.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

FORBIDDEN_BLACK_BOX_OBSERVABLES = {
    "hidden_states",
    "residual_stream",
    "attention",
    "sae_features",
    "transcoder_features",
}

FORBIDDEN_BLACK_BOX_INTERVENTIONS = {
    "feature_steering",
    "activation_patching",
    "activation_addition",
}

FEATURE_STEERING_SOURCE_KINDS = {"sae", "transcoder", "probe"}
ACTIVATION_PATCHING_SOURCE_KINDS = {"model", "activation_cache"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_fixture_dir(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.glob("*.json")):
        rows.append((path, load_json(path)))
    return rows


def fixture_kind(value: dict[str, Any]) -> str:
    if value.get("binding_kind") == "provider-binding":
        return "provider-binding"
    if value.get("lock_kind") == "artifact-source-lock":
        return "artifact-source-lock"
    if value.get("entry_kind") == "feature-registry-entry":
        return "feature-registry-entry"
    if "intervention_kind" in value and "intervention_id" in value:
        return "intervention-spec"
    return "unknown"


def index_by(rows: list[tuple[Path, dict[str, Any]]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for _, value in rows:
        item_id = value.get(key)
        if isinstance(item_id, str):
            out[item_id] = value
    return out


def provider_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    access_mode = value.get("access_mode")
    observables = set(value.get("supported_observables") or [])
    interventions = set(value.get("supported_interventions") or [])
    runtime_claims = value.get("runtime_claims") or {}

    if access_mode == "black_box":
        forbidden_observables = sorted(observables & FORBIDDEN_BLACK_BOX_OBSERVABLES)
        if forbidden_observables:
            errors.append(f"black_box provider exposes forbidden observables: {forbidden_observables}")
        forbidden_interventions = sorted(interventions & FORBIDDEN_BLACK_BOX_INTERVENTIONS)
        if forbidden_interventions:
            errors.append(f"black_box provider exposes forbidden interventions: {forbidden_interventions}")

    if access_mode == "registry_only":
        if runtime_claims.get("live_runtime_execution"):
            errors.append("registry_only provider claims live runtime execution")
        if runtime_claims.get("internal_state_replay"):
            errors.append("registry_only provider claims internal-state replay")
        if runtime_claims.get("white_box_replay_possible"):
            errors.append("registry_only provider claims white-box replay")

    return errors


def source_lock_errors(value: dict[str, Any], providers: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    provider_ref = value.get("provider_binding_ref") or {}
    provider_id = provider_ref.get("provider_binding_id")
    access_mode = provider_ref.get("access_mode")
    artifact_kind = value.get("artifact_kind")

    provider = providers.get(provider_id)
    if provider is None:
        errors.append(f"unknown provider_binding_id: {provider_id}")
    elif provider.get("access_mode") != access_mode:
        errors.append(
            f"provider access mode mismatch for {provider_id}: "
            f"ref={access_mode}, provider={provider.get('access_mode')}"
        )

    if artifact_kind == "sae" and access_mode not in {"white_box", "registry_only"}:
        errors.append("SAE source lock must be white_box or registry_only")
    if artifact_kind == "feature_registry_entry" and access_mode not in {"registry_only", "white_box"}:
        errors.append("feature registry source lock must be registry_only or white_box")

    return errors


def feature_entry_errors(
    value: dict[str, Any],
    providers: dict[str, dict[str, Any]],
    source_locks: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    registry_source = value.get("registry_source") or {}
    provider_id = registry_source.get("provider_binding_id")
    if provider_id not in providers:
        errors.append(f"unknown provider_binding_id in registry_source: {provider_id}")

    for ref in value.get("source_lock_refs") or []:
        lock_id = ref.get("source_lock_id")
        if lock_id not in source_locks:
            errors.append(f"unknown source_lock_id in feature entry: {lock_id}")

    if value.get("claim_status") != "candidate_only" and not value.get("evidence_refs"):
        errors.append("promoted feature entry lacks evidence_refs")

    return errors


def intervention_errors(
    value: dict[str, Any],
    providers: dict[str, dict[str, Any]],
    source_locks: dict[str, dict[str, Any]],
    feature_entries: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    intervention_kind = value.get("intervention_kind")
    provider_ref = value.get("provider_binding_ref") or {}
    provider_id = provider_ref.get("provider_binding_id")
    access_mode = provider_ref.get("access_mode")
    provider = providers.get(provider_id)

    if provider is None:
        errors.append(f"unknown provider_binding_id in intervention: {provider_id}")
    elif provider.get("access_mode") != access_mode:
        errors.append(
            f"provider access mode mismatch in intervention for {provider_id}: "
            f"ref={access_mode}, provider={provider.get('access_mode')}"
        )

    target = value.get("target") or {}
    feature_entry_id = target.get("feature_entry_id")
    if feature_entry_id is not None and feature_entry_id not in feature_entries:
        errors.append(f"unknown feature_entry_id in intervention target: {feature_entry_id}")

    source_refs = value.get("required_source_locks") or []
    source_kinds = {ref.get("artifact_kind") for ref in source_refs}
    for ref in source_refs:
        lock_id = ref.get("source_lock_id")
        if lock_id not in source_locks:
            errors.append(f"unknown source_lock_id in intervention: {lock_id}")

    if intervention_kind == "feature_steering":
        if access_mode != "white_box":
            errors.append("feature_steering requires white_box provider access")
        if not source_kinds.intersection(FEATURE_STEERING_SOURCE_KINDS):
            errors.append("feature_steering requires SAE, transcoder, or probe source lock")
        safety_policy = value.get("safety_policy") or {}
        if not safety_policy.get("policy_decision_required"):
            errors.append("feature_steering requires policy_decision_required")
        if not safety_policy.get("off_target_audit_required"):
            errors.append("feature_steering requires off_target_audit_required")

    if intervention_kind == "activation_patching":
        if access_mode != "white_box":
            errors.append("activation_patching requires white_box provider access")
        if not source_kinds.intersection(ACTIVATION_PATCHING_SOURCE_KINDS):
            errors.append("activation_patching requires model or activation_cache source lock")

    if intervention_kind == "prompt_only":
        if target.get("target_kind") != "prompt":
            errors.append("prompt_only intervention must target prompt")
        if source_refs:
            errors.append("prompt_only intervention should not require source locks")

    if intervention_kind in FORBIDDEN_BLACK_BOX_INTERVENTIONS and access_mode == "black_box":
        errors.append(f"{intervention_kind} is forbidden for black_box provider access")

    return errors


def semantic_errors(
    path: Path,
    value: dict[str, Any],
    providers: dict[str, dict[str, Any]],
    source_locks: dict[str, dict[str, Any]],
    feature_entries: dict[str, dict[str, Any]],
) -> list[str]:
    kind = fixture_kind(value)
    if kind == "provider-binding":
        return provider_errors(value)
    if kind == "artifact-source-lock":
        return source_lock_errors(value, providers)
    if kind == "feature-registry-entry":
        return feature_entry_errors(value, providers, source_locks)
    if kind == "intervention-spec":
        return intervention_errors(value, providers, source_locks, feature_entries)
    return [f"unknown fixture kind for {path.name}"]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture_dir", type=Path, help="Directory containing interpretability harness fixtures.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    rows = load_fixture_dir(args.fixture_dir)
    providers = index_by(rows, "provider_binding_id")
    source_locks = index_by(rows, "source_lock_id")
    feature_entries = index_by(rows, "feature_entry_id")

    failed = False
    for path, value in rows:
        errors = semantic_errors(path, value, providers, source_locks, feature_entries)
        expected_invalid = ".invalid." in path.name
        if expected_invalid and not errors:
            print(f"FAIL {path}: expected semantic failure, got pass")
            failed = True
        elif not expected_invalid and errors:
            print(f"FAIL {path}: unexpected semantic errors:")
            for error in errors:
                print(f"  - {error}")
            failed = True
        else:
            status = "expected-fail" if expected_invalid else "ok"
            print(f"{status}: {path.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
