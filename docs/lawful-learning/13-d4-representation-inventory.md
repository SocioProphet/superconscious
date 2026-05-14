# Lawful Learning D4 Representation Inventory

**Status:** Scoping deliverable v1 under C-7'.  
**Date:** May 14, 2026.  
**Scope:** Representation-theoretic inventory for D4 after C-7' scoping.  
**Claim class:** [M|T|G] where marked. This inventory is not theorem doctrine.

## 0. Purpose and scope

[G] C-7' identified three candidate strategies for extending the T2' template beyond the A-series. This inventory records the representation-theoretic facts needed before selecting a D4 strategy.

[T] The inventory clarifies which representations of `Spin(8)` and adjacent groups are available as polarization-space candidates under the three strategies:

```text
A — non-simple extension
B — non-scalar auxiliary element
C — graded / decomposable polarization
```

[G] This document does not commit to a D4 theorem. It supplies the representation inventory on which a future D4 strategy-B scoping document should build.

## 1. Spin(8) structural data

[M] `Spin(8)` is the simply connected compact simple Lie group of type `D4`.

```text
rank = 4
dimension = 28
Coxeter number h(D4) = 6
|W(D4)| = 192 = 2^6 * 3
```

[M] Its center is the Klein four-group:

```text
Z(Spin(8)) = Z/2 x Z/2 = {1, epsilon, delta, epsilon_delta}
```

[M] The center has no element of order 3 or 6.

[G] This is the structural obstruction to naively extending the A_n scalar-center template to D4. The D4 Coxeter order is 6, but `Spin(8)` does not supply a cyclic scalar center of order 6.

## 2. Triality

[M] `Out(Spin(8)) = S3`.

[T] The order-three triality automorphism cyclically permutes the three eight-dimensional irreducible representations:

```text
V -> S+ -> S- -> V
```

[T] The order-two conjugation exchanges `S+` and `S-` while fixing `V`.

[G] Triality makes D4 the most A-like D-series case, but it is not the same thing as a cyclic scalar center of order 6.

## 3. Quotients by central subgroups

[M] The quotients by central subgroups are:

| Quotient | pi_1 | Dimension | Notes |
|---|---:|---:|---|
| `Spin(8)` | trivial | 28 | simply connected |
| `Spin(8)/<epsilon> = SO(8)` | `Z/2` | 28 | standard D4 Lie group |
| `Spin(8)/<delta>` | `Z/2` | 28 | triality-conjugate quotient |
| `Spin(8)/<epsilon_delta>` | `Z/2` | 28 | triality-conjugate quotient |
| `Spin(8)/Z = PSO(8)` | `Z/2 x Z/2` | 28 | trivial center |

[G] None has `pi_1 = Z/6` or cyclic fundamental group of order divisible by 3. This confirms that the A_n faithful-frame loop-class template fails directly at D4.

## 4. Central actions on the three 8-dimensional irreducibles

[M] The central action table is:

| Element | Order | On `V = 8_v` | On `S+ = 8_s` | On `S- = 8_c` |
|---|---:|---:|---:|---:|
| `1` | 1 | `+I` | `+I` | `+I` |
| `epsilon` | 2 | `+I` | `-I` | `-I` |
| `delta` | 2 | `-I` | `+I` | `-I` |
| `epsilon_delta` | 2 | `-I` | `-I` | `+I` |

[T] Each nontrivial central element fixes exactly one of the three 8-dimensional irreducibles and acts by sign on the other two. Triality permutes this table.

## 5. Small representation catalog

[M] The irreducible complex representations of `Spin(8)` are parametrized by dominant weights in the D4 fundamental-weight basis. For the C-7' decision, the relevant small representations are:

| Dimension | Highest weight | Description | F-S indicator | Central character |
|---:|---|---|---:|---|
| 1 | `(0,0,0,0)` | trivial | `+1` | trivial |
| 8 | `(1,0,0,0)` | `V`, vector | `+1` | vector character |
| 8 | `(0,0,1,0)` | `S+`, positive spinor | `+1` | spinor-plus character |
| 8 | `(0,0,0,1)` | `S-`, negative spinor | `+1` | spinor-minus character |
| 28 | `(0,1,0,0)` | adjoint `so(8)` | `+1` | trivial |
| 35 | `(2,0,0,0)` | traceless symmetric on `V` | `+1` | trivial |
| 35 | `(0,0,2,0)` | traceless symmetric on `S+` | `+1` | trivial |
| 35 | `(0,0,0,2)` | traceless symmetric on `S-` | `+1` | trivial |
| 56 | `(1,0,1,0)` | `V tensor S+` component | `+1` | nontrivial |
| 56 | `(1,0,0,1)` | `V tensor S-` component | `+1` | nontrivial |
| 56 | `(0,0,1,1)` | `S+ tensor S-` component | `+1` | nontrivial |
| 112 | `(0,1,1,0)` | higher component | `+1` | nontrivial |
| 160 | `(1,1,0,0)` | higher component | `+1` | nontrivial |
| 300 | `(0,2,0,0)` | symmetric adjoint component | `+1` | trivial |
| 350 | `(1,0,2,0)` | higher component | `+1` | nontrivial |

[M] All listed representations are real type with Frobenius-Schur indicator `+1`.

[T] This makes D4 a third form-type regime: orthogonal, distinct from A1 symplectic and A_n>=2 Hermitian.

## 6. Dimension-6 obstruction

[M] `Spin(8)` has no faithful six-dimensional complex representation.

Proof sketch: the smallest nontrivial irreducible complex representations of `Spin(8)` have dimension 8. A six-dimensional representation would have to be a direct sum of irreducibles of dimension at most 6. The only such irreducible is the one-dimensional trivial representation. A sum of trivial representations is not faithful.

[G] Therefore the literal A_n dimensional pattern `V_A_n = C^(n+1)` cannot be copied to D4 as `V_D4 = C^6` under faithful `Spin(8)` action.

## 7. Strategy A — non-simple extension

[T] Strategy A augments the group to supply the missing cyclic class:

```text
G_A = (Spin(8) x U(1)) / Z_diag
```

[T] A diagonal quotient such as `<(epsilon, exp(pi*i/3))>` can couple a `Spin(8)` central involution to a sixth root in the `U(1)` factor.

Potential advantage:

```text
preserves scalar phase target
closest to the A_n scalar harness contract
```

Obstruction:

```text
does not produce a six-dimensional faithful Spin(8)-based polarization space
minimality becomes non-canonical unless the polarization law forces the extension
```

[T] Natural polarization candidates remain eight-dimensional, e.g. `V tensor chi_2`, `S+ tensor chi_1`, or `S- tensor chi_1`.

## 8. Strategy B — non-scalar auxiliary element

[T] Strategy B keeps the natural D4 group-theoretic carrier and abandons the scalar-center requirement.

```text
G_spatial = Spin(8) or a quotient by a central subgroup
V_D4 = one of V, S+, S-
zeta_D4 = M_6, an order-six non-scalar auxiliary element
```

[T] The harness P1/P5/P6 predicates change from scalar checks to matrix/conjugacy/order checks.

Candidate replacements:

```text
P1: matrix-valued Stokes multiplier M_6
P5: centrality replaced by conjugacy / centralizer / carrier-specific check
P6: M_6^6 = I plus minimal-order check
```

[G] Strategy B is the primary recommendation because it preserves the natural `Spin(8)` representation theory while requiring only bounded harness-contract changes.

## 9. Strategy C — graded or decomposable polarization

[T] Strategy C replaces a single polarization carrier with a decomposable or graded object:

```text
V_D4 = V1 direct_sum V2
monodromy order = lcm(order on V1, order on V2)
```

Potential advantage:

```text
most faithful to multi-component D/E phenomena
```

Obstruction:

```text
natural Spin(8) representation dimensions do not produce a clean total dimension six split
requires new category, new harness predicates, and new certificate shape
```

[G] Strategy C remains a long-horizon backup direction, not the recommended immediate path.

## 10. Comparative assessment

| Strategy | Spatial group | pi_1 target | V_D4 dimension | Form type | Harness P1 type | Status |
|---|---|---|---:|---|---|---|
| A | `(Spin(8) x U(1))/Z_diag` | `Z/6` | 8 | orthogonal | scalar | backup |
| B | `Spin(8)/Z'` | `Z/2` or `Z/2 x Z/2` | 8 | orthogonal | 8x8 matrix | primary |
| C | graded product carrier | combined | variable | mixed | block matrix | backup |

[G] The primary recommendation is Strategy B. Strategy A and Strategy C remain audited fallback paths if the Strategy B proof or harness contract hits a structural obstacle.

## 11. Open structural questions

### 11.1 Triality treatment

[T] The three eight-dimensional irreducibles `V`, `S+`, and `S-` are permuted by triality.

Open choices:

```text
(i) choose one, likely V, and record triality-conjugate variants;
(ii) state the theorem triality-equivariantly.
```

[G] This inventory does not resolve the choice. The next Strategy B scoping document must.

### 11.2 Central-element analog

[T] Once a polarization carrier is selected, the analogous sign element must be fixed by convention. For `V`, the element acting as `-I` is `delta`; for `S+` and `S-`, the corresponding elements are triality-conjugate.

[G] This is a convention choice that must be explicit before a D4 theorem candidate is well-defined.

### 11.3 Higher D and E series

[G] D4 is exceptional due to triality. D_n for n>=5 and E6/E7/E8 do not inherit triality. This inventory does not scope the full D/E series.

## 12. Next concrete deliverable

[G] The next deliverable is:

```text
docs/lawful-learning/14-d4-strategy-b-scoping.md
registry/lawful-learning/d4-strategy-b-scoping.v0.1.json
```

It should commit to:

1. `Spin(8)` or a declared quotient as the D4 spatial carrier.
2. A chosen 8-dimensional irreducible, likely `V`, as polarization space.
3. An explicit order-six element `M_6` with matrix realization.
4. T1' and T2' statements for D4 under Strategy B.
5. Harness modifications: matrix-valued P1, order-six P6, orthogonal form preservation, and triality bookkeeping.

## 13. Non-claims

This document does not claim:

```text
D4 theorem proved
D4 strategy B selected as theorem
M_6 constructed
D4 harness implemented
D4 Stokes observable computed
full D/E series scoped
```
