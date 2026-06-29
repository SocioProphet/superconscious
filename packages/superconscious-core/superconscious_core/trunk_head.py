"""trunk_head.py — the ARCHITECTURE: shared trunk + per-adapter heads, two softmaxes, two-layer approval (§5).

One shared Hopfield trunk (hopfield.retrieve over a substrate) is applied to every adapter. Each adapter `a`
adds: an input projection phi_a (lift its embeddings to the trunk space), a pattern store X_a (its catalog), and
a readout head (W_h, b_h). The forward pass produces TWO softmaxes with a clean latent-variable reading (§5.2):

    P(n | xi) = softmax(beta Re(X_a* phi_a(xi)))      trunk: pattern-index posterior  (the retrieval weights)
    P(y | n)  = softmax(W_h pi(x_n))                   head:  per-pattern observation model
    P(y | xi) = sum_n P(y | n) P(n | xi)               recompose: marginalize the discrete latent

This makes decompose / recompose / understand structurally sound:
  • decompose  — factor any decision into pattern-selection (trunk) × pattern-readout (head)
  • recompose  — marginalize the latent for P(y|xi); Bayes-invert for P(n | xi, y)
  • the head's accuracy with the trunk frozen is the Alain-Bengio anchored-probe measure of trunk content

Two-layer approval (§5.3): a decision needs human approval when the trunk retrieval is NOT decisive (regime !=
single, via hopfield.classify_regime — the substrate-invariant handle from the primitive) OR the head is not
confident (max P(y|xi) < threshold). Each trigger has a named source for the audit emission.

Pure + numpy-only; builds on hopfield.py + substrate.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from .substrate import Substrate, RealSubstrate
from .hopfield import retrieve_weights, classify_regime, Regime


def _softmax_rows(Z: np.ndarray) -> np.ndarray:
    Z = np.asarray(Z, dtype=float)
    m = Z.max(axis=-1, keepdims=True)
    e = np.exp(Z - m)
    return e / e.sum(axis=-1, keepdims=True)


@dataclass
class PerAdapterHead:
    """One adapter's head over the shared trunk. X is (N, d, dof); W_h is (K, d*dof); b is (K,)."""
    name: str
    X: np.ndarray                       # the adapter's pattern store, realifiable to (N, d*dof)
    W_h: np.ndarray                     # readout (K, d*dof)
    b: np.ndarray                       # bias (K,)
    substrate: Substrate = field(default_factory=RealSubstrate)
    beta: float = 8.0
    labels: list[str] | None = None     # optional K decision-vocabulary labels

    def _Xreal(self) -> np.ndarray:
        return np.asarray(self.X, dtype=float).reshape(self.X.shape[0], -1)  # (N, d*dof)

    def p_y_given_n(self) -> np.ndarray:
        """P(y|n): the head applied to each stored pattern, (N, K). The observation model."""
        logits = self._Xreal() @ self.W_h.T + self.b  # (N, K)
        return _softmax_rows(logits)


@dataclass
class HeadDecision:
    adapter: str
    trunk_weights: np.ndarray   # P(n|xi), (N,)
    regime: Regime              # the trunk retrieval regime (single/metastable/global)
    head_softmax: np.ndarray    # P(y|xi) = sum_n P(y|n) P(n|xi), (K,)  — the marginalized, latent-variable reading
    chosen_index: int
    chosen_prob: float
    chosen_label: str | None
    requires_approval: bool
    triggered_by: list[str]


def forward(head: PerAdapterHead, xi: np.ndarray, approval_threshold: float = 0.6) -> HeadDecision:
    """Run one adapter through the shared trunk + its head, with the two-layer approval gate.

    `xi` is already in the trunk space (apply phi_a upstream). The marginalized P(y|xi) = sum_n P(y|n)P(n|xi) is
    used as the decision distribution — the probabilistically-clean recompose, not head(retrieved-mean)."""
    w = retrieve_weights(head.X, xi, head.beta, head.substrate)   # P(n|xi), (N,)
    regime = classify_regime(w)
    p_yn = head.p_y_given_n()                                     # (N, K)
    p_y = w @ p_yn                                                # P(y|xi) = sum_n P(y|n) P(n|xi), (K,)
    k = int(p_y.argmax())
    pk = float(p_y[k])

    triggered: list[str] = []
    if regime.label != "single":
        triggered.append("trunk_regime_non_single")
    if pk < approval_threshold:
        triggered.append("head_confidence_low")

    return HeadDecision(
        adapter=head.name,
        trunk_weights=w,
        regime=regime,
        head_softmax=p_y,
        chosen_index=k,
        chosen_prob=pk,
        chosen_label=(head.labels[k] if head.labels and k < len(head.labels) else None),
        requires_approval=len(triggered) > 0,
        triggered_by=triggered,
    )


def posterior_over_patterns_given_label(decision: HeadDecision, head: PerAdapterHead, y: int) -> np.ndarray:
    """Bayes-invert (the `decompose`/`understand` direction): P(n | xi, y) ∝ P(y|n) P(n|xi). Returns (N,)."""
    p_yn = head.p_y_given_n()[:, y]                # P(y=given|n), (N,)
    joint = p_yn * decision.trunk_weights          # P(y|n) P(n|xi)
    s = joint.sum()
    return joint / s if s > 0 else joint
