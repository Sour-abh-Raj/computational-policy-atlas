# UrbanSim

!!! info "Bronze dossier"
    UrbanSim opens the atlas's **urban** domain — a microsimulation of how a metropolitan area evolves:
    households and firms **choosing where to locate**, developers **choosing what to build**, and a
    **real-estate market clearing** on price, all interacting with transportation accessibility over
    decades. It is the land-use half of the **integrated land-use/transport (LUTI)** modeling tradition,
    the long-horizon partner to travel-demand models like [ActivitySim](../transport/activitysim.md) and
    [MATSim](../transport/matsim.md).

> A microsimulation platform for urban land use, real estate and transportation interactions, driven by
> discrete-choice models of household and firm location over long horizons.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | UrbanSim |
|------|------|
| Optimization vs Simulation | **Simulation** (microsimulation) |
| Top-down vs Bottom-up | **Bottom-up** (agents / parcels) |
| Equilibrium | **Real-estate market clearing** (price adjustment) |
| Foresight | Recursive (annual) |
| Deterministic vs Stochastic | **Stochastic** (Monte-Carlo discrete choice) |
| Time / Space | Annual / **parcel or zone** |
| Solution method | **Discrete-choice location models + market clearing** |

| Field | Value |
|-------|-------|
| Full name | UrbanSim |
| Domain | Urban |
| First release / current | 1998 / ongoing (UDST: `urbansim`, `orca`, UrbanCanvas) |
| Institution · lead | Paul Waddell (UC Berkeley) / UrbanSim Inc. |
| Language · solver | Python (Urban Data Science Toolkit) |
| License / access | Open (BSD) + commercial services |

---

## 🎓 Scholar Track

**History & motivation.** UrbanSim was created by **Paul Waddell** in **1998** to replace the crude
aggregate land-use components of transportation planning with a **behaviorally-grounded microsimulation**.
US planning law (Clean Air Act, ISTEA) required regions to assess how transportation investments affect
land use, travel, and emissions — but the four-step models treated land use as fixed or aggregate.
UrbanSim's proposition: simulate the **individual decisions** — where a household lives, where a firm
locates, what a developer builds — as **discrete choices** responding to prices and **accessibility**,
so that land use and transportation **co-evolve** over long horizons.

**Mathematical formulation.** UrbanSim is a **recursive-dynamic microsimulation** over synthetic
**households, jobs/firms, buildings, and parcels/zones**. It is organized as a **system of discrete-
choice (logit) models** run annually:

- **Location choice** — households and firms choose locations by **multinomial/nested logit**,
  $P_i = \dfrac{e^{V_i}}{\sum_j e^{V_j}}$, with utility $V_i$ a function of price, characteristics, and
  **transportation accessibility** (logsums imported from a travel model);
- **Real-estate development** — developers choose whether/what to build via choice models;
- **Real-estate price/market clearing** — prices **adjust** to balance demand and supply of space by
  location (a market-clearing step, though recursive rather than a full general equilibrium);
- **Transition models** — demographic and economic evolution of the agent population.

Each year the models run in sequence, choices realized by **Monte-Carlo** draws, and the updated land
use feeds a **travel-demand model** (accessibility → next year's location utilities), closing the
**land-use ↔ transport feedback**. There is **no global objective**; the metropolitan pattern *emerges*
from many priced choices.

**Solution algorithm.** A **vectorized annual pipeline** (the **`orca`** orchestration + `urbansim`
choice models over **pandas** tables): estimate/apply each submodel, sample choices, clear prices,
advance a year, exchange accessibility with the travel model; repeat to horizon (often 2040–2050).
Built for metro populations of millions of agents/parcels.

**Calibration & validation.** Choice-model coefficients **estimated** from census, parcel, real-estate
transaction, and travel-survey data; the assembled model **calibrated** to observed development and
location patterns and **validated** by backcasting historical growth. Heavy data-integration
requirements (parcels, buildings, prices) are characteristic.

**Strengths / weaknesses / criticisms.** *Strengths:* **behavioral, disaggregate, parcel-level** land
use with a genuine **LUTI feedback**; open Python toolkit; policy-sensitive (zoning, transit,
pricing). *Criticisms:* **very data-hungry** and effort-intensive to set up; recursive myopia; logit/
IIA behavioral assumptions; real-estate "market clearing" is stylized; long calibration cycles.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** of nested-logit
choice models (the demand-side cousin of the [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)),
a stylized **[Market Engine](../../patterns/market-engine.md)** (real-estate price clearing), all
orchestrated as a **[Data Pipeline](../../patterns/data-pipeline.md)** over a synthetic population and
parcel geography (a **[Spatial Engine](../../patterns/spatial-engine.md)**), with a
**[Calibration Engine](../../patterns/calibration-engine.md)** for estimation. The **Urban Data Science
Toolkit (UDST)** — `orca` (task orchestration), `urbansim`, `pandana` (network accessibility) — is a
clean, reusable Python stack.

**Data & complexity.** Millions of agents/parcels × annual steps; vectorized pandas keeps it tractable.
The dominant cost is **data integration** (parcels, buildings, transactions, employment).

**Openness / extensibility.** **Open source (BSD)** UDST components plus commercial UrbanSim Inc.
services (UrbanCanvas); interoperates with travel models (ActivitySim, regional four-step, MATSim);
`pandana`/`orca` are reusable beyond UrbanSim.

## 🏛️ Architect Track

**Reusable patterns.** UrbanSim's transferable ideas: **coupled land-use/transport microsimulation**
(two feedback-linked models rather than one megamodel), **discrete choice as the universal behavioral
kernel** (location, development — the same logit math as travel mode and technology adoption), and a
**modular orchestration toolkit** (`orca`) that wires many submodels into a reproducible annual pipeline.

**Trade-offs & alternatives.** UrbanSim is the **land-use** engine of the LUTI pair; couple it with a
**transport** model — [ActivitySim](../transport/activitysim.md) (demand) or [MATSim](../transport/matsim.md)
(co-evolutionary) — for the full loop. Among urban models it is the **parcel-level microsimulation** pole;
peers include [SILO](silo.md) (a similar LUTI microsimulation) and the more **interactive/tangible**
[CityScope](cityscope.md). Its behavioral, disaggregate stance contrasts with aggregate spatial-interaction
land-use models. Discrete-choice + recursive dynamics place it near [GCAM](../climate-iam/gcam.md)/
recursive CGE on the [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)
axis.

**Adoption.** Used by **metropolitan planning organizations** and agencies (Bay Area/MTC, Puget Sound,
Paris, and others) for long-range land-use/transport/climate scenario planning; a leading open LUTI
platform.

**Ecosystem.** UDST (`urbansim`, `orca`, `pandana`, `synthpop`), UrbanSim Inc. (UrbanCanvas); couples to
ActivitySim/MATSim/travel models; peers SILO, CityScope, PECAS, ILUTE.

**Research gaps.** Lowering data/calibration burden; tighter land-use–transport equilibrium;
intra-household and developer behavior; uncertainty; transferability across regions.

!!! quote "Lesson for the integrated simulator"
    UrbanSim reinforces the atlas's **coupling thesis** in the urban arena: rather than one monolithic
    city model, it runs **two feedback-linked microsimulations** — land use and transport — exchanging
    **accessibility and location** each year, so cause and effect flow both ways over decades. For the
    integrated simulator this is a template for **inter-domain coupling by feedback** (the land-use ↔
    transport ↔ emissions loop), and yet another appearance of the **discrete-choice kernel** — the same
    nested-logit math drives household location here, travel mode in [ActivitySim](../transport/activitysim.md),
    and technology adoption in [GCAM](../climate-iam/gcam.md), arguing for **one shared choice engine**
    across domains. UrbanSim's **`orca` orchestration toolkit** — modular submodels wired into a
    reproducible pipeline over tidy tables — is also a concrete model for how the simulator should compose
    many engines without a monolith.

## Major publications

- Waddell, P. (2002). "UrbanSim: Modeling urban development for land use, transportation, and
  environmental planning." *Journal of the American Planning Association* 68(3).
- Waddell, P., et al. (2003). "Microsimulation of urban development and location choices: Design and
  implementation of UrbanSim." *Networks and Spatial Economics* 3.
- Waddell, P. (2011). "Integrated land use and transportation planning and modelling." *Transport
  Reviews* 31(2).

## See also
- Urban peers: [SILO](silo.md) · [CityScope](cityscope.md) · Couple with (transport): [ActivitySim](../transport/activitysim.md) · [MATSim](../transport/matsim.md)
- Contrasts: [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) · shared kernel: [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Market Engine](../../patterns/market-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Calibration Engine](../../patterns/calibration-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
