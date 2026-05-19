# Theorem-Language Review Gate — 2026-05-19

**Status:** H4 hardening control.  
**Scope:** Lawful-learning and proof-note files that use theorem-facing mathematical language.

## Rule

A document may use theorem-facing language only in one of three states:

```text
proof_reviewed
proof_review_required
theorem_track_candidate
```

If a document has no cited proof-review evidence, the strongest allowed status is:

```text
theorem_track_candidate
```

or, for docs that mainly organize vocabulary and governance:

```text
structural_doctrine_with_proof_review_required_for_mathematical_subclaims
```

## Forbidden promotion patterns

```text
proof sketch => proved theorem
harness passes => theorem proved
scaffold value => direct computation complete
inverse-radius diagnostic => Stokes-side witness
representation inventory => selected D4 theorem
CI green => mathematical verification
```

## Required local banner

The following banner or equivalent must appear near the top of theorem-facing docs until proof review is recorded:

```text
H4 theorem-language gate: this document is theorem-track / proof-review-required. It may define candidate objects, proof skeletons, and harness obligations, but it is not proof-reviewed theorem doctrine and must not be cited downstream as a proved theorem without a later proof-review record.
```

## Direct-computation boundary

For A2 and A_n material, the following distinction is mandatory:

```text
scaffold-supported numerical target != direct Stokes-side computation
Fuss-Catalan inverse-radius evidence != direct Stokes-side witness
passing harness predicates != theorem proof
```

## Promotion requirements

To promote a theorem-track candidate to theorem-facing status, a follow-up PR must add:

```text
self-contained proof note
explicit definitions
lemma dependency list
known-obstruction discussion
reviewer/auditor note or formalization plan
non-claims for what is not proven
```

For computational harness claims, the follow-up PR must add:

```text
pinned protocol
reference inputs
reference outputs
negative controls
receipt/hash manifest
claim boundary stating what the diagnostic can and cannot license
```

## Initial files governed by this gate

```text
docs/proofs/a1-gate-minimality-faithful.md
docs/lawful-learning/10-a2-gate-minimality-scoping.md
docs/lawful-learning/11-an-unified-gate-minimality-theorem.md
docs/lawful-learning/13-d4-representation-inventory.md
docs/lawful-learning/14-d4-strategy-b-scoping.md
```

## Non-claim

This gate does not assert that any mathematical statement is false. It only prevents unreviewed theorem-facing language from being promoted as proof-complete doctrine.