# Stella / iThink

!!! info "Bronze dossier"
    Stella is the tool that **made system dynamics visual** — the first widely-used environment where
    you *draw* stocks and flows and it writes the differential equations for you. It is the pedagogical
    and policy-facing complement to [Vensim](vensim.md): same stock-flow-feedback paradigm, but with a
    founding emphasis on **accessibility and learning**. If [NetLogo](netlogo.md) is the teaching
    environment for agent-based modeling, Stella is its equivalent for system dynamics.

> A pioneering visual system-dynamics tool that popularized stock-and-flow modeling for education and
> policy, emphasizing accessible causal-loop and simulation interfaces.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Stella |
|------|------|
| Optimization vs Simulation | **Simulation** (system dynamics) |
| Top-down vs Bottom-up | **Aggregate** (stocks/flows) |
| Equilibrium | N/A (dynamic) |
| Foresight | N/A / continuous |
| Deterministic vs Stochastic | Deterministic (stochastic inputs possible) |
| Time / Space | **Continuous** / aggregate (no space) |
| Solution method | **Numerical integration (Euler/RK)** |

| Field | Value |
|-------|-------|
| Full name | Stella / iThink (Structural Thinking Experiential Learning Laboratory) |
| Domain | Frameworks & Environments |
| First release / current | 1985 / ongoing |
| Institution · lead | **isee systems** (Barry Richmond) |
| Language · solver | Proprietary visual modeling + equation engine |
| License / access | Commercial (online viewer/free tiers) |

---

## 🎓 Scholar Track

**History & motivation.** Stella (**S**tructural **T**hinking **E**xperiential **L**earning
**La**boratory) was released in **1985** by **Barry Richmond**'s **isee systems** (originally High
Performance Systems), on the first Macintosh — deliberately exploiting the Mac's graphical interface.
Its motivation was **democratizing system dynamics**: Jay Forrester's paradigm (see [Vensim](vensim.md))
was powerful but locked behind equation-writing (DYNAMO). Richmond's insight was that people reason
better about **pictures of accumulation and feedback** than about ODE systems, so Stella let modelers
**draw** the stock-flow diagram and auto-generate the mathematics — coining "**systems thinking**" as a
teachable skill. (The business-oriented edition is **iThink**.)

**Mathematical formulation.** Stella is a **visual front-end to a system of ordinary differential
equations**, identical in substance to Vensim. The four primitives: **stocks** (accumulations, the
state variables $S_i$), **flows** (rates $\frac{dS_i}{dt}$ into/out of stocks), **converters**
(auxiliary variables and constants), and **connectors** (causal links). Drawing
$\text{stock} \xrightarrow{\text{flow}} \text{stock}$ defines

$$S_i(t) = S_i(0) + \int_0^t \big(\text{inflows}_i - \text{outflows}_i\big)\,d\tau,$$

which Stella integrates numerically (**Euler** or **Runge-Kutta**) over the simulation horizon.
Feedback loops (a stock influencing its own flows through converters) produce the nonlinear dynamics —
exponential growth, goal-seeking, S-curves, overshoot-and-collapse — that are the paradigm's signature.
There is **no space and no optimization**; the model *simulates* the consequences of the causal
structure you drew.

**Solution algorithm.** Fixed-step **numerical integration** of the ODE system each time step, with
live plotting; interactive "**flight simulator**" interfaces let users change parameters and watch
trajectories respond — the feature that made it a policy- and classroom-facing tool.

**Calibration & validation.** Parameters set from data or judgment; validation follows the
system-dynamics tradition (structural/behavioral validity, sensitivity testing) rather than statistical
fit — the same stance as [Vensim](vensim.md); Stella provides sensitivity and (in Pro) optimization
add-ons.

**Strengths / weaknesses / criticisms.** *Strengths:* **unmatched accessibility** and visual clarity;
excellent for **teaching, participation, and communication**; instant interactive simulation.
*Criticisms:* **commercial/closed**; aggregate-only (no agents, no space); less suited to large research
models or rigorous calibration than [Vensim](vensim.md); the ease can invite under-validated models.

## 🛠️ Engineer Track

**Architecture & engines.** A pure **[Integration Engine](../../patterns/integration-engine.md)**
(stock-flow ODE integrator) fronted by a **[Visualization Engine](../../patterns/visualization-engine.md)**
that is also the *authoring* surface — the diagram **is** the model. Add-ons provide a
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)** and optimization. No spatial or behavior
engine — by design.

**Data & complexity.** Trivial computationally (ODE integration of tens–hundreds of variables);
optimized for **interactivity and clarity**, not scale. **Stella Online** runs models in a browser.

**Openness / extensibility.** **Commercial** (isee systems), though widely licensed in education and
with online sharing/viewer tiers. Interchange via **XMILE** — an open XML standard for system-dynamics
models (co-developed by isee) that lets Stella/Vensim/others exchange models.

## 🏛️ Architect Track

**Reusable patterns.** Stella's contribution is **authoring-as-diagram**: make the **visual causal
structure the primary artifact**, and *generate* the equations from it — lowering the barrier to
building dynamic models and making them communicable. Also reusable: **interactive "flight-simulator"
interfaces** (let stakeholders drive the model live) and the **XMILE** interchange standard for model
portability.

**Trade-offs & alternatives.** Stella vs [Vensim](vensim.md): the two canonical system-dynamics
environments — Vensim leans **research/rigor** (calibration, optimization, large models), Stella leans
**pedagogy/communication and visual polish**; both integrate the same stock-flow ODEs and interchange
via XMILE. Against the ABM environments ([NetLogo](netlogo.md), [Mesa](mesa.md)) it is the
**aggregate/continuous** paradigm rather than individual/discrete — the
[System Dynamics vs Agent-Based](../../comparative/system-dynamics-vs-abm.md) and
[Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) contrasts. [AnyLogic](anylogic.md)
subsumes both by offering SD, ABM, and DES together.

**Adoption.** A staple of **systems-thinking education** (schools, universities, executive programs),
public-health and policy participatory modeling, and business strategy (iThink); the tool behind many
classic teaching models.

**Ecosystem.** isee systems (Stella Architect/Professional, Stella Online); XMILE standard; peers
Vensim, Powersim, AnyLogic; the System Dynamics Society community.

**Research gaps.** Openness; bridging accessible authoring with rigorous validation; coupling aggregate
SD to spatial/agent detail (the multi-method direction AnyLogic took).

!!! quote "Lesson for the integrated simulator"
    Stella's lesson is that **the modeling interface is part of the model's power**. By making the
    **stock-flow diagram the authoring surface** and generating the equations from it, Stella turned a
    mathematically-demanding paradigm into something a policymaker or student could build and *drive
    interactively* — expanding who can participate in modeling. For the integrated simulator this argues
    for **visual, diagrammatic authoring** of causal structure alongside code, **live interactive
    interfaces** that let stakeholders explore scenarios in real time (the En-ROADS lineage), and
    **open interchange standards** (like XMILE) so models move between tools. It also reinforces the
    atlas's paradigm map: system dynamics is the **aggregate-continuous** engine that the simulator
    should host next to the individual-discrete (ABM) and equilibrium engines — and, as
    [AnyLogic](anylogic.md) shows, ideally in one place.

## Major publications

- Richmond, B. (1985). *Stella: Software for Systems Thinking.* High Performance Systems / isee systems.
- Richmond, B. (1993). "Systems thinking: critical thinking skills for the 1990s and beyond." *System
  Dynamics Review* 9(2).
- Costanza, R., Voinov, A. (2001). "Modeling ecological and economic systems with STELLA." *Ecological
  Modelling* 143 (application review).

## See also
- Peer/analogy: [Vensim](vensim.md) (SD research environment) · [NetLogo](netlogo.md) (ABM pedagogy) · Multi-method: [AnyLogic](anylogic.md)
- Paradigm contrasts: [System Dynamics vs ABM](../../comparative/system-dynamics-vs-abm.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md)
- Patterns: [Integration Engine](../../patterns/integration-engine.md) · [Visualization Engine](../../patterns/visualization-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
