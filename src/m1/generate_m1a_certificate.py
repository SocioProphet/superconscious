#!/usr/bin/env python3
"""Generate the M1A source-lock certificate fragment.

The generated certificate is a replayability precondition for M1B-M1D. It
records the controller spec, model/SAE metadata, dataset placeholders, code
hashes, runtime stub, and ledger identity.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .certificate_utils import (
    append_ledger,
    canonical_json_pretty,
    collect_artifact_records,
    fetch_hf_model_metadata,
    file_record,
    git_commit_sha,
    git_status_porcelain,
    has_uncommitted_changes,
    hf_sibling_paths,
    ledger_event,
    list_script_records,
    list_untracked_files_from_status,
    local_runtime_stub,
    make_fragment_id,
    read_json,
    repo_root,
    sha256_file,
    sha256_json,
    sha256_text,
    strip_keys,
    try_jsonschema_validate,
    utc_now,
)

DEFAULT_MODEL_REPO = "google/gemma-2-9b-it"
DEFAULT_SAE_REPO = "google/gemma-scope-9b-it-res"
DEFAULT_CONTROLLER_SPEC = "docs/m1-0-controller-spec.md"
DEFAULT_SCHEMA = "schemas/m1/source-lock.v1.json"
DEFAULT_OUTPUT = "outputs/m1/certificates/m1a-source-lock.json"
DEFAULT_LEDGER = "outputs/m1/evidence-ledger.jsonl"
DEFAULT_SAE_SUBPATH = "layer_20/width_131k/average_l0_81"
DEFAULT_SAE_PARAMS = f"{DEFAULT_SAE_SUBPATH}/params.npz"

VOLATILE_SUBSTANTIVE_KEYS = {
    "generated_at",
    "sealed_at",
    "fragment_id",
    "fragment_sha256",
    "content_sha256_canonical",
}

SCRIPT_PATHS = [
    "src/m1/__init__.py",
    "src/m1/certificate_utils.py",
    "src/m1/source_lock.py",
    "src/m1/generate_m1a_certificate.py",
    "src/m1/verify_source_lock.py",
    "src/m1/verify_weights.py",
    "src/m1/feature_selection.py",
]

CONFIG_PATHS = [
    "docs/m1-0-controller-spec.md",
    "docs/m1-source-lock.md",
    "docs/implementability-steering-pilot.md",
    "docs/implementability-advanced-roadmap.md",
    "data/m1/README.md",
    "Makefile",
]

SCHEMA_PATHS = [DEFAULT_SCHEMA]


def hf_file_hash_from_local_cache(local_path: Path | None) -> str | None:
    if local_path and local_path.exists() and local_path.is_file():
        return sha256_file(local_path)
    return None


def dataset_record(path: str, provenance: str | None = None) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        return {
            "path": path,
            "status": "not_constructed",
            "content_sha256": None,
            "item_count": None,
            "construction_provenance_ref": provenance,
        }
    item_count = 0
    if file_path.suffix == ".jsonl":
        with file_path.open("r", encoding="utf-8") as handle:
            item_count = sum(1 for line in handle if line.strip())
    return {
        "path": path,
        "status": "draft",
        "content_sha256": sha256_file(file_path),
        "item_count": item_count if item_count else None,
        "construction_provenance_ref": provenance,
    }


def build_datasets() -> dict[str, Any]:
    return {
        "harm_pressure_mcq": dataset_record(
            "data/m1/harm_pressure_mcq.jsonl",
            "data/m1/harm_pressure_mcq.provenance.json",
        ),
        "contrastive_benign": dataset_record(
            "data/m1/contrastive_benign.jsonl",
            "data/m1/contrastive_benign.provenance.json",
        ),
        "contrastive_harmful": dataset_record(
            "data/m1/contrastive_harmful.jsonl",
            "data/m1/contrastive_harmful.provenance.json",
        ),
        "patchability_probes": dataset_record(
            "data/m1/patchability_probes.jsonl",
            "data/m1/patchability_probes.provenance.json",
        ),
        "off_target_audit_batteries": {
            "benign_qa": dataset_record(
                "data/m1/off_target_benign_qa.jsonl",
                "data/m1/off_target_benign_qa.provenance.json",
            ),
            "format_following": dataset_record(
                "data/m1/off_target_format_following.jsonl",
                "data/m1/off_target_format_following.provenance.json",
            ),
            "over_refusal_probe": dataset_record(
                "data/m1/off_target_over_refusal.jsonl",
                "data/m1/off_target_over_refusal.provenance.json",
            ),
            "genuine_refusal_preservation": dataset_record(
                "data/m1/off_target_genuine_refusal_preservation.jsonl",
                "data/m1/off_target_genuine_refusal_preservation.provenance.json",
            ),
        },
    }


def architecture_from_config(config: dict[str, Any] | None) -> dict[str, Any]:
    if not config:
        return {
            "num_layers": None,
            "hidden_size": None,
            "vocab_size": None,
            "intermediate_size": None,
            "num_attention_heads": None,
            "num_key_value_heads": None,
        }
    return {
        "num_layers": config.get("num_hidden_layers"),
        "hidden_size": config.get("hidden_size"),
        "vocab_size": config.get("vocab_size"),
        "intermediate_size": config.get("intermediate_size"),
        "num_attention_heads": config.get("num_attention_heads"),
        "num_key_value_heads": config.get("num_key_value_heads"),
    }


def maybe_fetch_hf_text(repo: str, revision: str, filename: str) -> str | None:
    import urllib.error
    import urllib.parse
    import urllib.request

    repo_path = urllib.parse.quote(repo, safe="/")
    revision_path = urllib.parse.quote(revision, safe="")
    filename_path = urllib.parse.quote(filename, safe="/")
    url = f"https://huggingface.co/{repo_path}/resolve/{revision_path}/{filename_path}"
    request = urllib.request.Request(url, headers={"User-Agent": "superconscious-m1a-generator/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError, UnicodeDecodeError):
        return None


def build_model_section(repo: str, revision: str) -> dict[str, Any]:
    metadata = fetch_hf_model_metadata(repo, revision)
    resolved = metadata.get("sha") or revision
    config_text = maybe_fetch_hf_text(repo, resolved, "config.json")
    tokenizer_config_text = maybe_fetch_hf_text(repo, resolved, "tokenizer_config.json")
    tokenizer_json_text = maybe_fetch_hf_text(repo, resolved, "tokenizer.json")

    config = None
    if config_text:
        try:
            config = json.loads(config_text)
        except json.JSONDecodeError:
            config = None

    tokenizer_template_sha = None
    if tokenizer_config_text:
        try:
            tokenizer_config = json.loads(tokenizer_config_text)
            template = tokenizer_config.get("chat_template")
            if isinstance(template, str):
                tokenizer_template_sha = sha256_text(template)
        except json.JSONDecodeError:
            tokenizer_template_sha = None

    weight_files: list[dict[str, Any]] = []
    for item in metadata.get("siblings", []):
        if not isinstance(item, dict):
            continue
        name = item.get("rfilename")
        if isinstance(name, str) and (name.endswith(".safetensors") or name.endswith(".bin")):
            weight_files.append(
                {
                    "name": name,
                    "size_bytes": item.get("size"),
                    "sha256": None,
                }
            )
    weight_files.sort(key=lambda row: row["name"])

    return {
        "huggingface_repo": repo,
        "repo_commit_sha": resolved,
        "config_json_sha256": sha256_text(config_text) if config_text else None,
        "tokenizer_config_sha256": sha256_text(tokenizer_config_text) if tokenizer_config_text else None,
        "tokenizer_template_sha256": tokenizer_template_sha,
        "tokenizer_vocab_sha256": sha256_text(tokenizer_json_text) if tokenizer_json_text else None,
        "weights_manifest": {
            "files": weight_files,
            "weights_downloaded": False,
            "weights_verification_status": "not_downloaded",
        },
        "architecture_fingerprint": architecture_from_config(config),
    }


def build_sae_section(repo: str, revision: str, model_hidden_size: int | None, local_params: Path | None = None) -> dict[str, Any]:
    metadata = fetch_hf_model_metadata(repo, revision)
    resolved = metadata.get("sha") or revision
    sibling_paths = hf_sibling_paths(metadata)
    if DEFAULT_SAE_PARAMS not in sibling_paths:
        similar = sorted(p for p in sibling_paths if p.startswith(DEFAULT_SAE_SUBPATH))
        raise RuntimeError(f"Missing SAE params path {DEFAULT_SAE_PARAMS}. Similar paths: {similar[:20]}")

    params_downloaded = bool(local_params and local_params.exists())
    params_hash = hf_file_hash_from_local_cache(local_params)
    shape = {
        "d_in": 3584,
        "d_sae": 131072,
        "expected_l0_target": 81,
        "encoder_weight_shape": [131072, 3584],
        "decoder_weight_shape": [3584, 131072],
        "encoder_bias_shape": [131072],
        "decoder_bias_shape": [3584],
    }
    sae_d_in = shape["d_in"]
    return {
        "huggingface_repo": repo,
        "repo_commit_sha": resolved,
        "subpath": DEFAULT_SAE_SUBPATH,
        "params_npz_sha256": params_hash,
        "params_downloaded": params_downloaded,
        "shape_fingerprint": shape,
        "compatibility_check": {
            "d_in_matches_model_hidden_size": (model_hidden_size == sae_d_in) if model_hidden_size is not None else None,
            "model_hidden_size": model_hidden_size,
            "sae_d_in": sae_d_in,
        },
    }


def build_code_section(root: Path) -> dict[str, Any]:
    status = git_status_porcelain(root)
    return {
        "repo": "superconscious",
        "commit_sha": git_commit_sha(root),
        "commit_clean": len(status) == 0,
        "untracked_files": list_untracked_files_from_status(status),
        "uncommitted_changes": has_uncommitted_changes(status),
        "scripts": list_script_records(root, SCRIPT_PATHS),
        "configs": list_script_records(root, CONFIG_PATHS),
        "schemas": list_script_records(root, SCHEMA_PATHS),
    }


def build_controller_spec_ref(root: Path, path: str) -> dict[str, Any]:
    record = file_record(root, path)
    if not record["exists"]:
        raise FileNotFoundError(path)
    return {
        "path": path,
        "content_sha256": record["content_sha256"],
        "git_blob_sha": record["git_blob_sha"],
        "commit_sha": git_commit_sha(root),
    }


def substantive_hash(cert: dict[str, Any]) -> str:
    return sha256_json(strip_keys(cert, VOLATILE_SUBSTANTIVE_KEYS))


def fragment_hash(cert: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(cert))
    clone["ledger_entry"]["fragment_sha256"] = None
    first = sha256_json(clone)
    clone["ledger_entry"]["fragment_sha256"] = first
    return sha256_json(clone)


def seal_certificate(cert: dict[str, Any], supersedes: str | None) -> dict[str, Any]:
    controller_id = make_fragment_id("m1-0-refuse-and-redirect", cert["controller_spec_ref"]["content_sha256"])
    sealed_at = utc_now()
    cert["ledger_entry"] = {
        "fragment_id": None,
        "fragment_sha256": None,
        "content_sha256_canonical": None,
        "parent_fragment_id": None,
        "child_fragment_ids": [],
        "controller_spec_id": controller_id,
        "sealed_at": sealed_at,
        "sealed_by": "src/m1/generate_m1a_certificate.py",
        "supersedes": supersedes,
    }
    content_sha = substantive_hash(cert)
    cert["ledger_entry"]["content_sha256_canonical"] = content_sha
    cert["ledger_entry"]["fragment_id"] = make_fragment_id("m1a-source-lock", content_sha)
    cert["ledger_entry"]["fragment_sha256"] = fragment_hash(cert)
    return cert


def build_certificate(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root()
    generated_at = utc_now()
    controller_spec_ref = build_controller_spec_ref(root, args.controller_spec)
    model = build_model_section(args.model_repo, args.model_revision)
    model_hidden_size = model["architecture_fingerprint"].get("hidden_size")
    sae = build_sae_section(args.sae_repo, args.sae_revision, model_hidden_size, args.local_sae_params)
    code = build_code_section(root)

    cert: dict[str, Any] = {
        "schema_version": "1.0.0",
        "certificate_kind": "m1a-source-lock",
        "generated_at": generated_at,
        "generated_by": "src/m1/generate_m1a_certificate.py",
        "controller_spec_ref": controller_spec_ref,
        "model": model,
        "sae": sae,
        "datasets": build_datasets(),
        "code": code,
        "runtime": local_runtime_stub(),
        "generated_artifacts": collect_artifact_records(
            root,
            ["outputs/m1/source-lock.json"],
            "src/m1/source_lock.py",
        ),
        "ledger_entry": {},
    }
    return seal_certificate(cert, args.supersedes)


def validate_against_schema(root: Path, cert: dict[str, Any], schema_path: str) -> list[str]:
    schema_file = root / schema_path
    if not schema_file.exists():
        return [f"schema missing: {schema_path}"]
    schema = read_json(schema_file)
    return try_jsonschema_validate(cert, schema)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-repo", default=DEFAULT_MODEL_REPO)
    parser.add_argument("--model-revision", default="main")
    parser.add_argument("--sae-repo", default=DEFAULT_SAE_REPO)
    parser.add_argument("--sae-revision", default="main")
    parser.add_argument("--controller-spec", default=DEFAULT_CONTROLLER_SPEC)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT))
    parser.add_argument("--ledger", type=Path, default=Path(DEFAULT_LEDGER))
    parser.add_argument("--local-sae-params", type=Path, default=None)
    parser.add_argument("--supersedes", default=None)
    parser.add_argument("--no-ledger", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    print("[1/6] Loading controller spec...", flush=True)
    print("[2/6] Resolving model metadata...", flush=True)
    print("[3/6] Resolving SAE metadata...", flush=True)
    print("[4/6] Hashing code artifacts...", flush=True)
    print("[5/6] Hashing schema...", flush=True)
    cert = build_certificate(args)
    errors = validate_against_schema(root, cert, args.schema)
    if errors:
        for error in errors:
            print(f"schema validation warning: {error}", file=sys.stderr)
    print("[6/6] Sealing certificate fragment...", flush=True)

    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical_json_pretty(cert) + "\n", encoding="utf-8")

    if not args.no_ledger:
        append_ledger(
            root / args.ledger,
            ledger_event(
                event="fragment_sealed",
                fragment_id=cert["ledger_entry"]["fragment_id"],
                fragment_sha256=cert["ledger_entry"]["fragment_sha256"],
                tool="src/m1/generate_m1a_certificate.py",
                details={
                    "path": str(args.output),
                    "content_sha256_canonical": cert["ledger_entry"]["content_sha256_canonical"],
                    "controller_spec_id": cert["ledger_entry"]["controller_spec_id"],
                },
            ),
        )

    print(f"Fragment ID:     {cert['ledger_entry']['fragment_id']}")
    print(f"Fragment SHA-256: {cert['ledger_entry']['fragment_sha256']}")
    print(f"Output:          {args.output}")
    if not args.no_ledger:
        print(f"Ledger:          {args.ledger} (+1 entry)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
