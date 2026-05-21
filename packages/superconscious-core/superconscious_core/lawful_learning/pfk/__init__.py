"""Proof-fabric-kernel helper namespace for lawful-learning utilities.

This package currently exposes deterministic local serialization helpers only.
It does not perform proof checking, runtime evidence admission, source lookup,
or cross-repo authority promotion.
"""

from .serialization import canonical_json, digest, hash_prefixed

__all__ = ["canonical_json", "digest", "hash_prefixed"]
