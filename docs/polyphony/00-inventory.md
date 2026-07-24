# Phase 0 — Inventory: the atlas as raw material

This document reads the completed [Atlas of Computational Policy Simulation](../index.md)
as the **design foundation** for Polyphony: what we can compose, which assumptions become
**dials**, which of the 16 **engines** are our component blueprints, which **couplings** the
knowledge graph already implies, which **synergy loops** are worth testing, and where the
**gaps** and **candidate new factors** are.

Source of truth: the ~50 model dossiers, 14 method pages, 16 engine patterns, 10 comparative
matrices, and the typed graph (`docs/graph/graph.json`, 164 nodes / 444 edges).

---

## 1. Models by family — I/O, state, native paradigm

Compact reduction of each family to what Polyphony's **common interface** must expose
(state · step · dials · I/O). "Foresight" = recursive/myopic vs perfect-foresight.

### Climate — Integrated Assessment (economy⇄climate⇄energy)
| Model | Native paradigm | State (core) | Key inputs → outputs | Foresight |
|-------|-----------------|--------------|----------------------|-----------|
| [DICE](../model-families/climate-iam/dice.md) ⭐ | Optimization (optimal control) | capital, CO₂ stocks, temperature | savings & abatement rate → SCC, T, GDP | perfect |
| [GCAM](../model-families/climate-iam/gcam.md) ⭐ | Simulation (partial-eq, nested logit) | sector shares, land, emissions | prices/policy → tech shares, emissions | recursive |
| [FUND](../model-families/climate-iam/fund.md) | Optimization (cost-benefit) | sectoral damages by region | emissions → sector-disaggregated damages | perfect |
| [PAGE](../model-families/climate-iam/page.md) | Simulation + Monte-Carlo | climate + damage distributions | priors → SCC **distribution** | perfect (stochastic) |
| [REMIND](../model-families/climate-iam/remind.md) | Optimization (Ramsey + energy) | capital, energy tech, trade | welfare max → transition paths | perfect |
| [MESSAGEix](../model-families/climate-iam/messageix.md) | Optimization (energy LP + MACRO) | energy system, macro | least-cost + feedback → pathways | perfect |
| [IMAGE](../model-families/climate-iam/image.md) | Simulation (process-based) | gridded land, C/N cycles | SSP drivers → biophysical + emissions | recursive |
| [WITCH](../model-families/climate-iam/witch.md) | Optimization (Nash game) | regional capital, R&D stocks | strategic play → coop/free-riding | perfect |
| [AIM](../model-families/climate-iam/aim.md) | Hybrid CGE + enduse | economy + tech | policy → Asia/global mitigation | recursive |

### Energy systems (bottom-up)
[OSeMOSYS](../model-families/energy/osemosys.md) ⭐, [TIMES](../model-families/energy/times.md) ⭐
(least-cost LP capacity+dispatch; state = capacities & flows; demand/costs → technology mix,
system cost, marginal/shadow prices). [PyPSA](../model-families/energy/pypsa.md) adds **nodal
network power-flow** (Kirchhoff constraints). [Calliope](../model-families/energy/calliope.md)
= declarative LP. [EnergyPLAN](../model-families/energy/energyplan.md) = **rule-based
simulation** (no optimizer — the in-domain optimization↔simulation fork).

### Economics — equilibrium & macro
[CGE](../model-families/economics/cge.md) ⭐ (MCP market clearing, SAM-calibrated; prices/policy
→ sectoral output, welfare), [DSGE](../model-families/economics/dsge.md) ⭐ (optimizing agents,
Bayesian-estimated), [Input–Output](../model-families/economics/input-output.md) (linear
Leontief), [GTAP](../model-families/economics/gtap.md) (global trade CGE),
[GEM-E3](../model-families/economics/gem-e3.md)/[ENVISAGE](../model-families/economics/envisage.md)
(energy-economy CGE), [E3ME](../model-families/economics/e3me.md) (**macro-econometric,
disequilibrium, demand-led** — the anti-CGE voice).

### Transport · Health · Agriculture · Water · Urban · Frameworks
- **Transport:** [MATSim](../model-families/transport/matsim.md) ⭐ (co-evolutionary user
  equilibrium), [SUMO](../model-families/transport/sumo.md) (micro vehicle physics + TraCI
  control API), [TRANSIMS](../model-families/transport/transims.md), [ActivitySim](../model-families/transport/activitysim.md) (nested-logit demand).
- **Health:** [Covasim](../model-families/health/covasim.md) ⭐ (individual ABM),
  [GLEAM](../model-families/health/gleam.md) (metapopulation + mobility),
  [OpenABM](../model-families/health/openabm.md) (contact networks + tracing).
- **Agriculture/Land:** [GLOBIOM](../model-families/agriculture/globiom.md) ⭐ (spatial partial-eq),
  [MAgPIE](../model-families/agriculture/magpie.md) (land cost-min, REMIND-coupled),
  [DSSAT](../model-families/agriculture/dssat.md)/[EPIC](../model-families/agriculture/epic.md)
  (field-scale crop/biophysics — the "yield engine" economic land models consume).
- **Water:** [SWAT](../model-families/water/swat.md) (watershed process),
  [MODFLOW](../model-families/water/modflow.md) (groundwater PDE),
  [WEAP](../model-families/water/weap.md) (allocation LP + scenarios).
- **Urban:** [UrbanSim](../model-families/urban/urbansim.md) (LUTI microsim + real-estate market),
  [SILO](../model-families/urban/silo.md) (coupling-first LUTI), [CityScope](../model-families/urban/cityscope.md) (participatory).
- **Frameworks (host environments, not domain models):** [Mesa](../model-families/frameworks/mesa.md),
  [Repast](../model-families/frameworks/repast.md), [NetLogo](../model-families/frameworks/netlogo.md),
  [GAMA](../model-families/frameworks/gama.md) (ABM); [Vensim](../model-families/frameworks/vensim.md) ⭐,
  [Stella](../model-families/frameworks/stella.md) (system dynamics); [AnyLogic](../model-families/frameworks/anylogic.md)
  (**multi-method SD+ABM+DES — the closest existing thing to Polyphony's runtime, and a
  template for it**).

⭐ = Gold dossier (deepest, best-audited — natural first adapters).

---

## 2. Dials — contested assumptions as switchable parameters

From the [comparative matrices](../comparative/index.md). Each becomes a **first-class config
dial** in Polyphony; where a question sits near an axis boundary we **run both settings and
report the disagreement**.

| Dial | Poles | Matrix |
|------|-------|--------|
| Decision principle | optimization ↔ simulation/emergence | [opt-vs-sim](../comparative/optimization-vs-simulation.md) |
| Resolution direction | top-down ↔ bottom-up | [td-vs-bu](../comparative/top-down-vs-bottom-up.md) |
| Market closure | equilibrium ↔ disequilibrium (demand-led) | [eq-vs-diseq](../comparative/equilibrium-vs-disequilibrium.md) |
| Micro structure | agent-based ↔ aggregate/CGE | [abm-vs-cge](../comparative/abm-vs-cge.md) |
| Dynamics style | individual interaction ↔ stock-flow feedback | [sd-vs-abm](../comparative/system-dynamics-vs-abm.md) |
| Foresight | perfect foresight ↔ recursive/myopic | [recursive-vs-pf](../comparative/recursive-vs-perfect-foresight.md) |
| Uncertainty | deterministic ↔ stochastic (distributions) | [det-vs-stoch](../comparative/deterministic-vs-stochastic.md) |
| State type | continuous fields ↔ discrete agents/events | [cont-vs-disc](../comparative/continuous-vs-discrete.md) |
| Scale coupling | IAM (reduced) ↔ bottom-up energy detail | [iam-vs-energy](../comparative/iam-vs-energy.md) |
| Integrality | LP (convex) ↔ MILP (integer) | [lp-vs-milp](../comparative/lp-vs-milp.md) |
| **Values (added)** | efficiency ↔ equity/altruism weighting; discount rate; risk aversion | *welfare dial (Polyphony)* |

The **values dial** is Polyphony's own first-class addition (per the north star): welfare
objective, distributional weights, discount rate, and tail-risk aversion are **inspectable**,
producing Pareto frontiers and value-of-information rather than one buried constant.

---

## 3. The 16 engines as component blueprints

The [architecture patterns](../patterns/index.md) are Polyphony's **implementation units** —
reusable engines instantiated as coupled code. Grouped by role:

- **Solve/decide:** [Optimization](../patterns/optimization-engine.md),
  [Market](../patterns/market-engine.md), [Energy-Dispatch](../patterns/energy-dispatch-engine.md),
  [Behavior](../patterns/behavior-engine.md), [Technology-Adoption](../patterns/technology-adoption-engine.md).
- **Evolve state:** [Integration/Stock-Flow](../patterns/integration-engine.md),
  [Climate](../patterns/climate-engine.md), [Land](../patterns/land-engine.md),
  [Spatial](../patterns/spatial-engine.md).
- **Learn/quantify:** [Calibration](../patterns/calibration-engine.md),
  [Sensitivity](../patterns/sensitivity-engine.md), [Scenario](../patterns/scenario-engine.md).
- **Govern/represent:** [Policy](../patterns/policy-engine.md), [Validation](../patterns/validation-engine.md),
  [Visualization](../patterns/visualization-engine.md), [Data-Pipeline](../patterns/data-pipeline.md).

**Polyphony's runtime = a composition of these engines under one clock** (the
[AnyLogic](../model-families/frameworks/anylogic.md) multi-method lesson) on the **Digital-Twin
backbone** (model ⇄ [assimilation](../patterns/calibration-engine.md) ⇄
[control/policy](../patterns/policy-engine.md)), with [Validation](../patterns/validation-engine.md)
and a tournament wrapped around everything.

---

## 4. Couplings the knowledge graph already implies

The graph's `alternative_to`, `contrasts_with`, and shared-`exhibits_pattern` edges point to
where models **compete on the same question** (→ run-both-report-disagreement) and where they
**hand off state** (→ candidate synergy couplings):

**Rival voices on one question (report disagreement):**
- Climate/economy welfare: DICE ↔ FUND ↔ PAGE (cost-benefit trio) ↔ REMIND/WITCH.
- Economy-wide policy: CGE/GTAP (equilibrium) ↔ **E3ME** (disequilibrium) — sign of the
  double-dividend flips; a canonical disagreement to surface.
- Energy transition: OSeMOSYS/TIMES/PyPSA (optimize) ↔ EnergyPLAN (simulate).
- Land use: GLOBIOM (surplus-max) ↔ MAgPIE (cost-min).
- Epidemic resolution: Covasim/OpenABM (individual) ↔ GLEAM (metapopulation) ↔ SD (aggregate).

**State hand-offs (candidate couplings):**
- energy-system cost/mix → IAM emissions → climate T → damages → energy demand (the IAM loop,
  but with *swappable* energy and climate voices).
- crop biophysics (DSSAT/EPIC) → land economics (GLOBIOM/MAgPIE) → LUC emissions → climate.
- land/climate → water (SWAT/MODFLOW/WEAP) availability → agriculture & energy (cooling/hydro).
- transport demand (ActivitySim) ↔ land use (UrbanSim/SILO) ↔ energy & emissions.
- macro output (CGE/E3ME) ↔ energy demand ↔ health (air quality, heat) → labor/productivity.

---

## 5. Candidate synergy loops to test (Phase 3+)

Each is a **falsifiable** bet: coupled must beat sum-of-parts on real data.

1. **Energy⇄Economy⇄Climate** (the classic IAM loop, made paradigm-plural): does swapping the
   energy voice (LP vs simulation) or the macro voice (CGE vs E3ME) change which policy wins?
2. **Land⇄Climate⇄Water⇄Food**: biophysical yields + LUC emissions + water constraints — do
   coupled crop/land/water models predict food-price or emissions shocks better than isolated?
3. **Urban⇄Transport⇄Energy⇄Health**: accessibility ↔ location ↔ travel ↔ emissions ↔ air-quality
   mortality — a metro-scale loop with hard historical data (mode shares, AQ, health).
4. **Macro⇄Health** (pandemic economics): epidemic ABM ⇄ demand/labor shock ⇄ policy response —
   backtestable against 2020–2022.

---

## 6. Gaps & candidate new factors (open as issues)

Grounded extensions the atlas doesn't yet cover but Polyphony likely needs (each needs a cited
reason + a test before adoption; feeds back as a new dossier/engine + graph nodes):

- **Distributional/equity accounting** as an engine (income deciles, incidence) — atlas has it
  only inside ENVISAGE/E3ME; Polyphony needs a **cross-model welfare/equity engine** (the values
  dial's home).
- **Data-assimilation engine** (Kalman/EnKF/particle/4D-Var) — named in the digital-twin page
  but not yet an engine pattern; **required** for the model⇄data backbone. → propose new engine.
- **Surrogate/emulator engine** (Gaussian-process / neural) — for latency and uncertainty
  propagation across the ensemble; not yet a pattern. → propose new engine.
- **Ensemble/meta engine** — Bayesian model averaging **vs** deliberate disagreement-preservation
  (we lean to the latter; BMA is a rival to beat). → propose new engine + ADR.
- **Causal-inference layer** — for identifying which couplings are genuinely causal vs spurious
  fit (guards the synergy test against leakage). → method page.
- **Finance/debt, migration, biodiversity, informality** — domains absent from the atlas that
  policy questions touch; add only when a question and data demand them.

---

## 7. What Phase 1 must produce (hand-off)

- A **common model interface** (`state`, `step`, `params/dials`, `provenance`) that DICE, an
  energy model, and a CGE can all implement.
- A **coupling/orchestration** design: paradigm **routing**, **run-both-report-disagreement**,
  Bayesian **uncertainty propagation**, and the **welfare/equity multi-objective dial**.
- The **tournament + adversarial + synergy-measurement protocol** (how a feature/coupling/model
  *wins*, how the red team attacks, how synergy is measured vs sum-of-parts).
- A **new-engines decision**: data-assimilation, surrogate, ensemble/meta, welfare/equity —
  each via ADR, each fed back to the atlas.

> **First vertical slice (Phase 2 target):** DICE ⇄ a bottom-up energy model
> (OSeMOSYS/MESSAGEix) ⇄ a CGE — three families, three paradigms, one shared
> energy⇄economy⇄climate loop with a real historical backtest window.
