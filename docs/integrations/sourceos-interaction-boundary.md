# SourceOSInteractionEvent task-boundary binding

## Status

Boundary registration and deterministic fixture validation only.

Superconscious may accept or emit `SourceOSInteractionEvent` references at the task boundary so Noetica, AgentTerm, Superconscious, AgentPlane, Memory Mesh, Agent Registry, Policy Fabric, and model-router can coordinate over one interaction substrate without collapsing authority boundaries.

## Canonical contract

The canonical schema is owned by `SourceOS-Linux/sourceos-spec`:

- `schemas/SourceOSInteractionEvent.json`
- `generated/python/sourceos_interaction_event.py`
- `generated/typescript/sourceos-interaction-event.ts`

Superconscious does not own this schema. It may vendor, validate, or reference it from a pinned SourceOS spec revision.

## Allowed Superconscious behavior

Superconscious may:

- accept a source interaction event or event reference as bounded task context;
- emit a bounded result interaction event or event reference;
- preserve session, workroom, topic, thread, actor, participant, task, steering, governance, evidence, replay, and redaction references;
- coordinate the visible cognition/task loop around the event;
- route missing-authority states to the appropriate authority plane.

## Prohibited authority drift

Superconscious must not:

- become the Policy Fabric admission authority;
- become the Agent Registry grant/session/revocation authority;
- become the Memory Mesh durable memory or context-pack authority;
- become the AgentPlane execution evidence or replay authority;
- become the model-router authority in SourceOS mode;
- put raw secrets, credentials, unrestricted transcripts, unrestricted shell output, unrestricted browser history, or private chain-of-thought in event payloads;
- treat an interaction event as side-effect authorization.

## Required task-boundary fields

A Superconscious task-boundary binding should carry, at minimum:

- `source_interaction_event_ref` or `source_interaction_event`;
- `result_interaction_event_ref` or `result_interaction_event`;
- `session_ref`;
- `workroom_ref` or explicit null;
- `topic_ref` or explicit null;
- `actor_ref`;
- `policy_decision_refs`;
- `grant_refs`;
- `memory_scope_ref` or explicit null;
- `context_pack_refs`;
- `agentplane_run_ref` or explicit null;
- `evidence_refs`;
- `replay_ref` or explicit null;
- `redaction_refs`.

## Payload posture

Only bounded metadata, summaries, or references are allowed. `payload_mode` must be one of:

```text
metadata-only
summary
ref-only
inline-bounded
redacted
```

Private chain-of-thought is never a valid payload.

## Operational flow

```text
Noetica / AgentTerm / Matrix / API source event
  -> SourceOSInteractionEvent ref or bounded inline event
  -> Superconscious task-boundary binding
  -> Policy / grant / route / memory / evidence references preserved
  -> bounded result interaction event/ref emitted
  -> AgentTerm or Noetica can render the same governance trace
```

## Validation

Use the local checker:

```bash
python3 scripts/check_sourceos_interaction_boundary.py tests/fixtures/integrations/sourceos-interaction-boundary.valid.json
```

The checker validates that the binding is bounded, preserves authority references, and does not claim policy, grant, memory, route, or evidence authority.
