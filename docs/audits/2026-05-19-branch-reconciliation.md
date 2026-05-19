# Branch Reconciliation Audit — 2026-05-19

**Status:** H6 audit ledger.  
**Repository:** `SocioProphet/superconscious`.  
**Baseline main:** `9ab4f8dbd40fcd6173c9035637f8d065f8a8a231`.  
**Purpose:** classify ahead-of-main and stale branches without losing content.

## 0. Non-destruction rule

No branch should be deleted merely because it is stale, awkward, or generated under weak review.

Allowed outcomes:

```text
captured_on_main
superseded_by_merged_pr
quarantine_exploratory
replay_after_demotion
runtime_review_required
open_pr_active
delete_after_capture_confirmed
```

A branch may move to deletion only when one of the following is true:

```text
compare shows ahead_by = 0 against main;
path-level content equivalence is documented;
a superseding PR explicitly captures or intentionally omits every changed path;
unique content has been replayed onto a new hardened branch.
```

Squash merges can leave historical branches showing `ahead_by > 0` even when their file content was captured on main. Therefore `ahead_by > 0` is not, by itself, proof of uncaptured content. It is a trigger for path-level audit.

## 1. Active containment branch

| Branch | Status | Disposition |
|---|---:|---|
| `feat/neuronpedia-schema-bumps-v01` | diverged; ahead_by 20; behind_by 12; backs draft PR #37 | `open_pr_active`; keep draft until H7 readiness gates pass. |

## 2. Branches with no unique content relative to main

These branches compared with `ahead_by = 0`. They are candidates for deletion after this audit PR lands and issue #39 records the cleanup policy.

| Branch | Compare status | Disposition |
|---|---:|---|
| `feat/neuronpedia-schema-bumps-v01-main` | behind; ahead_by 0 | `delete_after_capture_confirmed` |
| `neuronpedia-schema-bumps-v01-clean` | behind; ahead_by 0 | `delete_after_capture_confirmed` |
| `m4j-jurisprudential-control` | behind; ahead_by 0 | `delete_after_capture_confirmed` |
| `audit/h6-branch-reconciliation` before this PR | behind; ahead_by 0 | now refreshed to current main and reused for this PR |

## 3. Quarantine / exploratory branches

| Branch | Unique content | Disposition | Rationale |
|---|---|---:|---|
| `capture/spo-baez-algebra-engine` | `docs/exploratory/spo-baez-algebra-engine.md`, `prototypes/spo/README.md`, `prototypes/spo/spo_activation_engine.py` | `quarantine_exploratory` | Useful exploratory capture, but not canonical SPO engine. Must not merge without explicit non-canonical and no-SPO-recursion boundary. |

## 4. Replay-after-demotion candidates

These branches contain useful-looking content that is not safely deletable and should be replayed through hardened PRs if retained.

| Branch | Unique content summary | Disposition | Replay constraints |
|---|---|---:|---|
| `doctrine/architecture-falsification-v0-1` | `docs/architecture-falsification-v0.1.md`; ARCHITECTURE/ROADMAP edits | `replay_after_demotion` | Replay as doctrine/audit doc only; no runtime/theorem promotion. |
| `lawful-learning-capture-v1` | `docs/lawful-learning/00-source-ledger.md`, `docs/lawful-learning/README.md` | `replay_after_demotion` | Likely useful source-ledger material; must harmonize with current Phase 2-8 docs and H4 claim status. |
| `capture/spo-baez-algebra-engine` | exploratory SPO/Baez bridge and prototype | `replay_after_demotion` only if desired | If replayed, use `exploratory_noncanonical` and explicitly state it does not implement full SPO recursion. |
| `turn4-cairnmark-stele-v13` | v1.3 Cairnmark/Stele transition doctrine, migration policy, additive schema placeholders | `replay_after_demotion` | Must reconcile with ProCybernetica / certificate-family namespace before any schema promotion. |

## 5. Runtime-review-required branches

These contain code/runtime surfaces or package surfaces. They are not deletion candidates and should not be merged blindly.

| Branch | Unique content summary | Disposition | Review constraints |
|---|---|---:|---|
| `copilot/integrate-superconscious-cognition-loop` | cognition loop, adapters, schema, examples, tests | `runtime_review_required` | Must preserve superconscious as coordinator, not authority. Requires adapter-boundary and no-direct-mutation review. |
| `lawful-learning-runtime-package` | `superconscious_core/lawful_learning` package and PFK serialization stub | `runtime_review_required` | Small but runtime-facing. Must define authority scope and avoid implicit execution claims. |
| `neural-fabric-capture` | neural-fabric package, schemas, workflow, Hopfield/May-Wigner modules | `runtime_review_required` | High semantic-risk. Requires claim-status gating before any merge. |

## 6. Likely captured by merged PR, pending path-level equivalence

These branches appear to correspond to already-merged PRs. Because most were squash-merged or replayed, compare can still show `ahead_by > 0`. Do not delete until a path-level equivalence or intentional non-capture note is recorded.

| Branch | Related merged PR / content | Compare status | Disposition |
|---|---|---:|---|
| `tier2-invariant-bindings` | PR #13 Tier 2 invariant bindings | ahead_by 1 | `superseded_by_merged_pr`; verify against hardened current `docs/composition/TIER2_INVARIANT_BINDINGS.md`. |
| `m1-tier2-binding-schema` | PR #14 M1 Tier 2 binding | ahead_by 5 | `superseded_by_merged_pr`; current main has hardened schema boundary from PR #40. |
| `m5-tier2-binding-schema` | PR #15 M5 Tier 2 binding | ahead_by 5 | `superseded_by_merged_pr`; current main has hardened schema boundary from PR #40. |
| `lawful-learning-tier2-binding-schema` | PR #16 lawful-learning trust-surface Tier 2 binding | ahead_by 5 | `superseded_by_merged_pr`; current main has hardened schema boundary from PR #40. |
| `docs/phase8-status-update` | PR #31 Phase 8 status update | ahead_by 1 | `superseded_by_merged_pr`; verify status file path. |
| `docs/trust-surface-adapters` | PR #25 adapter boundaries | ahead_by 3 | `superseded_by_merged_pr`; verify docs path. |
| `lawful-learning-phase2-framework` | PR #17 Phase 2 framework cleanup | ahead_by 1 | `superseded_by_merged_pr`; verify docs path. |
| `lawful-learning-phase3-categorical-foundations` | PR #18 Phase 3 categorical foundations | ahead_by 1 | `superseded_by_merged_pr`; verify docs path. |
| `lawful-learning-phase4-invariants` | PR #19 Phase 4 invariants | ahead_by 2 | `superseded_by_merged_pr`; verify docs/example paths. |
| `lawful-learning-phase5-schemas` | PR #20 Phase 5 schema lane | ahead_by 21 | `superseded_by_merged_pr`; verify schema/fixture paths. |
| `lawful-learning-phase6-checker` | PR #21 Phase 6 checker | ahead_by 4 | `superseded_by_merged_pr`; verify checker/workflow paths. |
| `lawful-learning-phase6-fixture-hardening` | PR #22/#23 Phase 6 fixture hardening | ahead_by 9 | `superseded_by_merged_pr`; verify negative fixtures. |
| `lawful-learning-t2-prime-doctrine` | Early T2-prime branch | ahead_by 5 | `superseded_by_merged_pr`; likely subset of PR #30; verify after H4 demotion. |
| `lawful-learning-t2-prime-doctrine-current` | PR #30 T2/A2/An/D4 tranche | ahead_by 49 | `superseded_by_merged_pr`; current main has H4-demoted variants; verify any unique remediation dossier. |
| `m0-m15-certificate-chain` | PR #8 superseded by #9 | ahead_by 18 | `superseded_by_merged_pr`; verify #9 captured all intended content or recorded non-capture. |
| `m0-m15-certificate-chain-current` | PR #9 M0/M1.5/Pneumachinalis tranche | ahead_by 30 | `superseded_by_merged_pr`; verify current main paths; note current hardening may differ from old schema descriptions. |
| `work/generalized-interpretability-harness-v0` | PR #11 generalized interpretability harness | ahead_by 22 | `superseded_by_merged_pr`; verify current main plus GNUmakefile overlay. |
| `work/generalized-interpretability-harness-v0-rebased` | partial replay of PR #11 docs | ahead_by 2 | `superseded_by_merged_pr`; verify docs captured. |
| `work/interpretability-harness-tier2-binding-moat` | PR #24 interpretability harness moat / Tier 2 binding | ahead_by 6 | `superseded_by_merged_pr`; current main has later schema-boundary hardening. |
| `work/neuronpedia-schema-bump-v0-1` | PR #29 registry-only steering boundary | ahead_by 2 | `superseded_by_merged_pr`; verify negative fixture in current main. |
| `work/wire-interpretability-harness-ci` | PR #28 interpretability harness CI wiring | ahead_by 1 | `superseded_by_merged_pr`; verify GNUmakefile state. |
| `work/toy-model-harness-v0` | appears to overlap PR #11 interpretability harness content | ahead_by 21 | `superseded_by_merged_pr` or `replay_after_demotion`; needs path-level diff against PR #11 before delete. |

## 7. Audit branches from completed hardening PRs

These branches are expected to be cleanup candidates after PRs have merged:

```text
audit/2026-05-19-hardening-plan
audit/tier2-source-pins-schema-boundaries
audit/claim-status-ledger
audit/h4-theorem-language-gate
```

Disposition: `delete_after_capture_confirmed` once this H6 audit lands and no open PR references them.

The immutable baseline branch should remain for now:

```text
audit/2026-05-19-claude-damage-baseline
```

Disposition: keep until the full damage-audit sequence closes.

## 8. Recommended replay order

1. **Path-equivalence deletion batch:** delete only branches with `ahead_by = 0` and completed audit branches after confirming no open PR references them.
2. **Low-risk doc replay:** `lawful-learning-capture-v1`, `doctrine/architecture-falsification-v0-1`.
3. **Exploratory quarantine replay:** `capture/spo-baez-algebra-engine`, if retained.
4. **Runtime branch review:** `lawful-learning-runtime-package`, `copilot/integrate-superconscious-cognition-loop`, `neural-fabric-capture`.
5. **Schema migration review:** `turn4-cairnmark-stele-v13`.
6. **PR #37 H7 readiness:** only after this H6 ledger and polarity/readiness evidence are durable.

## 9. Branch deletion policy

No deletion is authorized by this document alone except for branches later verified to satisfy:

```text
ahead_by = 0
or path-equivalence record exists
or supersession + intentional non-capture record exists
```

Branch cleanup should be executed as a separate cleanup step after this PR merges, with the exact branch list copied into the cleanup PR/issue comment.

## 10. H6 completion criteria

H6 is complete only when:

```text
all ahead-of-main branches have a disposition;
all unique runtime branches have explicit review gates;
all exploratory branches have quarantine or replay decisions;
all behind/no-ahead branches are deleted or intentionally retained;
all superseded branches have path-level equivalence or non-capture notes.
```

This PR completes the first H6 pass, not final branch deletion.
