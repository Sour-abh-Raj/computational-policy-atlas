# Multi-Objective Optimization

!!! info "Silver method dossier"
    Multi-objective optimization confronts the fact that **real policy has competing goals** — cost vs
    emissions vs equity vs reliability — that cannot be collapsed into one number without a value
    judgment. Instead of a single optimum it produces a **Pareto frontier** of non-dominated trade-offs,
    turning "what is *the* best policy?" into "what are the *efficient* trade-offs, and where on them do
    we choose to sit?" It is the method that makes value pluralism explicit rather than hiding it inside a
    weighting.

> Optimization with several conflicting objectives, producing a Pareto frontier of non-dominated
> trade-offs rather than a single optimum — essential where policy has competing goals (cost vs equity vs
> emissions).

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Multi-Objective Optimization |
|------|------|
| Optimization vs Simulation | **Optimization** (Pareto) |
| Top-down vs Bottom-up | N/A (method) |
| Equilibrium | N/A |
| Foresight | Method-dependent |
| Deterministic vs Stochastic | Deterministic or stochastic |
| Time / Space | N/A |
| Solution method | **Weighting / ε-constraint / evolutionary (NSGA-II)** |

| Field | Value |
|-------|-------|
| Full name | Multi-Objective Optimization (MOO / vector optimization) |
| Domain | Methods & Algorithms |
| First release / current | Pareto (1900s) / NSGA-II (2002), ongoing |
| Institution · lead | Vilfredo Pareto; Kalyanmoy Deb (NSGA-II) |
| Language · solver | pymoo, Platypus, jMetal; weighting / ε-constraint via any LP/NLP solver |
| License / access | Open libraries |

---

## 🎓 Scholar Track

**History & motivation.** The core concept — **Pareto optimality** — comes from **Vilfredo Pareto**
(c. 1900): an allocation is efficient if no objective can improve without another worsening. The modern
**algorithmic** era arrived with **evolutionary** methods, above all **Deb's NSGA-II (2002)**, which made
finding whole frontiers practical. The motivation for policy modeling is fundamental: a single objective
function **embeds a value judgment** (the weights). Multi-objective methods **externalize** that judgment
— compute the efficient trade-offs first, decide the weighting second (or never, leaving it to
deliberation).

**Mathematical formulation.** Minimize a **vector** of objectives
$\mathbf{F}(x) = \big(f_1(x),\dots,f_k(x)\big)$ over feasible $x\in\mathcal{X}$. Solution $x^\*$ is
**Pareto-optimal** if no feasible $x$ **dominates** it — i.e. there is no $x$ with $f_i(x)\le f_i(x^\*)$
for all $i$ and strict inequality for some $i$. The set of all such points is the **Pareto set**; its
image in objective space is the **Pareto frontier**. Three classical solution strategies:

- **Weighted sum** — scalarize: $\min \sum_i w_i f_i(x)$, sweep weights $w$. Simple, but **misses
  non-convex** frontier regions and the weights are the very value judgment one wanted to avoid.
- **ε-constraint** — optimize one objective while bounding the others ($\min f_1$ s.t. $f_j\le\varepsilon_j$),
  sweeping $\varepsilon$. Recovers **non-convex** frontiers; widely used in energy models.
- **Evolutionary multi-objective (EMO)** — population methods (**NSGA-II/III**, SPEA2, MOEA/D) that evolve
  a *set* of solutions toward the frontier in one run, using **non-dominated sorting** + **crowding
  distance** to spread coverage. Handle non-convex, discrete, black-box objectives.

**Choosing a point.** The frontier is where analysis stops and **values begin** — a decision-maker picks
via preferences, or methods like **compromise programming** (closest to an ideal point) formalize it.

**Strengths / weaknesses.** *Strengths:* makes **trade-offs explicit and value judgments transparent**;
supports deliberation; EMO handles messy (non-convex/black-box) problems. *Weaknesses:* frontiers grow
**exponentially costly** in many objectives (>3–4, "many-objective" problems); evolutionary methods are
compute-heavy and lack optimality guarantees; visualizing/high-dimensional frontiers is hard.

## 🛠️ Engineer Track

**Where it lives in the atlas.** Multi-objective methods are how the atlas's optimizing models handle
**more than cost**: energy-system models ([OSeMOSYS](../../model-families/energy/osemosys.md)/
[TIMES](../../model-families/energy/times.md), [PyPSA](../../model-families/energy/pypsa.md)) sweep
**cost vs emissions vs reliability** via ε-constraint or weighting; land and water models trade yield vs
environment. It is a natural extension of the **[Optimization Engine](../../patterns/optimization-engine.md)**
and dovetails with the **[Sensitivity Engine](../../patterns/sensitivity-engine.md)** (a frontier is a
structured scenario sweep).

**Implementation.** ε-constraint/weighting wrap any LP/NLP solver (re-solve across a grid of bounds/weights,
trivially parallel); evolutionary methods via **pymoo, Platypus, jMetal** (NSGA-II/III, MOEA/D). Cost =
(frontier resolution) × (single-solve cost) for scalarization, or (population × generations) for EMO.

**Data structures.** A **set** of non-dominated solutions (the archive/frontier), each a decision vector +
objective vector; non-dominated sorting ranks; crowding metrics maintain diversity.

## 🏛️ Architect Track

**Reusable patterns.** The headline pattern is **compute the frontier, defer the weighting** — separate
the *efficient trade-offs* (analysis) from the *choice among them* (values/politics). Also reusable:
**ε-constraint** as a clean way to turn a multi-objective problem into a family of single-objective solves,
and **non-dominated sorting** as a general way to rank a population by multiple criteria.

**Trade-offs & alternatives.** Multi-objective vs single-objective: a weighted single objective is a
*point* on the frontier for *fixed* weights — multi-objective **refuses to pre-commit** to those weights.
Against pure [sensitivity analysis](../../patterns/sensitivity-engine.md): both explore, but MOO
**optimizes** along the trade-off surface rather than sampling parameters. It composes with any solver —
[LP](lp.md), [MILP](milp.md), [optimal control](optimal-control.md), simulation-optimization — and with
[RL](reinforcement-learning.md) (multi-objective RL). It is the algorithmic embodiment of the atlas thesis
that **contested value weightings should be exposed, not hard-coded**.

**Adoption.** Ubiquitous in **energy-system planning** (cost–emissions–security frontiers), water and land
management (yield vs environment), engineering design, and increasingly **equity-aware** policy analysis
(efficiency vs distribution).

**Research gaps.** **Many-objective** (>4) scalability and visualization; incorporating **decision-maker
preferences** interactively; multi-objective under **deep uncertainty** (robust Pareto frontiers);
credible equity metrics as objectives.

!!! quote "Lesson for the integrated simulator"
    Multi-objective optimization is the method that operationalizes the atlas's most-repeated principle:
    **don't hard-code contested values — expose them**. A single welfare function silently fixes the
    weights on cost, emissions, equity, and reliability; the multi-objective stance instead computes the
    **Pareto frontier of efficient trade-offs** and hands the *choice among them* to deliberation. The
    integrated simulator should therefore make **multi-objective a native mode**: let any optimization
    declare several objectives and return a **frontier**, not a point; support **ε-constraint and
    evolutionary** solvers so non-convex and black-box trade-offs are reachable; and treat the frontier as
    a **first-class artifact to visualize and interrogate**. Where different modeling philosophies disagree
    about *what to value*, this is how the simulator honors the disagreement — by showing the trade-off and
    letting values, not the model, pick the point.

## Major publications

- Deb, K., Pratap, A., Agarwal, S., Meyarivan, T. (2002). "A fast and elitist multiobjective genetic
  algorithm: NSGA-II." *IEEE Transactions on Evolutionary Computation* 6(2).
- Miettinen, K. (1999). *Nonlinear Multiobjective Optimization.* Kluwer.
- Blank, J., Deb, K. (2020). "pymoo: Multi-Objective Optimization in Python." *IEEE Access* 8.

## See also
- Composes with: [LP](lp.md) · [MILP](milp.md) · [Optimal Control](optimal-control.md) · [Reinforcement Learning](reinforcement-learning.md)
- Applied in: [OSeMOSYS](../../model-families/energy/osemosys.md) · [TIMES](../../model-families/energy/times.md) · [PyPSA](../../model-families/energy/pypsa.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md) · [Visualization Engine](../../patterns/visualization-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
