"""Lawful-learning local primitives for Superconscious.

H6 replay boundary:
- This package is a local utility namespace only.
- It does not authorize runtime model execution, certificate promotion,
  schema promotion, durable memory admission, or empirical validation.
- Runtime-facing clients must be added through separate review.

The origin branch imported llrel certificate classes that are not present on
main. Those imports are intentionally not replayed here to avoid creating a
broken public API.
"""

__all__: list[str] = []
