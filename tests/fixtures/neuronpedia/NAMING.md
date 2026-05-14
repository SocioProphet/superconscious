# Neuronpedia Fixture Naming

This document defines the fixture naming convention for the `tests/fixtures/neuronpedia/` subtree. Other fixture subtrees may use different conventions; if a broader convention is needed in the future, this convention can be hoisted to `tests/fixtures/NAMING.md`.

## Filename pattern

Positive fixtures:

```text
<schema>.valid.synthetic.json
```

Negative fixtures:

```text
<schema>.<failure-mode>.invalid.synthetic.json
```

Existing historical positive fixtures may omit `.valid` when the file pre-dates this convention. New positive fixtures should include `.valid` unless preserving a path already referenced by CI.

## Fields

- `<schema>` names the schema under test, such as `artifact-source-lock`, `provider-binding`, or `intervention-spec`.
- `<failure-mode>` describes the expected failure mode in stable kebab-case.
- `invalid` means the fixture is expected to fail schema validation.
- `valid` means the fixture is expected to pass schema validation.
- `synthetic` means the fixture is manually constructed and not derived from live Neuronpedia data.

## Failure-mode vocabulary

Use stable kebab-case names. Prefer these shapes:

```text
missing-<field>
<field>-empty
<field>-malformed
<field>-incomplete-for-<declared-type>
<field>-conflicts-with-<other-field>
references-nonexistent-<target>
```

Examples:

```text
artifact-source-lock.missing-decomposition.invalid.synthetic.json
artifact-source-lock.frozen-metadata-incomplete-for-sae.invalid.synthetic.json
provider-binding.writeback.invalid.synthetic.json
intervention-spec.execution.invalid.synthetic.json
```

## Layer 1 and Layer 2 boundary

These fixtures test Layer 1 structural validation unless explicitly stated otherwise.

Layer 1 is JSON Schema validation. It can enforce:

- required fields;
- enum values;
- field shape;
- frozen metadata required by declared decomposition type;
- explicit non-claims;
- schema-local constraints.

Layer 2 is runtime validation. It is tracked separately and can enforce:

- referenced source actually exists;
- content hash matches retrieved artifact content;
- source-lock chain consistency;
- verified-source registry checks;
- correspondence between declared decomposition type and actual artifact contents.

`ArtifactSourceLock` does not currently carry a schema-level `verification_status` field. Therefore a `references-unverified-source` fixture is out of scope for Layer 1 in this PR. Verified-source enforcement is a Layer 2 runtime concern.

## Adding a new `decomposition_type`

When adding a new `decomposition_type`, the contributor must:

1. Add the enum value to `schemas/neuronpedia/artifact-source-lock.v0.1.json` or its successor.
2. Add or update required `frozen_metadata` fields for that decomposition type.
3. Add a positive fixture for the new type.
4. Add at least one negative fixture named `<schema>.frozen-metadata-incomplete-for-<type>.invalid.synthetic.json`.
5. Update Layer 2 runtime validation so the frozen metadata is checked against the actual artifact contents.
6. Update this file if the new type introduces a new failure-mode naming pattern.

## Synthetic-only policy

Neuronpedia fixtures in this subtree are synthetic by default. Live provider exports, provider snapshots, or derived-from-real artifacts require a separate review because they may introduce licensing, privacy, provider-authenticity, or provenance obligations.
