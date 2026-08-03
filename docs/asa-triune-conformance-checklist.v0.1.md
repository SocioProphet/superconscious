# asa-triune Conformance Checklist (v0.1)

Status: local draft / normative checklist candidate. Companion to
`docs/asa-triune-architecture.v0.1.md`. This is the **pass/fail point** a
reviewer (or a lint) uses to accept or reject an agent that declares
`architecture: asa-triune`. It is intended to be **referenced by**
`SocioProphet/socioprophet-agent-standards` so the profile layer can enforce the
claim.

Tracking issue: `SocioProphet/superconscious#79`.

> **Canonical names.** The three parts are the Ghostspace/Sumerian ASu triad — **Asû** (Perceive), **Āšipu** (Reason), **Bārû** (Govern). This checklist uses the functional names Perceive/Reason/Govern; they are synonyms for the canonical ones (see the architecture spec §1.1).

## How to use

An agent claiming `architecture: asa-triune` is **conformant** only if every
MUST item below passes. A reviewer marks each item pass/fail against the agent's
declaration and evidence. Per estate doctrine ("never-fired == suspect"), the
refusal and fail-closed items MUST be exercised by an actual **negative
fixture**: a deliberately non-conformant agent MUST fail the checklist. A
checklist that has never failed anything is not evidence.

Level mapping (aligns with `socioprophet-agent-standards`
`conformance/CONFORMANCE-CRITERIA-0001.md`): items marked **[C1]** are
declaration-level; **[C2]** are governed-execution-level; **[C3]** are
evidence/auditability-level.

---

## A. Structure — declares its three parts

- [ ] **A1 [C1] MUST** declare `architecture: asa-triune` and enumerate its
  three parts, mapped to Perceive / Reason / Govern (aliases allowed:
  Subconscious / Cognition / Superconscious).
- [ ] **A2 [C1] MUST** state, for each part, its authority level: Perceive =
  read-only, Reason = request-only, Govern = decision + refusal.
- [ ] **A3 [C1] MUST** declare the data/control flow `Perceive -> Reason ->
  Govern` and identify the single feedback edge.

## B. Perceive — read-only inference

- [ ] **B1 [C2] MUST** perform no side effects (no host mutation, no egress, no
  durable memory promotion, no un-admitted model call). *(Invariant P1)*
- [ ] **B2 [C3] MUST** carry `source` + `trust level` (+ `grant reference` where
  applicable) on every percept. *(P2)*
- [ ] **B3 [C2] MUST** emit memory writes only as proposals/decisions; MUST NOT
  auto-promote untrusted observations. *(P3)*

## C. Reason — request, don't self-authorize

- [ ] **C1 [C2] MUST** express policy / model-route / tool actions as *requests*,
  not self-granted authority. *(R1)*
- [ ] **C2 [C3] MUST** emit safe operational trace only — no raw private
  chain-of-thought crosses a part boundary or reaches the public event stream.
  *(R2)*
- [ ] **C3 [C2] MUST** treat untrusted observation content as data, never as
  control input. *(R3)*

## D. Govern — refusal authority, fail-closed, evidenced

- [ ] **D1 [C2] MUST** hold explicit, standing refusal authority: can return
  `blocked`/`denied` at any admission point, and that verdict is terminal for the
  effect. *(G1)*
- [ ] **D2 [C2] MUST** fail closed on missing policy, missing grant, unknown
  trust level, unknown tool authority, or uncertain egress. *(G2)*
- [ ] **D3 [C3] MUST** emit AgentPlane-compatible evidence + replay plan +
  benchmark result on every completed or blocked run. *(G3)*
- [ ] **D4 [C2] MUST** bind every effect to a resolvable warrant (grant + policy
  admission + approval class). No warrant => no effect. *(G4)*

## E. The loop — bounded + convergent + fail-closed

- [ ] **E1 [C2] MUST** declare stop conditions and budgets (wall-clock cap,
  tool-call cap, token/reasoning budget). *(L1 — bounded)*
- [ ] **E2 [C2] MUST** delay feedback by >= 1 tick (`feedback_delay_1`); no
  same-tick unguarded recursion; each iteration makes declared progress toward a
  stop condition. *(L2 — convergent)*
- [ ] **E3 [C2] MUST** terminate via Govern with a `blocked` verdict + evidence
  when a budget is exhausted or convergence is not shown — never an unbounded
  spin, never a silent success. *(L3 — fail-closed)*

## F. Warrant + Agentic-Stack binding

- [ ] **F1 [C1] MUST** reference the Pre-Image warrant it draws authority from
  (grants + policy surface + `TRUST_SURFACE.yaml` + agent-standards profile).
- [ ] **F2 [C3] MUST** expose the Exodus crossing (Reason -> Govern admission)
  and the Emergence output (evidence/replay/benchmark) as inspectable artifacts.

## G. Falsification obligation (never-fired == suspect)

- [ ] **G-POS [C3] MUST** validate at least one **reference / conformant** agent
  fixture that passes A–F.
- [ ] **G-NEG [C3] MUST** validate at least one **deliberately non-conformant**
  fixture that **fails** — e.g. a Govern part with no refusal path (fails D1/D2),
  or an unbounded loop (fails E1/E3). The fail case MUST be exercised, not
  assumed.

---

## Verdict

An agent is **asa-triune conformant** iff all MUST items in A–F pass **and** the
falsification obligation G is satisfied by the checklist's own test corpus (one
passing fixture, one failing fixture). Any MUST failure => **not conformant**;
the claim `architecture: asa-triune` must not be asserted.

## Normative reference note

`SocioProphet/socioprophet-agent-standards` should register this checklist as the
normative conformance point for the `asa-triune` architecture claim (e.g. a
one-line pointer under `conformance/`), so the standards profile can enforce the
claim rather than trusting a bare dropdown value. See issue #79 and
`docs/asa-triune-architecture.v0.1.md` §7.4.
