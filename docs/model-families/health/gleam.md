# GLEAM — GLobal Epidemic and Mobility model

!!! info "Bronze dossier"
    GLEAM is the **metapopulation** epidemic model — the mesoscale counterpart to individual-based
    [Covasim](covasim.md)/[OpenABM](openabm.md). Instead of simulating people, it partitions the
    world into thousands of **subpopulations** (grid cells around airports), runs **stochastic
    compartmental** disease dynamics inside each, and couples them with **real air-travel and
    commuting networks** — the design that produced some of the earliest quantitative forecasts of
    H1N1, Ebola, Zika, and COVID-19 global spread.

> A stochastic metapopulation epidemic model coupling disease dynamics with real air-travel and
> commuting mobility to forecast global spread of infectious diseases.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | GLEAM |
|------|------|
| Optimization vs Simulation | **Simulation** (metapopulation stochastic) |
| Top-down vs Bottom-up | **Meso** (subpopulations) |
| Equilibrium | N/A |
| Foresight | N/A |
| Deterministic vs Stochastic | **Stochastic** |
| Time / Space | Daily / global grid (~cells) + mobility network |
| Solution method | **Stochastic compartmental + mobility coupling** |

| Field | Value |
|-------|-------|
| Full name | GLEAM — GLobal Epidemic and Mobility model |
| Domain | Health / Epidemiology |
| First release / current | 2000s / ongoing |
| Institution · lead | MOBS Lab, Northeastern University (Alessandro Vespignani) |
| Language · solver | C++ / Python (GLEAMviz) |
| License / access | Tool freely available |

---

## 🎓 Scholar Track

**History & motivation.** GLEAM was developed by **Alessandro Vespignani's MOBS Lab** (Indiana, then
Northeastern) in the 2000s, out of the **statistical-physics / complex-networks** tradition applied
to epidemics. Its founding insight: for **global** epidemic spread, the dominant driver is **human
mobility** — who flies where — so a credible model must **fuse disease dynamics with real
transportation networks**. GLEAM gave early operational forecasts for the **2009 H1N1 pandemic**,
Ebola, Zika, MERS, and COVID-19.

**Mathematical formulation.** GLEAM is a **stochastic metapopulation (patch) model**. The globe is
divided into ~**tens of thousands of subpopulations** defined by a Voronoi tessellation around major
airports (a "geographic census × mobility" layer). Within each subpopulation $i$, disease spreads by
a **compartmental** model (e.g. SLIR/SEIR) but simulated **stochastically** — transitions are
**binomial/multinomial random draws** each day rather than deterministic ODE flows, so that **chance
extinction** and introduction timing (which matter enormously early in an outbreak) are captured. The
subpopulations are **coupled by mobility**: a long-range **air-travel network** (IATA flight data)
moves infected and susceptible individuals between patches stochastically, and a short-range
**commuting** layer couples neighbors. Formally the state is the vector of compartment counts per
patch; the update is *reaction* (within-patch stochastic epidemic) + *diffusion* (stochastic transport
on the networks) — a **stochastic reaction–diffusion** process on a metapopulation network. Ensembles
of many stochastic realizations produce **probabilistic** forecasts (median + confidence bands).

**Solution algorithm.** Discrete daily time step: (1) draw within-patch epidemic transitions
(binomial chain-binomial); (2) draw mobility fluxes moving individuals across the air/commute
networks; (3) advance. Run **thousands of stochastic realizations** and aggregate. Efficient because
patches (not individuals) are the unit — global runs are feasible on modest hardware.

**Calibration & validation.** Driven by **real data**: high-resolution population rasters, **IATA**
airline schedules, and census commuting flows; disease parameters ($R_0$, generation time) inferred
by fitting arrival times / case counts (often via likelihood over the observed international spread
pattern). Validated by predicting **outbreak arrival dates** in unaffected countries — a distinctive,
falsifiable check.

**Strengths / weaknesses / criticisms.** *Strengths:* **global reach** with real mobility;
computationally light relative to individual ABMs; **stochasticity** captures extinction/introduction;
strong operational track record. *Criticisms:* **mesoscale** homogeneity within a patch (no household/
contact structure like [Covasim](covasim.md)/[OpenABM](openabm.md)); depends on mobility-data quality;
coarse for fine within-city interventions.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** at
*subpopulation* granularity (stochastic compartmental kernel) over a **[Spatial Engine](../../patterns/spatial-engine.md)**
that is a **mobility network** (airports + commuting), stepped by a stochastic
**[Integration Engine](../../patterns/integration-engine.md)** and wrapped in an
**ensemble/[Scenario Engine](../../patterns/scenario-engine.md)** (many realizations, intervention
scenarios). Its signature is the **mobility-coupled metapopulation** — a
[Data Pipeline](../../patterns/data-pipeline.md) that fuses population rasters with IATA/commuting
flows into the patch network. Distributed via the **GLEAMviz** client.

**Data & complexity.** Tens of thousands of patches × daily steps × thousands of realizations —
cheap per patch, so global ensembles run fast. Data assembly (mobility + demography) is the heavy part.

**Openness / extensibility.** The **GLEAMviz tool is freely available** (GUI + engine), though the
full data/codebase is lab-maintained. Extensible to new pathogens/compartments and intervention
layers (travel restrictions, seasonality).

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is the **metapopulation (reaction–diffusion) architecture**:
choose **subpopulations as the unit** and couple them with a **real mobility network**, getting global
coverage at a fraction of an individual ABM's cost — plus **stochastic** dynamics so rare early events
are represented, and **ensembles** as the native output. This "patches + network" pattern generalizes
far beyond epidemics (regional trade, migration, invasive species).

**Trade-offs & alternatives.** GLEAM is the **mesoscale** point between aggregate compartmental ODEs
and full individual ABMs. Against [Covasim](covasim.md)/[OpenABM](openabm.md): GLEAM trades
within-population **contact structure** (households, ages, tracing) for **global mobility coverage and
speed** — the [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) and
[ABM vs CGE](../../comparative/abm-vs-cge.md) granularity discussions applied inside epidemiology. In
practice they are **complementary**: GLEAM for *where/when* a pathogen spreads globally, individual
ABMs for *which intervention* works locally. Peers: GLEaMviz, EpiRisk, Spatiotemporal Epidemic
Modeler (STEM), metapopulation models generally.

**Adoption.** Operational forecasts for **H1N1 (2009), Ebola, Zika, MERS, COVID-19**; used by public-
health agencies and cited in WHO-adjacent response planning; a flagship of network epidemiology.

**Ecosystem.** MOBS Lab (Northeastern); GLEAMviz client; IATA/population data; peers STEM, EpiRisk,
metapopulation frameworks; complements individual ABMs (Covasim, OpenABM).

**Research gaps.** Adding within-patch heterogeneity (age/contact) without losing scalability; real-
time mobility (mobile-phone data); coupling to behavioral response and to economic models.

!!! quote "Lesson for the integrated simulator"
    GLEAM teaches the **metapopulation** design: when the phenomenon is fundamentally about **flows
    between places**, the right unit may be **subpopulations coupled by a real mobility network**, not
    individuals — a **reaction–diffusion on a network** that buys global coverage cheaply and keeps the
    **stochasticity** that makes rare early events (a pathogen's first arrival) matter. For the
    integrated simulator this is a reminder that **granularity is a dial with a mesoscale setting**:
    between aggregate ODE (Vensim-style) and individual ABM (Covasim-style) sits the patch-and-network
    model, and the same **mobility/coupling substrate** (who moves between regions) is reusable across
    epidemics, migration, trade, and energy demand. It also models **ensemble forecasting** — many
    stochastic realizations reported as distributions — as the honest default the atlas keeps
    advocating.

## Major publications

- Balcan, D., Vespignani, A., et al. (2009). "Multiscale mobility networks and the spatial spreading
  of infectious diseases." *PNAS* 106(51).
- Van den Broeck, W., et al. (2011). "The GLEaMviz computational tool." *BMC Infectious Diseases* 11.
- Chinazzi, M., et al. (2020). "The effect of travel restrictions on the spread of COVID-19."
  *Science* 368(6489).

## See also
- Contrast: [Covasim](covasim.md) · [OpenABM](openabm.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) · [System Dynamics vs ABM](../../comparative/system-dynamics-vs-abm.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Scenario Engine](../../patterns/scenario-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
