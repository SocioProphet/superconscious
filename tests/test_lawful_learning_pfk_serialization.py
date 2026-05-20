from superconscious_core.lawful_learning.pfk.serialization import (
    canonical_json,
    digest,
    hash_prefixed,
)


def test_canonical_json_is_key_order_stable():
    left = {"b": 2, "a": [3, {"d": 4, "c": 5}]}
    right = {"a": [3, {"c": 5, "d": 4}], "b": 2}

    assert canonical_json(left) == canonical_json(right)
    assert canonical_json(left) == '{"a":[3,{"c":5,"d":4}],"b":2}'


def test_digest_and_prefixed_digest_are_stable():
    value = {"claim_id": "synthetic", "status": "candidate"}

    hex_digest = digest(value)

    assert len(hex_digest) == 64
    assert hash_prefixed(value) == f"sha256:{hex_digest}"
