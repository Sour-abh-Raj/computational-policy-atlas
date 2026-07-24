# PyPSA — Python for Power System Analysis

!!! info "Bronze dossier"
    PyPSA is the **modern, network-physics-aware** member of the bottom-up energy family. Where
    [OSeMOSYS](osemosys.md) and [TIMES](times.md) optimize an *energy-carrier* system with
    time-slice resolution, PyPSA optimizes an **electricity (and sector-coupled) network** at
    **hourly resolution over an explicit nodal grid**, carrying **real power-flow physics**
    (KCL/KVL, linearized load flow). It is the reference tool for European energy-transition
    studies (PyPSA-Eur, PyPSA-Earth).

> A modern open toolbox for power (and sector-coupled) system optimization at high spatial and
> hourly resolution, with true network power-flow physics — the reference for European
> energy-transition studies.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | PyPSA |
|------|------|
| Optimization vs Simulation | **Optimization** (least-cost dispatch + investment) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | Partial equilibrium |
| Foresight | Perfect foresight (over horizon) |
| Deterministic vs Stochastic | Deterministic (stochastic add-ons) |
| Time / Space | **Hourly / nodal network** |
| Solution method | **LP / MILP + linearized power flow** |

| Field | Value |
|-------|-------|
| Full name | PyPSA — Python for Power System Analysis |
| Domain | Energy Systems |
| First release / current | 2015 / ongoing |
| Institution · lead | TU Berlin (Tom Brown et al.) / open community |
| Language · solver | Python (Linopy/Pyomo; Gurobi/HiGHS/CBC) |
| License / access | Open (MIT; GPL data components) |

---

## 🎓 Scholar Track

**History & motivation.** PyPSA was created ~2015 by **Tom Brown, Jonas Hörsch and David
Schlachtberger** (then FIAS, now TU Berlin) to give the research community a **free, transparent,
Python-native** alternative to proprietary power-system tools — one that could co-optimize
**investment and operation** of a renewable-dominated grid while respecting **network physics**.
Its distinguishing bet against the classic MARKAL/TIMES lineage: **space matters**. Renewables are
where the wind and sun are, not where the load is, so a credible decarbonization model must
represent **transmission** explicitly.

**Mathematical formulation.** PyPSA solves a **linear (or mixed-integer) program**: minimize total
**annualized investment + operating cost** over generators, storage, and transmission, subject to
**nodal energy balance every hour at every bus**, generator capacity and availability (hourly
renewable capacity factors), **storage state-of-charge dynamics**, and — its signature —
**linearized power-flow constraints**. For AC networks it uses the **linear ("DC") load-flow**
approximation, imposing **Kirchhoff's voltage law** as cycle constraints on line flows in addition
to **Kirchhoff's current law** (nodal balance); line flows are bounded by thermal limits, and
**transmission expansion** can itself be an investment variable (LP if continuous, MILP if
discrete). Decision variables: capacities (generation, storage, lines) and hourly dispatch/flows.
The result is a least-cost **capacity-expansion + dispatch** plan that is *spatially explicit*.

**Solution algorithm.** A large sparse **LP** (or MILP with unit-commitment/discrete expansion),
built via **Linopy** (or legacy Pyomo) and handed to **Gurobi/HiGHS/CBC**. To stay tractable at
hourly × nodal scale, models use **time-series clustering** (representative snapshots), **spatial
clustering** (network reduction to k regions), and rolling-horizon dispatch.

**Calibration & validation.** Networks are built from **open data** — ENTSO-E grid topology,
OpenStreetMap, ERA5/atlite-derived renewable time series, powerplant databases — and validated
against historical dispatch and cross-border flows; PyPSA-Eur is benchmarked in multiple European
studies.

**Strengths / weaknesses / criticisms.** *Strengths:* **spatial + temporal detail** with real
grid physics; fully **open and reproducible**; excellent for high-renewable, transmission-,
storage-, and sector-coupling questions. *Criticisms:* the **linear load-flow** approximation omits
voltage/reactive-power and stability dynamics (it is a planning, not a stability, tool); full
hourly-nodal models are **large** and lean on clustering; perfect foresight and price-taking
partial equilibrium share the usual bottom-up idealizations.

## 🛠️ Engineer Track

**Architecture & engines.** A textbook **[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**
extended with a **network layer** — closest thing in the atlas to a
**[Spatial Engine](../../patterns/spatial-engine.md)** on a *graph* (buses/lines) rather than a
grid — wrapped by an **[Optimization Engine](../../patterns/optimization-engine.md)** and fed by a
substantial **[Data Pipeline](../../patterns/data-pipeline.md)** (atlite for weather→capacity
factors, network import/clustering). The data model is a set of **pandas DataFrames** (components:
buses, lines, generators, storage, loads) — a clean, inspectable in-memory representation.

**Data & complexity.** Hourly (8760 snapshots) × hundreds–thousands of buses is the stress point;
handled by **snapshot clustering** and **spatial aggregation**. Modular sector coupling
(**PyPSA-Eur-Sec**) adds heat, transport, hydrogen and industry to the same LP.

**Openness / extensibility.** **MIT-licensed**, pip-installable, with the **PyPSA-Eur** /
**PyPSA-Earth** open reference models; large academic user base and active GitHub community. Solver-
agnostic (open HiGHS through commercial Gurobi).

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is **network-resolved least-cost planning**: put the
transmission graph and its **power-flow constraints inside** the optimization so siting and
transmission trade against generation and storage. Also reusable: a **DataFrame-native component
model** and a **weather→capacity-factor pipeline** that turns reanalysis data into hourly renewable
availability.

**Trade-offs & alternatives.** Within the bottom-up family: [OSeMOSYS](osemosys.md) and
[TIMES](times.md) span **all energy carriers and long horizons with time-slices** but treat space
coarsely; PyPSA and [Calliope](calliope.md) go **hourly and spatially explicit** but focus on
power/sector-coupling over a shorter horizon. PyPSA's unique addition over Calliope is **actual
power-flow physics** (KVL cycle constraints); Calliope stays transport-model (energy-balance)
without load flow. All are the *optimization* pole against
[EnergyPLAN](energyplan.md)'s rule-based simulation — the
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) axis inside one
domain; LP-vs-MILP tension is the [LP vs MILP](../../comparative/lp-vs-milp.md) chapter.

**Adoption.** Heavy use in **European** transmission and 100%-renewable studies (Agora, ENTSO-E-
adjacent research, EU projects); **PyPSA-Earth** extends it to the global South; taught widely.

**Ecosystem.** PyPSA-Eur, PyPSA-Eur-Sec, PyPSA-Earth, atlite, Linopy, powerplantmatching; peers
Calliope, Switch, GenX, OSeMOSYS, TIMES.

**Research gaps.** Reactive-power/AC and stability integration; uncertainty (stochastic/robust
expansion) at scale; endogenizing demand; foresight realism.

!!! quote "Lesson for the integrated simulator"
    PyPSA is the atlas's proof that **space and network physics belong *inside* the optimization**,
    not bolted on afterward. By carrying Kirchhoff's laws as constraints, it makes **where** to
    build renewables and transmission a first-class decision that trades against **what** to build —
    something time-slice IAMs and carrier-only energy models structurally cannot see. For the
    integrated simulator this argues for a **graph-native spatial layer** with switchable physical
    fidelity (copper-plate → linear load-flow → AC), plus a **weather-to-availability data pipeline**
    as core infrastructure. Its DataFrame component model is also a lesson in *ergonomics*: an
    inspectable, open, scriptable representation lowers the barrier to reproducibility — a value the
    simulator should inherit.

## Major publications

- Brown, T., Hörsch, J., Schlachtberger, D. (2018). "PyPSA: Python for Power System Analysis."
  *Journal of Open Research Software* 6(1).
- Hörsch, J., et al. (2018). "PyPSA-Eur: An open optimisation model of the European transmission
  system." *Energy Strategy Reviews* 22.
- Neumann, F., et al. (2023). "The potential role of a hydrogen network in Europe" & PyPSA-Eur-Sec
  sector-coupling documentation.

## See also
- Contrast: [Calliope](calliope.md) · [OSeMOSYS](osemosys.md) · [TIMES](times.md) · [EnergyPLAN](energyplan.md) · [LP vs MILP](../../comparative/lp-vs-milp.md)
- Patterns: [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
