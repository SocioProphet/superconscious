#!/usr/bin/env python3
"""Validate a JSON instance against a JSON Schema.

This is intentionally small and dependency-explicit. CI installs `jsonschema`;
local users can do the same when they want full schema validation. The M1
certificate tooling itself avoids a hard runtime dependency on jsonschema.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path)
    parser.add_argument("instance", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        import jsonschema  # type: ignore
    except Exception as exc:  # noqa: BLE001
        print("jsonschema is required for schema instance validation", file=sys.stderr)
        print(f"import error: {exc}", file=sys.stderr)
        return 4

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    instance = json.loads(args.instance.read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            path = "/".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"{args.instance}: {path}: {error.message}", file=sys.stderr)
        return 1
    print(f"OK {args.instance} against {args.schema}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
