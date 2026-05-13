# Neural Fabric Capture

**Status:** initial upstream capture.

**Scope:** Captures the Neural Fabric / lawful-learning substrate, structure, circuit, and activation-time targeting work as repo-native doctrine, reference code, schemas, fixtures, and CI checks.

This directory is the human-facing control plane for two work tracks:

1. **Model-family instantiation** — a unified mapping of the framework across transformer, Hopfield, SSM, MoE, CNN, RNN, diffusion, GNN, EBM, and tree/forest families.
2. **Activation-time targeting** — reproducible CPU-only simulations for steering vectors, SAE clamping, May-Wigner stability monitoring, heavy-tail SPRT probe cost, and Hopfield query injection.

The capture is deliberately evidence-disciplined. The experiments are marked `toy_model_confirmed`, not production-validated. Runtime promotion requires later open-weight transformer probes and governance review.

## Repo surfaces

```text
docs/neural-fabric/                         human doctrine and mapping docs
research/activation-time-targeting/         reference simulation suite and claim summaries
schemas/neural-fabric/                      JSON schemas for model families and targeting results
packages/superconscious-core/.../neural_fabric/ stable reference primitives
scripts/                                    invariant validators and capacity checks
tests/neural_fabric/                        smoke tests for core primitives and result invariants
mk/neural-fabric.mk                         local CI entrypoint
.github/workflows/neural-fabric.yml         GitHub Actions lane
```

## Epistemic boundary

The framework treats a neural network as a governed circuit fabric: substrate and structure are declared, mixture choices are trained, circuits are discovered post-training, and intervention/targeting is governed by audit events. That does not claim sentience, production safety, or universal interpretability. It gives us a disciplined architecture for measuring and governing activation-time control without retraining.

## CI entrypoint

```bash
make -f mk/neural-fabric.mk neural-fabric-ci
```

This validates schema syntax, compiles the reference package, checks committed reference result invariants, and runs smoke tests.
