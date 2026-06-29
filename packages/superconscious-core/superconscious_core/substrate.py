"""substrate.py — the SUBSTRATE axis of the Substrates/Structures/Circuits framework (§3).

A Substrate is the algebra over which the Hopfield retrieval primitive operates. The framework's key
observation (§2.1, §3.1): the Hopfield update is a REAL-weighted convex combination — the softmax weights are
real — so the substrate enters retrieval ONLY through two real operations:

    inner_score(X, xi) -> real (N,)   the per-pattern score  Re(X* xi)
    combine(X, w)      -> in-substrate the weighted sum       X . w   (real w)
    magnitude(x)       -> real scalar  |x|

For the Cayley-Dickson chain (R, C, H, O, S) the real part of the conjugate inner product Re(conj(a)·b) is just
the Euclidean dot product of the realified components, so `inner_score` is substrate-INVARIANT once realified —
which is exactly why the three-regime governance classifier (hopfield.classify_regime) applies uniformly across
all substrates. Non-commutativity / non-associativity only bite in COMPOSED products (iterated projections), which
the framework forbids precomputing; QuaternionSubstrate.hamilton_product exposes that composition path explicitly
(Gaudet & Maida 2018, Deep Quaternion Networks) so it is audited rather than hidden.

dof(V): R=1, C=2, H=4, O=8, S=16. Capacity is exponential in d·dof (§2.2).

Pure + numpy-only.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np


class Substrate(ABC):
    """Abstract substrate. A pattern store X is real-shaped (N, d, dof); a query xi is (d, dof)."""

    #: real degrees of freedom per element (R=1, C=2, H=4, O=8, S=16, ...)
    dof: int = 1
    name: str = "abstract"

    def realify(self, x: np.ndarray) -> np.ndarray:
        """Flatten an in-substrate value to its real coordinates (the pi: V^d -> R^{d.dof} map)."""
        return np.asarray(x, dtype=float).reshape(-1)

    @abstractmethod
    def inner_score(self, X: np.ndarray, xi: np.ndarray) -> np.ndarray:
        """Per-pattern real score vector Re(X* xi), shape (N,). X is (N, d, dof), xi is (d, dof)."""

    @abstractmethod
    def combine(self, X: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """Real-weighted sum sum_n w_n x_n, returned in the substrate, shape (d, dof)."""

    @abstractmethod
    def magnitude(self, x: np.ndarray) -> float:
        """Euclidean norm of the realified element."""


class _NormedAlgebraSubstrate(Substrate):
    """Shared impl for R/C/H/O/S: retrieval is the realified Euclidean inner product + real combine."""

    def inner_score(self, X: np.ndarray, xi: np.ndarray) -> np.ndarray:
        Xf = np.asarray(X, dtype=float).reshape(X.shape[0], -1)  # (N, d*dof)
        xf = np.asarray(xi, dtype=float).reshape(-1)             # (d*dof,)
        return Xf @ xf                                           # Re(conj(x_n)·xi) summed = Euclidean dot

    def combine(self, X: np.ndarray, weights: np.ndarray) -> np.ndarray:
        w = np.asarray(weights, dtype=float)
        # sum_n w_n x_n with real w — never invokes a triple-substrate product (§3.1), so associativity-safe.
        return np.tensordot(w, np.asarray(X, dtype=float), axes=(0, 0))  # (d, dof)

    def magnitude(self, x: np.ndarray) -> float:
        return float(np.linalg.norm(np.asarray(x, dtype=float).reshape(-1)))


class RealSubstrate(_NormedAlgebraSubstrate):
    dof = 1
    name = "R"


class ComplexSubstrate(_NormedAlgebraSubstrate):
    dof = 2
    name = "C"


class QuaternionSubstrate(_NormedAlgebraSubstrate):
    dof = 4
    name = "H"

    @staticmethod
    def hamilton_product(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Hamilton product of two quaternions a,b given as 4-vectors [w,x,y,z] (Gaudet & Maida 2018).
        NON-COMMUTATIVE — a*b != b*a. The retrieval path never calls this (real-weighted combine only); it is the
        explicit, auditable composition op for the forbidden-to-precompute iterated-projection path (§3.1)."""
        aw, ax, ay, az = a
        bw, bx, by, bz = b
        return np.array([
            aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
        ])


class OctonionSubstrate(_NormedAlgebraSubstrate):
    dof = 8
    name = "O"  # non-associative; retrieval is still real-weighted so energy-descent carries (§3.1)


class SedenionSubstrate(_NormedAlgebraSubstrate):
    dof = 16
    name = "S"  # has zero divisors; runtime energy-descent assertion required per retrieval (§3.1)


SUBSTRATES = {
    "R": RealSubstrate,
    "C": ComplexSubstrate,
    "H": QuaternionSubstrate,
    "O": OctonionSubstrate,
    "S": SedenionSubstrate,
}


def get_substrate(name: str) -> Substrate:
    if name not in SUBSTRATES:
        raise ValueError(f"unknown substrate {name!r}; known: {sorted(SUBSTRATES)}")
    return SUBSTRATES[name]()
