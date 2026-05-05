.PHONY: test smoke validate

test:
	python3 -m pytest

smoke:
	python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json

validate: test smoke
