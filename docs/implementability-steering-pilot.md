# Implementability Steering Pilot

## Status

This is the first empirical pilot for the Heller Consciousness Program.

The pilot tests whether model steering interventions move activations inside the model's natural activation envelope or push them into an out-of-distribution regime.

The experiment is designed as a small, falsifiable, Colah-shaped artifact: one conceptual move, one load-bearing figure, one structural test absent from standard steering reports.

## Conceptual move

A steering intervention should not be evaluated only by whether it changes downstream behavior. It should also be evaluated by whether the steered activation is implementable by the unsteered model under natural inputs.

If the steered activation lies on the natural activation manifold, steering selects a behavior the model could have produced. If it lies outside that manifold, steering produces a counterfactual behavior in an extrapolative activation regime.

## Formal object

Let `M` be a transformer model. Let `a_l,p(x)` denote the residual-stream activation at layer `l` and token position class `p` for natural input `x`.

Let `D` be a deployment-realistic natural input distribution. The natural activation set at layer `l` and position class `p` is:

```text
A_l,p(D) = { a_l,p(x) : x in D }
```

A steering intervention is a triple:

```text
(l, p, delta)
```

and produces the counterfactual activation:

```text
a'_l,p(x) = a_l,p(x) + delta
```

The implementability question is:

```text
Is a'_l,p(x) close to A_l,p(D) under a behaviorally relevant metric?
```

## Self-calibrating distance test

Build a nearest-neighbor index over natural activations from `A_l,p(D)`.

For each natural activation, compute its leave-one-out nearest-neighbor distance. This gives a baseline distribution of natural activation density:

```text
B_l,p = distribution of NN distances among natural activations
```

For each steered activation, compute its nearest-neighbor distance to the natural activation set:

```text
d_steer = min_y distance(a'_l,p(x), y), y in A_l,p(D)
```

Classify by baseline quantile:

- `d_steer <= q95(B_l,p)`: implementable / in-envelope;
- `d_steer >= q99(B_l,p)`: out-of-distribution;
- between `q95` and `q99`: boundary / ambiguous.

This avoids choosing an arbitrary epsilon. The natural activation cloud sets its own density scale.

## Metrics

Run the test under three metrics.

### 1. Euclidean after layer-normalization projection

The next block often consumes normalized activations. Compare normalized activations rather than raw residual norms.

Use when asking whether the next block sees the steered activation as geometrically familiar.

### 2. Cosine distance

Scale-invariant direction metric.

Use when asking whether the steering direction preserves representational orientation.

### 3. Readout-weighted metric

Weight activation differences by their effect on the next block's read-in matrices.

Use when asking whether two activations are functionally close even if geometrically different.

Report all three. Disagreement between metrics is evidence, not noise.

## Pilot target

The preferred open pilot target is an instruction-tuned open model with public feature catalogs or reproducible SAE support.

Candidate shape:

- model: Gemma-family instruction model or comparable open instruction model;
- feature source: public SAE catalog where available, otherwise local SAE training;
- behavior: refusal, redirect, or safety-controller feature steering;
- layer: mid-to-late residual stream, with position-conditioned baselines;
- task: harmful-pressure or refusal-sensitive evaluation where negative or positive steering has measurable effect.

The pilot does not depend on reproducing any proprietary Anthropic result exactly. It tests the structural question on the closest open analogue.

## Activation cache

Construct a deployment-realistic cache:

- pretraining-style text;
- chat/instruction formatted prompts;
- task-specific evaluation prompts without the pressure condition;
- optional minimal-information prompts for autonomous-behavior audit.

Cache activation vectors by:

- layer;
- position class: end-of-prompt, beginning-of-completion, mid-completion;
- source distribution;
- prompt metadata;
- model commit/checkpoint;
- tokenizer version.

Position conditioning is mandatory. End-of-prompt activations and mid-completion activations should not share the same nearest-neighbor baseline unless a sensitivity check justifies it.

## Controls

Run the same distance test for four controls.

1. **No intervention.** Should remain in-envelope.
2. **Random direction.** Calibrates generic perturbation OOD behavior.
3. **Alternative feature direction.** Tests whether feature-direction steering is generically more in-envelope than random steering.
4. **Natural teleportation.** Replace one activation with another natural activation from the cache. Should be implementable by construction.

If the controls do not behave as expected, the metric or cache is invalid.

## Magnitude sweep

For steering direction `v`, run magnitudes:

```text
alpha in {0, 0.25, 0.5, 1.0, 2.0, 4.0} * alpha_behavioral
```

where `alpha_behavioral` is the smallest magnitude at which the target behavioral effect is measurable.

The core output is a curve:

```text
x-axis: steering magnitude
 y-axis: nearest-neighbor distance quantile against B_l,p
```

Overlay:

- studied feature steering;
- random direction;
- alternative feature direction;
- no intervention;
- natural teleportation;
- q95 and q99 natural-density thresholds.

This figure is the proof-carrying artifact.

## Decision patterns

### Pattern A: in-envelope at behavioral magnitude

The target steering remains below the q95 threshold where it produces the behavioral effect.

Interpretation: steering selects a behavior the model could naturally produce. This strengthens steering methodology.

### Pattern B: boundary-crossing at behavioral magnitude

The target steering crosses q95 or q99 near the behavioral magnitude.

Interpretation: the behavioral effect is real, but partly achieved by moving into a low-density activation regime. Further safety analysis is required.

### Pattern C: OOD before behavioral effect

The target steering is OOD at magnitudes smaller than those needed for the behavioral effect.

Interpretation: the steering result is produced by an unnatural activation regime. The causal/mechanistic story needs revision.

## Pre-registered expectations

Record predictions before running the experiment.

Default expectations:

1. Target feature steering will be more in-envelope than random-direction steering at the same magnitude.
2. Target feature steering may cross the boundary near the magnitude where behavioral effect becomes strong.
3. Alternative feature steering will likely behave more like target feature steering than like random-direction steering.
4. If every curve is identical, the metric is not discriminating.
5. If everything is always OOD, the natural cache or position conditioning is wrong.

## Relation to Heller Consciousness doctrine

This pilot operationalizes implementability.

It treats a steering intervention as a candidate controlled behavior and asks whether that behavior belongs to the plant's reachable activation behavior under natural input.

This is the model-interpretability analogue of behavior-first learning: do not trust a representation merely because it is convenient. Test the behavior class it induces.

## Report artifact

The final technical report should be 6-8 pages and follow Colah transmission discipline:

- one conceptual move: steering requires an implementability test;
- one toy diagram: a natural activation cloud, a steered point, and density thresholds;
- one load-bearing empirical figure: magnitude-distance curves with controls;
- explicit uncertainty: metric choice, natural-distribution definition, position conditioning;
- dismissal named directly: "Isn't this just anomaly detection?" Answer: yes operationally, but applied as a behavior-theoretic implementability criterion for steering, which current steering reports do not supply.

## Definition of done

The pilot is complete when it produces:

1. reproducible model and feature selection notes;
2. activation-cache manifest;
3. nearest-neighbor baseline by layer and position class;
4. metric comparison results;
5. control curves;
6. steering magnitude curves;
7. implementability classification;
8. written report;
9. AgentPlane-compatible evidence bundle;
10. follow-on issue list for conservation-coupled SAEs, behavioral equivalence classes, designated-latent partitioning, and autonomous-behavior audits.
