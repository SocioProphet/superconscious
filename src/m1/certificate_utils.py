#!/usr/bin/env python3
"""Shared helpers for M1 certificate generation and verification."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

HF_API_ROOT = "https://huggingface.co/api/models"
VOLATILE_CERT_FIELDS = {"generated_at"}
VOLATILE_LEDGER_FIELDS = {"timestamp"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_pretty(value) + "\n", encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_json_pretty(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def strip_keys(value: Any, keys_to_strip: set[str]) -> Any:
    if isinstance(value, dict):
        return {k: strip_keys(v, keys_to_strip) for k, v in value.items() if k not in keys_to_strip}
    if isinstance(value, list):
        return [strip_keys(item, keys_to_strip) for item in value]
    return value


def repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    result = run_git(["rev-parse", "--show-toplevel"], cwd=start, check=True)
    return Path(result.stdout.strip())


def run_git(args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git_commit_sha(root: Path) -> str:
    return run_git(["rev-parse", "HEAD"], cwd=root, check=True).stdout.strip()


def git_status_porcelain(root: Path) -> list[str]:
    output = run_git(["status", "--porcelain"], cwd=root, check=True).stdout
    return [line for line in output.splitlines() if line.strip()]


def git_blob_sha(root: Path, path: Path) -> str | None:
    rel = str(path.relative_to(root))
    result = run_git(["ls-files", "-s", "--", rel], cwd=root, check=False)
    if result.returncode != 0 or not result.stdout.strip():
        return None
    # Format: mode SHA stage\tpath
    return result.stdout.split()[1]


def file_record(root: Path, path_str: str) -> dict[str, Any]:
    path = root / path_str
    record: dict[str, Any] = {
        "path": path_str,
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
        "content_sha256": sha256_file(path) if path.exists() else None,
        "git_blob_sha": git_blob_sha(root, path) if path.exists() else None,
    }
    return record


def fetch_hf_model_metadata(repo_id: str, revision: str = "main", *, timeout: int = 30) -> dict[str, Any]:
    encoded_repo = urllib.parse.quote(repo_id, safe="")
    encoded_revision = urllib.parse.quote(revision, safe="")
    url = f"{HF_API_ROOT}/{encoded_repo}/revision/{encoded_revision}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "superconscious-m1-certificate/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Hugging Face API error for {repo_id}@{revision}: {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to reach Hugging Face API for {repo_id}@{revision}: {exc}") from exc


def hf_sibling_paths(metadata: dict[str, Any]) -> set[str]:
    return {
        item["rfilename"]
        for item in metadata.get("siblings", [])
        if isinstance(item, dict) and isinstance(item.get("rfilename"), str)
    }


def hf_sibling_record(metadata: dict[str, Any], filename: str) -> dict[str, Any] | None:
    for item in metadata.get("siblings", []):
        if isinstance(item, dict) and item.get("rfilename") == filename:
            return dict(item)
    return None


def append_ledger(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(entry) + "\n")


def ledger_event(
    *,
    event: str,
    fragment_id: str,
    fragment_sha256: str | None,
    tool: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "event": event,
        "fragment_id": fragment_id,
        "fragment_sha256": fragment_sha256,
        "timestamp": utc_now(),
        "tool": tool,
        "details": details or {},
    }


def make_fragment_id(prefix: str, content_sha256: str) -> str:
    return f"{prefix}-{content_sha256[:12]}"


def local_runtime_stub() -> dict[str, Any]:
    return {
        "execution_target": "local",
        "hardware": {
            "gpu_model": None,
            "gpu_count": None,
            "gpu_driver_version": None,
            "cuda_version": None,
            "cpu_model": platform.processor() or None,
            "total_memory_gb": None,
        },
        "software": {
            "python_version": platform.python_version(),
            "torch_version": None,
            "transformers_version": None,
            "sae_lens_version": None,
            "platform": platform.platform(),
        },
        "precision": {
            "model_dtype": None,
            "sae_dtype": None,
            "intervention_dtype": None,
        },
        "random_seeds": {
            "torch": None,
            "numpy": None,
            "python": None,
            "tokenizer_sample": None,
        },
        "execution_status": "not_executed",
    }


def collect_artifact_records(root: Path, paths: Iterable[str], generated_by: str) -> list[dict[str, Any]]:
    generated_at = utc_now()
    records: list[dict[str, Any]] = []
    for path_str in paths:
        path = root / path_str
        if not path.exists():
            continue
        records.append(
            {
                "path": path_str,
                "content_sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "generated_by_script": generated_by,
                "generated_at": generated_at,
            }
        )
    return records


def schema_validate_basic(cert: dict[str, Any]) -> list[str]:
    """Small built-in schema sanity check.

    We avoid a hard dependency on jsonschema. If jsonschema is installed, callers
    may use it separately; this check ensures the verifier can still run in a
    minimal Python environment.
    """

    errors: list[str] = []
    required = [
        "schema_version",
        "certificate_kind",
        "generated_at",
        "generated_by",
        "controller_spec_ref",
        "model",
        "sae",
        "datasets",
        "code",
        "runtime",
        "generated_artifacts",
        "ledger_entry",
    ]
    for key in required:
        if key not in cert:
            errors.append(f"missing top-level key: {key}")
    if cert.get("certificate_kind") != "m1a-source-lock":
        errors.append("certificate_kind must be m1a-source-lock")
    if cert.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    return errors


def try_jsonschema_validate(instance: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except Exception:
        return []
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except Exception as exc:
        return [str(exc)]
    return []


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def list_script_records(root: Path, paths: list[str]) -> list[dict[str, Any]]:
    return [file_record(root, path) for path in paths]


def list_untracked_files_from_status(status_lines: list[str]) -> list[str]:
    files: list[str] = []
    for line in status_lines:
        if line.startswith("?? "):
            files.append(line[3:])
    return files


def has_uncommitted_changes(status_lines: list[str]) -> bool:
    return any(not line.startswith("?? ") for line in status_lines)
