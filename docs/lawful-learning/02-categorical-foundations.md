# Categorical Foundations and Composition Discipline

**Status:** Phase 3 categorical foundations capture.

**Date:** May 13, 2026

**Scope:** Captures the categorical structure of lawful-learning adapters as open networks, defines three composition invariants with operational test forms, and ties those invariants to the existing Tier 2 binding infrastructure and Phase 1 claim ledger.

**Depends on:** Phase 1 claim ledger, Phase 2 framework document (`docs/lawful-learning/01-framework-substrates-structures-circuits.md`), and the lawful-learning trust-surface Tier 2 binding.

**Boundary:** Doctrine and operational invariant specification only. This document adds no schema, no checker implementation, and no trust-surface example. Those belong to later phases.

**Authorial status:** Captures the Heller lawful-learning program. Assistant changes are editorial structuring, cleanup, and governance alignment; the core framework is Michael Heller's work.

---

## 1. Why categorical structure matters for lawful learning

[G|T] The lawful-learning framework makes three recurring architectural claims:

1. adapters compose;
2. composed adapters can be audited without re-running their constituents;
3. replay seals are computable from constituent seals without re-executing the computation.

[M|T] These claims require a structure that supports composition, black-boxing, and seal derivation. Open networks with cospan-based composition provide that structure.

[G] This document establishes the categorical foundations that back those three claims and specifies the operational invariants that Phase 6 can later enforce.

The foundations are load-bearing for two reasons.

First, they determine what the Phase 6 checker can actually verify. A checker that enforces `adapter_dag_acyclic`, `black_boxing_composes`, and `replay_seal_for_composed_trace` needs operational specifications of those invariants, not prose statements.

Second, they tie into the existing Tier 2 composition infrastructure. The lawful-learning trust-surface Tier 2 binding pins:

```text
non_claim_analysis: explicit_propagate_or_resolve_v1
monitor_independence_analysis: declared_monitor_independence_v1
evidence_freshness_analysis: declared_evidence_freshness_v1
receipt_integration: hash_bound_reference
```

[G] These pins are meaningful only if the underlying compositions have a structure that makes manifest/latent distinction, black-box composition, and replay sealing operationally real.

---

## 2. Adapters as open networks

**Claim ledger reference:** `claim.adapter.open-network-cospan.M`

[M] An adapter is modeled as an open network: a structure `X` equipped with input and output boundary maps forming a cospan.

```text
∂_in: B_in → X ← B_out: ∂_out
```

where `B_in` is the input boundary, `B_out` is the output boundary, and `X` is the internal network.

### 2.1 Manifest and latent state

[T] Every adapter declares two state surfaces:

```text
manifest_state
latent_state
```

**Manifest state** is the portion of `X`'s state determined by the input boundary `B_in` and the composition rule. Manifest state is externally observable without inspecting `X`'s internals.

**Latent state** is the portion of `X`'s state internal to `X` and not determined by the input boundary alone. Latent state is opaque to external observers.

[T] The manifest/latent split is not necessarily a physical partition of parameters or activations. It is a declared interface: the adapter's statement of what is externally observable and what is internal.

[G] An adapter that declares its entire state manifest claims full transparency. An adapter that declares no state manifest claims full opacity. Both are valid declarations, but the declaration must be explicit.

[G] A composed manifest must be derivable from constituent declarations according to the composition rule. It must not silently inspect latent state.

### 2.2 Composition

[M] Given two adapters `A` and `B` where the output boundary of `A` matches the input boundary of `B`, their composition is the pushout of the shared boundary.

```text
X_A ← B_out^A = B_in^B → X_B
```

The composition `A ∘ B` has:

```text
input boundary:     B_in^A
output boundary:    B_out^B
internal network:   X_A ⊔_B X_B
composition rule:   the boundary-respecting map from B_in^A to B_out^B
```

[M] The pushout construction is the mathematical basis for the `black_boxing_composes` invariant.

[T] Operationally, this means the composed adapter's manifest behavior is determined by the constituent adapters' manifest behaviors and the shared boundary, without reference to constituent latent states.

**Source anchors:** `src.compositional.fong-spivak-2019`, `src.compositional.baez-pollard-2017` in the Phase 1 source ledger.

---

## 3. Three composition invariants with operational tests

Each invariant is stated in three layers:

```text
1. structural claim
2. operational test for the future Phase 6 checker
3. failure mode caught
```

The tests below are specifications, not current runtime implementations.

---

### 3.1 `adapter_dag_acyclic`

**Claim ledger reference:** `claim.adapter.dag-acyclic.G`

[G] Adapter dependency graphs must be acyclic.

[G] A directed cycle in the adapter dependency graph admits a composition that cannot be computed in finite time: if `A` depends on `B` and `B` depends on `A`, computing `A ∘ B` requires first computing `B ∘ A`, which requires first computing `A ∘ B`, and so on without termination.

#### Operational test

Given a declared adapter dependency graph `G = (V, E)` where `V` is the set of adapter identifiers and `E ⊆ V × V` is the set of declared dependency edges:

```python
def check_adapter_dag_acyclic(dependency_graph: dict[str, list[str]]) -> bool:
    """
    Returns True if the adapter dependency graph is acyclic.
    Raises ValueError with the violating cycle if a directed cycle exists.

    dependency_graph maps adapter_id -> list of adapter_ids it directly depends on.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in dependency_graph}
    cycle_path: list[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        cycle_path.append(node)

        for neighbor in dependency_graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                cycle_start = cycle_path.index(neighbor)
                detected_cycle = cycle_path[cycle_start:] + [neighbor]
                raise ValueError(
                    f"Adapter dependency cycle detected: {detected_cycle}"
                )
            if color.get(neighbor, WHITE) == WHITE:
                if neighbor not in color:
                    color[neighbor] = WHITE
                dfs(neighbor)

        cycle_path.pop()
        color[node] = BLACK

    for node in list(color):
        if color[node] == WHITE:
            dfs(node)

    return True
```

#### Failure mode caught

[G] The checker rejects adapter dependency declarations containing directed cycles before any composition is attempted.

#### Non-claims

[G] This test does not verify that the declared dependency graph is complete. An adapter may have undeclared dependencies.

[G] This test does not verify that dependencies are semantically correct. A declared edge may not correspond to an actual data dependency.

[G] Completeness and semantic correctness are Phase 6+ checker extensions, not Phase 3 claims.

---

### 3.2 `black_boxing_composes`

**Claim ledger reference:** `claim.adapter.black-boxing-composes.G`

[G] For every declared composition `A ∘ B`, the composed manifest must be derivable from `manifest(A)`, `manifest(B)`, and `composition_rule` only.

[G] The derivation must not inspect `latent_state(A)` or `latent_state(B)`.

[M] The mathematical basis is functorial black-boxing: the black-boxed behavior of a composition is the composition of the black-boxed behaviors.

```text
B(A ∘ B) = B(A) ∘ B(B)
```

[T] Functoriality is the structural statement that an external auditor does not need to look inside `A` or `B` to know what `A ∘ B` does externally, provided the manifest declarations and composition rule are valid.

#### Operational test

A composition declaration for `A ∘ B` is structurally valid for `black_boxing_composes` if and only if:

```text
composed_manifest = composition_function(
    manifest_A = manifest(A),
    manifest_B = manifest(B),
    composition_rule = declared_composition_rule(A, B)
)
```

The checker verifies:

```python
def check_black_boxing_composes(composition_declaration: dict) -> bool:
    """
    Verifies that composed_manifest is declared as derivable from
    manifest_A, manifest_B, and composition_rule only.

    Rejects if composed_manifest references any latent-state field.
    """
    required_inputs = {
        "manifest_A",
        "manifest_B",
        "composition_rule",
    }
    forbidden_inputs = {
        "latent_state_A",
        "latent_state_B",
        "internal_state_A",
        "internal_state_B",
        "hidden_state_A",
        "hidden_state_B",
    }

    derivation = composition_declaration.get("composed_manifest_derivation", {})
    declared_inputs = set(derivation.get("inputs", []))

    missing = required_inputs - declared_inputs
    if missing:
        raise ValueError(
            f"composed_manifest derivation missing required inputs: {missing}"
        )

    forbidden_used = forbidden_inputs & declared_inputs
    if forbidden_used:
        raise ValueError(
            "composed_manifest derivation references latent state: "
            f"{forbidden_used}. black_boxing_composes requires manifest-only derivation."
        )

    return True
```

#### Failure mode caught

[G] This catches a composition that claims to produce a composed manifest while the derivation depends on constituent latent state.

[G] Such a composition violates the black-boxing property because it cannot be audited without re-running or inspecting constituents.

#### Non-claims

[G] This test does not verify that `manifest(A)` and `manifest(B)` accurately represent the adapters' actual external behavior.

[G] This test does not verify that the `composition_rule` is semantically correct.

[G] It verifies only manifest-only derivation per the declaration.

#### Tier 2 relation

[G] `black_boxing_composes` is the structural basis for the `no_runtime_non_claim_verification` non-claim in the lawful-learning trust-surface binding.

[G] The binding declares that non-claim propagation operates on declared manifests, not runtime latent states. That declaration is structurally coherent only if manifest derivation is black-boxing-compliant.

---

### 3.3 `replay_seal_for_composed_trace`

**Claim ledger reference:** `claim.adapter.replay-seal-composed.G`

[G] For composed adapters, the replay seal of the composition is computable from constituent seals, the composition rule, and the shared boundary hash without rerunning the constituents.

```text
composed_replay_seal = H(seal(A), seal(B), composition_rule, boundary_hash)
```

where `H` is a declared collision-resistant hash function and `boundary_hash` is the hash of the shared boundary between `A` and `B`.

[T] The replay seal is a commitment over the adapter's manifest state and composition rule. For a composition `A ∘ B`, the composed seal commits to `seal(A)`, `seal(B)`, the composition rule, and the shared boundary.

[G] The seal is derivable without rerunning because the black-boxed composition is computed from manifest-only information.

#### Operational test

```python
def check_replay_seal_for_composed_trace(
    composition_declaration: dict,
    hash_function,
) -> bool:
    """
    Verifies that declared composed_replay_seal is the output of:

        H(seal_A, seal_B, composition_rule, boundary_hash)

    Rejects if seal derivation requires rerunning constituents or
    omits required seal inputs.
    """
    seal_declaration = composition_declaration.get(
        "composed_replay_seal_derivation", {}
    )

    if seal_declaration.get("requires_rerun_A", False):
        raise ValueError(
            "composed_replay_seal derivation requires rerun_A. "
            "replay_seal_for_composed_trace requires seal derivation "
            "without rerunning constituents."
        )

    if seal_declaration.get("requires_rerun_B", False):
        raise ValueError(
            "composed_replay_seal derivation requires rerun_B. "
            "replay_seal_for_composed_trace requires seal derivation "
            "without rerunning constituents."
        )

    required_inputs = {
        "seal_A",
        "seal_B",
        "composition_rule",
        "boundary_hash",
    }
    declared_inputs = set(seal_declaration.get("inputs", []))

    missing = required_inputs - declared_inputs
    if missing:
        raise ValueError(
            f"composed_replay_seal derivation missing required inputs: {missing}"
        )

    declared_seal = composition_declaration.get("composed_replay_seal")
    computed_seal = hash_function(
        seal_declaration["seal_A"],
        seal_declaration["seal_B"],
        seal_declaration["composition_rule"],
        seal_declaration["boundary_hash"],
    )

    if declared_seal != computed_seal:
        raise ValueError(
            "Declared composed_replay_seal does not match "
            "H(seal_A, seal_B, composition_rule, boundary_hash). "
            f"Declared: {declared_seal}. Computed: {computed_seal}."
        )

    return True
```

#### Failure mode caught

[G] This catches a composition that requires re-execution of constituent adapters to compute a replay seal.

[G] If the composition's replay requires rerunning `A` or `B`, replay is no longer a pure function of declared seals and the composition rule.

#### Non-claims

[G] This test does not verify collision resistance of the declared hash function.

[G] This test does not verify that `seal(A)` and `seal(B)` are authentic.

[G] Cryptographic authenticity is deferred to future checker extensions and future Tier 2 verified modes.

#### Cross-reference to superconscious M1.5

[T] The M1.5 attribution graph in `superconscious` distinguishes manifest digest from full latent digest. The replay states — bit-exact replay, manifest matches but latent diverges, and manifest diverges — map directly to the manifest/latent split here.

[G] `replay_seal_for_composed_trace` is the general lawful-learning version of what M1.5 implements for attribution graph replay discipline.

---

## 4. Composition of the three invariants

[G] A composition `A ∘ B` is structurally admissible under Phase 3 if and only if all three conditions hold:

1. the adapter dependency graph formed by `A ∘ B` is acyclic;
2. the composed manifest is derivable from `manifest(A)`, `manifest(B)`, and `composition_rule` without latent-state inspection;
3. the composed replay seal is derivable as `H(seal(A), seal(B), composition_rule, boundary_hash)` without constituent rerun.

[G] A composition that satisfies acyclicity and black-boxing but fails replay sealing is admissible for manifest audit but not for replay.

[G] A composition that satisfies acyclicity and replay sealing but fails black-boxing is replayable but not auditable as a manifest-only composition.

[G] A composition that satisfies black-boxing and replay sealing but fails acyclicity is not admissible for incorporation into a larger adapter dependency graph.

[G] Phase 6 should enforce all three as a unit. A composition declaration that fails any one of the three should be rejected.

---

## 5. Relationship to Tier 2 composition invariants

[G] The categorical foundations here are the structural substrate on which the ProCybernetica Tier 2 composition invariants operate.

### 5.1 Non-claim propagation

[G] Non-claim propagation requires that a composition's non-claim surface derives from its constituents' non-claim surfaces by propagate-or-resolve discipline.

[G] This derivation is structurally coherent only if compositions satisfy `black_boxing_composes`. A composition that secretly depends on latent state could absorb constituent non-claims without surfacing them.

### 5.2 Monitor independence

[G] Monitor independence requires monitor relationships to form an admissible graph.

[T] This is the Tier 2 projection of `adapter_dag_acyclic`: `adapter_dag_acyclic` operates on the general adapter dependency graph; `declared_monitor_independence_v1` operates on the monitoring subgraph.

### 5.3 Evidence freshness

[G] Evidence freshness requires composition claim times to be compared to receipt creation times.

[G] This presupposes that receipt references are opaque hash commitments rather than live-dereferenced artifacts.

[T] `replay_seal_for_composed_trace` is what makes hash-bound references semantically coherent: a receipt whose hash matches the replay-seal commitment is a structurally valid evidence reference.

### 5.4 Lawful-learning trust-surface binding

[G] The lawful-learning trust-surface Tier 2 binding pins the current Tier 2 declared modes. The categorical foundations here make those pins non-vacuous by defining what composition means for adapters, manifests, latent state, and replay seals.

---

## 6. What Phase 3 does not claim

This document does not claim:

```text
formal proof of all lawful-learning categorical structure
operational invariant checking before Phase 6
that neural network adapters are literally open networks
that manifest declarations are semantically complete
that replay seals are cryptographically authentic
that Tier 2 verified modes exist today
new Tier 2 binding updates
new schema or checker implementation
```

[M] The categorical structure of open networks with cospan composition is established in the cited source tradition. This document consumes that tradition for lawful-learning doctrine; it does not re-prove it.

[T] Neural network adapters are modeled as open networks for composition, black-boxing, and replay semantics. The model is an abstraction.

[G] The governance consequences are tagged [G], not promoted to further [M] claims about neural network structure.

---

## 7. Phase 4 handoff

Phase 4 consumes this document in two specific ways.

First, the three operational invariant specifications become the canonical sources for:

```text
adapter_dag_acyclic
black_boxing_composes
replay_seal_for_composed_trace
```

Phase 4 should reference Section 3 of this document rather than re-deriving the operational form.

Second, the relationship between the three categorical invariants and the three Tier 2 analysis modes provides the structural justification for why the lawful-learning trust-surface binding applies the modes it pins.

Phase 4 should also introduce the remaining governance invariants from the Phase 1 claim ledger, including:

```text
May-Wigner stability monitor
control-plane / data-plane separation
tail-integral audit
composition-superposition allocation
claim tag promotion prevention
trust-surface non-claim propagation
```

Each Phase 4 invariant should follow the same pattern used here:

```text
1. structural claim
2. operational test
3. failure mode caught
4. explicit non-claims
5. relationship to Tier 2 binding discipline
```

---

## 8. Phase 3 completion condition

Phase 3 is complete when this document is merged and existing trust-surface and certificate CI remain green.

After Phase 3, lawful-learning is ready for:

```text
Phase 4: lawful-learning governance invariants
Phase 5: schema lane for lawful-learning trust-surface artifacts
Phase 6: checker for tag discipline and invariant enforcement
```
