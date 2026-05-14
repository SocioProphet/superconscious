# Lawful Learning D4 Strategy B Scoping

**Status:** Draft v1, Strategy B scoping under C-7'.  
**Date:** May 14, 2026.  
**Scope:** D4 non-scalar auxiliary-element strategy after the D4 representation inventory.  
**Claim class:** [S|T|G] unless explicitly marked [M]. This is not yet D4 theorem doctrine.

## 0. Purpose

[G] The D4 representation inventory recommends Strategy B as the primary next scoping path.

[T] Strategy B keeps the natural D4 group-theoretic carrier and replaces the A_n scalar-center harness contract with a matrix-valued witness-object contract.

The central shift is:

```text
A_n: zeta = omega * I, scalar central element
D4 Strategy B: M_6, non-scalar order-6 element acting on an 8-dimensional representation
```

[G] This document scopes the D4 Strategy B theorem candidate and harness contract. It does not prove the theorem, construct the final Stokes-side observable, or implement the D4 harness.

## 1. Chosen Strategy B carrier

[T] We choose the initial Strategy B carrier as:

```text
G_spatial^D4 = Spin(8)
V_D4 = V = 8_v, the vector representation
form type = orthogonal
```

[M] `Spin(8)` is compact, simply connected, and of type D4.

[M] The vector representation `V = 8_v` is real type and preserves a non-degenerate orthogonal form.

[T] Triality-conjugate variants using `S+ = 8_s` or `S- = 8_c` are structurally equivalent candidates but are not selected in this first Strategy B scoping document.

[G] The choice of `V = 8_v` is a convention for concreteness, not a claim that triality is broken mathematically.

## 2. Why Strategy B is needed

[M] The D4 Coxeter number is 6.

[M] `Z(Spin(8)) = Z/2 x Z/2`, so no element of the center has order 3 or 6.

[G] Therefore the A_n scalar-center template cannot be applied to D4.

[T] Strategy B resolves this by moving the Stokes multiplier witness from a scalar central element to a non-scalar finite-order auxiliary element.

## 3. Candidate order-six element M_6

[T] Let `M_6` be an order-six element of `Spin(8)` whose image in the vector representation is an orthogonal 8x8 matrix with one 60-degree rotation block and six fixed directions.

Concrete vector-representation model:

```text
R_6 = diag(R(theta), I_6), theta = pi/3
R(theta) = [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]
```

[M] In `SO(8)`, this matrix has order 6.

[S] A specific lift `M_6 in Spin(8)` must be selected so that the lift has order 6 rather than order 12. This lift choice is part of the next harness/proof layer.

[G] This document scopes `M_6`; it does not yet construct the final certified lift.

## 4. Candidate T1'_D4^(B)

[S] Define the Strategy B admissible object as a tuple:

```text
(G, rho_8, V_D4, Q_D4, M_6, tau_policy)
```

where:

- `G` is the D4 spatial carrier, initially `Spin(8)`;
- `rho_8: G -> SO(V_D4, Q_D4)` is the selected eight-dimensional representation;
- `V_D4 = R^8` or its complexification `C^8` depending on harness convention;
- `Q_D4` is the preserved orthogonal form;
- `M_6` is a distinguished order-six non-scalar witness element;
- `tau_policy` records how triality is handled.

Candidate admissibility conditions:

```text
(i) compact Lie regularity
(ii'_D4) faithful eight-dimensional carrier action
(iii_D4) non-abelian active Lie action
(iv'_D4) order-six witness M_6 with minimal order exactly 6
(v'_D4) orthogonal polarization compatibility
(vi'_D4) triality policy declared
```

## 5. Candidate T2'_D4^(B)

[S] Candidate minimality statement:

```text
The Strategy B minimal D4 object is:
(Spin(8), 8_v, R^8, Q_std, M_6, triality_slice=V)
```

where `M_6` is a chosen lift of a 60-degree rotation block into `Spin(8)` acting in the vector representation.

[G] This is a candidate theorem statement, not a committed theorem in this document. It becomes theorem doctrine only after the `M_6` lift, triality policy, Schur/centralizer uniqueness, and harness predicates are fixed.

## 6. Proof obligations

### 6.1 Faithful carrier

[M] The vector representation of `Spin(8)` has kernel `<epsilon>`, so if strict faithfulness of `Spin(8)` itself is required, the carrier must be adjusted.

[T] There are two admissible framings:

```text
B1: G_spatial = SO(8), V = 8_v is faithful
B2: G_spatial = Spin(8), V = 8_v with auxiliary lift data explicitly retained
```

[G] This document keeps `Spin(8)` as the structure carrier but flags the faithfulness convention as a proof obligation. A theorem statement must choose B1 or B2 explicitly.

### 6.2 Order-six witness

[S] Construct `M_6` explicitly and prove:

```text
M_6^6 = I
M_6^k != I for 1 <= k < 6
```

in the selected representation and, if needed, in the selected lift.

### 6.3 Orthogonal preservation

[M] The chosen representation preserves the orthogonal form:

```text
rho_8(g)^T Q rho_8(g) = Q
```

for all `g` in the chosen carrier.

### 6.4 Centralizer / uniqueness analog

[S] The A2 Schur-uniqueness proof used irreducibility and scalar determinant constraints. Strategy B needs a different uniqueness argument, because the witness is non-scalar and the representation is orthogonal real type.

Candidate replacement:

```text
classify the centralizer or conjugacy class of M_6 in SO(8) / Spin(8)
fix M_6 by eigenvalue data and triality policy
prove uniqueness up to allowed conjugacy
```

[G] This is the likely hard point of Strategy B.

### 6.5 Triality policy

[T] There are two policies:

```text
slice policy: choose V = 8_v and record S+, S- as triality conjugates
triality-equivariant policy: formulate over the orbit {V, S+, S-}
```

[G] Strategy B scoping chooses the slice policy for harness usefulness, while recording that a theorem-level statement may later be made triality-equivariant.

## 7. Harness contract changes

[T] The A2 scaffold has scalar predicates. Strategy B changes the predicate surface.

| A_n/A2 predicate | D4 Strategy B replacement |
|---|---|
| `stokes_multiplier = omega * I` | `stokes_multiplier_matrix = M_6` |
| `zeta_central` | `M_6` carrier / centralizer / conjugacy predicate |
| `zeta^(n+1)=I` | `M_6^6 = I` and minimal-order check |
| Hermitian preservation | orthogonal preservation |
| rank predicates | D4 rank-four / triality-sensitive predicates |
| irreducibility | Schur commutant or centralizer dimension check |

[G] A D4 harness must not reuse the A2 scalar-center predicates unchanged.

## 8. Candidate D4 Strategy B harness predicates

Proposed predicates:

```text
P1_matrix_stokes_multiplier_D4
P2_order_six_minimality_D4
P3_orthogonal_preservation_D4
P4_nonabelian_so8_commutator_D4
P5_centralizer_or_conjugacy_class_D4
P6_triality_slice_declaration_D4
P7_no_scalar_center_reuse_D4
P8_representation_irreducibility_or_commutant_D4
```

[S] The exact P5 predicate depends on the selected uniqueness argument.

## 9. Open issues

### 9.1 Faithfulness convention

[G] Choose whether the theorem carrier is `SO(8)` for faithful vector action or `Spin(8)` with explicit auxiliary lift data.

### 9.2 Lift order

[S] The selected lift of `R_6` must be checked to have order 6 rather than order 12.

### 9.3 Triality

[G] Decide whether the theorem is stated with a chosen triality slice or triality-equivariantly.

### 9.4 Uniqueness

[S] Replace scalar Schur uniqueness with a centralizer/conjugacy uniqueness argument for `M_6`.

## 10. Recommended next deliverable

The next deliverable after this scoping document is:

```text
harness/d4_strategy_b_harness.py
harness/reference_reports/d4_strategy_b_report.v1.json
```

with scaffold predicates for the selected `M_6` matrix model and explicit open markers for the Stokes-side observable.

## 11. Non-claims

This document does not claim:

```text
D4 theorem proved
B1 or B2 faithfulness convention settled
M_6 certified in Spin(8)
D4 Stokes-side observable computed
D4 harness implemented
triality-equivariant theorem completed
full D/E series scoped
```
