"""hopfield.py — the Hopfield retrieval PRIMITIVE + the three-regime governance classifier (§2).

Modern continuous Hopfield retrieval (Ramsauer et al. 2020, "Hopfield Networks is All You Need" — the file
mislabeled Polson_2025). One concave-convex update minimizes the energy and IS transformer attention with X as
both key and value:

    energy:  E(xi) = -lse(beta, Re(X* xi)) + 1/2 <xi,xi> + beta^-1 log N + 1/2 M^2
    update:  xi_new = X . softmax(beta Re(X* xi))            ( = attention(Q=xi, K=V=X), beta = 1/sqrt(d_k) )

The softmax weights are REAL, so the substrate (substrate.py) enters only through inner_score + combine — making
the THREE-REGIME classification substrate-invariant (§2.3), the unifying governance handle the framework builds on:

    single      max_i w_i >= tau_single (0.85)                          decisive retrieval        -> proceed
    metastable  max_i w_i <  tau_single and H(w)/log N < rho (0.95)      a cluster shares the mass -> log / approve
    global      H(w)/log N >= rho                                        near-uniform, no decision -> block / escalate

Pure + numpy-only.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .substrate import Substrate, RealSubstrate

TAU_SINGLE = 0.85   # max-weight threshold for a decisive single-pattern retrieval
RHO_GLOBAL = 0.95   # normalized-entropy threshold above which the retrieval is near-uniform (no decision)


def _softmax(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    m = z.max()
    e = np.exp(z - m)
    return e / e.sum()


def retrieve_weights(X: np.ndarray, xi: np.ndarray, beta: float, substrate: Substrate) -> np.ndarray:
    """The real softmax retrieval weights w = softmax(beta Re(X* xi)), shape (N,)."""
    return _softmax(beta * substrate.inner_score(X, xi))


def retrieve(X: np.ndarray, xi: np.ndarray, beta: float, substrate: Substrate | None = None):
    """One Hopfield update. Returns (xi_new in-substrate, weights). substrate defaults to Real."""
    sub = substrate or RealSubstrate()
    w = retrieve_weights(X, xi, beta, sub)
    return sub.combine(X, w), w


def energy(X: np.ndarray, xi: np.ndarray, beta: float, substrate: Substrate | None = None) -> float:
    """Hopfield energy E(xi). Decreasing across a retrieve() step (energy-descent invariant, §3.1)."""
    sub = substrate or RealSubstrate()
    scores = beta * sub.inner_score(X, xi)              # (N,)
    n = scores.shape[0]
    lse = float(scores.max() + np.log(np.exp(scores - scores.max()).sum())) / beta
    xi_sq = sub.magnitude(xi) ** 2
    M = max(sub.magnitude(X[i]) for i in range(n))
    return -lse + 0.5 * xi_sq + np.log(n) / beta + 0.5 * M * M


def normalized_entropy(weights: np.ndarray) -> float:
    """H(w)/log N in [0,1]; 0 = one-hot (single), 1 = uniform (global)."""
    w = np.asarray(weights, dtype=float)
    n = w.shape[0]
    if n <= 1:
        return 0.0
    nz = w[w > 0]
    h = float(-(nz * np.log(nz)).sum())
    return h / np.log(n)


@dataclass
class Regime:
    label: str           # "single" | "metastable" | "global"
    max_weight: float
    norm_entropy: float
    top_index: int
    action: str          # "proceed" | "approve" | "block"


def classify_regime(weights: np.ndarray, tau_single: float = TAU_SINGLE, rho_global: float = RHO_GLOBAL) -> Regime:
    """The substrate-INVARIANT governance protocol. Maps the weight distribution to a regime + approval action."""
    w = np.asarray(weights, dtype=float)
    mx = float(w.max())
    ne = normalized_entropy(w)
    top = int(w.argmax())
    if mx >= tau_single:
        return Regime("single", mx, ne, top, "proceed")
    if ne >= rho_global:
        return Regime("global", mx, ne, top, "block")
    return Regime("metastable", mx, ne, top, "approve")


def capacity_bound(d: int, dof: int, c: float = 1.5, p: float = 1e-3) -> float:
    """Storage capacity is exponential in the REAL dimension d.dof (§2.2): N <= 1/4 p^-1/4 c^((d.dof-1)/2)."""
    return 0.25 * (p ** -0.25) * (c ** ((d * dof - 1) / 2.0))
