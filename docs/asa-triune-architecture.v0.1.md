# asa-triune Agent Architecture (v0.1) — the Sumerian Asû-triune (asû · āšipu · bārû)

Status: local draft / grounding spec. Proposes a v0.1 definition for owner
confirmation. This document adds **no runtime authority**: it does not modify the
M1 runner, and does not authorize network calls, model calls, host mutation,
durable memory promotion, browser automation, or terminal execution.

Home rationale: filed and specified in `SocioProphet/superconscious` because
`asa-triune` maps directly onto the superconscious governed-cognition loop
(`ARCHITECTURE.md` -> "Core loop"). The **conformance checklist** derived here
(`docs/asa-triune-conformance-checklist.v0.1.md`) is the normative
pass/fail point and is intended to be **referenced by**
`SocioProphet/socioprophet-agent-standards` so the profile layer can enforce the
claim.

Tracking issue: `SocioProphet/superconscious#79`.

---

## 1. Problem this document closes

`asa-triune` currently exists only as a selectable value in the
agent-configuration UI. A code search across `SocioProphet`, `SourceOS-Linux`,
and `SociOS-Linux` (`gh search code "asa-triune"`) returns **no definition** —
no schema, no invariants, no conformance criteria. An architecture that can be
*selected* but not *specified* cannot be governed or claimed truthfully: it is a
label without teeth.

This document grounds `asa-triune` as a real architecture: it names the three
parts, states the invariants each part must satisfy, defines how they compose,
and maps them onto the superconscious loop (which **admits loops** with refusal
authority) and the Agentic Stack (Pre-Image -> Exodus -> Emergence).

### 1.1 Canonical name and derivation (owner-confirmed 2026-08-03)

`asa-triune` is **not** an "Agentic-Stack Agent" acronym (an earlier draft
proposed that and flagged it for confirmation). Its canonical source is the
**Ghostspace Modeling Framework**, with the **Sumerian Asû** as the etymological
root.

**Ghostspace (estate source).** Ghostspace is a symbolic-topological modeling
language for recursive information systems whose primitives are **trits →
triadic relation → simplex → ASu unit**, together with S-layer strata and the
lifecycle **projection / collapse / re-anchoring / accreditation / discrediting**
under **claim-boundary discipline**. `ASu` is Ghostspace's core unit — a triadic
construct formed by trit activation, triad closure, and simplex formation. This
is the SAME trit substrate the estate's TritRPC / quantum-prophet rail carries
(balanced-ternary, qutrit-projectable), so `asa-triune` is not a loose metaphor:
the agent's three parts are the runtime realization of the Ghostspace ASu triad,
and its truth/claim discipline is Ghostspace's accreditation/discrediting made
governable.

**Sumerian root.** The name descends from the **Mesopotamian healer-seer triad** —
the three practitioners who between them sensed, diagnosed, and pronounced —
which is why the ASu triad reads so naturally as three agent roles:

| Sumerian role | Historical practice | Ghostspace / asa-triune part (function) |
|---|---|---|
| **Asû** (asû) — the physician | Empirical, materia-medica healer; treats from observed evidence | **Perceive** — read-only empirical inference (trit activation) |
| **Āšipu** (āšipu) — the exorcist / diagnostician | Reads the *cause*; interprets and proposes the remedy | **Reason** — request/propose (triad closure → diagnose, plan) |
| **Bārû** (bārû) — the diviner / seer | Reads the omens and pronounces the verdict / prognosis | **Govern** — decision + refusal authority (ASu collapse / re-anchoring) |

The stem **asa-** is **asû** (the empirical, sensing root and Ghostspace's ASu);
**-triune** is the three-in-one of asû + āšipu + bārû. Throughout this spec the
Sumerian/Ghostspace names are the **canonical identity** and Perceive / Reason /
Govern are the **functional descriptors** — synonyms, used interchangeably. The
*three-ness* is canonical (three historical roles; the ASu triad), which is why
the architecture is a triune, not the estate's bare two planes; the three map
cleanly onto the superconscious loop below.

> **Provenance note.** The Ghostspace framework and its artifacts (schema/OWL/
> SHACL/SPARQL/simulator/runtime/replay bundles) are a separate workstream
> captured in the "Ghostspace Modeling Framework" doc; landing `ghostspace-spec`
> as a repo (and mapping ASu-collapse to `asa-triune`'s Govern step formally) is
> tracked as follow-on, pending those artifacts.

### Honesty ledger (proposed vs cited)

This spec separates what the estate already defines from what this document
proposes for confirmation.

| Element | Status | Basis |
|---|---|---|
| The name **`asa-triune`** — the **Ghostspace ASu** triad (asû · āšipu · bārû) | **CITED (owner canonical, 2026-08-03)** | Canonical source is the **Ghostspace Modeling Framework** (ASu = trit→triad→simplex unit); etymological root is the Sumerian **Asû** (physician). Supersedes the earlier proposed "Agentic-Stack Agent" expansion. See §1.1. |
| Grounding of ASu in the **estate trit substrate** | **CITED** | Ghostspace's trits are the same balanced-ternary the TritRPC / quantum-prophet rail carries; ASu's collapse/re-anchoring/accreditation map onto Govern's admit/refuse + evidence. Formal `ghostspace-spec` mapping is follow-on (artifacts pending). |
| A **three-part** decomposition | **CITED (canonical triad)** | The three-ness is canonical to the Sumerian tradition — three distinct historical roles (asû sense, āšipu diagnose, bārû pronounce). The earlier tension ("the estate README names only two planes") is resolved: the triad supplies the third, and the three map onto the superconscious loop (`ARCHITECTURE.md` core loop). |
| Part names **Asû / Āšipu / Bārû** (functional: Perceive / Reason / Govern) | **CITED (canonical) + functional descriptors** | Sumerian names are the canonical identity; Perceive / Reason / Govern are the functional synonyms used throughout (aliases: Subconscious / Cognition / Superconscious). |
| Invariants (fail-closed, bounded-convergent loop, provenance carry, safe trace, refusal authority) | **CITED** | Drawn from `AGENTS.md`, `THREAT_MODEL.md`, `docs/safe-operational-traces.md`, `docs/behavior-calculus.md`, `docs/downstream-integration-contracts.md`. |
| Bounded + convergent + fail-closed **loop doctrine** | **CITED (estate doctrine) + mechanized here** | Estate doctrine: loops must be bounded + convergent + fail-closed and superconscious *admits* loops with refusal authority. Mechanized via `feedback_delay_1` from `docs/behavior-calculus.md`. |
| Mapping to Agentic Stack **Pre-Image -> Exodus -> Emergence** | **PROPOSED (layer names cited, contracts not)** | The three layer names come from the Agentic Stack integration spec; their precise per-layer contracts are owned by that spec and are **not** reproduced in the estate at a level this doc could cite verbatim. The mapping below is defensible but **needs Agentic-Stack owner confirmation**. |

---

## 2. What `asa-triune` is

`asa-triune` is an **agent architecture claim**: an agent that declares
`architecture: asa-triune` asserts that its cognition is realized as **three
governed subprocesses** — **Perceive**, **Reason**, **Govern** — composed as a
**single bounded, convergent, fail-closed correction loop** in which the Govern
part holds **refusal authority**.

Each part is a typed deterministic subprocess in the sense of the repo's
behavior calculus (`docs/behavior-calculus.md`):

```text
Proc<I, O, S>   step : S x I -> O x S
```

The three are not independent agents; they are the **three faces of one governed
agent**. "Triune" is used in its plain sense — three distinct parts, one
identity — matching the estate's existing "Triune" naming family
(`socioprophet-standards-storage/docs/standards/triune-agent-mesh`) without
importing that framework's runtime obligations.

### 2.1 The three parts

#### Part 1 — Asû · Perceive (alias: Subconscious)

| Field | Value |
|---|---|
| Role | Recursive inference over inputs, memory, and validation history. Turns raw observations into typed, provenance-tagged percepts and candidate plans. |
| Authority | **Read-only.** Proposes; never authorizes. May *recommend*, may *bias* planning, may *remember-as-proposal*. |
| Source in repo | `README.md`: "Subconscious optimizes recursive inference"; `docs/SVF_VALIDATION_HISTORY_CONSUMER.md` (read-only validation-history memory consumer); `ARCHITECTURE.md` core-loop `validate` + `MemoryDecision.proposed`. |

#### Part 2 — Āšipu · Reason (alias: Cognition)

| Field | Value |
|---|---|
| Role | Plan and decompose the task tree, select a skill, request a model route, request policy admission, and propose memory handling. This is the visible governed cognition loop. |
| Authority | **Request-only.** Emits *requests* and *proposals* (policy request, model-route request, skill selection, memory proposal). It does not itself decide admission. |
| Source in repo | `ARCHITECTURE.md` "Core loop"; `docs/safe-operational-traces.md`; the "M1 runner" fixed loop in `docs/behavior-calculus.md`. |

> **Canonical middle role.** Āšipu — the diagnostician who reads the cause and
> proposes the remedy — is the canonical middle of the Sumerian triad, so the
> three-part split is not an invention: it is the tradition. It also maps to the
> estate loop's `request/propose` phase between read-only inference (Asû) and
> admission/effect (Bārû). If an implementation collapses to two planes, Āšipu
> folds into Bārû's pre-decision stage; the conformance checklist still holds
> because its items are phrased over responsibilities, not part-count dogma.

#### Part 3 — Bārû · Govern (alias: Superconscious)

| Field | Value |
|---|---|
| Role | Admission and effect: decide policy, obtain approval, gate, run the tool through the adapter, then emit evidence, replay plan, and benchmark result. |
| Authority | **Decision + refusal.** Holds **refusal authority**: the standing power to block, abstain, or fail closed. Every effect crosses this boundary. |
| Source in repo | `README.md`: "Superconscious governs recursive agency"; `AGENTS.md` "Fail closed on missing policy, missing grants, unknown trust level…"; `THREAT_MODEL.md` (fail-closed non-negotiables, approval classes incl. `denied` = "must fail closed"); `docs/downstream-integration-contracts.md` ("must fail closed when grants are missing"). |

### 2.2 Alias table

| asa-triune part | Estate alias | Issue-vocabulary alias | Loop phase (ARCHITECTURE.md) |
|---|---|---|---|
| Asû · Perceive | Subconscious | sense | validate, MemoryDecision.proposed |
| Āšipu · Reason | Cognition | decide | plan, PolicyCheck.requested, ModelRoute.requested, SkillActivation.selected |
| Bārû · Govern | Superconscious | act (admit/refuse) | PolicyCheck.decided, ToolUse.observed, Evidence.emitted, ReplayPlan.emitted, ReasoningRun.blocked |

---

## 3. Invariants

Invariants are stated in checkable terms; the conformance checklist
(`docs/asa-triune-conformance-checklist.v0.1.md`) turns each into a pass/fail
item.

### 3.1 Per-part invariants

**Perceive**
- P1. **No side effects.** No host mutation, no egress, no durable memory
  promotion, no model call that leaves the device without a Govern-admitted
  route. (`THREAT_MODEL.md` M1 non-negotiables.)
- P2. **Provenance carry.** Every percept carries `source`, `trust level`, and,
  where relevant, `grant reference`. Untrusted observations stay untrusted.
  (`AGENTS.md` "Every tool call must include source, trust level, grant
  reference…"; `THREAT_MODEL.md` trust zones.)
- P3. **Propose-only memory.** Every memory write is a proposal or explicit
  decision; never auto-promotion of untrusted observations. (`AGENTS.md`.)

**Reason**
- R1. **Request, don't self-authorize.** Reason emits policy/model-route/tool
  *requests*; it must not treat its own plan as admission.
- R2. **Safe operational trace only.** Emits task decomposition, selected skill,
  tool requested, decision summaries — **not** raw private chain-of-thought.
  (`docs/safe-operational-traces.md`; `THREAT_MODEL.md` non-negotiable #1.)
- R3. **Separation of instructions from observations.** Content from untrusted
  observations is treated as data, never as control input. (`THREAT_MODEL.md`
  prompt-injection mitigation.)

**Govern**
- G1. **Refusal authority is explicit and standing.** Govern can return
  `blocked`/`denied` at any admission point, and that verdict is terminal for
  the effect. (`THREAT_MODEL.md` approval class `denied`; `ARCHITECTURE.md`
  `ReasoningRun … blocked`.)
- G2. **Fail closed.** Missing policy, missing grant, unknown trust level,
  unknown tool authority, or uncertain egress posture => refuse.
  (`AGENTS.md`; `docs/downstream-integration-contracts.md`.)
- G3. **Evidence + replay + benchmark on every run.** Every completed or blocked
  run emits AgentPlane-compatible evidence, a replay plan, and a benchmark
  result. (`README.md` M1 deliverable; `AGENTS.md` "Every run must include a
  replay plan and benchmark result".)
- G4. **Warrant-bound effect.** Every effect is bound to a resolvable warrant:
  a grant (`agent-registry`) + policy admission (`guardrail-fabric`) + approval
  class (`THREAT_MODEL.md`). No warrant => no effect.

### 3.2 Whole-loop invariants (the correction loop)

The three parts compose into a correction loop. Per estate doctrine, that loop
must be **bounded + convergent + fail-closed**:

- L1. **Bounded.** The loop declares stop conditions and budgets — wall-clock
  cap, tool-call cap, token/reasoning budget. (`THREAT_MODEL.md` "Budget
  runaway" mitigation: "Reasoning budgets, wall-clock caps, tool-call caps, and
  stop conditions".)
- L2. **Convergent.** Feedback is **delayed by at least one tick**
  (`feedback_delay_1` from `docs/behavior-calculus.md`): "No same-tick unguarded
  recursion is allowed in v0." Each iteration must make declared progress toward
  a stop condition, or the loop terminates.
- L3. **Fail-closed on exhaustion.** If a budget is exhausted or convergence is
  not shown, the loop terminates via Govern with a `blocked` verdict and
  evidence — never an unbounded spin and never a silent success.

This is precisely what it means for the superconscious to **admit** a loop:
a loop is admissible **iff** it is bounded (L1), convergent (L2), and
fail-closed (L3), and Govern (Part 3) is the refusal authority that enforces
admissibility. A DAG (identity/dependency) is acyclic and refuses cycles; a
loop (correction) is admitted only under L1–L3.

---

## 4. Composition

```text
        (Pre-Image warrant: grants + policy + trust surface + profile)
                                   |
                                   v
   +-----------+     percepts     +----------+   requests    +-----------+
   |  Perceive | ───────────────▶ |  Reason  | ────────────▶ |  Govern   |
   | (read)    |                  | (request)|               | (decide/  |
   +-----------+                  +----------+               |  refuse)  |
        ▲                                                     +-----------+
        │                                                          │
        │        feedback_delay_1  (>= 1 tick, bounded,            │ admit -> Exodus
        └──────────  convergent, fail-closed)  ◀───────────────────┘ effect + evidence
                                                                    │
                                                                    v
                                             Emergence: evidence + replay + benchmark
```

- **Serial composition** `Govern ∘ Reason ∘ Perceive` follows the behavior
  calculus serial operator (`Q ∘ P : Proc<I,O,S_P x S_Q>`). Output of one part is
  the input of the next; composite state is the product of the parts.
- **Delayed feedback** is the only cycle. Govern's verdict/evidence re-enters
  Perceive on the **next** tick (never the same tick), forming the bounded
  correction loop.
- **Observation projection** `obs : O -> O_pub` is mandatory on every edge: only
  safe operational trace crosses part boundaries into the public event stream
  (`docs/behavior-calculus.md`; `docs/safe-operational-traces.md`).

---

## 5. Mapping onto the superconscious core loop

`ARCHITECTURE.md` core loop, partitioned by part:

| Core-loop event | asa-triune part |
|---|---|
| `TaskInput`, `RunContext`, `ReasoningRun.created` | ingress (bound to Pre-Image warrant) |
| `ReasoningTask.started` (validate, decompose) | **Perceive** -> **Reason** |
| `PolicyCheck.requested`, `ModelRoute.requested`, `SkillActivation.selected`, `ToolUse.requested`, `MemoryDecision.proposed` | **Reason** (request/propose) |
| `PolicyCheck.decided`, `ModelRoute.decided`, `ToolUse.observed`, approval resolution | **Govern** (decide/refuse) |
| `Evidence.emitted`, `ReplayPlan.emitted`, `BenchmarkResult.emitted` | **Govern** (Emergence output) |
| `ReasoningRun.completed \| failed \| cancelled \| blocked` | **Govern** terminal verdict |

The two fixed loops named in `docs/behavior-calculus.md` are both asa-triune
instances: the **M1 runner** loop and the **M1.5 cognition** loop each traverse
Perceive -> Reason -> Govern and close through delayed feedback.

---

## 6. Mapping onto the Agentic Stack (Pre-Image -> Exodus -> Emergence)

> Layer names are cited from the Agentic Stack integration spec; precise
> per-layer contracts are owned there and are **not** reproduced verbatim in
> this repo. This mapping is defensible and **needs Agentic-Stack owner
> confirmation.**

| Agentic Stack layer | asa-triune reading |
|---|---|
| **Pre-Image** | The declared, warranted potential *before* a run: grants (`agent-registry`), policy admission surface (`guardrail-fabric`), the agent's `TRUST_SURFACE.yaml`, and its `socioprophet-agent-standards` profile. Perceive and Reason may only draw authority that Pre-Image warrants. |
| **Exodus** | The governed transition into effect — the Reason -> Govern admission crossing. Nothing crosses without a resolved warrant (G4); refusal (G1/G2) blocks the crossing. |
| **Emergence** | The realized, evidenced behavior — Govern's `Evidence.emitted` + `ReplayPlan.emitted` + `BenchmarkResult.emitted`. What actually happened, provable and replayable. |

---

## 7. Open questions for the owner

1. Confirm the name/expansion `asa-triune` = "Agentic-Stack Agent, triune".
2. Confirm three parts (Perceive/Reason/Govern) vs the estate's currently-named
   two planes (Subconscious/Superconscious). If two, Reason folds into Govern's
   pre-decision stage.
3. Confirm the Agentic Stack per-layer mapping in §6 against the canonical
   Agentic Stack spec.
4. Confirm home: architecture + checklist here in `superconscious`, referenced by
   `socioprophet-agent-standards`; or move the normative checklist into
   `agent-standards` and keep the mapping here (per issue #79 repo note).

## 8. References

- `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `THREAT_MODEL.md` (this repo)
- `docs/behavior-calculus.md` — Proc typing, serial/parallel composition,
  `feedback_delay_1`, observation projection, equivalence ladder
- `docs/safe-operational-traces.md` — safe-trace obligation
- `docs/SVF_VALIDATION_HISTORY_CONSUMER.md` — read-only inference consumer
- `docs/downstream-integration-contracts.md` — fail-closed on missing grants
- `SocioProphet/socioprophet-agent-standards` — profile + conformance layer that
  should reference the checklist
- Agentic Stack integration spec — Pre-Image / Exodus / Emergence layers
