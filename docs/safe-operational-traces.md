# Safe Operational Traces

Superconscious emits safe operational traces. It does not require or expose raw private chain-of-thought.

## Traceable facts

A safe operational trace may include:

- task input metadata;
- run context;
- task tree;
- skill selected;
- policy check requested;
- policy decision summary;
- model route decision;
- tool request;
- tool result summary;
- memory decision proposal;
- approval request and decision;
- evidence pointer;
- replay class;
- benchmark assertion;
- final answer summary;
- error class and recovery option.

## Non-traceable private content

The trace must not include:

- raw private chain-of-thought;
- secrets or credentials;
- full prompt text when prompt egress is denied;
- sensitive file contents unless explicitly allowed;
- browser profiles or app databases;
- private keys or token stores;
- unredacted user-private data without policy admission.

## Trace levels

| Level | Meaning |
|---|---|
| `public-safe` | Safe for public repo artifacts. |
| `workspace-safe` | Safe inside the project/workspace. |
| `operator-private` | Visible to the local operator only. |
| `restricted` | Hash/reference only; content withheld. |
| `denied` | Must not be emitted. |

## Default event fields

```json
{
  "eventId": "urn:srcos:reasoning-event:...",
  "runId": "urn:srcos:reasoning-run:...",
  "type": "reasoning.task.started",
  "occurredAt": "2026-05-04T00:00:00Z",
  "summary": "Started task",
  "traceLevel": "public-safe",
  "trustLevel": "trusted-control-input",
  "evidenceRefs": []
}
```

## Replay classes

| Class | Meaning |
|---|---|
| `exact` | All inputs are controlled and replayable. |
| `best-effort` | External state may have changed. |
| `evidence-only` | Replay is represented by evidence, not re-execution. |
| `non-replayable-side-effect` | External side effect occurred and cannot be safely replayed. |

M1 should only produce `exact` or `evidence-only` replay classes.
