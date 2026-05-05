from pathlib import Path

from superconscious_core.inspect_artifacts import inspect_run_dir
from superconscious_core.runner import run


def test_inspector_renders_run_summary(tmp_path: Path) -> None:
    run_dir = run(Path("examples/basic-reasoning-run/task.json"), tmp_path)

    rendered = inspect_run_dir(run_dir)

    assert "Superconscious run:" in rendered
    assert "Safe trace: operational-trace-only / rawChainOfThought=not-collected" in rendered
    assert "Adapter decisions:" in rendered
    assert "Event timeline:" in rendered
    assert "reasoning.run.completed" in rendered
