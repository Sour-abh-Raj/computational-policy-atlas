# EnergyPLAN

!!! info "Bronze dossier"
    EnergyPLAN is the **odd one out** of the energy family — and deliberately so. It does **not
    optimize**. It **simulates**, hour by hour, a complete national energy system (electricity,
    heat, cooling, transport, gas) under **explicit operating rules**, to test whether a proposed
    **100%-renewable / smart-energy** configuration actually balances. It is the atlas's
    in-domain example that the [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
    choice is a genuine fork even among bottom-up energy models.

> A deterministic hourly *simulation* (not optimization) of complete national energy systems —
> electricity, heat, transport, gas — built to analyze 100%-renewable and smart-energy-system
> scenarios.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | EnergyPLAN |
|------|------|
| Optimization vs Simulation | **Simulation** (rule-based dispatch) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A (no market clearing) |
| Foresight | Myopic (hourly) |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | Hourly (8784 h) / national aggregate |
| Solution method | **Analytical / heuristic simulation** |

| Field | Value |
|-------|-------|
| Full name | EnergyPLAN |
| Domain | Energy Systems |
| First release / current | 1999 / ongoing |
| Institution · lead | Aalborg University (Henrik Lund) |
| Language · solver | Delphi/Pascal (freeware GUI, Windows) |
| License / access | Freeware (closed source) |

---

## 🎓 Scholar Track

**History & motivation.** EnergyPLAN was created by **Henrik Lund at Aalborg University** from
1999, out of the Danish tradition of **integrated, cross-sector energy planning** ("smart energy
systems"). Its founding argument is a critique of pure optimization: a least-cost optimizer will
often hide the *operational feasibility* question behind an objective function. EnergyPLAN instead
asks, directly and transparently, **"given this exact system, does it balance every hour, and what
does it cost and emit?"** — making it a natural tool for **100%-renewable** feasibility studies
where the interesting question is coupling across electricity, heat, gas and transport, not marginal
least-cost dispatch.

**Mathematical formulation.** EnergyPLAN is a **deterministic hourly simulation** over a full year
(8784 hours) of a **single aggregated region** (a nation). There is **no objective function and no
solver**; instead the system state each hour is computed **analytically** from **explicit
priority/dispatch rules** and energy balances across coupled sub-systems: electricity supply/demand,
district heating with CHP and heat storage, individual heating and heat pumps, cooling, industry,
transport (including electric vehicles and electrofuels), and gas/fuel systems. The user chooses a
**regulation strategy** (e.g. "balance heat demand" vs "balance both heat and electricity",
technical vs market-economic dispatch), and EnergyPLAN steps through the year applying it,
dispatching flexible units, storage, and imports/exports to keep every carrier balanced. Outputs:
hourly balances, annual energy/fuel totals, CO₂ emissions, critical excess electricity production
(CEEP), and total socio-economic cost.

**Solution algorithm.** A **fast analytical pass** through 8784 hours applying the chosen dispatch
logic — seconds per run, no iterative optimization. Because it is a simulation, it can represent
system configurations directly and cheaply, enabling **large scenario sweeps**.

**Calibration & validation.** Configured from national energy-balance statistics (e.g. IEA/Eurostat)
and validated against historical annual balances and Danish energy-system data; extensively used to
reproduce and stress-test national decarbonization plans.

**Strengths / weaknesses / criticisms.** *Strengths:* **transparent, fast, cross-sector**, ideal for
**feasibility** and smart-energy-system coupling; no optimization opacity — you see exactly what the
rules do. *Criticisms:* **no optimization** means it answers "does *this* system work?" not "what is
the *best* system?"; single-node (no transmission/space); closed-source freeware (Pascal/GUI) limits
scripting and inspection; myopic hourly rules are not economic equilibrium.

## 🛠️ Engineer Track

**Architecture & engines.** A pure **[Integration Engine](../../patterns/integration-engine.md)** in
the discrete-time, rule-based sense — coupled sub-system balances stepped hour by hour — combined
with a **[Policy Engine](../../patterns/policy-engine.md)**-like set of selectable **regulation
strategies**. Notably it is **not** an [Optimization Engine](../../patterns/optimization-engine.md);
that absence is the whole point. Delivered as a **Windows GUI freeware** with spreadsheet-style
inputs.

**Data & complexity.** Trivial computationally (an annual hourly pass over one aggregated region),
which is exactly what makes it excellent for **thousands of scenario runs** and participatory /
teaching settings.

**Openness / extensibility.** **Freeware but closed-source** (Delphi/Pascal); extensibility is
through its rich built-in parameterization and strategy menu rather than code. A large user community
and training courses (Aalborg) surround it.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is **rule-based cross-sector simulation for
feasibility**: to test whether a configuration *works operationally*, simulate it under explicit
dispatch rules rather than optimizing — cheap, transparent, and honest about operational balancing
(CEEP, storage cycling). Also reusable: **selectable regulation strategies** as a first-class control,
and **sector coupling** (power↔heat↔gas↔transport) as the default scope, not an add-on.

**Trade-offs & alternatives.** EnergyPLAN is the **simulation** counterpoint to the optimizing
bottom-up models [PyPSA](pypsa.md)/[Calliope](calliope.md)/[OSeMOSYS](osemosys.md)/[TIMES](times.md):
it forgoes "what's optimal?" to gain transparency and speed on "does this exact plan balance?" — the
clearest in-domain instance of [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md).
Against [PyPSA](pypsa.md) specifically, it trades away spatial/network detail and optimization for
**cross-sector breadth and interpretability**. Many studies use **both**: EnergyPLAN to scan
feasible configurations, an optimizer to refine.

**Adoption.** The reference tool for **100%-renewable and smart-energy-system** studies (Denmark and
across Europe/globally); heavily cited in the Lund/Aalborg "Smart Energy Systems" literature; used by
municipalities, NGOs, and educators.

**Ecosystem.** Aalborg "Smart Energy Systems" school; companion tools (EnergyPLAN training, spinoffs
and open re-implementations); peers PyPSA, Calliope, oemof, TIMES.

**Research gaps.** Open-sourcing / scriptability; spatial disaggregation; bridging its simulation
outputs with optimization for combined feasibility-then-optimality workflows.

!!! quote "Lesson for the integrated simulator"
    EnergyPLAN reminds the atlas that **optimization is a choice, not a requirement — even inside the
    bottom-up energy world**. Some of the most policy-relevant questions are *feasibility* questions
    ("does this 100%-renewable plan actually balance every hour, and how much energy is wasted?"),
    and those are answered more honestly by **simulating an explicit configuration under transparent
    rules** than by trusting a least-cost objective. For the integrated simulator this argues for a
    **dual mode**: let a system be *simulated* under user-chosen dispatch/regulation strategies **and**
    *optimized*, and treat the pair as complementary — scan feasible cross-sector configurations
    cheaply by simulation, then optimize the promising ones. Its insistence on **sector coupling as
    the default scope** (power, heat, gas, transport in one balance) is also exactly the integrated
    view the simulator is meant to embody.

## Major publications

- Lund, H. (2014). *Renewable Energy Systems: A Smart Energy Systems Approach.* 2nd ed., Academic
  Press.
- Lund, H., et al. (2021). "EnergyPLAN — Advanced analysis of smart energy systems." *Smart Energy*
  1, 100007.
- Lund, H., Thellufsen, J. Z., et al. (2022). EnergyPLAN documentation, Aalborg University.

## See also
- Contrast: [PyPSA](pypsa.md) · [Calliope](calliope.md) · [OSeMOSYS](osemosys.md) · [TIMES](times.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Patterns: [Integration Engine](../../patterns/integration-engine.md) · [Policy Engine](../../patterns/policy-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
