# Mixed-Integer Linear Programming (MILP)

!!! success "Method dossier — Silver"
    MILP is LP **with some variables forced to be integers** — the method for decisions that
    are *indivisible* (build a plant or not, run a unit or not). It buys realism at a steep
    computational and interpretive price. Contrast with [LP](lp.md) and see
    [LP vs MILP](../../comparative/lp-vs-milp.md).

> Linear objective and constraints, but with **integrality restrictions** on some variables
> — expressive enough for on/off, build/don't, and lumpy investment decisions, at the cost
> of **NP-hardness** and **loss of shadow prices**.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Mixed-Integer LP (MILP) |
|------|------|
| Optimization vs Simulation | Optimization |
| Top-down vs Bottom-up | N/A (method; enables detailed bottom-up) |
| Equilibrium | N/A |
| Foresight | N/A |
| Deterministic vs Stochastic | Deterministic (stochastic-MILP variants) |
| Time / Space | N/A |
| Solution method | Branch-and-bound / branch-and-cut |

| Field | Value |
|-------|-------|
| Full name | Mixed-Integer Linear Programming |
| Domain | Methods & Algorithms |
| Key ideas | Branch-and-bound (Land & Doig, 1960); cutting planes (Gomory, 1958); branch-and-cut |
| Solvers | Gurobi, CPLEX, HiGHS, SCIP, CBC (open) |
| License / access | Solvers vary; modeling via Pyomo, GAMS, JuMP |

---

## 🎓 Scholar Track

### The canonical form

$$
\min_{\mathbf{x},\mathbf{y}} \; \mathbf{c}^\top \mathbf{x} + \mathbf{d}^\top \mathbf{y}
\quad\text{s.t.}\quad
A\mathbf{x} + B\mathbf{y} \le \mathbf{b}, \;\;
\mathbf{x} \ge \mathbf{0}, \;\;
\mathbf{y} \in \mathbb{Z}^p
$$

The integer variables $\mathbf{y}$ (often **binary**, $\{0,1\}$) encode *discrete* choices:
whether to build capacity, commit a generator, open a facility, choose one technology over
another. This is what LP cannot express — LP would happily build *0.37 of a power plant*.

### Why integrality is expensive: nonconvexity

Adding integer restrictions makes the feasible set **nonconvex** (a lattice of points, not a
polytope). The consequences are severe:

- **NP-hard** — no known polynomial-time algorithm; worst-case cost grows exponentially in
  the number of integer variables.
- **No duals / shadow prices** — the LP duality that hands energy models their marginal
  prices **does not hold** for the integer problem. You can read duals off the final LP
  relaxation, but they are not exact marginal values of the MILP. This is the single most
  important modeling consequence (see [LP vs MILP](../../comparative/lp-vs-milp.md)).

### Solution algorithm: branch-and-bound

MILP is solved by **implicitly enumerating** the integer possibilities:

1. **Relax** — drop integrality, solve the LP (fast, gives a bound).
2. **Branch** — pick a fractional integer variable, split into subproblems ($y \le \lfloor
   v \rfloor$ and $y \ge \lceil v \rceil$).
3. **Bound & prune** — use the LP bound to discard subtrees that cannot beat the incumbent.
4. **Cut** — add valid inequalities (Gomory, cover cuts) to tighten relaxations
   (**branch-and-cut**).

The art is in **pruning aggressively** so the exponential tree stays small in practice.

## 🛠️ Engineer Track

### Complexity & scale

Where an LP of $10^6$ variables solves in seconds, a MILP with a few thousand *binary*
variables can take hours or fail to close the **optimality gap**. Practitioners routinely
accept a solution "within X% of optimal" rather than proving optimality. Tricks: tight
formulations, symmetry breaking, warm starts, and **temporal aggregation** to shrink the
problem.

### Where it shows up

- **Unit commitment** in power systems — generators have minimum up/down times, start-up
  costs, and are either on or off → binary variables → **PyPSA** and detailed dispatch use
  MILP.
- **Lumpy investment** — discrete plant sizes, indivisible infrastructure.
- **Facility location, network design, scheduling** across operations research.

## 🏛️ Architect Track

### Trade-offs & alternatives

- **MILP vs [LP](lp.md)** — the core trade: integer realism vs speed + global-optimality +
  duals. Most energy-system models ([OSeMOSYS](../../model-families/energy/osemosys.md),
  [TIMES](../../model-families/energy/times.md)) stay **LP** deliberately, accepting
  fractional capacity to keep marginal prices and tractability; they reach for MILP only
  where indivisibility is essential.
- **MILP vs heuristics** — for very large discrete problems, metaheuristics (genetic
  algorithms, simulated annealing) trade the optimality guarantee for speed.
- **Relaxation quality matters** — a "tight" MILP formulation can solve orders of magnitude
  faster than a "loose" one describing the same problem.

!!! quote "Lesson for the integrated simulator"
    MILP marks a **hard cost boundary** the simulator must cross *consciously*. Integrality
    is sometimes unavoidable — a lumpy investment or a unit-commitment decision genuinely is
    discrete — but each block of binaries risks turning a seconds-long
    [LP](lp.md) into an intractable search *and forfeits the shadow prices* that make
    optimization outputs policy-legible. The design rule: keep the core in
    [LP](lp.md) wherever a continuous relaxation is honest, **isolate** the discrete
    decisions into the smallest possible MILP sub-block, and expose the **optimality-gap
    tolerance** as an explicit dial so users trade solve-time against precision with eyes
    open — rather than discovering it implicitly when a scenario fails to solve.

## Major publications

- Land, A. H., & Doig, A. G. (1960). "An automatic method of solving discrete programming
  problems." *Econometrica* 28(3).
- Wolsey, L. A. (1998). *Integer Programming*. Wiley.

## See also
- Contrast: [LP](lp.md) · [LP vs MILP](../../comparative/lp-vs-milp.md)
- Patterns: [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) · [Optimization Engine](../../patterns/optimization-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md)
