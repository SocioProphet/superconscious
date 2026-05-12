# M1.5 Attribution Graph Doctrine

## Position in the chain

M1.5 sits between M1C and M1D. M1C establishes a feature-level causal triad. M1.5 elaborates that feature into edge-level attribution evidence. M1D then audits off-target effects with optional references to the M1.5 graph.

The chain is therefore:

```text
M0 -> M1A -> M1B -> M1C -> M1.5 -> M1D -> M1 composite -> M2 -> M3 -> M5
```

## Manifest / latent split

Each edge has two layers.

The manifest layer is the load-bearing claim: source node, target node, edge kind, and weight. The latent layer records the computation state used to produce that claim: patching trajectory, residuals, and replication count.

The graph has two digests.

```text
graph_manifest_digest = digest of edge manifest claims
graph_full_digest     = digest of edge manifest + latent state
```

These digests must differ. Equal graph digests collapse the manifest/latent distinction and fail semantic validation.

## Three replay states

`bit_exact_replay` means both the manifest digest and the full digest reproduce. The claim and latent computation state are reproduced.

`manifest_matches_latent_diverges` means the manifest digest reproduces while the full digest differs. The edge claims stand, but the latent computation state is not bit-identical.

`manifest_diverges` means the manifest digest differs. The certificate's edge-level claims are invalidated pending re-derivation.

## Implementability test

M1.5 uses a Willems-style inclusion test at graph level:

```text
N_hidden_attribution <= G_claimed <= P_uncontrolled_model
```

`N_hidden_attribution` is the hidden attribution computation traversed by the model. `G_claimed` is the edge set claimed by the graph. `P_uncontrolled_model` is the upper bound of edges the uncontrolled model could support.

A graph is implementable only when both inclusions hold. If replay diverges at the manifest layer, implementability is indeterminate until the graph is re-derived.

## Non-claims

M1.5 does not claim that the discovered edges are the only causally relevant paths. It does not claim cross-prompt generalization unless a separate fixture demonstrates that. It does not audit the attribution method itself; it records the method, configuration, and replay state so later review can evaluate method adequacy.

## Integration with M1D and M1 composite

M1D v1.2 may reference M1.5 attribution graphs through `attribution_graph_refs`. Empty references are permitted only when M1D explicitly states that the off-target audit is feature-aggregate only.

The M1 composite v1.2 certificate summarizes replay coverage through `attribution_graph_summary` and extends authority concentration accounting to six fragment types: M0, M1A, M1B, M1C, M1.5, and M1D.
