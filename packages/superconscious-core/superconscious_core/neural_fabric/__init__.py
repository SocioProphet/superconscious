"""Neural Fabric reference primitives.

This package contains stable, CPU-only primitives extracted from the
activation-time targeting suite. Research scripts may depend on these modules;
runtime promotion still requires policy review and production evidence.
"""

from .may_wigner import may_wigner_number, classify_may_wigner
from .hopfield import hopfield_retrieve, query_injection, logit_boost

__all__ = [
    "may_wigner_number",
    "classify_may_wigner",
    "hopfield_retrieve",
    "query_injection",
    "logit_boost",
]
