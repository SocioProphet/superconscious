# Trust Surface Rollout Plan

This plan operationalizes the SourceOS Trust Surface Protocol across the SocioProphet, SourceOS-Linux, and SociOS-Linux GitHub estate.

## Rollout rule

A repo must adopt `TRUST_SURFACE.yaml` before it lands or expands local runtime authority.

Local runtime authority includes background services, containers, browser control, terminal control, model gateways, sync daemons, credential brokers, update channels, remote feature flags, or command execution.

## Priority tiers

### Tier 0: protocol seed

- `SocioProphet/superconscious`

Purpose: owns visible cognition governance and seeds the trust-surface protocol until canonical schema ownership is promoted.

### Tier 1: immediate runtime/control-plane repos

These repos should receive trust-surface files first:

- `SocioProphet/agentplane`
- `SocioProphet/sociosphere`
- `SocioProphet/PolicyFabric` or current policy/guardrail repo name
- `SocioProphet/agent-registry`
- `SocioProphet/node-commander` if/when formalized as a repo
- `SourceOS-Linux/sourceos-syncd`
- `SourceOS-Linux/TurtleTerm`
- `SourceOS-Linux/BearBrowser` or current browser repo name
- `SourceOS-Linux/agent-machine`
- `SourceOS-Linux/sourceosctl`
- `SociOS-Linux/socios`

### Tier 2: local-first and memory/runtime repos

- Memory Mesh repositories
- smart-tree integration repositories
- local-first sync/database repos
- model carry/model router repos
- workspace controller repos
- terminal/browser integration repos

### Tier 3: inherited upstream/fork estate

Large upstream forks should be classified but not immediately overworked. The first pass should identify whether we actively ship them, vendor them, reference them, or merely archive them.

## Adoption steps per repo

1. Add `TRUST_SURFACE.yaml`.
2. Add or map `scripts/doctor`.
3. Add or map `scripts/network-surface`.
4. Add or map `scripts/credential-surface`.
5. Add or map `scripts/policy-surface`.
6. Add or map `scripts/purge`.
7. Add or map `scripts/prove-clean`.
8. Add CI validation.
9. Add `SECURITY.md` section describing local authority.
10. Add `docs/threat-model.md` if the repo starts services, opens sockets, stores credentials, or controls browsers/terminals.

## Minimum first-pass acceptable state

A first-pass adoption is acceptable when the repo clearly states:

- whether it has runtime authority;
- what launch items or services it owns;
- what containers/images it runs;
- what ports/listeners it opens;
- what host paths it mounts or writes;
- what credentials it expects;
- whether it controls browser, terminal, model, memory, or sync surfaces;
- how to purge it;
- how to prove it is clean.

## Blocking criteria

A PR should be blocked when it adds any of the following without updating `TRUST_SURFACE.yaml`:

- LaunchAgent, LaunchDaemon, systemd, cron, scheduled task, login item, or service installer;
- Dockerfile, Containerfile, Podman machine/runtime, Compose stack, Kubernetes local runtime, or VM runtime;
- HTTP, WebSocket, SSE, MCP, ACP, CDP, browser relay, noVNC, dashboard, or local gateway listener;
- OAuth, API key, model-provider token, GitHub token, SSH agent, keychain, SecretRef, or credential cache handling;
- shell, exec, spawn, terminal, browser automation, workspace-write, repo-write, or subagent execution;
- auto-update feed, plugin installer, runtime download, or remote feature flag;
- filesystem write outside the repo workspace;
- secret-bearing logs, traces, telemetry, status labels, dashboard displays, or history exports.

## Review checklist

Use this checklist during code review:

- Is there new authority?
- Is the authority declared?
- Is the default posture deny-by-default?
- Are ports loopback-only unless explicitly justified?
- Is plaintext non-loopback transport rejected unless break-glass?
- Are secrets referenced, not embedded?
- Are secret values redacted in logs, status, traces, and UI?
- Are browser/CDP/noVNC controls authenticated?
- Are exec approvals bound to canonical paths and workdirs?
- Are sandbox path boundaries defended against symlinks and TOCTOU?
- Are containers declared with ports, mounts, env, image tags, and digests?
- Does purge remove authority, not just files?
- Does prove-clean verify no process, persistence, listener, credential, container, or residue remains?

## Estate dashboard target

The end state is an estate trust graph that can answer:

```text
Which repos start background services?
Which repos expose local or remote ports?
Which repos touch credentials?
Which repos control browsers or terminals?
Which repos can execute commands?
Which repos mount host paths into containers?
Which repos can write workspaces?
Which repos have purge/prove-clean support?
Which repos have undeclared authority drift?
```

This trust graph should eventually live in SocioSphere or AgentPlane and use the `TRUST_SURFACE.yaml` files as input.
