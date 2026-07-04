#!/usr/bin/env python3
"""Deterministic, CPU-only activation-time targeting suite.

Each experiment exercises a Neural Fabric reference primitive and emits a
``targeting-result.v1`` document under ``<out>/results``. Interventions
additionally emit ``intervention-event.v1`` audit records under ``<out>/events``
-- the doctrine governs every intervention by an audit event. The experiments
are intentionally ``toy_model_confirmed``: they demonstrate that steering and
capacity monitoring work *without updating weights* (``weights_updated`` is
always ``false``), not that they are production-safe.

    python3 research/activation-time-targeting/code/run_suite.py \
        --out research/activation-time-targeting
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "packages" / "superconscious-core"))

from superconscious_core.neural_fabric.hopfield import (  # noqa: E402
    hopfield_retrieve,
    logit_boost,
)
from superconscious_core.neural_fabric.may_wigner import (  # noqa: E402
    classify_may_wigner,
    may_wigner_number,
)

EPISTEMIC_STATUS = "toy_model_confirmed"


def experiment_hopfield_logit_boost() -> tuple[dict, list[dict]]:
    """NF-ATT-001: steer a Hopfield readout via logit boosting, no weight update."""
    patterns = np.eye(4)
    query = np.full(4, 0.25)
    target_idx = 1
    _, base_weights = hopfield_retrieve(patterns, query, beta=1.0)
    base_prob = float(base_weights[target_idx])

    rows: list[dict] = []
    events: list[dict] = []
    prev = -1.0
    monotone = True
    for strength in (0.0, 1.0, 2.0, 3.0):
        dist = logit_boost(patterns, query, target_idx=target_idx, strength=strength, beta=1.0)
        prob = float(dist[target_idx])
        monotone = monotone and (prob >= prev - 1e-12)
        prev = prob
        rows.append({"strength": strength, "target_prob": round(prob, 6)})
        if strength > 0.0:
            events.append(
                {
                    "event_id": f"NF-ATT-001-EV{len(events) + 1:03d}",
                    "experiment_id": "NF-ATT-001",
                    "intervention_type": "logit_boost",
                    "target_locus": "attention-logits",
                    "weights_updated": False,
                    "params": {"target_idx": target_idx, "strength": strength, "beta": 1.0},
                    "observed": {"target_prob": round(prob, 6)},
                    "epistemic_status": EPISTEMIC_STATUS,
                }
            )

    boosted_prob = rows[-1]["target_prob"]
    argmax_is_target = bool(
        np.argmax(logit_boost(patterns, query, target_idx=target_idx, strength=3.0, beta=1.0)) == target_idx
    )
    result = {
        "experiment_id": "NF-ATT-001",
        "weights_updated": False,
        "epistemic_status": EPISTEMIC_STATUS,
        "claim_invariants": [
            "weights_updated == false",
            "intervention is activation-time only",
            "target probability is monotone non-decreasing in boost strength",
        ],
        "metrics": {
            "baseline_target_prob": round(base_prob, 6),
            "boosted_target_prob": boosted_prob,
            "target_prob_lift": round(boosted_prob - base_prob, 6),
            "argmax_is_target_after_boost": argmax_is_target,
            "lift_is_monotone": bool(monotone),
        },
        "rows": rows,
    }
    return result, events


def experiment_may_wigner_sweep() -> tuple[dict, list[dict]]:
    """NF-ATT-002: sweep active-feature count and locate the stability boundaries."""
    C, s = 0.4, 0.1
    rows: list[dict] = []
    boundaries: dict[str, int | None] = {"warn": None, "error": None, "stop": None}
    max_ok_m = 0
    for m in range(10, 401, 10):
        value = may_wigner_number(m, C, s)
        cls = classify_may_wigner(value)
        if cls == "ok":
            max_ok_m = m
        for level in ("warn", "error", "stop"):
            if cls == level and boundaries[level] is None:
                boundaries[level] = m
        rows.append({"m": m, "may_wigner": round(value, 6), "classification": cls})

    result = {
        "experiment_id": "NF-ATT-002",
        "weights_updated": False,
        "epistemic_status": EPISTEMIC_STATUS,
        "claim_invariants": [
            "weights_updated == false",
            "control number is s*sqrt(m*C)",
            "classification is monotone non-decreasing in m",
        ],
        "metrics": {
            "C": C,
            "s": s,
            "max_ok_m": max_ok_m,
            "m_first_warn": boundaries["warn"] if boundaries["warn"] is not None else -1,
            "m_first_error": boundaries["error"] if boundaries["error"] is not None else -1,
            "m_first_stop": boundaries["stop"] if boundaries["stop"] is not None else -1,
        },
        "rows": rows,
    }
    return result, []  # capacity monitoring is observation, not intervention


EXPERIMENTS = (experiment_hopfield_logit_boost, experiment_may_wigner_sweep)


def _write(path: pathlib.Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Activation-time targeting suite")
    p.add_argument(
        "--out",
        type=pathlib.Path,
        default=_ROOT / "research" / "activation-time-targeting",
        help="suite root; results/ and events/ are written beneath it",
    )
    args = p.parse_args(argv)

    for build in EXPERIMENTS:
        result, events = build()
        exp_id = result["experiment_id"]
        _write(args.out / "results" / f"{exp_id}.result.json", result)
        print(f"[ok] {exp_id} result -> {args.out / 'results' / f'{exp_id}.result.json'}")
        for event in events:
            _write(args.out / "events" / f"{event['event_id']}.event.json", event)
        if events:
            print(f"[ok] {exp_id} emitted {len(events)} intervention event(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
