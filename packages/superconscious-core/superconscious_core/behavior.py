"""Deterministic behavior-calculus kernel for Superconscious.

The v0 kernel is intentionally small and inert. It models typed subprocesses as
pure deterministic transitions and provides serial, parallel, delayed-feedback,
and observation-projection helpers. It performs no network calls, model calls,
host mutation, policy admission, or durable memory promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


State = Mapping[str, Any]
Transition = Callable[[State, Any], tuple[Any, State]]
Projection = Callable[[Any], Any]


@dataclass(frozen=True)
class Proc:
    """A deterministic typed subprocess.

    A Proc implements the transition shape:

        step : S x I -> O x S

    `state_type`, `input_type`, and `output_type` are lightweight contract labels
    in v0. Schema-backed contract validation belongs to the JSON schema layer and
    later SourceOS contract promotion.
    """

    proc_id: str
    input_type: str
    output_type: str
    state_type: str
    step_fn: Transition

    def step(self, state: State, input_value: Any) -> tuple[Any, State]:
        output, next_state = self.step_fn(state, input_value)
        if not isinstance(next_state, Mapping):
            raise TypeError(f"{self.proc_id} returned non-mapping state")
        return output, next_state


def _state_key(proc: Proc) -> str:
    return proc.proc_id.replace(":", "_").replace("/", "_").replace(".", "_")


def serial(first: Proc, second: Proc, proc_id: str | None = None) -> Proc:
    """Compose two processes in sequence.

    The output of `first` becomes the input of `second`. Composite state is a
    product state stored under stable child keys.
    """

    if first.output_type != second.input_type:
        raise ValueError(
            f"serial type mismatch: {first.proc_id} outputs {first.output_type}, "
            f"but {second.proc_id} expects {second.input_type}"
        )

    first_key = _state_key(first)
    second_key = _state_key(second)
    composite_id = proc_id or f"{second.proc_id}_after_{first.proc_id}"

    def step(state: State, input_value: Any) -> tuple[Any, State]:
        first_state = state.get(first_key, {})
        second_state = state.get(second_key, {})
        middle, next_first_state = first.step(first_state, input_value)
        output, next_second_state = second.step(second_state, middle)
        return output, {first_key: next_first_state, second_key: next_second_state}

    return Proc(
        proc_id=composite_id,
        input_type=first.input_type,
        output_type=second.output_type,
        state_type=f"({first.state_type} x {second.state_type})",
        step_fn=step,
    )


def parallel(left: Proc, right: Proc, proc_id: str | None = None) -> Proc:
    """Run two processes side-by-side on paired inputs."""

    left_key = _state_key(left)
    right_key = _state_key(right)
    composite_id = proc_id or f"{left.proc_id}_tensor_{right.proc_id}"

    def step(state: State, input_value: Any) -> tuple[Any, State]:
        if not isinstance(input_value, tuple) or len(input_value) != 2:
            raise TypeError("parallel input must be a pair")
        left_input, right_input = input_value
        left_output, next_left_state = left.step(state.get(left_key, {}), left_input)
        right_output, next_right_state = right.step(state.get(right_key, {}), right_input)
        return (left_output, right_output), {left_key: next_left_state, right_key: next_right_state}

    return Proc(
        proc_id=composite_id,
        input_type=f"({left.input_type} x {right.input_type})",
        output_type=f"({left.output_type} x {right.output_type})",
        state_type=f"({left.state_type} x {right.state_type})",
        step_fn=step,
    )


def feedback_delay_1(
    proc: Proc,
    initial_feedback: Any,
    *,
    proc_id: str | None = None,
    input_type: str | None = None,
    output_type: str | None = None,
) -> Proc:
    """Close a one-tick delayed feedback loop around a process.

    The wrapped process receives `(external_input, previous_feedback)`. Its output
    is returned externally and also stored as the feedback value for the next tick.
    Same-tick unguarded recursion is intentionally unsupported in v0.
    """

    child_key = _state_key(proc)
    feedback_key = "feedback"
    composite_id = proc_id or f"feedback1_{proc.proc_id}"

    def step(state: State, input_value: Any) -> tuple[Any, State]:
        child_state = state.get(child_key, {})
        previous_feedback = state.get(feedback_key, initial_feedback)
        output, next_child_state = proc.step(child_state, (input_value, previous_feedback))
        return output, {child_key: next_child_state, feedback_key: output}

    return Proc(
        proc_id=composite_id,
        input_type=input_type or f"external({proc.input_type})",
        output_type=output_type or proc.output_type,
        state_type=f"({proc.state_type} x feedback)",
        step_fn=step,
    )


def project_observation(output: Any, projection: Projection | None = None) -> Any:
    """Apply an observation projection to a process output."""

    if projection is None:
        return output
    return projection(output)


def trace(proc: Proc, initial_state: State, inputs: list[Any]) -> tuple[list[Any], State]:
    """Run a process over a finite input stream and return outputs plus final state."""

    outputs: list[Any] = []
    state: State = initial_state
    for input_value in inputs:
        output, state = proc.step(state, input_value)
        outputs.append(output)
    return outputs, state


def trace_equivalent(
    left_outputs: list[Any],
    right_outputs: list[Any],
    projection: Projection | None = None,
) -> bool:
    """Return true when two finite traces match under the projection."""

    if len(left_outputs) != len(right_outputs):
        return False
    return [project_observation(item, projection) for item in left_outputs] == [
        project_observation(item, projection) for item in right_outputs
    ]
