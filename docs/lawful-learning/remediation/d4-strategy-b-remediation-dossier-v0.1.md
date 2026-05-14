# Remediation Dossier — D4 Strategy B / PR #30 Prior-Analysis Gaps

**Version:** v0.1  
**Status:** analytic correction / handoff artifact / not theorem doctrine.  
**Scope:** D4 Strategy B scoping corrections for PR #30.  
**Evidence class:** correction of prior mathematical and structural analysis gaps.  

This dossier is a remediation artifact. It does not choose Strategy B over Strategy A, does not resolve any D4 pin, does not select a conjugacy class for `M_6`, does not modify the claim ledger, and does not promote Strategy B to theorem doctrine.

## 1. Gap inventory

| ID | Type | Subject | Remediation status |
|---|---|---|---|
| G1 | Structural | Tunneled on D4 and ignored surrounding PR #30 context | Reframed as Q1/Q2 |
| G2 | Structural | Did not ask what the Fuss-Catalan verifier verifies | Reframed as Q2 |
| G3 | Structural | Treated four CI lanes as undifferentiated | Reframed as Q3 |
| G4 | Structural | Presumed Strategy B without asking about Strategy A | Reframed as Q4 |
| G5 | Mathematical | Conflated `ker(Spin(8)->SO(8)) = Z/2` with `Z(Spin(8)) = (Z/2)^2` | Corrected |
| G6 | Mathematical | Claimed triality survives under B1 as duality | Corrected |
| G7 | Mathematical | Waved at order-6 `SO(8)` eigenvalue enumeration | Corrected as unverified derived enumeration |
| G8 | Mathematical | Called B1 lift pin vacuous | Corrected to hygiene obligation |
| G9 | Mathematical | Described Stokes data as a single class | Corrected to tuple/product-constraint data |
| G10 | Methodological | Did not apply the boundary-first discipline to this analysis | Recorded |

## 2. G5 — Spin(8) center correction

Correct structure:

```text
ker(Spin(8) -> SO(8)) = <epsilon> ~= Z/2
Z(Spin(8)) ~= (Z/2)^2
```

The three nontrivial central elements can be characterized by their signs on the three eight-dimensional irreducible representations:

| Element | Acts on V | Acts on S+ | Acts on S- | Notes |
|---|---:|---:|---:|---|
| `epsilon` | +1 | -1 | -1 | Kernel of `Spin(8) -> SO(8)` |
| `epsilon_prime` | -1 | +1 | -1 | Kernel of `Spin(8) -> HSpin+(8)` |
| `epsilon_double_prime` | -1 | -1 | +1 | Kernel of `Spin(8) -> HSpin-(8)` |

Triality permutes these three nontrivial central elements faithfully.

Consequence:

- Under B1 (`SO(8)` carrier), the scalar-center-reuse predicate tests against `{+I, -I}` only.
- Under B2 (`Spin(8)` carrier), the predicate tests against the full center `{1, epsilon, epsilon_prime, epsilon_double_prime}`.

The predicate is carrier-dependent and must not be checked as a carrier-independent pin.

## 3. G6 — Triality under B1

Triality is an outer automorphism of `Spin(8)` permuting `V`, `S+`, and `S-`, and also permuting the three nontrivial central elements.

An outer automorphism descends to a quotient only if it preserves the quotient kernel.

Therefore:

- Under B1 (`SO(8) = Spin(8)/<epsilon>`), full `S3` triality does not descend. Only the stabilizer of `<epsilon>` remains.
- Under B2 (`Spin(8)` carrier), full `S3` triality remains available.

So B1 is not “triality as duality.” It is a vector-slice carrier with only the residual `Out(SO(8)) = Z/2` diagram automorphism.

## 4. G7 — Order-six SO(8) class enumeration

A real orthogonal order-six element has blocks of type:

| Block | Eigenvalues | Order |
|---|---|---:|
| `+1` | `1` | 1 |
| `-1` | `-1` | 2 |
| `zeta2_rotation` | primitive third-root pair | 3 |
| `zeta_rotation` | primitive sixth-root pair | 6 |

Let:

```text
n = number of +1 blocks
m = number of -1 blocks
j = number of primitive third-root rotation blocks
k = number of primitive sixth-root rotation blocks
```

Constraints:

```text
n + m + 2j + 2k = 8
m even
order exactly 6: k >= 1 or (j >= 1 and m >= 2)
```

The derived enumeration gives 26 `SO(8)` conjugacy classes of order exactly 6. This is a derived reference count and must be independently verified in GAP/Sage before registry citation.

Named candidate regions:

1. `purely_primitive`: `(k=4, j=0, m=0, n=0)`;
2. `coxeter_flavored`: `(k=1, j=3, m=0, n=0)`;
3. `balanced`: `(k=2, j=2, m=0, n=0)`.

The current harness predicates do not uniquely select one class from the 26. The intended class must be declared as registry data or additional cutting predicates must be added.

## 5. G8 — B1 lift pin

Under B1, the Spin lift order is not a harness pin. But it is not harmless. It creates a hygiene obligation:

```yaml
b1_hygiene_obligation:
  permitted_carriers:
    - V_tensor_algebra
  forbidden_carriers:
    - half_spin_S_plus
    - half_spin_S_minus
    - triality_paired
  audit_rule: >
    Any observable used under B1 must factor through SO(8). Half-spin,
    triality-bridging, and spin-lattice observables are out of scope.
```

Without this clause, a nominal `SO(8)` carrier can silently leak `Spin(8)` dependence through half-spin characters or triality-paired observables.

## 6. G9 — Stokes observable structure

The D4 Stokes observable should not be represented as a single conjugacy class by default.

At an irregular singularity, Stokes data is generally a tuple:

```text
(S_1, S_2, ..., S_N)
```

with each `S_i` in a Stokes subgroup and with an ordered cyclic product constraint, e.g. equal to the formal monodromy or a convention-dependent inverse/conjugate.

The registry must eventually declare:

1. Poincare rank;
2. leading spectrum;
3. product-constraint convention;
4. conjugation gauge;
5. whether the observable is a single generator or the full tuple / wild-character-variety point.

## 7. Pin coupling

The six D4 Strategy B pins are not independent.

```text
faithfulness convention B1/B2
├── B1: lift order out of harness scope + hygiene obligation
├── B1: triality policy reduces to residual Out(SO(8)) = Z/2
├── B1: scalar-center predicate tests {±I}
├── B2: lift order load-bearing
├── B2: full S3 triality available
└── B2: scalar-center predicate tests Z(Spin(8)) = (Z/2)^2
```

The checker must encode this dependency so it cannot accept incoherent states such as:

```text
B1 selected + M6 lift order unresolved as theorem-blocking harness pin
B1 selected + full S3 triality policy
B2 selected + scalar-center check only against {±I}
```

## 8. Open context questions

Q1. What exactly does C-6' require: instantiate the A_n template, extend it, or contrast against it?

Q2. What identity does the Fuss-Catalan inverse-radius verifier check, and is it A_n-side support, D4-side support, or a bridge diagnostic?

Q3. What does each CI lane gate: Lawful Learning T2 Prime, Trust Surface, Superconscious CI, Certificate Doctrine CI?

Q4. Is Strategy A failed/archived or parallel/live?

Q5. Is the intended `M_6` class declared elsewhere, or must the harness discover it by adding cutting predicates?

## 9. Methodology correction

Future D4 Strategy B analysis must begin with gap elicitation if program-context inputs are missing. It must declare assumptions about C-6', Strategy A, Fuss-Catalan verifier scope, CI lanes, and intended conjugacy class before proposing theorem or checker changes.

## 10. Limits

The 26-class enumeration is not externally cross-checked. It should not be cited as a registry fact without independent computer-algebra verification.

The `Spin(8)` lift bifurcation range `26-52` is an upper/lower range, not an exact count.

The named conjugacy candidates are heuristic reference regions, not selected doctrine.
