# WEAP — Water Evaluation And Planning system

!!! info "Bronze dossier"
    WEAP is the **planning and allocation** pole of the water domain — the tool that asks not "how does
    water physically move?" ([SWAT](swat.md)/[MODFLOW](modflow.md)) but "**who gets how much, and does
    supply meet demand under this policy?**" It couples **scenario-based demand/supply accounting** with
    a **priority-based network allocation (LP)** step, in an accessible interface built for
    **stakeholder-facing river-basin and transboundary** planning. It completes the water triad:
    process · physics · **allocation**.

> An integrated water-resources planning tool combining scenario-based demand/supply accounting with a
> network allocation (LP) step, widely used for river-basin and transboundary planning.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | WEAP |
|------|------|
| Optimization vs Simulation | **Simulation + allocation optimization** (LP each step) |
| Top-down vs Bottom-up | **Bottom-up** (nodes/links network) |
| Equilibrium | **Priority-based allocation** (not market equilibrium) |
| Foresight | Myopic (monthly step) |
| Deterministic vs Stochastic | Deterministic (+ scenarios) |
| Time / Space | **Monthly / basin network** |
| Solution method | **LP allocation embedded in a water-balance simulation** |

| Field | Value |
|-------|-------|
| Full name | WEAP — Water Evaluation And Planning system |
| Domain | Water |
| First release / current | 1990s / ongoing |
| Institution · lead | Stockholm Environment Institute (SEI) |
| Language · solver | Windows application (Delphi + embedded LP solver) |
| License / access | Freeware for qualifying (developing-country / academic) users |

---

## 🎓 Scholar Track

**History & motivation.** WEAP was developed by the **Stockholm Environment Institute (SEI)** from the
1990s to fill a gap the physical models leave open: **integrated water-resources planning** that
ordinary agencies and stakeholders can actually use. Its motivating stance is **management, not
mechanism** — combine all the pieces of a basin (rivers, reservoirs, aquifers, demands, wastewater,
hydropower) in **one accounting framework**, and let planners test **scenarios** (population growth,
climate, new dams, efficiency, allocation rules) on **supply reliability, unmet demand, and
environmental flows**. Accessibility and scenario transparency are the design priorities — hence its
heavy use in **developing countries and transboundary basins** (Nile, Mekong, etc.).

**Mathematical formulation.** WEAP represents a basin as a **network of nodes and links** — demand
sites, catchments, rivers, reservoirs, groundwater, treatment, hydropower — carrying a **monthly mass-
balance** of water. The distinctive step is **allocation**: at each time step WEAP solves a
**linear program** that allocates available supply to demands so as to **maximize satisfaction of
demand subject to priorities and constraints** (mass balance, capacities, environmental-flow
requirements, and user-assigned **demand priorities** and **supply preferences**). Formally, each
month:

$$\max \sum_d \text{coverage}_d \quad \text{s.t. mass balance, capacity, priority ordering, min-flow
constraints},$$

so higher-priority demands are met first and shortages fall on lower-priority uses — a **rule/priority-
based allocation**, not a market or welfare optimum. Optional modules add rainfall-runoff hydrology
(so WEAP can generate its own inflows), water quality, and financial cost-benefit. It is **recursive
(myopic)** month to month.

**Solution algorithm.** Step monthly: compute inflows (from data or the built-in hydrology module),
solve the **allocation LP** for the current step given priorities/constraints, update reservoir and
aquifer storages, record coverage/unmet demand and environmental indicators; repeat over the horizon
for each **scenario**. Fast and interactive.

**Calibration & validation.** Hydrology calibrated to gauged flows where the runoff module is used;
allocation validated against observed operations/deliveries; validation emphasis is **scenario
plausibility and stakeholder review** as much as statistical fit, reflecting its planning role.

**Strengths / weaknesses / criticisms.** *Strengths:* **integrative** (supply+demand+quality+economics
in one), **accessible** and scenario-centric, strong for **participatory and transboundary** planning,
free for qualifying users. *Criticisms:* **coarse physics** (monthly, network — not the process detail
of SWAT or the aquifer physics of MODFLOW); priority allocation is a simplification of real
institutions/markets; **closed-source Windows** app limits deep customization.

## 🛠️ Engineer Track

**Architecture & engines.** A water-balance **[Integration Engine](../../patterns/integration-engine.md)**
over a network **[Spatial Engine](../../patterns/spatial-engine.md)** (nodes/links), wrapping an
**[Optimization Engine](../../patterns/optimization-engine.md)** (the per-step allocation **LP**) and a
strong **[Scenario Engine](../../patterns/scenario-engine.md)** (the user-facing heart of the tool). A
**[Policy Engine](../../patterns/policy-engine.md)**-style layer expresses allocation rules, priorities,
and demand-management measures. Delivered as a Windows GUI with scripting/API access.

**Data & complexity.** Lightweight (monthly, network-scale) — deliberately, to keep whole-basin scenario
analysis interactive. Data assembly (demands, infrastructure, priorities) is the main effort.

**Openness / extensibility.** **Freeware** (SEI) for qualifying users, **closed source**; extensible via
its scripting API and by **linking to physical models** (e.g. WEAP-MODFLOW coupling for conjunctive
surface-groundwater management). Large global user community and training program.

## 🏛️ Architect Track

**Reusable patterns.** WEAP's transferable ideas: **embed an allocation LP inside a simulation**
(simulate the system, but solve a small optimization at each step to distribute a scarce resource by
priority), **priority-based allocation** as an alternative to market clearing, and a **scenario-first,
stakeholder-facing** design where comparing futures is the primary workflow. Its **coupling to MODFLOW**
exemplifies the multi-engine water domain.

**Trade-offs & alternatives.** WEAP is the **allocation/planning** engine; it complements
[SWAT](swat.md) (surface process hydrology) and [MODFLOW](modflow.md) (groundwater physics) — the three
answer *management*, *surface process*, and *subsurface physics* respectively, and are increasingly
**coupled**. WEAP's per-step LP makes it a **hybrid simulation+optimization** (like an energy-dispatch
model for water), distinct from pure-simulation SWAT/MODFLOW — a nuance on the
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) axis. Peers: RiverWare,
MIKE HYDRO/Basin, Aquatool, Pywr.

**Adoption.** Very widely used for **integrated water-resources management** worldwide, especially in
**developing countries and transboundary basins** (Nile, Mekong, Indus, Colorado); a staple of
climate-adaptation and water-security planning (SEI, UN agencies, development banks).

**Ecosystem.** SEI (WEAP, LEAP energy sibling); links to MODFLOW/QUAL; peers RiverWare, MIKE HYDRO,
Pywr, Aquatool.

**Research gaps.** Finer physics/coupling; representing institutions and water markets beyond priority
rules; open-sourcing; uncertainty.

!!! quote "Lesson for the integrated simulator"
    WEAP shows that within a single domain the **management question is distinct from the physics
    question**, and needs its own engine: to plan a basin you **embed a small allocation optimization
    (an LP over a priority-ordered network) inside a simulation**, rather than resolving physics in
    detail. For the integrated simulator this is the **hybrid simulate-then-allocate** pattern — the
    water analogue of energy dispatch — and it reinforces two atlas themes: **scenario comparison as the
    primary interface** (WEAP's whole design is "compare these futures"), and **coupling engines by
    question** (WEAP↔MODFLOW for conjunctive management). WEAP's **priority-based allocation** is also a
    reminder that not all resource sharing is a market: the simulator should offer **allocation rules,
    priorities, and equity constraints** as first-class alternatives to price-clearing — the same
    "which closure?" dial the economics family raised, now for water.

## Major publications

- Yates, D., Sieber, J., Purkey, D., Huber-Lee, A. (2005). "WEAP21—A demand-, priority-, and
  preference-driven water planning model: Part 1, Model characteristics." *Water International* 30(4).
- Sieber, J., Purkey, D. (2015). *WEAP: Water Evaluation And Planning System — User Guide.* Stockholm
  Environment Institute.
- Purkey, D. R., et al. (2008). "Robust analysis of future climate change impacts on water for
  agriculture (WEAP application)." *Climatic Change* 87.

## See also
- Water-domain peers: [SWAT](swat.md) (surface process) · [MODFLOW](modflow.md) (groundwater physics) · Contrast: [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Patterns: [Scenario Engine](../../patterns/scenario-engine.md) · [Optimization Engine](../../patterns/optimization-engine.md) · [Integration Engine](../../patterns/integration-engine.md) · [Policy Engine](../../patterns/policy-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
