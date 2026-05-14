#!/usr/bin/env python3
"""Supplementary verification for A2 Coxeter-jump scaffold value.

The A2 Coxeter jump coefficient is structurally predicted as -27/4 from
the inverse radius of the p=2 Fuss-Catalan generating function

    f = 1 + z f^3.

This script verifies independently that the p=2 Fuss-Catalan ratios converge
to 27/4. It is not a direct Stokes-side computation.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


def fuss_catalan(n: int, p: int = 2) -> Fraction:
    return Fraction(math.comb((p + 1) * n, n), p * n + 1)


def ratio(n: int, p: int = 2) -> Fraction:
    if n <= 0:
        raise ValueError("ratio index n must be positive")
    return fuss_catalan(n, p) / fuss_catalan(n - 1, p)


def richardson_ratio(n: int, p: int = 2) -> Fraction:
    """Cancel the leading 1/n drift in successive Fuss-Catalan ratios."""
    if n <= 1:
        raise ValueError("Richardson index n must exceed 1")
    return n * ratio(n, p) - (n - 1) * ratio(n - 1, p)


def run_verification(max_n: int = 1000, p: int = 2) -> dict[str, Any]:
    target = Fraction((p + 1) ** (p + 1), p**p)
    checkpoints = [10, 50, 100, 200, 500, max_n]
    rows = []
    for n in checkpoints:
        observed = ratio(n, p)
        rich = richardson_ratio(n, p)
        prediction = float(target) * ((n - 1) / n) ** 1.5
        rows.append(
            {
                "n": n,
                "ratio": float(observed),
                "target": float(target),
                "deviation": float(observed - target),
                "leading_prediction": prediction,
                "richardson_ratio": float(rich),
                "richardson_deviation": float(rich - target),
            }
        )
    final = rows[-1]
    return {
        "schemaVersion": "lawful-learning.fuss-catalan-verification.v0.1",
        "recordType": "FussCatalanVerification",
        "parameterP": p,
        "targetInverseRadius": float(target),
        "targetExact": f"{target.numerator}/{target.denominator}",
        "maxN": max_n,
        "rows": rows,
        "finalRichardsonDeviation": final["richardson_deviation"],
        "passes": abs(final["richardson_deviation"]) < 1e-4,
        "boundary": "Independent inverse-radius evidence only; not a direct Stokes-side computation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify p=2 Fuss-Catalan ratio convergence to 27/4")
    parser.add_argument("--max-n", type=int, default=1000)
    parser.add_argument("--out", default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    report = run_verification(max_n=args.max_n)
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    if args.check and not report["passes"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
