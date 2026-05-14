# Lawful Learning T2' Polarization Scope

**Status:** Phase 3 categorical-doctrine extension.  
**Date:** May 13, 2026.  
**Scope:** Places the T2' faithful-triad result inside Lawful Learning as a categorical and governance artifact: scope declaration, predicate interpretation, witness-object discipline, and non-promotion boundary.  
**Claim class:** [M|T|G] where explicitly marked. No empirical claim is introduced.

## 0. Why this belongs in Lawful Learning

[G|T] T2' is not primarily a prime-residual claim. It is a doctrine for how a lawful system may interpret a predicate when the numerical result is unchanged but the mathematical witness object changes.

[G] In Lawful Learning terms, this is a **claim interpretation and promotion-control problem**: the same harness value may remain numerically stable while its permitted theoretical interpretation changes.

[T] The correct home is therefore the Lawful Learning categorical layer, not the Heller-Winters prime/residual lane.

## 1. T2' scope declaration

[M] T2' is the faithful-triad framing of the A1 gate-minimality result.

[G] Any Lawful Learning artifact using A1 gate-minimality must declare one of:

```text
A1 gate-minimality scope: T2
A1 gate-minimality scope: T2'
A1 gate-minimality scope: fragment-only
```

[G] A document with no scope declaration is not eligible for theorem-level reuse.

[T] Under T2, the central sign is internal to `G = SU(2)`. Under T2', the spatial group is `G = SO(3)` and the sign is carried by an auxiliary `Spin(3)`-structure on the polarization space `V_A`.

## 2. Lawful Learning interpretation rule

[G] Lawful Learning must separate three layers:

```text
numeric predicate value
witness object
reuse permission
```

[G] A numerical predicate value may remain unchanged while the witness object changes.

[G] Therefore no consumer may promote a harness predicate directly into a mathematical claim without consulting the predicate-interpretation table.

The controlling rule is:

```text
same numerical predicate, different witness object
```

## 3. Gate-minimality language patch

[G] The phrase `faithful into Spin(3)` is forbidden in Lawful Learning doctrine because it conflates the spatial group with auxiliary polarization data.

Use instead:

```text
faithful into SO(3); the auxiliary Spin(3)-structure lives on V_A
```

[M] Under T2', the auxiliary `Spin(3)`-structure is data about `V_A`. It is not data about `G`.

[T] The fact that the auxiliary group is isomorphic to the universal cover of `SO(3)` in A1 is an A1-specific coincidence. It must not be generalized into higher Ak cases.

## 4. Predicate interpretation table

[G] Lawful Learning binds the T2/T2' distinction through the table:

```text
registry/lawful-learning/t2-prime-predicate-interpretation.v0.1.json
```

[G] Harness metadata should refer to that table instead of hard-coding theorem interpretation into the harness source.

Recommended metadata shape:

```json
{
  "gate_minimality_scope": "T2'",
  "predicate_interpretation_table": "registry/lawful-learning/t2-prime-predicate-interpretation.v0.1.json"
}
```

[G] Adding this table changes a harness hash-chain head exactly once. It should not change again unless the harness source, numerical target, or interpretation table changes.

## 5. Five-predicate interpretation discipline

[T] The numerical targets do not change under T2'. The interpretation layer changes.

| Predicate | T2 interpretation | T2' interpretation |
| --- | --- | --- |
| `stokes_multiplier_observed == -1` | witnesses central `-I` in `G = SU(2)` | witnesses the lifted loop endpoint in the auxiliary `Spin(3)`-structure on `V_A` |
| `catalan_jump_coefficient ~= -4` | quantitative witness for the central sign in `G` | same numerical content, interpreted as auxiliary-structure evidence |
| `pairing_preservation` | `G` preserves `Q_A` on `V_A` | auxiliary `sigma` preserves `Q_A`; `G` acts projectively |
| `commutator_norm == 2*sqrt(2)` | non-abelianness carried inside `G = SU(2)` | non-abelianness carried by the auxiliary spin algebra, compatible with `so(3)` |
| `zeta == -I` | `zeta` is an element of `G` | `zeta` is auxiliary data on `V_A`, not an element of `SO(3)` |

[G] The table is a non-promotion control. It prevents a consumer from citing a T2' predicate as if it witnessed a T2 group-level object.

## 6. C-1' categorical placement

[M|T] C-1' belongs to Lawful Learning as a categorical composition statement over broadened admissible categories.

[T] The strict connected category collapses too far: it is effectively singleton-shaped once T2' is fixed.

[M] To make the universal-property claim non-trivial, the category is broadened to admit disconnected closed subgroups of `O(3)` with compatible auxiliary structure.

Recommended two-clause doctrine:

```text
SO(3) is the maximal connected admissible spatial group.
O(3) with compatible pin/spin auxiliary structure is the terminal admissible group in the broadened category.
```

[G] This is a categorical doctrine statement for lawful composition and scope control. It does not create a new empirical claim.

## 7. A2 boundary

[S] The A2 extension is conjectural.

[T] T2' provides a template only:

```text
spatial-symmetry group + auxiliary group preserving the form on V_A
```

[S] For A2, the loop class is expected to be order three, the auxiliary group is conjecturally SU(3)-type, and the form is conjecturally Hermitian.

[G] The spatial-symmetry group for A2 is not identified here. It is a research problem, not a mechanical extension of T2'.

## 8. Lawful Learning non-claims

This document does not claim:

```text
A2 theorem proved
A2 spatial group identified
runtime harness updated
hash-chain head recomputed
empirical evidence added
all downstream documents patched
production proof assistant formalization completed
```

[G] Those claims require future evidence, checker, or formalization lanes.

## 9. Handoff

The next mechanical step is to bind this document into Phase 6 checker coverage by adding a schema/checker rule requiring:

```text
if gate_minimality_scope is T2 or T2' then predicate_interpretation_table is present
```

Until then, this document is the controlling doctrine for T2' interpretation under Lawful Learning.
