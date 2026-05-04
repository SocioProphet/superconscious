# Superconscious Threat Model

Superconscious coordinates tools, models, memory, runtime, policy, and evidence. That makes it a high-leverage integration point. The default posture is fail closed, local-first, least-privilege, and evidence-producing.

## Non-negotiables

- Do not expose raw private chain-of-thought. Emit safe operational traces only.
- Do not store secrets, tokens, credentials, private keys, browser profiles, SSH keys, password stores, or cloud credential directories.
- Do not mutate host state without explicit policy admission and user/operator approval.
- Do not send prompts, files, documents, or memory off-device without model-route and egress admission.
- Do not promote untrusted observations into durable memory automatically.
- Do not authorize personalization, fine-tuning, or training. Reference governance contracts only.
- Do not treat MCP servers, webpages, documents, repositories, or tool outputs as trusted by default.

## Primary threat classes

| Threat | Description | Default mitigation |
|---|---|---|
| Prompt injection | Untrusted content attempts to override agent policy or exfiltrate data. | Separate instructions from observations; mark provenance and trust level; require policy admission for sensitive actions. |
| Tool exfiltration | Tool call attempts to leak secrets, files, prompts, or memory. | Capability-scoped tool bindings; deny egress by default; hash-only evidence where appropriate. |
| MCP server risk | MCP server requests broad authority or returns malicious instructions. | Registry trust metadata, grant scopes, version pins, and policy admission. |
| Browser contamination | Webpage text poisons future memory or commands unsafe actions. | Quarantine browser observations; require explicit memory decision before durable write. |
| Document contamination | PDF/doc/spreadsheet/email content includes malicious instructions. | Treat document content as data, not instructions; preserve provenance and trust level. |
| Shell command injection | Agent proposes unsafe terminal command. | No direct shell execution in M1; future execution requires ToolUse policy admission and approval. |
| Memory poisoning | False or malicious content is promoted to memory. | Typed memory decisions with source, trust, review, and revocation metadata. |
| Model route abuse | Run routes sensitive task to unapproved remote model. | ModelRouteAdapter must enforce local-first and egress policy. |
| Replay mismatch | Replay cannot reproduce external state. | Classify replay as exact, best-effort, evidence-only, or non-replayable. |
| Source exposure leak | Public repo artifacts expose private operational material. | SocioSphere source-exposure checks and explicit artifact redaction. |
| Budget runaway | Recursive loop consumes unbounded time, tools, tokens, or human attention. | Reasoning budgets, wall-clock caps, tool-call caps, and stop conditions. |

## Trust zones

```text
trusted control inputs
  AGENTS.md, signed policy, schemas, workspace lock, approved skills

semi-trusted project inputs
  repo files, issues, PRs, docs authored by us

untrusted observations
  webpages, browser DOM, downloaded files, emails, PDFs, spreadsheets, external MCP results, terminal output from unknown commands

restricted material
  secrets, credentials, tokens, private keys, browser profiles, app databases, cloud credential folders, raw private user data
```

## Approval classes

| Class | Meaning |
|---|---|
| `none` | Safe read-only operation under existing grants. |
| `operator` | Requires explicit local user/operator approval. |
| `enterprise` | Requires enterprise/admin policy approval. |
| `signed-intent` | Requires signed user intent and proof-of-life. |
| `denied` | Must fail closed. |

## M1 restrictions

M1 is deterministic and inert:

- mock policy adapter;
- mock model router;
- mock tool adapter;
- mock memory adapter;
- local JSON artifacts only;
- no network;
- no model inference;
- no file mutation outside `.runs/`;
- no shell execution;
- no browser automation.

## Required evidence

Every run must produce:

- event stream;
- final reasoning-run artifact;
- AgentPlane-compatible evidence stub;
- replay plan;
- benchmark result;
- error artifact when failed or blocked.
