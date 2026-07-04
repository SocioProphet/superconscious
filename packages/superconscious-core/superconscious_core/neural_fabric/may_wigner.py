"""May-Wigner capacity monitor for activation-time targeting.

The control number is s * sqrt(m * C), where m is active feature count,
C is feature co-activation density, and s is effective interaction scale.
The stability boundary is 1.0; the operational policy should start warning
well before the boundary.
"""
from __future__ import annotations

from math import sqrt


def may_wigner_number(m: int | float, C: int | float, s: int | float) -> float:
    if float(m) < 0 or float(C) < 0 or float(s) < 0:
        raise ValueError("m, C, and s must be non-negative")
    return float(s) * sqrt(float(m) * float(C))


def classify_may_wigner(value: float, *, warn: float = 0.70, error: float = 0.85, stop: float = 0.95) -> str:
    """Classify a May-Wigner number for governance routing."""
    v = float(value)
    if v >= stop:
        return "stop"
    if v >= error:
        return "error"
    if v >= warn:
        return "warn"
    return "ok"
