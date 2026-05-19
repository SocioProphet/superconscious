# Superconscious Damage Audit and Hardening Plan — 2026-05-19

**Status:** audit and containment plan.  
**Scope:** `SocioProphet/superconscious` repository surfaces affected by the recent AI-assisted governance/schema/theorem/prototype workstream.  
**Non-claim:** this document does not assert that any suspect surface is false, malicious, or unrecoverable. It classifies repo surfaces by evidence level and defines hardening work needed before those surfaces can be treated as durable governance assets.

## 0. Operating rule

We prefer **keep-but-harden** over deletion when the artifact has useful structure. The hardening standard is:

```text
useful structure may remain;
claim status must be demoted or pinned to evidence;
CI must not be allowed to masquerade as semantic verification;
external doctrine references must be commit-bound;
runtime/verification claims require actual runtime/verification code.
```

## 1. Immediate containment state

The audit starts from current `main` head:

```text
e8e9da945a5178dd7299136d04a982f38ac7c650
```

A baseline branch has been created from that exact commit:

```text
audit/2026-05-19-claude-damage-baseline
```

The open Neuronpedia tranche PR has been converted back to draft for review before merge:

```text
PR #37 — Add Neuronpedia v0.1 schema tranche with fixture naming
```

## 2. Damage model

The primary risk is not obvious destructive code. The primary risk is **semantic overpromotion**:

1. schema/fixture validation can look like invariant verification;
2. doctrine references can look like imported authority without commit pins;
3. theorem-track language can look proof-complete when it is only structural doctrine or scaffold-supported;
4. exploratory prototypes can look canonical if merged without quarantine labels;
5. CI success can create false confidence when the claim being made is semantic, mathematical, or runtime-facing.

## 3. Keep / harden / demote / quarantine matrix

| Surface class | Current posture | Hardening disposition |
|---|---:|---|
| Tier 2 binding docs and schemas | Useful shape governance | Keep, but add commit pins, schema-only disclaimers, and unresolved-mode tracking. |
| M1/M5/lawful-learning binding fixtures | Useful Layer 1 validation | Keep, but explicitly state they validate declaration shape only. |
| Interpretability harness Tier 2 binding | Useful if boundary-preserved | Keep, but verify `GNUmakefile` aggregate behavior and non-runtime claims. |
| Neuronpedia v0.1 PR #37 | Open, CI-successful, not merged | Keep as draft until polarity, non-fixture, Layer 2, and readiness checks are recorded. |
| Lawful-learning theorem/theorem-pattern docs | Highest semantic risk | Keep only after claim-status audit; demote any theorem-level language not backed by proof-review evidence. |
| SPO/Baez algebra prototype branch | Exploratory, non-main | Quarantine as non-canonical prototype unless a later PR adds explicit non-SPO-recursion and surrogate warnings. |
| Closed/unmerged superseded branches | Possible content-loss risk | Reconcile each ahead-of-main branch against current main or an explicit superseding PR. |

## 4. Claim-status hardening taxonomy

Every repo surface touched by this audit should be normalized to one of these statuses:

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
```

Forbidden ambiguity:

```text
CI green => semantically verified
schema passes => invariant verified
doctrine-bound => runtime enforced
theorem framing => theorem proved
scaffold-supported => direct computation complete
prototype self-test => canonical implementation
```

## 5. Hardening work packages

### H0 — Containment ledger

Record current main, draft-state PRs, open branches, and all ahead-of-main branches with content deltas.

Acceptance criteria:

- current main SHA recorded;
- audit baseline branch exists;
- open PR #37 is draft;
- every branch ahead of main is listed with one of: merge candidate, captured, superseded, quarantine, delete-after-capture.

### H1 — External doctrine source pinning

Any document that consumes ProCybernetica, SocioSphere, AgentPlane, Ontogenesis, SourceOS/sourceos-spec, or other repo authority must cite an immutable commit SHA or PR/merge state, not only a path.

Acceptance criteria:

- Tier 2 invariant binding document has canonical source path plus commit/ref pin;
- any future ProCybernetica invariant-mode adoption records adopt/defer/reject status;
- no authority is silently imported through prose-only reference.

### H2 — Schema-only guarantee banners

Add a standard local banner for binding schemas and fixtures:

```text
This schema validates declaration shape only. It does not perform runtime lookup, source resolution, receipt verification, monitor attestation, timestamp authenticity, proof review, or semantic invariant verification.
```

Acceptance criteria:

- M1/M5/lawful-learning/interpretability binding schemas or adjacent docs carry the banner;
- valid fixtures and invalid fixtures remain Layer 1 fixtures;
- Layer 2 obligations are issue-tracked, not implied.

### H3 — Claim-status ledger

Create a repo-local ledger for high-risk claim surfaces.

Minimum fields:

```text
artifact_path
claim_surface
current_language
normalized_status
evidence_required
owning_plane
review_required
non_claims
next_action
```

Acceptance criteria:

- lawful-learning theorem/theorem-pattern docs are entered;
- Tier 2 bindings are entered;
- interpretability harness and Neuronpedia schemas are entered;
- SPO prototype branch is entered as exploratory if replayed.

### H4 — Theorem-language review gate

Any file using `theorem`, `theorem-level`, `proof`, `proved`, `minimal`, `structural theorem`, or equivalent load-bearing mathematical language must pass a review gate.

Acceptance criteria:

- theorem-facing docs either carry proof-review evidence or are demoted to theorem-track candidate / structural doctrine;
- scaffold-supported numerical claims cannot be described as direct computation;
- direct Stokes-side TODOs remain explicit non-claims.

### H5 — CI polarity and aggregate target audit

Verify that aggregate CI targets actually run all intended lanes and that invalid fixtures fail for the intended reason.

Acceptance criteria:

- `make certificate-ci` and `make -f GNUmakefile certificate-ci` semantics are documented;
- positive fixture corruption test or equivalent polarity proof is recorded for PR #37 before it leaves draft;
- invalid fixture failure paths are named in PR bodies or audit notes.

### H6 — Branch/content reconciliation

Ahead-of-main branches require explicit treatment. Closing or deleting is not allowed until content is captured or supersession is proven.

Priority branches seen during audit:

```text
capture/spo-baez-algebra-engine
copilot/integrate-superconscious-cognition-loop
doctrine/architecture-falsification-v0-1
feat/neuronpedia-schema-bumps-v01
lawful-learning-capture-v1
lawful-learning-runtime-package
lawful-learning-t2-prime-doctrine
lawful-learning-t2-prime-doctrine-current
m0-m15-certificate-chain
m0-m15-certificate-chain-current
```

Acceptance criteria:

- each branch gets a capture/supersession note;
- duplicate superseded branches are not deleted until path-level equivalence or explicit non-capture rationale is recorded;
- any useful uncaptured branch content is replayed through a hardened PR.

### H7 — PR #37 readiness gate

PR #37 may leave draft only after the following are recorded:

```text
positive fixture passes
negative fixtures fail
polarity check recorded
Layer 1 limitations recorded
Layer 2 tracking issues linked
no runtime/source verification implied
no provider authenticity implied
no model behavior/decomposition correctness implied
```

Acceptance criteria:

- PR body updated with readiness checklist;
- CI/polarity evidence linked;
- reviewer can distinguish schema validation from source verification.

## 6. First remediation sequence

Recommended PR order:

1. Audit plan PR: land this file.
2. Source-pin / schema-only banner PR for Tier 2 bindings.
3. Claim-status ledger PR covering theorem/doctrine/prototype/schema surfaces.
4. Lawful-learning theorem-language demotion or proof-review gate PR.
5. PR #37 hardening update, then mark ready only if gates pass.
6. Branch reconciliation PR(s), one branch family at a time.

## 7. Non-destruction policy

No file or branch should be deleted merely because it is uncomfortable or generated under weak review. The allowed outcomes are:

```text
merge after hardening
replay after demotion
capture as exploratory
record supersession
record intentional non-capture
then delete stale branch only after capture/supersession is durable
```

## 8. Audit open questions

1. Which ProCybernetica commit is the authoritative source for the Tier 2 invariant family consumed by `superconscious`?
2. Which mathematical claims in Lawful Learning have independent proof-review evidence?
3. Which scaffold-supported numerical claims are being used as doctrine inputs downstream?
4. Which branches are true superseded duplicates versus uncaptured content?
5. Should the SPO/Baez prototype remain quarantined forever or be replayed as an explicitly exploratory non-canonical artifact?

## 9. Summary

The repo can keep much of the work if it is treated as bounded infrastructure:

```text
schemas => declaration shape
fixtures => Layer 1 polarity
checkers => structural guardrails
doctrine => governance commitments
theorem docs => proof-review gated
prototypes => non-canonical exploratory artifacts
```

The hardening objective is not to erase the work. The objective is to prevent shape, prose, CI, or prototype self-tests from being mistaken for verification, proof, runtime execution, or cross-repo authority.