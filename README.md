# superconscious

**Superconscious** is the reference governed cognition loop for recursive agents across the SocioProphet / SourceOS stack.

It coordinates task trees, safe operational traces, skill activation, tool use, memory decisions, model routing, policy admission, approvals, benchmarks, replay plans, and AgentPlane-compatible evidence without becoming the authority for schemas, execution, runtime placement, model governance, or workspace topology.

## Position

Superconscious is the visible cognition/control-loop layer. It makes the estate behave like one governed agent operating system while preserving clean authority boundaries across the existing repositories.

```text
Task input
  -> validate
  -> plan
  -> request policy admission
  -> request model route
  -> activate skill
  -> call tool adapter
  -> record observation
  -> decide memory handling
  -> request approval when needed
  -> emit safe operational trace
  -> emit AgentPlane evidence
  -> emit replay plan
  -> run benchmark assertions
```

## Trust Surface Protocol

Superconscious now seeds the **SourceOS Trust Surface Protocol** for the estate.

The principle is direct: **no invisible authority**. Any repo that starts a process, installs a service, opens a socket, controls a browser or terminal, launches a container, stores credentials, runs agents, or routes model/provider traffic must declare that authority in `TRUST_SURFACE.yaml`.

This repo includes:

```text
TRUST_SURFACE.yaml
schemas/trust-surface.schema.json
docs/trust-surface-protocol.md
examples/TRUST_SURFACE.node-commander.yaml
scripts/validate-trust-surface.py
.github/workflows/trust-surface.yml
```

The first target is not bureaucracy. The target is inspectability, purgeability, and provable cleanup across local agent runtimes.

## What this repo owns

- Reference recursive reasoning loop implementation.
- Safe operational trace assembly.
- Local deterministic demo runner.
- Adapter interfaces for AgentPlane, Agent Machine, Model Router, Guardrail Fabric, Agent Registry, Memory Mesh, SocioSphere, sourceosctl, BearBrowser, TurtleTerm, and Socios.
- Example reasoning runs and benchmark fixtures.
- Product-facing cognition-console semantics.
- Trust-surface protocol seed, examples, and validation workflow until canonical schema ownership moves to `SourceOS-Linux/sourceos-spec`.

## What this repo does not own

- Canonical schemas: owned by `SourceOS-Linux/sourceos-spec`.
- Execution, placement, evidence, replay authority: owned by `SocioProphet/agentplane`.
- Workspace topology, manifests, locks, registry governance: owned by `SocioProphet/sociosphere`.
- Runtime substrate and AgentPod activation: owned by `SourceOS-Linux/agent-machine`.
- Local model profile carriage: owned by `SourceOS-Linux/sourceos-model-carry`.
- Model promotion, consent, and personalization authority: owned by `SocioProphet/model-governance-ledger` and `SociOS-Linux/socios`.
- Policy authority: owned by Guardrail / Policy Fabric.
- Agent identity and grants: owned by Agent Registry.

## M1 deliverable

M1 is a deterministic, no-network, no-model-call, no-side-effect reference loop that emits:

```text
.runs/<run-id>/events.jsonl
.runs/<run-id>/reasoning-run.json
.runs/<run-id>/agentplane-evidence.json
.runs/<run-id>/replay-plan.json
.runs/<run-id>/benchmark-result.json
```

The first goal is not model quality. The first goal is lifecycle discipline, evidence compatibility, replay shape, safe trace semantics, and declared trust surfaces.

## Repository layout

```text
superconscious/
  README.md
  ARCHITECTURE.md
  THREAT_MODEL.md
  ROADMAP.md
  AGENTS.md
  TRUST_SURFACE.yaml
  docs/
    trust-surface-protocol.md
  schemas/
    trust-surface.schema.json
  examples/
    TRUST_SURFACE.node-commander.yaml
  scripts/
    validate-trust-surface.py
  packages/superconscious-core/
  tests/
```

## Strategic framing

```text
Subconscious optimizes recursive inference.
Superconscious governs recursive agency.
```

Superconscious does not claim machine sentience. It defines operational consciousness as explicit awareness of task state, tools, memory, models, policy, runtime, evidence, and feedback loops.

The trust-surface layer extends that frame to local authority: a governed agent operating system must know what it can start, read, write, execute, expose, update, remember, and remove.
