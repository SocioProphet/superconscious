# Advanced Implementability Roadmap

## Status

This document upgrades the Implementability Steering Pilot from a one-off steering reproduction into a certificate pipeline for behavior-first interpretability.

The current M1 lane is intentionally conservative: source-lock Gemma/Gemma-Scope artifacts, identify a candidate refusal/safety feature, reproduce a measurable steering effect, and stop before making implementability-distance claims.

The advanced lane keeps that discipline but raises the ceiling. The target is an implementability certificate: a replayable statement that a controlled activation behavior is inside, outside, or on the boundary of the model's reachable activation envelope under declared data, metric, and intervention assumptions.

## Upgrade principle

The pilot should not ask only:

```text
Does steering change model behavior?
```

It should ask:

```text
Is the changed behavior reachable by the unsteered plant under natural inputs, under behaviorally relevant metrics, with calibrated uncertainty and causal controls?
```

This turns steering from an intervention trick into a governed behavior test.

## Upgrade 1: Source-lock becomes a certificate preamble

M1 already records model, SAE, layer, width, L0, revision, dtype, position classes, and safety boundary.

Advanced source-lock should add:

- resolved model and SAE commit SHAs;
- model-card and license hash references;
- tokenizer chat-template hash;
- SAE parameter-file hash after download;
- feature-dashboard / Neuronpedia export hash when used;
- exact prompt-set hash;
- exact evaluation script hash;
- hardware and numerical precision record;
- random seed ledger;
- generated artifact manifest.

Output target:

```text
outputs/m1/source-lock.json
outputs/m1/source-lock.sha256
outputs/m1/artifact-manifest.json
```

## Upgrade 2: Feature selection becomes multi-witness, not label-driven

The current Stage-1 funnel correctly treats generated descriptions as weak evidence. The advanced protocol requires four independent witnesses before a feature becomes the pilot target:

1. **Context witness.** Top-activating examples contain refusal, redirect, harm-detection, or policy-meta text.
2. **Activation witness.** The feature activates differentially on refusal/safety prompts versus benign prompts.
3. **Causal witness.** Ablation or steering produces a measurable behavioral change.
4. **Family witness.** Manual inspection places the feature into a typed family: harm-detection, refuse-and-redirect, policy-meta, correct-answer/task-completion, or ambiguous.

A feature is not selected by description. It is selected by convergence across witnesses.

Advanced output target:

```text
outputs/m1/feature-witness-card.json
outputs/m1/feature-family-table.md
outputs/m1/eliminated-candidates.jsonl
```

## Upgrade 3: Use behavioral equivalence classes as the analytic primitive

A single SAE feature direction is not canonical. The advanced lane should group features by downstream behavioral effect.

Procedure:

1. Select candidate features across at least two SAE settings where available: same layer but different width/L0, or nearby layers.
2. Run the same ablation/steering probes on each candidate.
3. Represent each feature by an effect vector over prompts and metrics.
4. Cluster effect vectors.
5. Treat clusters as behavioral equivalence classes.

This answers whether the target is a real refusal-controller behavior or an artifact of one dictionary.

Output target:

```text
outputs/m1/behavioral-equivalence-classes.json
outputs/m1/effect-vector-matrix.parquet
```

## Upgrade 4: Natural activation manifold gets conformal calibration

The current plan uses leave-one-out nearest-neighbor distances and q95/q99 thresholds.

Advanced calibration should split the natural activation cache into:

- reference set: builds the nearest-neighbor index;
- calibration set: estimates quantiles;
- test set: evaluates intervention distances.

This creates a conformal-style finite-sample calibration discipline. The result is not merely a heuristic nearest-neighbor anomaly score; it becomes an empirical coverage statement under the declared exchangeability assumption.

Output target:

```text
outputs/m2/natural-baseline-reference.manifest.json
outputs/m2/natural-baseline-calibration.json
outputs/m2/coverage-report.json
```

## Upgrade 5: Metric stack becomes geometric, functional, and behavioral

Current metrics:

- layernorm Euclidean;
- cosine;
- readout-weighted metric.

Advanced metrics:

1. **Layernorm Euclidean.** Geometry seen by the next normalized block.
2. **Cosine.** Directional representational similarity.
3. **Readout-weighted metric.** Functional closeness under the next block's read-in maps.
4. **Jacobian-weighted local metric.** Local downstream sensitivity of logits or task loss to activation perturbation.
5. **Logit-effect metric.** Distance between downstream logit deltas induced by two activations.
6. **Feature-coordinate metric.** Distance after encoding through the SAE, to check whether raw activation closeness agrees with sparse-feature closeness.

The advanced certificate should report agreement/disagreement across metric families.

Interpretation rule:

- geometrically OOD but functionally in-envelope: unusual representation, possibly benign;
- geometrically in-envelope but functionally OOD: high-priority warning;
- feature-coordinate in-envelope but raw/functionally OOD: SAE artifact suspicion;
- all metrics OOD: strong evidence of unnatural steering regime.

## Upgrade 6: Causal validation becomes triadic

Do not rely only on steering.

For the selected feature or behavioral-equivalence class, run:

1. **Ablation.** Clamp feature to zero and measure refusal/compliance/task impact.
2. **Positive steering.** Increase the feature and measure refusal or redirect strengthening.
3. **Negative steering.** Decrease the feature and measure recovery of task answering or reduction of refusal.

A true controller feature should show coherent directionality across all three tests.

Output target:

```text
outputs/m1/causal-triad-results.jsonl
outputs/m1/causal-triad-summary.md
```

## Upgrade 7: Add off-target and capability-preservation audits

A steering effect is not acceptable if it restores one target behavior while damaging unrelated capabilities.

Add side evaluations:

- benign QA accuracy;
- harmless refusal-sensitive prompts;
- format-following;
- calibration / confidence proxy;
- toxicity / policy overcorrection check;
- repetition / degeneration check.

Report:

```text
behavior_gain / off_target_damage
```

This prevents the pilot from rewarding blunt perturbations.

## Upgrade 8: Add designated-latent partitioning

SAE residual error is not garbage. Track it.

For every intervention, record:

- SAE reconstructed component;
- SAE residual component;
- residual norm;
- layernorm scale statistics;
- positional component proxy;
- change in these quantities under steering.

If behavioral recovery depends on a large shift in SAE residual or norm dynamics, the feature explanation is incomplete.

Output target:

```text
outputs/m2/designated-latent-report.json
```

## Upgrade 9: Add controller specification before interpretation

Before mechanistic analysis, define the refusal/safety behavior as a controller.

Controller specification fields:

- plant behavior being restricted;
- manifest control variables;
- latent control variables;
- admissible activation conditions;
- admissible refusal conditions;
- admissible non-refusal conditions;
- failure modes: under-refusal, over-refusal, irrelevant refusal, format corruption, capability damage;
- implementability bounds.

This converts the analysis from feature hunting into controller verification.

Output target:

```text
docs/m1-controller-spec.md
outputs/m1/controller-spec-checklist.json
```

## Upgrade 10: Add activation-field patchability

A feature that activates in one prompt may be brittle under context extension.

Patchability test:

1. Take contexts where the target feature activates.
2. Embed them in prefix/suffix variants.
3. Measure whether activation persists, vanishes, or changes family.
4. Classify feature as globally patchable, locally patchable, or brittle.

Patchability is the field-theoretic version of implementability: can the local activation slice extend to a globally consistent context field?

Output target:

```text
outputs/m3/patchability-profile.json
```

## Upgrade 11: Add conservation-coupled or cross-layer follow-up

Single-layer residual SAEs are a starting point. They are not the endpoint.

Advanced follow-up:

- compare layer 9, 20, 31 features;
- test whether the same behavioral class appears across layers;
- use transcoders or crosscoders where available;
- check whether steering at one layer creates coherent downstream feature changes;
- test whether feature effects compose with the residual stream update equation.

This moves from feature-level steering to typed interconnection over model layers.

## Upgrade 12: Add Colah-shaped public note

The public artifact should not be a manifesto.

Write one note with one conceptual move:

> Feature steering needs an implementability test.

The note should include:

- one toy 2D activation cloud;
- one real Gemma/Gemma-Scope steering curve;
- one control comparison;
- one explicit limitation section;
- one statement of what the test does not prove.

## Advanced issue sequence

Recommended follow-on issues:

1. **M1A: Source-lock certificate hardening.** Add hashes, model-card references, tokenizer-template hash, artifact manifest.
2. **M1B: Feature witness cards.** Produce multi-witness selection records and eliminated-candidate controls.
3. **M1C: Causal triad.** Run ablation, positive steering, and negative steering on selected candidate.
4. **M1D: Off-target audit.** Add benign QA and format/capability preservation checks.
5. **M2A: Conformal natural-baseline split.** Reference/calibration/test split for activation manifold distance.
6. **M2B: Metric stack expansion.** Add Jacobian/logit-effect/feature-coordinate metrics.
7. **M2C: Designated latent report.** Track SAE residuals, norm dynamics, and layernorm scale.
8. **M3A: Behavioral equivalence classes.** Cluster features by intervention effect vectors.
9. **M3B: Patchability profile.** Test local-to-global context extension.
10. **M4A: Public Colah note.** Produce a short explanatory artifact around the proof-carrying figure.

## Definition of advanced done

The advanced implementability lane is done when it can emit an `ImplementabilityCertificate` with:

- source-lock manifest;
- feature witness card;
- controller specification;
- behavioral steering curve;
- causal triad results;
- off-target audit;
- activation-manifold calibration;
- metric-agreement matrix;
- designated-latent report;
- Pattern A/B/C classification;
- uncertainty statement;
- replay/evidence bundle.

The certificate should be valid even if the result is negative. A failed steering reproduction, OOD steering regime, or metric disagreement is still a scientific result if the evidence chain is clean.
