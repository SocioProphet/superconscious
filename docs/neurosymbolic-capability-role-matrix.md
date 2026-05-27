# Neuro-Symbolic Capability Role Matrix

Status: v0.1 boundary matrix.

This matrix defines what Superconscious may do with neuro-symbolic capabilities and what it must not do.

The matrix is aligned with the existing adapter boundary rule: Superconscious coordinates; it does not authorize.

## Matrix

| Capability class | Example method family | May request | May record | Must not do | Final authority |
|---|---|---|---|---|---|
| `NSR-FOUNDATION-LOGIC` | formal logic / annotated logic / fuzzy operators | schema/vocabulary lookup | logic substrate reference | claim theorem-grade entailment without proof assumptions | sourceos-spec / Ontogenesis |
| `NSR-TAXONOMY` | Kautz-style NSR classification | method classification | capability role label | treat class as maturity, safety, or authority grade | SocioSphere for integration vocabulary |
| `NSR-SOFT-CONSTRAINT` | LTN-style semantic loss | soft constraint evaluation | satisfaction score and caveats | promote score to truth, policy admission, or evidence | policy / AgentPlane / sourceos-spec as applicable |
| `NSR-TRUTH-BOUND` | LNN-style truth bounds | bound/inconsistency assessment | lower/upper bounds and formula trace | claim global consistency or arbitrary entailment correctness | policy / Ontogenesis / sourceos-spec as applicable |
| `NSR-SYMBOLIC-ADJUDICATION` | NeurASP-style neural atoms + ASP | symbolic adjudication request | stable-model summary and policy request | execute, route, remember, or authorize from stable model alone | AgentPlane / policy fabric |
| `NSR-DIFFERENTIABLE-CONSTRAINT-LEARNING` | SATNet-style learned constraints | grounding-risk assessment | leakage/transduction risk report | accept apparent grounding without anti-leakage validation | AgentPlane / policy fabric / Ontogenesis |
| `NSR-RULE-LEARNING` | dILP-style learned rules | candidate rule review | rule candidate proposal | promote rule to schema, ontology, policy, or runtime authority | Ontogenesis / sourceos-spec / policy fabric |
| `NSR-ONTOLOGY-INFERENCE` | RRN / Deep Ontological Networks | ontology-delta review | relation candidate and embedding inference report | treat embeddings as ontology authority | Ontogenesis / sourceos-spec |
| `NSR-SYMBOLIC-POLICY` | DSR / DSP | symbolic policy review | controller candidate and objective-alignment report | run policy as controller before admission | policy fabric / AgentPlane / runtime plane |

## Event posture

A Superconscious event touching neuro-symbolic output must remain one of:

```text
observe
reflect
propose
record
risk_signal
policy_review_request
```

It must not become:

```text
authorize
execute
promote_schema
promote_memory
route_model
open_network
mutate_workspace
```

## Required fields for future NSR traces

Future NSR traces should include:

```json
{
  "methodFamily": "NSR-SOFT-CONSTRAINT",
  "carrierStatus": "candidate",
  "claimStatus": "advisory",
  "validationState": "verification_pending",
  "groundingStatus": "not_applicable_or_pending",
  "sourceEvidenceRef": "urn:...",
  "policyDecisionRef": "pending",
  "authorityPlane": "SocioProphet/policy-fabric",
  "nonAuthorityDeclaration": "Soft satisfaction score is advisory only."
}
```

## Mandatory rejection conditions

Superconscious must emit risk or policy review rather than promotion when any of the following appears:

- `soft_score_as_truth`
- `neural_output_as_evidence`
- `learned_rule_as_schema`
- `symbolic_derivation_as_policy_admission`
- `carrier_missing_provenance`
- `embedding_as_ontology_authority`
- `symbolic_policy_as_live_controller`
- `label_leakage_grounding_failure`
- `transduction_unvalidated`

## Non-goal

This matrix does not implement an NSR adapter. Any future adapter must update `TRUST_SURFACE.yaml` if it adds runtime authority.
