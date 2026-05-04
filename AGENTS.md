# Agent Instructions for Superconscious

Superconscious is the reference governed cognition loop for recursive agents across the SocioProphet / SourceOS stack.

## Work posture

- Keep this repo thin. Coordinate existing authorities; do not replace them.
- Prefer small, testable, deterministic changes.
- Fail closed on missing policy, missing grants, unknown trust level, unknown tool authority, or uncertain egress posture.
- Emit safe operational traces, not raw private chain-of-thought.
- Never add secrets, credentials, tokens, private keys, browser profiles, or local device-specific paths.
- No AGPL dependencies unless the estate policy changes explicitly.
- Public-source hygiene matters: assume this repository is public and should remain safe to inspect.

## Authority boundaries

- Put canonical contracts in `SourceOS-Linux/sourceos-spec`, not here.
- Put execution/evidence/replay authority in `SocioProphet/agentplane`, not here.
- Put workspace topology and registry validation in `SocioProphet/sociosphere`, not here.
- Put runtime substrate and activation in `SourceOS-Linux/agent-machine`, not here.
- Put local model profile carriage in `SourceOS-Linux/sourceos-model-carry`, not here.
- Put model route authority in `SocioProphet/model-router`, not here.
- Put policy authority in `SocioProphet/guardrail-fabric` / Policy Fabric, not here.
- Put agent identity and grants in `SocioProphet/agent-registry`, not here.
- Put opt-in personalization orchestration in `SociOS-Linux/socios`, not here.

## Implementation rules

- M1 must remain no-network, no-model-call, and no-host-mutation.
- Local outputs should go under `.runs/<run-id>/` only.
- Use JSONL for event streams and JSON for final artifacts.
- Every run must include a replay plan and benchmark result.
- Every tool call must include source, trust level, grant reference, policy decision, and side-effect class.
- Every memory write must be a proposal or explicit decision; never auto-promote untrusted observations.
- Every external adapter must have a mock implementation for deterministic tests.

## Required checks

Before claiming a change is complete:

```bash
python3 -m pytest
python3 packages/superconscious-core/superconscious_core/runner.py examples/basic-reasoning-run/task.json
```

If tests are not available yet, add at least one deterministic fixture and document the gap in `ROADMAP.md`.
