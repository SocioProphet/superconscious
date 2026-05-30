from pathlib import Path

import pytest

from scripts import check_sourceos_interaction_boundary as checker

ROOT = Path(__file__).resolve().parents[1]


def test_valid_sourceos_interaction_boundary():
    checker.validate(ROOT / "tests/fixtures/integrations/sourceos-interaction-boundary.valid.json")


def test_rejects_sourceos_interaction_authority_drift():
    with pytest.raises(Exception):
        checker.validate(
            ROOT / "tests/fixtures/integrations/sourceos-interaction-boundary.authority-drift.invalid.json"
        )
