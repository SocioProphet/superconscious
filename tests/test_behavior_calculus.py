from __future__ import annotations

import json
from pathlib import Path

from superconscious_core.behavior import (
    Proc,
    feedback_delay_1,
    parallel,
    project_observation,
    serial,
    trace,
    trace_equivalent,
)

ROOT = Path(__file__).resolve().parents[1]
ORGANISM_FIXTURE = ROOT / "examples" / "behavior" / "tiny-organism.json"


def make_append_proc(proc_id: str, input_type: str, output_type: str, token: str) -> Proc:
    def step(state, input_value):
        count = int(state.get("count", 0)) + 1
        return f"{input_value}|{token}:{count}", {"count": count}

    return Proc(
        proc_id=proc_id,
        input_type=input_type,
        output_type=output_type,
        state_type=f"S_{proc_id}",
        step_fn=step,
    )


def test_serial_composition_threads_output_and_product_state() -> None:
    first = make_append_proc("perceive", "Raw", "Features", "features")
    second = make_append_proc("policy", "Features", "Action", "action")

    composed = serial(first, second, proc_id="policy_after_perceive")
    output, state = composed.step({}, "raw")

    assert output == "raw|features:1|action:1"
    assert state["perceive"] == {"count": 1}
    assert state["policy"] == {"count": 1}
    assert composed.input_type == "Raw"
    assert composed.output_type == "Action"


def test_serial_composition_rejects_type_mismatch() -> None:
    first = make_append_proc("perceive", "Raw", "Features", "features")
    second = make_append_proc("policy", "Belief", "Action", "action")

    try:
        serial(first, second)
    except ValueError as exc:
        assert "serial type mismatch" in str(exc)
    else:  # pragma: no cover - defensive assertion shape
        raise AssertionError("serial composition should reject mismatched types")


def test_parallel_composition_runs_paired_inputs() -> None:
    left = make_append_proc("left", "I_left", "O_left", "L")
    right = make_append_proc("right", "I_right", "O_right", "R")

    composed = parallel(left, right)
    output, state = composed.step({}, ("a", "b"))

    assert output == ("a|L:1", "b|R:1")
    assert state["left"] == {"count": 1}
    assert state["right"] == {"count": 1}


def test_feedback_delay_1_uses_previous_output_next_tick() -> None:
    def step(state, input_value):
        external, previous_feedback = input_value
        count = int(state.get("count", 0)) + 1
        output = {"external": external, "previous": previous_feedback, "count": count}
        return output, {"count": count}

    proc = Proc(
        proc_id="feedback_demo",
        input_type="(External x Feedback)",
        output_type="Feedback",
        state_type="S_feedback_demo",
        step_fn=step,
    )
    wrapped = feedback_delay_1(proc, {"seed": True}, input_type="External", output_type="Feedback")

    first_output, first_state = wrapped.step({}, "tick-1")
    second_output, _ = wrapped.step(first_state, "tick-2")

    assert first_output["previous"] == {"seed": True}
    assert second_output["previous"] == first_output


def test_trace_equivalence_uses_projection() -> None:
    left_outputs = [
        {"summary": "created", "volatile": "t1"},
        {"summary": "completed", "volatile": "t2"},
    ]
    right_outputs = [
        {"summary": "created", "volatile": "x1"},
        {"summary": "completed", "volatile": "x2"},
    ]

    def projection(output):
        return {"summary": output["summary"]}

    assert trace_equivalent(left_outputs, right_outputs, projection)
    assert project_observation(left_outputs[0], projection) == {"summary": "created"}


def test_trace_runs_finite_input_stream() -> None:
    proc = make_append_proc("counter", "Raw", "Features", "seen")
    outputs, state = trace(proc, {}, ["a", "b", "c"])

    assert outputs == ["a|seen:1", "b|seen:2", "c|seen:3"]
    assert state == {"count": 3}


def test_tiny_organism_fixture_preserves_authority_boundaries() -> None:
    data = json.loads(ORGANISM_FIXTURE.read_text(encoding="utf-8"))
    boundary = data["authority_boundary"]

    assert data["kind"] == "OrganismWiring"
    assert data["determinism"] == "deterministic-v0"
    assert boundary["owner_repo"] == "SocioProphet/superconscious"
    assert boundary["schema_authority"] == "SourceOS-Linux/sourceos-spec"
    assert boundary["evidence_replay_authority"] == "SocioProphet/agentplane"
    assert boundary["direct_mutation_allowed"] is False
    assert "rawPrivateReasoning" in data["observation_projection"]["forbidden_fields"]
    assert any(edge["wire_type"] == "feedback-delay-1" for edge in data["wires"])
