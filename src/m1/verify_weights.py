#!/usr/bin/env python3
"""Verify downloaded model weights and SAE params for an M1A certificate.

This command is intentionally conservative. It updates nothing in-place yet; it
reports what must be hashed on the runtime where model and SAE artifacts are
actually downloaded. The mutation path will be enabled once the local cache
layout is committed for M1B/M1C.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .certificate_utils import read_json, repo_root

DEFAULT_CERTIFICATE = "outputs/m1/certificates/m1a-source-lock.json"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", default=DEFAULT_CERTIFICATE)
    parser.add_argument("--model-cache-dir", type=Path, default=None)
    parser.add_argument("--sae-params", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    cert_path = root / args.certificate
    if not cert_path.exists():
        print(f"certificate not found: {cert_path}", file=sys.stderr)
        return 3
    cert = read_json(cert_path)
    print("M1A weight verification is reserved for runtime execution.")
    print(f"Certificate: {args.certificate}")
    print(f"Model repo:  {cert['model']['huggingface_repo']}")
    print(f"SAE repo:    {cert['sae']['huggingface_repo']}")
    print(f"SAE path:    {cert['sae']['subpath']}/params.npz")
    print("Required next implementation step: hash downloaded safetensors and params.npz, then seal a superseding certificate fragment.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
