# SourceOS Interaction Reference Flow

Status: downstream reference pointer  
Canonical packet: `SourceOS-Linux/sourceos-spec#118`  
Canonical manifest: `examples/interaction-flow/noetica-superconscious-agentplane-agentterm.flow.json`

## Superconscious role

Superconscious is the task-boundary coordinator for the SourceOS interaction substrate.

The canonical reference flow is:

```text
Noetica creates SourceOSInteractionEvent
  -> Superconscious records task-boundary refs
  -> AgentPlane records evidence refs
  -> AgentTerm displays the governance trace
```

## Local references

- Boundary doc: `docs/integrations/sourceos-interaction-boundary.md`
- Boundary schema: `schemas/integrations/sourceos-interaction-boundary.v1.json`
- Boundary check: `python3 scripts/check_sourceos_interaction_boundary.py tests/fixtures/integrations/sourceos-interaction-boundary.valid.json`

## Boundary

Superconscious records task-boundary references. The schema remains owned by `SourceOS-Linux/sourceos-spec`; evidence records, policy decisions, identity grants, memory context, and display surfaces remain in their respective planes.
