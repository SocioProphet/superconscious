# Behavior Calculus v0

Status: local draft for Superconscious M2 extraction.

This document extracts a small compositional behavior calculus from the existing Superconscious deterministic runner and cognition loop. It does not add runtime authority, live execution, model calls, network calls, durable memory promotion, schema promotion, policy admission, or workspace mutation.

## Purpose

Superconscious already has two fixed governed loops:

```text
M1 runner:
TaskInput -> workspace -> grants -> policy -> model route -> skill -> tool -> memory -> approval -> evidence -> artifacts

M1.5 cognition loop:
WorkspaceOperation -> policy -> observe -> reflect -> remediation proposal -> learning record -> risk signal -> policy review -> evidence -> artifacts
```

The behavior calculus generalizes those fixed loops into typed subprocesses that can be composed, traced, replayed, and eventually compiled into SourceOS and AgentPlane contract surfaces.

## Default behavior model

A deterministic process is a typed coalgebra-like transition:

```text
Proc<I, O, S>
step : S x I -> O x S
```

The probabilistic upgrade is reserved for later:

```text
step : S x I -> Delta(O x S)
```

M2 starts deterministic. This preserves exact replay and keeps the current M1/M1.5 test posture intact.

## Current repo mapping

| Existing artifact | Behavior-calculus reading |
|---|---|
| `AdapterDecision` | concrete observable output carrier |
| `AdapterSet` | product of subprocess implementations |
| `AdapterTrace` | concrete serial trace over subprocess outputs |
| `runner.collect_adapter_trace` | fixed serial composition |
| `cognition_loop.collect_cognition_trace` | second fixed serial composition |
| `.runs/<run-id>/events.jsonl` | public-safe observation stream |
| `agentplane-evidence.json` | AgentPlane-facing evidence bridge |
| `replay-plan.json` | deterministic replay contract |

## Operators

### Serial composition

If:

```text
P : Proc<I, M, S_P>
Q : Proc<M, O, S_Q>
```

then:

```text
Q o P : Proc<I, O, S_P x S_Q>
```

The output of `P` becomes the input of `Q`. The state of the composite is the product of the two states.

### Parallel composition

If:

```text
P : Proc<I_P, O_P, S_P>
Q : Proc<I_Q, O_Q, S_Q>
```

then:

```text
P tensor Q : Proc<I_P x I_Q, O_P x O_Q, S_P x S_Q>
```

The two processes run side-by-side on paired inputs.

### Delayed feedback

If a process emits an output that must become part of the next input, feedback must be delayed by at least one tick:

```text
feedback_delay_1(P, initial_feedback)
```

No same-tick unguarded recursion is allowed in v0. This prevents accidental nontermination and keeps replay exact.

## Observation projection

Equivalence must be judged through an explicit projection:

```text
obs : O -> O_pub
```

This is mandatory because Superconscious emits safe operational traces and must not expose raw private reasoning. v0 supports trace equivalence on projected outputs, not full internal-state bisimulation.

## Equivalence ladder

1. Trace equivalence: projected event streams match.
2. Artifact equivalence: normalized artifact hashes match after volatile-field removal.
3. Governance equivalence: policy, model route, memory, approval, runtime-effect, grant-state, and evidence decisions match.
4. Bisimulation: future stronger relation over state pairs and projected outputs.

## Boundary alignment

The calculus must compile into existing authority boundaries:

```text
evidence/event envelope = observed fact or receipt
policy decision = governed policy evaluation
runtime effect/admission = execution/control decision
authority/grant mutation = registry/grant-state decision
ledger/state report = evidence record only
```

This follows the lifecycle-boundary contract posture in `SourceOS-Linux/sourceos-spec` and the Superconscious import posture in `SocioProphet/agentplane`.

## Non-goals

- No live execution.
- No network or model provider calls.
- No schema promotion to `sourceos-spec` in this tranche.
- No replacement of AgentPlane evidence/replay authority.
- No replacement of Guardrail/Policy Fabric admission authority.
- No replacement of Agent Registry grant authority.
- No claim of machine sentience.

## M2 extraction rule

Do not rewrite the working runner first. Wrap and prove.

1. Define generic `Proc` and composition operators.
2. Wrap existing deterministic adapters as process nodes.
3. Prove small-chain equivalence under projection.
4. Only then refactor runner/cognition internals if the equivalence tests remain stable.
