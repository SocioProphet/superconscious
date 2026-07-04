#!/usr/bin/env python3
"""Validate Neural Fabric activation-time targeting artifacts.

Given a suite root (e.g. ``research/activation-time-targeting``) this checks:

* ``families/*.family.json``      against ``model-family.v1.json``
* ``experiments/*.experiment.json`` against ``targeting-experiment.v1.json``
* ``results/**/*.result.json``    against ``targeting-result.v1.json``

plus the cross-cutting doctrine invariants: every experiment and result declares
``weights_updated == false``, and every result's ``experiment_id`` resolves to a
committed experiment. Exits non-zero on the first failure it can report.

    python3 scripts/validate-neural-fabric-results.py research/activation-time-targeting
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

_REPO = pathlib.Path(__file__).resolve().parents[1]
_SCHEMA_DIR = _REPO / "schemas" / "neural-fabric"

_SETS = (
    ("families", "*.family.json", "model-family.v1.json"),
    ("experiments", "*.experiment.json", "targeting-experiment.v1.json"),
    ("results", "*.result.json", "targeting-result.v1.json"),
    ("events", "*.event.json", "intervention-event.v1.json"),
)


def _load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(_load(_SCHEMA_DIR / schema_name))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate neural-fabric suite artifacts")
    p.add_argument("root", type=pathlib.Path, help="suite root, e.g. research/activation-time-targeting")
    args = p.parse_args(argv)
    root: pathlib.Path = args.root

    if not root.is_dir():
        print(f"[FAIL] suite root not found: {root}", file=sys.stderr)
        return 2

    errors: list[str] = []
    experiment_ids: set[str] = set()
    result_experiment_ids: list[tuple[pathlib.Path, str]] = []
    checked = 0

    for subdir, glob, schema_name in _SETS:
        validator = _validator(schema_name)
        for path in sorted((root / subdir).rglob(glob)):
            checked += 1
            doc = _load(path)
            for err in sorted(validator.iter_errors(doc), key=lambda e: e.path):
                loc = "/".join(str(x) for x in err.path) or "<root>"
                errors.append(f"{path}: {loc}: {err.message}")
            # doctrine invariant: activation-time targeting never updates weights
            if subdir in ("experiments", "results", "events") and doc.get("weights_updated") is not False:
                errors.append(f"{path}: weights_updated must be false (activation-time only)")
            if subdir == "experiments":
                experiment_ids.add(doc.get("experiment_id", ""))
            if subdir in ("results", "events"):
                result_experiment_ids.append((path, doc.get("experiment_id", "")))

    for path, exp_id in result_experiment_ids:
        if exp_id and exp_id not in experiment_ids:
            errors.append(f"{path}: references experiment_id '{exp_id}' with no committed experiment")

    if checked == 0:
        print(f"[FAIL] no artifacts found under {root}", file=sys.stderr)
        return 2
    if errors:
        for e in errors:
            print(f"[FAIL] {e}", file=sys.stderr)
        print(f"{len(errors)} neural-fabric artifact validation failure(s).", file=sys.stderr)
        return 1
    print(f"[OK] {checked} neural-fabric artifact(s) valid under {root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
