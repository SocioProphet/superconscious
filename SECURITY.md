# Security

Superconscious is specification-first and should not run background services, open sockets, persist credentials, call model providers, or execute tools by default.

## Security posture

The default posture is deny-by-default:

- no background daemon;
- no LaunchAgent, LaunchDaemon, systemd unit, cron job, or scheduled task;
- no listening socket;
- no browser/CDP/noVNC control surface;
- no terminal or shell execution;
- no credential storage;
- no model-provider calls;
- no network egress;
- no host mounts;
- no workspace writes;
- no auto-update feed;
- no remote feature flag authority.

Any pull request that changes this posture must update `TRUST_SURFACE.yaml` and explain the new authority in the PR description.

## Trust surface requirements

Runtime-bearing repos in the SocioProphet / SourceOS / SociOS estate should include:

```text
TRUST_SURFACE.yaml
scripts/doctor
scripts/network-surface
scripts/credential-surface
scripts/policy-surface
scripts/purge
scripts/prove-clean
```

Superconscious currently seeds this requirement through:

```text
schemas/trust-surface.schema.json
docs/trust-surface-protocol.md
docs/trust-surface-rollout.md
examples/TRUST_SURFACE.node-commander.yaml
scripts/validate-trust-surface.py
.github/workflows/trust-surface.yml
```

## Reporting security issues

Open a GitHub issue for non-sensitive security design gaps.

Do not paste secrets, tokens, private keys, cookies, OAuth material, local auth files, private logs, or machine-identifying sensitive data into issues.

For sensitive reports, use a private channel controlled by the repository owner until GitHub private vulnerability reporting is configured for the estate.

## Review rules

Block changes that introduce any of the following without a trust-surface update:

- process persistence;
- local or remote listeners;
- model/provider credentials;
- OAuth refresh/token storage;
- browser, CDP, noVNC, or dashboard control;
- terminal/shell/exec/subagent execution;
- container/VM/Kubernetes runtime behavior;
- host mounts or writes outside the workspace;
- updater feeds or plugin installers;
- remote feature flags that change local behavior;
- logs, traces, status output, or UI that may expose secrets.

## Cleanup and revocation standard

Any component that gains local authority must provide a purge path and prove-clean path.

`purge` removes authority.

`prove-clean` verifies the absence of processes, launch items, sockets, containers, credentials, caches, logs, update artifacts, and service-token drift.
