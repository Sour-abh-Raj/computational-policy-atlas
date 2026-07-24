# Optimal Control

!!! info "Silver method dossier"
    Optimal control is the **continuous-time theory of steering a dynamical system to extremize an
    objective** — and it is, quite literally, the engine of the atlas's flagship. [DICE](../../model-families/climate-iam/dice.md)
    *is* a discretized optimal-control problem: choose emissions-control and savings paths over time to
    maximize discounted welfare, subject to the climate–economy state dynamics. It is the continuous
    sibling of [dynamic programming](dp.md) and the mathematical parent of every intertemporal
    welfare-maximizing IAM.

> The continuous-time theory of steering a dynamical system to extremize an objective, via Pontryagin's
> Maximum Principle or the Hamilton-Jacobi-Bellman equation; DICE is a discretized instance.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Optimal Control |
|------|------|
| Optimization vs Simulation | **Optimization** (continuous control) |
| Top-down vs Bottom-up | N/A (method) |
| Equilibrium | N/A |
| Foresight | **Perfect foresight** (open-loop) / feedback (closed-loop) |
| Deterministic vs Stochastic | Deterministic or stochastic |
| Time / Space | **Continuous time / continuous state** |
| Solution method | **PMP (costate) / HJB / direct collocation** |

| Field | Value |
|-------|-------|
| Full name | Optimal Control |
| Domain | Methods & Algorithms |
| First release / current | 1950s–60s / mature |
| Institution · lead | Pontryagin (Maximum Principle); Bellman (HJB) |
| Language · solver | Pyomo.DAE, CasADi, GEKKO, GAMS, ACADO |
| License / access | Method (open + commercial solvers) |

---

## 🎓 Scholar Track

**History & motivation.** Optimal control crystallized in the **1950s–60s** from two directions: the
Soviet school of **Lev Pontryagin** (the **Maximum Principle**, 1956) and the American school of
**Richard Bellman** (the **HJB** equation, continuous [dynamic programming](dp.md)). Its motivating
problems were engineering — guiding rockets, steering processes — but the same mathematics governs any
system where you **choose a control trajectory over time to optimize an objective subject to state
dynamics**, which is exactly the structure of **growth economics** (Ramsey) and hence of cost-benefit
**climate-economy IAMs**.

**Mathematical formulation.** The canonical continuous-time problem: choose a control path $u(t)$ to

$$\max_{u(\cdot)}\;\; \int_0^T e^{-\rho t}\, L\big(x(t),u(t)\big)\,dt + \Phi\big(x(T)\big)
\quad\text{s.t.}\quad \dot x(t) = f\big(x(t),u(t)\big),\; x(0)=x_0,$$

with **state** $x$ (e.g. capital, carbon stocks), **control** $u$ (e.g. savings rate, emissions-control
rate), and dynamics $f$. Two classical solution routes:

- **Pontryagin's Maximum Principle (PMP)** introduces **costate/adjoint** variables $\lambda(t)$ (shadow
  prices of the state) and a **Hamiltonian** $H = L + \lambda^\top f$; optimality requires
  $u^\*=\arg\max_u H$, the state equation $\dot x = \partial H/\partial\lambda$, and the **costate
  equation** $\dot\lambda = -\partial H/\partial x$ with transversality conditions — a **two-point
  boundary-value problem**. (In climate economics, $\lambda$ on the carbon stock *is* the **social cost
  of carbon**.)
- **Hamilton–Jacobi–Bellman (HJB)** is the continuous-DP PDE for the value function $V(x,t)$:
  $-\partial_t V = \max_u\{L + (\partial_x V)^\top f\}$, giving a **feedback (closed-loop)** law
  $u^\*(x)$.

**Solution algorithms.** In practice large policy models use **direct methods**: **discretize** time and
state (transcribe the continuous problem into a finite **NLP**) and solve with an interior-point/SQP
solver — this is exactly how [DICE](../../model-families/climate-iam/dice.md) is solved (a few decades of
5- or 10-year steps → a modest NLP in GAMS). **Indirect methods** solve the PMP boundary-value problem
directly; **collocation** (Pyomo.DAE, CasADi, GEKKO) is the modern workhorse.

**Strengths / weaknesses.** *Strengths:* a **principled, interpretable** framework — costates deliver
**shadow prices** (the SCC), and the continuous formulation makes structural insight (e.g. optimal
carbon-price growth rates) transparent. *Weaknesses:* needs a **known, differentiable model**; scales
poorly in state dimension for closed-loop HJB (the [DP](dp.md) curse); perfect-foresight open-loop
solutions ignore uncertainty and learning unless extended (stochastic control).

## 🛠️ Engineer Track

**Where it lives in the atlas.** Optimal control is the formal core of the **[Optimization Engine](../../patterns/optimization-engine.md)**
in its *intertemporal* mode and the direct method behind [DICE](../../model-families/climate-iam/dice.md)
and the welfare-maximizing IAMs ([REMIND](../../model-families/climate-iam/remind.md),
[WITCH](../../model-families/climate-iam/witch.md)). Its discretize-to-NLP recipe is why those models are
"just" nonlinear programs despite being control problems underneath.

**Implementation.** **Direct transcription** (single/multiple shooting, orthogonal collocation) →
NLP solved by IPOPT/CONOPT/KNITRO; tools: **Pyomo.DAE, CasADi, GEKKO, GAMS, ACADO**. Complexity is that
of the resulting NLP (grows with time steps × state/control dimension), which is why policy models keep
the state small.

**Data structures.** State/control trajectories on a time grid; costate/adjoint variables (indirect) or
NLP multipliers (direct, which *are* the discretized costates — the SCC falls out as a dual).

## 🏛️ Architect Track

**Reusable patterns.** Optimal control contributes the **shadow-price-of-the-state** idea (costates =
marginal values, e.g. the SCC as the multiplier on the carbon-stock constraint) and the crisp
**open-loop vs closed-loop** distinction (a committed optimal *trajectory* vs a *feedback law* $u(x)$) —
the same fork [DP](dp.md) draws, here in continuous time. The **discretize-then-NLP** pattern is a
reusable bridge from elegant continuous theory to solvable computation.

**Trade-offs & alternatives.** Optimal control (continuous, differentiable dynamics) vs
[LP/MILP](lp.md) (large linear/discrete static or multi-period) vs [DP](dp.md)/[RL](reinforcement-learning.md)
(discrete/stochastic sequential with feedback). Perfect-foresight IAMs solve the **open-loop** control
problem (a trajectory) precisely because closed-loop HJB is intractable at useful state sizes — the
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) axis at the method
level. Where uncertainty/learning matter, **stochastic control** or [RL](reinforcement-learning.md)
takes over.

**Adoption.** Aerospace/robotics/process control (its home), and in policy: **cost-benefit climate IAMs**
(DICE/RICE and descendants), optimal-growth macro, resource economics (Hotelling), and epidemic-control
optimization.

**Research gaps.** Optimal control **under deep uncertainty** (robust/stochastic control) for climate;
scaling closed-loop solutions; differentiable coupling to complex simulators (differentiable
programming).

!!! quote "Lesson for the integrated simulator"
    Optimal control is the reason the integrated simulator can produce **shadow prices**, not just
    trajectories. When a policy problem is posed as "steer this system to extremize an objective," the
    **costate variables are marginal values** — the social cost of carbon is literally the multiplier on
    the carbon-stock dynamics — so the simulator should expose these **duals as first-class outputs**, the
    prices that make a plan decentralizable. It also teaches the **discretize-to-NLP** bridge (elegant
    continuous control becomes a solvable program), and it sharpens the **foresight dial**: open-loop
    optimal control assumes perfect foresight and no learning, so the simulator must offer the closed-loop
    ([DP](dp.md)) and learning ([RL](reinforcement-learning.md)) alternatives where the future is genuinely
    uncertain. DICE's whole authority rests on this method being small enough to state and audit in full —
    a reminder that **interpretability is a feature of keeping the controlled state minimal**.

## Major publications

- Pontryagin, L. S., et al. (1962). *The Mathematical Theory of Optimal Processes.* Wiley.
- Bellman, R. (1957). *Dynamic Programming.* Princeton (HJB / continuous DP).
- Nordhaus, W. (2017). "Revisiting the social cost of carbon." *PNAS* 114(7) (DICE as a discretized
  optimal-control instance). · Betts, J. T. (2010). *Practical Methods for Optimal Control* (direct
  methods).

## See also
- Parent/siblings: [Dynamic Programming](dp.md) (discrete DP) · [Reinforcement Learning](reinforcement-learning.md) (learned control) · [LP](lp.md) / [MILP](milp.md)
- Exhibited by: [DICE](../../model-families/climate-iam/dice.md) · [REMIND](../../model-families/climate-iam/remind.md) · [WITCH](../../model-families/climate-iam/witch.md)
- Axes: [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · Positioning: [Taxonomy](../../foundations/taxonomy.md)
