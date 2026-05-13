include Makefile

.PHONY: interpretability-harness-tier2-binding-static interpretability-harness-tier2-binding-fixtures interpretability-harness-tier2-binding-ci

interpretability-harness-tier2-binding-static:
	python3 -m json.tool schemas/composition/interpretability-harness-tier2-binding.v1.json >/dev/null
	python3 -m json.tool tests/fixtures/composition/interpretability-harness-tier2-binding.synthetic.json >/dev/null
	python3 -m json.tool tests/fixtures/composition/interpretability-harness-tier2-binding.runtime-field.invalid.synthetic.json >/dev/null

interpretability-harness-tier2-binding-fixtures:
	python3 -m src.m1.validate_schema_instance schemas/composition/interpretability-harness-tier2-binding.v1.json tests/fixtures/composition/interpretability-harness-tier2-binding.synthetic.json
	! python3 -m src.m1.validate_schema_instance schemas/composition/interpretability-harness-tier2-binding.v1.json tests/fixtures/composition/interpretability-harness-tier2-binding.runtime-field.invalid.synthetic.json

interpretability-harness-tier2-binding-ci: interpretability-harness-tier2-binding-static interpretability-harness-tier2-binding-fixtures

certificate-ci: interpretability-harness-tier2-binding-ci
