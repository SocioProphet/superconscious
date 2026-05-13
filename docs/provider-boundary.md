# Provider Boundary for Interpretability Harnesses

Status: v0.1 doctrine  
Owner: `SocioProphet/superconscious`  
Scope: provider access-mode classification and claim admissibility  
Non-scope: provider contract negotiation, production provider integration, pricing, secrets, or hosted API credential handling

## Purpose

This document prevents a recurring failure mode: importing white-box interpretability semantics into a provider that only exposes black-box outputs.

A model provider binding is not just a name like `Gemma`, `Gemini`, `Claude`, `GPT`, `Neuronpedia`, or `Goodfire`. It is a declared access surface: what can be observed, what can be intervened on, what evidence can be replayed, and what claims are forbidden.

## Access modes

### `white_box`

White-box access means the harness can inspect internal model state or model-adjacent learned interpreters.

Allowed examples:

- hidden states;
- residual stream activations;
- attention tensors;
- logits;
- SAE feature activations;
- transcoder features;
- local activation patching;
- feature steering where the intervention target is source-locked.

White-box access is required for implementability-envelope claims over activation manifolds.

### `gray_box`

Gray-box access means the provider exposes structured behavior or limited internal signals, but not enough to support full SAE/circuit claims.

Allowed examples:

- logits or logprobs without full hidden states;
- provider-side traces;
- tool traces;
- limited eval traces;
- constrained intervention APIs that do not expose the underlying latent state.

Gray-box claims must name exactly which observables were available.

### `black_box`

Black-box access means the harness sees prompt-level inputs and output-level behavior only.

Allowed examples:

- output text;
- refusal rates;
- response classifications;
- benchmark answers;
- prompt-only interventions;
- provider-route evidence.

Black-box access cannot support claims over hidden states, SAE features, activation patching, residual-stream implementability, or circuit edges unless another independently source-locked white-box artifact supplies that evidence.

### `registry_only`

Registry-only access means the provider exposes interpretability artifacts rather than live model execution.

Allowed examples:

- public feature registry entries;
- feature dashboards;
- public explanations;
- attribution graph records;
- registry metadata;
- exported activation examples.

Registry-only evidence can support candidate discovery and public artifact citation. It does not by itself prove that a local runtime reproduces the effect.

## Claim admissibility matrix

| Claim family | white_box | gray_box | black_box | registry_only |
| --- | --- | --- | --- | --- |
| Output behavior benchmark | yes | yes | yes | no, unless paired with runtime evidence |
| Prompt-only intervention | yes | yes | yes | no |
| Logit-level claim | yes | yes, if logits exposed | no | no |
| Hidden-state claim | yes | no | no | no |
| SAE feature activation | yes | no | no | registry evidence only, not runtime claim |
| Feature steering | yes | no, unless provider exposes equivalent intervention API | no | no |
| Activation patching | yes | no | no | no |
| Attribution graph runtime replay | yes | no, unless graph runtime is exposed | no | registry evidence only |
| Manifold implementability envelope | yes | no | no | no |
| Public dashboard citation | yes | yes | yes | yes |

## Fail-closed rules

A harness bundle must fail semantic validation if:

1. `access_mode` is `black_box` and `supported_observables` includes hidden states, residual stream, attention tensors, SAE features, or transcoder features.
2. `access_mode` is `black_box` and `supported_interventions` includes feature steering, activation patching, or activation addition.
3. `access_mode` is `registry_only` and the provider binding claims live runtime execution.
4. An intervention spec uses `feature_steering` without a source-locked SAE, transcoder, or probe artifact.
5. An intervention spec uses `activation_patching` without hidden-state or residual-stream observability.
6. A black-box provider is used to support an implementability-envelope claim.
7. A public interpretability note omits non-claims or evidence references.

## Gemma / Gemini rule

Gemma + Gemma Scope is the current open white-box pilot substrate.

Gemini hosted API bindings must be treated as black-box unless a future provider contract exposes internal activation or feature-level evidence. A file, issue, public note, or benchmark that says `Gemini single-parameter SAE steering` without a white-box provider binding is invalid.

## Neuronpedia rule

Neuronpedia-style registry evidence is admissible as public feature/circuit registry evidence. It is not automatically runtime replay evidence. Runtime replay requires a source-locked local model/SAE/transcoder/probe stack or a provider binding that exposes replayable internal state.

## Non-claims

This document does not claim that all providers should expose internals.

It does not claim that black-box behavior benchmarks are useless.

It does not claim that registry evidence is untrustworthy.

It claims only that evidence type must match claim type.
