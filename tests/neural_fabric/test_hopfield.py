"""Invariants for the Hopfield activation-time intervention primitives."""
from __future__ import annotations

import numpy as np
import pytest

from superconscious_core.neural_fabric.hopfield import (
    hopfield_retrieve,
    logit_boost,
    query_injection,
)


def _orthonormal_patterns() -> np.ndarray:
    return np.eye(4)


def test_retrieval_weights_form_a_distribution() -> None:
    patterns = _orthonormal_patterns()
    _, weights = hopfield_retrieve(patterns, patterns[0], beta=1.0)
    assert weights.shape == (4,)
    assert np.all(weights >= 0)
    assert weights.sum() == pytest.approx(1.0)


def test_high_beta_concentrates_on_nearest_pattern() -> None:
    patterns = _orthonormal_patterns()
    retrieved, weights = hopfield_retrieve(patterns, patterns[2], beta=50.0)
    assert int(np.argmax(weights)) == 2
    assert retrieved == pytest.approx(patterns[2], abs=1e-6)


def test_shape_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError):
        hopfield_retrieve(np.eye(4), np.zeros(3))
    with pytest.raises(ValueError):
        hopfield_retrieve(np.zeros(4), np.zeros(4))  # rank-1 patterns


def test_query_injection_shifts_query_toward_target() -> None:
    q = np.zeros(4)
    target = np.array([0.0, 1.0, 0.0, 0.0])
    out = query_injection(q, target, strength=2.0)
    assert out == pytest.approx(np.array([0.0, 2.0, 0.0, 0.0]))
    # Injection must not mutate the caller's query in place.
    assert q == pytest.approx(np.zeros(4))


def test_logit_boost_raises_target_probability_without_touching_weights() -> None:
    patterns = _orthonormal_patterns()
    query = np.full(4, 0.25)
    _, base_weights = hopfield_retrieve(patterns, query, beta=1.0)
    boosted = logit_boost(patterns, query, target_idx=1, strength=3.0, beta=1.0)
    assert boosted.sum() == pytest.approx(1.0)
    assert boosted[1] > base_weights[1]
    assert int(np.argmax(boosted)) == 1
