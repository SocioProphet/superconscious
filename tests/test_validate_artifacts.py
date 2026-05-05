from pathlib import Path

from superconscious_core.runner import run
from superconscious_core.validate_artifacts import validate_run_dir


def test_artifact_validator_accepts_runner_output(tmp_path: Path) -> None:
    run_dir = run(Path("examples/basic-reasoning-run/task.json"), tmp_path)

    assert validate_run_dir(run_dir) == []


def test_artifact_validator_rejects_missing_required_artifact(tmp_path: Path) -> None:
    run_dir = run(Path("examples/basic-reasoning-run/task.json"), tmp_path)
    (run_dir / "agentplane-evidence.json").unlink()

    errors = validate_run_dir(run_dir)

    assert any("missing required artifact: agentplane-evidence.json" in error for error in errors)
