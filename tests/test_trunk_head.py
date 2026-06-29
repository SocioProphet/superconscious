"""Tests for the shared-trunk + per-adapter-head architecture + two-layer approval (§5)."""
import numpy as np

from superconscious_core.substrate import RealSubstrate
from superconscious_core.trunk_head import (
    PerAdapterHead, forward, posterior_over_patterns_given_label,
)


def _head(n=5, d=6, k=3, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d, 1))
    for i in range(n):
        X[i] /= np.linalg.norm(X[i])
    W_h = rng.standard_normal((k, d))     # d*dof = d for Real
    b = np.zeros(k)
    return PerAdapterHead(name="policy", X=X, W_h=W_h, b=b, substrate=RealSubstrate(), beta=20.0,
                          labels=[f"y{j}" for j in range(k)]), X


def test_two_softmax_marginal_is_a_distribution():
    head, X = _head()
    d = forward(head, X[2] + 0.01 * np.random.default_rng(1).standard_normal(X[2].shape))
    assert abs(float(d.head_softmax.sum()) - 1.0) < 1e-9
    assert (d.head_softmax >= 0).all()
    assert 0 <= d.chosen_index < len(head.labels)
    assert d.chosen_label == head.labels[d.chosen_index]


def test_decisive_single_regime_with_confident_head_does_not_require_approval():
    head, X = _head(seed=2)
    # craft a head that is confident for pattern 2's observation: make W_h strongly align row 0 with x_2
    x2 = head.X[2].reshape(-1)
    head.W_h = np.vstack([8.0 * x2, -8.0 * x2, np.zeros_like(x2)])  # label y0 dominates near x_2
    d = forward(head, X[2] + 0.005 * np.random.default_rng(3).standard_normal(X[2].shape), approval_threshold=0.6)
    assert d.regime.label == "single"
    assert d.chosen_index == 0
    assert d.requires_approval is False
    assert d.triggered_by == []


def test_non_single_trunk_regime_triggers_approval():
    head, X = _head(seed=4)
    xi = np.zeros(X[0].shape)              # equidistant → global regime
    d = forward(head, xi)
    assert d.regime.label in ("global", "metastable")
    assert d.requires_approval is True
    assert "trunk_regime_non_single" in d.triggered_by


def test_low_head_confidence_triggers_approval_even_when_trunk_is_decisive():
    head, X = _head(seed=5)
    # flat head → P(y|n) near-uniform → marginal near-uniform → low max prob, but trunk can still be single
    head.W_h = np.zeros_like(head.W_h)
    d = forward(head, X[1] + 0.005 * np.random.default_rng(6).standard_normal(X[1].shape), approval_threshold=0.6)
    assert d.regime.label == "single"               # trunk is decisive
    assert d.chosen_prob < 0.6
    assert "head_confidence_low" in d.triggered_by
    assert d.requires_approval is True


def test_bayes_invert_posterior_over_patterns_is_a_distribution():
    head, X = _head(seed=7)
    d = forward(head, X[3] + 0.01 * np.random.default_rng(7).standard_normal(X[3].shape))
    post = posterior_over_patterns_given_label(d, head, y=d.chosen_index)
    assert abs(float(post.sum()) - 1.0) < 1e-9
    assert (post >= 0).all()
    # conditioning on the chosen label should concentrate mass on the retrieved pattern
    assert post.argmax() == d.trunk_weights.argmax()


def test_marginal_equals_explicit_sum_over_latent():
    """P(y|xi) returned by forward must equal sum_n P(y|n) P(n|xi) computed independently."""
    head, X = _head(seed=8)
    xi = X[0] + 0.05 * np.random.default_rng(8).standard_normal(X[0].shape)
    d = forward(head, xi)
    explicit = d.trunk_weights @ head.p_y_given_n()
    assert np.allclose(d.head_softmax, explicit)
