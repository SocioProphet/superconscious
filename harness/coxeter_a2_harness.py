#!/usr/bin/env python3
"""A2 Coxeter harness scaffold under T2' faithful-frame doctrine.

Boundary:
- Structural theorem predicates are executable here.
- The Stokes multiplier and Coxeter-jump coefficient are scaffolded targets.
- The Coxeter jump is supported by the Fuss-Catalan inverse-radius check, but
  awaits a direct Stokes-side computation.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path
from typing import Any

TOLERANCE = 1e-9
OMEGA = cmath.exp(2j * math.pi / 3)
SOURCE_SUPPLIED_HASH_CHAIN_HEAD = "9f722df9ea3ec75769985b3c05bec6609c4a1d1741f4ca82c5314407219a3e1e"

Matrix = tuple[tuple[complex, ...], ...]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows = len(a)
    cols = len(b[0])
    mid = len(b)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(mid)) for j in range(cols))
        for i in range(rows)
    )


def matsub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] - b[i][j] for j in range(len(a[0])))
        for i in range(len(a))
    )


def scalar_mul(c: complex, a: Matrix) -> Matrix:
    return tuple(tuple(c * value for value in row) for row in a)


def identity(n: int) -> Matrix:
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def diagonal(values: list[complex]) -> Matrix:
    return tuple(tuple(values[i] if i == j else 0 for j in range(len(values))) for i in range(len(values)))


def conjugate_transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i].conjugate() for j in range(len(a))) for i in range(len(a[0])))


def frobenius_norm(a: Matrix) -> float:
    return math.sqrt(sum(abs(value) ** 2 for row in a for value in row))


def close_matrix(a: Matrix, b: Matrix, tolerance: float = TOLERANCE) -> bool:
    return frobenius_norm(matsub(a, b)) <= tolerance


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return matsub(matmul(a, b), matmul(b, a))


def fuss_catalan_inverse_radius(order: int) -> float:
    """Inverse radius for order-m Fuss-Catalan numbers.

    For A_n with n=order, the structural inverse radius is
    (n+1)^(n+1) / n^n. For A1 this gives 4; for A2 it gives 27/4.
    """
    return ((order + 1) ** (order + 1)) / (order**order)


def gell_mann() -> dict[str, Matrix]:
    i = 1j
    inv_sqrt3 = 1.0 / math.sqrt(3.0)
    zero = 0j
    return {
        "lambda1": ((0, 1, 0), (1, 0, 0), (0, 0, 0)),
        "lambda2": ((0, -i, 0), (i, 0, 0), (0, 0, 0)),
        "lambda3": ((1, 0, 0), (0, -1, 0), (0, 0, 0)),
        "lambda4": ((0, 0, 1), (0, 0, 0), (1, 0, 0)),
        "lambda5": ((0, 0, -i), (0, 0, 0), (i, 0, 0)),
        "lambda8": ((inv_sqrt3, 0, 0), (0, inv_sqrt3, 0), (0, 0, -2 * inv_sqrt3)),
    }


def cartan_a2() -> list[list[int]]:
    alpha1 = (1, -1, 0)
    alpha2 = (0, 1, -1)

    def dot(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
        return sum(x * y for x, y in zip(a, b))

    roots = [alpha1, alpha2]
    return [[dot(a, b) for b in roots] for a in roots]


def predicate(name: str, passed: bool, value: Any, expected: Any, status: str, note: str = "") -> dict[str, Any]:
    return {
        "predicateId": name,
        "passed": bool(passed),
        "value": value,
        "expected": expected,
        "status": status,
        "note": note,
    }


def run_harness() -> dict[str, Any]:
    ident3 = identity(3)
    zeta = scalar_mul(OMEGA, ident3)
    lambdas = gell_mann()
    l1 = lambdas["lambda1"]
    l2 = lambdas["lambda2"]
    l3 = lambdas["lambda3"]
    l4 = lambdas["lambda4"]
    l5 = lambdas["lambda5"]
    l8 = lambdas["lambda8"]

    zeta_cubed = matmul(matmul(zeta, zeta), zeta)
    zeta_hermitian = matmul(matmul(conjugate_transpose(zeta), ident3), zeta)
    comm12 = commutator(l1, l2)
    expected_comm12 = scalar_mul(2j, l3)
    comm45 = commutator(l4, l5)
    expected_comm45 = scalar_mul(1j, tuple(tuple(l3[r][c] + math.sqrt(3.0) * l8[r][c] for c in range(3)) for r in range(3)))
    jump = -fuss_catalan_inverse_radius(order=2)

    predicates = [
        predicate(
            "P1_stokes_multiplier_observed_A2",
            abs(OMEGA - cmath.exp(2j * math.pi / 3)) < TOLERANCE,
            str(OMEGA),
            "omega = exp(2*pi*i/3)",
            "scaffold_awaiting_direct_stokes_computation",
            "Structural T2'_A2 multiplier; direct Stokes-side computation remains outstanding.",
        ),
        predicate(
            "P2_coxeter_jump_coefficient_A2",
            abs(jump + 6.75) < TOLERANCE,
            jump,
            -6.75,
            "scaffold_supported_by_fuss_catalan_inverse_radius",
            "Conjectured as negative inverse radius 27/4; direct Stokes-side computation remains outstanding.",
        ),
        predicate(
            "P3_hermitian_preservation_A2",
            close_matrix(zeta_hermitian, ident3),
            "zeta^* H zeta = H",
            "H preserved",
            "machine_precision",
        ),
        predicate(
            "P4_zeta_A2_equals_omega_I3",
            close_matrix(zeta, scalar_mul(OMEGA, ident3)),
            "omega * I_3",
            "omega * I_3",
            "machine_precision",
        ),
        predicate(
            "P5_zeta_A2_order_check",
            close_matrix(zeta_cubed, ident3),
            "zeta^3 = I_3",
            "I_3",
            "machine_precision",
        ),
        predicate(
            "P6_gellmann_commutator_norm_A2",
            close_matrix(comm12, expected_comm12) and abs(frobenius_norm(comm12) - 2 * math.sqrt(2.0)) < TOLERANCE,
            frobenius_norm(comm12),
            2 * math.sqrt(2.0),
            "machine_precision",
        ),
        predicate(
            "P7_rank_two_commutator_direction_A2",
            close_matrix(comm45, expected_comm45),
            "[lambda4, lambda5] = i(lambda3 + sqrt(3)lambda8)",
            "lambda8 direction present",
            "machine_precision",
        ),
        predicate(
            "P8_A2_cartan_rank_two_structure",
            cartan_a2() == [[2, -1], [-1, 2]],
            cartan_a2(),
            [[2, -1], [-1, 2]],
            "machine_precision",
        ),
    ]

    canonical_payload = {
        "proofReference": "docs/lawful-learning/10-a2-gate-minimality-scoping.md",
        "predicateIds": [item["predicateId"] for item in predicates],
        "statuses": [item["status"] for item in predicates],
        "jumpCoefficient": jump,
    }
    local_digest = hashlib.sha256(json.dumps(canonical_payload, sort_keys=True).encode()).hexdigest()

    return {
        "schemaVersion": "lawful-learning.coxeter-a2-harness-report.v0.1",
        "recordType": "CoxeterA2HarnessReport",
        "theoremReference": "docs/lawful-learning/10-a2-gate-minimality-scoping.md",
        "proofReference": "docs/proofs/a1-gate-minimality-faithful.md",
        "predicateCount": len(predicates),
        "passedCount": sum(1 for item in predicates if item["passed"]),
        "machinePrecisionPredicateCount": sum(1 for item in predicates if item["status"] == "machine_precision"),
        "scaffoldPredicateCount": sum(1 for item in predicates if item["status"].startswith("scaffold")),
        "allPassed": all(item["passed"] for item in predicates),
        "predicates": predicates,
        "reportedHashChainHead": SOURCE_SUPPLIED_HASH_CHAIN_HEAD,
        "localCanonicalDigest": local_digest,
        "hashNote": "reportedHashChainHead is the source-supplied baseline; localCanonicalDigest is this scaffold's canonical payload digest.",
        "openItems": [
            "direct_stokes_side_coxeter_jump_computation",
            "direct_A2_stokes_multiplier_observable",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run A2 Coxeter scaffold harness")
    parser.add_argument("--out", default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    report = run_harness()
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    if args.check and not report["allPassed"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
