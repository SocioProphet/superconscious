"""Invariants for the May-Wigner capacity monitor."""
from __future__ import annotations

from math import sqrt

import pytest

from superconscious_core.neural_fabric.may_wigner import (
    classify_may_wigner,
    may_wigner_number,
)


def test_control_number_matches_closed_form() -> None:
    assert may_wigner_number(60, 0.4, 0.1) == pytest.approx(0.1 * sqrt(60 * 0.4))
    assert may_wigner_number(0, 1, 1) == 0.0
    assert may_wigner_number(4, 1, 1) == pytest.approx(2.0)


def test_control_number_is_monotone_in_each_argument() -> None:
    base = may_wigner_number(50, 0.4, 0.1)
    assert may_wigner_number(80, 0.4, 0.1) > base
    assert may_wigner_number(50, 0.6, 0.1) > base
    assert may_wigner_number(50, 0.4, 0.2) > base


def test_negative_inputs_are_rejected() -> None:
    for bad in ((-1, 1, 1), (1, -1, 1), (1, 1, -1)):
        with pytest.raises(ValueError):
            may_wigner_number(*bad)


@pytest.mark.parametrize(
    "value,expected",
    [
        (0.0, "ok"),
        (0.69, "ok"),
        (0.70, "warn"),
        (0.84, "warn"),
        (0.85, "error"),
        (0.94, "error"),
        (0.95, "stop"),
        (1.5, "stop"),
    ],
)
def test_classification_thresholds(value: float, expected: str) -> None:
    assert classify_may_wigner(value) == expected


def test_smoke_operating_point_is_stable() -> None:
    # The point exercised by neural-fabric-smoke must stay comfortably below warn.
    assert classify_may_wigner(may_wigner_number(60, 0.4, 0.1)) == "ok"
