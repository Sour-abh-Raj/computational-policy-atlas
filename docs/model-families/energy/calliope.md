# Calliope

!!! info "Bronze dossier"
    Calliope is the **declarative, reproducibility-first** energy-system optimizer: you describe a
    system in **YAML** — technologies, locations, links, constraints — and Calliope builds and
    solves the least-cost LP/MILP for you. Same optimization pole as [PyPSA](pypsa.md),
    [OSeMOSYS](osemosys.md) and [TIMES](times.md), but its distinctive contribution is a **clean
    model-definition language** that separates *what the system is* from *how it is solved*.

> A flexible, declarative (YAML-configured) open energy-system optimization framework emphasizing
> reproducibility and high temporal/spatial resolution for scenario exploration.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Calliope |
|------|------|
| Optimization vs Simulation | **Optimization** (least-cost) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | Partial equilibrium |
| Foresight | Perfect foresight |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | Hourly / multi-node |
| Solution method | **LP / MILP** (declarative model build) |

| Field | Value |
|-------|-------|
| Full name | Calliope |
| Domain | Energy Systems |
| First release / current | 2013 / ongoing (v0.7+) |
| Institution · lead | ETH Zürich / Cambridge (Stefan Pfenninger, Bryn Pickering) |
| Language · solver | Python (Pyomo/`gurobipy`; Gurobi/CBC/GLPK) |
| License / access | Open (Apache 2.0) |

---

## 🎓 Scholar Track

**History & motivation.** Calliope was started ~2013 by **Stefan Pfenninger** (with Bryn
Pickering) to address a *software-engineering* pain point in energy modeling: models were bespoke
scripts, hard to reproduce and hard to share. Calliope's answer is **radical separation of
concerns** — the model is a **declarative YAML/CSV description** (technologies, carriers, nodes,
transmission links, costs, constraints, time series), and the framework compiles that description
into a mathematical program, solves it, and returns a tidy multi-dimensional dataset. The
philosophy: **a model should be data, not code**.

**Mathematical formulation.** Calliope builds a **linear (or mixed-integer) least-cost program**:
minimize total system cost (annualized investment + operation) over technology **capacities** and
hourly **flows**, subject to **per-node, per-carrier energy balance** at every timestep, capacity
and resource-availability constraints (e.g. hourly renewable capacity factors), storage
state-of-charge dynamics, and transmission link limits between nodes. It is a **transport /
energy-balance** representation of the network (flows on links, no Kirchhoff voltage law) — simpler
physics than [PyPSA](pypsa.md), which is often exactly the right abstraction for multi-carrier and
sector-coupled studies. In v0.7 the **constraints themselves are declarative** ("math" defined in
YAML), so users can add custom constraints without touching Python — an unusually clean realization
of a **model-generator** ([TIMES](times.md) is the classic model generator; Calliope is its modern,
open, YAML-native cousin).

**Solution algorithm.** The declarative model is compiled (via Pyomo or a native backend) into an
**LP/MILP** and solved with **Gurobi/CBC/GLPK**; results come back as an **xarray Dataset**.
Tractability at high resolution uses **time-series aggregation** (representative days/clustering).

**Calibration & validation.** Inputs are user-supplied open datasets (demand profiles, renewables.
ninja / atlite capacity factors — the **renewables.ninja** service comes from the same group);
validated by reproducing published national/European scenarios and through the model's strong
reproducibility tooling (every run is fully specified by its config).

**Strengths / weaknesses / criticisms.** *Strengths:* **reproducibility and clarity** — a model is
a self-contained, versionable set of text files; low barrier to build new systems; **declarative
custom math**. *Criticisms:* transport-flow network (no AC power-flow physics) limits grid-detail
questions PyPSA can answer; like all perfect-foresight LP bottom-up models it assumes a benevolent
least-cost planner and price-taking; very high resolution still needs aggregation.

## 🛠️ Engineer Track

**Architecture & engines.** An **[Optimization Engine](../../patterns/optimization-engine.md)**
driven by a **declarative model-definition layer** — the notable engineering idea is a
**[Data Pipeline](../../patterns/data-pipeline.md)** that *is* the model: YAML/CSV → compiled
program → **xarray** results. It exhibits the **[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**
pattern (least-cost dispatch + investment) and a lightweight
**[Scenario Engine](../../patterns/scenario-engine.md)** (scenario/override system for sweeping
assumptions).

**Data & complexity.** Multi-node, hourly, multi-carrier LPs; scales via **temporal clustering**
and node aggregation. The xarray-based I/O makes post-processing and comparison natural.

**Openness / extensibility.** **Apache-2.0**, pip-installable, thoroughly documented; the v0.7
**declarative custom-math** feature makes it extensible **without forking the code** — new
constraints live in config. Solver-agnostic.

## 🏛️ Architect Track

**Reusable patterns.** The headline pattern is **model-as-data / declarative model generator**:
describe the system and its math declaratively; let the framework build and solve. This is the open,
YAML-native evolution of the **[TIMES](times.md) model-generator** idea, and it is directly relevant
to any simulator that wants users to *configure* rather than *program* new cases. Also reusable:
**scenario overrides** as a first-class config construct and **tidy (xarray) result contracts**.

**Trade-offs & alternatives.** Calliope vs [PyPSA](pypsa.md): both are open, Python, hourly,
spatially explicit LP/MILP tools; PyPSA carries **power-flow physics** and a rich power-sector focus,
Calliope carries a **cleaner declarative modeling language** and multi-carrier generality — pick by
whether grid physics or model ergonomics dominates the question. Versus [OSeMOSYS](osemosys.md)/
[TIMES](times.md): Calliope is higher temporal resolution and more modern tooling but typically
shorter horizon. Versus [EnergyPLAN](energyplan.md): optimization vs rule-based simulation — the
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) contrast within energy.

**Adoption.** Widely used in **academic** European energy-transition and national-scenario studies;
popular in teaching for its clarity; paired with **renewables.ninja** for input data.

**Ecosystem.** renewables.ninja, atlite, the SPINE/oemof adjacent open-energy-modeling community;
peers PyPSA, oemof, Switch, TIMES, OSeMOSYS.

**Research gaps.** Optional power-flow fidelity; stochastic/robust formulations; endogenous demand;
scaling declarative math to very large systems.

!!! quote "Lesson for the integrated simulator"
    Calliope's lesson is about **ergonomics and reproducibility as architecture**, not just physics:
    make the model a **declarative artifact** — data and math expressed in config — so a run is fully
    specified, versionable, and reproducible without reading source code. That is exactly the
    "model-generator" idea [TIMES](times.md) pioneered, brought into the open-source, text-native
    world. For the integrated simulator, the takeaway is to expose a **declarative model-definition
    layer** above the solver so users compose new cases (technologies, constraints, scenarios) as
    *configuration*, and to standardize on a **tidy result contract** (labelled n-dimensional arrays)
    so cross-model and cross-scenario comparison — the atlas's whole purpose — is frictionless.

## Major publications

- Pfenninger, S., Pickering, B. (2018). "Calliope: a multi-scale energy systems modelling
  framework." *Journal of Open Source Software* 3(29), 825.
- Pickering, B., Pfenninger, S., et al. (2022). "Diversity of options to reach carbon-neutral
  Europe." *Joule* (Calliope-Euro-Calliope application).
- Pfenninger, S., Staffell, I. (2016). "Long-term patterns of European PV/wind output"
  (renewables.ninja), *Energy* 114.

## See also
- Contrast: [PyPSA](pypsa.md) · [TIMES](times.md) · [OSeMOSYS](osemosys.md) · [EnergyPLAN](energyplan.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Scenario Engine](../../patterns/scenario-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
