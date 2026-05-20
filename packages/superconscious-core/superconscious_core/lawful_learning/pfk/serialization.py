"""Deterministic JSON and digest helpers for lawful-learning artifacts.

Boundary:
- This is a narrow local canonicalization helper, not full RFC 8785/JCS.
- It does not perform semantic-serdes normalization.
- It does not prove artifact authenticity or source existence.
- It does not admit evidence into any runtime ledger.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for stable local hashing.

    This intentionally uses a narrow subset: sorted keys, compact separators,
    and UTF-8 output. Future integration may replace this with semantic-serdes
    or RFC 8785 once that authority boundary is wired.
    """

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    """Return a sha256 hex digest over ``canonical_json(value)``."""

    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def hash_prefixed(value: Any) -> str:
    """Return a ``sha256:<hex>`` digest over ``canonical_json(value)``."""

    return f"sha256:{digest(value)}"
