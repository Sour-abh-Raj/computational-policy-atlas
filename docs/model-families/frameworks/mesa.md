# Mesa

!!! info "Bronze dossier"
    Mesa is not a *model* but a **framework** — the Pythonic toolkit for *building* agent-based
    models. Where [Covasim](../health/covasim.md), [MATSim](../transport/matsim.md) and
    [GCAM](../climate-iam/gcam.md) are finished models, Mesa gives you the reusable machinery every
    ABM needs — a **scheduler**, **spatial grids/networks**, **data collection**, and
    **visualization** — so a modeler writes only the domain logic. It is the ABM counterpart to what
    [Vensim](vensim.md) is for system dynamics: the environment in which the paradigm is practiced.

> A Python framework for building agent-based models, providing scheduling, spatial grids/networks,
> data collection and browser-based visualization — the Pythonic entry point to ABM.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Mesa |
|------|------|
| Optimization vs Simulation | **Simulation** (ABM toolkit) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A (model-defined) |
| Foresight | Model-defined |
| Deterministic vs Stochastic | Model-defined (usually stochastic) |
| Time / Space | Model-defined / grid or network |
| Solution method | **Scheduler + agent step loop** |

| Field | Value |
|-------|-------|
| Full name | Mesa (Agent-Based Modeling in Python) |
| Domain | Frameworks & Environments |
| First release / current | 2014 / ongoing (Mesa 2.x/3.x) |
| Institution · lead | Project Mesa (open community; Masad, Kazil originators) |
| Language · solver | Python |
| License / access | Open (Apache 2.0) |

---

## 🎓 Scholar Track

**History & motivation.** Mesa began in **2014** (David Masad, Jackie Kazil) to fill an obvious gap:
the ABM world was dominated by **[NetLogo](netlogo.md)** (great for teaching, its own language) and
Java frameworks (**[Repast](repast.md)**, MASON), but there was **no first-class Python ABM
framework** — even as Python became the lingua franca of data science. Mesa's motivation is
**ecosystem**, not epistemics: let modelers build ABMs in Python and plug straight into
**NumPy/pandas/Matplotlib/networkx** for analysis. It has no scientific "position" of its own; its
contribution is **architecture and accessibility**.

**Mathematical formulation.** Mesa has **no fixed mathematics** — it is a *meta-model* substrate. It
formalizes the **structure common to all ABMs**: a `Model` owns a population of `Agent` objects, a
**scheduler** (`time`) that determines *activation order* (simultaneous, random, staged — each a
different discretization of "a step"), a **space** (`grid`/`network` — orthogonal/hex grids,
continuous space, or a `networkx` graph), and a **`DataCollector`** that records agent- and
model-level variables into tidy tables. The modeler supplies the **`step()`** logic — what each agent
does per tick — and Mesa runs the **discrete-time loop** and manages state, batching (parameter
sweeps), and reproducible RNG seeding. The "solution" is simply **iterated stepping** of the agent
population; any emergent regularity is a property of the user's rules, not of Mesa.

**Solution algorithm.** The canonical loop: `for step in range(N): scheduler.step()`, where the
scheduler calls each agent's `step()` in the chosen activation order; the `DataCollector` snapshots
state; **`batch_run`** repeats across parameter combinations and RNG seeds for ensembles. Everything is
ordinary Python, so profiling/parallelism use standard tools.

**Calibration & validation.** Out of scope for the framework itself — Mesa provides the **batch-run /
data-collection** plumbing on which calibration and sensitivity analysis are built (SALib, ABM
calibration libraries), but the modeler owns validation of their specific model.

**Strengths / weaknesses / criticisms.** *Strengths:* **Pythonic**, low barrier, integrates with the
entire scientific-Python stack; clean separation of scheduler/space/data/visualization; **browser-
based interactive** visualization; strong for prototyping and teaching. *Criticisms:* **pure-Python
performance** limits very large agent counts (mitigated by vectorization, Numba, or dropping to
C/Julia — the reason performance-critical models like [OpenABM](../health/openabm.md) use C);
less battle-tested at massive scale than Repast HPC.

## 🛠️ Engineer Track

**Architecture & engines.** Mesa **is** an explicit realization of several atlas patterns as software:
a **[Behavior Engine](../../patterns/behavior-engine.md)** (Agent/`step`), a
**[Spatial Engine](../../patterns/spatial-engine.md)** (grid/network space), an
**[Integration Engine](../../patterns/integration-engine.md)** (the scheduler/step loop), a
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)**/batch-runner, and a
**[Visualization Engine](../../patterns/visualization-engine.md)** (Solara/browser UI). It is, in
effect, a **pattern catalog turned into a library**.

**Data & complexity.** Agent state is plain Python objects; `DataCollector` yields pandas DataFrames.
Complexity is whatever the user's rules impose; framework overhead is modest but the Python
interpreter caps raw agent throughput.

**Openness / extensibility.** **Apache-2.0**, pip-installable, actively developed with a large
community and example library; extensible via mesa-geo (GIS), mesa-frames (vectorized), and the
scientific-Python ecosystem.

## 🏛️ Architect Track

**Reusable patterns.** Mesa is itself the lesson: it **factors the ABM paradigm into swappable
components** — *scheduler* (activation regime), *space* (grid vs network vs continuous), *data
collection*, *visualization*, *batch runner* — exactly the decomposition an engine-oriented simulator
wants. The **activation-order abstraction** (simultaneous vs random vs staged) is a subtle, reusable
insight: *how* you discretize "a step" changes results, so it should be an explicit, swappable choice.

**Trade-offs & alternatives.** Mesa (Python) vs [Repast](repast.md) (Java/HPC, scale) vs
[NetLogo](netlogo.md) (own language, teaching/prototyping) vs [GAMA](gama.md) (GIS-heavy, GAML
language) — the four are the main general ABM frameworks; Mesa wins on **Python-ecosystem integration
and accessibility**, Repast on **raw scale**, NetLogo on **pedagogy**, GAMA on **spatial/GIS**. Domain
ABMs ([Covasim](../health/covasim.md), [OpenABM](../health/openabm.md), [MATSim](../transport/matsim.md))
are either built on such frameworks or hand-rolled in C/Java for speed. Mesa is to ABM what
[Vensim](vensim.md) is to system dynamics — the practicing environment.

**Adoption.** Very widely used in **research and teaching** (social science, ecology, economics,
epidemiology prototypes); the default when a model must live in the Python data stack.

**Ecosystem.** Project Mesa (mesa, mesa-geo, mesa-frames, Solara viz); integrates NumPy/pandas/
networkx/SALib; peers Repast, MASON, NetLogo, GAMA, AnyLogic, Agents.jl.

**Research gaps.** Performance at massive scale (vectorized/GPU backends); standardized model
description (ODD protocol tooling); reproducibility conventions.

!!! quote "Lesson for the integrated simulator"
    Mesa is a **working blueprint for the atlas's own thesis** — that a simulator should be built from
    **swappable engines**. It decomposes agent-based modeling into exactly the components the pattern
    catalog names (behavior/`step`, space, integration/scheduler, sensitivity/batch, visualization) and
    lets each be chosen independently. Two specifics transfer directly: (1) the **activation-order** of
    a step is a *modeling decision*, not a hidden default, and must be explicit and swappable
    (simultaneous vs random vs staged can change outcomes); and (2) **integration with a general
    analysis ecosystem** (here, scientific Python) is what makes a framework actually usable — the
    integrated simulator should expose tidy, standard data contracts so calibration, sensitivity, and
    visualization tools attach without friction. Mesa also flags the perennial trade-off the simulator
    must manage: **expressiveness/accessibility vs raw performance**.

## Major publications

- Kazil, J., Masad, D., Crooks, A. (2020). "Utilizing Python for Agent-Based Modeling: The Mesa
  Framework." *SBP-BRiMS 2020*, Springer LNCS.
- Masad, D., Kazil, J. (2015). "Mesa: An Agent-Based Modeling Framework." *Proc. 14th Python in
  Science Conf. (SciPy 2015)*.
- Project Mesa (2014–). *Mesa Documentation.* (open-source, readthedocs).

## See also
- Peers: [Repast](repast.md) · [NetLogo](netlogo.md) · [GAMA](gama.md) · Analogy: [Vensim](vensim.md) (SD environment)
- Built with it (paradigm): [Covasim](../health/covasim.md) · [OpenABM](../health/openabm.md) · [MATSim](../transport/matsim.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Integration Engine](../../patterns/integration-engine.md) · [Visualization Engine](../../patterns/visualization-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
