# SourceOS Trust Surface Protocol

The SourceOS Trust Surface Protocol makes local agent authority explicit, inspectable, revocable, and testable across the SocioProphet, SourceOS-Linux, and SociOS-Linux estate.

This protocol came from direct operational forensics around local agent apps, Electron residue, LaunchAgents, Podman runtime behavior, local RPC surfaces, and agent-platform changelog archaeology. The conclusion is simple: an agent platform is a local operating system in miniature. It must declare every place where it gains authority.

## Principle

No invisible authority.

Every daemon, socket, credential, launch item, container, browser controller, terminal executor, update feed, model-provider bridge, runtime cache, and purge path must be declared in the repo that owns it.

## Required artifact

Runtime-bearing repositories must include a root-level `TRUST_SURFACE.yaml`.

A repository is runtime-bearing if it can do any of the following:

- start a process outside a normal foreground CLI invocation;
- install a LaunchAgent, LaunchDaemon, systemd unit, cron job, scheduled task, login item, service, or background worker;
- expose a local, LAN, tailnet, or remote network listener;
- open WebSocket, SSE, MCP, ACP, CDP, browser relay, noVNC, or dashboard control surfaces;
- run a container, VM, sandbox, Podman machine, Docker runtime, Lima runtime, or Kubernetes workload;
- control a browser, terminal, shell, editor, repo, workspace, node, phone, messaging channel, or model gateway;
- read, write, mint, refresh, copy, proxy, or store credentials;
- execute tools, commands, scripts, cron jobs, subagents, or model-suggested actions;
- call model providers or route between model providers;
- auto-update code or accept remote feature flags that can change local behavior.

## Required commands

Runtime-bearing repositories should provide these commands or equivalent package scripts:

```text
scripts/doctor
scripts/network-surface
scripts/credential-surface
scripts/policy-surface
scripts/purge
scripts/prove-clean
```

`doctor` reports health and configuration. `network-surface` enumerates listeners, bind addresses, protocols, and expected egress. `credential-surface` reports where secrets live without printing secret values. `policy-surface` reports what agents can read, write, execute, call, and escalate. `purge` removes runtime state and authority. `prove-clean` proves the component no longer has processes, launch items, sockets, containers, credentials, or residue.

## Runtime classes

Use one or more runtime classes in `TRUST_SURFACE.yaml`:

```text
spec_only
library
cli
desktop_app
launch_agent
container_runtime
browser_control
terminal_control
model_gateway
sync_service
agent_orchestrator
credential_broker
policy_engine
memory_runtime
local_first_database
```

Only `spec_only` and `library` repos may omit most operational surface fields. All other classes must declare authority boundaries.

## Minimum trust surface fields

Every runtime-bearing `TRUST_SURFACE.yaml` must declare:

- component identity;
- owning repo and org;
- runtime classes;
- binary or script entrypoints;
- install paths;
- launch services;
- containers and images;
- network listeners and bind addresses;
- network egress;
- host mounts and writable paths;
- credential locations;
- logs and caches;
- model providers;
- browser/CDP/noVNC/dashboard surfaces;
- execution permissions;
- update feeds or remote feature flags;
- purge procedure;
- prove-clean checks;
- known risks and compensating controls.

## Default-deny posture

The default posture is:

- no host mounts;
- no exposed ports;
- no inherited secrets;
- no SSH agent forwarding;
- no browser/CDP access;
- no model-provider credentials;
- no network egress;
- no background persistence;
- no auto-update authority;
- no runtime config writes;
- no command execution;
- no workspace write access.

Any deviation must be declared and justified.

## Lessons encoded

The protocol encodes the concrete failure modes we saw in real agent systems:

- app uninstall leaves cookies, trust tokens, HTTP storage, caches, logs, and updater artifacts;
- loopback RPC is still a security boundary;
- local WebSocket and browser-control APIs require authentication and origin controls;
- SSH/dev-environment discovery can map sensitive local topology;
- OAuth tokens and model-provider credentials spread across env, config, keychains, browser storage, service units, and runtime caches;
- LaunchAgent/systemd service token drift causes stale authority after rotation;
- browser/CDP/noVNC surfaces are privileged execution surfaces;
- `ws://` should be loopback-only by default;
- non-loopback plaintext control channels require explicit break-glass opt-in;
- exec approvals must bind canonical command paths, working directories, and immutable command plans;
- sandbox boundaries must defend against symlink and TOCTOU path escapes;
- webhook ingress must authenticate before expensive body parsing;
- logs, traces, dashboards, UI labels, and status output must redact secrets;
- diagnostic tooling must not assume BSD/GNU tool behavior or a single PATH layout.

## Estate adoption model

1. Seed this protocol in `superconscious` as the visible governance layer.
2. Promote the schema to the canonical spec repo when `sourceos-spec` is ready to own it.
3. Add `TRUST_SURFACE.yaml` to high-risk runtime repos first: AgentPlane, SocioSphere, PolicyFabric, TurtleTerm, BearBrowser, node-commander, sourceosctl, Agent Machine, model routers, local-first sync services, and browser/terminal automation.
4. Add CI that blocks runtime-bearing repos without a trust surface.
5. Build an estate trust graph that ingests all trust surfaces.

## Acceptance criteria

A runtime component is trust-surface compliant when a reviewer can answer these questions from the repo alone:

- What authority does this component gain on a user machine?
- What processes, services, ports, containers, sockets, mounts, credentials, and logs does it create?
- What can it read, write, execute, call, or control?
- How does a user revoke that authority?
- How do we prove it is gone after uninstall?
- What would be suspicious if it reappeared?
