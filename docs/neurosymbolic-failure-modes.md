# Neuro-Symbolic Failure Modes

Status: v0.2 failure-mode ledger.

This document records neuro-symbolic failure modes that Superconscious must treat as risk signals or policy-review triggers.

## Purpose

Neuro-symbolic systems often combine neural extraction, fuzzy scores, symbolic rules, ontology embeddings, constraint solvers, and policy candidates. Each piece can be useful. None of those outputs automatically carries authority.

Superconscious must preserve the boundary between:

```text
observed / proposed / explained / verified / admitted
```

and must never silently collapse those stages.

## Failure modes

### soft_score_as_truth

A differentiable fuzzy-logic score, satisfaction score, truth degree, or semantic-loss value is treated as a true claim.

Required response:

- record advisory score;
- attach non-authority declaration;
- request verification or policy review if action depends on it.

### neural_output_as_evidence

A model output is treated as evidence without a source anchor, provenance record, or replayable evidence path.

Required response:

- reject evidence promotion;
- request evidence anchor;
- emit risk signal if downstream action was proposed.

### learned_rule_as_schema

A learned rule from dILP-like, LNN-like, LTN-like, or other rule-learning machinery is treated as canonical schema, ontology, or policy.

Required response:

- record as `RuleCandidateProposal` only;
- route to Ontogenesis / sourceos-spec / policy fabric as applicable;
- prohibit direct promotion.

### symbolic_derivation_as_policy_admission

A symbolic solver, stable model, derivation, or proof-like trace is treated as authorization to execute.

Required response:

- record derivation as explanation or verification artifact;
- request policy admission;
- prohibit execution until AgentPlane and policy authority admit.

### carrier_missing_provenance

A carrier lacks source evidence, claim provenance, validation state, or owning authority plane.

Required response:

- reject carrier admission;
- request provenance repair;
- emit risk signal if carrier was used downstream.

### embedding_as_ontology_authority

An ontology embedding, RRN output, relation candidate, or similarity score is treated as canonical ontology.

Required response:

- record as `OntologyDeltaProposal` or `RelationInferenceCandidate`;
- route to Ontogenesis;
- prohibit canonical schema or ontology mutation.

### visual_embedding_as_evidence

A visualization of an embedding space, t-SNE plot, cluster picture, graph layout, or neighborhood diagram is treated as evidence for an ontology, claim, or relation.

Required response:

- record visualization as an inspection artifact only;
- require source provenance and replayable verification;
- route ontology implications to Ontogenesis;
- prohibit evidence or ontology promotion from visualization alone.

### symbolic_policy_as_live_controller

A symbolic regression or deep symbolic policy output is used as a live controller without objective alignment, safety envelope, governance admission, and replay.

Required response:

- record as `SymbolicPolicyProposal`;
- request controller admission;
- prohibit runtime execution.

### label_leakage_grounding_failure

A method appears to ground symbols but the evidence depends on leaked labels, hidden symbolic targets, or training artifacts that invalidate the grounding claim.

Required response:

- reject grounding promotion;
- require anti-leakage test;
- require transduction assessment;
- require held-out grounding validation.

### transduction_unvalidated

A perception-to-symbol mapping is used without validating how perceptual states map to symbolic states.

Required response:

- mark grounding status as pending;
- request validation;
- block admission if carrier depends on grounding.

### transduction_certificate_missing

A perception-to-symbol mapping is treated as verified even though the carrier lacks a transduction assessment, masked-output evaluation, held-out grounding validation, or evidence/replay authority reference.

Required response:

- mark grounding status as certificate-missing;
- request a `SymbolGroundingAssessment` or equivalent downstream artifact;
- emit risk signal if the carrier was proposed for action, memory, schema, ontology, or policy use;
- block admission until the missing certificate is supplied and reviewed.

### thresholded_interval_as_hard_truth

An interval-valued truth bound, fuzzy confidence range, or calibrated truth region is collapsed into hard truth without recording the threshold policy, alpha value, contradiction state, and decision-threshold provenance.

Required response:

- record the interval as an interval;
- require `TruthRegionCalibration` or equivalent threshold provenance;
- preserve contradiction and uncertainty states;
- prohibit policy or schema promotion from thresholded values alone.

## Superconscious invariant

Every failure mode above is handled by read / reflect / propose / record / risk-signal / policy-review posture.

No failure mode is handled by direct mutation, execution, memory promotion, model routing, or schema promotion inside Superconscious.
