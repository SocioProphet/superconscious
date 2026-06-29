"""Tests for the substrate-parametric Hopfield primitive + three-regime classifier (§2-§3)."""
import numpy as np

from superconscious_core.hopfield import (
    retrieve, retrieve_weights, energy, classify_regime, normalized_entropy, capacity_bound,
)
from superconscious_core.substrate import (
    RealSubstrate, ComplexSubstrate, QuaternionSubstrate, get_substrate,
)


def _patterns(real_sub, n=6, d=8, seed=0):
    """n well-separated real patterns shaped (N, d, dof) for the given substrate."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d, real_sub.dof))
    # normalize each pattern so magnitudes are comparable
    for i in range(n):
        X[i] /= np.linalg.norm(X[i])
    return X


def test_retrieve_recovers_a_stored_pattern_single_regime():
    sub = RealSubstrate()
    X = _patterns(sub)
    xi = X[2] + 0.01 * np.random.default_rng(1).standard_normal(X[2].shape)  # near pattern 2
    out, w = retrieve(X, xi, beta=20.0, substrate=sub)
    reg = classify_regime(w)
    assert reg.label == "single"
    assert reg.top_index == 2
    assert reg.action == "proceed"
    # the retrieved state is close to the stored pattern
    assert np.linalg.norm(out - X[2]) < np.linalg.norm(xi - X[2]) + 1e-6


def test_uniform_query_is_global_regime_and_blocks():
    sub = RealSubstrate()
    X = _patterns(sub)
    xi = np.zeros(X[0].shape)            # equidistant from all → near-uniform softmax
    _, w = retrieve(X, xi, beta=1.0, substrate=sub)
    reg = classify_regime(w)
    assert reg.label == "global"
    assert reg.action == "block"
    assert normalized_entropy(w) >= 0.95


def test_two_close_patterns_give_metastable():
    sub = RealSubstrate()
    rng = np.random.default_rng(3)
    base = rng.standard_normal((1, 8, 1)); base /= np.linalg.norm(base)
    twin = base + 0.05 * rng.standard_normal(base.shape)  # a near-duplicate
    far = rng.standard_normal((4, 8, 1))
    for i in range(4):
        far[i] /= np.linalg.norm(far[i])
    X = np.concatenate([base, twin, far], axis=0)
    xi = (base[0] + twin[0]) / 2          # sits between the two close patterns
    _, w = retrieve(X, xi, beta=12.0, substrate=sub)
    reg = classify_regime(w)
    assert reg.label == "metastable"
    assert reg.action == "approve"


def test_energy_descends_across_a_retrieval_step():
    sub = RealSubstrate()
    X = _patterns(sub)
    xi = X[1] + 0.3 * np.random.default_rng(4).standard_normal(X[1].shape)
    e0 = energy(X, xi, beta=8.0, substrate=sub)
    out, _ = retrieve(X, xi, beta=8.0, substrate=sub)
    e1 = energy(X, out, beta=8.0, substrate=sub)
    assert e1 <= e0 + 1e-9                 # concave-convex update does not increase energy


def test_regime_labels_are_substrate_invariant():
    """The same query/pattern geometry yields the same regime label across R, C, H (§2.3)."""
    labels = {}
    for name in ("R", "C", "H"):
        sub = get_substrate(name)
        X = _patterns(sub, seed=7)         # same seed → same realified geometry up to dof width
        xi = X[3] + 0.01 * np.random.default_rng(7).standard_normal(X[3].shape)
        _, w = retrieve(X, xi, beta=20.0, substrate=sub)
        labels[name] = classify_regime(w).label
    assert labels["R"] == labels["C"] == labels["H"] == "single"


def test_quaternion_hamilton_product_is_noncommutative_and_correct():
    # i * j = k  but  j * i = -k  (the defining non-commutativity Gaudet's networks exploit)
    i = np.array([0.0, 1, 0, 0]); j = np.array([0.0, 0, 1, 0]); k = np.array([0.0, 0, 0, 1])
    ij = QuaternionSubstrate.hamilton_product(i, j)
    ji = QuaternionSubstrate.hamilton_product(j, i)
    assert np.allclose(ij, k)
    assert np.allclose(ji, -k)


def test_capacity_is_exponential_in_real_dimension():
    # higher-dof substrate carries more patterns per pattern-slot (§2.2): C(d,dof=4) > C(d,dof=1)
    assert capacity_bound(8, 4) > capacity_bound(8, 1)
    assert capacity_bound(16, 1) > capacity_bound(8, 1)


def test_retrieve_weights_sum_to_one():
    sub = RealSubstrate()
    X = _patterns(sub)
    w = retrieve_weights(X, X[0], beta=5.0, substrate=sub)
    assert abs(float(w.sum()) - 1.0) < 1e-9
    assert (w >= 0).all()
