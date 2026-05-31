# Neuro-Symbolic Capability Role Matrix

Status: v0.1 boundary matrix.

This matrix binds neuro-symbolic capability families to Superconscious adapter posture.

Superconscious coordinates and records. It does not authorize.

## Role matrix

| Capability | Input surface | Superconscious may emit | Required downstream authority | Hard boundary |
|---|---|---|---|---|
| `NSR-FOUNDATION-LOGIC` | formal vocabulary, claim syntax, rule language | method classification, normalized vocabulary reference | Ontogenesis / sourceos-spec for canonical vocabulary or schema | no theorem claim without explicit proof system |
| `NSR-TAXONOMY` | method description | capability classification | none for classification; owning plane for use | taxonomy is not maturity, safety, or authority |
| `NSR-SOFT-CONSTRAINT` | fuzzy score, satisfaction score, semantic loss result | `ConstraintEvaluationResult` reference | Policy Fabric for admission; AgentPlane for evidence/replay | score cannot admit action or truth |
| `NSR-TRUTH-BOUND` | lower/upper truth bounds, inconsistency report | `TruthBoundAssessment` reference | Ontogenesis/sourceos-spec for semantic promotion; Policy Fabric for use | local bounds are not global correctness |
| `NSR-SYMBOLIC-ADJUDICATION` | neural atoms, ASP/stable-model output, constraint solution | `SymbolGroundingAssessment` or adjudication summary | AgentPlane evidence/replay; Policy Fabric admission | stable model is not execution authority |
| `NSR-DIFFERENTIABLE-CONSTRAINT-LEARNING` | learned constraint matrix/layer, differentiable solver output | grounding risk and leakage-test request | AgentPlane evidence/replay; Ontogenesis/sourceos-spec if promoted | apparent grounding requires anti-leakage validation |
| `NSR-RULE-LEARNING` | learned rule candidate | `RuleCandidateProposal` reference | Ontogenesis/sourceos-spec for semantic/schema promotion | learned rule is never canonical by default |
| `NSR-ONTOLOGY-INFERENCE` | inferred relation, ontology embedding, RRN output | `OntologyDeltaProposal` reference | Ontogenesis for vocabulary; sourceos-spec for canonical schema | embedding is not ontology authority |
| `NSR-SYMBOLIC-POLICY` | symbolic expression or controller candidate | `SymbolicPolicyProposal` reference | Policy Fabric, AgentPlane, runtime owner | proposal is not live control |

## Adapter mapping

| Adapter | NSR usage | Forbidden local action |
|---|---|---|
| `PolicyAdapter` | request policy review for carrier or symbolic policy | decide policy locally |
| `ModelRouteAdapter` | request route for NSR model use | call provider directly |
| `ToolAdapter` | record requested tool envelope for symbolic solver or validator | perform live tool execution in inert posture |
| `MemoryAdapter` | propose memory handling for admitted carriers | persist unadmitted claim or private data |
| `EvidenceAdapter` | emit evidence reference and replay refs | claim final truth |
| `SchemaAdapter` | request schema validation refs | promote draft schemas |
| `WorkspaceAdapter` | bind run to workspace constraints | change topology or locks |
| `ApprovalAdapter` | request approval when required | fabricate or downgrade approval |
| `BenchmarkAdapter` | check boundary assertions | treat benchmark success as policy admission |

## Required fields for NSR trace records

```text
methodFamily
methodOutputType
sourceEvidenceRef
carrierStatus
provenanceStatus
validationStatus
authorityPlane
governanceState
forbiddenPromotion
replayRef
```

## Minimal statuses

```text
candidate
explained
verification_pending
verified
rejected
admission_pending
admitted
receipt_emitted
learning_recorded
```

Superconscious may record these statuses. It may not transition a carrier to `admitted` unless the owning authority decision is present.
