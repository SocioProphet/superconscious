#!/usr/bin/env python3
"""Validate SourceOS TRUST_SURFACE.yaml files with dependency-free checks.

This validator intentionally avoids third-party dependencies so it can run in fresh
GitHub Actions runners and local developer machines. It performs structural checks
that complement the canonical JSON Schema.
"""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Iterable

REQUIRED_TOP_LEVEL = [
    "schema_version:",
    "component:",
    "repo:",
    "runtime_classes:",
    "authority_summary:",
    "entrypoints:",
    "network:",
    "credentials:",
    "policy:",
    "purge:",
    "prove_clean:",
]

RUNTIME_MARKERS = [
    "LaunchAgent",
    "LaunchDaemon",
    "systemd",
    "Dockerfile",
    "Containerfile",
    "podman",
    "docker",
    "lima",
    "WebSocket",
    "websocket",
    "ws://",
    "wss://",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "listen(",
    "createServer(",
    "exec(",
    "spawn(",
    "oauth",
    "token",
    "keychain",
    "browser",
    "cdp",
    "noVNC",
    "terminal",
    "agent",
]


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def iter_repo_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    ignored_parts = {".git", "node_modules", ".venv", "venv", "dist", "build", ".runs"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        yield path


def has_runtime_markers(root: pathlib.Path) -> bool:
    for path in iter_repo_files(root):
        rel = str(path.relative_to(root))
        if rel == "TRUST_SURFACE.yaml" or rel.startswith("examples/"):
            continue
        if path.name in {"Dockerfile", "Containerfile"}:
            return True
        if path.suffix.lower() not in {".py", ".js", ".ts", ".sh", ".bash", ".zsh", ".go", ".rs", ".yaml", ".yml", ".json", ".md", ".plist", ".service"}:
            continue
        text = read_text(path)
        if any(marker in text for marker in RUNTIME_MARKERS):
            return True
    return False


def validate_trust_surface(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    text = read_text(path)
    if not text.strip():
        return [f"{path}: file is empty"]

    for key in REQUIRED_TOP_LEVEL:
        if not re.search(rf"(?m)^\s*{re.escape(key)}", text):
            errors.append(f"{path}: missing required key {key}")

    if "redaction_required: true" not in text:
        errors.append(f"{path}: credentials.redaction_required must be true")

    if re.search(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", text):
        errors.append(f"{path}: possible literal secret; use a redacted path/ref instead")

    if "plaintext_non_loopback_allowed: true" in text and "break-glass" not in text.lower():
        errors.append(f"{path}: plaintext non-loopback requires break-glass justification")

    return errors


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    trust_surface = root / "TRUST_SURFACE.yaml"
    errors: list[str] = []

    if has_runtime_markers(root) and not trust_surface.exists():
        errors.append("runtime markers found but TRUST_SURFACE.yaml is missing")

    if trust_surface.exists():
        errors.extend(validate_trust_surface(trust_surface))

    for example in sorted((root / "examples").glob("TRUST_SURFACE*.yaml")) if (root / "examples").exists() else []:
        errors.extend(validate_trust_surface(example))

    if errors:
        print("trust surface validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("trust surface validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
