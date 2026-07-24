# SILO — Simple Integrated Land-Use Orchestrator

!!! info "Bronze dossier"
    SILO is the **coupling-first** land-use microsimulation — designed from the start to **plug cleanly
    into a travel-demand model** (especially [MATSim](../transport/matsim.md)) rather than to be a
    self-contained megamodel. It shares [UrbanSim](urbansim.md)'s discrete-choice, agent-level land-use
    approach but makes **modularity and integration** its organizing principle, embodying the atlas's
    thesis that a city is best modeled as **coupled engines**, not one monolith.

> An open land-use microsimulation designed to couple cleanly with travel-demand models (e.g. MATSim),
> simulating household relocation, real-estate and demographic evolution.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | SILO |
|------|------|
| Optimization vs Simulation | **Simulation** (microsimulation) |
| Top-down vs Bottom-up | **Bottom-up** (households / dwellings) |
| Equilibrium | Housing-market clearing (recursive) |
| Foresight | Recursive (annual) |
| Deterministic vs Stochastic | **Stochastic** (Monte-Carlo choice) |
| Time / Space | Annual / zone (dwelling-level) |
| Solution method | **Discrete-choice microsimulation** |

| Field | Value |
|-------|-------|
| Full name | SILO — Simple Integrated Land-Use Orchestrator |
| Domain | Urban |
| First release / current | 2010s / ongoing |
| Institution · lead | Rolf Moeckel et al. (TU Munich and collaborators) |
| Language · solver | Java |
| License / access | Open source |

---

## 🎓 Scholar Track

**History & motivation.** SILO was developed by **Rolf Moeckel** and collaborators (Maryland, then
**TU Munich**) in the 2010s with a deliberately **pragmatic** design goal encoded in its name — *Simple
Integrated Land-Use Orchestrator*. Reacting to the data- and effort-heaviness of comprehensive LUTI
platforms like [UrbanSim](urbansim.md), SILO aims to capture the **essential** land-use dynamics
(where households live, how the housing stock and population evolve) at a level of complexity that is
**maintainable and easy to couple** with transport and other models — integration over completeness.

**Mathematical formulation.** SILO is a **recursive-dynamic microsimulation** of a synthetic population
of **households, persons, dwellings, and jobs** over annual steps. Core processes are **discrete-choice
(logit) models** plus demographic transitions: **household relocation** (a residential-location choice
by multinomial logit over dwellings/zones, valuing price, dwelling attributes, and **accessibility**
imported from the coupled travel model), **real-estate / housing-market** dynamics (dwelling
construction, pricing, vacancy — a recursive market clearing), and **demographic evolution** (birth,
death, ageing, household formation/dissolution, employment change) via transition-rate models. Each
year, transitions and choices are realized by **Monte-Carlo** draws; the updated population and land use
feed a **travel model** (MATSim or a demand model), whose **accessibility** outputs re-enter next year's
location utilities — the **land-use ↔ transport feedback**. No global objective; patterns emerge.

**Solution algorithm.** An **annual loop**: apply demographic transitions, run relocation/real-estate
choice models (Monte-Carlo), clear the housing market, then exchange with the transport model
(accessibility ↔ land use); repeat to horizon. Java implementation; kept lean for tractability and
coupling.

**Calibration & validation.** Choice and transition parameters estimated/borrowed from household and
census data; validated against observed population distributions and coupled-model consistency. Used in
integrated **SILO-MATSim** applications (Munich, Maryland).

**Strengths / weaknesses / criticisms.** *Strengths:* **clean modular coupling** (esp. to MATSim),
**open**, lighter data/effort burden than full UrbanSim, transparent. *Criticisms:* deliberately
**simpler** (less real-estate/firm detail than UrbanSim); recursive myopia; logit assumptions; still
needs meaningful demographic and housing data.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** of logit choice
+ demographic transition models over a synthetic population, a recursive **[Market Engine](../../patterns/market-engine.md)**
(housing), orchestrated as a **[Data Pipeline](../../patterns/data-pipeline.md)** and, above all,
built for **inter-model coupling** — its defining engineering feature is a clean interface to
**[MATSim](../transport/matsim.md)** (accessibility exchange). Java; modular by design.

**Data & complexity.** Zone/dwelling-level annual microsimulation; lighter than parcel-level UrbanSim,
which is the point — tractable coupling for whole metros. Effort concentrates on demographic and housing
inputs.

**Openness / extensibility.** **Open source** (GitHub), Java; explicitly extensible and **coupling-
oriented** (SILO + MATSim + optionally emissions/health modules); used in academic integrated-modeling
studies.

## 🏛️ Architect Track

**Reusable patterns.** SILO's contribution is **integration as a first-class design goal**: keep each
model (land use, transport, demographics) **simple and modular**, and invest in **clean coupling
interfaces** so they compose — the "**orchestrator**" philosophy. Also reusable: **demographic
transition microsimulation** as the population's evolution engine beneath location choice.

**Trade-offs & alternatives.** SILO vs [UrbanSim](urbansim.md): same LUTI-microsimulation family and
discrete-choice core, but SILO trades **UrbanSim's parcel-level real-estate depth** for **simplicity and
ease of coupling** — a classic completeness-vs-maintainability choice. It pairs naturally with
[MATSim](../transport/matsim.md) (both open, agent-based, ETH/TUM-adjacent), the way UrbanSim pairs with
[ActivitySim](../transport/activitysim.md). The more **interactive/participatory** urban tool is
[CityScope](cityscope.md). Its recursive discrete-choice stance sits with UrbanSim on the
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) axis.

**Adoption.** Academic and applied **integrated land-use/transport** studies (Munich, Maryland, and
others); a favored **open** LUTI model in the MATSim ecosystem.

**Ecosystem.** TU Munich (MSM chair) and collaborators; tight **MATSim** coupling; peers UrbanSim, PECAS,
ILUTE, CityScope; often combined with emissions/health post-processors.

**Research gaps.** Balancing simplicity with needed detail; land-use–transport equilibrium; firm/
non-residential modeling; transferability.

!!! quote "Lesson for the integrated simulator"
    SILO makes the **coupling thesis** explicit in its very name — *orchestrator*. Rather than one
    all-encompassing city model, it keeps land use, demographics, and transport as **simple, modular
    components** and treats the **interface between them** as the primary engineering artifact — so a
    land-use model and a travel model ([MATSim](../transport/matsim.md)) exchange accessibility and
    location each year and co-evolve. For the integrated simulator this is a direct endorsement of a
    **microkernel-of-engines** architecture: prefer several well-coupled simple models over one complex
    monolith, and make **coupling interfaces and orchestration** (the accessibility ↔ land-use handshake)
    a first-class part of the design. SILO is the pragmatic counterpoint to comprehensive platforms — a
    reminder that **maintainability and integration** are themselves modeling virtues.

## Major publications

- Moeckel, R. (2017). "Constraints in household relocation: Modeling land-use/transport interactions
  that respect time and monetary budgets." *Journal of Transport and Land Use* 10(1).
- Moeckel, R., et al. (2020). "The integrated land use / transport model SILO-MATSim." (SILO
  documentation and application reports, TU Munich).
- Nguyen, T., Moeckel, R., et al. (2023). SILO model documentation, MSM chair, TU Munich.

## See also
- Urban peers: [UrbanSim](urbansim.md) · [CityScope](cityscope.md) · Couples with: [MATSim](../transport/matsim.md)
- Contrasts: [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) · shared kernel: [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Market Engine](../../patterns/market-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
