# Pattern — Integration Engine (Stock-Flow / ODE)

!!! abstract "Pattern at a glance"
    **Intent:** evolve a set of **stocks** (accumulations) forward in time by numerically
    integrating **flow rates** that depend, through **feedback loops**, on the current
    state — the conserved accounting backbone of a dynamic model.
    **Also known as:** stock-flow engine, ODE integrator, system-dynamics core.
    **Grounded in:** [Vensim / System Dynamics](../model-families/frameworks/vensim.md);
    the carbon/temperature boxes of [DICE](../model-families/climate-iam/dice.md).

## Problem & forces

Every dynamic model must track quantities that **accumulate** — capital, CO₂, water,
population, debt — and can only change through flows. The Integration Engine makes that
accounting explicit and conserved. The forces:

- **Conservation** — a stock changes *only* by its inflows minus outflows; nothing appears
  or vanishes unaccounted.
- **Feedback & delay** — flows depend on stocks (often nonlinearly, with lags), closing
  reinforcing/balancing loops that generate the dynamics.
- **Continuous time** — behavior is defined by rates; the solver approximates the integral.
- **Numerical fidelity** — step size and method (Euler vs Runge-Kutta) trade speed for
  accuracy/stability.

## Structure

```mermaid
graph TD
    subgraph state
        S[Stocks S_k]
    end
    S --> AUX[Auxiliaries<br/>algebraic + table functions]
    AUX --> F[Flows<br/>inflow_k, outflow_k]
    F --> INT[Integrator<br/>S_k += Δt·(inflow−outflow)]
    INT --> S
    INT --> OUT[Time series]
```

The engine (1) evaluates auxiliaries in dependency order, (2) computes flows, (3) advances
each stock by the integrated net flow, and (4) repeats. The **feedback** is that flows read
the very stocks they update. This is the same three-box carbon cycle / two-box climate
integrator inside [DICE](../model-families/climate-iam/dice.md) — an Integration Engine
embedded under an [Optimization Engine](optimization-engine.md).

## Interface

```
stocks     := S_k with initial S_k(0)
flows      := f_k(S, auxiliaries, params)   # the ODE right-hand side
step(Δt)   := S_k ← S_k + Δt · Σ(inflow − outflow)
integrate(0..T) → trajectories
```

## Exemplars

| Model / module | Stocks | Feedback of note | Method |
|----------------|--------|------------------|--------|
| [Vensim / SD](../model-families/frameworks/vensim.md) | Any (population, capital…) | R/B loops, delays | Euler / RK |
| [DICE](../model-families/climate-iam/dice.md) climate module | Carbon boxes, ocean/atm temp | Radiative forcing → warming | Discrete difference eqns |
| SEIR epidemic core | S, E, I, R compartments | Infection ∝ S·I | ODE / difference |

## Trade-offs & variants

- **Aggregate vs individual** — stocks homogenize the population; where heterogeneity
  matters, use a [Behavior Engine](behavior-engine.md) (see
  [SD vs ABM](../comparative/system-dynamics-vs-abm.md)).
- **Structure is the modeler's** — dramatic dynamics can hinge on assumed loops/table
  functions; make feedback **inspectable and testable** (reference modes, extreme-condition
  tests) — the *Limits to Growth* lesson.
- **Explicit vs implicit / adaptive step** — stiff systems need better integrators;
  fixed-step Euler is cheap but can mislead.
- **Deterministic core + sampled parameters** — pair with a
  [Sensitivity Engine](sensitivity-engine.md) for uncertainty.

!!! quote "Lesson for the integrated simulator"
    The Integration Engine is the simulator's **shared accounting substrate**. Every
    physical and financial quantity the whole system tracks should live here as a
    **conserved stock**, so that whatever sets the *rates* — an
    [optimizer](optimization-engine.md), a [market](market-engine.md), or a swarm of
    [agents](behavior-engine.md) — the stocks integrate them **consistently and without
    leakage**. This is what lets otherwise incompatible paradigms share one world: agents
    and markets produce flows; the Integration Engine accumulates them into the CO₂,
    capital, and population that everyone then reads back. Its discipline requirement is
    that the feedback structure be **transparent and stress-tested**, so a striking result
    can always be traced to the specific loop driving it.

## See also
- [Behavior Engine](behavior-engine.md) · [Optimization Engine](optimization-engine.md) · [Sensitivity Engine](sensitivity-engine.md)
- [System Dynamics vs Agent-Based](../comparative/system-dynamics-vs-abm.md) · [Patterns catalog](index.md)
