# M0 Training Provenance Doctrine

M0 sits upstream of M1A source-lock. M1A pins what an artifact is. M0 records what is known about how that artifact came to exist.

The required commitments are dataset, code, config, seed, base model, checkpoint, eval spec, and compute environment. Each commitment must be present and either populated or explicitly marked unavailable, withheld, not applicable, or unknown.

The temporal invariant is that the model commitment timestamp must precede the eval-spec commitment timestamp. If either timestamp is unavailable, the temporal flag must be false and the certificate must state the limitation.

The provenance completeness index is computed as available commitments divided by eight. The interpretation bands are fully certified, partial provenance, minimal provenance, and no-provenance external artifact.

M0 does not prove training execution correctness. It does not prove that a dataset is unbiased. It does not prove that the resulting artifact has a behavioral property. It commits to typed terminals and to the temporal anti-overfit constraint.

M1A v1.2 must either reference an upstream M0 certificate or explicitly state that no upstream provenance certificate exists.
