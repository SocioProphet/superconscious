# M1.5 Attribution Graph Doctrine

M1.5 sits between M1C and M1D. M1C establishes feature-level causal evidence. M1.5 elaborates that feature into edge-level attribution evidence. M1D may then reference those graphs when auditing off-target behavior.

Each edge has a manifest layer and a latent layer. The manifest layer is the load-bearing claim. The latent layer records computation state used to produce the claim. The graph therefore carries two digests: a manifest digest and a full digest. These digests must differ; equality collapses the distinction and fails semantic validation.

Replay has three states. `bit_exact_replay` means the graph and its latent state reproduce. `manifest_matches_latent_diverges` means the manifest claim reproduces while latent state differs. `manifest_diverges` means the claim diverges and the graph must be re-derived before it can support a downstream certificate.

The implementability check is graph-level: the claimed edge count must match the graph and, for full certificates, the inclusion discipline is hidden attribution <= claimed graph <= uncontrolled model upper bound.

M1.5 does not claim that the discovered edges are the only relevant paths. It does not claim cross-prompt generalization unless a separate certificate demonstrates that. It records the method and replay state so later review can evaluate method adequacy.
