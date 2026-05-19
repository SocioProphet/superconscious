# Claim-Status Ledger — superconscious hardening audit

**Status:** H3 audit ledger.  
**Date:** 2026-05-19.  
**Scope:** High-risk surfaces in `SocioProphet/superconscious` that could be misread as stronger than their actual evidence level.

## 0. Ledger rule

This ledger does not decide whether an artifact is valuable. It records what an artifact is allowed to claim.

Allowed normalized statuses:

```text
runtime_verified
schema_validated_shape_only
structural_doctrine
computational_diagnostic
proof_review_required
theorem_track_candidate
exploratory_noncanonical
superseded_content_captured
superseded_content_not_yet_captured
quarantine_pending_review
```

Forbidden inference patterns:

```text
CI green => semantically verified
schema passes => invariant verified
doctrine-bound => runtime enforced
theorem framing => theorem proved
scaffold-supported => direct computation complete
prototype self-test => canonical implementation
```

## 1. Tier 2 binding surfaces

| Artifact path | Claim surface | Normalized status | Evidence required for promotion | Owning plane | Next action |
|---|---|---:|---|---|---|
| `docs/composition/TIER2_INVARIANT_BINDINGS.md` | Cross-repo Tier 2 binding doctrine | `structural_doctrine` | ProCybernetica source pin; adopt/defer table; explicit local non-claims | ProCybernetica canonical, superconscious consumer | Source pin and schema-only boundary landed in PR #40; maintain on future mode changes. |
| `schemas/composition/m1-tier2-binding.v1.json` | M1 Tier 2 binding declaration | `schema_validated_shape_only` | Runtime receipt lookup, artifact resolution, ProCybernetica composition-certificate instantiation | superconscious local schema | Keep as Layer 1 declaration shape only. |
| `schemas/composition/m5-tier2-binding.v1.json` | M5 public-note Tier 2 binding declaration | `schema_validated_shape_only` | Publication gate evidence, peer-review evidence, runtime receipt lookup | superconscious local schema | Keep as Layer 1 declaration shape only. |
| `schemas/composition/interpretability-harness-tier2-binding.v1.json` | 14-fragment interpretability release binding | `schema_validated_shape_only` | Runtime provider/source verification, artifact resolution, steering/execution evidence | superconscious local schema | Add explicit schema-only boundary in follow-up if not already mirrored in schema description. |
| `schemas/composition/lawful-learning-trust-surface-tier2-binding.v1.json` | Lawful-learning trust-surface binding | `schema_validated_shape_only` | Circuit discovery, ablation verification, tag-promotion evidence, substrate verification | superconscious local schema | Keep as Layer 1 declaration shape only. |
| `docs/composition/TIER2_BINDING_SCHEMA_BOUNDARY.md` | Local interpretation rule for Tier 2 binding schemas | `structural_doctrine` | None for current use; must be kept aligned with new schemas | superconscious | Apply to all future Tier 2 binding schemas. |

## 2. Interpretability and Neuronpedia surfaces

| Artifact / PR | Claim surface | Normalized status | Evidence required for promotion | Owning plane | Next action |
|---|---|---:|---|---|---|
| PR #37 `Add Neuronpedia v0.1 schema tranche with fixture naming` | Neuronpedia ArtifactSourceLock / ProviderBinding / InterventionSpec schema tranche | `quarantine_pending_review` | Polarity proof, negative-fixture failure evidence, Layer 2 issue tracking, source/authenticity non-claims | superconscious schema lane, future runtime/source verifier elsewhere | Remain draft until readiness gate is recorded. |
| `schemas/neuronpedia/artifact-source-lock.v0.1.json` on PR #37 branch | Artifact source lock structure | `schema_validated_shape_only` if merged | Source existence, content-hash match, provider authenticity, decomposition correctness | superconscious schema lane | Keep only with source-verification non-claims and Layer 2 tracker. |
| `schemas/neuronpedia/provider-binding.v0.1.json` on PR #37 branch | Provider binding declaration | `schema_validated_shape_only` if merged | Provider trust, live fetch authorization, provider writeback, claim promotion | superconscious schema lane | Keep as declaration only; no authority escalation. |
| `schemas/neuronpedia/intervention-spec.v0.1.json` on PR #37 branch | Intervention plan declaration | `schema_validated_shape_only` if merged | Execution authority, live mutation, behavioral claim promotion, safety claim | superconscious schema lane | Keep as review/spec object only. |
| `docs/moat-claim.md` | Governed interpretability composition moat | `structural_doctrine` | Runtime/source/harness evidence for any public claim | superconscious + ProCybernetica boundary | Keep as doctrine; ensure it does not overclaim runtime moat. |
| `docs/interpretability-harness-architecture.md` | Generalized harness architecture | `structural_doctrine` | Runtime adapter implementation and evidence receipts for execution claims | superconscious | Keep; ensure provider-boundary language remains fail-closed. |

## 3. Lawful-learning theorem and theorem-pattern surfaces

These are the highest semantic-risk surfaces because theorem-facing language can outpace review evidence.

| Artifact path | Claim surface | Current risk | Normalized status | Evidence required for promotion | Next action |
|---|---|---|---:|---|---|
| `docs/proofs/a1-gate-minimality-faithful.md` | Faithful A1 proof note / T2' framing | May be theorem-facing | `proof_review_required` | Independent proof review or demotion to theorem-track candidate | Review before downstream citation. |
| `docs/lawful-learning/09-t2-prime-polarization-scope.md` | T2' predicate interpretation doctrine | Theorem-reuse boundary could be read as proof certification | `structural_doctrine` plus `proof_review_required` for theorem claims | Proof review for mathematical assertions; doctrine can remain | Split doctrine from proof claims if needed. |
| `docs/lawful-learning/10-a2-gate-minimality-scoping.md` | A2 structural theorem framing | Uses theorem-level language while direct Stokes-side computation remains open | `theorem_track_candidate` pending review | Direct proof review for structural theorem; direct Stokes computation for numerical harness | Demote from theorem-level doctrine unless proof evidence is recorded. |
| `docs/lawful-learning/11-an-unified-gate-minimality-theorem.md` | Unified A_n theorem pattern | Pattern may be read as proved theorem family | `theorem_track_candidate` pending review | Proof review for A_n statement; parametric harness evidence | Demote title/status or add proof-review gate. |
| `docs/lawful-learning/12-d4-c7-prime-scoping.md` | D4/ADE extension scoping | Correctly appears scoping, but may inherit theorem track by proximity | `structural_doctrine` | D4 construction/proof if promoted | Keep as scoping; guard against promotion. |
| `docs/lawful-learning/13-d4-representation-inventory.md` | D4 representation inventory | Contains representation claims requiring math review | `proof_review_required` for structural claims; `structural_doctrine` for inventory role | Independent representation-theory review | Keep inventory; verify high-load-bearing claims. |
| `docs/lawful-learning/14-d4-strategy-b-scoping.md` | D4 Strategy B scoping | Strategy could be mistaken for construction | `structural_doctrine` / `theorem_track_candidate` for any theorem-facing claims | Candidate realization and proof before promotion | Keep as scoping only. |
| `harness/coxeter_a2_harness.py` | A2 scaffold harness | Passing predicates may be mistaken for direct Stokes proof | `computational_diagnostic` | Direct Stokes-side computation and receipt if promoted | Keep scaffold; prohibit proof promotion. |
| `harness/fuss_catalan_verification.py` | Inverse-radius verifier | Useful but not direct Stokes computation | `computational_diagnostic` | Direct Stokes witness for Coxeter jump | Keep; label as supporting diagnostic only. |

## 4. Lawful-learning governance/schema surfaces

| Artifact group | Claim surface | Normalized status | Evidence required for promotion | Next action |
|---|---|---:|---|---|
| `schemas/lawful-learning/*.json` | Lawful-learning local schema lane | `schema_validated_shape_only` | Runtime invariant execution, cross-plane evidence resolution | Keep with shape-only interpretation. |
| `scripts/check-lawful-learning.py` | Structural checker over fixtures / trust-surface example | `computational_diagnostic` / structural guardrail | Runtime execution and evidence receipts for real-world claims | Keep as structural checker. |
| `examples/TRUST_SURFACE.lawful-learning.yaml` | Example trust-surface declaration | `schema_validated_shape_only` / `structural_doctrine` | Live source/evidence resolution if used operationally | Keep example-only. |
| Phase 2-6 lawful-learning docs | Governance doctrine | `structural_doctrine` | Runtime/evidence validation for operational claims | Keep; gate theorem language separately. |
| Phase 8 status update | Cross-repo status doc | `structural_doctrine` | Cross-repo citation pin and verification | Keep if pinned to SocioSphere merge state. |

## 5. SPO / Baez algebra prototype branch

| Branch / artifact | Claim surface | Normalized status | Evidence required for promotion | Next action |
|---|---|---:|---|---|
| `capture/spo-baez-algebra-engine` | Exploratory SPO/Baez algebra bridge | `exploratory_noncanonical` | Explicit claim that it does not implement actual SPO recursion; math review for algebra; prototype tests | Keep quarantined unless replayed as exploratory artifact. |
| `docs/exploratory/spo-baez-algebra-engine.md` | Exploratory explanatory bridge | `exploratory_noncanonical` | None for exploratory capture; proof/semantic claims require separate review | Keep only with non-canonical label. |
| `prototypes/spo/spo_activation_engine.py` | Cayley-Dickson / carrier-mode prototype | `computational_diagnostic` / `exploratory_noncanonical` | Full SPO subject-predicate-object recursion implementation if claimed | Do not merge as canonical engine. |

## 6. Branch and supersession surfaces

Branch reconciliation requires exact comparison before deletion. These initial dispositions are provisional until H6 branch audit completes.

| Branch | Initial disposition | Reason |
|---|---:|---|
| `feat/neuronpedia-schema-bumps-v01` | `quarantine_pending_review` | Open PR #37 is draft; keep until readiness gates pass. |
| `feat/neuronpedia-schema-bumps-v01-main` | `superseded_content_captured` if identical to main; verify before deletion | Prior compare showed identical to main; re-check before cleanup. |
| `capture/spo-baez-algebra-engine` | `exploratory_noncanonical` | Useful but not canonical; requires explicit quarantine label. |
| `copilot/integrate-superconscious-cognition-loop` | `superseded_content_not_yet_captured` | Ahead-of-main runtime/cognition-loop content; must review before closure. |
| `doctrine/architecture-falsification-v0-1` | `superseded_content_not_yet_captured` | Architecture/falsification docs may be useful; needs capture review. |
| `lawful-learning-capture-v1` | `superseded_content_not_yet_captured` | Source-ledger and README content must be checked against current main. |
| `lawful-learning-runtime-package` | `superseded_content_not_yet_captured` | Runtime package files are ahead of main; must review authority implications. |
| `lawful-learning-t2-prime-doctrine` | `superseded_content_not_yet_captured` | Likely superseded by current branch/PR #30 but must verify. |
| `lawful-learning-t2-prime-doctrine-current` | `superseded_content_not_yet_captured` | Likely mostly merged in current main; compare before deletion. |
| `m0-m15-certificate-chain` | `superseded_content_not_yet_captured` | Superseded by #9 according to PR history; verify path-level capture. |
| `m0-m15-certificate-chain-current` | `superseded_content_not_yet_captured` | Superseded by #9 but still ahead in compare; verify path-level capture. |

## 7. Promotion gates

### 7.1 From `schema_validated_shape_only` to stronger status

Requires at least one of:

```text
runtime resolver
receipt lookup evidence
artifact existence check
hash dereference check
source authenticity evidence
cross-field semantic checker over real artifacts
```

### 7.2 From `computational_diagnostic` to stronger status

Requires:

```text
pinned protocol
reference inputs
reference outputs
negative controls
receipt/hash manifest
claim boundary stating what the diagnostic can and cannot license
```

### 7.3 From `theorem_track_candidate` or `proof_review_required` to theorem-facing status

Requires:

```text
self-contained proof note
explicit definitions
lemma dependency list
known-obstruction discussion
independent proof review or formalization plan
non-claim list for what is not proven
```

### 7.4 From `exploratory_noncanonical` to canonical implementation

Requires:

```text
clear functional specification
unit tests that test the claimed function, not only a surrogate
claim-boundary doc
negative tests for forbidden interpretations
owner-plane assignment
```

## 8. Immediate H4 theorem-language targets

The next hardening PR should process these first:

```text
docs/lawful-learning/10-a2-gate-minimality-scoping.md
docs/lawful-learning/11-an-unified-gate-minimality-theorem.md
docs/proofs/a1-gate-minimality-faithful.md
docs/lawful-learning/13-d4-representation-inventory.md
```

Minimum action:

```text
replace theorem-level status with theorem-track candidate unless proof-review evidence is cited;
keep computational scaffold language separate from direct computation;
retain direct Stokes-side computations as open non-claims;
forbid downstream promotion without proof-review gate.
```

## 9. Ledger maintenance

This ledger must be updated when:

```text
a high-risk artifact is added;
a claim status changes;
a branch is merged, closed, or deleted;
a proof review lands;
a runtime verifier lands;
a schema-only declaration becomes backed by runtime evidence.
```

No high-risk artifact may be treated as hardened unless it appears in this ledger or in a successor claim-status registry.
