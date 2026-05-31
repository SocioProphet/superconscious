# Neuro-Symbolic Failure Modes

Status: v0.1 boundary checklist.

This document records failure modes Superconscious must guard against when coordinating neuro-symbolic cognition.

## Failure modes

### `soft_score_as_truth`

A fuzzy satisfaction score, semantic-loss value, truth degree, or differentiable constraint result is treated as true evidence, final truth, or policy admission.

Required response: keep the score advisory and request verification/governance.

### `neural_output_as_evidence`

A neural model output is treated as evidence without source anchoring, provenance, or independent verification.

Required response: convert to a candidate claim and require evidence anchoring.

### `learned_rule_as_schema`

A dILP-style or other learned rule is promoted directly into canonical schema, ontology, or policy.

Required response: emit a `RuleCandidateProposal` and route to owning authority.

### `symbolic_derivation_as_policy_admission`

A symbolic derivation, stable model, theorem-prover result, or constraint-solver output is treated as permission to act.

Required response: request Policy Fabric admission and AgentPlane execution/replay handling.

### `carrier_missing_provenance`

A carrier lacks source references, method family, validation status, authority plane, or replay path.

Required response: reject as inadmissible or return to candidate status.

### `embedding_as_ontology_authority`

An ontology embedding or inferred relation is treated as canonical ontology.

Required response: emit `OntologyDeltaProposal`; route to Ontogenesis/sourceos-spec.

### `symbolic_policy_as_live_controller`

A symbolic expression or policy learned from DSR/DSP-style systems is executed as a live controller before policy/runtime admission.

Required response: hold as `SymbolicPolicyProposal`; require governance and runtime admission.

### `label_leakage_grounding_failure`

A perception-to-symbol or differentiable-constraint system appears grounded because labels, target structure, or symbolic inputs leaked into training or evaluation.

Required response: require anti-leakage and transduction validation before verification.

### `transduction_unvalidated`

A system claims to map perception or language to symbols without validating that the symbols are grounded in the intended observation surface.

Required response: request `SymbolGroundingAssessment` and replayable validation.

## Superconscious rule

Superconscious may detect and report these failure modes. It must not resolve them by local authority.
