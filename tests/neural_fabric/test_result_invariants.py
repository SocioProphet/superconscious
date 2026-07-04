"""Invariants for the committed activation-time targeting artifacts.

These pin the reference results/events so a regression in the suite or the
primitives is caught in CI, and they enforce the core doctrine (activation-time
interventions never update weights).
"""
from __future__ import annotations

import json
import pathlib
import re

import pytest

_REPO = pathlib.Path(__file__).resolve().parents[2]
_SUITE = _REPO / "research" / "activation-time-targeting"
_EXP_ID = re.compile(r"^NF-ATT-[0-9]{3}$")
_EVENT_ID = re.compile(r"^NF-ATT-[0-9]{3}-EV[0-9]{3}$")


def _load(rel: str) -> dict:
    return json.loads((_SUITE / rel).read_text(encoding="utf-8"))


def _all(subdir: str, glob: str) -> list[pathlib.Path]:
    return sorted((_SUITE / subdir).glob(glob))


def test_reference_results_exist() -> None:
    assert _all("results", "*.result.json"), "no committed reference results"


@pytest.mark.parametrize("path", _all("results", "*.result.json"), ids=lambda p: p.stem)
def test_result_never_updates_weights(path: pathlib.Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["weights_updated"] is False
    assert _EXP_ID.match(doc["experiment_id"])
    assert doc["epistemic_status"] == "toy_model_confirmed"


@pytest.mark.parametrize("path", _all("events", "*.event.json"), ids=lambda p: p.stem)
def test_event_is_a_non_weight_updating_audit_record(path: pathlib.Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["weights_updated"] is False
    assert _EVENT_ID.match(doc["event_id"])
    assert doc["event_id"].startswith(doc["experiment_id"])


def test_logit_boost_experiment_lifts_target_monotonically() -> None:
    m = _load("results/NF-ATT-001.result.json")["metrics"]
    assert m["target_prob_lift"] > 0
    assert m["lift_is_monotone"] is True
    assert m["argmax_is_target_after_boost"] is True


def test_may_wigner_sweep_locates_stability_boundaries() -> None:
    m = _load("results/NF-ATT-002.result.json")["metrics"]
    # sweep should stay stable at small m and cross into the stop band by m=400.
    assert m["max_ok_m"] > 0
    assert m["m_first_warn"] > m["max_ok_m"] >= 0
    assert m["m_first_stop"] >= m["m_first_error"] >= m["m_first_warn"]
