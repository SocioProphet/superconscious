.PHONY: test smoke trust-surface artifact-validate canonicalize inspect validate m0-static m0-schema-fixtures m0-ci m1-5-static m1-5-schema-fixtures m1-5-ci tier2-binding-static tier2-binding-fixtures tier2-binding-ci m5-tier2-binding-static m5-tier2-binding-fixtures m5-tier2-binding-ci v1-1-static v1-1-fixtures v1-1-cross-field v1-1-ci m1-source-lock m1a-generate m1-verify-source-lock m1-verify-source-lock-strict m1-verify-weights m1-feature-stage1 m1-static m1-schema-fixtures m1b-cross-width-smoke m1-ci m2-static m2-schema-fixtures m2-ci m3-static m3-schema-fixtures m3-ci m5-static m5-schema-fixtures m5-template-set m5-ci certificate-ci

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
	python3 -m json.tool schemas/m1/common-certificate-additions.v1.1.json >/dev/null

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

m2-static:
	python3 -m json.tool schemas/m2/activation-cache.v1.json >/dev/null
	python3 -m json.tool schemas/m2/manifold-baseline.v1.json >/dev/null
	python3 -m json.tool schemas/m2/implementability-curve.v1.json >/dev/null
	python3 -m json.tool schemas/m2/implementability-certificate.v1.json >/dev/null

m2-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m2/activation-cache.v1.json tests/fixtures/m2/activation-cache.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m2/manifold-baseline.v1.json tests/fixtures/m2/manifold-baseline.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m2/implementability-curve.v1.json tests/fixtures/m2/implementability-curve.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m2/implementability-certificate.v1.json tests/fixtures/m2/implementability-certificate.synthetic.json

m2-ci: m2-static m2-schema-fixtures

m3-static:
	python3 -m json.tool schemas/m3/cross-layer-comparison.v1.json >/dev/null
	python3 -m json.tool schemas/m3/transcoder-evidence.v1.json >/dev/null
	python3 -m json.tool schemas/m3/robustness-certificate.v1.json >/dev/null

m3-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m3/cross-layer-comparison.v1.json tests/fixtures/m3/cross-layer-comparison.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m3/transcoder-evidence.v1.json tests/fixtures/m3/transcoder-evidence.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m3/robustness-certificate.v1.json tests/fixtures/m3/robustness-certificate.synthetic.json

m3-ci: m3-static m3-schema-fixtures

m5-static:
	python3 -m json.tool schemas/m5/public-note.v1.json >/dev/null

m5-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m5/public-note.v1.json tests/fixtures/m5/public-note.synthetic.json

m5-template-set:
	ls templates/m5/public-note-pattern-a-clean.md \
	   templates/m5/public-note-pattern-b-clean.md \
	   templates/m5/public-note-pattern-c-clean.md \
	   templates/m5/public-note-off-target-damage.md \
	   templates/m5/public-note-no-viable-feature.md >/dev/null

m5-ci: m5-static m5-schema-fixtures m5-template-set

m0-static:
	python3 -m json.tool schemas/m0/training-provenance.v1.json >/dev/null
	python3 -m json.tool schemas/m1/source-lock.v1.2.json >/dev/null

m0-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m0/training-provenance.v1.json tests/fixtures/m0/training-provenance.fully-certified.synthetic.json
	python3 scripts/check-m0.py tests/fixtures/m0/training-provenance.fully-certified.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m0/training-provenance.v1.json tests/fixtures/m0/training-provenance.external-artifact.synthetic.json
	python3 scripts/check-m0.py tests/fixtures/m0/training-provenance.external-artifact.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m1/source-lock.v1.2.json tests/fixtures/m1/source-lock.valid-provenance-ref.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/m1/source-lock.v1.2.json tests/fixtures/m1/source-lock.invalid-null-provenance.synthetic.json

m0-ci: m0-static m0-schema-fixtures

m1-5-static:
	python3 -m json.tool schemas/m1-5/attribution-graph.v1.json >/dev/null
	python3 -m json.tool schemas/m1/off-target-audit.v1.2.json >/dev/null
	python3 -m json.tool schemas/m1/implementability-certificate.v1.2.json >/dev/null

m1-5-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/m1-5/attribution-graph.v1.json tests/fixtures/m1-5/attribution-graph.bit-exact-replay.synthetic.json
	python3 scripts/check-m15.py tests/fixtures/m1-5/attribution-graph.bit-exact-replay.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m1-5/attribution-graph.v1.json tests/fixtures/m1-5/attribution-graph.manifest-matches-latent-diverges.synthetic.json
	python3 scripts/check-m15.py tests/fixtures/m1-5/attribution-graph.manifest-matches-latent-diverges.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m1-5/attribution-graph.v1.json tests/fixtures/m1-5/attribution-graph.manifest-diverges.synthetic.json
	python3 scripts/check-m15.py tests/fixtures/m1-5/attribution-graph.manifest-diverges.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/m1-5/attribution-graph.v1.json tests/fixtures/m1-5/attribution-graph.digest-rule.synthetic.json
	! python3 scripts/check-m15.py tests/fixtures/m1-5/attribution-graph.digest-rule.synthetic.json

m1-5-ci: m1-5-static m1-5-schema-fixtures

tier2-binding-static:
	python3 -m json.tool schemas/composition/m1-tier2-binding.v1.json >/dev/null

tier2-binding-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/composition/m1-tier2-binding.v1.json tests/fixtures/composition/m1-tier2-binding.synthetic.json
	python3 scripts/check-m1-tier2-binding.py tests/fixtures/composition/m1-tier2-binding.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/composition/m1-tier2-binding.v1.json tests/fixtures/composition/m1-tier2-binding.runtime-field.invalid.synthetic.json
	! python3 scripts/check-m1-tier2-binding.py tests/fixtures/composition/m1-tier2-binding.runtime-field.invalid.synthetic.json

tier2-binding-ci: tier2-binding-static tier2-binding-fixtures

m5-tier2-binding-static:
	python3 -m json.tool schemas/composition/m5-tier2-binding.v1.json >/dev/null

m5-tier2-binding-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/composition/m5-tier2-binding.v1.json tests/fixtures/composition/m5-tier2-binding.synthetic.json
	python3 scripts/check-m5-tier2-binding.py tests/fixtures/composition/m5-tier2-binding.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/composition/m5-tier2-binding.v1.json tests/fixtures/composition/m5-tier2-binding.runtime-field.invalid.synthetic.json
	! python3 scripts/check-m5-tier2-binding.py tests/fixtures/composition/m5-tier2-binding.runtime-field.invalid.synthetic.json

m5-tier2-binding-ci: m5-tier2-binding-static m5-tier2-binding-fixtures

v1-1-static:
	python3 -m json.tool schemas/pneumachinalis/microbeat-event.v1.1.json >/dev/null
	python3 -m json.tool schemas/pneumachinalis/mesobeat-intent.v1.1.json >/dev/null
	python3 -m json.tool schemas/pneumachinalis/macrobeat-commitment.v1.1.json >/dev/null
	python3 -m json.tool schemas/governance/redaction-cascade.v1.json >/dev/null

v1-1-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/pneumachinalis/microbeat-event.v1.1.json tests/fixtures/pneumachinalis/microbeat-event.human-with-consent.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/pneumachinalis/microbeat-event.v1.1.json tests/fixtures/pneumachinalis/microbeat-event.human-without-consent.invalid.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/governance/redaction-cascade.v1.json tests/fixtures/governance/redaction-cascade.full-rederivation.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/governance/redaction-cascade.v1.json tests/fixtures/governance/redaction-cascade.invalid-non-institutional-authority.synthetic.json

v1-1-cross-field:
	python3 scripts/check-v11-cross-field.py microbeat tests/fixtures/pneumachinalis/microbeat-event.human-with-consent.synthetic.json
	! python3 scripts/check-v11-cross-field.py microbeat tests/fixtures/pneumachinalis/microbeat-event.human-without-consent.invalid.synthetic.json
	python3 scripts/check-v11-cross-field.py cascade tests/fixtures/governance/redaction-cascade.full-rederivation.synthetic.json
	! python3 scripts/check-v11-cross-field.py cascade tests/fixtures/governance/redaction-cascade.invalid-non-institutional-authority.synthetic.json

v1-1-ci: v1-1-static v1-1-fixtures v1-1-cross-field

certificate-ci: m0-ci m1-ci m1-5-ci tier2-binding-ci m5-tier2-binding-ci m2-ci m3-ci m5-ci v1-1-ci
