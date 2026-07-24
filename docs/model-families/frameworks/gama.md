# GAMA — GIS Agent-based Modeling Architecture

!!! info "Bronze dossier"
    GAMA is the **GIS-first** ABM platform: agents live in **real geographic space** — shapefiles,
    OSM, rasters, road networks — as naturally as [NetLogo](netlogo.md)'s turtles live on a patch
    grid. With its own **GAML** modeling language and strong support for **large, spatially explicit**
    simulations (cities, epidemics, floods, land use), GAMA is what you choose when **geography is
    the substrate**, not an afterthought.

> A powerful open ABM platform with first-class GIS support and its own GAML language, aimed at
> spatially explicit simulations at large scale (cities, epidemics, environment).

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | GAMA |
|------|------|
| Optimization vs Simulation | **Simulation** (ABM + GIS) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A (model-defined) |
| Foresight | Model-defined |
| Deterministic vs Stochastic | Model-defined |
| Time / Space | Model-defined / **real GIS space** (vector + raster) |
| Solution method | **Agent scheduler over GIS space** |

| Field | Value |
|-------|-------|
| Full name | GAMA — GIS Agent-based Modeling Architecture |
| Domain | Frameworks & Environments |
| First release / current | 2007 / ongoing (GAMA 1.9+) |
| Institution · lead | IRD / UMMISCO (France & international partners) |
| Language · solver | **GAML** (Java-based platform) |
| License / access | Open (GPL) |

---

## 🎓 Scholar Track

**History & motivation.** GAMA emerged around **2007** from **UMMISCO / IRD** (a Franco-Vietnamese and
international research network) to serve modelers whose problems are **inherently geographic** —
urban dynamics, disease spread on real terrain, water and land management in specific landscapes.
Existing frameworks treated space as an abstract grid; GAMA's founding bet was to make **real GIS data
a first-class citizen** of the modeling language, so agents can *be* buildings, parcels, road segments,
or river reaches with authentic geometry and topology.

**Mathematical formulation.** GAMA fixes **no domain math**; its distinctive content is a
**geographically-grounded agent ontology** expressed in **GAML** (GAml Modeling Language). A
**`species`** defines a class of agents; agents have **geometries** (point/line/polygon) drawn directly
from **GIS layers** (shapefiles, OSM, GeoJSON, rasters). Space is a real **topology**: agents query
spatial relations (distance, intersection, neighbors, shortest path on a road **graph**) natively, and
raster **`grid`** species coexist with vector agents. Time advances in scheduled **cycles**; behaviors
are written as **`reflex`** blocks (fire each step) and rule-based actions. GAML also includes
**declarative experiments** (batch, exploration, optimization via built-in methods like genetic
algorithms) and rich **3D/2D visualization**. The "solution" is the scheduled advance of a
spatially-embedded agent population over authentic geography.

**Solution algorithm.** Each cycle, the scheduler runs agents' `reflex` behaviors over the GIS space,
resolving spatial queries against optimized spatial indexes; batch/exploration experiments repeat runs
across parameters (including built-in **calibration/optimization** algorithms). Handles **large**
agent populations with GIS topology efficiently via spatial data structures.

**Calibration & validation.** GAML's **experiment** layer provides batch runs, sensitivity, and
**built-in optimization** (e.g. GA, hill-climbing) for calibration; models are validated against
spatial data (observed land-use change, epidemic maps, traffic). Its GIS grounding makes
**spatially-explicit validation** natural.

**Strengths / weaknesses / criticisms.** *Strengths:* **best-in-class GIS integration**, expressive
GAML, scalable spatial simulation, strong 2D/3D viz, built-in exploration/optimization. *Criticisms:*
learning a **domain-specific language** (GAML) is a barrier; heavier than NetLogo for simple models;
smaller community than NetLogo/Mesa; JVM performance ceiling for extreme scales (vs [Repast](repast.md)
HPC).

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** (species/reflex)
over a genuinely **geographic [Spatial Engine](../../patterns/spatial-engine.md)** — the atlas's clearest
example of a **GIS-native** spatial layer (vector + raster + network topology) — driven by a cycle
**[Integration Engine](../../patterns/integration-engine.md)**, with built-in
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)**/optimization experiments and a strong
**[Visualization Engine](../../patterns/visualization-engine.md)** (2D/3D). Its data ingestion is a
**[Data Pipeline](../../patterns/data-pipeline.md)** for real geospatial formats.

**Data & complexity.** Ingests shapefiles/OSM/rasters directly; spatial indexing keeps queries fast at
scale; comfortably runs **city-scale** spatially explicit models. GAML raises abstraction (less
boilerplate than Java frameworks).

**Openness / extensibility.** **GPL open source**, cross-platform (Eclipse-based IDE + headless);
extensible via plugins (comodeling, statistics, DB, and even coupling to external models); active
academic community, especially in Europe/Asia.

## 🏛️ Architect Track

**Reusable patterns.** GAMA's headline contribution is a **GIS-native spatial engine**: making **real
geographic topology** (geometry, adjacency, networks, rasters) a first-class part of the modeling
language, so "where" is authentic rather than stylized. Also reusable: a **high-level declarative
modeling DSL** (GAML) that folds behavior, space, experiments, and visualization into one language, and
**built-in optimization/calibration** as language constructs.

**Trade-offs & alternatives.** Framework niche map: GAMA = **GIS/spatial**, [NetLogo](netlogo.md) =
**pedagogy**, [Mesa](mesa.md) = **Python ecosystem**, [Repast](repast.md) = **HPC/scale**. GAMA
overlaps Repast's GIS projection and NetLogo's GIS extension but goes further by making geography
**central to the language**. It is the framework of choice when a model's questions are **place-specific**
(this city, this watershed). Like its peers it is a simulation-paradigm environment, contrasted with the
SD environment [Vensim](vensim.md); its GIS focus echoes the domain models GLOBIOM/MATSim that also live
in real space.

**Adoption.** Strong in **urban, environmental, epidemiological, and disaster** modeling, especially in
European and Asian research (participatory "companion modeling"); used for COVID-19 spatial models,
flood/evacuation, land-use and water management.

**Ecosystem.** IRD/UMMISCO and partners (GAMA platform, GAML); comodeling/participatory-modeling
tradition (Cormas lineage nearby); peers NetLogo, Repast, Mesa, AnyLogic; ingests standard GIS stacks.

**Research gaps.** Broadening the community beyond GAML's learning curve; extreme-scale/HPC and GPU;
tighter coupling to equation-based (SD/PDE) and economic models for true multi-paradigm studies.

!!! quote "Lesson for the integrated simulator"
    GAMA's lesson is that **geography deserves to be first-class**. Many policy questions —
    urban growth, epidemics, floods, land and water — are *irreducibly spatial*, and a simulator that
    treats space as an abstract grid loses the topology (real road networks, parcel adjacency, terrain)
    that drives the answer. GAMA shows how to make a **GIS-native spatial engine** — vector geometry,
    rasters, and network topology together — a core capability wielded through a **high-level modeling
    language**, and to fold **experiments, calibration/optimization, and 2D/3D visualization** into the
    same declarative layer. For the integrated simulator this argues that the shared **spatial substrate**
    should speak authentic geography (the same substrate PyPSA's network, GLOBIOM's Simulation Units, and
    MATSim's road graph all need), and that a **declarative modeling DSL** can lower the barrier to
    building spatially-explicit models without sacrificing rigor.

## Major publications

- Taillandier, P., Gaudou, B., Grignard, A., Drogoul, A., et al. (2019). "Building, composing and
  experimenting complex spatial models with the GAMA platform." *GeoInformatica* 23(2).
- Grignard, A., et al. (2013). "GAMA 1.6: Advancing the art of complex agent-based modeling and
  simulation." *PRIMA 2013*, Springer LNCS.
- Drogoul, A., et al. (2013). "GAMA: A spatially explicit, multi-level, agent-based modeling and
  simulation platform." *PAAMS 2013*.

## See also
- Peers: [NetLogo](netlogo.md) · [Mesa](mesa.md) · [Repast](repast.md) · Analogy: [Vensim](vensim.md) (SD environment)
- Spatial kin: [MATSim](../transport/matsim.md) · [GLOBIOM](../agriculture/globiom.md) · [PyPSA](../energy/pypsa.md)
- Patterns: [Spatial Engine](../../patterns/spatial-engine.md) · [Behavior Engine](../../patterns/behavior-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Visualization Engine](../../patterns/visualization-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
