"""Canonical JSON and digest helpers for lawful-learning artifacts."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for stable hashing.

    This intentionally uses a narrow JSON-canonicalization subset: sorted keys,
    no insignificant whitespace, and UTF-8 output. Future integration may replace
    this with semantic-serdes/RFC-8785 once that boundary is wired.
    """

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def hash_prefixed(value: Any) -> str:
    return f"sha256:{digest(value)}"
