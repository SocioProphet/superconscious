"""Lawful-learning runtime primitives for Superconscious.

This package is structural and deterministic. It provides certificate,
ledger, attribution-audit, and training-provenance primitives. It does not
claim production SAE training, runtime model execution, or empirical validation.
"""

from .llrel.certificates import ActiveLawCertificate, CertificateVerdict

__all__ = ["ActiveLawCertificate", "CertificateVerdict"]
