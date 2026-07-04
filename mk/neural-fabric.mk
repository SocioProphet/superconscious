.PHONY: neural-fabric-static neural-fabric-smoke neural-fabric-ci neural-fabric-full

neural-fabric-static:
	python3 -m json.tool schemas/neural-fabric/model-family.v1.json >/dev/null
	python3 -m json.tool schemas/neural-fabric/targeting-experiment.v1.json >/dev/null
	python3 -m json.tool schemas/neural-fabric/targeting-result.v1.json >/dev/null
	python3 -m compileall packages/superconscious-core/superconscious_core/neural_fabric scripts research/activation-time-targeting/code >/dev/null

# NOTE: neural-fabric-smoke / neural-fabric-full depend on the results-validation
# and experiment-harness that are not yet committed (scripts/validate-neural-fabric-results.py,
# scripts/check-capacity-bounds.py, tests/neural_fabric, research/.../run_suite.py). They are
# kept here as the roadmap for that harness and are intentionally NOT part of neural-fabric-ci
# until those files land, so CI gates only what this module actually delivers.
neural-fabric-smoke:
	python3 scripts/validate-neural-fabric-results.py research/activation-time-targeting
	python3 scripts/check-capacity-bounds.py --m 60 --C 0.4 --s 0.1
	python3 -m pytest tests/neural_fabric -q

neural-fabric-full:
	python3 research/activation-time-targeting/code/run_suite.py --out research/activation-time-targeting/results/generated
	python3 scripts/validate-neural-fabric-results.py research/activation-time-targeting

neural-fabric-ci: neural-fabric-static
