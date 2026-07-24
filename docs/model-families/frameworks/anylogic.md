# AnyLogic

!!! info "Bronze dossier"
    AnyLogic is the **multi-method** simulation platform — the one environment that puts **system
    dynamics, agent-based, and discrete-event** modeling *together*, so a single model can mix
    aggregate feedback, individual agents, and process/queue logic. It is the practical embodiment of a
    thesis the whole atlas circles: that **paradigms are complementary tools to be combined**, not
    rival worldviews to choose between. Widely used in **logistics, supply chain, health, and business
    policy**.

> A commercial multi-method simulation platform uniquely combining system dynamics, agent-based and
> discrete-event modeling in one environment — often used for logistics, health and policy.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | AnyLogic |
|------|------|
| Optimization vs Simulation | **Simulation** (multi-method: SD + ABM + DES) |
| Top-down vs Bottom-up | **Any** (mixable in one model) |
| Equilibrium | N/A (model-defined) |
| Foresight | Model-defined |
| Deterministic vs Stochastic | Model-defined (usually stochastic DES/ABM) |
| Time / Space | Model-defined (continuous ODE + discrete events + GIS/space) |
| Solution method | **Hybrid engine** (ODE integrator + event calendar + agent stepping) |

| Field | Value |
|-------|-------|
| Full name | AnyLogic |
| Domain | Frameworks & Environments |
| First release / current | 2000 / ongoing |
| Institution · lead | The AnyLogic Company (St. Petersburg origins; Andrei Borshchev) |
| Language · solver | Java-based (visual editor + Java code) |
| License / access | Commercial (free Personal Learning Edition) |

---

## 🎓 Scholar Track

**History & motivation.** AnyLogic was released in **2000** by **XJ Technologies** (now The AnyLogic
Company), founded by **Andrei Borshchev** out of St. Petersburg. Its founding thesis, argued in
Borshchev & Filippov's influential 2004 paper, is that the three great simulation methods —
**System Dynamics** (aggregate, continuous), **Agent-Based** (individual, emergent), and
**Discrete-Event** (process/queue, entities flowing through resources) — are **not competitors but
complementary abstraction levels**, and real problems often need **more than one at once**. AnyLogic
was built to make that mixing routine in a single tool.

**Mathematical formulation.** AnyLogic has **no fixed domain math**; it provides **three interoperating
formal engines** and lets them share state and time:

- **System Dynamics** — **stock-flow ODEs** integrated numerically (the [Stella](stella.md)/[Vensim](vensim.md)
  paradigm): $\dot S_i = \text{inflows}-\text{outflows}$.
- **Discrete-Event** — entities move through a **process flowchart** (source → queue → delay/resource →
  sink), advanced by a **future-event calendar**; the mathematics is queueing theory / event scheduling.
- **Agent-Based** — agents with **statecharts** (UML-style finite-state machines) and behaviors, stepped
  in time and/or driven by events, optionally over **GIS space** or networks.

The distinctive capability is **coupling**: e.g. a system-dynamics market model sets parameters for a
population of decision-making **agents**, whose choices feed a **discrete-event** logistics network —
all in one synchronized clock. AnyLogic runs a **hybrid simulation engine** that interleaves ODE
integration, event processing, and agent updates.

**Solution algorithm.** A unified engine advances **continuous** state (ODE integrator) between
**discrete events** (event calendar), while **agents** execute statechart transitions on events/ticks;
the three are synchronized on one simulated timeline. Built-in **experiments** provide parameter
variation, **optimization** (via OptQuest), Monte-Carlo, sensitivity, and calibration.

**Calibration & validation.** Ships **OptQuest-based optimization/calibration** and experiment
framneworks; validation is model-specific. Strong industrial validation culture (models tied to
operational KPIs).

**Strengths / weaknesses / criticisms.** *Strengths:* **genuine multi-method** in one environment;
professional tooling (GIS, 3D animation, optimization, cloud); strong in **industry** (supply chain,
manufacturing, healthcare). *Criticisms:* **commercial/closed** and expensive; Java-based extension has
a learning curve; heavyweight for small studies; less used in open academic reproducibility workflows
than [Mesa](mesa.md)/[NetLogo](netlogo.md).

## 🛠️ Engineer Track

**Architecture & engines.** Literally a **composition of the atlas's engines** in one product: an
**[Integration Engine](../../patterns/integration-engine.md)** (SD/ODE), a discrete-event process engine,
and a **[Behavior Engine](../../patterns/behavior-engine.md)** (agents/statecharts), over an optional
GIS **[Spatial Engine](../../patterns/spatial-engine.md)**, with a
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)**/optimization (OptQuest) and rich
**[Visualization Engine](../../patterns/visualization-engine.md)** (2D/3D). A **[Data Pipeline](../../patterns/data-pipeline.md)**
connects to databases/Excel/GIS. Java under the hood; visual editor on top.

**Data & complexity.** Scales to large industrial models; **AnyLogic Cloud** runs experiments/
parameter sweeps at scale. Complexity depends on method mix; the hybrid engine manages
continuous/discrete synchronization.

**Openness / extensibility.** **Commercial** (free **Personal Learning Edition** for education);
extensible via **Java**, custom libraries, and a marketplace; exchanges data with standard enterprise
systems. Not open source — the main contrast with Mesa/Repast/NetLogo/GAMA.

## 🏛️ Architect Track

**Reusable patterns.** AnyLogic's central lesson is **multi-paradigm composition**: a **single
synchronized clock and shared state** under which SD, ABM, and DES coexist and exchange information —
the concrete proof that the atlas's separate "engines" can live in one runtime. Also reusable:
**statecharts** as a clean agent-behavior formalism, and **process flowcharts** (source/queue/resource/
sink) as a reusable DES vocabulary.

**Trade-offs & alternatives.** AnyLogic **unifies** what the rest of the frameworks family splits:
[Vensim](vensim.md)/[Stella](stella.md) (SD), [Mesa](mesa.md)/[Repast](repast.md)/[NetLogo](netlogo.md)/
[GAMA](gama.md) (ABM), and dedicated DES tools (Arena, Simio, FlexSim). Its trade-off is
**openness/cost** vs **integration/professional tooling**. It is the tool that most directly answers the
[System Dynamics vs Agent-Based](../../comparative/system-dynamics-vs-abm.md) debate with "**why not
both, coupled?**" — and adds discrete-event as a third register.

**Adoption.** Heavy **industry** use — supply-chain/logistics, manufacturing, transportation,
healthcare operations, defense, and business policy; taught via the free PLE; a market leader in
commercial multi-method simulation.

**Ecosystem.** The AnyLogic Company (AnyLogic, AnyLogic Cloud, libraries: Process Modeling, Pedestrian,
Rail, Fluid, Material Handling); OptQuest; peers Arena/Simio/FlexSim (DES), Vensim/Stella (SD),
Mesa/Repast/NetLogo (ABM).

**Research gaps.** Open/reproducible workflows; standardized cross-method model description; tighter
coupling to equilibrium/optimization (economic) engines; provenance for mixed-paradigm models.

!!! quote "Lesson for the integrated simulator"
    AnyLogic is the **closest existing thing to the atlas's own goal** — a single environment where
    **system dynamics, agent-based, and discrete-event** models coexist under one clock and share state.
    It is the existence proof that the pattern catalog's engines can be **composed in one runtime**, and
    it names the mechanism: a **hybrid engine** that interleaves ODE integration, an event calendar, and
    agent stepping on a common timeline, with data flowing between the layers. For the integrated policy
    simulator this is the architectural template — **multi-paradigm composition with shared state and a
    unified scheduler** — extended with the pieces AnyLogic leaves out: **equilibrium/optimization**
    engines (CGE, LP) and an **open, reproducible** substrate. Where the atlas says "route each question
    to the paradigm where it's valid, and where they overlap run both," AnyLogic already lets you *wire
    them together*; the simulator's job is to do that openly, at world scale, across the economic and
    physical engines too.

## Major publications

- Borshchev, A., Filippov, A. (2004). "From System Dynamics and Discrete Event to Practical Agent Based
  Modeling: Reasons, Techniques, Tools." *22nd Int. Conf. of the System Dynamics Society*.
- Borshchev, A. (2013). *The Big Book of Simulation Modeling: Multimethod Modeling with AnyLogic.*
  AnyLogic North America.
- Grigoryev, I. (2015+). *AnyLogic in Three Days: A Quick Course in Simulation Modeling.* (editions
  ongoing).

## See also
- Unifies: [Vensim](vensim.md) · [Stella](stella.md) (SD) · [Mesa](mesa.md) · [Repast](repast.md) · [NetLogo](netlogo.md) · [GAMA](gama.md) (ABM)
- Paradigm debate it answers: [System Dynamics vs Agent-Based](../../comparative/system-dynamics-vs-abm.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md)
- Patterns: [Integration Engine](../../patterns/integration-engine.md) · [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Visualization Engine](../../patterns/visualization-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
