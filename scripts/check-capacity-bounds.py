#!/usr/bin/env python3
"""Check a May-Wigner capacity number against the stability policy.

The control number is ``s * sqrt(m * C)`` (see
``superconscious_core.neural_fabric.may_wigner``). The stability boundary is
1.0; governance should warn well before it. This is a deterministic, CPU-only
gate used by ``neural-fabric-smoke``: it computes the number for the supplied
``--m/--C/--s`` and exits non-zero when the classification is worse than the
allowed ceiling.

    python3 scripts/check-capacity-bounds.py --m 60 --C 0.4 --s 0.1
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "packages" / "superconscious-core"))

from superconscious_core.neural_fabric.may_wigner import (  # noqa: E402
    classify_may_wigner,
    may_wigner_number,
)

# Order of increasing severity; used to compare against --max-class.
_SEVERITY = ["ok", "warn", "error", "stop"]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="May-Wigner capacity gate")
    p.add_argument("--m", type=float, required=True, help="active feature count")
    p.add_argument("--C", type=float, required=True, help="feature co-activation density")
    p.add_argument("--s", type=float, required=True, help="effective interaction scale")
    p.add_argument("--warn", type=float, default=0.70)
    p.add_argument("--error", type=float, default=0.85)
    p.add_argument("--stop", type=float, default=0.95)
    p.add_argument(
        "--max-class",
        choices=_SEVERITY,
        default="warn",
        help="highest classification allowed to pass (default: warn)",
    )
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = p.parse_args(argv)

    value = may_wigner_number(args.m, args.C, args.s)
    cls = classify_may_wigner(value, warn=args.warn, error=args.error, stop=args.stop)
    ok = _SEVERITY.index(cls) <= _SEVERITY.index(args.max_class)

    report = {
        "m": args.m,
        "C": args.C,
        "s": args.s,
        "may_wigner": round(value, 6),
        "boundary": 1.0,
        "classification": cls,
        "max_class": args.max_class,
        "pass": ok,
    }
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(
            f"may_wigner={value:.6f} boundary=1.0 class={cls} "
            f"max_class={args.max_class} -> {'PASS' if ok else 'FAIL'}"
        )
    if not ok:
        print(
            f"[FAIL] capacity classification '{cls}' exceeds allowed '{args.max_class}'",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
