.PHONY: test smoke trust-surface artifact-validate canonicalize inspect validate

test:
	python3 -m pytest

trust-surface:
	python3 scripts/validate-trust-surface.py .

smoke:
	python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json

artifact-validate:
	run_dir="$$(python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json)"; \
	python3 packages/superconscious-core/superconscious_core/validate_artifacts.py "$$run_dir"

canonicalize:
	run_dir="$$(python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json)"; \
	python3 packages/superconscious-core/superconscious_core/canonicalize_artifacts.py "$$run_dir"; \
	ls "$$run_dir"/reasoning-*.json "$$run_dir"/reasoning-events.sourceos.jsonl >/dev/null

inspect:
	run_dir="$$(python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json)"; \
	python3 packages/superconscious-core/superconscious_core/inspect_artifacts.py "$$run_dir"

validate: trust-surface test artifact-validate canonicalize inspect
