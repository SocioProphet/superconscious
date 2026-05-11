# Implementability Steering Pilot

## Status

This is the first empirical pilot for the Heller Consciousness Program.

The pilot tests whether model steering interventions move activations inside the model's natural activation envelope or push them into an out-of-distribution regime.

The experiment is designed as a small, falsifiable, Colah-shaped artifact: one conceptual move, one load-bearing figure, one structural test absent from standard steering reports.

## Decision

The next concrete step is **not** to build the full manifold-distance analysis first.

The next concrete step is to reproduce one open-model steering effect with public infrastructure, then run the implementability test against that reproduced effect.

The preferred pilot target is Gemma 2 9B instruction-tuned with Gemma Scope residual-stream sparse autoencoders. This gives an open analogue of proprietary refusal/redirect steering claims without depending on inaccessible Anthropic models or private crosscoders.

## 1. Formal definition

Let $M$ be a transformer with residual-stream dimension $d_{\mathrm{model}}$.

Let

$$
a_{\ell,t}(x) \in \mathbb{R}^{d_{\mathrm{model}}}
$$

denote the layer-$\ell$ residual-stream activation at token position $t$ for input $x$.

Let $D$ denote a natural input distribution. For this pilot, natural means deployment-realistic: a mixture of pretraining-style text, instruction/chat-format examples, and task-near evaluation prompts. It is intentionally not only pretraining text and not only chat data.

Define the natural activation set at layer $\ell$ as

$$
\mathcal{A}_{\ell}(D) = \{ a_{\ell,t}(x) : x \sim D,\ t \in T(x) \}.
$$

When position class matters, use

$$
\mathcal{A}_{\ell,p}(D) = \{ a_{\ell,t}(x) : x \sim D,\ t \in T_p(x) \},
$$

where $p$ is a position class such as end-of-prompt, beginning-of-completion, or mid-completion.

A steering intervention is a triple

$$
I = (\ell, t, \delta),
$$

where $\ell$ is the target layer, $t$ is the target token position, and $\delta \in \mathbb{R}^{d_{\mathrm{model}}}$ is an additive steering vector.

It produces the counterfactual activation

$$
a'_{\ell,t}(x) = a_{\ell,t}(x) + \delta,
$$

which is then propagated through the remaining model.

### Implementability test

The intervention is implementable if $a'_{\ell,t}(x)$ lies within the natural activation manifold $\mathcal{A}_{\ell,p}(D)$ at the resolution of the metric we care about.

Equivalently: some natural input would produce an activation indistinguishable from the steered activation at the relevant layer, position class, and metric resolution.

Operationally, sample natural activations

$$
\{z_i\}_{i=1}^{N} \subset \mathcal{A}_{\ell,p}(D).
$$

For a metric $\rho$, define the intervention distance

$$
d_{\mathrm{steer}}(a') = \min_{1 \leq i \leq N} \rho(a', z_i).
$$

Define the natural baseline distribution $B_{\ell,p}^{\rho}$ by computing, for each natural activation $z_i$, the leave-one-out nearest-neighbor distance

$$
d_i^{\mathrm{LOO}} = \min_{j \neq i} \rho(z_i, z_j),
$$

and taking the empirical distribution of $\{d_i^{\mathrm{LOO}}\}_{i=1}^{N}$.

Classify the intervention by where $d_{\mathrm{steer}}$ falls in $B_{\ell,p}^{\rho}$:

- $d_{\mathrm{steer}} \leq q_{95}(B_{\ell,p}^{\rho})$: implementable / in-envelope.
- $d_{\mathrm{steer}} \geq q_{99}(B_{\ell,p}^{\rho})$: out-of-distribution.
- $q_{95}(B_{\ell,p}^{\rho}) < d_{\mathrm{steer}} < q_{99}(B_{\ell,p}^{\rho})$: boundary / ambiguous.

This is one-class anomaly detection with a self-calibrating threshold. It does not require choosing an arbitrary $\epsilon$ in advance. The natural activation cloud sets its own scale.

## 2. Metric choice

Run the test under three metrics. Each metric captures a different aspect of activation-manifold structure.

### 2.1 Euclidean after layer-norm projection

Transformers often apply layer normalization before the next block consumes the residual stream. Two activations with different raw residual norms may be downstream-close if their normalized forms are similar.

Let $\mathrm{LN}_{\ell}$ denote the layer norm preceding the next block. Define

$$
\rho_{\mathrm{LN2}}(u,v) = \left\| \mathrm{LN}_{\ell}(u) - \mathrm{LN}_{\ell}(v) \right\|_2.
$$

Use this metric when asking whether the next block sees the steered activation as geometrically familiar.

### 2.2 Cosine distance

Define

$$
\rho_{\cos}(u,v) = 1 - \frac{\langle u,v \rangle}{\|u\|_2\|v\|_2}.
$$

Use this metric when asking whether the steering preserves representational direction while ignoring scale.

### 2.3 Readout-weighted Mahalanobis distance

Activations matter downstream through how they project into the next block's read-in maps.

Let $R_{\ell+1}$ be the concatenated read-in operator for the next block: attention QKV projections plus MLP input projection, or the closest architecture-specific equivalent.

Define

$$
\rho_{R}(u,v)^2 = (u-v)^\top R_{\ell+1}^{\top}R_{\ell+1}(u-v).
$$

This is behaviorally relevant: two activations that read out identically into the next block are functionally close even if raw geometry differs.

Run all three metrics. Agreement is strong evidence. Disagreement is itself diagnostic.

If an intervention is implementable under $\rho_R$ but OOD under $\rho_{\mathrm{LN2}}$, the steered activation is geometrically unusual but functionally normal. If it is geometrically typical but functionally unusual under $\rho_R$, that is the more concerning case.

## 3. Pilot target

The proprietary Anthropic refusal/redirect steering case is treated as a motivating analogy, not as an implementation dependency.

The open pilot target is:

- model: Gemma 2 9B instruction-tuned, or the closest currently practical Gemma-family instruction model;
- feature source: Gemma Scope residual-stream SAE where available;
- candidate layers: layers 9, 20, and 31 for Gemma 2 9B-IT residual SAEs, with layer 20 as the preferred initial target;
- intervention: refusal, redirect, or safety-controller feature steering;
- behavior: negative or positive steering that measurably changes refusal-sensitive or harm-pressure multiple-choice behavior.

The headline question:

> Does the behavioral effect require pushing activations out of the natural envelope, or can it be achieved with in-envelope steering?

If the result is in-envelope, the steering literature gains a structural validation test. If it is OOD, we have found a structural caveat that ordinary behavioral scoring does not surface.

Either result is useful.

## 4. Experimental design

### 4.1 Activation cache

Sample $N$ inputs from a deployment-realistic mixture:

- 50% pretraining-style text;
- 30% instruction/chat-format completions;
- 20% task-near refusal-sensitive or harm-pressure multiple-choice prompts without the pressure condition.

Forward-pass each input. For each layer under test, save residual-stream activations at three position classes:

1. end-of-prompt;
2. beginning-of-completion;
3. mid-completion.

The cache must record:

- model identifier and checkpoint;
- tokenizer identifier;
- layer;
- position class;
- source-distribution tag;
- prompt identifier;
- activation dtype and shape;
- extraction code commit;
- random seed;
- any safety/filtering exclusions.

The cache scales linearly in number of layers and position classes. It should be reusable across all subsequent intervention tests on the same model.

### 4.2 FAISS or equivalent nearest-neighbor index

Build an approximate nearest-neighbor index over each layer/position/metric view of the cache.

The default index class is HNSW or another high-recall approximate nearest-neighbor structure. Exact search is acceptable for small pilot caches and should be used to validate approximate-search error on a subset.

The project should not reimplement nearest-neighbor search.

### 4.3 Steering parameter sweep

Let the steering direction be $v$ and steering magnitude be $\alpha$:

$$
\delta(\alpha) = \alpha v.
$$

Let $\alpha_{\mathrm{behavioral}}$ be the smallest magnitude that produces a measurable behavioral effect in the reproduction run.

Run the implementability test for

$$
\alpha \in \{0, 0.25, 0.5, 1.0, 2.0, 4.0\}\alpha_{\mathrm{behavioral}}.
$$

The core curve is

$$
\alpha \mapsto \mathrm{Quantile}_{B_{\ell,p}^{\rho}}(d_{\mathrm{steer}}(\alpha)).
$$

Overlay the $q_{95}$ and $q_{99}$ thresholds of the natural baseline.

### 4.4 Controls

Run four controls under identical extraction, indexing, metric, and position-conditioning rules.

1. **No intervention.** $\delta=0$. This should test as in-envelope.
2. **Random direction.** $\delta=\alpha r$, where $r$ is a random unit vector. This calibrates generic perturbation OOD behavior.
3. **Alternative-feature steering.** $\delta=\alpha v_{\mathrm{alt}}$, where $v_{\mathrm{alt}}$ is a decoder direction for a non-target feature with comparable activation statistics. This tests whether feature-direction steering is generically in-envelope or whether the studied feature is special.
4. **Natural teleportation.** Replace an activation with another natural activation from the cache. This should be implementable by construction. If teleportation does not read as in-envelope, the metric or index is broken.

### 4.5 Deliverable plot

The proof-carrying figure has five curves:

- studied feature steering;
- random direction;
- alternative-feature steering;
- no intervention;
- natural teleportation.

The x-axis is steering magnitude. The y-axis is distance quantile against the natural baseline. The $q_{95}$ and $q_{99}$ thresholds are shaded.

The figure tells us at what magnitude each intervention type leaves the natural envelope.

## 5. Decision rule

### Pattern A: in-envelope across the behavioral range

The studied steering remains below $q_{95}$ at the magnitude where it produces the behavioral effect. The random-direction control crosses the threshold at a smaller magnitude.

Interpretation: the studied feature is behaviorally efficient. Small movement along this direction has large behavioral effect while staying natural. Steering selects a behavior the model could have produced.

### Pattern B: boundary-crossing at the behavioral magnitude

The studied steering crosses $q_{95}$ or $q_{99}$ near the magnitude required for the behavioral effect.

Interpretation: the behavioral effect is real, but partly achieved by pushing the model into a low-density activation regime. The safety properties of that regime require further analysis.

### Pattern C: OOD throughout the behavioral range

The studied steering is OOD at magnitudes smaller than those required for the behavioral effect.

Interpretation: feature steering in this case produces a non-natural activation regime. The mechanistic story must be revised: the model under steering is not doing the same thing it does when the feature naturally activates.

Pattern A confirms and extends feature-steering methodology. Pattern B complicates it. Pattern C contradicts the simplest feature-steering interpretation and is the highest-information outcome.

## 6. Compute budget

Initial planning target:

- activation cache: one to three layers; batch extraction on a single accelerator where available;
- index build: minutes per layer/position class for pilot scale;
- intervention testing: cheap after the cache and index exist;
- steering reproduction: the dominant engineering task, because the target feature and effective magnitude must be found before implementability analysis matters.

The pilot should not start by optimizing manifold-distance code. It starts by proving we can reproduce a behavioral steering effect on the chosen open model and feature source.

## 7. Connection to the learning manuscript

The LLM implementability test is the operational analogue of the implementability proposition for the gated constraint-learning manuscript.

For the manuscript-side system:

- $\mathcal{B}_{0}$ is the predictive behavior of the unconstrained model;
- $\mathcal{B}_{1}$ is the predictive behavior with all constraints binding everywhere;
- $\mathcal{B}_{\theta}$ is the predictive behavior of the gated model under gate parameters $\theta$;
- a target behavior $\mathcal{B}_{\star}$ is admissible only if it lies in the reachable behavior interval defined by the representation and constraints.

The regularizer's role is to select a useful interior point or equivalence class, not to create behavior outside the feasible envelope.

The LLM pilot gives the same structural test in another substrate:

- $\mathcal{A}_{\ell,p}(D)$ is the plant's reachable activation behavior;
- $a'_{\ell,t}(x)$ is a candidate controlled behavior;
- implementability asks whether $a'_{\ell,t}(x) \in \mathcal{A}_{\ell,p}(D)$ up to metric resolution.

This gives the Heller Consciousness Program two distinct instances of the same principle: spectral shape-constrained learning and LLM steering.

## 8. Open implementation choices

### 8.1 Distance weighting across layers

Default: report per-layer results separately with no cross-layer weighting.

Reason: cross-layer weighting adds assumptions about downstream amplification. If results are confusing, add an operator-norm or readout-sensitivity analysis later.

### 8.2 Position conditioning

Default: condition the natural baseline by position class.

End-of-prompt, beginning-of-completion, and mid-completion activations are statistically different. A mixed baseline may hide OOD behavior or create false positives.

### 8.3 Intrinsic dimension correction

Default: estimate intrinsic dimension with PCA spectral-knee diagnostics and report both raw and normalized distances.

Do not use intrinsic dimension correction as the primary decision rule in the first pilot. Use it as an interpretive diagnostic.

### 8.4 Multiple-feature steering

Default: single-feature steering only.

Multi-feature steering is a follow-up because controls and equivalence classes multiply.

### 8.5 Natural-distribution definition

Default: deployment-realistic mixture.

Sensitivity check: broader pretraining-only or pretraining-heavy distribution.

The stricter the natural distribution, the smaller the activation manifold and the more interventions will classify as OOD. This is not a bug; it is part of what the test measures.

## 9. Pre-registration

Before running the experiment, record predictions.

Default predictions:

1. Studied refusal/safety feature steering will likely be Pattern B: boundary-crossing near the behavioral magnitude.
2. Random-direction steering will cross the OOD threshold at a smaller magnitude than feature-direction steering.
3. Alternative-feature steering will look more like target-feature steering than random-direction steering.
4. If all interventions look identical and in-envelope, the metric is not discriminating.
5. If all interventions look identical and OOD, the natural baseline or position conditioning is wrong.

The key value of pre-registration is not prediction theater. It is diagnostic discipline. The experiment should be capable of surprising us.

## 10. Report artifact

The final technical report should be 6-8 pages.

It should follow Colah transmission discipline:

- one conceptual move: steering requires an implementability test;
- one toy diagram: natural activation cloud, steered point, and density threshold;
- one load-bearing empirical figure: magnitude-distance curves with controls;
- explicit uncertainty markers: metric choice, natural-distribution definition, position conditioning, approximate-nearest-neighbor error;
- dismissal named directly: "Is this just anomaly detection?" Answer: operationally yes, but applied as a behavior-theoretic implementability criterion for steering, which ordinary steering reports do not supply.

## 11. Engineering sequence

### M0: Source lock

- Verify available model weights, license, tokenizer, and SAE release identifiers.
- Verify the target layers and release names.
- Record exact external artifact versions before writing analysis claims.

### M1: Reproduce one steering effect

- Select candidate refusal/safety feature.
- Validate top-activating contexts.
- Run refusal-sensitive or harm-pressure multiple-choice evaluation.
- Sweep steering magnitude.
- Identify $\alpha_{\mathrm{behavioral}}$.

Exit criterion: a measurable behavioral effect under steering.

### M2: Activation cache and natural baseline

- Build layer/position-conditioned activation cache.
- Build nearest-neighbor baselines.
- Validate no-intervention and teleportation controls.

Exit criterion: controls behave as expected.

### M3: Implementability curves

- Run target feature, random direction, and alternative-feature sweeps.
- Produce metric-specific curves.
- Classify Pattern A/B/C.

Exit criterion: implementability classification under all three metrics.

### M4: Report and evidence bundle

- Write 6-8 page technical report.
- Emit AgentPlane-compatible evidence bundle.
- Open follow-on issues for conservation-coupled SAEs, behavioral equivalence classes, designated-latent partitioning, autonomous-behavior audit, and activation-field patchability.

## Definition of done

The pilot is complete when it produces:

1. reproducible model and feature selection notes;
2. activation-cache manifest;
3. nearest-neighbor baseline by layer and position class;
4. metric comparison results;
5. control curves;
6. steering magnitude curves;
7. implementability classification;
8. written technical report;
9. AgentPlane-compatible evidence bundle;
10. follow-on issue list for the next interpretability reforms.
