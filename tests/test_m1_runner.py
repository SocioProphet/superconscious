from pathlib import Path

from superconscious_core.runner import run


def test_basic_reasoning_run_emits_required_artifacts(tmp_path: Path) -> None:
    task_path = Path("examples/basic-reasoning-run/task.json")

    run_dir = run(task_path, tmp_path)

    required = [
        "events.jsonl",
        "reasoning-run.json",
        "agentplane-evidence.json",
        "replay-plan.json",
        "benchmark-result.json",
    ]
    for name in required:
        assert (run_dir / name).exists(), name

    benchmark = (run_dir / "benchmark-result.json").read_text(encoding="utf-8")
    assert '"passed": true' in benchmark

    reasoning_run = (run_dir / "reasoning-run.json").read_text(encoding="utf-8")
    assert '"rawChainOfThought": "not-collected"' in reasoning_run
