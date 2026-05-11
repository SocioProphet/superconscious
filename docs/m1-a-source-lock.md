# M1A Source-Lock Certificate

## Status

M1A hardens source-lock from an identity note into a certificate fragment.

The M1A certificate does not prove the steering effect and does not prove implementability. It records the fixed preconditions against which M1B-M1D will be verified: controller spec, model artifact, SAE artifact, code state, schema, runtime stub, datasets, generated artifacts, and evidence-ledger entry.

## Files

```text
schemas/m1/source-lock.v1.json
src/m1/certificate_utils.py
src/m1/generate_m1a_certificate.py
src/m1/verify_source_lock.py
src/m1/verify_weights.py
outputs/m1/certificates/m1a-source-lock.json
outputs/m1/evidence-ledger.jsonl
```

Generated files under `outputs/m1/` are runtime artifacts and should be regenerated per checkout/runtime rather than treated as source doctrine.

## Generate

```bash
make m1a-generate
```

This resolves public Hugging Face metadata for the locked model and SAE, hashes repo files, records dataset placeholders, seals the M1A certificate fragment, and appends a `fragment_sealed` event to:

```text
outputs/m1/evidence-ledger.jsonl
```

## Verify

```bash
make m1-verify-source-lock
```

Default verification allows pending model weights / SAE parameter downloads and should exit with code `1` for partial verification until runtime artifacts are available.

Strict verification:

```bash
make m1-verify-source-lock-strict
```

Strict mode requires downloaded weights and SAE params to be verified and should be used once the runtime cache is populated.

## Exit codes

```text
0: full verification passed
1: partial verification passed; weights or SAE params pending
2: verification failed
3: schema validation failed
4: network failure or upstream artifact unavailable
```

## Hash convention

The certificate carries two hashes:

- `fragment_sha256`: event-snapshot hash. It includes the timestamp and therefore changes when the certificate is regenerated.
- `content_sha256_canonical`: substantive-content hash. It excludes volatile and derived identity fields, so regenerated equivalent certificates can be detected by the ledger.

This preserves both event auditability and substantive equivalence.

## Ledger discipline

The evidence ledger is JSONL and append-only. Each generator or verifier run appends an event:

```text
fragment_sealed
fragment_verified
fragment_failed_verification
fragment_superseded
```

Multiple verification events for the same fragment are intentional. The ledger answers when a fragment was verified and whether the most recent verification passed.

## Pending work

`src/m1/verify_weights.py` is a runtime placeholder. It names the required runtime hashing step but does not yet mutate certificate fragments in place. The mutation path should be added once the M1B/M1C local cache layout is fixed.

## Acceptance criterion

M1A is operational when a clean checkout can run:

```bash
make m1a-generate
make m1-verify-source-lock
```

and obtain a structurally valid certificate plus partial verification because weights and SAE params are not downloaded yet.
