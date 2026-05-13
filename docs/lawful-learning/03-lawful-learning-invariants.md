# Lawful Learning Governance Invariants

**Status:** Phase 4 governance invariant capture.

**Date:** May 13, 2026

**Scope:** Defines the seven lawful-learning governance invariants with operational test form. References the three categorical invariants from Phase 3 rather than re-deriving them. Introduces the local trust-surface example at `examples/TRUST_SURFACE.lawful-learning.yaml`.

**Depends on:** Phase 1 claim ledger, Phase 3 categorical foundations (`02-categorical-foundations.md`), and the lawful-learning trust-surface Tier 2 binding.

**Boundary:** Doctrine and operational invariant specification only. This document adds no schema, no checker implementation, and no runtime execution.

**Authorial status:** Captures the Heller lawful-learning program. Assistant changes are editorial structuring, cleanup, and governance alignment; the core framework is Michael Heller's work.

---

## 1. Invariant catalog structure

Each invariant is specified with five elements following the Phase 3 pattern:

1. claim ledger reference;
2. structural claim;
3. operational test;
4. failure mode caught;
5. explicit boundary.

Phase 3's three categorical invariants are not repeated here:

```text
adapter_dag_acyclic
black_boxing_composes
replay_seal_for_composed_trace
```

This document adds seven governance-specific invariants. All ten constitute the full lawful-learning invariant set for Phase 6 checker implementation.

---

## 2. Invariant 1: May-Wigner stability monitor

**Claim ledger references:**

```text
claim.invariant.may-wigner-monitor.G
claim.invariant.may-wigner-monitor.T
```

### Structural claim

[G] Every lawful-learning training run must declare a May-Wigner-style stability monitor that tracks a scalar quantity intended to indicate proximity to a stability threshold. The monitor must be declared before training begins and must produce a logged value at each declared checkpoint interval.

[T] The monitored quantity is computed by analogy to May's stability criterion `sigma * sqrt(NC) < 1` for random community matrices. This is a structural parallel to the random-matrix stability result; the training dynamics being monitored generally do not satisfy May-Wigner random-Gaussian-connectivity and weak-coupling assumptions.

[G] The monitored quantity does not inherit May-Wigner predictive guarantees. The monitor is an operational governance commitment, not a mathematical proof that training will be stable.

### Operational test

```python
def check_may_wigner_monitor_declared(training_run_declaration: dict) -> bool:
    """
    Verifies that a training run declaration includes a May-Wigner-style
    stability monitor with required fields.

    Required fields:
    - monitor_name
    - monitored_quantity
    - checkpoint_interval
    - threshold_declaration
    """
    required_fields = {
        "monitor_name",
        "monitored_quantity",
        "checkpoint_interval",
        "threshold_declaration",
    }
    declared = set(training_run_declaration.get("may_wigner_monitor", {}).keys())
    missing = required_fields - declared
    if missing:
        raise ValueError(
            f"May-Wigner monitor declaration missing required fields: {missing}"
        )
    return True
```

### Failure mode caught

[G] This catches a training run that omits the stability monitor declaration entirely or declares one without required structural fields.

### What this test does not verify

[G] It does not verify that the monitored quantity satisfies May-Wigner assumptions. [G] It does not verify that the declared threshold corresponds to a real stability boundary. [G] It does not verify computational correctness of the monitor.

---

## 3. Invariant 2: Control-plane / data-plane separation

**Claim ledger reference:** `claim.invariant.control-data-plane-separation.G`

### Structural claim

[G] Lawful-learning systems must declare explicit separation between control-plane components and data-plane components. Control-plane components include routing decisions, gating, scheduling, and admission. Data-plane components include expert computations, residual flows, and output generation.

[G] Control-plane and data-plane components must not share implementation components beyond declared boundary interfaces.

### Operational test

```python
def check_control_data_plane_separation(system_declaration: dict) -> bool:
    control = set(system_declaration.get("control_plane_components", []))
    data = set(system_declaration.get("data_plane_components", []))
    boundary = set(system_declaration.get("boundary_interfaces", []))

    if not control:
        raise ValueError("No control_plane_components declared.")
    if not data:
        raise ValueError("No data_plane_components declared.")

    overlap = control.intersection(data) - boundary
    if overlap:
        raise ValueError(
            "Components appear in both control and data plane without "
            f"boundary_interfaces declaration: {overlap}"
        )
    return True
```

### Failure mode caught

[G] This catches implicit coupling where a routing gate and computation layer share implementation without declaring it.

### What this test does not verify

[G] It does not verify that declared control-plane components actually perform control functions. [G] It does not verify that data-plane components actually perform computation. Implementation conformance is deferred.

---

## 4. Invariant 3: Tail-integral audit allocation

**Claim ledger references:**

```text
claim.invariant.tail-integral-audit.G
claim.invariant.tail-integral-audit.S
```

### Structural claim

[G] Audit allocation must include a declared tail component beyond expected-case coverage. Every audit plan must name a tail allocation strategy and declare its scope.

[S] The proposed tail-integral form `integral_t^infinity f(s) ds` is a candidate operationalization whose convergence properties depend on `f` and have not been characterized for general lawful-learning systems.

[G] The tail allocation strategy is operationally required. [S] The particular tail-integral formula remains a research placeholder until `f`, the measure, convergence conditions, and estimator are specified.

### Operational test

```python
def check_tail_audit_allocated(audit_plan: dict) -> bool:
    required = {
        "expected_case_coverage",
        "tail_allocation_strategy",
        "tail_scope_declaration",
    }
    declared = set(audit_plan.keys())
    missing = required - declared
    if missing:
        raise ValueError(f"Audit plan missing tail allocation fields: {missing}")
    if not audit_plan.get("tail_allocation_strategy"):
        raise ValueError(
            "tail_allocation_strategy must be non-empty. "
            "Audit without tail coverage is structurally incomplete."
        )
    return True
```

### Failure mode caught

[G] This catches an audit plan that covers only expected cases without declaring a tail strategy.

### What this test does not verify

[G] It does not verify the mathematical form of the tail coverage. [G] It does not verify that the tail strategy actually covers tail events. [S] The tail-integral formula remains speculative until made operational.

---

## 5. Invariant 4: Emergent-discretization discipline

**Claim ledger reference:** `claim.invariant.emergent-discretization-discipline.G`

### Structural claim

[G] When a lawful-learning system exhibits emergent discrete behavior — grokking, phase transitions, feature splitting, loss-cliff events, or similar events — the discretization event must be logged with timestamp, declared cause, and replay seal within one checkpoint interval of detection.

### Operational test

```python
def check_emergent_discretization_logged(event_log: list[dict]) -> bool:
    for event in event_log:
        if event.get("event_class") != "discretization":
            continue
        required = {
            "event_type",
            "detected_at_checkpoint",
            "timestamp",
            "declared_cause",
            "replay_seal",
        }
        missing = required - set(event.keys())
        if missing:
            raise ValueError(
                f"Discretization event missing required fields: {missing}. "
                f"Event: {event.get('event_type', 'unknown')}"
            )
        if not event.get("declared_cause"):
            raise ValueError(
                "declared_cause must be non-empty; use 'unknown' if cause is not yet identified."
            )
    return True
```

### Failure mode caught

[G] This catches a discretization event that is absent, incomplete, or not replay-sealed after detection.

### What this test does not verify

[G] It does not verify that the declared cause is correct. [G] It does not verify that the replay seal actually reconstructs the system state. [G] It does not verify that all discretization events were detected.

---

## 6. Invariant 5: Composition-superposition allocation declaration

**Claim ledger references:**

```text
claim.invariant.composition-superposition-allocation.G
claim.invariant.composition-superposition-allocation.T
```

### Structural claim

[G] When a circuit can be modeled as either a composition of distinct features or a superposition within a shared subspace, the declared model must explicitly state which allocation applies.

[G] Ambiguous allocation is not admissible; the declaration must name the allocation type and structural evidence for that choice.

[T] This distinction is structurally parallel to direct-sum versus tensor-product decompositions in linear algebra. The parallel is structural and does not claim that neural network feature geometry literally instantiates one of these decompositions as a canonical algebraic structure.

### Operational test

```python
def check_composition_superposition_declared(circuit_declaration: dict) -> bool:
    required = {
        "allocation_type",
        "allocation_evidence",
        "allocation_basis",
    }
    declared = set(circuit_declaration.keys())
    missing = required - declared
    if missing:
        raise ValueError(f"Circuit declaration missing allocation fields: {missing}")

    valid_types = {"composition", "superposition", "mixed", "unknown"}
    allocation_type = circuit_declaration.get("allocation_type")
    if allocation_type not in valid_types:
        raise ValueError(f"allocation_type must be one of {valid_types}. Got: {allocation_type}")

    if not circuit_declaration.get("allocation_evidence"):
        raise ValueError(
            "allocation_evidence must be non-empty. Allocation declaration requires structural evidence."
        )
    return True
```

### Failure mode caught

[G] This catches a circuit declaration that omits the composition-vs-superposition distinction or names an allocation type without structural evidence.

### What this test does not verify

[G] It does not verify that the declared allocation is correct. [T] It does not algebraically verify the direct-sum or tensor-product parallel.

---

## 7. Invariant 6: Anti-satisficing continuation

**Claim ledger reference:** `claim.invariant.anti-satisficing-continuation.G`

### Structural claim

[G] When a lawful-learning system meets a declared sufficient condition — loss threshold, evaluation pass rate, benchmark score, or alignment check pass — the system must not halt further search unless a declared continuation rule has been applied.

[G] The continuation rule must be declared before the sufficient condition is evaluated.

### Operational test

```python
def check_anti_satisficing_continuation(
    training_run_declaration: dict,
    run_log: dict,
) -> bool:
    continuation_rule = training_run_declaration.get("continuation_rule")
    if not continuation_rule:
        raise ValueError(
            "No continuation_rule declared. Anti-satisficing continuation requires "
            "a declared continuation rule before training begins."
        )

    conditions_met = run_log.get("sufficient_conditions_met", [])
    if conditions_met and not run_log.get("continuation_applied", False):
        raise ValueError(
            f"Sufficient conditions met ({conditions_met}) but continuation_rule was not applied."
        )
    return True
```

### Failure mode caught

[G] This catches a training run that halts when it meets a sufficient condition instead of continuing per the declared continuation rule.

### What this test does not verify

[G] It does not verify that the continuation rule is adequate. [G] It does not verify that declared sufficient conditions are meaningful.

---

## 8. Invariant 7: Epistemic non-collapse

**Claim ledger reference:** `claim.invariant.epistemic-non-collapse.G`

### Structural claim

[G] Claims at distinct epistemic tags — [M], [T], [S], [E], [G] — must not collapse into single-register statements.

[G] Every claim in lawful-learning documentation must carry an explicit tag.

[G] Mixed-tag claims must be sentence-by-sentence demarcated.

[G] Tag promotion requires the promotion evidence specified in the Phase 1 ledger hard rules.

### Operational test

```python
def check_epistemic_non_collapse(claim_ledger_entry: dict) -> bool:
    tag = claim_ledger_entry.get("tag", "")
    if not tag:
        raise ValueError("Claim ledger entry missing tag field.")

    valid_base_tags = {"M", "T", "S", "E", "G"}
    tags = set(tag.split("|"))
    invalid = tags - valid_base_tags
    if invalid:
        raise ValueError(f"Unrecognized tag values: {invalid}")

    required_by_tag = {
        "M": "mathematical_dependency",
        "T": "typological_parallel_target",
        "S": "speculative_test_artifact",
        "E": "empirical_measurement_ref",
        "G": "governance_invariant_ref",
    }
    for base_tag in tags:
        field = required_by_tag[base_tag]
        if not claim_ledger_entry.get(field):
            raise ValueError(
                f"Tag [{base_tag}] requires non-empty {field}. "
                f"claim_id: {claim_ledger_entry.get('claim_id', 'unknown')}"
            )

    if "|" in tag and not claim_ledger_entry.get("claim_demarcation"):
        raise ValueError(
            f"Mixed-tag claim {claim_ledger_entry.get('claim_id')} requires claim_demarcation."
        )

    if claim_ledger_entry.get("status") == "promoted" and not claim_ledger_entry.get("promotion_rule"):
        raise ValueError(
            f"Promoted claim {claim_ledger_entry.get('claim_id')} requires promotion_rule."
        )

    claim_text = claim_ledger_entry.get("claim", "").lower()

    if "hopfield" in claim_text and "M" in tags:
        dependency = claim_ledger_entry.get("mathematical_dependency", "")
        if "energy" not in dependency.lower():
            raise ValueError("Hopfield [M] claim must name energy-function form.")

    if "may-wigner" in claim_text or "may wigner" in claim_text:
        if "M" in tags:
            dependency = claim_ledger_entry.get("mathematical_dependency", "")
            if "random" not in dependency.lower() and "gaussian" not in dependency.lower():
                raise ValueError(
                    "May-Wigner [M] claim must state random-matrix assumptions."
                )

    return True
```

### Failure mode caught

[G] This catches missing tags, missing evidence fields, undeclared mixed-tag demarcation, promoted claims without promotion evidence, and subject-specific Hopfield / May-Wigner overclaims.

### What this test does not verify

[G] It does not verify the accuracy of evidence fields. [G] It does not verify that a promoted claim deserves promotion. Substantive promotion remains a review step.

---

## 9. Full invariant set reference

Ten invariants constitute the complete lawful-learning invariant set for Phase 6 checker implementation.

From Phase 3:

| Invariant | Type | Source |
|---|---:|---|
| `adapter_dag_acyclic` | [G] | `02-categorical-foundations.md` Section 3.1 |
| `black_boxing_composes` | [G] | `02-categorical-foundations.md` Section 3.2 |
| `replay_seal_for_composed_trace` | [G] | `02-categorical-foundations.md` Section 3.3 |

From Phase 4:

| Invariant | Type | Section |
|---|---:|---|
| `may_wigner_monitor_declared` | [G|T] | Section 2 |
| `control_data_plane_separation` | [G] | Section 3 |
| `tail_audit_allocated` | [G|S] | Section 4 |
| `emergent_discretization_logged` | [G] | Section 5 |
| `composition_superposition_declared` | [G|T] | Section 6 |
| `anti_satisficing_continuation` | [G] | Section 7 |
| `epistemic_non_collapse` | [G] | Section 8 |

---

## 10. Relationship to Tier 2 composition invariants

[G] Tier 2 invariants govern composition certificates. They enforce structural properties of how governed artifacts are composed into publications or higher-level certificates.

[G] Lawful-learning invariants govern the artifacts themselves. They enforce structural properties of training runs, audit plans, circuit declarations, and claim ledger entries before those artifacts are composed.

[G] The lawful-learning trust-surface Tier 2 binding is the composition point. When lawful-learning artifacts are composed into a trust surface, the Tier 2 invariants apply to the composition and the ten lawful-learning invariants apply to the constituents.

[G] Both sets apply. Neither substitutes for the other.

---

## 11. Boundary

Phase 4 does not add:

```text
schema encoding
checker implementation
runtime execution
cryptographic authenticity checks on seals or hashes
Tier 2 verified-mode claims
recursive composition
meta-governance
```

The trust-surface example in `examples/TRUST_SURFACE.lawful-learning.yaml` is a draft example, not a promoted artifact.

---

## 12. Phase 5 handoff

Phase 5 should encode these invariants into schemas under:

```text
schemas/lawful-learning/
```

Planned schema set:

```text
evidence-status.v1.json
decision-emission.v1.json
lawful-learning-invariants.v1.json
circuit-registry.v1.json
forbidden-circuits.v1.json
alignment-check.v1.json
claim-ledger-entry.v1.json
```

Phase 6 should implement the checker over the Phase 5 schema lane.
