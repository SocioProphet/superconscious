# Human Protection Layer adoption for Superconscious

Status: adoption stub referencing ProCybernetica reconciliation draft.

Authoritative doctrine source: `SocioProphet/ProCybernetica/docs/reconciliation/HUMAN_PROTECTION_LAYER.md`.

## 0. Position

Superconscious adopts the Human Protection Layer as a mandatory planning and trace constraint for recursive agent cognition across the SocioProphet / SourceOS stack.

Superconscious remains intentionally thin. It may decompose tasks, propose plans, request policy admission, route tool/model requests through adapters, emit safe operational traces, emit AgentPlane-compatible evidence, emit replay plans, and run benchmark assertions. It must not become the authority for schemas, execution, runtime placement, policy, model governance, workspace topology, or human-impacting action.

## 1. Superconscious-specific protection rule

Superconscious may plan. Superconscious may not authorize.

Default policy:

- no invisible authority;
- no side effects without policy admission;
- no human-impacting decision without review/appeal path;
- no hidden persuasion or emotional exploitation;
- no autonomous human actuation;
- no direct tool execution outside declared adapters;
- no durable memory promotion without explicit memory decision;
- no export of private evidence in safe traces;
- no treating Atlas validity as operational permission.

## 2. HPL in the cognition loop

HPL gates attach to the existing Superconscious loop:

```text
TaskInput
  -> RunContext
  -> ReasoningRun.created
  -> HPLScope.assessed
  -> ReasoningTask.started
  -> PolicyCheck.requested
  -> PolicyCheck.decided
  -> ModelRoute.requested
  -> ModelRoute.decided
  -> SkillActivation.selected
  -> ToolUse.requested
  -> ToolUse.observed
  -> MemoryDecision.proposed
  -> HPLAudit.emitted
  -> Evidence.emitted
  -> ReplayPlan.emitted
  -> BenchmarkResult.emitted
  -> ReasoningRun.completed | failed | cancelled | blocked
```

## 3. Required planning fields

Any Superconscious plan that may affect a protected person must include:

```yaml
hpl_scope:
  protected_person_possible: boolean
  human_impacting_action_possible: boolean
  private_evidence_possible: boolean
  physical_actuation_possible: boolean
  cognitive_safety_risk_possible: boolean
  world_action_affects_population_possible: boolean
  policy_admission_required: boolean
  allowed_next_step: plan_only | request_policy | block
```

## 4. Atlas planning boundary

For Digital Control Atlas work, Superconscious may:

- identify candidate charts;
- decompose tasks into profile-specific planner steps;
- request policy admission;
- request model route decisions;
- assemble safe traces;
- emit replay plans;
- produce benchmark assertions;
- mark blocked/speculative status.

Superconscious may not:

- authorize Atlas execution;
- authorize human actuation;
- export HDT claims;
- promote GAIA action templates;
- finalize ProCybernetica schemas;
- bypass trust-surface declarations;
- convert speculative mechanisms into valid planning assumptions.

## 5. Safe operational trace requirements

Safe traces for HPL-relevant runs must include operational facts only:

- task decomposition summary;
- HPL scope assessment;
- policy request and decision;
- tool/model route request and result summary;
- memory decision proposal;
- evidence pointer;
- replay pointer;
- benchmark result;
- blocked reasons where applicable.

Safe traces must not include raw private chain-of-thought, raw private evidence, credentials, sensitive telemetry, or unauthorized personal data.

## 6. Required tests before promotion

Superconscious should add or maintain tests proving:

- HPL scope is assessed before tool requests in protected-person contexts;
- planning does not authorize execution;
- missing policy admission blocks side-effectful tool use;
- human actuation plans are blocked or marked external-review-required;
- unsupported mechanism labels cannot become planning assumptions;
- private evidence is not emitted in safe traces;
- memory write requires explicit memory decision;
- HPL blocked status appears in replay and benchmark artifacts.

## 7. Relationship to authorities

Superconscious coordinates authorities through adapters. It does not replace them.

HPL-relevant authorities remain external:

- ProCybernetica: doctrine, reconciliation, conformance law;
- Human Digital Twin: human-boundary claims and Ω exports;
- GAIA: world-chart actions and reports;
- AgentPlane: execution evidence and replay authority;
- Policy Fabric / Guardrail Fabric: policy admission;
- SourceOS spec: canonical schemas after promotion;
- Agent Registry: identity and grants;
- Model Router and Model Governance Ledger: model route and model consent/promotion.
