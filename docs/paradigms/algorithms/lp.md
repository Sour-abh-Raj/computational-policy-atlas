# Linear Programming (LP)

!!! success "Method dossier — Silver"
    LP is the **computational backbone of bottom-up energy-system modeling** — the engine
    under [OSeMOSYS](../../model-families/energy/osemosys.md),
    [TIMES](../../model-families/energy/times.md), and PyPSA. This page documents the
    *method*; contrast it with [MILP](milp.md) and see
    [LP vs MILP](../../comparative/lp-vs-milp.md).

> Optimization of a **linear objective** over **linear constraints** — convex, globally
> optimal, scalable to millions of variables, and equipped with **dual prices** that carry
> direct policy meaning.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Linear Programming (LP) |
|------|------|
| Optimization vs Simulation | Optimization |
| Top-down vs Bottom-up | N/A (method; enables bottom-up models) |
| Equilibrium | N/A |
| Foresight | N/A (usually perfect within horizon) |
| Deterministic vs Stochastic | Deterministic (stochastic-LP variants) |
| Time / Space | N/A |
| Solution method | Simplex / interior-point |

| Field | Value |
|-------|-------|
| Full name | Linear Programming |
| Domain | Methods & Algorithms |
| First formulated | Dantzig (simplex, 1947); Kantorovich (1939); interior-point (Karmarkar 1984) |
| Solvers | Gurobi, CPLEX, HiGHS (open), GLPK (open), COIN-OR CLP |
| License / access | Solvers vary (open + commercial); modeling via Pyomo, GAMS, JuMP |

---

## 🎓 Scholar Track

### The canonical form

An LP optimizes a linear objective subject to linear equalities/inequalities and (usually)
non-negativity:

$$
\min_{\mathbf{x}} \; \mathbf{c}^\top \mathbf{x}
\quad\text{s.t.}\quad
A\mathbf{x} \le \mathbf{b}, \;\; \mathbf{x} \ge \mathbf{0}
$$

The feasible region is a convex **polytope**; because the objective is linear, an optimum
(if one exists and is bounded) is always attained at a **vertex** of that polytope.

### Why LP is special: convexity + duality

Two properties make LP the workhorse of policy optimization:

- **Convexity → global optimality.** There are no local optima to trap a solver; *the*
  optimum is *the* optimum. This is exactly why energy models can be trusted to report the
  true least-cost system.
- **Duality → shadow prices.** Every LP has a **dual**; the optimal dual variable on a
  constraint is its **shadow price** — the marginal change in the objective per unit
  relaxation. In an energy model, the shadow price on the energy-balance constraint *is the
  marginal cost of energy*, and the dual on an emissions cap *is the carbon price*. **Policy
  numbers fall out of the math for free** — see the
  [Optimization Engine](../../patterns/optimization-engine.md) and
  [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) patterns.

### Solution algorithms

- **Simplex** (Dantzig, 1947) — walks vertex-to-vertex along the polytope edges, improving
  the objective each step. Exponential worst case, but superb in practice; warm-starts well.
- **Interior-point** (Karmarkar, 1984) — traverses the *interior* of the polytope toward the
  optimum; **polynomial-time**, excellent for very large sparse problems.
Modern solvers (Gurobi, HiGHS) run both and pick per problem.

## 🛠️ Engineer Track

### Complexity & scale

LP is **polynomial-time** (interior-point); real solvers handle $10^6$–$10^7$ variables on
a workstation, which is what lets an [OSeMOSYS](../../model-families/energy/osemosys.md) or
[TIMES](../../model-families/energy/times.md) resolve hundreds of technologies × regions ×
time-slices × years. Performance hinges on **sparsity** (few nonzeros per row) and good
**presolve**.

### The model-generator pattern

Energy tools rarely hand-write the LP: a **model generator** (OSeMOSYS's algebra, TIMES's
GAMS core) *builds* the constraint matrix from a data table of technologies and demands, so
the analyst edits **data, not equations** — the separation of data from solver highlighted
in the [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) pattern.

## 🏛️ Architect Track

### Exhibited by

| Model | LP role | Dual of interest |
|-------|---------|------------------|
| [OSeMOSYS](../../model-families/energy/osemosys.md) | Least-cost capacity + dispatch | Marginal energy / cap price |
| [TIMES](../../model-families/energy/times.md) | Partial-equilibrium least cost | Marginal abatement cost |
| PyPSA | Power dispatch + expansion | Nodal (locational) prices |

### Trade-offs & alternatives

- **LP vs [MILP](milp.md)** — LP's continuous variables give speed, global optimality, and
  clean duals; the moment you need *indivisibility* (build-or-not, on-or-off) you move to
  MILP and **lose the duals** (full treatment: [LP vs MILP](../../comparative/lp-vs-milp.md)).
- **LP vs NLP** — nonlinearities (e.g. [DICE](../../model-families/climate-iam/dice.md)'s
  damage function) need nonlinear programming, which sacrifices guaranteed global optimality.
- **Linearity as an assumption** — economies of scale, thresholds, and nonconvex physics
  must be *approximated* (piecewise-linearized) to stay in the LP world.

!!! quote "Lesson for the integrated simulator"
    LP is the **default gear** for any subsystem that can be honestly posed as linear
    least-cost: it scales, it is globally optimal, and — most valuable — its **duals hand
    back the policy prices** (energy cost, carbon price, congestion charge) as a by-product
    of solving. A capable simulator should *reach for LP first*, keep the constraint matrix
    **generated from data** rather than hand-coded, and treat the jump to
    [MILP](milp.md)/NLP as a deliberate, costed decision made only when indivisibility or
    nonlinearity genuinely changes the answer — because that jump forfeits the very duals
    that make LP so policy-useful.

## Major publications

- Dantzig, G. B. (1963). *Linear Programming and Extensions*. Princeton University Press.
- Karmarkar, N. (1984). "A new polynomial-time algorithm for linear programming."
  *Combinatorica* 4(4).

## See also
- Contrast: [MILP](milp.md) · [LP vs MILP](../../comparative/lp-vs-milp.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md)
