"""Boundary tests for neuro-symbolic cognition doctrine.

These tests keep the ASU / CHRONOS neuro-symbolic capture in the same
read/reflect/propose posture as the rest of Superconscious M1.
"""

from pathlib import Path

DOCS = Path("docs")
POSITION = DOCS / "neurosymbolic-cognition-position.md"
ROLE_MATRIX = DOCS / "neurosymbolic-capability-role-matrix.md"
FAILURE_MODES = DOCS / "neurosymbolic-failure-modes.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_neurosymbolic_position_preserves_non_authority_boundary() -> None:
    text = _read(POSITION)

    assert "Superconscious coordinates neuro-symbolic cognition; it does not authorize neuro-symbolic claims." in text
    assert "It does not add runtime authority." in text
    assert "M1 remains deterministic and inert." in text
    assert "does not own the carrier's final authority" in text


def test_neurosymbolic_position_names_forbidden_promotions() -> None:
    text = _read(POSITION)

    required = [
        "treat model output as evidence",
        "treat fuzzy scores as truth",
        "treat stable-model output as execution permission",
        "treat learned rules as canonical schemas",
        "treat ontology embeddings as ontology authority",
        "treat symbolic policies as live controllers",
        "persist symbolic memory without governance",
        "call a model provider directly",
    ]
    for phrase in required:
        assert phrase in text


def test_role_matrix_keeps_event_posture_read_reflect_propose_only() -> None:
    text = _read(ROLE_MATRIX)

    allowed = ["observe", "reflect", "propose", "record", "risk_signal", "policy_review_request"]
    forbidden = [
        "authorize",
        "execute",
        "promote_schema",
        "promote_memory",
        "route_model",
        "open_network",
        "mutate_workspace",
    ]

    for item in allowed:
        assert item in text
    for item in forbidden:
        assert item in text


def test_role_matrix_declares_all_expected_method_families() -> None:
    text = _read(ROLE_MATRIX)

    families = [
        "NSR-FOUNDATION-LOGIC",
        "NSR-TAXONOMY",
        "NSR-SOFT-CONSTRAINT",
        "NSR-TRUTH-BOUND",
        "NSR-SYMBOLIC-ADJUDICATION",
        "NSR-DIFFERENTIABLE-CONSTRAINT-LEARNING",
        "NSR-RULE-LEARNING",
        "NSR-ONTOLOGY-INFERENCE",
        "NSR-SYMBOLIC-POLICY",
    ]
    for family in families:
        assert family in text


def test_failure_modes_cover_authority_drift_cases() -> None:
    text = _read(FAILURE_MODES)

    failure_modes = [
        "soft_score_as_truth",
        "neural_output_as_evidence",
        "learned_rule_as_schema",
        "symbolic_derivation_as_policy_admission",
        "carrier_missing_provenance",
        "embedding_as_ontology_authority",
        "symbolic_policy_as_live_controller",
        "label_leakage_grounding_failure",
        "transduction_unvalidated",
    ]
    for failure_mode in failure_modes:
        assert failure_mode in text


def test_failure_modes_route_to_risk_or_review_not_mutation() -> None:
    text = _read(FAILURE_MODES)

    assert "Every failure mode above is handled by read / reflect / propose / record / risk-signal / policy-review posture." in text
    assert "No failure mode is handled by direct mutation, execution, memory promotion, model routing, or schema promotion inside Superconscious." in text
