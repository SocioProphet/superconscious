# M1-0 Controller Specification

## Status

This document is the semantic prerequisite for M1A-M1D of the Implementability Steering Pilot.

M1A-M1D should not be treated as a checklist of activities. They verify different facets of a specified controller behavior. This document defines that controller target before source-lock hardening, feature witness cards, causal triads, or off-target audits proceed.

M1-0 is doctrinal and structural. It requires no model execution and makes no implementability claim.

## Controller name

```text
refuse-and-redirect controller for MCQ harm-pressure behavior
```

## External grounding

This specification is motivated by three external anchors:

1. The refusal-direction line of work showing that refusal behavior in chat models can be modulated by residual-stream directions.
2. Gemma Scope / Neuronpedia exposing Gemma 2 9B-IT layer-20 residual SAE artifacts suitable for open inspection.
3. The Transformer Circuits November 2025 harm-pressure case study, which reports a `refuse-and-redirect` feature involved in multiple-choice withholding behavior and notes that residual error components may interact with that feature.

The pilot does not depend on proprietary Anthropic models or private crosscoders. The Anthropic case is the motivating failure mode; the pilot target remains the open Gemma/Gemma-Scope analogue.

## Plant

The plant is the unmodified model:

```text
google/gemma-2-9b-it
```

under its resolved instruction-tuned chat template, tokenizer, precision policy, and source-locked model revision.

The plant behavior is the set of completion trajectories the model can produce for user-side prompts under the declared natural input distribution.

The plant's reachable behavior includes:

- ordinary benign question answering;
- instruction-following completions;
- refusals and redirects on safety-sensitive prompts;
- multiple-choice answer selection;
- over-refusal and withholding failure modes under safety pressure.

The plant does not include externally modified activations. Steering interventions are candidate controlled behaviors imposed on the plant.

## Manifest control variables

Manifest control variables are surface-observable variables available without reading hidden activations.

For M1, the manifest variables are:

1. **User-turn safety-pressure signals.** Surface patterns indicating that the user frames a question with harmful intent, policy-sensitive intent, or misuse-oriented context.
2. **Question form.** Whether the prompt is a multiple-choice factual question, open-ended request, benign factual request, or operationally harmful request.
3. **Answer-choice structure.** Which tokens correspond to answer options, correct answer markers, and distractors.
4. **Assistant-turn refusal markers.** Surface language indicating refusal, inability, safety redirection, or alternative-help framing.
5. **Assistant-turn compliance markers.** Surface language indicating direct answer selection or task completion.
6. **Final answer status.** Whether the completion selects the correct MCQ answer, refuses, redirects, gives an incorrect answer, or degenerates.

The manifest variables must be declared in the dataset metadata. They should be evaluative, not instructional: the dataset probes refusal-controller behavior without providing step-by-step harmful procedures.

## Latent control variables

Latent control variables are internal state variables hypothesized to mediate the controller behavior.

For M1, the declared latent variables are:

1. **Layer-20 residual-stream activations.** The primary inspection site for the Gemma/Gemma-Scope pilot.
2. **Candidate SAE feature activations.** Sparse feature coordinates from `google/gemma-scope-9b-it-res/layer_20/width_131k/average_l0_81`.
3. **Refusal / redirect feature family.** Features whose contexts, activation profiles, and causal effects align with refusal or redirection behavior.
4. **Harm-detection feature family.** Features that activate on user-side safety-pressure signals or misuse-oriented framing.
5. **Answer-selection feature family.** Features that support correct MCQ answer selection or task completion.
6. **Designated latent quantities.** Residual-stream norm, layer-norm scale, SAE reconstruction error norm, and any position-sensitive residual components that affect the intervention but are not captured by the selected manifest feature.

M1 does not assume that one SAE feature is canonical. A candidate feature must be validated by witnesses and causal effects before it is treated as a controller-relevant feature.

## Controlled behavior

The controlled behavior under study is the model's tendency, under harm-pressure framing, to withhold or redirect in a way that degrades factual MCQ answer selection.

The motivating pattern is:

1. Without harm-pressure framing, the model answers an MCQ correctly.
2. With harm-pressure framing, the model refuses, redirects, or selects an incorrect answer.
3. A targeted intervention on the refusal / redirect mechanism restores the correct answer without damaging unrelated behavior or weakening appropriate refusal on genuinely harmful operational requests.

M1 tests only whether an open-model analogue of this behavior can be reproduced and source-locked. M2 tests whether the effective intervention remains inside the natural activation envelope.

## Admissible controller behavior

The controller is admissible when:

1. It activates on declared safety-pressure prompts that match the safety-flagged set.
2. It does not activate on benign factual prompts that lack safety-pressure signals.
3. It does not suppress factual MCQ answer selection merely because the prompt contains abstract safety-sensitive vocabulary.
4. It preserves refusal on genuinely harmful operational requests.
5. It preserves ordinary benign capability and format-following behavior.
6. It operates through latent variables that can be audited by witness cards, causal probes, and designated-latent tracking.

In the pilot framing, the target failure mode is controller over-activation or misrouting: the model withholds or redirects in a context where the correct factual answer remains known and should be selected under the benchmark's declared task semantics.

## Implementability bounds

The controller cannot restore behavior the plant cannot produce.

For MCQ harm-pressure evaluation:

- the no-harm-pressure accuracy is an upper bound on expected recovery under refusal suppression;
- if the model does not know the answer without harm pressure, refusal suppression should not be credited for failure to answer correctly;
- if the model answers incorrectly without harm pressure, the item should not be used as evidence of refusal-specific withholding;
- if the intervention produces correct answers only by breaking format, damaging unrelated behavior, or weakening genuine harmful-request refusal, the effect is not admissible success.

M2 will add the activation-envelope bound: an intervention that works only outside the natural activation manifold is extrapolative and must be certified differently from an in-envelope intervention.

## Failure modes that matter

### F1: Over-refusal

The controller activates on benign requests or benign factual questions, causing unnecessary refusal, redirection, or incorrect MCQ selection.

### F2: Under-refusal

The controller fails to activate on genuinely harmful operational requests. This is a safety regression, especially if negative steering increases compliance with such requests.

### F3: Off-target degradation

The steering intervention restores one target behavior while degrading benign QA, format-following, coherence, calibration proxies, or general completion quality.

### F4: Latent leakage

The observed behavior changes, but the mechanism appears to run through SAE residual error, residual-stream norm shifts, layer-norm scale changes, or other designated latents rather than the selected feature. This means the feature explanation is incomplete.

### F5: Representation artifact

The candidate appears important in one SAE dictionary but fails cross-width, cross-L0, or behavioral-equivalence checks. This means the feature identity is not stable enough for a certificate claim.

### F6: Extrapolative intervention

The intervention succeeds behaviorally but places activations outside the natural activation envelope. This is not a failed result, but it changes the claim: the intervention is an extrapolative control, not an in-envelope behavior selection.

### F7: Underspecified controller

A candidate feature cannot be classified as matching, partially matching, or missing the controller specification. If this occurs, M1-0 is underspecified and must be revised before M1B proceeds.

## Milestone verification roles

### M1A: forensic source-lock

Verifies that the plant, SAE, controller spec, datasets, code, runtime, random seeds, and generated artifacts are fixed and replayable.

M1A answers:

```text
Are we verifying this controller against fixed artifacts?
```

### M1B: feature witness cards

Verifies that the candidate feature identity is supported by independent witnesses: contexts, contrastive activation, preliminary causal effect, behavioral equivalence neighborhood, patchability, and family classification.

M1B answers:

```text
Does this candidate feature match the specified controller target?
```

### M1C: causal triad with designated latents

Verifies that ablation, positive steering, and negative steering have coherent directionality, while tracking whether designated latents explain the effect.

M1C answers:

```text
Does intervening on the candidate causally modulate the specified controller behavior, and is the manifest-feature story complete enough?
```

### M1D: off-target audit

Verifies that the effective intervention does not produce unacceptable damage on benign QA, harmless prompts, format-following, generation quality, or genuine refusal preservation.

M1D answers:

```text
Does the intervention improve the target failure mode without breaking adjacent behavior?
```

### M2: implementability envelope

Verifies whether the effective steering activation is inside, outside, or on the boundary of the natural activation envelope under declared metrics and calibration.

M2 answers:

```text
Is the controlled behavior reachable by the unsteered plant under natural inputs at the metric resolution we declared?
```

## Acceptance criterion for M1-0

M1-0 is complete when, for any candidate feature surfaced in M1B, the analyst can classify the feature as:

1. matching the controller specification;
2. partially matching the controller specification;
3. off-target;
4. ambiguous because evidence is insufficient;
5. unclassifiable because the controller specification is underspecified.

Only the fifth outcome is a failure of M1-0.

## Certificate fragment

M1-0 should be hashed and included in every downstream certificate fragment.

Expected generated record:

```text
outputs/m1/certificates/m1-0-controller-spec.json
```

Minimum fields:

```json
{
  "schema_version": "m1-0-controller-spec.v0.1",
  "controller_name": "refuse-and-redirect controller for MCQ harm-pressure behavior",
  "controller_spec_path": "docs/m1-0-controller-spec.md",
  "controller_spec_sha256": "<filled by M1A>",
  "plant_model_repo": "google/gemma-2-9b-it",
  "primary_latent_site": "layer_20 residual stream",
  "primary_sae_path": "google/gemma-scope-9b-it-res/layer_20/width_131k/average_l0_81/params.npz",
  "claim_boundary": "M1-0 specifies the controller target; it does not certify feature identity, causal effect, off-target safety, or implementability."
}
```

## Non-claim boundary

M1-0 does not claim:

- the selected feature exists;
- Gemma reproduces the proprietary Anthropic finding;
- any steering intervention is safe;
- any steering intervention is in-envelope;
- SAE features are canonical;
- refusal is globally one-dimensional;
- the controller is fully represented at layer 20.

M1-0 only defines what the downstream certificate fragments are trying to verify.
