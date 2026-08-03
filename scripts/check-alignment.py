#!/usr/bin/env python3
"""Procrustes feature-alignment / drift checker.

Substrates, Structures, and Circuits framework, sections 11 and 13.3. The
cognition-decision-trace schema (PR #82) declares the ``alignment_drift_exceeded``
approval trigger; this is the checker that computes the quantity behind it and
emits a ``feature-alignment-drift.v1`` record.

Given two feature spaces over a shared trunk output basis -- e.g. a new model's
SAE dictionary ``F_A`` and the previous model's ``F_B``, both ``(n_features x
n_dims)`` -- we solve the orthogonal Procrustes problem

    Q* = argmin_Q ||F_A - F_B Q||_F   subject to  Q^T Q = I

whose solution is the orthogonal polar factor of ``M = F_B^T F_A`` (equivalently
``U V^T`` from ``M = U S V^T``). Because drift is judged AFTER alignment, a space
that is merely rotated relative to the reference registers as *aligned*: the
residual measures geometry change, not basis choice.

Both matrices are normalized to unit Frobenius norm first, so the residual is
scale-free and directly comparable to the framework thresholds. The linear
algebra is pure stdlib (Jacobi eigendecomposition of the small symmetric Gram
matrix), so the checker adds no third-party dependency.

Drift classification (framework 13.3), with the reference thresholds
``stable_max = 0.05`` and ``drift_max = 0.20``:

    stable   if residual < stable_max AND no critical feature drifted
    drifted  if residual < drift_max  OR  <= 1 critical feature drifted
    broken   otherwise

The emitted ``decision`` is ``aligned`` iff the classification is ``stable``,
otherwise ``drift``. The record carries a SHA-256 (FIPS 180-4) replay seal over
the canonical inputs and verdict.

Exit codes:
    0  classification within the allowed ceiling (--max-class, default drifted)
    1  classification exceeds the ceiling (drift gate fails / promotion blocked)
    2  malformed input REJECTED (shape mismatch, ragged rows, non-finite values)

Usage:
    python3 scripts/check-alignment.py CHECK_INPUT.json
    python3 scripts/check-alignment.py CHECK_INPUT.json --max-class stable
    python3 scripts/check-alignment.py CHECK_INPUT.json --emit-record OUT.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

# Order of increasing severity; --max-class picks the highest that still passes.
_SEVERITY = ["stable", "drifted", "broken"]

_ORTHO_TOL = 1e-6
_EIG_EPS = 1e-12


class MalformedInput(Exception):
    """Raised when the input cannot be interpreted as two conformable, finite matrices."""


# --------------------------------------------------------------------------- #
# Small dense linear algebra (pure stdlib; intended for small trunk bases).
# --------------------------------------------------------------------------- #
def _validate_matrix(name: str, m: object) -> list[list[float]]:
    if not isinstance(m, list) or not m:
        raise MalformedInput(f"{name}: must be a non-empty list of rows")
    width = None
    out: list[list[float]] = []
    for r, row in enumerate(m):
        if not isinstance(row, list) or not row:
            raise MalformedInput(f"{name}: row {r} must be a non-empty list")
        if width is None:
            width = len(row)
        elif len(row) != width:
            raise MalformedInput(
                f"{name}: ragged rows (row {r} has {len(row)}, expected {width})"
            )
        conv: list[float] = []
        for c, v in enumerate(row):
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise MalformedInput(f"{name}: entry [{r}][{c}] is not a number")
            fv = float(v)
            if not math.isfinite(fv):
                raise MalformedInput(f"{name}: entry [{r}][{c}] is non-finite")
            conv.append(fv)
        out.append(conv)
    return out


def _transpose(m: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*m)]


def _matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    bt = _transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def _frob(m: list[list[float]]) -> float:
    return math.sqrt(sum(x * x for row in m for x in row))


def _scale(m: list[list[float]], s: float) -> list[list[float]]:
    return [[x * s for x in row] for row in m]


def _sub(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def _identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _jacobi_eigh(a: list[list[float]], max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Symmetric eigendecomposition via the cyclic Jacobi method.

    Returns (eigenvalues, eigenvectors) where eigenvectors are columns of the
    returned matrix. ``a`` is assumed symmetric.
    """
    n = len(a)
    s = [row[:] for row in a]
    v = _identity(n)
    for _ in range(max_sweeps):
        off = math.sqrt(sum(s[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < 1e-15:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(s[p][q]) < 1e-300:
                    continue
                theta = (s[q][q] - s[p][p]) / (2.0 * s[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                if theta == 0.0:
                    t = 1.0
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(n):
                    skp, skq = s[k][p], s[k][q]
                    s[k][p] = c * skp - sn * skq
                    s[k][q] = sn * skp + c * skq
                for k in range(n):
                    spk, sqk = s[p][k], s[q][k]
                    s[p][k] = c * spk - sn * sqk
                    s[q][k] = sn * spk + c * sqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - sn * vkq
                    v[k][q] = sn * vkp + c * vkq
    eigenvalues = [s[i][i] for i in range(n)]
    return eigenvalues, v


def orthogonal_procrustes(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Return Q minimizing ||A - B Q||_F over orthogonal Q.

    Q is the orthogonal polar factor of M = B^T A, computed as
    M (M^T M)^{-1/2} via the symmetric eigendecomposition of M^T M. Equivalent
    to U V^T from the SVD M = U S V^T, without forming the SVD explicitly.
    """
    m = _matmul(_transpose(b), a)  # (d x d)
    g = _matmul(_transpose(m), m)  # M^T M, symmetric (d x d)
    eigvals, eigvecs = _jacobi_eigh(g)
    d = len(g)
    inv_sqrt = [[0.0] * d for _ in range(d)]
    for k in range(d):
        lam = eigvals[k]
        scale = 1.0 / math.sqrt(lam) if lam > _EIG_EPS else 0.0
        for i in range(d):
            for j in range(d):
                inv_sqrt[i][j] += eigvecs[i][k] * scale * eigvecs[j][k]
    return _matmul(m, inv_sqrt)


def orthogonality_error(q: list[list[float]]) -> float:
    d = len(q)
    return _frob(_sub(_matmul(_transpose(q), q), _identity(d)))


# --------------------------------------------------------------------------- #
# Drift computation and classification.
# --------------------------------------------------------------------------- #
def compute_drift(spec: dict) -> dict:
    a = _validate_matrix("feature_space_a", spec.get("feature_space_a"))
    b = _validate_matrix("feature_space_b", spec.get("feature_space_b"))
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise MalformedInput(
            f"shape mismatch: A is {len(a)}x{len(a[0])}, B is {len(b)}x{len(b[0])}"
        )

    n_features, n_dims = len(a), len(a[0])
    na, nb = _frob(a), _frob(b)
    if na <= _EIG_EPS or nb <= _EIG_EPS:
        raise MalformedInput("a feature space has zero Frobenius norm")
    an = _scale(a, 1.0 / na)
    bn = _scale(b, 1.0 / nb)

    q = orthogonal_procrustes(an, bn)
    ortho_err = orthogonality_error(q)
    aligned = _matmul(bn, q)  # B_n Q
    diff = _sub(an, aligned)
    residual = _frob(diff)

    thresholds = spec.get("thresholds") or {}
    stable_max = float(thresholds.get("stable_max", 0.05))
    drift_max = float(thresholds.get("drift_max", 0.20))
    if not (math.isfinite(stable_max) and math.isfinite(drift_max)) or stable_max > drift_max:
        raise MalformedInput("thresholds must satisfy 0 <= stable_max <= drift_max")

    crit = spec.get("critical_features") or {}
    crit_indices = crit.get("indices", [])
    per_feature_max = float(crit.get("per_feature_max", stable_max))
    drifted_indices: list[int] = []
    for idx in crit_indices:
        if not isinstance(idx, int) or idx < 0 or idx >= n_features:
            raise MalformedInput(f"critical feature index {idx!r} out of range [0,{n_features})")
        row_res = math.sqrt(sum(x * x for x in diff[idx]))
        if row_res > per_feature_max:
            drifted_indices.append(idx)
    drifted_count = len(drifted_indices)

    # Framework 13.3 classification.
    if residual < stable_max and drifted_count == 0:
        classification = "stable"
    elif residual < drift_max or drifted_count <= 1:
        classification = "drifted"
    else:
        classification = "broken"
    decision = "aligned" if classification == "stable" else "drift"

    record = {
        "check_id": spec.get("check_id", "feature-alignment-drift"),
        "feature_space_a_ref": spec["feature_space_a_ref"],
        "feature_space_b_ref": spec["feature_space_b_ref"],
        "procrustes": {
            "residual": round(residual, 9),
            "disparity": round(residual * residual, 9),
            "rotation_orthogonal": ortho_err < _ORTHO_TOL,
            "orthogonality_error": round(ortho_err, 12),
            "n_features": n_features,
            "n_dims": n_dims,
        },
        "critical_features": {
            "per_feature_max": per_feature_max,
            "drifted_count": drifted_count,
            "drifted_indices": drifted_indices,
        },
        "thresholds": {"stable_max": stable_max, "drift_max": drift_max},
        "classification": classification,
        "decision": decision,
    }
    if "checker_ref" in spec:
        record["checker_ref"] = spec["checker_ref"]
    if "non_claims" in spec:
        record["non_claims"] = spec["non_claims"]
    record["replay_seal"] = _seal(record)
    return record


def _seal(record: dict) -> str:
    """SHA-256 (FIPS 180-4) over the canonical inputs and verdict."""
    payload = {
        "check_id": record["check_id"],
        "feature_space_a_ref": record["feature_space_a_ref"],
        "feature_space_b_ref": record["feature_space_b_ref"],
        "procrustes": {
            "residual": record["procrustes"]["residual"],
            "disparity": record["procrustes"]["disparity"],
            "n_features": record["procrustes"]["n_features"],
            "n_dims": record["procrustes"]["n_dims"],
        },
        "critical_features": record["critical_features"],
        "thresholds": record["thresholds"],
        "classification": record["classification"],
        "decision": record["decision"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# CLI.
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Procrustes feature-alignment / drift checker")
    p.add_argument("input", type=Path, help="check-input JSON (two feature spaces + thresholds)")
    p.add_argument(
        "--max-class",
        choices=_SEVERITY,
        default="drifted",
        help="highest drift classification that still passes (default: drifted; broken blocks)",
    )
    p.add_argument("--emit-record", type=Path, default=None, help="write the emitted record to this path")
    p.add_argument("--quiet", action="store_true", help="suppress the record on stdout")
    args = p.parse_args(argv)

    try:
        spec = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[REJECT] cannot read check input: {exc}", file=sys.stderr)
        return 2
    if not isinstance(spec, dict):
        print("[REJECT] check input must be a JSON object", file=sys.stderr)
        return 2
    for key in ("feature_space_a_ref", "feature_space_b_ref"):
        if not spec.get(key):
            print(f"[REJECT] missing required field: {key}", file=sys.stderr)
            return 2

    try:
        record = compute_drift(spec)
    except MalformedInput as exc:
        print(f"[REJECT] malformed input: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(record, indent=2, sort_keys=True)
    if args.emit_record is not None:
        args.emit_record.write_text(rendered + "\n", encoding="utf-8")
    if not args.quiet:
        print(rendered)

    cls = record["classification"]
    ok = _SEVERITY.index(cls) <= _SEVERITY.index(args.max_class)
    summary = (
        f"residual={record['procrustes']['residual']:.6f} "
        f"critical_drifted={record['critical_features']['drifted_count']} "
        f"class={cls} decision={record['decision']} "
        f"max_class={args.max_class} -> {'PASS' if ok else 'FAIL'}"
    )
    print(summary, file=sys.stderr)
    if not ok:
        print(
            f"[FAIL] alignment drift classification '{cls}' exceeds allowed '{args.max_class}' "
            "(model promotion blocked)",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
