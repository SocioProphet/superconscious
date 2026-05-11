#!/usr/bin/env python3
"""Verify an M1A source-lock certificate fragment.

Exit codes:
  0: full verification passed.
  1: partial verification passed; pending artifacts such as weights were not downloaded.
  2: verification failed.
  3: schema validation failed.
  4: network failure or upstream artifact unavailable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from .certificate_utils import (
    append_ledger,
    canonical_json,
    fetch_hf_model_metadata,
    file_record,
    git_commit_sha,
    git_status_porcelain,
    hf_sibling_paths,
    ledger_event,
    read_json,
    repo_root,
    schema_validate_basic,
    sha256_file,
    sha256_json,
    strip_keys,
    try_jsonschema_validate,
)

DEFAULT_CERTIFICATE = "outputs/m1/certificates/m1a-source-lock.json"
DEFAULT_SCHEMA = "schemas/m1/source-lock.v1.json"
DEFAULT_LEDGER = "outputs/m1/evidence-ledger.jsonl"
DEFAULT_SAE_PARAMS = "layer_20/width_131k/average_l0_81/params.npz"


def check(ok: bool, label: str, failures: list[str], *, detail: str = "") -> None:
    status = "OK" if ok else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"{label:<68} {status}{suffix}")
    if not ok:
        failures.append(f"{label}{suffix}")


def check_schema(cert: dict[str, Any], schema: dict[str, Any] | None) -> list[str]:
    errors = schema_validate_basic(cert)
    if schema is not None:
        errors.extend(try_jsonschema_validate(cert, schema))
    return errors


def recompute_fragment_hash(cert: dict[str, Any]) -> str:
    clone = dict(cert)
    clone["ledger_entry"] = dict(cert["ledger_entry"])
    clone["ledger_entry"]["fragment_sha256"] = None
    first = sha256_json(clone)
    clone["ledger_entry"]["fragment_sha256"] = first
    return sha256_json(clone)


def recompute_content_hash(cert: dict[str, Any]) -> str:
    stripped = strip_keys(cert, {"generated_at", "sealed_at", "fragment_sha256", "content_sha256_canonical"})
    return sha256_json(stripped)


def verify_controller_spec(root: Path, cert: dict[str, Any], failures: list[str]) -> None:
    ref = cert["controller_spec_ref"]
    record = file_record(root, ref["path"])
    check(record["exists"], "[2/8] Controller spec exists", failures, detail=ref["path"])
    if record["exists"]:
        check(record["content_sha256"] == ref["content_sha256"], "[2/8] Controller spec content hash", failures)
        check(record["git_blob_sha"] == ref["git_blob_sha"], "[2/8] Controller spec git blob hash", failures)


def verify_code(root: Path, cert: dict[str, Any], failures: list[str], *, explain: bool) -> None:
    code = cert["code"]
    status = git_status_porcelain(root)
    current_commit = git_commit_sha(root)
    check(current_commit == code["commit_sha"], "[3/8] Git commit matches certificate", failures, detail=current_commit)
    clean_now = len(status) == 0
    check(clean_now == code["commit_clean"], "[3/8] Git clean-state matches certificate", failures, detail=f"clean={clean_now}")

    checked = 0
    mismatches: list[str] = []
    for section in ("scripts", "configs", "schemas"):
        for rec in code.get(section, []):
            checked += 1
            current = file_record(root, rec["path"])
            if current["exists"] != rec["exists"] or current["content_sha256"] != rec["content_sha256"]:
                mismatches.append(rec["path"])
                if explain:
                    print(f"    mismatch {rec['path']}: expected={rec.get('content_sha256')} actual={current.get('content_sha256')}")
    check(not mismatches, "[4/8] Scripts/configs/schema hashes", failures, detail=f"{checked - len(mismatches)}/{checked} match")


def verify_schema_self(root: Path, cert: dict[str, Any], failures: list[str]) -> None:
    schema_records = cert["code"].get("schemas", [])
    if not schema_records:
        check(False, "[5/8] Schema self-hash", failures, detail="no schema records")
        return
    ok = True
    for rec in schema_records:
        current = file_record(root, rec["path"])
        if current["content_sha256"] != rec["content_sha256"]:
            ok = False
    check(ok, "[5/8] Schema self-hash", failures)


def verify_hf(root: Path, cert: dict[str, Any], failures: list[str], network_errors: list[str], *, offline: bool) -> None:
    if offline:
        print(f"{'[6/8] Resolving model metadata from Hugging Face':<68} SKIP (offline)")
        print(f"{'[7/8] Resolving SAE metadata from Hugging Face':<68} SKIP (offline)")
        return

    try:
        model_meta = fetch_hf_model_metadata(cert["model"]["huggingface_repo"], cert["model"]["repo_commit_sha"] or "main")
        ok = (model_meta.get("sha") == cert["model"]["repo_commit_sha"]) or (cert["model"]["repo_commit_sha"] in {None, "main"})
        check(ok, "[6/8] Resolving model metadata from Hugging Face", failures, detail=str(model_meta.get("sha")))
    except Exception as exc:  # noqa: BLE001
        network_errors.append(str(exc))
        print(f"{'[6/8] Resolving model metadata from Hugging Face':<68} ERROR ({exc})")

    try:
        sae_meta = fetch_hf_model_metadata(cert["sae"]["huggingface_repo"], cert["sae"]["repo_commit_sha"] or "main")
        paths = hf_sibling_paths(sae_meta)
        ok_commit = (sae_meta.get("sha") == cert["sae"]["repo_commit_sha"]) or (cert["sae"]["repo_commit_sha"] in {None, "main"})
        ok_path = DEFAULT_SAE_PARAMS in paths
        check(ok_commit and ok_path, "[7/8] Resolving SAE metadata from Hugging Face", failures, detail=str(sae_meta.get("sha")))
    except Exception as exc:  # noqa: BLE001
        network_errors.append(str(exc))
        print(f"{'[7/8] Resolving SAE metadata from Hugging Face':<68} ERROR ({exc})")


def verify_weight_status(cert: dict[str, Any], failures: list[str], partials: list[str], *, strict: bool) -> None:
    status = cert["model"]["weights_manifest"]["weights_verification_status"]
    sae_downloaded = cert["sae"]["params_downloaded"]
    if status == "verified" and sae_downloaded and cert["sae"].get("params_npz_sha256"):
        check(True, "[8/8] Verifying weights/SAE params", failures, detail="verified")
        return
    message = f"weights={status}; sae_downloaded={sae_downloaded}"
    if strict:
        check(False, "[8/8] Verifying weights/SAE params", failures, detail=message)
    else:
        partials.append(message)
        print(f"{'[8/8] Verifying weights/SAE params':<68} SKIP ({message})")


def append_verification_ledger(root: Path, cert: dict[str, Any], event: str, details: dict[str, Any]) -> None:
    append_ledger(
        root / DEFAULT_LEDGER,
        ledger_event(
            event=event,
            fragment_id=cert["ledger_entry"]["fragment_id"],
            fragment_sha256=cert["ledger_entry"].get("fragment_sha256"),
            tool="src/m1/verify_source_lock.py",
            details=details,
        ),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", default=DEFAULT_CERTIFICATE)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--strict", action="store_true", help="Require full verification including downloaded weights/SAE params.")
    parser.add_argument("--allow-pending", action="store_true", help="Accept pending model weights/SAE params as partial verification.")
    parser.add_argument("--offline", action="store_true", help="Skip Hugging Face network metadata checks.")
    parser.add_argument("--explain", action="store_true", help="Print hash mismatch details.")
    parser.add_argument("--no-ledger", action="store_true", help="Do not append verification event to evidence ledger.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    certificate_path = root / args.certificate
    if not certificate_path.exists():
        print(f"certificate not found: {certificate_path}", file=sys.stderr)
        return 3

    cert = read_json(certificate_path)
    schema = read_json(root / args.schema) if (root / args.schema).exists() else None
    schema_errors = check_schema(cert, schema)
    if schema_errors:
        print(f"{'[1/8] Validating against schema':<68} FAIL")
        for err in schema_errors:
            print(f"schema error: {err}", file=sys.stderr)
        if not args.no_ledger:
            try:
                append_verification_ledger(root, cert, "fragment_failed_verification", {"reason": "schema", "errors": schema_errors})
            except Exception:
                pass
        return 3
    print(f"{'[1/8] Validating against schema':<68} OK")

    failures: list[str] = []
    partials: list[str] = []
    network_errors: list[str] = []

    verify_controller_spec(root, cert, failures)
    verify_code(root, cert, failures, explain=args.explain)
    verify_schema_self(root, cert, failures)

    expected_fragment_hash = cert["ledger_entry"].get("fragment_sha256")
    actual_fragment_hash = recompute_fragment_hash(cert)
    check(expected_fragment_hash == actual_fragment_hash, "[5/8] Fragment self-hash", failures)

    expected_content_hash = cert["ledger_entry"].get("content_sha256_canonical")
    actual_content_hash = recompute_content_hash(cert)
    check(expected_content_hash == actual_content_hash, "[5/8] Substantive content hash", failures)

    verify_hf(root, cert, failures, network_errors, offline=args.offline)
    verify_weight_status(cert, failures, partials, strict=args.strict)

    if network_errors:
        if not args.no_ledger:
            append_verification_ledger(root, cert, "fragment_failed_verification", {"reason": "network", "errors": network_errors})
        print("Result: NETWORK FAILURE")
        return 4

    if failures:
        if not args.no_ledger:
            append_verification_ledger(root, cert, "fragment_failed_verification", {"reason": "hash_or_state", "failures": failures})
        print("Result: FAILED")
        return 2

    if partials and not args.strict:
        if not args.no_ledger:
            append_verification_ledger(root, cert, "fragment_verified", {"mode": "partial", "partials": partials})
        print("Result: VERIFIED (partial: weights pending)")
        print(f"Fragment ID: {cert['ledger_entry']['fragment_id']}")
        print(f"Fragment SHA-256: {cert['ledger_entry']['fragment_sha256']}")
        print(f"Controller Spec: {cert['ledger_entry']['controller_spec_id']}")
        print(f"Sealed: {cert['ledger_entry']['sealed_at']}")
        return 1

    if not args.no_ledger:
        append_verification_ledger(root, cert, "fragment_verified", {"mode": "full"})
    print("Result: VERIFIED")
    print(f"Fragment ID: {cert['ledger_entry']['fragment_id']}")
    print(f"Fragment SHA-256: {cert['ledger_entry']['fragment_sha256']}")
    print(f"Controller Spec: {cert['ledger_entry']['controller_spec_id']}")
    print(f"Sealed: {cert['ledger_entry']['sealed_at']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
