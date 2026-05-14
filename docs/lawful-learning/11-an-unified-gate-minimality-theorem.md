# Lawful Learning C-6' — Unified A_n Gate-Minimality Theorem

**Status:** Draft v1, theorem-pattern statement under T2' faithful-frame doctrine.  
**Date:** May 14, 2026.  
**Scope:** Unified `A_n` structural theorem for `n >= 2`, with `A_1` retained as the exceptional symplectic base case.  
**Claim class:** [M|T|G] as marked. Direct Stokes-side coefficients remain harness/evidence obligations.

## 0. Placement

[G] This document extends the committed Lawful Learning T2' / A2 theorem lane from individual A1 and A2 statements to the uniform `A_n` structural theorem pattern.

[G] It does not compute direct Stokes-side observables. It states the structural theorem pattern and the corresponding parametric harness targets.

## 1. Exceptional base case: A1

[M] Under T2', the faithful-frame A1 minimal object is:

```text
(SO(3), Ad/spatial triad, C^2, epsilon, Spin(3)=SU(2), gamma_can)
```

[M] The auxiliary representation is the `SU(2)` spinor representation on `C^2`.

[M] The central element is:

```text
- I_2
```

[M] The form on `V_A1 = C^2` is symplectic because the defining `SU(2)` representation is quaternionic type.

[T] This is the exceptional low-rank case: `SU(2) ~= Sp(1)`, and the defining representation has invariant symplectic form.

## 2. Unified statement for n >= 2

[M] For `n >= 2`, the faithful-frame structural theorem has minimal object:

```text
(PSU(n+1), Ad, C^(n+1), H_std, sigma_def, gamma_can)
```

where:

- `PSU(n+1) = SU(n+1) / Z(SU(n+1))`;
- `Z(SU(n+1)) = Z/(n+1)`;
- `pi_1(PSU(n+1)) = Z/(n+1)`;
- `Ad` is the faithful adjoint-frame action on `su(n+1)`;
- `sigma_def: SU(n+1) -> U(C^(n+1), H_std)` is the defining representation;
- `gamma_can` is the generator of `pi_1(PSU(n+1))`;
- the lifted central endpoint is `omega_(n+1) * I_(n+1)` with `omega_(n+1) = exp(2*pi*i/(n+1))`.

[M] The central element is not an element of `G = PSU(n+1)`. It lives in the auxiliary `SU(n+1)` structure on `V_A_n = C^(n+1)`.

## 3. Form type dichotomy

[M] The form type splits as:

```text
A1:       symplectic form on C^2
A_n>=2:   Hermitian form on C^(n+1)
```

[M] For `n >= 2`, the defining representation of `SU(n+1)` is complex type. It is not self-dual in the relevant sense and does not carry the A1 symplectic bilinear structure.

[G] Any uniform `A_n` harness must branch on this dichotomy rather than mechanically copying the A1 symplectic predicate.

## 4. Proof skeleton for n >= 2

### 4.1 Candidate reduction

[M] The required loop-class structure is `Z/(n+1)`. The faithful-frame spatial group must carry the corresponding projective loop class while acting faithfully on the adjoint frame.

[M] `PSU(n+1)` has fundamental group `Z/(n+1)` and faithful adjoint action on `su(n+1)`.

[T] The reduction step excludes lower-rank or abelian candidates that fail either non-abelianness, faithful adjoint-frame action, or the required cyclic loop class.

### 4.2 Admissibility

[M] `PSU(n+1)` is connected, compact, and Lie. Its universal cover is `SU(n+1)`, and the center of `SU(n+1)` maps to the loop class of `PSU(n+1)`.

[M] The defining auxiliary action of `SU(n+1)` on `C^(n+1)` preserves `H_std`.

### 4.3 Auxiliary necessity

[M] The defining `(n+1)`-dimensional representation of `SU(n+1)` does not descend to a faithful linear representation of `PSU(n+1)` because the center acts nontrivially.

[M] The corresponding `PSU(n+1)` action is projective, and the auxiliary `SU(n+1)` structure is required for the linear action on `V_A_n`.

### 4.4 Schur uniqueness

[M] Given two auxiliary `SU(n+1)` structures inducing the same projective action, Schur's lemma reduces their difference to a scalar.

[M] Hermitian preservation gives `|lambda| = 1`. The special-unitary determinant condition gives:

```text
lambda^(n+1) = 1
```

[M] The coherent loop condition selects the branch `omega_(n+1) * I_(n+1)`.

### 4.5 Minimality

[M] Candidate reduction plus auxiliary uniqueness identifies the minimal admissible object up to isomorphism:

```text
(PSU(n+1), Ad, C^(n+1), H_std, sigma_def, gamma_can)
```

## 5. Parametric harness targets

[T] The uniform `A_n` scaffold harness targets are:

```text
stokes_multiplier_A_n          = omega_(n+1)
coxeter_jump_coefficient_A_n   = - (n+1)^(n+1) / n^n
polarization_preservation_A_n  = Hermitian preservation for n >= 2
zeta_A_n                      = omega_(n+1) * I_(n+1)
zeta_A_n^(n+1)                = I_(n+1)
rank_structure_predicates      = Lie-rank checks beyond A1
irreducibility_predicate       = Schur commutant dimension 1
```

[M] The inverse-radius expression follows from the Fuss-Catalan generating function pattern:

```text
f = 1 + z f^(n+1)
critical f = (n+1)/n
critical z = n^n / (n+1)^(n+1)
inverse radius = (n+1)^(n+1) / n^n
```

[G] This inverse-radius evidence is not the direct Stokes-side computation. A complete numerical harness still requires direct Stokes-side observables for the relevant singularity.

## 6. Relationship to current A2 scaffold

[T] The current A2 harness is the `n = 2` instance:

```text
G_A2 = PSU(3)
auxiliary = SU(3)
V_A2 = C^3
omega = exp(2*pi*i/3)
coxeter_jump = -27/4
```

[G] The A2 harness has eight passing predicates, with six computed and two scaffold values pending direct Stokes-side verification.

## 7. Precedent: Basak / Allcock complex-hyperbolic reflection construction

[T] Basak's complex-hyperbolic reflection construction supplies a large-scale precedent for the same discipline this document uses: start from a rigid arithmetic reflection substrate, extend a diagram through an over-determined system, and require uniqueness rather than accepting free parameters.

[M] In the Basak/Allcock setting, the Eisenstein-integer lattice has signature `(1,13)`, the relevant complex hyperbolic space is `CH^13`, and the incidence graph `Inc(P^2(F_3))` supplies 26 order-three simple reflections. The 26 simple mirrors are characterized as closest mirrors to a distinguished Weyl vector, and Basak's 2007 theorem verifies the corresponding braid/commute relations in the mirror-complement orbifold fundamental group.

[G] This is a precedent citation, not an import of the bimonster program into Lawful Learning. The active C-6' theorem remains the `A_n` faithful-frame structural theorem. The Basak/Allcock construction is cited only as evidence that the no-free-knob, closest-mirror/gate-minimality, and over-determined-extension methodology scales to large arithmetic reflection systems.

[G] The parallel quaternionic construction — Hurwitz integers, `P^2(F_2)`, 14 order-four reflections, and an `M444`-type diagram — is a possible future stress-test lane because it is smaller than the 26-node Eisenstein construction and arithmetically closer to quaternionic tooling used elsewhere in the broader estate. It is not part of this PR.

## 8. V2 26D framing boundary

[G] No V2 26-dimensional Lawful Learning spec is edited by this PR because no matching V2 file was found in this repository during implementation.

[G] Any future V2 document using a 26-dimensional allocation must state one of the following explicitly:

```text
CH13_modeling: true
```

meaning the 26 real dimensions are intentionally modeling `CH^13` / projectivized signature `(1,13)` complex-hyperbolic geometry; or

```text
CH13_modeling: false
```

meaning the 26 dimensions derive from internal spectral/unitary/Poincare-channel requirements and the Basak/Allcock `CH^13` / 26-mirror coincidence is parallel but independent.

[G] Until such a declaration exists, no Lawful Learning artifact may cite the bimonster/`CH^13` construction as an explanation for a `22 + 1 + 3` dimensional split.

## 9. Open work

[G] The direct Stokes-side computation remains open for A2 and for the parametric `A_n` family.

[G] The D and E singularity series are not covered by this theorem. Their Weyl groups and Lie-theoretic structures are not cyclic `A_n` extensions and require separate scoping.

## 10. Non-claims

This document does not claim:

```text
direct Stokes-side coefficients computed for all A_n
A_n runtime harness implemented
D_n or E_n series scoped
proof-assistant formalization completed
bimonster or Allcock conjecture work is active
V2 26D allocation derives from CH13
M444 quaternionic stress-test lane is active
```

## 11. Handoff

The next mechanical deliverable is a parametric `coxeter_an_harness.py` scaffold generated from the targets in Section 5, with A1 handled as an exceptional branch and `n >= 2` handled by the Hermitian-cyclic branch.

The next analytic deliverable remains the direct A2 Stokes-side computation, because it anchors the scaffold value `-27/4` to the canonical singularity-theoretic observable.
