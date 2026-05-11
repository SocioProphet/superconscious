.PHONY: test smoke trust-surface artifact-validate canonicalize inspect validate m1-source-lock m1a-generate m1-verify-source-lock m1-verify-source-lock-strict m1-verify-weights m1-feature-stage1 m1-static m1-schema-fixtures m1b-cross-width-smoke m1-ci

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

m1-static:
	python3 -m compileall src/m1
	python3 -m json.tool schemas/m1/source-lock.v1.json >/dev/null
	python3 -m json.tool schemas/m1/witness-card.v1.json >/dev/null
	python3 -m json.tool schemas/m1/causal-triad.v1.json >/dev/null
	python3 -m json.tool schemas/m1/off-target-audit.v1.json >/dev/null
	python3 -m json.tool schemas/m1/implementability-certificate.v1.json >/dev/null

m1-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m1/causal-triad.v1.json tests/fixtures/m1/causal-triad.valid.json
	python3 -m src.m1.validate_schema_instance schemas/m1/off-target-audit.v1.json tests/fixtures/m1/off-target-audit.valid.json
	python3 -m src.m1.validate_schema_instance schemas/m1/implementability-certificate.v1.json tests/fixtures/m1/implementability-certificate.valid.json

m1b-cross-width-smoke:
	python3 -m src.m1.witness_card_cross_width \
		--primary-summaries tests/fixtures/m1/primary_summaries.jsonl \
		--witness-summaries tests/fixtures/m1/witness_summaries.jsonl \
		--feature-index 7 \
		--test-set-ref tests/fixtures/m1/test_set_ref.json \
		--out outputs/m1/ci/cross_width_equivalence.json
	python3 -m json.tool outputs/m1/ci/cross_width_equivalence.json >/dev/null

m1-ci: m1-static m1-schema-fixtures m1b-cross-width-smoke
