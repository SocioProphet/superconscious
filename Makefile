.PHONY: test smoke trust-surface artifact-validate canonicalize inspect validate m1-source-lock m1a-generate m1-verify-source-lock m1-verify-source-lock-strict m1-verify-weights m1-feature-stage1

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

m1-source-lock:
	python3 -m src.m1.source_lock --write outputs/m1/source-lock.json --print

m1a-generate:
	python3 -m src.m1.generate_m1a_certificate

m1-verify-source-lock:
	python3 -m src.m1.verify_source_lock outputs/m1/certificates/m1a-source-lock.json --allow-pending

m1-verify-source-lock-strict:
	python3 -m src.m1.verify_source_lock outputs/m1/certificates/m1a-source-lock.json --strict

m1-verify-weights:
	python3 -m src.m1.verify_weights outputs/m1/certificates/m1a-source-lock.json

m1-feature-stage1:
	python3 -m src.m1.feature_selection --features data/m1/feature_contexts.jsonl --out-dir outputs/m1
