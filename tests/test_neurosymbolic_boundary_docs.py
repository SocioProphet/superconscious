from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POSITION = ROOT / "docs" / "neurosymbolic-cognition-position.md"
ROLE_MATRIX = ROOT / "docs" / "neurosymbolic-capability-role-matrix.md"
FAILURE_MODES = ROOT / "docs" / "neurosymbolic-failure-modes.md"
EXAMPLE_TASK = ROOT / "examples" / "neurosymbolic-cognition-run" / "task.json"

REQUIRED_METHOD_FAMILIES = [
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

REQUIRED_FAILURE_MODES = [
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

REQUIRED_BOUNDARIES = [
    "Superconscious coordinates",
    "does not authorize",
    "policy admission",
    "schema authority",
    "AgentPlane",
    "Ontogenesis",
    "sourceos-spec",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_neurosymbolic_docs_exist() -> None:
    for path in [POSITION, ROLE_MATRIX, FAILURE_MODES, EXAMPLE_TASK]:
        assert path.exists(), f"missing {path}"


def test_method_families_are_bound_in_role_matrix_and_task() -> None:
    text = read(ROLE_MATRIX) + read(EXAMPLE_TASK)
    for family in REQUIRED_METHOD_FAMILIES:
        assert family in text


def test_failure_modes_are_named_in_failure_ledger_or_task() -> None:
    text = read(FAILURE_MODES) + read(EXAMPLE_TASK)
    for failure_mode in REQUIRED_FAILURE_MODES:
        assert failure_mode in text


def test_authority_boundary_language_is_present() -> None:
    text = read(POSITION) + read(ROLE_MATRIX)
    for boundary in REQUIRED_BOUNDARIES:
        assert boundary in text


def test_no_local_authority_claims_for_neurosymbolic_methods() -> None:
    text = (read(POSITION) + read(ROLE_MATRIX) + read(FAILURE_MODES)).lower()
    forbidden_pairs = [
        ("superconscious", "authorizes"),
        ("superconscious", "owns schema authority"),
        ("superconscious", "owns policy admission"),
        ("superconscious", "owns ontology authority"),
        ("fuzzy score", "is truth"),
        ("neural output", "is evidence"),
    ]
    for left, right in forbidden_pairs:
        assert f"{left} {right}" not in text
