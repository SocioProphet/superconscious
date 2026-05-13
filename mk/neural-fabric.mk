.PHONY: neural-fabric-static neural-fabric-smoke neural-fabric-ci neural-fabric-full

neural-fabric-static:
	python3 -m json.tool schemas/neural-fabric/model-family.v1.json >/dev/null
	python3 -m json.tool schemas/neural-fabric/targeting-experiment.v1.json >/dev/null
	python3 -m json.tool schemas/neural-fabric/targeting-result.v1.json >/dev/null
	python3 -m json.tool schemas/neural-fabric/intervention-event.v1.json >/dev/null
	python3 -m compileall packages/superconscious-core/superconscious_core/neural_fabric scripts research/activation-time-targeting/code >/dev/null

neural-fabric-smoke:
	python3 scripts/validate-neural-fabric-results.py research/activation-time-targeting
	python3 scripts/check-capacity-bounds.py --m 60 --C 0.4 --s 0.1
	python3 -m pytest tests/neural_fabric -q

neural-fabric-full:
	python3 research/activation-time-targeting/code/run_suite.py --out research/activation-time-targeting/results/generated
	python3 scripts/validate-neural-fabric-results.py research/activation-time-targeting

neural-fabric-ci: neural-fabric-static neural-fabric-smoke
