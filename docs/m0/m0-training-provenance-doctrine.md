# M0 Training Provenance Doctrine

## Position in the chain

M0 sits upstream of M1A source-lock. M1A pins what an artifact is; M0 records what is known about how the artifact came to exist.

## Constitutional invariant

The model commitment timestamp must precede the eval-spec commitment timestamp. This prevents benchmark overfitting structurally: if an eval-spec is committed first and an artifact is optimized against it, the constraint is violated and the certificate must not be treated as satisfied.

For external artifacts where training timestamps are unavailable, `model_precedes_eval_spec` must be set to `false` and the `non_claims` array must record the limitation explicitly.

## The eight commitments

The required commitments are: dataset, code, config, seed, base model, checkpoint, eval spec, and compute environment. Each commitment is either populated with structured evidence or explicitly marked as unavailable, withheld, not applicable, or unknown. Silent omissions are schema validation errors.

## Provenance completeness index

The completeness index is computed as:

```text
available_commitments / 8
```

Interpretation bands:

```text
1.0          fully_provenance_certified
0.625-0.875  partial_provenance
0.25-0.5     minimal_provenance
0.0-0.125    no_provenance_external_artifact
```

## What M0 does not prove

M0 does not prove training execution correctness. It does not prove that a dataset is unbiased. It does not prove that the resulting artifact has any specific behavioral or interpretability property. It commits to typed terminals and the temporal constraint. Behavioral properties remain the job of M1B through M5.

## Integration with M1A

M1A v1.2 requires either `upstream_training_provenance_ref` to point to a valid M0 certificate, or `non_claims` to contain a statement matching `No upstream provenance certificate exists`. There is no third option.
