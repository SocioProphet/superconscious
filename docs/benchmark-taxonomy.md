# Benchmark Taxonomy

Superconscious benchmarks must produce evidence, not just scores.

## Benchmark classes

| Class | Purpose |
|---|---|
| `browser` | Browser task execution, navigation, extraction, and web-agent safety. |
| `terminal` | Terminal task planning, command safety, and operator UX. |
| `repo` | Repository editing, tests, diffs, and PR-readiness workflows. |
| `office` | Document, spreadsheet, slide, and artifact generation workflows. |
| `mcp` | MCP server trust, grant, and tool-call correctness. |
| `memory` | Memory proposal, quarantine, recall, and revocation behavior. |
| `policy` | Denial, approval, fail-closed, and source-exposure behavior. |
| `model-route` | Local-first routing, fallback, egress denial, and route evidence. |
| `replay` | Exact, best-effort, evidence-only, and non-replayable classifications. |

## Benchmark result requirements

Every result must include:

- benchmark id;
- run id;
- input task hash;
- assertion list;
- pass/fail;
- evidence refs;
- replay class;
- evaluator type;
- timestamp.

## Evaluator priority

1. Deterministic assertions.
2. Structured artifact validation.
3. Golden output comparison.
4. Screenshot or visual judgment only when deterministic checks are impossible.
5. LLM judge only as a last resort and always with model-route evidence.

## M1 benchmark

M1 includes only `m1-deterministic-smoke`, which asserts:

- run completed;
- safe trace mode is operational-only;
- five required artifacts exist.
