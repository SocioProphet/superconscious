include Makefile

.PHONY: interpretability-harness-tier2-binding-static interpretability-harness-tier2-binding-fixtures interpretability-harness-tier2-binding-ci interpretability-harness-static interpretability-harness-schema-fixtures interpretability-harness-cross-field interpretability-harness-ci

interpretability-harness-tier2-binding-static:
	python3 -m json.tool schemas/composition/interpretability-harness-tier2-binding.v1.json >/dev/null
	python3 -m json.tool tests/fixtures/composition/interpretability-harness-tier2-binding.synthetic.json >/dev/null
	python3 -m json.tool tests/fixtures/composition/interpretability-harness-tier2-binding.runtime-field.invalid.synthetic.json >/dev/null

interpretability-harness-tier2-binding-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/composition/interpretability-harness-tier2-binding.v1.json tests/fixtures/composition/interpretability-harness-tier2-binding.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/composition/interpretability-harness-tier2-binding.v1.json tests/fixtures/composition/interpretability-harness-tier2-binding.runtime-field.invalid.synthetic.json

interpretability-harness-tier2-binding-ci: interpretability-harness-tier2-binding-static interpretability-harness-tier2-binding-fixtures

interpretability-harness-static:
	python3 -m json.tool schemas/interpretability/provider-binding.v0.json >/dev/null
	python3 -m json.tool schemas/interpretability/artifact-source-lock.v0.json >/dev/null
	python3 -m json.tool schemas/interpretability/feature-registry-entry.v0.json >/dev/null
	python3 -m json.tool schemas/interpretability/intervention-spec.v0.json >/dev/null
	python3 -m py_compile scripts/check-interpretability-harness.py

interpretability-harness-schema-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/interpretability/provider-binding.v0.json tests/fixtures/interpretability/provider-binding.gemma-white-box.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/provider-binding.v0.json tests/fixtures/interpretability/provider-binding.gemini-api-black-box.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/provider-binding.v0.json tests/fixtures/interpretability/provider-binding.neuronpedia-feature-registry.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/interpretability/provider-binding.v0.json tests/fixtures/interpretability/provider-binding.black-box-hidden-state.invalid.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/artifact-source-lock.v0.json tests/fixtures/interpretability/artifact-source-lock.gemma-model.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/artifact-source-lock.v0.json tests/fixtures/interpretability/artifact-source-lock.gemma-scope-sae.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/artifact-source-lock.v0.json tests/fixtures/interpretability/artifact-source-lock.neuronpedia-feature.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/artifact-source-lock.v0.json tests/fixtures/interpretability/artifact-source-lock.gemma-activation-cache.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/feature-registry-entry.v0.json tests/fixtures/interpretability/feature-registry-entry.neuronpedia.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/intervention-spec.v0.json tests/fixtures/interpretability/intervention-spec.feature-steering.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/intervention-spec.v0.json tests/fixtures/interpretability/intervention-spec.activation-patching.synthetic.json
	python3 -m src.m1.validate_schema_instance schemas/interpretability/intervention-spec.v0.json tests/fixtures/interpretability/intervention-spec.prompt-only-black-box.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/interpretability/intervention-spec.v0.json tests/fixtures/interpretability/intervention-spec.feature-steering-missing-source-lock.invalid.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/interpretability/intervention-spec.v0.json tests/fixtures/interpretability/intervention-spec.neuronpedia-registry-steering.invalid.synthetic.json

interpretability-harness-cross-field:
	python3 scripts/check-interpretability-harness.py tests/fixtures/interpretability

interpretability-harness-ci: interpretability-harness-static interpretability-harness-schema-fixtures interpretability-harness-cross-field

certificate-ci: interpretability-harness-tier2-binding-ci interpretability-harness-ci
