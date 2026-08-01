# The Semantic-Address Algebra as the Discrete Skeleton of the Constrained-Spectral Field Theory

Status: DOCTRINE v0.1 · Public · Clean-room (no third-party lexicon or mark)
Grounds: the compositional semantic-address algebra (the coordinate kernel, `AgentCoordinateVector`,
`BoundaryTransition` actants, the abstraction-level gate, `lift ⊣ ground`, the 23×6 intent grid) in
the SocioProphet Research Programme manuscript *Constrained Spectral Learning with Prime–Even
Structured Gates* (working draft, 2026).

---

## 0 · Thesis

> **The manuscript is a continuous, field-theoretic *measurement* framework for a digital system;
> the semantic-address algebra is its discrete, typed *skeleton*. They are one object at two
> resolutions.** The manuscript works in ℝ²⁶ with a spectral operator, a convex constraint cone,
> learned regime gates, an arithmetic prior, and a hyperbolic embedding. The algebra is the
> combinatorial shadow of exactly that object: primitives and products for the spectrum, `pullback`
> for the constraint cone, `meet` for the supermodular interaction, the 23×6 grid for the gates, the
> `layer`/`lift⊣ground` grading for the hyperbolic hierarchy, and the `SemanticAddress` warrant for
> the forensic ledger.

This is not a metaphor. Each correspondence below carries an equation or proposition number from the
manuscript, and the two tightest are *the same mathematics in two costumes*.

## 1 · The correspondence, with references

| Manuscript (continuous / spectral) | Algebra (discrete / symbolic) | Grade |
|---|---|---|
| Feasible cone `K={θ:Cθ≥d}` (eq 32–33); gated cone `diag(w_R)Cθ ≥ diag(w_R)d` (eq 34–35) | `pullback` (limit/restrict) + the derived 23×6 cells | tight |
| **Edgeworth supermodularity** `H_ij θ ≥ 0` (eq 21; Topkis 1998, Milgrom–Roberts 1990) | **`meet`** — the lattice `∧` in `Truth = Law × Evidence` | **tight (identical lattice)** |
| Per-cell clipping projection `θ ↦ θ + max(0,−aᵀθ)·a/‖a‖²` (eq 57) | `pullback` onto a single constraint half-space | tight |
| Prime–even regulariser `R_{p/e}` (eq 45): soft `ℓ₁` projection `Π_P, Π_E` toward index subspaces | derived-not-authored + `lift ⊣ ground` (pull toward structure, yield to data) | tight |
| Even-prime anchor `P∩E∩{1..22}={2}` (eq 42) — the single cross-family bridge | the second-order meta row; the coreflection fixed point | structural |
| Poincaré ball `𝔹³×ℝ²²`, K=−1; nested index hierarchy (§11.1); **Prop 11.1** gated cone geodesically convex | `layer` grading + `bind_tiered` + `lift ⊣ ground` (hyperbolic = the geometry of hierarchy) | strong |
| Three-phase gate dynamics; entropy-driven **bimodal saturation** `w→{0,1}` (§8.2–8.3) | `bind_tiered` admit / **BOTTOM**; the entropy term = decisiveness | strong |
| Forensic provenance ledger; 10⁻¹² reproducibility (§10) | `SemanticAddress` warrant + provenance register + sealed receipts | tight |
| Block-coordinate descent (Alg 1; Thm 6.1): project `θ` ∥ descend `Θ` | the two-field dynamics (form ∥ action) | tight |
| `f = Σ gᵢ + Σ g_ij`, ANOVA order ≤2 (eq 7) | primitives + ternary products (interaction locality) | good |

### 1.1 The two that are *identical*, not analogous

**Supermodularity is the meet.** The manuscript derives Edgeworth complementarity as the standard
lattice supermodularity of Topkis and Milgrom–Roberts: on a 2×2 cell, `θ^{t+1,u+1} − θ^{t+1,u} −
θ^{t,u+1} + θ^{t,u} ≥ 0`, which is exactly `g(a∨b) + g(a∧b) ≥ g(a) + g(b)` with `∨=max`, `∧=min`.
That `∧` is the operation `meet` implements. The manuscript's headline constraint family and the
algebra's reconciliation operator live on one lattice. (Proven in code: `tools/spectral_grounding.py`,
where the cross-difference and the lattice supermodularity condition are shown equal, both ways.)

**The gate is the derived grid.** "The model never discovers *which* constraints to use — those are
stated up front — but it learns *where* each one binds" (§4) is the 23×6's derived-not-authored
posture stated in spectral language. A gate value `w_R` per (constraint, regime) *is* a grid cell:
VALID with evidence when `w_R≈1`, EMPTY with a named reason when `w_R≈0`. Entropy-driven bimodality
(§8.3) is the discrete admit/abstain of `bind_tiered` — a gate saturating to 0 is `BOTTOM`.

## 2 · Form and action; fermions and bosons

The manuscript's block structure carries the analogy the algebra encodes in its two operations:

- **Fermionic / form / matter** — the **spectral block** `λ₁≥…≥λ₂₂`. The ordering is Pauli-like
  exclusion, and the manuscript notes prime modes are *non-degenerate, single-multiplicity* — literal
  exclusion. In the algebra: **non-commutative `mul`** and the canonical form (no two expressions
  denote one set).
- **Bosonic / action / force** — the **unitary scalar `υ`** (the gauge rotation) and the **gates**
  (mediators coupling constraints to regimes). In the algebra: **commutative `add`** (superposition)
  and the operators `pushout`/`pullback`/`meet`.
- **The dynamics** — block-coordinate descent (project `θ` [form] ∥ descend `Θ` [action], Alg 1) is
  the two-field evolution; Theorem 6.1 is its convergence.

The analogy is structural, not a derivation — the manuscript is explicit that its arithmetic prior is
"a hypothesis, not a law," which is the algebra's exact posture (inductive bias, never authored fact).

## 3 · The number-theoretic grounding (why this matters for the estate)

The prime–even structure gives a **public, citable grounding for the 22-coordinate spine**: 22 = 2×11,
Pascal-encoded (row sums → 2ⁿ, row digits → 11ⁿ); the partition into prime `{2,3,5,7,11,13,17,19}`,
even `{2,4,…,22}`, their intersection `{2}` (the even-prime anchor), and neither. This lets the whole
framework be justified in the open — on Pascal's triangle, Topkis supermodularity, hyperbolic
embedding (Nickel–Kiela, Ganea, Sala), and forensic provenance — all citable, none esoteric, none
third-party-encumbered. The rigorous grounding is also the publishable one.

## 4 · What the geometry licenses, honestly

**Prop 11.1** proves the gated constraint cone is geodesically convex under the Poincaré/Klein
embedding: half-spaces stay convex along hyperbolic geodesics. This is the rigorous warrant for the
`layer` grading and `lift ⊣ ground`: eigenvalues span orders of magnitude → the natural metric is
logarithmic/hyperbolic → the discrete `layer` index is the combinatorial radial coordinate, and the
nested index hierarchy (§11.1) is what `lift`/`ground` traverse. The manuscript is disciplined (§11.5)
that the hyperbolic lens is a *structural description*, not a practical replacement for the Euclidean
algorithm — so the algebra takes the geometry as *grounding for the grading*, not as a runtime
requirement. The Riemannian and Euclidean formulations share stationary points (§11.4).

## 5 · What this doctrine licenses

1. The **kernel** (algebra + contracts) is the reference implementation of this field theory's
   discrete skeleton; it belongs in a versioned Apache-2.0 sovereign library (ProCybernetica),
   vendored by the AI/intelligence stacks through the freshness plane.
2. **superconscious** carries this doctrine and the lifecycle; it does not host the code (per its
   authority-boundary posture: coordinate authorities, do not replace them).
3. The tightest claim — supermodularity = meet — is proven with a teeth-both-ways test, not asserted.

## 6 · Open

- The fermion/boson mapping is a genuine structural analogy, not a derivation.
- Poincaré↔layer is strong via Prop 11.1 but the exact functor from `layer` index to hyperbolic
  radius is not yet pinned by a test.
- The manuscript's empirical section (§12) is a protocol, not results; the algebra's gates and grid
  are the discrete instrument that could report against it.

*Source manuscript: SocioProphet Research Programme, "Constrained Spectral Learning with Prime–Even
Structured Gates," working draft. Code: the semantic-coordinate-algebra kernel (prophet-platform →
ProCybernetica).*
