# A1 Gate Minimality: Faithful Triad Action Version

**Status:** Draft v1, parallel to the non-faithful version.  
**Location target:** `docs/proofs/a1-gate-minimality-faithful.md`  
**Relationship to non-faithful version:** This proof note holds when condition (ii) is strengthened from “induces a nontrivial action on the triad” to “acts faithfully on the triad.” Under that strengthening, the minimal element changes from `SU(2)` acting through `SO(3)` with kernel `{+I,-I}` to `SO(3)` with auxiliary spin data on `V_A`. The two versions are not in conflict; they answer different questions about where the central sign lives.

## 0. Categorical setup

Let `A'_1` denote the category whose objects are tuples

```text
(G, rho_spatial, V_A, Q_A, S, gamma)
```

where:

- `G` is a connected compact Lie group;
- `rho_spatial: G -> SO(3)` is faithful and nontrivial;
- `V_A` is a two-dimensional complex vector space carrying a non-degenerate symplectic form `Q_A`;
- `S` is a `Spin(3)`-structure on `V_A`, represented by a homomorphism `sigma: Spin(3) -> Sp(V_A, Q_A) = SL(2,C)`;
- `gamma in pi_1(SO(3)) = Z/2` is the distinguished nontrivial loop class.

The compatibility between `rho_spatial` and `S` is that the `G` action on the triad, pulled back through `rho_spatial` and lifted through `sigma`, gives a well-defined projective action of `G` on `P(V_A)` that becomes linear after lifting through the auxiliary `Spin(3)` structure.

Morphisms preserve all six pieces of structure: group, spatial representation, polarization space, symplectic form, auxiliary spin structure, and loop class.

The key ontological move relative to the non-faithful version is that `V_A` and its symplectic action are not representations of `G` in `A'_1`. They are auxiliary data carrying their own `Spin(3)` symmetry, with `G` acting only through compatibility with that auxiliary symmetry. Under faithfulness, `G` cannot itself carry the `{+I,-I}` structure; that structure must come from the auxiliary spin frame.

## 1. Theorem statements

### T1' — Admissibility under faithfulness

An object `(G, rho_spatial, V_A, Q_A, S, gamma) in A'_1` realizes the A1 gate semantics iff:

1. `G` is a connected compact Lie group.
2. `rho_spatial: G -> SO(3)` is faithful and nontrivial.
3. The induced action on `V_A` through `rho_spatial` and `sigma` is non-abelian.
4. The distinguished loop class `gamma in pi_1(SO(3))` lifts under `sigma` to the central element `-I in SL(2,C)` of `Spin(3) = SU(2)`.
5. `Q_A` is preserved: `sigma(g)` is symplectic for all `g in Spin(3)`, and the induced action of `G` on `P(V_A)` factors through the projection `SL(2,C) -> PSL(2,C)`.

### T2' — Minimality under faithfulness

The class `A'_1` has a unique minimal object up to isomorphism:

```text
(SO(3), id, C^2, epsilon, sigma_spinor, gamma_can)
```

where `sigma_spinor: Spin(3) -> SL(2,C)` is the canonical spinor representation and `gamma_can` generates `pi_1(SO(3)) = Z/2`.

In particular, the central element `-I in Spin(3)` is the lift of `gamma`; the sign of the gate semantics resides in the auxiliary spin structure rather than in `G` itself; and `G = SO(3)` is the smallest connected compact Lie group satisfying T1'.

## 2. Proof of T2'

### Step 1 — Reduce to candidates by faithfulness

The connected compact subgroups of `SO(3)` are, up to conjugacy:

```text
{e}, SO(2), SO(3)
```

Under faithfulness, `G` must inject into `SO(3)`. Under connectedness and nontriviality, `G` is either `SO(2)` or `SO(3)`.

### Step 2 — Eliminate `SO(2)` by non-abelianness

`SO(2)` is abelian. Any induced image through the projective auxiliary spin structure remains abelian. Hence condition (iii) fails for `SO(2)`, and the only candidate is `SO(3)`.

### Step 3 — Verify `SO(3)` is admissible

For `G = SO(3)` with the canonical auxiliary spin structure:

- `SO(3)` is connected, compact, and Lie.
- `rho_spatial = id: SO(3) -> SO(3)` is faithful.
- The lifted action on `V_A` is the spinor representation of `Spin(3) = SU(2)` on `C^2`, which is non-abelian.
- The generator of `pi_1(SO(3))` lifts through the universal cover `Spin(3) -> SO(3)` to the nontrivial central element `-I`.
- The spinor representation preserves the canonical symplectic form `Q_A = epsilon`, and the induced `SO(3)` action on `P(V_A) = CP^1` is well-defined because projectivization quotients out `{+I,-I}`.

Thus the canonical tuple is admissible.

### Step 4 — Necessity and uniqueness of the auxiliary spin structure

#### 4a. Necessity

`SO(3)` has no faithful two-dimensional complex representation.

The irreducible complex representations of `SO(3)` are the integer-spin representations with dimensions `2l + 1`, hence all odd. No irreducible two-dimensional complex representation exists. A reducible two-dimensional representation is a sum of trivial representations and is not faithful.

Therefore, if `V_A` is a two-dimensional complex symplectic space, `SO(3)` cannot act linearly and faithfully on `V_A` preserving `Q_A`. The action must be projective, and the linear lift is supplied by the auxiliary `Spin(3)` structure.

#### 4b. Uniqueness

Given two `Spin(3)` structures on `(V_A, Q_A)` inducing the same projective action of `SO(3)` on `P(V_A)`, Schur's lemma implies that they differ by a scalar. Preservation of the symplectic form forces the scalar to satisfy `lambda^2 = 1`, hence `lambda = +/- 1`. The coherent loop condition selects the branch for which the lift of `gamma` terminates at `-I`.

Thus the auxiliary spin structure is unique up to the central `Z/2`, and condition (iv') fixes the canonical lift.

### Step 5 — Minimality

Steps 1 and 2 force `G = SO(3)`. Step 4 forces the auxiliary spin structure to be canonical up to the central branch fixed by the loop condition. The remaining data are canonical. Hence the faithful admissible category has a unique minimal object up to isomorphism.

## 3. Counterexamples when conditions are removed

- Remove non-abelianness: `SO(2)` is faithful and connected but abelian.
- Remove polarization compatibility: `SO(3)` acting only on its standard real triad lacks the two-dimensional symplectic spinor witness.
- Remove loop coherence: the wrong auxiliary branch lifts the distinguished loop to `+I` rather than `-I`.
- Remove faithfulness: the non-faithful theorem returns `SU(2)` with kernel `{+I,-I}` in the map to `SO(3)`.
- Remove connectedness: finite non-abelian subgroups and their binary covers enter, but they fail the connected Lie-group condition.

## 4. Structural notes

### 4.1 Where the sign lives

In the non-faithful version T2, `-I` is an element of `G = SU(2)` itself.

In the faithful version T2', `-I` is not an element of `G = SO(3)`. It is an element of the auxiliary `Spin(3)` structure on `V_A`:

```text
-I = sigma(gamma_lift_endpoint)
```

This is the central distinction between the two branches.

### 4.2 Catalan harness contract under T2'

The five-predicate harness content is numerically unchanged:

```text
Stokes = -1
Catalan jump = -4
pairing preserved
commutator = 2*sqrt(2)
zeta = -I
```

Under T2', the `zeta = -I` check tests the auxiliary spin structure, not a central element of `G = SO(3)`. The pairing-preservation check tests that `sigma` takes values in `SL(V_A) = Sp(V_A, Q_A)`. The Stokes and Catalan-jump checks test the abstract `Z/2` monodromy. The commutator check tests non-abelianness at the auxiliary Lie-algebra level.

### 4.3 Comparison with the non-faithful version

| Aspect | Non-faithful T2 | Faithful T2' |
| --- | --- | --- |
| Minimal group | `SU(2)` | `SO(3)` |
| Location of sign | central element of `G` | auxiliary `Spin(3)` frame |
| Loop class | path class in `G` | `pi_1(SO(3)) = Z/2` |
| `V_A` data | `G` representation | auxiliary `Spin(3)` representation |
| Polarization | internal to `G` | compatibility between `G` and auxiliary spin |
| Ontology | `G` knows the sign | `G` acts through auxiliary spin data |

## 5. Categorical subclaim C-1'

Under the strict morphism category preserving all six pieces of structure, `A'_1` is essentially singleton-shaped. The terminal-object formulation is therefore degenerate.

To make the categorical formulation nontrivial, broaden the category to admit disconnected closed subgroups of `O(3)` with compatible auxiliary structure. In that broadened category, `SO(3)` is the maximal connected admissible spatial group, while the full terminal object is the corresponding disconnected admissible group with compatible pin/spin auxiliary structure.

## 6. Load-bearing structural choices

- Loop class location: `gamma` lives in `pi_1(SO(3))`.
- Faithfulness: relaxing faithfulness collapses back to the non-faithful T2 branch.
- Representation theory: `SO(3)` has no faithful two-dimensional complex representation.
- Auxiliary spin: `Spin(3)` is auxiliary data on `V_A`; its identification with the universal cover of `SO(3)` is A1-specific and must not be overgeneralized.
- Morphism preservation: morphisms preserve group, spatial representation, `V_A`, `Q_A`, auxiliary spin structure, and loop class.

## 7. Summary

T2' states that under faithful action on the spatial triad, the minimal connected compact Lie group is `SO(3)`, with the A1 sign data carried by an auxiliary `Spin(3)` structure on `V_A`.

T2 and T2' are not competing theorems. They allocate the spin data differently.
