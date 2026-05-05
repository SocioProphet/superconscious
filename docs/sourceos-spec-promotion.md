# SourceOS Spec Promotion Plan

Superconscious may stage local draft artifact shapes only to harden the loop. Canonical contract ownership belongs in `SourceOS-Linux/sourceos-spec`.

## Promotion target

The following draft objects should be promoted to `SourceOS-Linux/sourceos-spec` once M1 stabilizes:

| Draft object | Purpose | Target family |
|---|---|---|
| `ReasoningRun` | Top-level governed cognition run artifact. | Agent Plane / Execution / Provenance |
| `ReasoningEvent` | JSONL event stream entry for safe operational traces. | Agent Plane / Telemetry |
| `AdapterDecision` | Generic adapter decision envelope. | Governance / Agent Plane |
| `PolicyCheck` | Admission request/decision summary. | Governance |
| `ModelRouteDecision` | Model/provider route decision summary. | Agent Plane / Models |
| `SkillActivation` | Skill selection and activation evidence. | Agent Plane / Skills |
| `ToolUse` | Tool request/result operational summary. | Agent Plane / Tooling |
| `MemoryDecision` | Memory proposal/quarantine/promotion decision. | Agent Plane / Memory |
| `ApprovalDecision` | Operator/enterprise/signed-intent approval state. | Governance / Agreements |
| `AgentPlaneReasoningEvidence` | Evidence stub consumable by AgentPlane. | Execution / Provenance |
| `ReplayPlan` | Replay class and deterministic replay inputs. | Execution / Provenance |
| `BenchmarkResult` | Evidence-backed benchmark outcome. | Release / Experiments |

## Required upstream additions

For each promoted object, add:

- JSON Schema under `schemas/`;
- conforming example under `examples/`;
- OpenAPI patch entry when externally addressable;
- AsyncAPI event/channel fragment when streamed;
- JSON-LD context/vocabulary terms;
- changelog entry;
- ADR if the object changes existing semantics.

## Compatibility rules

- All IDs should use stable `urn:srcos:<type>:<slug-or-hash>` forms.
- Draft objects here use `specVersion: 0.1.0-draft`; upstream promotion should assign the correct SourceOS spec version.
- Superconscious must consume upstream canonical schema once available.
- Local draft schemas should then become examples/tests only, not authority.

## First promotion batch

Promote these first:

1. `ReasoningRun`;
2. `ReasoningEvent`;
3. `AdapterDecision`;
4. `AgentPlaneReasoningEvidence`;
5. `ReplayPlan`;
6. `BenchmarkResult`.

Those six give AgentPlane, SocioSphere, sourceosctl, and product surfaces enough structure to render and validate the M1 loop.
