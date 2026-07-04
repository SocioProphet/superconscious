# SPO′ Baez Algebra Activation Engine

**Status:** exploratory capture.  
**Scope:** semantic geometry / algebraic interoperability / executable prototype.  
**Doctrinal boundary:** this is not a theorem, physics claim, consciousness claim, or canonical SourceOS schema. It is an inspectable bridge between the user's SPO′ semantic architecture and a typed algebraic prototype.

## Why this exists

The original SPO′ sketch used a ten-fold algebraic stack to describe recursive semantic activation inside the `S^{15}` field. That sketch intentionally mixed several registers:

- symbolic semantics;
- Baez-style algebraic motifs;
- Sefirot / cybernetic labels;
- recursive Subject–Predicate–Object activation;
- boundary phase matching across an `S^2` identity surface;
- an ontology-compiler direction.

The useful correction is not to delete the structure. The useful correction is to make the structure readable and typed.

This capture therefore preserves the exploratory mapping while separating the algebraic content into two orthogonal axes:

```text
Layer_n := (
  Carrier_n,
  Mode_n,
  x_n in Carrier_n,
  phi_n in S^2
)
```

where:

```text
Carrier ∈ {R, C, H, O}
Mode    ∈ {NORM, LIE, JORDAN, CLIFFORD, ALTERNATIVE, EXCEPTIONAL_JORDAN}
```

This removes the category drift from the first version, where concrete carriers such as `H` and `O` sat beside property classes such as `Lie algebra`, `Jordan algebra`, and `Clifford algebra`.

## Epistemic labels

| Label | Meaning |
|---|---|
| `[S]` | Symbolic / exploratory correspondence. |
| `[A]` | Algebraic construction or analogy. |
| `[F]` | Formalizable candidate definition. |
| `[C]` | Computable prototype artifact. |
| `[X]` | Known surrogate or non-final implementation. |

The Sefirot naming layer is `[S]`. The Cayley–Dickson carriers and coherence predicates are `[A]/[C]`. The activation predicate is `[F]/[C]`. The exceptional Jordan layer is currently `[X]`.

## Carrier spine

The only strictly algebraic ascent in this prototype is the Cayley–Dickson spine:

```text
R -> C -> H -> O
```

The prototype demonstrates the expected property transitions:

```text
R : ordered, commutative, associative
C : loses order
H : loses commutativity
O : loses associativity, retains alternativity
```

In the executable engine this is represented by a single `CD` class with level:

```text
0 = R
1 = C
2 = H
3 = O
```

## Modes and coherence predicates

| Mode | Coherence predicate |
|---|---|
| `NORM` | Hurwitz norm composition: `|xy|^2 = |x|^2 |y|^2`. |
| `LIE` | Jacobi identity for `[x,y] = xy - yx`; admitted only over associative carriers. |
| `JORDAN` | Jordan identity for `x ∘ y = (xy + yx)/2`. |
| `CLIFFORD` | Embedded quadratic witness: `v^2 = -|v|^2` on the pure-imaginary carrier part. |
| `ALTERNATIVE` | Middle Moufang identity: `(xy)(zx) = x((yz)x)`. |
| `EXCEPTIONAL_JORDAN` | Current surrogate: octonionic Moufang coherence; full `h_3(O)` is a later implementation. |

## Sefirot configuration table

Each Sefirah is now a named `(Carrier, Mode)` configuration rather than a free-floating algebra class.

| Sefirah | Configuration | Preserved role |
|---|---|---|
| Malkhut | `(R, NORM)` | Real grounding; semantic object reality. |
| Yesod | `(C, NORM)` | Phase oscillation; complex coherence. |
| Hod | `(H, NORM)` | Quaternionic rotation; subject-orientation stability. |
| Netzach | `(O, NORM)` | Octonionic emergence; nonlinear semantic branching. |
| Tiferet | `(H, CLIFFORD)` | Boundary mediation; embedded Clifford witness over `H`. |
| Gevurah | `(C, JORDAN)` | Observables, judgment, logical pruning. |
| Chesed | `(H, JORDAN)` | Permission, soft projection, admissible object formation. |
| Binah | `(C, LIE)` | Associative Lie-bracket coherence; placeholder for richer operator-mode treatment. |
| Chokhmah | `(O, ALTERNATIVE)` | Moufang branching and counterfactual recursion. |
| Keter | `(O, EXCEPTIONAL_JORDAN)` | `h_3(O)` / `F_4` direction; currently a surrogate. |

## Activation predicate

The executable SPO′ activation predicate is:

```text
Activation_n =
    previous layer on-shell
    ∧ next layer well-typed
    ∧ S² phase match
    ∧ next layer coherent
    ∧ carrier transition permitted
```

A carrier transition is admitted only if the next layer stays at the same Cayley–Dickson level or rises one level:

```text
Carrier_{n+1} ∈ {Carrier_n, Carrier_n + 1}
```

This gives a minimal typed realization of the earlier symbolic line:

```text
SPO′_n activates when the prior layer is resolved,
the boundary phase matches,
and the algebraic gate permits coherence.
```

## Current limitations

### Exceptional Jordan is a surrogate

`EXCEPTIONAL_JORDAN` currently verifies a necessary octonionic alternativity witness through Moufang coherence. It does **not** yet build the 27-dimensional exceptional Jordan algebra `h_3(O)` of `3x3` Hermitian octonionic matrices.

A future implementation should add:

```text
HermitianOctonionMatrix3x3
exceptional_jordan_product(X,Y) = (XY + YX)/2
exceptional_jordan_identity_check
```

### Lie is carrier-internal, not operator-level

The `LIE` mode currently uses the commutator bracket over associative carriers. That keeps the prototype typed, but it is not the richer object needed for gauge/operator semantics.

A future implementation should add an `OperatorMode` axis carrying operator Lie algebras such as:

```text
u(n), su(2), so(3), g_2 = Der(O)
```

This would let the engine distinguish:

```text
carrier-valued semantic state
operator algebra acting on the state
```

### Clifford is an embedded witness

`CLIFFORD` currently checks the quadratic relation on the pure-imaginary part of an associative carrier. It is not yet a full `Cl(V,Q)` constructor.

## Prototype location

Executable capture:

```text
prototypes/spo/spo_activation_engine.py
```

Run it locally with:

```bash
python3 prototypes/spo/spo_activation_engine.py
```

Expected result:

```text
ALL CHECKS PASS: True
```

## Interpretation boundary

This artifact preserves the exploratory SPO′ / Sefirot / Baez-algebra interface as a readable research object. It does not assert that semantic cognition, consciousness, Ricci flow, or physical matter are mathematically derived by this prototype.

The practical value is interoperability:

```text
semantic triple
  -> typed recursive layer
  -> carrier/mode gate
  -> boundary phase
  -> coherence witness
  -> activation result
```

That is a usable bridge toward ontology compilation, semantic validation, SocioSphere reasoning-state inspection, and future categorical/operator extensions.
