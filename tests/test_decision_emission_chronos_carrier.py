"""Tests for the additive CHRONOS-carrier extension to the decision-emission schemas.

Covers issue #76 (SocioProphet/superconscious): decision-emission records should be able
to carry the safe-trace fields docs/neurosymbolic-cognition-position.md and
docs/neurosymbolic-capability-role-matrix.md already prescribe conceptually, without
disturbing any existing decision-emission record's validity.

Two independent decision-emission schemas exist in this repo and both are extended
identically:

- schemas/decision-emission.draft.schema.json (adapter/trunk/head/approval/replay_seal
  governed-cognition-loop emission; wired into `make validate`)
- schemas/lawful-learning/decision-emission.v1.json (decision_id/decision_type/... lawful-
  learning ledger emission; wired into `make lawful-learning-ci`)

Every check here is run twice, once per schema, to prove the extension is a real
superset in both places and that pre-existing fixtures still validate unchanged.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
LL_FIXTURES = FIXTURES / "lawful-learning"

CASES = [
    pytest.param(
        ROOT / "schemas" / "decision-emission.draft.schema.json",
        FIXTURES / "decision-emission.valid.json",
        FIXTURES / "decision-emission.chronos-carrier.valid.json",
        FIXTURES / "decision-emission-carrier-missing-non-authority.invalid.json",
        None,
        id="draft-schema",
    ),
    pytest.param(
        ROOT / "schemas" / "lawful-learning" / "decision-emission.v1.json",
        LL_FIXTURES / "decision-emission.valid.json",
        LL_FIXTURES / "decision-emission.chronos-carrier.valid.json",
        LL_FIXTURES / "decision-emission-carrier-missing-non-authority.invalid.json",
        LL_FIXTURES / "decision-emission-carrier-overreach-declaration.invalid.json",
        id="lawful-learning-v1",
    ),
]


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    return jsonschema


def _load(path: Path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "schema_path,pre_existing_valid,carrier_valid,carrier_missing_declaration,carrier_overreach",
    CASES,
)
def test_pre_existing_fixture_still_validates_unchanged(
    schema_path, pre_existing_valid, carrier_valid, carrier_missing_declaration, carrier_overreach
):
    """The superset check: fixtures that predate this extension must still pass, untouched."""
    jsonschema = _validator()
    schema = _load(schema_path)
    instance = _load(pre_existing_valid)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    errors = list(validator_cls(schema).iter_errors(instance))

    assert errors == [], f"pre-existing fixture must still validate: {errors}"


@pytest.mark.parametrize(
    "schema_path,pre_existing_valid,carrier_valid,carrier_missing_declaration,carrier_overreach",
    CASES,
)
def test_new_carrier_fixture_validates(
    schema_path, pre_existing_valid, carrier_valid, carrier_missing_declaration, carrier_overreach
):
    """A decision-emission carrying the new neurosymbolic_carrier block is valid."""
    jsonschema = _validator()
    schema = _load(schema_path)
    instance = _load(carrier_valid)

    validator_cls = jsonschema.validators.validator_for(schema)
    errors = list(validator_cls(schema).iter_errors(instance))

    assert errors == [], f"new carrier fixture should validate: {errors}"


@pytest.mark.parametrize(
    "schema_path,pre_existing_valid,carrier_valid,carrier_missing_declaration,carrier_overreach",
    CASES,
)
def test_carrier_without_non_authority_declaration_is_rejected(
    schema_path, pre_existing_valid, carrier_valid, carrier_missing_declaration, carrier_overreach
):
    """A decision claiming a neuro-symbolic carrier without the required non-authority
    declaration must be rejected — this is the concrete guardrail issue #76 asked for."""
    jsonschema = _validator()
    schema = _load(schema_path)
    instance = _load(carrier_missing_declaration)

    validator_cls = jsonschema.validators.validator_for(schema)
    errors = list(validator_cls(schema).iter_errors(instance))

    assert errors, "carrier missing nonAuthorityDeclaration must fail schema validation"
    assert any("nonAuthorityDeclaration" in str(error.message) for error in errors)


def test_lawful_learning_carrier_with_overreaching_declaration_text_is_rejected():
    """Even a *present* non-authority declaration is rejected if its own text claims the
    authority it is supposed to disclaim (schema-level content check, not just presence)."""
    jsonschema = _validator()
    schema = _load(ROOT / "schemas" / "lawful-learning" / "decision-emission.v1.json")
    instance = _load(LL_FIXTURES / "decision-emission-carrier-overreach-declaration.invalid.json")

    validator_cls = jsonschema.validators.validator_for(schema)
    errors = list(validator_cls(schema).iter_errors(instance))

    assert errors, "an overreaching non-authority declaration must still be rejected"


def _run_checker(fixture: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check-lawful-learning.py"), "--file", str(fixture)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_structural_checker_accepts_pre_existing_and_new_carrier_fixtures():
    """scripts/check-lawful-learning.py previously had no dispatch rule for decision-emission
    fixtures at all (they silently skipped). Confirm the new dispatch rule runs real checks
    and both the pre-existing and new fixtures pass."""
    for fixture in [
        LL_FIXTURES / "decision-emission.valid.json",
        LL_FIXTURES / "decision-emission.chronos-carrier.valid.json",
    ]:
        result = _run_checker(fixture)
        assert result.returncode == 0, result.stdout + result.stderr


def test_structural_checker_rejects_carrier_authority_drift_fixtures():
    for fixture in [
        LL_FIXTURES / "decision-emission-carrier-missing-non-authority.invalid.json",
        LL_FIXTURES / "decision-emission-carrier-overreach-declaration.invalid.json",
    ]:
        result = _run_checker(fixture)
        # run_fixture_file's CLI exits 0 for both "PASS" and "PASS (negative correctly
        # rejected)"; the report text distinguishes the two, so assert on the text instead
        # of return code and additionally confirm a FAIL line was recorded internally.
        assert result.returncode == 0, result.stdout + result.stderr
        assert "negative correctly rejected" in result.stdout
        assert "FAIL" in result.stdout
