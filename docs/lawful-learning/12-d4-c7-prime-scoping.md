# Lawful Learning C-7' — D4 / ADE Extension Scoping

**Status:** Draft v1, research scoping after C-6'.  
**Date:** May 14, 2026.  
**Scope:** Comparative analysis of D-series extension paths, using D4 as the first stress test after the unified A_n theorem pattern.  
**Claim class:** [S|T|G] unless explicitly marked [M]. This is not theorem doctrine.

## 0. Placement

[G] C-6' closes the structural A_n pattern under the faithful-frame doctrine: A1 is the exceptional symplectic branch, and n >= 2 follows the Hermitian-cyclic branch.

[G] C-7' is not a mechanical continuation of C-6'. It is a research scoping layer for non-A singularity series.

[T] The D4 case is the correct first stress test because it combines:

```text
D-series Coxeter monodromy
Spin(8) center mismatch
triality
multiple natural representations
non-scalar monodromy options
```

## 1. Why the A_n template fails outside A_n

[M] For A_n, the Coxeter number is n+1 and the faithful-frame spatial group pattern uses:

```text
G_A_n = PSU(n+1)
pi_1(G_A_n) = Z/(n+1)
auxiliary = SU(n+1)
center = Z/(n+1)
```

[M] This exact match between Coxeter order and cyclic center is the structural coincidence that makes C-6' work.

[T] For D_n and the exceptional series, the Coxeter number does not match the available cyclic center of the natural simply connected compact group.

Representative mismatch:

```text
D_n: Coxeter number h = 2n - 2
Spin(2n) center = Z/4 for n odd, Z/2 x Z/2 for n even
D4: h = 6, center(Spin(8)) = Z/2 x Z/2
E6: h = 12, center = Z/3
E7: h = 18, center = Z/2
E8: h = 30, center = trivial
```

[G] Therefore the simple A_n rule — scalar central element of order equal to the Coxeter number — must not be copied into D/E cases.

## 2. D4 as the first C-7' target

[M] D4 has Coxeter number 6.

[M] The natural simply connected compact Lie group is `Spin(8)`, with center:

```text
Z(Spin(8)) = Z/2 x Z/2
```

[M] The outer automorphism group of `Spin(8)` is `S3`, the triality symmetry permuting the vector and two half-spin representations.

[T] D4 is therefore A-like only in the sense that it has a visible order-3 symmetry through triality, not because its center supplies a cyclic order-6 scalar.

## 3. Three candidate directions

### 3.1 Direction A — non-simple spatial/auxiliary group

[S|T] Add a non-simple factor or central extension so that a cyclic order-6 loop class is available.

Template:

```text
auxiliary candidate = Spin(8) x U(1) / relation
central phase source = U(1) factor or diagonal finite quotient
```

Potential advantage:

```text
retains scalar phase target
closest to A_n harness structure
most tractable computationally
```

Failure risk:

```text
ad hoc unless the polarization side canonically forces the extension
minimality argument is no longer automatic
adding U(1) factors is too cheap without a law selecting the extension
```

[G] This direction is admissible only if a Lawful Learning constraint explains why the extra factor is required by the D4 polarization structure, not merely added to repair the center mismatch.

### 3.2 Direction B — non-scalar central or finite-order auxiliary element

[S|T] Drop the scalar-central-element requirement. Replace it with a distinguished finite-order auxiliary element of order 6 that acts non-scalar on the polarization structure.

Template:

```text
zeta_D4 is finite-order in the auxiliary group
zeta_D4^6 = identity
zeta_D4 need not be scalar
```

Potential advantage:

```text
respects the fact that D4 has richer representation structure
avoids artificial U(1) factors
can use triality/Spin(8) internal structure
```

Failure risk:

```text
breaks the A_n P5/P6 scalar-center harness predicates
requires replacing zeta_central with an order-spectrum or conjugacy-class predicate
requires a new witness-object discipline
```

[G] This direction requires a new harness contract. The A_n predicate `zeta = omega * I` is invalid for D4 under this option.

### 3.3 Direction C — graded or decomposable polarization

[S|T] Treat the D4 polarization structure as decomposable or graded, with monodromy acting as a tuple across components rather than as a single scalar.

Template:

```text
V_D4 = direct sum or graded object
auxiliary structure acts componentwise or by triality permutation
Stokes observable is a tuple / operator / graded trace, not a scalar
```

Potential advantage:

```text
most faithful to D4 structure
naturally accommodates vector and spinor representations
may absorb triality without artificial central extensions
```

Failure risk:

```text
largest framework shift
requires replacing single-carrier V_A_n with graded auxiliary data
requires a new category, new harness predicates, and new certificate shape
```

[G] This is likely the mathematically right direction if the D-series Stokes phenomenon is intrinsically multi-component, but it is not a small patch to C-6'.

## 4. Recommended D4 work plan

[G] Start with D4 rather than a full D_n theorem. C-7' should not attempt to state a unified D/E theorem before D4 resolves the center/monodromy mismatch.

Recommended sequence:

1. **D4 representation inventory.** Record vector, half-spin, adjoint, and triality action surfaces.
2. **D4 monodromy target.** State exactly what order-6 Coxeter monodromy must witness.
3. **Option A/B/C decision.** Evaluate whether the witness is scalar-extension, non-scalar element, or graded tuple.
4. **Harness contract draft.** Define replacement predicates for the A_n scalar-center checks.
5. **Theorem statement only after witness-object selection.** Do not assert a D4 minimal theorem until the witness object is selected.

## 5. Candidate predicate replacements

[T] A D4 harness must not copy the A_n scalar predicate set unchanged.

Possible replacements:

| A_n predicate | D4 status | Candidate D4 replacement |
| --- | --- | --- |
| `zeta = omega * I` | invalid unless Direction A succeeds | `zeta_D4` finite-order witness object |
| `zeta^(n+1)=I` | replace | `zeta_D4^6 = I` plus minimal-order check |
| scalar centrality | generally invalid | conjugacy-class / commutant / graded-center check |
| Hermitian preservation | unknown until carrier chosen | representation-specific form preservation |
| rank predicates | required | D4 rank-four / triality-sensitive predicates |
| irreducibility | representation-dependent | Schur commutant check per component |

## 6. Non-claims

This document does not claim:

```text
D4 theorem proved
D_n theorem proved
D4 spatial group selected
D4 auxiliary group selected
D4 harness implemented
D4 Stokes-side observable computed
D/E series scoped
```

## 7. Handoff

The next concrete deliverable is a D4 representation-and-triality inventory:

```text
docs/lawful-learning/13-d4-representation-inventory.md
registry/lawful-learning/d4-representation-inventory.v0.1.json
```

Only after that inventory should a D4 theorem candidate or harness scaffold be written.
