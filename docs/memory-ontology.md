# Memory Ontology

Superconscious treats memory as typed, governed, and provenance-bound. It does not auto-promote observations into durable memory.

## Memory classes

| Class | Meaning | Default posture |
|---|---|---|
| `episodic` | Facts about a specific run, task, or interaction. | Stored as run evidence only. |
| `semantic` | General reusable knowledge. | Proposal-only until reviewed. |
| `procedural` | Skills, playbooks, and process knowledge. | Requires skill lifecycle review. |
| `preference` | User or workspace preferences. | Requires explicit approval. |
| `policy` | Governance, safety, and compliance constraints. | Authority-owned; not locally invented. |
| `environment` | Runtime, tool, repo, OS, or workspace state. | Evidence-bound and time-scoped. |
| `evidence` | Receipts, hashes, replay pointers, and run artifacts. | Always preserved for run audit. |

## Decision states

```text
proposed
quarantined
accepted
rejected
promoted
deprecated
revoked
```

## Trust levels

```text
trusted-control-input
trusted-workspace-source
semi-trusted-project-source
untrusted-observation
restricted-material
```

## M1 rule

M1 emits memory decisions as `proposal-only`. No durable memory promotion occurs.
