# M1 Source Lock

## Status

This document records the M1 source-lock decisions for the Implementability Steering Pilot.

M1 does not prove implementability. M1 proves that one open-model steering effect can be reproduced on fixed public artifacts. Only after this gate is passed do M2/M3 build activation caches, nearest-neighbor baselines, and implementability curves.

## Locked target

### Model

- Repository: `google/gemma-2-9b-it`
- Variant: instruction-tuned Gemma 2 9B
- Reason: refusal and safety-controller behavior should be materially present in the instruction-tuned model. The base model is not the pilot target because its refusal apparatus is weaker and would confound the steering-reproduction gate.
- Access note: Hugging Face requires acceptance of Google's Gemma usage terms before file access.
- Precision target: `bfloat16` unless hardware constraints force an explicitly recorded alternative.
- Revision policy: use `main` only to resolve a concrete Hugging Face commit SHA during M0. All M1 outputs must record that SHA.

### SAE source

- Repository: `google/gemma-scope-9b-it-res`
- Family: Gemma Scope residual-stream sparse autoencoders for Gemma 2 9B instruction-tuned activations.
- Reason: use IT-tuned residual SAEs, not base-model SAEs applied to IT activations. Applying base SAEs to IT activations would introduce a distribution shift and weaken the steering interpretation.
- License note: Gemma Scope repository is CC-BY-4.0 on Hugging Face.
- Revision policy: start from `main`, but resolve and record a concrete Hugging Face commit SHA during M0.

### Layer

- Primary layer: `20`
- Rationale: layer 20 is the mid-stack pilot target and is available in the Gemma Scope 9B-IT residual SAE release.
- Follow-up layers: `9` and `31` may be used only after M1 succeeds or if layer 20 fails and the failure analysis justifies fallback.

### SAE width

- Primary width: `131k`
- Rationale: enough granularity to separate refusal, redirect, harm-detection, and policy-meta features while remaining within the public 9B-IT residual SAE release.

### L0 / sparsity

- Primary L0 directory: `average_l0_81`
- Path: `layer_20/width_131k/average_l0_81/params.npz`
- Rationale: this is within the intended L0 70-100 range and is present in the public layer-20 / width-131k tree.
- Fallback rule: do not change L0 mid-run. If `average_l0_81` is unavailable locally, stop and record the failure rather than silently using another L0.

## Cross-width witness targets

M1B Witness 4 uses cross-width behavioral-equivalence checks. The public 9B-IT residual release exposes 16k and 131k widths at layers 9, 20, and 31. It does **not** expose the 65k or 1M width family for 9B-IT; those widths belong to the 9B-PT residual release and are therefore outside the primary IT source lock.

For M1B v1, cross-width comparison is restricted to the same model family and same layer:

```text
primary:  google/gemma-scope-9b-it-res/layer_20/width_131k/average_l0_81/params.npz
witness:  google/gemma-scope-9b-it-res/layer_20/width_16k/average_l0_91/params.npz
```

Rationale:

- both artifacts are instruction-tuned residual SAEs;
- both target layer 20;
- both have hidden dimension `d_in = 3584`;
- `average_l0_91` is the Neuronpedia-demonstrated 16k layer-20 configuration;
- the comparison is conservative: it tests whether a candidate survives a representation-size change without introducing PT-vs-IT distribution shift.

Deferred cross-width / cross-release comparisons:

```text
9B-PT width_65k
9B-PT width_1m
9B-PT width_32k / 262k / 524k
```

These belong to M3 robustness, not M1B v1, because they change the model training regime from IT to PT and therefore require a separate compatibility argument.

## Source-lock command

The source lock is materialized by:

```bash
python3 src/m1/source_lock.py --write outputs/m1/source-lock.json
```

The script must resolve:

- model repository;
- model commit SHA;
- model access/license status if visible;
- tokenizer source;
- SAE repository;
- SAE commit SHA;
- SAE path;
- SAE file metadata exposed by Hugging Face;
- pilot layer, width, L0, and position classes;
- cross-width witness target path for M1B v1.

The script does not download full model weights or SAE parameters by default. It records metadata and raises if the target path is not present.

## Lock invariants

Changing any of the following invalidates cross-run comparisons and requires a new source-lock record:

- model repository;
- model commit SHA;
- tokenizer commit SHA;
- SAE repository;
- SAE commit SHA;
- layer;
- width;
- average L0;
- cross-width witness width/L0;
- intervention site;
- activation dtype;
- chat template;
- evaluation dataset version;
- safety filtering rules.

## M1 acceptance gate

M1 is successful only when the source-locked artifacts support a measurable behavioral steering effect.

The acceptance target is:

1. a selected refusal / redirect / safety-controller feature;
2. a steering magnitude sweep;
3. an identified `alpha_behavioral`;
4. an accuracy gain of at least 30 percentage points over harm-pressure baseline, or a clearly recorded negative result that forces source-lock revision.

No implementability-distance claim may be made at M1.

## Safety and data doctrine

The refusal-sensitive MCQ dataset must be evaluative, not instructional. Dataset items may test whether a model suppresses or restores answering under safety pressure, but they should avoid operational step-by-step harmful procedures. The M1 artifact is a model-governance and interpretability experiment, not a capability manual.
