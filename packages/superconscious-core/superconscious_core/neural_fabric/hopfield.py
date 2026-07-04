"""Hopfield retrieval and activation-time intervention primitives."""
from __future__ import annotations

import numpy as np


def _softmax(x: np.ndarray) -> np.ndarray:
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def hopfield_retrieve(patterns: np.ndarray, query: np.ndarray, *, beta: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Return Hopfield-style retrieved vector and pattern weights.

    `patterns` is shaped [N, d]. The update is the transformer-attention/Hopfield
    primitive: softmax(beta * X q) followed by X^T w.
    """
    X = np.asarray(patterns, dtype=float)
    q = np.asarray(query, dtype=float)
    if X.ndim != 2:
        raise ValueError("patterns must be a rank-2 array")
    if q.shape != (X.shape[1],):
        raise ValueError(f"query shape {q.shape} does not match pattern dimension {X.shape[1]}")
    logits = beta * (X @ q)
    weights = _softmax(logits)
    return weights @ X, weights


def query_injection(query: np.ndarray, target_pattern: np.ndarray, strength: float) -> np.ndarray:
    """Inject target direction into the query vector without changing weights."""
    return np.asarray(query, dtype=float) + float(strength) * np.asarray(target_pattern, dtype=float)


def logit_boost(patterns: np.ndarray, query: np.ndarray, *, target_idx: int, strength: float, beta: float = 1.0) -> np.ndarray:
    """Boost one target logit directly and return the resulting distribution."""
    X = np.asarray(patterns, dtype=float)
    q = np.asarray(query, dtype=float)
    logits = beta * (X @ q)
    logits[int(target_idx)] += float(strength)
    return _softmax(logits)
