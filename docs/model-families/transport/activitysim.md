# ActivitySim

!!! info "Bronze dossier"
    ActivitySim is the **demand-side** flagship of modern transport modeling: a consortium-maintained,
    open **activity-based travel-demand model** that predicts *who* travels *where, when, and how*
    through a coordinated pipeline of **discrete-choice (logit) submodels** applied to a **synthetic
    population**. It is the statistical-behavioral complement to the physical simulators
    [MATSim](matsim.md)/[SUMO](sumo.md), and the modern heir to [TRANSIMS](transims.md)'s activity
    generator.

> An open, consortium-maintained activity-based travel-demand model: a coordinated system of
> discrete-choice submodels predicting who travels where, when and how, over a synthetic population.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | ActivitySim |
|------|------|
| Optimization vs Simulation | **Simulation** (microsimulation of choices) |
| Top-down vs Bottom-up | **Bottom-up** (households/persons) |
| Equilibrium | N/A on its own (paired with network assignment) |
| Foresight | Myopic (nested choices) |
| Deterministic vs Stochastic | **Stochastic** (Monte-Carlo choice) |
| Time / Space | Daily (tour/trip) / zone system |
| Solution method | **Nested-logit discrete-choice pipeline** |

| Field | Value |
|-------|-------|
| Full name | ActivitySim |
| Domain | Transportation |
| First release / current | 2010s / ongoing |
| Institution · lead | ActivitySim consortium (US MPOs / agencies) |
| Language · solver | Python (pandas / numpy) |
| License / access | Open (BSD-3) |

---

## 🎓 Scholar Track

**History & motivation.** ActivitySim was created in the 2010s as a **consortium** of US
**Metropolitan Planning Organizations (MPOs)** and transport agencies (SFCTA, MTC, PSRC, ARC, and
others) to pool resources behind a **shared, open, professionally-maintained** activity-based model —
ending the era where each agency paid consultants for a bespoke, closed ABM. Its purpose is
**regional travel-demand forecasting** for planning and policy (transit investments, pricing, land-use
scenarios), grounded in the **activity-based** paradigm: travel is *derived demand* from people's need
to pursue activities, so model the **daily activity–travel pattern**, not just trips.

**Mathematical formulation.** ActivitySim implements a **coordinated sequence of discrete-choice
submodels** over a **synthetic population**. The workhorse is the **(nested) multinomial logit**: for
a decision-maker choosing among alternatives $j$ with systematic utility $V_j$, the choice
probability is

$$P_j = \frac{e^{V_j/\mu}}{\sum_{k} e^{V_k/\mu}},\qquad
V_j = \beta' x_j \; (+\text{ logsum from lower nests}),$$

where **nesting** and the **inclusive-value (logsum)** carry information up from finer choices (mode,
destination) to coarser ones (tour frequency), consistent with random-utility theory. The pipeline
chains dozens of such models: long-term (work/school location, auto ownership) → coordinated daily
activity pattern → tour generation → tour destination, time-of-day, and mode → intermediate stops →
trip mode. Each person's choices are realized by **Monte-Carlo draws**, producing a fully
**disaggregate list of tours and trips**. The output demand is then **assigned** to the network by a
separate static or dynamic assignment step (or handed to MATSim/DTA), where congestion feedback closes
the loop.

**Solution algorithm.** A **vectorized simulation pipeline**: each submodel evaluates utilities for
the whole population as **pandas/numpy** array operations, then samples choices; models run in
dependency order, passing logsums downstream. Congestion consistency is achieved by **outer-loop
feedback** with network skims (travel-time matrices) until stable. Engineered for **memory-efficient**
runs on populations of millions (chunking, sharded skims).

**Calibration & validation.** Submodel coefficients are **estimated econometrically** from household
travel surveys (and transferred/asserted where data is thin), then the assembled model is
**calibrated** to match observed mode shares, trip-length distributions, and counts; validated against
survey targets and traffic/transit observations.

**Strengths / weaknesses / criticisms.** *Strengths:* **open, shared, maintained** by the agencies
that use it; rigorous **random-utility** behavioral foundation; disaggregate and policy-sensitive
(pricing, demographics, accessibility); fast vectorized Python. *Criticisms:* it is a **demand**
model — network dynamics/equilibrium come from a separate assignment; myopic within-day; heavy
**data/estimation** requirements; logit's IIA/behavioral assumptions; calibration effort is
substantial.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** built from
**nested-logit choice** submodels — the demand-side cousin of the
**[Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)** (both are logit share
models) — orchestrated as a **[Data Pipeline](../../patterns/data-pipeline.md)** over a **synthetic
population**, with a **[Calibration Engine](../../patterns/calibration-engine.md)** for estimation/
adjustment. Its distinctive engineering is **vectorized microsimulation**: population-wide choices as
DataFrame operations rather than per-agent loops.

**Data & complexity.** Inputs: synthetic population, zone system, network **skims** (level-of-service
matrices), estimated coefficients. Scales to metro populations via **chunking** and shared-memory
skims; runtime dominated by utility evaluation and skim I/O.

**Openness / extensibility.** **BSD-3 open source**, Python, with a **declarative configuration**
(CSV/YAML spec files define utilities and nesting) so agencies customize models **without editing
code** — echoing [Calliope](../energy/calliope.md)'s model-as-data ethos. Active consortium
governance and shared examples.

## 🏛️ Architect Track

**Reusable patterns.** Transferable ideas: **consortium-maintained open infrastructure** (agencies
co-funding one shared model — the [GTAP](../economics/gtap.md)-style community-good lesson in a new
domain), **declarative discrete-choice specification** (utilities/nesting in config), and
**vectorized microsimulation** of a synthetic population. Also the clean **demand ↔ assignment**
separation of concerns.

**Trade-offs & alternatives.** ActivitySim is the **statistical-behavioral demand** pole; pair it with
network **assignment** (static, DTA, or [MATSim](matsim.md)) for a full loop. Versus MATSim: MATSim
reaches behavior *and* network equilibrium via **utility-scored day-plan co-evolution** in one engine;
ActivitySim reaches demand via **estimated choice models** then assigns separately — the
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) and
[Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md) contrasts. It is the
**estimated** modern successor to [TRANSIMS](transims.md)'s activity generator, and the demand-side
complement to microscopic [SUMO](sumo.md). Peers: CT-RAMP, DaySim, POLARIS.

**Adoption.** Widely adopted by US **MPOs** (SFCTA, MTC, PSRC, ARC, SANDAG, and more) for regional
planning; a growing international user base; increasingly the **default open ABM**.

**Ecosystem.** ActivitySim consortium; PopulationSim (synthetic population), network skims from
assignment models; interoperates with MATSim/DTA; peers CT-RAMP, DaySim, POLARIS.

**Research gaps.** Tighter demand–supply equilibrium; joint/intra-household and dynamic within-day
choice; reducing calibration burden; transferability of estimated coefficients across regions.

!!! quote "Lesson for the integrated simulator"
    ActivitySim delivers three lessons at once. First, **random-utility discrete choice** is a
    portable behavioral kernel — the *same* nested-logit math drives travel mode here and technology
    adoption in [GCAM](../climate-iam/gcam.md)/energy models, so the integrated simulator should carry
    a **shared logit/choice engine** reused across domains. Second, **consortium-maintained open
    infrastructure** is how a demanding model stays alive and comparable — the agencies that use it
    build it together, the same community-good pattern GTAP proved in economics. Third, ActivitySim's
    **declarative choice specification** and **vectorized microsimulation** show how to make
    disaggregate, million-agent behavior both *configurable* and *fast*. Its clean **demand ↔
    assignment** split is also a model for how the simulator should let behavioral and physical layers
    be developed and swapped independently, then coupled through feedback.

## Major publications

- ActivitySim Consortium (2016–). *ActivitySim: An Open Platform for Activity-Based Travel Modeling.*
  Documentation & technical specifications.
- Ben-Akiva, M., Lerman, S. (1985). *Discrete Choice Analysis.* MIT Press (the random-utility
  foundation).
- Bradley, M., Bowman, J., Griesenbeck, B. (2010). "SACSIM activity-based model" (methodological
  lineage of ActivitySim submodels). *Journal of Choice Modelling* 3(1).

## See also
- Contrast: [MATSim](matsim.md) · [SUMO](sumo.md) · Successor to: [TRANSIMS](transims.md) · [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Calibration Engine](../../patterns/calibration-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
