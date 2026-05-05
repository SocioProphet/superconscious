from pathlib import Path

from superconscious_core.canonicalize_artifacts import CANONICAL_ARTIFACTS, canonicalize
from superconscious_core.runner import run
from superconscious_core.validate_artifacts import load_json, load_jsonl


def test_canonicalization_emits_sourceos_reasoning_artifacts(tmp_path: Path) -> None:
    run_dir = run(Path("examples/basic-reasoning-run/task.json"), tmp_path)

    written = canonicalize(run_dir)

    assert {path.name for path in written} == set(CANONICAL_ARTIFACTS)
    for artifact in CANONICAL_ARTIFACTS:
        assert (run_dir / artifact).exists(), artifact

    canonical_run = load_json(run_dir / "reasoning-run.sourceos.json")
    assert canonical_run["type"] == "ReasoningRun"
    assert canonical_run["safeTrace"]["rawPrivateReasoning"] == "not-collected"
    assert canonical_run["eventRefs"]

    canonical_events = load_jsonl(run_dir / "reasoning-events.sourceos.jsonl")
    assert canonical_events[0]["type"] == "ReasoningEvent"
    assert canonical_events[0]["runRef"] == canonical_run["id"]

    canonical_receipt = load_json(run_dir / "reasoning-receipt.json")
    assert canonical_receipt["type"] == "ReasoningReceipt"
    assert canonical_receipt["runRef"] == canonical_run["id"]

    canonical_replay = load_json(run_dir / "reasoning-replay-plan.json")
    assert canonical_replay["type"] == "ReasoningReplayPlan"
    assert canonical_replay["replayClass"] == "exact"

    canonical_benchmark = load_json(run_dir / "reasoning-benchmark.json")
    assert canonical_benchmark["type"] == "ReasoningBenchmark"
    assert canonical_benchmark["passed"] is True
