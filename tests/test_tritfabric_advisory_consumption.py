from pathlib import Path

import pytest

from scripts import check_tritfabric_advisory_consumption as checker

ROOT = Path(__file__).resolve().parents[1]


def test_valid_tritfabric_advisory_consumption_boundary():
    checker.validate(ROOT / "tests/fixtures/integrations/tritfabric-advisory.valid.json")


def test_rejects_authority_drift():
    with pytest.raises(Exception):
        checker.validate(ROOT / "tests/fixtures/integrations/tritfabric-advisory.authority-drift.invalid.json")
